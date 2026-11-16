"""Shared test scaffolding for the compliance_core plugin's suite."""

import json
import uuid

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
_TEST_NAMESPACE = uuid.UUID("01a1d7f0-0000-7000-8000-00000000c0de")


@pytest.fixture(autouse=True)
def declared_test_dimensions(tmp_path):
    """Declare ``TEST_DIMENSIONS`` for the test, on a grid that only accepts declared dimensions.

    Such a grid takes its vocabulary from the installed seed documents, so the names are added to that table from a
    seed document of the test's own and the table is put back afterwards. A grid from tap 0.3.4 or earlier accepts
    any key and has no table.
    """
    try:
        from tap_grid import dimension_vocabulary
    except ImportError:
        yield
        return
    nodes = [
        {
            "entity": {"entity_id": str(uuid.uuid5(_TEST_NAMESPACE, name)), "entity_type": "dimension", "name": name},
            "node": {"name": name},
        }
        for name in TEST_DIMENSIONS
    ]
    batch = {"batch_entity": {"entity_id": str(_TEST_NAMESPACE), "entity_type": "batch"}, "nodes": nodes}
    seed = tmp_path / "test-dimensions.grift.json"
    seed.write_text(json.dumps({"batches": [batch]}), encoding="utf-8")
    base = dimension_vocabulary.vocabulary()
    extra = dimension_vocabulary.build([("compliance_core tests", seed)])
    dimension_vocabulary.reset(
        dimension_vocabulary.Vocabulary(by_id={**base.by_id, **extra.by_id}, by_name={**base.by_name, **extra.by_name})
    )
    try:
        yield
    finally:
        dimension_vocabulary.reset(base)
