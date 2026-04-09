# Context Collapse Defense
## Architectural Insight
When terminal outputs or tool results exceed thousands of lines, standard context window drops drastically in reasoning quality.

## Best Practices
- Implement intermediate "Summarizer Subagents" for any action with heavy payloads.
- Instead of showing a 5000-line log to the main agent, route it to an independent pipeline that yields a 5-line `<summary>`.
