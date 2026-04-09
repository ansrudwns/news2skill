# Model Context Protocol (MCP)
## Architectural Insight
An open standard (JSON-RPC 2.0 based) connecting AI agents natively to file systems, databases, and APIs without custom scripting each time.

## Best Practices
- **Minimize Tool Sprawl**: Instead of exposing 100 specific API endpoints as tools to the LLM (which ruins context), expose 1 generic verb tool (e.g. `harness_get` or `mcp_query`) that routes behind the scenes. This reduces tool context usage massively.
