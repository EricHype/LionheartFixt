"""The troll chief can be told Enrique is dead. Reported: "if we take the troll chief's quest to negotiate with enrique
but enrique is already dead there's no way to resolve the quest".

`Speak for the Trolls` (0.99.24, `build_troll_voice.py`) is taken at `131 say it then` (`SPK2H7VL`), advanced only by
Enrique agreeing in his own tree (`SPK5N3BQ`), and completed at the chief's `132 no price`. Enrique's death fails `Find
Enrique` and `Help the Beggars against the Thieves Guild` and advances `Kill The Beggar Master`, but never touches the
trolls' quest, so a dead Enrique left it open for good, and the chief still offered the errand when he was already dead.

"Enrique is dead" is read from what his death leaves behind: `Kill The Beggar Master` completed or at its killed state,
`Help the Thieves Destroy the Beggars Guild` completed, or `Find Enrique` or `Help the Beggars against the Thieves Guild`
failed, which only his death does. A cured Enrique is alive and keeps the errand.

  * The chief's greeting, with the quest taken and Enrique dead, offers *"Enrique Garcia is dead. Nobody is left up there
    to pay anyone to come down."*, to `138 Fixt the price died`, which completes the quest with its XP as `132` does.
  * `130 the man above` hides *"I can go up. Let me say it for you."* when Enrique is dead and offers the same claim.

Dialogue only, so every save, one already stuck included. A rerun is a no-op.

    python tools/build_troll_enrique_dead.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH, balanced
from build_shrine_repairs import register

TREE = "Resources/Levels/Sewers/Dialog/Warning Troll.DialogTree"
Q = "Levels/Sewers/Quests/"
SPEAK = Q + "Speak for the Trolls"
NODE = "138 Fixt the price died"
CLAIM = "Enrique Garcia is dead. Nobody is left up there to pay anyone to come down."
ANSWER = ("<He is quiet a long while.> Dead. Then nobody pays, and nobody comes. That is not how I wanted it said. But it "
          "is said. Now we count quiet days instead of dead ones.")
for s in (CLAIM, ANSWER):
    assert "—" not in s and "--" not in s
OFFER = "Requirement=!None" + CR + "Reply Text=I can go up. Let me say it for you." + CR


def act(cls, **f):
    return B("CActionExpression", [("Action", (cls, list(f.items())))])


def any_of(xs):
    out = xs[-1]
    for x in reversed(xs[:-1]):
        out = "COR" + CR + "{" + CR + "Operand1=" + x + "Operator=" + CR + "Operand2=" + out + "}" + CR
    return out


def enrique_dead():
    return any_of([act("CIsQuestCompletedAction", Quest=Q + "Kill The Beggar Master"),
                   B("CActionExpression", [("Action", ("CWasQuestStateActivatedAction", [("Quest", Q + "Kill The Beggar Master"), ("State", "VVRLBE0M")]))]),
                   act("CIsQuestCompletedAction", Quest=Q + "Help the Thieves Destroy the Beggars Guild"),
                   act("CIsQuestFailedAction", Quest=Q + "Find Enrique"),
                   act("CIsQuestFailedAction", Quest=Q + "Help the Beggars against the Thieves Guild")])


def both(a, b):
    return "CAND" + CR + "{" + CR + "Operand1=" + a + "Operator=" + CR + "Operand2=" + b + "}" + CR


def node_span(t, nid):
    s = t.index(CR + "Node ID=" + nid + CR) + len(CR)
    e = t.find(DASH, s)
    return s, (t.rindex("}" + CR) if e < 0 else e)


def claim(gate):
    return ("Requirement=!None" + CR + "Custom Requirement=" + gate + "Reply Text=" + CLAIM + CR +
            "Go to node ID=" + NODE + CR + "Icon=Quest Icon" + CR + CR)


def main():
    t = lhbuild.read(TREE)
    if "Node ID=" + NODE + CR in t:
        print("troll enrique dead: []")
        return
    taken = act("CIsQuestStateTheCurrentStateAction", Quest=SPEAK, State="SPK2H7VL")
    # the chief's greeting: before his last reply, which is the boy's or an exit
    s, e = node_span(t, "95 the chief")
    k = t.index("Requirement=", t.index("Reply Text=The beggar has taken the price off you", s, e))
    k = t.index(CR + CR, k) + len(CR + CR)  # after the agreed-price reply
    t = t[:k] + claim(both(taken, enrique_dead())) + t[k:]
    # the man above: no errand for a dead man
    s, e = node_span(t, "130 the man above")
    i = t.index(OFFER, s, e)
    alive = "CExpressionNot" + CR + "{" + CR + "Operand1=" + enrique_dead() + "}" + CR
    t = t[:i] + claim(enrique_dead()) + "Requirement=!None" + CR + "Custom Requirement=" + alive + t[i + len("Requirement=!None" + CR):]
    # the node: the agreed-price ending's own completion
    s, e = node_span(t, "132 no price")
    a = t.index("Custom Action=", s, e)
    done = t[a:balanced(t, a + len("Custom Action=")) + len(CR)]
    assert "SPK9C6XZ" in done and "CSetQuestSatusToCompletedAction" in done
    node = ("Node ID=" + NODE + CR + "Text=" + ANSWER + CR + "Should Have Voiceover=0" + CR + CR +
            "Requirement=!None" + CR + "Reply Text=<Leave him to it.>" + CR + "Go to node ID=" + CR + done +
            "Icon=Quest Icon" + CR + "Is Default Reply=1" + CR)
    assert t.endswith("}" + CR)
    t = t[:-len("}" + CR)].rstrip(CR) + CR + DASH + CR + node + "}" + CR
    assert t.count(CR) == t.count("\n")
    (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
    register([TREE])
    print("troll enrique dead:", [TREE])


if __name__ == "__main__":
    main()
