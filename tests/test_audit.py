import copy
import hashlib
import io
import json
import os
import socket
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from predictor.__main__ import main
from predictor.acquisition import register, save_private, validate_receipts
from predictor.audit import audit, markdown
from predictor.records import Invalid, dumps, load_json, validate
from tests.fixtures import AT, CID, EID, NOTION, SID, claim, registry

ROOT = Path(__file__).resolve().parents[1]


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.r = registry()
        self.c = self.r["candidates"][0]

    def valid(self):
        return validate(self.r, allow_examples=True)

    def test_unknown_rights_remain_candidate_and_example_cannot_be_public(self):
        self.valid()
        self.assertEqual(self.c["review_status"], "pending")
        with self.assertRaises(Invalid):
            validate(self.r)
        for field, value in [
            ("review_status", "approved"),
            ("authentication_status", "supported"),
            ("readability_status", "readable"),
            ("completeness_status", "complete"),
            ("answer_status", "approved"),
            ("access_state", "acquired"),
        ]:
            with self.subTest(field=field), self.assertRaises(Invalid):
                r = registry()
                r["candidates"][0][field] = value
                validate(r, allow_examples=True)

    def test_missing_vs_null_and_bad_scalars(self):
        for field in self.c:
            with self.subTest(missing=field), self.assertRaises(Invalid):
                r = registry()
                del r["candidates"][0][field]
                validate(r, allow_examples=True)
        for field in ("published_on", "answer_key", "content_hash", "paper_identity"):
            with self.subTest(reason=field), self.assertRaises(Invalid):
                r = registry()
                del r["candidates"][0]["missing_reasons"][field]
                validate(r, allow_examples=True)
        for field, value in [
            ("year", True),
            ("year", 2020.5),
            ("year", "2020"),
            ("year", 1800),
            ("phase", "III"),
            ("phase", []),
            ("paper", "ESI"),
            ("session", "morning"),
        ]:
            with self.subTest(field=field, value=value), self.assertRaises(Invalid):
                r = registry()
                r["candidates"][0]["claims"][0][field] = value
                validate(r, allow_examples=True)
        for field, value in [
            ("revision", True),
            ("published_on", "2026-02-30"),
            ("content_hash", "0" * 64),
            ("provider", None),
            ("example_only", False),
        ]:
            with self.subTest(field=field), self.assertRaises(Invalid):
                r = registry()
                r["candidates"][0][field] = value
                validate(r, allow_examples=True)

    def test_unknown_year_phase_paper_have_explicit_reasons(self):
        for c in (self.c["claims"][0], self.r["ledger"][0]["claims"][0]):
            for field in ("year", "phase", "paper"):
                c[field] = None
                c["missing_reasons"][field] = "unverified"
        self.valid()

    def test_publication_date_needs_matching_evidence(self):
        self.c["published_on"] = "2026-01-01"
        del self.c["missing_reasons"]["published_on"]
        with self.assertRaises(Invalid):
            self.valid()
        self.r["ledger"][0]["published_on"] = "2026-01-01"
        self.valid()
        self.r["ledger"][0]["published_on"] = "2026-02-01"
        with self.assertRaises(Invalid):
            self.valid()

    def test_duplicate_ids_and_mismatched_evidence(self):
        self.r["candidates"].append(copy.deepcopy(self.c))
        with self.assertRaises(Invalid):
            self.valid()
        self.r = registry()
        self.r["ledger"].append(copy.deepcopy(self.r["ledger"][0]))
        with self.assertRaises(Invalid):
            self.valid()
        for mutate in ("category", "claim", "subject", "refs", "access"):
            r = registry()
            if mutate == "category":
                r["candidates"][0]["source_category"] = "official"
            elif mutate == "claim":
                r["candidates"][0]["claims"][0]["year"] = 2021
            elif mutate == "subject":
                r["ledger"][0]["subject_id"] = "EXAMPLE-cand-other"
            elif mutate == "access":
                r["candidates"][0]["access_state"] = "access_blocked"
            else:
                r["candidates"][0]["evidence_refs"] = [[]]
            with self.subTest(mutate=mutate), self.assertRaises(Invalid):
                validate(r, allow_examples=True)

    def test_rights_scopes_and_human_assertions(self):
        self.c["rights"]["export"] = self.c["rights"]["acquisition"]
        with self.assertRaises(Invalid):
            self.valid()
        self.r = registry()
        self.c = self.r["candidates"][0]
        right = self.c["rights"]["acquisition"]
        right.update(status="permitted", missing_reason=None, evidence_refs=[EID])
        with self.assertRaises(Invalid):
            self.valid()
        event = self.r["ledger"][0]
        event["rights"] = {"acquisition": "permitted"}
        with self.assertRaises(Invalid):
            self.valid()
        event["assessor"] = "human_metadata_review"
        self.valid()
        self.assertEqual(self.c["rights"]["model_ingestion"]["status"], "unknown")
        event["rights"] = {"personal_analysis": "permitted"}
        with self.assertRaises(Invalid):
            self.valid()

    def test_private_data_and_unsafe_urls_fail_before_serialization(self):
        for key in (
            "question_text",
            "questions",
            "answer",
            "cookie",
            "file_path",
            "acquired",
            "receipts",
        ):
            r = registry()
            r["candidates"][0][key] = "not public"
            with self.subTest(key=key), self.assertRaises(Invalid):
                validate(r, allow_examples=True)
        for value in (
            "https://example.org/?token=private",
            "https://user:password@example.org/",
            "file:///tmp/file",
            "https://127.0.0.1/",
            "https://example.local/",
            "https://example.org/%3Ftoken%3Dprivate",
            "https://example.org/#private",
        ):
            r = registry()
            r["candidates"][0]["landing_url"] = value
            with self.subTest(value=value), self.assertRaises(Invalid):
                validate(r, allow_examples=True)
        for value in ("/home/private/file.pdf", "C:\\private\\file.pdf", "token=do-not-print"):
            r = registry()
            r["candidates"][0]["title"] = value
            with self.assertRaises(Invalid):
                validate(r, allow_examples=True)

    def test_malformed_leaf_types_fail_as_validation_errors(self):
        def leaves(value, path=()):
            if isinstance(value, dict):
                for key, child in value.items():
                    yield from leaves(child, (*path, key))
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    yield from leaves(child, (*path, index))
            else:
                yield path

        for path in leaves(registry()):
            r = registry()
            target = r
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = []
            with self.subTest(path=path), self.assertRaises(Invalid):
                validate(r, allow_examples=True)

    def test_failure_does_not_mutate_registry(self):
        self.c["claims"][0]["phase"] = "invalid"
        before = dumps(self.r)
        with self.assertRaises(Invalid):
            self.valid()
        self.assertEqual(dumps(self.r), before)

    def test_json_duplicate_keys_malformed_and_non_utf8(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "input.json"
            for content in (b'{"a":1,"a":2}', b"{", b"\xff"):
                p.write_bytes(content)
                with self.assertRaises(Invalid):
                    load_json(p)
        with self.assertRaises(Invalid):
            load_json("/nonexistent/metadata.json")


class ReportTests(unittest.TestCase):
    def test_generated_and_sample_references_do_not_imply_historical_availability(self):
        for category, kind in [
            ("model_generated", "practice_collection"),
            ("official", "sample_archive"),
        ]:
            r = registry()
            r["candidates"][0]["source_category"] = category
            r["candidates"][0]["content_kind"] = kind
            r["ledger"][0]["source_category"] = category
            result = audit(r, allow_examples=True)
            self.assertTrue(all(c["status"] == "not_audited" for c in result["cells"]))

    def test_zero_and_partial_coverage_are_complete_and_deterministic(self):
        r = dict(schema_version="1.0.0", as_of=AT, candidates=[], slots=[], ledger=[])
        result = audit(r)
        self.assertEqual(len(result["cells"]), 56)
        self.assertTrue(all(c["status"] == "not_audited" for c in result["cells"]))
        self.assertEqual(result["approved_papers"], 0)
        r = registry()
        result = audit(r, allow_examples=True)
        year2020 = [c for c in result["cells"] if c["year"] == 2020]
        self.assertEqual(sum(c["status"] == "lead_found" for c in year2020), 4)
        self.assertTrue(all(c["exam_occurrence"] == "unverified" for c in year2020))
        self.assertEqual(result, audit(r, allow_examples=True))
        self.assertEqual(len(result["exceptions"]), 1)
        self.assertNotIn("PRIVATE", markdown(result))

    def test_slot_blank_access_unavailable_and_mismatch(self):
        for access, expected in [
            ("checked_blank", "missing"),
            ("not_checked_access_unavailable", "not_accessible"),
            ("not_audited", "not_audited"),
        ]:
            r = registry()
            r["candidates"][0]["claims"] = []
            slot = dict(
                slot_id=SID,
                revision=1,
                year=2020,
                phase="II",
                notion_url=NOTION,
                access_state=access,
                exam_occurrence=None,
                missing_reasons={"exam_occurrence": "unverified"},
                evidence_refs=["EXAMPLE-ev-slot"],
            )
            r["slots"] = [slot]
            r["ledger"].append(
                dict(
                    event_id="EXAMPLE-ev-slot",
                    subject_id=SID,
                    subject_revision=1,
                    source_url=NOTION,
                    assessed_at=AT,
                    assessor="agent_metadata_review",
                    summary="Artificial slot audit.",
                    source_category=None,
                    claims=[
                        dict(
                            claim(),
                            phase="II",
                            paper=None,
                            missing_reasons={"paper": "not_provided", "session": "not_provided"},
                            evidence_refs=[],
                        )
                    ],
                    published_on=None,
                    rights={},
                    access_state=access,
                )
            )
            report = audit(r, allow_examples=True)
            self.assertTrue(
                all(
                    c["status"] == expected
                    for c in report["cells"]
                    if c["year"] == 2020 and c["phase"] == "II"
                )
            )
            slot["year"] = 2021
            with self.assertRaises(Invalid):
                audit(r, allow_examples=True)

    def test_audit_validate_import_have_no_file_or_network_reads(self):
        r = registry()
        with (
            patch("builtins.open", side_effect=AssertionError("file read")),
            patch.object(Path, "open", side_effect=AssertionError("file read")),
            patch.object(socket, "socket", side_effect=AssertionError("network")),
        ):
            validate(r, allow_examples=True)
            audit(r, allow_examples=True)
        code = "import builtins,socket; builtins.open=lambda *a,**k: (_ for _ in ()).throw(AssertionError('read')); socket.socket=builtins.open; import predictor; import predictor.__main__"
        subprocess.run([sys.executable, "-c", code], check=True, cwd=ROOT)

    def test_real_registry_outputs_and_permutation_stability(self):
        r = load_json(ROOT / "registry/sources.json")
        report = audit(r)
        self.assertEqual((report["candidate_count"], report["notion_slots_recorded"]), (6, 16))
        self.assertEqual(report["approved_papers"], 0)
        self.assertEqual(markdown(report), (ROOT / "docs/SOURCE_AUDIT_REPORT.md").read_text())
        self.assertEqual(dumps(report), (ROOT / "registry/audit.json").read_text())
        for field in ("candidates", "slots", "ledger"):
            r[field].reverse()
        self.assertEqual(report, audit(r))


class AcquisitionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.file = self.root / "EXAMPLE-owned.pdf"
        self.content = b"%PDF-1.0\nEXAMPLE test-owned bytes only\n%%EOF\n"
        self.file.write_bytes(self.content)
        self.options = dict(
            registered_at=AT,
            permission_reference="EXAMPLE-local-permission",
            assessor="EXAMPLE-reviewer",
            rights_cleared=True,
            allow_examples=True,
        )

    def tearDown(self):
        self.temp.cleanup()

    def receipt(self):
        return register(registry(), CID, self.file, **self.options)

    def test_hash_size_private_only_no_content_and_no_promotion(self):
        ledger = self.receipt()
        receipt = ledger["acquisitions"][0]
        self.assertEqual(receipt["sha256"], hashlib.sha256(self.content).hexdigest())
        self.assertEqual(receipt["byte_size"], len(self.content))
        self.assertNotIn(str(self.root), dumps(ledger))
        self.assertNotIn("test-owned bytes", dumps(ledger))
        self.assertEqual(ledger, self.receipt())
        with self.assertRaises(Invalid):
            validate_receipts(ledger)
        with self.assertRaises(Invalid):
            validate(ledger)

    def test_files_and_permission_fail_safely(self):
        for name, content in [
            ("missing.pdf", None),
            ("bad.pdf", b"NOT PDF"),
            ("unsupported.txt", self.content),
            ("empty.pdf", b""),
        ]:
            p = self.root / name
            if content is not None:
                p.write_bytes(content)
            with self.subTest(name=name), self.assertRaises(Invalid):
                register(registry(), CID, p, **self.options)
        symlink = self.root / "symlink.pdf"
        symlink.symlink_to(self.file)
        with self.assertRaises(Invalid):
            register(registry(), CID, symlink, **self.options)
        with (
            self.assertRaises(Invalid),
            patch("os.open", side_effect=AssertionError("must not read")),
        ):
            register(registry(), CID, self.file, **dict(self.options, rights_cleared=False))

    def test_symlinked_private_directory_writes_nothing(self):
        outside = self.root / "outside"
        outside.mkdir()
        (self.root / "data").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(Invalid):
            save_private(
                self.receipt(),
                self.root / "data/private/receipt.json",
                root=self.root,
                allow_examples=True,
            )
        self.assertFalse((outside / "private").exists())

    def test_duplicate_ids_invalid_receipt_and_atomic_save(self):
        ledger = self.receipt()
        duplicated = copy.deepcopy(ledger)
        duplicated["acquisitions"] *= 2
        with self.assertRaises(Invalid):
            validate_receipts(duplicated, allow_examples=True)
        target = self.root / "data/private/receipt.json"
        save_private(ledger, target, root=self.root, allow_examples=True)
        before = target.read_bytes()
        self.assertEqual(os.stat(target).st_mode & 0o777, 0o600)
        with self.assertRaises(Invalid):
            save_private(ledger, target, root=self.root, allow_examples=True)
        self.assertEqual(target.read_bytes(), before)
        invalid = copy.deepcopy(ledger)
        invalid["acquisitions"][0]["sha256"] = "invented"
        other = target.with_name("other.json")
        with self.assertRaises(Invalid):
            save_private(invalid, other, root=self.root, allow_examples=True)
        self.assertFalse(other.exists())
        with self.assertRaises(Invalid):
            save_private(ledger, self.root / "public.json", root=self.root, allow_examples=True)


class CLITests(unittest.TestCase):
    def test_readonly_commands_read_only_explicit_registry(self):
        registry_path = ROOT / "registry/sources.json"
        original = Path.open

        def guarded(path, *args, **kwargs):
            self.assertEqual(path, registry_path)
            return original(path, *args, **kwargs)

        for command in ("validate", "audit"):
            with (
                patch.object(Path, "open", guarded),
                patch.object(socket, "socket", side_effect=AssertionError("network")),
                redirect_stdout(io.StringIO()),
            ):
                self.assertEqual(main([command, str(registry_path)]), 0)

    def test_bad_input_atomic_no_stdout_or_private_path_echo(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "private.json"
            r = registry()
            r["candidates"][0]["title"] = "token=DO-NOT-ECHO"
            p.write_text(json.dumps(r))
            before = p.read_bytes()
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                self.assertEqual(main(["audit", str(p)]), 2)
            self.assertEqual(out.getvalue(), "")
            self.assertNotIn(temp, err.getvalue())
            self.assertNotIn("DO-NOT-ECHO", err.getvalue())
            self.assertEqual(p.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
