"""Assemble the playtest guide, and refuse to emit one that is broken.

The guide is published as an Artifact, which wraps whatever this produces in a
document skeleton -- so `head.html` carries the <title> and the whole stylesheet,
`body.html` carries the route, and this script is only glue plus a gate.

The gate matters more than the glue. The guide is a QA document: a checkbox that
silently vanished inside an unclosed tag is worse than no guide, because the run
still looks complete. So a build that fails any check below writes nothing.

    python docs/playtest-guide/build.py            # build and validate
    python docs/playtest-guide/build.py --check     # validate only, touch nothing

Publish `guide.html` with the Artifact tool, passing the existing artifact URL so
it updates in place rather than claiming a new one.
"""
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
QA = HERE.parent / "qa.md"
OUT = HERE / "guide.html"

# Void elements never close; anything else that opens must.
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}


def assemble():
    """Concatenate the two sources, normalising to LF.

    Line endings are forced rather than inherited: the mod payload under files/
    is marked -text in .gitattributes because it is CRLF game data, but these are
    ordinary documents, and a build whose output depends on the checkout's
    autocrlf setting is a build that differs between machines for no reason.
    """
    parts = []
    for name in ("head.html", "body.html"):
        src = HERE / name
        if not src.exists():
            sys.exit(f"missing source: {src}")
        parts.append(src.read_text(encoding="utf-8").replace("\r\n", "\n"))
    return "".join(parts)


def check(html):
    """Return a list of problems. Empty means the guide is publishable."""
    problems = []

    # ASCII only. The repo rule, and it also catches a smart quote pasted in
    # from somewhere that would render as a mojibake box under latin-1 tooling.
    for n, line in enumerate(html.split("\n"), 1):
        bad = [c for c in line if ord(c) > 127]
        if bad:
            problems.append(f"line {n}: non-ascii {bad!r} (use HTML entities)")

    # Tag balance. This is the check that earns the script: the guide is a long
    # list of nested <li><div><div>, and one missing </div> swallows every check
    # that follows it -- invisibly, since the page still renders.
    stack = []
    for m in re.finditer(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*?)(/?)>", html):
        closing, tag, _attrs, self_closing = m.groups()
        tag = tag.lower()
        if tag in VOID or self_closing:
            continue
        line = html.count("\n", 0, m.start()) + 1
        if closing:
            if not stack:
                problems.append(f"line {line}: </{tag}> with nothing open")
            elif stack[-1][0] != tag:
                problems.append(
                    f"line {line}: </{tag}> closes <{stack[-1][0]}> "
                    f"opened on line {stack[-1][1]}")
                stack.pop()
            else:
                stack.pop()
        else:
            stack.append((tag, line))
    for tag, line in stack:
        problems.append(f"line {line}: <{tag}> never closed")

    # The Artifact tool reads the title from the first 8KB and nowhere else.
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    if not title:
        problems.append("no <title> -- the artifact would be named after the file")
    elif html.index("<title>") > 8192:
        problems.append("<title> sits past the 8KB the publisher scans")

    # Every check should be tickable, and every case ID in the guide should be a
    # case that actually exists in qa.md. The second half is the anti-drift
    # check: qa.md and the guide are two views of one case list, and the way
    # they rot is a case being renumbered in one and not the other.
    boxes = len(re.findall(r'<input type="checkbox">', html))
    if boxes == 0:
        problems.append("no checkboxes -- this is a checklist")
    if QA.exists():
        qa = QA.read_text(encoding="utf-8")
        known = set(re.findall(r"^\|\s*([A-Z]+\d+)\s*\|", qa, re.M))
        cited = set()
        for span in re.findall(r'<span class="id">(.*?)</span>', html):
            span = span.replace("&ndash;", "-").replace("&mdash;", "-")
            cited.update(re.findall(r"[A-Z]+\d+", span))
        # A range like "R2-R3" cites its endpoints; only those are verified.
        for cid in sorted(cited - known):
            problems.append(f"cites {cid}, which is not a case in docs/qa.md")
        if not cited:
            problems.append("no case IDs cited -- the guide is untraceable to qa.md")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="validate without writing guide.html")
    args = ap.parse_args()

    html = assemble()
    problems = check(html)
    if problems:
        print(f"guide NOT built -- {len(problems)} problem(s):", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1

    boxes = len(re.findall(r'<input type="checkbox">', html))
    title = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
    if args.check:
        print(f"ok  {title!r}: {boxes} checks, {len(html)} bytes (nothing written)")
        return 0

    OUT.write_text(html, encoding="utf-8", newline="\n")
    print(f"ok  {OUT.relative_to(HERE.parent.parent)}: "
          f"{title!r}, {boxes} checks, {OUT.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
