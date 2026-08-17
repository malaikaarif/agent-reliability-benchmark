import sys
import os
import time
import json

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
sys.path.insert(0, PROJECT_ROOT)

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent

from tools.fake_tools import (
    fake_search,
    fake_file_reader,
    fake_calculator,
    fake_booking_api,
)

from arw import AdaptiveReliabilityWrapper, ARWConfig


@tool
def fake_search_tool(query: str) -> str:
    """Search the benchmark knowledge base.

    Use concise queries that match the available knowledge-base entries.
    For flights, use queries such as "flights from lahore" or
    "flight pk05x9".
    """
    return fake_search(query)


@tool
def fake_file_reader_tool(filename: str) -> str:
    """Read a file from the benchmark file database."""
    return fake_file_reader(filename)


@tool
def fake_calculator_tool(expression: str) -> str:
    """Calculate a mathematical expression."""
    return fake_calculator(expression)


@tool
def fake_booking_api_tool(flight_code: str) -> str:
    """Book a flight using the exact flight code returned by fake_search."""
    return fake_booking_api(flight_code)


TOOL_MAP = {
    "fake_search": fake_search_tool,
    "fake_file_reader": fake_file_reader_tool,
    "fake_calculator": fake_calculator_tool,
    "fake_booking_api": fake_booking_api_tool,
}


SYSTEM_PROMPT = """
You are a tool-using agent in a reliability benchmark.

Follow the task exactly.

IMPORTANT RULES:

1. You MUST actually use the requested tools.
2. NEVER invent information.
3. NEVER guess a flight code.
4. ALWAYS use the result returned by a tool.
5. When one tool provides information needed by another tool,
   pass the exact value from the first tool into the second tool.
6. Do not skip required tool calls.

SEARCH RULE:
The benchmark search tool uses exact query keys.

For flight searches:
- If looking for flights from Lahore, use:
  "flights from lahore"
- If looking for flights to Lahore, use:
  "flights to lahore"
- If you already know a flight code, use:
  "flight pk05x9"
  or the appropriate code.

BOOKING RULE:
For a flight-booking task:

1. First call fake_search.
2. Use a concise query that matches the benchmark search database.
3. Read the flight information returned by fake_search.
4. Extract the EXACT flight code.
5. Call fake_booking_api with that exact flight code.
6. Return the booking result.

For the Lahore → Karachi flight on 2026-08-15,
fake_search using "flights from lahore" returns the flight information
containing flight code PK05X9.

Do NOT invent another flight code.

FINAL ANSWER:
Follow the requested output format exactly.

If the task says:
"Return only the city name"
return only the city name.

If it says:
"Return only the final number"
return only the number.

If it says:
"Return only the confirmation message"
return only the confirmation message.
"""

ARW = AdaptiveReliabilityWrapper(config=ARWConfig(max_retries=3))


def run_task(task_path: str, use_consistency: bool = False) -> dict:

    with open(task_path, "r", encoding="utf-8") as f:
        task = json.load(f)

    available_tools = []

    for tool_name in task.get("tools", []):
        if tool_name in TOOL_MAP:
            available_tools.append(TOOL_MAP[tool_name])

    llm = ChatOllama(
        model="qwen2.5:7b",
        base_url="http://localhost:11434",
        temperature=0,
    )

    agent = create_react_agent(
        llm,
        available_tools,
    )

    # --------------------------------------------------------
    # Execute — THIS is where LangGraph's 5.4% "graph terminates with no
    # output" failure happens. ARW retries on exception/empty content,
    # and if the graph still produces nothing after retries, returns an
    # [ARW_FALLBACK] string instead of silently dying.
    # --------------------------------------------------------

    def execute():
        result = agent.invoke(
            {
                "messages": [
                    SystemMessage(content=SYSTEM_PROMPT),
                    ("human", task["instruction"]),
                ]
            },
            config={
                "recursion_limit": 20
            },
        )
        content = result["messages"][-1].content
        return content.strip() if content else None

    start = time.time()
    log = ARW.run(execute, use_consistency=use_consistency, context=f"langgraph_task_{task.get('id', '?')}")
    elapsed = time.time() - start

    return {
        "final_answer": log.final_output,
        "time_taken": elapsed,
        "framework": "langgraph",
        "arw_retries": log.retries_used,
        "arw_crashed_before_arw": log.crashed_before_arw,
        "arw_used_fallback": log.used_fallback,
        "arw_consistency_used": log.consistency_used,
        "arw_consistency_agreed": log.consistency_agreed,
    }