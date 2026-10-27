import os, json, collections
folder = "logs/baseline/autogen"
by = collections.defaultdict(lambda: [0, 0])
for f in os.listdir(folder):
    if not f.endswith(".json"):
        continue
    with open(os.path.join(folder, f), encoding="utf-8") as fh:
        r = json.load(fh)
    k = r["repeat"] if r["repeat"] <= 4 else "5+"
    by[k][0] += 1
    by[k][1] += 1 if r.get("success") else 0
for k in sorted(by, key=str):
    n, ok = by[k]
    print(f"repeat {k}: runs={n}  pass={100*ok/n:.1f}%")
n12 = by[1][0] + by[2][0]
ok12 = by[1][1] + by[2][1]
print(f"repeats 1+2 only: runs={n12}  pass={100*ok12/n12:.1f}%")
tn = sum(v[0] for v in by.values())
tok = sum(v[1] for v in by.values())
print(f"all repeats: runs={tn}  pass={100*tok/tn:.1f}%")
