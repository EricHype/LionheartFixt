"""The Inquisition learns of Torquemada's death from Raphael, or not at all. Reported after the fight: "i couldn't click
on/attack the one that was left. When i went upstairs to talk to raphael, the guards attacked me. They should be neutral
until raphael goes hostile. We should be forced to talk to him after killing torquemada unless we sneak by", then "the
guards outside torquemada's chamber and the inquisitor there should fight too", and "if you sneak out and then return,
he shouldn't know you killed torquemada, right?"

0.96.0 (`build_inquisition_turns.py`) made starting Torquemada's fight the point of no return: it set `Fixt Inquisition
Hostile`, and every Inquisitor in Barcelona and Montaillou attacked on sight until a deal with Raphael. Now:

  * **The chambers fight, and only the chambers.** Starting his fight sets `Fixt Chambers Hostile` instead. The chambers'
    own turn relay (every Inquisitor spawned there, the guards and the jailor included) reads it as well as the old
    flag, so the house he died in fights you, now and on a later visit, until Raphael absolves you or you got away
    clean. Everywhere else reads only `Fixt Inquisition Hostile`, which now only Raphael's fight sets.
  * **Torquemada can be fought.** The fight relay took his talk specifier away and gave him nothing, so there was no
    cursor; his party killed him while the player could not. The relay, and for saves that have already entered the
    chambers his fight reply half a second later, give him the monsters' `GetCloseThenTriggerAndFight`.
  * **Raphael confronts you.** The mortal Raphael (`Inquisitor Raphael Mortal.can`, spawned fresh by the foyer's reset on
    every visit, so the can reaches every save) now targets the player, and his `Patrol End Action`, which fires when
    a creature acquires its target and in vanilla only ever plays a skeleton's activate sound, records
    `Fixt Raphael Saw You`, stands him down and opens his fever conversation (member or outsider) himself. Sneaking
    shortens the distance he spots you at, which is the only part of sneaking the engine exposes, so a good sneak can
    pass him. Clicking him still opens it. Once he has turned on you, he comes to fight instead of talking.
  * **A clean getaway.** Entering any other map Inquisitors patrol (the turn relays of the Forest Exterior, the Temple,
    Gate and Port Districts, and Montaillou's inn and church) with Torquemada dead (his titles) and Raphael having
    neither seen you, fought you nor dealt with you records `Fixt Torquemada Unwitnessed`. Then the foyer spawns the
    ordinary Raphael, who knows nothing, the chambers settle, and the ending says so.
  * **The ending.** `900 order inquisition unwitnessed`, played where `dark` or `broken` would be, unless Raphael was
    later fought or killed.

Reach: the can, the trees and the ending reach every save; the chambers, foyer and getaway relays are maps, so ones not
entered since installing. A save that already started the fight under 0.96.0 has the old flag set; Raphael's deal still
clears it. A rerun is a no-op.

    python tools/build_inquisition_quiet.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balanced, delay, multi, relay
from build_shrine_repairs import register
from build_inquisition_slides import SLIDE_TREE, flag, say, var_if, write_var
from build_inquisition_turns import (ABSOLVED, CHAMBERS, FOYER, HOSTILE, MAPS, RAPHAEL_DEAD, SEDE, TEMPLATES, TREE_PATH,
                                     TURN, MORTAL_CAN, spawn_names, titled)
from build_torquemada import clone, part_span, to_combat
from build_crossroads_standard import specifier

VARS = "Derived Character Attributes/Game Scripting Variables/"
CH_HOSTILE = VARS + "Fixt Chambers Hostile"
WITNESSED = VARS + "Fixt Raphael Saw You"
UNWITNESSED = VARS + "Fixt Torquemada Unwitnessed"
SLIDES = "Resources/Levels/8 Alamut/Dialog/Fixt Ending Slides.DialogTree"
ENDGAME = "Levels/8 Alamut/END GAME Siege Map.zax"
GI_TREE = "Resources/Levels/1 Barcelona/Dialog/Temple District/GrandInquisitor.DialogTree"
UNW_NODE = "900 order inquisition unwitnessed"
UNW_TEXT = ("The Inquisition entered the siege with a new head. Torquemada died in his own chambers, and the Holy Office "
            "recorded it as a fever. For once the record was all anyone had. Raphael took the chair within the year and "
            "spent the first of it looking for the hand, because a man who has found one door into those chambers looks "
            "for the others. He never found it. He burned more than Torquemada ever had, with better records, and the "
            "cities paid for the wood. The archive holds every name he suspected. Yours is not among them.")
assert "—" not in UNW_TEXT and "--" not in UNW_TEXT
FIGHT_KIND = "GetCloseThenTriggerAndFight"  # what 428 of the vanilla monster cans carry


def everyone(action):
    return ("CForEachPlayerAction", [("Action", action)])


def fight_click(name):
    return specifier(name, FIGHT_KIND, "")


def bump_array(text, array_at, by):
    c = text.index("Item Count=", array_at)
    m = re.compile(r"Item Count=(\d+)").match(text, c)
    return text[:c] + "Item Count=" + str(int(m.group(1)) + by) + text[m.end():]


# ---- the chambers ------------------------------------------------------------------------------

def chambers_turn(z):
    stand_down = MAPS[CHAMBERS]
    from build_inquisition_turns import deactivate, exists, if_action
    extra = [if_action(exists("Fixt Torquemada is dead"), "", relay("Fixt Torquemada fight"))]
    body = multi([deactivate(n) for n in stand_down] + [to_combat(n) for n in spawn_names(z)] + extra)
    quiet = var_if(ABSOLVED, "", body)
    return delay(1.5, var_if(HOSTILE, quiet, var_if(CH_HOSTILE, var_if(UNWITNESSED, "", quiet), "")))


def build_chambers():
    z = lhbuild.read(CHAMBERS)
    if "Fixt Chambers Hostile" in z:
        return []
    s, e = part_span(z, "Fixt Torquemada fight")
    p = z[s:e]
    assert p.count("Game Scripting Variables/Fixt Inquisition Hostile" + CR) == 1
    p = p.replace("Game Scripting Variables/Fixt Inquisition Hostile" + CR, "Game Scripting Variables/Fixt Chambers Hostile" + CR)
    r = p.index("Action=CRemoveAIAction")
    assert "Target Name=Grand Inquisitor" in p[r:r + 200]
    end = balanced(p, r) + len(CR)
    p = p[:end] + "Action=" + B(*fight_click("Grand Inquisitor")) + p[end:]
    p = bump_array(p, p.index("Action=CMultipleActionsAction"), 1)
    z = z[:s] + p + z[e:]
    s, e = part_span(z, TURN)
    z = z[:s] + lhbuild.relay_part(TURN, chambers_turn(z), 40, 40, once="0") + z[e + len(CR):]
    lhbuild.write_map(CHAMBERS, z)
    return [CHAMBERS]


# ---- the foyer: a clean getaway meets the ordinary Raphael -------------------------------------

def build_foyer():
    z = lhbuild.read(FOYER)
    if "Fixt Torquemada Unwitnessed" in z:
        return []
    s, e = part_span(z, "RESET MAP for Invulnerable Raphael")
    p = z[s:e]
    i = p.index("Perk To Check For=Perks/!Event Title Perks/Dark Inquisitor")
    a = p.rindex("Action=CIfExpressionAction", 0, i)
    b = balanced(p, a)
    vanilla = clone("Inquisitor Raphael generator", "Used Raphael Generator")
    mortal = var_if(ABSOLVED, "", var_if(RAPHAEL_DEAD, "", clone("Fixt Mortal Raphael generator", "Used Raphael Generator")))
    pick = titled(var_if(UNWITNESSED, vanilla, mortal), var_if(HOSTILE, "", vanilla))
    p = p[:a] + "Action=" + B(*pick).rstrip(CR) + p[b:]
    lhbuild.write_map(FOYER, z[:s] + p + z[e:])
    return [FOYER]


# ---- Raphael spots you ---------------------------------------------------------------------------

def confront():
    greet = ("CIfExpressionAction", [
        ("If Expression", ("CUseCannedExpressionExpression", [("Canned Expression", "Dialog/Requirements/Faction/Inquisitor IS")])),
        ("Character to get attributes from", "Player1"),
        ("Then", ("CDisplayDialogTreeAction", [("Dialog Tree File", TREE_PATH), ("Node ID", "1300 Fixt the fever member"),
                                               ("Speaker", "Inquisitor Raphael"), ("Player Being Spoken To", "Player1")])),
        ("Else", ("CDisplayDialogTreeAction", [("Dialog Tree File", TREE_PATH), ("Node ID", "1300 Fixt the fever"),
                                               ("Speaker", "Inquisitor Raphael"), ("Player Being Spoken To", "Player1")]))])
    talk = multi([everyone(flag(WITNESSED)),
                  ("CSetTargetTypeAction", [("Entity Name", "Inquisitor Raphael"), ("Name To Target", ""), ("Valid Targets", "")]),
                  greet])
    # Only a Raphael who has already confronted you comes to fight: a save that started Torquemada's fight under
    # 0.96.0 carries the old flag from the chambers alone, and he still talks to it, so the deal can clear it.
    return var_if(WITNESSED, var_if(HOSTILE, to_combat("Inquisitor Raphael"), talk), talk)


def build_raphael():
    z = lhbuild.read(MORTAL_CAN)
    if "Fixt Raphael Saw You" in z:
        return []
    f = re.sub(r"(?m)^Object ID=[^\r\n]*\r\n", "", re.sub(r"(?m)^\t+", "", z))
    k = f.index("Activity=CSkeletonAI" + CR)
    end = balanced(f, k)
    sk = f[k:end]
    assert sk.count("Patrol End Action=" + CR) == 1 and sk.count("Valid Targets=" + CR) == 1, "skeleton fields"
    # targets first: the confrontation inserted below has an empty Valid Targets of its own (its stand-down), and the
    # first build set that one instead, so he never looked for anyone and could be walked past
    t = sk.index("Target Type=CEntityBehaviorStateSetClosestTarget" + CR)
    v = sk.index("Valid Targets=" + CR, t)
    sk = sk[:v] + "Valid Targets=Player" + CR + sk[v + len("Valid Targets=" + CR):]
    sk = sk.replace("Patrol End Action=" + CR, "Patrol End Action=" + B(*confront()), 1)
    lhbuild.write_map(MORTAL_CAN, f[:k] + sk + f[end:])
    return [MORTAL_CAN]


# ---- leaving unseen ------------------------------------------------------------------------------

def getaway():
    return titled(var_if(WITNESSED, "", var_if(HOSTILE, "", var_if(ABSOLVED, "", everyone(flag(UNWITNESSED))))), "")


def build_getaway():
    done = []
    for rel in MAPS:
        if rel in (FOYER, CHAMBERS):
            continue
        z = lhbuild.read(rel)
        if "Fixt Torquemada Unwitnessed" in z:
            continue
        s, e = part_span(z, TURN)
        p = z[s:e]
        a = p.index("Action=CDelayAction")  # the relay's one action
        b = balanced(p, a)
        old = p[a + len("Action="):b]
        new = "CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR + \
              "Action=" + old + CR + "Action=" + B(*getaway()) + "}" + CR + "}"
        p = p[:a] + "Action=" + new + p[b:]
        lhbuild.write_map(rel, z[:s] + p + z[e:])
        done.append(rel)
    return done


# ---- Torquemada's fight reply gives him a cursor, for saves past the chambers ----------------------

def build_gi_tree():
    t = lhbuild.read(GI_TREE)
    if FIGHT_KIND in t:
        return []
    s = t.index("Node ID=120 combat" + CR)
    e = t.index("-" * 60, s)
    old = "CTriggerRelayAction" + CR + "{" + CR + "Relay Name=Fixt Torquemada fight" + CR + "}"
    node = t[s:e]
    n = node.count(old)
    assert n == 2, n  # the plain fight, and the twin-clearing arm's delayed one
    new = B(*multi([relay("Fixt Torquemada fight"), delay(0.5, fight_click("Grand Inquisitor"))])).rstrip(CR)
    node = node.replace(old, new)
    t = t[:s] + node + t[e:]
    (FX / GI_TREE).write_bytes(t.encode("latin-1"))
    return [GI_TREE]


# ---- the ending --------------------------------------------------------------------------------

def build_slides():
    t = lhbuild.read(SLIDES)
    if "Node ID=" + UNW_NODE + CR in t:
        return []
    node = ("Node ID=" + UNW_NODE + CR + "Text=" + UNW_TEXT + CR + "Should Have Voiceover=1" + CR + CR +
            "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=" + CR +
            "Custom Action=" + B(*relay("Fixt order epilogue relay")) + "Is Default Reply=1" + CR + "-" * 60 + CR)
    key = "Node ID=900 order wielder ring" + CR
    assert t.count(key) == 1
    t = t.replace(key, node + key)
    assert t.count(CR) == t.count("\n")
    (FX / SLIDES).write_bytes(t.encode("latin-1"))
    return [SLIDES]


def build_endgame():
    z = lhbuild.read(ENDGAME)
    if UNW_NODE in z:
        return []
    f = re.sub(r"(?m)^Object ID=[^\r\n]*\r\n", "", re.sub(r"(?m)^\t+", "", z))
    n = 0
    for nid in ("900 order inquisition dark", "900 order inquisition broken"):
        pat = re.compile(r"(?m)^(Then|Else)=CDisplayDialogTreeAction\r\n\{\r\nDialog Tree File=" + re.escape(SLIDE_TREE) +
                         r"\r\nNode ID=" + re.escape(nid) + r"\r\n")
        pos = 0
        while True:
            m = pat.search(f, pos)
            if not m:
                break
            v = m.start() + len(m.group(1)) + 1
            e = balanced(f, v)
            orig = f[v:e] + CR
            wrapped = var_if(UNWITNESSED, var_if(HOSTILE, "@ORIG@", say(UNW_NODE)), "@ORIG@")
            txt = B(*wrapped).replace("@ORIG@" + CR, orig).rstrip(CR)
            f = f[:v] + txt + f[e:]
            pos = v + len(txt)  # past the wrapper, which holds the original twice and must not be wrapped again
            n += 1
    assert n >= 2, n
    lhbuild.write_map(ENDGAME, f)
    return [ENDGAME]


def main():
    for path, short, what in ((CH_HOSTILE, "Fixt Chambers Hostile", "1 means the player started the fight with Torquemada in his chambers."),
                              (WITNESSED, "Fixt Raphael Saw You", "1 means Raphael confronted the player after Torquemada died."),
                              (UNWITNESSED, "Fixt Torquemada Unwitnessed", "1 means the player killed Torquemada and got away without Raphael seeing.")):
        rel = "Resources/" + path + ".DerivedCharacterAttribute"
        if not (FX / rel).exists():
            write_var(path, short, what)
            register([rel])
    done = build_chambers() + build_foyer() + build_raphael() + build_getaway() + build_gi_tree() + build_slides() + build_endgame()
    if done:
        register(done)
    print("inquisition quiet:", done)


if __name__ == "__main__":
    main()
