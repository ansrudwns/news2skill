# autoDream (Self-Healing Memory Daemon)
## Architectural Insight
A background daemon strategy to prevent Context Collapse over long-running projects.

## Mechanism

This architecture now operates on a Two-Track Active-Sync paradigm, integrating WorldDB logic:
1. **Active Track (Write-Time Reconciliation)**: Utilizing an Ontology-Aware Vector Graph, agents reconcile nodes with the overarching graph immediately at write-time. This prevents context contradiction and fragmentation instantly without waiting for idle time.
2. **Lazy Track (Deep Consolidation)**: Trigger sub-agents during system idle time (user absence) to deeply collapse long logs into shorter deterministic facts and aggressively scrub residual redundancies.
- Together, this ensures identity continuity and permanently prevents memory decay.
