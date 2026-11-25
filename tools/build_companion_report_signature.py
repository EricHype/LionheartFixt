"""The order menu's "How are you holding up?" names each companion's own growth. Asked, after the per-companion
signatures (`build_companion_power_growth.py`): "can we also add it to the description when we ask how they are doing".

`build_companion_report.py` prints health, armor, fighting skill and Celestial Smite as exact numbers, one fixed line per
value picked by halving the range (no script can print a number). This adds one can, `Fixt Companion Report/Signature`,
called after Celestial Smite. It reads the clicked companion's own attributes, so each line appears only when that
companion has the gain, and the numbers are what the engine will use:

  * `Weapon damage: N%.`             the best of slashing, crushing and piercing percent, above 100
  * `Fire power: N%.` / `Shock power: N%.`   above 100 (Darsh; Diego and the Golem)
  * `Attack speed: N%.`              the attack animation multiplier, from 105 (Fang, Ernesto)
  * `Poison on each blow: up to N.`  additional poison maximum (Goblin Girl, Grumdjum)
  * `Critical strikes: +N% chance.`  from `PhysicalCriticalResult`, which only this growth raises on a companion and which
                                     rises 5 a level beside `CriticalChance`'s 12: 12 x 0.105% / 5 = 0.252% per point
  * `Life drain: N% of damage dealt.`, `Returns N% of physical damage to attackers.` (Lost Knight, Grace)
  * `Burns attackers N% of the time.`, `Burn damage: N fire.` (Joan)

A tree edit and a new can: every save. A rerun is a no-op.

    python tools/build_companion_report_signature.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register
from build_companion_report import TREE, REPLY, DIR, attr, say, below, can_text, top_actions, call

NAME = "Signature"
REL = "Resources/" + DIR + NAME + ".can"


def times(expr, k):
    return ("CMultiply", [("Operand1", expr), ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", str(k))]))])


def best(*names):
    return ("CExpressionAggregateFunctionMax", [("Parameters", [("Parameter", attr(n)) for n in names])])


OFF = "Damage Related/Offensive/"
DR = "Damage Related/"
# expression on $Trigger, text before and after the number, the lowest value shown (below it: no line), the top value
LINES = [
    (best(OFF + "Slashing Damage Percent", OFF + "Crushing Damage Percent", OFF + "Piercing Damage Percent"),
     "Weapon damage: ", "%.", 101, 400),
    (attr(OFF + "Fire Damage Percent"), "Fire power: ", "%.", 101, 500),
    (attr(OFF + "Electrical Damage Percent"), "Shock power: ", "%.", 101, 500),
    (times(attr("Speed/Attack Animation Speed Multiplier"), 100), "Attack speed: ", "%.", 105, 300),
    (attr(DR + "Additional Poison Damage Maximum"), "Poison on each blow: up to ", ".", 1, 60),
    (times(attr("PhysicalCriticalResult"), 0.252), "Critical strikes: +", "% chance.", 1, 40),
    (times(attr(DR + "Melee Damage Percentage Gives Health To Attacker Zero To One"), 100), "Life drain: ",
     "% of damage dealt.", 1, 80),
    (times(attr(DR + "Physical Damage Percentage Given To Attacker Zero To One"), 100), "Returns ",
     "% of physical damage to attackers.", 1, 80),
    (attr(DR + "Should Give Backlash Fire Damage To Attacker Percentage"), "Burns attackers ", "% of the time.", 1, 100),
    (attr(DR + "Backlash Fire Damage To Give Attacker"), "Burn damage: ", " fire.", 1, 60),
]
for _, a, b, _, _ in LINES:
    assert "—" not in a + b and "--" not in a + b


def lookup(expr, pre, post, lo, hi):
    """Exact value lo..hi; below lo prints nothing; the top leaf says "or more"."""
    def node(a, b):
        if a == b:
            return say(pre + str(a) + post if a < hi else pre + str(a) + post.rstrip(".") + " or more.")
        mid = (a + b + 1) // 2
        return below(expr, mid, node(a, mid - 1), node(mid, b))
    return below(expr, lo, "", node(lo, hi))


def build_can():
    if (lhbuild.FX / REL).exists():
        return []
    acts = [lookup(*line) for line in LINES]
    body = ("CMultipleActionsAction", [("Action", ("Array", [("Item Count", str(len(acts)))] + [("Action", a) for a in acts]))])
    lhbuild.write_map(REL, can_text(body))
    return [REL]


def build_reply():
    t = lhbuild.read(TREE)
    if DIR + NAME + CR in t:
        return []
    r = t.index(REPLY)
    arr = t.index("Action=Array", r)
    acts = top_actions(t, arr)
    count = re.compile(r"Item Count=(\d+)\r\n").search(t, arr)
    assert int(count.group(1)) == len(acts)
    smite = [e for s, e in acts if DIR + "Celestial Smite" + CR in t[s:e]]
    assert len(smite) == 1
    e = smite[0]
    t = t[:e] + call(NAME) + t[e:]
    t = t[:count.start()] + "Item Count=" + str(len(acts) + 1) + CR + t[count.end():]
    (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
    return [TREE]


def main():
    done = build_can() + build_reply()
    if done:
        register(done)
    print("companion report signature:", done)


if __name__ == "__main__":
    main()
