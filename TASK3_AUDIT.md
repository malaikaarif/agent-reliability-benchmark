# Task 3 audit: checker/format contradiction, t08, t28

## Checker findings
1. Paper Eq. 1 says: case-insensitive, pass if exact OR substring. Code did: one checker per task (34 exact, 17 substring), case-sensitive. t34, t39, t41 are all `exact_match`, so extra text or quotes fail them.
2. Literal Eq. 1 is too lenient: expected "2" would match inside "12"; t41 "AI agents are useful REJECTED" would pass although the reviewer rejected it. Fixed with whole-token containment and a `forbidden` field on t41.
3. Rescoring existing logs (python rescore.py), legacy -> Eq. 1:
   - AutoGen baseline (919 runs): 56.4% -> 58.4% (legacy reproduces the paper's 56.4%)
   - LangGraph (107 logs in logs/): 50.5% -> 61.7%
   - CrewAI (54 logs in logs/): 57.4% -> 57.4%
   All baseline AND ARW numbers must be rescored with the same checker before computing deltas.

## t34, t39, t41 (what the logs show)
- t39 LangGraph: answer is "Hello World" in quotes -> format only. Passes under Eq. 1.
- t34 LangGraph: "Return only the total payroll, which is 275000." -> format only. Passes under Eq. 1.
- t34 AutoGen: always "222950" (true sum is 275000) -> a wrong-value error, NOT a format error. Table X's "t34 = format violation" holds only for LangGraph.
- t41 AutoGen: often "... REJECTED" -> wrong answer, not format.

## t08 and t28
- Paper says they fail 100% of runs. Logs: AutoGen passes ~100% on both, CrewAI passes at least once, LangGraph returns an empty answer every time.
- Manual solvability: search "all flights" returns all 3 flights; cheapest PK18B2 (12000), most expensive UAE12A (45000). Solvable. Keep both tasks; do not remove.
- So it is a LangGraph adapter/model problem, not a benchmark defect. The paper's "structural crash in all frameworks" wording is wrong.
- Cause not confirmed (needs Ollama): in langgraph_adapter.py the final message content is empty. Next step: for t08/t28 dump result["messages"] and see whether the last AIMessage is empty after the tool call. The system prompt also only hints "flights from lahore", not "all flights", which differs from the other adapters (prompt parity, Iqra's task 4).

## Other things noticed
- Task IDs in the repo do not match the paper's ranges (paper: t01-t09 web ... ; repo has no t09/t10 and category counts are 11/11/10/10/9, not 9 each).
- t01-t06 each have two JSON variants (short/long) with different checkers; scorers read tasks/{id}.json.
- Repo has 107 LangGraph logs in logs/ vs 294 in the paper (relevant to task 5 log policy).