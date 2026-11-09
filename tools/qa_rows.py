"""Every QA case in docs/qa.md as data, so the 1.0 route can be built from the authority rather than retyped.

A case is a table row whose first cell is an ID (`A0.3`, `GL1`, `HR4`). Its section is the `##` heading above it, which
for release rows names the release. The script writes docs/test-route/rows.json and prints a count per section.

    python tools/qa_rows.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QA = ROOT / "docs" / "qa.md"
OUT = ROOT / "docs" / "test-route" / "rows.json"


def cells(line):
    """Split a markdown table row on pipes that are not inside backticks."""
    out, cur, tick = [], "", False
    for ch in line.strip().strip("|"):
        if ch == "`":
            tick = not tick
        if ch == "|" and not tick:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    out.append(cur.strip())
    return out


def rows():
    section, header, found = "", None, []
    for n, line in enumerate(QA.read_bytes().decode("utf8").splitlines(), 1):
        if line.startswith("## "):
            section, header = line[3:].strip(), None
            continue
        if not line.startswith("|"):
            header = None if not line.strip() else header
            continue
        c = cells(line)
        if header is None:
            header = [h.lower() for h in c]
            continue
        if set(line.replace("|", "").strip()) <= set("-: "):
            continue
        if not re.fullmatch(r"[A-Z][A-Za-z]*\d*(\.\d+)?[a-z]?", c[0].strip("*")):
            continue
        row = {"id": c[0].strip("*"), "section": section, "line": n}
        for h, v in zip(header[1:], c[1:]):
            row[h] = v
        found.append(row)
    return found


def main():
    r = rows()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(r, indent=1, ensure_ascii=False), encoding="utf8")
    ids = [x["id"] for x in r]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    print(len(r), "cases in", len({x["section"] for x in r}), "sections;", len(dup), "IDs used twice:", dup[:20])


if __name__ == "__main__":
    main()
