# Crewai + ARW Benchmark Results

Scored 68 runs (34 tasks x 2 repeats) using tasks/checkers/checkers.py.

| Task | Repeat | Result | ARW Fallback | Retries | Crashed Before ARW | Final Answer |
|------|--------|--------|--------------|---------|--------------------|--------------|
| t01 | 1 | PASS | no | 0 | no | Islamabad |
| t01 | 2 | PASS | no | 0 | no | Islamabad |
| t02 | 1 | PASS | no | 0 | no | 40000 |
| t02 | 2 | PASS | no | 0 | no | 40000 |
| t03 | 1 | FAIL | no | 0 | no | Error: Flight code NO RESULTS not found. |
| t03 | 2 | FAIL | no | 0 | no | Error: Flight code NO RESULTS not found. |
| t04 | 1 | PASS | no | 0 | no | 3497 |
| t04 | 2 | PASS | no | 0 | no | 3497 |
| t05 | 1 | PASS | no | 0 | no | 237 |
| t05 | 2 | PASS | no | 0 | no | 237 |
| t06 | 1 | FAIL | no | 0 | no | {"name": "fake_calculator", "arguments": {"expression":"YES" |
| t06 | 2 | FAIL | no | 0 | no | NO |
| t07 | 1 | FAIL | no | 0 | no | "math" |
| t07 | 2 | FAIL | no | 0 | no | "math" |
| t08 | 1 | PASS | no | 0 | no | PK18B2 |
| t08 | 2 | FAIL | no | 0 | no | PK05X9 |
| t11 | 1 | PASS | no | 0 | no | Paris |
| t11 | 2 | PASS | no | 0 | no | Paris |
| t12 | 1 | PASS | no | 0 | no | Japanese Yen |
| t12 | 2 | PASS | no | 0 | no | Japanese Yen |
| t13 | 1 | PASS | no | 0 | no | '14 million, Japanese Yen' |
| t13 | 2 | PASS | no | 0 | no | '14 million, Japanese Yen' |
| t14 | 1 | PASS | no | 0 | no | Berlin, Paris, Tokyo |
| t14 | 2 | PASS | no | 0 | no | Berlin, Paris, Tokyo |
| t15 | 1 | FAIL | no | 0 | no | 143346 |
| t15 | 2 | FAIL | no | 0 | no | 143388 |
| t16 | 1 | FAIL | no | 0 | no | LPK |
| t16 | 2 | FAIL | no | 0 | no | PIT |
| t17 | 1 | FAIL | no | 0 | no | 11 |
| t17 | 2 | FAIL | no | 0 | no | 11 |
| t18 | 1 | PASS | no | 0 | no | 55000 |
| t18 | 2 | PASS | no | 0 | no | 55000 |
| t19 | 1 | FAIL | no | 0 | no | 3 |
| t19 | 2 | FAIL | no | 0 | no | 3 |
| t20 | 1 | PASS | no | 0 | no | 68750 |
| t20 | 2 | PASS | no | 0 | no | 68750 |
| t21 | 1 | PASS | no | 0 | no | 6500 |
| t21 | 2 | PASS | no | 0 | no | 6500 |
| t22 | 1 | FAIL | yes | 4 | yes | [ARW_FALLBACK] No valid response after retries — routed to f |
| t22 | 2 | FAIL | yes | 4 | yes | [ARW_FALLBACK] No valid response after retries — routed to f |
| t23 | 1 | PASS | no | 0 | no | 2 |
| t23 | 2 | FAIL | no | 0 | no | 25.0 |
| t24 | 1 | FAIL | no | 0 | no | "Ayesha" |
| t24 | 2 | FAIL | no | 0 | no | "Ayesha" |
| t25 | 1 | PASS | no | 0 | no | 45000 |
| t25 | 2 | PASS | no | 0 | no | 45000 |
| t26 | 1 | FAIL | no | 0 | no | None available. |
| t26 | 2 | FAIL | no | 0 | no | None |
| t27 | 1 | FAIL | no | 0 | no | NO |
| t27 | 2 | FAIL | no | 0 | no | NO |
| t28 | 1 | PASS | no | 0 | no | UAE12A |
| t28 | 2 | PASS | no | 0 | no | UAE12A |
| t29 | 1 | FAIL | no | 0 | no | PK18B2, 12000 PKR, YES |
| t29 | 2 | FAIL | no | 0 | no | PK18B2, 12000 PKR, YES |
| t30 | 1 | FAIL | no | 0 | no | 240 |
| t30 | 2 | FAIL | no | 0 | no | 240 |
| t31 | 1 | FAIL | no | 0 | no | NO_FLIGHT_FOUND |
| t31 | 2 | FAIL | no | 0 | no | NO_FLIGHT_FOUND |
| t32 | 1 | PASS | no | 0 | no | 275 |
| t32 | 2 | PASS | no | 0 | no | 275 |
| t33 | 1 | PASS | no | 0 | no | 30 |
| t33 | 2 | PASS | no | 0 | no | 30 |
| t34 | 1 | PASS | no | 0 | no | 275000 |
| t34 | 2 | PASS | no | 0 | no | 275000 |
| t35 | 1 | FAIL | no | 0 | no | 82500.0 |
| t35 | 2 | FAIL | no | 0 | no | 82500.0 |
| t36 | 1 | FAIL | no | 0 | no | 0 |
| t36 | 2 | FAIL | no | 0 | no | 2 |

## Summary

- Total runs: 68
- Passed: 34 (50.0%)
- Failed: 34 (50.0%)
- ARW fallback triggered: 2 (2.9%)
- Total retries consumed: 8
