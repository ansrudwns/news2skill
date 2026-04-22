---
description: Prompt engineering and scaffolding adaptations to dramatically increase coding proficiency in sub-10B parameter LLMs.
score: 95 (Highly actionable, updates existing Anthropic Prompt framework)
---
# Small Model Scaffolds

## Actionable Strategy
1. **Reduce Abstractions**: Do not use ambiguous instructions. Sub-10B models struggle with implicit logic leaps.
2. **Step-by-step enforcement**: Force the model to output a `[PLAN]` block before any code is generated.
3. **Restricted Context**: Do not feed the entire project context. Limit File fetching to less than 3 relevant files simultaneously.
4. **Concrete Edits**: For code modifications, enforce block replacements strictly mapped to line numbers, rather than asking the model to rewrite the whole file.

## Integration
Update `.agents/skills/Anthropic_Prompting.md` to detect when a draft/draft-inference model is active and deploy these constrained scaffolds natively.
