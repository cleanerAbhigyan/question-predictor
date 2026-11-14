"""Artificial metadata only. EXAMPLE records are never CLI/public inputs."""

from predictor.records import RIGHTS

AT = "2026-01-02T00:00:00Z"
CID = "EXAMPLE-cand-artificial"
EID = "EXAMPLE-ev-artificial"
SID = "EXAMPLE-slot-artificial"
NOTION = "https://app.notion.com/p/" + "0" * 32
URL = "https://example.org/artificial-collection"


def claim():
    return dict(
        year=2020,
        phase="I",
        paper="combined",
        session=None,
        missing_reasons={"session": "not_provided"},
        evidence_refs=[EID],
    )


def registry():
    c = dict(
        candidate_id=CID,
        revision=1,
        example_only=True,
        title="Artificial metadata fixture",
        provider="Example provider",
        landing_url=URL,
        content_kind="landing_page",
        source_category="unverified",
        authentication_status="unreviewed",
        readability_status="unreviewed",
        completeness_status="unknown",
        answer_status="unknown",
        review_status="pending",
        access_state="landing_read",
        discoverability="lead_only",
        published_on=None,
        answer_key=None,
        content_hash=None,
        paper_identity=None,
        missing_reasons={
            f: "not_checked"
            for f in ("published_on", "answer_key", "content_hash", "paper_identity")
        },
        rights={
            s: dict(status="unknown", missing_reason="not_checked", evidence_refs=[])
            for s in RIGHTS
        },
        claims=[claim()],
        evidence_refs=[EID],
        unresolved=["Artificial fixture; no real paper."],
    )
    event = dict(
        event_id=EID,
        subject_id=CID,
        subject_revision=1,
        source_url=URL,
        assessed_at=AT,
        assessor="agent_metadata_review",
        summary="Artificial landing metadata fixture only.",
        source_category="unverified",
        claims=[{**claim(), "evidence_refs": []}],
        published_on=None,
        rights={},
        access_state="landing_read",
    )
    return dict(schema_version="1.0.0", as_of=AT, candidates=[c], slots=[], ledger=[event])
