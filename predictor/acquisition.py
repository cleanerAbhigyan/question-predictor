"""Explicit local hashing only; receipts contain no path or question content."""

import hashlib
import os
import stat
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from .records import (
    VERSION,
    Invalid,
    dumps,
    identifier,
    require,
    sequence,
    shape,
    text,
    timestamp,
    validate,
)


def validate_receipts(ledger, *, allow_examples=False):
    shape(ledger, "schema_version acquisitions", "private ledger")
    require(ledger["schema_version"] == VERSION, "private schema_version")
    receipts = sequence(ledger["acquisitions"], "acquisitions")
    for r in receipts:
        shape(
            r,
            "acquisition_id source_id candidate_id candidate_revision sha256 byte_size media_type registered_at assessor permission_reference rights_cleared",
            "receipt fields",
        )
        for field, prefix in (
            ("acquisition_id", "acq"),
            ("source_id", "src"),
            ("candidate_id", "cand"),
        ):
            identifier(r[field], prefix, field, allow_examples)
        require(
            type(r["candidate_revision"]) is int and r["candidate_revision"] > 0,
            "candidate_revision",
        )
        require(
            type(r["sha256"]) is str
            and len(r["sha256"]) == 64
            and all(c in "0123456789abcdef" for c in r["sha256"]),
            "sha256",
        )
        require(type(r["byte_size"]) is int and r["byte_size"] > 5, "byte_size")
        require(r["media_type"] == "application/pdf", "media_type")
        timestamp(r["registered_at"], "registered_at")
        text(r["assessor"], "assessor")
        text(r["permission_reference"], "permission_reference")
        require(r["rights_cleared"] == ["acquisition", "personal_analysis"], "rights_cleared")
    for key in ("acquisition_id", "source_id"):
        require(len({r[key] for r in receipts}) == len(receipts), f"duplicate {key}")
    return ledger


def register(
    registry,
    candidate_id,
    path,
    *,
    registered_at,
    permission_reference,
    assessor,
    rights_cleared,
    allow_examples=False,
):
    validate(registry, allow_examples=allow_examples)
    candidates = [c for c in registry["candidates"] if c["candidate_id"] == candidate_id]
    require(len(candidates) == 1, "candidate reference")
    require(rights_cleared is True, "explicit acquisition and personal-analysis permission")
    require(
        all(
            candidates[0]["rights"][scope]["status"] not in {"restricted", "prohibited"}
            for scope in ("acquisition", "personal_analysis")
        ),
        "existing rights restriction",
    )
    timestamp(registered_at, "registered_at")
    require(registered_at >= registry["as_of"], "receipt chronology")
    text(permission_reference, "permission_reference")
    text(assessor, "assessor")
    require(Path(path).suffix.lower() == ".pdf", "supported local format (PDF only)")
    # O_NONBLOCK prevents a FIFO from hanging before the regular-file check.
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(fd, "rb") as handle:
            before = os.fstat(handle.fileno())
            require(stat.S_ISREG(before.st_mode), "regular local file")
            header = handle.read(5)
            require(header == b"%PDF-", "PDF signature")
            digest = hashlib.sha256(header)
            size = len(header)
            while block := handle.read(1024 * 1024):
                digest.update(block)
                size += len(block)
            after = os.fstat(handle.fileno())
            require(
                (before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns),
                "file changed during hashing",
            )
    except OSError as exc:
        raise Invalid("cannot read regular local PDF") from exc
    checksum = digest.hexdigest()
    example_prefix = "EXAMPLE-" if allow_examples else ""
    receipt = {
        "acquisition_id": example_prefix
        + "acq-"
        + str(uuid5(NAMESPACE_URL, candidate_id + checksum + registered_at)),
        "source_id": example_prefix + "src-" + str(uuid5(NAMESPACE_URL, checksum)),
        "candidate_id": candidate_id,
        "candidate_revision": candidates[0]["revision"],
        "sha256": checksum,
        "byte_size": size,
        "media_type": "application/pdf",
        "registered_at": registered_at,
        "assessor": assessor,
        "permission_reference": permission_reference,
        "rights_cleared": ["acquisition", "personal_analysis"],
    }
    return validate_receipts(
        {"schema_version": VERSION, "acquisitions": [receipt]}, allow_examples=allow_examples
    )


def save_private(ledger, destination, *, root=None, allow_examples=False):
    """Publish one immutable private receipt with no overwrite, even on failure."""
    import tempfile

    validate_receipts(ledger, allow_examples=allow_examples)
    root = (Path.cwd() if root is None else Path(root)).resolve()
    directory = root / "data" / "private"
    target = Path(destination).absolute()
    require(target.parent == directory, "receipt destination must be data/private/<name>.json")
    require(target.suffix == ".json" and not target.exists(), "new JSON receipt destination")
    require(directory.resolve() == directory, "private directory must not be a symlink")
    directory.mkdir(parents=True, exist_ok=True)
    temp = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=directory, delete=False
        ) as f:
            temp = Path(f.name)
            os.chmod(temp, 0o600)
            f.write(dumps(ledger))
            f.flush()
            os.fsync(f.fileno())
        os.link(temp, target)  # Atomic create; refuses existing paths and dangling symlinks.
    except OSError as exc:
        raise Invalid("cannot save new private receipt") from exc
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)
