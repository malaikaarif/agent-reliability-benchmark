# LangGraph + ARW Benchmark Results

Scored 90 runs (45 tasks x 2 repeats) using tasks/checkers/checkers.py.

| Task | Repeat | Result | ARW Fallback | Retries | Crashed Before ARW | Final Answer |
|------|--------|--------|--------------|---------|--------------------|--------------|
| t01 | 1 | PASS | no | 0 | no | Islamabad |
| t01 | 2 | PASS | no | 0 | no | Islamabad |
| t02 | 1 | PASS | no | 0 | no | 40000 |
| t02 | 2 | PASS | no | 0 | no | 40000 |
| t03 | 1 | PASS | no | 0 | no | Confirmation message for booking flight PK05X9: Booking conf |
| t03 | 2 | PASS | no | 0 | no | Confirmation message for booking flight PK05X9: Booking conf |
| t04 | 1 | PASS | no | 0 | no | 3497 |
| t04 | 2 | PASS | no | 0 | no | 3497 |
| t05 | 1 | PASS | no | 0 | no | 237 |
| t05 | 2 | PASS | no | 0 | no | 1237 |
| t06 | 1 | FAIL | no | 0 | no | The total value of all stock is 6500 PKR. The remaining budg |
| t06 | 2 | FAIL | no | 0 | no | The total value of all stock is 6500 PKR and the remaining b |
| t07 | 1 | FAIL | no | 0 | no | The average math score is 85 and the average science score i |
| t07 | 2 | FAIL | no | 0 | no | The average math score is 85 and the average science score i |
| t08 | 1 | FAIL | yes | 4 | yes | [ARW_FALLBACK] No valid response after retries — routed to f |
| t08 | 2 | FAIL | yes | 4 | yes | [ARW_FALLBACK] No valid response after retries — routed to f |
| t11 | 1 | PASS | no | 0 | no | Paris |
| t11 | 2 | PASS | no | 0 | no | Paris |
| t12 | 1 | FAIL | no | 0 | no | Yen |
| t12 | 2 | FAIL | no | 0 | no | Yen |
| t13 | 1 | PASS | no | 0 | no | '14 million, Japanese Yen' |
| t13 | 2 | PASS | no | 0 | no | '14 million, Japanese Yen' |
| t14 | 1 | PASS | no | 0 | no | Berlin, Paris, Tokyo |
| t14 | 2 | PASS | no | 0 | no | Berlin, Paris, Tokyo |
| t15 | 1 | FAIL | no | 0 | no | -131488 |
| t15 | 2 | FAIL | no | 0 | no | 0 |
| t16 | 1 | FAIL | no | 0 | no | PIJ |
| t16 | 2 | FAIL | no | 0 | no | PIJ |
| t17 | 1 | PASS | no | 0 | no | 2 |
| t17 | 2 | PASS | no | 0 | no | 2 |
| t18 | 1 | PASS | no | 0 | no | 55000 |
| t18 | 2 | PASS | no | 0 | no | 55000 |
| t19 | 1 | FAIL | no | 0 | no | 3 |
| t19 | 2 | FAIL | no | 0 | no | 3 |
| t20 | 1 | PASS | no | 0 | no | 68750 |
| t20 | 2 | PASS | no | 0 | no | 68750 |
| t21 | 1 | PASS | no | 0 | no | 6500 |
| t21 | 2 | PASS | no | 0 | no | 6500 |
| t22 | 1 | PASS | no | 0 | no | 92 |
| t22 | 2 | PASS | no | 0 | no | 92 |
| t23 | 1 | PASS | no | 1 | yes | 2 |
| t23 | 2 | PASS | no | 0 | no | 2 |
| t24 | 1 | PASS | no | 0 | no | Hina |
| t24 | 2 | FAIL | no | 0 | no | Sorry, need more steps to process this request. |
| t25 | 1 | PASS | no | 0 | no | 45000 |
| t25 | 2 | PASS | no | 0 | no | 45000 |
| t26 | 1 | PASS | no | 0 | no | PK18B2 |
| t26 | 2 | PASS | no | 0 | no | PK18B2 |
| t27 | 1 | FAIL | no | 0 | no | Check if the price is under 55000 PKR. |
| t27 | 2 | FAIL | yes | 4 | yes | [ARW_FALLBACK] No valid response after retries — routed to f |
| t28 | 1 | FAIL | yes | 4 | yes | [ARW_FALLBACK] No valid response after retries — routed to f |
| t28 | 2 | FAIL | yes | 4 | yes | [ARW_FALLBACK] No valid response after retries — routed to f |
| t29 | 1 | FAIL | no | 0 | no | "PK05X9, 15000 PKR, YES" |
| t29 | 2 | FAIL | no | 0 | no | "PK05X9, 15000 PKR, YES" |
| t30 | 1 | PASS | no | 0 | no | 30000 |
| t30 | 2 | PASS | no | 0 | no | 30000 |
| t31 | 1 | FAIL | no | 0 | no | "PK05X9" |
| t31 | 2 | FAIL | no | 0 | no | Since no flights were found under 20000 PKR, we cannot proce |
| t32 | 1 | PASS | no | 0 | no | 275 |
| t32 | 2 | PASS | no | 0 | no | 275 |
| t33 | 1 | PASS | no | 0 | no | 30 |
| t33 | 2 | PASS | no | 0 | no | 30 |
| t34 | 1 | FAIL | no | 0 | no | Return only the total payroll, which is 275000. |
| t34 | 2 | FAIL | no | 0 | no | Return only the total payroll, which is 275000. |
| t35 | 1 | PASS | no | 0 | no | 137500 |
| t35 | 2 | PASS | no | 0 | no | 137500 |
| t36 | 1 | FAIL | no | 0 | no | 8 |
| t36 | 2 | FAIL | no | 0 | no | 8 |
| t37 | 1 | FAIL | no | 0 | no | The lowest price per unit is for the Mouse with a value of 0 |
| t37 | 2 | FAIL | no | 0 | no | The calculations for price per unit are as follows:
- Laptop |
| t38 | 1 | FAIL | no | 0 | no | 467500 |
| t38 | 2 | FAIL | no | 0 | no | 467500.0 |
| t39 | 1 | FAIL | no | 0 | no | "Hello World" |
| t39 | 2 | FAIL | no | 0 | no | "Hello World" |
| t40 | 1 | FAIL | no | 0 | no | REJECTED |
| t40 | 2 | FAIL | no | 0 | no | REJECTED |
| t41 | 1 | FAIL | no | 0 | no | "AI agents are useful" contains 'AI', so the result is:

AI  |
| t41 | 2 | FAIL | no | 0 | no | "AI agents are useful" contains 'AI', so the result is:

AI  |
| t42 | 1 | FAIL | no | 0 | no | REJECTED |
| t42 | 2 | FAIL | no | 0 | no | REJECTED |
| t43 | 1 | FAIL | no | 0 | no | Ali, Sara, Zain, Noor |
| t43 | 2 | FAIL | no | 0 | no | Ali, Sara, Zain, Noor |
| t44 | 1 | PASS | no | 0 | no | 300 |
| t44 | 2 | PASS | no | 0 | no | 300 |
| t45 | 1 | PASS | no | 0 | no | 55000 |
| t45 | 2 | PASS | no | 0 | no | 55000 |
| t46 | 1 | FAIL | no | 0 | no | PK18B2 
REJECTED |
| t46 | 2 | FAIL | no | 0 | no | PK18B2 
REJECTED |
| t47 | 1 | PASS | no | 0 | no | Laptop |
| t47 | 2 | PASS | no | 0 | no | Laptop |

## Summary

- Total runs: 90
- Passed: 47 (52.2%)
- Failed: 43 (47.8%)
- ARW fallback triggered (would've crashed/emptied pre-ARW): 5 (5.6%)
- Runs that failed on the very first attempt but recovered via retry: 1
- Total retries consumed across all runs: 21
