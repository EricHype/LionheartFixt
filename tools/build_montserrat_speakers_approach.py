"""The Grove sentry and Sahar walk out to meet you before they speak. Reported: "the gate guard at the abbey and sahar are
not able to be seen, they are at the very edge of visible space for my character, so low perception or helmeted
players will not know who is talking to them. Can they walk toward the player before speaking?"

Both scenes open from a touch poly whose speaker is spawned at its middle: `gate parley poly` (600 x 500, `Grove
Sentry Generator`) in `01 Grove Exterior` and `sahar approach poly` (460 x 440, `Sahar Generator`) in `02 Druid Council
Level2`. The dialogue opened 0.8 s after the spawn, with the speaker 220 to 300 units off, at the edge of the screen.

  * **Four corners, not one box.** Each poly is replaced by its four quarters, split at the generator and keeping the
    poly's name, so the Escort Arrival's `CDeactivateAction` by name still turns Sahar's off. A shared checker (`Fixt
    sentry met`, `Fixt sahar met`) lets only the first quarter touched run the scene.
  * **The speaker walks.** The quarter's copy of the poly's own enter action is unchanged but for its delayed
    dialogue: the speaker is first sent, by Darsh's own walk-off task (`Darsh Leaves for Good`, the `CGoToAI` the
    retreat builder already reuses), to a marker halfway to that quarter's corner, and the dialogue opens in its `Done
    action`. The player there is `Player1`, as vanilla's Slave Pits drunk guard has it, since `$Instigator` is the
    walker in a task's done slot. If the walk fails, both speakers still talk on a click.
  * **Sahar's stage direction.** `1 too late` opened *"<She does not rise from the reliquary's step...>"*; she now
    comes down off it.

Map edits: a Grove Exterior or Level 2 not yet entered. The tree line reaches every save. A rerun is a no-op.

    python tools/build_montserrat_speakers_approach.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, balanced, if_action, multi, activate
from build_shrine_repairs import register

D = "Levels/2 Montserrat/"
GROVE = D + "01 Grove Exterior.zax"
SITES = [
    # map, poly, generator, speaker, checker, marker stem
    (GROVE, "gate parley poly", "Grove Sentry Generator", "Grove Sentry", "Fixt sentry met", "Fixt sentry meets you"),
    (D + "02 Druid Council Level2.zax", "sahar approach poly", "Sahar Generator", "Sahar", "Fixt sahar met", "Fixt sahar meets you"),
]
TREE = "Resources/Levels/2 Montserrat/Dialog/Sahar.DialogTree"
OLD = ("Text=<She does not rise from the reliquary's step. Two of the creatures coil at her feet; a third, older, "
       "stands behind her with its hands folded.>")
NEW = ("Text=<She comes down off the reliquary's step to meet you. Behind her two of the creatures coil on the stair; a "
       "third, older, stands with its hands folded.>")
assert "—" not in NEW and "--" not in NEW


def part_span(z, name):
    i = z.index("\t\t\tName=" + name + CR)
    s = z.rindex(CR + "\t\tLevel Part=", 0, i) + len(CR)
    return s, balanced(z, s)


def field(p, k):
    return re.search(r"\n\t\t\t" + k + r"=([^\r]*)", p).group(1)


def darsh_walk():
    z = lhbuild.read(GROVE)
    i = z.index("\t\t\tName=Darsh Leaves for Good" + CR)
    s = z.index("Action=CAssignTemporaryTaskAction", i)
    return z[s + len("Action="):balanced(z, s)]


def walk(template, speaker, dest, dialog):
    t = re.sub(r"(\n\s*)Target=Darsh\r", lambda m: m.group(1) + "Target=" + speaker + CR, template)
    t = t.replace("Destination=Companion goto spot for deletion", "Destination=" + dest)
    a = t.index("Done action=CDeleteAction")
    done = multi([("CSendAIDoneMessage", [("Target", "$Trigger")]), dialog])
    t = t[:a] + "Done action=" + B(*done).rstrip(CR) + t[balanced(t, a):]
    t = t.replace("Suppress can't assign error=0", "Suppress can't assign error=1")
    assert t.count("Sequence=Run" + CR) == 1
    t = t.replace("Sequence=Run" + CR, "Sequence=Walk" + CR)  # a speaker coming to meet you, not fleeing
    assert "Darsh" not in t and "Destination=" + dest in t and "Original AI Type=CSkeletonAI" in t
    return t


def walking_enter(enter, template, speaker, dest):
    """The poly's enter action, its delayed dialogue now opened by the speaker's arrival."""
    d = enter.index("CDisplayDialogTreeAction")
    n = enter.rindex("Next Action=", 0, d)
    assert "CDelayAction" in enter[enter.rindex("CDelayAction", 0, n) - 20:n]
    v = n + len("Next Action=")
    e = balanced(enter, v)
    dialog = enter[v:e].replace("Player Being Spoken To=$Instigator", "Player Being Spoken To=Player1")
    assert "$Instigator" not in dialog and "Speaker=" + speaker in dialog, dialog[:300]
    return enter[:v] + walk(template, speaker, dest, dialog) + enter[e:]


def build_map(rel, poly, gen, speaker, met, stem, template):
    z = lhbuild.read(rel)
    if "\t\t\tName=" + met + CR in z:
        return []
    gs, ge = part_span(z, gen)
    gx, gy = (round(float(field(z[gs:ge], k))) for k in ("Position X", "Position Y"))
    s, e = part_span(z, poly)
    p = z[s:e]
    assert z.count("\t\t\tName=" + poly + CR) == 1
    pts = [int(v) for v in field(p, "Polygon").split(",")]
    xs, ys = pts[0::2], pts[1::2]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    assert len(pts) == 10 and x0 < gx < x1 and y0 < gy < y1, (pts, gx, gy)
    a = p.index("Enter Action=") + len("Enter Action=")
    enter = p[a:balanced(p, a)]
    parts = [lhbuild.checker(met, gx, gy - 60)]
    for tag, cx, cy in (("NW", x0, y0), ("NE", x1, y0), ("SE", x1, y1), ("SW", x0, y1)):
        dest = stem + " " + tag
        mx, my = (gx + cx) // 2, (gy + cy) // 2
        parts.append(lhbuild.marker(dest, mx, my))
        act = if_action(("CNotAction", [("Action", lhbuild.exists(met))]),
                        multi([activate(met), walking_enter(enter, template, speaker, dest)]))
        quarter = [min(gx, cx), min(gy, cy), max(gx, cx), max(gy, cy)]
        qx0, qy0, qx1, qy1 = quarter
        parts.append(lhbuild.touch_poly(poly, act, [qx0, qy0, qx1, qy0, qx1, qy1, qx0, qy1, qx0, qy0]))
    z = z[:s] + z[e + len(CR):]
    z = lhbuild.add_parts(z, parts)
    lhbuild.write_map(rel, z)
    return [rel]


def build_tree():
    t = lhbuild.read(TREE)
    if NEW in t:
        return []
    assert t.count(OLD) == 1
    (lhbuild.FX / TREE).write_bytes(t.replace(OLD, NEW).encode("latin-1"))
    return [TREE]


def main():
    template = darsh_walk()
    done = []
    for site in SITES:
        done += build_map(*site, template)
    done += build_tree()
    if done:
        register(done)
    print("montserrat speakers approach:", done)


if __name__ == "__main__":
    main()
