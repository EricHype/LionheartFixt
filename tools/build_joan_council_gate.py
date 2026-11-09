"""Jehanne's "I have spoken to your Council" needs the player to have spoken to it.

0.16.0's tier 7 gave Jehanne thirteen new nodes (43 the successor to 55 the charge), and twelve of them offer
`I have spoken to your Council.` with no gate, so a player who had never met the Spirit Council could claim to bring its
words. Every vanilla reply that makes that claim, in the same tree, is gated on the checker
`Joan player spoken to Spirit Council`. These now carry the same gate, written the way vanilla writes it. Every node keeps
another reply, so hiding this one cannot leave a node without a way out.

Found in play, 0.99.12. A dialogue tree is not frozen in a save, so this reaches a game in progress.

A rerun is a no-op.

    python tools/build_joan_council_gate.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import CR, DASH
from build_shrine_repairs import register

TREE = "Resources/Levels/4 Crypt/Dialog/JoanofArc.DialogTree"
CLAIM = "Reply Text=I have spoken to your Council." + CR
GATE = ("Custom Requirement=CActionExpression" + CR + "{" + CR + "Action=CCheckExistenceAction" + CR + "{" + CR +
        "Name To Check For=Joan player spoken to Spirit Council" + CR + "Desired Minimum Count=1" + CR + "}" + CR + "}" + CR)


def main():
    t = lhbuild.read(TREE)
    crlf = t.count(CR)
    blocks = t.split(DASH)
    gated = 0
    for n, b in enumerate(blocks):
        replies = re.split(r"(?<=\r\n)(?=\r\nRequirement=)", b)
        changed = False
        for k, r in enumerate(replies):
            if CLAIM in r and "Custom Requirement=" not in r:
                assert "\r\nRequirement=!None\r\n" in r, r[:200]
                replies[k] = r.replace("\r\nRequirement=!None\r\n", "\r\nRequirement=!None\r\n" + GATE, 1)
                assert len(re.findall(r"Reply Text=", b)) > 1, "a node would lose its only reply"
                changed = True
                gated += 1
        if changed:
            blocks[n] = "".join(replies)
    new = DASH.join(blocks)
    if gated:
        assert "\n" not in new.replace(CR, "")
        (lhbuild.FX / TREE).write_bytes(new.encode("latin-1"))
        register([TREE])
    print("council claims gated:", gated, "| CRLF", crlf, "->", new.count(CR))


if __name__ == "__main__":
    main()
