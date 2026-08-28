<div align="center">

# 🤖 ARW — Adaptive Reliability Wrapper
### Diagnosing and Mitigating Reliability Failures in AI Agent Frameworks

*A lightweight, framework-agnostic reliability layer for LangGraph, CrewAI, and AutoGen — and what happens when the same fix doesn't work the same way twice.*

[![Paper Status](https://img.shields.io/badge/paper-under%20review-yellow)](.)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](.)
[![Model](https://img.shields.io/badge/model-Qwen%202.5%207B-purple)](.)
[![Ollama](https://img.shields.io/badge/Ollama-local%20inference-blue)](.)

**Authors:** Malaika Arif · Iqra Safdar · Yawar Abbas  
**Affiliation:** Department of Computer Science, COMSATS University Islamabad, Sahiwal Campus

</div>

---

## 📋 Table of Contents
- [🔥 The Core Problem](#-the-core-problem)
- [📊 The Benchmark](#-the-benchmark)
  - [Task Categories](#task-categories)
  - [Fake Tool Suite](#fake-tool-suite)
  - [Evaluation Protocol](#evaluation-protocol)
- [🏗️ Failure Taxonomy](#️-failure-taxonomy)
  - [Mapping to MAST](#mapping-to-mast)
  - [Baseline Failure Characterization](#baseline-failure-characterization)
- [⚙️ ARW: The Adaptive Reliability Wrapper](#️-arw-the-adaptive-reliability-wrapper)
  - [Design Philosophy](#design-philosophy)
  - [Three Mechanisms](#three-mechanisms)
  - [Architecture](#architecture)
  - [Algorithm 1: ARW Execution Procedure](#algorithm-1-arw-execution-procedure)
  - [Algorithm 2: Full ARW Pipeline](#algorithm-2-full-arw-pipeline)
  - [Equations & Formal Definitions](#equations--formal-definitions)
- [🔧 Framework Integration](#-framework-integration)
  - [Adapter Design](#adapter-design)
  - [Framework Characteristics](#framework-characteristics)
  - [CrewAI Integration Constraints](#crewai-integration-constraints)
- [📈 Results](#-results)
  - [Baseline Performance](#baseline-performance)
  - [ARW Performance](#arw-performance)
  - [LangGraph Failure Breakdown](#langgraph-failure-breakdown)
  - [Representative Failure Traces](#representative-failure-traces)
  - [Cross-Dataset Comparison](#cross-dataset-comparison)
- [💡 Key Findings & Discussion](#-key-findings--discussion)
  - [Framework-Dependent Effectiveness](#framework-dependent-effectiveness)
  - [Why ARW Helps AutoGen But Not LangGraph](#why-arw-helps-autogen-but-not-langgraph)
  - [Comparison with AgentTether](#comparison-with-agenttether)
  - [Limitations](#limitations)
  - [Future Work](#future-work)
- [📁 Repository Structure](#-repository-structure)
- [🚀 Reproducing Results](#-reproducing-results)
- [📚 Citation](#-citation)
- [📄 License](#-license)

---

## 🔥 The Core Problem

LLM-based agents are now routinely deployed on multi-step tasks that require tool use, planning, reasoning, and coordination — yet they fail unpredictably at both the **execution** and **model-output** levels.

| Failure Mode | What It Means | Clinical / Production Risk |
|:---|:---|:---|
| 🛠️ **Tool Misuse** | Wrong tool selected or incorrect arguments passed | Cascading errors in multi-step pipelines |
| 🧠 **Hallucination** | Factually incorrect output presented as truth | Wrong decisions based on fabricated data |
| 📐 **Math/Computation Error** | Wrong arithmetic or logic in reasoning chain | Financial, booking, or scientific miscalculations |
| 📝 **Format Mismatch** | Correct semantic answer, wrong syntactic format | Downstream parsers break, pipelines halt |
| 💥 **Infrastructure Crash** | Runtime exception or empty LLM response | Silent failures, resource leaks, hung processes |
| ⏹️ **Premature Termination** | Agent stops before task completion | Incomplete transactions, partial data writes |

> **The Gap:** Existing work characterizes these failures well (taxonomies, benchmarks), and recent runtime repair frameworks like **AgentTether** achieve strong single-agent recovery. But **nobody links observed failure patterns to targeted execution-level mitigations** — and **nobody tests whether the same repair mechanisms transfer across different agent frameworks.**

> **Our Question:** *Does the same lightweight repair mechanism actually work across LangGraph, CrewAI, and AutoGen — or does "reliability" mean something different depending on the framework you're wrapping?*

---

## 📊 The Benchmark

We built a **reproducible 45-task benchmark** covering five categories, using **deterministic fake tools** and **automated checkers** to isolate where reliability breaks down.

> **Why Fake Tools?** Real APIs introduce noise — rate limits change, services go down, responses vary — making it hard to know whether a failure belongs to the agent or the environment. Our deterministic tools remove API non-determinism entirely.

### Task Categories

#### Table IV — Task Categories and Complexity

| Category | Task IDs | Count | Example Task |
|:---|:---:|:---:|:---|
| **Web Search** | t01 – t09 | 9 | Find the capital of a country |
| **File Manipulation** | t10 – t18 | 9 | Read CSV, compute average |
| **Booking & Transactions** | t19 – t27 | 9 | Book flight + hotel together |
| **Math Reasoning** | t28 – t36 | 9 | Multi-step mathematical reasoning |
| **Team Coordination** | t37 – t45 | 9 | Delegate subtasks, merge outputs |
| **Total** | — | **45** | — |

Each task is stored as a JSON object containing:
- Natural-language instruction
- Expected output
- Evaluation criteria
- Required tools

Complexity varies from simple single-tool calls to multi-step chains demanding tool composition and intermediate reasoning.

### Fake Tool Suite

#### Table V — Fake Tool Suite

| Tool | Description | Return Type | Deterministic |
|:---|:---|:---:|:---:|
| `fake_search` | Pre-defined knowledge-base lookup | String | ✅ |
| `fake_file_reader` | Reads CSV/TXT files | String / JSON | ✅ |
| `fake_calculator` | Arithmetic evaluation | Number | ✅ |
| `fake_booking_api` | Flight/hotel booking simulation | Confirmation Code | ✅ |

### Evaluation Protocol

Every task is scored by an **automated checker** implementing two strategies:

1. **`exact_match`** — case-insensitive string equality between agent output and expected answer
2. **`contains_substring`** — expected answer appears anywhere inside the output

A task **passes** if either check succeeds. Before any framework was run, every task was manually validated to confirm it was actually solvable with the provided tools.

**Formal Scoring Function:**

```
                ⎧ 1   if a = e          (exact_match)
Pass(a, e) =    ⎨ 1   if e ⊆ a          (contains_substring)
                ⎩ 0   otherwise
```

Where equality and containment are evaluated after **case-insensitive normalization**.

#### Table II — Comparison of Agent Benchmarks

| Benchmark | Tasks | Real APIs | Cross-Framework | Taxonomy | Reproducible |
|:---|:---:|:---:|:---:|:---:|:---:|
| GAIA [2] | 466 | ✅ | ❌ | ❌ | ⚠️ Partial |
| τ-bench [3] | 189 | ✅ | ❌ | ❌ | ✅ |
| MAST [1] | — | — | ✅ (5 FW) | ✅ (14 cats) | ✅ |
| **Ours** | **45** | **❌** | **✅ (3 FW)** | **✅ (11 cats)** | **✅** |

---

## 🏗️ Failure Taxonomy

We define **11 failure categories** that map onto the MAST taxonomy [1], with additions for framework-specific failures encountered during pilot runs.

### Mapping to MAST

#### Table I — Mapping of Our Failure Taxonomy to MAST Categories

| Our Category | MAST Category | Description |
|:---|:---|:---|
| **Tool Misuse** | Spec. & System Design | Wrong tool or incorrect arguments |
| **Hallucination** | Task Verification & Term. | Factually incorrect output |
| **Math/Computation Error** | Spec. & System Design | Wrong arithmetic or logic |
| **Reasoning/Logic Error** | Task Verification & Term. | Incorrect boolean or causal inference |
| **Format Mismatch** | Spec. & System Design | Correct answer, wrong format |
| **Reviewer Over-rejection** | Inter-Agent Misalignment | Correct output rejected by critic |
| **Recovery Failure** | Inter-Agent Misalignment | Agent fails to recover from error |
| **Context Loss** | Inter-Agent Misalignment | Forgets constraints mid-execution |
| **Premature Termination** | Task Verification & Term. | Stops before task completion |
| **Framework Crash** | Spec. & System Design | Runtime exception or empty LLM response |
| **Timeout** | Spec. & System Design | Execution exceeded time limit |

> **Note:** Our taxonomy draws directly from MAST (UC Berkeley, 2025), which identified 14 fine-grained failure modes across 150+ execution traces. Their automated annotator agreed with human experts 94% of the time (Cohen's Kappa = 0.77).

### Baseline Failure Characterization

#### Figure 3 — Baseline Reliability Failure Distribution

```
Failure Proportion (%)
  │
 50┤        ┌───┐              ┌───┐              ┌───┐
   │        │ ▓▓│              │ ▓▓│              │▓▓▓│
   │        │ ▓▓│              │ ▓▓│              │▓▓▓│ 10.3%
   │        │ ▓▓│              │ ▓▓│              │▓▓▓│ Infra Crash
   │        │ ▓▓│ 5.4%         │ ▓▓│              │▓▓▓│
   │        │ ▓▓│ Empty        │ ▓▓│              │▓▓▓│
 40┤        │ ▓▓│ Answer       │ ▓▓│              │▓▓▓│
   │        │ ▓▓│              │ ▓▓│              │▓▓▓│
   │        │ ▓▓│              │ ▓▓│              │▓▓▓│
   │        │██▓│              │██▓│              │██▓│
   │        │██▓│ 38.4%        │██▓│ 43.5%        │██▓│ 23.0%
   │        │██▓│ Wrong        │██▓│ Wrong        │██▓│ Wrong
 30┤        │██▓│ Answer       │██▓│ Answer       │██▓│ Answer
   │        │██▓│              │██▓│              │██▓│
   │        │██▓│              │██▓│              │██▓│
   │        │██▓│              │██▓│              │██▓│
   │        │██▓│              │██▓│              │██▓│
 20┤        │██▓│              │██▓│              │██▓│
   │        │██▓│              │██▓│              │██▓│
   │        │██▓│              │██▓│              │██▓│
   │        │██▓│              │██▓│              │██▓│
   │        │██▓│              │██▓│              │██▓│
 10┤        │██▓│              │██▓│              │██▓│
   │        │██▓│              │██▓│              │██▓│
   │        │██▓│              │██▓│              │██▓│
   │        │██▓│              │██▓│              │██▓│
   │        │██▓│              │██▓│              │██▓│
  0┼────────┴───┴────────────┴───┴────────────┴───┴────────
            LangGraph          AutoGen            CrewAI
```

**Key Observations:**
- **Wrong answers dominate everywhere** — 38.4% (LangGraph), 43.5% (AutoGen), 23.0% (CrewAI)
- **Empty answers concentrated in LangGraph** — 5.4% of runs terminated before emitting output
- **Infrastructure crashes only in CrewAI** — 10.3% of runs returned `ValueError: Invalid response from LLM call - None or empty`
- **AutoGen and CrewAI almost never produce empty answers** — their conversational loops enforce a final response turn

---

## ⚙️ ARW: The Adaptive Reliability Wrapper

### Design Philosophy

> **Failure-Driven Design:** First characterize how agents break, then build targeted recovery mechanisms around those observations.

ARW is a **thin, framework-agnostic layer** that sits **outside** the agent execution loop and provides three services. It does **not** modify the framework's internal control flow.

### Three Mechanisms

| Mechanism | What It Catches | Design Trigger | Status |
|:---|:---|:---|:---|
| 🔁 **Retry-with-Backoff** | Transient empty/invalid LLM responses | CrewAI's 10.3% infra crashes | ✅ Evaluated |
| 🛡️ **Fallback Termination Guard** | Silent execution termination with no output | LangGraph's 5.4% empty answers | ✅ Evaluated |
| ⚖️ **Self-Consistency Verification** | Syntactically valid but semantically wrong answers | 23–53% wrong answers across frameworks | 🔄 Implemented, not yet evaluated |

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      BENCHMARK TASK                          │
│              (45 tasks, 5 categories)                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              AGENT FRAMEWORK                                │
│         LangGraph / AutoGen / CrewAI                        │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              ARW LAYER (thin wrapper)                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  1. Retry-with-Backoff                                │   │
│  │     t_wait(k) = t_base · β^k                          │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  2. Fallback Termination Guard                       │   │
│  │     Guard(a) = a if a ≠ ∅ else FALLBACK_MESSAGE     │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  3. Self-Consistency Verification                  │   │
│  │     â = argmax_a Σᵢ 𝟙[aᵢ = a]  (majority vote)     │   │
│  └─────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    FINAL ANSWER                              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  AUTO-CHECKER                                │
│         exact_match  OR  contains_substring                │
└───────────────┬─────────────────────┬───────────────────────┘
                │                     │
                ▼                     ▼
         ┌──────────┐          ┌──────────┐
         │  ✅ PASS  │          │  ❌ FAIL  │
         └──────────┘          └──────────┘
```

### Algorithm 1: ARW Execution Procedure

```
┌─────────────────────────────────────────────────────────────────────┐
│  ALGORITHM 1: ARW Execution Procedure                              │
├─────────────────────────────────────────────────────────────────────┤
│  REQUIRE: Task T; framework execution function f;                  │
│           max retries r; backoff parameters t_base, β              │
│  ENSURE:  Final answer A; execution telemetry L                    │
├─────────────────────────────────────────────────────────────────────┤
│  1:  k ← 0                                                          │
│  2:  while k ≤ r do                                                 │
│  3:      response ← f(T)        ▷ may raise exception              │
│  4:      if response is valid (non-empty) then                     │
│  5:          return response, L(k, success)                        │
│  6:      end if                                                    │
│  7:      if k = 0 then                                             │
│  8:          mark crashed_before_arw ← true                        │
│  9:      end if                                                    │
│ 10:      sleep(t_base · β^k)        ▷ exponential backoff         │
│ 11:      k ← k + 1                                                 │
│ 12:  end while                                                     │
│ 13:  return FALLBACK_MESSAGE, L(k, fallback)                       │
└─────────────────────────────────────────────────────────────────────┘
```

**Retry-with-Backoff Parameters:**
- `t_base` = 0.5s (base delay)
- `β` = 2.0 (backoff multiplier)
- `k` = zero-indexed retry attempt number

**Exponential Backoff Schedule:**

```
t_wait(k) = t_base · β^k

Attempt 0:  t_wait(0) = 0.5 · 2^0 = 0.5s
Attempt 1:  t_wait(1) = 0.5 · 2^1 = 1.0s
Attempt 2:  t_wait(2) = 0.5 · 2^2 = 2.0s
Attempt 3:  t_wait(3) = 0.5 · 2^3 = 4.0s
...
```

This follows the exponential backoff strategy widely used for transient fault recovery in distributed systems [31].

### Algorithm 2: Full ARW Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│  ALGORITHM 2: Full ARW Pipeline                                      │
├─────────────────────────────────────────────────────────────────────┤
│  REQUIRE: Task T; framework execution function f;                  │
│           max retries r; backoff parameters t_base, β;              │
│           consistency sample size n; self-consistency flag SC      │
│  ENSURE:  Final answer A                                            │
├─────────────────────────────────────────────────────────────────────┤
│  1:  if SC is enabled then                                          │
│  2:      S ← ∅                                                      │
│  3:      for i = 1 to n do                                          │
│  4:          (aᵢ, Lᵢ) ← RetryWithBackoff(T, f, r, t_base, β)       │
│              ▷ Algorithm 1                                          │
│  5:          S ← S ∪ {aᵢ}                                          │
│  6:      end for                                                    │
│  7:      â ← majority vote over S  (Equation 4)                    │
│  8:      if â exists then                                           │
│  9:          A ← â                                                  │
│ 10:      else                                                       │
│ 11:          A ← FALLBACK_MESSAGE                                  │
│ 12:      end if                                                     │
│ 13:  else                                                           │
│ 14:      (A, L) ← RetryWithBackoff(T, f, r, t_base, β)           │
│              ▷ Algorithm 1                                          │
│ 15:  end if                                                         │
│ 16:  A ← Guard(A)        ▷ Equation 3                              │
│ 17:  return A                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

> **Note:** In the evaluation reported in Section IV, SC was set to `false` for all runs, since self-consistency was not experimentally validated in this study.

### Equations & Formal Definitions

**1. Exponential Backoff:**

```
t_wait(k) = t_base · β^k
```

Where `t_base` is the base delay (0.5s), `β` is the backoff multiplier (2.0), and `k` is the zero-indexed retry attempt number.

**2. Fallback Termination Guard:**

```
          ⎧ a           if a ≠ ∅
Guard(a) = ⎨
          ⎩ FALLBACK    otherwise
```

Ensures execution always terminates with a well-formed output rather than propagating an unhandled exception or silent empty result.

**3. Self-Consistency Majority Vote:**

Given `n` sampled responses {a₁, ..., aₙ}:

```
â = argmax_a Σᵢ₌₁ⁿ 𝟙[aᵢ = a]

Accepted if:  max_a Σᵢ₌₁ⁿ 𝟙[aᵢ = a] > n/2
```

This majority-vote acceptance rule follows the self-consistency decoding strategy of Wang et al. [24].

**4. Pass Rate & Delta:**

```
              1    N
Rate = ───   Σ   Pass(aᵢ, eᵢ)
              N   i=1

Δ = Rate_ARW − Rate_Base
```

Where `N` is the number of runs, `aᵢ` is the agent output, and `eᵢ` is the expected value.

---

## 🔧 Framework Integration

### Adapter Design

We wrote **lightweight adapters** for each framework so that all three see identical tool interfaces. ARW sits outside each framework, connected through these adapters.

```
┌──────────┐     ┌──────────────┐     ┌─────┐     ┌──────────┐     ┌──────────┐     ┌─────────┐
│ Task     │────▶│ Framework    │────▶│ LLM │────▶│ Tool     │────▶│ Final    │────▶│ Auto-   │
│ JSON     │     │ Adapter      │     │     │     │ Calls    │     │ Answer   │     │ Checker │
└──────────┘     └──────────────┘     └─────┘     └──────────┘     └──────────┘     └────┬────┘
                                                                                       │
                                                                                  ┌────┴────┐
                                                                                  │ Log +   │
                                                                                  │ Pass/   │
                                                                                  │ Fail    │
                                                                                  └─────────┘
```

The adapters expose a common execution interface while preserving the native behavior of the framework underneath. This lets ARW observe outcomes and apply recovery without touching the framework's internal control flow.

### Framework Characteristics

#### Table VI — Framework Integration Characteristics

| Property | LangGraph | CrewAI | AutoGen |
|:---|:---|:---|:---|
| **Architecture** | Directed graph | Role-based crew | Conversational group chat |
| **State Management** | Explicit graph state | Implicit context window | Turn-based message history |
| **Agent Count** | 1 (monolithic) | 2–4 (specialized) | 2–3 (assistant + reviewer) |
| **Control Flow** | Deterministic routing | Manager-driven delegation | Group consensus / termination |
| **Built-in Retry** | No | No | Yes (reviewer loop) |

### CrewAI Integration Constraints

Integrating ARW with CrewAI revealed three engineering constraints:

1. **Crew/Task Object Corruption on Reuse** — CrewAI's Crew and Task objects carry internal state that corrupts when reused across retry attempts. ARW's retry mechanism introduces per-attempt overhead by allocating new objects on retry.

2. **OpenAI Fallback (Silent)** — CrewAI's native function-calling implementation falls back to OpenAI's API unless routed somewhere else explicitly. We discovered this during adapter debugging and had to add explicit routing configuration to lock execution to the Qwen 2.5 7B model.

3. **Async Timeout Incompatibility** — Thread-based timeouts do not play well with CrewAI's internal async event system. A thread-based cancel signal does not actually stop CrewAI's background async work, so resources accumulate and state becomes unpredictable across retries. A proper fix would require a multiprocessing-based timeout instead.

> **Impact:** Because of these constraints, we excluded team-coordination tasks **t37–t45** from CrewAI's ARW evaluation. CrewAI's ARW evaluation covers **34 tasks (68 runs)** rather than the full 45-task benchmark.

---

## 📈 Results

### Baseline Performance

#### Table VII — Baseline Experimental Corpus

| Framework | Runs | Date Range | Passes | Pass Rate |
|:---|:---:|:---|:---:|:---:|
| **LangGraph** | 294 | Aug 7–13 | 160 | **54.4%** |
| **AutoGen** | 919 | Aug 11–15 | 518 | **56.4%** |
| **CrewAI** | 331 | Aug 8–15 | 220 | **66.5%** |
| **Total** | **1,544** | — | **898** | **58.2%** |

> **Note:** Baseline runs were collected without a fixed-N protocol (repetition counts vary by framework according to experimental availability). The differing sample sizes yield unequal precision: AutoGen's larger corpus produces tighter empirical estimates, while LangGraph and CrewAI have wider effective confidence intervals.

### ARW Performance

#### Table VIII — Baseline and ARW Performance

| Framework | Baseline | With ARW | Scope | Δ |
|:---|:---:|:---:|:---:|:---:|
| LangGraph | 54.4% | 52.2% | Full (90 runs) | 🔴 **−2.2 pp** |
| **AutoGen** | 56.4% | **60.0%** | Full (90 runs) | 🟢 **+3.6 pp** |
| CrewAI | 66.5% | 50.0% | Partial (68 runs)* | 🔴 **−16.5 pp** |

\* *CrewAI evaluated on 34/45 tasks — team-coordination tasks excluded due to async timeout incompatibility.*

#### Figure 4 — Checker-Verified Pass Rates (Before vs. After ARW)

```
Pass Rate (%)
  │
 70┤        ┌───┐
   │        │███│ 66.5%
   │        │███│
   │        │███│
 60┤        │███│              ┌───┐
   │        │███│              │▓▓▓│ 60.0%  ← +3.6 pp
   │        │███│              │▓▓▓│
   │        │███│              │▓▓▓│
 50┤        │███│ 50.0% ──────▶│░░░│        ┌───┐
   │        │███│              │░░░│        │░░░│
   │        │███│              │░░░│        │░░░│
   │        │███│              │░░░│        │░░░│
 40┤        │███│              │░░░│        │░░░│
   │        │███│              │░░░│        │░░░│
   │        │███│              │░░░│        │░░░│
   │        │███│              │░░░│        │░░░│
 30┤        │███│              │░░░│        │░░░│
   │        │███│              │░░░│        │░░░│
   │        │███│              │░░░│        │░░░│
   │        │███│              │░░░│        │░░░│
 20┤        │███│              │░░░│        │░░░│
   │        │███│              │░░░│        │░░░│
   │        │███│              │░░░│        │░░░│
   │        │███│              │░░░│        │░░░│
 10┤        │███│              │░░░│        │░░░│
   │        │███│              │░░░│        │░░░│
   │        │███│              │░░░│        │░░░│
   │        │███│              │░░░│        │░░░│
  0┼────────┴───┴────────────┴───┴────────┴───┴───────────────────
            Baseline    ARW      Baseline    ARW      Baseline    ARW
              LangGraph          AutoGen            CrewAI*

              ─2.2 pp           +3.6 pp            −16.5 pp

  Legend: ███ Baseline    ▓▓▓ ARW (improved)    ░░░ ARW (degraded)
```

**Interpretation:**
- **AutoGen** responded best — checker-verified pass rate rose from 56.4% to 60.0% (+3.6 pp). Some portion of AutoGen's failures were recoverable at execution time.
- **LangGraph** moved in the opposite direction — fell from 54.4% to 52.2% (−2.2 pp). The retry and fallback mechanisms did not reach the dominant failure source (wrong answers = 53.5%).
- **CrewAI's** ARW evaluation is harder to interpret — covers only 34/45 tasks, so 50.0% is not directly comparable to full-scope numbers.

### LangGraph Failure Breakdown

#### Table IX — LangGraph ARW Failure Breakdown (90 Runs)

| Failure Category | Proportion |
|:---|:---:|
| **Reasoning / Wrong-Value** | **53.5%** |
| **Format Violation** | 34.9% |
| **Crash / Infrastructure** | 11.6% |

**Why ARW Didn't Help LangGraph:**
Reasoning and wrong-value failures dominate at 53.5%, followed by format violations at 34.9%. Infrastructure crashes account for just 11.6%. When the majority of failures stem from the model getting the answer wrong, a wrapper that retries execution or catches empty outputs can only do so much. That is exactly what we see in LangGraph's aggregate result.

### Representative Failure Traces

#### Table X — Representative ARW Failure Traces

| Task | Failure Type | Expected | Observed Behavior | ARW Response |
|:---|:---|:---|:---|:---|
| **t08** | Structural Crash | `PK18B2` | Graph routing failure; empty output | Fallback guard activated; retry exhausted |
| **t28** | Structural Crash | `UAE12A` | Tool call malformed; execution halted | Retry-with-backoff attempted; failed after 3 attempts |
| **t34** | Format Violation | `275000` | Correct numeric value wrapped in extra text | Consistency check flagged mismatch; no recovery path |
| **t39** | Format Violation | `Hello World` | Output contained correct string plus noise | Fallback guard accepted non-empty output |
| **t41** | Format Violation | `AI agents are useful` | Correct answer embedded in explanatory text | Fallback guard accepted non-empty output |
| **t29** | Wrong-Value | `1500` | Hallucinated intermediate fact | All retry attempts produced same hallucination |
| **t31** | Wrong-Value | — | Incorrect multi-step reasoning | Retry reproduced same reasoning chain |

**Pattern:** Tasks t08 and t28 fail deterministically (100% of runs) due to structural execution errors — framework-level incompatibilities with specific task patterns, not random model mistakes. Tasks t34, t39, and t41 show format violations: the semantic answer is correct, but the syntactic packaging breaks the checker. Tasks t29 and t31 are different — the model reasons incorrectly, and retrying simply reproduces the same error.

### Cross-Dataset Comparison

#### Table XI — Comparison with Recent Agent Reliability Studies (2025–2026)

| Study | Year | Model(s) | Mechanism | Cross-Framework? |
|:---|:---:|:---|:---|:---:|
| Cemri et al. [1] (MAST) | 2025 | — | Failure taxonomy only | ✅ (5 FW) |
| Jeong & Shin [28] | 2026 | Not specified | Detection + replanning | ❌ |
| Chen et al. [29] | 2026 | Not specified | Trace-guided harness repair | ❌ |
| Zhao et al. [27] (AgentTether) | 2026 | Qwen3.7-max / GPT-5.4 | Graph diagnosis + intervention | ❌ |
| Dubey [30] | 2026 | Qwen2.5 7B / 3B, Llama3.1 8B | Telemetry detection + rollback-repair | ✅ (3 FW) |
| Li et al. [26] | 2025 | Not specified | Hallucination analysis (no mitigation) | — |
| **Ours (ARW)** | **2026** | **Qwen 2.5 7B** | **Retry + fallback + consistency** | **✅ (3 FW)** |

#### Table III — AgentTether vs. ARW Detailed Comparison

| Aspect | AgentTether [27] | ARW (Ours) |
|:---|:---|:---|
| **Mechanism** | CTG + HGT detector + Isolation Forest + analyst LLM + intervention harness | Retry-with-backoff + fallback guard + self-consistency |
| **Complexity** | Heavy (offline training on 21K trajectories, graph construction) | **Lightweight** (no training, no auxiliary models) |
| **Model** | Qwen3.7-max / GPT-5.4 (commercial API) | **Qwen 2.5 7B, served locally, zero inference cost** |
| **Benchmark** | τ-bench (261 tasks, 3 domains) | Custom benchmark (45 tasks, 5 categories) |
| **Frameworks** | Single architecture | **LangGraph, AutoGen, CrewAI** |
| **Repair / Pass Rate** | 69.11% repair on failed tasks | AutoGen +3.6 pp; LangGraph −2.2 pp; CrewAI 50.0% (partial) |
| **Cross-framework?** | ❌ Not evaluated | ✅ Explicitly evaluated — efficacy varies |

> **AgentTether asks:** *"How much can we repair within one architecture?"*  
> **ARW asks:** *"Does the same lightweight repair work everywhere?"*  
> The answers are complementary. ARW is directly relevant to **resource-constrained or on-premises deployments** where 7B-scale local models, not commercial frontier APIs, are the reality.

---

## 💡 Key Findings & Discussion

### Framework-Dependent Effectiveness

ARW's effect is **not uniform** across frameworks:

| Framework | Δ | Why? |
|:---|:---:|:---|
| **AutoGen** | +3.6 pp | Conversational architecture with built-in reviewer loops gives retries a foothold — dialogue history can nudge execution onto a different path |
| **LangGraph** | −2.2 pp | Deterministic graph routing offers no flexibility; retry often reenters the same path and reproduces the same error |
| **CrewAI** | −16.5 pp* | Partial evaluation + async timeout incompatibility; reduced task coverage makes comparison exploratory |

### Why ARW Helps AutoGen But Not LangGraph

```
┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│         AUTOGEN                 │     │         LANGGRAPH               │
│  ┌─────────────────────────┐    │     │  ┌─────────────────────────┐    │
│  │ Conversational          │    │     │  │ Deterministic           │    │
│  │ reviewer loop           │    │     │  │ graph routing           │    │
│  └───────────┬─────────────┘    │     │  └───────────┬─────────────┘    │
│              │                   │     │              │                   │
│              ▼                   │     │              ▼                   │
│  ┌─────────────────────────┐    │     │  ┌─────────────────────────┐    │
│  │ Retry gets fresh        │    │     │  │ Retry re-enters         │    │
│  │ dialogue context        │    │     │  │ same path               │    │
│  └───────────┬─────────────┘    │     │  └───────────┬─────────────┘    │
│              │                   │     │              │                   │
│              ▼                   │     │              ▼                   │
│  ┌─────────────────────────┐    │     │  ┌─────────────────────────┐    │
│  │ ✅ Execution nudged     │    │     │  │ ❌ Same error           │    │
│  │    onto new path        │    │     │  │    reproduced           │    │
│  └─────────────────────────┘    │     │  └─────────────────────────┘    │
└─────────────────────────────────┘     └─────────────────────────────────┘
```

### Reliability Intervention Is Failure-Dependent

ARW is a **targeted intervention**, not a universal fix:

| Failure Type | ARW Mechanism | Effectiveness |
|:---|:---|:---:|
| Infrastructure crash | Retry-with-backoff | ✅ High |
| Silent termination | Fallback guard | ✅ High |
| Fluctuating-but-correct output | Self-consistency | ✅ High (untested) |
| Wrong reasoning chain | None — model-level | ❌ Low |

> **The dominant wrong-answer category (23–53%) is a harder problem.** Retrying a hallucinated value or a flawed reasoning chain simply repeats the mistake — the wrapper cannot rewrite the model's internals. This motivates the self-consistency module: flagging disagreement between independent responses rather than accepting either blindly.

### Limitations

1. **Single model** — Qwen 2.5 7B was used; a stronger model could shift both absolute rates and rankings.
2. **Small benchmark** — 45 tasks is smaller than GAIA (466) or τ-bench (189), widening confidence intervals.
3. **"Other" failure category** — lacks fine-grained manual labeling.
4. **Latency and cost** — not measured, though both matter for deployability.
5. **CrewAI partial evaluation** — covered only 34/45 tasks, so cross-framework comparisons are exploratory.
6. **Self-consistency** — implemented but not experimentally evaluated.

### Future Work

1. Re-run with **GPT-4o-mini** to separate model effects from framework effects.
2. Add a **multiprocessing-based timeout** so CrewAI's team-coordination tasks (t37–t45) can be included.
3. Expand beyond **100 tasks** for statistical power.
4. Add a **direct LLM baseline** with no framework scaffolding.
5. Experimentally evaluate **self-consistency** on model-level reasoning errors.

---

## 📁 Repository Structure

```
arw-agent-reliability/
│
├── 📄 README.md                          # This file
├── 📄 LICENSE                            # MIT License
├── 📄 requirements.txt                   # Python dependencies
│
├── 📁 tasks/                             # 45 task definitions + correctness checkers
│   ├── 📁 web_search/                    # t01–t09
│   ├── 📁 file_manipulation/             # t10–t18
│   ├── 📁 booking_transactions/          # t19–t27
│   ├── 📁 math_reasoning/                # t28–t36
│   └── 📁 team_coordination/             # t37–t45
│
├── 📁 frameworks/                        # Per-framework adapter code
│   ├── 🔧 langgraph_adapter.py
│   ├── 🔧 crewai_adapter.py
│   └── 🔧 autogen_adapter.py
│
├── 📁 arw/                               # The reliability layer itself
│   ├── 🔁 retry_backoff.py              # Exponential backoff retry logic
│   ├── 🛡️ fallback_guard.py             # Termination guard
│   └── ⚖️ self_consistency.py           # Majority-vote consistency (future work)
│
├── 📁 runner/                            # Orchestrates tasks across frameworks
│   └── 🏃 run_benchmark.py               # Main benchmark execution script
│
├── 📁 logs/                              # Raw JSON logs of every run
│   ├── baseline/
│   │   ├── langgraph_runs.json
│   │   ├── autogen_runs.json
│   │   └── crewai_runs.json
│   └── arw/
│       ├── langgraph_arw_runs.json
│       ├── autogen_arw_runs.json
│       └── crewai_arw_runs.json
│
├── 📁 annotation/                        # Failure taxonomy labeling (11 categories)
│   └── label_failures.py
│
├── 📁 analysis/                        # Metrics, statistics, figure generation
│   ├── 📊 failure_distribution.py       # Generates Figure 3
│   ├── 📊 arw_performance.py            # Generates Figure 4 / Table VIII
│   ├── 📊 bootstrap_ci.py               # Statistical confidence intervals
│   └── 📊 mcnemar_test.py               # Paired statistical testing
│
└── 📁 report/                            # Final written report / paper source
    └── paper.tex
```

---

## 🚀 Reproducing Results

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) installed and running locally
- 8GB+ RAM recommended

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/malaikaarif/arw-agent-reliability.git
cd arw-agent-reliability

# 2. Install dependencies
pip install -r requirements.txt

# 3. Serve Qwen 2.5 7B locally via Ollama
ollama pull qwen2.5:7b
ollama serve

# 4. Run the full benchmark across all frameworks (baseline)
python runner/run_benchmark.py \
    --mode baseline \
    --frameworks langgraph autogen crewai \
    --tasks-dir ./tasks \
    --output-dir ./logs/baseline

# 5. Run with ARW enabled
python runner/run_benchmark.py \
    --mode arw \
    --frameworks langgraph autogen crewai \
    --tasks-dir ./tasks \
    --output-dir ./logs/arw \
    --arw-config ./arw/config.yaml

# 6. Generate figures and tables
python analysis/failure_distribution.py --input ./logs/baseline
python analysis/arw_performance.py --baseline ./logs/baseline --arw ./logs/arw
python analysis/bootstrap_ci.py --runs ./logs/baseline/autogen_runs.json
```

### ARW Configuration

```yaml
# arw/config.yaml
arw:
  retry:
    max_retries: 3
    base_delay: 0.5        # seconds
    backoff_multiplier: 2.0
  fallback:
    enabled: true
    fallback_message: "FALLBACK: Task could not be completed."
  self_consistency:
    enabled: false         # not yet experimentally validated
    sample_size: 3
    majority_threshold: 0.5
```

### Reproducibility Notes

> **Baseline runs** were collected without a fixed-N protocol (repetition counts vary: 294 LangGraph / 919 AutoGen / 331 CrewAI runs), so raw proportions are reported without significance testing for the baseline corpus.

> **ARW evaluation** uses a controlled paired design with equal repetition:
> - 90 runs each for LangGraph and AutoGen (full 45 tasks × 2 repetitions)
> - 68 runs for CrewAI (partial: 34 tasks × 2 repetitions)
>
> This is what supports the Δ comparisons above.

---

## 📚 Citation

If you use this benchmark, framework, or find our work valuable, please cite:

```bibtex
@unpublished{arif2026arw,
  title   = {Beyond Accuracy: Diagnosing and Mitigating Reliability Failures in AI Agent Frameworks},
  author  = {Arif, Malaika and Safdar, Iqra and Abbas, Yawar},
  note    = {Under review},
  year    = {2026},
  institution = {COMSATS University Islamabad, Sahiwal Campus}
}
```

### Related Work Referenced

| Citation | Contribution |
|:---|:---|
| Cemri et al. [1] | MAST: Multi-Agent System Failure Taxonomy (14 categories, 5 frameworks) |
| Mialon et al. [2] | GAIA: General AI Assistants benchmark (466 tasks, real APIs) |
| Yao et al. [3] | τ-bench: Tool-Agent-User Interaction benchmark (189 tasks) |
| LangChain [4] | LangGraph: Directed graph execution for agents |
| CrewAI [5] | Role-based multi-agent crew delegation |
| Wu et al. [6] | AutoGen: Multi-agent conversation framework |
| Zhao et al. [27] | AgentTether: Graph-guided diagnosis and runtime intervention |
| Wang et al. [24] | Self-Consistency improves Chain-of-Thought reasoning |
| Jacobson [31] | Exponential backoff for transient fault recovery |

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 Malaika Arif, Iqra Safdar, Yawar Abbas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙏 Acknowledgments

We thank the **Department of Computer Science at COMSATS University Islamabad, Sahiwal Campus**, for supporting this work. We also thank colleagues who provided feedback on the failure taxonomy and experimental design.

---

<div align="center">

**⭐ Star this repo if you find it useful!**

<sub>Built with ❤️ at COMSATS University Islamabad, Sahiwal Campus</sub>

</div>
