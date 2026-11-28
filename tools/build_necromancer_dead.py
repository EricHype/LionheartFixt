"""The Necromancer title commands the dead. Reported of a speech-and-necromancy character at level 13: "the character
feels more and more like it can't finish the game ... When facing a rock titan, I can't even hit them and neither can
my companions", then "enemies get multiple summons at once, why shouldn't I if I have the mana capacity?", and the
design settled on: "what if instead of raising the same, we stack. So you start with a zombie, then a zombie and a
skeleton, then a zombie a skeleton and a reaver."

The title (`Perks/!Event Title Perks/Necromancer`, Relican's, for delivering La Calle Perdida) is vanilla's and does
nothing. Raise Undead is rated at Summoning minus 49 and picks its creature by that rating: a Zombie below 50 (Ranged
75, 30 HP), a Greater Skeleton from 50 (one-handed 120), a Soul Reaver from 100 (one-handed 160). So at Summoning 80 a
necromancer raises a zombie, needs 99 for a skeleton and 149, past most of a game, for a reaver; and one at a time,
because a cast locks the spell for its 180 s duration until the summon dies. The Mountain Pass titans (AC 230-280,
immune to the Tribal school's acid and poison) come two to five at once.

For a caster holding the title:

  * **Full strength.** Every read of the spell's own rating, in the skill and in its projectile, adds 49 when the caster
    has the perk: `CAdd(rating, CIfExpression(has Necromancer, 49, 0))`. So the title rates it at the full Summoning,
    and the HP and damage percentages that grow with the rating grow with it. Without the title the sum adds 0.
  * **One of each kind.** The projectile's hit gains a first branch for the title: raise the strongest kind the rating
    allows that is not already standing (a reaver from 100, a skeleton from 50, else a zombie); with all of them up,
    *"Your dead already stand with you."* Each branch is vanilla's own for that kind, unchanged but for the name: the
    summon is set up as `Raised Zombie`, `Raised Skeleton` or `Raised Reaver` and keeps it, where vanilla sets it up as
    `Summoned Undead` and renames it `Undead Energy target`. So each kind can be counted (`CIsAliveAction`), and a new
    raise never touches the standing ones. Mana still caps it: every summon drains 3 every 2 s and is released when the
    caster runs dry, as in vanilla.
  * **A 30 s cooldown, per cast.** The cast's own 180 s lock is released 30 s after each raise (a `CDelayAction` before
    the timer reset vanilla's summons already use), not when the summon is gone. Vanilla frees every summoning spell
    when its summon dies, is released or turns hostile; the necromancer's copies still free the other three but not
    Raise Undead, so a loss does not skip the wait. The "already standing" cast takes the same 30 s, so mashing the key
    cannot waste mana over and over. Asked: "Why shouldn't we keep a longer recast charge?" A full army of three takes
    about a minute; a fallen skeleton is a real loss mid-fight. A map change inside the 30 s may drop the delayed
    release, and then the lock simply runs its 180 s.
  * **Undead Energy** buffs `Undead Energy target`; it gains the same check and buff for each of the three names, so it
    still reaches a necromancer's dead.
  * The description gains one sentence.

Without the title nothing changes: the old hit runs in the else-arm, and the rating sum adds 0. Monster Summoning and
Raise Enemy keep their one-summon lock.

Skills and a projectile are resources, so every save. A rerun is a no-op.

    python tools/build_necromancer_dead.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, balanced
from build_shrine_repairs import register

SKILL = "Resources/Skills/Magic Tribal/Offensive/Raise Undead.Skill"
PROJ = "Resources/Spell Projectiles/Raise Undead Instant Hit Projectile.InventoryItem"
ENERGY = "Resources/Skills/Magic Tribal/Defensive/Undead Energy.Skill"
RAISE = "Skills/Magic Tribal/Offensive/Raise Undead"
PERK = "Perks/!Event Title Perks/Necromancer"
BONUS = 49  # the spell's own differential under Summoning
COOLDOWN = 30  # seconds between a necromancer's raises: a full army of three in about a minute, a loss felt
KINDS = [("Raised Reaver", 100), ("Raised Skeleton", 50), ("Raised Zombie", 0)]  # strongest first
SHARED, VANILLA_FINAL = "Summoned Undead", "Undead Energy target"
FULL = "Your dead already stand with you."
SENTENCE = (" One who holds the Necromancer title raises the dead as though this spell were at their full Summoning "
            "skill, and keeps one of each kind it can command: a Zombie, a Greater Skeleton from 50, and a Soul Reaver "
            "from 100. Each cast raises the strongest one missing.")
for s in (FULL, SENTENCE):
    assert "—" not in s and "--" not in s
READ = "CVariableSkill" + CR + "{" + CR + "Skill=" + RAISE + CR + "}"


def flat(t):
    t = re.sub(r"(?m)^\t+", "", t)
    return re.sub(r"(?m)^Object ID=[^\r\n]*\r\n", "", t)


def has_perk():
    return ("CHasPerkExpression", [("Perks To Check For", ("Array", [("Item Count", "1"), ("Perk To Check For", PERK)]))])


def boosted_read():
    bonus = ("CIfExpression", [("Condition", has_perk()), ("OperatorPart1", ""), ("Value if True ", ("CConstant", [("Constant Value", str(BONUS))])),
                               ("OperatorPart2", ""), ("Value if False", ("CConstant", [("Constant Value", "0")]))])
    return "CAdd" + CR + "{" + CR + "Operand1=" + READ + CR + "Operator=" + CR + "Operand2=" + B(*bonus) + "}"


def fields(t, brace):
    """Depth-1 fields of the block whose '{' is at `brace`: {key: (value start, value end)}."""
    out, d, pos = {}, 0, brace
    while True:
        nl = t.index(CR, pos)
        line = t[pos:nl]
        if d == 1 and "=" in line and not line.startswith("}"):
            k = line.split("=", 1)[0]
            v = pos + len(k) + 1
            e = balanced(t, v) if t.startswith("C", v) and t.startswith("{", t.index(CR, v) + len(CR)) else nl
            out[k] = (v, e)
        d += line.count("{") - line.count("}")
        pos = nl + len(CR)
        if d == 0:
            return out


def branch_items(branch):
    """The items of a vanilla tier branch (a CMultipleActionsAction), each 'Action=...' ending CR."""
    a = branch.index("Item Count=")
    m = re.compile(r"Item Count=(\d+)\r\n").match(branch, a)
    pos, out = m.end(), []
    for _ in range(int(m.group(1))):
        assert branch.startswith("Action=", pos), branch[pos:pos + 60]
        e = balanced(branch, pos)
        out.append(branch[pos:e + len(CR)])
        pos = e + len(CR)
    return out


def multi_raw(items):
    return "CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=" + str(len(items)) + CR + "".join(items) + "}" + CR + "}"


RESETS = re.compile(r"Item Count=4\r\n((?:Action=CResetSpellCastTimerAction\r\n\{\r\nSpell=[^\r\n]*\r\nCharacter To Reset=[^\r\n]*\r\n\}\r\n){4})")
ONE_RESET = re.compile(r"Action=CResetSpellCastTimerAction\r\n\{\r\nSpell=([^\r\n]*)\r\nCharacter To Reset=[^\r\n]*\r\n\}\r\n")


def no_release_on_loss(text):
    """Vanilla frees every summoning spell when its summon dies, is released or turns hostile. A necromancer's copy
    still frees the other three but not Raise Undead, so a loss does not skip the cooldown."""
    def drop(m):
        kept = [r.group(0) for r in ONE_RESET.finditer(m.group(1)) if r.group(1) != RAISE]
        assert len(kept) == 3, m.group(1)[:200]
        return "Item Count=3" + CR + "".join(kept)
    out, n = RESETS.subn(drop, text)
    return out, n


def release_later():
    """The cooldown: the cast's own 180 s lock, released COOLDOWN seconds after the raise."""
    return "Action=" + B(*lhbuild.delay(COOLDOWN, ("CResetSpellCastTimerAction", [("Spell", RAISE), ("Character To Reset", "$Caster")])))


def kind_branch(vanilla_branch, name):
    """Vanilla's branch for one kind, set up under `name` and keeping it, then the cooldown."""
    items = branch_items(vanilla_branch)
    last = items[-1]
    assert last.startswith("Action=CSetName" + CR) and "New Name=" + VANILLA_FINAL + CR in last, last[:120]
    items = [i.replace(SHARED, name) for i in items[:-1]]
    assert all(SHARED not in i for i in items)
    out, total = [], 0
    for i in items:
        o, n = no_release_on_loss(i)
        out.append(o)
        total += n
    assert total == 3, (name, total)  # its death, its release for want of mana, and its turning hostile
    return multi_raw(out + [release_later()])


def necro_hit(t, hit_brace):
    top = fields(t, hit_brace)
    zombie = t[slice(*top["Then"])]
    else_v = top["Else"]
    inner = fields(t, t.index("{", else_v[0]))
    skeleton, reaver = t[slice(*inner["Then"])], t[slice(*inner["Else"])]
    for b, cls in ((zombie, "Zombie 01"), (skeleton, "Skeleton"), (reaver, "Reaver")):
        assert b.startswith("CMultipleActionsAction" + CR), b[:60]
    raw = {"Raised Zombie": zombie, "Raised Skeleton": skeleton, "Raised Reaver": reaver}

    def rating_at_least(n):
        rating = "CAdd" + CR + "{" + CR + "Operand1=" + READ + CR + "Operator=" + CR + "Operand2=" + B("CConstant", [("Constant Value", str(BONUS))]) + "}" + CR
        return ("CExpressionAction" + CR + "{" + CR + "Expression=CIsGreaterThanOrEqual" + CR + "{" + CR + "Operand1=" + rating +
                "Operator=" + CR + "Operand2=" + B("CConstant", [("Constant Value", str(n))]) + "}" + CR +
                "Character to get attributes from=$Caster" + CR + "}" + CR)

    def not_alive(name):
        return "CNotAction" + CR + "{" + CR + "Action=" + B("CIsAliveAction", [("Name To Check For", name), ("Desired Minimum Count", "1")]) + "}" + CR

    full = multi_raw(["Action=" + B("CPrintCombatTextAction", [("Text to print", FULL), ("Character to show text to", "$Caster"), ("Emphasize", "0"), ("Suppress Duplicates", "1")]),
                      release_later()]) + CR
    chain = full
    for name, at in reversed(KINDS):
        cond = not_alive(name) if at == 0 else ("CAndAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=2" + CR +
                                                  "Action=" + rating_at_least(at) + "Action=" + not_alive(name) + "}" + CR + "}" + CR)
        chain = ("CIfAction" + CR + "{" + CR + "If=" + cond + "Then=" + kind_branch(raw[name], name) + CR + "Else=" + chain +
                 "Return failure if the If failes=0" + CR + "}" + CR)
    return chain


def build_projectile():
    t = flat(lhbuild.read(PROJ))
    if "Perk To Check For=" + PERK + CR in t:
        return []
    i = t.index("Hit Action=CIfExpressionAction" + CR)
    v = i + len("Hit Action=")
    e = balanced(t, v)
    old = t[v:e] + CR
    new = ("CIfExpressionAction" + CR + "{" + CR + "If Expression=" + B(*has_perk()) + "Character to get attributes from=$Caster" + CR +
           "Then=" + necro_hit(t, t.index("{", v)) + "Else=" + old + "}")
    lhbuild.write_map(PROJ, t[:v] + new + t[e:])
    return [PROJ]


def build_skill():
    t = flat(lhbuild.read(SKILL))
    if "Perk To Check For=" + PERK + CR in t:
        return []
    n = t.count(READ)
    assert n == 24, n
    t = t.replace(READ, boosted_read())
    m = re.search(r"(?m)^Description=([^\r\n]*)", t)
    t = t[:m.end()] + SENTENCE + t[m.end():]
    lhbuild.write_map(SKILL, t)
    return [SKILL]


def build_energy():
    t = flat(lhbuild.read(ENERGY))
    if "Name To Check For=Raised Reaver" + CR in t:
        return []
    m = re.search(r"(?m)^Action=CIfAction\r\n\{\r\nIf=CIsAliveAction\r\n\{\r\nName To Check For=" + VANILLA_FINAL + r"\r\n", t)
    s = m.start()
    e = balanced(t, s) + len(CR)
    one = t[s:e]
    assert one.count(VANILLA_FINAL) == 3, one.count(VANILLA_FINAL)
    copies = "".join(one.replace(VANILLA_FINAL, name) for name, _ in KINDS)
    # the CIfAction is a direct item of the launch action's array: bump that array by three
    arr = t.rindex("Action=Array" + CR, 0, s)
    assert t.rindex("{", 0, s) == t.index("{", arr) or t[t.index("{", arr):s].count("{") == t[t.index("{", arr):s].count("}") + 1, "not a direct item"
    t = t[:e] + copies + t[e:]
    c = t.index("Item Count=", arr)
    mc = re.compile(r"Item Count=(\d+)").match(t, c)
    t = t[:c] + "Item Count=" + str(int(mc.group(1)) + len(KINDS)) + t[mc.end():]
    lhbuild.write_map(ENERGY, t)
    return [ENERGY]


def main():
    done = build_skill() + build_projectile() + build_energy()
    if done:
        register(done)
    print("necromancer dead:", done)


if __name__ == "__main__":
    main()
