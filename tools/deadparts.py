#!/usr/bin/env python3
"""Find level parts that start inactive and that nothing in the game ever switches on.

    python tools/deadparts.py "4 Crypt"          # one act, or any path fragment
    python tools/deadparts.py --all              # every map in the game

A part with `Active=0` is not dead content on its own -- the shipped game leaves thousands of
parts inactive on purpose -- so this only reports parts that no `CActivateAction`,
`CTriggerRelayAction` or `CCloneAction` anywhere in the mod or in vanilla names. Four separate
false-positive families cost real work in 0.15.0 and 0.16.0 before this script existed, and each
is handled here:

* **case** -- the engine's name lookup is case-insensitive, and the designers were inconsistent:
  a reward activated as `Thierry Reward` is a part named `thierry reward`.
* **comma lists** -- `Target Name=Joan Skeleton Generator, Ghoul Male attacking Joan bottom
  Generator` activates *two* parts. Splitting on lines alone reported both as dead, which is how
  the Doomed Plateau set-piece came to be called unbuilt when it runs.
* **clone prototypes** -- generators are usually cloned (`CCloneAction{Source Name=...}`) rather
  than activated, so the prototype sits inactive by design.
* **secrets** -- `CAISecretReveal` parts are switched on by the engine's own detection, not by
  script.

What it cannot know is whether the thing that activates a part is itself reachable. Treat the
output as a list of candidates and read each one before calling it a defect.
"""
import re
import sys
import zipfile
from pathlib import Path

CR = "\r\n"
REPO = Path(__file__).resolve().parent.parent
FILES = REPO / "files"
GAME = Path(r"C:\Program Files (x86)\GOG Galaxy\Games\Lionheart - Legacy of the Crusader")
VANILLA = GAME / "data.dat.vanilla.bak"

zf = zipfile.ZipFile(VANILLA)


def read(name):
    """The mod's copy of a resource if it has one, else vanilla's."""
    local = FILES / name
    if local.exists():
        return local.read_bytes().decode("latin-1")
    return zf.read(name).decode("latin-1")


def balanced(text, start):
    depth, i = 0, text.index("{", start)
    while True:
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1


def switched_on():
    """Every name any activate / trigger / clone action anywhere refers to, folded and split."""
    named = set()
    sources = [n for n in zf.namelist() if n.endswith((".zax", ".DialogTree"))]
    for name in sources:
        text = read(name)
        for m in re.finditer(r"=C(Activate|TriggerRelay|Clone)Action" + CR, text):
            try:
                end = balanced(text, m.end())
            except ValueError:
                continue
            for value in re.findall(r"(?:Target Name|Relay Name|Source Name)=([^\r\n]*)",
                                    text[m.end():end]):
                named.update(v.strip().lower() for v in value.split(",") if v.strip())
    return named


def survey(fragment, on):
    maps = sorted(n for n in zf.namelist()
                  if n.endswith(".zax") and (fragment is None or fragment.lower() in n.lower()))
    if not maps:
        print("no maps match %r" % fragment)
        return 0
    total = 0
    for mp in maps:
        text = read(mp)
        rows, seen = [], set()
        for m in re.finditer(r"\t\tLevel Part=", text):
            block = text[m.start():balanced(text, m.start())]
            name = re.search(r"\r\n\t\t\tName=([^\r\n]*)", block)
            active = re.search(r"\r\n\t\t\tActive=(\d)", block)
            if not (name and name.group(1).strip() and active and active.group(1) == "0"):
                continue
            key = name.group(1).strip().lower()
            if key in on or key in seen:
                continue
            classes = sorted(set(re.findall(r"Activity=(C\w+)", block)))
            if classes == ["CAISecretReveal"]:
                continue
            seen.add(key)
            pos = re.search(r"Position X=([^\r\n]*)\r\n\t\t\tPosition Y=([^\r\n]*)", block)
            rows.append((name.group(1).strip(), ",".join(classes),
                         ("(%s,%s)" % pos.groups()) if pos else ""))
        if rows:
            total += len(rows)
            print("\n%s" % mp)
            for name, classes, pos in rows:
                print("    %-44s %-32s %s" % (name[:44], classes[:32], pos))
    print("\n%d inactive part(s) that nothing names, across %d map(s)." % (total, len(maps)))
    print("Read each one before calling it a defect: this cannot tell whether whatever would")
    print("activate a part is itself reachable.")
    return total


def main():
    args = [a for a in sys.argv[1:] if a != "--all"]
    fragment = args[0] if args else None
    if fragment is None and "--all" not in sys.argv:
        print(__doc__.strip().splitlines()[0])
        print("\nusage: python tools/deadparts.py \"<path fragment>\" | --all")
        return 1
    survey(fragment, switched_on())
    return 0


if __name__ == "__main__":
    sys.exit(main())
