# T1: Tool-integrated Verification for Test-time Compute (Toy Sandbox)

## Hypothesis
Small Language Models (SLMs) can achieve High-Reasoning performance (comparable to massive 100B parameter models) by spending more compute at *test-time*. Instead of one single greedy forward pass, the SLM generates $N$ candidate solutions and runs them through an external rule-based tool (Verifier).

## Local Implementation
This script simulates the 'T1' methodology. 
We simulate a stochastic SLM generator and a strict external tool environment.

## Execution
Run `python experiment.py` to see how increasing $N$ (test-time compute) drastically increases the pass rate of the SLM.
