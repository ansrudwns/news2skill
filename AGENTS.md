# Antigravity Agent — Knowledge Registry

This is the central registry for this personal AI R&D knowledge pipeline.
Before starting any task, read this file first. If the task relates to one of the domains below, use a file-reading tool to load the relevant `.md` file before proceeding. Do not load files you don't need — follow Progressive Disclosure.

## Track A: Executable Skills Registry

### [RESEARCH MODE] AI Scientist Protocol
- **Research_Dialectic_Tree_Search (Orchestrator)**: "[RESEARCH MODE] The ultimate entry point and Orchestrator for 5th gear RAG/Benchmarking. Manages AST sandboxes, dialectic loops, and multi-agent synergy." (Path: `.agents/skills/Research_Dialectic_Tree_Search.md`)
  - **Phase 1 Sub-module**: *Research_Progressive_Tree_Search* (Path: `.agents/skills/Research_Progressive_Tree_Search.md`)
  - **Phase 2 Sub-module**: *Research_Toy_Sandboxing* (Path: `.agents/skills/Research_Toy_Sandboxing.md`)
  - **Phase 3 Sub-module**: *Adversarial_Verification* (Path: `.agents/skills/Adversarial_Verification.md`)
  - **Phase 4 Sub-module**: *Iterative_Dialectic_RAG* (Path: `.agents/skills/Iterative_Dialectic_RAG.md`)
  - **Phase 5 Sub-module**: *Research_Formal_Verifier* (Path: `.agents/skills/Research_Formal_Verifier.md`)
- **Research_Self_Discover**: "[RESEARCH MODE] Autonomous meta-reasoning logic topology composer." (Path: `.agents/skills/Research_Self_Discover.md`)
- **Dynamic_Web_Deep_Dive**: "[RESEARCH MODE] Intercept information gaps, fetch primary sources (papers/docs) via search, and formulate archive patches for explicit user approval." (Path: `.agents/skills/Dynamic_Web_Deep_Dive.md`)

### [STANDARD MODE] Automation & Engineering
- **IG_Search_RL**: No description provided. (Path: `.agents/skills/IG_Search_RL.md`)
- **SnapState**: No description provided. (Path: `.agents/skills/SnapState.md`)
- **ClawGuard**: No description provided. (Path: `.agents/skills/ClawGuard.md`)

- **Anthropic_Prompting**: Implement Anthropic Agentic best practices including XML Scratchpads, Undercover Mode, and Layered Prompts. (Path: `.agents/skills/Anthropic_Prompting.md`)
- **Defensive_Execution_Protocol**: Unified robust execution enforcing dummy returns, exponential backoffs, and strict JSON schemas, suppressing infinite loops and pipeline crashes. (Path: `.agents/skills/Defensive_Execution_Protocol.md`)
- **Karpathy_Strict_Mode**: Suppress AI hallucination and over-engineering by enforcing minimal, surgical code modifications. (Path: `.agents/skills/Karpathy_Strict_Mode.md`)
- **Skeptical_Memory**: Ensure factual accuracy by actively verifying system file states before code editing. (Path: `.agents/skills/Skeptical_Memory.md`)
- **Blocking_Budget**: Restrict autonomous background actions (pings/commands) to avoid blocking the user. (Path: `.agents/skills/Blocking_Budget.md`)

## Track B: Architectural Diaries Registry
- **K_Token_Merging**: No description provided. (Path: `.agents/diaries/K_Token_Merging.md`)
- **Agentic_Aggregation**: No description provided. (Path: `.agents/diaries/Agentic_Aggregation.md`)
- **Hardware_Profile**: Host hardware benchmarks and offline fallback constraints (24GB VRAM). (Path: `.agents/diaries/Hardware_Profile.md`)
- **Harness_Engineering**: The definitive meta-cognitive Control Layer playbook - combining structural guardrails, context pruning (Progressive Disclosure), and tool routing architectures (MCP). (Path: `.agents/diaries/Harness_Engineering.md`)
- **LaCT_Spatial_Memory**: Resilient Test-Time Training architecture for long-context 3D/video environments. (Path: `.agents/diaries/LaCT_Spatial_Memory.md`)
- **autoDream**: Context maintenance and background memory healing strategies. (Path: `.agents/diaries/autoDream.md`)

## Track C: Research Backlog (Epics)
- **TurboQuant_Compression**: "Optimization architecture implementing TurboQuant compression patterns for bounded environments." (Path: `.agents/backlog/TurboQuant_Compression.md`)
- **Research Proposals**: `.agents/backlog/research_proposals/`

## Track D: Experimental Laboratory
- **01_Agent_Cryptographic_Identity**: Cryptographic signature infrastructure research for agent supply-chain security. (Path: `.agents/laboratory/01_Agent_Cryptographic_Identity/`)
- **02_Anthropic_Prompt_Middleware**: Prompt parsing middleware experimentation. (Path: `.agents/laboratory/02_Anthropic_Prompt_Middleware/`)
- **02_T1_Test_Time_Compute**: Inference-time compute and logical pause experiments. (Path: `.agents/laboratory/02_T1_Test_Time_Compute/`)
- **03_Draft_Inference**: Draft model execution strategies. (Path: `.agents/laboratory/03_Draft_Inference/`)
- **04_Quantization_Scale**: Quantization scaling parameter exploration. (Path: `.agents/laboratory/04_Quantization_Scale/`)

## Track E: Analytics & Staging
- **Reports**: Aggregated collection of AI-generated summaries and daily briefings. (Path: `.agents/reports/`)
- **Staging Area**: A secure holding area for unverified drafts awaiting signing and promotion. (Path: `.agents/staging/`)

## Track F: Knowledge Archives
- **INT4_Quantization_Collapse**: No description provided. (Path: `.agents/archives/INT4_Quantization_Collapse.md`)
- **Claude_Advisor_API**: Anthropic's Advisor Tool architectural paradigm for Meta-Cognitive Orchestration handoffs. (Path: `.agents/archives/Agent_Orchestration/Claude_Advisor_API.md`)
- **hnsw_3bit_quantization**: "Optimization architecture implementing 3-bit Lloyd-Max scalar quantization for HNSW vector embeddings." (Path: `.agents/archives/Mathematical_Optimization/hnsw_3bit_quantization.md`)
- **Archives**: Past reference solutions, methodologies, and closed epics used strictly as contextual memory. (Path: `.agents/archives/`)
- **Mathematical_Optimization**: "Frequency domain translations, Cosine Gradient Bypasses, and non-linear metric smoothing techniques via SIREN/FNO/SAM." (Path: `.agents/archives/Mathematical_Optimization/Reference_Gradient_Bypass.md`)

## Track G: External Approved Skill Store
- Non-authoritative, pull-based skill index for externally sourced assets.
- External skills are **not active instructions** until explicitly selected and loaded by the agent for a relevant task.
- Promotion to core AGENTS.md requires separate explicit user approval.
- See `.agents/external_approved/INDEX.json` for the discovery index.
- Managed via `python scripts/skill_triage.py`. See `.agents/external_approved/README.md` for SLSA boundary documentation.
