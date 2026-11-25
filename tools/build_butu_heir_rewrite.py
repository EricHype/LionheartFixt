"""Hrargrub's lines rewritten, and taking off the Khan's mark means it. Reported: "i opted to take off the kahn's mark when
bhutu asked. It didn't affect my perks? Also Bhutu's dialog is bad", then: "it should happen when you say it, but you
should be made aware of what the choice is going to do", and of the opening: "He's not a teenager moping he's not
popular, he's the heir of a different kahn trying to rival the current leader".

  * **The mark.** *"I will take it off."* went to the rank speech and did nothing; the standing only changed when the book
    was settled (`Join Butus Line`). It now opens `35 Fixt the cost of the mark`, which names the price (Plumdjum's
    goblins call you traitor, the Khan never stands with you again, Grumdjum will not follow), and only *"I take off
    his mark."* runs `Join Butus Line` there and then, into `36 Fixt the mark is off`. The book's own call stays; the
    can is guarded, so a second run does nothing.
  * **The voice.** Every line is shorter and plainer, nearer vanilla's goblins, with at most one stage direction. The Khan
    stays *Plumdjum*, vanilla's spelling nine times in ten. Hrargrub is a rival claimant, not a grievance.

A tree edit: every save. A rerun is a no-op.

    python tools/build_butu_heir_rewrite.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, DASH
from build_shrine_repairs import register

TREE = "Resources/Levels/Wilderness/Dialog/Fixt Butu Heir.DialogTree"
COST = "35 Fixt the cost of the mark"
OFF = "36 Fixt the mark is off"
TEXT = {
    "1 the heir challenges you": "Stop there, morsel. <Red bows rise all around you.> I am Hrargrub, son of Butu Khan, and Khan after him by right. This cave is mine. The east rock is mine. Soon the Warrens will be mine, and Plumdjum will learn whose chair he has been warming. Speak carefully. I am deciding whether you are useful or dinner.",
    "20 you emptied the chair": "Dead? <He sags, then straightens.> Six winters I planned to kill him, and you did it in an afternoon. Fine. The chair is empty, and I am standing next to it.",
    "30 take off his mark": "His Champion. Then Plumdjum sent you. Take off his mark and we talk. Keep it, and my people take it off you the hard way.",
    "40 he gives everyone ranks": "A rank. Plumdjum hands out ranks the way he hands out speeches, and both cost him nothing. Butu gave his goblins poems, and he kept his word.",
    "50 a qualification": "You have killed more of Plumdjum's goblins than I have. I do not like you. I am very interested in you.",
    "60 who was butu": "Khan of this horde, before Plumdjum. Plumdjum took the Warrens from him, and took his book of poems as a trophy, to show the clan who rules now. My father's goblins followed me to this cave. We have waited six winters. We are done waiting.",
    "90 the book": "Butu's book of poems. Plumdjum keeps it in the Warrens with his gold and does not know what it is. Humans in the city buy such things by weight. Bring it to me, and this cave is yours to walk.",
    "95 agreed": "Then go and find it. My people know your face now. They will let you pass, for now.",
    "100 the book returned": "<He takes the book in both hands and does not open it.> Butu's. This cave is Butu's again, and you may walk it. Go tell Plumdjum who holds his east rock now, if he still speaks to you.",
    "70 combat": "Good. Butu's goblins never needed a plan.",
    "80 go then": "Then walk out. My people will watch you to the door. Come back with your blade out and they will not just watch.",
    "101 the collector": "A collector. A human who keeps words he cannot eat. Then Butu is read in a city that never heard of him, which is further than Plumdjum ever carried anything. Walk where you like, morsel. I did not expect that answer from you.",
    "102 the price of poems": "Sold. <He holds out a flat hand.> Then pay me what they paid you, and we will both know what my Khan was worth to you. Two hundred and fifty gold. A human picked the number. You took it.",
    COST: "Know what that costs before you say it twice. Plumdjum's goblins will call you traitor from now on. Plumdjum himself will never stand with you again, and his clever Grumdjum will not follow you anywhere.",
    OFF: "Good. <Red bows lower around you.> Then you are nobody's Champion, morsel, which makes two of us. Now we can talk.",
}
REPLIES = [("Then your people can decide.", "Then we fight.")]
for v in list(TEXT.values()) + [r for _, r in REPLIES]:
    assert "—" not in v and "--" not in v and v.count("<") <= 1, v


def build():
    t = lhbuild.read(TREE)
    if "Node ID=" + COST + CR in t:
        return []
    for nid, text in TEXT.items():
        if nid in (COST, OFF):
            continue
        s = t.index(CR + "Node ID=" + nid + CR) + len(CR)
        a = t.index("Text=", s)
        assert a == s + len("Node ID=" + nid + CR), nid
        e = t.index(CR, a)
        t = t[:a] + "Text=" + text + t[e:]
    for old, new in REPLIES:
        assert t.count("Reply Text=" + old + CR) == 1
        t = t.replace("Reply Text=" + old + CR, "Reply Text=" + new + CR)
    s = t.index(CR + "Node ID=30 take off his mark" + CR)
    old = "Reply Text=I will take it off." + CR + "Go to node ID=40 he gives everyone ranks" + CR
    k = t.index(old, s)
    t = t[:k] + "Reply Text=I will take it off." + CR + "Go to node ID=" + COST + CR + t[k + len(old):]
    join = ("CUseCannedActionAction", [("Canned Object", "Levels/Wilderness/Quests/Join Butus Line")])
    cost = lhbuild.node(COST, TEXT[COST], [
        {"text": "I take off his mark. (You lose the Champion title and become a Goblin Traitor.)", "go": OFF, "action": join,
         "icon": "Quest Icon"},
        {"text": "Then I keep it.", "go": "70 combat", "icon": "Fight Icon"},
        {"text": "Let me think on it.", "go": "80 go then", "icon": "Exit Icon", "default": True}])
    off = lhbuild.node(OFF, TEXT[OFF], [{"text": "", "go": "90 the book", "default": True}])
    assert t.endswith("}" + CR)
    t = t[:-len("}" + CR)].rstrip(CR) + CR + CR + DASH + CR + cost + DASH + CR + off + "}" + CR
    (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
    assert "Plumjum" not in t
    return [TREE]


def main():
    done = build()
    if done:
        register(done)
    print("butu heir rewrite:", done)


if __name__ == "__main__":
    main()
