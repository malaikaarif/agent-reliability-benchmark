# CrewAI Benchmark Results (t01–t47)

| t01 | web | short | PASS | - | |
| t02 | file | short | PASS | - | |
| t03 | booking | short | FAIL | Tool Misuse | Never called booking API correctly |
| t04 | reasoning | short | PASS | - | |
| t05 | web | medium | FAIL | Hallucination | Wrong math: got 1845 instead of 237 |
| t06 | file | long | FAIL | Wrong Planning | Wrong comparison: got NO instead of YES |
| t07 | reasoning | medium | FAIL | Wrong Planning | Wrong subject: got math instead of science |
| t08 | booking | medium | FAIL | Wrong Tool Selection | Picked PK05X9 instead of PK18B2 |
| t11 | web | short | PASS | - | |
| t12 | web | short | PASS | - | |
| t13 | web | medium | PASS | - | Checker fixed (quote formatting) |
| t14 | web | medium | PASS | - | |
| t15 | web | long | FAIL | Hallucination | Wrong calculation: got 85937880 instead of 3318 |
| t16 | web | long | FAIL | Wrong Planning | Wrong sort: got POT instead of IPT |
| t17 | web | long | FAIL | Hallucination | Wrong count: got 3 instead of 2 |
| t18 | file | short | PASS | - | |
| t19 | file | short | PASS | - | |
| t20 | file | medium | PASS | - | |
| t21 | file | medium | PASS | - | |
| t22 | file | medium | FAIL | Recovery Failure | CrewAI crashed: "Invalid response from LLM" |
| t23 | file | long | PASS | - | |
| t24 | file | long | PASS | - | |
| t25 | booking | short | PASS | - | |
| t26 | booking | short | PASS | - | |
| t27 | booking | medium | FAIL | Wrong Planning | Wrong budget check: got NO instead of YES |
| t28 | booking | medium | PASS | - | |
| t29 | booking | long | PASS | - | Checker fixed (PKR in output) |
| t30 | booking | long | PASS | - | |
| t31 | booking | long | FAIL | Premature Stopping | Gave up: got N/A instead of PK18B2 |
| t32 | reasoning | short | PASS | - | |
| t33 | reasoning | short | PASS | - | |
| t34 | reasoning | medium | PASS | - | |
| t35 | reasoning | medium | PASS | - | |
| t36 | reasoning | long | FAIL | Hallucination | Wrong math: got 8 instead of 15 |
| t37 | reasoning | long | FAIL | Wrong Planning | Wrong product: got Keyboard instead of Mouse |
| t38 | reasoning | long | FAIL | Hallucination | Wrong total: got 8400 instead of 34000 |
| t39 | team | short | PASS | - | |
| t40 | team | short | FAIL | Multi-Agent Disagreement | Writer + reviewer conflict: REJECTED |
| t41 | team | short | PASS | - | |
| t42 | team | medium | FAIL | Multi-Agent Disagreement | Writer + reviewer conflict: REJECTED |
| t43 | team | medium | PASS | - | Checker fixed (spacing issue) |
| t44 | team | medium | PASS | - | |
| t45 | team | long | FAIL | Recovery Failure | CrewAI crashed: "Invalid response from LLM" |
| t46 | team | long | PASS | - | |
| t47 | team | long | FAIL | Recovery Failure | CrewAI crashed: "Invalid response from LLM" |


















## Summary
## Summary
- Total tasks: 47
- PASS: 25
- FAIL (real weaknesses): 19
- Framework crashes: 3 (t22, t45, t47)
- Top failure categories:
  - Hallucination (6): t05, t15, t17, t19, t36, t38
  - Wrong Planning (5): t06, t07, t08, t16, t27, t37
  - Recovery Failure (3): t22, t45, t47
  - Multi-Agent Disagreement (2): t40, t42
  - Tool Misuse (1): t03
  - Premature Stopping (1): t31