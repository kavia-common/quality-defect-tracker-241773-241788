"""
In-memory storage for defects (demo-safe).

This module intentionally avoids any external services or persistence. Data will
reset when the Flask process restarts.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4


def _now_iso() -> str:
    """Return current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Defect:
    """Internal defect record shape used by the demo backend."""

    id: str
    title: str
    description: str = ""
    status: str = "Open"
    severity: str = "Medium"
    createdAt: str = field(default_factory=_now_iso)
    updatedAt: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict:
        """Convert defect to JSON-serializable dict."""
        return asdict(self)


class DefectsStore:
    """A tiny in-memory store for defects."""

    def __init__(self) -> None:
        self._items: Dict[str, Defect] = {}

    def list(self) -> List[dict]:
        """List all defects."""
        return [d.to_dict() for d in self._items.values()]

    def get(self, defect_id: str) -> Optional[dict]:
        """Get a defect by id."""
        defect = self._items.get(defect_id)
        return defect.to_dict() if defect else None

    def create(self, payload: dict) -> dict:
        """Create a defect from payload."""
        defect_id = payload.get("id") or str(uuid4())
        now = _now_iso()

        defect = Defect(
            id=defect_id,
            title=str(payload.get("title") or "").strip() or "Untitled defect",
            description=str(payload.get("description") or ""),
            status=str(payload.get("status") or "Open"),
            severity=str(payload.get("severity") or "Medium"),
            createdAt=str(payload.get("createdAt") or now),
            updatedAt=str(payload.get("updatedAt") or now),
        )
        self._items[defect.id] = defect
        return defect.to_dict()

    def update(self, defect_id: str, payload: dict) -> Optional[dict]:
        """Patch/update defect fields."""
        defect = self._items.get(defect_id)
        if not defect:
            return None

        # Patch semantics: only update provided fields.
        if "title" in payload:
            defect.title = str(payload.get("title") or "").strip() or defect.title
        if "description" in payload:
            defect.description = str(payload.get("description") or "")
        if "status" in payload:
            defect.status = str(payload.get("status") or defect.status)
        if "severity" in payload:
            defect.severity = str(payload.get("severity") or defect.severity)

        defect.updatedAt = _now_iso()
        return defect.to_dict()

    def delete(self, defect_id: str) -> bool:
        """Delete a defect by id."""
        return self._items.pop(defect_id, None) is not None


# Singleton store instance for the demo app.
STORE = DefectsStore()
