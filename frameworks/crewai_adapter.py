import os
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

import sys
import time
import threading
import json


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool

from tools.fake_tools import (
    fake_search,
    fake_file_reader,
    fake_calculator,
    fake_booking_api,
)

from arw import AdaptiveReliabilityWrapper, ARWConfig


# ============================================================
# TOOLS  (unchanged)
# ============================================================

@tool("fake_search")
def fake_search_tool(query: str) -> str:
    """Search the benchmark knowledge base. Always use this tool when the task asks for fake_search."""
    return fake_search(query)


@tool("fake_file_reader")
def fake_file_reader_tool(filename: str) -> str:
    """Read a file from the benchmark file database."""
    return fake_file_reader(filename)


@tool("fake_calculator")
def fake_calculator_tool(expression: str) -> str:
    """Calculate a mathematical expression using the benchmark calculator."""
    return fake_calculator(expression)


@tool("fake_booking_api")
def fake_booking_api_tool(flight_code: str) -> str:
    """Book a flight using the exact flight code returned by fake_search."""
    return fake_booking_api(flight_code)


TOOL_MAP = {
    "fake_search": fake_search_tool,
    "fake_file_reader": fake_file_reader_tool,
    "fake_calculator": fake_calculator_tool,
    "fake_booking_api": fake_booking_api_tool,
}

# ARW instance — shared config for every task in this framework.
# use_consistency defaults False here (see run_task below) because CrewAI
# is by far your slowest framework already; turn it on only if you want
# the "ARW-full" ablation run for the paper (see note at bottom of file).
ARW = AdaptiveReliabilityWrapper(config=ARWConfig(max_retries=3))


# ============================================================
# RUN TASK
# ============================================================

def run_task(task_path: str, use_consistency: bool = False) -> dict:

    with open(task_path, "r", encoding="utf-8") as f:
        task = json.load(f)

    available_tools = []

    for tool_name in task.get("tools", []):
        if tool_name in TOOL_MAP:
            available_tools.append(TOOL_MAP[tool_name])

    # --------------------------------------------------------
    # CrewAI-native Ollama configuration
    # --------------------------------------------------------

    llm = LLM(
        model="ollama/qwen2.5:7b",
        base_url="http://localhost:11434",
        temperature=0,
        timeout=60,
    )

    # --------------------------------------------------------
    # Strong tool-use instructions
    # --------------------------------------------------------

    agent = Agent(
        role="Deterministic Benchmark Executor",

        goal=(
            "Execute benchmark instructions exactly. "
            "Never invent tool results. "
            "Never skip a required tool. "
            "When the instruction specifies multiple tools, execute "
            "them in the specified order and use the output of earlier "
            "tools as input to later tools."
        ),

        backstory=(
            "You are a deterministic benchmark agent. "
            "You operate only with the tools provided to you. "
            "The benchmark requires reliable multi-tool execution. "
            "If the instruction says to search, you MUST call the search tool. "
            "If the instruction says to calculate, you MUST call the calculator. "
            "If the instruction says to book using a result from search, "
            "you MUST pass the exact returned identifier to the booking tool. "
            "Never replace a tool call with your own knowledge or guess."
        ),

        llm=llm,

        tools=available_tools,

        verbose=True,

        allow_delegation=False,

        # Enough iterations for search -> search -> calculator
        max_iter=15,

        # Prevent unnecessary delegation.
        max_retry_limit=2,
    )

    # --------------------------------------------------------
    # Explicit task-level instructions
    # --------------------------------------------------------

    task_description = f"""
You are executing benchmark task {task["id"]}.

Follow the instruction EXACTLY:

{task["instruction"]}

CRITICAL RULES:

1. Use ONLY the tools provided for this task.
2. If the instruction says "Use fake_search", actually call fake_search.
3. If multiple tools are required, execute them in the exact order requested.
4. Never invent, estimate, or substitute a tool result.
5. If a later tool needs information returned by an earlier tool,
   pass the exact relevant value from the earlier tool.
6. For booking tasks:
   - search first;
   - extract the exact flight code returned by fake_search;
   - pass that exact flight code to fake_booking_api;
   - return the booking API result.
7. For calculation tasks:
   - obtain the required values from the specified tools;
   - perform the requested calculation using fake_calculator;
   - return the calculator result.
8. Do not stop before all required tool calls have been completed.
9. Do not explain your reasoning.
10. Return ONLY the final answer requested by the user.
"""

    crew_task = Task(
        description=task_description,

        expected_output=(
            "The exact final answer requested by the benchmark instruction. "
            "No explanation, no reasoning, no additional commentary."
        ),

        agent=agent,
    )

    # --------------------------------------------------------
    # Execute — THIS is where the 10.3% None/empty crash happens.
    # ARW wraps it: retries on exception/empty, and if all retries are
    # exhausted, returns an [ARW_FALLBACK] string instead of raising.
    #
    # IMPORTANT: a fresh Crew/Agent/Task is built INSIDE execute(),
    # so every ARW retry gets its own independent objects. Reusing one
    # shared `crew` across retries caused two kickoff() calls to run
    # concurrently (the abandoned/timed-out one plus the new retry),
    # which corrupted CrewAI's internal event bus ("Event pairing
    # mismatch" / "Crew Execution Failed").
    #
    # The kickoff() call runs in a daemon thread with a hard timeout,
    # so a stuck call (e.g. a tool-call parse loop that never returns)
    # can't hang the batch AND can't block Python process exit even
    # after being abandoned. If it times out, we raise TimeoutError so
    # ARW.run() treats it like any other failure and retries/falls
    # back accordingly.
    # --------------------------------------------------------

    def _build_crew():
        fresh_agent = Agent(
            role=agent.role,
            goal=agent.goal,
            backstory=agent.backstory,
            llm=llm,
            tools=available_tools,
            verbose=True,
            allow_delegation=False,
            max_iter=15,
            max_retry_limit=2,
        )
        fresh_task = Task(
            description=task_description,
            expected_output=crew_task.expected_output,
            agent=fresh_agent,
        )
        return Crew(agents=[fresh_agent], tasks=[fresh_task], verbose=True)

    def execute():
        result_box = {}

        def _run():
            try:
                fresh_crew = _build_crew()
                result_box["value"] = str(fresh_crew.kickoff()).strip()
            except Exception as e:
                result_box["error"] = e

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        thread.join(timeout=90)

        if thread.is_alive():
            # Abandon it — daemon=True means it can't block process exit.
            raise TimeoutError(f"crew.kickoff() exceeded 90s for task {task['id']}")

        if "error" in result_box:
            raise result_box["error"]

        return result_box.get("value", "")

    start = time.time()
    log = ARW.run(execute, use_consistency=use_consistency, context=f"crewai_task_{task['id']}")
    elapsed = time.time() - start

    return {
        "final_answer": log.final_output,
        "time_taken": elapsed,
        "framework": "crewai",
        # extra ARW fields — safe to ignore in analyze_failures.py if you
        # don't need them yet; useful for the ARW-vs-baseline table.
        "arw_retries": log.retries_used,
        "arw_crashed_before_arw": log.crashed_before_arw,
        "arw_used_fallback": log.used_fallback,
        "arw_consistency_used": log.consistency_used,
        "arw_consistency_agreed": log.consistency_agreed,
    }

# NOTE on the two ablation runs for the paper:
#   1) ARW-retry-only  : run_task(path)                      (use_consistency=False, default)
#      -> targets the crash/empty failure modes specifically
#   2) ARW-full         : run_task(path, use_consistency=True)
#      -> also targets the wrong-answer bucket, but runs the crew up to
#         3x per task, so it's ~3x slower. Worth reporting both numbers
#         in the paper as an ablation, if your runner supports passing
#         this flag through.