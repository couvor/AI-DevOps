#!/usr/bin/env bash
set -euo pipefail
SEEDS_FILE=${1:-seeds/ityfuzz_seeds.jsonl}
echo "[RUN] (stub) would invoke Ityfuzz with $SEEDS_FILE"
# docker run --rm -v "$PWD":/work ityfuzz:latest ityfuzz --seed-file "$SEEDS_FILE" --out fuzz_out/
