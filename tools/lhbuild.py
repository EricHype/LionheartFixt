"""Builders for Fixt map and dialogue-tree scripts.

Every build script in this project imports this module. It emits the game's brace-delimited resource
text (`B`), whole `Level Part=` blocks (`entity`, `relay_part`, `checker`, `poly_part`, `touch_poly`,
`touch_oval`, `generator`, `door_part`, ...) and the DialogTree hybrid format (`node`, `tree`), then
`write_map()` round-trips the result through `resource_format` so indentation comes out canonical.

Two rules the hard way, both of which have cost a release:

* An `Array` block must declare the number of items it actually holds, and a slice taken by counting
  braces excludes the trailing newline -- `balanced()` returns the index *after* the closing brace, so
  splice with `z[:s] + new + z[e + len(CR):]` when `new` already ends in CR.
* A generated block must carry every field vanilla writes, not merely the ones that look load-bearing.
  `touch_poly()` once omitted `Auto-Flip Switch` and shipped twelve triggers that could not re-arm.
  `tools/test_triggers.py` now asserts the trigger builders against the field lists parsed out of real
  vanilla triggers; run it after touching any of them.

Paths come from the environment so this is not tied to one machine:
  LIONHEART_MODTOOLS  -- the LionheartModTools checkout (default ~/LionheartModTools)
  LIONHEART_VANILLA   -- data.dat.vanilla.bak (default: the GOG install path)
"""
import os
import re
import sys
import zipfile
from pathlib import Path

MODTOOLS = Path(os.environ.get("LIONHEART_MODTOOLS", Path.home() / "LionheartModTools"))
sys.path.insert(0, str(MODTOOLS))
import resource_format

FX = Path(__file__).resolve().parent.parent / "files"
VANILLA = Path(os.environ.get(
    "LIONHEART_VANILLA",
    r"C:\Program Files (x86)\GOG Galaxy\Games\Lionheart - Legacy of the Crusader\data.dat.vanilla.bak"))
zf = zipfile.ZipFile(VANILLA)
CR = "\r\n"
T = "\t"
DASH = "-" * 60

# -- Montserrat prisoner-build constants, kept because hover_poly() reads HOVER_TREE. Nothing else
# -- in the library depends on them; they are leftovers from where this file was extracted.
D = "Levels/2 Montserrat/Dialog/"
SENTRY_TREE, HANDLER_TREE, BEAR_TREE, HOVER_TREE, BARKS_TREE = D + "Montserrat Sentry", D + "Montserrat Handler", D + "Chained Bear", D + "Montserrat Hover", D + "Montserrat Barks"
ASSASSIN = "Levels/2 Montserrat/Character Templates/Montserrat Assassin"
BEAR_CAN = "Monster Cans/Animals/Bear"
DEN_MAP = "2 Montserrat/3 Animal Den"
INVADER_NAMES = "Montserrat Assassin, Montserrat Assassin Tough, Montserrat Assassin Super, Snakebreed, Snakebreed Super, Snakebreed Tough, Snakebreed Boss, Snakebreed Boss Tough, Snakebreed Boss Super, Grove Sentry, Assassin"
BASES = ["LongSword", "Scimitar", "BastardSword", "ShortSword", "TwoHandedSword", "TwoHandedSwordGreat", "BattleAxe", "BattleAxeGreat",
         "Mace", "MaceGreat", "MorningStar", "WarHammer", "Club", "LongBow", "LongBow Composite", "Crossbow", "Arrow", "Bolt"]
NAMED = ["Quest Items/Bounty Hunter Sword Everlasting", "Quest Items/Beggar Short Sword in Sewers", "Quest Items/Felgnash Sword", "Quest Items/Kublai Khans Sword",
         "Quest Items/Sacred Scimitar Saladin Quest", "Quest Items/DaVinci Repeating Crossbow", "Quest Items/Special Objects for RED file/Sword of Undead Ice",
         "Unique Magic Items/Axe Unholy Smite", "Unique Magic Items/Blade of Berserker", "Unique Magic Items/Bow of Electricity", "Unique Magic Items/Bow of Fiery Smite",
         "Unique Magic Items/Bow of Icy Death", "Unique Magic Items/Holy Mace", "Unique Magic Items/Sword of Fire"]


def balanced(t, s):
    d, j = 0, t.index("{", s)
    while True:
        if t[j] == "{":
            d += 1
        elif t[j] == "}":
            d -= 1
            if d == 0:
                return j + 1
        j += 1


def B(cls, fields):
    """Flat resource block: canonical indentation is restored by resource_format on write."""
    out = cls + CR + "{" + CR
    for k, v in fields:
        if isinstance(v, tuple):
            out += k + "=" + B(v[0], v[1])
        elif isinstance(v, list):  # an Array of same-keyed items: [(key, block-tuple), ...]
            out += k + "=" + B("Array", [("Item Count", str(len(v)))] + v)
        else:
            out += k + "=" + v + CR
    return out + "}" + CR


def arr(items):  # Action=Array{Item Count=n, Action=...}
    return [("Action", it) for it in items]


def multi(items):
    return ("CMultipleActionsAction", [("Action", arr(items))])


def activate(name):
    return ("CActivateAction", [("Target Name", name), ("Play Activate Sound", "0"), ("Delay Between Activations", "0"), ("Warp Behavior", "")])


def deactivate(name):
    return ("CDeactivateAction", [("Target Name", name)])


def relay(name):
    return ("CTriggerRelayAction", [("Relay Name", name)])


def exists(name):
    return ("CCheckExistenceAction", [("Name To Check For", name), ("Desired Minimum Count", "1")])


def if_action(cond, then, els=""):
    return ("CIfAction", [("If", cond), ("Then", then), ("Else", els), ("Return failure if the If failes", "0")])


def delay(secs, nxt):
    return ("CDelayAction", [("Next Action", nxt), ("Delay", str(secs)), ("Plus or Minus", "0"), ("Forget Trigger", "0")])


def balloon(tree, node, anchor, off="-70"):
    return ("CDisplayDialogBalloonAction", [("Dialog Tree File", tree), ("Node ID", node), ("Name of Position", anchor),
                                            ("Position Offset", "0.000000," + off + ".000000"), ("After Action", ""), ("Include In Log", "1")])


def dialog(tree, node, speaker):
    return ("CDisplayDialogTreeAction", [("Dialog Tree File", tree), ("Node ID", node), ("Speaker", speaker), ("Player Being Spoken To", "$Instigator")])


def set_target(entity, name=""):
    return ("CSetTargetTypeAction", [("Entity Name", entity), ("Name To Target", name), ("Valid Targets", "")])


def passive(entity):
    return [set_target(entity), ("CRemoveCategoryAction", [("Target Name", entity), ("Categories To Remove", "Enemy")])]


def other_map(map_name, action):
    return ("COtherMapAction", [("Action", action), ("Other Map Name", map_name)])


def specifier(interaction, action, radius="55", locked="0", lockadj="0", once="0"):
    return ("CAIInteractionSpecifier", [("Marked For Deletion", "0"), ("Publisher", ""), ("Trigger Only Once", once), ("Was Triggered", "0"), ("Auto-Flip Switch", "1"),
                                        ("Trigge Must Have HP", "0"), ("Triggered By Anything", "0"), ("Triggered By Players", "1"), ("Triggered By Player Friends", "0"),
                                        ("Triggered By Enemies", "0"), ("Triggered By Projectiles", "0"), ("Triggered By Companions", "0"), ("Triggered By Name", ""),
                                        ("Interaction Description", ""), ("Interaction Type", "Interaction Specifiers/" + interaction), ("Action", action),
                                        ("X Radius", radius), ("Attacker Range Modifier", "0"), ("YX Ratio", "0.712766"), ("Highlight Self Time", "0"),
                                        ("Highlight Until Clicked", "0"), ("Is Locked", locked), ("Allow Interact If Has Target", "1"), ("Lock Pick Adjustment", lockadj),
                                        ("Inventory item to use as key", "Inventory Items/!None"), ("Is Bussy Talking", "0")])


def swap_specifier(target, spec):
    return [("CRemoveAIAction", [("Target Name", target), ("AI", "CAIInteractionSpecifier"), ("Delay Between Removes", "0")]),
            ("CAddAIAction", [("Target Name", target), ("AI", spec), ("Delay Between Adds", "0")])]


def generate_item(item, location, radius="40"):
    return ("CGenerateInventoryItemAction", [("Number of items to generate", "1"), ("Level of item to generate", ""), ("Location", location), ("Location Offset", "0,0"),
                                             ("Generate Within Radius", radius), ("Aspect Ratio", "0.712766"),
                                             ("Item List", ("CInventoryItemGeneratorMixedList", [("Items", ("Array", [("Array Count", "1"), ("Array Item", ("CInventoryItemGeneratorMixedListItem", [
                                                 ("Weighting", "1"), ("Item", ("CInventoryItemGeneratorBasic", [("Items", ("Array", [("Array Count", "1"), ("Array Item", ("CInventoryItemGeneratorBasicItem", [("Weighting", "10"), ("Item", item)]))]))]))]))]))]))])


def generate_good_weapon(location):
    return ("CGenerateInventoryItemAction", [("Number of items to generate", "1"),
                                             ("Level of item to generate", ("CUseCannedExpressionExpression", [("Canned Expression", "Common Objects and Scripts/Generate Magic Item Level Cans/Chest Generator Good")])),
                                             ("Location", location), ("Location Offset", "0,0"), ("Generate Within Radius", "40"), ("Aspect Ratio", "0.712766"),
                                             ("Item List", ("CInventoryItemGeneratorMixedList", [("Items", ("Array", [("Array Count", "1"), ("Array Item", ("CInventoryItemGeneratorMixedListItem", [
                                                 ("Weighting", "1"), ("Item", ("CInventoryItemGeneratorCannedList", [("Canned Item List", "Inventory/Creating Random Magic Items/All Weapons")]))]))]))]))])


def take_and_return(item, location):
    return ("CConditionalAction", [("Try Action", ("CActionRemoveInventoryItem", [("Who to remove from", "$instigator"), ("Inventory Item To remove", item)])),
                                   ("Succeed Action", generate_item(item, location)), ("Fail Action", ""), ("Return failure if the TryAction failes", "0")])


# ---------------------------------------------------------------- part builders
BASE_FIELDS = [("Child List", ""), ("Visible", "0"), ("Collideable", "1"), ("Half Height", "0"), ("Full Height", "1"), ("Tries To Collide", "0"), ("Has Hit Points", "0"),
               ("Stationary", "1")]
TAIL_FIELDS = [("Category", ""), ("Team Number", "Nutral"), ("Used In", "QuestMode"), ("Current Target", ""), ("Publisher", "")]


def entity(name, active, activities, model, x, y, visible="0", extra_tail=None, cls="CEntityBase", collideable="1"):
    fields = [("Name", name)] + [(k, (visible if k == "Visible" else collideable if k == "Collideable" else v)) for k, v in BASE_FIELDS] + \
             [("Active", active), ("Is Temporarily Excluded", "0"), ("Is Marked For Deletion", "0"),
              ("Activity", ("Array", [("Item Count", str(len(activities)))] + [("Activity", a) for a in activities]))] + TAIL_FIELDS + \
             [("Model", model), ("Position X", str(x)), ("Position Y", str(y)), ("Rendering Height", "0"), ("Rendering Height Float", "0"), ("Cur Sequence", "Idle")] + (extra_tail or [])
    return "Level Part=" + B(cls, fields)


def checker(name, x, y):
    return entity(name, "0", [], "Editor/Checker", x, y, visible="1")


def marker(name, x, y):
    return entity(name, "1", [], "Editor/Position Marker", x, y)


def relay_part(name, action, x, y, once="1"):
    return entity(name, "1", [("CRelayAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Action", action), ("Trigger Only Once", once), ("Was Triggered", "0")])], "Editor/Relay", x, y)


def poly_part(name, cls_ai_fields, points, active="1", collideable="0"):
    fields = [("Name", name)] + [(k, ("1" if k == "Visible" else collideable if k == "Collideable" else v)) for k, v in BASE_FIELDS] + \
             [("Active", active), ("Is Temporarily Excluded", "0"), ("Is Marked For Deletion", "0"),
              ("Activity", ("Array", [("Item Count", "1"), ("Activity", cls_ai_fields)]))] + TAIL_FIELDS + \
             [("Polygon", ", ".join(str(p) for p in points)), ("Center Position Offset", "0.000000,0.000000")]
    return "Level Part=" + B("CFreeRangePoly", fields)


# Vanilla's touching-trigger field set, in vanilla's order. This list used to be short: it omitted
# Auto-Flip Switch, which is what lets a trigger re-arm after the player leaves, so a `once="0"` poly
# built with it did not reliably retry. Every use before act 7's ambush check wanted a one-shot, so the
# gap never showed. Model: Titan Village's `Eavesdrop trigger`, which drives the game's only live-sneak
# encounter and uses all three action slots. `trigger_fields` is asserted against it by tests/.
def trigger_fields(once, enter_action, exit_action, repeat_action, repeat_every, by_name, by_players):
    return [("Marked For Deletion", "0"), ("Publisher", ""), ("Trigger Only Once", once), ("Was Triggered", "0"),
            ("Auto-Flip Switch", "1"), ("Trigge Must Have HP", "0"), ("Triggered By Anything", "0"),
            ("Triggered By Players", by_players), ("Triggered By Player Friends", "0"), ("Triggered By Enemies", "0"),
            ("Triggered By Projectiles", "0"), ("Triggered By Companions", "0"), ("Triggered By Name", by_name),
            ("Enter Action", enter_action), ("Exit Action", exit_action), ("Repeat Action", repeat_action),
            ("Repeat Every", repeat_every), ("Touching LayerPart", ""), ("Next Repeat Time", "0")]


def touch_poly(name, enter_action, points, once="1", exit_action="", repeat_action="", repeat_every="0",
               by_name="", by_players="1", active="1"):
    """A CFreeRangePoly that fires on entry. once="0" makes it retryable -- see trigger_fields."""
    ai = ("CTouchingPolygonTriggerAI",
          trigger_fields(once, enter_action, exit_action, repeat_action, repeat_every, by_name, by_players))
    return poly_part(name, ai, points, active=active)


def touch_oval(name, enter_action, x, y, radius="30", once="1", exit_action="", repeat_action="",
               repeat_every="0", by_name="", by_players="1", active="1"):
    """The oval form of the same trigger, e.g. Titan Village's `Mathuo-Iapetus Bubble trigger`, which
    watches for a named NPC (by_name="Mathuo", by_players="0") rather than the player."""
    ai = ("CTouchingOvalTriggerAI",
          trigger_fields(once, enter_action, exit_action, repeat_action, repeat_every, by_name, by_players)
          + [("X Radius", str(radius)), ("YX Ratio", "0.712766")])
    return entity(name, active, [ai], "Editor/Trigger Icon, Proximity", x, y, collideable="0")


def hover_poly(name, node, points):
    return poly_part(name, specifier("GetCloseThenTrigger", balloon(HOVER_TREE, node, "$trigger", "-50")), points)


def generator(name, active, entity_can, new_name, after, x, y, ais=None, radius="11", facing="Any Direction"):
    gen = ("CGeneratorAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Already Generated", "0"), ("Area", ("COvalGeneratorArea", [("Radius", radius)])), ("Has Started Generating", "0"),
                            ("Groups", ("Array", [("Item Count", "1"), ("Group", ("CGeneratorAIGroup", [("Max Party Mojo", "40"), ("Quantity to generate min", "1"), ("Quantity to generate max", "1"),
                                                                                                        ("Things to Generate", ("Array", [("Item Count", "1"), ("Thing to Generate", ("CSpawnableCannedEntity", [("Weight", "1"), ("Entity", entity_can)]))]))]))])),
                            ("New Name", new_name), ("Remove Default AIs", "0"),
                            ("AIs to Add", ("Array", [("Item Count", str(len(ais or [])))] + [("AI", a) for a in (ais or [])])),
                            ("Canned AIs to Add", ("Array", [("Item Count", "0")])), ("After Action", after), ("New Facing Angle", facing), ("Angle Variation", "0.785398")])
    return entity(name, active, [gen], "Editor/Enemy Generator Spot", x, y)


def spawn_point(name, x, y, per_party, facing="230"):
    ai = ("CSpawnPointAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Per Party Spawn Action", per_party), ("Per Character Spawn Action", ""), ("Set Facing Angle", "1"), ("Facing Angle", facing)])
    return entity(name, "1", [ai], "Editor/Spawn Point", x, y, visible="1")


def door_part(name, model, x, y, spec):
    door_ai = ("CDoorAI", [("Marked For Deletion", "0"), ("Publisher", ""), ("Is Locked", "0"), ("Allow Open or Close?", ""), ("Before Open", ""), ("After Opened", ""), ("Before Closed", ""),
                           ("After Closed", ""), ("After Locked", ""), ("After Unlocked", ""), ("Auto-Close Timeout", "0"), ("State", "Unknown"), ("Timeout Time Left", "0"),
                           ("Frame Andvance", "0"), ("Next Pain", "0"), ("Triggered By Players", "1"), ("Triggered By Enemies", "1")])
    tail = [("Cur Damage", "0"), ("Destroyed Script Action", ""), ("Destroyed Effect Action", ""), ("Damaged Script Action", ""), ("Damaged Effect Action", ""), ("Hit Action", ""),
            ("Default Death Type", "!None"), ("Has Done Death Processing", "0"), ("Play Ratio", "0"), ("Aiming Angle", "0"), ("Movement Angle", "0"), ("Start FacingAngle", "0"),
            ("Current Frame", "0"), ("Created By", ""), ("BehaviorStack", ("CEntityBehaviorStack", [("InProcess", "0"), ("Blocking Priority", "Idle"), ("BehaviorList", ("Array", [("Item Count", "0")]))])),
            ("Facing Backwards", "0"), ("Last Facing Backwards", "0"), ("Upper Body Present", "0"), ("Synch Aiming And Moving", "1"), ("Frame Index Locked", "0"), ("Waiting For Discharge", "0"),
            ("Still Shooting", "0"), ("Trying To Move", "0"), ("Tracking Updates Since Relocate", "0")]
    e = entity(name, "1", [door_ai, spec], model, x, y, visible="1", extra_tail=tail, cls="CEntityAnimated")
    return e.replace("Cur Sequence=Idle" + CR, "Cur Sequence=closed" + CR, 1)


def prop_part(name, model, x, y, activities=(), seq="idle"):
    tail = [("Cur Damage", "0"), ("Destroyed Script Action", ""), ("Destroyed Effect Action", ""), ("Damaged Script Action", ""), ("Damaged Effect Action", ""), ("Hit Action", ""),
            ("Default Death Type", "!None"), ("Has Done Death Processing", "0"), ("Play Ratio", "0"), ("Aiming Angle", "0"), ("Movement Angle", "0"), ("Start FacingAngle", "0"),
            ("Current Frame", "0"), ("Created By", ""), ("BehaviorStack", ("CEntityBehaviorStack", [("InProcess", "0"), ("Blocking Priority", "Idle"), ("BehaviorList", ("Array", [("Item Count", "0")]))])),
            ("Facing Backwards", "0"), ("Last Facing Backwards", "0"), ("Upper Body Present", "0"), ("Synch Aiming And Moving", "1"), ("Frame Index Locked", "0"), ("Waiting For Discharge", "0"),
            ("Still Shooting", "0"), ("Trying To Move", "0"), ("Tracking Updates Since Relocate", "0")]
    e = entity(name, "1", list(activities), model, x, y, visible="1", extra_tail=tail, cls="CEntityAnimated")
    return e.replace("Cur Sequence=Idle" + CR, "Cur Sequence=" + seq + CR, 1)


def read(rel):
    p = FX / rel
    return (p.read_bytes() if p.exists() else zf.read(rel)).decode("latin-1")


def write_map(rel, text):
    (FX / rel).parent.mkdir(parents=True, exist_ok=True)
    (FX / rel).write_bytes(resource_format.parse_resource_text(text).to_text().encode("latin-1"))


def add_parts(z, parts):
    k = z.index(T*2 + "Level Part=")
    return z[:k] + "".join(parts) + z[k:]


def node(nid, text, replies):
    out = "Node ID=" + nid + CR + "Text=" + text + CR + "Should Have Voiceover=0" + CR
    for r in replies:
        out += CR + "Requirement=" + r.get("req", "!None") + CR
        if "creq" in r:
            out += "Custom Requirement=" + r["creq"]
        out += "Reply Text=" + r["text"] + CR + "Go to node ID=" + r.get("go", "") + CR
        if "action" in r:
            out += "Custom Action=" + B(*r["action"])
        if "icon" in r:
            out += "Icon=" + r["icon"] + CR
        if r.get("default"):
            out += "Is Default Reply=1" + CR
    return out


def tree(name, nodes, canceled=""):
    return ("CDialogTree" + CR + "{" + CR + "Name=" + name + CR + "Portrait=!None" + CR + "Should Have Voiceovers=0" + CR +
            "Default Canceled Node Action=" + (B(*canceled) if canceled else CR) + DASH + CR + (DASH + CR).join(nodes) + "}" + CR)


def cor(a, b):
    return "COR" + CR + "{" + CR + "Operand1=" + a + "Operator=" + CR + "Operand2=" + b + "}" + CR


def canned(name):
    return "CUseCannedExpressionExpression" + CR + "{" + CR + "Canned Expression=Dialog/Requirements/" + name + CR + "}" + CR


