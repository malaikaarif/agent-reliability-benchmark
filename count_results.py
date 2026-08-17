import json
import glob

for fw in ['langgraph', 'autogen', 'crewai']:
    files = glob.glob(f'logs/*{fw}*.json')
    success = fail = infra_fail = 0

    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                d = json.load(fp)

            if d.get('success', False):
                success += 1
            else:
                fail += 1
                details = str(d.get('checker_details', ''))
                if 'Invalid response from LLM' in details or 'None or empty' in details:
                    infra_fail += 1
        except:
            fail += 1

    total = success + fail
    rate = (success / total * 100) if total else 0
    print(f"\n{'='*50}")
    print(f"{fw.upper()}")
    print(f"  Total:  {total}")
    print(f"  Passed: {success}")
    print(f"  Failed: {fail}")
    print(f"  Rate:   {rate:.1f}%")
    if fw == 'crewai' and infra_fail:
        adj = (success / (total - infra_fail) * 100) if (total - infra_fail) else 0
        print(f"  Infra failures: {infra_fail}")
        print(f"  Adjusted rate:  {adj:.1f}%")

print(f"\n{'='*50}")