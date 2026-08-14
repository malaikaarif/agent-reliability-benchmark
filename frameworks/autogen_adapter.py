import sys
import os
import time
import json
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.ollama import OllamaChatCompletionClient

from tools.fake_tools import (
    fake_search,
    fake_file_reader,
    fake_calculator,
    fake_booking_api,
)


# ============================================================
# TOOLS
# ============================================================

async def fake_search_tool(query: str) -> str:
    result = fake_search(query)
    print(f"\n[TOOL] fake_search({query!r})")
    print(f"[RESULT] {result}")
    return result


async def fake_file_reader_tool(filename: str) -> str:
    result = fake_file_reader(filename)
    print(f"\n[TOOL] fake_file_reader({filename!r})")
    print(f"[RESULT] {result}")
    return result


async def fake_calculator_tool(expression: str) -> str:
    result = fake_calculator(expression)
    print(f"\n[TOOL] fake_calculator({expression!r})")
    print(f"[RESULT] {result}")
    return result


async def fake_booking_api_tool(flight_code: str) -> str:
    result = fake_booking_api(flight_code)
    print(f"\n[TOOL] fake_booking_api({flight_code!r})")
    print(f"[RESULT] {result}")
    return result


TOOL_MAP = {
    "fake_search": fake_search_tool,
    "fake_file_reader": fake_file_reader_tool,
    "fake_calculator": fake_calculator_tool,
    "fake_booking_api": fake_booking_api_tool,
}


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are a tool-using agent in a reliability benchmark.

Follow the benchmark instruction EXACTLY.

RULES:

1. You MUST actually use every requested tool.
2. NEVER invent information.
3. NEVER guess.
4. Tool results are authoritative.
5. If a tool returns information, use that exact information.
6. Follow the requested order of operations.
7. Complete ALL required steps before answering.
8. The final response MUST contain ONLY the requested answer.
9. Do NOT repeat the task instruction.
10. Do NOT explain your reasoning.
11. Do NOT add quotation marks.
12. Do NOT say "The answer is".
13. Do NOT return an empty response.

Examples:

If the task says:
"Use fake_search to find the capital of Pakistan.
Return only the city name."

You MUST:
- call fake_search
- read its result
- return:

Islamabad

If the task says:
"Return only the final number."

Return only the number.

If the task says:
"Return only the city name."

Return only the city name.

If the task requires multiple tools, complete all tool calls first,
then return ONLY the final requested value.
"""


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

    start = time.time()

    async def execute():

        model_client = OllamaChatCompletionClient(
            model="qwen2.5:7b",
            host="http://localhost:11434",
            temperature=0,
        )

        try:

            agent = AssistantAgent(
                name="benchmark_agent",
                model_client=model_client,
                tools=available_tools,
                system_message=SYSTEM_PROMPT,
                max_tool_iterations=10,
            )

            result = await agent.run(
                task=task["instruction"]
            )

            # ------------------------------------------------
            # Find the LAST useful text response
            # ------------------------------------------------

            for message in reversed(result.messages):

                if isinstance(message, TextMessage):

                    content = message.content

                    if content and content.strip():

                        text = content.strip()

                        # Ignore the original task instruction
                        if text != task["instruction"].strip():

                            return text

            return ""

        finally:

            await model_client.close()

    try:

        final_answer = asyncio.run(execute())

    except Exception as e:

        final_answer = (
            f"ERROR: {type(e).__name__}: {str(e)}"
        )

    elapsed = time.time() - start

    return {
        "final_answer": final_answer.strip(),
        "time_taken": elapsed,
        "framework": "autogen",
    }