import os, json, collections
zero = ["t03","t06","t12","t16","t17","t19","t20","t21","t27","t29","t31","t34","t35","t36","t37","t38"]
answers = collections.defaultdict(collections.Counter)
folder = "logs/baseline/autogen"
for f in os.listdir(folder):
    if not f.endswith(".json"):
        continue
    with open(os.path.join(folder, f), encoding="utf-8") as fh:
        r = json.load(fh)
    if r["task_id"] in zero:
        answers[r["task_id"]][" ".join(str(r.get("final_answer", "")).split())[:90]] += 1
for t in zero:
    with open(f"tasks/{t}.json", encoding="utf-8") as fh:
        spec = json.load(fh)
    print(f"\n=== {t} | {spec['type']} | checker={spec['checker']} | expected={spec['expected']!r}")
    print("task:", spec["instruction"][:160])
    for a, n in answers[t].most_common(3):
        print(f"   {n}x  {a!r}")
