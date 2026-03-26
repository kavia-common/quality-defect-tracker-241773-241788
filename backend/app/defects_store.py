"""
In-memory storage for defects (demo-safe).

This module intentionally avoids any external services or persistence. Data will
reset when the Flask process restarts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4


def _now_iso() -> str:
    """Return current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _iso_utc(year: int, month: int, day: int, hour: int = 12, minute: int = 0, second: int = 0) -> str:
    """Return a stable ISO-8601 UTC timestamp for sample data."""
    return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc).isoformat()


@dataclass
class Defect:
    """Internal defect record shape used by the demo backend."""

    id: str
    title: str
    description: str = ""
    status: str = "Open"
    severity: str = "Major"
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
            # Frontend/user instruction uses Critical/Major/Minor; keep backend permissive.
            severity=str(payload.get("severity") or "Major"),
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


# PUBLIC_INTERFACE
def seed_sample_defects(store: DefectsStore = STORE) -> None:
    """
    Seed the in-memory store with sample defects.

    This is intended for hackathon/demo usage so the frontend shows data
    immediately after refresh.

    Seeding is idempotent: if the store already has any items, this function
    does nothing.

    Args:
        store: The DefectsStore instance to seed (defaults to the global STORE).

    Returns:
        None
    """
    if store.list():
        return

    # 3–5 sample defects per user request (using 5 for a richer dashboard).
    samples = [
        {
            "title": "Login form allows blank password submission",
            "severity": "Critical",
            "status": "Open",
            "createdAt": _iso_utc(2026, 3, 10, 9, 15, 0),
        },
        {
            "title": "Dashboard status chart miscounts 'In Progress' items",
            "severity": "Major",
            "status": "In Progress",
            "createdAt": _iso_utc(2026, 3, 12, 14, 30, 0),
        },
        {
            "title": "Mobile table layout overflows on small screens",
            "severity": "Major",
            "status": "Open",
            "createdAt": _iso_utc(2026, 3, 14, 11, 0, 0),
        },
        {
            "title": "Export CSV includes internal IDs column unexpectedly",
            "severity": "Minor",
            "status": "Complete",
            "createdAt": _iso_utc(2026, 3, 16, 16, 45, 0),
        },
        {
            "title": "Corrective action notes not persisted after refresh",
            "severity": "Critical",
            "status": "In Progress",
            "createdAt": _iso_utc(2026, 3, 18, 10, 5, 0),
        },
    ]

    for s in samples:
        # Keep updatedAt aligned to createdAt for sample data.
        store.create({**s, "updatedAt": s["createdAt"]})
