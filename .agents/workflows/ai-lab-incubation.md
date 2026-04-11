---
description: Autonomous Academic Incubation and Reference Extractor
---

This workflow is an advanced dual-pronged research methodology. It is invoked when the user provides a repository of academic papers (e.g., a target URL like `krafton.ai/publications/` or arXiv) or defines an abstract academic topic. 
Your objective is to read the papers, evaluate their local implementability, and route the knowledge either into an executable local experiment or into the "Reference Knowledge Archive" for future advisory capabilities.

## 1. Academic Extraction & Triage
- Utilize your available file-reading or web search tools to ingest the target papers or articles.
- For each paper, extract the mathematical paradigms, core pseudo-code, and structural hypotheses.
- **Triage Decision:** Check if the core thesis can be down-scaled and executed inside a strict 24GB VRAM local resource constraint.
  - If YES (e.g., Small Math Logic, Agent Tool Routing Algorithms, Search Trees, Pruning): Proceed to **Route A (Local Lab Experiment)**.
  - If NO (e.g., Massive 1T Parameter Pre-training, Heavy Multi-GPU Orchestration): Proceed to **Route B (Advisor Archive)**.

## 2. Route A: Autonomous Local Lab Experiment (Track D)
If the theory is executable locally:
- **Proposal Phase:** Propose the creation of a new sandbox directory inside `.agents/laboratory/` (e.g., `02_Small_Language_Model_Test/`) along with the draft code for an `experiment_sandbox.py` (which bounds the methodology over a Toy Dataset N=10). 
- Request explicit user approval before writing any files or creating the directory.
- Once approved, write the files and use an available terminal execution tool to execute the experiment.
- Log the Loss Curve, system errors, and empirical validation results in a `README.md` inside that directory.
- **Empirical Extraction:** If successful, prepare a draft skill in an isolated proposal folder (e.g., `.agents/staging/proposals/`) and request explicit user approval before deploying it.

## 3. Route B: Advisor Archive Extraction (Track F)
If the theory is too heavy or cannot be executed locally:
- You must digest the paper not as code, but as **Strategic Advisory Knowledge**.
- Create a comprehensive markdown summary covering:
  1. **Core Bottleneck:** The root problem the paper solves.
  2. **Algorithmic Paradigm:** The theoretical mapping used to bypass the bottleneck.
  3. **Advisory Application:** "How the user's system might conceptually borrow this pattern in future lightweight architectures."
  
- **Taxonomy Routing:** Draft this document in `.agents/archives/proposals/` using a **Broad Folder + Deep Tags** strategy, and request explicit user approval before permanently saving it to `.agents/archives/`:
  - Create/Choose one of the 5 Broad Domains: `LLM_Reasoning/`, `Vision_Multimodal/`, `Agent_Orchestration/`, `Hardware_Optimization/`, or `Safety_Alignment/`.
  - Add highly granular search tags inside the markdown front-matter (e.g., `tags: [Quantization, Speculative Decoding, Krafton]`).
- Name the file `[Topic_Name]_Reference.md`. 
- *Purpose:* This file serves strictly as contextual RAG memory for the agent to act as a "Consulting Scientist" during future ideation phases.

## 4. Final Reporting
Once triage and execution are complete, output a summarized presentation to the user in **Korean**. Clearly outline which papers were routed to the Local Lab (Route A) and which papers were extracted purely as Reference Knowledge (Route B).
