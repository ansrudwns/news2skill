# Harness Engineering
## Architectural Insight
The future of Agentic AI is not purely reliant on the foundational model parameters, but the "Control Layer" (Harness) wrapped around it. 

## Key Principles
- **Source of Truth**: Maintain a root AGENTS.md to inject standard conventions overriding default LLM behavior.
- **Execution-Intelligence Split**: Delegate pure deterministic tasks (crawling, building) to Python/Bash scripts, keeping the LLM focused ONLY on intelligence analysis. This prevents token bloat.
