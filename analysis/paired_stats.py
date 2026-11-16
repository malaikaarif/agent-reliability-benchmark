import argparse
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

def task_rates(df, system, cond):
    d = df[(df.system == system) & (df.condition == cond)]
    return d.groupby("task").passed.mean()

def paired_diff(df, system, base, treat, n=10000, seed=12345):
    rng = np.random.default_rng(seed)
    a, b = task_rates(df, system, base), task_rates(df, system, treat)
    t = a.index.intersection(b.index)
    if len(t) == 0:
        return None
    d = (b[t] - a[t])
    v = d.to_numpy()
    idx = rng.integers(0, len(v), (n, len(v)))
    lo, hi = np.percentile(v[idx].mean(1), [2.5, 97.5])
    signs = rng.choice([-1.0, 1.0], (n, len(v)))
    p = ((np.abs((signs * v).mean(1)) >= abs(v.mean()) - 1e-12).sum() + 1) / (n + 1)
    return dict(system=system, n_tasks=len(t), base=a[t].mean(), treat=b[t].mean(),
                delta=v.mean(), ci_lo=lo, ci_hi=hi, p=p, d=d)

def power(p0, delta, reps, sims=500, seed=7):
    rng = np.random.default_rng(seed)
    p0 = np.asarray(p0, dtype=float)
    p1 = np.clip(p0 + delta, 0, 1)
    hits = 0
    for _ in range(sims):
        diff = rng.binomial(reps, p1) / reps - rng.binomial(reps, p0) / reps
        if diff.std() > 0 and stats.ttest_1samp(diff, 0).pvalue < 0.05:
            hits += 1
    return hits / sims

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--base", default="base")
    ap.add_argument("--treat", default="arw")
    ap.add_argument("--power", action="store_true")
    a = ap.parse_args()
    df = pd.read_csv(a.csv)
    res = []
    for s in sorted(df.system.unique()):
        if s == "direct":
            continue
        r = paired_diff(df, s, a.base, a.treat)
        if r is None:
            print(f"{s}: no paired data ({a.base} vs {a.treat})")
        else:
            res.append(r)
    if res:
        holm = multipletests([r["p"] for r in res], method="holm")[1]
        print(f"{'system':10}{'tasks':>6}{'base':>8}{'treat':>8}{'delta pp':>10}{'95% CI (pp)':>20}{'p':>8}{'p holm':>8}")
        for r, h in zip(res, holm):
            ci = "[%+.1f, %+.1f]" % (100 * r["ci_lo"], 100 * r["ci_hi"])
            print(f"{r['system']:10}{r['n_tasks']:6d}{100*r['base']:7.1f}%{100*r['treat']:7.1f}%"
                  f"{100*r['delta']:+10.1f}{ci:>20}{r['p']:8.3f}{h:8.3f}")
    if a.power:
        for s in sorted(df.system.unique()):
            if s == "direct":
                continue
            p0 = task_rates(df, s, a.base).to_numpy()
            print(f"\npower for {s} ({len(p0)} tasks), 10 reps per task:")
            for delta in (0.03, 0.05, 0.10):
                print(f"  true effect {delta:+.2f}: power {power(p0, delta, 10):.2f}")

if __name__ == "__main__":
    main()
