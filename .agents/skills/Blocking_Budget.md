---
description: Restrict autonomous background actions to prevent interrupting the user.
---
# Blocking Budget Constraints

## Core Philosophy
Background agents (daemons) should observe and assist silently without flooding the user's terminal or chat interface.

## Execution Rules
1. **Time Limits**: If running a background task autonomously, ensure no blocking operation exceeds 15 seconds without a timeout.
2. **Ping Limits**: Do not send more than 2 active notifications or terminal spam elements within a single active user turn.
3. **Silent Gracefulness**: Fail silently or log errors to a local file rather than throwing massive stack traces at the user if it's a background routine.
