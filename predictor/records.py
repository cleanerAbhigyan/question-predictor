"""Strict Phase 1A public records; no question content or promotion to PYQs."""

import ipaddress
import json
import re
from datetime import date, datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit
from uuid import UUID

VERSION = "1.0.0"
PAPERS = {"I": ("GA", "English", "Quant", "Reasoning"), "II": ("ESI", "FM", "English Writing")}
RIGHTS = (
    "acquisition",
    "personal_analysis",
    "quotation",
    "model_ingestion",
    "public_redistribution",
)
REASONS = {
    "not_provided",
    "not_checked",
    "not_acquired",
    "unverified",
    "not_applicable",
    "conflicting",
}
SLOT_ACCESS = {"not_audited", "checked_blank", "checked_content", "not_checked_access_unavailable"}
CATEGORIES = {
    "official",
    "memory_based",
    "coaching_reconstruction",
    "unverified",
    "model_generated",
}


class Invalid(ValueError):
    """A safe error identifying a field, never echoing untrusted input."""


def require(condition, field):
    if not condition:
        raise Invalid(f"invalid {field}")


def shape(value, keys, field):
    require(type(value) is dict and set(value) == set(keys.split()), field)


def choice(value, values, field):
    require(type(value) is str and value in values, field)


def text(value, field):
    require(type(value) is str and 0 < len(value) <= 700, field)
    require(not any(ord(c) < 32 or c in "<>|`\\@" for c in value), field)
    require(not re.search(r"(?:^|\s)/(?!/)", value), field)
    require(
        not re.search(r"https?://\S*[?#%]", value)
        or re.fullmatch(r"https://(?:www\.)?rbi\.org\.in/[^\s?]+\?Id=\d+", value),
        field,
    )
    require(
        not re.search(
            r"(?i)(/home/|/tmp/|/Users/|file:|\b[a-z]:[\\/]|"
            r"(?:token|password|secret|cookie|api_key)\s*[:=]|"
            r"(?:ghp_|github_pat_|sk-)[\w-]{12,}|AKIA[A-Z0-9]{16}|PRIVATE KEY)",
            unquote(value),
        ),
        field,
    )


def url(value, field):
    text(value, field)
    try:
        p = urlsplit(value)
    except ValueError as exc:
        raise Invalid(f"invalid {field}") from exc
    require(p.scheme == "https" and p.hostname and p.netloc == p.hostname, field)
    require("." in p.hostname and not p.hostname.endswith((".local", ".localhost")), field)
    try:
        ipaddress.ip_address(p.hostname)
    except ValueError:
        pass
    else:
        raise Invalid(f"invalid {field}")
    # Only the exact legacy RBI public document query is supported. No signed URLs.
    require(
        not p.query
        or (p.hostname in {"rbi.org.in", "www.rbi.org.in"} and re.fullmatch(r"Id=\d+", p.query)),
        field,
    )
    require(not p.fragment and not re.search(r"%|\s|\\", value), field)


def identifier(value, prefix, field, examples=False):
    require(type(value) is str, field)
    if examples and re.fullmatch(r"EXAMPLE-" + prefix + r"-[a-z0-9-]+", value):
        return
    require(value.startswith(prefix + "-"), field)
    try:
        require(str(UUID(value[len(prefix) + 1 :])) == value[len(prefix) + 1 :], field)
    except ValueError as exc:
        raise Invalid(f"invalid {field}") from exc


def timestamp(value, field):
    require(type(value) is str and value.endswith("Z"), field)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise Invalid(f"invalid {field}") from exc
    require(parsed.isoformat(timespec="seconds").replace("+00:00", "Z") == value, field)


def publication(value):
    if value is not None:
        require(type(value) is str, "published_on")
        try:
            require(date.fromisoformat(value).isoformat() == value, "published_on")
        except ValueError as exc:
            raise Invalid("invalid published_on") from exc


def missing(record, fields, reasons_key="missing_reasons"):
    reasons = record[reasons_key]
    require(type(reasons) is dict, reasons_key)
    require(set(reasons) == {f for f in fields if record[f] is None}, reasons_key)
    for reason in reasons.values():
        choice(reason, REASONS, reasons_key)


def sequence(value, field):
    require(type(value) is list, field)
    return value


def unique(records, key, field):
    require(len({r[key] for r in records}) == len(records), field)


def claim(record):
    shape(record, "year phase paper session missing_reasons evidence_refs", "claim fields")
    missing(record, ("year", "phase", "paper", "session"))
    if record["year"] is not None:
        require(type(record["year"]) is int and 1900 <= record["year"] <= 2100, "claim year")
    if record["phase"] is not None:
        choice(record["phase"], PAPERS, "claim phase")
    if record["paper"] is not None:
        require(record["phase"] is not None, "paper requires phase")
        choice(record["paper"], (*PAPERS[record["phase"]], "combined"), "claim paper")
    if record["session"] is not None:
        choice(record["session"], {"shift_1", "shift_2"}, "claim session")


def validate(registry, *, allow_examples=False):
    """Validate all records atomically, without following any URLs or receipt paths.

    This version cannot approve/acquire historical papers. Advanced states fail
    closed; private receipts are separate records and never public registry input.
    """
    shape(registry, "schema_version as_of candidates slots ledger", "registry fields")
    require(registry["schema_version"] == VERSION, "schema_version")
    timestamp(registry["as_of"], "as_of")
    events = sequence(registry["ledger"], "ledger")
    for e in events:
        shape(
            e,
            "event_id subject_id subject_revision source_url assessed_at assessor summary source_category claims published_on rights access_state",
            "ledger fields",
        )
        identifier(e["event_id"], "ev", "event_id", allow_examples)
        url(e["source_url"], "ledger source_url")
        timestamp(e["assessed_at"], "assessed_at")
        require(e["assessed_at"] <= registry["as_of"], "assessment chronology")
        choice(e["assessor"], {"agent_metadata_review", "human_metadata_review"}, "assessor")
        text(e["summary"], "summary")
        text(e["subject_id"], "subject_id")
        require(
            type(e["subject_revision"]) is int and e["subject_revision"] > 0, "subject_revision"
        )
        publication(e["published_on"])
        require(
            e["published_on"] is None or e["published_on"] <= e["assessed_at"][:10],
            "publication chronology",
        )
        choice(
            e["access_state"],
            SLOT_ACCESS | {"access_not_checked", "landing_read", "access_blocked"},
            "ledger access_state",
        )
        require(
            type(e["rights"]) is dict and set(e["rights"]) <= set(RIGHTS), "ledger rights scopes"
        )
        for value in e["rights"].values():
            choice(value, {"permitted", "restricted", "prohibited"}, "ledger rights status")
        require(
            not e["rights"] or e["assessor"] == "human_metadata_review",
            "rights require human evidence",
        )
        if e["source_category"] is not None:
            choice(e["source_category"], CATEGORIES, "ledger source_category")
        for c in sequence(e["claims"], "ledger claims"):
            claim(c)
            require(c["evidence_refs"] == [], "ledger claim evidence_refs")
    unique(events, "event_id", "duplicate event IDs")
    by_event = {e["event_id"]: e for e in events}

    def evidence(record, subject, source=None, revision=1):
        refs = sequence(record["evidence_refs"], "evidence_refs")
        require(all(type(ref) is str for ref in refs), "evidence_refs")
        require(bool(refs) and len(set(refs)) == len(refs), "evidence_refs")
        for ref in refs:
            require(type(ref) is str and ref in by_event, "unresolved evidence")
            event = by_event[ref]
            require(
                event["subject_id"] == subject
                and event["subject_revision"] == revision
                and (source is None or event["source_url"] == source),
                "evidence subject/source",
            )
        return [by_event[r] for r in refs]

    candidates = sequence(registry["candidates"], "candidates")
    for c in candidates:
        shape(
            c,
            "candidate_id revision example_only title provider landing_url content_kind source_category authentication_status readability_status completeness_status answer_status review_status access_state discoverability published_on answer_key content_hash paper_identity missing_reasons rights claims evidence_refs unresolved",
            "candidate fields",
        )
        identifier(c["candidate_id"], "cand", "candidate_id", allow_examples)
        require(type(c["revision"]) is int and c["revision"] > 0, "revision")
        require(type(c["example_only"]) is bool, "example_only")
        require(allow_examples or not c["example_only"], "example_only public record")
        require(
            c["example_only"] == c["candidate_id"].startswith("EXAMPLE-"), "example ID fidelity"
        )
        text(c["title"], "title")
        if c["provider"] is not None:
            text(c["provider"], "provider")
        url(c["landing_url"], "landing_url")
        choice(
            c["content_kind"],
            {"landing_page", "sample_archive", "practice_collection"},
            "content_kind",
        )
        choice(c["source_category"], CATEGORIES, "source_category")
        choice(
            c["authentication_status"],
            {"unreviewed", "disputed", "rejected"},
            "authentication_status",
        )
        choice(c["readability_status"], {"unreviewed", "not_accessible"}, "readability_status")
        require(c["completeness_status"] == "unknown", "completeness_status")
        require(c["answer_status"] == "unknown", "answer_status")
        choice(c["review_status"], {"pending", "rejected"}, "review_status")
        choice(
            c["access_state"],
            {"access_not_checked", "landing_read", "access_blocked"},
            "access_state",
        )
        choice(
            c["discoverability"],
            {"lead_only", "links_advertised", "login_required"},
            "discoverability",
        )
        missing(c, ("provider", "published_on", "answer_key", "content_hash", "paper_identity"))
        require(
            all(c[f] is None for f in ("answer_key", "content_hash", "paper_identity")),
            "public unacquired fields",
        )
        publication(c["published_on"])
        observed = evidence(c, c["candidate_id"], c["landing_url"], c["revision"])
        require(
            any(e["source_category"] == c["source_category"] for e in observed),
            "source category fidelity",
        )
        require(
            any(e["published_on"] == c["published_on"] for e in observed), "publication evidence"
        )
        require(any(e["access_state"] == c["access_state"] for e in observed), "access evidence")
        shape(c["rights"], " ".join(RIGHTS), "rights scopes")
        for scope, assertion in c["rights"].items():
            shape(assertion, "status missing_reason evidence_refs", "rights fields")
            choice(
                assertion["status"],
                {"unknown", "permitted", "restricted", "prohibited"},
                "rights status",
            )
            if assertion["status"] == "unknown":
                choice(assertion["missing_reason"], REASONS, "rights missing_reason")
            else:
                require(assertion["missing_reason"] is None, "known rights missing_reason")
                supporting = evidence(assertion, c["candidate_id"], revision=c["revision"])
                require(
                    any(e["rights"].get(scope) == assertion["status"] for e in supporting),
                    "rights evidence/scope mismatch",
                )
            sequence(assertion["evidence_refs"], "rights evidence_refs")
            for ref in assertion["evidence_refs"]:
                require(type(ref) is str and ref in by_event, "rights evidence_refs")
        for item in sequence(c["claims"], "claims"):
            claim(item)
            supporting = evidence(item, c["candidate_id"], c["landing_url"], c["revision"])
            bare = {**item, "evidence_refs": []}
            require(any(bare in e["claims"] for e in supporting), "claim/evidence mismatch")
            require(c["access_state"] == "landing_read", "unread landing claims")
        unresolved = sequence(c["unresolved"], "unresolved")
        require(bool(unresolved), "unresolved gaps")
        for item in unresolved:
            text(item, "unresolved")
    unique(candidates, "candidate_id", "duplicate candidate IDs")

    slots = sequence(registry["slots"], "slots")
    for s in slots:
        shape(
            s,
            "slot_id revision year phase notion_url access_state exam_occurrence missing_reasons evidence_refs",
            "slot fields",
        )
        identifier(s["slot_id"], "slot", "slot_id", allow_examples)
        require(type(s["revision"]) is int and s["revision"] > 0, "slot revision")
        require(type(s["year"]) is int and 2018 <= s["year"] <= 2025, "slot year")
        choice(s["phase"], PAPERS, "slot phase")
        url(s["notion_url"], "notion_url")
        require(
            re.fullmatch(r"https://app.notion.com/p/[0-9a-f]{32}", s["notion_url"]),
            "Notion slot URL",
        )
        choice(s["access_state"], SLOT_ACCESS, "slot access_state")
        require(s["exam_occurrence"] is None, "slot label is not exam occurrence evidence")
        missing(s, ("exam_occurrence",))
        for e in evidence(s, s["slot_id"], s["notion_url"], s["revision"]):
            require(e["access_state"] == s["access_state"], "slot access evidence")
            require(e["source_category"] is None and len(e["claims"]) == 1, "slot evidence")
            claim_evidence = e["claims"][0]
            require(
                claim_evidence["year"] == s["year"] and claim_evidence["phase"] == s["phase"],
                "slot/evidence mismatch",
            )
    unique(slots, "slot_id", "duplicate slot IDs")
    unique(slots, "notion_url", "duplicate Notion slot URLs")
    require(
        len({(s["year"], s["phase"]) for s in slots}) == len(slots), "duplicate year/phase slot"
    )
    subjects = {r["candidate_id"] for r in candidates} | {r["slot_id"] for r in slots}
    require(all(e["subject_id"] in subjects for e in events), "orphan ledger event")
    return registry


def _object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def load_json(path):
    """Read just the explicitly supplied JSON, never paths embedded in records."""
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=_object)
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        raise Invalid("cannot read valid JSON metadata") from exc


def dumps(value):
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
