import json
import glob
import os
import sys
import re
from pathlib import Path

sys.path.insert(0, os.path.join(os.getcwd(), 'tasks', 'checkers'))
from checkers import run_checker

LOG_DIR = Path('logs')
TASK_DIR = Path('tasks')

def get_task_id_from_filename(filename):
    m = re.match(r'^(t\d+)_', filename)
    if m:
        return m.group(1)
    m = re.search(r'(t\d+)', filename)
    if m:
        return m.group(1)
    return None

def safe_json_read(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def safe_json_write(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def process_framework(framework):
    files = sorted(LOG_DIR.glob(f'*{framework}*.json'))
    processed = corrupt = no_task = skipped = 0

    print(f"\n{'='*60}")
    print(f"Framework: {framework.upper()} | Files: {len(files)}")
    print(f"{'='*60}")

    for f in files:
        task_id = get_task_id_from_filename(f.name)
        if not task_id:
            skipped += 1
            continue

        data = safe_json_read(f)
        if data is None:
            corrupt += 1
            continue

        task_path = TASK_DIR / f"{task_id}.json"
        if not task_path.exists():
            no_task += 1
            continue

        # Ensure final_answer is a string
        final_answer = data.get('final_answer', '')
        if final_answer is None:
            final_answer = ''
        elif not isinstance(final_answer, str):
            final_answer = str(final_answer)

        # ── CORRECTED: pass path string, not dict ─────────────────
        try:
            check = run_checker(str(task_path), final_answer)
            data['success'] = check['success']
            data['checker_details'] = check.get('details', '')
        except Exception as e:
            print(f"  ⚠️  Checker error on {f.name}: {e}")
            data['success'] = False
            data['checker_details'] = f"checker_error: {e}"

        data['task_id'] = task_id

        if safe_json_write(f, data):
            processed += 1

    print(f"\n📊 {framework.upper()}: Processed {processed} | Corrupt {corrupt} | Missing task {no_task} | Skipped {skipped}")
    return processed

total = 0
for fw in ['langgraph', 'autogen', 'crewai']:
    total += process_framework(fw)

print(f"\n{'='*60}")
print(f"✅ GRAND TOTAL PROCESSED: {total}")
print(f"{'='*60}")