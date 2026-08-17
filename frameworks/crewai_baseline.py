import sys
import os
import time
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


# ============================================================
# TOOLS
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


# ============================================================
# RUN TASK
# ============================================================

def run_task(task_path: str) -> dict:

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

        verbose=False,

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
    # Crew
    # --------------------------------------------------------

    crew = Crew(
        agents=[agent],
        tasks=[crew_task],
        verbose=False,
    )

    # --------------------------------------------------------
    # Execute
    # --------------------------------------------------------

    start = time.time()

    try:
        result = crew.kickoff()
        final_answer = str(result).strip()

    except Exception as e:
        final_answer = f"ERROR: {type(e).__name__}: {str(e)}"

    elapsed = time.time() - start

    return {
        "final_answer": final_answer,
        "time_taken": elapsed,
        "framework": "crewai",
    }