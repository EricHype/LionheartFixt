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

## Suggested order

1. **Link repair, Barcelona and Montaillou first** — 68 of 84, ships standalone, needs no
   new writing.
2. **Cut content into its right home** — Goblin Girl into Goblin Warrens, the Titan quest
   into Titan Village, Guard Pablo into Temple District. All three go where the section
   already works, so a mistake is visible immediately.
3. **The silent maps** — one balloon each, 17 maps, no new NPCs.
4. **Inner Sanctum and Druid Council Level1** — the two rooms most obviously built for a
   scene that was never written. Small, self-contained, high value.
5. **The Crypt's quests** — the act's real problem, and the largest single job here.
6. **Thinning** — last, and only after the acts have more to do. `Max Party Mojo` still
   needs understanding first.

## Still unanswered

- **What is `Max Party Mojo`?** 7493 generators carry it. Thinning waits on it.
- **Andre or Marcus?** The cut Titan quest disagrees with itself.
- **Do companion balloons need the companion present?** Decides whether banter is cheap or
  not.
- **Why does Barcelona measure 16.8 spawnable entries per map here against the design
  doc's 8?** Every other section reconciles to within a few percent; this one does not, and
  it should be chased before any Barcelona thinning (though none is planned).
