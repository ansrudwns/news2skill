# Progressive Disclosure
## Architectural Insight
To maintain maximum reasoning capacity (token economy) while storing hundreds of skills, architecture must load knowledge progressively.

## Best Practices
- **Discovery Layer**: Load only the title and a 100-token summary of a skill during standard operations.
- **Activation Layer**: Only when the user request explicitly triggers a specific domain, load the full `SKILL.md` instructions.
- Never feed the entire knowledge base at once. Always fracture knowledge into distinct, micro-segmented files.
