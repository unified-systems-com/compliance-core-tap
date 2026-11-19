"""Shared test scaffolding for the compliance_core plugin's suite."""

import pytest


def dimension_view(entity) -> dict:
    """An entity's dimensions as ``{name: value}``, whichever way the grid under test stores them.

    A grid from tap 0.3.4 or earlier stores that map directly. A later one keys it by Dimension
    node and wraps each value; its own ``view`` turns that back into names and values.
    """
    try:
        from tap_grid.dimension_names import view
    except ImportError:
        return dict(entity.dimensions or {})
    return view(entity.dimensions)


def stored(dimensions: dict) -> dict:
    """A ``{name: value}`` map in the shape the grid under test stores, for a test that writes a spine row directly.

    Such a test puts a value the service layer would refuse (JSON null, a number) on a row. On a grid that keys the map
    by Dimension node, each name becomes its node's id and each value is wrapped.
    """
    try:
        from tap_grid import dimension_names
    except ImportError:
        return dimensions
    return {dimension_names.storage_key(name): {"v": value, "src": "declared"} for name, value in dimensions.items()}


# Dimension names the Search-runner tests stamp on entities. They belong to no plugin: the runners take the key as an
# input and know none, so the tests make their own.
TEST_DIMENSIONS = ("zone", "team", "inventory", "a__b", "has.dot", "x__isnull")


def _live_names() -> set[str] | None:
    """The names live Dimension nodes carry, or None on a grid that accepts any key (tap 0.3.4 or earlier)."""
    try:
        from tap_grid.live_dimensions import vocabulary
    except ImportError:
        return None
    return set(vocabulary().by_name)


def grid_requires_declared_dimensions() -> bool:
    """Whether the grid under test refuses a dimension key that no live Dimension node declares."""
    return _live_names() is not None


def declare_dimension(name: str, description: str = "") -> None:
    """Declare the Dimension node ``name`` with ``description``, whether or not the grid already carries the name.

    A grid that only accepts declared dimensions refuses a second node of one name, and core's test harness seeds
    some of the names these suites use (``zone``). So a name that is already live keeps its node and takes the
    description; any other name gets a new node. On a grid from tap 0.3.4 or earlier the node is simply created.
    """
    from tap_grid.models import Dimension
    from tap_grid.services import WriteOperation, write_batch

    live = _live_names()
    if live is not None and name in live:
        if description:
            Dimension.objects.filter(name=name).update(description=description)
        return
    payload = {"name": name, "description": description} if description else {"name": name}
    result = write_batch([WriteOperation(verb="create_node", type_slug="dimension", payload=payload)])
    assert result.success, result.errors or [r.errors for r in result.results]  # nosec B101


@pytest.fixture(autouse=True)
def declared_test_dimensions(request):
    """Declare ``TEST_DIMENSIONS`` for a database test, on a grid that only accepts declared dimensions.

    Such a grid resolves a dimension name through its live Dimension nodes, so each name the suites stamp needs a
    node before the first write. A grid from tap 0.3.4 or earlier accepts any key and needs nothing.
    """
    marker = request.node.get_closest_marker("django_db")
    if marker is None or _live_names() is None:
        return
    request.getfixturevalue("transactional_db" if marker.kwargs.get("transaction") else "db")
    for name in TEST_DIMENSIONS:
        declare_dimension(name)
