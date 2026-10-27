import os, json, csv, collections

CATS = [("web search", 1, 9), ("file manipulation", 10, 18), ("booking", 19, 27),
        ("math", 28, 36), ("team coordination", 37, 45)]

def cat(task_id):
    n = int(task_id[1:])
    for name, a, b in CATS:
        if a <= n <= b:
            return name
    return "?"

groups = collections.defaultdict(dict)
for root, dirs, files in os.walk("logs"):
    for f in files:
        if not f.endswith(".json"):
            continue
        p = os.path.join(root, f)
        try:
            with open(p, encoding="utf-8") as fh:
                r = json.load(fh)
        except Exception:
            print("unreadable:", p)
            continue
        groups[(root, r.get("framework", "?"))][r.get("run_id", f)] = r

rows = []
for (root, fw), runs in sorted(groups.items()):
    vals = list(runs.values())
    n = len(vals)
    passed = sum(1 for r in vals if r.get("success"))
    echo = sum(1 for r in vals if str(r.get("final_answer", "")).strip() == str(r.get("instruction", "")).strip())
    empty = sum(1 for r in vals if not str(r.get("final_answer", "")).strip())
    sub = sum(1 for r in vals if "inside answer" in str(r.get("checker_details", "")))
    plain = sum(1 for r in vals if str(r.get("checker_details", "")).startswith("Expected") and "inside answer" not in str(r.get("checker_details", "")))
    print(f"\n{root} | {fw} | runs={n} pass={100*passed/n:.1f}% ({passed})")
    print(f"   answer==instruction: {echo} | empty answer: {empty} | failures with substring message: {sub} | failures with plain-Expected message: {plain}")
    bycat = collections.defaultdict(lambda: [0, 0])
    for r in vals:
        c = cat(r.get("task_id", "t00"))
        bycat[c][0] += 1
        bycat[c][1] += 1 if r.get("success") else 0
    for c, (tot, ok) in bycat.items():
        print(f"   {c:20s} {100*ok/tot:5.1f}%  ({ok}/{tot})")
        rows.append([root, fw, c, tot, ok, round(100*ok/tot, 1)])

with open("audit_summary.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["folder", "framework", "category", "runs", "passed", "pass_pct"])
    w.writerows(rows)
print("\nSaved audit_summary.csv")
