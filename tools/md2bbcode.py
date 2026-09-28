"""Convert a release's forum post from Markdown to the bbcode the forum wants.

Every release ships `dist/forum-post-<v>.md` and `dist/forum-post-<v>.bbcode.txt`, and the two are the
same text in two markups -- the `.md` is byte-identical to `dist/release-notes-<v>.md`. This module is
the second step, so the bbcode stops being retyped by hand.

The rules were recovered by diffing the shipped pairs, not invented, and the shipped pairs disagree with
each other -- they were hand-converted for twenty-one releases and the conventions drifted:

* `## X` became `[size=125][b]X[/b][/size]` in 0.4.1 through 0.10.0 and plain `[b]X[/b]` everywhere else.
* `*emphasis*` was converted to `[i]...[/i]` up to 0.21.1 and left as asterisks from 0.22.0.
* Backticks became `[i]...[/i]` in most posts but were **deleted** in 0.16.0, 0.18.0 and 0.20.0.
* 0.21.1 has a `[i]`/`[/i]` pair inverted mid-sentence, where a `*"..."*` quote straddled a line break
  and a per-line substitution closed the span on the wrong side of the words.

So there is no single house rule to implement. This implements the convention that has held since
**0.22.0**, which is the only stretch that is self-consistent, and `tools/test_md2bbcode.py` holds that
as a hard requirement for 0.22.0 and later while pinning a floor for how many older posts still come out
right. Older posts are deliberately not reproducible and must not be regenerated.

Two rules worth keeping in mind when editing this:

* Bold and code spans **straddle line breaks** in these posts, so they are substituted over the whole
  document before any per-line work. Doing it per line is what produced 0.21.1's inverted pair.
* Tables stay as Markdown pipes. The forum renders them as plain text and every shipped post does the
  same, so converting them would be a change in output, not a fix.

    python tools/md2bbcode.py dist/forum-post-0.25.0.md dist/forum-post-0.25.0.bbcode.txt
    python tools/md2bbcode.py --check dist/forum-post-0.25.0.md dist/forum-post-0.25.0.bbcode.txt
"""
import argparse
import re
import sys

BOLD = re.compile(r"\*\*(.+?)\*\*", re.S)
CODE = re.compile(r"`(.+?)`", re.S)
LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def convert(md):
    """Markdown -> bbcode, in the convention shipped since 0.22.0."""
    # bold and code spans can straddle a line break, so run them over the whole text first
    md = BOLD.sub(r"[b]\1[/b]", md)
    md = CODE.sub(r"[i]\1[/i]", md)
    md = LINK.sub(r"\1", md)          # keep the label; the release URL goes at the bottom of the post
    out = []
    for line in md.split("\n"):
        if line.startswith("# "):
            out.append("[size=150][b]" + line[2:] + "[/b][/size]")
        elif line.startswith("## "):
            out.append("[b]" + line[3:] + "[/b]")
        elif line.startswith("> "):
            out.append("[i]" + line[2:] + "[/i]")
        else:
            out.append(line)
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("source", help="the forum post's .md")
    ap.add_argument("dest", help="the .bbcode.txt to write, or to compare against with --check")
    ap.add_argument("--check", action="store_true",
                    help="compare instead of writing; exit 1 if dest is not what source converts to")
    a = ap.parse_args(argv)

    with open(a.source, encoding="utf-8") as f:
        got = convert(f.read())
    if a.check:
        with open(a.dest, encoding="utf-8") as f:
            want = f.read()
        if got == want:
            print("%s matches %s" % (a.dest, a.source))
            return 0
        print("%s does NOT match what %s converts to" % (a.dest, a.source), file=sys.stderr)
        return 1
    with open(a.dest, "w", encoding="utf-8", newline="\n") as f:
        f.write(got)
    print("wrote %s (%d bytes)" % (a.dest, len(got)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
