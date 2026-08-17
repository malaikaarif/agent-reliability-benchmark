import json
import glob
from collections import defaultdict, Counter

def analyze_framework(framework):
    files = glob.glob(f'logs/*{framework}*.json')
    
    passes = 0
    failures = defaultdict(list)  # reason -> list of file names
    
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                d = json.load(fp)
        except:
            continue
        
        if d.get('success'):
            passes += 1
            continue
        
        # Categorize the failure
        details = str(d.get('checker_details', '')).lower()
        final_ans = str(d.get('final_answer', '')).lower()
        
        # Infrastructure / framework crashes
        if 'invalid response from llm' in final_ans or 'none or empty' in final_ans:
            reason = 'infra_crash'
        elif 'timeout' in final_ans or 'timed out' in final_ans:
            reason = 'timeout'
        elif 'error' in final_ans and len(final_ans) < 200:
            reason = 'runtime_error'
        # Answer quality failures
        elif 'exact_match' in details:
            reason = 'wrong_answer_exact'
        elif 'contains' in details:
            reason = 'wrong_answer_contains'
        elif len(final_ans.strip()) == 0:
            reason = 'empty_answer'
        elif 'i don\'t know' in final_ans or 'unable to' in final_ans:
            reason = 'refused'
        else:
            reason = 'other'
        
        failures[reason].append(f.replace('\\', '/').split('/')[-1])
    
    total = passes + sum(len(v) for v in failures.values())
    
    print(f"\n{'='*60}")
    print(f"{framework.upper()} — {passes}/{total} passed ({passes/total*100:.1f}%)")
    print(f"{'='*60}")
    
    for reason, files_list in sorted(failures.items(), key=lambda x: -len(x[1])):
        pct = len(files_list) / total * 100
        print(f"\n  {reason}: {len(files_list)} ({pct:.1f}%)")
        # Show 3 examples
        for ex in files_list[:3]:
            print(f"    - {ex}")
    
    return passes, failures, total

# Run for all frameworks
results = {}
for fw in ['langgraph', 'autogen', 'crewai']:
    p, f, t = analyze_framework(fw)
    results[fw] = {'passes': p, 'failures': f, 'total': t}

# Cross-framework comparison
print(f"\n{'='*60}")
print("CROSS-FRAMEWORK FAILURE COMPARISON")
print(f"{'='*60}")

all_reasons = set()
for fw in results:
    all_reasons.update(results[fw]['failures'].keys())

for reason in sorted(all_reasons):
    print(f"\n  {reason}:")
    for fw in ['langgraph', 'autogen', 'crewai']:
        count = len(results[fw]['failures'].get(reason, []))
        total = results[fw]['total']
        pct = count / total * 100 if total else 0
        print(f"    {fw:10s}: {count:3d} / {total:3d}  ({pct:5.1f}%)")