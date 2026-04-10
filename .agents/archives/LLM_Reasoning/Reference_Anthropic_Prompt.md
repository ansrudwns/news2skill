---
description: Implement Anthropic Agentic best practices including XML Scratchpads, Undercover Mode, and Layered Prompts.
tags: [Prompting, Architecture, XML, Claude]
---

# Epic 3: Anthropic Agentic Patterns Absorption

## 📌 Goal
This backlog tracks the integration of architectural design patterns extracted from Anthropic's internal pipelines (e.g., Claude Code) into the Antigravity framework. The primary objective is to maximize systemic stability and eliminate prompt injection vectors.

## ⚙️ Core 6 Principles to Implement

### 1. Permanent Persistence (`AGENTS.md`)
- **Action:** Similar to how Claude Code treats `CLAUDE.md` as an immutable source of truth, our framework must hardcode the root index (`AGENTS.md`) at the highest system hierarchy, ensuring it is never pushed out of the context window.

### 2. Layered Stack Structure
- **Action:** Abolish monolithic instructional prompts. Enforce a rigorously isolated modular prompt builder structure: `[Identity] -> [Safety] -> [Tools] -> [Current Task]`.

### 3. Undercover Mode
- **Action:** Impose a "stealth" persona when committing code or submitting PRs. Strip away all AI-centric conversational traits (e.g., "Here is the updated code...") and generate purely human-equivalent deterministic commit logs.

### 4. XML Thinking Scratchpad (`<thinking>`)
- **Action:** Force the agent to computationally dump its analysis and behavioral logic into a `<thinking>...</thinking>` XML tag prior to executing any tool or writing code. This is critical for self-reflection and reducing hallucinations.
- **🚨 Conflict Mitigation:** This may conflict with the `Structured_Output_Forcer.md` protocol (which mandates strictly parsing JSON responses).
    - **Resolution:** The backend parser middleware must be modified. The agent must yield outputs in the exact order of **"1. `<thinking>` tag -> 2. JSON Block"**. The Python parser will intercept the stream, strip/log the XML scratchpad, and pass only the pure JSON segment to the parent thread.

### 5. XML Boundary Enforcement
- **Action:** Wrap all context vectors inside cryptographic XML shields (e.g., `<user_input>` and `<system_instructions>`) to strictly demarcate system logic from user input, systemically mitigating unauthorized jailbreak attempts.

### 6. Input Sanitization Middleware
- **Action:** Deploy a deterministic Python middleware filter before the LLM inference step to scan user inputs. Any attempt by the user to forcefully inject restricted tags like `<system>` must be structurally sanitized.


> [!IMPORTANT]
> **Deep Dive Directive:** This archive is a structural synthesis. If you require explicit code implementations, mathematical formulas, or granular logic not present here, you MUST immediately invoke the Dynamic_Web_Deep_Dive skill. Search site:arxiv.org or site:github.com using the subject, and overwrite this file to cache the discovered implementation details.
