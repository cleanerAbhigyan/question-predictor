"""Offline repository hygiene and archived-task checks, also run by CI."""

import hashlib
import re
import subprocess
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class RepositoryTests(unittest.TestCase):
    def test_local_markdown_links(self):
        paths = [ROOT / "README.md", ROOT / "AGENTS.md", *ROOT.joinpath("docs").rglob("*.md")]
        count = 0
        for path in paths:
            content = path.read_text()
            self.assertEqual(content.count("```") % 2, 0, path)
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
                parts = urlsplit(target)
                if parts.scheme or target.startswith("#"):
                    continue
                resolved = (path.parent / unquote(parts.path)).resolve()
                self.assertTrue(resolved.is_relative_to(ROOT), path)
                self.assertTrue(resolved.is_file(), f"{path}: {target}")
                self.assertFalse(parts.fragment, f"anchor needs separate review: {target}")
                count += 1
        self.assertGreater(count, 40)

    def test_prompt_archives_preserved(self):
        expected = {
            "2026-11-07-phase-0-repo-foundation.md": "4ba2b9991c0e8a947616a3ea328d249241666b0ac5d064a8f2c82bc0a185ff56",
            "2026-11-07-phase-1a-source-registry-audit.md": "2fb80f5ef5050d26d012817bd465591482f1945787ee48ef2e4f7b4bc90cfe7e",
        }
        for name, digest in expected.items():
            self.assertEqual(
                hashlib.sha256((ROOT / "docs/prompts" / name).read_bytes()).hexdigest(), digest
            )
        self.assertTrue(
            (ROOT / "docs/prompts/2026-11-07-phase-1a-source-registry-audit.md").is_file()
        )

    def test_private_paths_ignored_and_registry_visible(self):
        for path in (
            "data/raw/paper.pdf",
            "data/private/receipt.json",
            ".env",
            "local/private.json",
        ):
            self.assertEqual(
                subprocess.run(
                    ["git", "check-ignore", "--no-index", "-q", path], cwd=ROOT
                ).returncode,
                0,
                path,
            )
        for path in ("registry/sources.json", "registry/audit.json", "docs/SOURCE_AUDIT_REPORT.md"):
            self.assertEqual(
                subprocess.run(
                    ["git", "check-ignore", "--no-index", "-q", path], cwd=ROOT
                ).returncode,
                1,
                path,
            )

    def test_no_papers_or_secrets_in_publication_files(self):
        paths = (
            subprocess.check_output(
                ["git", "ls-files", "-c", "-o", "--exclude-standard", "-z"], cwd=ROOT
            )
            .decode()
            .split("\0")
        )
        patterns = [
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
            r"\bAKIA[0-9A-Z]{16}\b",
            r"\bgh[pousr]_[A-Za-z0-9]{20,}\b",
            r"\bgithub_pat_[A-Za-z0-9_]{20,}\b",
            r"\bsk-[A-Za-z0-9_-]{20,}\b",
        ]
        for path in set(paths) - {""}:
            self.assertNotIn(
                Path(path).suffix.lower(), {".pdf", ".zip", ".sqlite", ".sqlite3"}, path
            )
            content = (ROOT / path).read_text()
            for pattern in patterns:
                self.assertIsNone(re.search(pattern, content), f"possible credential in {path}")


if __name__ == "__main__":
    unittest.main()
