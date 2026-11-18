"""Relican offers the Da Vinci task once, and pays for its report once. Issue #15: "You can keep asking Relican about
Da Vinci joining the dark wielders even after the quest is accepted as if you didn't start the quest".

0.40.0 gave Relican's `5 Return Dialogue` three hand-written replies for `Convince DaVinci to Join the Dark Wielders`:

  * "You spoke of wizards who refuse you. What of Leonardo...?" -> `90 Fixt DaVinci task`, whose "I will go to him."
    activates the quest at `QD7XV2MK`. Gated only on `Relican Player has gotten started getting quests`, so it was
    offered forever, and taking it again pushed a finished quest back to its opening state, hiding the report replies
    and re-offering Da Vinci's side of it.
  * "Leonardo will not stand against you..." and "Leonardo refused you...", the report-backs. Gated on the joined
    (`RB4NW8TJ`) and refused (`ZH6PC3YF`) states being current. They complete the quest, and the joined one pays
    `Convince DaVinci to Dark Side XP`. Completing leaves that state current, so both could repeat, and the XP with them.

Each now carries a `Custom Requirement` beside its existing `Requirement`, in the CNotAction form vanilla uses:
the offer needs the quest never activated (`CWasQuestEverActivatedAction`), and the two reports need it not yet
completed (`CIsQuestCompletedAction`). A tree, so it reaches every save, including one that already re-took the task:
that save's quest is open again, so its report shows once more and then closes for good.

A rerun is a no-op.

    python tools/build_relican_davinci_gates.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR
from build_shrine_repairs import register

TREE = "Resources/Levels/1 Barcelona/Dialog/La Calle Perdida/Lord Relican.DialogTree"
QUEST = "Levels/1 Barcelona/Quests/Calle Perdida/Wielder Initiation Quests/Convince DaVinci to Join the Dark Wielders"


def never(check):
    return ("Custom Requirement=CActionExpression" + CR + "{" + CR + "Action=CNotAction" + CR + "{" + CR +
            "Action=" + check + CR + "{" + CR + "Quest=" + QUEST + CR + "}" + CR + "}" + CR + "}" + CR)


GATES = [
    ("Requirement=Relican Player has gotten started getting quests" + CR,
     "Reply Text=You spoke of wizards who refuse you. What of Leonardo, in the Gate District?" + CR,
     never("CWasQuestEverActivatedAction")),
    ("Requirement=Fixt DaVinci Joined" + CR,
     "Reply Text=Leonardo will not stand against you. He gave me his word on it." + CR,
     never("CIsQuestCompletedAction")),
    ("Requirement=Fixt DaVinci Refused" + CR,
     "Reply Text=Leonardo refused you. He will not be moved, and he asked me to turn back." + CR,
     never("CIsQuestCompletedAction")),
]


def build():
    t = lhbuild.read(TREE)
    n0 = t.count(CR)
    done, added = 0, 0
    for req, reply, gate in GATES:
        pair = req + reply
        if req + gate + reply in t:
            continue
        assert t.count(pair) == 1, "cannot pin %r" % reply
        t = t.replace(pair, req + gate + reply)
        done += 1
        added += gate.count(CR)
    if done:
        assert t.count(CR) == n0 + added, "line count is off"
        assert "\n" not in t.replace(CR, ""), "a bare LF crept in"
        (lhbuild.FX / TREE).write_bytes(t.encode("latin-1"))
        register([TREE])
    return done


def main():
    print("relican davinci gates:", build())


if __name__ == "__main__":
    main()
