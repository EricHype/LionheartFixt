"""The druid priests hold the English in the two Barcelona sieges. Release 5 of the post-0.99 plan.

The Crossroads standard and the Shrine already say it: the English army is held by druid magic, and breaking it wakes the
men. The sieges of the Gate and Temple Districts had druid priests in generators of their own beside nameless soldier
generators, and no script waits on the English being dead, so a stand-down cannot block either map.

The Shrine's machinery does it, with each siege's own names so that no vanilla script starts reaching these men: while any
druid of a siege lives, its soldiers fight; when the last falls they stand down, say a waking line, and can be talked to;
hit one and the whole siege turns again. The lines are the Crossroads standard's, because these men wake in Spain, not under
an English hill. No Karma: they were fighting you.

A rerun is a no-op.

    python tools/build_siege_hold.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR
import build_shrine_druids as druids
from build_shrine_repairs import register

SIEGES = {"Levels/6 Barcelona Attack/Gate District Siege.zax": "Gate Siege",
          "Levels/6 Barcelona Attack/Temple District Siege.zax": "Temple Siege"}
WOKEN_TREE = "Levels/6 Barcelona Attack/Dialog/Fixt The Standard"
WOKEN = ["80 woke 1", "81 woke 2", "82 woke 3", "83 woke 4", "84 woke 5", "85 woke 6", "86 woke 7", "87 woke 8"]


def parts(z):
    return re.findall(r"(?ms)^\t\tLevel Part=\w+\r\n\t\t\{\r\n.*?^\t\t\}", z)


def build(rel, room):
    z = lhbuild.read(rel)
    if "Name=Fixt " + room + " druid watch" + CR in z:
        return 0, 0
    new = z
    men = posts = 0
    for x in parts(z):
        if "CGeneratorAI" not in x:
            continue
        full = re.findall(r"Entity=([^\r\n]*)", x)
        nn = re.search(r"New Name=([^\r\n]*)", x)
        if not full or not nn or nn.group(1):
            continue
        if all("English Enemies/Priest" in e for e in full):
            new = new.replace(x, re.sub(r"New Name=\r\n", "New Name=" + room + " Druid" + CR, x, count=1))
            posts += 1
        elif all("English Enemies/Soldier" in e for e in full):
            new = new.replace(x, re.sub(r"New Name=\r\n", "New Name=" + room + " Soldier" + CR, x, count=1))
            men += 1
    if not posts or not men:
        return 0, 0
    druids.TREE, druids.NODES = WOKEN_TREE, WOKEN
    gens = [x for x in parts(new) if "New Name=" + room + " Soldier" + CR in x]
    px, py = druids.pos(gens[0])
    new = lhbuild.add_parts(new, druids.watcher(room, px, py + 60))
    lhbuild.write_map(rel, new)
    register([rel])
    return men, posts


def main():
    for rel, room in SIEGES.items():
        men, posts = build(rel, room)
        print(rel.split("/")[-1], men, "soldier generators held by", posts, "druid generators")


if __name__ == "__main__":
    main()
