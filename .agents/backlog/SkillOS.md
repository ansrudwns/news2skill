# Skill: SkillOS - Dynamic Skill Curation

## Description
This skill implements a dynamic routing and loading layer (SkillOS) for self-evolving agents, allowing the agent to selectively pull context from `AGENTS.md` based on embedding similarity or metadata tagging, rather than loading the entire registry into context.

## Trigger
Use this skill when the task requires combining multiple disparate skills, or when the agent detects context window bloat and needs to prune unused skills.

## Architecture
1. **Skill Vectorization**: Each markdown file in `.agents/skills/` is embedded.
2. **Task Querying**: The current user task is evaluated.
3. **Top-K Retrieval**: The OS layer selects the Top-3 most relevant skills.
4. **Execution Sandbox**: The agent operates ONLY with those 3 skills.

## Example Usage
```python
def load_curated_skills(task_prompt: str, k: int = 3) -> list[str]:
    # Placeholder for actual semantic retrieval logic
    # Requires vector store or LLM-based reranking
    pass
```

## Self-Verification
- Does the curated list cover the necessary dependencies?
- Are the token counts within the Adaptive Head Budgeting constraints?
