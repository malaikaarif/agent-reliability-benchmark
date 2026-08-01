#!/usr/bin/env python3
"""
generate_all_tasks.py
Run this from your agent-reliability-benchmark folder.
It creates all 45 task JSON files in tasks/
"""
import json
import os

tasks_dir = "tasks"
os.makedirs(tasks_dir, exist_ok=True)

tasks = []

# ============================================================
# TYPE 1: WEB RESEARCH (9 tasks)
# ============================================================

# Short
tasks.append({
    "id": "t01",
    "type": "web_research",
    "length": "short",
    "instruction": "Use fake_search to find the capital of Pakistan. Return only the city name.",
    "tools": ["fake_search"],
    "expected": "Islamabad",
    "checker": "exact_match"
})

tasks.append({
    "id": "t11",
    "type": "web_research",
    "length": "short",
    "instruction": "Use fake_search to find the capital of France. Return only the city name.",
    "tools": ["fake_search"],
    "expected": "Paris",
    "checker": "exact_match"
})

tasks.append({
    "id": "t12",
    "type": "web_research",
    "length": "short",
    "instruction": "Use fake_search to find the currency of Japan. Return only the currency name.",
    "tools": ["fake_search"],
    "expected": "Japanese Yen",
    "checker": "exact_match"
})

# Medium
tasks.append({
    "id": "t05",
    "type": "web_research",
    "length": "medium",
    "instruction": "Step 1: Use fake_search to find the height of Everest. Step 2: Use fake_search to find the height of K2. Step 3: Use fake_calculator to subtract K2's height from Everest's height. Return only the difference in meters as a number.",
    "tools": ["fake_search", "fake_calculator"],
    "expected": "237",
    "checker": "exact_match"
})

tasks.append({
    "id": "t13",
    "type": "web_research",
    "length": "medium",
    "instruction": "Step 1: Use fake_search to find the population of Lahore. Step 2: Use fake_search to find the currency of Japan. Step 3: Return the two answers separated by a comma with exactly one space after the comma, like: '14 million, Japanese Yen'.",
    "tools": ["fake_search"],
    "expected": "14 million, Japanese Yen",
    "checker": "exact_match"
})

tasks.append({
    "id": "t14",
    "type": "web_research",
    "length": "medium",
    "instruction": "Step 1: Use fake_search to find the capital of Germany. Step 2: Use fake_search to find the capital of France. Step 3: Use fake_search to find the capital of Japan. Step 4: Sort these three capitals alphabetically. Step 5: Return them separated by commas with one space after each comma.",
    "tools": ["fake_search"],
    "expected": "Berlin, Paris, Tokyo",
    "checker": "exact_match"
})

# Long
tasks.append({
    "id": "t15",
    "type": "web_research",
    "length": "long",
    "instruction": "Step 1: Use fake_search to find the height of Everest in meters. Step 2: Use fake_search to find the height of K2 in meters. Step 3: Use fake_calculator to subtract K2 from Everest. Step 4: Use fake_search to find the population of Lahore. Step 5: Extract just the number (14) from the population. Step 6: Use fake_calculator to multiply the height difference by the population number. Return only the final number.",
    "tools": ["fake_search", "fake_calculator"],
    "expected": "3318",
    "checker": "exact_match"
})

tasks.append({
    "id": "t16",
    "type": "web_research",
    "length": "long",
    "instruction": "Step 1: Use fake_search to find the capital of Pakistan. Step 2: Use fake_search to find the capital of France. Step 3: Use fake_search to find the capital of Japan. Step 4: Take the first letter of each capital. Step 5: Concatenate them in alphabetical order. Return only the 3-letter result.",
    "tools": ["fake_search"],
    "expected": "IPT",
    "checker": "exact_match"
})

tasks.append({
    "id": "t17",
    "type": "web_research",
    "length": "long",
    "instruction": "Step 1: Use fake_search to find flights from Lahore. Step 2: Count how many flights are found. Step 3: Use fake_search to find flights to Lahore. Step 4: Count how many flights are found. Step 5: Use fake_calculator to add both counts. Return only the total number.",
    "tools": ["fake_search", "fake_calculator"],
    "expected": "2",
    "checker": "exact_match"
})

# ============================================================
# TYPE 2: FILE / DATA (9 tasks)
# ============================================================

# Short
tasks.append({
    "id": "t02",
    "type": "file_data",
    "length": "short",
    "instruction": "Use fake_file_reader to read 'employees.csv'. Use fake_calculator to find the difference between the highest and lowest salary. Return only the number.",
    "tools": ["fake_file_reader", "fake_calculator"],
    "expected": "40000",
    "checker": "exact_match"
})

tasks.append({
    "id": "t18",
    "type": "file_data",
    "length": "short",
    "instruction": "Use fake_file_reader to read 'budget.txt'. Extract the remaining budget number. Return only the number.",
    "tools": ["fake_file_reader"],
    "expected": "55000",
    "checker": "exact_match"
})

tasks.append({
    "id": "t19",
    "type": "file_data",
    "length": "short",
    "instruction": "Use fake_file_reader to read 'employees.csv'. Count how many employees are listed (excluding the header). Return only the count.",
    "tools": ["fake_file_reader"],
    "expected": "4",
    "checker": "exact_match"
})

# Medium
tasks.append({
    "id": "t20",
    "type": "file_data",
    "length": "medium",
    "instruction": "Step 1: Use fake_file_reader to read 'employees.csv'. Step 2: Use fake_calculator to find the average salary. Step 3: Return only the average as a number.",
    "tools": ["fake_file_reader", "fake_calculator"],
    "expected": "68750",
    "checker": "exact_match"
})

tasks.append({
    "id": "t21",
    "type": "file_data",
    "length": "medium",
    "instruction": "Step 1: Use fake_file_reader to read 'products.csv'. Step 2: Use fake_calculator to calculate total stock value (price multiplied by stock for each item, then sum all). Return only the total.",
    "tools": ["fake_file_reader", "fake_calculator"],
    "expected": "6500",
    "checker": "exact_match"
})

tasks.append({
    "id": "t22",
    "type": "file_data",
    "length": "medium",
    "instruction": "Step 1: Use fake_file_reader to read 'grades.csv'. Step 2: Find the highest math score. Step 3: Return only the score number.",
    "tools": ["fake_file_reader"],
    "expected": "92",
    "checker": "exact_match"
})

# Long
tasks.append({
    "id": "t06",
    "type": "file_data",
    "length": "long",
    "instruction": "Step 1: Use fake_file_reader to read 'products.csv'. Step 2: Calculate total value of all stock (price multiplied by stock for each item, then sum). Step 3: Read 'budget.txt' and find the remaining budget number. Step 4: Return 'YES' if total stock value fits in the remaining budget, otherwise return 'NO'.",
    "tools": ["fake_file_reader", "fake_calculator"],
    "expected": "YES",
    "checker": "exact_match"
})

tasks.append({
    "id": "t23",
    "type": "file_data",
    "length": "long",
    "instruction": "Step 1: Use fake_file_reader to read 'employees.csv'. Step 2: Identify employees with salary greater than 60000. Step 3: Count how many such employees exist. Step 4: Return only the count.",
    "tools": ["fake_file_reader", "fake_calculator"],
    "expected": "2",
    "checker": "exact_match"
})

tasks.append({
    "id": "t24",
    "type": "file_data",
    "length": "long",
    "instruction": "Step 1: Use fake_file_reader to read 'grades.csv'. Step 2: Calculate total score (math + science) for each student. Step 3: Find the student with the highest total. Step 4: Return only the student's name.",
    "tools": ["fake_file_reader", "fake_calculator"],
    "expected": "Hina",
    "checker": "exact_match"
})

# ============================================================
# TYPE 3: BOOKING / SHOPPING (9 tasks)
# ============================================================

# Short
tasks.append({
    "id": "t03",
    "type": "booking_shopping",
    "length": "short",
    "instruction": "Use fake_search to find the flight code for Lahore to Karachi on 2026-08-15. Then use fake_booking_api to book it. Return only the confirmation message.",
    "tools": ["fake_search", "fake_booking_api"],
    "expected": "Booking confirmed for flight PK05X9. Price: 15000 PKR.",
    "checker": "exact_match"
})

tasks.append({
    "id": "t25",
    "type": "booking_shopping",
    "length": "short",
    "instruction": "Use fake_search to find the price of flight UAE12A. Return only the price number.",
    "tools": ["fake_search"],
    "expected": "45000",
    "checker": "exact_match"
})

tasks.append({
    "id": "t26",
    "type": "booking_shopping",
    "length": "short",
    "instruction": "Use fake_search to find the flight code for Karachi to Lahore on 2026-08-18. Return only the code.",
    "tools": ["fake_search"],
    "expected": "PK18B2",
    "checker": "exact_match"
})

# Medium
tasks.append({
    "id": "t08",
    "type": "booking_shopping",
    "length": "medium",
    "instruction": "Step 1: Use fake_search to find all flights. Step 2: Use fake_calculator to find the cheapest flight price. Step 3: Return only the flight code of the cheapest flight.",
    "tools": ["fake_search", "fake_calculator"],
    "expected": "PK18B2",
    "checker": "exact_match"
})

tasks.append({
    "id": "t27",
    "type": "booking_shopping",
    "length": "medium",
    "instruction": "Step 1: Use fake_search to find the cheapest flight. Step 2: Use fake_booking_api to book that flight. Step 3: Check if the price is under 55000. Return 'YES' if under budget, else 'NO'.",
    "tools": ["fake_search", "fake_booking_api", "fake_calculator"],
    "expected": "YES",
    "checker": "exact_match"
})

tasks.append({
    "id": "t28",
    "type": "booking_shopping",
    "length": "medium",
    "instruction": "Step 1: Use fake_search to find all flights. Step 2: Use fake_calculator to find the most expensive flight price. Step 3: Return only the flight code of the most expensive flight.",
    "tools": ["fake_search", "fake_calculator"],
    "expected": "UAE12A",
    "checker": "exact_match"
})

# Long
tasks.append({
    "id": "t29",
    "type": "booking_shopping",
    "length": "long",
    "instruction": "Step 1: Use fake_search to find the cheapest flight. Step 2: Extract its code and price. Step 3: Use fake_booking_api to book it. Step 4: Return the result in exact format: 'CODE, PRICE, CONFIRMED' where CONFIRMED is 'YES' if booking succeeded.",
    "tools": ["fake_search", "fake_booking_api"],
    "expected": "PK18B2, 12000, YES",
    "checker": "exact_match"
})

tasks.append({
    "id": "t30",
    "type": "booking_shopping",
    "length": "long",
    "instruction": "Step 1: Use fake_search to find the price of flight PK05X9. Step 2: Use fake_calculator to calculate the cost for 2 tickets. Step 3: Return only the total cost.",
    "tools": ["fake_search", "fake_calculator"],
    "expected": "30000",
    "checker": "exact_match"
})

tasks.append({
    "id": "t31",
    "type": "booking_shopping",
    "length": "long",
    "instruction": "Step 1: Use fake_search to find all flights under 20000 PKR. Step 2: Pick the first one found. Step 3: Use fake_booking_api to book it. Step 4: Return only the flight code.",
    "tools": ["fake_search", "fake_booking_api"],
    "expected": "PK18B2",
    "checker": "exact_match"
})

# ============================================================
# TYPE 4: REASONING / MATH (9 tasks)
# ============================================================

# Short
tasks.append({
    "id": "t04",
    "type": "reasoning_math",
    "length": "short",
    "instruction": "Use fake_calculator to compute (150 * 23) + 47. Return only the final number.",
    "tools": ["fake_calculator"],
    "expected": "3497",
    "checker": "exact_match"
})

tasks.append({
    "id": "t32",
    "type": "reasoning_math",
    "length": "short",
    "instruction": "Use fake_calculator to compute 1000 divided by 4 plus 25. Return only the final number.",
    "tools": ["fake_calculator"],
    "expected": "275",
    "checker": "exact_match"
})

tasks.append({
    "id": "t33",
    "type": "reasoning_math",
    "length": "short",
    "instruction": "Use fake_calculator to compute 15 percent of 200. Return only the final number.",
    "tools": ["fake_calculator"],
    "expected": "30",
    "checker": "exact_match"
})

# Medium
tasks.append({
    "id": "t07",
    "type": "reasoning_math",
    "length": "medium",
    "instruction": "Step 1: Use fake_file_reader to read 'grades.csv'. Step 2: Use fake_calculator to find the average math score. Step 3: Use fake_calculator to find the average science score. Step 4: Return the name of the subject with the higher average (math or science).",
    "tools": ["fake_file_reader", "fake_calculator"],
    "expected": "science",
    "checker": "exact_match"
})

tasks.append({
    "id": "t34",
    "type": "reasoning_math",
    "length": "medium",
    "instruction": "Step 1: Use fake_file_reader to read 'employees.csv'. Step 2: Use fake_calculator to find the total payroll (sum of all salaries). Step 3: Return only the total.",
    "tools": ["fake_file_reader", "fake_calculator"],
    "expected": "275000",
    "checker": "exact_match"
})

tasks.append({
    "id": "t35",
    "type": "reasoning_math",
    "length": "medium",
    "instruction": "Step 1: Use fake_file_reader to read 'employees.csv'. Step 2: Use fake_calculator to find the average salary. Step 3: Use fake_calculator to multiply the average salary by 2. Step 4: Return only the final number.",
    "tools": ["fake_file_reader", "fake_calculator"],
    "expected": "137500",
    "checker": "exact_match"
})

# Long
tasks.append({
    "id": "t36",
    "type": "reasoning_math",
    "length": "long",
    "instruction": "Step 1: Use fake_file_reader to read 'products.csv'. Step 2: Use fake_calculator to find total stock value. Step 3: Use fake_file_reader to read 'budget.txt' and extract total budget (100000). Step 4: Use fake_calculator to divide total budget by total stock value. Step 5: Return only the integer part (floor) of the result.",
    "tools": ["fake_file_reader", "fake_calculator"],
    "expected": "15",
    "checker": "exact_match"
})

tasks.append({
    "id": "t37",
    "type": "reasoning_math",
    "length": "long",
    "instruction": "Step 1: Use fake_file_reader to read 'products.csv'. Step 2: For each product, use fake_calculator to divide price by stock to get price per unit. Step 3: Find the product with the lowest price per unit. Step 4: Return only the product name.",
    "tools": ["fake_file_reader", "fake_calculator"],
    "expected": "Mouse",
    "checker": "exact_match"
})

tasks.append({
    "id": "t38",
    "type": "reasoning_math",
    "length": "long",
    "instruction": "Step 1: Use fake_file_reader to read 'employees.csv'. Step 2: Use fake_calculator to find total payroll. Step 3: Use fake_calculator to calculate 10 percent of total payroll. Step 4: Use fake_file_reader to read 'products.csv'. Step 5: Use fake_calculator to find total stock value. Step 6: Use fake_calculator to add the 10 percent payroll to the total stock value. Return only the final number.",
    "tools": ["fake_file_reader", "fake_calculator"],
    "expected": "34000",
    "checker": "exact_match"
})

# ============================================================
# TYPE 5: TEAM TASKS (9 tasks) - For CrewAI + AutoGen only
# ============================================================

# Short
tasks.append({
    "id": "t39",
    "type": "team",
    "length": "short",
    "instruction": "Writer Agent: Write exactly 'Hello World'. Reviewer Agent: Confirm it is exactly 'Hello World'. Return only the final confirmed text.",
    "tools": ["fake_file_reader"],
    "expected": "Hello World",
    "checker": "exact_match"
})

tasks.append({
    "id": "t40",
    "type": "team",
    "length": "short",
    "instruction": "Writer Agent: Write a 5-word sentence about Pakistan. Reviewer Agent: Count the words. If exactly 5, return the sentence. If not, return 'REJECTED'. Return only the final result.",
    "tools": ["fake_file_reader"],
    "expected": "Pakistan is a beautiful country",
    "checker": "contains_substring"
})

tasks.append({
    "id": "t41",
    "type": "team",
    "length": "short",
    "instruction": "Writer Agent: Write 'AI agents are useful'. Reviewer Agent: Check that the text contains 'AI'. If yes, return the text. If no, return 'REJECTED'. Return only the final result.",
    "tools": ["fake_file_reader"],
    "expected": "AI agents are useful",
    "checker": "exact_match"
})

# Medium
tasks.append({
    "id": "t42",
    "type": "team",
    "length": "medium",
    "instruction": "Writer Agent: Summarize the following in exactly 3 words: 'The capital of Pakistan is Islamabad and it is beautiful.' Reviewer Agent: Count the words in the summary. If exactly 3, return the summary. If not, return 'REJECTED'. Return only the final result.",
    "tools": ["fake_file_reader"],
    "expected": "Capital is Islamabad",
    "checker": "exact_match"
})

tasks.append({
    "id": "t43",
    "type": "team",
    "length": "medium",
    "instruction": "Writer Agent: Read 'employees.csv' and list all employee names separated by commas. Reviewer Agent: Check that all 4 names (Ali, Sara, Zain, Noor) are present. If yes, return the list. If no, return 'REJECTED'. Return only the final result.",
    "tools": ["fake_file_reader"],
    "expected": "Ali, Sara, Zain, Noor",
    "checker": "contains_substring"
})

tasks.append({
    "id": "t44",
    "type": "team",
    "length": "medium",
    "instruction": "Writer Agent: Calculate 100 plus 200. Reviewer Agent: Verify the answer is 300. If correct, return '300'. If wrong, return 'REJECTED'. Return only the final result.",
    "tools": ["fake_calculator"],
    "expected": "300",
    "checker": "exact_match"
})

# Long
tasks.append({
    "id": "t45",
    "type": "team",
    "length": "long",
    "instruction": "Writer Agent: Read 'budget.txt' and extract the remaining budget number. Reviewer Agent: Verify the number is 55000. If correct, return '55000'. If wrong, return 'REJECTED'. Return only the final result.",
    "tools": ["fake_file_reader"],
    "expected": "55000",
    "checker": "exact_match"
})

tasks.append({
    "id": "t46",
    "type": "team",
    "length": "long",
    "instruction": "Writer Agent: Use fake_search to find the cheapest flight code. Reviewer Agent: Verify the code is PK18B2. If correct, return 'PK18B2'. If wrong, return 'REJECTED'. Return only the final result.",
    "tools": ["fake_search"],
    "expected": "PK18B2",
    "checker": "exact_match"
})

tasks.append({
    "id": "t47",
    "type": "team",
    "length": "long",
    "instruction": "Writer Agent: Read 'products.csv' and find the product with the highest price. Reviewer Agent: Verify the answer is 'Laptop'. If correct, return 'Laptop'. If wrong, return 'REJECTED'. Return only the final result.",
    "tools": ["fake_file_reader"],
    "expected": "Laptop",
    "checker": "exact_match"
})

# ============================================================
# WRITE ALL FILES
# ============================================================
for task in tasks:
    filepath = os.path.join(tasks_dir, f"{task['id']}.json")
    with open(filepath, "w") as f:
        json.dump(task, f, indent=2)
    print(f"Created {filepath}")

print(f"\n✅ Done! Created {len(tasks)} task files in {tasks_dir}/")
print("Next: Run python runner/manual_test.py to validate all tasks.")
