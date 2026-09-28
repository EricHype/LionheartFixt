"""Assert lhbuild's trigger builders against the vanilla triggers they model.

A generated block must carry every field vanilla writes. `touch_poly()` once omitted
`Auto-Flip Switch` -- the field that lets a trigger re-arm after the player walks out of it, which
vanilla writes on 756 touching triggers out of 756 -- and twelve Fixt triggers shipped unable to
re-arm before anyone noticed (see 0.21.5).

So the field lists here are not typed out. They are parsed from real vanilla triggers at run time:

    Eavesdrop trigger             Titan Village        CTouchingPolygonTriggerAI
    Mathuo-Iapetus Bubble trigger Titan Village        CTouchingOvalTriggerAI
    To Exalted Chambers poly      02 Temple Initiate   CAIInteractionSpecifier

Run after touching any trigger builder:  python tools/test_triggers.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lhbuild import B, CR, T, read, balanced, touch_poly, touch_oval, specifier  # noqa: E402


def part_named(z, name):
    i = z.index(CR + T * 3 + "Name=" + name + CR)
    s = z.rindex(CR + T * 2 + "Level Part=", 0, i) + len(CR)
    return z[s:balanced(z, s)]


def fields_of(block, cls):
    """The key names of `cls`'s own fields, in order, skipping anything inside a nested block."""
    b = block[block.index(cls + CR):]
    b = b[b.index("{") + len(CR) + 1:]
    out, depth = [], 0
    for line in b.split(CR):
        st = line.strip()
        if st == "{":
            depth += 1
        elif st == "}":
            if depth == 0:
                break
            depth -= 1
        elif not depth and "=" in st:
            out.append(st.split("=", 1)[0])
    return out


def check(label, vanilla, mine):
    if vanilla == mine:
        print("  ok    %-28s %d fields" % (label, len(vanilla)))
        return True
    print("  FAIL  %s" % label)
    missing = [f for f in vanilla if f not in mine]
    extra = [f for f in mine if f not in vanilla]
    if missing:
        print("        missing from the builder: %s" % missing)
    if extra:
        print("        not in vanilla          : %s" % extra)
    if not missing and not extra:
        print("        same fields, different order")
        print("        vanilla: %s" % vanilla)
        print("        builder: %s" % mine)
    return False


def main():
    titan = read("Levels/3 Montaillou/Titan Village.zax")
    shrine = read("Levels/7 English Shrine/02 Temple Initiate.zax")
    ok = True
    print("lhbuild trigger builders vs vanilla:")
    ok &= check("CTouchingPolygonTriggerAI",
                fields_of(part_named(titan, "Eavesdrop trigger"), "CTouchingPolygonTriggerAI"),
                fields_of(touch_poly("x", "", [0, 0, 1, 1, 0, 0], once="0"), "CTouchingPolygonTriggerAI"))
    ok &= check("CTouchingOvalTriggerAI",
                fields_of(part_named(titan, "Mathuo-Iapetus Bubble trigger"), "CTouchingOvalTriggerAI"),
                fields_of(touch_oval("x", "", 0, 0), "CTouchingOvalTriggerAI"))
    ok &= check("CAIInteractionSpecifier",
                fields_of(part_named(shrine, "To Exalted Chambers poly"), "CAIInteractionSpecifier"),
                fields_of("x=" + B(*specifier("GetCloseThenTrigger", "")), "CAIInteractionSpecifier"))

    # every touching trigger the mod ships must carry the re-arm field, whatever its value
    missing = []
    for p in sorted((Path(__file__).resolve().parent.parent / "files" / "Levels").rglob("*.zax")):
        z = p.read_bytes().decode("latin-1")
        for cls in ("CTouchingPolygonTriggerAI", "CTouchingOvalTriggerAI"):
            for m in re.finditer(r"Activity=" + cls + CR, z):
                i = z.index("{", m.end())
                d, j = 0, i
                while True:
                    if z[j] == "{":
                        d += 1
                    elif z[j] == "}":
                        d -= 1
                        if d == 0:
                            break
                    j += 1
                if "Auto-Flip Switch" not in z[m.start():j + 1]:
                    missing.append(p.name)
    if missing:
        ok = False
        print("  FAIL  shipped triggers with no Auto-Flip Switch: %s" % sorted(set(missing)))
    else:
        print("  ok    every shipped touching trigger carries Auto-Flip Switch")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
