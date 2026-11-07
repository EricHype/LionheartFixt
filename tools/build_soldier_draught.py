"""Turn the English soldiers' healing draught into something the player can see and stop. Found in play: a heal that fires
inside the hit that triggers it has no animation and no counter, so it is only more HP to chew through.

At 40% health he now stops, plays his fidget for three seconds and heals at the end of it. Any damage in that window spills
may spill the draught (SPILL percent a hit, because you usually keep hitting the man you were already hitting, and a
certain spill made the window meaningless), and then he goes straight back to fighting. Either way he has only the one: the existing one-shot series still
holds it. The models have no drink or cast sequence, so the fidget stands in, sped up to fit (bow 8.0s, sword 4.33s,
mace 3.0s, read from the GR2s).

CAssignTemporaryTaskAction (55 vanilla uses) pauses CSkeletonAI for a CPlaySequenceOnceAI and runs its Stop Action when the
sequence ends. The heal lives there rather than in a CDelayAction, so it dies with him and cannot reach a corpse. Scripted
Custom 2 is the per-creature flag; vanilla sets it on the player, and a soldier holds it only for those three seconds.

A rerun is a no-op.

    python tools/build_soldier_draught.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, FX, if_action, multi

CANS = FX / "Resources/Monster Cans/English Enemies"
FLAG = "Scripted Custom 2"
WINDOW = 3.0
SPILL = "40"
EFFECT = "Spell Effects/Hits and Effects/Target Affected/Divine Strength"


def fidget(can):
    if "Bow" in can:
        return "FidgetBow", 8.0
    if "Mace" in can:
        return "FidgetMace", 3.0
    return "Fidget", 4.33


def health(cmp, value):
    return ("CExpressionAction", [
        ("Expression", (cmp, [("Operand1", ("CExpressionHealthPercent", [])), ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", value)]))])),
        ("Character to get attributes from", "$Trigger")])


def say(text):
    return ("CPrintCombatTextAction", [("Text to print", text), ("Character to show text to", "Player1"), ("Emphasize", "0"), ("Suppress Duplicates", "0")])


def flagged():
    return ("CCheckCategoryAction", [("Target Name", "$Trigger"), ("Category to check for", FLAG)])


def unflag():
    return ("CRemoveCategoryAction", [("Target Name", "$Trigger"), ("Categories To Remove", FLAG)])


def done():
    return ("CSendAIDoneMessage", [("Target", "$Trigger")])


def heal(text):
    amount = ("CMultiply", [
        ("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", "Derived Character Attributes/(HP) Hit Points")])),
        ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", "0.35")]))])
    return multi([
        unflag(),
        ("CGiveHealthToCharacterAction", [("Character to give health to", "$Trigger"), ("Amount of health to give", amount), ("Expression Context", "$Trigger")]),
        say(text),
        ("CSpawnEffectAction", [("Explosion Model", EFFECT), ("Location Entity", "$Trigger"), ("Make effect a child of the location entity", "0"),
                                ("X Offset", "0"), ("Y Offset", "0"), ("Height Offset", "35"), ("Play Default Sound", "1")])])


def task(can, text):
    seq, length = fidget(can)
    speed = f"{length / WINDOW:.2f}"
    behavior = ("CEntityBehaviorPlaySequenceOnce", [
        ("Sequence", seq), ("Speed To Play", speed), ("Done Sequence", "Idle"), ("Done Frame", "0"), ("Was Stationary", "0"), ("Old Play Ratio", "0"),
        ("Move With Sequence", "0"), ("After Action", ""), ("Cur Speed To Play", speed)])
    ai = ("CPlaySequenceOnceAI", [
        ("Marked For Deletion", "0"), ("Publisher", ""), ("Behavior", behavior),
        ("Stop Action", multi([if_action(flagged(), heal(text)), done()])),
        ("Execute Action Only Once", "1"), ("Stop Action Executed", "0")])
    return ("CAssignTemporaryTaskAction", [
        ("Target", "$Trigger"), ("Temporary Task AI", ai), ("Original AI Type", "CSkeletonAI"),
        ("Completion Message to wait for", "AI Done"), ("Suppress can't assign error", "1")])


def script(can, name, text):
    start = multi([
        ("CAddCategoryAction", [("Target Name", "$Trigger"), ("Categories to add", FLAG)]),
        say(name + " reaches for a healing draught."),
        task(can, text)])
    once = ("CSeriesAction", [
        ("Action", [("Action", start), ("Action", ("CSucceedAction", [("Action", "")]))]),
        ("When Done", "Repeat Last Action"), ("Require Success To Advance", "1"), ("Next Action Index", "0")])
    # The killing blow fires this slot too, and a sequence played on him then would stand the corpse back up.
    wounded = if_action(health("CIsLessThanOrEqual", "40"), if_action(health("CIsGreaterThan", "0"), once))
    spilled = multi([unflag(), say(name + " is struck and spills the draught."), done()])
    roll = ("CExpressionAction", [
        ("Expression", ("CIsLessThan", [
            ("Operand1", ("CRandom", [("Operator", ""), ("Minimum", ("CConstant", [("Constant Value", "0")])), ("Maximum", ("CConstant", [("Constant Value", "100")]))])),
            ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", SPILL)]))])),
        ("Character to get attributes from", "$Trigger")])
    return if_action(flagged(), if_action(roll, spilled, say(name + " takes the blow and keeps drinking.")), wounded)


def main():
    done_ = 0
    for f in sorted(CANS.glob("*.can")):
        rel = f.relative_to(FX).as_posix()
        z = lhbuild.read(rel)
        k = z.find("Damaged Script Action=CIfAction")
        if k < 0:
            continue
        e = lhbuild.balanced(z, k)
        old = z[k:e]
        if "CGiveHealthToCharacterAction" not in old or "CRandom" in old:
            continue
        name = re.search(r"User Assigned Name=([^\r\n]*)", z).group(1)
        text = re.search(r"Text to print=([^\r\n]*drinks[^\r\n]*)", old).group(1)
        c = script(f.name, name, text)
        new = "Damaged Script Action=" + B(c[0], c[1]).rstrip()
        lhbuild.write_map(rel, z[:k] + new + z[e:])
        done_ += 1
    print(done_, "cans")


if __name__ == "__main__":
    main()
