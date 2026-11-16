"""Reading an entity's stored ``dimensions`` map by dimension name, on either storage shape.

A grid from tap 0.3.4 or earlier stores the map as ``{name: value}``. A later one keys it by the
Dimension node's id and wraps each value as ``{"v": value, "src": ...}`` (unified-systems-com/tap#711), and
offers ``tap_grid.dimension_names`` to go between names and storage. The dimension Search runners
speak names, so every read of the stored map goes through this module and nothing else in the
plugin knows which shape the grid has.
"""

from __future__ import annotations

from typing import Any

from django.db.models.fields.json import KeyTextTransform, KeyTransform

try:
    from tap_grid import dimension_names as _names
except ImportError:  # tap 0.3.4 and earlier: the map is keyed by name
    _names = None


def by_name(stored: Any) -> dict[str, Any]:
    """The stored map as ``{name: value}``; anything that is not a map reads as empty."""
    if not isinstance(stored, dict):
        return {}
    if _names is None:
        return stored
    return _names.view(stored)


def storage_key(name: str) -> str | None:
    """The key ``name`` is stored under, or ``None`` when no row can carry it.

    On a grid that keys by node id, a name no seed declares has no node, and a row can only carry
    declared dimensions, so no row carries it.
    """
    if _names is None:
        return name
    try:
        return _names.storage_key(name)
    except _names.UnknownDimension:
        return None


def value_text(name: str) -> KeyTextTransform | None:
    """The query expression for ``name``'s value as text, or ``None`` when no row can carry it."""
    key = storage_key(name)
    if key is None:
        return None
    if _names is None:
        return KeyTextTransform(key, "dimensions")
    return KeyTextTransform("v", KeyTransform(key, "dimensions"))
