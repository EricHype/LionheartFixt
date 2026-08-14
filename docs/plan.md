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

**The plan for the act — keep it a combat act.** The instinct to convert Montserrat into a
settlement is wrong: it works as a fight. What it lacks is any way for a build other than a
combat build to *change* that fight. "Druid Council Level1" is still a room built for a
scene never written, and a druid or two to talk to would help, but the larger opportunity
is below.

### Montserrat: making a combat act read your build

**What actually fights you here:**

| Map | Enemy | Generators |
|---|---|---|
| 01 Grove Exterior | **Snakebreed**, incl. **Snakebreed Venom** ×3 tiers, plus 7 Vodyanoi | 113 |
| 02 Druid Council Level1 | Snakebreed, Venom and **Boss** tiers | 48 |
| 02 Druid Council Level2 | the same | 30 |
| 3 Animal Den | **Bears** — Bear, Tough, Super, and nothing else | 9 |
| 4 Animal Cave | **Wasps**, incl. Tainted variants | 24 |

Venomous snake-people, bears and wasps. **It is a poison-and-beasts act**, and two shipped
perks name those things exactly:

- **`Snake Eater`** — *"a slight immunity to poison, adding 30% to your Poison Resistance"*
  — against three maps of Snakebreed Venom. Today it is a passive number and nothing more.
- **`Wolf Trapper`** — *"You are able to strip a **wolf or bear** of the..."* — and
  `3 Animal Den` is nine bear generators, 78 entities, zero conversations. The perk names
  the map's entire contents.

Others that fit the ground: `Earthen Contact` (attunement to nature, in a druid grove),
`Superior Senses` (+1 Perception, "tribal ancestors"), `Observant` ("notice when things are
out of place"), `Ghost` and `Master Thief` (Sneak and Find Traps).

**What the act gives you to work with, and what it does not:**

| | Grove | Council L1 | Council L2 | Den | Cave |
|---|---|---|---|---|---|
| `CFreeRangePoly` zones | 104 | 71 | 90 | 3 | 3 |
| Doors | 2 | 1 | 4 | 0 | 0 |
| **Locked doors** | 0 | 0 | **1** | 0 | 0 |
| Secret doors, `Door` tree uses | 0 | 0 | 0 | 0 | 0 |

265 interaction zones already placed across the three main maps, **one locked door in the
whole act**, and the shared `Door` tree — the game's vehicle for lockpicking, trap disarming
and revealing false walls — used **zero times**.

**And the act has one NPC of its own.** `Brother Montgomerie`, 11 nodes. Everything else
that speaks in Montserrat is a companion you brought with you: `cortes`, `Cervantes`,
`Inquisitor Darsh` in the Grove.

### What to add, in cost order

1. **A locked flank into Druid Council Level 1.** Eighteen Lockpick gates exist and are
   used zero times game-wide; the act has one locked door. A side entrance that avoids the
   frontal approach turns the silent 48-generator map into a build check. **No NPC needed,
   which is the whole point in a corridor.**
2. **Sneak past the Grove patrols.** Four Sneak gates built, zero used, against 104 zones
   already placed. `202 sneaking into titan pen` in the `Door` tree is the shipped model —
   *"if you're caught in here the titans will be very displeased."*
3. **Make `Snake Eater` visible.** A venom pool, a poisoned passage, or a Snakebreed nest
   that does not rouse for someone who reeks of it. The act is built of the exact enemy the
   perk answers.
4. **Give `3 Animal Den` a reason — and bring the bear.** See below; this is the act's best
   small set piece and the map with the most room for improvement, because it currently has
   none at all.
5. **Perception and Outwit on the ambushes.** Thirteen derived gates, zero uses. Spot the
   Grove ambush before it triggers.
6. **One druid who can be talked down**, on the `GoblinVillager` pattern — the act's
   enemies currently have no voice at all, so this is the only item here that needs writing.

Items 1, 2 and 5 need no new art, no NPC and no map. They are requirement files and trigger
zones against geometry that is already placed — which is why this approach works in acts
where a town would not.

### The bear cub and the Animal Den

**`3 Animal Den` is the emptiest map in the game.** Four named entities — the two Grove
transitions, `Start Here`, and `AMBIENT Cave SFX` — **zero loot generators and zero items**,
against nine bear generators. You walk in, fight bears, and leave with nothing at all.

**And you can already be travelling with a bear.** `Bear Companion.DialogTree` is placed at
the Crossroads: *"&lt;The bear looks at you affectionately&gt;"*, with *"Encourage the bear to
rejoin you"* and a `20 Whine` node — *"&lt;The bear whines with disappointment&gt;"* — for turning
it down. It is a small one: the companion runs on `Weak Crossroads Bear` at **27 HP**,
against the den's Bear 39, Tough 46 and Super 53. It cannot win that fight.

Which is the point. **Arriving at a bear den with a bear should not be a fight.** The
obvious reading is the one the numbers suggest: it is a cub, and this is where it came
from. Bring it home and the den is not hostile; the reward is whatever the den should have
held all along, and it costs the player their companion — a real trade, not a bonus.

Everything needed is shipped:

| Piece | Mechanism | Precedent |
|---|---|---|
| Detect the bear is with you | `CCheckExistenceAction` on the companion | `Name To Check For=Cervantes` ×18, `Cortes with arm` ×10, `player is close enough to see bear` ×8 |
| Stop the den attacking | `CRemoveCategoryAction` / `CSetTargetTypeAction` | 922 uses between them |
| Say something on entry | `CDisplayDialogBalloonAction` | 1974 uses |
| Put something worth finding there | an inventory generator | the map currently has none |

**This also partly answers an open question.** The plan asks whether a script can tell if a
companion is present; Cervantes and Cortes are existence-checked 28 times between them, so
the answer is yes for a named companion. What remains untested is whether the check
distinguishes *following* from merely *alive*.

Note the shape it shares with the lava trolls, at a fraction of the size: a hostile
population, a peaceful route that needs something brought to it, and a reward the violent
route does not give. If the troll faction is the large version of that idea, the bear den is
the version that could be built in an afternoon — and it improves a map that presently has
nothing in it whatsoever.

#### The reward, and the bears returning

Giving up a companion deserves more than a chest, and the game supplies both halves.

**Immediate:** the den should hold something, since it holds nothing today, plus an
event-given perk on the `!NPC or Event Given Perks` model — the folder where
`Brambles Patience`, `Weng Choi Perk` and `Stargazer` already live, each a small permanent
boon granted by a one-off act of kindness or mastery. A nature boon fits the company
exactly.

**Scale it by race, and give the Feralkin the most.** They are, by the game's own
definition, *"the descendants of humans imbued with **the magic of a beast or a bestial
spirit**"* — a bear den is their inheritance, not a curiosity.

The contrast is already written, and it is the reason this lands. Barcelona is wary of
Feralkin everywhere: **71 distinct Feralkin-specific nodes** across the game, nearly all
suspicion. The Blacksmith greets one with *"Ah… a long way from the forests, aren't you, my
big friend?"*, and node `48 Angry Feralkin` exists so the player can say *"is it because of
my nature that you think I would agree to roam the sewers…"*. The Gate Guards, the Grumpy
Port Guard, GuardTomas, `inquistorcanned` and the bickering couple all carry Feralkin
variants of the same wariness.

So a Feralkin is a beast-blooded outsider whom every human in Barcelona eyes sideways —
and the bears simply take them in. That is the whole reward, and the tiering writes itself:

| Player | Reception | Gate |
|---|---|---|
| **Feralkin** | recognised as kin; the fullest boon | `Feralkin IS` — 17 uses, well proven |
| **Sylvant** | nature-touched, accepted | `Sylvant IS` — 10 uses |
| Human, Imbued | tolerated; the baseline reward | — |
| Demokin | uneasy; the beasts keep their distance | `Demokin IS` — 11 uses |

**And a gate for the middle tier already exists, unused:**
`Tainted race - feralkin or sylvant`, built and referenced **zero times** — exactly the
"nature-touched" bracket this needs. Its sibling `NOT Feralkin or Sylvant` is also built
and unused.

The mechanism is the shipped one: race-gated node variants, as in `GoblinVillager`'s
`1 Greeting N Feralkin` / `N Sylvant` / `N Demokin`, or the Blacksmith's three race-specific
introductions.

**Later, and this is the better reward: the bears come back.** The mechanism is ordinary —
a dormant group placed in advance, woken with `CActivateAction` and set friendly through
`CSetTargetTypeAction` or a category change, gated on the flag set in the den. The Crossroads
already stages an encounter this way with `CForceGenerateAction` and `CSetPatrolAIAction`.

**And Montaillou is where they should arrive, because the Cathars are bears.**

> `Cathar Warden` — *"I saw you as a bear, and then magically change into your current
> form."*
> *"Like the rest of my clan, I am a **lycanthrope** and must take the form of the bear for
> half of the day. It is a secret our..."*

`Cathar Bearform` is placed **9 times in `01 Hamlet Exterior` and 34 times in
`02 Hamlet Burned`** — `Team Number=Nutral`, `Category=Enemy`. A player who returned a cub
to its den in act 2 arriving in act 3 among a bear-clan being hunted by the Inquisition is a
connection the shipped content makes on its own; it only needs to be noticed.

That also lands on the strongest unclaimed pair in the game: `Root out the heretic Cathars`
and `Prevent the Inquisitor from killing the Cathars`, both empty, both already activated by
`02 Hamlet Burned`. Mercy shown to bears earning standing with bear-people is exactly the
kind of thread that makes a massacre-or-save choice weigh something.

One complication worth keeping rather than smoothing away: **not every bear is a friend.**
`ToulouseIapetus` warns that *"The creature is no mere bear, as we at first thought. It is,
I fear, a Daeva... We have seen it take the forms of a bear, an ogre, a bird."* A player who
has learned that bears are allies meeting a Daeva wearing one is the natural sting, and the
line is already written.

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
alone has 102 conversations and 1006 reachable nodes. Three jobs here — the cut
`Help Andre the Titan with his tasks` quest belongs in Titan Village (61 conversations, 44
spawns, already the right shape); the act holds 20 broken links in 5 files; and it is where
the Montserrat bear thread should pay off, because the Cathars are bear-lycanthropes and
`Cathar Bearform` is placed 43 times across two of its maps.

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

## The Sewers' third and fourth parties — lava trolls and wererats

The act 1 section covers the Thieves and Beggars. Beneath them are two more peoples who
speak, who hate each other, and whom the player cannot side with at all. Both sides of the
feud are written; one of them was never placed.

### They are peoples, not monster nests

**The lava trolls speak.** `Warning Troll.DialogTree` is placed twice in `05 Troll Pit`:

> `01 Greeting` — *"You! Stop! No welcome."*
> — *"I come in peace. Eduardo said I should speak to you about Red Ore."*
>
> `20 no trust` — *"We no trust Eduardo no more. We no trust no one. **Too many dead
> Trolls. Wererats sneaky.** Leave or face problem."*

A trade relationship, a grievance, and a named enemy — in two nodes.

**The wererats answer, and their half is cut.** `wereratwarriorcan.DialogTree` (4 nodes,
"Wererats Helpful Canned") and its `Helpful wererat.can` template are referenced by
**nothing**:

> *"Since you are a **friend of beasts**, I'll give you some advice. Never trust a thief
> and **beware of the lava trolls**."*
> `30 trolls` — *"The lava trolls are in the lower levels of the sewers. I suggest you
> avoid them."*

Each side warns you about the other. Note the greeting condition — *friend of beasts* —
which is the game already reaching for a standing check it never got.

### Three parties want them dead or used, and none of it resolves

| Who | Wants | Status |
|---|---|---|
| Enrique the beggar leader | the trolls exterminated — `Destroy the Lava Troll Menace`, a sub-quest of `Help the Beggars against the Thieves Guild` | works |
| Inquisitor Raphael | the wererats exterminated — `Deal with the Afflicted in the Sewers` | works |
| Eduardo, DaVinci and Cortes | the trolls' **Red Ore**, for the mechanical arm | see below |
| The trolls | to be left alone, and something done about the wererats | no way to say so |

`Warning Troll` has **no success branch**. Every path from `20 no trust` is "I must pass" or
leave. And the Red Ore quest states *"Eduardo told you to go to the sewers below Barcelona
and obtain Red Ore directly from the lava trolls"* — but every
`Inventory Item To Give=...Red Ore` site is in `Blacksmith map.zax`. **The trolls grant
none.** The game sends you to trade with them and makes the trade impossible.

Even the merciful wererat path kills their leader: the beggars' cure quest requires slaying
the Prime Wererat for a patch of fur.

### And a cut item with an obvious home

**`Lava Troll Hide`** has a quest-item definition, an inventory icon and a world pickup
model — and exactly one file in the archive mentions it: its own definition. Nothing grants
it, nothing wants it. `Wolf Trapper` already establishes hide-stripping as a mechanic.

### One voice is not a faction

The trolls have **one dialogue file and three nodes**. The goblins, who feel like a people,
have twelve files and roughly 198 nodes:

| | Files | Nodes |
|---|---|---|
| Goblin village | 12 — Villager, Khan, Rakeb, Shaman, EntranceGuard, Crier, Lt, VendorHub, Guards, Girl, Hut Ritual Sayings, guarding Woodcutter daughter | ~198 |
| Lava trolls | 1 — `Warning Troll` | 3 |

**The technique that makes the difference is cheap.** `GoblinVillager` is a single tree
opened **52 times** in Goblin Warrens, across fifteen lettered entry nodes —
`1 Greeting A` through `1 Greeting M`, plus `N Feralkin`, `N Sylvant` and `N Demokin` — each
on a different `$trigger`. Fifteen goblins with their own opening line, from one file. The
Khan and Rakeb get their own trees on top, because they are characters rather than
population.

So the trolls want the same shape, at minor-faction scale:

1. **A `LavaTrollVillager` tree** on the `GoblinVillager` model: lettered greetings for the
   rank and file, race-specific variants, and state-gated ones for before and after the
   alliance. One file, several placements, many voices.
2. **A chief with his own tree**, the Khan's counterpart — the face you negotiate the trade
   with. *(This reverses an earlier recommendation in this section's review to cut the
   chief on scope grounds. That was right about the ransom mechanics and wrong about the
   cast: a faction needs someone to be its face, and the Khan is why the goblins have one.)*
3. **Keep `Warning Troll` as the gatekeeper**, the `GoblinEntranceGuard` equivalent. It is
   already placed and already `Team Number=Nutral`.

Three files rather than twelve, and only one of them large.

**The voice is already set, and it is not the goblins'.** The trolls speak in broken,
plural, blunt sentences — *"You! Stop! No welcome."*, *"We no trust Eduardo no more."*,
*"Too many dead Trolls. Wererats sneaky."* Hrubjub and his kin rhyme; the trolls do not.
Two registers, both established in shipped text, and the troll one is cheap to write more
of.

Worth placing a mourner among them, because the map supplies the reason: a
`Fixed Dead Body Generator` in the pit spawns a **`Lava Troll Boss` corpse**. Somebody down
there lost a chief.

### The build — a minor faction, kept minor

Same tier as the goblins and the guilds: standing, reactivity and at most a couple of small
quests, not an initiation ladder.

1. **Place the cut wererat.** `Helpful wererat.can` and `wereratwarriorcan` exist and go
   nowhere. Placing them is restoration and it gives the wererats a voice to set against
   the trolls'. This belongs with the phase 2 cut-content work.
2. **Give `Warning Troll` a success branch.** Speech, or evidence you have moved against the
   wererats. Without it the trolls cannot be sided with at all, and the Red Ore promise
   stays unkeepable.
3. **Make the Red Ore come from the trolls**, as its own quest text says. That turns the
   trade into the reward for the peaceful branch and gives the faction an economic reason
   to exist — DaVinci and Cortes' arm depend on it.
4. **Give the hide to the violent branch.** Kill them and take hides; deal with them and get
   ore. One `InventoryAddition`-scale change that makes the choice symmetric rather than
   punitive, and it retires a cut item.
5. **Gate on standing, both ways.** Enrique's extermination contract should close the trade,
   and Raphael's should open the trolls. The wererats' *friend of beasts* greeting is the
   hook already written for the other direction.

### Tomas, and why the trolls took him

The lost boy in the Troll Pit is the hinge for all of this, because rescuing him is the one
reason a player *must* go down there.

**The rescue already works peacefully.** Nothing about Tomas is gated on killing trolls. His
opening line — *"Did you kill all of those things out there?"* — accepts either answer, the
quest completion and XP fire from `50 Fine` and `60 No thanks` with no troll condition, and
he leaves under his own power: *"No thanks. I can get out of here on my own. You would just
slow me down."* The only `Kill all Lava Trolls` strings in the map are comments on `warp`
entities carrying `CPainAction` — lava damage, not quest gates. The genuine
kill-them-all requirement belongs to the Beggar Captain, for Enrique's separate contract.

So the fighting is only about *reaching* him. An alliance makes the whole errand peaceful,
which is exactly the kind of thing that should be possible and currently is not.

**He is not a lost child.** *"I come down here all the time with the beggars. I know my way
around."* He is a beggar boy who works the sewers, and the pit is full of caches —
`Hidden Treasure`, `secret area treasure`, `secret area2 chest`, two secret doors, and a
**`red ore chest`**.

**The reading that costs one invented fact: he was caught stealing Red Ore.** Everything
else is already written, and this single addition ties three threads together:

- It explains the capture without making the trolls monsters. A people who have lost members
  and been cheated by their trade partner catch a human child in their ore store and shut
  him in rather than kill him.
- **It explains why the Eduardo trade broke.** *"We no trust Eduardo no more."* The ore keeps
  reaching Barcelona without payment, and Tomas is the evidence — he comes down here "all
  the time with the beggars", and Enrique is the man paying to have the trolls exterminated.
- It makes Tomas's own line better. *"I was looking forward to getting revenge on them for
  throwing me in this room to die"* becomes a caught thief's account rather than testimony.
  An unreliable narrator is better writing than a victim, and it is already in the shipped
  text.

The grievance is even visible on the map: one `Fixed Dead Body Generator` in the pit spawns
a **`Lava Troll Boss` corpse**. There is a dead chief lying down there.

**Getting him out is its own quest.** It must stand alone, and specifically **must not be
the wererat contract**: a player who only wants the boy should not be conscripted into a war
with the Afflicted to get him. That allegiance is a separate choice and folding it in would
collapse two decisions into one.

**But it is not a ransom, and the shipped content is why.** Two findings rule that framing
out:

- **There is no cell to open.** Tomas sits behind `secret door1`, whose
  `Relay Name=Save Tomas relay` fires a `CBeginNonInteractiveSequenceAction` when *the
  player* opens it. `Tomas Generator` and `Tomas Fog pusher` are both `Active=0` until then.
  He is hidden, not held, and the discovery is the mechanic.
- **He refuses escort.** *"No thanks. I can get out of here on my own. You would just slow
  me down."* Then `CDeleteAction` and `COtherMapAction` — he walks out unaided.

So the quest is about **settling his debt and buying passage**, not unlocking a door. The
theft stays as backstory: it is why the gatekeeper distrusts you and what the price is for.

And **the price cannot be the ore.** There is exactly one Red Ore in the game, it sits in
the `red ore chest`, and the Blacksmith's dialogue consumes it — seven
`Inventory Item To remove=Red Ore` sites. Spend it here and Cortes' mechanical arm becomes
impossible. So:

| Route | Mechanism | Precedent |
|---|---|---|
| Pay what the boy took | gold, at a price the chief names | Eduardo's `Barter 25 and 100 gold` node |
| Barter or talk him down | Barter/Speech gate | Eduardo's test of valour offers six such outs |
| Hand back something else he lifted | one of the pit's cache items | `CActionCheckForInventoryItem`, 653 uses |

All three are about the immediate theft, and all three are settleable on the spot. The
*larger* grievance — that Barcelona has been taking their ore for years without paying — is
deliberately left standing, because that is the first faction quest below. Settling the
boy's debt buys a hearing, not a partnership.

**Sequence:** settle the debt, then the alliance, then the faction quests. Getting Tomas out
is what gets you listened to; the standing follows; the errands come after. A player who
takes the boy and walks away has still had the entire peaceful route without joining
anything or fighting anyone — which is the point.

And **Tomas still walks out on his own line.** That scene is better than anything a rescue
would replace it with, and keeping it costs nothing: the negotiation is with the trolls, not
with him.

**Who you negotiate with.** `Warning Troll` belongs to a dedicated speaker —
`Speaker=warning troll` — so a talking troll already exists and is placed, and it is
`Team Number=Nutral`, so it is approachable rather than hostile. The `Lava Troll Boss`
entries are *spawnable* entries inside generators, in three difficulty tiers, so there is
no chief character today; see the cast above for why one should be made anyway.

**And keep the sting.** Tomas wants the trolls dead. Free him by making peace and you return
a boy who resents the bargain, to a guild leader who is paying to exterminate them. Marisol
gets her brother back; Enrique gets an informant who now knows the way in. That is a real
cost for the peaceful route, and every piece of it is in the shipped text already.

### Two minor quests for the allied route only

Separate from the ransom, and available after it. Killing the trolls stays the simple
option: you get through, you loot the chest, you take hides. Allying gets you what violence
cannot — errands built from grievances the trolls already state and geography already
placed.

The two below are the core. Four more follow in the next subsection; the aim is not to
build all six but to have enough that the trolls can be given work in **different
registers** — diplomacy, ritual, trade, war — which is what stops a faction reading as a
quest dispenser.

**"Wererats sneaky."** Gated on the alliance *and* on having turned against the Afflicted,
so it stays a choice rather than a consequence of rescuing a child. The incursion is real
in the data, not just in the complaint:
`05 Troll Pit` contains wererat references and `04 Hall of Beggars` contains troll ones, so
the two peoples already overlap on each other's ground. The Troll Pit also holds
`secret area1`, `secret area2`, `secret door1`, `secret door2` and their `tophide`
counterparts — a ready-made answer to *how* the wererats keep getting in. Find the way
they come through, or clear the incursion. The map does the work; the quest is the reason
to look.

**"We no trust Eduardo no more."** The first faction quest, and the one that needs no
allegiance beyond the alliance itself. A broken trade, stated in the second line of their
only conversation, with a merchant the player already knows. Carry word between them and
the Red Ore becomes a trade rather than a theft — which is what the Red Ore quest's own
text says should happen. This one quietly repairs the chain described above, and it is the
larger version of the debt the ransom only settled for one boy.

The Troll Pit already holds a **`red ore chest`** entity, so today the ore is something you
fight through them for. That is exactly the asymmetry to preserve: kill them and the chest
is loot; ally and the ore is given, plus two errands and a supplier who stays alive for
DaVinci and Cortes.

Neither quest needs a new map, a new NPC or a new item. Both are one quest definition and a
handful of nodes on a conversation that has to be extended anyway for step 2.

### Four more, all from things already placed

Build two of these, not four. They are listed with their grounding so the choice can be
made on what the Sewers need rather than on what sounds good.

**The chief's spirit.** The pit holds **30 Spirit generators** (Spirit 2/3/4/5) and a
`Fixed Dead Body Generator` that spawns a **`Lava Troll Boss` corpse**. The trolls say *"Too
many dead Trolls."* Their chief is dead and unsettled — lay him to rest, or carry his spirit
where it needs to go. Spirits are a first-class Lionheart system, and the trolls themselves
drop spirit charges, so this reads as native rather than bolted on. Everything is already in
the map; the quest is the reason to notice it. **This is the one that gives the mourner NPC
a purpose.**

**Speak for us.** Trolls cannot walk into Barcelona. Enrique can, and he is paying to have
them exterminated. Argue their case: talk him down, or find something that makes the
beggars stand off. Existing NPC, existing contract, no new map or enemy — and it is a
**Speech and Barter quest rather than another clearance**, which the Sewers badly need
since nearly everything down there is a kill count. It also creates the tension worth
having: siding with the trolls sets you against the beggars, who are the other people you
might have been helping.

**The vodyanoi.** The most numerous creature in the Sewers by a wide margin — roughly 285
spawn entries across the maps in eight variants. Lava trolls are fire and stone, vodyanoi
are water; the antagonism writes itself and costs nothing to stage. Clear a flooded stretch,
or stop them fouling the trolls' workings. Pure reuse of enemies that already exist in bulk.

**The dead below.** `03 Unholy Oubliette` is 480 entities, 57 generators and **zero
conversations** — one of the 17 silent maps listed above. It is full of ghouls, with
skeletons, terrors and zombies through Dungeons 1-3. The trolls dig; the dead are through
the wall. Recover the trolls who went down and did not come back. **This lands a quest on a
map that currently has no dialogue at all**, so it clears an item from two lists at once.

**Thieves in the tunnels.** The cut helpful wererat says the thieves *"control the eastern
sewer corridors and hide within a maze of secret corridors. Their passageways are filled
with traps."* `09 Secret Quest` — a map named for content it does not contain — holds
thieves, guard dogs and 45 generators. The trolls want them out. This gives the trolls a
stake in the Juanita and Enrique war rather than leaving them outside it, and gives
`09 Secret Quest` something to be.

**Recommendation: the chief's spirit and Speak for us.** With the Eduardo trade and the
wererat incursion that makes four errands in four registers — ritual, diplomacy, trade,
war. The vodyanoi and the dead below are cheaper but both are clearances, and the Sewers
already have too many of those; keep them in reserve.

**Five new quests if the recommendation is taken**, and only one of them is required to see
the peaceful route: getting Tomas out. The Eduardo trade needs the alliance; the chief's
spirit and Speak for us need the alliance; the wererat incursion needs the alliance *and* a
side taken in a war the player may want no part of. Each gate is one step further in, and
none of them is a toll on the one before.

The result is a four-cornered Sewers — Thieves, Beggars, trolls, wererats — where the two
non-human parties are the ones nobody has been able to talk to.

**Total cost:** three dialogue files (a villager tree, a chief, and the existing gatekeeper
extended), a handful of placements, two item grants, five small quests, and the cut wererat
put back where it belongs. Against the goblins' twelve files that is still a small faction —
but it is a faction, which one talking troll is not.

Two remaining unknowns, neither blocking: `Blacksmith map.zax` contains two
`Inventory Item To Give=Red Ore` actions despite the quest text saying Eduardo has none, so
the ore's provenance is not fully traced; and nothing in the pit currently reacts to
Enrique's extermination contract, so "his contract closes the trade" is new wiring rather
than a repair.

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

The zero rows are the opportunity, and they are not only for conversations: Lockpick,
Sneak and the derived attributes are how a build expresses itself in a *fight*, not just in
a dialogue. Worked through for one act in
[Section 2 — Montserrat](#section-2--montserrat).

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
   into Titan Village, Guard Pablo into Temple District, Isabella's recruit wiring, and the
   helpful wererat into the Sewers. All go where the section already works, so a mistake is
   visible immediately.
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
  off rather than a blind test. Partly answered: a named companion *can* be existence-checked
  — Cervantes 18 times, Cortes 10 — but whether that distinguishes following from merely
  alive is untested.
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
