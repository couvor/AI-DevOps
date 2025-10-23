#!/usr/bin/env python
import os, sys, json, argparse, random, yaml, time
from pathlib import Path

P1 = "Task: Generate transaction sequences to cover functions/branches/paths."
P2 = "Context: Use ABI & examples. Output only valid, encoded calls."
P3 = "Review: Remove illegal/duplicate/low-diversity sequences."
P4 = "Refine: Improve edge-case coverage and parameter variety."

def load_cfg(p):
    with open(p, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def fake_llm_generate(abi_items, max_seeds, max_len):
    # Placeholder generator producing pseudo-seeds for CI demo.
    seeds = []
    for i in range(max_seeds):
        seq = []
        for _ in range(random.randint(2, max_len)):
            fun = random.choice(abi_items) if abi_items else {"name":"transfer","inputs":[{"type":"address"},{"type":"uint256"}]}
            call = {
                "function": fun.get("name","f"),
                "params": ["0x" + "".join(random.choice("0123456789abcdef") for _ in range(40)), random.randint(1,10**6)]
            }
            seq.append(call)
        seeds.append({"id": f"seed-{i:04d}", "sequence": seq})
    return seeds

def load_abi(abi_dir):
    items = []
    p = Path(abi_dir)
    if not p.exists():
        return items
    for f in p.glob("*.json"):
        try:
            data = json.loads(Path(f).read_text(encoding="utf-8"))
            for it in data:
                if it.get("type") == "function":
                    items.append({"name": it.get("name"), "inputs": it.get("inputs", [])})
        except Exception:
            continue
    return items

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", help="configs/fuzz_llm.yaml")
    ap.add_argument("--out", help="output seeds jsonl")
    ap.add_argument("--validate", help="validate jsonl file")
    ap.add_argument("--min_valid_ratio", type=float, default=0.6)
    args = ap.parse_args()

    if args.validate:
        total = 0
        valid = 0
        with open(args.validate, "r", encoding="utf-8") as f:
            for line in f:
                total += 1
                try:
                    obj = json.loads(line)
                    if isinstance(obj.get("sequence", None), list) and len(obj["sequence"])>0:
                        valid += 1
                except Exception:
                    pass
        ratio = valid / total if total else 0.0
        print(f"[VALIDATOR] valid={valid} total={total} ratio={ratio:.2f}")
        if ratio < args.min_valid_ratio:
            print(f"::error title=Seed valid ratio too low::ratio={ratio:.2f} < {args.min_valid_ratio}")
            sys.exit(1)
        sys.exit(0)

    cfg = load_cfg(args.config)
    c = cfg["fuzz_llm"]
    abi_items = load_abi(c.get("abi_dir", "contracts/abi"))
    seeds = fake_llm_generate(abi_items, c.get("max_seeds", 100), c.get("limits",{}).get("max_sequence_len", 6))

    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    with open(outp, "w", encoding="utf-8") as f:
        for s in seeds:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    print(f"[SEED_GEN] Wrote {len(seeds)} seeds to {outp}")

if __name__ == "__main__":
    main()
