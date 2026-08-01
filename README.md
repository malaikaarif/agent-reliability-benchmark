# Agent Reliability Benchmark

Cross-framework failure analysis of LLM agent frameworks (LangGraph, CrewAI, AutoGen, OpenAI Agents SDK).

## Structure
- `tasks/`  task definitions + correctness checkers
- `frameworks/`  per-framework adapter code
- `runner/`  script to run tasks across frameworks
- `logs/`  raw JSON logs of every run
- `annotation/`  human + AI-judge failure labels
- `analysis/`  metrics + statistics notebooks
- `report/`  final written report

## Team
- Malaika  frameworks, runner
- Iqra  tasks, annotation
