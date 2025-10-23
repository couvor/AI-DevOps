# AI-DevOps + Model Security Dual-Layer Validation

This repo provides a reference CI pipeline combining:
- **Layer A (Model QA)**: Multi-objective test sample selection (coverage/diversity/fault-trigger) based on NSGA-II.
- **Layer B (Contract Security)**: LLM-driven, chain-of-prompts, adversarial seed generation to supercharge smart-contract fuzzers (e.g., Ityfuzz).

> Plug this into your project as a subfolder or template. See `configs/*.yaml` for knobs.
