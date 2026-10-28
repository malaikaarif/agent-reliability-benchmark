import os, json, collections
folder = "logs/baseline/autogen"
types = {}
for f in os.listdir("tasks"):
    if f.endswith(".json") and "_" not in f:
        with open(os.path.join("tasks", f), encoding="utf-8") as fh:
            s = json.load(fh)
        types[s["id"]] = s["type"]
split = ["t20","t21","t31","t35","t36","t38"]
byans = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
bytype = collections.defaultdict(lambda: [0, 0, set()])
for f in os.listdir(folder):
    if not f.endswith(".json"):
        continue
    with open(os.path.join(folder, f), encoding="utf-8") as fh:
        r = json.load(fh)
    t = r["task_id"]
    if t in split:
        byans[t][" ".join(str(r["final_answer"]).split())[:40]][r["timestamp"][:10]] += 1
    b = bytype[types.get(t, "?")]
    b[0] += 1
    b[1] += 1 if r.get("success") else 0
    b[2].add(t)
print("=== Which dates produced which answer ===")
for t in split:
    print(t)
    for ans, dates in byans[t].items():
        print("   ", repr(ans), dict(dates))
print("\n=== Pass rate by task type (AutoGen baseline) ===")
for ty, (n, ok, ts) in sorted(bytype.items()):
    print(f"{ty:18s} tasks={len(ts):2d} runs={n:3d} pass={100*ok/n:5.1f}%")
