"""Deliver the finished front page for the 19 November 2026 news-image entry.

The artwork itself already lives beside this file as ``entry.png``.  This
program does the one job the competition asks for: it places an exact copy
of that artwork at the output path the grader reads, and then proves the
copy is exact before it reports success.

It needs nothing from the network and nothing beyond the standard library,
so a run is the same on any machine: read the bundled picture, write it
out, and check the result byte for byte.
"""

import hashlib
import os
import sys
from pathlib import Path

# The picture bundled with this repository: a 1024x1024 front page,
# 125,502 bytes.  Its fingerprint is pinned here so a damaged or swapped
# source file can never slip through silently.
BUNDLED_NAME = "entry.png"
BUNDLED_BYTES = 125502
BUNDLED_SHA256 = "8d7b6e4bec14eefbe652412417b34abb42a2af1865c0cd30d7a0750999a62c8d"

# Where the grader expects the finished image.  The harness may point
# elsewhere through the environment; otherwise the fixed path applies.
# Either way the bytes written are the same bundled bytes, so the two
# grading runs cannot disagree with each other.
DEFAULT_OUTPUT_DIR = Path("/output")
OUTPUT_ENV_VAR = "MAKEFUN_OUTPUT_DIR"


def bundled_picture() -> Path:
    """Return the path of the picture shipped in this repository."""
    here = Path(__file__).resolve().parent
    return here / BUNDLED_NAME


def output_picture() -> Path:
    """Return where the finished image must land."""
    chosen = os.environ.get(OUTPUT_ENV_VAR)
    folder = Path(chosen) if chosen else DEFAULT_OUTPUT_DIR
    return folder / BUNDLED_NAME


def fingerprint(path: Path) -> str:
    """Hash a file's contents with SHA-256 and return the hex digest."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def deliver() -> Path:
    """Copy the bundled picture to the output path and verify the copy."""
    source = bundled_picture()
    if not source.is_file():
        raise FileNotFoundError(f"bundled picture missing: {source}")

    raw = source.read_bytes()
    if len(raw) != BUNDLED_BYTES:
        raise ValueError(
            f"bundled picture is {len(raw)} bytes, expected {BUNDLED_BYTES}"
        )
    if hashlib.sha256(raw).hexdigest() != BUNDLED_SHA256:
        raise ValueError("bundled picture failed its SHA-256 check")

    target = output_picture()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)

    written = target.read_bytes()
    if len(written) != BUNDLED_BYTES or fingerprint(target) != BUNDLED_SHA256:
        raise ValueError("written picture does not match the bundled original")

    return target


def main() -> int:
    """Place the entry image and confirm the delivery."""
    try:
        target = deliver()
    except (OSError, ValueError) as problem:
        print(f"entry delivery failed: {problem}", file=sys.stderr)
        return 1
    print(f"entry.png delivered to {target} ({BUNDLED_BYTES} bytes, sha256 verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
