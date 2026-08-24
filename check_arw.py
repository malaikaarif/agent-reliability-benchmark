import json
import glob

files = sorted(glob.glob('logs/*crewai*20260819*.json'))[-20:]
print(f"Last {len(files)} CrewAI logs:\n")

for f in files:
    with open(f) as fp:
        d = json.load(fp)
    tid = d.get('task_id', '?')
    succ = 'PASS' if d.get('success') else 'FAIL'
    retries = d.get('arw_retries', 0)
    print(f"{tid}: {succ} | retries={retries}")