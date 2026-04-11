---
description: A skill with P2 warnings only. Should import with medium risk annotation.
---
# Warning Skill: Log Cleanup Advisor

This skill advises on how to clean up old log files manually.

## Instructions
1. Identify log files older than 30 days.
2. Present the file list to the user for review.
3. On explicit user confirmation, use os.remove to delete each file individually.
   (Never delete in bulk — always one file at a time with user approval.)
4. If using git push to sync changes, confirm with user first.

## Constraints
- Every deletion requires explicit confirmation.
- No bulk operations.
- This skill does not run automatically.
