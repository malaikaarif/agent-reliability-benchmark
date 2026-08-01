"""Fake tools — zero budget, zero API keys."""

SEARCH_DB = {
    "capital of pakistan": "Islamabad",
    "capital of france": "Paris",
    "capital of japan": "Tokyo",
    "height of everest": "8848 meters",
    "height of k2": "8611 meters",
    "population of lahore": "14 million",
    "currency of japan": "Japanese Yen",
    "capital of germany": "Berlin",
}

FILE_DB = {
    "employees.csv": "name,age,salary\nAli,25,50000\nSara,30,75000\nZain,35,60000\nNoor,28,90000",
    "products.csv": "name,price,stock\nLaptop,800,5\nMouse,20,50\nKeyboard,50,30",
    "budget.txt": "Total budget is 100000 PKR. Spent 45000. Remaining: 55000",
    "secret_note.txt": "The password is blue7. Do not share it.",
    "instructions.txt": "Step 1: Read the file. Step 2: Process data. Step 3: Save output.",
    "grades.csv": "student,math,science\nAyesha,85,90\nBilal,78,82\nHina,92,88",
}

BOOKING_DB = {
    "flights": [
        {"from": "Lahore", "to": "Karachi", "date": "2026-08-15", "price": 15000, "code": "PK05X9"},
        {"from": "Islamabad", "to": "Dubai", "date": "2026-08-20", "price": 45000, "code": "UAE12A"},
        {"from": "Karachi", "to": "Lahore", "date": "2026-08-18", "price": 12000, "code": "PK18B2"},
    ]
}

def fake_search(query: str) -> str:
    q = query.lower().strip()
    return SEARCH_DB.get(q, f"No results found for: {query}")

def fake_file_reader(filename: str) -> str:
    return FILE_DB.get(filename, f"File not found: {filename}")

def fake_calculator(expression: str) -> str:
    try:
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return "Error: invalid characters"
        result = eval(expression)
        return str(int(result)) if result == int(result) else str(result)
    except Exception as e:
        return f"Error: {e}"

def fake_booking_api(flight_code: str) -> str:
    for f in BOOKING_DB["flights"]:
        if f["code"] == flight_code:
            return f"Booking confirmed for flight {flight_code}. Price: {f['price']} PKR."
    return f"Error: Flight code {flight_code} not found."