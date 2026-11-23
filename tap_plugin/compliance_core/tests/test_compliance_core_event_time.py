"""Event time (core's req-grid-entity-event-time, tap 0.4.7): what each compliance_core model declares, and
what core derives from it.

The first class pins the declarations, so a model added later without one, or one that names the wrong
field, fails here. `compliance_scan_run` is the one model left undeclared on purpose, held for the owner,
and the pin says so. The second class applies core's own derivation to plain values: an exception with no
ceiling is open-ended, not timeless.
"""

from datetime import UTC, datetime

from tap_plugin.compliance_core.models import (
    ComplianceArtifact,
    ComplianceBoundary,
    ComplianceContext,
    ComplianceEvidence,
    ComplianceException,
    ComplianceExceptionInstance,
    ComplianceFinding,
    ComplianceScanner,
    ComplianceScanRun,
    ComplianceSearchSnapshot,
    ComplianceVulnerability,
)

from tap_grid.event_time import NO_EVENT_TIME, Interval, Moment, declaration_problems, derive
from tap_grid.registry import get_model_class, list_entity_types

DECLARED = {
    ComplianceFinding: Moment(field="first_detected_at", kind="first_seen"),
    ComplianceVulnerability: Moment(field="published_at", kind="published"),
    ComplianceException: Interval(start="granted_at", kind="created", end="expires_at"),
    ComplianceArtifact: NO_EVENT_TIME,
    ComplianceBoundary: NO_EVENT_TIME,
    ComplianceContext: NO_EVENT_TIME,
    ComplianceEvidence: NO_EVENT_TIME,
    ComplianceExceptionInstance: NO_EVENT_TIME,
    ComplianceScanner: NO_EVENT_TIME,
    ComplianceSearchSnapshot: NO_EVENT_TIME,
}
#: Left undeclared until the owner rules what its observed_at means (see the model's comment).
UNDECLARED = {ComplianceScanRun}

GRANTED = datetime(2026, 11, 2, 9, 30, tzinfo=UTC)
CEILING = datetime(2027, 5, 2, 9, 30, tzinfo=UTC)


class TestDeclarations:
    def test_every_model_of_the_plugin_decides_or_is_held(self) -> None:
        own = {get_model_class(slug) for slug in list_entity_types() if slug.startswith("compliance_core__")}
        assert own == set(DECLARED) | UNDECLARED
        assert {model: model.EVENT_TIME for model in DECLARED} == DECLARED

    def test_the_held_model_declares_nothing(self) -> None:
        for model in UNDECLARED:
            assert "EVENT_TIME" not in vars(model), model.__name__

    def test_core_accepts_each_declaration(self) -> None:
        for model in DECLARED:
            assert declaration_problems(model) == [], model.__name__


class TestDerivation:
    def test_an_exception_holds_from_grant_to_its_ceiling(self) -> None:
        derived = derive(ComplianceException.EVENT_TIME, {"granted_at": GRANTED, "expires_at": CEILING}.get)
        assert (derived.event_start, derived.event_end, derived.kind) == (GRANTED, CEILING, "created")

    def test_an_exception_with_no_ceiling_has_no_end(self) -> None:
        derived = derive(ComplianceException.EVENT_TIME, {"granted_at": GRANTED, "expires_at": None}.get)
        assert (derived.event_start, derived.event_end, derived.kind) == (GRANTED, None, "created")

    def test_a_finding_detected_once_is_a_moment(self) -> None:
        derived = derive(ComplianceFinding.EVENT_TIME, {"first_detected_at": GRANTED}.get)
        assert (derived.event_start, derived.event_end, derived.kind) == (GRANTED, GRANTED, "first_seen")

    def test_a_finding_with_no_detection_time_has_none(self) -> None:
        derived = derive(ComplianceFinding.EVENT_TIME, {"first_detected_at": None}.get)
        assert (derived.event_start, derived.event_end, derived.kind) == (None, None, None)
