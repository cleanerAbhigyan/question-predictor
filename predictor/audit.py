"""Deterministic coverage and exception reporting from public metadata only."""

from .records import PAPERS, VERSION, dumps, validate


def audit(registry, *, allow_examples=False):
    validate(registry, allow_examples=allow_examples)
    candidates = sorted(registry["candidates"], key=lambda c: c["candidate_id"])
    slots = {(s["year"], s["phase"]): s for s in registry["slots"]}
    cells = []
    for year in range(2018, 2026):
        for phase, papers in PAPERS.items():
            slot = slots.get((year, phase))
            for paper in papers:
                leads = [
                    c["candidate_id"]
                    for c in candidates
                    if c["source_category"] != "model_generated"
                    and c["content_kind"] != "sample_archive"
                    if any(
                        cl["year"] == year
                        and cl["phase"] == phase
                        and cl["paper"] in {paper, "combined"}
                        for cl in c["claims"]
                    )
                ]
                access = slot["access_state"] if slot else "not_audited"
                # Notion state and external leads stay independent, never upgrade a paper.
                status = (
                    "lead_found"
                    if leads
                    else {
                        "checked_blank": "missing",
                        "not_checked_access_unavailable": "not_accessible",
                    }.get(access, "not_audited")
                )
                cells.append(
                    {
                        "year": year,
                        "phase": phase,
                        "paper": paper,
                        "status": status,
                        "notion_access": access,
                        "notion_url": slot["notion_url"] if slot else None,
                        "candidate_ids": leads,
                        "exam_occurrence": "unverified",
                    }
                )
    return {
        "schema_version": VERSION,
        "as_of": registry["as_of"],
        "candidate_count": len(candidates),
        "notion_slots_recorded": len(slots),
        # No corpus admission or approval exists in the Phase 1A metadata model.
        "acquired_papers": 0,
        "approved_papers": 0,
        "cells": cells,
        "candidates": candidates,
        "exceptions": [
            {"candidate_id": c["candidate_id"], "unresolved": sorted(c["unresolved"])}
            for c in candidates
        ],
    }


def markdown(report):
    lines = [
        "# Source availability audit",
        "",
        f"Generated offline from registry version {report['schema_version']}; as of {report['as_of']}.",
        "",
        f"Candidates: {report['candidate_count']}. Notion slots recorded: {report['notion_slots_recorded']}.",
        "Acquired papers in this public registry: 0. Approved historical papers: 0.",
        "",
        "A lead is an attributed landing-page claim, not a downloaded, readable or complete paper.",
        "Combined-paper leads are shown against each component as discovery leads only; component availability is unverified.",
        "Missing means no source in a checked blank Notion page, not proof that no paper exists elsewhere.",
        "Partial/reviewed paper states are unavailable until a later evidence-bearing corpus schema exists.",
        "All exam occurrences, including 2020, remain unverified here. Private receipts do not promote a candidate.",
        "",
        "| Year | Phase | Paper/section | Availability | Notion access | Candidate IDs |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for c in report["cells"]:
        access = (
            f"[{c['notion_access']}]({c['notion_url']})" if c["notion_url"] else c["notion_access"]
        )
        lines.append(
            f"| {c['year']} | {c['phase']} | {c['paper']} | {c['status']} | {access} | "
            f"{', '.join(c['candidate_ids']) or 'none'} |"
        )
    lines += ["", "## Candidate evidence and gaps", ""]
    for c in report["candidates"]:
        lines += [
            f"### {c['title']}",
            "",
            f"ID: {c['candidate_id']} (revision {c['revision']}).",
            f"Landing page: [{c['provider'] or 'unknown provider'}]({c['landing_url']}).",
            f"Category: {c['source_category']}; type: {c['content_kind']}; access: {c['access_state']}; discoverability: {c['discoverability']}.",
            f"Authentication: {c['authentication_status']}; source readability: {c['readability_status']}; completeness: {c['completeness_status']}; answers: {c['answer_status']}; review: {c['review_status']}.",
            f"Evidence: {', '.join(c['evidence_refs'])}. Publication date: {c['published_on'] or 'unknown'}.",
            "Rights: "
            + ", ".join(f"{scope}={r['status']}" for scope, r in sorted(c["rights"].items()))
            + ".",
            "",
            *[f"- {gap}" for gap in sorted(c["unresolved"])],
            "",
        ]
    return "\n".join(lines)


def render(registry, format_name):
    report = audit(registry)
    return dumps(report) if format_name == "json" else markdown(report)
