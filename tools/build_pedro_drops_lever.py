"""Pedro drops the switch lever when he dies, unless he has already given it to you.

The lever (`Rod Switch working Calle Top Island`) works the switch on La Calle Perdida's northern island, whose rock
becomes the bridge to the Lost Soul. Pedro is its only source: once you have tried the switch empty-handed he answers
"Have you found a small lever around here?" (`50 Small lever found`). He spawns as a `Wielder`, and Relican's takeover
turns every Wielder hostile, so a character who used the ring first could never get it. Attacking any wizard makes
them all hostile too.

Vanilla's own shape for this, the Herbalist dropping Quinn's amulet: the spawn's destroyed script is an `if not
<checker>` around a `CGenerateInventoryItemAction` at `$Trigger`. Here Pedro's generator `After Action` sets it (the
Wizard Can's own destroyed script slot is empty, so nothing is overridden), and the reply that hands the lever over
also activates the new checker `pedro gave you the lever`.

Map-side: reaches a character who has not yet entered La Calle Perdida. A rerun is a no-op.

    python tools/build_pedro_drops_lever.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, activate, checker, exists, generate_item, if_action
from build_shrine_repairs import register

MAP = "Levels/1 Barcelona/Calle Perdida.zax"
TREE = "Resources/Levels/1 Barcelona/Dialog/La Calle Perdida/Pedro.DialogTree"
ROD = "Inventory/Specific Item Cans/Quest Items/Rod Switch working Calle Top Island"
GAVE = "pedro gave you the lever"


def build_map():
    t = lhbuild.read(MAP)
    if "Name To Check For=" + GAVE in t:
        return False
    i = t.index("\t\t\tName=Pedro Generator" + CR)
    end = t.index("\t\tLevel Part=", i)
    a = t.index("After Action=CMultipleActionsAction", i, end)
    s = t.index("CMultipleActionsAction", a)
    arr = t.index("Action=Array", s) + len("Action=")
    arr_end = lhbuild.balanced(t, arr)
    assert arr_end < end and "Relay Name=Gives XtraPain to Cedric n Pedro" in t[arr:arr_end]
    count = "Item Count=3" + CR
    k = t.index("Item Count=", arr)
    assert t.startswith(count, k), "%s: Pedro's After Action is not the vanilla three" % MAP
    close = t.rindex(CR, 0, arr_end - 1) + len(CR)  # start of the array's closing-brace line
    drop = ("CSetDestroyedScriptActionAction", [("New Destroyed Action", if_action(("CNotAction", [("Action", exists(GAVE))]),
                                                                                   generate_item(ROD, "$Trigger", "128"))),
                                                ("Target Name", "$Instigator")])
    t = t[:close] + "Action=" + B(*drop) + t[close:]
    t = t[:k] + "Item Count=4" + CR + t[k + len(count):]
    t = lhbuild.add_parts(t, [checker(GAVE, 1380, 1213)])
    lhbuild.write_map(MAP, t)
    return True


def build_tree():
    p = lhbuild.FX / TREE
    t = lhbuild.read(TREE)
    if "Target Name=" + GAVE in t:
        return False
    n = t.index("Node ID=50 Small lever found" + CR)
    old = "Item Count=2" + CR + "Action=CActionGiveStandardInventoryItem" + CR
    k = t.index(old, n)
    assert "Inventory Item To Give=" + ROD in t[k:k + 400]
    t = t[:k] + "Item Count=3" + CR + "Action=" + B(*activate(GAVE)) + t[k + len("Item Count=2" + CR):]
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(t.encode("latin-1"))
    return True


def main():
    changed = [build_map(), build_tree()]
    if any(changed):
        register([MAP, TREE])
    print("pedro drops the lever:", changed)


if __name__ == "__main__":
    main()
