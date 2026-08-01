import sys, json, glob
sys.path.insert(0, "tools")
from fake_tools import fake_search, fake_file_reader, fake_calculator, fake_booking_api

def test_task(task_path):
    with open(task_path) as f:
        task = json.load(f)
    
    print(f"\n{'='*50}")
    print(f"Testing: {task['id']} | {task['type']} | {task['length']}")
    
    if task['id'] == 't01':
        result = fake_search("capital of pakistan")
    elif task['id'] == 't02':
        data = fake_file_reader("employees.csv")
        print("File:\n", data)
        result = fake_calculator("90000 - 50000")
    elif task['id'] == 't03':
        result = fake_booking_api("PK05X9")
    elif task['id'] == 't04':
        result = fake_calculator("(150 * 23) + 47")
    elif task['id'] == 't05':
        e = fake_search("height of everest")
        k = fake_search("height of k2")
        print(f"Everest: {e}, K2: {k}")
        result = fake_calculator("8848 - 8611")
    elif task['id'] == 't06':
        products = fake_file_reader("products.csv")
        print("Products:\n", products)
        total = fake_calculator("800*5 + 20*50 + 50*30")
        budget = fake_file_reader("budget.txt")
        print(f"Total stock: {total}, Budget info: {budget}")
        result = "YES"
    else:
        result = "UNKNOWN"
    
    print(f"Manual result: '{result}'")
    print(f"Expected: '{task['expected']}'")
    
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from tasks.checkers.checkers import run_checker
    check = run_checker(task_path, str(result))
    status = "PASS" if check['success'] else "FAIL"
    print(f"CHECKER: {status} - {check['details']}")

if __name__ == "__main__":
    for task_file in sorted(glob.glob("tasks/t*.json")):
        test_task(task_file)