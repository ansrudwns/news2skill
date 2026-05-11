# Antigravity Agent — Knowledge Registry

This is the central registry for this personal AI R&D knowledge pipeline.
Before starting any task, read this file first. If the task relates to one of the domains below, use a file-reading tool to load the relevant `.md` file before proceeding. Do not load files you don't need — follow Progressive Disclosure.

## Track A: Executable Skills Registry

### [RESEARCH MODE] AI Scientist Protocol
- **Research_Dialectic_Tree_Search**: "[RESEARCH MODE] The ultimate entry point and Orchestrator for 5th gear RAG/Benchmarking. Manages AST sandboxes, dialectic loops, and multi-agent synergy." (Path: `.agents/skills/Research_Dialectic_Tree_Search.md`)
  - **Research_Progressive_Tree_Search**: Phase 1 Sub-module. (Path: `.agents/skills/Research_Progressive_Tree_Search.md`)
  - **Research_Toy_Sandboxing**: Phase 2 Sub-module. (Path: `.agents/skills/Research_Toy_Sandboxing.md`)
  - **Adversarial_Verification**: Phase 3 Sub-module. (Path: `.agents/skills/Adversarial_Verification.md`)
  - **Iterative_Dialectic_RAG**: Phase 4 Sub-module. (Path: `.agents/skills/Iterative_Dialectic_RAG.md`)
  - **Research_Formal_Verifier**: Phase 5 Sub-module. (Path: `.agents/skills/Research_Formal_Verifier.md`)
- **Research_Self_Discover**: "[RESEARCH MODE] Autonomous meta-reasoning logic topology composer." (Path: `.agents/skills/Research_Self_Discover.md`)
- **Dynamic_Web_Deep_Dive**: "[RESEARCH MODE] Intercept information gaps, fetch primary sources (papers/docs) via search, and formulate archive patches for explicit user approval." (Path: `.agents/skills/Dynamic_Web_Deep_Dive.md`)

### [STANDARD MODE] Automation & Engineering

- **small_model_scaffold**: Prompt engineering and scaffolding adaptations to dramatically increase coding proficiency in sub-10B parameter LLMs. (Path: `.agents/skills/small_model_scaffold.md`)
- **IG_Search_RL**: [RESEARCH MODE] Step-Level Information Gain heuristic that prunes redundant search branches inside Research_Dialectic_Tree_Search via novelty-vs-overlap scoring. (Path: `.agents/skills/IG_Search_RL.md`)
- **SnapState**: Workflow resilience layer — serializes pipeline state to `.agents/staging/checkpoint.json` on Dummy Returns so retries resume rather than burn API tokens from scratch. (Path: `.agents/skills/SnapState.md`)
- **ClawGuard**: Runtime boundary shield against indirect prompt injection — sanitizes MCP/web payloads with aggressive regex at the tool_call input boundary, the only place regex is permitted under DSP Rule 2. (Path: `.agents/skills/ClawGuard.md`)

- **Anthropic_Prompting**: Implement Anthropic Agentic best practices including XML Scratchpads, Undercover Mode, and Layered Prompts. (Path: `.agents/skills/Anthropic_Prompting.md`)
- **Defensive_Execution_Protocol**: Unified robust execution enforcing dummy returns, exponential backoffs, and strict JSON schemas, suppressing infinite loops and pipeline crashes. (Path: `.agents/skills/Defensive_Execution_Protocol.md`)
- **Karpathy_Strict_Mode**: Suppress AI hallucination and over-engineering by enforcing minimal, surgical code modifications. (Path: `.agents/skills/Karpathy_Strict_Mode.md`)
- **Skeptical_Memory**: Ensure factual accuracy by actively verifying system file states before code editing. (Path: `.agents/skills/Skeptical_Memory.md`)
- **Blocking_Budget**: Restrict autonomous background actions (pings/commands) to avoid blocking the user. (Path: `.agents/skills/Blocking_Budget.md`)
- **WorldDB_Memory**: Ontology-Aware Agentic Graph Memory for Context Collapse Prevention. (Path: `.agents/skills/WorldDB_Memory.md`)
- **Inference_Optimizers**: Advanced Hardware Optimization & Error Correction Protocols (LPSR & EDEN). (Path: `.agents/skills/Inference_Optimizers.md`)

## Track B: Architectural Diaries Registry
- **Skill_Quality_Schema**: Six-axis evaluation schema (Trigger / Thresholds / DO-DON'T / Failure Mode / Cross-Skill Edges / Self-Verification) that any new skill draft MUST answer before promotion out of staging. (Path: `.agents/diaries/Skill_Quality_Schema.md`)
- **Adaptive_Head_Budgeting**: Adaptive Head Budgeting for Multi-Head Attention under Hardware Constraints (Path: `.agents/diaries/Adaptive_Head_Budgeting.md`)
- **K_Token_Merging**: Context compression via cosine-similarity-based agglomerative merging of adjacent token latents — mitigates O(N²) attention scaling and feeds into the autoDream healing loop. (Path: `.agents/diaries/K_Token_Merging.md`)
- **Agentic_Aggregation**: Hierarchical Map-Reduce architecture (Planner → Fanout → Synthesizer) gated to engage only above 80% prompt usage or anticipated 180s timeout, per Harness_Engineering Pillar 2. (Path: `.agents/diaries/Agentic_Aggregation.md`)
- **Hardware_Profile**: Host hardware benchmarks and offline fallback constraints (24GB VRAM). (Path: `.agents/diaries/Hardware_Profile.md`)
- **Harness_Engineering**: The definitive meta-cognitive Control Layer playbook - combining structural guardrails, context pruning (Progressive Disclosure), and tool routing architectures (MCP). (Path: `.agents/diaries/Harness_Engineering.md`)
- **LaCT_Spatial_Memory**: Resilient Test-Time Training architecture for long-context 3D/video environments. (Path: `.agents/diaries/LaCT_Spatial_Memory.md`)
- **autoDream**: Context maintenance and background memory healing strategies. (Path: `.agents/diaries/autoDream.md`)

## Track C: Research Backlog (Epics)
- **SkillOS**: Dynamic skill curation layer for selecting relevant agent skills by task context and reducing context-window bloat. (Path: `.agents/backlog/SkillOS.md`)
- **Recursive_Agent_Optimization**: Recursive agent optimization workflow for spawning bounded sub-agents to improve prompts, tool use, or weak intermediate outputs. (Path: `.agents/backlog/Recursive_Agent_Optimization.md`)
- **wasserstein_metric**: Concept for fixing tensor drift in quantized GGUF models via Wasserstein metric W1 (Path: `.agents/backlog/wasserstein_metric.md`)
- **kv_svd_compression**: Multi-stage KV cache compression utilizing Entropy selection, OLS reconstruction, and SVD. (Path: `.agents/backlog/kv_svd_compression.md`)
- **kv_cartridges_still**: Open-source single-GPU reproduction of Cartridges and STILL for Neural KV-cache Compaction. (Path: `.agents/backlog/kv_cartridges_still.md`)
- **TurboQuant_Compression**: "Optimization architecture implementing TurboQuant compression patterns for bounded environments." (Path: `.agents/backlog/TurboQuant_Compression.md`)
- **Research Proposals**: `.agents/backlog/research_proposals/`

## Track D: Experimental Laboratory
- **01_Agent_Cryptographic_Identity**: Cryptographic signature infrastructure research for agent supply-chain security. (Path: `.agents/laboratory/01_Agent_Cryptographic_Identity/`)
- **02_Anthropic_Prompt_Middleware**: Prompt parsing middleware experimentation. (Path: `.agents/laboratory/02_Anthropic_Prompt_Middleware/`)
- **03_Draft_Inference**: Draft model execution strategies. (Path: `.agents/laboratory/03_Draft_Inference/`)
- **04_Quantization_Scale**: Quantization scaling parameter exploration. (Path: `.agents/laboratory/04_Quantization_Scale/`)
- **05_Dual_Agent_Codex**: Dual Agent Harness experimentation integrating Claude Code CLI via isolated subprocess bridges. (Path: `.agents/laboratory/05_Dual_Agent_Codex/`)
- **06_Test_Time_Compute**: Inference-time compute and logical pause experiments. (Path: `.agents/laboratory/06_Test_Time_Compute/`)
- **07_Sandbox**: Experimental environment for execution sandboxing and AST validation. (Path: `.agents/laboratory/07_Sandbox/`)

## Track E: Analytics & Staging
- **Reports**: Aggregated collection of AI-generated summaries and daily briefings. (Path: `.agents/reports/`)
- **Staging Area**: A secure holding area for unverified drafts awaiting signing and promotion. (Path: `.agents/staging/`)

## Track F: Knowledge Archives
- **StraTA**: Reference archive for strategic trajectory abstraction in long-horizon agentic reinforcement learning. (Path: `.agents/archives/StraTA.md`)
- **Gradient_von_Neumann_Entropy**: Data-Free Contribution Estimation in FL using Gradient von Neumann Entropy (Path: `.agents/archives/Gradient_von_Neumann_Entropy.md`)
- **turboquant_eden_note**: Theoretical grounding for TurboQuant relating back to DRIVE and EDEN algorithms. (Path: `.agents/archives/turboquant_eden_note.md`)
- **test_time_correction**: Inference-Time Error Correction via Residual Stream Monitoring and KV-Cache Steering (Path: `.agents/archives/test_time_correction.md`)
- **mixture_of_depths**: Mixture-of-Depths Attention for mitigating deep layer signal dilution. (Path: `.agents/archives/mixture_of_depths.md`)
- **gradient_fingerprints**: Detecting Reward Hacking in RL environments via Gradient Fingerprints. (Path: `.agents/archives/gradient_fingerprints.md`)
- **c64_transformer**: A real transformer model running on a 1 MHz Commodore 64, providing a paradigm of extreme hardware constraints. (Path: `.agents/archives/c64_transformer.md`)
- **asmr_bench**: Auditing ML Research systems for autonomous sabotage. (Path: `.agents/archives/asmr_bench.md`)
- **INT4_Quantization_Collapse**: Diagnoses INT4 PTQ failure modes (Hessian eigenvector misalignment under discrete projection) and prescribes orthogonal clipping plus LoRA outlier compensation for 24GB constrained deployments. (Path: `.agents/archives/INT4_Quantization_Collapse.md`)
- **Claude_Advisor_API**: Anthropic's Advisor Tool architectural paradigm for Meta-Cognitive Orchestration handoffs. (Path: `.agents/archives/Agent_Orchestration/Claude_Advisor_API.md`)
- **hnsw_3bit_quantization**: "Optimization architecture implementing 3-bit Lloyd-Max scalar quantization for HNSW vector embeddings." (Path: `.agents/archives/Mathematical_Optimization/hnsw_3bit_quantization.md`)
- **Reference_Agent_Distillation_Framework**: Reference Archive: Structured Distillation of Web Agent Capabilities Enables Generalization (Agent-as-Annotators) (Path: `.agents/archives/Agent_Orchestration/Reference_Agent_Distillation_Framework.md`)
- **Reference_Execution_Loop**: Implement robust error loops and Ouroboros logic for python execution. (Path: `.agents/archives/Agent_Orchestration/Reference_Execution_Loop.md`)
- **Reference_Orak_Benchmark**: A Foundational Benchmark for Training and Evaluating LLM Agents on Diverse Video Games (Path: `.agents/archives/Agent_Orchestration/Reference_Orak_Benchmark.md`)
- **Reference_Offline_Fallback**: Seamless routing and offline LLM inference bridging using LiteLLM. (Path: `.agents/archives/Hardware_Optimization/Reference_Offline_Fallback.md`)
- **Reference_TurboQuant**: Optimization architecture implementing TurboQuant compression patterns for bounded environments. (Path: `.agents/archives/Hardware_Optimization/Reference_TurboQuant.md`)
- **Reference_Anthropic_Prompt**: Implement Anthropic Agentic best practices including XML Scratchpads, Undercover Mode, and Layered Prompts. (Path: `.agents/archives/LLM_Reasoning/Reference_Anthropic_Prompt.md`)
- **Reference_Autonomous_AI_Researcher**: Synthesis of Autonomous AI Researcher Methodologies from OpenAI o1, Google DeepMind, and Sakana AI. (Path: `.agents/archives/LLM_Reasoning/Reference_Autonomous_AI_Researcher.md`)
- **Reference_Temporal_Extrapolation**: Epistemological guidelines and baseline modeling for temporal extrapolation, mitigating Golden Hammer bias and data masking hallucinations. (Path: `.agents/archives/Mathematical_Optimization/Reference_Temporal_Extrapolation.md`)
- **Reference_Agent_Telemetry**: Integration of OpenTelemetry architectures (Langfuse) for continuous agentic evolution. (Path: `.agents/archives/Safety_Alignment/Reference_Agent_Telemetry.md`)
- **Reference_Reward_Hacking_RL**: Reference Archive: Reward Hacking in Reinforcement Learning (Lilian Weng) (Path: `.agents/archives/Safety_Alignment/Reference_Reward_Hacking_RL.md`)
- **Reference_GRPO_Visual_Reasoning**: Reference Archive: Improving Visual Spatial Reasoning in Multimodal Language Models via Constrained Policy Optimization (Faithful GRPO) (Path: `.agents/archives/Vision_Multimodal/Reference_GRPO_Visual_Reasoning.md`)
- **Reference_VLM_SubtleBench**: How Far Are VLMs from Human-Level Subtle Comparative Reasoning? (Path: `.agents/archives/Vision_Multimodal/Reference_VLM_SubtleBench.md`)
- **Reference_Gradient_Bypass**: Frequency domain translations, Cosine Gradient Bypasses, and non-linear metric smoothing techniques via SIREN/FNO/SAM. (Path: `.agents/archives/Mathematical_Optimization/Reference_Gradient_Bypass.md`)

## Track G: External Approved Skill Store
- Non-authoritative, pull-based skill index for externally sourced assets.
- External skills are **not active instructions** until explicitly selected and loaded by the agent for a relevant task.
- **Proactive Suggestion Rule**: The agent MUST proactively scan `.agents/external_approved/INDEX.json` and suggest loading a relevant external skill when the user asks for tasks that match skill descriptions (e.g., debugging -> suggest `diagnose`, planning -> suggest `to-issues`).
- **Selective Loading Rule**: Load only the selected skill file from `.agents/external_approved/skills/`; do not bulk-load the whole external approved store.
- **Registry Boundary**: `.agents/external_approved/` stores copied, approved reference skills. `skills-lock.json` stores source-path registrations for live `external_skills/**/SKILL.md` files. Do not treat them as the same registry.
- Promotion to core AGENTS.md requires separate explicit user approval.
- See `.agents/external_approved/INDEX.json` for the discovery index.
- Managed via `python scripts/skill_triage.py`. See `.agents/external_approved/README.md` for SLSA boundary documentation.
