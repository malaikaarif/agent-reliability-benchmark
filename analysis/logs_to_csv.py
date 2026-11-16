import argparse, collections, csv, glob, json, os, re, sys
sys.path.insert(0, os.getcwd())
from tasks.checkers.checkers import run_checker

PAT = re.compile(r"(t\d+)_(langgraph|autogen|crewai)_r(\d+)_(\d{8}_\d{6})\.json$")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="eq1", choices=["eq1", "legacy"])
    ap.add_argument("--out", default="runs.csv")
    ap.add_argument("--latest", type=int, default=0)
    a = ap.parse_args()
    rows = []
    for f in glob.glob("logs/**/t*_*_r*_*.json", recursive=True):
        if "archive" in f:
            continue
        m = PAT.match(os.path.basename(f))
        if not m:
            continue
        tid, fw, rep, ts = m.groups()
        tp = f"tasks/{tid}.json"
        if not os.path.exists(tp):
            continue
        try:
            with open(f, encoding="utf-8") as fh:
                log = json.load(fh)
        except Exception:
            continue
        ans = str(log.get("final_answer", ""))
        arw = log.get("arw_retries") is not None
        rows.append(dict(task=tid, system=fw, condition="arw" if arw else "base",
                         repeat=int(rep), ts=ts, retries=log.get("arw_retries") or 0,
                         passed=int(run_checker(tp, ans, a.mode)["success"])))
    if a.latest:
        keep, grp = [], collections.defaultdict(list)
        for r in rows:
            if r["condition"] == "arw":
                grp[(r["system"], r["task"])].append(r)
            else:
                keep.append(r)
        for v in grp.values():
            keep += sorted(v, key=lambda x: x["ts"])[-a.latest:]
        rows = keep
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} runs to {a.out}")

if __name__ == "__main__":
    main()
