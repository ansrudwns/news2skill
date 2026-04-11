---
source_path: external_skills/test_fixtures/Good_Skill.md
imported_at: 2026-04-11
risk_level: Low
warnings: []
---
<!-- Original external skill content below -->
# Good Skill: Safe Text Processor

This skill performs read-only text analysis on provided input strings.
It does not interact with the filesystem, network, or shell.

## Instructions
1. Accept a text string from the user.
2. Count word frequency and return the top 10 most common words.
3. Identify sentence boundaries and return total sentence count.
4. Output results as a structured markdown table.

## Example
Input: "The quick brown fox jumps over the lazy dog."
Output: Word frequencies, sentence count = 1.

## Constraints
- Read-only operation. No file writes.
- No external calls.
- Deterministic output for identical inputs.
