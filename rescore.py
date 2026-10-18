"""Rescore existing logs under the legacy checker and Eq. 1. Run from repo root: python rescore.py"""
import collections, glob, json, os, re
from tasks.checkers.checkers import run_checker

res = collections.defaultdict(lambda: [0, 0, 0])
for f in glob.glob("logs/**/t*_*_r*_*.json", recursive=True):
    m = re.match(r"t\d+_(langgraph|autogen|crewai)_r\d+_", os.path.basename(f))
    if not m:
        continue
    try:
        log = json.load(open(f))
    except Exception:
        continue
    tp = f"tasks/{log.get('task_id', '')}.json"
    if not os.path.exists(tp):
        continue
    ans = str(log.get("final_answer", ""))
    r = res[(os.path.dirname(f), m.group(1))]
    r[0] += 1
    r[1] += run_checker(tp, ans, "legacy")["success"]
    r[2] += run_checker(tp, ans, "eq1")["success"]
print(f"{'folder':28}{'fw':11}{'n':>5}{'legacy':>9}{'eq1':>8}")
for (d, fw), (n, a, b) in sorted(res.items()):
    print(f"{d:28}{fw:11}{n:5d}{100*a/n:8.1f}%{100*b/n:7.1f}%")