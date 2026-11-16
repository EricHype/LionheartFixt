"""Felipe remembers what you told him, and the woodcutter's eyes and liver reach the player. Reported from play after
0.99.25: "when talking to the woodcutter, I tell him I am the reason his daughter did not return and he still greets me as
a friend when i talk to him again. Also, I took the quest to kill him and on his death i got darkwood, but not his eyes and
liver."

**He remembers.** `31 she never came home` (9407b4a), reached by the admission or the lie, set nothing, so the next visit
opened `1 Conversation Start` or `3 Return Dialogue happy` again. Its exit now sets `Fixt Felipe Knows` on the player and
activates `Angry Return`, the map's own "you pissed off the woodcutter" marker, so the map opens `2 Return Dialogue angry`:
*"What do you want? What do you think I have to say to *you*?"* Every reply there that would talk him round (the Darkwood,
the cave, *"I didn't mean to offend you"*, *"What's wrong?"*, the rude exit, the found daughter) is hidden once he knows, and
a new exit takes its place. The shaman's kill reply stays. `Angry Return` exists in vanilla's map, so this reaches every save.

**The eyes and liver.** Vanilla's death script gives both to `$Instigator`, and in a death script that is whoever landed the
blow: in the report it was Ernesto (`Ernesto kills Woodcutter`), and the save has both items in his inventory, which the UI
cannot open. The script then marks them as handed out, so the ground drop that was meant as the fallback never comes. Each
give is now wrapped in `CForEachPlayerAction`, vanilla's own fix for the same trap on `Relican Dead`. That is the
Woodcutter Forest map, so it reaches a forest not yet entered, and new games.

**Rakeb takes them anyway.** For a save where a companion already holds them, Rakeb's turn-in gets a second reply, *"One of my
companions carries his eyes and liver."*, for when the quest says you have them and you do not; it opens
`121`, a copy of `120 Returning with the eyes` without the two item removals, so the reward, the rank and the completion
are vanilla's. The items stay with the companion.

**Rakeb's greeting.** c1bc303 sent `fish done and eyes quest not completed` to `63`, *"I have a job for you"*, which also
caught a player holding the eyes and buried the turn-in three nodes deep in the re-pitch. Node 63 now carries both turn-in
replies (every save), and the selector asks *never activated* instead (a Goblin Warrens not yet entered, and new games).

A rerun is a no-op.

    python tools/build_woodcutter_fixes.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register
from build_troll_choices import AND, NOT, act, modifier, node_span, reply, reply_start, add_node, VARS

FELIPE = "Resources/Levels/Wilderness/Dialog/Woodcutter.DialogTree"
RAKEB = "Resources/Levels/Wilderness/Dialog/Rakeb.dialogtree"
FOREST = "Levels/Wilderness Maps/Woodcutter Forest.zax"
WARRENS = "Levels/Wilderness Maps/Goblin Warrens.zax"
KNOWS = "Fixt Felipe Knows"
KNOWS_DCA = "Resources/" + VARS + KNOWS + ".DerivedCharacterAttribute"
EYES_QUEST = "Levels/Wilderness/Quests/Bring the Woodcutter's Eyes to the Goblin Shaman"
HAS_EYES_STATE = "3EUUJA40"
EYES = "Inventory/Specific Item Cans/Quest Items/Woodsman Eyes"
LIVER = "Inventory/Specific Item Cans/Quest Items/Woodsman Liver"
# node 2's replies that would talk him round, hidden once he knows
SOFT = ["I have found your daughter.", "I have heard that you can give me Darkwood.",
        "I have cleared the cave below your house of creatures.", "I didn't mean to offend you, who are you?",
        "What's wrong?", "Nothing. I'll be going now."]
TEXT = {"32 nothing to say": "<He turns his back on you and goes on with his work.>"}
TURN_IN = "I have the woodsman's eyes and liver."
CARRIED = "One of my companions carries his eyes and liver."
CARRIED_NODE = "121 Returning with the eyes carried"


def knows():
    return ("CIsGreaterThan", [("Operand1", ("CVariableDerivedCharacterAttribute", [("Character Attribute", VARS + KNOWS)])),
                               ("Operator", ""), ("Operand2", ("CConstant", [("Constant Value", "0")]))])


def holds(item):
    return act(("CActionCheckForInventoryItem", [("Who to give check", "$instigator"), ("Inventory Item To Check For", item)]))


def build_dca():
    if (lhbuild.FX / KNOWS_DCA).exists():
        return
    t = lhbuild.read("Resources/" + VARS + "Fixt Fernand Stride.DerivedCharacterAttribute")
    t = t.replace("Fixt Fernand Stride", KNOWS)
    t = re.sub(r"Description=[^\r\n]*", "Description=1 once the player has told Felipe the woodcutter that his daughter is not coming home (tools/build_woodcutter_fixes.py).", t)
    (lhbuild.FX / KNOWS_DCA).write_bytes(t.encode("latin-1"))
    register([KNOWS_DCA])


def and_into(t, nid, text, extra):
    """AND `extra` into the gate of the reply with this text in node nid."""
    k = reply_start(t, nid, text)
    e = t.index("Reply Text=" + text + CR, k)
    head = t[k:e]
    req = head[:head.index(CR) + len(CR)]
    assert req.startswith("Requirement="), head[:80]
    old = head[len(req):]
    if old:
        assert old.startswith("Custom Requirement="), old[:80]
        gate = B("CAND", [("Operand1", "RAW"), ("Operator", ""), ("Operand2", extra)]).replace(
            "Operand1=RAW" + CR, "Operand1=" + old[len("Custom Requirement="):], 1)
    else:
        gate = B(*extra)
    return t[:k] + req + "Custom Requirement=" + gate + t[e:]


def build_felipe():
    t = lhbuild.read(FELIPE)
    if "Node ID=32 nothing to say" + CR in t:
        return 0
    # 1. the exit of 31 records it, and turns on the map's own angry-greeting marker
    i, j = node_span(t, "31 she never came home")
    blk = t[i:j]
    old = "Reply Text=" + CR + "Go to node ID=" + CR + "Icon=Exit Icon" + CR
    assert blk.count(old) == 1 and "Custom Action" not in blk
    told = lhbuild.multi([modifier("Player1", "Game Scripting Variables/" + KNOWS, "1", "0"), lhbuild.activate("Angry Return")])
    blk = blk.replace(old, "Reply Text=" + CR + "Go to node ID=" + CR + "Custom Action=" + B(*told) + "Icon=Exit Icon" + CR, 1)
    t = t[:i] + blk + t[j:]
    # 2. the angry greeting: nothing that would talk him round, once he knows
    for text in SOFT:
        t = and_into(t, "2 Return Dialogue angry", text, NOT(knows()))
    k = reply_start(t, "2 Return Dialogue angry", "Nothing. I'll be going now.")
    t = t[:k] + reply("<Leave him alone.>", "32 nothing to say", creq=knows(), icon="Exit Icon").replace(
        "Icon=Exit Icon" + CR, "Icon=Exit Icon" + CR + "Is Default Reply=1" + CR) + t[k:]
    t = add_node(t, "32 nothing to say", TEXT["32 nothing to say"], [])
    (lhbuild.FX / FELIPE).write_bytes(t.encode("latin-1"))
    register([FELIPE])
    return len(SOFT)


def build_rakeb():
    t = lhbuild.read(RAKEB)
    if CARRIED in t:
        return 0
    state = act(("CIsQuestStateTheCurrentStateAction", [("Quest", EYES_QUEST), ("State", HAS_EYES_STATE)]))
    both = AND(holds(EYES), holds(LIVER))
    # the companion path gets its own copy of 120 without the two removals, which would act on a player who has nothing
    i, j = node_span(t, "120 Returning with the eyes")
    blk = t[i:j]
    for item in (EYES, LIVER) * 2:  # two replies, each removes both
        s = blk.index("Action=CActionRemoveInventoryItem" + CR)
        assert item in blk[s:lhbuild.balanced(blk, s)]
        blk = blk[:s] + blk[lhbuild.balanced(blk, s) + len(CR):]
    assert blk.count("Item Count=5" + CR) == 2 and "CActionRemoveInventoryItem" not in blk
    blk = blk.replace("Item Count=5" + CR, "Item Count=3" + CR).replace("Node ID=120 Returning with the eyes" + CR, "Node ID=" + CARRIED_NODE + CR, 1)
    k = t.rindex("}" + CR)
    t = t[:k] + lhbuild.DASH + CR + blk.rstrip(CR) + CR + t[k:]
    carried = reply(CARRIED, CARRIED_NODE, creq=AND(state, NOT(both)), icon="Quest Icon")
    # node 3: beside the vanilla turn-in
    k = reply_start(t, "3 Return Dialogue", TURN_IN)
    e = t.index(CR + CR, t.index("Reply Text=" + TURN_IN + CR, k)) + len(CR + CR)
    t = t[:e] + carried + t[e:]
    # node 63: both turn-ins, first
    k = reply_start(t, "63 Returning after the node 60 without accepting the other task", "Tell me more.")
    t = t[:k] + reply(TURN_IN, "120 Returning with the eyes", creq=AND(state, both), icon="Quest Icon") + carried + t[k:]
    (lhbuild.FX / RAKEB).write_bytes(t.encode("latin-1"))
    register([RAKEB])
    return 3


def build_forest():
    z = lhbuild.read(FOREST)
    n = 0
    for item in (EYES, LIVER):
        i = z.index("Inventory Item To Give=" + item + CR)
        s = z.rindex("Action=CActionGiveStandardInventoryItem" + CR, 0, i)
        # already wrapped: the line two above is the CForEachPlayerAction (then its brace)
        prev = z.rindex(CR, 0, z.rindex(CR, 0, z.rindex(CR, 0, s)))
        if "Action=CForEachPlayerAction" in z[prev:s]:
            continue
        e = lhbuild.balanced(z, s)
        give = z[s + len("Action="):e]
        wrapped = B("CForEachPlayerAction", [("Action", "RAW")]).replace("Action=RAW" + CR, "Action=" + re.sub(r"\r\n\t*", CR, give) + CR, 1)
        z = z[:s] + "Action=" + wrapped.rstrip(CR) + z[e:]
        n += 1
    if n:
        lhbuild.write_map(FOREST, z)
        register([FOREST])
    return n


def build_warrens():
    z = lhbuild.read(WARRENS)
    i = z.index("Node ID=63 Returning after the node 60")
    s = z.rindex("If=CAndAction" + CR, 0, i)
    seg = z[s:i]
    pat = re.compile(r"CNotAction\r\n(\t*)\{\r\n(\t*)Action=CIsQuestCompletedAction\r\n(\t*)\{\r\n(\t*)Quest=" + re.escape(EYES_QUEST) + CR)
    m = pat.search(seg)
    if not m:
        assert "CWasQuestEverActivatedAction" in seg
        return 0
    seg = seg[:m.start()] + m.group(0).replace("CIsQuestCompletedAction", "CWasQuestEverActivatedAction") + seg[m.end():]
    lhbuild.write_map(WARRENS, z[:s] + seg + z[i:])
    register([WARRENS])
    return 1


def main():
    build_dca()
    print("felipe gates:", build_felipe(), "| rakeb replies:", build_rakeb(), "| forest gives wrapped:", build_forest(),
          "| warrens selector:", build_warrens())


if __name__ == "__main__":
    main()
