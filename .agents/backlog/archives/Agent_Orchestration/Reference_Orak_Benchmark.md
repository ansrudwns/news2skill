---
description: A Foundational Benchmark for Training and Evaluating LLM Agents on Diverse Video Games
tags: [Benchmark, Video Games, Multi-Agent, Environment, Krafton]
---

# Orak: Foundational Benchmark for Video Game Agents

## 1. Core Bottleneck
Current benchmarks for evaluating LLM agents are limited to simple, static environments (like web browsing or text adventures). Modern video games pose a far more complex challenge: spatial reasoning, real-time feedback, long-horizon planning, and partially observable states. Existing agents often fail completely when transitioning to such dynamic environments.

## 2. Algorithmic Paradigm
Orak introduces a massive, diverse suite of video game environments wrapped in a standardized API. It evaluates agents not just on final success, but on intermediate reasoning and spatial navigation capabilities.

## 3. Advisory Application
**Future System Integration:** While we cannot run a heavy 3D game simulator on the 24GB laptop, we can extract the *Action-Space Mapping* theories from Orak. If the user wants to build a trading bot or an OS-control agent, we can apply Orak's spatial/temporal reasoning patterns (like framing visual UI as a grid) to non-game contexts.
