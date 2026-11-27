"""Relican's undead guards fetch him. Reported: "in my playthrough I cannot talk to relican again (we have already fixed
this) is there a way around it?"

`tools/build_relican_after_montserrat.py` fixed his click, but the click lives on the spawned `Relican`, and a save that
has already entered La Calle Perdida keeps vanilla's: once the Crown quest has been activated it shows `40 dark wielder
task 4` as a balloon over `Lord Relican`, a name nothing has, so nothing happens. That save loses `5 Return Dialogue` and
everything Fixt hangs off it (the Montserrat report and Sir Tomas's journal from 0.99.41, Leonardo, the Sceptre shell).

Dialogue trees reach every save, and the undead in the street have their own: `Undead Guards Can` ("Yes, dark master?")
and `UndeadLackey` ("How may I serve you, master?"). Both greetings gain *"Summon your master. I would speak with Lord
Relican."* The reply closes the guard's conversation and sends Relican to you:

  * **The walk.** Darsh's walk-off task (`Darsh Leaves for Good`, the `CGoToAI` the Montserrat speakers reuse), aimed at
    `Player1` with a 90-unit offset so he stops in front of you, at a walk. Its `Done action` opens `5 Return Dialogue`.
  * **The fallback.** A walk stuck on scenery would leave him silent, so after 15 s the dialogue opens anyway and the task
    is released. A tree cannot place a checker, so "only one of the two opens it" is two counters on the player: each
    summons adds one to `Fixt Relican Summoned`, each opening adds one to `Fixt Relican Came`, and an opening needs
    Summoned > Came. A second summons works the same way.
  * **The gate.** The Crown quest ever activated (when the click broke), `Relican` present, and `Has talked to Lord
    Relican already` present. That checker is only in `Calle Perdida.zax`, so the endgame maps that reuse both trees
    never show the reply.

Trees and two new variables, so every save. A rerun is a no-op.

    python tools/build_relican_summoned.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, balanced, if_action, multi
from build_shrine_repairs import register
from build_montserrat_speakers_approach import darsh_walk
from build_sahar_road_north import cand, CROWN

DLG = "Resources/Levels/1 Barcelona/Dialog/La Calle Perdida/"
TREES = {DLG + "Undead Guards Can.DialogTree": "I need nothing from you. Goodbye.",
         DLG + "UndeadLackey.DialogTree": "I need nothing from you. Goodbye."}
RELICAN_TREE = "Levels/1 Barcelona/Dialog/La Calle Perdida/Lord Relican"
SPEAKER = "Relican"
CALLE_ONLY = "Has talked to Lord Relican already"
REPLY = "Summon your master. I would speak with Lord Relican."
assert "—" not in REPLY and "--" not in REPLY
VARS = "Resources/Derived Character Attributes/Game Scripting Variables/"
GSV = "Derived Character Attributes/Game Scripting Variables/"
SUMMONED, CAME = "Fixt Relican Summoned", "Fixt Relican Came"
NEW_VARS = {SUMMONED: "the number of times the player has had Relican's undead summon him.",
            CAME: "the number of those summonses Relican's return dialogue has answered."}
FALLBACK = 15  # seconds: his hall is a long walk from the street, and a stuck walk still has to end in talk


def var(name):
    return ("CVariableDerivedCharacterAttribute", [("Character Attribute", GSV + name)])


def bump(name):
    """Add one to a player counter. Accumulating, like Fixt's companion growth, so each summons counts."""
    return ("CAddCharacterModifierToCharacterAction", [
        ("Modifier Description", name), ("Modification is permanent", "1"), ("Character to modify", "Player#1-9#"),
        ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
            ("Modification Amount", ("CConstant", [("Constant Value", "1")])), ("Modification amount is a percent", "0"),
            ("Allow Accumulation", "1"), ("Derived character attribute to modify", GSV + name)]))])),
        ("OPTIONAL Duration", ""), ("Expression Context", "$Instigator")])


def owed():
    return ("CExpressionAction", [("Expression", ("CIsGreaterThan", [("Operand1", var(SUMMONED)), ("Operator", ""), ("Operand2", var(CAME))])),
                                  ("Character to get attributes from", "Player1")])


DIALOG = ("CDisplayDialogTreeAction", [("Dialog Tree File", RELICAN_TREE), ("Node ID", "5 Return Dialogue"),
                                       ("Speaker", SPEAKER), ("Player Being Spoken To", "Player1")])


def answer(extra):
    return if_action(owed(), multi([bump(CAME)] + extra + [DIALOG]))


def walk():
    t = darsh_walk()
    t = re.sub(r"(\n\s*)Target=Darsh\r", lambda m: m.group(1) + "Target=" + SPEAKER + "\r", t)
    assert t.count("Destination=Companion goto spot for deletion" + CR) == 1
    t = t.replace("Destination=Companion goto spot for deletion", "Destination=Player1")
    assert t.count("Offset=0.000000,0.000000" + CR) == 1
    t = t.replace("Offset=0.000000,0.000000" + CR, "Offset=0.000000,-90.000000" + CR)  # stop in front, not on top
    a = t.index("Done action=CDeleteAction")
    done = multi([("CSendAIDoneMessage", [("Target", "$Trigger")]), answer([])])
    t = t[:a] + "Done action=" + B(*done).rstrip(CR) + t[balanced(t, a):]
    t = t.replace("Suppress can't assign error=0", "Suppress can't assign error=1")
    assert t.count("Sequence=Run" + CR) == 1
    t = t.replace("Sequence=Run" + CR, "Sequence=Walk" + CR)  # the master does not run to his servants' call
    assert "Darsh" not in t and "Original AI Type=CSkeletonAI" in t
    return re.sub(r"\r\n\t+", CR, re.sub(r"[\t ]*Object ID=[^\r\n]*\r\n", "", t)) + CR


def summons():
    stuck = lhbuild.delay(FALLBACK, answer([("CSendAIDoneMessage", [("Target", SPEAKER)])]))
    return ("CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=3" + CR +
            "Action=" + B(*bump(SUMMONED)) + "Action=" + walk() + "Action=" + B(*stuck) + "}" + CR + "}" + CR)


def gate():
    def ex(a):
        return B("CActionExpression", [("Action", a)])
    return cand(cand(ex(("CWasQuestEverActivatedAction", [("Quest", CROWN)])), ex(lhbuild.exists(SPEAKER))),
                ex(lhbuild.exists(CALLE_ONLY)))


def build_trees():
    done = []
    reply = ("Requirement=!None" + CR + "Custom Requirement=" + gate() + "Reply Text=" + REPLY + CR + "Go to node ID=" + CR +
             "Custom Action=" + summons() + CR)
    for rel, before in TREES.items():
        t = lhbuild.read(rel)
        if REPLY in t:
            continue
        assert CR in t and t.count(CR) == t.count("\n")
        s = t.index("Node ID=01 Conversation Start" + CR)
        e = t.index("-" * 60, s)
        k = t.index("Requirement=!None" + CR + "Reply Text=" + before + CR, s, e)
        t = t[:k] + reply + t[k:]
        (lhbuild.FX / rel).parent.mkdir(parents=True, exist_ok=True)
        (lhbuild.FX / rel).write_bytes(t.encode("latin-1"))
        done.append(rel)
    return done


def build_vars():
    done = []
    for name, what in NEW_VARS.items():
        rel = VARS + name + ".DerivedCharacterAttribute"
        if (lhbuild.FX / rel).exists():
            continue
        v = lhbuild.read(VARS + "Esteban Dead.DerivedCharacterAttribute").replace("Esteban Dead", name)
        v = v.replace("Description=" + CR, "Description=The value is " + what + CR)
        (lhbuild.FX / rel).write_bytes(v.encode("latin-1"))
        done.append(rel)
    return done


def main():
    done = build_vars() + build_trees()
    if done:
        register(done)
    print("relican summoned:", done)


if __name__ == "__main__":
    main()
