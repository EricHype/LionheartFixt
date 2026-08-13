# Lionheart Fixt — the work, by section and by map

Status: **planning**. Nothing below is built.

The [design doc](lionheart-fixt-design.md) argues *what* to do and why. This is *where*:
every section of the game, every map that needs work, and what the work is. Content
inventory lives in [`cut-content.md`](cut-content.md).

## How the numbers were taken

Everything is measured from `data.dat.vanilla.bak`, never the install, which carries our
own mods. Every figure here is reproducible:

```
python survey_maps.py "<game dir>/data.dat.vanilla.bak"                  # the summary table
python survey_maps.py "<game dir>/data.dat.vanilla.bak" --section "4 Crypt"
python survey_maps.py "<game dir>/data.dat.vanilla.bak" --silent
```

Per map, read straight out of the `.zax`:

| Column | What it counts |
|---|---|
| **ents** | `CEntityBase` — everything placed, props included |
| **convs** | `CDisplayDialogTreeAction` — openable conversations |
| **balloons** | `CDisplayDialogBalloonAction` — floating one-liners |
| **nodes** | dialogue nodes *reachable from this map*, summed over the trees it opens |
| **gated** | replies on those trees behind a skill, faction or gender check |
| **spawns** | sum of `Quantity to generate max` over the map's `CGeneratorAIGroup`s |
| **loot** | `CInventoryItemGenerator*` — there is no container class; loot is a generator |

### Two ways to count dialogue, and why they disagree

The design doc's table counts nodes **filed under an act's own `Dialog/` folder**. This
document counts nodes **reachable from a map**. Trees are shared — a companion follows you
into the Crypt and brings their Barcelona dialogue along — so the second number is larger
wherever an act borrows.

Both are right; they answer different questions. Filed-under says *how much was written
for this act*. Reachable says *how much a player can actually talk to here*, which is what
per-map planning needs. They reconcile exactly:

| Section | Maps | Nodes filed here | Per map (design doc's figure) | Reachable per map |
|---|---|---|---|---|
| 1 Barcelona | 36 | 2619 | 72.8 | 125.2 |
| Sewers | 9 | 173 | 19.2 | 20.4 |
| Wilderness | 43 | 825 | 19.2 | 62.6 |
| 2 Montserrat | 5 | 11 | 2.2 | 34.0 |
| 3 Montaillou | 17 | 1085 | 63.8 | 148.3 |
| 4 Crypt | 10 | 94 | 9.4 | 34.3 |
| 5 Nostrodomus | 10 | 103 | 10.3 | 35.8 |
| 6 Barcelona Attack | 8 | 43 | 5.4 | 26.6 |
| 7 English Shrine | 11 | 49 | 4.5 | 7.6 |
| 8 Alamut | 11 | 153 | 13.9 | 64.3 |

Montserrat is the sharpest case: **11 nodes were written for the whole act**, and the 34
per map a player meets are almost entirely companions carrying their own lines in.

### A section the first pass missed

**Wilderness is 43 maps** — more than any single act — and it was not in the design doc's
table at all. It is the travel layer between acts: Crossroads, Plains, Lake, the goblin
warrens, the ogre caves. It holds 825 authored nodes and 31 quests, and it is where
`goblingirl` and `goblinguards` are filed. Any plan that skips it skips a quarter of the
game's maps.

## The campaign at a glance

161 shipped maps (excluding test and multiplayer), 7493 generators, 13,945 declared enemy
spawns.

| Section | Maps | Reachable nodes/map | Spawns/map | Spawns per node | Verdict |
|---|---|---|---|---|---|
| 1 Barcelona | 36 | 125.2 | 20.9 | 0.2 | The model. Repair only. |
| 3 Montaillou | 17 | 148.3 | 38.7 | 0.3 | The realistic target. Restore the cut quest. |
| Wilderness | 43 | 62.6 | 68.9 | 1.1 | Healthy but repetitive. Place cut content here. |
| 8 Alamut | 11 | 64.3 | 117.5 | 1.8 | Better than its reputation. Thin the middle. |
| 5 Nostrodomus | 10 | 35.8 | 134.8 | 3.8 | Five silent caves. |
| 2 Montserrat | 5 | 34.0 | 138.6 | 4.1 | **11 nodes written.** Needs new writing most, per map. |
| 6 Barcelona Attack | 8 | 26.6 | 136.5 | 5.1 | A siege; density is the point. Light touch. |
| Sewers | 9 | 20.4 | 116.3 | 5.7 | Front half is fine, back half is four empty dungeons. |
| 4 Crypt | 10 | 34.3 | 296.0 | 8.6 | **The worst act.** Half its maps are unnamed filler. |
| 7 English Shrine | 11 | 7.6 | 85.2 | 11.2 | **The emptiest act.** Ends on a silent boss room. |

## Section 4 — The Crypt

Ten maps, one quest, 2960 spawns. Four of them are called "Misc Crypt". The act's own
writers gave them no names, no NPCs and no reason to exist beyond length.

| Map | ents | convs | nodes | spawns | Work |
|---|---|---|---|---|---|
| 1 Crypt Entrance | 192 | 3 | 159 | 37 | Fine. The act's only conversation hub — build outward from here. |
| 2 Retreat of Souls Entry | 95 | 2 | 6 | 24 | Fine as a junction. |
| 2 Retreat of Souls | 756 | 0 | 13 | **873** | Worst ratio in the game: 873 spawns, no conversation. Halve it; add a survivor or a prisoner. |
| 3 Misc Crypt 1 | 42 | 0 | 0 | 41 | Silent filler. Give it one reason to exist or cut it from the route. |
| 4 Misc Crypt 2 | 141 | 0 | 0 | 161 | Silent filler. |
| 5 Misc Crypt 3 | 180 | 0 | 0 | 171 | Silent filler. |
| 6 Misc Crypt 4 | 46 | 0 | 0 | 26 | Silent filler. |
| 7 Doomed Plateau | 1014 | 10 | 65 | **1010** | Densest map in the game. It already talks — thin it hard rather than adding. |
| 8 Ante Chamber | 401 | 0 | 38 | 361 | 19 gated replies reachable and zero conversations to use them on. |
| 9 Burial Chamber | 352 | 4 | 62 | 256 | The act's payoff. Fine. |

**The plan for the act.** One quest across ten maps is the real failure, not the spawn
count. Three or four objectives that send the player back through the Misc Crypts with a
purpose would change how the act reads more than any thinning. Then thin: Retreat of Souls
873 -> ~350, Doomed Plateau 1010 -> ~450, Ante Chamber 361 -> ~200.

The four Misc Crypts are the strongest argument in the game for the "non-combatants who
belong in a dungeon" idea — a prisoner, a dying English soldier, a trapped scholar. One
per map is four conversations and takes the act from one quest to five.

## Section 7 — The English Shrine

The emptiest act in the game: 49 nodes written across 11 maps, and the ratio is worse than
that suggests because three of those maps share one 5-node tree between them.

| Map | ents | convs | nodes | spawns | Work |
|---|---|---|---|---|---|
| 01 Outside Shrine | 43 | 0 | 0 | 0 | An empty threshold. A gatekeeper belongs here. |
| 02 Temple Initiate | 669 | 7 | 33 | 245 | The act's only real hub. 57 balloons, 21 gated replies. |
| 03 Stone Chamber | 626 | 0 | 5 | 259 | Silent. |
| 04 Antechamber of Lore | 493 | 0 | 5 | 181 | Named "of Lore" and contains none. |
| 05 Exalted Chambers | 254 | 4 | 20 | 64 | The best of the interior maps. |
| 06 Meditation Chamber1 | 71 | 0 | 5 | 11 | Three near-identical rooms sharing one tree. |
| 07 Meditation Chamber2 | 44 | 0 | 5 | 16 | As above. |
| 08 Meditation Chamber3 | 106 | 0 | 6 | 29 | As above. |
| 09 Secret Chamber | 191 | 0 | 6 | 73 | Silent. |
| 10 Inner Sanctum | 148 | 0 | 0 | 49 | **The act's final map has no dialogue at all.** |
| England to Alamut | 52 | 0 | 0 | 10 | Transition. Leave it. |

**The plan for the act.** Inner Sanctum ending in silence is the single most fixable thing
in Lionheart: a boss with no words. Give it a confrontation. Then differentiate the three
Meditation Chambers — they are the same room three times, and one tree between them proves
it was known at the time. The 14 unused `English in Caverns of Nostrodomus` templates
belong here as much as they do in act 5.

## Section 5 — Nostrodomus

Two good maps and eight corridors. Unlike the Crypt, the good maps are genuinely good —
Heart Entrance reaches 209 nodes and 21 gated replies.

| Map | ents | convs | nodes | spawns | Work |
|---|---|---|---|---|---|
| 01 Heart Entrance | 439 | 5 | 209 | 164 | Strong. Leave it. |
| 02 Clan of the Hand A | 1050 | 0 | 12 | 336 | A named faction with nothing to say. Give the Clan a voice. |
| 03 Tourniquet of Pain | 595 | 0 | 17 | 149 | Silent. |
| 04 Clan of the Skull B | 843 | 0 | 14 | 291 | As Clan of the Hand: two rival clans, zero dialogue between them. |
| 05 Nostrodomus Demesne | 138 | 9 | 66 | 24 | The act's set piece. Fine. |
| 06 Cave 1 | 93 | 0 | 6 | 10 | Filler. |
| 07 Cave 2 | 310 | 0 | 0 | 110 | Silent filler. |
| 08 Cave 3 | 337 | 0 | 20 | 143 | Filler. |
| 09 Cave 4 | 376 | 0 | 0 | 77 | Silent filler. |
| 10 Cave 5 | 92 | 0 | 14 | 44 | Filler. |

**The plan for the act.** Two named clans — Hand and Skull — that never speak is a premise
already written into the map names. A faction the player can side with across those two
maps is the highest-value addition in the act, and it uses the faction gates that already
work everywhere. Caves 1-5 are where the cut English force should be fielded for variety.

## Section 2 — Montserrat

Five maps and **eleven authored nodes**. Per map this is the thinnest writing in the game;
it only looks better than the Shrine because companions carry lines in.

| Map | ents | convs | nodes | spawns | Work |
|---|---|---|---|---|---|
| 01 Grove Exterior | 969 | 3 | 159 | 321 | The druid grove. Three conversations for a whole faction's home. |
| 02 Druid Council Level1 | 466 | 0 | 0 | 158 | **A council chamber with no council.** |
| 02 Druid Council Level2 | 511 | 1 | 11 | 120 | One conversation, 3 quests. |
| 3 Animal Den | 78 | 0 | 0 | 22 | Silent. |
| 4 Animal Cave | 216 | 0 | 0 | 72 | Silent. |

**The plan for the act.** "Druid Council Level1" is a room built for a scene that was never
written. Individual druids to talk to, disagreeing with each other about the player, is
the obvious fix and the act is short enough to finish. Highest new-writing value per map
in the game.

## Section 6 — Barcelona Attack

A siege. High density is correct here and thinning it would be a mistake. The problem is
different: the city you spent act 1 in has almost nothing to say while it burns.

| Map | ents | convs | nodes | spawns | Work |
|---|---|---|---|---|---|
| Blacksmith map | 21 | 3 | 43 | 1 | Fine. |
| Church Crypt Interior Siege | 8 | 0 | 0 | 0 | Empty shell. |
| Church Interior ruined | 40 | 0 | 3 | 0 | Ruined and silent. Survivors belong here. |
| Crossroads Siege | 797 | 0 | 0 | **435** | 435 spawns, not one word. The densest silent map in the game. |
| Crossroads to England map | 135 | 3 | 20 | 79 | Fine. |
| Gate District Siege | 730 | 1 | 86 | 239 | 33 balloons doing the work of conversations. |
| Temple District Siege | 868 | 0 | 28 | 337 | References 123 quest paths — a bulk state-setting script, not 123 quests. |
| Weng Choi Shop Siege | 34 | 2 | 33 | 1 | The one shop that survived, and it works. Use it as the pattern. |

**The plan for the act.** Do not thin, except Crossroads Siege. Add survivors to the
Church and the Gate District — Weng Choi Shop Siege shows the developers' own pattern for
"the shopkeeper you know, now under siege", and it is the most affecting thing in the act.

## Sewers

Front half is a real place; back half is four numbered dungeons.

| Map | ents | convs | nodes | spawns | Work |
|---|---|---|---|---|---|
| 01 Sewer Main Entrance | 980 | 8 | 39 | 155 | Fine. 73 loot sources. |
| 02 Thieves Congregation | 1012 | 20 | 70 | 170 | Strong. 9 quests. |
| 03 Unholy Oubliette | 480 | 0 | 0 | 193 | Silent, and 193 spawns. |
| 04 Hall of Beggars | 1505 | 6 | 51 | 166 | Strong: 36 gated replies, 11 quests. |
| 05 Troll Pit | 558 | 1 | 12 | 89 | Thin. |
| 06 Dungeon1 | 108 | 0 | 3 | 28 | Numbered filler. |
| 07 Dungeon2 | 228 | 0 | 3 | 68 | Numbered filler. |
| 08 Dungeon3 | 226 | 0 | 3 | 64 | Numbered filler. |
| 09 Secret Quest | 281 | 0 | 3 | 114 | Named for a quest it does not contain. |

**The plan.** The 11 unused Sewer Thieves templates belong in Dungeons 1-3, which would at
least make them varied. "09 Secret Quest" is a map named after content that was cut — the
best candidate in the section for a restored objective.

## Section 8 — Alamut

Better than its reputation: 707 reachable nodes, and the finale works. The middle sags.

| Map | ents | convs | nodes | spawns | Work |
|---|---|---|---|---|---|
| 01 Desert Sprawl | 4184 | 6 | 64 | 168 | Huge and fine. |
| 02 Shifting Dunes | 5584 | 9 | 178 | 226 | The largest map in the game. Fine. |
| 03 Sand Dragon | 441 | 1 | 10 | 4 | A set piece. Fine. |
| 04 Maw of the Assasin | 865 | 1 | 4 | 242 | Named for assassins who do not speak. |
| 05 Acid Wash | 249 | 0 | 0 | 45 | Silent. |
| 06 Chamber of Torment | 1053 | 0 | 27 | 330 | 330 spawns, no conversation. Prisoners belong in a torture chamber. |
| 07 Dark Temple | 522 | 1 | 208 | 245 | Fine. |
| 08 Final Encounter | 205 | 15 | 58 | 22 | The finale, and it is well built. |
| END GAME Calle Perdida | 236 | 16 | 144 | 0 | Ending. 29 gated replies. Leave alone. |
| END GAME Nostrodomus Demesne | 106 | 4 | 5 | 1 | Ending. Leave alone. |
| END GAME Siege Map | 266 | 3 | 9 | 9 | Ending. Leave alone. |

**The plan.** Chamber of Torment is the one obvious addition. Otherwise thin 04 and 06 and
leave the act alone — the endings are reachable and the branch logic is engine-side.

## Sections 1, 3 and Wilderness — repair, do not rebuild

These work. Touch them only where something is broken or where cut content belongs.

**1 Barcelona (36 maps).** Nothing to add. It holds 48 of the 84 broken links, in 17 files
— by far the biggest share of phase 1, and those files are reachable from five other
sections because companions carry them.

**3 Montaillou (17 maps).** The strongest late act and the bar to aim at: Hamlet Exterior
alone has 102 conversations and 1006 reachable nodes. Two jobs here — the cut
`Help Andre the Titan with his tasks` quest belongs in Titan Village (61 conversations, 44
spawns, already the right shape), and the act holds 20 broken links in 5 files.

**Wilderness (43 maps).** Healthy but repetitive: nine Goblin House Interiors share one
55-node tree between them, and the five `Random *` maps have 2 nodes each. This is where
the **Goblin Girl** and `goblinguards` belong — Goblin Warrens already has 15
conversations, 9 quests and 304 reachable nodes, so the village exists and she was cut
from it. That answers open question 3 in the design doc as well as it can be answered
without finding a placement record.

## Cross-cutting: the 84 broken links, by area

Phase 1 is not per-map — links live in dialogue files, which are shared. It is per area:

| Area | Files | Broken | Reached from |
|---|---|---|---|
| 1 Barcelona | 17 | 48 | Barcelona, Montserrat, Montaillou, Crypt, Nostrodomus, Wilderness |
| 3 Montaillou | 5 | 20 | Montaillou |
| Wilderness | 9 | 11 | six sections plus Alamut |
| 6 Barcelona Attack | 1 | 2 | Barcelona Attack |
| 8 Alamut | 2 | 2 | no map references these files |
| 4 Crypt | 1 | 1 | Crypt |

Barcelona and Montaillou are 68 of the 84. Doing those two areas first fixes 81% of the
link rot and covers every act that borrows their trees.

The three targets that are not IDs at all, for the record:

- `Fish Monger`, node `10 other questions`: "Goodbye." -> `5 Goodbye.` (stray full stop)
- `Fish Monger`, node `20 fish`: "Goodbye." -> `I'll be leaving now.` (reply text in the
  target field)
- `Demonic Spirit`, node `500 divine explanation demon`: "What is a Daeva?" ->
  `500 daevas explanation elemental`

## Cross-cutting: the 17 silent maps

Maps with enemies, no conversation and no balloon — nobody says anything on them at all:

Crossroads Siege (435), Unholy Oubliette (193), Misc Crypt 3 (171), Misc Crypt 2 (161),
Druid Council Level1 (158), Nostrodomus Cave 2 (110), Ravine Cave West (107), Abandoned
Cave (92), Nostrodomus Cave 4 (77), Animal Cave (72), **Inner Sanctum (49)**, Acid Wash
(45), Misc Crypt 1 (41), Old Ship 10 Luck (36), Misc Crypt 4 (26), Animal Den (22),
England to Alamut (10).

A single balloon line on entering each is the cheapest possible improvement in the
project — `CDisplayDialogBalloonAction` has 1974 uses to copy from, and it needs no NPC.
Inner Sanctum being on this list is the one that matters: it is a final boss room.

## Cross-cutting: reactivity to the player's choices

Lionheart has a complete, general, data-only reactivity system and ships with most of it
switched off. This is the cheapest quality per hour available anywhere in the project,
because almost none of it needs new machinery — only new writing against machinery that
already works.

### How a gate works

`Requirement=` on a reply does not name a built-in check. It names a **`.can` expression
file**, and 609 of them ship — 290 shared under `Resources/Dialog/Requirements/`, 319
area-local beside the dialogue that uses them. Each is a small comparison:

```
Object=CIsGreaterThan
    Operand1=CVariableDerivedCharacterAttribute
        Character Attribute=Derived Character Attributes/Uber Perks/Templar Rank
    Operand2=CConstant  Constant Value=0
```

That file is `Templar IS`. Every axis works the same way, so **anything expressible as a
number is gateable, and adding an axis is authoring a file rather than patching an
engine.**

### What is built against what is used

1568 of 10,915 replies are gated — 14%. By category:

| Axis | Gates built | Ever used | Replies |
|---|---|---|---|
| Speech | 42 | 25 | 239 |
| Faction rank | 15 | 8 | 264 |
| Race | 10 | 5 | 167 |
| Barter | 43 | 18 | 95 |
| Attributes (ST/PE/IN/CH/AG/LK) | 50 | 16 | 65 |
| **Karma** | **78** | **2** | **4** |
| **Lockpick** | **18** | **0** | **0** |
| **Sneak** | **4** | **0** | **0** |
| **Outwit and other derived** | **13** | **0** | **0** |
| **Monster races** (Dragon/Goblin/Titan/Undead) | **4** | **0** | **0** |
| **Magic school totals** | **3** | **0** | **0** |
| area-local | 319 | 244 | 657 |

Beyond the library, `Custom Requirement` embeds arbitrary expressions. What the game
already leans on: **entity existence, 1179 uses** of `CCheckExistenceAction` — this is how
it asks "is that person still alive"; quest state (413 current, 238 ever-activated, 106
completed, 15 failed); inventory 292; money 159; traits 32; race 11.

State is stored as derived character attributes, including a general-purpose namespace,
`Derived Character Attributes/Game Scripting Variables/`, holding 28 shipped flags —
`Herbalist Dead`, `Woodcutter Dead`, `River Dryad Dead`, `FACTION LEADERS KILLED`,
`Goblin Kill Counter`, `Player has heard Grumjun poetry`.

### The two big gaps

**Karma is real and unused.** `Derived Character Attributes/Karma`, with 78 threshold
gates authored from 50 to 1950 — and the shipped game gates **four replies**, on
`Karma equalless 400` and `Karma equalless 650`. Outside that library only seven files
read karma at all, and one of them is a developer tool: Shylocke's shop, Nostradamus'
demesne, Crossroads, Plains, and the `BrotherMichel` and `Nostradamus` conversations. A
full good/evil axis was built and never wired into the writing.

**Perks are barely checked.** 98 exist; 20 are awarded by script and only 17 are ever
checked. Nine live in a folder called `!NPC or Event Given Perks`. The reactive ones are
already there and mostly idle: `Child Killer`, `Merchant Slayer`, `Ruler of Calle Perdida`,
`Exposer of Calle Perdida`, `Free Demon in Inquisition`, `Goblin Champion`, `Thief Friend`,
`Beggar Friend`, and `FACTION Inquisitor / Templar / Saladin / Wielder Killer`. **Those
four faction-killer perks are awarded and almost never reacted to** — you can destroy a
faction's leadership and nobody mentions it.

Factions themselves are 13 records in four families of three ranks (Inquisitor
Acolyte/Hallowed/Inquisitor, Templar Squire/Warden/Paladin, Saladin Aswaran/Blessed/
Exalted, Wielder Conjurer/Mage/Wizard), assigned by `CAssignFactionToCharacterAction` at
29 sites and read as `Uber Perks/<family> Rank`.

### Adding a new axis — proven, four steps

1. **Define the variable** — a `.DerivedCharacterAttribute` file, `Expression=CConstant{0}`.
2. **Raise it at the moment of choice** — `CAddCharacterModifierToCharacterAction` holding
   a `CCharacterModifierDerivedAttribute` on `$Instigator`. `Allow Accumulation=1` makes it
   a counter rather than a flag.
3. **Gate on it** — a new `Requirements/*.can` comparing it to a constant.
4. **Name that file** in `Requirement=` on a reply.

**This was the open risk and it is now closed.** Every `.can` and every `.zax` enumerates
the full derived-attribute list inline, so it was not obvious a new attribute could be
added without sweeping 1698 templates. It can: the round trip is live in `test-pocket` on
Lucia and was confirmed in-game **on a save whose character predates the attribute**, which
is the harder case. New tracked state costs three files.

One caution learned from that test: Lionheart has **no cancel key** in dialogue. Every
conversation is left by choosing a reply that ends it, so any node added behind a gate
needs its own way out. The editor's `no way out` check covers it.

### What to add, in order of cost

1. **Turn karma on.** 76 unused gates, no new mechanism. Two or three karma-gated replies
   per major NPC is authoring only, and it is the axis players most expect to matter.
2. **React to the faction-killer perks.** Already awarded. Highest drama per line available.
3. **Use `CCheckExistenceAction` for consequence.** 1179 uses of machinery already exist —
   "you killed the herbalist, and his brother knows" needs no new system.
4. **Lockpick and Sneak gates.** 22 files built, zero uses. Non-combat solutions for thief
   builds, which is the most direct answer to "your build stops mattering after Barcelona".
5. **New flags for Fixt's own content**, per the recipe above. The goblin village and the
   Titan quest both want "how did you resolve this" memory.

Items 1 to 4 need nothing that does not already exist. Note how this pairs with the
per-act reading above: the design doc found that the *share* of gated replies barely falls
across the game (38% in Barcelona to 27% in the Crypt) — what collapsed was the volume of
dialogue to gate. Reactivity is not a system to repair. It is writing to attach to a system
that already works.

## Cross-cutting: companions

Three complaints are usually made about companions — they die instantly, they never level,
and there is nothing to them once they join. All three are true, each has a different
cause, and two are data edits rather than design work.

### They die because their toughness is a fixed preset

A companion's durability comes from a `Value To Preset` on their `.Race`, and presets do
not move. The player's does: `(HP) Hit Points` is computed as roughly
`15 + 2*EN + (CVariableCharacterLevel - 1) * <an Endurance term>`, so the gap widens every
act while the companion stands still.

| Companion | HP | AC | |
|---|---|---|---|
| Cub Companion | 27 | 50 | |
| Distressed Sailor | 36 | 90 | |
| Bear | 39 | 80 | |
| Cervantes | 60 | 50 | |
| Conquistador | 60 | 75 | |
| **Grumdjum** | **225** | **200** | |
| Beatrice | 12 | 60 | *fragile on purpose — see below* |

For scale: an Alamut Assassin is 150 HP / 280 AC, an Ogre 83 / 215. Cervantes joins in
Barcelona at 60 HP and is still at 60 HP in the Crypt.

**Grumdjum is the proof.** He is the companion players remember as actually useful, and the
only thing separating him from the others is that he is built on a race with real numbers.
A survivable companion is a value, not a system.

**Beatrice is the exception that must not be "fixed".** She is a woman transformed into a
chicken — her entire dialogue is `Bawk bawk bawk!`, her voice lines are
`Beatrice Chicken Cluck 10-50.ogg`, and the recruiting reply is *"Come with me, I will help
you get right again."* She is an escort to protect, so 12 HP is the design, and raising it
would remove the quest.

### Which is why the roster has to be split by role first

Reading each recruiting line makes the division obvious, and it is not the division the HP
column suggests:

| Fighters — offer their sword | Escorts — the quest is delivering them alive |
|---|---|
| Cervantes — *"Sure, come with me."* | **Beatrice** — clucks; take her to be cured |
| Sir Roger — *"My sword is yours against the..."* | **Inquisitor Darsh** — *"I will escort you back to Barcelona."* |
| Lost Knight — *"with your help, I'm sure we can fight our way out"* | **Distressed Sailor** — *"Help! Someone, I need help quickly!"* |
| Conquistador — *"Are you my next challenger? Glory is my destiny!"* | |
| Diego, Joan of Arc, the Saladin knight, Grumdjum, Bear, Cub | |

For the escorts, fragility *is* the content — making them tough deletes the quest. Only the
fighters should be touched. Low numbers here are not automatically defects; check what a
companion is for before changing it.

Worth recording while we were in there: the developers built an `Invulnerable Chicken`
race — 1337 HP, 1337 AC, 1337 healing rate — and an
`Invulnerable Chicken Companion.can` to go with it. It is placed on exactly one map, the
`Fighting Test` scratch map, so the shipped escort can die. Whether that was a decision or
an oversight is arguable; either way the lever for "should this escort be failable" already
exists and is not the HP preset.

### They never level, though the action to do it already ships

Every companion template is `Character Level=1`. `CSetCharacterLevelAction` is used **13
times across 11 campaign maps** as a level *floor for the player* at act boundaries — Grove
Exterior sets 8 then 10, Hamlet Exterior 12, Burial Chamber 16, rising to 28.

Its field is `Character to give experiecne to` (the engine's own typo) and **it takes a
character name**. In all 13 campaign uses it reads `$instigator`. Pointing those same
act-boundary actions at whichever companions can be present is close to free.

One thing to establish before relying on it: the field is named "give experience to", so
whether setting a level re-derives HP and skills or merely stamps a number wants the same
one-NPC experiment that settled the new-attribute question.

### There is no plot because there is no post-recruitment content

Fourteen dialogues recruit a companion — `cortes` (78 nodes), `Cervantes` (53),
`JoanofArc` (38), `Distressed Sailor` (31), `Inquisitor Darsh` (29), `Beatrice` (21),
`Crazy Goblin Trapped Conquistador` (18), `SirRoger` (17), `Diego` (10),
`alamutknightsaladin` (9), `Lost Knight` (9), `RED FILE underground characters` (8),
`War Golem Companion` (6), `Bear Companion` (2).

Once they join, the entire interaction surface is `Generic Companion Dialog`, referenced
exactly once in the game. In full:

> **"What would you like your companion to do?"** -> *Release Companion* / *Nothing*

One node. That is the whole of it — except for Grumdjum, who has 42 nodes and three wired
`companion quips` voice lines. Banter exists, was recorded, and works, for one companion
out of fourteen.

**Captain Isabella is cut content.** 43 dialogue nodes, recorded companion voice lines
including `502 grace joined companion` and `502 grace companion asked to return` — and
**zero** `CSetCompanionAction`. Two of her companion VOs are referenced by nothing. She was
meant to be recruitable and the wiring never landed.

### What to do, cheapest first

1. **Raise the presets — for the fighters only.** Scaling Cervantes, Sir Roger, the Lost
   Knight, the Conquistador and the animals toward Grumdjum's numbers addresses the
   complaint players actually voice, and it is a handful of values. Leave the three
   escorts — Beatrice, Darsh and the Distressed Sailor — exactly as they are; their
   fragility is the quest.
2. **Point the act-boundary level actions at companions.** Reuses shipped machinery at the
   exact moments the game already thinks about levels.
3. **Wire Isabella.** Recorded voice, 43 nodes, needs the recruit action. Restoration, not
   invention — and it belongs with the phase 2 cut-content work.
4. **Copy Grumdjum's quip pattern to the other thirteen.** Proven in the shipped game, and
   it is the reactivity work above pointed at companions: `CCheckExistenceAction` already
   answers "is this companion still alive", which is most of what banter needs to know.

Item 4 also answers the open question about whether a balloon can fire against a companion
who may or may not be following: Grumdjum's wiring is a working example to read the answer
off, rather than something to test blind.

## Suggested order

1. **Link repair, Barcelona and Montaillou first** — 68 of 84, ships standalone, needs no
   new writing.
2. **Cut content into its right home** — Goblin Girl into Goblin Warrens, the Titan quest
   into Titan Village, Guard Pablo into Temple District. All three go where the section
   already works, so a mistake is visible immediately.
3. **The silent maps** — one balloon each, 17 maps, no new NPCs.
4. **Inner Sanctum and Druid Council Level1** — the two rooms most obviously built for a
   scene that was never written. Small, self-contained, high value.
5. **Companion presets and levelling** — a handful of numbers and a reused action, and it
   fixes the loudest complaint after the content collapse itself. Isabella's recruit wiring
   goes with step 2, being restoration.
6. **Karma and the faction-killer perks** — pure writing against gates that already exist,
   and it can ride along with any of the above rather than being a phase of its own.
7. **The Crypt's quests** — the act's real problem, and the largest single job here.
8. **Thinning** — last, and only after the acts have more to do. `Max Party Mojo` still
   needs understanding first.

## Still unanswered

- **What is `Max Party Mojo`?** 7493 generators carry it. Thinning waits on it.
- **Andre or Marcus?** The cut Titan quest disagrees with itself.
- **Do companion balloons need the companion present?** Decides whether banter is cheap or
  not. Grumdjum's three wired `companion quips` are a working example to read the answer
  off rather than a blind test.
- **Does `CSetCharacterLevelAction` re-derive HP and skills, or only stamp a number?** Its
  field is named "give experience to", which suggests the former. Companion levelling
  depends on the answer, and one NPC settles it.
- **What does `Is Default Reply` actually do?** Not the cancel binding — an in-game test
  disproved that. 874 of the 959 blank, unclickable replies carry it, which reads as
  auto-advance, but that is a clue rather than an answer. It matters because 2894 replies
  have it and new writing has to decide whether to.
- **What moves Karma?** Seven files read it and nothing in the data appears to write it, so
  it is presumably engine-maintained. Turning karma on means knowing what raises and lowers
  it, or setting it explicitly the way any other scripting variable is set.
- **Why does Barcelona measure 16.8 spawnable entries per map here against the design
  doc's 8?** Every other section reconciles to within a few percent; this one does not, and
  it should be chased before any Barcelona thinning (though none is planned).
