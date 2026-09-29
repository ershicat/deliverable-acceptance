#!/usr/bin/env python3
"""Validate SKILL.md against the format invariants that make a skill loadable.

Why this exists
---------------
A Markdown formatter once rewrote SKILL.md in this repository: it escaped the
frontmatter delimiters to ``\\---`` and padded every line with trailing spaces.
Every file-level check still passed, but the skill could no longer be loaded --
the platform merely logs a warning and ignores the file. This script catches
that class of damage, plus the rules that decide whether a skill loads at all.

It is intentionally dependency-light: PyYAML is used when available, otherwise
the structural checks still run and the YAML check is reported as SKIP.

Usage
-----
    python scripts/check_skill.py

Exit code 0 = every check passed, 1 = at least one check failed.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DESC_MAX = 1024

_failed = False


def report(ok: bool, label: str, detail: str = "") -> None:
    global _failed
    if not ok:
        _failed = True
    line = f"[{'PASS' if ok else 'FAIL'}] {label}"
    if detail:
        line += f"  --  {detail}"
    print(line)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    skill = root / "SKILL.md"
    dirname = root.name

    print(f"checking {skill}")
    print(f"skill directory name: {dirname}")
    print()

    if not skill.is_file():
        report(False, "SKILL.md exists", str(skill))
        print("\nFAILED - no SKILL.md to check.")
        return 1

    raw = skill.read_bytes()
    text = raw.decode("utf-8", errors="replace")

    has_bom = raw[:3] == b"\xef\xbb\xbf"
    report(
        not has_bom,
        "no UTF-8 BOM",
        "a BOM makes the first line fail the '---' test, so the skill is ignored" if has_bom else "",
    )
    has_crlf = b"\r\n" in raw
    report(not has_crlf, "LF line endings only", "CRLF found" if has_crlf else "")
    report(text.endswith("\n"), "file ends with a newline")

    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()

    trailing = [i + 1 for i, line in enumerate(lines) if line != line.rstrip()]
    report(
        not trailing,
        "no trailing whitespace",
        ("lines " + ", ".join(map(str, trailing[:10]))) if trailing else "",
    )

    escaped = [i + 1 for i, line in enumerate(lines) if line.lstrip().startswith("\\---")]
    report(
        not escaped,
        "no escaped frontmatter delimiter",
        ("line(s) " + ", ".join(map(str, escaped[:10])) + " start with \\---") if escaped else "",
    )

    report(bool(lines) and lines[0] == "---", "first line is exactly '---'")

    end = -1
    for i in range(1, len(lines)):
        if lines[i] == "---":
            end = i
            break
    report(end > 0, "frontmatter is closed with '---'")

    if end <= 0:
        print("\nFAILED - cannot read the frontmatter.")
        return 1

    fm_text = "\n".join(lines[1:end])

    data = None
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError:
        print("[SKIP] frontmatter parses as YAML  --  PyYAML not installed (pip install pyyaml)")
    else:
        try:
            data = yaml.safe_load(fm_text)
        except Exception as exc:  # noqa: BLE001 - surface any parser error verbatim
            report(False, "frontmatter parses as YAML", str(exc).split("\n")[0])
        else:
            report(
                isinstance(data, dict),
                "frontmatter parses as YAML",
                "" if isinstance(data, dict) else "top level is not a mapping",
            )

    def fm_value(key: str) -> str | None:
        """Read a frontmatter string field, preferring the parsed mapping."""
        if isinstance(data, dict):
            value = data.get(key)
            return value if isinstance(value, str) else None
        match = re.search(rf"(?m)^{re.escape(key)}:[ \t]*(.+)$", fm_text)
        return match.group(1).strip() if match else None

    name = fm_value("name")
    report(bool(name), "frontmatter has a non-empty 'name'")
    if name:
        report(bool(NAME_RE.match(name)), "name matches ^[a-z0-9]+(-[a-z0-9]+)*$", name)
        report(
            name == dirname,
            "name equals the containing directory name",
            ""
            if name == dirname
            else f"name={name!r} dir={dirname!r} -- platforms that enforce this will not load the skill",
        )

    desc = fm_value("description")
    report(bool(desc), "frontmatter has a non-empty 'description'")
    if desc and len(desc) > DESC_MAX:
        print(f"[WARN] description is {len(desc)} chars; the Agent Skills spec recommends <= {DESC_MAX}")

    report((root / "README.md").is_file(), "README.md exists")
    report(
        any((root / p).is_file() for p in ("LICENSE", "LICENSE.md", "LICENSE.txt")),
        "a LICENSE file exists",
    )

    print()
    if _failed:
        print("FAILED - fix the items marked FAIL above.")
        return 1
    print("OK - SKILL.md is well-formed and loadable.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
