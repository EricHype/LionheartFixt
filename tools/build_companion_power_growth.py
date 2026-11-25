"""Companions' damage grows with them, each in their own way. Asked: "We should build in a formula that works for both
ranged and melee so they don't get outclassed the longer they are with you", then "what if we considered different
buffs for different characters ... That way they feel more unique and solve the same problem".

Fixt's growth (`Fixt Companion Growth Install`, and Ernesto's own watch in his Joined can) gives each companion, at every
player level-up, +9 health, +8 armor and +3 one-handed skill (Celestial Smite for Diego and Darsh). Companions cannot be
given weapons: each has one built-in attack of fixed damage (Lost Knight 3-12, Cervantes 1-6), so they hit more often
but never harder, while median enemy HP grows about 3.3x from Montserrat to Alamut.

Each level-up now also gives every companion a shared floor and a signature (`SIGNATURE` below):

  * Floor: +5 `Slashing`, `Crushing` and `Piercing Damage Percent` (default 100), so whatever their attack does grows.
    Lost Knight and Joan, whose signatures defend rather than hit, get +10. Diego and Darsh get it on fire and
    electrical instead, the two halves of Celestial Smite.
  * Signature: speed (`Speed/Attack Animation Speed Multiplier` +0.035, Fang and Ernesto, whose models' attacks read
    it), added poison (`Additional Poison Damage` +0.5/+1, Goblin Girl and Grumdjum), critical hits (`CriticalChance`
    +12 and `PhysicalCriticalResult` +5, Fernand, Cervantes, the Knight of Saladin), more of their own blade (+7
    slashing, Cortes and Sir Roger), elemental power (+12 electrical for the Golem and Diego, +12 fire for Darsh), life
    drain (+0.02, Lost Knight), reflection (+0.02, Grace) and fire backlash (+5% chance, +1 damage, Joan).
  * Ernesto's attack rolls to hit on `TwoHandedMelee`, but his growth has always raised one-handed, so his hit chance
    never grew. He now also gains +3 two-handed.

Checked in the exe: drain and reflection (`0x49c660`), backlash (`0x49cb07`: a percent roll on the struck character's
chance, then its fire amount) and added poison (`0x49a0c1`) read the attacker or defender from the damage record with no
player test. Damage percent is evaluated per damage type, and vanilla's Monster Summoning raises it on the summoned
monster. Critical chance is `Rules/CriticalHitExpressionMelee` (about 0.1% per point) and a crit adds 25-150%.

The first watch's actions are saved inline with it, so editing it would never reach an armed game. This is a second
watch, `Fixt Companion Power Install`, behind its own `Fixt Companion Power Watch`, called beside every call of the
first installer (the fifteen Joined cans and the order menu's three). Its watch calls `Fixt Companion Power Growth` by
name, so the numbers can be retuned later and reach every save. An existing save arms it when a companion joins or the
player opens a companion's orders; levels before that are not paid back, since nothing records how many a companion
has grown. A rerun is a no-op.

    python tools/build_companion_power_growth.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register

COS = "Resources/Common Objects and Scripts/"
VARS = "Resources/Derived Character Attributes/Game Scripting Variables/"
GROWTH_INSTALL = COS + "Fixt Companion Growth Install.can"
POWER = COS + "Fixt Companion Power Growth.can"
INSTALL = COS + "Fixt Companion Power Install.can"
WATCH_REL = VARS + "Fixt Companion Power Watch.DerivedCharacterAttribute"
GROWTH_WATCH_REL = VARS + "Fixt Companion Growth Watch.DerivedCharacterAttribute"
OLD_CALL = "Canned Object=Common Objects and Scripts/Fixt Companion Growth Install"
NEW_CALL = "Canned Object=Common Objects and Scripts/Fixt Companion Power Install"
CALLERS = [COS + "Fixt Companion Joined/" + n + ".can" for n in [
    "Bishop Diego", "Cervantes", "Cortes", "Darsh", "Distressed Sailor", "Fang", "Goblin Girl", "Goblin Grumdjum", "Golem",
    "Grace", "Joan of Arc", "Knight of Saladin", "Lost Knight", "Sir Roger Templeton", "Trapped Conquistador"]] + [
    "Resources/Levels/Generic Companion Dialog.DialogTree"]
DCA = "Derived Character Attributes/"
OFF = DCA + "Damage Related/Offensive/"
DR = DCA + "Damage Related/"
PHYSICAL = [OFF + k + " Damage Percent" for k in ("Slashing", "Crushing", "Piercing")]
SMITE = [OFF + "Fire Damage Percent", OFF + "Electrical Damage Percent"]
FLOOR, STRONG_FLOOR = "5", "10"
LEVERS = {
    "speed": [(DCA + "Speed/Attack Animation Speed Multiplier", "0.035")],
    "poison": [(DR + "Additional Poison Damage Minimum", "0.5"), (DR + "Additional Poison Damage Maximum", "1")],
    "crit": [(DCA + "CriticalChance", "12"), (DCA + "PhysicalCriticalResult", "5")],
    "blade": [(OFF + "Slashing Damage Percent", "7")],
    "shock": [(OFF + "Electrical Damage Percent", "12")],
    "fire": [(OFF + "Fire Damage Percent", "12")],
    "drain": [(DR + "Melee Damage Percentage Gives Health To Attacker Zero To One", "0.02")],
    "reflect": [(DR + "Physical Damage Percentage Given To Attacker Zero To One", "0.02")],
    "backlash": [(DR + "Should Give Backlash Fire Damage To Attacker Percentage", "5"),
                 (DR + "Backlash Fire Damage To Give Attacker", "1")],
}
# scripting name -> (signature, floor attributes, floor amount, extra skills)
SIGNATURE = {
    "Fang": ("speed", PHYSICAL, FLOOR, ()),
    "Goblin Girl": ("poison", PHYSICAL, FLOOR, ()),
    "Distressed Sailor": ("crit", PHYSICAL, FLOOR, ()),
    "Cervantes": ("crit", PHYSICAL, FLOOR, ()),
    "Cortes": ("blade", PHYSICAL, FLOOR, ()),
    "Cortes with arm": ("blade", PHYSICAL, FLOOR, ()),
    "Lost Knight": ("drain", PHYSICAL, STRONG_FLOOR, ()),
    "Trapped Conquistador": ("speed", PHYSICAL, FLOOR, ("TwoHandedMelee",)),
    "Golem": ("shock", PHYSICAL, FLOOR, ()),
    "Grace": ("reflect", PHYSICAL, FLOOR, ()),
    "Joan of Arc": ("backlash", PHYSICAL, STRONG_FLOOR, ()),
    "Sir Roger Templeton": ("blade", PHYSICAL, FLOOR, ()),
    "Knight of Saladin": ("crit", PHYSICAL, FLOOR, ()),
    "Goblin Grumdjum": ("poison", PHYSICAL, FLOOR, ()),
    "Bishop Diego": ("shock", SMITE, FLOOR, ()),
    "Darsh": ("fire", SMITE, FLOOR, ()),
}
LOG = "<Your companions grow more dangerous, each in their own way.>"
assert "—" not in LOG and "--" not in LOG


def derived(attr, amount):
    return ("Modifier", ("CCharacterModifierDerivedAttribute", [
        ("Modification Amount", ("CConstant", [("Constant Value", amount)])), ("Modification amount is a percent", "0"),
        ("Allow Accumulation", "1"), ("Derived character attribute to modify", attr)]))


def gains(name):
    sig, floor_attrs, floor, skills = SIGNATURE[name]
    mods = [derived(a, floor) for a in floor_attrs] + [derived(a, v) for a, v in LEVERS[sig]]
    mods += [("Modifier", ("CCharacterModifierSkill", [
        ("Modification Amount", ("CConstant", [("Constant Value", "3")])), ("Modification amount is a percent", "0"),
        ("Allow Accumulation", "1"), ("Skill to modify", "Skills/Fighting/" + s)])) for s in skills]
    return ("CAddCharacterModifierToCharacterAction", [
        ("Modifier Description", "Fixt companion power"), ("Modification is permanent", "1"), ("Character to modify", name),
        ("Modifiers", ("Array", [("Item Count", str(len(mods)))] + mods)), ("OPTIONAL Duration", ""),
        ("Expression Context", "$Instigator")])


def block(var, name):
    log = ("CPrintCombatTextAction", [("Text to print", LOG), ("Character to show text to", "Player1"), ("Emphasize", "0"),
                                      ("Suppress Duplicates", "1")])
    inner = ("CIfAction", [("If", ("CCheckExistenceAction", [("Name To Check For", name), ("Desired Minimum Count", "1")])),
                           ("Then", ("CMultipleActionsAction", [("Action", ("Array", [("Item Count", "2"), ("Action", gains(name)),
                                                                                     ("Action", log)]))])),
                           ("Else", ""), ("Return failure if the If failes", "0")])
    return ("CIfExpressionAction", [
        ("If Expression", ("CIsEqualTo", [("Operand1", ("CVariableDerivedCharacterAttribute", [
            ("Character Attribute", "Derived Character Attributes/Game Scripting Variables/" + var)])),
            ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", "1")]))])),
        ("Character to get attributes from", "Player1"), ("Then", inner), ("Else", "")])


def companions():
    """(variable, name) per block of the first installer, then Ernesto, whose watch is his own."""
    t = lhbuild.read(GROWTH_INSTALL)
    pairs = re.findall(r"Game Scripting Variables/(Fixt Companion [^\r]+)\r\n(?:[^\r]*\r\n){1,12}?\s*Character to get attributes "
                       r"from=Player1\r\n\s*Then=CIfAction\r\n\s*\{\r\n\s*If=CCheckExistenceAction\r\n\s*\{\r\n\s*Name To Check "
                       r"For=([^\r]+)\r\n", t)
    assert len(pairs) == 15, pairs
    return pairs + [("Fixt Companion Trapped Conquistador", "Trapped Conquistador")]


def enclosing_array_count(t, k):
    """Index of the `Item Count=` that opens the innermost block enclosing k."""
    d, j = 0, k - 1
    while True:
        if t[j] == "}":
            d += 1
        elif t[j] == "{":
            if d == 0:
                break
            d -= 1
        j -= 1
    m = re.match(r"\{\r\n\s*Item Count=", t[j:])
    assert m, t[j - 80:j + 80]
    return j + m.end() - len("Item Count=")


def add_call(rel):
    t = lhbuild.read(rel)
    if NEW_CALL in t:
        return False
    for _ in range(t.count(OLD_CALL + CR)):
        c = [m.start() for m in re.finditer(re.escape(OLD_CALL + CR), t) if NEW_CALL not in t[m.start():m.start() + 300]][0]
        a = t.rindex("Action=CUseCannedActionAction", 0, c)
        ls = t.rindex(CR, 0, a) + len(CR)
        e = lhbuild.balanced(t, a) + len(CR)
        copy = t[ls:e].replace(OLD_CALL, NEW_CALL)
        ic = enclosing_array_count(t, a)
        ie = t.index(CR, ic)
        n = int(t[ic + len("Item Count="):ie])
        t = t[:ic] + "Item Count=%d" % (n + 1) + t[ie:e] + copy + t[e:]
        # the inserted copy now follows the original; the next search skips originals already followed
    assert t.count(NEW_CALL + CR) == t.count(OLD_CALL + CR)
    (lhbuild.FX / rel).write_bytes(t.encode("latin-1"))
    return True


def main():
    done = []
    if not (lhbuild.FX / WATCH_REL).exists():
        v = lhbuild.read(GROWTH_WATCH_REL).replace("Fixt Companion Growth Watch", "Fixt Companion Power Watch")
        v = v.replace("1 means the level-up watcher has already been added to the player.",
                      "1 means the companion power watcher (weapon damage and skills per level) has been added to the player.")
        (lhbuild.FX / WATCH_REL).write_bytes(v.encode("latin-1"))
        done.append(WATCH_REL)
    if not (lhbuild.FX / POWER).exists():
        pairs = companions()
        assert sorted(n for _, n in pairs) == sorted(SIGNATURE), set(n for _, n in pairs) ^ set(SIGNATURE)
        acts = [block(v, n) for v, n in pairs]
        body = B("CMultipleActionsAction", [("Action", ("Array", [("Item Count", str(len(acts)))] + [("Action", a) for a in acts]))])
        lhbuild.write_map(POWER, "CCannedObject" + CR + "{" + CR + "Object=" + body + "}" + CR)
        done.append(POWER)
    if not (lhbuild.FX / INSTALL).exists():
        t = lhbuild.read(GROWTH_INSTALL)
        s = t.index("AI=CXRPGAITriggerWhenLevelUp")
        a = t.index("Action=CMultipleActionsAction", s) + len("Action=")
        e = lhbuild.balanced(t, a)
        call = B("CUseCannedActionAction", [("Canned Object", "Common Objects and Scripts/Fixt Companion Power Growth")])
        t = t[:a] + call.rstrip(CR) + t[e:]
        assert t.count("Fixt Companion Growth Watch") == 2
        t = t.replace("Fixt Companion Growth Watch", "Fixt Companion Power Watch")
        lhbuild.write_map(INSTALL, t)
        done.append(INSTALL)
    for rel in CALLERS:
        if add_call(rel):
            done.append(rel)
    if done:
        register(done)
    print("companion power growth:", len(done), "files")


if __name__ == "__main__":
    main()
