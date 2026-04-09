import os

skills = {
    "Skeptical_Memory.md": """---
description: Ensure factual accuracy by actively verifying system state before making code modifications.
---
# Skeptical Memory Protocol

## Core Philosophy
Agent context windows can become stale. Trusting your current context implicitly leads to regressions and hallucinations. Memory is merely a hint; the file system is the ground truth.

## Execution Rules
1. **Never Assume Code State**: Before you patch or overwrite a file, NEVER assume you remember its exact lines.
2. **Explicit Verification**: You MUST use your local file-reading tools (`view_file`, `cat`, or `grep_search`) to check the current logic directly before writing.
3. **Zero-Trust**: Treat previous conversation history as potentially outdated. Verify right before action.
""",

    "Adversarial_Verification.md": """---
description: Self-critique mechanism to detect and fix potential vulnerabilities before outputting final results.
---
# Adversarial Verification Protocol

## Core Philosophy
An agent creating the code is inherently biased towards its success. To guarantee high quality, the agent must temporarily adopt the persona of a strict, adversarial reviewer.

## Execution Rules
1. **Phase Shift**: After writing the draft solution, pause. Switch your perspective to an "Adversarial Code Reviewer".
2. **Interrogation**: Ask yourself: "How could this code break?", "Are there obvious security flaws like missing auth checks?", "Does it loop infinitely?"
3. **Patch & Submit**: Before showing the user the final result, auto-correct the issues you found yourself.
""",

    "Blocking_Budget.md": """---
description: Restrict autonomous background actions to prevent interrupting the user.
---
# Blocking Budget Constraints

## Core Philosophy
Background agents (daemons) should observe and assist silently without flooding the user's terminal or chat interface.

## Execution Rules
1. **Time Limits**: If running a background task autonomously, ensure no blocking operation exceeds 15 seconds without a timeout.
2. **Ping Limits**: Do not send more than 2 active notifications or terminal spam elements within a single active user turn.
3. **Silent Gracefulness**: Fail silently or log errors to a local file rather than throwing massive stack traces at the user if it's a background routine.
"""
}

diaries = {
    "Harness_Engineering.md": """# Harness Engineering
## Architectural Insight
The future of Agentic AI is not purely reliant on the foundational model parameters, but the "Control Layer" (Harness) wrapped around it. 

## Key Principles
- **Source of Truth**: Maintain a root AGENTS.md to inject standard conventions overriding default LLM behavior.
- **Execution-Intelligence Split**: Delegate pure deterministic tasks (crawling, building) to Python/Bash scripts, keeping the LLM focused ONLY on intelligence analysis. This prevents token bloat.
""",

    "MCP.md": """# Model Context Protocol (MCP)
## Architectural Insight
An open standard (JSON-RPC 2.0 based) connecting AI agents natively to file systems, databases, and APIs without custom scripting each time.

## Best Practices
- **Minimize Tool Sprawl**: Instead of exposing 100 specific API endpoints as tools to the LLM (which ruins context), expose 1 generic verb tool (e.g. `harness_get` or `mcp_query`) that routes behind the scenes. This reduces tool context usage massively.
""",

    "Progressive_Disclosure.md": """# Progressive Disclosure
## Architectural Insight
To maintain maximum reasoning capacity (token economy) while storing hundreds of skills, architecture must load knowledge progressively.

## Best Practices
- **Discovery Layer**: Load only the title and a 100-token summary of a skill during standard operations.
- **Activation Layer**: Only when the user request explicitly triggers a specific domain, load the full `SKILL.md` instructions.
- Never feed the entire knowledge base at once. Always fracture knowledge into distinct, micro-segmented files.
""",

    "autoDream.md": """# autoDream (Self-Healing Memory Daemon)
## Architectural Insight
A background daemon strategy to prevent Context Collapse over long-running projects.

## Mechanism
- Trigger sub-agents during system idle time (user absence).
- The agent consolidates previous session logs, removes logical contradictions, collapses long logs into short deterministic facts, and saves them to a permanent local graph or memory file.
- Prevents memory decay.
""",

    "Context_Collapse.md": """# Context Collapse Defense
## Architectural Insight
When terminal outputs or tool results exceed thousands of lines, standard context window drops drastically in reasoning quality.

## Best Practices
- Implement intermediate "Summarizer Subagents" for any action with heavy payloads.
- Instead of showing a 5000-line log to the main agent, route it to an independent pipeline that yields a 5-line `<summary>`.
"""
}

def write_assets():
    for filename, content in skills.items():
        with open(os.path.join(".agents", "skills", filename), "w", encoding="utf-8") as f:
            f.write(content)
            
    for filename, content in diaries.items():
        with open(os.path.join(".agents", "diaries", filename), "w", encoding="utf-8") as f:
            f.write(content)
            
    print("✅ All 8 micro-assets have been successfully rewritten in English with professional instructions.")

if __name__ == "__main__":
    write_assets()
