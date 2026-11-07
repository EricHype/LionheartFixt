"""Give nameless spawns a real name, so the scripts aimed at them land. Found because the English did not stand down.

An action's name list compares an entity's `Name` (`0x62bc00`, through `0x5b9b40`), and skips one with none. A generator
with a blank `New Name`, over a can with a blank `Name`, spawns exactly that. `User Assigned Name` is a display name the
lookup never reads, so 0.79.4's repair of the garrison lists, and 0.97.3's Hujark retarget, were aimed at nobody. This
corrects engine-notes.md, which said the opposite.

Each generator here takes the display name of its first can, which every list naming that family already includes.
Corpse generators are left alone. Gate District and Maw of the Assasin are left alone too: their references are vanilla's,
dead since 2003, and waking them would change fights nobody has asked to change.

A rerun is a no-op.

    python tools/build_spawn_names.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR, FX

SKIP = {"Levels/1 Barcelona/Gate District.zax", "Levels/8 Alamut/04 Maw of the Assasin.zax"}
FIELDS = r"(?:Target Name|Entity Name|Enemy Name|Name To Check For|Target|Name of Position)"
cans = {}


def can(e):
    """(display name, Name) of a can, or blanks."""
    if e not in cans:
        d = n = ""
        try:
            t = lhbuild.read("Resources/" + e + ".can")
            r = re.findall(r"User Assigned Name=([^\r\n]*)", t)
            d = r[0] if r else ""
            r = re.findall(r"(?m)^\t\tName=([^\r\n]*)\r", t)
            n = r[0] if r else ""
        except Exception:
            pass
        cans[e] = (d, n)
    return cans[e]


def parts(z):
    return re.findall(r"(?ms)^\t\tLevel Part=\w+\r\n\t\t\{\r\n.*?^\t\t\}", z)


def nameless(x):
    """The display names a generator's spawns would have, if it spawns nameless characters."""
    if "CGeneratorAI" not in x and "CSimpleGenerator" not in x:
        return []
    if re.search(r"(?m)^\t\t\tName=[^\r\n]*Dead Body", x):
        return []
    nn = re.search(r"New Name=([^\r\n]*)", x)
    if not nn or nn.group(1):
        return []
    out = []
    for e in re.findall(r"Entity=([^\r\n]+)", x):
        d, n = can(e)
        if d and not n and d not in out:
            out.append(d)
    return out


def wanted(z):
    """Lower-cased names this map's scripts aim at."""
    out = set()
    for m in re.finditer(r"(?m)^\s*" + FIELDS + r"=([^\r\n$][^\r\n]*)\r", z):
        out.update(t.strip().lower() for t in m.group(1).split(",") if t.strip())
    return out


def missed(z):
    """Names scripts aim at that only nameless spawns would bear."""
    named = {n.lower() for n in re.findall(r"(?m)^\t\t\tName=([^\r\n]+)\r", z)} | {n.lower() for n in re.findall(r"New Name=([^\r\n]+)\r", z)}
    bear = {d.lower() for x in parts(z) for d in nameless(x)}
    return sorted((wanted(z) & bear) - named)


def main():
    done = 0
    for f in sorted((FX / "Levels").rglob("*.zax")):
        rel = f.relative_to(FX).as_posix()
        if rel in SKIP:
            continue
        z = lhbuild.read(rel)
        want = set(missed(z))
        new = z
        n = 0
        for x in parts(z):
            names = [d for d in nameless(x) if d.lower() in want]
            if names:
                y = re.sub(r"New Name=\r", lambda m: "New Name=" + names[0] + CR, x, count=1)
                new = new.replace(x, y)
                n += 1
        if n:
            lhbuild.write_map(rel, new)
            done += n
            print(rel[7:], n)
    print(done, "generators named")


if __name__ == "__main__":
    main()
