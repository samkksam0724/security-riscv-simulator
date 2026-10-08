# PASTA Threat Model: Security-Aware RV32I Processor Simulator

## Stage 1: Define Objectives
* **Business & Security Goals:** Develop a functional 32-bit RV32I RISC-V simulator with integrated runtime detection for memory corruption and execution anomalies.
* **Compliance & Standards:** CVSS v3.1 scoring standard for severity assessment; SDG 9 alignment.

## Stage 2: Define Technical Scope
* **Hardware Core Scope:** 5-stage pipeline (IF, ID, EX, MEM, WB) with hazard forwarding.
* **Security Monitoring Scope:** Stack canary checks, memory bounds enforcement, and Isolation Forest anomaly tracking.

## Stage 3: Application Decomposition
* **Assets:**
  1. Return Addresses on the stack (`sp` relative memory locations).
  2. Register File State (`x0` - `x31`).
  3. Program Counter (`PC`) state and control-flow integrity.
* **Trust Boundaries:**
  * Boundary between execution core logic and runtime security monitor layer.
  * Boundary between normal instruction execution and stack/data memory boundaries.