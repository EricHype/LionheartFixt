"""Hold tools/md2bbcode.py against the forum posts already shipped.

The strict half: every post from **0.22.0** onward must come back byte-identical, because that is the
stretch whose conventions are self-consistent and it is the convention the converter implements.

The floor half: the older posts were hand-converted and their conventions drifted -- `[size=125]`
headings, `*emphasis*` converted, backticks sometimes deleted rather than italicised, and one inverted
`[i]` pair in 0.21.1 where a quote straddled a line break. Many of them still come out right anyway, so
the count is pinned: an edit that drops it means the converter changed behaviour beyond the current
convention, which is worth knowing even though those files must never be regenerated.

    python tools/test_md2bbcode.py
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from md2bbcode import convert  # noqa: E402

DIST = pathlib.Path(__file__).resolve().parent.parent / "dist"
STRICT_FROM = (0, 22, 0)      # the convention md2bbcode implements begins here
LEGACY_FLOOR = 23             # how many posts reproduce today, older drifting ones included
NAME = re.compile(r"^forum-post-(\d+(?:\.\d+)*)\.md$")


def version(p):
    return tuple(int(x) for x in NAME.match(p.name).group(1).split("."))


def main():
    pairs = []
    for md in sorted((p for p in DIST.glob("forum-post-*.md") if NAME.match(p.name)), key=version):
        bb = md.with_name(md.name[:-len(".md")] + ".bbcode.txt")
        if bb.exists():
            pairs.append((version(md), md, bb))
    assert pairs, "no forum-post pairs found in %s" % DIST

    failures, reproduced = [], 0
    for v, md, bb in pairs:
        got = convert(md.read_text(encoding="utf-8"))
        want = bb.read_text(encoding="utf-8")
        if got == want:
            reproduced += 1
        elif v >= STRICT_FROM:
            failures.append((v, md.name, got, want))

    for v, name, got, want in failures:
        print("FAIL %s does not round-trip" % name)
        g, w = got.split("\n"), want.split("\n")
        for i in range(max(len(g), len(w))):
            a = g[i] if i < len(g) else "<missing>"
            b = w[i] if i < len(w) else "<missing>"
            if a != b:
                print("  line %d" % (i + 1))
                print("    converter: %s" % a)
                print("    shipped  : %s" % b)
                break

    strict = [(v, md, bb) for v, md, bb in pairs if v >= STRICT_FROM]
    print("pairs on disk            : %d" % len(pairs))
    print("strict (>= %s)        : %d, %d failing"
          % (".".join(str(x) for x in STRICT_FROM), len(strict), len(failures)))
    print("reproduced overall       : %d (floor %d)" % (reproduced, LEGACY_FLOOR))

    if failures:
        return 1
    if reproduced < LEGACY_FLOOR:
        print("FAIL reproduced count fell below the pinned floor -- the converter changed behaviour",
              file=sys.stderr)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
