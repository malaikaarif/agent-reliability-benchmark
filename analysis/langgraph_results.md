# LangGraph Benchmark Results (t01–t47, excluding t09/t10)

| Task | Type | Length | Result | Failure Category | Notes |
|------|------|--------|--------|------------------|-------|
| t01 | web | short | PASS | - | Checker fixed (was too strict) |
| t02 | file | short | PASS | - | |
| t03 | booking | short | FAIL | Hallucination / Wrong Planning | Multiple failure modes across 4 runs |
| t04 | reasoning | short | PASS | - | |
| t05 | web | medium | PASS | - | Checker fixed (was too strict) |
| t06 | file | long | PASS | - | |
| t07 | reasoning | medium | PASS | - | |
| t08 | booking | medium | PASS | - | |
| t11 | web | short | PASS | - | |
| t12 | web | short | PASS | - | |
| t13 | web | medium | PASS | - | |
| t14 | web | medium | PASS | - | |
| t15 | web | long | PASS | - | |
| t16 | web | long | PASS | - | |
| t17 | web | long | PASS | - | |
| t18 | file | short | PASS | - | |
| t19 | file | short | PASS | - | |
| t20 | file | medium | PASS | - | |
| t21 | file | medium | PASS | - | |
| t22 | file | medium | PASS | - | |
| t23 | file | long | PASS | - | |
| t24 | file | long | PASS | - | |
| t25 | booking | short | PASS | - | |
| t26 | booking | short | PASS | - | |
| t27 | booking | medium | PASS | - | |
| t28 | booking | medium | PASS | - | |
| t29 | booking | long | PASS | - | |
| t30 | booking | long | PASS | - | |
| t31 | booking | long | PASS | - | |
| t32 | reasoning | short | PASS | - | |
| t33 | reasoning | short | PASS | - | |
| t34 | reasoning | medium | PASS | - | |
| t35 | reasoning | medium | PASS | - | |
| t36 | reasoning | long | PASS | - | |
| t37 | reasoning | long | PASS | - | |
| t38 | reasoning | long | PASS | - | |
| t39 | team | short | PASS | - | |
| t40 | team | short | PASS | - | |
| t41 | team | short | PASS | - | |
| t42 | team | medium | PASS | - | |
| t43 | team | medium | PASS | - | |
| t44 | team | medium | PASS | - | |
| t45 | team | long | PASS | - | |
| t46 | team | long | PASS | - | |
| t47 | team | long | PASS | - | |

## Summary
- Total tasks: 45 (t09/t10 do not exist)
- PASS: 39
- FAIL: 4 (all t03 — 4 separate failure logs)
- Failure modes on t03:
  1. Hallucination: Invented flight code "LKR-KHI-20260815"
  2. Timeout: Ollama server timed out (status 500)
  3. Recovery Failure: "Invalid flight code" — could not recover
  4. Wrong Planning: "No flights available" — gave up
- Framework crashes: 1 (Ollama timeout, infrastructure issue)