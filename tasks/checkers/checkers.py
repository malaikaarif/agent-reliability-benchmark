"""Auto-checkers for task validation."""

import json

def exact_match(final_answer: str, expected: str) -> dict:
    clean = final_answer.strip()
    return {
        "success": clean == expected,
        "details": f"Expected '{expected}', got '{clean}'"
    }

def contains_substring(final_answer: str, expected: str) -> dict:
    clean = final_answer.strip()
    return {
        "success": expected in clean,
        "details": f"Expected '{expected}' inside answer, got '{clean}'"
    }

def run_checker(task_path: str, final_answer: str) -> dict:
    with open(task_path) as f:
        task = json.load(f)
    
    checker_name = task.get("checker", "exact_match")
    expected = task["expected"]
    
    if checker_name == "exact_match":
        return exact_match(final_answer, expected)
    elif checker_name == "contains_substring":
        return contains_substring(final_answer, expected)
    else:
        return {"success": False, "details": f"Unknown checker: {checker_name}"}