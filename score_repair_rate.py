"""
Computes REPAIR RATE — the metric AgentTether (and its own baselines:
Blind retry, Outcome feedback, Reflexion) actually report — so we have
one legitimate, matched-definition number to cite alongside theirs.

Repair rate = (tasks that were FAILING at baseline AND now PASS under ARW)
              / (tasks that were FAILING at baseline)

This is fundamentally different from your existing "overall pass rate"
table (Table VII), which includes tasks that never failed in the first
place. Do NOT delete Table VII — this is an ADDITIONAL table, not a
replacement, because overall pass rate and repair rate answer different
questions and both are legitimate to report.

Run from repo root:
    python score_repair_rate.py --framework langgraph

Requires: baseline logs still present in logs/ (or logs/archive_langgraph/
etc.) with the ORIGINAL date range (Aug 2025), separate from the ARW
logs (today's date). A task is scored as "baseline-failing" if it failed
in MORE THAN HALF of its baseline runs (majority rule, since baseline
repeat counts varied per task/framework per your own Section III-F).
"""

import argparse
import glob
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from tasks.checkers.checkers import run_checker

# Baseline logs predate the ARW work; ARW logs are from the ARW testing
# session. Both are dated 2026, so we split by day-of-month within
# August instead of by year. Baseline runs finished by ~Aug 15-16;
# ARW runs started ~Aug 18. Adjust ARW_CUTOFF_DATE if your own dates
# differ from this.
ARW_CUTOFF_DATE = 20260817  # any log dated on/after this = ARW, before = baseline

import re

def log_date(filename):
    m = re.search(r"(\d{8})_\d{6}", filename)
    return int(m.group(1)) if m else None


def score_log(path, fw):
    with open(path) as f:
        log = json.load(f)
    task_id = log.get("task_id") or os.path.basename(path).split(f"_{fw}_")[0]
    final_answer = log.get("final_answer", "")
    is_fallback = isinstance(final_answer, str) and final_answer.startswith("[ARW_FALLBACK]")
    task_path = os.path.join("tasks", f"{task_id}.json")
    if not os.path.exists(task_path):
        return task_id, None
    check = run_checker(task_path, final_answer)
    ok = check["success"] and not is_fallback
    return task_id, ok


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--framework", required=True, choices=["langgraph", "crewai", "autogen"])
    args = parser.parse_args()
    fw = args.framework

    all_logs = glob.glob(os.path.join("logs", "**", f"t*_{fw}_r*_*.json"), recursive=True)
    if not all_logs:
        print(f"ERROR: no {fw} logs found anywhere under logs/.")
        return 1

    baseline_logs = [f for f in all_logs if log_date(os.path.basename(f)) is not None and log_date(os.path.basename(f)) < ARW_CUTOFF_DATE]
    arw_logs = [f for f in all_logs if log_date(os.path.basename(f)) is not None and log_date(os.path.basename(f)) >= ARW_CUTOFF_DATE]

    print(f"Found {len(baseline_logs)} baseline-dated logs and {len(arw_logs)} ARW-dated logs for {fw}.")
    print("SANITY CHECK: verify these counts look right before trusting the output below.\n")

    # baseline: majority-vote pass/fail per task
    baseline_by_task = defaultdict(list)
    for f in baseline_logs:
        task_id, ok = score_log(f, fw)
        if ok is not None:
            baseline_by_task[task_id].append(ok)

    baseline_failing_tasks = set()
    for task_id, results in baseline_by_task.items():
        pass_rate = sum(results) / len(results)
        if pass_rate < 0.5:
            baseline_failing_tasks.add(task_id)

    print(f"Tasks failing at baseline (majority-fail rule): {len(baseline_failing_tasks)} of {len(baseline_by_task)}")

    # ARW: most recent 2 logs per task (same selection rule as score_arw.py)
    arw_by_task = defaultdict(list)
    for f in arw_logs:
        base = os.path.basename(f)
        task_id = base.split(f"_{fw}_")[0]
        arw_by_task[task_id].append(f)

    repaired = 0
    still_failing = 0
    details = []

    for task_id in sorted(baseline_failing_tasks):
        flist = sorted(arw_by_task.get(task_id, []), key=os.path.getmtime, reverse=True)[:2]
        if not flist:
            print(f"WARNING: no ARW logs found for baseline-failing task {task_id}, skipping")
            continue
        results = []
        for f in flist:
            _, ok = score_log(f, fw)
            if ok is not None:
                results.append(ok)
        if not results:
            continue
        arw_pass_rate = sum(results) / len(results)
        fixed = arw_pass_rate >= 0.5
        if fixed:
            repaired += 1
        else:
            still_failing += 1
        details.append((task_id, arw_pass_rate, fixed))

    total = repaired + still_failing
    print("\n" + "=" * 60)
    print(f"{fw.upper()} — REPAIR RATE (AgentTether-comparable metric)")
    print("=" * 60)
    print(f"Baseline-failing tasks evaluated: {total}")
    print(f"Repaired under ARW:               {repaired}")
    print(f"Still failing under ARW:          {still_failing}")
    if total:
        print(f"Repair rate:                       {repaired/total:.1%}")
    print("=" * 60)
    for task_id, rate, fixed in details:
        print(f"  {task_id}: ARW pass rate {rate:.0%} -> {'REPAIRED' if fixed else 'still failing'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())