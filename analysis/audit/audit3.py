import os, json, re, collections
pat = re.compile(r"Expected '(.*?)'( inside answer)?, got '")
leaky = collections.Counter()
echo = echo_pass = 0
for root, d, files in os.walk("logs"):
    for f in files:
        if not f.endswith(".json"):
            continue
        try:
            with open(os.path.join(root, f), encoding="utf-8") as fh:
                r = json.load(fh)
        except Exception:
            continue
        m = pat.match(str(r.get("checker_details", "")))
        if not m:
            continue
        exp = m.group(1).strip().lower()
        ins = str(r.get("instruction", "")).lower()
        ans = str(r.get("final_answer", "")).strip().lower()
        if exp and exp in ins:
            leaky[r.get("task_id")] += 1
        if ins and ans.startswith(ins[:40]):
            echo += 1
            echo_pass += 1 if r.get("success") else 0
print("answers that start with the instruction:", echo, "| of those marked pass:", echo_pass)
print("tasks whose instruction contains the expected answer:", dict(leaky))
