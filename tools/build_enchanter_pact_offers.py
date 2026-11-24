"""The Enchanter's pact is offered where it can happen, not only on a conversation nobody knows to start. Asked: "i just
met the mad enchanter and had no option to have him assist me / work with relican".

0.39.0 put the pact (`70`/`71 Fixt Pact`, the Ring, the proper bind) only on `05 Return Dialogue 1`, which exists only
after he has spared you and you click him again. Both sparing routes end with "Now leave", and the Speech route (the
lie, `60` -> `62 Others`) ends only in his suicide, so the pact was invisible to anyone who did not think to come back,
and unreachable for a high-Speech character.

  * The two moments he spares you, `45 Barter 3` and `59 Winner`, gain the pact reply `05` already has, ahead of the
    goodbye, to `70 Fixt Pact 1`. It does what the goodbye does (`Pacify Enchanter in Dialog`, and 0.99.37's spared
    reactions); on `59` it also hands over the amulet the crystal route's `61 Fixt Bound Token` gives.
  * The lie route's `62 Others`, where he asks "What can be done?!", gains a third answer besides suicide: serve
    Relican, who can unmake this prison. It spares him the same way and goes to `71 Fixt Pact 2`, since you have
    already named Relican.

All three are gated on `Fixt Enchanter Pact Available`, as `05`'s pact reply is. A tree edit: every save. A rerun is a
no-op.

    python tools/build_enchanter_pact_offers.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR, relay
from build_shrine_repairs import register
from build_ether_plane_reckoning import ENCHANTER, SPARED_ACTIONS

SEP = "-" * 60
PACT_REPLY = ("My word was true, and I can do better than words. There is a hidden city of wielders above this place, "
              "and a necromancer who means to take it. Their dead could be yours.")
LIE_REPLY = ("There is one who could put you out of their reach. A necromancer named Relican is taking the hidden city of "
             "wielders above this place. Serve him, and when the city is his, he can unmake this prison before they arrive.")
MARK = "Reply Text=" + LIE_REPLY
assert "—" not in LIE_REPLY and "--" not in LIE_REPLY


def reply(text, go, actions):
    body = "".join("Action=" + B(*a) for a in actions)
    return ("Requirement=Fixt Enchanter Pact Available" + CR + "Reply Text=" + text + CR + "Go to node ID=" + go + CR +
            "Custom Action=CMultipleActionsAction" + CR + "{" + CR + "Action=Array" + CR + "{" + CR +
            "Item Count=%d" % len(actions) + CR + body + "}" + CR + "}" + CR + "Icon=Quest Icon" + CR + CR)


def insert_before(t, node, before_text, block):
    s = t.index("Node ID=" + node + CR)
    e = t.index(SEP, s)
    r = t.index("Reply Text=" + before_text, s, e)
    k = t.rindex(CR + CR + "Requirement=", s, r) + len(CR + CR)
    return t[:k] + block + t[k:]


def build():
    t = lhbuild.read(ENCHANTER)
    if MARK in t:
        return False
    assert t.count("Reply Text=" + PACT_REPLY + CR) == 1  # 05's own
    spare = [relay("Pacify Enchanter in Dialog")] + SPARED_ACTIONS
    t = insert_before(t, "45 Barter 3", "Very well. Goodbye.", reply(PACT_REPLY, "70 Fixt Pact 1", spare))
    t = insert_before(t, "59 Winner", "Very well. I shall see if I can open the portal",
                      reply(PACT_REPLY, "70 Fixt Pact 1", spare + [relay("Fixt give Trapped Spirit Amulet")]))
    t = insert_before(t, "62 Others", "There is nothing to be done", reply(LIE_REPLY, "71 Fixt Pact 2", spare))
    (lhbuild.FX / ENCHANTER).write_bytes(t.encode("latin-1"))
    register([ENCHANTER])
    return True


def main():
    print("enchanter pact offers:", build())


if __name__ == "__main__":
    main()
