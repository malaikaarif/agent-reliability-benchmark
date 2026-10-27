import os, json, collections
d = collections.defaultdict(lambda: [0, 0])
for f in os.listdir("logs/baseline/autogen"):
    if not f.endswith(".json"):
        continue
    with open(os.path.join("logs/baseline/autogen", f), encoding="utf-8") as fh:
        r = json.load(fh)
    d[r["task_id"]][0] += 1
    d[r["task_id"]][1] += 1 if r.get("success") else 0
rows = sorted(d.items(), key=lambda x: x[1][1] / x[1][0])
for t, (n, ok) in rows:
    print(f"{t}  runs={n:3d}  pass={100*ok/n:5.1f}%")
print("tasks at 0%:", [t for t, (n, ok) in d.items() if ok == 0])
print("tasks at 90%+:", [t for t, (n, ok) in d.items() if ok / n >= 0.9])
