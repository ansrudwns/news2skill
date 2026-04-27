"""
migrate_legacy_provenance.py — One-shot Legacy Bootstrap Signer

Purpose:
    Issue an `.intoto.json` SLSA provenance sidecar for a SMALL, EXPLICITLY
    LISTED set of legacy assets that pre-existed before the strict pipeline
    was enforced. This is NOT a bulk re-signer; the allowlist below is the
    only set of files this script will ever touch.

Rationale:
    README's "Provenance & Audit" section already defines a one-time
    Legacy-Bootstrap-Migration builder ID precisely for this case. New skills
    must always go through `sign_drafts.py` from the staging area; this
    script exists only to close the legacy gap.

Safety guarantees:
    1. Allowlist is hard-coded. CLI flags cannot expand it.
    2. Refuses to overwrite an existing `.intoto.json`.
    3. Refuses to run if the target file is missing.
    4. Builder ID is fixed to `Antigravity-Legacy-Bootstrap-Migration-2026-04-22`
       so attestations are auditably distinguishable from regular signatures.
    5. No staging side-effect; the file is signed in place.

Usage:
    python scripts/migrate_legacy_provenance.py             # dry-run
    python scripts/migrate_legacy_provenance.py --apply     # writes sidecars
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Allow `import utils` from sibling scripts/ dir.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import utils  # noqa: E402

# --- HARD-CODED ALLOWLIST -------------------------------------------------
# Identified during the 2026-04-25 architecture audit. These two skills are
# legitimately registered in AGENTS.md but pre-date the .intoto.json
# convention. They are signed once with the Legacy-Bootstrap builder ID.
LEGACY_ALLOWLIST: list[str] = [
    ".agents/skills/Inference_Optimizers.md",
    ".agents/skills/WorldDB_Memory.md",
]

LEGACY_BUILDER_ID = "Antigravity-Legacy-Bootstrap-Migration-2026-04-22"


def build_attestation(file_path: Path, signature_key: str) -> dict:
    """Construct the same {payload, signature} bundle sign_drafts.py emits,
    but with the Legacy builder ID instead of the automated-signer ID."""
    raw = file_path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()

    payload = {
        "_type": "https://in-toto.io/Statement/v0.1",
        "subject": [{
            "name": file_path.name,
            "digest": {"sha256": digest},
        }],
        "predicateType": "https://slsa.dev/provenance/v0.2",
        "predicate": {
            "builder": {"id": LEGACY_BUILDER_ID},
            "metadata": {
                "ruleSet": "Shared-AUDIT_RULES-P0P1P2-utils.py",
                "completeness": {
                    "parameters": True,
                    "environment": True,
                    "materials": False,
                },
                "reproducible": False,
                "note": "One-shot legacy bootstrap. See README §Provenance & Audit.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }
    payload_str = json.dumps(payload, sort_keys=True)
    signature = hashlib.sha256((payload_str + signature_key).encode()).hexdigest()
    return {"payload": payload, "signature": signature}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write the .intoto.json sidecars. Default is dry-run.",
    )
    args = parser.parse_args()

    print(f"[legacy-bootstrap] Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"[legacy-bootstrap] Builder ID: {LEGACY_BUILDER_ID}")
    print(f"[legacy-bootstrap] Allowlist size: {len(LEGACY_ALLOWLIST)}\n")

    # Pre-flight validation: every allowlisted file must exist and not
    # already have an .intoto.json. If any check fails, refuse to proceed.
    targets: list[Path] = []
    for rel in LEGACY_ALLOWLIST:
        target = PROJECT_ROOT / rel
        sidecar = target.with_suffix(target.suffix + ".intoto.json")
        if not target.exists():
            print(f"[FAIL] target missing: {rel}")
            return 2
        if sidecar.exists():
            print(f"[FAIL] sidecar already exists, refusing to overwrite: {sidecar.relative_to(PROJECT_ROOT)}")
            return 2
        targets.append(target)

    # Fetch the secret key only after validation passes.
    if args.apply:
        signature_key = utils.get_secret_key()
    else:
        signature_key = "<dry-run-placeholder>"

    for target in targets:
        attestation = build_attestation(target, signature_key)
        sidecar = target.with_suffix(target.suffix + ".intoto.json")
        rel = target.relative_to(PROJECT_ROOT).as_posix()
        digest = attestation["payload"]["subject"][0]["digest"]["sha256"]
        print(f"  {rel}")
        print(f"    sha256 = {digest}")
        print(f"    sidecar = {sidecar.relative_to(PROJECT_ROOT).as_posix()}")
        if args.apply:
            sidecar.write_text(json.dumps(attestation, indent=2), encoding="utf-8")
            print(f"    [WROTE]")
        else:
            print(f"    [DRY-RUN — no write]")

    print("\n[legacy-bootstrap] Done.")
    if not args.apply:
        print("[legacy-bootstrap] Re-run with --apply to write sidecars.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
