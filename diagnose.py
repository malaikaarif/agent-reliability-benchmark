import json
import glob
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), 'tasks', 'checkers'))
from checkers import run_checker

# Find a LangGraph log for a simple task (e.g., t01 or t02)
files = sorted(glob.glob('logs/*langgraph*.json'))
if not files:
    print("No LangGraph logs found")
    exit()

# Pick the first one
f = files[0]
print(f"=== Inspecting: {f} ===\n")

with open(f, 'r', encoding='utf-8') as fp:
    data = json.load(fp)

print("Keys in log:", list(data.keys()))
print(f"\ntask_id: {data.get('task_id')}")
print(f"success (current): {data.get('success')}")
print(f"checker_details: {data.get('checker_details')}")
print(f"\nfinal_answer (first 500 chars):\n{str(data.get('final_answer', ''))[:500]}")

# Load the task
task_id = data.get('task_id', '')
task_path = f'tasks/{task_id}.json'
if os.path.exists(task_path):
    with open(task_path, 'r') as fp:
        task = json.load(fp)
    print(f"\n=== Task: {task_id} ===")
    print(f"Keys in task: {list(task.keys())}")
    print(f"expected_answer: {task.get('expected_answer')}")
    print(f"checker: {task.get('checker')}")
    
    # Run checker and print raw result
    print(f"\n=== Running checker ===")
    result = run_checker(data.get('final_answer', ''), task)
    print(f"Checker returned: {result}")
    print(f"Type: {type(result)}")
else:
    print(f"\nTask file not found: {task_path}")