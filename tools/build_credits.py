"""Thank the people who reported bugs: in the game's credits roll and in the README.

One list, two outputs, so they cannot drift:

  * `Credits.txt`, the file the end-game credits roll reads, gains a `Lionheart Fixt` section after Interplay's team
    and before the third-party logos, in the file's own format: `_` for a section header, `+` for a role followed by
    a line holding one space, then names. Fixt did not override this file before; the rest of it is vanilla's.
  * `README.md` gains a `## Thanks` section, rewritten between its markers on every run.

Reporters are gathered from the GitHub issues, the Steam thread
(https://steamcommunity.com/app/595060/discussions/0/589561710754497274) and the RPG Codex thread
(https://rpgcodex.net/forums/threads/some-crazy-guy-is-modding-lionheart-legacy-of-the-crusader.157467), as of
2026-11-18. A person under two names is listed once. Add new reporters to REPORTERS and rerun.

    python tools/build_credits.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from build_shrine_repairs import register

AUTHOR = "Eric Heitmuller (EricHype)"
# name shown, where they reported, what they found (README only)
REPORTERS = [
    ("0gpa", "Steam", "the missing Lava Troll Hide"),
    ("Laz Sundays", "RPG Codex", "a long playtest: wands, enchantment balance, the Scimitar questline, Weng Choi, cloaks and more"),
    ("LucianCumpata", "GitHub", "the Lord Javier cutscene in the Cathedral"),
    ("Mixxer5", "GitHub", "the peaceful Montserrat path and a Lord Javier cutscene"),
    ("pgavryushov", "GitHub", "Quinn's quests, wasp stingers, capes and scrolls"),
    ("Phevrlezz", "Steam", "installing on a non-English copy"),
    ("Przemyslaw92pl", "GitHub", "magic bonus balance"),
    ("sacellem", "Steam", "the Inquisition chambers crash and installing on a Mac"),
    ("Stricken145", "GitHub and Steam", "seven reports, from the Inquisition chambers crash to the trolls and the Titans"),
    ("uroshpet", "GitHub", "a twelve-item list that became 0.99.33"),
]
ALSO = [("Litmanen", "for carrying reports between the forums")]

CREDITS = "Credits.txt"
ANCHOR = "________________________________"
CR = "\r\n"
BEGIN, END = "<!-- thanks:begin -->", "<!-- thanks:end -->"


def credits():
    t = lhbuild.read(CREDITS)
    if "_Lionheart Fixt" + CR in t:
        s = t.index("_Lionheart Fixt" + CR)
        e = t.index(ANCHOR, s)
        t = t[:s] + t[e:]
    first = t.index(ANCHOR)
    assert t.count(ANCHOR) == 2 and "_Interplay Entertainment" in t[:first], "unexpected Credits.txt layout"
    names = sorted((n for n, _, _ in REPORTERS), key=str.lower)
    lines = (["_Lionheart Fixt", "", "", "+Restoration, Implementation and Design", " ", AUTHOR, "", "",
              "+Bug Reports and Playtesting", " "] + names + ["", "", "+Thanks", " "] +
             [n + ", " + why for n, why in ALSO] + ["", "", "", ""])
    t = t[:first] + CR.join(lines) + t[first:]
    (lhbuild.FX / CREDITS).write_bytes(t.encode("latin-1"))
    register([CREDITS])


def readme():
    p = HERE.parent / "README.md"
    t = p.read_bytes().decode("utf8")
    rows = ["| " + n + " | " + where + " | " + what + " |" for n, where, what in sorted(REPORTERS, key=lambda r: r[0].lower())]
    body = (BEGIN + "\n## Thanks\n\nEvery bug report makes Fixt better. Thank you to everyone who took the time to write one up.\n\n"
            "| Reporter | Where | What they found |\n|---|---|---|\n" + "\n".join(rows) + "\n\n" +
            "".join("Thanks also to " + n + ", " + why + ".\n" for n, why in ALSO) +
            "\nThe same names are in the game's credits, after the original team. Found a bug? Open an issue.\n" + END)
    if BEGIN in t:
        s, e = t.index(BEGIN), t.index(END) + len(END)
        t = t[:s] + body + t[e:]
    else:
        anchor = "\n## Compatibility\n"
        assert t.count(anchor) == 1
        t = t.replace(anchor, "\n" + body + "\n" + anchor)
    p.write_bytes(t.encode("utf8"))


if __name__ == "__main__":
    credits()
    readme()
    print("credits: %d reporters, %d thanks" % (len(REPORTERS), len(ALSO)))
