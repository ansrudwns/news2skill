---
source_path: external_skills/test_fixtures/Warning_Skill.md
imported_at: 2026-04-11
risk_level: Medium
warnings: ["os.remove", "git push"]
---
<!-- Original external skill content below -->
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
