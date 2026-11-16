"""Auto-checkers for task validation.

Default mode "eq1" implements Eq. 1 of the paper:
    pass = 1 if a == e (exact_match) or e is contained in a (contains_substring),
    both evaluated after case-insensitive normalization.

Two deliberate safeguards on top of the literal equation (document them in the paper):
  1. Containment is whole-token ("2" does not match inside "12" or "275000").
  2. A task may list "forbidden" strings (e.g. t41: "REJECTED"); an answer that
     contains one fails even if it also contains the expected text.

mode="legacy" reproduces the old behaviour (one checker per task, case-sensitive)
so the numbers in the first draft stay reproducible.
"""

import json
import re


def normalize(s) -> str:
    return re.sub(r"\s+", " ", str(s).casefold().strip())


def _contains_token(answer: str, expected: str) -> bool:
    return re.search(r"(?<!\w)" + re.escape(expected) + r"(?!\w)", answer) is not None


def exact_match(final_answer: str, expected: str) -> dict:
    a, e = normalize(final_answer), normalize(expected)
    return {"success": a == e, "details": f"Expected '{expected}', got '{a}'"}


def contains_substring(final_answer: str, expected: str) -> dict:
    a, e = normalize(final_answer), normalize(expected)
    return {"success": _contains_token(a, e),
            "details": f"Expected '{expected}' inside answer, got '{a}'"}


def eq1(final_answer: str, expected: str, forbidden=()) -> dict:
    a = normalize(final_answer)
    for bad in forbidden:
        if _contains_token(a, normalize(bad)):
            return {"success": False, "details": f"Forbidden '{bad}' in answer '{a}'"}
    ex, sub = exact_match(final_answer, expected), contains_substring(final_answer, expected)
    return {"success": ex["success"] or sub["success"],
            "details": f"exact={ex['success']} contains={sub['success']}; expected '{expected}', got '{a}'"}


def _legacy(task: dict, final_answer: str) -> dict:
    clean, expected = final_answer.strip(), task["expected"]
    if task.get("checker", "exact_match") == "contains_substring":
        return {"success": expected in clean, "details": f"Expected '{expected}' inside answer, got '{clean}'"}
    return {"success": clean == expected, "details": f"Expected '{expected}', got '{clean}'"}


def run_checker(task_path: str, final_answer: str, mode: str = "eq1") -> dict:
    with open(task_path) as f:
        task = json.load(f)
    if mode == "legacy":
        return _legacy(task, final_answer)
    return eq1(final_answer, task["expected"], task.get("forbidden", ()))