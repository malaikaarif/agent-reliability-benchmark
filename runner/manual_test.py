#!/usr/bin/env python3
"""
manual_test_all.py
Validates ALL 45 tasks by manually executing fake tools.
Run from project root: python runner/manual_test_all.py
"""
import sys
import json
import glob
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, "tools")
from fake_tools import fake_search, fake_file_reader, fake_calculator, fake_booking_api
from tasks.checkers.checkers import run_checker

# ============================================================
# MANUAL SOLUTIONS FOR ALL 45 TASKS
# ============================================================

def solve_t01():
    return fake_search("capital of pakistan")

def solve_t02():
    data = fake_file_reader("employees.csv")
    return fake_calculator("90000 - 50000")

def solve_t03():
    return fake_booking_api("PK05X9")

def solve_t04():
    return fake_calculator("(150 * 23) + 47")

def solve_t05():
    e = fake_search("height of everest")
    k = fake_search("height of k2")
    return fake_calculator("8848 - 8611")

def solve_t06():
    total = fake_calculator("800*5 + 20*50 + 50*30")
    return "YES"  # 6500 < 55000

def solve_t07():
    data = fake_file_reader("grades.csv")
    math_avg = fake_calculator("(85 + 78 + 92) / 3")
    sci_avg = fake_calculator("(90 + 82 + 88) / 3")
    return "science"  # 86.67 > 85

def solve_t08():
    return "PK18B2"  # cheapest flight code

def solve_t11():
    return fake_search("capital of france")

def solve_t12():
    return fake_search("currency of japan")

def solve_t13():
    return "14 million, Japanese Yen"

def solve_t14():
    return "Berlin, Paris, Tokyo"

def solve_t15():
    diff = fake_calculator("8848 - 8611")
    return fake_calculator("237 * 14")

def solve_t16():
    return "IPT"  # Islamabad, Paris, Tokyo first letters sorted

def solve_t17():
    return "2"  # 1 from Lahore + 1 to Lahore

def solve_t18():
    return "55000"

def solve_t19():
    return "4"

def solve_t20():
    return fake_calculator("(50000 + 75000 + 60000 + 90000) / 4")

def solve_t21():
    return fake_calculator("800*5 + 20*50 + 50*30")

def solve_t22():
    return "92"

def solve_t23():
    return "2"  # Sara 75000, Noor 90000

def solve_t24():
    return "Hina"  # 92+88=180 highest

def solve_t25():
    return "45000"

def solve_t26():
    return "PK18B2"

def solve_t27():
    return "YES"  # 12000 < 55000

def solve_t28():
    return "UAE12A"

def solve_t29():
    return "PK18B2, 12000, YES"

def solve_t30():
    return fake_calculator("15000 * 2")

def solve_t31():
    return "PK18B2"

def solve_t32():
    return fake_calculator("1000 / 4 + 25")

def solve_t33():
    return fake_calculator("15 / 100 * 200")

def solve_t34():
    return fake_calculator("50000 + 75000 + 60000 + 90000")

def solve_t35():
    return fake_calculator("68750 * 2")

def solve_t36():
    return "15"  # floor(100000 / 6500)

def solve_t37():
    return "Mouse"  # 20/50=0.4 lowest

def solve_t38():
    payroll = fake_calculator("50000 + 75000 + 60000 + 90000")
    ten_pct = fake_calculator("275000 * 0.1")
    stock = fake_calculator("800*5 + 20*50 + 50*30")
    return fake_calculator("27500 + 6500")

def solve_t39():
    return "Hello World"

def solve_t40():
    return "Pakistan is a beautiful country"

def solve_t41():
    return "AI agents are useful"

def solve_t42():
    return "Capital is Islamabad"

def solve_t43():
    return "Ali, Sara, Zain, Noor"

def solve_t44():
    return "300"

def solve_t45():
    return "55000"

def solve_t46():
    return "PK18B2"

def solve_t47():
    return "Laptop"

# Map task IDs to solver functions
SOLVERS = {
    "t01": solve_t01, "t02": solve_t02, "t03": solve_t03, "t04": solve_t04,
    "t05": solve_t05, "t06": solve_t06, "t07": solve_t07, "t08": solve_t08,
    "t11": solve_t11, "t12": solve_t12, "t13": solve_t13, "t14": solve_t14,
    "t15": solve_t15, "t16": solve_t16, "t17": solve_t17, "t18": solve_t18,
    "t19": solve_t19, "t20": solve_t20, "t21": solve_t21, "t22": solve_t22,
    "t23": solve_t23, "t24": solve_t24, "t25": solve_t25, "t26": solve_t26,
    "t27": solve_t27, "t28": solve_t28, "t29": solve_t29, "t30": solve_t30,
    "t31": solve_t31, "t32": solve_t32, "t33": solve_t33, "t34": solve_t34,
    "t35": solve_t35, "t36": solve_t36, "t37": solve_t37, "t38": solve_t38,
    "t39": solve_t39, "t40": solve_t40, "t41": solve_t41, "t42": solve_t42,
    "t43": solve_t43, "t44": solve_t44, "t45": solve_t45, "t46": solve_t46,
    "t47": solve_t47,
}

# ============================================================
# RUN ALL TESTS
# ============================================================

def test_task(task_path):
    with open(task_path) as f:
        task = json.load(f)

    tid = task["id"]
    solver = SOLVERS.get(tid)

    if not solver:
        print(f"\n{'='*50}")
        print(f"⚠️  No solver for {tid} — skipping")
        return None

    result = solver()
    check = run_checker(task_path, str(result))
    status = "PASS" if check["success"] else "FAIL"

    print(f"\n{'='*50}")
    print(f"Testing: {tid} | {task['type']} | {task['length']}")
    print(f"Manual result: '{result}'")
    print(f"Expected: '{task['expected']}'")
    print(f"CHECKER: {status} — {check['details']}")

    return check["success"]

if __name__ == "__main__":
    task_files = sorted(glob.glob("tasks/t*.json"))
    passed = 0
    failed = 0
    skipped = 0

    for task_file in task_files:
        tid = os.path.basename(task_file).replace(".json", "")
        if tid not in SOLVERS:
            print(f"\n⚠️  Skipping {tid} — no solver defined yet")
            skipped += 1
            continue

        ok = test_task(task_file)
        if ok is True:
            passed += 1
        elif ok is False:
            failed += 1

    print(f"\n{'='*50}")
    print(f"RESULTS: PASS={passed} | FAIL={failed} | SKIPPED={skipped} | TOTAL={passed+failed+skipped}")
    print(f"{'='*50}")

    if failed == 0 and skipped == 0:
        print("✅ ALL TASKS PASSED!")
    elif failed > 0:
        print("❌ Some tasks failed. Check expected values or task instructions.")
