# AutoGen Benchmark Results

## Summary
- Total logs: 112
- Total failures: 60
- Total passes: 52
- Pass rate: ~46%

## Failure Categories

| Category | Tasks | Count | Description |
|----------|-------|-------|-------------|
| Math/Computation Error | t05, t17, t19, t20, t21, t23, t34, t35, t36, t38 | ~20 | Wrong calculations |
| Reviewer Over-rejection | t40, t41, t42, t43, t45, t47 | ~14 | Agent rejected correct answers |
| Reasoning/Logic Error | t06, t27 | ~6 | Boolean/logic mistakes |
| Format Mismatch | t03, t12, t29, t37 | ~10 | Correct answer, wrong format |
| Hallucination | t16, t31 | ~4 | Wrong facts/codes |
| Tool Misuse | t01 | ~3 | Didn't execute tool |

## Notable Findings
1. AutoGen's reviewer agent rejects correct outputs (t40-t47)
2. Math errors are pervasive across 10+ tasks
3. t01 shows complete tool execution failure