"""Companions report exact numbers, and say what each level-up gave them. Requested after 0.99.20: "I am not sure if
Fernand is levelling up, when I ask him his condition, the numbers don't seem to be different from base level."

He was. Every save from level 6 to level 7 shows +9 HP, +8 AC and +3 one-handed skill on his record, exactly the growth
grant. The report hid it: health came in bands of 10 and skill in bands of 10 (+3 a level stays in one band for three
levels), and armour, the stat that grows most, was not reported at all.

**A. Exact numbers on demand.** No script action can print a number. Settled in the exe: `CPrintCombatTextAction`'s
execute (0x586c40) passes a pointer to its own `Text to print` straight to the combat log writer (0x584c40 ->
0x585a80 -> 0x585eb0 -> 0x586080), which only word-wraps to the dialog font and splits on newlines. The `%s[Name]`
formatter the combat log uses is a separate object whose values the engine's C++ fills in; nothing in the action's path
calls it. So every value is written out as its own fixed line, and the script picks one by halving the range: nine or
ten comparisons per lookup.

The lookups live in four cans under `Fixt Companion Report/`, called from the reply with `CUseCannedActionAction`.
That is safe for `$Trigger`: the action's execute (0x4f8160) loads the can once, caches it, and calls the canned
action's own execute (vtable +0x74, through 0x41e6b0) with the same four context arguments it was given. So
`Character to get attributes from=$Trigger` inside the can is the companion that was clicked, as it is in the reply.

* `Health at full strength: N.`  (HP) Hit Points, the computed maximum (0.8x established this from the healing potion)
* `Armor class: N.`              (AC) Armor Class, the game's own name for it
* `Fighting skill: N.`           best of one-handed, two-handed and ranged, as before
* `Celestial Smite: N.`          only when it is above zero, because Diego and Darsh grow it instead of fighting skill

Fractions (health uses Endurance / 3) print the whole number below. The top line of each says "or more".

**B. The level-up says what it gave.** The growth watcher on Player1 is saved INLINE in a save, so editing
`Fixt Companion Growth Install` would never reach a game where it is already armed. But the balloon it shows is named by
reference, `Dialog Tree File=Levels/Fixt Companion Growth` and `Node ID=<companion>`, and that tree loads from data.dat.
So the gains go on the end of each companion's balloon line, in the game's own <narration> brackets, and reach every
save. `Include In Log=1` puts the line in the combat log too, so it survives the balloon fading. The amounts are read
from the installer, never typed here.

A rerun is a no-op.

    python tools/build_companion_report.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register

TREE = "Resources/Levels/Generic Companion Dialog.DialogTree"
GROWTH_TREE = "Resources/Levels/Fixt Companion Growth.DialogTree"
INSTALL = "Resources/Common Objects and Scripts/Fixt Companion Growth Install.can"
DIR = "Common Objects and Scripts/Fixt Companion Report/"
REPLY = "Reply Text=How are you holding up?" + CR


def attr(name):
    return ("CVariableDerivedCharacterAttribute", [("Character Attribute", "Derived Character Attributes/" + name)])


def skill(name):
    return ("CVariableSkill", [("Skill", "Skills/" + name)])


BEST_FIGHTING = ("CExpressionAggregateFunctionMax", [("Parameters", [("Parameter", skill("Fighting/OneHandedMelee")),
                                                                      ("Parameter", skill("Fighting/TwoHandedMelee")),
                                                                      ("Parameter", skill("Fighting/Ranged"))])])
SMITE = skill("Magic Divine/Offensive/Celestial Smite")

# can name, the expression read off $Trigger, the line's label, the lowest and highest exact values
REPORTS = [
    ("Health", attr("(HP) Hit Points"), "Health at full strength", 0, 500),
    ("Armor", attr("(AC) Armor Class"), "Armor class", 0, 500),
    ("Fighting Skill", BEST_FIGHTING, "Fighting skill", 0, 300),
    ("Celestial Smite", SMITE, "Celestial Smite", 1, 300),
]


def say(text):
    return ("CPrintCombatTextAction", [("Text to print", text), ("Character to show text to", "$Instigator"),
                                       ("Emphasize", "0"), ("Suppress Duplicates", "0")])


def below(expr, n, then, els):
    return ("CIfExpressionAction", [
        ("If Expression", ("CIsLessThan", [("Operand1", expr), ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", str(n))]))])),
        ("Character to get attributes from", "$Trigger"), ("Then", then), ("Else", els)])


def lookup(expr, label, lo, hi):
    """Exact value lo..hi. Leaf v covers [v, v+1); the bottom leaf also covers anything lower, the top anything higher."""
    def node(a, b):
        if a == b:
            return say(label + ": " + str(a) + (" or more." if a == hi else "."))
        mid = (a + b + 1) // 2
        return below(expr, mid, node(a, mid - 1), node(mid, b))
    return node(lo, hi)


def can_text(action):
    return "CCannedObject" + CR + "{" + CR + "Object=" + B(*action) + "Use=Shared Global Instance" + CR + "}" + CR


def build_cans():
    made = 0
    for name, expr, label, lo, hi in REPORTS:
        rel = "Resources/" + DIR + name + ".can"
        if (lhbuild.FX / rel).exists():
            continue
        act = lookup(expr, label, lo, hi)
        if lo > 0:   # a skill this companion lacks prints nothing, rather than a line about a spell they cannot cast
            act = below(expr, lo, "", act)
        lhbuild.write_map(rel, can_text(act))
        register([rel])
        made += 1
    return made


def top_actions(t, start):
    """[(start, end)] of every Action= directly inside the Array whose '{' follows `start`."""
    a = t.index("{", start)
    end = lhbuild.balanced(t, a)
    out, j = [], a + 1
    while True:
        k = t.find(CR + "Action=", j, end)
        if k < 0:
            return out
        s = k + len(CR)
        e = lhbuild.balanced(t, s)
        out.append((s, e + len(CR)))
        j = e


def call(name):
    return "Action=" + B("CUseCannedActionAction", [("Canned Object", DIR + name)])


def build_report():
    t = lhbuild.read(TREE)
    if DIR + "Health" in t:
        return 0
    r = t.index(REPLY)
    arr = t.index("Action=Array", r)
    acts = top_actions(t, arr)
    count = re.compile(r"Item Count=(\d+)\r\n").search(t, arr)
    assert int(count.group(1)) == len(acts), (count.group(1), len(acts))
    health = [x for x in acts if "Text to print=Health at full strength" in t[x[0]:x[1]]]
    fight = [x for x in acts if "Text to print=Fighting skill" in t[x[0]:x[1]]]
    assert health and fight and len(health) + len(fight) < len(acts)
    for group in (health, fight):   # each group is one contiguous run, so one call can stand in for it
        assert acts[acts.index(group[0]):acts.index(group[-1]) + 1] == group
    out, n = [], 0
    pos = acts[0][0]
    for s, e in acts:
        if (s, e) == health[0]:
            out.append(call("Health") + call("Armor")); n += 2
        elif (s, e) == fight[0]:
            out.append(call("Fighting Skill") + call("Celestial Smite")); n += 2
        elif (s, e) in health or (s, e) in fight:
            continue
        else:
            out.append(t[s:e]); n += 1
    body = "".join(out)
    t = t[:count.start()] + "Item Count=" + str(n) + CR + t[count.end():pos] + body + t[acts[-1][1]:]
    (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
    register([TREE])
    return 1


def gains():
    """{balloon node: '+9 health, +8 armor, +3 fighting skill'} read from the installer itself."""
    t = lhbuild.read(INSTALL)
    words = {"(HP) Hit Points": "health", "(AC) Armor Class": "armor", "Fighting/OneHandedMelee": "fighting skill",
             "Magic Divine/Offensive/Celestial Smite": "Celestial Smite"}
    out = {}
    for m in re.finditer(r"Modifier Description=Fixt companion growth\r\n(.*?)Node ID=([^\r\n]+)", t, re.S):
        body, node = m.group(1), m.group(2)
        vals = re.findall(r"Constant Value=([\d.]+)\s*\}\s*Modification amount is a percent=0\s*Allow Accumulation=1\s*"
                          r"(?:Derived character attribute to modify=Derived Character Attributes/|Skill to modify=Skills/)([^\r\n]+)", body)
        assert len(vals) == 3, (node, vals)
        line = ", ".join("+" + v + " " + words[k] for v, k in vals)
        assert out.get(node, line) == line, node   # Cortes and Cortes with arm share one node and must agree
        out[node] = line
    return out


def build_balloons():
    t = lhbuild.read(GROWTH_TREE)
    if "<+" in t:
        return 0
    g = gains()
    nodes = re.findall(r"Node ID=([^\r\n]+)\r\nText=([^\r\n]*)\r\n", t)
    assert sorted(n for n, _ in nodes) == sorted(g), (sorted(n for n, _ in nodes), sorted(g))
    for nid, text in nodes:
        old = "Node ID=" + nid + CR + "Text=" + text + CR
        assert t.count(old) == 1, nid
        t = t.replace(old, "Node ID=" + nid + CR + "Text=" + text + " <" + g[nid] + ">" + CR)
    (lhbuild.FX / GROWTH_TREE).write_bytes(t.encode("latin-1"))
    register([GROWTH_TREE])
    return len(nodes)


def main():
    print("lookup cans:", build_cans(), "| report:", build_report(), "| balloons:", build_balloons())


if __name__ == "__main__":
    main()
