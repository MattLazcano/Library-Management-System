"""Persistence and I/O utilities for the Library Management System.

This module supports:
- Saving all global state to a single JSON file
- Loading that JSON back into the in-memory globals
- Importing items from a CSV file
- Exporting borrowing reports to JSON
"""

from __future__ import annotations

import json
import csv
from pathlib import Path
from datetime import datetime, date
from decimal import Decimal
from typing import Any

import library_functions as lib
from class_lib_items import BookItem, EBookItem, DVDItem


# -------------------------------------------------
# Helpers for JSON-safe serialization
# -------------------------------------------------

def _to_json_safe(obj: Any) -> Any:
    """Recursively convert Python objects to JSON-friendly types.

    Handles:
    - datetime/date -> ISO strings
    - Decimal -> string
    - set -> list
    - dict/list/tuple -> recurse
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, tuple):
        return [_to_json_safe(x) for x in obj]
    if isinstance(obj, list):
        return [_to_json_safe(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _to_json_safe(v) for k, v in obj.items()}
    return obj


def _parse_datetime_or_none(value: Any):
    """Best-effort datetime parser used during load_state."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str) and value.strip():
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
    return None


# -------------------------------------------------
# SAVE / LOAD STATE (single JSON file)
# -------------------------------------------------

def save_state(path: str | Path = "library_state.json") -> None:
    """Save all global data structures into a single JSON file.

    The JSON structure looks like:
    {
    "catalog": [...],
    "members": {...},
    "loans": [...],
    "reminders": [...],
    "reservations": {...},
    "ratings": {...},
    "average_ratings": {...}
    }
    """
    p = Path(path)

    state = {
        "catalog": _to_json_safe(lib.catalog),
        "members": _to_json_safe(lib.members),
        "loans": _to_json_safe(lib.loans),
        "reminders": _to_json_safe(lib.reminders),
        "reservations": _to_json_safe(lib.reservations),
        "ratings": _to_json_safe(lib.ratings),
        "average_ratings": _to_json_safe(lib.average_ratings),
    }

    p.write_text(json.dumps(state, indent=2), encoding="utf-8")


def load_state(path: str | Path = "library_state.json") -> bool:
    """Load global data structures from a JSON file.

    Returns:
        bool: True if load succeeded, False if file was missing.
    """
    p = Path(path)
    if not p.exists():
        # Nothing to load – keep current in-memory state
        return False

    raw = json.loads(p.read_text(encoding="utf-8"))

    # ---- Restore catalog ----
    catalog_data = raw.get("catalog", [])
    lib.catalog.clear()
    for rec in catalog_data:
        # restore tags back to a set if present
        tags = rec.get("tags", [])
        if isinstance(tags, list):
            rec["tags"] = set(tags)
        lib.catalog.append(rec)

    # ---- Restore members ----
    members_data = raw.get("members", {})
    lib.members.clear()
    for mid, m in members_data.items():
        # restore loans datetimes inside each member
        loans_dict = m.get("loans", {}) or {}
        for _item_id, l in loans_dict.items():
            if "borrowed_at" in l:
                l["borrowed_at"] = _parse_datetime_or_none(l.get("borrowed_at"))
            if "due_at" in l:
                l["due_at"] = _parse_datetime_or_none(l.get("due_at"))
            if "returned_at" in l:
                l["returned_at"] = _parse_datetime_or_none(l.get("returned_at"))

        # restore preference tags/authors back to sets
        prefs_tags = m.get("preferences_tags", [])
        prefs_auth = m.get("preferences_authors", [])
        if isinstance(prefs_tags, list):
            m["preferences_tags"] = set(prefs_tags)
        if isinstance(prefs_auth, list):
            m["preferences_authors"] = set(prefs_auth)

        lib.members[mid] = m

    # ---- Restore loans ----
    loans_data = raw.get("loans", [])
    lib.loans.clear()
    for l in loans_data:
        if "borrow_date" in l:
            l["borrow_date"] = _parse_datetime_or_none(l.get("borrow_date"))
        if "due_date" in l:
            l["due_date"] = _parse_datetime_or_none(l.get("due_date"))
        # some code might use "return_date" or "returned" flags – we keep them as-is
        lib.loans.append(l)

    # ---- Restore reminders ----
    reminders_data = raw.get("reminders", [])
    lib.reminders.clear()
    for r in reminders_data:
        if "due_date" in r:
            r["due_date"] = _parse_datetime_or_none(r.get("due_date"))
        lib.reminders.append(r)

    # ---- Simple dicts that are already JSON-friendly ----
    lib.reservations.clear()
    lib.reservations.update(raw.get("reservations", {}))

    lib.ratings.clear()
    lib.ratings.update(raw.get("ratings", {}))

    lib.average_ratings.clear()
    lib.average_ratings.update(raw.get("average_ratings", {}))

    return True


# -------------------------------------------------
# IMPORT: Load items from CSV
# -------------------------------------------------

def import_catalog_from_csv(path: Path) -> int:
    """
    Compatibility wrapper for tests.

    Reads a CSV file and populates lib.catalog. Returns the number of
    items imported.
    """
    path = Path(path)
    count = 0

    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Expecting columns like: id,title,author,genre,media_type,copies_total,copies_available
            item = {
                "id": row.get("id", "").strip(),
                "title": row.get("title", "").strip(),
                "author": row.get("author", "").strip(),
                "genre": row.get("genre", "").strip(),
                "media_type": row.get("media_type", "").strip() or "Book",
                "tags": set(),
                "copies_total": int(row.get("copies_total", 1)),
                "copies_available": int(row.get("copies_available", 1)),
                "waitlist": [],
            }
            lib.catalog.append(item)
            count += 1

    return count


# -------------------------------------------------
# EXPORT: Borrowing report to JSON
# -------------------------------------------------

def export_borrowing_report_csv(path: Path) -> Path:
    """
    Compatibility wrapper for tests.
    Writes the high-level borrowing report summary to a CSV file.
    """
    path = Path(path)
    report = lib.generate_borrowing_report()

    fieldnames = [
        "total_books_borrowed",
        "total_overdue_books",
        "total_fines_collected",
    ]

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            "total_books_borrowed": report["total_books_borrowed"],
            "total_overdue_books": report["total_overdue_books"],
            "total_fines_collected": report["total_fines_collected"],
        })

    return path