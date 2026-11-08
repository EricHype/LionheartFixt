"""How the Druid Master ended now matters, and the shrine's inner halls are no longer silent.

`Stop the Druids` completes on arrival at England to Alamut, so nothing ever recorded what you did in Exalted Chambers.
Three scripting variables do now, each set where the thing happens: the talk-down relay, the spoiled-ambush relay, and her
can's death slot, which was blank and is not overridden by her generator. A fourth outcome, walking on with her alive, is
read as the quest done with none of the three.

They pay off twice. An ending slide, in four variants, joins the series before the companions. Each line was checked
against her tree and Sir Roger's: her circle, the dragon in the hill, Richard's grave and "do not come back to England" are
hers; the Queen keeping druids is his. And Sir Roger says one line at England to Alamut if he is with you.

Stone Chamber, the Antechamber and Exalted Chambers each give Roger and Grace one line on the first visit, if they are with
you. Neither says anything about the past that their own dialogue does not.

A rerun is a no-op.

    python tools/build_shrine_outcome.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, FX, balanced, delay, if_action, multi, relay
from build_epilogue_flow import ENDGAME, items, relay_span
from build_inquisition_slides import VARS, flag, say, var_if, write_var
from build_shrine_repairs import into_relay, register

SHRINE = "Levels/7 English Shrine/"
EXALTED = SHRINE + "05 Exalted Chambers.zax"
EXIT_MAP = SHRINE + "England to Alamut.zax"
MASTER_CAN = "Resources/Levels/7 English Shrine/Character Templates/Druid Master.can"
SLIDES = "Resources/Levels/8 Alamut/Dialog/Fixt Ending Slides.DialogTree"
QUEST = "Levels/7 English Shrine/Quests/Stop the Druids"
TALKED, SPOILED, KILLED = VARS + "Fixt Druid Master Talked Down", VARS + "Fixt Druid Ambush Spoiled", VARS + "Fixt Druid Master Killed"
RELAY = "Fixt order epilogue relay"
ROGER, GRACE = "Sir Roger Templeton", "Grace"
TREE = "Levels/7 English Shrine/Dialog/Fixt Shrine Companions"

SLIDE = {
    "900 order shrine talked": "The Druid Master put out her fires and let you walk out through the front of the shrine. She had told you not to come back to England. Her circle under the hill was never finished, and the dragon stayed stone. The druids kept the Queen's favour, and nobody in England charged them with anything. She kept the hill. As far as anyone knows, she kept her word.",
    "900 order shrine spoiled": "You counted the Druid Master's ambush before she could spring it, and then you killed her in her own circle. The men behind the wall never got their moment. The druids lost their master and their hill in one night, and the dragon stayed stone. The court in London called it a disturbance in the west. It sent nobody to ask what had been disturbed.",
    "900 order shrine killed": "You killed the Druid Master in the shrine where Richard is buried. Her circle stayed unfinished, and the dragon under the hill stayed stone. The druids who survived her went back to the Queen's protection, which had never been withdrawn. Within a generation they had another master and another hill. The court in London never mentioned the shrine at all.",
    "900 order shrine left": "You went on to Alamut with the Druid Master still in her shrine. Her circle was cut and her men were waiting. Whether the dragon woke is not recorded anywhere in England, because the Queen's druids recorded nothing for anyone. The hill is still there. Nobody local will graze sheep on it, and nobody will say why.",
}
LINES = {
    "1 roger stone": "Keep close, Lionheart. They have had weeks to dig in down here.",
    "2 grace stone": "All this stone and not a breath of wind. I hate it already.",
    "3 roger lore": "English halls, full of druids. One more thing my Queen will not explain.",
    "4 grace lore": "Books and candles. Somebody down here can read. That worries me more than the swords.",
    "5 roger exalted": "Whatever they are raising, it is close. I can feel it through the floor.",
    "6 grace exalted": "If this goes badly, I am not dying in a hole in England.",
    "10 roger talked": "You let her walk. The Queen will call that wisdom, Lionheart, and so will I, quietly.",
    "11 roger spoiled": "You heard them breathing behind a wall. Remind me never to hide from you.",
    "12 roger killed": "One less of the Queen's druids. She will not thank us for it.",
    "13 roger left": "We leave her standing? Then pray the dragon sleeps as soundly as the Queen does.",
}
REMARKS = {"03 Stone Chamber": ("1 roger stone", "2 grace stone"), "04 Antechamber of Lore": ("3 roger lore", "4 grace lore"),
           "05 Exalted Chambers": ("5 roger exalted", "6 grace exalted")}


def everyone(action):
    return ("CForEachPlayerAction", [("Action", action)])


def outcomes():
    z = lhbuild.read(EXALTED)
    if TALKED not in z:
        z = into_relay(z, "Fixt the Druid Master stands down", "Action=" + B(*everyone(flag(TALKED))), 1)
        z = into_relay(z, "Fixt the ambush is spoiled", "Action=" + B(*everyone(flag(SPOILED))), 1)
        lhbuild.write_map(EXALTED, z)
    c = lhbuild.read(MASTER_CAN)
    if KILLED not in c:
        x = "Destroyed Script Action=" + CR
        assert c.count(x) == 1
        c = c.replace(x, "Destroyed Script Action=" + B(*everyone(flag(KILLED))).rstrip() + CR)
        lhbuild.write_map(MASTER_CAN, c)
    for path, short, desc in ((TALKED, "Fixt Druid Master Talked Down", "1 means the player talked the Druid Master into putting out her fires."),
                              (SPOILED, "Fixt Druid Ambush Spoiled", "1 means the player named the Druid Master's ambush before she sprang it."),
                              (KILLED, "Fixt Druid Master Killed", "1 means the Druid Master died.")):
        write_var(path, short, desc)
        register(["Resources/" + path + ".DerivedCharacterAttribute"])


def slides():
    t = lhbuild.read(SLIDES)
    if "Node ID=900 order shrine talked" + CR in t:
        return
    reply = CR + "Requirement=!None" + CR + "Reply Text=" + CR + "Go to node ID=" + CR + "Custom Action=CTriggerRelayAction" + CR + "{" + CR + \
        "Relay Name=" + RELAY + CR + "}" + CR + "Is Default Reply=1" + CR
    add = "".join("-" * 60 + CR + "Node ID=" + n + CR + "Text=" + x + CR + "Should Have Voiceover=1" + CR + reply for n, x in SLIDE.items())
    end = t.rindex("}")
    (FX / SLIDES).write_bytes((t[:end] + add + t[end:]).encode("latin-1"))


def series_step():
    """After `order none`, before the companions. Killed outranks spoiled, because a spoiled ambush can still be walked away from."""
    z = lhbuild.read(ENDGAME)
    i, e = relay_span(z)
    p = z[i:e]
    if "900 order shrine" in p:
        return
    _, _, steps = items(p)
    k = next(n for n, s in enumerate(steps) if "Node ID=900 order none" in s) + 1
    on = ("CIsQuestCompletedAction", [("Quest", QUEST)])
    step = var_if(TALKED, say("900 order shrine talked"),
                  var_if(KILLED, var_if(SPOILED, say("900 order shrine spoiled"), say("900 order shrine killed")),
                         if_action(on, say("900 order shrine left"), delay("0.1", relay(RELAY)))))
    tabs = re.match(r"\t*", steps[k]).group(0)
    new = tabs + "Action=" + B(*step)
    q = p.replace(steps[k], new + steps[k], 1)
    m = re.search(r"Item Count=(\d+)\r\n", q[q.index("Action=CSeriesAction"):])
    s = q.index("Action=CSeriesAction") + m.start()
    q = q[:s] + "Item Count=" + str(int(m.group(1)) + 1) + CR + q[s + m.end() - m.start():]
    lhbuild.write_map(ENDGAME, z[:i] + q + z[e:])


def companion_tree():
    p = FX / ("Resources/" + TREE + ".DialogTree")
    if p.exists():
        return
    t = "CDialogTree" + CR + "{" + CR + "Name=" + CR + "Portrait=!None" + CR + "Should Have Voiceovers=0" + CR + "Default Canceled Node Action=" + CR
    for n, x in LINES.items():
        t += "-" * 60 + CR + lhbuild.node(n, x, [])
    p.write_bytes((t + "}" + CR).encode("latin-1"))
    register(["Resources/" + TREE + ".DialogTree"])


def line(who, node):
    alive = ("CIsAliveAction", [("Name To Check For", who), ("Desired Minimum Count", "1")])
    return if_action(alive, lhbuild.balloon(TREE, node, who, "-80"))


def once_on_arrival(name, action, x, y):
    timer = ("CRepeatTimerTriggerAI", [("Marked For Deletion", "0"), ("Publisher", ""),
                                       ("Action", multi([action, ("CDeactivateAction", [("Target Name", name)])])),
                                       ("Delay Between Actions", "600"), ("Plus or Minus", "0"), ("Seconds Till Next Execute", "3")])
    return lhbuild.entity(name, "1", [timer], "Editor/Position Marker", x, y)


def remarks():
    for m, (roger, grace) in REMARKS.items():
        rel = SHRINE + m + ".zax"
        z = lhbuild.read(rel)
        name = "Fixt companions remark"
        if "Name=" + name + CR in z:
            continue
        lhbuild.write_map(rel, lhbuild.add_parts(z, [once_on_arrival(name, multi([line(ROGER, roger), delay("4", line(GRACE, grace))]), 60, 60)]))
    z = lhbuild.read(EXIT_MAP)
    name = "Fixt Roger on the druids"
    if "Name=" + name + CR not in z:
        said = var_if(TALKED, line(ROGER, "10 roger talked"),
                      var_if(KILLED, var_if(SPOILED, line(ROGER, "11 roger spoiled"), line(ROGER, "12 roger killed")), line(ROGER, "13 roger left")))
        lhbuild.write_map(EXIT_MAP, lhbuild.add_parts(z, [once_on_arrival(name, said, 60, 60)]))
    register([EXIT_MAP])  # vanilla until now, so the manifest has never listed it


def main():
    outcomes()
    slides()
    series_step()
    companion_tree()
    remarks()
    print("shrine outcome wired")


if __name__ == "__main__":
    main()
