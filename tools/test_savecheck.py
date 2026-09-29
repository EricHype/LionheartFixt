"""Hold tools/savecheck.py against whatever saves are on this machine.

Saves are not in the repo and differ per tester, so this asserts invariants rather than values. It
skips cleanly when the game is not installed, which is the normal case in CI.

The two invariants that matter are the ones that were got wrong while writing it:

* **Every zlib stream must inflate**, and scanning only for `#### BEGIN TEMPORARY FILE ####` misses the
  stream holding the player -- so a save must yield more than the marker count suggests.
* **The player's two scopes must not be mixed.** Karma appears twice in the player's window, once under
  `Derived Character Attribute Temporary Modifiers` and once under the permanent array, and only the
  permanent one is the character's karma. Reading Character Level from the whole stream instead of the
  player's window picks up the first NPC serialised.

    python tools/test_savecheck.py
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import savecheck as S  # noqa: E402


def main():
    if not S.SAVES.exists():
        print("SKIP: no game install at %s" % S.GAME)
        return 0
    saves = sorted(S.SAVES.glob("*.sav"))
    if not saves:
        print("SKIP: no saves in %s" % S.SAVES)
        return 0

    fails, with_player = [], 0
    for p in saves:
        raw = p.read_bytes()
        try:
            ss = [t for _, t in S.streams(raw)]
        except Exception as e:                                    # noqa: BLE001
            fails.append("%s: streams() raised %s" % (p.name, e))
            continue
        if not ss:
            fails.append("%s: no stream inflated" % p.name)
            continue
        # every stream must be the brace grammar, not garbage that happened to inflate
        for t in ss:
            if not re.match(r"^C[A-Za-z]+\r\n\{", t):
                fails.append("%s: a stream does not open with a class and brace: %r" % (p.name, t[:30]))
                break
        # the marker count understates the streams -- that miss is what hid the player
        markers = raw.count(b"#### BEGIN TEMPORARY FILE ####")
        if len(ss) < markers:
            fails.append("%s: %d streams for %d markers" % (p.name, len(ss), markers))

        name, window, perm = S.player_block(ss)
        if perm is None:
            continue
        with_player += 1
        if not name:
            fails.append("%s: player block found but no User Assigned Name" % p.name)
        # karma must come from the permanent array; the window alone can hand back the temporary one
        kperm = S.field(perm, "Derived Character Attributes/Karma")
        if kperm is not None:
            enclosing = re.findall(r"\t*([A-Za-z][A-Za-z ]*)=Array",
                                   perm[:perm.find("Derived Character Attributes/Karma")])
            if enclosing and "Temporary" in enclosing[-1]:
                fails.append("%s: karma read out of %s" % (p.name, enclosing[-1]))
        # Character Level must come from the player's window, never the whole stream
        if window is not None and S.field(window, "Character Level") is None:
            fails.append("%s: no Character Level in the player window" % p.name)
        f = S.facts(ss)
        if "User Assigned Name" not in f:
            fails.append("%s: facts() produced no character name" % p.name)

    if S.CHARACTER.exists():
        t = S.read_character()
        if "CSavedCharacter" not in t:
            fails.append("character file did not inflate to CSavedCharacter")
        if len(S.attrs(t, "Uber Perks/")) != 5:
            fails.append("character file: expected 5 Uber Perks ranks, got %d"
                         % len(S.attrs(t, "Uber Perks/")))

    for f in fails:
        print("FAIL " + f)
    print("saves checked        : %d" % len(saves))
    print("with a player block  : %d" % with_player)
    print("character file       : %s" % ("read" if S.CHARACTER.exists() else "absent"))
    if fails:
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
