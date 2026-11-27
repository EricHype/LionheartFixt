"""The Snakebreed Venom Sac is green on the ground too. Reported: "the ground model for the venom sac is still flesh
colored instead of green like the inventory icon".

`tools/build_display_name_leftovers.py` moved the sac's ground model off the Lava Troll Hide and onto the Woodsman's
Liver's (`Items/PickUps/Special Items/WoodsmanLiver_PU`), but only its inventory icon was recoloured, so on the ground it
was a red liver. The icon is the liver's with its red and green channels exchanged (docs/releases.md, "The art is two
recolours"). The ground model gets the same exchange: the liver's pickup file, recoloured in place by
`mdl16_format.recolor_icon_in_place`, which leaves every control byte, run and length as they were, saved as
`SnakebreedVenomSac_PU`, and the sac's `On the ground` points at it. The liver keeps its own.

The pickup file carries its sprite inline, a 16 x 8 RLE-16bpp frame, as `Cloak_PU` does (0.86.1).

Reach: an item records its ground model when it is made, so sacs dropped from now on. A rerun is a no-op.

    python tools/build_venom_sac_ground.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "LionheartModTools"))
import lhbuild
import mdl16_format as m
from lhbuild import CR
from build_shrine_repairs import register

LIVER = "Cache/Models/Items/PickUps/Special Items/WoodsmanLiver_PU.mdl16"
SAC_PU = "Cache/Models/Items/PickUps/Special Items/SnakebreedVenomSac_PU.mdl16"
ITEM = "Resources/Inventory/Specific Item Cans/Quest Items/Snakebreed Venom Sac.InventoryItem"
OLD = "On the ground=Items/PickUps/Special Items/WoodsmanLiver_PU" + CR
NEW = "On the ground=Items/PickUps/Special Items/SnakebreedVenomSac_PU" + CR


def swap_rg(v):
    """RGB565 with red and green exchanged, the icon's own recolour."""
    r, g, b = (v >> 11) & 31, (v >> 5) & 63, v & 31
    return ((g >> 1) << 11) | (((r << 1) | (r >> 4)) << 5) | b


def main():
    done = []
    out = lhbuild.FX / SAC_PU
    if not out.exists():
        src = lhbuild.zf.read(LIVER)
        h = m.find_header(src)
        assert h and h.flags & 6 == 4 and (h.width, h.height) == (16, 8), h
        new = m.recolor_icon_in_place(src, swap_rg)
        assert len(new) == len(src) and new != src
        m.verify_icon(new)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(new)
        done.append(SAC_PU)
    t = lhbuild.read(ITEM)
    if OLD in t:
        assert t.count(OLD) == 1
        (lhbuild.FX / ITEM).write_bytes(t.replace(OLD, NEW).encode("latin-1"))
        done.append(ITEM)
    if done:
        register(done)
    print("venom sac ground:", done)


if __name__ == "__main__":
    main()
