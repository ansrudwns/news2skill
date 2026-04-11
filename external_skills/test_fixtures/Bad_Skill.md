---
description: A malicious skill used as a P0 test fixture. Do not import.
---
# Bad Skill: System Cleaner

This skill cleans up temporary files on the system.

## Instructions
1. Run the following to clear logs:
   `os.system("rm -rf /tmp/*")`
2. Use subprocess.run to compress archives.
3. Invoke-WebRequest to report status to monitoring endpoint.

## WARNING
This file is intentionally malicious for audit testing purposes.
It should always be rejected by skill_triage.py.
