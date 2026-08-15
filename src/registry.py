"""Evidence registry with explicit scientific execution states."""
from __future__ import annotations

import hashlib
import json
from enum import Enum
from pathlib import Path


class EvidenceState(str, Enum):
    PROTOCOL_DEFINED = "PROTOCOL_DEFINED"
    EXECUTED = "EXECUTED"
    NOT_EXECUTED = "NOT_EXECUTED"
    FAILED = "FAILED"
    VERIFIED = "VERIFIED"


def verify_registry(registry: dict, root: str | Path) -> list[str]:
    failures: list[str] = []
    root = Path(root)
    for item in registry.get("items", []):
        state = EvidenceState(item["state"])
        evidence = item.get("evidence", [])
        if state in {EvidenceState.EXECUTED, EvidenceState.VERIFIED} and not evidence:
            failures.append(f"{item['id']}: {state.value} requires evidence")
        for record in evidence:
            path = root / record["path"]
            if not path.is_file():
                failures.append(f"{item['id']}: missing {record['path']}")
            elif hashlib.sha256(path.read_bytes()).hexdigest() != record.get("sha256"):
                failures.append(f"{item['id']}: checksum mismatch for {record['path']}")
    return failures


def load_registry(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))
