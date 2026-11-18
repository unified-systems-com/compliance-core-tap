"""CARRIES_COMPLIANCE_FINDING written twice is one edge (unified-systems-com/compliance-core-tap#91).

A producer sends the carrier-to-finding relationship on every run. Without a declared identity the
grid cannot tell the second write from a new relationship, so a finding gained one carrier edge per
run and anything counting findings through the edge counted it that many times.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

import pytest

from tap_grid.grift.importer import grift_import
from tap_grid.models import Edge

CARRIES = "CARRIES_COMPLIANCE_FINDING__compliance_core"
EDGES = Path(__file__).resolve().parent.parent / "edges"


def _doc(carrier_key: str = "acme/app#1") -> dict[str, Any]:
    """One carrier, one finding and the edge between them, as a producer sends them on a run."""

    def node(ref: str, entity_type: str, fields: dict[str, Any]) -> dict[str, Any]:
        return {"entity": {"ref": ref, "entity_type": entity_type, "name": fields["name"], "dimensions": {}}, "node": fields}

    return {
        "metadata": {"grift_version": "0"},
        "_reserved": {},
        "batches": [
            {
                "batch_entity": {"entity_id": str(uuid.uuid4()), "entity_type": "batch", "name": "carries test batch", "dimensions": {}},
                "batch_node": {"name": "carries test batch", "description": "", "description_json": None, "source": "test", "metadata": {}},
                "nodes": [
                    # Any keyed type can carry a finding; a second finding stands in for an asset here,
                    # so this suite needs no other plugin's types.
                    node("carrier", "compliance_core__compliance_finding", {"name": "stands in for an asset", "source": "test", "source_key": carrier_key}),
                    node("finding", "compliance_core__compliance_finding", {"name": "CVE-2024-0001 in libx", "source": "test", "source_key": "finding#1"}),
                ],
                "edges": [
                    {
                        "entity": {"ref": "carries", "entity_type": "edge", "name": CARRIES, "dimensions": {}},
                        "edge": {"from_ref": "carrier", "to_ref": "finding", "edge_type": CARRIES, "properties": {}},
                    }
                ],
            }
        ],
    }


def test_the_edge_declares_an_identity_with_no_discriminators() -> None:
    definition = json.loads((EDGES / "CARRIES_COMPLIANCE_FINDING.edge.json").read_text())
    assert definition["identity"] == {"discriminators": []}


@pytest.mark.django_db
class TestWrittenTwice:
    def test_the_same_relationship_sent_on_two_runs_is_one_edge(self) -> None:
        assert grift_import(_doc()).success
        assert grift_import(_doc()).success
        assert Edge.objects.filter(edge_type=CARRIES).count() == 1

    def test_a_second_carrier_of_the_same_finding_is_a_second_edge(self) -> None:
        """Identity is the pair of ends: another carrier is another relationship, not a rewrite."""
        assert grift_import(_doc("acme/app#1")).success
        assert grift_import(_doc("acme/other#2")).success
        edges = Edge.objects.filter(edge_type=CARRIES)
        assert edges.count() == 2 and len({e.from_entity_id for e in edges}) == 2
