"""Act 7's repairs, found by the 0.99.0 survey of the English Shrine.

* **The Druid Master is voiced and was never heard.** Her tree is `DruidMaste`, her ten recordings sit in `DruidMaster VOs`,
  and voice resolves as `<tree basename> VOs/<node>.ogg`. It is the only folder in the game that matches no tree. A copy under
  the tree's name gives her a voice. `vo_reach.py` now lists any folder like it.
* **The sanctum's stones all said "Two stones left."** Each switch line now ends on what it opened, and a count follows,
  kept on the player so the order the stones are pulled in does not matter.
* **Sir Roger's "That changes nothing. Stand aside." fired nothing**, inside the scene his greeting opens, so the scene never
  ended. It now fires the relay every other exit fires, which ends the scene and gives him his return-talk.
* **The second passage could pay twice.** The way back from Exalted Chambers fires the relay that opens 02's secret door, and
  the door's After Opened reads Sneak on whoever opened it. That relay now closes the two Sneak rewards first, and the reward
  relay fires it last, so the player who found the passage is still paid.

A rerun is a no-op.

    python tools/build_shrine_repairs.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balanced, deactivate, delay, multi
from build_inquisition_slides import VARS, write_var

DIALOG = "Resources/Levels/7 English Shrine/Dialog/"
SANCTUM = "Levels/7 English Shrine/10 Inner Sanctum.zax"
TEMPLE = "Levels/7 English Shrine/02 Temple Initiate.zax"
STONES_TREE = DIALOG + "The Inner Sanctum.DialogTree"
ROGER_TREE = DIALOG + "SirRoger.DialogTree"
STONES = VARS + "Fixt Sanctum Stones Pulled"
COUNT = [("6 two left", "Two stones left."), ("7 one left", "One stone left."), ("8 none left", "That was the last of them.")]


def register(rels):
    mods = FX.parent / "mod.json"
    text = mods.read_bytes().decode("utf8")
    have = set(json.loads(text)["files"])
    new = [r for r in rels if r not in have]
    if not new:
        return
    nl = "\r\n" if "\r\n" in text else "\n"
    anchor = '    "Levels/8 Alamut/01 Desert Sprawl.zax",'
    assert text.count(anchor) == 1
    mods.write_bytes(text.replace(anchor, "".join('    "' + r + '",' + nl for r in new) + anchor).encode("utf8"))


def into_relay(z, name, extra, n):
    """Prepend n actions to a relay's own action list. The first Item Count after the name is the Activity array's."""
    i = z.index("\t\t\tName=" + name + CR)
    a = z.index("Activity=CRelayAI", i)
    b = z.index("Action=CMultipleActionsAction", a)
    assert b < balanced(z, z.rindex("Level Part=", 0, i)), name
    m = re.compile(r"Item Count=(\d+)\r\n").search(z, b)
    return z[:m.start()] + "Item Count=" + str(int(m.group(1)) + n) + CR + extra + z[m.end():]


def voice():
    import zipfile
    z = zipfile.ZipFile(lhbuild.VANILLA)
    src = DIALOG + "DruidMaster VOs/"
    out = []
    for n in z.namelist():
        if n.startswith(src) and n.lower().endswith(".ogg"):
            rel = DIALOG + "DruidMaste VOs/" + n[len(src):]
            p = FX / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            if not p.exists():
                p.write_bytes(z.read(n))
            out.append(rel)
    assert len(out) == 10, len(out)
    register(out)


def stones():
    t = lhbuild.read(STONES_TREE)
    if "Node ID=6 two left" + CR in t:
        return
    for n in ("3 the north door", "4 the chests", "5 the south door"):
        k = "Node ID=" + n + CR + "Text="
        i = t.index(k) + len(k)
        e = t.index(CR, i)
        assert t[i:e].endswith(" Two stones left."), n
        t = t[:i] + t[i:e][:-len(" Two stones left.")] + t[e:]
    sep = "-" * 60
    tail = "".join(sep + CR + lhbuild.node(nid, text, []) for nid, text in COUNT)
    end = t.rindex("}")
    assert t[end:].strip() == "}"
    t = t[:end] + tail + t[end:]
    (FX / STONES_TREE).write_bytes(t.encode("latin-1"))

    z = lhbuild.read(SANCTUM)
    pulled = ("CAddCharacterModifierToCharacterAction", [
        ("Modifier Description", ""), ("Modification is permanent", "0"), ("Character to modify", "$Instigator"),
        ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
            ("Modification Amount", ("CConstant", [("Constant Value", "1")])), ("Modification amount is a percent", "0"),
            ("Allow Accumulation", "1"), ("Derived character attribute to modify", STONES)]))])),
        ("OPTIONAL Duration", ""), ("Expression Context", "$Instigator")])

    def say(node):
        return ("CDisplayDialogBalloonAction", [("Dialog Tree File", "Levels/7 English Shrine/Dialog/The Inner Sanctum"), ("Node ID", node),
                                                ("Name of Position", "$Instigator"), ("Position Offset", "0.000000,-70.000000"), ("After Action", ""), ("Include In Log", "1")])

    def at(n):
        return ("CIsEqualTo", [("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", STONES)])), ("Operator", ""),
                               ("Operand2", ("CConstant", [("Constant Value", str(n))]))])

    count = ("CIfExpressionAction", [("If Expression", at(1)), ("Character to get attributes from", "$Instigator"), ("Then", say(COUNT[0][0])),
             ("Else", ("CIfExpressionAction", [("If Expression", at(2)), ("Character to get attributes from", "$Instigator"), ("Then", say(COUNT[1][0])),
                                               ("Else", say(COUNT[2][0]))]))])
    extra = "Action=" + B(*pulled) + "Action=" + B(*delay("4", count))
    for n in ("Secret door1 relay", "Secret door2 relay", "Secret door3 relay"):
        z = into_relay(z, n, extra, 2)
    lhbuild.write_map(SANCTUM, z)
    write_var(STONES, "Fixt Sanctum Stones Pulled", "How many of the three sanctum stones the player has pulled, so the count reads right in any order.")
    register(["Resources/" + STONES + ".DerivedCharacterAttribute"])


def roger():
    t = lhbuild.read(ROGER_TREE)
    i = t.index("Node ID=60 the queens favour" + CR)
    e = t.index("-" * 60, i)
    x = "Reply Text=That changes nothing. Stand aside." + CR + "Go to node ID=" + CR
    fix = x + "Custom Action=CTriggerRelayAction" + CR + "{" + CR + "Relay Name=Sir Roger Switch Talk AI" + CR + "}" + CR
    if fix in t[i:e]:
        return
    assert t[i:e].count(x) == 1
    t = t[:i] + t[i:e].replace(x, fix, 1) + t[e:]
    (FX / ROGER_TREE).write_bytes(t.encode("latin-1"))


def passage():
    z = lhbuild.read(TEMPLE)
    i = z.index("\t\t\tName=Last secret entrance from last level trigger" + CR)
    a = z.rindex("Level Part=", 0, i)
    p = z[a:balanced(z, a)]
    if "Target Name=Fixt the second passage" in p:
        return
    shut = "Action=" + B(*deactivate("Fixt the second passage")) + "Action=" + B(*deactivate("Fixt the draught under the door"))
    z = into_relay(z, "Last secret entrance from last level trigger", shut, 2)
    # The reward relay must pay before it fires the relay that now shuts it.
    i = z.index("\t\t\tName=Fixt the second passage" + CR)
    a = z.rindex("Level Part=", 0, i)
    p = z[a:balanced(z, a)]
    fire = re.search(r"\t*Action=CTriggerRelayAction\r\n\t*\{\r\n\t*Relay Name=Last secret entrance from last level trigger\r\n\t*\}\r\n", p)
    assert fire
    body = p[:fire.start()] + p[fire.end():]
    k = body.rindex("\t\t\t\t\t\t}\r\n\t\t\t\t\t}\r\n")
    body = body[:k] + fire.group(0) + body[k:]
    z = z.replace(p, body)
    lhbuild.write_map(TEMPLE, z)


def main():
    voice()
    stones()
    roger()
    passage()
    print("shrine repaired")


if __name__ == "__main__":
    main()
