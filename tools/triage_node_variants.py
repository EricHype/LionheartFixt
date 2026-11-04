"""Rank check_node_variants' findings by what the unreachable node actually does.

The survey reports ~275 destinations that some variant of a greeting cannot reach. Most are
harmless -- a gendered goodbye, an insult only the hostile opening offers. The ones that matter
are the Farshad shape: a variant cut off from something the player is *given*.

So each unreachable destination is classified by what its node contains, and the output is
ordered worst first. Text-only nodes are counted and not listed.

Usage: python tools/triage_node_variants.py [--all]
"""
import collections
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lhbuild
from lhbuild import read, FX
import check_node_variants as cnv

# worst first; the first pattern that matches wins
KINDS = [
    ("GIVES AN ITEM", r"CActionGiveStandardInventoryItem|CGenerateInventoryItemAction"),
    ("GRANTS A SKILL OR ATTRIBUTE", r"CAddCharacterModifierToCharacterAction"),
    ("ASSIGNS A FACTION", r"CAssignFactionToCharacterAction"),
    ("GIVES XP", r"CGiveExperiencePointsToAllPlayersAction|Experience Points To Add"),
    ("GIVES OR TAKES MONEY", r"CGiveMoneyToAllPlayersAction|CTakeMoneyAction"),
    ("COMPLETES A QUEST", r"CSetQuestSatusToCompletedAction"),
    ("ADVANCES A QUEST", r"CActivateQuestStateAction"),
    ("MAKES A COMPANION", r"CSetCompanionAction"),
    ("OPENS A MERCHANT", r"CDisplayMerchantWindowAction"),
    ("FIRES A RELAY", r"CTriggerRelayAction"),
]


def classify(block):
    for name, pat in KINDS:
        if re.search(pat, block):
            return name
    return None


def node_blocks(text):
    out = {}
    for b in cnv.SEP.split(text.replace("\r\n", "\n")):
        m = re.match(r"\s*Node ID=(.+)", b)
        if m:
            out[m.group(1).strip()] = b
    return out


def main():
    everything = "--all" in sys.argv
    files = cnv.all_files()
    fixt = {("Resources/" + p.relative_to(FX / "Resources").as_posix())
            for p in (FX / "Resources").rglob("*") if p.is_file()}
    groups = cnv.selections(files)

    found = collections.defaultdict(list)
    plain = 0
    for (tree, nodes), maps in groups.items():
        rel = "Resources/" + tree + ".DialogTree"
        if rel not in files or (not everything and rel not in fixt):
            continue
        try:
            text = read(rel)
        except Exception:
            continue
        dests = cnv.tree_nodes(text)
        blocks = node_blocks(text)
        present = {n: dests.get(n) for n in nodes if n in dests}
        if len(present) < 2:
            continue
        union = set()
        for d in present.values():
            union |= set(d)
        for variant, d in present.items():
            for miss in sorted(union - set(d)):
                kind = classify(blocks.get(miss, ""))
                if kind is None:
                    plain += 1
                    continue
                found[kind].append((tree, variant, miss, sorted(maps)))

    order = [k for k, _ in KINDS]
    total = sum(len(v) for v in found.values())
    print("%d unreachable destinations DO something; %d are text only\n" % (total, plain))
    for kind in order:
        rows = found.get(kind)
        if not rows:
            continue
        print("=" * 78)
        print("%s  (%d)" % (kind, len(rows)))
        for tree, variant, miss, maps in sorted(rows):
            print("   %s" % tree.split("/Dialog/")[-1])
            print("      %-38s cannot reach  %s" % (variant[:38], miss))
    print()
    print("Text-only misses are not listed: a gendered goodbye or an insult only the hostile")
    print("opening offers is drift, not a defect. Judge the ones above by hand.")


if __name__ == "__main__":
    main()
