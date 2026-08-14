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

The front half is also where the Thieves' and Beggars' guild war lives, which is act 1's
real opportunity — see [Act 1 — the choices that go
nowhere](#act-1--the-choices-that-go-nowhere).

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

**1 Barcelona (36 maps).** Nothing to add *density*. It holds 48 of the 84 broken links, in
17 files — by far the biggest share of phase 1, and those files are reachable from five
other sections because companions carry them. But the act does have a real opportunity that
is not about volume: see [Act 1 — the choices that go nowhere](#act-1--the-choices-that-go-nowhere).

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

## Act 1 — the choices that go nowhere

Barcelona and the Sewers do not need more content. They need the content they have to
*matter later*. The clearest case is the Thieves' and Beggars' guild war, which is the
best-implemented faction choice in the game and the least consequential.

### The guild war is fully built

Two symmetric, mutually exclusive ladders:

| Thieves — Juanita Suarez | Beggars — Enrique Garcia |
|---|---|
| `TASKS OF THE THIEVES' GUILD` (4 states) | `AID THE BEGGAR GUILDMASTER` (2 states) |
| Collect Dues in Port District | Destroy the Lava Trolls |
| Recover Juanita's Stolen Locket | Discover a cure for wererat lycanthropy (5 states) |
| Steal from a Noble's house | Steal from the Inquisition |
| **Kill the Beggar Guildmaster** | **Kill the Thief Guildmistress** |

Even the framing mirrors: `Find Juanita` calls her *"leader of the Thieves Guild and enemy
of the rival Beggars"*, and `Find Enrique` says the same in reverse.

**And it is genuinely exclusive** — 30 `CSetQuestSatusToFailed*` links. `02 Thieves
Congregation` closes the beggar path, `04 Hall of Beggars` closes the thief path, and
Juanita's own dialogue fails her rival's questline. The tracking is detailed to match:
`Beggar leader requires you to have killed Juanita`, `Juanita requires PC to have killed
Beggar leader Enrique Garcia`, and a romance subplot with a 9-node `Juanita Seduction` tree
and a requirement file for having *refused* her at node 140.

This is the proof the developers knew how to build exclusivity — which is exactly what the
goblin faction lacks. **The guild war has exclusivity and no reach; the goblin faction has
reach and no exclusivity.** The two fixes are opposites.

### Its reach is zero

`Thief Friend` and `Beggar Friend` are each **awarded and checked by exactly one NPC, the
one that grants them.** Neither perk is referenced anywhere else in the game.

The apparent exceptions are not exceptions. Barcelona's `Juanita` references are the thief
questline reaching outward — her henchman shaking down a debtor in the Port District — not
the world reacting to your allegiance. Every act 6 reference is `Temple District Siege`
failing the quests in its cleanup sweep.

You choose a side, kill a guild leader, take a title perk, and acts 2 through 8 never
mention it. Neither do the endings.

### The Afflicted are a three-way that nobody finished

Three factions already have written positions on the sewer lycanthropes:

| Faction | Quest | States |
|---|---|---|
| Beggars | `Discover a cure for wererat lycanthropy` | 5 |
| Inquisition | `Deal with the Afflicted in the Sewers` | 2 |
| Temple District | `Investigate the Beggar Menace in the Sewers` | **0, and unofferable** |

Cure them, exterminate them, or — the missing third — treat the beggars themselves as the
infestation. Two of the three are shipped and finished. This is the strongest unclaimed
story in act 1.

Two further cut resolutions belong to the same thread, both among the 21 unofferable
quests: **`Rob the Thief Guildhouse`** (side with neither) and **`Convince the Thief
Guildmistress to leave the Sewers`** (the non-violent ending the war visibly lacks).

### What to do

1. **Gate replies on the two title perks outside the Sewers.** They exist, they are
   awarded, and nothing reads them. A fence in Montaillou who treats a `Thief Friend`
   differently costs one requirement file and one reply. This is the single cheapest piece
   of long-range reactivity in the project.
2. **Feed karma.** Killing Enrique or Juanita moves nothing today, while killing the
   Barmaid does.
3. **Restore the two cut resolutions**, so the war has a neutral and a peaceful ending.
4. **Finish the Afflicted three-way**, which needs one side written rather than three.

Note what is *not* on this list: new quests for Barcelona. The act has 88 quests and 125
reachable dialogue nodes per map. Its problem is consequence, not volume.

## The Knights of Saladin — a minor faction, three repairs and one small addition

Saladin is a **minor** faction and should stay one: it gets reactivity, not the Inquisition's
content budget. Fortunately almost nothing needs writing, because the order is already
built — three ranks with stat bonuses, 8 initiation quests with 18 states, and reactivity
scattered across five acts. What it has are three specific breaks.

### 1. Favoured One never becomes Saladin Rank

The Dream Djinni trials award `Dervish of the Crescent` — *"You have become a **Favored One
of the Knights of Saladin**"* — and `Scholar of the Crescent`. That questline is reachable
and completable.

But those perks confer only skills (Dervish: +5 to five Fighting skills; Scholar: +1 IN,
+5 Speech). `Dream Djinni Map.zax` performs **0 faction assignments and 0 derived-attribute
writes**. Meanwhile `Saladin IS` tests `Uber Perks/Saladin Rank > 0`, and the only things
that increment that rank are the three `.Faction` records — assigned nowhere outside
`James.zax`, a test map.

So the title and the rank are never connected, and **23 `Saladin IS` replies across five
acts can never appear**: Barcelona 9, Montaillou 3 (Brother Michel), Crypt 3 (Joan of Arc
claiming the Bleeding Lance for the Order), English Shrine 7 (Sir Roger), Alamut 1. Plus
node-level greetings — both Barcelona knights have *"Welcome, brother/sister, into the
Order of Saladin"* nodes, and the Alamut companion has male and female Saladin variants.

**Repair:** one `CAssignFactionToCharacterAction` for `Factions/Saladin Aswaran`, beside
the two `Perk to give` calls that already fire in `Dream Djinni Map.zax`. Aswaran is the
entry rank, which matches "Favored One" and leaves Blessed and Exalted as headroom.

Watch the stacking: the faction record adds +10 One-Handed, +10 Two-Handed, +1 Endurance
and +20 carry weight on top of Dervish's +5s.

### 2. The Sacred Scimitar cannot be started

The quest is fully authored. Amir (in `Jafar.DialogTree`, whose `Name` field is
**`Amir Ibn Shazid`** — the same filename-versus-content rename as Andre/Marcus) is meant
to set it; Eduardo the blacksmith has a complete parallel branch to the Templars' Lion
Shield, with a test of valour (recover his father's sword from the beggar Felgnash in the
Sewers), a material hunt (magnetized silver), and **six** ways to talk past the test
(Speech 25/35, CH 6+, IN 6+, Barter 25 with 100 gold, or Feralkin with IN 4+). The item
`Sacred Scimitar Saladin Quest.InventoryItem` exists.

Three things are broken, at both ends and in the middle:

| Break | Detail |
|---|---|
| **The starter is switched off** | The only thing that sets state `53F5R12P` is an entity named `warp` in `Blacksmith map.zax`, tagged `Comment=activate find scimitar quest`, with **`Active=0`** and **`X Radius=0`** — a deactivated, zero-radius proximity trigger |
| **Amir never offers it** | Node `202 make a scimitar` says *"I have decided on your second task"* and its only reply goes to `210 give shard quest` — the Shard of Dreams. The node kept the scimitar name after being rewired |
| **Amir cannot receive it** | *"I have forged the Sacred Scimitar."* -> `210 have scimitar`, which does not exist — and that reply carries the quest's `CSetQuestSatusToCompletedAction` |

### The second task was a fork

`202 make a scimitar` is not a mis-named passthrough — it is a **choice point that lost one
of its arms**:

> *"&lt;Amir stops speaking, appears to contemplate something for a few moments, and then
> resumes&gt; Hmmm. Yes, yes, **I have decided on** your second task."*

He deliberates and then picks. There is nothing to deliberate if only one task exists. The
numbering agrees: `210 give shard quest` and the missing `210 have scimitar` share a
number, which is what happens when one branch is written over another rather than added
beside it.

The intended shape, then:

```
201 ali continued
      |
202 make a scimitar          "I have decided on your second task"
      |                    \
210 give shard quest        (scimitar assignment -- MISSING)
      |                        |
215 shard                   210 have scimitar -- MISSING
      \                        /
        120 donate gem  ->  trials  ->  230 knight of saladin  ->  Favored One
```

Two arms of one fork, converging on the gem and the trials. What survives is the shard arm
plus both ends of the scimitar quest itself — Eduardo's full branch, the item, the
requirement files — with only Amir's two nodes gone.

**Restoring it means making the fork real again:** `202` offers both, each arm assigns its
quest, each has a receipt node, and both lead to `120 donate gem`. The player does one or
the other, not both.

**Repair, and why not the obvious one.** Re-enabling the `warp` trigger is tempting and
wrong: it is ungated, so it would hand the quest to every player who walks into the smithy,
which is plausibly why it was switched off. Do it through Amir instead, matching the quest's
own text (*"Bring Scimitar to Amir in Gate District"*):

1. Give `202 make a scimitar` two replies rather than one, so Amir's deliberation ends in an
   actual choice — the scimitar or the Shard.
2. Author the scimitar assignment node, activating state `53F5R12P`, so the quest can start
   without the dead trigger.
3. Author `210 have scimitar` as the receipt, mirroring `215 shard`: acknowledge, then send
   the player on to `120 donate gem`. Retarget the existing hand-in reply to it.
4. Leave the dead `warp` trigger alone.

This is the project's best first content job: self-contained, entirely in act 1, restores a
finished questline rather than inventing one, and exercises the node authoring the dialogue
editor just gained.

### 3. Reward the route, not just the completion

The Saladin line already contains the pattern, shipped and working. The Dream Djinni trials
branch on *how* you win:

| Route | Reward |
|---|---|
| Beat Kabool's champions in combat | `Dervish of the Crescent` — +5 to all five Fighting skills |
| Beat Kabool in a contest of wits | `Scholar of the Crescent` — +1 Intelligence, +5 Speech |

Two entities, `Give Dervish Perk` and `Give Scholar Perk`, hand them out. Same quest, two
outcomes, chosen by approach.

**The scimitar has the same branching and none of the payoff.** The game already tracks
which route you took:

- whether you retrieved Eduardo's father's sword from Felgnash, or talked past the test
  through Speech 25/35, CH 6+, IN 6+, Barter 25 with 100 gold, or Feralkin indignation
- whether he offered you payment for the retrieval — a flag entity literally named
  `Blacksmith offered payment`, checked by `CCheckExistenceAction`, giving two separate
  nodes, `50 Got Sword Payment` and `50 Got Sword No Payment`

And then **node `64 here is your scimitar` hands the identical
`Sacred Scimitar Saladin Quest` to everyone.** The same is true of the Templars' Lion
Shield at `63 here is your shield`.

Eduardo argues the case himself:

> *"Fashioning a Sacred Scimitar… it requires a test of valor, of bravery on the part of the
> owner to give the scimitar its strength, its spiritual center."*

By the game's own fiction, a scimitar forged for someone who bartered their way out of the
test should not be the same weapon. Proposed differentiation, using the state that already
exists:

| How you got it | Reward |
|---|---|
| Retrieved the sword, refused payment | the Sacred Scimitar as it ships (+5% critical), and karma |
| Retrieved the sword, took payment | the scimitar and the gold, no karma |
| Talked or bartered past the test | a plain scimitar — no critical bonus. He never got his father's blade back, and said himself where the enchantment comes from |

That is one new `InventoryAddition` variant and a gate on an existing node, not new content.

**And restoring the fork creates a second, larger split.** Once `202` offers a real choice,
the two arms should not pay out the same way, because they are different kinds of deed:

| Second task | What it costs | What it should return |
|---|---|---|
| **Forge the Sacred Scimitar** | errands in Barcelona and the Sewers, and a test of valour | the weapon — a personal arm, earned |
| **Recover the Shard of Dreams** | a raid on the slavers' lair in the Wilderness | standing with the order, and a treasure surrendered to it |

The scimitar arm ends with the player holding something; the Shard arm ends with the player
handing something over. That asymmetry is already in the writing — Amir's *"Amir is
extremely pleased!"* on receiving the Shard is gratitude for a gift, while Eduardo's
scimitar is made *for* you.

The **gem is not part of this fork** — it is the toll for the trials, paid after either arm,
and its own lever is *which* gem. Handing over the Eye of the Dragon rather than any common
stone is a larger sacrifice and deserves to be noticed.

**The general principle, worth applying beyond Saladin:** where the game already records
*how* a quest was resolved and then pays out identically, differentiating the reward is
cheap reactivity. The thieves-and-beggars war and the goblin threads both qualify — each
already tracks which side you took and rewards both the same.

### 4. A sparring lesson for a real sword

A small designed addition, and the only genuinely new content proposed for this faction.
It costs one node and one custom action because the cast, the staging and the pattern all
already exist.

**The knights are already sparring.** `saladinknightcan` is Farshad ibn Almassizad, and he
says so himself:

> *"Fight? No, I am merely dueling with my twin brother, **Farshid**. He has much to learn
> in the ways of the blade…"*

Twin brothers, mid-duel, in the Gate District beside Amir's tents. Farshid is a named NPC
in his own right — he activates `Seek out Ali Huban`.

**The interaction.** If the player is carrying the Sacred Scimitar, Farshad offers a lesson
now that they have a proper blade. Accepting fades to black over the sound of sparring, and
the player comes back with a few points of One-Handed Melee.

**Every piece has a shipped reference:**

| Piece | Mechanism | Reference |
|---|---|---|
| Gate on carrying the scimitar | `CActionCheckForInventoryItem` on `Quest Items/Sacred Scimitar Saladin Quest` | 653 uses |
| Fade to black | `CFadeScreenDownAction { Time Until Auto Fade Up=3 }` | **the Blacksmith's own forging montage**, `60 Back With Silver`, in the same district |
| Sparring noise | `CPlaySoundAction` with `Sounds/Ambient/Environmental Hits/AMB_barc_attack_SS*.ogg` | 3536 uses; 226 combat-sound candidates |
| Pause between | `CDelayAction` | pairs with the fade in every shipped use |
| Award the skill | `CAddCharacterModifierToCharacterAction` -> `CCharacterModifierSkill` on `Skills/Fighting/OneHandedMelee` | 143 uses, including the Saladin faction records themselves |

The fade needs no counterpart action: `Time Until Auto Fade Up` brings the screen back on
its own, which is why the Blacksmith's montage is self-contained.

**Fire it once.** `CCharacterModifierSkill` with `Allow Accumulation=1` is repeatable, so
without a guard the lesson is a skill farm. Use the derived-attribute recipe — a
`Game Scripting Variables/Saladin Lesson Taken` flag, raised by the same custom action and
checked by the reply's requirement. This is exactly the pattern proved in `test-pocket`.

**Size the bonus against its neighbours:** the Crescent perks give +5 to five skills each,
and the Aswaran rank gives +10 One-Handed and +10 Two-Handed. **+3 One-Handed** is a
noticeable nudge that does not compete with either, and it fits "a quick lesson" rather
than a training arc.

The nice detail is that it reads as a reward for the *scimitar arm* of the second-task fork
specifically — take the Shard instead and the brothers have nothing to teach you, because
you never got the sword. That is reward differentiation expressed as content rather than
as a stat table.

### 5. Nothing else

No Saladin questline expansion, no Montaillou coverage to match the Inquisition's eleven
NPCs, and **no Crown of Thorns work** — `Travel to Montserrat` is already activated by
Jafar, and every other order plus the faction-neutral Brother Montgomerie sends you to
Montserrat anyway.

Minor faction, kept minor: one faction assignment, one restored fork, two reward splits and
a single sparring scene. Everything else it needs, it already has.

## The back half — roleplaying space, and two new areas

Acts 4 to 8 are dungeons, and a dungeon has nobody to talk to. Two responses are needed
together: give the existing maps more to do, and add **one or two genuinely new places**
where the player is not fighting at all. The second matters because there is a limit to how
much roleplaying you can staple onto a corridor.

### There is almost no social space to work with

Counting maps in the back half with at least three conversations and at most 80 spawns —
somewhere you can stand and talk:

| Act | Social maps | Which |
|---|---|---|
| 4 Crypt | 1 | `1 Crypt Entrance` (3 convs, 37 spawns) |
| 5 Nostrodomus | 1 | `05 Nostrodomus Demesne` (9 convs, 24 spawns) |
| 6 Barcelona Attack | 2 | `Blacksmith map` (3 convs, 1 spawn), `Crossroads to England` |
| 7 English Shrine | 1 | `05 Exalted Chambers` (4 convs, but 64 spawns) |
| 8 Alamut | 4 | all of them the `END GAME` maps and the finale |

Across acts 4 to 7 there are **four** such maps, and only one — Nostrodomus Demesne — is a
real hub. Everything else is a fight. That is the pacing complaint stated as a measurement.

### More roleplaying in the areas that exist

Covered per act in the section tables above; the recurring moves are the same four:

- **Non-combatants who belong in a dungeon** — prisoners, survivors, a dying English
  soldier, a trapped scholar. One per silent map takes the Crypt from one quest to five.
- **Objectives that reuse the geography** rather than adding it, so the player walks back
  through a place with a reason.
- **Companion reaction**, which is the only act-1 dialogue that travels into acts 2 to 5.
- **Balloons** on the 17 silent maps, needing no NPC at all.

### New area 1 — built from the Outpost's parts, not from the Outpost

`Levels/Oupost.zax` is the only unused non-test map, it is large (7500 x 4000, 934
entities, 11 working doors) and it is completely peaceful — **zero enemy generators**. The
temptation is to ship it as-is. It should not be shipped as-is: it is a developer scratch
area, and measurement says so throughout rather than only in the corner already known
about.

Cluster its entities and score each cluster by how often it reuses a sprite. A built room
uses a small kit many times; a sampler uses many pieces once each:

| Region | Entities | Distinct sprites | Repeats each |
|---|---|---|---|
| left half (x < 3000) | 601 | 229 | **2.6** |
| right half (x >= 3000) | 333 | 173 | **1.9** |

No 500-unit cell anywhere on the map exceeds 2.8 repeats, and most sit between 1.0 and
1.5 — one placement per distinct piece. The left half is better than the right, which is
why the earlier `outpost-expedition` mod moved the arrival point there, but it is *not*
good; it is a slightly tidier sampler. The tileset mixing says the same thing: the right
half puts `Hamlet/General` and `Heart of Fire` pieces beside Dwarf Region ones.

**So harvest it as a parts bin and a catalogue, not as a place.** Its genuine value:

- It lays out a broad sample of the kit — 229 distinct sprites in the left half alone —
  so it shows an author what exists and what sits together.
- Its coherent fragments (the bridge runs around x=2000, the walled sections along
  x=0-1500, y=1500-2500) transplant as *rooms* into a purpose-built map.
- The tiling vectors this project has already learned came from exactly this kind of
  reading.

**One correction worth recording: the "Outpost" tilesets are not unused.**
`Outpost/Dwarf Region` has 4351 placements game-wide and is really the **Sewers kit** —
Sewer Main Entrance 762, Thieves Congregation 752, Troll Pit 427, Hall of Beggars 367.
`Outpost/Transformed Region` is Hall of Beggars (865), the Secret Red File Level (628) and
Unholy Oubliette (364). The kit is 450 and 139 distinct sprites respectively.

Two consequences. First, a new area built from these parts will read as **underground
stone**, so it should be sited as such — an undercroft or a sheltered cavern, not a
surface settlement. Second, and more useful: the *shipped Sewers maps are the reference
for how to use this kit properly*, at hundreds of placements each. Building the new area
means copying arrangements from `01 Sewer Main Entrance` and `04 Hall of Beggars`, with the
Outpost as the index of what is available.

### The constraint that decides how both are made

**Terrain blending is not solved.** Every shipped exterior blends ground textures
procedurally through `CPlasmaTileMap`; a hand-built map gets one flat unblended texture and
looks it. Test Pocket is the demonstration of that ceiling.

So neither new area can be an outdoor space. Both must be **interiors** — cave, undercroft,
hall — which lean on placed geometry rather than blended ground, and that is the part the
editor does well. It also happens to suit the kit: the Sewers/Outpost pieces are
underground stone.

### New area 2 — a variant of an existing map

The game's own trick for a cheap new place is to copy one and change it:
`13 House4 Interior After Burned`, `Church Interior ruined`, `Weng Choi Shop Siege`, and
the whole of act 6, which is act 1's maps under siege.

A cleared or captured section of the Crypt or the Shrine, repopulated with survivors, costs
a copy and a repopulation rather than a build — and it inherits the original's navigation
polygons, which a hand-built map does not get. That last point is not a detail: the missing
`CWayPointsPolygon` data is why an invisible interaction zone never worked in Test Pocket.

If only one new area gets built, make it this one. It is the cheaper of the two and the
less likely to look wrong.

### Where they slot in

The two worst acts are the Crypt (one quest across ten maps, 296 spawns per map) and the
English Shrine (49 authored nodes, and a final boss room with no dialogue). Nostrodomus
already has its Demesne and does not need one.

- **The built undercroft between the Crypt and Nostrodomus** — a survivors' waystation
  after the act with the least to do in it, assembled from the Sewers kit with the Outpost
  as the parts index. It is also where the cut Sewer Thieves and English templates could be
  fielded as residents rather than enemies.
- **The map variant in or before the English Shrine**, the act that shares *zero* dialogue
  with act 1 and therefore has no other way to hear about anything you have done.

Neither reuses `Oupost.zax` itself. The existing `mods/outpost-expedition` stays what it
is — a way to go and look at a developer sandbox — and is not the foundation for either.

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

The Karma row counts **dialogue replies only** and understates the system badly — see
below. Map scripts test karma too, and the finale decides your ending on it. What that row
really measures is how rarely a *character* remarks on your morality.

Beyond the library, `Custom Requirement` embeds arbitrary expressions. What the game
already leans on: **entity existence, 1179 uses** of `CCheckExistenceAction` — this is how
it asks "is that person still alive"; quest state (413 current, 238 ever-activated, 106
completed, 15 failed); inventory 292; money 159; traits 32; race 11.

State is stored as derived character attributes, including a general-purpose namespace,
`Derived Character Attributes/Game Scripting Variables/`, holding 28 shipped flags —
`Herbalist Dead`, `Woodcutter Dead`, `River Dryad Dead`, `FACTION LEADERS KILLED`,
`Goblin Kill Counter`, `Player has heard Grumjun poetry`.

### The two big gaps

**Karma is fully implemented, drives the ending, and is never mentioned in between.**
`Derived Character Attributes/Karma` is written at **213 sites across 86 files** — 101 in
dialogue, 64 in map scripts, 47 in character templates and one in a perk. Amounts run from
-1000 to +1000, clustering on -50 (59 sites), +25 (30), +50 (24), -25 (20) and +75 (20).

The 47 character templates are the part worth knowing: **named innocents carry a karma
penalty for killing them** — the Barmaid, the Blacksmith, the Fish Monger, Guard Pablo,
Cervantes, Brother Michel, Esclarmonde, Quinn the Herbalist. Murdering your way through
Barcelona already costs you something.

And it pays off at the end. `08 Final Encounter.zax` writes karma 15 times and tests
`Karma moreequal 600` and `Karma moreequal 650` through canned expressions, with relays
named `Test Relay BAD Karma` and `Test Relay GOOD Karma`. **Karma selects your ending.**

So the gap is not the system, it is the commentary. Of the 78 threshold gates in the
library, only **seven distinct thresholds are ever tested, at 17 sites**, and only **four
of those are dialogue replies**. The game tracks your morality meticulously, decides your
ending with it, and no character ever remarks on it along the way.

> Earlier drafts of this document said nothing wrote Karma. That was wrong: the scan
> looked only for the read side, `Character Attribute=`, and missed the write side,
> `Derived character attribute to modify=`. Recorded because it inverted the conclusion —
> karma went from "a dead system to revive" to "a live system nobody talks about".

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

1. **Make karma audible.** The tracking, the penalties and the ending selector all work
   already; 71 of the 78 thresholds are simply never tested. Two or three karma-gated
   replies per major NPC is authoring only, needs no new mechanism, and is the axis players
   most expect to matter. Nothing blocks it.
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

## Cross-cutting: the evil path and the goblin faction

The game's most developed evil content is the pro-goblin thread in the Wilderness, and it
feeds nothing — no faction, no rank, no karma, no reaction. Making it a real minor faction
on the model of the Order of Saladin is mostly assembly, because the parts are already
written.

### What makes Saladin a real faction

The entire mechanism lives in the `.Faction` file. `Saladin Aswaran`, in substance:

```
CCharacterFaction
  PlugIn Behavior = CPlugInBehaviorModifyCharacterWhenSelected
    Modification is permanent = 1
    +10 Skills/Fighting/OneHandedMelee
    +10 Skills/Fighting/TwoHandedMelee
    +1  Character Attributes/(EN) Endurance
    +20 Derived Character Attributes/CarryWeight
    +1  Derived Character Attributes/Uber Perks/Saladin Rank
  Display Name = Aswaran
  Description  = "The enclave of Knights in this area has been impressed with your
                  service to the goals of Saladin..."
```

A faction is **three small files**, one per rank, each granting concrete benefits *and
incrementing its own rank counter*. `CAssignFactionToCharacterAction` at the joining moment
is the only script needed; the rank follows from the record, and the rank is what
`Saladin IS` and `Saladin Highlevel` read. That is the whole template, and it is
authorable.

### What the goblins already have

**16 dialogues, 282 nodes.** GoblinVillager 55, Grumdjum 42 (33 of them gated — the most
reactive NPC in the set), GoblinKhan 41, Rakeb 30, Goblin Sapper 26, plus the cut
GoblinGirl 19 and GoblinGuards 4.

**Eleven quests in a near-symmetric structure.** Each goblin leader already has both a
serve-them and a kill-them quest:

| Leader | Serve them | Kill them |
|---|---|---|
| Plumdjum Khan | Slay the Bounty Hunter for the Khan | Slay the Goblin Khan (Torquemada), Rid the Dryad's Forest |
| Rakeb the shaman | Collect the Woodcutter's Eyes | Collect the Bounty of the Goblin Shaman Rakeb (Raylark) |
| Hrubjub | Spy for Hrubjub the Goblin | *(none)* |
| Raylark, for the other side | Slay Goblins for the Savage Heart, Rakeb's bounty | Kill him for the Khan |

**Both capstone titles are already written.** `Goblin Champion` — *"TITLE PERK: You have
slain Raylark and Fenclaw and recovered the Everlasting"* — and `Goblin Slayer` — *"You
have slain a great number of goblins."* One per side, each already awarded by its own
thread. There is also a `Goblin Kill Counter` attribute and a
`Raylark Have killed 10 goblins` gate.

### What is actually missing

**Nothing locks anything out.** Checking every `CSetQuestSatusToFailed*` against those
eleven quests finds **zero links**. You can be hired by Plumdjum to kill Raylark while
being hired by Raylark to collect bounties on Plumdjum's shaman, and neither side remarks
on it. The threads do not conflict; they fail to notice each other. The action is used 239
times elsewhere in the game, so this is wiring, not invention.

**No faction records**, so no ranks, no benefits, no allegiance gate. A `Goblin IS`
requirement does exist under `Monster Races` with zero uses, but it tests the player's
*race*, not their loyalty — it is not the gate this needs.

**The village is under-populated** — GoblinGirl and GoblinGuards are cut, which is already
phase 2 work and lands here.

**The dialogue does not know what you did.** 282 nodes, and the villagers greet a goblin
champion and a goblin butcher identically.

### The way in already exists, and nobody finds it

Hrubjub is the goblin scaling the wall west of Barcelona's gate — the `Goblin Sapper`
dialogue, whose tree name is `Hrubjub`, filed under Gate District. Reporting him to the
guard looks like the only option. It is not: you can join him, and the branch is well
written.

The route in is a **single reply**. Ask *"Did you kill this town guard?"*, then answer:

> *"I admire your handiwork. I am no friend to these city guards."*

That is the only in-link to `100 bad karma`. The node's other three replies all report him,
threaten him, or leave. From there:

> **`100 bad karma`** — *"Oh, how delicious, your heart sounds black and vicious. Perhaps
> you could perform a goblin favor and complete a task of stealthy flavor?"*
>
> **`100 completed quest`** — *"You completed that task with practiced ease, and brought
> news that will make **the Great Khan** pleased. Next time we return, Nueva Barcelona will
> be burned."*

**It already feeds karma**, at three points: -25 for admiring the murder, -50 for reporting
the gate's defences, -50 on completion. This is one of the most thoroughly wired evil
branches in the game, and it flows straight to the ending selector.

Three gaps, in cost order:

1. **Discoverability.** The whole path hangs off one reply, behind a question about a
   corpse. Answer *"This doesn't concern me"* and you never learn the option existed. A
   second entry — a Speech- or karma-gated line on `1 Start Conversation`, or an option on
   `60 used speech` after talking him down — costs one reply and is the single highest-value
   change to the goblin thread.
2. **No onward pointer.** Hrubjub says the Khan will be pleased, and the thread stops. You
   can betray Barcelona to the Horde and then arrive at Goblin Warrens as a stranger. He is
   a spy with every reason to tell a useful human where to report, so `100 completed quest`
   should name the village and the Khan. **This is what makes `Spy for Hrubjub` rung one of
   the ladder below rather than a dead-ended errand** — step 2 currently assumes it leads
   somewhere and it does not.
3. **Two dead links, in this conversation.** `20 ate a poet` and `30 goblin name` both
   target `5 goobye`, the typo for `5 goodbye`. That is the Goblin Sapper case already on
   the phase 1 list — two replies, not one.

The staging is better than it looks: Hrubjub is at the wall, and both Barcelona goblin
dialogues are Gate District files. The connective tissue between the city and the Warrens
is placed. Nothing runs through it.

### The Crossroads: the second rung, and the first real cost

Sir Esteban, guardsman of the Crossroads, sends you to clear out the goblin patrol. The
patrol has no way to make you the opposite offer — and it should, because almost everything
needed is already placed.

**The goblins there already talk.** `Crossroads.zax` fires `CDisplayDialogBalloonAction`
against `GoblinVillager` nodes through a scripted encounter — entities named
`goblin encounter` (force-generate and patrol), `goblin confrontation`, `goblin attack
banter`, `goblin second mark`. Two of those balloons come from a named speaker,
**`Goblin Patrol Leader`**:

> `500 goblin confrontation` — *"So, you seek to eliminate the goblin scourge? But it will
> be you that will be purged!"*

That node **already reacts to your allegiance** — it is a response to having taken
Esteban's contract. It is the natural branch point.

**And they are the Khan's, not vermin.** `500 wilderness banter 4`: *"I do hope **the Khan**
allows us to attack this day. I am famished."* The same Khan Hrubjub reports to. A player
who spied on Barcelona for the Horde is notionally already on their side, and the patrol
treats them as meat.

**The parley machinery exists too.** `GoblinVillager` carries
`20 used speech to avoid digestion / conflict / battle`, plus race-specific greetings for
Feralkin, Demokin and Sylvant. Talking a goblin patrol down is a shipped pattern.

**The addition:** gate a second variant of `500 goblin confrontation` on goblin standing.
Instead of promising to purge you, the Patrol Leader recognises the human who carried word
to the Khan and offers the counter-contract — **kill Esteban**.

**Why this one matters more than the rest of the ladder:** it is the first goblin choice
with a price. `LordJavier` checks `prior completion of estebans tasks` three times, so
Esteban's tasks feed the Knights Templar initiation. Killing him closes a Templar rung.
That is real cross-faction exclusivity, which is exactly what the goblin thread lacks — and
unlike the quest-fails-quest wiring in step 3 below, the player can *see* what it costs.

Esteban is already written as someone you can fall out with: `Crossroads.zax` holds
`piss off esteban`, `Esteban Sends you to jail`, `Esteban mad cam` and
`Esteban balloon after sending you to jail`. He is not a fixed friendly, so turning on him
does not fight the characterisation.

### The build

1. **Three `Goblin` rank records modelled on Saladin's**, with goblin-flavoured benefits —
   Sneak, poison resistance, carry weight. Three files, following a shipped pattern exactly.
2. **Use the existing quests as the initiation ladder.** Spy for Hrubjub to rank 1; the
   Crossroads patrol's contract on Esteban to rank 2; Slay the Bounty Hunter to rank 3;
   deliver the Everlasting to the capstone, where `Goblin Champion` already sits. Only the
   Esteban contract is new, and it needs one gated node variant. Rung one needs the onward
   pointer above, or the ladder starts with a step into nothing.
3. **Add the exclusivity.** Torquemada's contract fails the Khan's and the reverse. This is
   the change that turns a checklist into a choice, and it is the smallest of the three.
4. **Gate the 282 existing nodes on rank.** Free reactivity against gates that already work.
5. **Feed karma.** Harvesting a man's eyes and liver for a goblin shaman is the darkest
   thing in the game and currently moves nothing — while killing the Barmaid does. Adding
   the modifier is one action per choice, and it flows straight through to the ending
   selector.

Steps 1 to 3 make it a faction without writing a single new quest, which is what makes this
worth doing early. Step 4 is where new writing goes, and it lands on dialogue that already
exists. Step 5 is now unblocked: karma is a live system, not a dead one.

### The unfinished evil quests

Six of the game's 21 unofferable quests are the evil path's missing content —
`FIND THE RELICS FOR THE DARK WIELDERS`, `Convince DaVinci to Join the Dark Wielders`,
`Find the Yellow Node within the Sewers`, `Investigate Quinn the Herbalist for suspicion of
heresy`, and the `Rob the Thief Guildhouse` / `Convince the Thief Guildmistress to leave
the Sewers` pair. Two more, `Root out the heretic Cathars` and `Prevent the Inquisitor from
killing the Cathars`, are already activated by `02 Hamlet Burned` and display nothing.
Full inventory and how it was established: [`cut-content.md`](cut-content.md#quests).

The Cathar pair is the most valuable: a massacre-or-save choice, hooks already placed, in
the aftermath map of the one late act that still works.

### Do not restore "Convince DaVinci to Join the Dark Wielders"

The quest exists with **zero states**, mirroring `Convince Quinn the Herbalist to Join the
Dark Wielders`, which shipped with three including a refuse-and-kill branch. It is tempting
to finish it symmetrically. Don't — the finale already disagrees.

DaVinci is a real participant in the last fight: `08 Final Encounter.zax` names him 235
times, against Galileo's 224, and he has his own `DaVinci Ending` tree. **That tree already
contains his evil-path lines:**

> `17 DaVinci Talk Evil1` — *"I have misjudged you, young one. The divine promise within
> you has turned sickly and putrid and has made you more evil than I could have ever
> forseen."*
>
> `18 DaVinci Talk Evil2` — *"You may have become one with the Darkness... It is likely
> that I cannot defeat you, but we shall fight to the last against your evil scourge."*

On an evil playthrough DaVinci **denounces you and fights**. A quest that recruits him to
Relican contradicts the ending the game ships. That is very likely why it was cut with no
states while Quinn's shipped intact: Quinn is expendable and has a `Herbalist Dead` flag to
prove it, whereas DaVinci is load-bearing and is explicitly made invulnerable in
`DaVinci Workshop interior.zax` and `01 Hamlet Exterior.zax` by a
`RESET MAP for Invulnerable DaVinci` relay. The developers blocked the kill on purpose.

His *death* is nonetheless an accounted-for outcome — `GoodEndingDavinciDies`,
`GoodEndingOldManEscapesDaVinciDies`, a `20 DaVinci dies` node in the Galileo ending, and
`30 Good Ending Old Man Escapes DaVinci or Galileo Dies` in each of the three spirit
endings — but those read as him falling *in the final battle*, not being murdered in act 1.

Two ways to use the stub without fighting the finale:

1. **Reframe it as theft rather than recruitment.** Relican wants DaVinci's research or a
   relic, not his allegiance. It fits the Dark Wielder ladder, leaves the ending intact, and
   makes his evil-ending denunciation land harder for having been robbed by you.
2. **If the kill is wanted**, it needs a `DaVinci Dead` flag on the `Herbalist Dead`
   pattern, the invulnerability relay lifted, and the finale gated so he does not reappear.
   Feasible, but that is endgame surgery for one quest.

Option 1 is the recommendation.

One loose thread to resolve while in here: `Goblin Champion` requires slaying **Raylark and
Fenclaw**, but only Raylark appears in the quest text. Fenclaw has his own 18-node dialogue
with cooperative and tolerant branches, so the second bounty hunter looks like a step that
was written and only partly wired into the quest.

And a warning for whoever restores the Goblin Girl: her dialogue holds two of vanilla's 21
`no way out` nodes, `220 Liver` and `225 Liver pie`. They want fixing as part of placing
her, not afterwards.

## Suggested order

1. **Link repair, Barcelona and Montaillou first** — 68 of 84, ships standalone, needs no
   new writing.
2. **Cut content into its right home** — Goblin Girl into Goblin Warrens, the Titan quest
   into Titan Village, Guard Pablo into Temple District, Isabella's recruit wiring. All go
   where the section already works, so a mistake is visible immediately.
3. **The goblin faction** — three rank records, the existing quests wired as a ladder, and
   the exclusivity that makes it a choice. No new quests, and it gives the Goblin Girl
   somewhere to belong, so it follows straight on from step 2.
4. **The Knights of Saladin** — one faction assignment lights up 23 written replies across
   five acts; restoring two of Amir's nodes returns the Sacred Scimitar questline; and
   splitting the scimitar's reward by route follows the Dervish/Scholar pattern the act
   already ships. Small, self-contained, all in act 1, and the best first content job in
   the project.
5. **Give act 1's choices reach** — gate replies in later acts on `Thief Friend` and
   `Beggar Friend`, which are awarded today and read by nobody. One requirement file and one
   reply per acknowledgement, and it is the cheapest long-range reactivity available.
6. **The silent maps** — one balloon each, 17 maps, no new NPCs.
7. **A map variant as the first new area** — copy a cleared section of the Crypt or Shrine
   and repopulate it with survivors. Cheapest way to break the back half's pacing, and it
   inherits the original's navigation polygons.
8. **Inner Sanctum and Druid Council Level1** — the two rooms most obviously built for a
   scene that was never written. Small, self-contained, high value.
9. **Companion presets and levelling** — a handful of numbers and a reused action, and it
   fixes the loudest complaint after the content collapse itself.
10. **Karma and the faction-killer perks** — pure writing against gates that already exist,
    and it can ride along with any of the above rather than being a phase of its own. Karma
    already tracks and already picks the ending; only the mid-game commentary is missing.
11. **The Crypt's quests** — the act's real problem, and the largest single job here.
12. **The built undercroft** — a new interior assembled from the Sewers kit, with the
    Outpost as the parts index and the shipped Sewers maps as the reference for using it.
    Last of the content work because it is the only item that builds a map from nothing.
13. **Thinning** — last, and only after the acts have more to do. `Max Party Mojo` still
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
- ~~**What moves Karma?**~~ **Answered.** 213 write sites across 86 files, including 47
  character templates that penalise killing named innocents, and the finale tests
  `Karma moreequal 600` / `650` to pick the ending. The earlier "nothing writes it" reading
  came from scanning only `Character Attribute=` and missing
  `Derived character attribute to modify=`.
- **Why does Barcelona measure 16.8 spawnable entries per map here against the design
  doc's 8?** Every other section reconciles to within a few percent; this one does not, and
  it should be chased before any Barcelona thinning (though none is planned).
