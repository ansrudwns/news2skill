# Draft-based Approximate Inference for LLMs (Toy Sandbox)

## Hypothesis
Autoregressive LLM generation is slow because it generates one token at a time. By using a highly compressed "Draft" model to guess the next 5 tokens, and then having the Main model verify those 5 tokens in parallel in a single forward pass, we can achieve massive latency reductions.

## Local Implementation
We simulate a slow target model and a fast draft model.
The draft model predicts sequences. The target model verifies them.

## Execution
Run `python experiment.py` to observe speedup comparisons.
