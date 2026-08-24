# 1. Introduction

AI agents built on large language models (LLMs) are increasingly deployed in production systems for tasks ranging from web browsing to database queries to multi-step reasoning [1,2]. However, these agents frequently fail in ways that are difficult to predict: they hallucinate facts, misuse tools, deviate from instructions, and crash on long tasks [3,4].

Existing benchmarks such as GAIA [5] and τ-bench [6] measure task completion accuracy but do not systematically compare how different agent architectures affect reliability. In particular, there is no empirical study comparing graph-based execution (LangGraph) against conversational multi-agent patterns (CrewAI, AutoGen) on the same tasks with the same evaluation protocol.

We hypothesize that graph-based execution achieves higher reliability because it maintains deterministic state transitions, whereas conversational multi-agent frameworks introduce coordination failures between agents. To test this, we build a benchmark of 45 tasks across 5 categories and evaluate 3 popular frameworks.

Our contributions:
1. A reproducible 45-task benchmark with fake tools, auto-checkers, and a validated failure taxonomy
2. The first head-to-head comparison of LangGraph, CrewAI, and AutoGen on identical tasks
3. A novel finding: AutoGen's built-in reviewer agent systematically rejects correct outputs, a failure mode not reported in existing taxonomies










# 2. Related Work

## 2.1 Failure Taxonomies for AI Agents

The Multi-Agent System Failure Taxonomy (MAST) [1] introduced by UC Berkeley in 2025 is the first empirically grounded taxonomy of MAS failures, derived from 150+ execution traces across 5 frameworks. MAST identifies 14 fine-grained failure modes organized into 3 categories: Specification & System Design, Inter-Agent Misalignment, and Task Verification & Termination. Their automated annotator achieved 94% accuracy and Cohen's Kappa of 0.77 against human experts. Our 11-category taxonomy maps directly to MAST but adds granularity for framework-specific failures such as AutoGen's reviewer over-rejection.

## 2.2 Agent Benchmarks

GAIA [2] evaluates general-purpose AI assistants on web browsing, file manipulation, and multi-step reasoning tasks. τ-bench [3] focuses on customer service simulation with consequential actions such as refunds and booking modifications. While these benchmarks measure task completion accuracy, they do not systematically compare how different agent architectures affect reliability on identical tasks. Our benchmark fills this gap by holding the task constant while varying the framework.

## 2.3 Agent Frameworks

LangGraph [4] implements graph-based execution where nodes represent tools or reasoning steps and edges define deterministic state transitions. CrewAI [5] adopts a team-based conversational pattern where specialized agents collaborate via role-based delegation. AutoGen [6] enables multi-agent conversation with built-in reviewer and critic agents. Prior work has evaluated these frameworks independently [7,8] but no study has compared their reliability head-to-head on the same benchmark with a shared failure taxonomy.

## 2.4 Gap

Despite the maturity of individual benchmarks and frameworks, there is no empirical study comparing graph-based execution against conversational multi-agent patterns on identical tasks with trajectory-level failure analysis. We address this gap.



Section 3: Methodology (~600 words)
Task design (45 tasks, 5 categories)
Fake tools (why zero cost, deterministic)
Evaluation protocol (exact_match + contains_substring)
Failure taxonomy (11 categories, manual validation)
Framework adapters (how each was implemented)





# 3. Methodology

## 3.1 Benchmark Design

We construct a benchmark of 45 tasks spanning 5 categories: web search (t01–t09), file manipulation (t10–t18), booking and transactions (t19–t27), mathematical reasoning (t28–t36), and team coordination (t37–t47). Tasks are defined as JSON objects containing a natural language instruction, expected output, and evaluation criteria. Task complexity ranges from single-tool calls (e.g., "What is the capital of Pakistan?") to multi-step chains requiring tool composition and reasoning (e.g., booking a flight and calculating total cost).

## 3.2 Fake Tools

To ensure deterministic, zero-cost evaluation, we implement fake tools that simulate real APIs without external dependencies:
- `fake_search`: Returns pre-defined knowledge-base entries for queries
- `fake_file_reader`: Reads local CSV and text files
- `fake_calculator`: Evaluates arithmetic expressions
- `fake_booking_api`: Simulates flight/hotel booking with confirmation codes

These tools return consistent outputs, eliminating non-determinism from external API latency, rate limits, or changing data.

## 3.3 Evaluation Protocol

Each task is evaluated by an auto-checker implementing two strategies:
- `exact_match`: String equality between agent output and expected answer
- `contains_substring`: Expected answer appears within agent output

A task is marked PASS if either check succeeds. This balances strict correctness with tolerance for formatting variations. All tasks were manually validated to confirm solvability.

## 3.4 Failure Taxonomy

We define 11 failure categories mapping to the MAST taxonomy [1]:
1. Tool Misuse — Wrong tool or arguments
2. Hallucination — Factually incorrect output
3. Math/Computation Error — Wrong calculation
4. Reasoning/Logic Error — Incorrect boolean or logical inference
5. Format Mismatch — Correct answer, wrong format
6. Reviewer Over-rejection — Correct answer rejected by critic agent
7. Wrong Planning — Incorrect task decomposition
8. Recovery Failure — Agent fails to recover from error
9. Context Loss — Forgets constraints mid-execution
10. Premature Termination — Stops before task complete
11. Framework Crash — Runtime exception or timeout

## 3.5 Framework Adapters

We implement lightweight adapters for each framework:
- **LangGraph**: Graph-based state machine with deterministic node transitions
- **CrewAI**: Role-based multi-agent team with conversational delegation
- **AutoGen**: Multi-agent conversation with built-in reviewer/critic agents

All adapters use the same underlying LLM (Qwen 2.5 7B via Ollama) to isolate framework architecture as the independent variable.

## 3.6 Experimental Protocol

Each framework executes all 45 tasks. For reliability measurement, we repeat each task twice, recording success consistency (PASS both times, FAIL both times, or MIXED). This yields 90 runs per framework for variance analysis.



# References

[1] MAST: Multi-Agent System Failure Taxonomy, UC Berkeley, 2025
[2] GAIA: A Benchmark for General AI Assistants, 2024
[3] τ-bench: A Benchmark for Tool-Agent-User Interaction, 2024
[4] LangGraph Documentation, LangChain, 2024
[5] CrewAI Documentation, 2024
[6] AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation, Microsoft, 2023
[7] (Find 1-2 papers that evaluate single frameworks)
[8] (Find 1-2 more)