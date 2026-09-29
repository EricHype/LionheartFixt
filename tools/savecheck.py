"""Read Lionheart's saves and character file, so a playtest can be checked instead of remembered.

Most rows in `docs/qa.md` ask about state the game already writes to disk -- a faction rank, a scripting
variable, whether an entity is still on a map. This reads that state directly, so a tester plays the
scene and one command afterwards says whether it took.

**Both formats are zlib, not opaque binary.** The modding notes long described a save's swapped layers as
raw bytes. They are deflate streams, and so is the character file:

    Characters/Last Character.RPG   1 flag byte, u32 compressed len, u32 raw len, then the zlib stream
    SaveGames/*.sav                 a text envelope holding SEVERAL zlib streams

Decompressed, both are the ordinary `TypeName { Key=Value }` grammar every other resource file uses. One
quicksave holds a 778 KB `CLayerSaveData` and a 2.8 MB `CLayerHolder`.

**Only some streams are announced.** A `Current Temp File=TempFile` blob sits behind a
`#### BEGIN TEMPORARY FILE ####` marker, but the save also carries `Mission Temp File` and
`Mission Marker Temp File`, whose streams have no such marker. Scanning for the markers alone finds the
levels you have left and **misses the live one, which is the stream holding the player**. So this scans
for every `78 9c` in the file and keeps whatever inflates.

**Where the player is, and how the two sources differ.**

* A **save** carries the live player inside `Derived Character Attribute Permanent Modifiers`, in the
  one `CLayerHolder` stream (the live layer). That array stores only what has been **changed from
  default**, so a rank that is absent is zero -- never read absence as "missing".

  The player is found by anchoring on `Uber Perks`, which no NPC carries. The consequence of the
  store-only-changes rule is that **a character who has joined no order has no anchor at all**: 38 of
  the 60 saves tested are in that state, and there the tool reports all ranks 0 rather than guessing.
  Two anchors that look better and are not: the nearest `User Assigned Name=` above the ranks can be
  17 KB away and belong to a Goblin Archer, and `Name=Player1` occurs up to five times per stream as a
  script target. A stale copy of the player also survives in swapped-out `CLayerSaveData` layers, so
  candidates are scored and the live holder wins.
* The **character file** is a full table with every attribute listed, zeros included. It is written at
  character creation, not on every save: in testing its mtime trailed the quicksave by sixteen minutes.
  **Treat it as the starting state, and prefer the save for anything current.**

The workflow `snapshot` and `diff` exist for:

    python tools/savecheck.py snapshot before-bishop --save latest
    ... play the scene, save ...
    python tools/savecheck.py diff before-bishop        # Saladin Rank 0 -> 1, and what else moved

Snapshots go to ~/.lionheart-snapshots so nothing lands in the repo.

    python tools/savecheck.py save latest               # map, player, ranks, variables, layers
    python tools/savecheck.py character                 # the starting character
    python tools/savecheck.py grep "Goblin Khan" --save latest
    python tools/savecheck.py dump latest -o out        # write the plain text and grep it yourself
"""
import argparse
import os
import re
import shutil
import struct
import sys
import zlib
from pathlib import Path

GAME = Path(os.environ.get(
    "LIONHEART_GAME",
    r"C:\Program Files (x86)\GOG Galaxy\Games\Lionheart - Legacy of the Crusader"))
CHARACTER = GAME / "Characters" / "Last Character.RPG"
SAVES = GAME / "SaveGames"
SNAPS = Path(os.environ.get("LIONHEART_SNAPSHOTS", Path.home() / ".lionheart-snapshots"))
ZLIB = b"\x78\x9c"
WINDOW = 8000             # how far above the ranks the player's own fields sit
MIN_STREAM = 512          # below this it is not a layer, just a coincidental byte pair


# --------------------------------------------------------------------------- containers
def streams(raw):
    """Every zlib stream in the file, as (offset, text). Scans for the header rather than trusting
    the `#### BEGIN TEMPORARY FILE ####` markers, which do not precede all of them."""
    out, pos = [], 0
    while True:
        z = raw.find(ZLIB, pos)
        if z < 0:
            return out
        try:
            text = zlib.decompressobj().decompress(raw[z:])
        except zlib.error:
            pos = z + 2
            continue
        if len(text) >= MIN_STREAM:
            if z >= 8:
                declared = struct.unpack("<II", raw[z - 8:z])[1]
                if declared and declared != len(text):
                    text = text            # header is advisory; the stream is what it is
            out.append((z, text.decode("latin-1")))
            pos = z + 2
        else:
            pos = z + 2


def envelope(raw):
    return re.sub(rb"#### BEGIN TEMPORARY FILE ####.*?#### END TEMPORARY FILE ####", b"<blob>",
                  raw, flags=re.S).decode("latin-1", "replace")


def read_character(path=CHARACTER):
    s = streams(path.read_bytes())
    if not s:
        raise SystemExit("%s carries no zlib stream" % path)
    return max(s, key=lambda x: len(x[1]))[1]


def newest_save():
    saves = sorted(SAVES.glob("*.sav"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not saves:
        raise SystemExit("no saves in %s" % SAVES)
    return saves[0]


def resolve_save(which):
    if which in (None, "latest"):
        return newest_save()
    for cand in (Path(which), SAVES / which, SAVES / (str(which) + ".sav")):
        if cand.exists():
            return cand
    raise SystemExit("no such save: %s" % which)


# --------------------------------------------------------------------------- reading fields
def field(t, key):
    m = re.search(r"\t*" + re.escape(key) + r"=([^\r\n]*)", t)
    return m.group(1) if m else None


def attrs(t, group):
    return dict(re.findall(r"Derived Character Attributes/" + group + r"([^=\r\n]*)=([^\r\n]*)", t))


def perks(t):
    m = re.search(r"Selected Perks=Array\r\n\t*\{\r\n\t*Item Count=(\d+)(.*?)\n\t*\}", t, re.S)
    return re.findall(r"Perks/([^\r\n]*)", m.group(2)) if m else []


def nonzero(d):
    return {k: v for k, v in d.items() if v not in ("0", "0.000000", "", None)}


def player_block(texts):
    """The player's live state in a save.

    Anchored on `Uber Perks`, which only the player carries -- every NPC has none.

    Two scopes come back, and mixing them up gives wrong answers both ways:

    * `window`, from the `User Assigned Name=` down to the ranks, holds Character Level and Experience
      Points. Reading those from the whole stream instead picks up whatever NPC serialises first
      (Signor Leo, in the save this was written against).
    * `perm`, the `Derived Character Attribute Permanent Modifiers` array, holds the ranks, karma and
      scripting variables. Karma appears **twice** in the window -- once under
      `Derived Character Attribute Temporary Modifiers` and once here -- and the temporary one is not
      the character's karma (-46 against a real 25 in the save this was written against).
    """
    best = None
    for t in texts:
        live = t.startswith("CLayerHolder")
        for m in re.finditer(r"Derived Character Attributes/Uber Perks/", t):
            i = m.start()
            lo = max(0, i - WINDOW)
            j = t.rfind("User Assigned Name=", lo, i)
            k = t.rfind("Derived Character Attribute Permanent Modifiers=Array", lo, i)
            window = t[(j if j >= 0 else lo):i]
            end = t.find("\n\t\t\t\t\t\t}", i)
            score = (live, j >= 0, "Character Level=" in window)
            cand = (score,
                    t[j:t.find("\r", j)].split("=", 1)[1] if j >= 0 else None,
                    window,
                    t[(k if k >= 0 else i):end if end > 0 else i + WINDOW])
            if best is None or cand[0] > best[0]:
                best = cand
    return best[1:] if best else (None, None, None)


def facts(source_texts, name_hint=None):
    """A flat dict of everything worth comparing, from either source."""
    joined = "\n".join(source_texts)
    name, window, perm = player_block(source_texts)
    # a save is read through the player's two scopes; the character file IS the player, so the whole
    # text serves as both
    ident = window if window else joined
    attr = perm if perm else joined
    d = {}
    for k in ("User Assigned Name", "Character Level", "Experience Points"):
        v = field(ident, k)
        if v is not None:
            d[k] = v
    if name:
        d["User Assigned Name"] = name
    for k, v in attrs(attr, "Uber Perks/").items():
        d["rank/" + k] = v
    for k, v in attrs(attr, "Game Scripting Variables/").items():
        d["var/" + k] = v
    kv = field(attr, "Derived Character Attributes/Karma")
    if kv is not None:
        d["Karma"] = kv
    for x in perks(joined):
        d["perk/" + x] = "yes"
    return d


def load(path):
    """-> (list of stream texts, envelope text or None)."""
    raw = Path(path).read_bytes()
    ss = [t for _, t in streams(raw)]
    env = envelope(raw) if str(path).lower().endswith(".sav") else None
    return ss, env


# --------------------------------------------------------------------------- commands
def show_character(a):
    t = read_character()
    print("character file : %s (%d bytes inflated)" % (CHARACTER.name, len(t)))
    print("  NOTE: written at character creation, not on every save -- this is the STARTING state.")
    print("        Use `savecheck save` for anything current.\n")
    for k in ("User Assigned Name", "Gender", "Character Level", "Experience Points", "Karma", "Spirit"):
        v = field(t, k)
        if v is not None:
            print("  %-20s %s" % (k, v))
    print("\nfaction ranks")
    for k, v in sorted(attrs(t, "Uber Perks/").items()):
        print("  %-22s %s%s" % (k, v, "  <--" if v not in ("0", "") else ""))
    p = perks(t)
    print("\nperks (%d)%s" % (len(p), "" if p else "  none"))
    for x in p:
        print("   " + x)
    sv, allv = nonzero(attrs(t, "Game Scripting Variables/")), attrs(t, "Game Scripting Variables/")
    print("\nscripting variables: %d set, of %d tracked" % (len(sv), len(allv)))
    for k in sorted(sv):
        print("  %-52s %s" % (k, sv[k]))
    if a.all:
        print("\n  unset: %s" % ", ".join(sorted(k for k in allv if k not in sv)))
    return 0


def show_save(a):
    p = resolve_save(a.which)
    ss, env = load(p)
    print("save           : %s" % p.name)
    for k in ("Save Date and Time", "Save Game Description", "Map File Name", "Map Description",
              "Player Health", "Elapsed Time"):
        v = field(env, k)
        if v is not None:
            print("  %-20s %s" % (k, v))

    name, window, perm = player_block(ss)
    print("\nplayer (live, from the save)")
    if not perm:
        print("  no Uber Perks entry in this save, which IS the answer: the permanent-modifier array")
        print("  stores only values changed from default, so all five faction ranks are 0 and this")
        print("  character has joined nothing yet. Level, karma and variables cannot be read without")
        print("  that anchor -- 38 of the 60 saves tested are in this state.")
    else:
        print("  %-22s %s" % ("name", name))
        for k in ("Character Level", "Experience Points"):
            v = field(window, k)
            if v is not None:
                print("  %-22s %s" % (k, v))
        r = attrs(perm, "Uber Perks/")
        print("  ranks set             %s" % (", ".join("%s=%s" % kv for kv in sorted(r.items()))
                                              or "none (all five default to 0)"))
        kv = field(perm, "Derived Character Attributes/Karma")
        print("  %-22s %s" % ("Karma", kv if kv is not None else "0 (default)"))
        sv = nonzero(attrs(perm, "Game Scripting Variables/"))
        print("  scripting vars set    %s" % (", ".join("%s=%s" % x for x in sorted(sv.items()))
                                              or "none"))
        print("  (this array stores only values CHANGED from default; absent means zero)")

    print("\nstreams (%d)" % len(ss))
    for t in ss:
        kind = t.split("\r\n", 1)[0]
        print("  %-22s %9d bytes  %5d entities  %4d generators"
              % (kind, len(t), t.count("CEntityBase"), t.count("CGeneratorAI")))
    names = re.findall(r"Partial Layer Name=([^\r\n]*)", env)
    print("\nlayers left behind (%d): %s" % (len(names), ", ".join(names) or "none"))
    return 0


def do_dump(a):
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if a.which == "character":
        (out / "character.txt").write_text(read_character(), encoding="latin-1", newline="")
        print("wrote", out / "character.txt")
        return 0
    p = resolve_save(a.which)
    ss, env = load(p)
    (out / (p.stem + ".envelope.txt")).write_text(env, encoding="latin-1", newline="")
    for i, t in enumerate(ss, 1):
        kind = re.sub(r"[^A-Za-z0-9]+", "", t.split("\r\n", 1)[0])[:24] or "stream"
        (out / ("%s.%02d.%s.txt" % (p.stem, i, kind))).write_text(t, encoding="latin-1", newline="")
    print("wrote %d file(s) to %s" % (len(ss) + 1, out))
    return 0


def do_grep(a):
    rx = re.compile(a.pattern, 0 if a.case else re.I)
    sources = []
    if not a.save_only:
        sources.append(("character", read_character()))
    if a.save:
        p = resolve_save(a.save)
        ss, env = load(p)
        sources.append((p.name + ":envelope", env))
        sources += [("%s:%d" % (p.name, i), t) for i, t in enumerate(ss, 1)]
    hits = 0
    for label, text in sources:
        for i, line in enumerate(text.split("\r\n"), 1):
            if rx.search(line):
                hits += 1
                print("%-28s %7d  %s" % (label, i, line.strip()[:110]))
                if hits >= a.limit:
                    print("... stopped at %d hits" % a.limit)
                    return 0
    if not hits:
        print("no match for %r" % a.pattern)
    return 0


def do_snapshot(a):
    SNAPS.mkdir(parents=True, exist_ok=True)
    src = resolve_save(a.save) if a.save else CHARACTER
    dest = SNAPS / (a.label + src.suffix)
    shutil.copy2(src, dest)
    ss, _ = load(src)
    f = facts(ss)
    print("snapshot %-22s <- %s" % (a.label, src.name))
    print("  %s" % ", ".join("%s=%s" % kv for kv in sorted(f.items())[:6]) or "  (no facts read)")
    return 0


def do_diff(a):
    found = [p for p in SNAPS.glob(a.label + ".*")]
    if not found:
        raise SystemExit("no snapshot %r in %s" % (a.label, SNAPS))
    old = found[0]
    new = resolve_save(a.save) if (a.save or old.suffix.lower() == ".sav") else CHARACTER
    b, c = facts(load(old)[0]), facts(load(new)[0])
    print("diff %s (%s)  ->  %s" % (a.label, old.name, new.name))
    changed = [(k, b.get(k), c.get(k)) for k in sorted(set(b) | set(c)) if b.get(k) != c.get(k)]
    if not changed:
        print("  nothing changed")
    for k, x, y in changed:
        print("  %-52s %s -> %s" % (k, x if x is not None else "0/absent",
                                    y if y is not None else "0/absent"))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd")

    c = sub.add_parser("character", help="the STARTING character: ranks, perks, scripting variables")
    c.add_argument("--all", action="store_true", help="also list the scripting variables still unset")
    c.set_defaults(fn=show_character)

    s = sub.add_parser("save", help="a save: map, live player state, streams, layers")
    s.add_argument("which", nargs="?", default="latest")
    s.set_defaults(fn=show_save)

    d = sub.add_parser("dump", help="write the decompressed text out for grepping")
    d.add_argument("which", nargs="?", default="latest")
    d.add_argument("-o", "--out", default="savecheck-out")
    d.set_defaults(fn=do_dump)

    g = sub.add_parser("grep", help="search the decompressed character and/or a save")
    g.add_argument("pattern")
    g.add_argument("--save", nargs="?", const="latest")
    g.add_argument("--save-only", action="store_true", help="skip the character file")
    g.add_argument("--case", action="store_true")
    g.add_argument("--limit", type=int, default=60)
    g.set_defaults(fn=do_grep)

    n = sub.add_parser("snapshot", help="park a copy to diff against later")
    n.add_argument("label")
    n.add_argument("--save", nargs="?", const="latest", help="snapshot a save instead of the character")
    n.set_defaults(fn=do_snapshot)

    f = sub.add_parser("diff", help="what changed since a snapshot")
    f.add_argument("label")
    f.add_argument("--save", nargs="?", const="latest")
    f.set_defaults(fn=do_diff)

    a = ap.parse_args(argv or None)
    if not a.cmd:
        a = ap.parse_args(["save"])
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
