"""The wands' attack spells fly at what you aim at again. Reported: "when i used the lighting wand I bought, it caused
damage to me and not the target", and "there was also no lightning bolt graphic when casted".

0.88.0 put every wand on one system: the wand pins a copy of the spell under `Skills/Fake Wand Spells/`, and the copy's
`Launch Action` checks for a `Wand Charge`, delivers the effect and spends it. The launcher went, because a launcher fires
around that gate (docs/engine-notes.md, "A launcher delivers its effect around the gate"). But in a launch action
`$Trigger` is the caster: vanilla `Lightning Chain` says "within a radius of the caster" and centres its oval on
`$Trigger`, as do `Electrical Burst` and `Exorcise`. No vanilla spell reaches a target or a spot without a projectile.
So the copies hit their caster:

| copy | delivered by | so |
|---|---|---|
| Lightning Bolt, Spike | `CActionDoDamage` on `$Trigger` | the wielder takes the bolt; nothing is drawn, since the bolt was the projectile |
| Poison Touch | `CActionDoDamage` (poison over time) on `$Trigger` | the wielder is poisoned |
| Fireball, Ice Storm, Insect Plague, Fire Circle | an oval on `$Instigator` | bursts round the wielder, not "the targeted area" |

Poison Ring's oval round the caster is right ("around the caster") and is left alone.

The fix gives each its vanilla projectile back, as a Fixt copy (`Spell Projectiles/Fixt Wand <spell>`) that reads the
wand spell's expressions instead of the player's skill, and moves the gate onto the projectile:

  * **Cast.** The copy's gated payload loses its delivery item and gains an arm instead: a 2.4 s `Fixt Wand Armed` on
    the caster. The charge is spent and *"The wand discharges."* shown as before; *"The wand has no charges left"* still
    answers an empty wand. The vanilla launcher is restored, launching the Fixt projectile.
  * **Hit.** Every `Hit Action` in the projectile runs only if its shooter (`$Instigator`) holds a charge or is armed.
    Either order of cast and hit therefore works: a hit before the cast sees the charge, a hit after sees the arm. 2.4 s
    is under the 2.5 s recast lock every damage copy carries, so an empty wand cannot ride a previous cast's arm.
  * **Damage plugins.** `Spike Projectile` and `Poison Spike Projectile` deal their damage from `CPlugInBehaviorDamage`,
    outside any hit action, so the gate could not hold it. The copies deal the same damage from the hit action instead.
  * **Poison Touch** has no vanilla spell; it flies Poison Ring's single spike, with its own poison and effect in the
    hit, and targets a creature like Spike.

Skills and projectiles are resources, and a wand casts its copy, so every wand in every save. A rerun is a no-op.

    python tools/build_wand_projectiles.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, balanced
from build_shrine_repairs import register

FAKE = "Skills/Fake Wand Spells/"
PROJ = "Resources/Spell Projectiles/"
VARS = "Resources/Derived Character Attributes/Game Scripting Variables/"
ARMED = "Fixt Wand Armed"
GSV = "Derived Character Attributes/Game Scripting Variables/"
CHARGE = "Inventory Items/Wand Charge"
ARM_SECONDS = "2.4"  # under the 2.5 s recast lock of every damage copy
# copy: (vanilla spell whose launcher and projectile it takes, the vanilla projectile, the skill that projectile reads)
SPELLS = {
    "Lightning Bolt": ("Magic Thought/Offensive/Lightning Bolt", "Lighting Bolt Instant Projectile", "Magic Thought/Offensive/Lightning Bolt"),
    "Spike": ("Magic Thought/Offensive/Spike", "Spike Projectile", "Magic Thought/Offensive/Spike"),
    "Fireball": ("Magic Thought/Offensive/Fireball", "Fire Ball Projectile", "Magic Thought/Offensive/Fireball"),
    "Ice Storm": ("Magic Thought/Offensive/Ice Storm", "Ice Storm Instant Hit", "Magic Thought/Offensive/Ice Storm"),
    "Insect Plague": ("Magic Tribal/Offensive/Insect Plague", "Insect Plague Instant Hit Projectile", "Magic Tribal/Offensive/Insect Plague"),
    "Fire Circle": ("Magic Thought/Offensive/Fire Circle", "Fire Circle Instant Hit Projectile", "Magic Thought/Offensive/Fire Circle"),
    "Poison Touch": ("Magic Thought/Offensive/Spike", "Poison Spike Projectile", "Magic Thought/Offensive/Poison Ring"),
}
DELIVERY = {"CActionDoDamage", "CAddAIAction"}


def flat(s):
    """Strip indentation; resource_format re-indents on write."""
    return re.sub(r"(?m)^\t+", "", s)


def items_at(t, a):
    """The top-level items of the Array whose `Item Count=` is at index a: [(start, end)], end after the CR."""
    m = re.compile(r"Item Count=(\d+)\r\n").match(t, a)
    pos, out = m.end(), []
    for _ in range(int(m.group(1))):
        assert t.startswith("Action=", pos), t[pos:pos + 80]
        e = balanced(t, pos)
        out.append((pos, e + len(CR)))
        pos = e + len(CR)
    assert t.startswith("}" + CR, pos), t[pos:pos + 80]
    return m, out


def has_charge():
    return ("CActionCheckForInventoryItem", [("Who to give check", "$Instigator"), ("Inventory Item To Check For", CHARGE)])


def is_armed():
    return ("CExpressionAction", [("Expression", ("CIsEqualTo", [
        ("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", GSV + ARMED)])), ("Operator", ""),
        ("Operand2", ("CConstant", [("Constant Value", "1")]))])), ("Character to get attributes from", "$Instigator")])


def arm():
    return ("CAddCharacterModifierToCharacterAction", [
        ("Modifier Description", ARMED), ("Modification is permanent", "0"), ("Character to modify", "$Instigator"),
        ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
            ("Modification Amount", ("CConstant", [("Constant Value", "1")])), ("Modification amount is a percent", "0"),
            ("Allow Accumulation", "0"), ("Derived character attribute to modify", GSV + ARMED)]))])),
        ("OPTIONAL Duration", ("CConstant", [("Constant Value", ARM_SECONDS)])), ("Expression Context", "$Instigator")])


def gated(raw):
    """`raw` (an action value, flat, ending CR) run only if the shooter holds a charge or is armed."""
    def ifa(cond, then, els):
        return ("CIfAction" + CR + "{" + CR + "If=" + B(*cond) + "Then=" + then + "Else=" + els +
                "Return failure if the If failes=0" + CR + "}" + CR)
    return ifa(has_charge(), raw, ifa(is_armed(), raw, CR))


def gate_hit_actions(t):
    """Wrap every non-empty `Hit Action=` value in the gate. Returns (text, count)."""
    out, pos, n = [], 0, 0
    for m in re.finditer(r"(?m)^Hit Action=(C\w+)", t):
        v = m.start() + len("Hit Action=")
        e = balanced(t, v)
        out.append(t[pos:v] + gated(t[v:e] + CR).rstrip(CR))
        pos = e
        n += 1
    return "".join(out) + t[pos:], n


def damage_plugin_to_hit(t):
    """`CPlugInBehaviorDamage`'s damages become a `CActionDoDamage` on the target, last in the projectile's hit action."""
    k = t.index("PlugIn Behavior=CPlugInBehaviorDamage" + CR)
    e = balanced(t, k)
    plug = t[k:e]
    d = plug.index("Damages=Array" + CR)
    damages = plug[d + len("Damages="):balanced(plug, d)] + CR
    t = t[:k] + t[e + len(CR):]
    c = t.index("Item Count=", t.index("PlugIn Behaviors=Array"))
    m = re.compile(r"Item Count=(\d+)").match(t, c)
    t = t[:c] + "Item Count=" + str(int(m.group(1)) - 1) + t[m.end():]
    hit = ("CActionDoDamage" + CR + "{" + CR + "Character Doing Damage=$Instigator" + CR + "Character To Damage=$Trigger" + CR +
           "Defend Against=1" + CR + "No Friendly Fire Check=0" + CR + "Damages=" + damages + "}" + CR)
    return add_to_first_hit(t, [hit])


def add_to_first_hit(t, raw_actions):
    """Append raw actions to the first `Hit Action`, making it a CMultipleActionsAction if it is not one."""
    m = re.search(r"(?m)^Hit Action=(C\w+)", t)
    v = m.start() + len("Hit Action=")
    e = balanced(t, v)
    old = t[v:e] + CR
    if m.group(1) == "CMultipleActionsAction":
        a = old.index("Item Count=")
        mm, its = items_at(old, a)
        end = its[-1][1]
        new = old[:a] + "Item Count=" + str(len(its) + len(raw_actions)) + CR + old[mm.end():end] + \
            "".join("Action=" + r for r in raw_actions) + old[end:]
    else:
        new = ("CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=" + str(1 + len(raw_actions)) + CR +
               "Action=" + old + "".join("Action=" + r for r in raw_actions) + "}" + CR + "}" + CR)
    return t[:v] + new.rstrip(CR) + t[e:]


def build_projectile(copy, vanilla_proj, reads, extra_hit=None, replace_hit=False):
    rel = PROJ + "Fixt Wand " + copy + ".InventoryItem"
    t = flat(lhbuild.zf.read(PROJ + vanilla_proj + ".InventoryItem").decode("latin-1"))
    t = re.sub(r"(?m)^Object ID=[^\r\n]*\r\n", "", t)
    n_reads = t.count("Skill=Skills/" + reads + CR)
    t = t.replace("Skill=Skills/" + reads + CR, "Skill=" + FAKE + copy + CR)
    # CVariableSpellDuration names the spell too; the wand spells already read their own, so the projectile does
    t = t.replace("Spell=Skills/" + reads + CR, "Spell=" + FAKE + copy + CR)
    if replace_hit:
        # Poison Touch: the spike's own delayed Poison Ring damage is not this spell's; its hit is the copy's poison
        t = re.sub(r"(?m)^(Hit Action=)", r"\1", t)
        m = re.search(r"(?m)^Hit Action=(C\w+)", t)
        v = m.start() + len("Hit Action=")
        e = balanced(t, v)
        t = t[:v] + "CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR + "Item Count=" + str(len(extra_hit)) + CR + \
            "".join("Action=" + r for r in extra_hit) + "}" + CR + "}" + t[e:]
    if "PlugIn Behavior=CPlugInBehaviorDamage" + CR in t:
        if replace_hit:
            k = t.index("PlugIn Behavior=CPlugInBehaviorDamage" + CR)
            t = t[:k] + t[balanced(t, k) + len(CR):]
            c = t.index("Item Count=", t.index("PlugIn Behaviors=Array"))
            mc = re.compile(r"Item Count=(\d+)").match(t, c)
            t = t[:c] + "Item Count=" + str(int(mc.group(1)) - 1) + t[mc.end():]
        else:
            t = damage_plugin_to_hit(t)
    t, gates = gate_hit_actions(t)
    assert gates >= 1 and "Skills/" + reads + CR not in t and "Skills/Magic " not in t, (copy, gates)
    lhbuild.write_map(rel, t)
    return rel, n_reads, gates


def launcher_from(vanilla_spell, projectile):
    t = flat(lhbuild.zf.read("Resources/Skills/" + vanilla_spell + ".Skill").decode("latin-1"))
    k = t.index("PlugIn Behavior=CXRPGPlugInBehaviorLauncher" + CR)
    plug = re.sub(r"(?m)^Object ID=[^\r\n]*\r\n", "", t[k:balanced(t, k)]) + CR
    olds = re.findall(r"Secondary Launchable Type=([^\r\n]*)", plug)
    assert len(olds) == 1, olds
    return plug.replace("Secondary Launchable Type=" + olds[0] + CR, "Secondary Launchable Type=Spell Projectiles/Fixt Wand " + projectile + CR)


def build_skill(copy, vanilla_spell):
    """Returns (rel, the delivery actions taken out, for a copy whose projectile carries them)."""
    rel = "Resources/" + FAKE + copy + ".Skill"
    t = flat(lhbuild.read(rel))
    t = re.sub(r"(?m)^Object ID=[^\r\n]*\r\n", "", t)
    i = t.index("Then=CMultipleActionsAction" + CR, t.index("Launch Action=CIfAction" + CR))
    a = t.index("Item Count=", i)
    m, its = items_at(t, a)
    taken = [t[s + len("Action="):e] for s, e in its if re.match(r"Action=(C\w+)", t[s:e]).group(1) in DELIVERY]
    moved = [t[s + len("Action="):e] for s, e in its if copy == "Poison Touch" and t[s:e].startswith("Action=CSpawnEffectAction")]
    keep = [t[s:e] for s, e in its if re.match(r"Action=(C\w+)", t[s:e]).group(1) not in DELIVERY and not
            (copy == "Poison Touch" and t[s:e].startswith("Action=CSpawnEffectAction"))]
    assert len(taken) == 1, (copy, len(taken))
    body = ["Action=" + B(*arm())] + keep
    t = t[:a] + "Item Count=" + str(len(body)) + CR + "".join(body) + t[its[-1][1]:]
    # the vanilla launcher, launching the Fixt projectile
    p = t.index("PlugIn Behaviors=Array" + CR)
    c = t.index("Item Count=", p)
    mc = re.compile(r"Item Count=(\d+)\r\n").match(t, c)
    t = t[:c] + "Item Count=" + str(int(mc.group(1)) + 1) + CR + t[mc.end():]
    close = balanced(t, p + len("PlugIn Behaviors=")) - 1  # the array's closing brace: the launcher goes last, as in vanilla
    assert t[close] == "}" and t[close - len(CR):close] == CR, t[close - 20:close + 5]
    t = t[:close] + launcher_from(vanilla_spell, copy) + t[close:]
    if copy == "Poison Touch":
        assert t.count("Is Location Based=1" + CR) == 1
        t = t.replace("Is Location Based=1" + CR, "Is Location Based=0" + CR)  # a creature, as Spike
    lhbuild.write_map(rel, t)
    return rel, taken, moved


def build_var():
    rel = VARS + ARMED + ".DerivedCharacterAttribute"
    if (lhbuild.FX / rel).exists():
        return []
    v = lhbuild.read(VARS + "Esteban Dead.DerivedCharacterAttribute").replace("Esteban Dead", ARMED)
    v = v.replace("Description=" + CR, "Description=1 for 2.4 s after a wand spell spent a charge; its projectile reads it." + CR)
    (lhbuild.FX / rel).write_bytes(v.encode("latin-1"))
    return [rel]


def main():
    done = build_var()
    for copy, (vanilla_spell, vproj, reads) in SPELLS.items():
        if "CXRPGPlugInBehaviorLauncher" in lhbuild.read("Resources/" + FAKE + copy + ".Skill"):
            continue
        srel, taken, moved = build_skill(copy, vanilla_spell)
        if copy == "Poison Touch":
            prel, n, g = build_projectile(copy, vproj, reads, extra_hit=taken + moved, replace_hit=True)
        else:
            prel, n, g = build_projectile(copy, vproj, reads)
        print("  ", copy, "| projectile reads repointed:", n, "| hit actions gated:", g)
        done += [srel, prel]
    if done:
        register(done)
    print("wand projectiles:", done)


if __name__ == "__main__":
    main()
