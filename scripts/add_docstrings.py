#!/usr/bin/env python3
"""Add missing module-level docstrings (safe mode).

This script inserts a simple, Google-style module docstring at the top of Python files
that lack one. It intentionally does NOT modify classes or functions to avoid breaking
syntax or formatting. Suitable for CI use (with --check) and local autofix (default).

Exit codes:
    0  -> no issues (or issues fixed in write mode)
    1  -> missing docstrings detected in --check mode

Usage examples:
    # Dry-run: just report files missing a module docstring
    ./scripts/add_docstrings.py --check

    # Write changes in-place (default)
    ./scripts/add_docstrings.py

    # Limit to app/ only and exclude migrations/versions
    ./scripts/add_docstrings.py app --exclude "migrations/versions/*.py"
"""

from __future__ import annotations

import argparse
import ast
import fnmatch
import logging
import pathlib
import sys
from collections.abc import Iterable

LOGGER = logging.getLogger("add_docstrings")


def iter_python_files(
    roots: list[pathlib.Path],
    exclude_patterns: list[str],
) -> Iterable[pathlib.Path]:
    """Yield Python files under given roots, skipping excluded paths.

    Args:
        roots: Root paths (directories or files) to scan.
        exclude_patterns: Glob patterns to exclude from scanning.

    Returns:
        An iterator of Python file paths.
    """
    for root in roots:
        for path in root.rglob("*.py"):
            parts = set(path.parts)
            if "__pycache__" in parts:
                continue
            # quick excludes by directory
            if "migrations" in parts and "versions" in parts:
                continue
            # glob-style excludes
            if any(fnmatch.fnmatch(str(path), pat) for pat in exclude_patterns):
                continue
            yield path


def ensure_module_docstring(src: str, module_name: str) -> tuple[str, bool]:
    """Ensure a top-level docstring is present.

    Args:
        src: Original file content.
        module_name: Module name used in the generated docstring.

    Returns:
        A tuple of (updated_source, changed) where changed indicates whether a docstring was added.
    """
    try:
        tree = ast.parse(src)
    except SyntaxError:
        # Do not touch syntactically invalid files
        return src, False

    if ast.get_docstring(tree) is not None:
        return src, False

    header = f'"""Module {module_name}."""\n\n'
    return header + src, True


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        argv: Raw argument vector (usually ``sys.argv[1:]``).

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Add missing module-level docstrings (safe mode).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Root paths to scan (directories or files).",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Glob pattern(s) to exclude (can be passed multiple times).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Do not write changes; exit 1 if any file needs a module docstring.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce log verbosity.",
    )
    return parser.parse_args(argv)


def configure_logging(quiet: bool) -> None:
    """Configure basic logger output.

    Args:
        quiet: If True, use WARNING level; otherwise INFO.
    """
    level = logging.WARNING if quiet else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def main(argv: list[str]) -> int:
    """Entry point.

    Args:
        argv: Raw argument vector (usually ``sys.argv[1:]``).

    Returns:
        Process exit code (0 on success; 1 if --check finds issues).
    """
    args = parse_args(argv)
    configure_logging(args.quiet)

    roots = [pathlib.Path(p).resolve() for p in args.paths]
    exclude_patterns = list(args.exclude)

    missing: list[pathlib.Path] = []
    fixed: list[pathlib.Path] = []

    for path in iter_python_files(roots, exclude_patterns):
        text = path.read_text(encoding="utf-8")
        updated, changed = ensure_module_docstring(text, module_name=path.stem)

        if changed:
            if args.check:
                missing.append(path)
            else:
                path.write_text(updated, encoding="utf-8")
                fixed.append(path)

    if args.check:
        if missing:
            for p in missing:
                LOGGER.info("Missing module docstring: %s", p)
            LOGGER.info("Total files missing docstring: %d", len(missing))
            return 1
        LOGGER.info("All files have a module docstring.")
        return 0

    LOGGER.info("Added module docstrings to %d file(s).", len(fixed))
    for p in fixed:
        LOGGER.info("Updated: %s", p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
