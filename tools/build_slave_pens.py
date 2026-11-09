"""Captives in the Slave Pits. The game had a slaver camp with no slaves in it, and you were the only one it showed.

Five stand in the yard where you were sold, each decided alone: Don Alfonso de Cardona, two Sylvants and two goblins.
They arrive with the Part 2 slavers when you come back, because the map's opening must stay as it was. Free, sell or
kill, and selling needs the Inquisition's buyer, who is not there for a character the Inquisition already hunts.

Every captive is the clean `Tainted sylvant` can with a model, a name and a weak race, because that can carries no
talk specifier of its own. Karma on a kill sits in the can's death script, so a sword does what the reply does, and
goes through `Player#1-9#` because $Instigator in a death script is the corpse. Spots are ones the opening itself
spawns on, in the yard. Only the noble reaches the end slides.

Two guards do not depend on unproven engine behaviour. Each captive's `Gone` flag is set before the CDeleteAction, and
the death script checks it, so a freed captive is never scored as a kill even if a delete runs that script. `Placed`
makes the spawn action a one-shot, because it fires on every entry through the same door.

Each stage checks whether it has already run, so a rerun is a no-op.

    python tools/build_slave_pens.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, activate, balanced, exists, if_action, multi, node, relay
from build_inquisition_slides import ENDGAME, SLIDES, VARS, flag, say, var_if, write_var
from build_inquisition_turns import HOSTILE

MAP = "Levels/1 Barcelona/Slave Pits.zax"
TREE_PATH = "Levels/Wilderness/Dialog/Fixt Slave Pit Captives"
TREE = "Resources/" + TREE_PATH + ".DialogTree"
BASE = "Resources/Levels/1 Barcelona/Character Templates/Port District/Tainted sylvant.can"
FEMALE = "Resources/Levels/1 Barcelona/Character Templates/Port District/Tainted Sylvant Female.can"
FOLDER = "Levels/Wilderness/Character Templates/"
GEN = "Fixt Captive generator"
BUYER = "Fixt Slave Buyer"
FREED, SOLD, KILLED = VARS + "Fixt Noble Freed", VARS + "Fixt Noble Sold", VARS + "Fixt Noble Killed"
PLACED = VARS + "Fixt Captives Placed"
GOBLIN = "Characters/Monsters/Mongol Goblin"

CAPTIVES = {
    # key: spawn name, can base, model, shown name, position, karma (free, sold, killed), gold (free, sold)
    "noble": ("Fixt Captive Noble", BASE, "Characters/NPC/Barcelona/Generic Townspeople/Merchant Generic03", "Don Alfonso de Cardona", (1248, 1288), (50, -75, -100), (300, 750)),
    "sylvant1": ("Fixt Captive Sylvant 1", BASE, None, "Sylvant", (1075, 1216), (75, -100, -125), (0, 200)),
    "sylvant2": ("Fixt Captive Sylvant 2", FEMALE, None, "Sylvant", (1376, 1200), (75, -100, -125), (0, 200)),
    "goblin1": ("Fixt Captive Goblin 1", BASE, GOBLIN, "Goblin", (1412, 1206), (25, -25, -25), (0, 75)),
    "goblin2": ("Fixt Captive Goblin 2", BASE, GOBLIN, "Goblin", (894, 1156), (25, -25, -25), (0, 75)),
}

LINES = {
    "noble": ("You there. I am Don Alfonso de Cardona, and these animals have held me four months for a ransom my family will not pay fast enough. Open this. My house will remember you.",
              "You have the word of a Cardona. That is worth more than you know. <He presses a hidden purse into your hand, and he is gone.>",
              "You cannot. Do you know who I am? Do you know what they will do to--"),
    "sylvant1": ("Do not look at me like that. I know what I am, and so did the man who sold me. Have you come to buy, or to stare?",
                 "The fire in my blood has cost me everything I ever had. You are the first who did not ask me to pay for it.",
                 "Of course. The Inquisition pays by the head, and it is always my kind."),
    "sylvant2": ("They took my daughter to the ship and left me here. If you have a key, use it. If you have not, walk on.",
                 "She sailed for Marseilles. I will find her.",
                 "<She says nothing at all, and looks at you until you look away.>"),
    "goblin1": ("Morsel, mind this chain of mine. I was told on brains I soon would dine. Now a priest has come to name my price. Break it, and I shall call you nice.",
                "You are as ugly as the rest of your race, but I shall not forget your face.",
                "The Holy Office has no taste. Such a fine brain, gone to waste."),
    "goblin2": ("Nine of us came here on this chain. Two are left. Now count again. The man who feeds us wears a knife. Spare a goblin one more life.",
                "Khara'Khorum will hear of you, though no one there will think it true.",
                "Sold twice this year, for less each time. A falling price is the only crime."),
}

SLIDE_TEXT = {
    "900 order pits freed": ("Don Alfonso de Cardona went home, and his family's gratitude lasted longer than most. He told the story of the slave pits at table for thirty years. In his version he broke the chain himself. Your name came up once a year, at the feast of his return, and the house of Cardona paid for one mass in it. Nobody there knew what you had been doing in that yard."),
    "900 order pits sold": ("Don Alfonso de Cardona was entered in the Holy Office's ledger as a heretic, which was cheaper than admitting what he was worth. His family paid a ransom for two years to men who no longer had him. You had the money by then. The house of Cardona never learned who sold him. It is still looking."),
    "900 order pits killed": ("Don Alfonso de Cardona was found in the yard of the slave pits with his chain still on. The house of Cardona paid for the search, for the mass, and for a man to ask questions along the western road. He was good at his work. He got as far as a name. He never got a face to go with it."),
}


def gone_var(key):
    return VARS + "Fixt Captive " + key.capitalize() + " Gone"


def karma(n, who="$Instigator"):
    return ("CAddCharacterModifierToCharacterAction", [
        ("Modifier Description", ""), ("Modification is permanent", "0"), ("Character to modify", who),
        ("Modifiers", ("Array", [("Item Count", "1"), ("Modifier", ("CCharacterModifierDerivedAttribute", [
            ("Modification Amount", ("CConstant", [("Constant Value", str(n))])), ("Modification amount is a percent", "0"),
            ("Allow Accumulation", "1"), ("Derived character attribute to modify", "Derived Character Attributes/Karma")]))])),
        ("OPTIONAL Duration", ""), ("Expression Context", "$Instigator")])


def gone(name):
    return ("CDeleteAction", [("Target Name", name)])


def pay(n):
    return ("CGiveMoneyAction", [("Give to", "$instigator"), ("Value to give", str(n))])


def cans():
    for key, (name, base, model, shown, _, kar, _) in CAPTIVES.items():
        rel = "Resources/" + FOLDER + name + ".can"
        if (FX / rel).exists():
            continue
        z = lhbuild.read(base)
        z, n = re.subn(r"(User Assigned Name=)[^\r\n]*", lambda m: m.group(1) + shown, z, count=1)
        assert n == 1
        z, n = re.subn(r"(\bRace=)Races/NPCs/Generic Human", r"\1Races/NPCs/Weak Prisoner more hit points", z)
        assert n == 1
        if model:
            z, n = re.subn(r"(\t\tModel=)[^\r\n]*", lambda m: m.group(1) + model, z)
            assert n == 1
        if model == GOBLIN:
            z = z.replace("Sequence Name=AttackPunch", "Sequence Name=Attack")
            for old, new in (("Pain.ogg", "pain.ogg"), ("Pain2.ogg", "pain2.ogg"), ("Pain3.ogg", "pain3.ogg")):
                z = z.replace("Sound=Enemies/People/Male " + old, "Sound=Enemies/Mongol Goblins/Goblin " + new)
        acts = [karma(kar[2], "Player#1-9#")]
        if key == "noble":
            acts.append(("CForEachPlayerAction", [("Action", flag(KILLED))]))
        i = z.index("Destroyed Script Action=" + CR)
        z = z[:i] + "Destroyed Script Action=" + B(*var_if(gone_var(key), "", multi(acts))) + z[i + len("Destroyed Script Action=" + CR):]
        lhbuild.write_map(rel, z)


def tree():
    # 0.99.1's fact-check rewrote lines in the shipped tree, so it is the authority now; a rerun must not restore these
    if (FX / TREE).exists():
        return
    nodes = []
    buyer = "CActionExpression" + CR + "{" + CR + "Action=" + B(*exists(BUYER)) + "}" + CR
    for key, (name, _, _, shown, _, kar, gold) in CAPTIVES.items():
        hello, thanks, doomed = LINES[key]
        him = "him"
        if key == "sylvant2":
            him = "her"
        left = ("CForEachPlayerAction", [("Action", flag(gone_var(key)))])
        free = [left, karma(kar[0])] + ([pay(gold[0])] if gold[0] else [])
        if key == "noble":
            free.append(flag(FREED))
        sold = [left, karma(kar[1]), pay(gold[1])] + ([flag(SOLD)] if key == "noble" else [])
        kill = ("CActionDoDamage", [("Character Doing Damage", "$instigator"), ("Character To Damage", name), ("Defend Against", "0"),
                                    ("No Friendly Fire Check", "1"),
                                    ("Damages", ("Array", [("Item Count", "1"), ("Damage", ("CXRPGDamage", [
                                        ("Damage Type", "Damage Types/Piercing"), ("Damage Amount", ("CConstant", [("Constant Value", "9999")]))]))]))])
        nodes.append(node(f"{key} hello", hello, [
            {"text": "<Break the chain.> Go.", "go": f"{key} freed", "action": multi(free), "default": True},
            {"creq": buyer, "text": "<Call the Inquisition's buyer over.>", "go": f"{key} sold", "action": multi(sold)},
            {"text": f"<Kill {him} where {'she' if him == 'her' else 'he'} stands.>", "action": kill, "icon": "Fight Icon"},
            {"text": "<Leave.>", "icon": "Exit Icon"}]))
        nodes.append(node(f"{key} freed", thanks, [{"text": "", "action": gone(name), "default": True}]))
        nodes.append(node(f"{key} sold", doomed, [{"text": "", "action": gone(name), "default": True}]))
    (FX / TREE).parent.mkdir(parents=True, exist_ok=True)
    z = lhbuild.tree("Captive", nodes)
    assert z.count(CR) == z.count("\n")
    (FX / TREE).write_bytes(z.encode("latin-1"))


def pits():
    z = lhbuild.read(MAP)
    if GEN in z:
        return
    parts = []
    for key, (name, _, _, _, pos, _, _) in CAPTIVES.items():
        talk = lhbuild.specifier("GetCloseThenTalk", lhbuild.dialog(TREE_PATH, f"{key} hello", "$trigger"), radius="100")
        parts.append(lhbuild.generator(GEN, "0", FOLDER + name, name, "", pos[0], pos[1], ais=[talk]))
    parts.append(lhbuild.generator(BUYER + " generator", "0", "Levels/Start Game/Character Templates/Inquisitor Buying Player", BUYER, "", 1304, 1276))
    i = z.index("\t\t\tName=From Slave Pit Exterior" + CR)
    j = z.index("Per Party Spawn Action=CMultipleActionsAction", i)
    k = z.index("Item Count=7" + CR, j)
    assert k - j < 120
    once = multi([("CForEachPlayerAction", [("Action", flag(PLACED))]), activate(GEN), var_if(HOSTILE, "", activate(BUYER + " generator"))])
    add = "Action=" + B(*var_if(PLACED, "", once))
    z = z[:k] + "Item Count=8" + CR + add + z[k + len("Item Count=7" + CR):]
    lhbuild.write_map(MAP, lhbuild.add_parts(z, parts))


def slides():
    z = lhbuild.read(SLIDES)
    if "900 order pits freed" in z:
        return
    add = ""
    for nid, text in SLIDE_TEXT.items():
        add += ("Node ID=" + nid + CR + "Text=" + text + CR + "Should Have Voiceover=1" + CR + CR +
                "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=" + CR +
                "Custom Action=" + B(*relay("Fixt order epilogue relay")) + "Is Default Reply=1" + CR + "-" * 60 + CR)
    key = "Node ID=900 order none" + CR
    assert z.count(key) == 1
    z = z.replace(key, add + key)
    assert z.count(CR) == z.count("\n")
    (FX / SLIDES).write_bytes(z.encode("latin-1"))


def endgame():
    z = lhbuild.read(ENDGAME)
    if "900 order pits freed" in z:
        return
    action = var_if(KILLED, say("900 order pits killed"),
                    var_if(SOLD, say("900 order pits sold"),
                           var_if(FREED, say("900 order pits freed"), relay("Fixt order epilogue relay"))))
    k = z.index("Node ID=900 order horde traitor")
    s = z.rindex("\t" * 7 + "Action=C", 0, k)
    z = z[:s] + "\t" * 7 + "Action=" + B(*action) + z[s:]
    a = z.index("\t\t\tName=Fixt order epilogue relay" + CR)
    i = z.index("Item Count=31" + CR, a)
    assert i - a < 900
    z = z[:i] + "Item Count=32" + z[i + len("Item Count=31"):]
    lhbuild.write_map(ENDGAME, z)


def main():
    write_var(FREED, "Fixt Noble Freed", "1 means the player freed Don Alfonso de Cardona.")
    write_var(SOLD, "Fixt Noble Sold", "1 means the player sold Don Alfonso de Cardona to the Inquisition.")
    write_var(KILLED, "Fixt Noble Killed", "1 means Don Alfonso de Cardona was killed.")
    write_var(PLACED, "Fixt Captives Placed", "1 means the Slave Pits captives have been spawned.")
    for key, (_, _, _, shown, _, _, _) in CAPTIVES.items():
        write_var(gone_var(key), "Fixt Captive " + key.capitalize() + " Gone", "1 means this Slave Pits captive was freed or sold, so a later delete is not a kill.")
    cans()
    tree()
    pits()
    slides()
    endgame()


if __name__ == "__main__":
    main()
