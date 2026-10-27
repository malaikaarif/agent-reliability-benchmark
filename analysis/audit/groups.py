import os, json, collections
folder = "logs/baseline/autogen"
g = collections.defaultdict(list)
for f in os.listdir(folder):
    if not f.endswith(".json"):
        continue
    with open(os.path.join(folder, f), encoding="utf-8") as fh:
        r = json.load(fh)
    if r["task_id"] == "t20":
        g[" ".join(str(r["final_answer"]).split())[:20]].append((r["repeat"], round(r["time_taken"]), r["timestamp"][:16]))
for a, rows in g.items():
    print(repr(a), len(rows))
    for x in sorted(rows, key=lambda x: x[2]):
        print("   ", x)
