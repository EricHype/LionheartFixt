"""Names and a ground model left over from the cans they were cloned from.

Asked: after the Wasp Queen ("still called cursed wasp in the quick status"), "fix the others", and "the ground sprite
for the poison sac from the snakebreed is the lava troll hide, can we use the one for the liver instead?"

  * `Fixt Butu Heir` is Hrargrub (his generator's `New Name` in `Ravine Cave East.zax`, his own dialogue), but displayed
    as `Goblin Striker`, the hat goblin he was copied from. He now displays `Hrargrub`.
  * `Fixt Butu Officer` leads Butu's warbands and displayed `Goblin Striker` too. It now displays `Butu War Leader`, after
    0.99.7's `Goblin War Leader` for the Horde's.
  * `Snakebreed Venom Sac` (0.76.0) lay on the ground as the Lava Troll Hide. It now uses the Woodsman Liver's model,
    `WoodsmanLiver_PU`.

Can edits reach creatures spawned after install (a `Ravine Cave East` not yet entered). The sac's model reaches every
sac dropped after install; one already lying on the ground or carried keeps the old one. A rerun is a no-op.

    python tools/build_display_name_leftovers.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR

EDITS = [
    ("Resources/Monster Cans/Fixt Butu Heir.can", "User Assigned Name=Goblin Striker", "User Assigned Name=Hrargrub"),
    ("Resources/Monster Cans/Fixt Butu Officer.can", "User Assigned Name=Goblin Striker", "User Assigned Name=Butu War Leader"),
    ("Resources/Inventory/Specific Item Cans/Quest Items/Snakebreed Venom Sac.InventoryItem",
     "On the ground=Items/PickUps/Special Items/LavaTrollHide_PU", "On the ground=Items/PickUps/Special Items/WoodsmanLiver_PU"),
]


def main():
    done = []
    for rel, old, new in EDITS:
        t = lhbuild.read(rel)
        if new + CR in t:
            continue
        assert t.count(old + CR) == 1, rel
        (lhbuild.FX / rel).write_bytes(t.replace(old + CR, new + CR).encode("latin-1"))
        done.append(rel)
    print("display name leftovers:", done)


if __name__ == "__main__":
    main()
