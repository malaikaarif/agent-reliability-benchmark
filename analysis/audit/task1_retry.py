import glob, json, re, os, collections
from tasks.checkers.checkers import run_checker
rows = []
for f in glob.glob("logs/**/t*_*_r*_*.json", recursive=True):
    m = re.match(r"(t\d+)_(langgraph|autogen|crewai)_r(\d+)_(\d{8}_\d{6})\.json$", os.path.basename(f))
    if not m:
        continue
    try:
        with open(f, encoding="utf-8") as fh:
            log = json.load(fh)
    except Exception:
        continue
    if log.get("arw_retries") is None:
        continue
    tid, fw, rep, ts = m.groups()
    tp = f"tasks/{tid}.json"
    if not os.path.exists(tp):
        continue
    ans = str(log.get("final_answer", ""))
    rows.append((fw, tid, log.get("arw_retries"), bool(log.get("arw_crashed_before_arw")),
                 bool(log.get("arw_used_fallback")),
                 run_checker(tp, ans, "legacy")["success"], run_checker(tp, ans, "eq1")["success"]))
by = collections.defaultdict(list)
for r in rows:
    by[r[0]].append(r)
for fw, rs in by.items():
    n = len(rs)
    fired = [r for r in rs if r[2] > 0]
    print(f"\n{fw}: ARW runs={n}")
    print(f"  retry fired (arw_retries>0): {len(fired)} | of those passed legacy/eq1: {sum(r[5] for r in fired)}/{sum(r[6] for r in fired)}")
    print(f"  crashed_before_arw: {sum(r[3] for r in rs)} | used_fallback: {sum(r[4] for r in rs)}")
    print(f"  pass overall legacy: {sum(r[5] for r in rs)}/{n}  eq1: {sum(r[6] for r in rs)}/{n}")
