"""
ARW — Adaptive Reliability Wrapper (v2)
=========================================
v2 change: real adapters (LangGraph/CrewAI/AutoGen) don't expose one raw
"llm.invoke(prompt)" line you can hook — they run multi-step tool loops
internally and only fail when you call crew.kickoff() / agent.run() /
agent.invoke(). So `run()` now accepts either:

  - a STRING prompt  -> uses the llm_call you passed to the constructor
                        (this is what demo.py still uses)
  - a CALLABLE (zero-arg function) -> ARW calls it directly and treats
                        whatever it returns/raises as the thing to retry
                        (this is what the real adapters use — see
                        crewai_adapter.py / langgraph_adapter.py /
                        autogen_adapter.py)

Same three modules as before:
  1. Retry-with-backoff        -> fixes CrewAI's 10.3% None/empty crash
  2. Fallback termination guard -> fixes LangGraph's 5.4% silent empty-answer
  3. Self-consistency check     -> targets the 23-43% "wrong answer" bucket
"""

import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Callable, Optional, List, Tuple, Union


@dataclass
class ARWConfig:
    max_retries: int = 3                # Module 1
    backoff_base: float = 0.5           # seconds, Module 1
    backoff_factor: float = 2.0         # exponential multiplier, Module 1
    consistency_samples: int = 3        # Module 3 (odd number -> clean majority vote)
    consistency_temperature: float = 0.3
    fallback_message: str = "[ARW_FALLBACK] No valid response after retries — routed to fallback instead of crashing/terminating silently."


@dataclass
class ARWRunLog:
    """Everything you need for the paper's ARW-vs-baseline results table."""
    final_output: Optional[str] = None
    retries_used: int = 0
    crashed_before_arw: bool = False     # would this run have crashed/emptied on attempt 1?
    consistency_used: bool = False
    consistency_agreed: Optional[bool] = None
    consistency_samples: List[str] = field(default_factory=list)
    used_fallback: bool = False
    last_error: Optional[str] = None     # exception message on final failed attempt, if any


class AdaptiveReliabilityWrapper:
    def __init__(self, llm_call: Optional[Callable[..., Optional[str]]] = None,
                 config: ARWConfig = None):
        """
        llm_call: OPTIONAL. Only needed if you plan to call `run("some prompt string")`.
                  For real framework adapters, you don't need this — call
                  `run(your_execute_function)` instead. See adapter files.
        """
        self.llm_call = llm_call
        self.config = config or ARWConfig()

    @staticmethod
    def _is_invalid(response) -> bool:
        return response is None or (isinstance(response, str) and response.strip() == "")

    def _resolve(self, task: Union[str, Callable[[], Optional[str]]], **kwargs) -> Callable[[], Optional[str]]:
        if callable(task):
            return task
        if self.llm_call is None:
            raise ValueError("ARW: got a string prompt but no llm_call was provided to the constructor.")
        return lambda: self.llm_call(task, **kwargs)

    # ---------- Module 1: Retry-with-backoff ----------
    def _call_with_retry(self, func: Callable[[], Optional[str]]) -> Tuple[Optional[str], int, bool, Optional[str]]:
        crashed_before_arw = False
        last_error = None
        for attempt in range(self.config.max_retries + 1):
            try:
                response = func()
            except Exception as e:
                response = None
                last_error = f"{type(e).__name__}: {e}"
            if self._is_invalid(response):
                if attempt == 0:
                    crashed_before_arw = True  # would've crashed/emptied on the very first try, pre-ARW
                if attempt < self.config.max_retries:
                    time.sleep(self.config.backoff_base * (self.config.backoff_factor ** attempt))
                    continue
                return None, attempt + 1, crashed_before_arw, last_error
            return response, attempt, crashed_before_arw, None
        return None, self.config.max_retries + 1, crashed_before_arw, last_error

    # ---------- Module 3: Self-consistency check ----------
    def _self_consistency(self, task, **kwargs) -> Tuple[Optional[str], bool, List[str], bool, Optional[str]]:
        samples = []
        crashed_first = False
        last_error = None
        for i in range(self.config.consistency_samples):
            func = self._resolve(task, temperature=self.config.consistency_temperature, **kwargs) if isinstance(task, str) else task
            resp, _, crashed, err = self._call_with_retry(func)
            if i == 0:
                crashed_first = crashed
            if err:
                last_error = err
            if resp is not None:
                samples.append(resp.strip())
        if not samples:
            return None, False, samples, crashed_first, last_error
        counts = Counter(samples)
        top_answer, top_count = counts.most_common(1)[0]
        agreed = top_count > len(samples) / 2
        return top_answer, agreed, samples, crashed_first, last_error

    # ---------- Module 2: Fallback termination guard ----------
    def _fallback_guard(self, response: Optional[str], context: Optional[str], last_error: Optional[str]) -> Tuple[str, bool]:
        if self._is_invalid(response):
            msg = self.config.fallback_message
            if context:
                msg += f" (context: {context})"
            if last_error:
                msg += f" (last_error: {last_error})"
            return msg, True
        return response, False

    # ---------- Public entry point ----------
    def run(self, task: Union[str, Callable[[], Optional[str]]],
            use_consistency: bool = False, context: Optional[str] = None, **kwargs) -> ARWRunLog:
        """
        task: either a prompt string (needs llm_call bound in constructor)
              or a zero-arg callable, e.g. `lambda: crew.kickoff()` — use
              this form for real framework adapters.
        """
        log = ARWRunLog()

        if use_consistency:
            answer, agreed, samples, crashed, err = self._self_consistency(task, **kwargs)
            log.consistency_used = True
            log.consistency_agreed = agreed
            log.consistency_samples = samples
            log.crashed_before_arw = crashed
            log.last_error = err
            if answer is None:
                func = self._resolve(task, **kwargs)
                answer, retries, crashed2, err2 = self._call_with_retry(func)
                log.retries_used = retries
                log.last_error = err2 or log.last_error
        else:
            func = self._resolve(task, **kwargs)
            answer, retries, crashed, err = self._call_with_retry(func)
            log.retries_used = retries
            log.crashed_before_arw = crashed
            log.last_error = err

        final, used_fallback = self._fallback_guard(answer, context, log.last_error)
        log.final_output = final
        log.used_fallback = used_fallback
        return log