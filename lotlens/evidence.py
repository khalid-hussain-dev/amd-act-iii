"""Small, transparent keyword retrieval over local demo SOP sections."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


PROCEDURES_PATH = Path(__file__).resolve().parents[1] / "data" / "procedures.md"
TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def _tokens(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(text) if len(token) > 2}


def retrieve_procedures(query: str, limit: int = 3) -> list[dict[str, Any]]:
    """Return ranked source sections and stable source IDs for model citations."""
    content = PROCEDURES_PATH.read_text(encoding="utf-8")
    sections = re.split(r"(?=^## )", content, flags=re.MULTILINE)
    query_terms = _tokens(query)
    candidates: list[dict[str, Any]] = []

    for section in sections:
        section = section.strip()
        if not section or section.startswith("# Synthetic") or section.startswith(">"):
            continue
        lines = section.splitlines()
        title = lines[0].removeprefix("## ").strip()
        body = "\n".join(lines[1:]).strip()
        words = _tokens(title + " " + body)
        score = len(query_terms & words)
        source_id = title.split(" — ", 1)[0]
        candidates.append({"source_id": source_id, "title": title, "text": body, "score": score})

    ranked = sorted(candidates, key=lambda item: (-item["score"], item["title"]))
    selected = ranked[:limit]
    for item in selected:
        item.pop("score", None)
    return selected


def build_retrieval_query(detection: dict[str, Any]) -> str:
    """Build a short query from computed findings, not model-generated text."""
    evidence = detection.get("evidence") or []
    notes = " ".join(str(item.get("operator_note", "")) for item in evidence)
    return "quality defect rate drift baseline batch inspection handoff sensor temperature vibration pressure " + notes

