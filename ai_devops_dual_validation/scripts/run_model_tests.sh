#!/usr/bin/env bash
set -euo pipefail
SEL_FILE=${1:-selected_tests.json}
echo "[RUN] (stub) would execute model tests with $SEL_FILE"
# python tests/run_model_eval.py --testset "$SEL_FILE"
