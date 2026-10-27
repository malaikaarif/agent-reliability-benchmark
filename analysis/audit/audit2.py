import os, json, re, collections

pat = re.compile(r"Expected '(.*?)'( inside answer)?, got '")
valid = re.compile(r"t(0[1-9]|[1-3][0-9]|4[0-5])")
runs = []
for root, dirs, files in os.walk("logs"):
    for f in files:
        if not f.endswith(".json"):
            continue
        try:
            with open(os.path.join(root, f), encoding="utf-8") as fh:
                r = json.load(fh)
        except Exception:
            continue
        r["_folder"] = root
        runs.append(r)

print("=== Task IDs outside t01-t45 ===")
odd = collections.Counter((r["_folder"], r.get("task_id")) for r in runs if not valid.fullmatch(str(r.get("task_id"))))
for k, v in sorted(odd.items(), key=lambda x: -x[1])[:15]:
    print(k, v)

print("\n=== Tasks that use BOTH checker styles ===")
styles = collections.defaultdict(collections.Counter)
for r in runs:
    m = pat.match(str(r.get("checker_details", "")))
    if m:
        styles[r.get("task_id")][(r.get("framework"), "substring" if m.group(2) else "exact")] += 1
both = {t: c for t, c in styles.items() if len({k[1] for k in c}) > 1}
print(len(both), "of", len(styles), "tasks use both styles")
for t, c in sorted(both.items())[:10]:
    print(t, dict(c))

print("\n=== Failed runs where the expected answer IS inside the output ===")
by = collections.defaultdict(lambda: collections.Counter())
examples = []
for r in runs:
    if r.get("success"):
        continue
    m = pat.match(str(r.get("checker_details", "")))
    if not m:
        continue
    exp = m.group(1).strip().lower()
    ans = str(r.get("final_answer", "")).lower()
    kind = "substring" if m.group(2) else "exact"
    by[r["_folder"]]["failed_" + kind] += 1
    if exp and exp in ans:
        by[r["_folder"]]["contained_" + kind] += 1
        if len(examples) < 6:
            examples.append((r.get("task_id"), r.get("framework"), kind, exp, str(r.get("final_answer", ""))[:70]))
for folder, c in sorted(by.items()):
    print(folder, dict(c))
print("\nExamples (task, framework, checker, expected, answer):")
for e in examples:
    print(e)
