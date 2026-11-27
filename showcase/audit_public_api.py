#!/usr/bin/env python3
"""Extract a reviewable public-declaration inventory from Kira sources."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECL = re.compile(
    r"^(?P<indent>\s*)(?:(?P<mods>(?:public|internal|private|protected|expect|actual|"
    r"abstract|open|sealed|data|value|enum|annotation|inline|suspend|operator|infix|tailrec)\s+)*)"
    r"(?P<kind>fun|class|interface|object|typealias)\s+(?:<[^>]+>\s*)?"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)",
)
PACKAGE = re.compile(r"^package\s+([\w.]+)")
SRC = re.compile(r"/src/([^/]+)/")


def source_set(path: Path) -> str:
    match = SRC.search(path.as_posix())
    return match.group(1) if match else "unknown"


def main() -> None:
    entries = []
    for path in sorted(ROOT.glob("kira-*/src/**/*.kt")):
        if "/build/" in path.as_posix():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        package = "unknown"
        lines = text.splitlines()
        for line in lines:
            m = PACKAGE.match(line)
            if m:
                package = m.group(1)
                break
        for index, line in enumerate(lines):
            m = DECL.match(line)
            if not m:
                continue
            mods = (m.group("mods") or "").split()
            if "internal" in mods or "private" in mods or "protected" in mods:
                continue
            prefix = " ".join(lines[max(0, index - 3):index])
            entries.append({
                "module": path.relative_to(ROOT).as_posix().split("/")[0],
                "sourceSet": source_set(path),
                "file": path.relative_to(ROOT).as_posix(),
                "line": index + 1,
                "package": package,
                "kind": m.group("kind"),
                "name": m.group("name"),
                "expect": "expect" in mods,
                "actual": "actual" in mods,
                "composable": "@Composable" in prefix,
            })
    out = ROOT / "showcase" / "public-api.json"
    out.write_text(json.dumps({"count": len(entries), "entries": entries}, indent=2) + "\n", encoding="utf-8")
    by_module = {}
    for entry in entries:
        by_module.setdefault(entry["module"], 0)
        by_module[entry["module"]] += 1
    print(f"wrote {len(entries)} declarations")
    for module, count in sorted(by_module.items()):
        print(f"{module}: {count}")


if __name__ == "__main__":
    main()
