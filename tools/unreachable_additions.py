"""Which authored enchantments can a player never get?

**Membership is declared by the addition, not by the group.** A `.AdditionGroup.txt` file lists
only the *other groups* it nests; the additions themselves carry `Inventory Addition Group=`
pointing at the group they belong to. So a group file reading `Item Count=0` means "nests no
sub-groups", NOT "has no members" -- `Shield LARGE Additions` is `Item Count=0` and has twelve
members. Reading the group files alone gets this exactly backwards.

Reachability, then, is a graph walk:

    item  --Inventory Addition Group-->  group
    group --Other Group that are part of this group--> group   (transitive)
    addition --Inventory Addition Group--> group               (membership)

An addition is **generable** if its group is reachable from the group named by some inventory
item. It is additionally **grantable** if any map, can or dialogue names it directly in an
`Addition to add=` or `Additions to add=` list, which bypasses generation entirely.

`Inventory/!None` is the explicit opt-out and is not a defect: 81 additions sit there on purpose,
including this project's own test probes.

Usage: python tools/unreachable_additions.py [--verbose]
"""
import collections
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import zf, read, FX

NONE = "Inventory/!None"
GROUP_ROOT = "Inventory/Inventory Addition Groups/"


def all_files():
    return sorted(set(zf.namelist())
                  | {"Resources/" + p.relative_to(FX / "Resources").as_posix()
                     for p in (FX / "Resources").rglob("*") if p.is_file()})


def norm(path):
    """Resource references are given without the Resources/ prefix or the extension."""
    return path.strip().rstrip("\x00")


def main():
    verbose = "--verbose" in sys.argv
    files = all_files()
    adds = [n for n in files if n.endswith(".InventoryAddition")]
    groups = [n for n in files if n.endswith(".AdditionGroup.txt")]
    items = [n for n in files if n.endswith(".InventoryItem")]
    print("%d additions, %d groups, %d items" % (len(adds), len(groups), len(items)))

    # group -> groups it nests
    nests = collections.defaultdict(set)
    group_names = set()
    for n in groups:
        gname = n.split("Resources/")[-1].replace(".AdditionGroup.txt", "")
        group_names.add(gname)
        for m in re.finditer(r"Inventory Addition Group=(.+)", read(n)):
            nests[gname].add(norm(m.group(1)))

    # addition -> its group
    member_of = {}
    for n in adds:
        name = n.split("/")[-1].replace(".InventoryAddition", "")
        m = re.search(r"Inventory Addition Group=(.+)", read(n))
        member_of[n] = (name, norm(m.group(1)) if m else "(unset)")

    # groups named by real items
    roots = set()
    item_users = collections.defaultdict(list)
    for n in items:
        m = re.search(r"Inventory Addition Group=(.+)", read(n))
        if not m:
            continue
        g = norm(m.group(1))
        if g != NONE:
            roots.add(g)
            item_users[g].append(n.split("/")[-1].replace(".InventoryItem", ""))

    # transitive closure from the item-named roots
    reachable, stack = set(), list(roots)
    while stack:
        g = stack.pop()
        if g in reachable:
            continue
        reachable.add(g)
        stack.extend(nests.get(g, ()))

    # additions handed out directly, bypassing generation entirely
    granted = set()
    for n in files:
        if not n.lower().endswith((".zax", ".can", ".dialogtree", ".inventoryitem")):
            continue
        try:
            t = read(n)
        except Exception:
            continue
        for m in re.finditer(r"Addition to add=(.+)", t):
            granted.add(norm(m.group(1)).split("/")[-1])

    gen, direct, orphan, optout = [], [], [], []
    for n, (name, g) in sorted(member_of.items(), key=lambda kv: kv[1][0].lower()):
        if g == NONE:
            optout.append((name, g))
        elif g in reachable:
            gen.append((name, g))
        elif name in granted:
            direct.append((name, g))
        else:
            orphan.append((name, g))

    print("\n  generable from an item's pool : %d" % len(gen))
    print("  only granted directly         : %d" % len(direct))
    print("  explicit opt-out (!None)      : %d" % len(optout))
    print("  UNREACHABLE                   : %d" % len(orphan))

    if orphan:
        print("\n=== unreachable: authored, in a group nothing can roll, granted by nothing ===")
        by_group = collections.defaultdict(list)
        for name, g in orphan:
            by_group[g].append(name)
        for g in sorted(by_group):
            print("\n  group: %s" % g.replace(GROUP_ROOT, ""))
            print("    (named by %d items, %s)" % (
                len(item_users.get(g, [])),
                "reachable" if g in reachable else "NOT reachable from any item"))
            for name in sorted(by_group[g]):
                print("      %s%s" % (name, "   [granted directly]" if name in granted else ""))

    dead_groups = sorted(g for g in group_names if g not in reachable)
    if dead_groups:
        print("\n=== groups no item can reach (%d) ===" % len(dead_groups))
        for g in dead_groups:
            n = sum(1 for _, (_, gg) in member_of.items() if gg == g)
            print("   %-58s %d members" % (g.replace(GROUP_ROOT, ""), n))

    if verbose:
        print("\n=== every group an item names ===")
        for g in sorted(roots):
            n = sum(1 for _, (_, gg) in member_of.items() if gg == g)
            print("   %-56s %2d members, %2d items" % (
                g.replace(GROUP_ROOT, "")[:54], n, len(item_users[g])))


if __name__ == "__main__":
    main()
