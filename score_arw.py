"""
Scores the most recent ARW batch run for ANY framework, using the real
checker (tasks/checkers/checkers.py) — same logic that produced the
original baseline numbers, so results are directly comparable.

Run from the repo root:
    python score_arw.py --framework crewai
    python score_arw.py --framework autogen

Isolates "this run" from older logs the same way as the LangGraph
version: for each task, takes the N most recently modified logs for
that framework (N = --repeats, default 2), ignoring older baseline
logs automatically.
"""

import argparse
import glob
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from tasks.checkers.checkers import run_checker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--framework", required=True, choices=["langgraph", "crewai", "autogen"])
    parser.add_argument("--repeats", type=int, default=2, help="Must match --repeats used in batch_run.py")
    parser.add_argument("--max-task-num", type=int, default=None)
    args = parser.parse_args()

    fw = args.framework
    pattern = os.path.join("logs", f"t*_{fw}_r*_*.json")
    files = glob.glob(pattern)
    if not files:
        print(f"ERROR: no {fw} logs found in logs/. Run this from the repo root.")
        return 1

    by_task = defaultdict(list)
    for f in files:
        base = os.path.basename(f)
        task_id = base.split(f"_{fw}_")[0]
        if args.max_task_num is not None and (not task_id[1:].isdigit() or int(task_id[1:]) > args.max_task_num): continue
        by_task[task_id].append(f)

    selected = []
    for task_id, flist in by_task.items():
        flist_sorted = sorted(flist, key=os.path.getmtime, reverse=True)
        selected.extend(flist_sorted[:args.repeats])

    selected.sort(key=os.path.getmtime)
    oldest, newest = os.path.basename(selected[0]), os.path.basename(selected[-1])
    print(f"Selected {len(selected)} logs across {len(by_task)} tasks")
    print(f"Timestamp range: {oldest}  ->  {newest}")
    print("(Sanity check: these should all be from your most recent batch run, today.)\n")

    passed = failed = fallback_triggered = crashed_before_arw = total_retries = 0
    rows = []

    for f in selected:
        with open(f) as fh:
            log = json.load(fh)

        task_id = log.get("task_id") or os.path.basename(f).split(f"_{fw}_")[0]
        final_answer = log.get("final_answer", "")
        is_fallback = isinstance(final_answer, str) and final_answer.startswith("[ARW_FALLBACK]")

        task_path = os.path.join("tasks", f"{task_id}.json")
        if not os.path.exists(task_path):
            print(f"WARNING: {task_path} not found, skipping {f}")
            continue

        check = run_checker(task_path, final_answer)
        ok = check["success"] and not is_fallback

        if is_fallback:
            fallback_triggered += 1
        if log.get("arw_crashed_before_arw"):
            crashed_before_arw += 1
        total_retries += log.get("arw_retries") or 0

        if ok:
            passed += 1
        else:
            failed += 1

        rows.append({
            "task_id": task_id, "repeat": log.get("repeat"), "pass": ok,
            "fallback": is_fallback, "arw_retries": log.get("arw_retries"),
            "crashed_before_arw": log.get("arw_crashed_before_arw"),
            "final_answer": str(final_answer)[:60],
        })

    total = passed + failed
    print("=" * 60)
    print(f"{fw.upper()} + ARW — REAL CORRECTNESS SCORE")
    print("=" * 60)
    print(f"Total runs scored:        {total}")
    print(f"Passed:                   {passed} ({passed/total:.1%})")
    print(f"Failed:                   {failed} ({failed/total:.1%})")
    print(f"ARW fallback triggered:   {fallback_triggered} ({fallback_triggered/total:.1%})")
    print(f"Crashed before ARW retry: {crashed_before_arw} ({crashed_before_arw/total:.1%})")
    print(f"Total retries used:       {total_retries}")
    print("=" * 60)

    os.makedirs("analysis", exist_ok=True)
    out_path = os.path.join("analysis", f"{fw}_results_arw.md")
    with open(out_path, "w", encoding="utf-8") as out:
        out.write(f"# {fw.capitalize()} + ARW Benchmark Results\n\n")
        out.write(f"Scored {total} runs ({len(by_task)} tasks x {args.repeats} repeats) "
                   f"using tasks/checkers/checkers.py.\n\n")
        out.write("| Task | Repeat | Result | ARW Fallback | Retries | Crashed Before ARW | Final Answer |\n")
        out.write("|------|--------|--------|--------------|---------|--------------------|--------------|\n")
        for r in sorted(rows, key=lambda x: (x["task_id"], x["repeat"] or 0)):
            out.write(
                f"| {r['task_id']} | {r['repeat']} | {'PASS' if r['pass'] else 'FAIL'} | "
                f"{'yes' if r['fallback'] else 'no'} | {r['arw_retries']} | "
                f"{'yes' if r['crashed_before_arw'] else 'no'} | {r['final_answer']} |\n"
            )
        out.write("\n## Summary\n\n")
        out.write(f"- Total runs: {total}\n")
        out.write(f"- Passed: {passed} ({passed/total:.1%})\n")
        out.write(f"- Failed: {failed} ({failed/total:.1%})\n")
        out.write(f"- ARW fallback triggered: {fallback_triggered} ({fallback_triggered/total:.1%})\n")
        out.write(f"- Total retries consumed: {total_retries}\n")

    print(f"\nWrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())