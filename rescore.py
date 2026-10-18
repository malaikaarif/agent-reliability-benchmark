import collections, glob, json, os, re
from tasks.checkers.checkers import run_checker

# Collect runs. ARW run = non-null "arw_retries". Order by timestamp in the file name.
runs = []
for f in glob.glob("logs/**/t*_*_r*_*.json", recursive=True):
    m = re.match(r"(t\d+)_(langgraph|autogen|crewai)_r(\d+)_(\d{8}_\d{6})\.json$", os.path.basename(f))
    if not m:
        continue
    try:
        log = json.load(open(f))
    except Exception:
        continue
    tid, fw, _, ts = m.groups()
    tp = f"tasks/{tid}.json"
    if not os.path.exists(tp):
        continue
    ans = str(log.get("final_answer", ""))
    runs.append(dict(
        fw=fw, tid=tid, ts=ts, folder=os.path.dirname(f),
        arw=log.get("arw_retries") is not None,
        legacy=run_checker(tp, ans, "legacy")["success"],
        eq1=run_checker(tp, ans, "eq1")["success"]))

def rate(rs, key):
    return 100 * sum(r[key] for r in rs) / len(rs) if rs else float("nan")

REPEATS = 2  # latest N ARW runs per task, same as score_arw.py
print(f"{'fw':11}{'tasks':>6}{'base n':>8}{'ARW n':>7}"
      f"{'base leg':>10}{'ARW leg':>9}{'delta':>7}{'base eq1':>10}{'ARW eq1':>9}{'delta':>7}")
for fw in ["langgraph", "autogen", "crewai"]:
    arw_all = [r for r in runs if r["fw"] == fw and r["arw"]]
    base_all = [r for r in runs if r["fw"] == fw and not r["arw"] and "archive" not in r["folder"]]
    by_task = collections.defaultdict(list)
    for r in arw_all:
        by_task[r["tid"]].append(r)
    arw = [r for t in by_task.values() for r in sorted(t, key=lambda x: x["ts"])[-REPEATS:]]
    tasks = set(by_task)
    base = [r for r in base_all if r["tid"] in tasks]   # matched task set
    if not arw:
        print(f"{fw:11}  no ARW runs found")
        continue
    print(f"{fw:11}{len(tasks):6d}{len(base):8d}{len(arw):7d}"
          f"{rate(base,'legacy'):9.1f}%{rate(arw,'legacy'):8.1f}%{rate(arw,'legacy')-rate(base,'legacy'):+7.1f}"
          f"{rate(base,'eq1'):9.1f}%{rate(arw,'eq1'):8.1f}%{rate(arw,'eq1')-rate(base,'eq1'):+7.1f}")
    if len(tasks) != 45:
        print(f"   tasks covered by {fw} ARW: {sorted(tasks)}")