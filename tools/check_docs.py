#!/usr/bin/env python3
"""Simple Markdown link validator for internal documentation."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

INLINE_LINK_RE = re.compile(r"!?\[[^\]]+\]\(([^)]+)\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]]+]:\s*(\S+)", re.MULTILINE)
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#", "data:", "javascript:")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate that local Markdown links point to existing files."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Markdown files or directories containing Markdown files to check.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print every processed link for debugging.",
    )
    return parser.parse_args()


def iter_markdown_files(paths: Sequence[str]) -> Iterable[Path]:
    for raw_path in paths:
        path = Path(raw_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"{raw_path} does not exist")
        if path.is_dir():
            yield from sorted(path.rglob("*.md"))
        elif path.suffix.lower() == ".md":
            yield path


def extract_targets(markdown: str) -> Iterable[str]:
    for match in INLINE_LINK_RE.finditer(markdown):
        yield match.group(1).strip()
    for match in REFERENCE_LINK_RE.finditer(markdown):
        yield match.group(1).strip()


def normalize_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if not target or target.startswith(SKIP_PREFIXES):
        return None
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    if target.startswith(SKIP_PREFIXES) or not target:
        return None

    # Drop optional title sections: path "Some Title"
    if " " in target and not target.startswith(("http://", "https://")):
        target = target.split()[0]

    # Remove anchors or query strings.
    target = target.split("#", 1)[0]
    target = target.split("?", 1)[0]
    if not target or target.startswith(SKIP_PREFIXES):
        return None
    if target.startswith("{#"):
        return None
    return target


def validate_links(paths: Sequence[str], verbose: bool = False) -> Tuple[int, List[str]]:
    files = list(iter_markdown_files(paths))
    missing: List[str] = []
    checked = 0

    for file_path in files:
        contents = file_path.read_text(encoding="utf-8")
        for target in extract_targets(contents):
            normalized = normalize_target(target)
            if not normalized:
                continue
            resolved = (file_path.parent / normalized).resolve()
            checked += 1
            if verbose:
                print(f"[check] {file_path.relative_to(Path.cwd())} -> {normalized}")
            if not resolved.exists():
                missing.append(
                    f"{file_path.relative_to(Path.cwd())}: missing target '{normalized}'"
                )
    return checked, missing


def main() -> int:
    args = parse_args()
    try:
        checked_count, missing_links = validate_links(args.paths, args.verbose)
    except FileNotFoundError as exc:
        print(f"[docs] {exc}", file=sys.stderr)
        return 2

    if missing_links:
        print("[docs] Broken documentation links detected:")
        for problem in missing_links:
            print(f"  - {problem}")
        print(f"[docs] Checked {checked_count} link(s).", file=sys.stderr)
        return 1

    print(f"[docs] All good — validated {checked_count} link(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
