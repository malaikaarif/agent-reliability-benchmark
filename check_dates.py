import json
import glob
from collections import defaultdict

# Group LangGraph logs by date from filename
by_date = defaultdict(lambda: {'pass': 0, 'fail': 0})

for f in glob.glob('logs/*langgraph*.json'):
    parts = f.replace('\\', '/').split('/')[-1].split('_')
    if len(parts) >= 4:
        date = parts[-2]  # e.g., 20260807
    else:
        date = 'unknown'
    
    try:
        with open(f, 'r') as fp:
            d = json.load(fp)
        if d.get('success'):
            by_date[date]['pass'] += 1
        else:
            by_date[date]['fail'] += 1
    except:
        by_date[date]['fail'] += 1

print("=== LangGraph by date ===")
for date in sorted(by_date.keys()):
    p = by_date[date]['pass']
    f = by_date[date]['fail']
    t = p + f
    rate = (p/t*100) if t else 0
    print(f"  {date}: {p}/{t} passed ({rate:.1f}%)")

print(f"\n=== Totals ===")
total_p = sum(v['pass'] for v in by_date.values())
total_f = sum(v['fail'] for v in by_date.values())
print(f"  Overall: {total_p}/{total_p+total_f} = {total_p/(total_p+total_f)*100:.1f}%")