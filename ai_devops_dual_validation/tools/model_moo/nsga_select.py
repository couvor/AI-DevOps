#!/usr/bin/env python
import os, sys, json, argparse, random, yaml
from pathlib import Path

def load_cfg(p):
    with open(p, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def score_sample():
    # Stub: pretend we can compute three objectives per sample in [0,1]
    return {
        "neuron_coverage": random.uniform(0.5, 0.99),
        "diversity": random.uniform(0.5, 0.99),
        "fault_triggerability": random.uniform(0.2, 0.9)
    }

def fake_nsga2_select(n=50):
    # Produce a small "Pareto-like" set
    selected = []
    for i in range(n):
        s = score_sample()
        selected.append({"id": f"case-{i:04d}", "objectives": s})
    return selected

def gate_check(items, min_cov=0.85, max_reg=0):
    cov = sum(x["objectives"]["neuron_coverage"] for x in items)/len(items)
    regressions = 0  # stub: replace with real regression count
    ok = (cov >= min_cov) and (regressions <= max_reg)
    return ok, cov, regressions

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config")
    ap.add_argument("--out")
    ap.add_argument("--gate")
    ap.add_argument("--min_neuron_cov", type=float, default=0.85)
    ap.add_argument("--max_regressions", type=int, default=0)
    args = ap.parse_args()

    if args.gate:
        items = json.loads(Path(args.gate).read_text(encoding="utf-8"))
        ok, cov, reg = gate_check(items, args.min_neuron_cov, args.max_regressions)
        print(f"[GATE] neuron_cov={cov:.3f} regressions={reg} (min_cov={args.min_neuron_cov}, max_reg={args.max_regressions})")
        if not ok:
            print("::error title=Model QA gate failed::Coverage or regressions not satisfied")
            sys.exit(1)
        sys.exit(0)

    cfg = load_cfg(args.config)
    sel = fake_nsga2_select(n=32)
    Path(args.out).write_text(json.dumps(sel, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[NSGA2] Selected {len(sel)} samples to {args.out}")

if __name__ == "__main__":
    main()
