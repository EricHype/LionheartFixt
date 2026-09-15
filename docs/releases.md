# Lionheart Fixt - the mod, and its releases

Status: **0.1.0 through 0.9.4 are published**. 0.6.0 is played only as far as the Juan rescue; **0.7.0 and 0.8.0 are entirely unplayed**, and 0.7.0 changed a late-game promotion for every faction combination. 0.9.0 is scoped below and not started. 0.5.0 was built and never published; its artifact crashes on entering the vault and is superseded by 0.5.1. The sections below are in reverse release order, newest first.

The diagnosis lives in [`design.md`](design.md); the
map-by-map work lives in [`plan.md`](plan.md). This document
is the other half: what actually gets packaged, under what name, in what order, and what
"done" means for each release.

## The name, and what it commits us to

**Lionheart Fixt**, after Fallout Fixt - a single, cumulative, community-maintained mod
that repairs the shipped game, restores what was cut, and adds new content, in that order
of confidence. Taking the name means taking the discipline that came with it:

- **One mod, one install.** Not a suite of optional patches the player has to reason
  about. The whole thing installs and enables as one id.
- **Fix, then restore, then extend** - each release visible in all three registers, so a
  version is never "just the new stuff".
- **Vanilla-compatible saves are not promised.** Fixt never promised them either. New
  factions and new dialogue nodes will not retrofit onto a mid-game save cleanly.
- **The original writers' voice is the house style.** Goblins speak in rhyming couplets.
  Anything new that does not is wrong.

## Packaging

| Decision | Value | Why |
|---|---|---|
| Mod id | `lionheart-fixt` | One id, cumulative, matching the Fixt model |
| Display name | `Lionheart Fixt` | |
| First version | `0.1.0` | |
| Format | `mod_format_version: 1` | The shape `modmanager.py` already installs |
| `requires` | none | Fixt must stand alone |

**Versioning.** `0.MINOR.PATCH` until the whole-game reactivity pass is in. Each MINOR is
one themed release that ships alone and is playable alone; PATCH is repair to a shipped
MINOR. 1.0.0 is when every act, not just the front half, has been through a reactivity
pass.

**Conflicts with the existing mods in this repo.** The scratch mods are not part of Fixt
and will collide with it on shared files. Recorded now so it is not discovered during a
build:

| Mod | Shared file | Note |
|---|---|---|
| `marco-the-pickpocket` | `Levels/1 Barcelona/Gate District.zax` | Fixt 0.1.0 touches Hrubjub's dialogue but *not* the Gate District map - no collision expected, but this is the one to watch if placement becomes necessary |
| `test-pocket`, `outpost-expedition` | `Herbalist Dialogue.DialogTree`, `Test Pocket.zax` | No overlap with 0.1.0 |

Last-enabled wins on conflict, so Fixt should load **last** in `enabled.json` during
development.

## Release map

| Version | Theme | Why this order |
|---|---|---|
| **0.1.0** | **The Horde** - the goblin thread becomes a faction you can join, and the camp starts reading your build | The most complete unfinished thread in the game. Almost no new machinery, one new quest, and it is the only evil path with writing already in place |
| **0.1.1** | **The Crossroads patrol** (built) - disarm the spawn-hostility, add the counter-contract on Esteban, and let the Templar exclusivity bite | Finishes the goblin theme while its machinery is fresh. Kept out of 0.2.0 deliberately: it is new writing, and 0.2.0's value is that it has none |
| **0.1.2** | **Standing** (built) - the camp reacts to your rank, and standing accumulates across every service rather than being granted once | Completes the faction as a thing with texture, not just a gate |
| **0.1.4** | **What playtesting found** (built) - Esteban's death is recognised, the rank titles stop naming a deed you may not have done, and the Goblin Girl's dead replies are repaired | The first release made entirely of play reports. Cut as its own version because the fixes change behaviour players had already seen |
| 0.2.0 | Link repair, whole game | 84 true dead ends. Ships standalone, needs no new writing. Deliberately *not* first: 0.1.0 needs to demonstrate the thing Fixt is for |
| 0.3.0 | **The Knights of Saladin** (built) - the order awards the rank, not just the title | The second minor faction. Ordered ahead of Quinn deliberately: the core repair is one faction assignment with four acts of payoff, which is far cheaper than a three-quest chain |
| 0.4.0 | **Quinn's reagents** (built) - three quests, three healing potion tiers | The project's first new content. Most of the assets already existed |
| 0.5.0 | Cut content into its right home | Titan quest, Guard Pablo, Isabella, the helpful wererat |
| 0.6.0 | **The Port District** - Fernand Desoto becomes the game's fourth companion, because his brother can finally be saved | The companion is written and wired on both sides and reachable by nothing. It exercises the companion machinery on the cheapest case before Grace or the Crypt need it |
| 0.7.0+ | The back half - the Crypt's war, the two new areas, the England companion | The largest work, and it wants the faction and reactivity templates settled first |

## The Crossroads patrol, and why it is hostile

Found while testing 0.1.0-rc1: talking to Guard Esteban about the local dangers makes the
Crossroads goblins attack, with no quest accepted. This is vanilla, and the mechanism is
now fully traced.

`30 Dangers` -> `500 goblins` -> `500 goblin continued` fires `Relay Name=goblin encounter`
unconditionally, unless `Corner Goblins Dead` is already set. There is no quest gate
anywhere on that path.

**The relay itself is innocent.** `goblin encounter` is a `CRelayAI` whose six actions
force-generate the Corner Goblins, activate the Scout Generator, set a patrol route to
`Goblin patrols here`, and fade in the Patrol Leader and Scout. It contains **no combat
action at all**, and it is `Trigger Only Once=1`.

**The hostility is in the template, and the fix is in the generator.** The spawned entity
is `Monster Cans/Mongol Gate District`, which carries `Valid Targets=Player,Player Friend`
and `Category=Enemy,Goblin` -- it aggroes on sight, with no script needed.

The decisive detail is that **Goblin Warrens spawns the same kind of goblin from equally
hostile templates and its villagers are peaceful**. `Mongol Archer Village` and
`Mongol SwordsmanVillage` also ship as `Valid Targets=Player,Player Friend` /
`Category=Enemy,Goblin`. What makes them neutral is two actions in the generator's
`After Action`, run at spawn:

```
Action=CSetTargetTypeAction
{
    Entity Name=$Instigator
    Name To Target=
    Valid Targets=            <- clears targeting
}
Action=COldBad_S_e_t__C_a_t_e_g_o_r_y_Action
{
    Target Name=$Instigator
    New Category=Goblin       <- drops "Enemy"
}
```

`Corner Goblin Generator` at the Crossroads has no `After Action` at all. That single
omission is the whole difference between a patrol you can walk past and one that charges.

**So the fix is small and fully precedented**: add that two-action `After Action` to
`Corner Goblin Generator`, and let the existing `goblin confrontation` relay -- which
already does `CSetTargetTypeAction` + `CGoToCombatAction` on the Patrol Leader -- turn them
hostile when the scene calls for it. Do not edit the shared template; it is used elsewhere.

**It should not ship alone.** A neutral patrol with nothing to say is worse content than a
hostile one: it removes an encounter and replaces it with nothing. This lands with the
counter-contract, which is the thing that gives a peaceful patrol a purpose. It is
also why the counter-contract could never have worked as scoped -- a patrol that is
already charging cannot offer you a job.

**Both shipped in 0.1.1.** This was briefly recorded as 0.2.0, which was wrong twice over:
0.2.0 is defined as link repair that needs no new writing, and `plan.md` had originally
scoped the counter-contract inside the goblin faction ladder -- 0.1.0's own theme. It also
no longer has to be rung 2 of that ladder, since rank 2 now comes from the shaman's eyes
quest, so it is optional content that can be sequenced on its merits rather than forced
into a release it does not fit.

## 0.10.0 - Montserrat (scope)

**Built, unplayed, unpublished.** What follows is the scope as written; "What was built" at the end records where the build departed from it and why.

**Originally:** Planned after a tester's report that the act is "nothing but combat with
repetitive enemies". The report is accurate, and the survey below shows why: Montserrat was
built as a corridor. This is the first release whose centre of gravity is new content rather
than restoration, because it is the first place the game *plainly ran out* in the sense the
charter means -- not a dark branch, but an act with one conversation in it.

Measured against `data.dat.vanilla.bak` as this mod leaves the game
(`python tools/reachability.py --survey "Montserrat" --with-mod`, plus the part-level scan
0.9.0 and 0.9.1 used).

### What Montserrat is

| Map | Scripted content | Enemies |
|---|---|---|
| `01 Grove Exterior` | the Ways Crystal and its undead node; the doors; the script that dismisses the Barcelona companions (Cervantes, Cortes and Darsh all leave here, by design); two loot spots | 8 snakebreed variants, vodyanoi |
| `02 Druid Council Level1` | a switch and a big door | snakebreed |
| `02 Druid Council Level2` | ten snakebreed generators, a treasure, and **Brother Montgomerie -- the act's only conversation** | snakebreed |
| `3 Animal Den` | ambient sound | bears |
| `4 Animal Cave` | ambient sound | wasps |

One character template, one tree (11 nodes, 6 voiced), two quests, 32 identical mojo drops.
Every Montserrat quest state -- Templar, Inquisition, Saladin, both Wielder variants, and the
three report-backs to Javier, Raphael and Cedric -- is activated somewhere. The relic icons
that sit unused in the cache belong to other acts. The Mountain Pass's sealed door is still
the one cut area on the road, and there is no map behind it.

**One thing is genuinely cut**: Montgomerie's `60 not long` -- *"Not long ago. A few days
maybe. I tried to stay alive until someone... came. I'm glad you did."* Voiced, and nothing
reaches it. Its own reply leads to Brother Michel, so it belongs on `45 prophecy 2`, where
Michel is first named.

**What the survey got wrong on first pass.** I said nothing on the map accounts for the
knights Javier and Torquemada dispatched. It does, silently: the three maps carry **31 dead
bodies** from `Dead Body Generator` parts -- Dead Knight Templar 1 through 4, Inquisitors, the
abbey's jailors, and dead snakebreed among them. The battle is depicted. What is missing is
anyone acknowledging it: no journal, no line, no name. That changes Tier 2 from "place a
fallen party" to "give the one that is there a voice".

### Tier 0 - the voiced orphan

`45 prophecy 2` gains a reply, *"How long ago did they come?"*, to `60 not long`. One authored
player line; the node and its reply are the game's. Dialogue only, any save.

### Tier 1 - the roster matches the text

Montgomerie: *"Horrible, powerful beasts. Monsters, assassins."* The maps are one enemy in
eight recolours. The snakebreed are the monsters. The *assassins* -- the other half of his
sentence -- are nowhere: every human assassin can the game ships is Act 4 or later (`Assasin`
is HP 150 / AC 280, the race 0.9.0 gave Machiavelli's two ambushers, and a tester called those
tough). The beasts are the bears and wasps in the two side caves, and they stay there.

**Decided: human assassins and Summoners join the packs; no bears, no titans, no ogres.**
Every outdoor generator is a `CSimpleGeneratorForCannedEntitiesAI` holding the six snakebreed
tiers so the pick scales with party mojo. The change is to the *mix*, not the count:

| Addition | HP / AC | Source | Role |
|---|---|---|---|
| Montserrat assassin, three tiers | 60 / 80 / 100, AC in the snakebreed band | a clone of the unused `Assasin EarlyLevels` can (Act 4 model, no map places it) on a **new `.Race`** authored on the shipped preset shape -- the first race file Fixt writes | the men behind the creatures; the same organisation as Tier 3's wounded handler and Tier 4's boss |
| Snakebreed Summoner / Tough / Super | 100-160 / 175-250 | Act 5, and `Random Forest Map 1` in the Wilderness | the family's caster: Poison Touch, Rigor Mortis, cure spells, summoning. The one enemy whose kill order matters |

Shares: Grove and Level 1, one human in every pack of three or more and a Summoner in every
pack of four; Level 2, the boss's crew is human and snakebreed together. Counts unchanged, so
XP is unchanged. Act 4's Crypt mixes human assassins with creatures the same way, which is
the precedent. This is tuning, it is a taste call, and it is reversible with no trace --
which is why it is recorded as a choice and not as a repair.

### Tier 2 - the fallen party gets a voice

The bodies are there. Add one that matters: a named knight at the Grove's gate (`Montserrat
Entrance door`, 2790,317 -- two Dead Knight Templar 4s already lie at 2770,793 and 715,3590),
on the shipped `Dead Body Generator` shape, with the one thing the shipped bodies lack -- an
`Action` on their `GetCloseThenTalk` specifier. Clicking him opens a small tree in the voice
of the *Saint Bartholomew coffin text* balloon: `<His hand is closed around a leather
journal.>` -> read it (three or four entries, one node each) -> take it / leave it. The
journal is a quest item on the Darkwood envelope, no Use Action -- the reading happens at the
body, which is the only readable-object idiom the game ships (no vanilla item opens text when
used; the four that have Use Actions open the generic no-talk bubble).

**The journal's content, and its limits.** Three entries: arrival and the abbot's welcome; the
attack -- snake-creatures out of the treeline and men in black behind them, from the south
road; the last -- the Crown is taken, they have gone north over the mountains, *"if you find
this, tell Brother Michel at Montaillou"*. It must not name who sent them. The player's first
naming of the Old Man of the Mountain is the Crypt assassins' `20 threat` in Act 4;
Machiavelli's *"Beware the Old Man from the east"* (`300`, restored in 0.9.0) is the earliest
the game lets it slip, and that is Act 3. Michel's `140 Dark Forces` -- *"I do not know for
certain"* -- must stay true when the player reaches him.

**Who reacts.** Montgomerie, one new reply on `20 attack` gated on holding the journal --
*"I found your captain's journal."* -- to one new node (unvoiced, beside six voiced ones; the
same compromise as Rakeb's additions) that names the captain and gives the *"they went north"*
beat a person to grieve. Lord Javier, one reply on his report-back for a Templar carrying the
journal, XP only. The Inquisition and Cedric get nothing extra: the journal is a Templar's.

The captain needs a name. Vanilla Templars are *Sir Auric*, *Sir Jorge*, *Sir Roger
Templeton*; the name is a decision for the maintainer, not the scope.

### Tier 3 - the assassin who talks

**The body exists and is unused.** `Resources/Levels/Start Game/Character Templates/Assasin
EarlyLevels.can`: a human assassin on the `Characters/Monsters/Assasin` model (the Act 4 model
0.9.0 gave Machiavelli's assassins), `Races/Demokin`, no inventory, placed by no map. An
"early levels" assassin the game built and never used -- exactly the enemy a Montserrat handler
would be.

**The pose is Montgomerie's.** His generator sets `Cur Sequence=Dead` at spawn and leaves the
talk specifier live; that is how a dying man is done here. Same shape: a wounded handler among
the dead knights in Level 1's great hall, past the big door (bodies cluster around 1600-2500,
1200-2500), where a fight both sides lost is already on the floor.

**The tree, about seven nodes.** He laughs at being found. Asks: who are you (Speech check ->
*"We serve the Master. In the East. You will meet him."*; fail -> *"Ask the snakes."*); where
did they go (*"North. Over the mountains. There is a second one."* -- Michel's `230 Explore
the Crypt` says the same from the other side); why (the relics, no more). Three exits: finish
him (XP; a Wielder variant in the register of Montgomerie's *"the relics will be mine"*),
leave him to die, or -- Karma good -- a mercy line. The fight exit is the proven 0.9.0 shape:
a template with `Category=Enemy` and a fight specifier, converted by `CGoToCombatAction` on the
reply; his race is cloned with HP in the twenties so "finish him" is one blow.

**The lore rule, stated once.** He may say *the Master* and *the East*. He may not say *the
Old Man of the Mountain*, *Alamut*, or *Hashashin*. Act 4 owns the name.

**Who reacts.** A checker `questioned the assassin`; at Brother Michel's `80 Advice`, the
player's question *"Do you know who attacked Montserrat?"* gains a sibling reply -- *"Assassins
out of the East. One of them told me before he died."* -- to a new unvoiced Michel node that
accepts it without contradicting his `140 Dark Forces`. Optional; the scene stands without it.

### Tier 4 - the fights

**What the combat is now.** 64 generators across three maps, each holding the same six
snakebreed tiers, each spawning two to four when the player comes within radius 40. No roles,
no ranged, no casters, no traps, no scripted encounter, no boss with a name. The one scripted
beat is real and invisible: Level 2's `Snakebreed dead relay` lets Montgomerie speak only once
the snakebreed near him are dead -- a "clear the sanctum" rule the player never perceives.

**What the AI is.** Scan, chase, attack; patrol; guard a moving position; go to a point. Across
the 700-odd monster cans there is no flee, flank, focus-fire or kite. Tactics in this game are
never innate; they are set pieces scripted over a simple AI, and the game ships every hook:

| Hook | Shipped use | The tactic |
|---|---|---|
| `CAIHealthPercentThresholdTrigger` (crosses below N%) | Wizard Tremblethorn: relays at 60% and 25% | boss phases |
| Damaged Script on a can (relay on first hit) | Goblin Bludjund: hit him and the camp turns | a sentry that calls for help |
| Destroyed Script (relay on death) | the troll pit, Jafar | consequences: the priestess dies, her summons drop |
| Go-to marker + delete (the walk-off) | Machiavelli, 184 vanilla uses | a scripted retreat |
| `CGaurdNearMovingPosAI` | Fernand as companion | bodyguards that stay on the boss |
| Fade-in generator on an interaction | the assassins' trapped chest | an ambush, not a radius spawn |
| `Valid Targets=Summoned Creature` | 50 uses | enemies that go for the player's summons first |
| razor / spike / fire trap repeaters | Maw of the Assassin, Alamut, the Crypt | the assassins mined their retreat |

None of this makes an enemy decide anything. It makes encounters with a shape. That is the
honest ceiling, and it is stated here so nobody reads "tactics" as "smarter AI".

**Encounter by encounter.**

*Grove.* Bears replace a third of the packs (Tier 1). One patrol group walks the ruins on
`CPatrolAreaAI` instead of standing at a radius. One pack has a **sentry**: a Snakebreed Venom
with a Damaged Script that activates two reinforcement generators behind the player (the
Mongol Camp's `Goblin Reinforcements` shape). Kill him in one blow, or sneak past, and they
never come.

*Level 1, the hall.* The **big door is an ambush**: pulling the switch opens it and activates
a fade-in pack behind the player (Port District's `Ambush Generator Poly`). A **razor
corridor** on the far side, telegraphed by a dead knight lying in it, on the Maw's repeater. A
Summoner in every pack, so the priestess is always the first problem. The **last** snakebreed
of the hall's final pack is scripted to break off and run for the sanctum on the walk-off
shape -- the player sees it go, and meets it again.

*Level 2, the sanctum.* The **rearguard's captain, Sahar**, on `Snakebreed Boss Super` (HP
160, AC 250 -- already the strongest can placed here), standing at the reliquary between the
door and Montgomerie, with two Venom bodyguards on guard-AI and a Summoner behind her. A
short exchange on approach -- cold, amused, the Crypt assassins' register: *"You are too late,
Lionheart. The Master has what he came for."* -- three replies and the fight; the lore rule of Tiers 2 and 3 applies -- *the Master*,
*the East*, never *the Old Man*. **At 60%** the side doors open and the hall's runner comes in
with whatever retreated; **at 25%** she falls back to the reliquary and the priestess heals
her -- the player learns to kill the priestess. Then Montgomerie's own gate does what vanilla
wrote it to do. The sacristy chest (`Hidden Treasure`) is **trapped** on the Chamber of
Torment shape: open it and two assassins fade in -- unless it is disarmed first (Tier 6).

**Roster and difficulty.** Total spawns unchanged; XP unchanged. Difficulty moves from sixty
identical fights to six different ones and some walking. The boss is the only new template
(0.9.0's clone pattern: shipped race, shipped model, a name).

**Risks, all paid for once already.** A spawned enemy that will not fight (0.9.0 first pass:
no specifier, no Enemy category); an ambush that fires on the wrong side of a door (0.9.0's
inn polygon, three passes); bodyguards that attack a neutral (0.9.0's assassins and
Machiavelli). Gate 3 cases for each.

### Tier 5 - the abbey tells its own story

**The primitive is shipped.** A prop with a `GetCloseThenTrigger` specifier whose action is a
`CDisplayDialogBalloonAction` on a "HOVER TEXT" tree: the Columbus statue, the Montaillou
headstones, the Crossroads signpost, the telescope, the *Saint Bartholomew coffin*, and
`Cervantes Dead Body text` -- *"<Examining the body, you observe it to be that of Cervantes...
the result of very apparent torture.>"* Click a thing, read a line. The burned hamlet in
Montaillou is sixty bodies and Beatrice narrating; Montserrat is thirty-one bodies and silence.

**What is on the maps and says nothing.**

- *31 bodies* in three clusters -- at the gate, in the hall around the big door, in the
  sanctum -- Templar knights, Inquisitors, the abbey's jailors, dead snakebreed among them.
  The placement already tells the story (they held the gate, fell back to the hall, died at
  the reliquary). Nobody narrates it.
- *A camp* in the Grove at 4400,3400: five bedrolls, a campfire, a woodpile. Unlabelled.
- *98 candles and 80 torches, all lit.* Montgomerie says "a few days". Lit candles mean
  someone is still tending them.
- *The big door's model is `DruidGroveGate`*, and the level is named Druid Council. The abbey
  stands on a druid site; the game's Act 7 is *Stop the Druids*. Its own thread, three acts
  early, unremarked.
- *The sacristy chest* (`Hidden Treasure`, L2 1806,1111) is where the Crown was. It is a loot
  chest.
- *No monks.* Knights, inquisitors, jailors -- not one monk among the dead. Montgomerie is
  "the last survivor of Montserrat".

**The sanctum is re-dressed as an abbey.** Level 2 is a candle-lit cave: candles, torches,
pots, brick. The sanctum around Montgomerie (3878,2391) and the reliquary gains, from the
shipped prop library: an `altar cross` on an `altar wall`, a `last book` on the altar, two
rows of `pew` with two knocked over, a `burned banner` on the wall, `debris` and `bones` at
the reliquary, and the chest replaced by an open `chest_gold` that is the Crown's empty case.
The hall gains a `broken barracade` at the big door -- the thing the knights died behind.
This is a visual change to two vanilla rooms and is recorded as such. Every prop is checked
against the walkable floor before placement (the 0.9.0 inn anchor lesson), and none of them
is collidable where a path runs.

**The monks are missing, and the game says so.** One hover text in the sanctum: `<Knights of
the Temple, men of the Inquisition, the abbey's own jailors. Not one monk among them. The
cells below are empty.>` It notes the absence and does not explain it. The game never does
either; the Crypt assassins take a seer alive in Act 4, and a player who remembers this line
there will draw the line themselves. Nothing in Fixt will ever confirm it.

**The trail -- about ten hover texts, gate to sanctum**, each a thing the player can see:

| Where | On | The line says |
|---|---|---|
| Grove, the camp | the campfire | cold ash; bedrolls slept in once. The party camped here the night before they went in |
| Grove, the gate | Tier 2's captain | the journal; his shield still raised, wounds from the front |
| Grove, the gate | a dead snakebreed | the first thing that came out of the treeline |
| Hall, the big door | the barricade | broken from the inside -- they opened it to sally, and died in the doorway |
| Hall | a jailor's body | the abbey kept cells; his keys are gone |
| Hall, the razor corridor | the knight lying in it | Tier 4's telegraph |
| Hall or sanctum | a candle stand | the wax is fresh. Someone lit these today |
| The druid gate | the door | carved long before any abbey; the monks built over it and did not remove it |
| Sanctum | the reliquary | open, empty, the velvet still shaped to what it held |
| Sanctum | the dead | the missing monks, above |

All unvoiced. All `.zax` edits, so the same save constraint as the rest of the release. The
lore rule of Tiers 2, 3 and 4 applies to every line: nothing names who sent them, nothing
contradicts Montgomerie's *"a few days"* or Michel's *"I do not know for certain"*.

### Tier 6 - the abbey reads the player

**What vanilla maps read.** Across every shipped `.zax` (test maps excluded): Karma 160
times, gender 39, race 38, Sneak 32, perks 28 (almost all the *title* perks -- Merchant
Slayer, Child Killer, Stargazer), Perception 22, the factions about 80, Speech 7, Find Traps /
Secret Doors 1, Strength 1. The shapes are simple: `Sneak < 50` at the Khan's chest wakes the
guards; `Find Traps >= 35` at a Temple store room reveals the cache; a Fenclaw line varies on
`ST <= 5 OR female`; a secret is a `CAISecretReveal` with a skill adjustment, revealed
passively by the Find Traps skill; a prop can carry a second description node (`1 Description
alt` on the Columbus statue) chosen by the opener. Nothing simulates stealth or tactics -- a
check is a threshold read at a trigger. That is what this tier builds on, and nothing more.

**Seven levers, each riding a scene the scope already builds. No new scenes.**

| Lever | Where | Shape |
|---|---|---|
| **Sneak** | The Grove sentry and the big-door ambush (Tier 4) read `Sneak >= 40` while the player is sneaking: pass, and neither fires; the hall's runner never runs. A stealth build reaches the wounded assassin (Tier 3) with the pack still asleep | the Khan's chest |
| **Find Traps / Secret Doors** | The razor corridor (Tier 4) reveals itself at skill >= 35 instead of cutting. A **secret door** in the druid level -- the druids' back way into the sanctum -- is the only flank in the boss fight; the AI cannot take it, so it belongs to the build that finds it. A Sylvant opens it by touch (below) | the Temple store room; `CAISecretReveal` |
| **Perception** | Alternate lines on the Tier 5 trail at `PE 7+`: the tracks lead north, the wax is hours old, the captain's wounds are from *behind*. The same props, a second node | `1 Description alt` |
| **Outwit / Speech** | The boss (Tier 4) and the wounded assassin (Tier 3). The assassins hold Machiavelli's contract *"to find one such as yourself"*; at `Outwit 7+` the player claims to be his courier and the bodyguards stand down before the fight -- she still fights, alone. Speech at the assassin as Tier 3 already has it. Bounded by the lore rule | `Outwit N greater or equal` (13 shipped cans, almost unused) |
| **Race** | The unused assassin can is **Demokin**: a Demokin player is recognised -- *"one of the Master's own?"* -- and hears a line the others do not. A **Sylvant** opens the druid door by touch, no skill: the tainted races are the game's nature-magic people, and the door is a druid's | `Demokin IS`, `Sylvant IS` |
| **Lockpick / Disarm** | The trapped sacristy chest (Tier 4): at `Lockpick Disarm Traps` >= 35 the trap is found and defused and the chest opens quietly; below it, the two assassins come. Pulled forward from the held list by decision | `Lock Pick Adjustment` / the store-room threshold shape |
| **Faction** | Templar: the fallen are the player's brothers -- Javier's journal reply (Tier 2) and one Templar-only line from Montgomerie. Inquisitor: the Inquisition dead carry a sealed order, one hover text. Saladin: the assassin's *"the East"* lands differently on an Aswaran -- one line. Wielder: the Ways Crystal already pays a Wielder; the druid gate answers spirit, one line. Horde: nothing, and it should be nothing | the faction cans |

**Held for a later cut, with the reason.** *Strength* -- forcing the barricade to skip the
switch and its ambush is a good trade but the one vanilla ST check is a dialogue variant, not
a door; untested shape. *Lockpick / Disarm* on the jailors' cells -- cheap, deferred; the trapped
chest's disarm is pulled forward into the six (decided). *Divine* consecration of the
re-dressed altar for a blessing -- the *Torquemada Divine Boon* perk shape, a new reward
that needs its own design. *Karma* -- selling the assassin what he wants, Michel's
whereabouts, for gold, has a consequence at Montaillou that has to be designed before it is
promised. *Title perks* at the dead of the player's own victims -- one line each, cheap,
later. **The necromancer** -- raising the thirty-one dead to fight the boss is the best idea
on the list and is **untested**: whether Raise Undead works on generator-spawned bodies is a
question for a live save, not for the archive, and nothing is written into the scope until
it has an answer.

**Rule for all of it.** A lever opens a route or adds a line. None removes one. The player
with no Sneak, no Perception and no faction gets exactly the abbey Tiers 0 through 5 build.

### What is NOT in it

- The Mountain Pass's sealed door. There is no map behind it.
- Companions at Montserrat. Their dismissal at the Grove is scripted and deliberate.
- The Wilderness "beasts" cut from other acts (the `undead to kill cortes` pair, etc.).
- Voice. Every new line is unvoiced. The two voiced nodes touched (`45`, `60`) keep theirs.

### Decisions before build

All taken, in order:

1. **Roster**: human assassins and Summoners at the shares in Tier 1; bears stay in the den.
   The tester's words: the animals in the caves are enough for beasts.
2. **The captain** is *Sir Tomas de Vilanova*; Javier reacts for a Templar, XP only.
3. **The assassin** gives up all three lines -- who (Speech-gated), where, why -- under the
   lore rule.
4. **Michel** accepts what the player learned, one unvoiced node beside his voiced ones.
5. **The boss** is *Sahar*, contemptuous, three replies and the fight.
6. **The chest** is trapped and disarmable at Lockpick / Disarm 35.
7. The sanctum is re-dressed as an abbey; the monks' absence is noted and not explained.
8. Tier 6 at seven levers. The necromancer is tested on a live save before anything is
   written.

### What was built, and where it departs from the scope

Everything above is in `files/`, on a save that has never entered Montserrat. Twenty-three
files: three Montserrat maps, Michel's house and the Temple District; seven dialogue trees
(four new); five character cans (four new); four race files (new); one item. Every
`.zax` re-serialised canonically; `validate.py` clean, and it earned its keep -- it caught
five props placed with `Cur Sequence=idle` on models that use `Idle`, the exact class of
crash 0.5.1 shipped and then wrote the check for.

**Tier 0.** As scoped.

**Tier 1.** As decided. 34 generator groups in the Grove and 36 in Level 1 gain a Montserrat
Assassin of the group's tier weighted to average one per pack; the 40 groups of four also gain
a Summoner; four fixed snakebreed spawns become assassins. The three pack races are
150/60/35, 175/80/45, 200/100/55 (AC/HP/melee) against the snakebreed's 150/60/30,
175/75/35, 220/100/50.

**Tier 2.** As scoped, with one simplification: the game's own corpse script strips a dead
body's interaction and replaces it with a spells-on-the-dead specifier, so the captain is a
plain vanilla dead knight (the `Fixed Dead Body Generator` shape) and the *reading* is an
examine polygon over him -- exactly how the game does Cervantes's body. The journal reads
at the body, three entries, take it or leave it; the item is the Feralkin Journal envelope.
Montgomerie's `21 the captain`; Javier's `531 tomas` takes the book, gives the quest state
the vanilla reply gives, and pays 500 XP from a new Experience part in the Temple District.

**Tier 3.** As scoped. The dying pose is Montgomerie's generator verbatim; the talk is both
the can's own specifier and an examine polygon, since nothing proves a Dead-sequence entity
takes a click. Three questions (the first Speech-gated, the fail line *"Ask the snakes"*), two
exits and a Karma-650 variant of the second. "Finish him" is a scripted execution -- a dying
man does not stand up to fight -- through a half-second delay, a corpse generator and the
polygon retiring; 100 XP. Any question fires a once-only relay: 150 XP, the local checker, and
`COtherMapAction` into Michel's house, which is how vanilla carries state between maps. Michel's
`80 Advice` swaps its *"Do you know who attacked Montserrat"* for the player's own answer once
that checker exists, to the unvoiced `141 out of the east`.

**Tier 4 -- three departures.** *The big door is not a mid-level gate.* It is the
`DruidGroveGate` at 3329,424, three feet from the entrance spawn, and pulling its switch
relocates the player back to the Grove; it is the way out. The ambush is a strip across the
hall at y=1700 instead, a fade-in pack of three north of it -- behind a player heading for the
inner door -- with the Sneak-40 pass. *The razor corridor is a needle trap.* The buzzsaw
props animate but carry no damage of their own that the archive shows; the Thieves
Congregation's Lightning Trap does -- mojo-scaled, three tiers -- so the trap is that
envelope with poison, before the inner door, found and stepped over at Find Traps 35 (and it
keeps the vanilla trap's own `CAISecretReveal`, so the skill reveals it twice over). *The
bodyguards are not on guard-AI.* `CGaurdNearMovingPosAI` guards a companion's follow target,
not a named entity, and the read did not find the field that would point it elsewhere. Two
Venom spawn beside Sahar when the fight starts and fight; the priestess likewise. The runner
is as scoped, on the walk-off; Level 2 learns he arrived through the same cross-map activate.

Sahar herself: `Snakebreed Boss Super` named, force-generated by a once-only strip at the
sanctum threshold, standing passive (empty target type) for four lines and the fight; her
tree's `Default Canceled Node Action` also starts the fight, so closing the window is not a
way past her. The Montgomerie gate's `CIsAliveAction{Snakebreed}` is now an OR with `Sahar`,
because `New Name=Snakebreed` is what every vanilla snakebreed carries and she needed her own.
**Phase two is a scripted cure** -- 60 HP, the heal effect, *"The Master is not done with me"*
-- not the priestess's AI, which the archive cannot prove targets allies. **The trapped chest
is the west one** (1143,365), the first thing in Level 2, not the sanctum's: springing two
assassins beside a dying man and a boss fight was the wrong room for it.

**Tier 5.** As decided. Seven props, all `Collideable=0` so nothing new can block a path;
the altar is a wall, a cross and an open book against the sanctum's north wall, two pews on
the south side, a burned banner west, bones by the well grate, the barricade at Level 1's
door. The reliquary is the altar's own hover text -- *"the velvet cloth still holds the
shape of what rested there"* -- rather than a chest sprite that would have read as closed.
Ten hover stops as scoped, less the captain's Perception line: *"wounds from behind"* would
have implied a betrayal the release does not otherwise support, and his body says *from the
front*.

**Tier 6.** Six of seven levers built; **the druid secret door is not.** The sanctum has one
entrance and the flank needs a passage the map does not have, and props cannot make one.
Sylvant gets a reading at the druid gate instead, beside Wielder's; the gate now has four
readings (Wielder, Sylvant, Intelligence-or-Educated, plain). Outwit 7 at Sahar stands her
crew down and she fights alone (`sahar fights alone`). Demokin at the assassin gets the road
without a Speech roll; Saladin gets *"he has men in your order too, Aswaran"*. Templar gets
Montgomerie's `22 brother`. Inquisitor gets the sealed order on the Inquisition dead in Level
2 -- *"let no one speak with the prisoners"* -- which is the one place the release lets the
monks' absence be a question. Nobody answers it.

**Not in it, with reasons:** the patrol group (vanilla's patrol-on-spawn is a
`CLimitedTimeAI` inside canned AIs, more shape than the value warranted); guard-AI bodyguards
and the secret door, above; the necromancer, untested.

### Repairs from the 0.10.0 playthrough, as they come in

**The goodbye was in the middle of the menu.** A reply's position in the menu is its position in
the file, and every reply Fixt spliced into an existing node went wherever the splice was
easiest -- after the goodbye, on Quinn, Enrique, the Warning Troll, the Blacksmith, Amir,
Javier, the Saladin knight, the Goblin Girl and the Khan. Twenty-eight nodes, each compared
against its vanilla copy and reordered only if Fixt had touched it: the Exit-icon replies move
to the end, everything else keeps its order, and the pass asserted per node that no line
changed. Vanilla's own convention, restored.

**Quinn's reserve joins his shop, and the errands come out from under "questions".** The
tester's question was why the potion tiers needed a separate store at all. Because the engine
has no action that adds an item to a merchant: a shop's stock is a fixed list on a `CMerchantAI`
map part, and the only runtime knobs are price multipliers. So the choice was a second window
(what 0.4.0 built) or a second copy of the whole shop with the tiers folded in. Now the
latter: six merged merchants -- Good Store and the Templar/Inquisition store, each with Reserve
One / Two / Three appended -- and every one of the 23 replies that opens a base store opens
the richest merged one the player has earned instead. Each step also checks that the merged
part *exists*, so a save that entered the shop before this build falls through to the plain
store and gets the old reserve reply -- on the greeting, not buried. The three errand offers
sit on a hub, `805 errands`, reachable from every greeting by *"Is there anything around here
I could help you with?"*; the copies under `05 Other Questions` stay.

**The wounded assassin vanished when finished.** Delete-and-respawn-a-corpse in one tick left
nothing behind. "Finish him" is now a 500-point blow from the player through
`CActionDoDamage`, so he dies where he lies and stays. Level part; a character who has not
entered Level 1.

**0.9.1 crashed the game on entering the Mongol Camp from the cave.** *"Tried to use an unknown
class 'CMultipleActionsAction' for a 'Then'"* -- the gate polygon's `Then=` value began with
three tabs, left over from re-indenting the vanilla challenge block under the new `Else`. The
canonical re-serialiser keeps leading whitespace as part of a value, so the file passed every
check and the engine looked up a class that does not exist. The only such value in the mod.
`validate.py` now fails any class-valued field whose value starts with whitespace, and it
names the 0.9.1 file when run against it. Shipped in 0.9.1, 0.9.2 and 0.9.3; hotfixed as
0.9.4.

**The peaceful road through the sewers ended two steps short.** A player who reached troll
peace by the parley, ran the chief's errands and then argued Enrique out of the contract had
done more for the trolls than anyone -- and could not get a hide for Quinn without either
killing a Lava Troll Boss (breaking the peace) or having settled the wererats first. And
Enrique's chain is linear: kill the trolls, take the gold, *"there is one thing more"*, the
cure quest -- so withdrawing the contract stopped the chain and the beggars stayed wererats.
Two additions, both on the chain's own facts. **The chief gives a hide from his dead** once
*Speak for the Trolls* is complete, Quinn's errand is open and no hide is held -- the field of
thirteen the player counted for him. **Enrique still asks for the cure** after the
withdrawal: one new reply on both greetings, one line of his acknowledging the argument, and
then vanilla's own confession flowing into the shipped `155 Potion 2`. Four routes to the
hide now, and the peaceful one is complete.

**Enrique's red-ore door was shut.** The third way to talk him out of the troll contract --
*"There is red ore moving up out of that pit now"* -- was gated on `current(final state)` of
The Red Ore Trade alone, and that quest completes in the same reply that sets its final
state. The chief's own tier gates on the same quest are `completed OR current(final)`; the
door now is too. Fifth confirmed instance of the rule, 0.5's own, and one the sweep missed
because it looked at the state being *set*, not at the completion beside it. Played to
passing.

**The Saladin summit froze, then Amir attacked.** 0.7.0 built the Knights of Saladin's cathedral
scene by cloning the Templar chain, and the Templar chain has a precondition the clone did not
carry. The summit's script lives on a *generated* Javier: `RESET MAP for Invulnerable Javier`
deletes the placed one and spawns one whose AI waits for "AI Done" and then starts the
faction's conversation. That reset fires on entering the cathedral through the door -- which
every Templar has done before their summit, and which the Inquisition relay calls explicitly
because an Inquisitor may not have. A Saladin arrives by Amir's relocate, never through the
door; "AI Done" went to a Javier with no script, and nothing happened. The Saladin relay now
calls the reset as the Inquisition's does. Amir, meanwhile, was spawned from `Jafar Generator
Wielder NIS` -- the Wielder summit's Jafar, scripted to hunt the dark wielder as an
uninteractable actor -- so when the tester skipped the frozen scene he attacked and could not
be attacked. A `Jafar Generator Saladin NIS` with the target type blanked replaces it.

**Then the scene would not end.** Javier's *"I am ready to depart for Montserrat"* fires
`determine ending relay`; Amir's copy of the reply jumped to his goodbye node instead and left
the sequence running with nothing to end it. Amir's reply now fires the relay; his goodbye is
the end relay's own balloon. Played to passing: the scene, the exchange, the fade, and the
return to the Gate District.

**The Vodyanoi Anatomist perk did nothing.** 0.6.0 built it as a `CPlugInBehaviorStrikeAction`
with a model check on `$trigger` inside the strike -- an invented shape. The game's own
Necrosage uses two behaviours, a strike that re-strikes the current target and a
`CPlugInBehaviorDamage` gated by a `Hit Or Miss` condition file; rebuilt on that, with a
`Vodyanoi IS` monster-race can and a `HitVodyanoiOnly` condition, it *still* did nothing for
the tester's unarmed character -- and the archive says why: every vanilla use of that shape is
a weapon addition or a perk written for weapons, and the game's own unarmed perks (Pugilist,
Bonus HtH Damage) never touch it; they raise the unarmed damage attributes directly. The
working build is on the target side: `Common Objects and Scripts/Vodyanoi Anatomist Strike`
is the `Damaged Script Action` of all twelve vodyanoi cans (the Bludjund shape, which fires on
any damage from any source) -- if the attacker holds the perk, 4-10 piercing through
`CActionDoDamage`, with a 0.3-second category guard so the bonus hit cannot re-trigger
itself. The perk file is a title with no behaviours. **Proven from the save's combat log**:
*"Grall hit Vodyanoi for 14 (14 Crushing Damage)"* / *"Grall hit Vodyanoi for 6 (6 Piercing
Damage)"*, fifteen bonus hits in a row, all in the band -- and the log is how the next such
question gets answered, since the save keeps it. Two things learned on the way: a spawned
creature carries the can it was spawned from, so a can change reaches only creatures
generated after it (the tester's first fight was against vodyanoi spawned before the
install); and the save's event log records every hit with its damage type.

**The goblin in Scar Ravine thought everyone knew the Khan.** 0.5's variance pass gave the
goblin holding the woodcutter's daughter a Strength route (*"Step over him, pick the child up,
and look down. Try."*) and a Barter route (the salt-pork offer), and pointed both at `70
scared` -- the vanilla node written for the two routes that invoke the Khan: *"Y-you know the
Khan? You will speak well of me?"* Neither added route mentions him. Each now has its own
answer, unvoiced like the replies, with `70`'s flee-and-free actions verbatim: `71 backs
down` for the strong, `72 the trade` for the trader. Fixt's own defect, found by the tester
on the second playthrough. Dialogue only, any save.

**Fernand handed out the wrong bottle, and it was 0.8.1's fault.** 0.8.1 made Juan's rescue
check for `Potion Fernand Healing` by name and repointed a give to hand it out -- but the give
it repointed was `mute sailor rewards for solving quest`, which is the Mute Sailor's reward,
not Fernand's. Fernand's own gives are in his tree, `Distressed Sailor.DialogTree`, on `30
take the job` and `40 hard barter`, and both still gave the vanilla `Inventory Items/Potion`.
A fresh character reached Juan with a plain potion and was told a potion might have saved
him. Now Fernand's two gives hand out the draught and the Mute Sailor's reward is vanilla
again. The lesson is the one 0.8.2 already wrote down about Quinn: **count the copies, and
check whose reward it is.**

**Juan was a corpse, and draining him soft-locked the quest.** He was spawned through the
game's dead-body script, which is what Fixt's 0.6.0 restoration inherited from vanilla's
unsaveable Juan. Two wrong fixes before the right one, recorded because the reads matter:
stripping the `Corpse` category on approach (the drain still worked from range), then
stripping it at spawn (the drain still worked). **Absorb Spirit does not target the category.**
Its targeting is `Interaction Filter=After Death Spell`, which matches the
`GetCloseThenFightWhenDead` specifier the dead-body script attaches -- "allows dead entities
to still be interactable (for spells on the dead)". Juan now spawns the way the wounded
assassin at Montserrat does, on Montgomerie's dying pose: `Dead` sequence, hit points intact,
a `CWaitAI` listening for the rescue's `Raise Enemy` message, his sailor-banter click removed,
non-collidable, and no dead-body script at all -- so the specifier the skill filters on never
exists on him. The rescue and the 45-second bleed-out both key on a checker `juan saved` now;
the bleed-out had keyed on `Corpse` too, so the first "fix" would have disarmed it and
soft-locked a slow player the other way. Whatever happens to Juan, one of the two branches
fires. The item is *Fernand's Draught*; the engine appends the effect's name to magic
consumables, and *Fernand's Healing Draught of Healing* was the result.

Proven by the report along the way: a Dead-sequence entity takes a click through an ordinary
interaction specifier, which is what Tier 3's belt-and-braces polygon was hedging.

**The brothers' reunion was written and never played.** Vanilla has three lines for it:
Juan's *"Mi hermano! You saved me!"* (`1 Save Juan`), Fernand's `30 saved juan` -- *"Claro que
si! You don't think I would let those devil fish kill my little brother, eh? You should thank
this stranger too"* -- and Juan's *"And many thanks to you, stranger"*. `30 saved juan` is a
balloon nothing fires. 0.6.0 had played the first at the rescue spot and made the third a
click. Now the rescue stands Juan up and sends him to a marker beside his brother (the vanilla
walk-off's own `CGoToAI`, one leg); on arrival a relay plays the three vanilla lines and
**three new ones** in which Fernand chides him for fishing off the north island alone --
*"Twice I told you, Juan"* / *"You did not say what was doing the fishing"* / *"before you
bleed on my boots"* -- and then the vanilla walk to the ship. If Fernand is not alive, Juan
goes straight home. The rescue's click on Juan (*"And many thanks..."*) stays, for a player
who catches him on the way. And he does not run off the instant he stands: his thanks to
the player plays over his head at the rescue spot first, and the walk starts when it closes.

**The timer is visible now.** The bleed-out relay always ran 45 seconds from the first
approach with nothing to say so; a second delay at 20 seconds plays *"<His breathing is
shallower. He has minutes, not hours.>"* if he is not yet saved. Both are gated on the checker.
Played and passing on a fresh Port District: the draught, the cursor, the thanks, the
reunion, the chiding and the walk.

### Gates before this ships

- Gate 0: `validate.py` clean; the new template's `Race=` real, its `Model=` and every `Cur
  Sequence=` ones vanilla uses; every new quest item icon a path that exists.
- Gate 1: **needs a character who has not entered Montserrat.** Every tier but 0 edits the
  three `.zax` files. Play order: Grove gate (journal) -> Level 1 (assassin) -> Level 2
  (Montgomerie, `60`, the journal reply) -> Montaillou (Michel).
- Gate 3: the assassin must be attackable from the fight reply (0.9.0's first-pass defect) and
  must not attack Montgomerie or the player's companions -- there are none here, which is one
  reason the scene is placed at Montserrat.

### The honest recommendation

Tier 0 costs nothing and ships regardless. Tiers 2 and 3 are the release: a body with a name
and an enemy with a voice are what a corridor needs to become a place, and both are built from
templates and idioms the game already has, with the lore boundary written down. Tiers 1 and 4 are
the maintainer's call; the recommendation is to do both, because the tester's complaint was
as much about the sixty identical fights as the empty rooms, and Tier 4 is where the act
stops being a corridor with a conversation at the end.
## 0.9.4 - hotfix

**Published.** Cut on a branch from `v0.9.3`. One crash, four repairs, one new check.

**0.9.1 crashed the game on entering the Mongol Camp.** *"Tried to use an unknown class
'CMultipleActionsAction' for a 'Then'"* -- the gate polygon's `Then=` value began with three
tabs, left over from re-indenting the vanilla challenge block under the new `Else`. The
canonical re-serialiser keeps leading whitespace as part of a value, so the file passed every
check and the engine looked up a class that does not exist. Shipped in 0.9.1, 0.9.2 and 0.9.3.
`validate.py` now fails any class-valued field whose value starts with whitespace, and names
the 0.9.1 file when run against it.

**The Knights of Saladin's cathedral summit froze, then Amir attacked, then it would not
end.** 0.7.0 cloned the Templar chain without its precondition: the summit's script lives on
a Javier generated by `RESET MAP for Invulnerable Javier`, which fires on entering through the
door -- every Templar has, a Saladin arriving by Amir's relocate never has. The Saladin relay
now calls the reset as the Inquisition relay does. Amir was the Wielder summit's hostile,
uninteractable Jafar; a Saladin generator with the target type blanked replaces him. And
Amir's *"I am ready to depart"* now fires `determine ending relay` as Javier's does. Played
to passing. The map half needs a character who has not entered the cathedral; the ending is
dialogue and works on any save.

**Enrique's red-ore door was shut.** The third way to talk him out of the troll contract was
gated on `current(final state)` of The Red Ore Trade alone, which completes in the reply that
sets the state. Now `completed OR current`, the shape the chief's tiers already use.

**The peaceful road ended two steps short.** A player who reached troll peace by the parley,
ran the chief's errands and argued Enrique out of the contract could get no hide for Quinn
without breaking the peace, and never heard about the wererat cure because Enrique's chain
only continued past a completed kill. The chief now gives a hide from his counted dead once
*Speak for the Trolls* is complete and Quinn's errand is open; Enrique still asks for the cure
after the withdrawal, in vanilla's own words behind one acknowledging line.

All dialogue and one map; the Mongol Camp and cathedral halves take effect on characters who
have not entered those maps.

## 0.9.3 - repairs

**Published.** Repair only, cut on a branch from `v0.9.2`: one dialogue file, one perk, one
shared script and the twelve vodyanoi cans. Both found on the second playthrough; both proven
before the cut.

**The Vodyanoi Anatomist perk did nothing.** 0.6.0 built it as a `CPlugInBehaviorStrikeAction`
with a model check on `$trigger` inside the strike -- an invented shape. Rebuilt on the game's
own Necrosage shape (a strike that re-strikes the current target plus a `CPlugInBehaviorDamage`
gated by a `Hit Or Miss` condition), it *still* did nothing for an unarmed character, and the
archive says why: every vanilla use of that shape is a weapon addition or a perk written for
weapons, and the game's own unarmed perks never touch it. The working build is on the target
side: `Common Objects and Scripts/Vodyanoi Anatomist Strike` is the `Damaged Script Action` of
all twelve vodyanoi cans -- the shape Goblin Bludjund uses to raise the camp when he is hit,
which fires on any damage from any source -- and if the attacker holds the perk it deals 4-10
piercing through `CActionDoDamage`, with a 0.3-second category guard so the bonus cannot
re-trigger itself. The perk file is now a title with no behaviours. Proven from the save's
combat log: *"Grall hit Vodyanoi for 14 (14 Crushing Damage)"* / *"Grall hit Vodyanoi for 6
(6 Piercing Damage)"*, fifteen bonus hits in the band.

Two things learned on the way, both now in the modding notes: a generated creature carries
the can it was spawned from, so this reaches only vodyanoi spawned after the install; and the
save's event log records every hit with its damage type, which is how the next question of
this kind gets answered.

**The goblin in Scar Ravine thought everyone knew the Khan.** 0.5's variance pass gave the
goblin holding the woodcutter's daughter a Strength route and a Barter route and pointed both
at `70 scared`, the vanilla node for the two routes that invoke the Khan -- *"Y-you know the
Khan? You will speak well of me?"* Each now has its own answer, unvoiced like the replies,
with `70`'s flee-and-free actions verbatim: `71 backs down` for the strong, `72 the trade` for
the trader.

Both work on any save; the perk's bonus on any vodyanoi spawned after installing.

## 0.9.2 - repairs

**Published.** Repair only, cut on a branch from `v0.9.1`, four files, all in the Port District,
all found on a fresh character's first visit and each played to passing before the cut.

**Fernand handed out the wrong bottle, and it was 0.8.1's fault.** 0.8.1 made Juan's rescue
check for `Potion Fernand Healing` by name and repointed a give to hand it out -- but the give
it repointed was `mute sailor rewards for solving quest`, the Mute Sailor's reward. Fernand's
own gives are in his tree, on `30 take the job` and `40 hard barter`, and both still gave the
vanilla potion, so a fresh character reached Juan with a plain potion and was told a potion
might have saved him. Both of Fernand's gives now give the draught; the Mute Sailor's reward is
vanilla again. The item is *Fernand's Draught*: the engine appends the effect's name to magic
consumables, and *Fernand's Healing Draught of Healing* was the result.

**Juan was a corpse, and draining him soft-locked the quest.** Two wrong fixes before the
right one, recorded because the reads matter: stripping the `Corpse` category on approach
(the drain still worked from range), then at spawn (still worked). Absorb Spirit does not
target the category; its `Interaction Filter=After Death Spell` matches the
`GetCloseThenFightWhenDead` specifier the game's dead-body script attaches. Juan now spawns
on Montgomerie's dying pose -- `Dead` sequence, hit points intact, a `CWaitAI` listening for
the rescue's `Raise Enemy`, no dead-body script -- so the thing the skill filters on never
exists. Rescue and bleed-out both key on a checker `juan saved`; the bleed-out had keyed on
`Corpse` too, so the first "fix" would have disarmed it and soft-locked a slow player the
other way. Whatever happens to Juan, one branch fires.

**The brothers' reunion was written and never played.** Vanilla has Juan's *"Mi hermano! You
saved me!"*, Fernand's `30 saved juan` -- *"Claro que si! You don't think I would let those
devil fish kill my little brother, eh? You should thank this stranger too"* -- and Juan's
thanks; `30 saved juan` is a balloon nothing fires. Now Juan stands, thanks the player over
his head, walks to a marker beside his brother on the vanilla walk-off's own `CGoToAI`, the
two vanilla lines play, and then **three new ones** in which Fernand chides him for fishing
off the north island alone; then the vanilla walk to the ship. If Fernand is not alive, Juan
goes straight home.

**The timer is visible.** The bleed-out ran 45 silent seconds from the first approach; it now
says *"<His breathing is shallower. He has minutes, not hours.>"* at twenty if he is not yet
saved.

Needs a character who has not entered the Port District; Fernand's tree and the item name
work on any save.

## 0.9.1 - the areas around Barcelona

**Published.** A survey of the Wilderness maps that ring Barcelona -- Rio Ebro / the
River, the Crossroads, Darkwood, Scar Ravine, the Plains, the Lake, Cortez Cave, the Mongol Camp,
the Bounty Hunter Camp, the Woodcutter's forest and the coast -- for content that was written
and never reached. Two things came out of it. The rest of what the scan flagged was read and
is recorded here so it is not re-opened.

Measured against `data.dat.vanilla.bak` as this mod leaves the game:

```
python tools/reachability.py --survey "Wilderness" --with-mod
```

plus a map-side pass the dialogue survey cannot see: every level part that starts `Active=0`
and is never activated, cloned, relayed or force-generated by anything in the whole game. That
is where switched-off scenes live, and it is how 0.9.0 found the inn.

### The gate greets a goblin friend

The Mongol Camp's entrance polygon fires `1 Conversation Start Gob 1` -- *"Stand fast and be
recognized, knave!"* -- once (`Trigger Only Once=1`) and is silent for the rest of the game.
`3 Return Dialogue` -- *"Greetings goblin friend. What do you want?"* -- is written for the
player the guards let through, with the audience ask and the Darsh ask behind it, and nothing
opens it.

Now: two checkers on the map, `gate challenge given` and `welcomed at the gate`. The polygon
retriggers and branches on entry: welcomed -> `3 Return Dialogue`; not yet challenged -> the
vanilla challenge, marking the first checker; otherwise nothing, which is the vanilla silence
for a player who was challenged and neither welcomed nor fought. The four replies that get a
player past the gate -- Grumdjum's friend, the Horde's messenger, the Schmooze grin and the
Speech ask -- set the second checker. `Make Goblins Hostile Relay` already deactivates the
polygon, so a camp at war stays silent.

Node 3 needed three small things to be usable: its fight reply had no action at all (node 1's
same line fires the hostile relay; it does now), its Darsh reply is gated on the Darsh quest
being current exactly as node 1's is, and it had no way to leave -- every reply either went
hostile or to the Khan. It has a plain exit, *"Nothing today. I will be on my way."* -- one
authored line, flagged as such.

Needs a character who has not entered the Mongol Camp: the polygon and both checkers are level
parts, and a level's parts are captured into the save on first entry.

### Brendan Sullivan's clover

The Irish sailor at the Port District tavern bar has a node, `200 low luck`, that nothing
opens and that carries no reply: *"Forgive me, but I can't help but notice that you be a bit
down on yer luck, now, eh lad? Here, perhaps this will bring you some good fortune - it's
clover, plucked from the last patch of dry ground 'afore me island sank. <Whispers> Legend
says it be magic, so keep it safe..."* The clover exists only as an icon in the cache --
`Items/Inventory Images/Quest Items/Clover.mdl16`, a four-leaf clover on a stem, referenced by
no item, no tree and no map. And the requirement it needs, `Dialog/Requirements/Attributes/LK
1-3`, ships with zero users: a can for "Luck three or less" that the game built and never
asked.

Now: the drink he buys you (`200 drink`) splits its empty reply on `LK 1-3` -- low luck goes to
`200 low luck` (or `200 low luck lass` for a woman; one word changed, on the pattern of his own
gendered return greetings), everyone else goes where it always went. The low-luck node's new
empty reply gives the clover and rejoins his *"Grand. Now, what can I do fer ye?"* It sits
inside the one-time drink, so it is given once.

The item is `Quest Items/Clover.InventoryItem`: **Sullivan's Clover**, a neck-slot charm that
adds +1 to Luck, on the Amulet of the Prophet's envelope with the shipped
`CCharacterModifierAttribute` shape (the Sword of Kublai Khan and the Gauntlets of La Mancha
both carry +1 Luck the same way). **The effect is ours.** The line, the icon and the Luck test
are the game's; what the clover does was never written down, and a charm with no effect would
make his whisper a lie. Dialogue and a new item file, so it works on any save.

### Read and left alone

**Cortez Cave's undead boss.** Two `Undead Boss Generator` parts, `Active=0`, never targeted --
one named `undead to kill cortes`, one `undead boss`, ghouls and pre-Crypt skeletons with a
stand-up After Action, plus a `dragon eye glow` light. No dialogue, relay or quest mentions an
undead boss. The live scene at the same spot is complete and different: the pirate ghosts
guarding the treasure, `Spirits pissed off`, the `Crypt 2` generators from the secret cave,
Cortes leaving with his half. The undead pair is an earlier draft of the guardians. There is no
text behind it.

**The Plains' `Bishop is near player when the rogues are killed`.** Read by nobody; the only
mention is its own definition. The rogue / Diego scene around it is fully live on both sides,
including the dark one -- `20 ally` gives `Eliminate Bishop Diego`, `30 join` opens their store.
An unused flag, not a branch.

**The Lake's `Got Kill Dryad Quest from Mongol Camp Save Darsh`.** A real orphan, superseded.
Grumdjum's tree still carries a second way in -- *"Rakeb sent me. Tell me what I can do for
you."* and *"Darsh is worth the life of a Dryad. If this must be done, then so be it."* on three
nodes, all gated on `Grumdjun Have Darsh quest to kill Dryad`, which requires that relay to
exist. Nothing activates it. Rakeb's own tree shows why: his ransom node is still titled
`60 Returning after Dryad is killed` and his task node `50 Grumdjum`, but the text of both is
about the devil fish. The original price for Darsh was the dryad's head; the writers replaced
it with the vodyanoi task and left Grumdjum's three replies stranded. Restoring it would add a
dryad-kill route to the ransom that they deliberately took out, for three unvoiced player
lines with no NPC text behind them.

**`Bounty Hunter.DialogTree`'s `3 Return Dialogue`.** The whole tree is an earlier draft of
`Raylark.DialogTree` -- same opening, same Cristobal Suarez question -- and the map opens only
its four henchman barks. Raylark's own return greeting is live and richer.

**Cortes's four tavern nodes** (`5 cortes agrees to deliberation return`, `800 Return
Dialogue`, `15 Return Greeting`, `165 help with arm 2`). All drafts from before the argument
was split across two trees: `800`'s replies go to `50 more info`, `130 compromise` and `140 no
resolution`, none of which exist in his tree (they are Shylocke's, and live there). `15` /
`165` is Cortes offering the arm quest himself; the shipped route is DaVinci's `220 cortes`,
which is how the quest is actually given.

**`ShipSailorsonShipCanned`'s Irish nodes** are a draft copy of Brendan; the live one is `Bar
Patrons`, above. **Cervantes's `500 magic quill explanation`** is a draft copy of the Don
Quixote tree's `500 convince don quixote`, which the coast's `dispel don quixote` relay plays --
the Speech resolution is live. **The Woodcutter's A-1 through G greeting ladder** was cleared in
0.2.0 as superseded by the happy / angry / saved-daughter ladder and is still that. **The Bar
Patrons' `1500 converse with drunk`** (three replies, unreachable) is noted and not read.

**Act 8's orphans** -- the Khan's `500 Start in Persia`, Grumdjum's `300 companion` set, the
spirits' `1000 druid finale` -- surfaced again in this scan and are not near Barcelona. They
return with Act 8.

### Gates before this ships

- Gate 0: `tools/validate.py` clean; both nodes reachable under `--with-mod`; the map
  re-serialised canonically through `resource_format`.
- Gate 1: unplayed. Both pieces are small and additive; the gate one changes a polygon that
  vanilla fires once into one that fires on every entry, which is the thing to watch.

## 0.9.0 - the Temple District

**Published.** What follows is the scope as written, corrected in place as the reads and the playtest overturned it; the shipped shape is in "The honest recommendation" at the end. Every figure is measured against
`data.dat.vanilla.bak` **as this mod leaves the game**, not as it shipped:

```
python tools/reachability.py --survey "Temple District" --with-mod
```

The Temple District surveys at **40 trees, 738 nodes, 72 unreachable, 27 of them carrying
replies**. All 27 are triaged below.

**This district is not the Gate District.** The Gate District's remainder was greeting variants
and nodes that can never be fixed; 0.8.0 was a chore release and said so. Here the survey turns
up **a complete quest with a perk at the end that nobody can be given**, a cross-act
consequence branch with two opposite endings and no caller, and four faction- or race-gated
variants of the kind 0.3.0 and 0.7.0 built. 27 is a smaller number than 42 and a much larger
amount of content.

One correction recorded up front, because the first pass got it wrong. Three orphaned Montserrat
briefings turned up in one district and that looked like the Inquisition having no road north --
the exact shape 0.7.0 fixed for the Knights of Saladin. It is not. `Inquisition Foyer1.zax`
activates `Investigate the fate of Montserrat` from a live map trigger, and **five** live sources
put the abbey on the world map (Cedric Alsen, Lord Relican, Jafar, Lord Javier, and
`Crossroads.zax`). The Inquisition's road north works. What is orphaned is a set of *parallel
copies* in the Inquisition characters' own trees -- which makes several of them duplicates rather
than cut content, and is why they are in Tier 4 and not Tier 1.

### Tier 1 - the Inquisition's second task: half built, half impossible

**Scoped as the headline restoration. It split in two.** The Khan report is built and shipped;
the shadow dryad is out, because it is not unwired content -- it is *unfinished* content, and
finishing it would mean authoring. The reads that established this are below, in the order they
happened, because the order is the lesson.

`Purify the Shadow Dryad` is a complete three-state quest with its own `.Quest.txt`, XP, and a
**perk** on completion. Its states, verbatim:

| State | Text |
|---|---|
| `AM6C3B5E` | *"Grand Inquisitor Torquemada has asked you to perform a service for the Inquisition..."* |
| `S6JH3MKG` | *"To complete Grand Inquisitor Torquemada's task you must slay the shadow dryad..."* |
| `V3X8REJC` | *"Return to the Chambers of the Inquisition in Nueva Barcelona and tell the Grand Inquisitor..."* |

**Only `V3X8REJC` is ever set by anything reachable**, and by a map part rather than a
conversation: `Inquisition Chambers2.zax`, commented *"if this is active, PC killed Shadow Dryad
(Weird Woman) before encountering Torquemada"*. States 1 and 2 are set only by the orphaned
`411 shadow dryad 2`. So the quest can enter the journal only at its final step, and only for a
player who happened to kill her before ever meeting Torquemada. **It cannot be given.**

The obvious objection was checked, because two witch quest files exist.
`Find the Witch for Inquisitor Fournier` is fully live -- given by `MontailluInquisitor / 70
Tasks` and completed in five reachable places. It is a *different* quest: Fournier's local
errand in Montaillou. Torquemada's is a Barcelona-side arc with its own three states, its own
reward, and its own giver. Same target, different quest.

**And the way in is one faction check.** The Khan is Torquemada's first task -- content 0.1.0
already restored. On reporting the kill, every greeting routes the player to
`408 killed khan not inquisitor`. The node written for an Inquisitor reporting it,
`407 killed khan`, pays **150 gold**, asks *"Are you ready for another task?"*, and has no
parent at all.

| Node | Verdict | What it is |
|---|---|---|
| `407 killed khan` | **BUILT** | the Inquisitor's own Khan report, 150 gold |
| `401 already dead` | left orphaned | "I killed him before you asked" -- the only route to the dryad chain, deliberately not opened |
| `410 shadow dryad` | OUT | Na Roqua named, and Montaillou named |
| `411 shadow dryad 2` | OUT | sets the quest, or completes it if she is already dead, plus XP |
| `412 shadow dryad dead` | OUT | grants a **perk** |

Reachable for comparison: `405 kill khan` (the task), `408`/`409 killed khan not inquisitor`
(the outsider's report). A variant exists, is correct, and nothing selects it, while the
not-a-member version is what everyone gets. That is the 0.3.0 Saladin shape exactly, and the
fix is a faction-gated reply on the greetings that already offer the outsider's line.

#### What it actually takes -- read, not assumed

The scope first described this as a faction-gated reply plus four links. That was wrong, and the
read that corrected it is the most important one in this section.

**`Weird Woman dead` has no legitimate source. It is a debug switch.** The only thing in the
shipped game that sets it is a part named `warp`, `Active=0`, carrying the comment *"Weird woman
killer 1 - This is to kill the Weird woman to test what happens when you kill her"*, sitting
beside an `Editor/Test Interaction` that relocates the player to `Inquisition Foyer1`. No
Montaillou map references the flag under any spelling.

That cascades further than the flag itself:

- `411`'s second reply, *"I have already made arrangements"*, is gated on it, so it can **never
  fire**.
- That reply is the only thing that completes the quest and pays its XP.
- `412 shadow dryad dead` -- the **perk** -- is reachable only from that reply.

So wiring `410` -> `411` and stopping there yields a quest the player can accept and never
finish, with the perk still unreachable. The scope's original description would have shipped
exactly that.

The repair is visible in the shipped files, though. The third checker, `Torquemade requires
Shadow Dryad killed`, tests whether `V3X8REJC` is the current state and is **used by nobody** --
which is precisely the gate a report-back reply needs. So Tier 1 is three pieces, not one:

| Piece | Where | Outcome |
|---|---|---|
| faction-gated reply into `407` | `GrandInquisitor.DialogTree` | **BUILT** |
| a death hook that advances the quest to `V3X8REJC` | `06 Witch Interior.zax` | **impossible -- see below** |
| a report-back reply gated on the unused third checker | `GrandInquisitor.DialogTree` | out, with the hook |

The Khan's generator is the shipped precedent for a quest keyed to a death --
`CSetDestroyedScriptActionAction` in the generator's `After Action`, whose `CIfAction` advances
the quest state on the `Then` arm and, on the `Else`, reaches across the act boundary with
`COtherMapAction` to set a flag defined in a Barcelona map. That idiom is worth recording even
though this release cannot use it: it is how anything in a later act reports back to Torquemada.

#### Why the dryad half is out: she cannot be killed

The death hook has nothing to hook. Na Roqua is protected three independent ways:

| Layer | What it does |
|---|---|
| `Wierd Woman.can` | `Has Hit Points=0` |
| `Races/NPCs/Weird Woman.Race` | **AC 1000, HP 10000**, and full damage resistances across 11 presets |
| her generator's `After Action` | a `CHandleMessageAI` on **`Gotocombat`** that fires the `kicks you` relay |

`kicks you` is not a failure state. It plays SpellCast, spawns a teleport effect on the player,
has her say *"Away with you!"*, and relocates them to `01 Hamlet Exterior` -- and **the live
Fournier questline has shipped dialogue for exactly that outcome**: *"when I confronted her she
used her magic to send me to a den of wolves"*, *"when I confronted her she vanished."* Being
banished is a written beat. She is also never made a combat target anywhere in the game:
`CGoToCombatAction` naming her occurs zero times.

So `Weird Woman dead` has a debug switch as its only source because **there was never any other
way to set it**. `Purify the Shadow Dryad` was written, voiced, quest-filed and checker-copied
from the working Khan chain, and then blocked on a character built to be unkillable. Two halves
that never met.

Completing it would mean giving her hit points, removing or conditioning the banish, and
overriding a live scene -- authoring, and invasive authoring. Out.

**One correction to record, because it was stated confidently and was wrong.** `Has Hit Points=0`
does *not* mean invulnerable. Every shapeshifting daeva template carries it too, and that
creature fights and dies; its races carry HP 150 to 275. The flag is not what protects her -- her
race numbers and the banish relay are.

**A method error recorded, because it is the fourth of its kind.** This read first reported the
activation as living inside the `Grand Inquisitor generator`. It does not. The brace-walker
searched backwards for `Level Part=CEntityBase`, and the real parent is a `CEntityAnimated`, so
it walked straight past it into the previous sibling and attributed the action to the wrong
entity. The fix was to stop filtering and dump the region raw, at which point the `warp` comment
was the first thing visible. Same family as the wrong-baseline and absolute-count mistakes:
**when a structural query returns something surprising, print the bytes before believing the
parse.**

`407 killed khan` still ends on a question its one shipped reply does not answer -- *"Are you
ready for another task?"* -- and that is now permanent rather than pending, since the task it
would offer cannot be finished. `402 tasks 3` and `401 already dead` were deliberately left
untouched for the same reason: opening that pair is the only way into the dryad chain, and it
would hand the player a quest with no ending.

**Two dryads, and they are not the same person.** Worth settling explicitly, because the game
uses the word for both and one of them is famously live. The **River Dryad** is Wilderness
content: template `River Dryad.can`, race `River Dryad by Lake`, level 4, generated by
`Lake.zax`, with her own DialogTree, seventeen voice files and dedicated combat sounds. She is
the subject of two live quests -- `Slay the River Dryad for the Goblin Grumdjum`, and
`Rid the Dryad's Forest of the Goblins`, her counter-offer -- which is 0.1.0's territory. The
**Shadow Dryad** is Na Roqua, the Montaillou perfecti, and the phrase "shadow dryad" occurs in
exactly six files, all of them Barcelona. Nothing anywhere links the shadow dryad to the lake,
the river or the forest. The one sentence connecting the two vocabularies is the authors' own
comment in `Inquisition Chambers2.zax` -- *"PC killed Shadow Dryad (Weird Woman)"* -- which
identifies the shadow dryad as the Weird Woman, not as the River Dryad. Neither character is
cut; only Torquemada's quest about Na Roqua is.

Note also that neither is a tree-spirit: the River Dryad's model is `Woman Generic2`, a generic
townswoman. "Dryad" in this game is a label applied to a woman, which is worth knowing before
writing any new line that uses the word.

**And the evidence that this chain was finished is stronger than a normal restoration.** Two
things beyond the written dialogue:

- **All five orphaned nodes have shipped voice-over.** `401 already dead.ogg`,
  `407 killed khan.ogg`, `410 shadow dryad.ogg`, `411 shadow dryad 2.ogg` and
  `412 shadow dryad dead.ogg` are all present under `GrandInquisitor VOs/`. Voice actors
  recorded this and it shipped on the disc. It was lost at the wiring stage, not abandoned in
  writing -- the strongest class of evidence this project gets, and the same one that carried
  the Sacred Scimitar.
- **The gating is already built, and it is correct.** Three requirement checkers ship for this
  chain. `Torquemade requires Shadow Dryad NOT killed yet` wraps a `CCheckExistenceAction` on
  `Weird Woman dead` in a `CNotAction`; `Torquemada Requires Shadow Dryad Dead before meeting`
  is the same check unwrapped. Both are already wired onto `411 shadow dryad 2`'s two replies,
  so the out-of-order case is handled. The third, `Torquemade requires Shadow Dryad killed`,
  tests whether `V3X8REJC` is the current state -- exactly what a report-back reply needs -- and
  is **used by nobody**. Vanilla built the whole state machine and wired two thirds of it.

One false alarm recorded so it is not re-raised: the two existence checkers look identical under
a field-by-field dump and appear to be a bug where "NOT killed yet" tests "killed". They are not
identical -- one is wrapped in `CNotAction`. A selective dump that lists only leaf keys hides the
wrapper. Read such files whole; they are under 250 bytes.

#### Two design decisions, settled before building

**Use Na Roqua. Do not build a separate shadow dryad.** The alternative was considered
seriously, and its best arguments are real: a purpose-built creature would keep Torquemada out
of Act 3's most intricate live questline, and it would give the quest an actual fight, which
Na Roqua cannot -- `CGoToCombatAction` appears **zero** times in her tree and zero times in
`06 Witch Interior.zax`, so nothing in vanilla ever makes her hostile. It loses anyway, on five
counts:

- The authors said so, in a comment: *"PC killed Shadow Dryad (Weird Woman)"*.
- Both shipped checkers test `Name To Check For=Weird Woman dead`. Pointing the quest at an
  invented character means **rewriting shipped requirement files** -- overwriting the author's
  wiring and calling the result restored.
- `410` names her and her village: *"Na Roqua... lurks within the French village of Montaillou."*
- **No shadow dryad assets exist at all** -- no template, no race, no model, no creature voice.
  Compare the River Dryad: a template, a dedicated race, her own tree, five checkers, seventeen
  voice files. That is what a built dryad looks like here. The shadow dryad has three
  requirement files and three lines of Torquemada's voice: the fingerprint of a character who
  was always meant to be someone who already existed.
- She is *better* built than the River Dryad -- dedicated race (`Races/NPCs/Weird Woman`) and
  dedicated model (`Characters/NPC/Montaillou/Weird Woman`), where the River Dryad wears
  `Woman Generic2`, a generic townswoman.

And the reveal makes the name literally true: *"I am no longer Druj, the \*creature\* that your
spirit named. I am Na Roqua, and I have atoned for my past."* She really was a shadow creature.
A separate monster would not be redundant so much as destructive -- the weight of the quest is
that the thing you are sent to purify already purified itself.

**That decision is now partly superseded, and the reason matters.** It was made on the premise
that using her was *restoration* and a separate creature was *invention*. Once she turned out to
be unkillable, that premise died: there is no restoration available either way, so the choice is
no longer between restoring and inventing but between leaving the quest unfinished and finishing
it as declared new content. A separate creature is back on the table on those terms -- see
"The impostor" below. One objection from the list above does fall: the shipped checkers test a
flag *name*, `Weird Woman dead`, not an entity, so any creature's death could set it and both
checkers would keep working unmodified.

**Author no refusal reply. Torquemada would not accept the atonement, and the game already put
the refusal somewhere better.** The question was whether to add *"she has atoned; I will not"* to
`411`, whose only two shipped replies are *"I shall do it"* and *"I have already made
arrangements."* No, for four reasons drawn from the text:

- **His charge is present-tense teaching, not past creaturehood.** *"A wolf in sheep's clothing
  that is leading a flock astray"*; *"masquerading as a Cathar perfecti... spreading a perverted
  faith to unsuspecting people. **End her heresy.**"* Atonement for having been Druj is not a
  defence he rejects -- it is not responsive to the charge he actually makes.
- **She concedes his facts in her own dialogue.** *"Are you not lying to your flock by not
  telling the cathars of your past?"* -- *"Alas, the sins of the past chain me to this world...
  and I admit that I have not told the \*truth\* to those that look to me for guidance."* So
  "masquerading" is accurate and the accusation is not slander. Torquemada is factually correct
  on every particular; only his conclusion is monstrous. That is better writing than a villain
  who lies.
- **Mercy is absent from his vocabulary, measurably.** Across his fifty-node tree: "mercy" x0,
  "forgive" x0, "repent" x0, "atone" x0. Not a gap to fill -- the characterization. Compare the
  fire trial, where he watches a miracle and cannot tell it from damnation: *"is this a miracle
  or the work of demons?"*, *"I do not know whether divine providence or fiendish charms guard
  your body from the fire, so I will test your honor."* He resolves holiness by testing loyalty.
- **Refusal already exists and costs nothing.** Every declining reply in his tree lands on
  `10 Goodbye` -- *"I regret I cannot perform such a task, your grace."* No penalty, no
  follow-up. The player can decline, or take the task and never act on it.

The meaningful refusal is already written, live, and in the right mouth -- in her house, to her
face, as an Inquisitor. These are shipped reachable replies in `weirdwoman.DialogTree`:
*"Though I am an Inquisitor, I am willing to spare the Cathars"*, *"I promise no harm will come
to the Cathars by my hand"*, and hers in answer: *"Very well, I sense a \*truth\* in your
conviction... I will help you if you promise not to harm the cathars."*

**Which is the strongest argument for restoring Tier 1 exactly as shipped.** That promise is
currently free. A player can swear to spare the Cathars and nothing ever tests it, because
Torquemada never asks for her. Restoring the quest supplies the temptation the promise was
written to resist: a perk, XP and *"your deeds shall be transcribed in the Annals of the
Inquisition"* on one side; a woman who trusted you and a vow you made on the other. The half
that is missing is the pressure, and the pressure is the half that shipped voiced and unwired.

**Recorded as a knowing choice: this makes the mod darker.** A vanilla player cannot be asked to
do this. Restoring Tier 1 adds a rewarded path -- perk plus experience -- for killing a repentant
pacifist in her home, and the reward is framed as a blessing. That is the game's own moral
architecture and the Inquisition is written to be exactly like this, so it ships as found. It is
noted here rather than left implicit, because it is a real change in what the mod hands a player
and it should be a decision on the record rather than a side effect.

### One faction, one rank -- and Amir's replies on the wrong node

**Played, and it overturned a premise two releases were built on.** Amir offered no Montserrat
directions to a tester who had just won the Dream Djinni's trials. Two causes, one shallow and
one deep.

**The shallow one.** Amir's generator picks his greeting in this order: `passed trials` ->
`650 Favored one`; `passed on Dream Djinn` -> `600 ready to resume`; the initiation quest
current -> `230 knight of saladin`; otherwise `3 Return Dialogue`. 0.7.0 put both replies on
`3 Return Dialogue`, which a Favored One never sees again. Same shape as the Trapper fix on one
of seven copies: content on a node the player no longer reaches.

**The deep one.** The tester's saves, read in order:

| save | `Faction=` | rank attribute |
|---|---|---|
| before the trials | Inquisitor Acolyte | Inquisition Rank=1 |
| after the trials | **Saladin Aswaran** | Saladin Rank=1, **Inquisition gone** |
| after Raphael's promotion | Inquisitor Inquisitor | Inquisition Rank=1, **Saladin gone** |

A character holds one `Faction=`. `CAssignFactionToCharacterAction` replaces it, and the
`.Faction` record's `CPlugInBehaviorModifyCharacterWhenSelected` modifiers -- including the +1
rank -- are removed on deselection despite `Modification is permanent=1`. So `Saladin IS`
(Saladin Rank > 0) is true only while Saladin is the player's *current* order, 0.3.0's
"join Saladin alongside your order" was never possible, and the trials were silently defrocking
sworn Inquisitors and Templars -- and their next promotion was silently defrocking the Knight.
Vanilla knew: Cedric refuses Wielder initiation to anyone already sworn. 0.3.0 added no such
guard.

**Decision: gate Saladin content on being a Favored One, not on the faction.** That is
vanilla's own vocabulary -- `650 Favored one` is gated on `passed trials`, not on rank -- and the
Crescent perks survive faction changes, which the tester's save proves.

- `Dialog/Requirements/Faction/Saladin Favored` -- new canned expression: has Dervish OR Scholar
  of the Crescent. `CHasPerkExpression` is used bare in three vanilla `Custom Requirement`s and
  as an `Operand` fourteen times, so both positions are shipped idiom.
- Amir's two replies gate on it and now sit on `650 Favored one` as well as `3 Return Dialogue`.
- The Knight of Saladin's brother/sister greeting gates on it (map-side; fresh save).
- **The Djinni no longer defrocks.** Both `Saladin Aswaran` assignments are guarded on holding
  no order: `NOT Templar or Inquisitor`, `Wielder NOT`, `Goblin Horde NOT`. A sworn player keeps
  their order and gains the title; an unaffiliated one becomes a Knight of Saladin with the
  stat bonuses.

**Left rank-based on purpose**, because each of them would otherwise overwrite a real order:
the Ways Crystal promotes the order you currently hold; the Cathedral summit plays the scene for
the order that sent you north (its dispatcher reads the `if inquisition` / `if templar` /
`if wielder` event flags, with Saladin as the fall-through -- so the Saladin summit plays only
for a character who went north through Amir and nobody else); Amir's Blessed promotion stays
guarded on `Saladin Rank == 1`.

**Still open, and the saves cannot settle it:** whether same-family promotion accumulates
(Acolyte -> Inquisitor = rank 2) or replaces (= 1). Every `.Faction` says
`Allow Accumulation=1`, which reads as intent to stack, but the tester's path had Saladin in
between and cannot distinguish the cases. If promotion replaces, every `Mid Level` and
`Highlevel` check in the game is dead, including 0.7.0's Blessed/Exalted ladder. The next clean
data point is this character's promotion to Hallowed.

### The Cathar friend, and the cave that was not empty

Not in the original scope at all. It came out of the dryad investigation and is the better find.

`06 Witch Interior.zax` ships a part named **`cathar friend`**, `Active=0`, `Editor/Checker`, and
`weirdwoman.DialogTree` checks it -- and **nothing in the game ever activated it**. So
`100 Favorable Return`, the greeting written for that state (*"Welcome spiritbearer and Cathar
friend. What do you seek?"*), could never fire. Same shape as `Weird Woman dead`, with a happier
ending: this flag has somewhere legitimate to be set.

**BUILT.** The three promise replies -- including the Inquisitor's *"Though I am an Inquisitor, I
am willing to spare the Cathars"* -- now set `cathar friend` alongside the `heard node 50` they
already set, and the greeting ladder gained one arm. The arm is nested *inside* the existing
heard-50 branch rather than above it: sound, because the same replies set both flags so
`cathar friend` is a strict subset, and it kept the edit to a six-line re-indent instead of
shifting the whole ladder.

That reclaims `100 Favorable Return` and the two nodes behind it, and unlocks her admission about
the shapeshifter: *"It is true that **we once hunted together**. It preys on mortals and **takes
their forms** to strike again at the unsuspecting."*

**And it nearly shipped a trap.** `100 Shapeshifting Daeva 2` gives the same periapt advice as the
live `100 shapeshifting demon 2` and carries **no action**, where the live node fires a
`CTriggerRelayAction` on `shapeshifter ring` -- the relay that activates `secret cave entrance`,
activates `met the demon`, and plays her *"Step through the fire"* balloon. Restored as-is, the
informed path would have given advice and left the cave door shut while the ordinary phrasing of
the same question worked. Both its replies now fire the same relay, copied verbatim.

**A correction worth keeping, because it is the fourth of its kind.** This file previously said
her cave was empty and that the periapt would have to be authored. It is not empty: it holds a
`Chest 01 C`, `Active=1`, that generates the **Ring of the Prophet** -- one of the two Zarathustra
relics the shapeshifter's permanent-kill gate already tests for. The miss came from searching for
`Entity=` and `Inventory Item To Give=`; the chest uses `CGenerateInventoryItemAction` inside a
nested generator list, on a part whose `Name=` is blank. Nothing needed authoring. **Search by
what a thing does, not by the one key you expect it to use.**

For the record on duplication: the Amulet of the Prophet comes from Jafar/Amir plus containers in
`01 Hamlet Exterior.zax` and `Titan Village.zax`; the Ring comes from those two maps plus this
chest; and both kill gates accept either. Multiple relics in one playthrough is shipped design,
and this release adds no new source.

### The impostor - proposed, and openly new content

The only route left to finishing Torquemada's quest, and it is authoring, so it ships labelled as
such or not at all.

Druj is confirmed a daeva -- *"Druj, the daeva of lies"* (Nostradamus), *"Druj the Daeva of Lies
and Deception"* (the Beast, Demonic and Elemental Spirits, independently) -- and Druj is
**Na Roqua's own former name**, not a separate being. So the killable thing cannot be Druj. It
would be a different daeva wearing her face, which the game supports directly: Na Roqua herself
says the formless one *"preys on mortals and takes their forms"*, and Torquemada's own briefing
is second-hand -- *"we have heard **reports**"*.

What already exists to build on: the `Demon Shapeshifter` model with a full animation set, four
daeva races with real combat stats, a Trueform dialogue tree, the seven-daevas fiction, and -- as
of this release -- a live, signposted route to the Ring of the Prophet, which is exactly a
true-form reveal mechanism in the player's hands.

What would be new: the creature's placement, its dialogue, and the reveal scripting. Note the
shipped shapeshifter is **Nanghaithya**, *"one of the seven demons, he with a thousand faces"*,
whose questline is fully live through Iapetus in Toulouse -- so it is not a spare part and cannot
be reused as the impostor.

### Tier 2 - cheap and additive, one reply or one field each

**Five items** -- two fewer than first scoped; Sanchez's pair turned out to need a condition and
moved to Tier 3. None of these invents a condition; none removes a route.

1. **`SirAuric / 100 join tainted`** -- the Weng Choi shape. `100 join` is live with three
   parents; the tainted variant (*"I didn't think someone like you could have completed the
   task"*) has none, though Auric's tree handles tainted characters everywhere else
   (`1 Conversation Start Tainted`, `100 convince auric tainted`,
   `3 Return Hostile Tainted Did Not Use Speech`, all live). A tainted player earns the
   sponsorship and gets the generic acceptance. `105 join feralkin` is the same shape and
   carries no replies, so it is not one of the 27.
2. **`LordJavier / 190 need sponsor`** -- and it closes a loop. The join reply needs
   `Javier req spoke with Auric`; the direct route needs an entity named `second chance` to
   exist. A player with neither has **no join reply at all**. `190 need sponsor` is that
   missing branch -- *"you'll need a sponsor. Perhaps Sir Auric will do it. I have heard he is
   seeking an apprentice"* -- and its reply is *"I will seek out Auric,"* while Auric's live
   `100 join` ends *"go speak with Lord Javier."* Both ends written, entrance orphaned. Purely
   additive: it adds the explanation and the pointer and gates nothing.
3. **`Cervantes / 3 Return Dialogue`** -- the Farshad shape, fifth instance. All four of its
   replies lead to live nodes; the map opens `1 conversation start` and four scripted nodes but
   never the return greeting.
4. **`LordJavier / 500 Sacred Lance`** -- Jafar's identical lore node is live and Javier's is
   not. One "tell me about the Sacred Lance" reply; its own reply already feeds the live
   `238 Leave for Montserrat`.
5. **`ShylockeChests / 600 gold chest opened 2`** -- the middle line of the gold casket's verse.
   The map opens `600 gold chest opened` and `600 gold chest opened 3` and skips the one
   between, so the inscription is read with a line missing. Pure flavour, one field.
*(Sanchez's `100 faction let off inquisitor` and `100 low fine` were items 6 and 7 here. The
read moved them -- see Tier 3.)*

### Tier 3 - needs a map-side route or a condition, not just a link

**Nine items**, each real but each more than a value change.

1. **`Shylocke / 7 return with shakepeares money`** -- the payoff for the Shakespeare loan job,
   *"Here is your share of the gold, plus a bonus."* Needs a return route conditioned on having
   collected, which is map-side work.
2. **`Shylocke / 312 charge`** -- the hundred-gold asking price, with all four of its replies
   landing on live nodes (`315 barter charge`, `330 pay the price`, `400 threat`). Needs a
   parent in the 310 range.
3. **`Shylocke / 140 no resolution`** -- *"I shall take this matter to the magistrates and we
   will let the courts decide."* Reclaims `151 no resolution 2` with it.
4. **`Cervantes / 500 magic quill explanation`** -- the doppelganger reveal, *"I am real!
   Cervantes is the shade!"* Reclaims `500 don quixote attacks`. Needs the Don Quixote encounter
   located first.
5. **`InquisitorRaphael / 500 Return from Montaillou`** -- Jafar's equivalent is live; Raphael
   has no post-Montaillou reception. Reclaims `238 Leave for Montserrat` inside his tree.
6. **`LordJavier / 400 Esteban Slain`** -- reactivity to Sir Esteban's death, whose reply feeds
   the live `305 speak with auric 2`. Almost certainly wants a map relay fired on the death
   rather than a dialogue reply, which is why it is here and not Tier 2.
7. **`Machiavelli`, the whole consequence branch** -- see below. No longer held back for its
   own release; it now ships with Tier 1, for the reason given there.
8. **`Sanchez / 100 faction let off inquisitor`** -- *"Very well, your grace, I believe we can
   come to an understanding."* Faction-gated leniency on your fine.
9. **`Sanchez / 100 low fine`** -- the same for a persuasive rather than a well-connected player.

   Both were scoped as Tier 2 field fixes and are not. The fines are a **money ladder in the
   map**, not a dialogue branch: `Inquisition Chambers2.zax` tests `CHasMoneyAction` for 100,
   then 50, then 25, takes that amount, and only then opens the matching narration node
   (`100 high fine`, `100 medium fine`, `100 low cash fine`, then `100 no cash take item` which
   takes an item instead). Because the map takes the money *before* opening the node, a reduced
   fine is not a destination an existing arm can be repointed at -- it needs a **new arm** that
   tests Speech or faction and takes less. Note this lands in the same file as Tier 1's Barcelona
   work.

### Tier 4 - read before touching, all four plausibly superseded

Four candidates with the Cortes shape. The Tier 4 test from 0.8.0 applies: not *"does another
node do this?"* but *"does a **reachable** node do this?"*

- **`GrandInquisitor / 400 NIS Dialogue 4b`** -- a third copy of the summit's Montserrat
  briefing. Jafar's `400 NIS Dialogue 4b` is *also* an orphan and 0.7.0 correctly left it alone,
  because the live copy plays through Lord Javier. This is the Torquemada-side copy of the same
  scene. The one thing that could make it real: 0.7.0 built the summit with Javier and Jafar as
  speakers, so an Inquisition player's summit may want Torquemada. Read against the summit
  before deciding.
- **`InquisitorRaphael / 321 chapter 2 mission 2`** -- sets `Investigate the fate of Montserrat`,
  which `Inquisition Foyer1.zax` sets from a live map trigger. Very likely the dialogue version
  a map trigger replaced -- the Weng Choi scroll pattern.
- **`GrandInquisitor / 202 trial 2`** -- the middle step of the fire trial. `Inquisition
  Chambers2.zax` opens `203 trial 3` directly, so the map may be skipping step 2 deliberately.
- **`Machiavelli / 201 not helping`** -- its reply lands on `202 not helping 2`, which is live
  from elsewhere, so this is probably a superseded entry node into a branch that already works.

### Out now, with reasons

- **`Shylocke / 500 shylocke gets gold`** -- pays 500 gold, and the live `60 borrow money` and
  `61 borrow money tainted` already pay exactly that. Wiring it would add a second loan window.
- **`LordJavier / 500 pyrenees`** -- sets `Ensure safety of Monserrat Relics`, which his own
  live `400 NIS Montserrat Directions` already sets.

### Machiavelli, and why he now ships with Tier 1

Refuse to partner with him and he sells you out: *"you forced me to seek aid from those that
seek to do us harm. It turns out that you have a most formidable enemy, Lionheart."* Save him
and he repays you in Montaillou with **500 gold**. Both endings are written --
`230`/`231 ambush greeting if you don't help mach`, and `300 machiavelli helps you in
montaillou` with a `2` and a `3` behind it -- and **nothing calls either one**.

He is not on any Montaillou map. He exists as an entity only in `House of Ilk map.zax` (five
generators) and as a door and a relocate-target in `Temple District.zax`. So restoring this is
not a dialogue fix: it is a generator, a position, and a conditional greeting selection on a map
in another act -- the Cathedral summit's shape and roughly its size.

It is also the most interesting thing in the district after Tier 1, because it is a Barcelona
choice with an Act 3 consequence, in both directions.

**And that is now the argument for shipping it here rather than later.** The original plan held
it back for its own release, on the grounds that it needs a Montaillou map edit and Tier 1 did
not. Read 1 destroyed that distinction: Tier 1 needs a death hook in `06 Witch Interior.zax`, so
both items open `3 Montaillou`. Opening that act costs a tester a fresh character through two
acts every time, because a level's contents are captured into a save the first time it is
entered. Paying that once for two features is worth much more than paying it twice for one each.

### The dormant-check sweep, and a clean result

A pre-build sweep was run for the defect class that produced 0.7.0's Ways Crystal bug: **vanilla
logic that was unreachable in the shipped game because nobody could be a Knight of Saladin, and
which this mod made live in 0.3.0.** That is regression surface Fixt created rather than found,
and it went undetected for four releases, so it was worth measuring rather than assuming.

There are five such checks, across four files outside the ones this mod already edits. **All
five are correctly guarded.** Cedric Alsen's three form a proper mutually exclusive set:

| Checker | Selects |
|---|---|
| `Cedric Player IS Templar Inquisitor or Saladin` | *"Nevermind. I have already joined a faction."* -> `55 dismissal warning` |
| `Cedric Player is NOT Inquisitor Knight or Saladin` | *"I accept your challenge."* -> `70 first task` |
| `Cedric Player is Feralkin AND is NOT Inq Temp or Saladin` | the feralkin variant -> `70 first task` |

A Knight of Saladin is correctly turned away from the Wielder initiation. `Grumpy Port Guard`'s
two `Saladin IS` checks route to `41 Mistake End (Non Inquisition)`, also correct.

Two conclusions. **The worry is retired**: 0.3.0 did not switch on a pile of broken logic, it
switched on one unguarded branch, and 0.7.0 fixed that one. And this is **fresh evidence for the
Saladin thesis from an angle the project had not used** -- Cedric's author wrote `Saladin IS`
into a three-way faction test that could never be true in the game as shipped. Three separate
authors wrote for a faction that shipped unjoinable.

### Gates before this ships

- Both existing gates, unchanged.
- **Tier 1 spans two acts for real, not just in effect** -- the quest is given in Barcelona,
  resolved in Montaillou by a hook this release has to build, and reported in Barcelona. That
  round trip is the risk, not the dialogue.
- **This is the project's first edit to `3 Montaillou`**, and both Tier 1 and Machiavelli land
  there. Everything the 0.5 and 0.7 releases learned about scripted sequences failing in ways no
  static check catches applies with full force.
- **A save that has never entered the affected levels**, as always for map edits.
- Tier 1 wants a character who joins the Inquisition, and one who has *not* yet killed the
  Weird Woman, so the early-kill flag can be tested separately.

### The honest recommendation

**Shipped as: the Khan report, the Cathar friend chain, the Favored One gate (out early as
0.8.3), Machiavelli's inn scene, and four of Tier 2's five.** Tier 1's dryad half is out; the
gold casket was a superseded draft.

**What was played before it shipped, all on one tester's save:** the Cathar friend chain end to
end (TD4, TD5, TD7, TD8, TD9), and Machiavelli's refused branch through six passes to working
(TD11, TD11b). Those were the two Act 3 pieces and the two flagged as riskiest; they are the
two that are proven. The Khan report, Tier 2 and the saved branch are built and unplayed.

The original recommendation follows, kept for the record.

**Revised: 0.9.0 is the Khan report, the Cathar friend chain, Machiavelli, and Tier 2's five
cheap items.** Tier 1's dryad half is out, and the two items below replaced it.

**0.9.0 was originally scoped as Tier 1 complete, Machiavelli, and Tier 2's five cheap items.** That is a larger
release than this section first proposed, and the enlargement is a correction rather than
ambition: Tier 1 cannot be shipped as originally described, because doing so would hand the
player a quest with no ending and leave the perk unreachable.

The shape follows from read 1. Tier 1 needs an Act 3 death hook, Machiavelli needs an Act 3
generator, and a tester pays for opening Act 3 once either way -- so the two ship together. Tier
2's five items are cheap, additive Barcelona work that needs no new conditions and can ride
along.

Hold Tier 3 (now nine items, including Sanchez's money-ladder arm) and Tier 4 for 0.10.0.

**And the caveat that has now stood for three releases running.** 0.6.0 is unplayed past the
Juan rescue and 0.7.0 is entirely unplayed, including a change to a late-game promotion that
affects every faction combination. Tier 1 here would add a second Inquisition quest on top of
that untested pile. Playing what exists is still worth more than building more of it.

## 0.8.4 - repairs

**Published.** Repair only, cut on a branch from `v0.8.3`. The fish monger's hidden perk was
unreachable: only the normal-price sale counted. Bartered sales removed the skull without
counting, and once `vendor full of skulls` was set every later sale ran through the map relay
`determine vendor node after full` at ten gold, which 0.6.0 never touched -- a tester reached
"full" around the eighth skull. All ten sale replies now carry the normal sale's two-way split,
the after-full fifteenth doing the sale inline at the relay's own price rule. The tester's log
was the tell: "Received 10 gold" before each removal, a price the scripted sales never pay.

## 0.8.3 - repairs

**Published.** Repair only, cut on a branch from `v0.8.2`. The Amir / Favored One change -- see
the 0.9.0 section "One faction, one rank -- and Amir's replies on the wrong node" for the full
account. In short: Amir's Montserrat replies moved to the greeting a Favored One actually gets;
Saladin content gates on the Crescent title rather than the faction, because a character holds
one faction and the trials had been defrocking sworn players; the Djinni assigns Saladin Aswaran
only to a player with no order.

## 0.8.2 - repairs

**Published.** Repair only, cut on a branch from `v0.8.1`. Quinn's three reagent errands from
0.4.0, played for the first time, plus the drinkable draught decided after 0.8.1.

- **A `[TEST]` XP reply was live**, ungated, inherited from the very first mod. Removed.
- **Completed errands were re-offered**, and re-activated. The offer guard was
  `NOT CIsQuestStateTheCurrentStateAction`, which passes again the moment the quest completes.
  All three now gate on `NOT CWasQuestEverActivatedAction`.
- **Short turn-ins consumed the reagents and played the success text.** The reply's destination
  was unconditional and the remove-then-check chain removed a unit per step. Every failing arm
  now refunds exactly what its path removed -- computed by walking the parsed chain, since the
  quality-pelt tree makes refunds path-dependent -- and the reply lands on a neutral counting
  node whose empty replies are gated on `CIsQuestCompletedAction`. Gated empty replies are a
  shipped idiom (34 uses). The counting line and two refusals are new prose.
- **0.4.0's Trapper fix was on one of seven turn-in copies.** The quest-reply duplication
  convention means a fix applied to one copy is applied to one copy. All seven are now the
  quality-aware chain.
- **The reserve never opened.** Only that same one copy advanced `Quinn Reagents Delivered`. An
  Inquisitor's first greeting, and every return greeting, used the other six. Increments are on
  all seven now, and the reserve gates on completed-quest flags instead of the counter -- the
  errands are strictly sequential, so `completed(pelts)` / `completed(wasps)` /
  `completed(troll)` carry the same information and repair saves already at 0.
- **The draught is drinkable** -- see the 0.8.1 note.

A sweep of all 61 Fixt-added `CIsQuestStateTheCurrentStateAction` uses found no further misuse:
the four fixed this week (Fernand, the inn, Quinn's offers) were the only two positions where it
is wrong -- negated as a not-yet-offered guard, or as a did-this-happen test after a completion.
The rule is now in the modding skill.

## 0.8.1 - repairs

**Published.** Repair only, cut on a branch from `v0.8.0` so the unpublished 0.9.0 work on `main`
did not ship with it. Three fixes, each found by playing the feature it fixes, and each the same
class of defect: byte-correct on disk, green on every automated gate, wrong on a timing or state
detail only the running game shows.

- **The wrong bottle.** The Juan rescue checked for `Inventory Items/Potion`, the generic base,
  and the engine's inventory check has no addition filter -- exactly two fields across 653 vanilla
  uses -- so any potion satisfied it. Vanilla's own answer to "a specific potion" is a specific
  item can, so Fernand now gives `Potion Fernand Healing`, a quest item cloned from the
  Lycanthropy Cure that cannot be drunk, and the rescue checks for it by name. 0.8.1 shipped it
  undrinkable. **Decided after: drinkable.** On `main` the draught is now a real Extra Healing
  potion -- Potion Luck's envelope with the Extra Healing addition's drink behaviour copied
  verbatim -- so saving Juan costs a potion you could have used yourself. A player who drinks it
  cannot save him; that is the sacrifice, made real for the first time, since in 0.6.0 as shipped
  any other bottle would do. Shipped in 0.8.2.
- **Fernand forgets.** Reporting back completes the quest; a completed quest has no current
  state; the `told fernand juan lives` flag sat inside the JUA1LIVE test and was never consulted
  again. It is now the outermost test. A wrong theory is recorded in the commit -- that the 2.5s
  delayed block never fired -- disproved by the tester having seen the acknowledgment.
- **The troll that won the race.** Trolls spawn hostile and the keeper pacifies on a 2-second
  timer; a troll spawning beside the player in the far-left alcove can lock on inside that
  window, and no vanilla action releases a locked target. All 15 generators now pacify at spawn
  while the keeper is active, and both use vanilla's full stand-down idiom (target type *and*
  `CRemoveCategoryAction{Enemy}`).
- **The Helpful Wererat.** His tree's header was the writers' working title; now
  `Helpful Wererat`. He is on `Beggar enemy trigger`'s named list and his generator pings
  `Make unspawned beggar mad at player`, so he turns with the beggars whether already present or
  spawned into a hall turned from the other Sewers map.

## 0.8.0 - the Gate District remainder (scope)

**Built and unplayed. The scope is closed:** Tiers 1 to 3 are done and Tier 4 is ruled out
with evidence. The district has gone from **42 reply-carrying orphans to 34**, and the
remaining 34 are accounted for below -- none of them is a cut quest. Every figure is measured against
`data.dat.vanilla.bak` **as this mod leaves the game**, not as it shipped:

```
python tools/reachability.py --survey "Gate District" --with-mod
```

The Gate District surveys at **92 unreachable nodes, 42 of them carrying replies**, down
from 107/53 in the shipped game. What follows is all 42, triaged.

There is no cut quest left here. The district's one narrative find was the Knights of
Saladin and 0.7.0 spent it. What remains is greeting variants, four missing parent replies,
and a dozen nodes that can never be fixed at all -- so **42 is not a to-do list**, and this
is a chore release rather than another 0.7.0.

### Tier 1 - one field each, the Farshad shape

Two `CSeriesAction` pairs where the *return* slot points at the first-meeting node while a
dedicated return node sits unused. This is the third and fourth instance of the bug shape
0.3.0 found on Farshad.

| Map | Part | Now | Change to |
|---|---|---|---|
| `Gate District.zax` | `Temple Gate Guard 2` | opens `1 Conversation Start` **twice** | second entry -> `3 Conversation Start` (**9 replies**) |
| `Temple District.zax` | `Disturbed Citizen Generator` | opens `1 Conversation Start` twice | second entry -> `05 Return` |

Lowest risk on the list: one value each, no new parts, shipped text. Note the citizen fix
lands in **Temple District** -- the Gate District's own `Helpful Citizen` has no return slot
at all and is Tier 3.

### Tier 2 - a missing parent reply

Each is an orphan whose parent reply does not exist. One new player line each at most.

1. **`DaVinci / 320 gem is with inquisitor`** -- the item worth doing. It is the root of a
   live sub-branch, linking to `320 no to inquisition`, `320 oppose the inquisition` and
   `320 job reject`. **One entry reply reclaims three nodes** and restores a real choice
   about whether to cross the Inquisition for DaVinci's gem. The parent is `320 business 2`,
   which is reachable.
2. **`Goblin Sapper / 30 goblin name`** -- *"I am Hrubjub of the Goblin Horde, on a secret
   mission to serve my goblin lord."* No actions, exits to `40 combat threat` / `5 goodbye`.
   Needs a "who are you?" reply on his greeting. The cleanest item here.
3. **`Merchant Lope / 87 Perceptive` -> `87 Perceptive 2`** -- a two-node haggle ending in a
   discount (`CActivateAction` plus a merchant window). Needs a Perception-gated reply
   accusing him of overcharging. Two nodes for one reply.
4. ~~**`Merchant Lope / 60 beg from already`**~~ -- dropped, see above: eight parent nodes
   for a two-reply brush-off.

### What got built, and one scope error

**Tier 1, both.** `Gate District / Temple Gate Guard 2` now opens `3 Conversation Start` on
return, and `Temple District / Disturbed Citizen Generator` opens `05 Return`. One line
changed in each map, confirmed by `git diff --numstat` reading `1 1` for both.

A caution for anyone repeating this work: the citizen's series hangs off the **`Else=`** of a
`CIfAction` branching on whether he has heard the Cervantes rumour, not off an `Action=`. A
matcher looking only for `Action=CSeriesAction` finds nothing and reports the part as having
no conversation at all.

**Tier 2, three of four.**

- **`DaVinci / 320 gem is with inquisitor`** -- a reply on `320 business 2`, gated on
  `TN10C2WO`, *"Go to Inquisitor Fournier and retrieve the confiscated spirit gem"*, which is
  set by `05 Church Interior.zax` and by Guillaume's own tree. The gate is shipped, not
  invented. This reclaims the node plus `320 no to inquisition`, and is the only way into
  `320 oppose the inquisition` -- so one reply restores the choice of whether to steal from
  the Inquisition for DaVinci's gem. `320 progress` was the other candidate parent and is
  wrong: it is about Nostradamus, not the errand.
- **`Goblin Sapper / 30 goblin name`** -- one reply on `10 goblin`, the hub reachable from
  five places.
- **`Merchant Lope / 87 Perceptive`** -- the third way to stop him overcharging a tainted
  player. He activates `Lope normal` and opens the un-inflated inventory, exactly as
  `85 Threatened` (intimidation) and `86 Speech skill` (Barter 35) do; those two are each
  offered from the same three nodes and the Perception approach from none. Added to all three.
  **The threshold is a choice, not a discovery**: Lope's tree contains no Perception gates to
  mirror, so `Attributes/PE 7+` was picked because it is shipped and is the game's convention
  for seeing through a facade -- 14 uses, with lines like *"You might fool others, but I can
  see..."*. `PE 4+` reads too low for calling out a merchant; `PE 8+` has one use.

**Dropped: `Merchant Lope / 60 beg from already`.** The scope listed it as a Tier 2 item. It
is not one. `50 Beg from Human` and `51 Beg from NONHuman` are offered from **eight** separate
nodes, so gating a repeat-beg properly means eight variants for a two-reply brush-off.
Disproportionate, and better left than done badly.

**A scope error worth recording.** The Tier 1 entry for the guard was found with a regex over
a 2600-character window, which reported both series entries as opening `1 Conversation Start`.
That was right. But the same loose method was then used to *verify* the fix, against a file
that had already been written, and briefly produced the conclusion that vanilla had been
correct all along. Read the committed copy, not the working tree, when asking what a change
did.

### Tier 3 - built, and the premise was wrong

Scoped as "variant greetings that require a `CIfAction`... in scope only if the gating
condition turns out to be derivable from the files." Two of the three did not need a
condition derived at all, and the third was not a variant.

**`WengChoi / 03 Return Dialogue Special Customer` -- BUILT, and it was a one-value fix.**
His generator's greeting series has three entries: first meeting, plain return, and then a
`CIfAction` on `Gave Book to Weng Relay` **whose both arms open `03 Return Dialogue`**.
Vanilla built the branch, wired the correct checker, and pointed both outcomes at the same
node, so *"Welcome back spirit bearer, how can Weng Choi help one of his most valued
customers?"* could never fire. Only the `Then` destination was wrong. This is the same shape
as 0.7.0's Ways Crystal: a branch that collapses to a single outcome.

**`BarcelonaCitizenCan / 05 Return` for `Helpful Citizen` -- BUILT, and it reclaims nothing.**
Genuinely structural: the part opened `1 Conversation Start` through a bare
`CDisplayDialogTreeAction` with no return slot, so it became a two-entry `CSeriesAction`. But
Tier 1's Temple District fix had already made `05 Return` reachable, so no node is recovered
here. It is consistency polish -- Gate District citizens should not greet a returning player
as a stranger either -- and is recorded as such rather than as a repair.

**`Blacksmith / 6 Return Dialogue Wizard` -- NOT BUILT.** Its text is character-for-character
identical to `03 Return Dialogue 1, Insulted`: *"Eh...welcome back to Eduardo's Blacksmith
Shop. Perhaps you have forgiven me for my earlier insult?"* The map already selects `Insulted`
through the live `Blacksmith has insulted player in dialog` checker. A duplicate with a
misleading name, not a third variant -- the Cortes verdict, and the fourth time that shape has
appeared in this project.

One false alarm worth recording, because it looked serious for a minute. `6 Return Dialogue
Wizard` carries a reply gated on `The Red Ore Trade / TRD4K8ZM` -- a **Fixt** quest state, in
Fixt's own mnemonic ID style -- which suggested an earlier release had spliced content into an
orphaned node and broken its own feature. It had not: `790 the troll terms` is reachable from
**nine** nodes including both live return dialogues. An earlier release simply added that reply
to every greeting variant, orphan included.

### Tier 4 - read, and both ruled OUT

Both were suspected superseded drafts and both are. The test that settled it is worth stating,
because two earlier passes at it gave the wrong answer: the question is not "does another node
pay this?" but **"does a *reachable* node pay this?"** Attribute every payout to its owning
node, then split by reachability.

**`Blacksmith / 80 Do You Have The Item I Need?` -- OUT.** It completes two quests and pays two
XP awards, and *every one of those payouts is already made by reachable nodes*:
`03 Return Dialogue 1 Normal`, `07 what more`, `08 No Discount Yet`, `09 Discount Given`,
`100 Is Business Good`, `21 Problem Demokin 2`, and all five race introductions. Nothing is
unique to node 80. Wiring it would not restore content; it would add a second way to be paid
for the Felgnash sword and the Estral silver.

An intermediate pass wrongly concluded the opposite, by comparing node 80 against four
hand-picked live nodes rather than the whole tree. The Blacksmith tree completes the Felgnash
quest in **44** places; picking four of them proves nothing.

**`WengChoi / 570 scroll give` -> `600 something else` -- OUT.** `570` is the dialogue version of
buying the Wind Scroll: `CTakeMoneyAction` plus a hand-over. The shipped game sells it through
the shop instead -- `550 Wind Scroll`'s reply opens **`Special Inventory for Weng Choi`**, which
**stocks `Scroll Wind`**, and then checks whether the player now holds it and triggers
`Swap Special Merchant AI`. So the purchase is fully live and `570` is the superseded original.
`600 something else` goes with it: its nine book XP awards are all paid by reachable nodes
(`03 Return Dialogue`, `55 collection`, `110 become special customer`, `115 Good Barter`,
`200 show special stock`).

That makes **five** superseded drafts this project has now identified and correctly left alone
-- Cortes's arm, Bartolome's boots, the Blacksmith's Wizard greeting, and these two.

### Explicitly not in it

**DaVinci's starting gift** (`500 davinci gives a gift to help you get started`, male and
female). An earlier note in this file called it appealing. It has **no actions at all**: the
line says *"I have something for you"* and nothing is given. Restoring it faithfully means
choosing an item, which is authoring rather than restoration. Out unless it is taken up
deliberately as new content.

**`DaVinci / 320 general surly response 3`** and **`340 return spirit`** -- the third surly
escalation, and a spirit turn-in paying XP and gold. Both plausible; neither has a gating
condition derivable from the files, so wiring them would be guessing.

**Twelve nodes that can never be fixed.** Three whole trees no map opens anywhere --
`barcelonavendor` (3), `Barcelona Vendor Sympathetic2` (3) and `KnightSaladincanned2` (4,
including two *"Welcome, brother/sister, into the Order of Saladin"* greetings) -- plus two
nodes the authors named `10 Don't use this node`. These are the Irish-sailor pattern: spare
copies nobody wired. They will show as orphans forever.

**The six `dreamdjinn` orphans** (`90 Moral Test`, `400 riddle combat`, the failure
branches) are 0.3.0 territory and the trials demonstrably work -- these read as alternate
trial variants the game chooses between. Plus two one-line flavour barks,
`Magic Machine / 500 nothing happens` and `Viola Organista / 40 broken key`.

**`Jafar / 400 NIS Start` and `400 NIS Dialogue 4b`** -- duplicates whose live copies now
play through Lord Javier in the summit. Correctly left alone; they will always survey as
orphans.

### Gates before this ships

- Both existing gates, unchanged.
- **Two of these fixes land outside the Gate District** -- the citizen in Temple District,
  and DaVinci's tree is shared with Montaillou content. The blast radius is wider than the
  section title suggests.
- **A save that has never entered the affected levels**, as always for map edits.

### The honest recommendation

Seven items built, **eight reply-carrying nodes reclaimed** (42 -> 34), the DaVinci gem branch
as the headline. Two of the three Tier 3 items turned out to be one-value fixes rather than the
conditional work the scope predicted; the third was a duplicate. Tier 4 ended in "out" twice,
as expected.

**The Gate District is finished.** What remains of its 34 orphans is: twelve nodes in dead trees
and author-labelled corpses that can never be fixed, six deliberate `dreamdjinn` trial variants,
five superseded drafts, two duplicates left by 0.7.0's own summit work, two flavour barks, and
the DaVinci gift and surly/spirit nodes that would need invented conditions. There is no cut
quest left here and no further list to work through.

A lesson from Tier 3 worth carrying: **assert deltas, not absolute counts.** Two attempts at
verifying the citizen change failed on `count(...) == 1` because vanilla's Gate District
already opens an `05 Return` on a *different* tree, `BarcelonaCitizenCan Gate Beg`, in
`Person to beg from Generator`. An absolute count cannot tell "my change worked" from "the
name occurs elsewhere".

**This is still stacked on unplayed work.** 0.7.0 is entirely unplayed and 0.6.0 is unplayed
past the rescue, one of them having changed a late-game promotion for every faction
combination. Nothing here is urgent: the remaining items are greeting variants and two reads.
Playing what exists is worth more than the rest of this list.

## 0.7.0 - the road north

**Built and unplayed.** Every figure is measured against `data.dat.vanilla.bak`.

0.3.0 got the player *into* the Knights of Saladin. This gets them out again: the order
could be joined and never served, and Amir had the whole speech for sending you to
Montserrat without the one action that makes it possible.

### The order is a peer, and the game says so

Three patrons send the player to Montserrat, each in ordinary conversation, each revealing
the abbey on the world map: **Lord Javier** (Templar/Inquisition), **Cedric Alsen** (the
druids) and **Lord Relican** (the Wielders). Cedric ships requirement files for the
*unaffiliated* player too, so joining anyone is a choice rather than a gate.

The game already treats Saladin as a fourth peer. `Cedric Player IS Templar Inquisitor or
Saladin.can` is a shipped requirement testing whether you already serve one of the orders,
and Saladin is in the list. `Saladin IS` is checked in **Acts 1, 3, 4 and 7** -- the same
span as `Templar IS`, at lower density (20 uses against 46).

### What was broken: one missing action

Amir's directions node says, in the shipped text:

> *"Montserrat Abbey lies some fifty miles to the northeast. **I shall mark the path on
> your map.** You must travel with all speed to Montserrat..."*

It sets the quest state and contains **no `CEnablePointOfInterestOnWorldMapAction`**. All
three other patrons have one. That single omission is why the Saladin route dead-ends, and
adding it is a repair the line itself demands rather than an invention.

### The build

| | |
|---|---|
| `400 NIS Montserrat Directions` | now marks Montserrat on the world map, alongside the quest state it already set |
| `3 Return Dialogue` | two gated replies, both behind `Dialog/Requirements/Faction/Saladin IS` |

That reclaims **seven nodes**, all of them shipped text, none of it altered:
`400 NIS Dialogue 4a`, `400 crown of thorns`, `400 relics explanation`,
`400 NIS Montserrat Directions`, `238 Leave for Montserrat`,
`500 Return from Montaillou`, `500 Sacred Lance`. The Gate District's still-cut count falls
from **102 unreachable / 51 carrying replies** to **95 / 45**.

`400 NIS Dialogue 4a` is genuinely Amir's and exists nowhere else -- *"an unidentified
group attempted to steal the True Cross from **our** possession"*. Most of the summit
chain is not: Jafar's `400 NIS Start`, `Montserrat Directions`, `crown of thorns` and
`relics explanation` are character-for-character copies of Lord Javier's, because the scene
was duplicated into every participant's tree. That duplication is what made this look like
a superseded draft on first reading.

**No new quest state was needed.** The other factions' report-back states (`FX3UY821`
Javier, `V8439DKP` Raphael, `XQX0TUT7` Cedric) are alternatives to one another; the step
that actually advances the story is Brother Montgomerie's `SAXRA7U2`, which every route
shares. Saladin simply uses the shared one.

### The two new lines, and why there are any

Everything Amir says is his own. Two **player** replies are new:

- *"What troubles the Order, Amir?"* -> `400 NIS Dialogue 4a`
- *"I have returned from Montserrat."* -> `500 Return from Montaillou`

They exist because the chain's only authored entry is `400 next duty` -- *"The Knights
Templar have requested an audience... accompany me to the Cathedral"* -- which relocates
the player and belongs to the summit variant below. A conversation route needs a way in,
and there was none.

### The rank ladder, and a bug 0.3.0 had made live

The order could be joined at one rank and never rise. `Saladin Blessed` and
`Saladin Exalted` are fully authored faction records that vanilla assigns in exactly one
place: `Levels/Test Maps/James/James.zax`, a developer test map.

**How the Templars do it** was the only precedent worth copying, and it is three different
mechanisms:

| Tier | Awarded by | Earned by |
|---|---|---|
| Squire | node `210 give gold` | paying the tithe |
| Warden | node `450 made a knight` | a dedicated knighting, after Esteban's tasks |
| Paladin | the **Ways Crystal** | a world object in Act 7 and Act 8 |

Join, serve, be knighted, and a late-game relic crowns you. So:

| Tier | Awarded by |
|---|---|
| Aswaran | the Dream Djinni trials -- 0.3.0, unchanged |
| **Blessed** | reporting back to Amir from Montserrat, which 0.7.0 made reachable |
| **Exalted** | the Ways Crystal, a new fourth arm |

**The ranks are increments, not alternatives.** Each record grants `+1 Rank`, permanent,
with `Allow Accumulation=1`, so the ladder only reads 1 -> 2 -> 3 if the player holds all
three -- which is why `Saladin Highlevel` tests rank **> 2**, and why Blessed's stat line
looks smaller than Aswaran's in isolation. The totals are the largest melee numbers in the
game:

| | Aswaran | Blessed | Exalted | total |
|---|---|---|---|---|
| One-Handed Melee | +10 | +6 | +13 | **+29** |
| Two-Handed Melee | +10 | +6 | +13 | **+29** |
| Carry Weight | +20 | +10 | +20 | **+50** |
| Endurance | +1 | - | +2 | **+3** |
| Turn Undead | - | - | +12 | **+12** |
| Crushing / Slashing % | - | - | +5 / +5 | **+5 / +5** |

Templar by comparison is 4/8/12 across *three* weapon skills including Ranged, plus +5 HP
a tier and HealingRate; Wielder is elemental damage, AC and Intelligence. Saladin is the
pure melee specialist, and Turn Undead +12 at the top appears in no other ladder.

#### The bug

Both crystals -- Act 7 `09 Secret Chamber` and Act 8 `02 Shifting Dunes`, byte-identical in
the relevant block -- branch like this, read by walking braces rather than by proximity:

```
if   Inquisitor IS  ->  Inquisitor Hallowed
elif Templar IS     ->  Templar Paladin
else                ->  Wielder Wizard        <- unguarded
```

Anyone who is neither Inquisitor nor Templar is made a **Wielder Wizard**. In vanilla a
Knight of Saladin cannot exist, so that case was dormant -- **and 0.3.0 made it live.**
Since then, Fixt has been converting Saladin knights into Wielders when they touch the
crystal in Act 7. The crystal's balloon is generic (`Find All 5 Green Crystals`), so no new
words were needed to fix it -- but a single extra arm turned out not to be enough either,
for the reason below.

This is the fourth instance of one shape: a faction branch with three arms and a missing
fourth. `Choose NIS Player` in the Cathedral has the same gap.

#### The orders are not exclusive, so the crystal now honours all of them

**CORRECTED BY PLAY -- see the 0.9.0 section "One faction, one rank". The paragraph below is
wrong.** A character holds one `Faction=` and one live rank; assigning another faction replaces
it and removes the old rank, "permanent" or not. A tester's saves showed the Djinni trials
replacing Inquisitor Acolyte with Saladin Aswaran (Inquisition rank gone), and Raphael's
promotion then replacing Saladin (Saladin rank gone). The four-arm crystal below still behaves
acceptably, by accident: only one rank is ever above zero, so only one arm fires.

Adding a fourth arm to the chain was not enough, and the reason is worth recording:
**faction membership is not exclusive.** None of the four joins -- Templar Squire,
Inquisitor Acolyte, Wielder Conjurer, Saladin Aswaran -- is gated on already serving
someone. Nothing outside `James.zax` ever clears a faction. And the rank modifiers are
`Modification is permanent=1`, so once a rank is above zero it stays there for the rest of
the game. Javier and Raphael at least test for each other and for Wielders; **Amir tests
for nobody.**

So a player can be a Knight Templar *and* a Knight of Saladin, and vanilla's if/elif chain
grants only the first match -- which left the restored Saladin arm dead for exactly the
players most likely to have it, since the djinni trials are an optional side questline that
a Templar can happily complete.

The chain is now four **independent** arms, the side order first and the main allegiance
awarded in addition rather than instead:

```
if Saladin IS                     ->  Saladin Exalted
if Inquisitor IS                  ->  Inquisitor Hallowed
if Templar IS                     ->  Templar Paladin
if Wielder IS OR no order at all  ->  Wielder Wizard
```

Every match fires, so the order does not decide who gets what; it states the intent. The
fourth arm tests `Wielder IS` **as well as** the no-order case, which the first sketch of
this did not: without it, a Wielder who had also done the djinni trials would have lost the
Wizard grant they get today, because the Saladin arm would have claimed them. Nothing is
taken away from anyone.

By membership, against what the game does today:

| Serves | Gets | Change |
|---|---|---|
| nobody | Wizard | unchanged -- vanilla's freebie for the unaffiliated, kept deliberately |
| Inquisition | Hallowed | unchanged |
| Templars | Paladin | unchanged |
| Wielders | Wizard | unchanged |
| Templars + Wielders | Paladin + Wizard | gains Wizard |
| Saladin | Exalted | gains Exalted -- was silently made a Wielder |
| Templars + Saladin | Paladin + Exalted | gains Exalted |

The unaffiliated freebie is still left in place on purpose. Guarding it away would be
defensible, but it takes a bonus off unaffiliated playthroughs, which is a balance change
rather than a repair.

#### How Blessed is kept to one grant

By testing the rank itself -- `Saladin Rank == 1` -- rather than a checker entity or
`COnlyOnceAction`, whose state persistence for a dialogue action is unproven. The modifier
is permanent and accumulating, so an unguarded grant would stack on every revisit. The test
sits on the **action**, not the reply, so the reply still works at rank 2 and the player is
never stranded in the conversation.

### The Cathedral summit: three deleted parts whose callers survived

This is the strongest evidence of cut content the project has found, and it was nearly
missed. `Church Interior.zax` references **three relays that do not exist**, and all three
call sites are live in the shipped map:

| Caller | Calls | Exists? |
|---|---|---|
| a `warp` with `Comment=start NIS` | `Saladin NIS Relay` | no |
| **`Lord Javier generator`** | `Start Saladin NIS Conversation` | no |
| **`determine ending relay`** | `End Saladin NIS Relay` | no |

The variant was deleted and nobody cleaned up its callers. Better still, both surviving
dispatchers carry a **complete four-way chain with Saladin as the else**:

```
Lord Javier generator : if inquisition / if wielder / if dark wielder / if templar
                        else -> Start Saladin NIS Conversation
determine ending relay: if dark wielder / if wielder / if inquisition / if templar
                        else -> End Saladin NIS Relay
```

So the original design is legible: **serve no other order and you are at that table as a
Knight of Saladin.** `Choose NIS Player` is the odd one out -- it has no `if templar` test
and defaults to the Templar relay, exactly the shape you get by collapsing a deleted final
arm. It is restored to match its siblings, which also fixes a live vanilla defect: a player
who is none of Inquisition, Wielder or Templar currently reaches two parts that do not
exist, so the summit has no conversation driver and no ending for them.

Two of the three part names were written before any of this was known, by following the
Templar naming convention. They matched the names the map already expected, character for
character -- which is what the original authors had done too.

#### Amir was switched on, not added

`Jafar Generator Wielder NIS` is a complete, positioned, dialogue-wired Knight of Saladin
named Jafar at (788,1000), beside the summit's own spawn point. It is `Active=0` and
**referenced by nothing in the entire map**, so Amir appears in no variant of the scene --
including the one the generator is named for. The new relay simply activates it. No
character template, no new spawn point: the relocate reuses `Start Player NIS TEMPLAR`, the
same framing of the same room.

#### The scene

```
Lord Javier   400 NIS Start          "Amir, we are honored that you and the
                                      Knights of Saladin are with us..."
Amir          400 NIS Dialogue 2     "As Saladin stood with Richard centuries ago,
                                      we now stand with our western brothers..."
Amir          400 NIS Dialogue 2b    "As living proof of this bond, I have brought
                                      the scion of Lionheart, who has recently joined"
Lord Javier   400 NIS Dialogue 4a    the True Cross, and the three replies
Amir          238 Leave for Montserrat  "May the Prophet guide you."
```

Only `2` and `2b` are uniquely Amir's. `400 NIS Start` is Javier's welcome *to* him and
exists on both trees. **`4a` is Cathedral-side, not Amir's** -- an earlier draft of these
notes had it the other way round. The True Cross rests in the Cathedral (the Knight Guard,
Javier and Raphael all say so), so "from our possession" is Javier's line; it survives only
in Jafar's copy of the scene and is restored by showing it with Javier as speaker.

The interactive tail deliberately runs in **Jafar's** tree so its replies reach Jafar's
`Montserrat Directions`, which sets the Saladin quest state and marks the map. Javier's
identical copy would set the Templar quest instead.

#### What this replaced

The direct reply added earlier in this release -- *"What troubles the Order, Amir?"* going
straight to the briefing -- now leads to `400 next duty`, Amir's authored summons: *"The
Knights Templar have requested an audience with us... accompany me to the Cathedral."* Its
`CRelocateAction` lands on `Start Player NIS Here`, which is one of the things that triggers
`Choose NIS Player`, so the summons needed no new wiring at all. Reverting to the shortcut
is a one-line change if the scene misbehaves in play.

One consequence worth stating: a player who is **also** a Templar or Inquisitor gets their
own variant rather than the Saladin one, because Saladin is the else. That is vanilla's own
logic in the two surviving dispatchers, not a choice made here.

### Explicitly not in it

**Promotion dialogue.** The ranks themselves are now restored (see above), but there is
still no line in which anyone *says* you have been promoted. A search of every dialogue tree
for any mention of rising in the order -- Aswaran, Blessed, Exalted, promotion, elevation --
returns five hits and **none of them Saladin**. Amir hands over Blessed silently, and the
crystal shows its generic balloon. Writing promotion speeches is authoring, not restoring,
so it is left undone; and nothing is gated on the higher ranks in any case, since
`Saladin Highlevel.can` is used **zero** times. The ranks are a stat reward for service,
not a key to new content.

**The Cathedral summit is now in** -- see above. It turned out not to be a new cutscene
at all but three deleted parts whose callers are still live in the map. Correcting an
earlier claim in these notes: `MX_FACT_KNIGHTSALADIN1/2.ogg` are **not** unused -- all three
uses are in `Dream Djinni Map.zax`, the trials. The track is the order's music, not orphaned
summit music, and it is reused here rather than restored.

### What to play

Needs a character who joins the Knights of Saladin -- the Dream Djinni trials, which
0.3.0 made completable.

1. Complete the initiation, then talk to Amir. *"What troubles the Order, Amir?"* should
   appear, and only for a member.
2. Take his directions. **Montserrat should appear on the world map** -- this is the whole
   release in one check.
3. Confirm the reply disappears once the quest is taken.
4. Go north, learn about Montaillou, come back. *"I have returned from Montserrat."*
   should appear and Amir should send you on with the Sacred Lance explanation.
5. Confirm a non-member sees neither reply.

## 0.6.0 - the Port District

**The Fernand quest is built and unplayed. The rest of the section is still scope.**
Every figure is measured against `data.dat.vanilla.bak` and is reproducible from the
scripts described under "how this was found".

The Sewers work closed with the thieves and the beggars roughly level. The Port District
is the next-largest cluster of Barcelona content, and it holds **the game's fourth
companion** - written, wired on both the dialogue and the map side, and reachable by
nothing.

### How this was found

Reachability, per tree: walk `Go to node ID` outward from every entry point and report
what is never visited. Entry points are the first node in the file, plus any node named
by a `Dialog Tree File=` / `Node ID=` pair anywhere in the shipped game. Both of those
fields sit in the same brace block **in either order**, so the block has to be delimited
properly rather than scanned forwards a fixed distance - a forward-only scan misses
entries and reports live balloons as orphans.

Across the district's **31 trees that is 111 unreachable nodes**, and most of them are
balloons and combat barks that a map fires directly. Sorting by "carries replies" cuts it
to **38**, which is where authored branches live. Two of those branches are cut content.
The rest are barks, superseded drafts, or one-line flavour.

Reproduce with:

```
python tools/reachability.py --survey "Port District"
```

That is `tools/reachability.py`, promoted out of scratch while this was being written -
which immediately corrected two figures in an earlier draft of this section. The
district has 31 trees, not 30: `Character Templates/Port District/Maria.DialogTree` sits
outside the `Dialog/` folder and a folder glob misses it.

### Fernand Desoto is a finished companion

`Distressed Sailor.DialogTree` - header `Name=Fernand Desoto` - is 31 nodes, **17 of them
unreachable**, and the unreachable half is the entire success branch.

Node `80 companion` runs a real
`CSetCompanionAction{Player=$Instigator, Companion=Distressed Sailor}`. That is the same
call that makes Cervantes, Cortes and Fang follow you, and those three are the only
companions in the shipped game. The map side is finished too: `Port District.zax` carries
a 14KB relay named `fernand joins you` that strips his `CSkeletonAI` and adds a
follow-capable one, swaps his `CAIInteractionSpecifier`, and gives him companion banter
through `100 companion banter` - *"Where you go, I follow."*

Nothing fires any of it. `1 return after saving juan`, the node the whole branch hangs
off, is **defined once and referenced nowhere in the game**. It offers six replies:

| Reply | Gate | Goes to | Pays |
|---|---|---|---|
| "I would like you to accompany me for a time." | none | `40 companion` | the companion |
| "don't you think his life is worth more than I was paid?" | Barter 20 | `40 hard barter` | chain mail, an Extra Healing potion, 100 gold |
| "I have great need of gold." | Barter 20 | `40 barter` | 100 gold |
| "Tell me about yourself." | none | `50 who are you` | - |
| two exits | none | - | - |

`40 companion` then gates the recruitment on **Speech 20 or Barter 20**, with a written
refusal (`70 rejection`) for anyone who has neither. Both routes reach `80 companion`.

### Why it is unreachable: Juan cannot be saved

The only Juan on the map is a `Fixed Dead Body Generator` at (5293,221) - a
`CSimpleGeneratorForCannedEntitiesAI` over `ShipSailorsonShipCanned`, `New Name=Juan`,
dropping leather armour and a club. The `sailor rescues brother` proximity trigger at
(5275,242) **unconditionally** plays `Sailor Juan / 100 dead` (*"you notice that it has
been very recently killed"*) and sets the quest to `VMS91BAX`.

`help distressed sailor.Quest.txt` ships with exactly two states and **neither is a
success state**:

- `S1NPX04I` - "Search the coast for Fernand's missing brother and see if it is possible
  to save him."
- `VMS91BAX` - "Return to Fernand and tell him that unfortunately, his brother perished."

You get 150 XP for reporting a death, and that is the whole quest as shipped.

But the rescue was written:

- `Sailor Juan.DialogTree` - *"Mi hermano! You saved me!"*, `1 Juan lives thanks you`, and
  male and female thanks nodes. **Three of its five nodes are unreachable.**
- Fernand's `20 still breathing`, `20 not breathing`, `30 saved juan`.
- Map position markers named for Juan - `juan heads to ship` (4639,1354),
  `juan travels back` (4345,1483), `juan travels back further` (4176,1703) - tracing a
  route from the island back to the ship. **These are not unused**, and an earlier draft
  of this section wrongly said nothing sends anyone to them: `sailor leaves` walks
  *Fernand* down all three, plus `sailor runs to help` and `distressed sailor goes here`,
  when the quest ends badly. Each of the five is referenced exactly once, by that one
  relay. That they carry Juan's name while moving his brother suggests the route was laid
  out for Juan and reused - but that is inference, not evidence, and it is weaker support
  for "the rescue was written" than the dialogue and the unused requirement are.
- The fight is there too: three `Vodyanoi agile Generator`s at (4967,231), (4987,549) and
  (5232,226), straight across the approach to the body.

### The intended mechanic is identifiable

When you take the job, node `30 take the job` hands you a healing potion: *"Take this
potion of healing, you might need it against those creatures."*

And `Dialog/Port District/Requirements/Player has a potion of healing.can` exists, checks
`CActionCheckForInventoryItem` against `Inventory Items/Potion`, and is **referenced by
nothing in the game**. It is one of four unused requirement files in the district.

Reach Juan with the potion still on you and he lives. That is the design, and it wants
wiring rather than authoring.

### The build

1. **A success state.** Add one to `help distressed sailor.Quest.txt` - "Return to
   Fernand and tell him his brother lives." Note this would be **the first shipped
   `.Quest.txt` Fixt edits**; all eight quest files it currently ships are new ones. The
   shape is an `Item Count=N` array of `State=` entries, which is the same edit made
   routinely inside `.zax`, so the risk is low - but it is a new file class and gets its
   own validator check and a first-entry playtest before anything else is judged.

2. **The rescue.** `sailor rescues brother` becomes a `CIfAction` on the unused
   requirement. Potion in hand: spawn Juan alive, play `Sailor Juan / 1 Save Juan`, set
   the new state. No potion: exactly what happens today, unchanged.

3. **A living Juan.** A `CGeneratorAI` beside the corpse generator, which stays for the
   no-potion path. The walk home copies `sailor leaves`, which already does
   `CAssignTemporaryTaskAction` over a chain of five `CGoToAI` for Fernand; Juan shares
   three of its destinations rather than claiming them, and his `CGoToAI` legs are
   lifted out of that relay byte-for-byte with only `Destination=` changed.

4. **Fernand's return branch.** His generator's interaction is a two-armed `CIfAction`:
   quest ever activated -> `1 Return 2`, else -> `1 Return`. `CIfAction` has one `Then`
   and one `Else`, so a third arm nests: put the brother-alive test outermost with
   `1 return after saving juan` as its `Then`, and the existing `CIfAction` as its `Else`.

5. **Rewards.** Nothing new is needed. Both Barter routes self-limit through the
   `fernand gave barter` checker, already placed at (4592,1759) and `Active=0`. Success
   XP is the one decision: the death report pays 150 through the `saved juan but died`
   entity, and a rescue should pay more - a **second** XP entity, so the failure path
   keeps its shipped value.

### What got built

The footprint on `Port District.zax` is **four parts added, two changed, none
removed**, out of 1317, plus one line changed and one node added in a shipped dialogue
tree:

| Part | |
|---|---|
| `juan goes home` | new, walks him back down three of `sailor leaves`' markers |
| `juan bleeds out` | new, the 45-second clock and the shipped failure path |
| `told fernand juan lives` | new checker, so the payout happens once |
| `saved juan and he lived` | new XP entity, 300 |
| `sailor rescues brother` | changed: the potion branch |
| `Distressed Sailor generator` | changed: a third arm to the reward node |

The no-potion path is the shipped balloon and the shipped quest-If, **character for
character** -- the verifier re-extracts both from the archive and compares. Juan's three
`CGoToAI` legs are lifted out of `sailor leaves` byte-for-byte with only `Destination=`
changed; each is ~75 lines of movement boilerplate, and retyping them is how a default
gets altered by accident. Fernand's shipped two-armed `CIfAction` survives untouched as
the `Else` of the new one.

Both gates pass. The quest-state check needed fixing first: it scanned only the mod tree
for activations, so the two states this quest inherits -- activated by vanilla maps we do
not ship -- would have been reported as dead. It now reads the vanilla archive too, with
our files shadowing their archive counterparts rather than being unioned with them.

### Decisions taken while building

- **The potion is consumed, and the rescue is a click on the body.** Both of these
  reverse what the first build did, and both came out of playing it. The first build
  fired on the proximity trigger, so the rescue happened *to* the player rather than
  being something they did; and it did not take the potion, on the grounds that vanilla
  only ever removes specific quest items. That second claim was simply wrong. DaVinci's
  Magic Machine asks for "a magical potion - any potion will do", tests
  `Inventory Items/Potion` and then removes `Inventory Items/Potion` -- the same generic
  path Fernand hands out. One survey of `CActionRemoveInventoryItem` had shown only
  `Specific Item Cans/...` uses and that was taken as the whole picture; four generic ones
  were in the same result set, further down. The known limitation stands, but is now a
  cost paid deliberately rather than a reason not to act: the remove carries no
  `Additions`, so it takes *a* potion and may take a better one than the healing potion
  Fernand gave you. Vanilla's own Magic Machine has exactly this flaw.
- **300 XP**, against the district's own scale: Helped Bartolome 250, Saved Tomas 200,
  the death report 150, the murder-mystery payouts 500. The failure path keeps its
  shipped 150 through its own entity; this adds a second rather than editing that one.
- **Juan is revived in place, not replaced.** The first build deleted the corpse and
  spawned a fresh Juan from a generator, which is precisely a teleport, and looked like
  one. The engine never needed that. `Genderate Dead Body` -- the shared canned script
  behind every corpse in the game -- *transforms an entity in place* in nine steps, and
  each one has an inverse: drop the `Corpse` category, make him collidable, re-add the
  `CAISetOpacityBasedOnVisibility` it stripped, and wake the CSkeletonAI it parked in a
  `CWaitAI`. Then `GetUp` plays on the body already lying there.
  - **Order is load-bearing.** `Raise Enemy Action.can`, the necromancy spell and the only
    shipped thing that raises one of these corpses, sends the `Raise Enemy` message
    *before* playing `getup`. That is not cosmetic: the corpse script's `CWaitAI` has
    `Completion Message to wait for=Raise Enemy`, and `CPlayAnimationAction`'s
    `AI To Interrupt=CSkeletonAI` has nothing to interrupt until the message restores it.
  - **The animation exists for this model**, which had to be checked rather than assumed:
    `Boatswain/Shared Animations/{01,02}/GetUp.ANIMATION.GR2` is on disk, and the
    pre-rendered sprite the game actually draws,
    `Cache/Models/Characters/NPC/Barcelona/Sailors/BoatswainMace.mdl16`, lists
    `Shared Animations/02/GetUpB` among its baked sequences. A source animation with no
    baked frames would have played as nothing.
  - **Double-clicking cannot cost two potions.** The whole interaction is wrapped in
    `CCheckCategoryAction` for `Corpse`, and the revive drops that category as its second
    action, so a second click during the get-up finds nothing to do. This is structural
    rather than a `Trigger Only Once` flag, which would have burned the one chance for a
    player who arrived without a potion.
- **A player who never took the quest can still save Juan.** The trigger is `Active=1`
  from map load, so anyone who wanders to the island with a potion sets `JUA1LIVE`, which
  starts the quest already at "go tell Fernand". Vanilla anticipates the no-quest case on
  the death path the same way, through `discoverd brother dead`. Fernand's greeting then
  says "thank you *again*", which is slightly off for someone he has never met.

- **Juan is dying, not dead, and he can run out of time.** Play turned up a line
  that the restoration itself had made false: the shipped bark on approach reads
  *"<Arriving at the body, you notice that it has been very recently killed.>"*, which is
  correct for a corpse and absurd for a man who sits up when you pour a potion into him.
  Rewording it is one line, but it cannot ship alone, and the reason is worth writing
  down. `VMS91BAX` -- the state vanilla sets the instant you walk up -- is what gates
  Fernand's reply *"No, I was not. I'm very sorry, but your brother has perished."* So in
  the first build you could walk up, immediately report him dead, walk back, and revive
  him. A bark that says he is *dying* makes that contradiction impossible to ignore, so
  the state had to move to a moment when it is true, and nothing in the vanilla design
  provides such a moment. The timer creates it.
  - The approach trigger now sets **no quest state at all**. It starts a 45-second relay.
  - The **shipped quest-state If moves across whole** -- both arms, character for
    character, including the `discoverd brother dead` branch for a player who never took
    the job. The failure path is not rewritten, only rescheduled.
  - **The delay is not cancellable, by design.** `CDelayAction` fires no matter what, so
    rather than adding a second mechanism to call it off, the delayed block re-checks the
    same `Corpse` category the rescue does. Healed Juan has no such category and the whole
    block does nothing. One guard, read in two places, instead of two mechanisms that can
    drift apart.
  - It lives on a **relay** rather than inside the trigger because the trigger deletes
    itself on the frame it fires. Vanilla gets away with ordering actions after that
    `CDeleteAction` because deletion is deferred to end of frame; ninety seconds is not.
  - **45 seconds**, down from 90 after the first playtest, where the clock did not
    fire at all -- for the ordering reason below, not because 90 was too long. Verified
    in play at 45. A `Vodyanoi agile Generator` sits 61 units from the body --
    Agile, Super and Tough -- so the player usually arrives into the fight Fernand
    describes. That is what makes the timer a decision (pour the potion mid-fight, or
    clear the creatures first and gamble) rather than a formality. Too short and it stops
    being a decision and becomes a reload.
  - **A relay must be fired before its trigger deletes itself. Confirmed in play.**
    The first build ordered `CTriggerRelayAction` *after* the `CDeleteAction` that removes
    the trigger, and the clock silently never ran. Moving the relay call one slot earlier
    fixed it, and Juan now dies on schedule.

    This is worth stating as a general engine rule, because everything else about the
    relay was already correct and none of it was the problem: `Relay Name` is the only
    field the game ever uses (4021 times), `Forget Trigger=0` is what all 4089 shipped
    `CDelayAction`s use, a 130-second delay inside a `CRelayAI` is shipped, and
    runtime-added categories *are* visible to `CCheckCategoryAction` -- vanilla both adds
    and checks `Player Friend` and `Scripted Custom 1`. Chasing any of those would have
    been wasted effort.

    What found it was asking a narrower question: *what does this build do that no shipped
    map does?* Of the two vanilla enter-actions containing both a `CDeleteAction` and a
    `CTriggerRelayAction`, neither orders the delete first. That was the only deviation,
    and it was the bug. The trap is that vanilla **does** put a `CIfAction` and a
    `CDeactivateAction` after its self-delete and those demonstrably run -- deletion is
    deferred to end of frame -- which makes "actions after a self-delete are fine" look
    like a safe general rule. It is not: those actions need nothing *from* the trigger,
    whereas dispatching a relay evidently goes through it. The failure is silent, with no
    error and no partial effect.
  - **A regression the timer introduced, still open.** Vanilla set `VMS91BAX` the instant
    you walked up, so the death report to Fernand was always available. It is now set only
    when the clock runs out. A player who looks at Juan and walks off the map probably
    loses the pending delay along with the layer, which would leave the quest stuck at
    "I have not found him yet" and the shipped 150 XP report unreachable. The short clock
    makes it much more likely the question resolves while the player is still standing
    there, but that is mitigation, not a fix. If play confirms it, the answer is probably
    a second always-on trigger that resolves the state on re-entry.
  - This is the first **timed failure in the game**. Nothing in vanilla fails a quest on a
    clock -- no shipped quest state mentions running out of time -- so it is a new kind of
    pressure for Lionheart, and the main thing to be suspicious of in play. The primitive
    is not new, though: `CDelayAction` at this scale is shipped (vanilla runs one at 130s),
    and the map already uses `CLimitedTimeAI`.
  - It stays **losable, never unwinnable**: failing just routes to the vanilla death
    report, which still pays its shipped 150 XP and 100 gold.

### What to play

No QA cases yet, deliberately -- 0.5.0's lesson was that they should be written against
what play shows rather than what the build intends. Needs **a save that has never entered
the Port District**. Four routes:

1. Take the job, keep the potion, reach the body. You should get the shipped "he's dead"
   balloon on approach, exactly as in vanilla, and then the cursor should turn to the
   Interact hand over Juan. Click him: the potion goes, he plays a get-up animation,
   thanks you, and walks off toward the ship.
2. Take the job, arrive without a potion. Clicking him prints that he is beyond your
   help, and leaves the body clickable -- but the clock is running, so coming back with
   one is only possible inside 45 seconds.
3. Take the job and stand there. After 45 seconds he dies -- **confirmed in play**.
   Still to check: that the body stops being clickable, that only then does the log say to
   tell Fernand he perished, and that reporting it pays the unchanged vanilla 150 XP and
   100 gold.
4. **Whether the clock survives leaving the map is not known and needs watching.** The
   engine swaps a level out when you leave, so a pending delay may pause, may resume, or
   may be lost. All three are survivable -- worst case he stays savable indefinitely --
   but which one happens decides whether "go buy a potion" is a real option.
5. Report back to Fernand after 1. The reward node should open, pay 300 once, close the
   quest, and offer the companion at Speech 20 or Barter 20.
6. Recruit him, and take him somewhere. This is the first time the companion machinery
   has ever run for this character.

### Open decisions

- **The potion check is loose.** `Player has a potion of healing.can` tests for
  `Inventory Items/Potion` generically; Healing and Extra Healing are distinguished by
  their `Additions`, not the item. As written, any potion passes, so a player carrying
  one for any reason gets the good ending without spending Fernand's. Recommend accepting
  the vanilla file's own looseness rather than tightening it: it only ever helps someone
  who came prepared, and using the shipped file unmodified is the stronger claim about
  what was intended.
- **Fernand is fragile.** `Distressed Sailor.can` points at `Races/NPCs/Sailor` - a real
  race, so not the dangling-self-reference bug - at **36 HP and AC 90**, against the
  Wererat Boss's 150. Recommend leaving him: the writing is explicit that he is a sailor
  of modest means breaking a vow of duty, and a companion you have to keep alive is the
  more interesting object than a repointed one. Revisit only if play says he dies before
  he can say anything.
- **Where he can follow.** He has one banter node and no hurt or combat barks, unlike
  Cortes, who has ten. Nothing needs stripping, but he will be silent in a way the other
  companions are not, and that is worth seeing in play before deciding whether to write
  any.

### The rest of the district

| Item | Verdict |
|---|---|
| Port guards' murder reaction - `200 Duke is Dead`, `300 assassination`, `500 tragedy` | **Built.** See below. |
| Fish Monger `60 sold skull normal price` | **Built.** See below. |
| Brendan Michael Sullivan, the Irish sailor | **Built.** See below. |
| `Gather the drunken sailors from the tavern` | Zero states, referenced only by the fall-of-Barcelona failure sweep, and `DrunkSailorsInBar.DialogTree` is seven ambient barks with no quest content. Nothing to restore - it would be new writing. **Out.** |
| Cortes `165 help with arm` -> `170 accept cortes arm quest`, and the unused `Cortes Help Him Rebuild Arm.can` | **Out, and now on evidence rather than suspicion.** The read was done. `Give Cortes a Hand` has six states. The orphaned chain is `15 Return Greeting` -> `165 help with arm` -> `165 help with arm 2` -> `170`, and `165 help with arm 2` activates **`WEDKYW9X`** - *"DaVinci has told you that Eduardo will need Red Ore"* - which is the quest's **second** step. The reachable `164 cortes needs to repair the arm` activates **`EPVSO4Y0`**, *"you will find DaVinci and ask"*, the first. Restoring the branch would drop the player into the middle of the arm quest with the DaVinci conversation already assumed, and `WEDKYW9X` is reachable four other ways in normal play. `Cortes Help Him Rebuild Arm.can` has **zero** references, consistent with an abandoned gate. A superseded draft, confirmed. |
| Bartolome's `80 thank you`, handing out Boots Arid dJinn | Orphaned, but `100 saved brother` is reachable, gives the same boots and completes the quest. A draft, not a loss. **Out.** |

### The Duke's murder leaves no crime scene

The assassination plays in vanilla: blow up the Duke and a guard runs in shouting
`400 guard calls for help`. What that guard's balloon then does is fire
`Fade down and remove the duke`, which **deletes both the Duke and the guard** 2.1 seconds
later and ends the cutscene at 3.1. When the screen fades back up the scene is empty. That
is why `200 Duke is Dead` - *"Move along, citizen. This is a crime scene."* - and its
answer `300 assassination` cannot be reached: after the murder there is nobody there to
say them.

Two guards now stay, using the two positions the level already has:

- `Duke Guard Goes Here` (2255,1394), where the shouting guard runs to, free again once
  he is deleted.
- `Duke Guard 2` (2344,1306), an `Editor/Position Marker` **defined once and referenced
  nowhere** - a second guard post placed and never used. Established by counting
  references, not by reading the name, after the `juan travels back` markers taught that
  lesson earlier in this same release.

Both open `200 Duke is Dead`. A one-shot proximity trigger balloons `500 tragedy` over the
second guard when the player next walks in; that node carries no replies, exactly like the
shipped `400`, so a bark is the consistent reading rather than a conversation. They are
switched on inside `Fade down and remove the duke`, behind the screen fade, so the scene
changes while the picture is black.

**A vanilla name mismatch, checked and harmless.** The clone that spawns the shouting guard
names `Duke Guard Generator`; the entity is `Duke Guard generator`. Play confirms he
arrives, so lookup is case-insensitive - and a census puts a number on it: **232
references across the shipped maps resolve only if case is ignored**, in scenes that
demonstrably work. Worth knowing, because had it been case-sensitive the cutscene would
never have ended.

### The Fish Monger, and a perk for the skulls

Selling a vodyanoi skull at the normal price works, but the reply that takes the gold has
a blank `Go to node ID=`, so the conversation just stops. `60 sold skull normal price`
- *"Excellent! A pleasure doing business with you. Anything else?"* - is written for that
moment and nothing reached it. Its own first reply, "I have another vodyanoi skull to sell
you.", was likewise blank; it now returns to `50 skull`, closing the loop the two nodes
were plainly written to form.

Restoring it exposed a second defect behind the first: node 60's *"I have other
questions."* points at `10 Goodbye`, which does not exist, so the reply would have closed
the conversation instead of asking anything. Repointed at `10 other questions`. The
tree's other dead targets are left alone - `5 Goodbye` against a node called `5 goodbye`,
one with a trailing full stop, one where a reply's own text was pasted into the target
field - because all of them are *goodbye* replies, and a dead target ends the
conversation, which is what a goodbye does.

**New content, deliberately: sell him fifteen skulls and he tells you where to aim.** This is
not restoration and is the one thing in 0.6.0 that is not, so the reasoning is recorded in
full. The engine supports every piece except one:

- `CriticalChance` is a real derived attribute and `More Criticals.Perk` is a template.
- `CGiveCharacterPerkAction` has 56 shipped uses, so a script can grant a perk, and
  `!NPC or Event Given Perks` is where NPC-given ones live. They carry a deliberately
  unsatisfiable `0 >= 1` requirement so they can never be chosen at level-up; ours does
  too.
- Fifteen is comfortably reachable, which was checked rather than assumed. All twelve
  vodyanoi cans use `Vodyanoi Drop Action`, a three-way `CRandomAction` over
  nothing / skull / gold, so roughly one kill in three yields a skull - and the game
  places **471-589 vodyanoi**, about 160-200 skulls. Barcelona Coast alone (147) covers
  it several times over. The *summoned* vodyanoi cans are not among the twelve, so the
  count cannot be farmed with Monster Summoning.
- Counting uses the `Goblin Kill Counter` idiom - a `DerivedCharacterAttribute`
  incremented with `Allow Accumulation=1`. Reading it back in dialogue with
  `Custom Requirement=CIsGreaterThanOrEqual` over `CVariableDerivedCharacterAttribute` is
  what the Port District's own `Grumpy Port Guard.DialogTree` already does.
- The bonus copies `Animal Slayer.InventoryAddition`: a `CPlugInBehaviorStrikeAction`
  guarded by `CExpressionHitMargin > 0` so it only pays on a blow that lands. The
  condition is `CCheckModelAction` over all three vodyanoi models rather than Animal
  Slayer's category check, because vodyanoi are `Category=Animal,Enemy` and a category
  check would fire on every animal in the game.

**The unproven part:** no shipped *perk* carries a `CPlugInBehaviorStrikeAction`. Perks and
inventory additions share the same `PlugIn Behaviors=Array` and the behaviour is real -
five critical-hit effects and a dozen weapon additions use it - but whether the engine
runs one from a perk is unknown until it is played. If it never fires, the fallback is a
flat `CriticalChance` perk in the shape of `More Criticals`.

It is bonus damage rather than literal critical chance because crit chance is a character
attribute and nothing in the perk system can see who you are fighting; there is also no
action that *applies* a critical hit, only `CActionRemoveCriticalHits`.

**It is a hidden perk, and that is deliberate - do not "fix" it by adding a hint.** The
monger never mentions the soft spot until the fifteenth sale, so nothing signposts the
reward and nothing tracks it on screen: the counter attribute ships with
`Display In Attributes Window=0`, `Display In Character Creation Summary=0` and
`Display Some Other Place=0`, so the player sees no progress bar and no clue. The whole
thing is discovered by having sold him skulls for their own sake. A hint line in
`60 sold skull normal price` was considered and rejected. The perk itself does appear in
the perks window once granted, which is the reveal.

### The Irish sailor: the dead copy names the missing link

Brendan Michael Sullivan exists twice. `Bar Patrons` is opened by the tavern 45 times
including his greeting; `ShipSailorsonShipCanned` is opened by no map at any 200-series
node. So the live copy is `Bar Patrons` - and the **dead** copy is what identifies the
break, because it carries the one reply that reaches `200 irish`:

    That accent is odd - where are you from?    ->  200 irish

The live greeting offers drink / who are you / insult / goodbye and no way to ask, so the
node answering it - the one saying Ireland *"sank some three hundred years ago during the
troubled times"* - was unreachable. The reply is lifted from the duplicate rather than
written, so this restores text the game already ships.

### Explicitly not in it

**Grace O'Malley.** Isabella's tree carries eleven unreachable `500`/`502`/`503` nodes for
the England act - `502 grace joined romantic`, `502 grace companion near death`,
`503 druids` - with matching `.ogg` files sitting in her Port District VO folder. They are
unreachable for a blunter reason than Fernand's: `Captain Isabella.DialogTree` is opened
by exactly one map, `Port District.zax`, and she is never placed in Act 7 at all.
Restoring her means placing a character in the English Shrine and deciding what her
presence does to that act's ending. That is a release of its own, and it belongs after the
companion machinery has been exercised once on Fernand.

### Gates before this ships

- `tools/validate.py` extended with a `.Quest.txt` check (**built**): state IDs unique and
  well-formed, `Item Count` matching the array, and every ID activated by a
  `CActivateQuestStateAction` somewhere - scanning the vanilla archive as well as the mod
  tree, since an edited shipped quest inherits states that vanilla maps activate.
  Negative-tested on all four rules against a deliberately corrupted copy of
  `help distressed sailor.Quest.txt`; each fires with the right message, and the restored
  file passes.
- `tools/validate.py`'s dangling-target check now tolerates targets **already dangling in
  the shipped copy of the same tree**, the way reachability.py tolerates vanilla orphans.
  A Fixt tree is usually a shipped tree with nodes spliced in, and `Fish Monger` alone
  inherits four dead targets; reporting those says nothing about this mod and buries the
  ones it would introduce. A tree authored from scratch has no vanilla counterpart, so
  every dangling target in it is still reported.
- `tools/reachability.py` in gate mode (**built**, and now part of Gate 0 as A0.13): no
  node this mod adds may be unreachable. Nodes already orphaned in the shipped tree are
  tolerated, since a Fixt tree is usually a shipped tree with nodes spliced into it - it
  currently tolerates 69 and passes. Negative-tested against both halves of the rule: a
  new node nothing links to, and a broken link orphaning a node that used to be reachable.
  This release exists because that check did not exist, and it should not have to be
  rediscovered.
- **A save that has never entered the Port District.** New entities on an edited map do
  not appear on a save that has already visited it, and this release adds several.
- The vodyanoi fight, the potion route, the no-potion route, and the recruitment played
  separately. Nine defects in 0.5 passed parse, byte-identical round-trip, every validator
  check and verified deployment, and were visible only in the running game.

## 0.5.1 - the two crashes 0.5.0 would have shipped

0.5.0 was packaged and never tagged. Play found two fatal errors within minutes of each
other, both on entering the vault, both the same underlying mistake: art referenced
without being checked against the archive.

- **`Model=Environments/Misc/Chest/Chest A` does not exist.** An invented path. The game
  dies on map entry with a "Fatal Not Found Error" naming the model and the map.
- **`Cur Sequence=Idle` on a chest.** Chest models have `Closed`, `Open` and `Opening`,
  and no `Idle`. Same dialog, same fatality, one field over -- found immediately after
  fixing the first, because fixing the model did not prompt me to check the animation on
  it.

Both are now gates. `tools/validate.py` asserts every `Model=` exists, and that every
`(Model, Cur Sequence)` pair a Fixt file introduces is one the shipped game uses for that
model -- 200 vanilla maps are a better authority on which animation belongs to which
model than anything inferred, and it means the check reports the correct value rather
than just refusing. Both were written before their fix and confirmed against the real
crash. Neither existed before, which is exactly why 0.5.0 was packaged with two of them
after passing every other check, round-tripping byte-exact and deploying byte-identical.

A sweep of every entity this mod adds across all four edited maps found no other
instance of either fault.

### The guard attacked after the Speech check passed

Also found in play. The quiet routes ran `CDeactivateAction` on `Secret Quest Guard`,
which is the **generator**, not the man. The spawned guard carries three AIs of his own
and one is a `CTouchingOvalTriggerAI` holding `CGoToCombatAction` -- a proximity trigger
that fires when you walk into his oval regardless of anything said. Deactivating the
generator only stops it spawning a replacement.

He also spawned as `New Name=Sewer Thief`, shared with every thief in the den and with
the mass-hostility relay's target list, so he could not be addressed individually. He is
now `Vault Guard` on that generator alone; the other eight `Sewer Thief` spawners are
untouched. The four quiet routes strip the proximity trigger and clear his targeting --
`CRemoveAIAction` and `CSetTargetTypeAction`, both idioms vanilla already uses in that
map and in the jail relay -- and the fight route names him explicitly rather than
relying on `$Trigger` scoping.

One consequence: because he is no longer called `Sewer Thief`, the mass-hostility relay
does not include him. On the fight route he is made hostile directly, so that path is
unaffected, but if the den is roused some other way while he lives he will not join in.

## 0.5.0 - the thieves' guild

**Not signed off.** Of the three things in this release only one has been played: the
final job, end to end, by a tester on the day it was built. The caught-in-the-act
branch and the vault job are built, verified and unplayed. `docs/qa.md` SR1-SR42
covers the first two; the vault has no cases yet, deliberately, because they should be
written against what play shows rather than what the build intends.

### Why the thieves needed it

Counted properly, Enrique offers five jobs and Juanita four. He pays out around 600
gold across his line; she has seven `CTakeMoneyAction` and not one give. The single
biggest quest in the Sewers -- the wererat cure, five states across three maps -- is on
his side. Her jobs pay more XP each (500 against 200), but there is one fewer of them
and they cost money to take.

Her fifth job was written and never reachable. `130 Final Job` is the only thing that
activates `Thieve in Temple District`; nothing reaches node 130; that quest's second
state is activated by nothing; and the requirement `.can` written to gate its turn-in
is used nowhere. The frame shipped whole with nowhere to happen.

### The first new map

There was no house to rob, so this adds one. That is possible because no file registers
the 200 shipped maps, a room's walls and floor are a single prefab entity rather than
baked terrain, and -- per the tools repo's own `test-pocket`, built from scratch and
shipping no caches at all -- the engine generates the waypoint graph and automap when
they are absent.

The entrance took three attempts and the two failures are worth keeping. An unnamed
door with a `CDoorAI` and an empty `After Opened` looked like an unused entrance; it is
the only door in Barcelona that draws behind its own building, sitting at 48% across
and 49% down the House Of Ilk's sprite, and the ground behind its fence is unreachable.
Both are why it shipped dead. The second attempt then treated walkable ground as
reachable ground -- the `.way` positions decode reliably, but connectivity lives in the
edge lists, which do not.

### Getting caught

Skill decides the cost, not whether the job is possible. Vanilla's own equivalent
robbery has no gate at all: the entity named `hidden poly reveaked if perception check
passed` is `Active=1` with zero activations anywhere. Here, Perception 5 or Find Traps
35 gets you out quietly. Without either, a guard is waiting outside. Surrender copies
`Eduardo Sends you to jail` and lands you in `Inquisition Chambers2 @ Jail Start`, where
Sanchez already handles the fine, the Speech routes and release -- and nothing in that
flow strips inventory, so the quest survives a sentence. Fight instead and Juanita
takes you anyway, with a word about drawing the watch onto the guild.

She reacts only to *this* arrest. Vanilla's `been in jail before` is set and read only
inside `Inquisition Chambers2`, purely to pick Sanchez's greeting, and six shipped
routes reach that cell; keying off it would have made her hostile over a Templar
scuffle. Two new markers carry it instead.

### The vault

`09 Secret Quest` is a 324KB map -- spike-trap doors, thief archers, guard dogs, ~950
XP of markers -- that no quest points at, behind a door that is unlocked. Its guard is
fully built and `Active=0`, so today you are shouted at twice by warning balloons
belonging to someone who is not there, and you walk in.

Taking Skulker's job switches him on. Five ways past: the `Thief Friend` perk, Speech
40, a hundred gold at Barter 35, Sneak 35, or steel. Fighting fires vanilla's own
`Thief enemy trigger` -- `CGoToCombatAction` over Sewer Thief, Juanita and the dogs,
plus `Make unspawned thieves mad at player` -- and the den comes for you. Quiet costs
nothing.

Skulker rather than Juanita for a reason: after the seduction she is stripped of her
interaction specifier and walks out through `secret door2`. She is not deleted, but she
can never be spoken to again, so her arc has a hard terminus.

### Repairs found on the way

- **Juanita's fee was avoidable.** Refuse her 70 gold, walk away, come back, and the
  reply "I've decided to pay you for another lead" handed it over free -- no
  `CHasMoneyAction`, no `CTakeMoneyAction`. Node `81 decided to pay` charges 100 and was
  unreachable, and `Juanita requires player to have less than 100 gold` ships used
  nowhere. Both are now wired.
- **The night with Juanita explains itself.** `Juanita Seduction` ships with real text
  in all nine nodes but no replies in any of them, so it opens and closes on its own and
  does not register. The low-charisma path takes up to 500 gold and tells you only
  through that box.

### Gates

`tools/validate.py` passes at 97 files. Every map edited round-trips byte-identically
through `resource_format`, and the deployed `data.dat` was byte-compared against source
after every change. Check A0.7b caught a hard crash before it shipped -- an empty
`Node ID=` in the guard confrontation poly.

None of that is a substitute for playing it, which is the whole point of the note at the
top of this section.

## 0.4.1 - repair

**No new content.** Every line of this release fixes something already shipped, and two of
the three items were only found because 0.5's work made a player walk paths that had never
been walked.

### The blank line

A reply in a `.DialogTree` must be preceded by an empty line. Vanilla holds this without a
single exception -- 10915 replies, zero violations -- and the parser needs it: without the
separator a reply is swallowed into the one before it, so it never becomes its own choice and
its `Custom Action` never runs. The failure is silent and looks nothing like its cause. A
conversation plays through normally and a quest simply does not advance.

Fixt has been shipping that defect since 0.2.0, in **47 places across six conversations**,
because every helper used to reorder or append replies rebuilt the node by joining on a single
newline:

| Conversation | Sites | Shipped in |
|---|---|---|
| Herbalist (Quinn) | 21 | 0.4.0 |
| GoblinKhan | 5 | 0.2.0 |
| Jafar (Amir) | 2 | 0.3.0 |
| saladinknightcan | 1 | 0.3.0 |
| Guard Esteban | 1 | 0.2.0 |
| Blacksmith (Eduardo) | 1 | 0.5 work |
| Warning Troll | 16 | 0.5 work |

Jafar's `3 Return Dialogue` being on that list matters: it is the node the Sacred Scimitar
hand-in was moved to after being reported unreachable **twice** in 0.3.0. The move was correct
both times. It was very likely landing in a malformed node all along, which means that
diagnosis was wrong.

### Two of Quinn's three errands could never be started

The replies offering the wasp stingers and the troll hide carried a `Custom Requirement` --
the gate deciding whether to *show* them -- and no `Custom Action` at all. Quinn asks, the
player agrees, and the quest never activates, so both turn-ins stay invisible and both errands
are uncompletable. That is two thirds of 0.4.0.

`QN8HD4LM` also gates the Warning Troll's peaceful trade reply, so the non-violent route to a
lava troll hide was dead as well.

### Esteban's contract never closed its journal

`Kill Guard Esteban for the Goblin Patrol` defines a second state -- "Esteban is dead. Return
to the goblin patrol leader and collect what you were promised" -- that nothing ever set, so a
player carrying his corpse still read "kill him". The hand-in always worked, being gated on
his death rather than the state; only the log was wrong. Now hooked into the death script and
guarded on the contract actually having been taken, so it cannot retroactively hand a goblin
contract to somebody who killed him for the Templars.

### Two new gates, because none of the above was catchable

`tools/validate.py` now fails on a reply that is not preceded by a blank line, naming the
node, and on any state of a Fixt-authored quest that is never activated. Both were verified by
deliberately breaking them. The second immediately caught the Esteban state -- and then caught
its own first implementation being wrong, because the regex assumed no indentation, which
holds for DialogTrees and not for tab-indented `.can` files.

### What is NOT in this release

The Sewers faction work -- troll peace, the Tomas ransom, three allied errands, the
desecration scene -- is on `main` but is **0.5.0**, unfinished and lightly played. None of it
is reachable on an existing save, so it is inert for anyone installing 0.4.1 over 0.4.0.

## 0.4.0 - "Quinn's Reagents"

**The first release that is mostly new content**, and it should be read as a deliberate
crossing rather than more restoration. The project's order is fix, then restore, then
extend, and this is extend.

What makes it cheap is that almost none of it needed authoring. Two of the three reagents
already exist as items with finished art, and one of them -- `Lava Troll Hide` -- was
referenced by **nothing at all** in the shipped game: a quest item for a quest nobody wrote.
The three healing tiers were already built in a separate mod, shipping into a test map where
no player could reach them.

### The chain

| Errand | Reagent | Unlocks |
|---|---|---|
| 1 | three wolf pelts | Great Healing |
| 2 | five wasp stingers | Superior Healing |
| 3 | one lava troll hide | Supreme Healing |

Strictly ordered, and **paced by where each reagent lives** rather than by a level check --
which is the whole reason the order matters. Supreme Healing is roughly four times Extra
Healing and would wreck act 1 if it arrived there.

### Three ways to the hide, so nobody is locked into hostility

Vanilla wrote a diplomatic opening to the lava trolls and closed it. Every branch of
`Warning Troll.DialogTree` ends in combat or walking away, and killing one turns the whole
pit. But the troll states his grievance unprompted, and it is **pragmatic, not moral**: the
wererats are killing his people, and he does not care how that stops.

Because the Beggars *are* the wererats, both endings are already tracked vanilla quests:

| Route | Read |
|---|---|
| Cure them | `Discover a cure for wererat lycanthropy` |
| Exterminate them | `Kill The Beggar Master`, or `Help the Thieves Destroy the Beggars Guild` |
| Kill a Lava Troll Boss | it drops the hide |

Good path, evil path, or no diplomacy at all. The route deliberately does not reward mercy
specifically -- vanilla's own cure quest requires killing the Prime Wererat for a patch of
fur, so framing it that way would be dishonest.

### The Wolf Trapper perk locked you out of the errand

The migrated wolf-pelt mod consumed the plain `Wolf Pelt`. Every wolf can branches on
`Wolf Trapper Perk Checker`: without the perk you get one plain pelt through a canned list,
with it you get two `Wolf Pelt Perk Quality`. So taking the perk handed you pelts your own
quest would not accept. Either now counts, at each of the three units.

*(My first diagnosis of this was wrong -- I said the quest was uncompletable by anyone,
having missed the canned-list indirection. The user had completed it in play. Corrected in
`321a9cb`.)*

### Also in it

Gate 0's validator moved into the repo at [`tools/validate.py`](../tools/validate.py). It
had been described as scripted since 0.1.0 while only ever existing in a session scratchpad.

## 0.3.0 - "The Knights of Saladin"

### The order awards the title and never the rank

The Dream Djinni trials are reachable and completable, and they award `Dervish of the
Crescent` -- whose own text reads *"You have become a **Favored One of the Knights of
Saladin**"* -- or `Scholar of the Crescent`, chosen by whether you beat Kabool in combat or
in a contest of wits. Both are perks, and perks confer only skills.

`Dream Djinni Map.zax` performs **0 faction assignments and 0 Saladin Rank writes.**
Meanwhile `Saladin IS` tests `Uber Perks/Saladin Rank > 0`, and the only things that
increment that counter are the three `.Faction` records -- assigned nowhere in the shipped
game except `Levels/Test Maps/James/James.zax`, a test map.

So the title and the rank were never connected, and **20 replies across four acts can never
appear:**

| Where | Replies |
|---|---|
| Quinn the Herbalist, Gate District | 6 |
| Sir Roger, English Shrine | 7 |
| Brother Michel, Montaillou | 3 |
| Joan of Arc, the Crypt | 3 |
| Temple Entrance Guard, Gate District | 1 |

Plus node-level greetings: both Barcelona knights have *"Welcome, brother into the Order of
Saladin"* nodes, and the Alamut companion has male and female Saladin variants.

**The repair is one `CAssignFactionToCharacterAction` for `Factions/Saladin Aswaran`, beside
each of the two perk grants that already fire.** Aswaran is the entry rank, which matches
"Favored One" and leaves Blessed and Exalted as headroom.

Safe against double-assignment two ways. Each grant is already wrapped in a *"does the
player not already have this perk"* guard, so it fires once; and faction tiers replace
rather than stack -- the lesson 0.1.4 learned the hard way with the goblins -- so a player
who somehow earned both trials still lands on Aswaran at rank 1, which is all `Saladin IS`
needs.

Note the stacking that becomes visible for the first time: the faction record adds +10
One-Handed, +10 Two-Handed, +1 Endurance and +20 carry weight on top of Dervish's +5s. That
is vanilla's arithmetic, but nobody has ever had it applied.

Six of the twenty replies are on **Quinn**, which is a useful accident -- he is metres from
the Dream Djinni, so the cheapest test of this fix is also the character the next release is
built around.

### What else shipped in it

**The Sacred Scimitar questline, restored.** Fully authored, unstartable, broken at all
three ends -- the starter was a proximity trigger with both `Active=0` and `X Radius=0`,
Amir's second-task node was a fork that had lost an arm, and the hand-in reply pointed at a
node that does not exist while carrying the quest's completion action. Routed through Amir
rather than by re-enabling the dead trigger, which is ungated and would hand the quest to
anyone who walked into the smithy.

**Farshad's conversation.** Sixteen nodes, including two "Welcome into the Order of Saladin"
greetings, hidden because his talk interaction opened a *balloon* of `10 Goodbye` and
`saladinknightcan` was never opened as a tree anywhere. Third instance of that bug shape
this project has found.

**The scimitar remembers how you earned it**, and the Dream Djinni sets it alight rather
than handing you a duplicate. See the release notes.

### Four vanilla defects the restoration exposed

All four found by playing, none catchable by Gate 0, and all invisible before because the
questline could not be started:

| Defect | |
|---|---|
| The quest could move backwards | `I8FFAL7P`, the state Amir's gate needs, is set in exactly one place; the other reply at node 64 sent the quest back to "Do as Blacksmith requests" with nothing to advance it again |
| The hand-in was unreachable | Its reply sits on `15 questions`, entered from seventeen topic nodes and never from the greeting the map opens |
| A duplicate reward | The combat trial hands out the same Sacred Scimitar -- almost certainly the cut quest's payoff, relocated |
| A near miss | Enchanting the blade would have broken Farshad's lesson gate, which tested only for the item |

**The lesson of the release:** restoring content runs code that has never executed. Static
verification proves every reference resolves and tells you nothing about any of this.

## 0.2.1 - the bandit you killed before he asked

A patch. One relay in `Crossroads.zax`, `After Verify thief display dialog tree`, opened
`113 Thief success` -- *"Good work! Here is your justly deserved reward"* -- when the only
path that can reach it is the one where Esteban never gave you the job. `114 pre assigned
thief success` was written for it and reached by nothing.

The path is provably exclusive: `140 verify too` has two inbounds and both sit behind
`Esteban will not reassign thief quest`, which succeeds only when `Find the Crossroads
Bandit` was never activated.

Corroborating, and the reason this was findable at all: the shipped gate `Esteban requires
bandit dealth with before assinging quest` -- the bandit quest *completed* -- is read by
nothing anywhere in the game. Built for this state and never wired, the same shape as the
`Goblin Horde Midlevel` gate that 0.2.0 finally gave a reader.

### Pointing the relay at 114 exposed that 114 was unfinished

Consistent with it being the arm that got dropped. Both gaps closed with lines and targets
already present in the tree:

- Its wasps reply had an empty target. Both nodes complete `Slay the Giant Wasps` inline
  and pay 100 gold, but 113 continues to `103 wasps killed` and 114 did not, so handing in
  the wasps on this path ended the conversation with no acknowledgement. `103 wasps killed`
  completes nothing and pays nothing itself -- checked before retargeting, because
  double-payment is exactly how this class of fix goes wrong.
- It had no goodbye, and its default reply advanced to `35 dangers 2` rather than closing.
  It now carries 113's *"I should be on my way."* as the default.

`113` is untouched and still reached from six places, which is the regression to watch.

**This is a voice fix.** The 150 gold, the experience and the quest completion all worked
before.

## 0.2.0 - "What Was Written"

Almost everything here was written by Black Isle and never reached the game. Not cut lines
in a leftover file -- finished nodes, in the files the engine loads, that nothing in the
game can ever open. The release is named for that.

It is also the first release scoped deliberately rather than by opportunity. The survey
found 84 repairable dead ends across five acts; shipping them all would have been more
surface than one person can play-test, so 0.2.0 stays inside the goblin thread that 0.1.x
already established.

### The Goblin Girl's follow was written and never wired

Vanilla ships `90 Follow`, `190 Follow 2` and `195 Follow 2 no snails` -- three terminal
nodes in which she announces she is coming along, each with no replies and no action. Their
neighbours carry `Action work in progress=girls walks away` and `girl storms off`, the
original designers' inline to-do key, so the whole gesture was cut rather than forgotten.

The engine has exactly one follow mechanism, `CSetCompanionAction`. There is no generic
follow AI: `CApproachTargetAI` and `CPursueAI` have zero uses in shipped content and
`CGaurdNearMovingPosAI` has no target field. Companions cross map transitions, gated on
"You must gather your party", and vanilla bounds them with a remover entity on each map
where they are unwanted -- `Remover of Barcelona Companions` appears on eight. The Warrens
is cheap to bound because both its exits relocate to the same map, so the release happens
at the exits themselves, behind a farewell node.

**Confirmed in play.**

### The Khan's war campaign, and the fight for walking out of it

`350 next task` -> `360 attack barcelona` -> `365 barcelona walls`, all vanilla, all
orphaned, all reply-less. `365` names Guard Esteban as step one of an invasion -- which is
the motive the Esteban contract has never had, one release after 0.1.4 made that kill pay
out. `400 Where are you going?` was a fourth orphan and is what refusing the campaign now
reaches.

Gated on Champion, the rank the Khan himself grants. One new node, `370`, for the case Fixt
created: a player who killed Esteban before ever hearing why.

**The horde never does attack Barcelona.** Act 6 has essentially no goblins in it. The
briefing restores the plan the Khan states and leaves it stated; wiring the second half of
the order is buildable -- the Gate District holds nine `Gate Guard` entities and a
`Barcelona Portcullis` -- but it would resolve to nothing, and a tracked objective that
visibly fails to pay is worse than a stated plan that never happens.

### Grumdjum's post-dryad conversation opened a bark

One field. Handing in the dryad kill despawns him and spawns a second copy at her body,
whose talk interaction opened `160 After Dryad death bubble` -- one line, no replies -- instead
of `8 Return Dialogue Dryad Dead`. The tree proves the intent: node 8's own exit reply goes
to 160, so the designers wrote the bubble as the sign-off and the wiring sat one level too
shallow.

Node 8 is the sole gateway to `100 Goblin City`, where he says to seek the goblin city
*through the waterfall to the east* -- the only in-world direction to the Warrens that
exists -- and to `200 new poem`.

### Standing counts with the goblin jailor

The Darsh escort scene is fully wired in vanilla and needed no repair; it offers one
non-violent way past the jailor, Speech 25. `Goblin Horde Midlevel` had been built in 0.1.2
and read by nothing, so Blooded and Champion now pull rank instead. Adds a route, removes
none.

### Five dead replies

One dangling target in Inquisitor Darsh's tree, cleared rather than retargeted because all
four replies on that node fire a relay and the relay is the outcome. Four blank options
that did nothing when clicked -- deleted where the node had other replies, marked as the
default close where they were its only exit.

### What the survey got wrong

The scan that found this release -- a node nothing reaches, counting both the tree's own
`Go to node ID` and every `.zax` that opens it -- runs at about a one-in-three hit rate.
Three leads were investigated and cleared, and are recorded in `qa.md` so they are not
re-opened: the goblin jailor (vanilla wires it end to end), the captive child on Scar
Ravine (a duplicate node ID in a sibling file), and the Woodcutter's A-1 through G greeting
matrix (superseded by two consolidated nodes, not cut).

### Explicitly out of 0.2.0

**Grumdjum's companion arc** -- ten nodes covering join, dismissal, rejoin, injury barks and
combat quips, all in rhyming couplets. His join line is about Alamut, the Khan's `500 Start
in Persia` is a matching cut goblin companion for the same act, and neither has a companion
generator on any map. One cut Act 8 feature, and it should return with Act 8.

## 0.1.4 - "What Playtesting Found"

*Written up as 0.1.3 and never published; more fixes landed before it went out, so it
ships as 0.1.4 rather than leaving a version that exists only in this repository.*

Everything here came from a play session rather than from reading the archive, which makes
it the first release whose contents could not have been planned.

### Rakeb's unreachable greetings

**Rakeb had 33 nodes and the map opened two of them.** Three finished return-greetings were
unreachable, because `3 Return Dialogue` was shown unconditionally and swallowed every
situation they were written for:

| Node | What he says | When it now shows |
|---|---|---|
| `115` | *"You return, but we do not see the eyes. Find the woodsman and return with them."* | you took the eyes job and have not delivered |
| `63` | *"I knew you would return. I have a job for you."* | the devil fish are dead, the second task untaken |
| `136` | *"We hope the items have served you well..."* | all his business concluded |

He now has a selector on the same pattern as the Goblin Girl's -- most specific first, each
rung a strict narrowing of the one below, with `3 Return Dialogue` as the fallback. His
first-meeting node is untouched.

**Confirmed in play**: returning with the eyes job outstanding produces node 115 rather than
the generic greeting. That also settles a question the selector depended on --
`CIsQuestStateTheCurrentStateAction` does evaluate correctly from a map interaction, not
only from a dialogue requirement.

Two orphans are deliberately left alone. `200 dead woodcutter` has no text and no replies:
an empty placeholder, with nothing to restore. `300 shaman` and `300 shaman 2` are
Khan's-court guard lines sitting in the wrong file -- no map anywhere opens Rakeb's tree at
them, and inventing a reason for a shaman to shout *"Bow before the Great Plumdjum Khan, you
worm!"* would be writing new content rather than restoring it.

An audit of the rest of his tree found nothing else wrong. Two things that looked broken are
not: `43 Crazy`'s *"You'll die for that remark!"* has no target because it carries
`CGoToCombatAction`, and the two identical *"I have killed the Devil fish"* replies on node 3
are mutually exclusive -- one requires the Darsh rescue quest to be current, the other
requires it not to be.

### Two rewards were repeatable

**Two rewards could be collected over and over.** The Goblin Girl handed out a liver pie
every time you asked, and Rakeb would re-issue the devil fish quest as often as you cared to
say *"speak to me as clan"*. Same defect in two shapes: a one-time transaction offered from
a node the player returns to freely, with nothing asking whether it had already happened.

Her node 200 is the greeting for as long as the woodcutter is dead, and its *"Here, I
brought you his liver"* reply led to the pie unconditionally -- it did not even check you
were carrying a liver. It is now gated on a flag set when the pie is handed over, so the
reply disappears once the exchange is done.

Rakeb's offer already carried a guard -- `NOT exists("killed all fish")` -- so vanilla did
think about it, but that only rules out re-taking the quest *after* the fish are dead. It
says nothing about taking the quest, walking away and coming back. Vanilla's test is kept
and ANDed with whether the quest was ever activated.

### The faction tiers replaced each other

**Faction tiers replace each other, and that broke the ranks.** The in-game log settles
what no amount of reading the archive had: taking Goblin Blooded prints *"-10 modifier to
Sneak, -10 to Poison Resistance, -10 to Carry Weight"* -- Goblin Chum's whole package being
withdrawn -- and then applies Blooded's. A character holds one faction, not a stack.

Two bugs fell out of that. Every tier granted `+1 Goblin Rank`, so promotion removed the
old `+1` and added a new one and **the rank never exceeded 1** -- which is precisely why the
Crossroads contract kept refusing players who had earned it. The gates were correct; the
number they read was not. Each tier now grants its own number: 1, 2, 3.

And because the previous package is withdrawn, each tier has to be a strict superset of the
one below or promotion is a demotion. Champion granted Barter +6 against Blooded's +8 and
dropped Blooded's disease resistance entirely. The tiers now escalate the way vanilla's
Templar line does -- melee 4, then 8, then 12, each keeping everything beneath it:

| | Chum | Blooded | Champion |
|---|---|---|---|
| Sneak | +10 | +18 | +30 |
| Barter | -- | +8 | +14 |
| Poison Resistance | +10 | +20 | +35 |
| Disease Resistance | -- | +10 | +10 |
| Carry Weight | +10 | +10 | +30 |
| Agility | -- | -- | +1 |
| **Goblin Rank** | **1** | **2** | **3** |

Each tier grants the **running total** of everything below it, so replacement produces the
same character a stack would have. Moving the bonuses onto the perks would stack genuinely
-- perks accumulate and cannot be removed -- but **no shipped title perk grants a bonus**,
all 13 of vanilla's are pure text, and the behaviour that would carry them is named
`...WhenSelected` on a perk the player can never select. Faction bonuses are confirmed
working in play; that path is not, so the arithmetic route wins on evidence.

**Confirmed in play.** Standing climbs 1, 2, 3 across three services, and the disease
resistance survives promotion to Champion -- so both halves landed: the escalating grant
that makes the rank equal the tier, and the cumulative totals that stop a promotion taking
something away. This was the longest-lived defect in the project: it made the Crossroads
contract refuse players who had earned it, and I spent three sessions checking gate
thresholds, branch mappings, name resolution and save snapshots before a screenshot of the
in-game log showed the tiers withdrawing each other.

**Vanilla has the identical defect.** Templar Squire, Warden and Paladin all grant `+1
Templar Rank`, so vanilla's own `Rank > 2` gates can never fire. Fixt inherited this by
copying the shipped pattern faithfully -- which is the lesson worth keeping: a pattern
being vanilla's does not make it a working one.

One thing that cannot be fixed the same way: the titles stay in your perk list as you rise,
so a Champion still shows Goblin Chum and Goblin Blooded. There is no remove-perk action in
the engine -- `CGiveCharacterPerkAction` exists and nothing withdraws one -- so the three
read as a record of what you earned rather than a single current rank.

### Esteban's death went unnoticed

The contract paid nothing, the quest never completed, and the Templar initiation never
failed. All three consequences hung on a destroyed script installed by appending an action
to Esteban's generator -- and a generator's `After Action` runs when it *spawns* the
entity. On a character who had already visited the Crossroads it had therefore never run,
and vanilla gives Esteban no destroyed script at all, so there was nothing underneath it.

Two fixes failed before the cause was found, and both were reasoning errors worth keeping:

1. The first put the check on Esteban's interaction in `Crossroads.zax`. Map entity data is
   snapshotted into a save the first time a level is entered, so a map edit can never reach
   an existing character -- a rule already documented in this project and ignored while
   writing the fix.
2. The second moved it into the dialogue, where it *is* re-read at conversation time, but
   asked `CCheckExistenceAction`. **A killed NPC leaves a corpse, and a corpse exists.**
   The test stayed true after death, so the negation never fired -- on a new game either.
   This is also the likeliest reason the destroyed script never fired: killing is not
   destroying.

`CIsAliveAction` is the question that was actually meant, with 349 uses in the shipped
game and the same two fields. The patrol leader now asks it, and dispatches
`Esteban Death Consequences.can`: set `Esteban Dead`, and fail *Investigate the goblin
menace*, *Slay the Giant Wasps* and the Templar initiation's *Seek out Guard Esteban*.
Every part is idempotent -- the flag does not accumulate, the quest actions are
`...IfActive` -- so it is safe alongside the destroyed script, which stays for the
fresh-spawn path.

### The rank titles named the wrong deed

Accumulating standing broke the titles without anyone noticing. Each perk described the one
route that used to grant it, so killing the river dryad awarded a title saying you had
butchered a woodcutter for his eyes. The general shape is worth stating, because it will
recur: **a description that names an event, attached to a state reachable by several
routes, will eventually describe something the player did not do.** All three now describe
the standing. Rank 3's was vanilla's own text and is overridden.

### Six blank replies in the Goblin Girl's tree

An empty reply with no target, no action and no default flag renders as a clickable blank
that does nothing. Only 0.5% of vanilla's 10,915 replies have that shape, so it is a defect
rather than a convention -- the real close idiom is an empty reply *with*
`Is Default Reply=1`, which node 250 in the same tree uses correctly.

Two of the six had working replies beside them and were deleted. The other four were the
only exit from their node, so deleting them would have left the conversation with no way
out; they are now proper closes. This is exactly the class of repair Fixt exists for, and
all six were vanilla's.

### The Goblin Girl did not remember you

Her greeting keys on `Met the Goblin Girl`, written the first time you speak to her, and on
a fresh character it was not taking effect -- so every visit was her first. The write used
the minority option on all three fields vanilla varies for scripting variables:
`permanent=1` where 47 of 50 use 0, `Player#1-9#` where 34 use `$Instigator`,
`accumulation=0` where 31 use 1. Each is individually legal, which is why nothing caught it.
It now matches the dominant pattern.

What settled it was shipping a diagnostic rather than theorising: a reply on her
first-meeting node, visible only when the flag was set, so its presence on a second visit
would separate a failed write from a failed read. That is the habit worth keeping from this
release -- three earlier bugs cost multiple cycles each to inference that a single
measurement would have ended.

## 0.1.0 - "The Horde"

**The thesis.** Lionheart's most developed evil content is the pro-goblin thread, and it
feeds nothing. There is no faction, no rank, no standing, and no side of the war to be on -
and the settlement answers to exactly one skill. 0.1.0 makes the goblins a faction you can
join, gives joining a price, makes the camp notice which side you picked, and gives it more
than Speech to notice you *with*.

**What is already there.** Measured against `data.dat.vanilla.bak`:

- **16 dialogue trees, 282 nodes, 460 replies, 67 of them gated (14.6%).**
- **15 quests** across Barcelona and the Wilderness, near-symmetrically paired - every
  goblin leader already has a serve-them quest and a kill-them quest.
- **Both capstone perks are written and awarded** - `Goblin Champion` and `Goblin Slayer`.
- **Full voice acting for Grumdjum** - 40 `.ogg` files including companion quips, rejoin
  lines and hurt lines.
- **A camp-wide allegiance switch already exists.** `Make Goblins Hostile Relay` is used
  **250+ times across 17 maps** and from 5 dialogue trees and character templates. The
  goblins can already collectively turn on you. What is missing is the other direction.

**What the 67 gates actually read.** This is the problem in one table:

| Gate | Uses |
|---|---|
| Speech (7 thresholds, 15 to 55) | 19 |
| Quest state and relay flags | 38 |
| Faction (`Inquisitor IS`, `Templar IS`, `NOT Templar or Inquisitor`) | 6 |
| Barter (20, 35) | 2 |
| `IN >= 4` | 1 |
| `ST 8+` | 1 |

A whole settlement, and 19 of its 23 skill checks are the same skill. The six faction
checks are `GoblinKhan` asking who you serve - the right question, asked by exactly one
character, with no goblin answer available.

### The four strands

Each strand ships something visible on its own, and they are built in this order.

#### Strand 1 - Fix

The goblin thread's own dead ends. Four true dangling targets (case-only mismatches
excluded - see *Corrections*):

| File | Node | Broken target |
|---|---|---|
| `Resources/Levels/1 Barcelona/Dialog/Gate District/Goblin Sapper.DialogTree` | `20 ate a poet` | `5 goobye` (typo for `5 goodbye`) |
| same | `30 goblin name` | `5 goobye` |
| `Resources/Levels/Wilderness/Dialog/GoblinVillager.DialogTree` | - | `100 avoid dinner` |
| `Resources/Levels/Wilderness/Dialog/Guard Esteban.DialogTree` | - | `5 Goodbye` |

Esteban is in because strand 3 turns him into a target; a contract on a man whose farewell
dead-ends is a poor advertisement.

#### Strand 2 - Restore

`GoblinGirl` (19 nodes, 28 replies) and `GoblinGuards` (4 nodes, 3 replies) ship in the
archive with **zero map references** - written, finished, never placed. They go into
`Goblin Warrens`.

- `Resources/Levels/Wilderness/Dialog/GoblinGirl.DialogTree` - fix `250 Rejection` and
  `290 follow 3`, and the two `no way out` nodes `220 Liver` / `225 Liver pie`, as part of
  placing her rather than afterwards.
- `Resources/Levels/Wilderness/Dialog/GoblinGuards.DialogTree`.
- New character templates under
  `Resources/Levels/Wilderness/Character Templates/`, following
  `Goblin Grumdjum.can` and `Goblin Lieutenant.can`.
- Placement in `Levels/Wilderness Maps/Goblin Warrens.zax`. The
  `marco-the-pickpocket` mod is the proven recipe for placing a new NPC.

Her node IDs already describe the design - `1 First time PC enters village`,
`2 PC Enters the village again, before completing any quest`, `5 Give me some sugar` ->
*"you'll have to prove yourself"*. That last one wants a rank gate, which strand 3
provides, so she is built before it and wired after.

#### Strand 3 - Enhance: the Horde as a faction

**3a. The faction records.** Three files on the `Saladin Aswaran` pattern, each granting
concrete benefits and incrementing its own rank counter:

- `Resources/Factions/Goblin Chum.Faction` - the vendor's own word for a friend
- `Resources/Factions/Goblin Blooded.Faction`
- `Resources/Factions/Goblin Champion.Faction` - the perk of that name already exists and
  is already awarded; the faction record is the rank behind it
- `Resources/Derived Character Attributes/Uber Perks/Goblin Rank.DerivedCharacterAttribute`

Benefits should be goblin-flavoured rather than a copy of Saladin's melee package: Sneak,
poison resistance, carry weight. Each record grants `+1` to `Goblin Rank` with
`Allow Accumulation=1`, and each tier's benefits are written as **increments on top of the
last, not as tier totals** - see *Ranks accumulate* below.

**3b. The gates.** `Resources/Dialog/Requirements/Monster Races/Goblin IS.can` already
exists and tests the player's *race*. Do not reuse it. New files under
`Resources/Dialog/Requirements/Factions/`:

- `Goblin Horde IS.can`, `Goblin Horde Rank 2+.can`, `Goblin Horde Rank 3.can`
- `NOT Goblin Horde.can`

**3c. The way in.** Hrubjub, the goblin scaling the Barcelona wall, is the entrance and
almost nobody finds it - the whole path hangs off one reply behind a question about a
corpse. Two changes to `Goblin Sapper.DialogTree`:

- a second entry on `1 Start Conversation` or `60 used speech`, so the option survives a
  player who did not ask about the body;
- an onward pointer on `100 completed quest` naming the Warrens and the Khan. He is a spy
  with every reason to tell a useful human where to report, and without it rung one of the
  ladder leads nowhere.

Completing `Spy for Hrubjub the Goblin` assigns rank 1.

**3d. The price.** The Crossroads goblin patrol gets to make the opposite offer to
Esteban's. `Goblin Patrol Leader` already has a node that reacts to having taken Esteban's
contract (`500 goblin confrontation`); it gets a rank-gated variant offering the
counter-contract instead of a fight. New quest, one gated node variant, and rank 2.

This is the strand's centre of gravity, because it is the first goblin choice with a
visible cost: `LordJavier` checks completion of Esteban's tasks three times, so killing
him closes a Knights Templar rung. Esteban is already written as someone you can fall out
with - `Crossroads.zax` holds `piss off esteban`, `Esteban Sends you to jail` and
`Esteban mad cam` - so this does not fight his characterisation.

**3e. The exclusivity.** Torquemada's `Slay the Goblin Khan` and the Khan's own contracts
currently do not notice each other - checking every `CSetQuestSatusToFailed*` against the
goblin quests finds **zero links**, in a game that uses the action 239 times elsewhere.
Wiring the mutual failure is the smallest change here and the one that turns a checklist
into a choice.

**3f. The reactivity pass.** Rank-gated variants across the trees that already exist. The
skill and attribute dimension is strand 4; this is standing only.

| Tree | What it gains from rank |
|---|---|
| `GoblinEntranceGuard` (10/19) | Recognition at the gate. The first place standing should be legible |
| `GoblinVillager` (55/31) | The camp's ambient voice, gated on rank rather than Speech alone |
| `GoblinKhan` (41/77) | Already asks `Templar IS` / `Inquisitor IS`. Add the goblin answer |
| `Rakeb` (30/63) | Whether the shaman treats you as a client or a rival |
| `GoblinVendorHub` (3/4) | Chum prices for a chum |
| `GoblinGirl` | `5 Give me some sugar` -> the "prove yourself" gate she was written for |

**3g. Karma.** Harvesting a man's eyes and liver for a goblin shaman currently moves
nothing, while killing the Barmaid does. One modifier per choice, and karma is a live
system that feeds the ending selector directly.

#### Strand 4 - Check

The camp answers to one skill. Nineteen of its twenty-three skill and attribute gates are
Speech; the other four are two Barter, one `IN >= 4` and one `ST 8+`. Strand 4 is the
build-reads-the-world half of the release, and it is deliberately a peer of the faction
work rather than a garnish on it.

**Most of it costs no new `.can` files.** The gates already exist in the archive and are
referenced by nothing at all:

| Ready-made gate files | Count | Uses in the shipped game |
|---|---|---|
| `Lockpick moreequal 10` .. `95` | 18 | **0** |
| `Schmooze 4..10 greater or equal` | 7 | **0** |
| `Outwit 5..10 greater or equal` | 6 | **0** |
| `AG 1-3`, `4-6`, `7+`, `8+`, `10+` | 5 | **0** |
| `EN` (same five) | 5 | **0** |
| `LK` (same five) | 5 | **0** |
| `Sneak moreequal 10..35` | 5 | 3 |

**46 finished requirement files that nothing in Lionheart reads.** Agility, Endurance and
Luck have never gated a line of dialogue in the shipped game. 0.1.0 can be the release
where they get their first.

**`Outwit` and `Schmooze` are the developers' own names for this idea.** Both are
pass-through derived attributes - `Outwit` is `(IN) Intelligence` unmodified, the file
behind the `Schmooze` gates is `(CH) Charisma` unmodified - built so a writer could say
"outwit him" instead of "IN 7+". They wrote the gate files and then never used one.

And the fossil is in the goblin thread itself:
`Grumdjun Dryad talked to NOT killed Player high Outwit.can` **does not test Outwit.** It
tests `Speech >= 20`. Somebody meant to gate Grumdjum's dryad branch on intelligence,
named the file for it, and shipped Speech. Strand 4 finishes that thought.

**Where the checks go.** Each of these is an existing scene that currently reads nothing
or reads only Speech:

| Where | Check | What it does |
|---|---|---|
| `Crazy Goblin Trapped Conquistador` (18/25, **0 gates**) | `ST 8+`, Lockpick, `Outwit` | He is pinned. Force it, pick it, or work out the mechanism - three ways into a scene that presently has one |
| `Goblin guarding Woodcutter daughter` (14/11, 1 gate) | `Schmooze` / `CH`, `PE` | Talk the guard off her, or notice she is not the only one being held |
| `GoblinVendorHub` / Hub'blub (3/4, **0 gates**) | Barter | A merchant with no Barter check, in a game with 51 Barter gate files. Built as a second `CMerchantAI` entity at a lower `Price Multiplier`, the way `Lope Inventory low`/`high` already works |
| `Rakeb` (30/63) | `Tribal` | The camp's real shaman, and the Tribal tree gates exactly one conversation in the whole game |
| `Goblin Sapper` / Hrubjub | `PE` | Spot what he is actually doing at the wall before asking about the corpse - a second, observation-based way into the entire Horde path |
| `GoblinKhan`, poetry | `Outwit` / `Schmooze` | `XP for flattering Khan` and `Khan told poetry to once` already exist. Rhyming at a goblin king is a Charisma check that writes itself |
| `GoblinGrumdjum`, dryad branch | `Outwit` | Replace the mis-named Speech gate with the check its filename promises |
| `GoblinEntranceGuard` (Speech 40/55) | `Sneak`, `AG` | A second way past the gate for a build that does not talk |
| Slave Pit hut - `trap poly on trapped chest1`, `fire pain radius` | Find Traps, `PE` | Placed trap content with no detection check in front of it |
| `Khan Chest` (`Lock Pick Adjustment=40`) | `LK` | Luck's first use in the game: whether the one goblin who might have seen you happened to look |

**Why `Outwit` and `Schmooze` rather than `IN 7+` and `CH 7+` wherever both would work.**
They live under `Perk and Trait Support`, which is what that folder is for: a derived
attribute a perk can add to. Nothing in the shipped game writes to either, so today
`Outwit 7+` and `IN 7+` are the same test - but gating on the derived one means a perk can
later grant the *reading* without touching the stat. That is the "if you are intelligent
enough, **or** have the observant perk, you notice Y" shape, and it costs nothing extra now
to leave the socket open. Use the raw attribute only where no perk should ever substitute -
`ST 8+` to lift the beam off the conquistador is strength, not cleverness about strength.

**The rule for every one of them:** a check adds a route, it never removes one. The Speech
path stays exactly as shipped. This is the correction the design already carries - "not
combat" is as boring as "only combat", and "only Speech" is the same failure in a third
costume.

### Explicitly out of 0.1.0

- **A new goblin area.** The back half needs one more than the Wilderness does.
- **The unfinished evil quests** (`FIND THE RELICS FOR THE DARK WIELDERS` and the rest) -
  Dark Wielder content, not Horde content.
- **`Goblin Champion` requires slaying Raylark and Fenclaw, but only Raylark is in the
  quest text.** Real, and a 0.1.x patch, not a 0.1.0 blocker.
- **Rebalancing goblin combat.** Subtracting enemies changes pacing in ways only play
  reveals.

### Verification

Per the standing rule, nothing is announced as testable until the deployed bytes are read
back. For each strand:

1. **Static** - re-run the dangling-target scan over the shipped mod and assert the four
   true breaks are gone and no new ones appeared.
2. **Faction** - assert each new `.Faction` parses on the `Saladin Aswaran` shape and that
   `Goblin Rank` increments once per record.
3. **Deploy** - `modmanager.py install <path-to-this-repo> <game-dir>` then
   `modmanager.py build <game-dir>`, then byte-compare the loose `data\` mirror and the
   `data.dat` entries against the mod source.
4. **In-game, in one pass** - Hrubjub via the new entry, spy quest, rank 1; Crossroads
   patrol offers the contract; Esteban dies; Templar rung visibly closes; the Warrens
   greet a ranked player differently; Goblin Girl is present and her rejection branch
   resolves.
5. **Strand 4 needs two characters, not one.** The checks are invisible to a build that
   passes everything. Run the pass a second time on a low-`IN`, low-`CH`, high-`ST`
   character and confirm the Speech routes still work untouched and the new ones are
   correctly absent. A check that silently replaced a shipped route is the failure mode to
   look for.

## Corrections to `plan.md` found while scoping this

Three claims in the plan document are wrong and are fixed there:

- **The Goblin Shaman is not a mute character.**
  `Resources/Levels/Wilderness/Dialog/Goblin Shaman.DialogTree` ("Goblin Shaman Yumjum",
  3 nodes, 0 replies) is a **taunt bank** attached to generic shaman monsters across 16
  maps via `CDisplayDialogBalloonAction`, not a conversation that was left unfinished.
  Giving it replies would give every generic shaman in the game a conversation. The camp's
  real shaman is **Rakeb** - 30 nodes, 63 replies, 7 gates, placed in `Goblin Warrens`,
  with his own kill-quest and bounty. The Tribal-magic opportunity belongs to him.
- **Robbing the Khan's chest is already noticed.** `Khan Chest` in `Goblin Warrens.zax`
  fires `Make Goblins Hostile Relay`, triggers `Stealing from Khan relay` and cancels
  sneaking; Rakeb's chest does the same. `Lock Pick Adjustment=40` and `30` respectively.
  The gap is not that theft goes unremarked - it is that the consequence is *binary*.
  There is no graded standing to lose, no Khan who hears you were in his tent, only the
  whole camp going hostile at once. That is exactly what a rank fixes.
- **244 "broken" links are case-only mismatches and the engine tolerates them.**
  `GoblinKhan` sends players to `130 the job` when the node is `130 The job`, and Rakeb
  does it six times to `90 goodbye`. These are traversed constantly in normal play. The
  84-count in the plan already excludes them; recording the evidence so nobody re-counts
  them as work.

## Answered - how factions and merchants actually work

The three questions that were blocking strands 3 and 4 are resolved against
`data.dat.vanilla.bak`.

### Faction assignment works from a dialogue reply

`CAssignFactionToCharacterAction` has **29 uses: 20 in maps, 9 in four dialogue trees**.
Joining from a conversation is the shipped pattern, not the exception. `CedricAlsen`,
`Lord Relican`, `InquisitorRaphael` and `LordJavier` all recruit the player mid-sentence.
The exact shape, from Cedric:

```
Reply Text=Yes, I will join the Wielders.
Go to node ID=110 fashion
Custom Action=CMultipleActionsAction
  Action=CAssignFactionToCharacterAction
    Faction To Assign=Factions/Wielder Conjurer
    Character To assign=$Instigator
  Action=CActionRemoveInventoryItem ...
  Action=CGiveExperiencePointsToAllPlayersAction ...
```

Note the field names: `Faction To Assign` and `Character To assign` - the second has a
lower-case `a`, and the engine will not forgive a corrected spelling. Strand 3c is
unblocked and copies this verbatim.

### Ranks accumulate, and tier benefits stack

All twelve shipped records grant `+1` to their own rank counter with
`Allow Accumulation=1` and `Modification is permanent=1`, and the `Highlevel` gates test
`Rank > 2`. So rank climbs 1 -> 2 -> 3 across three assignments and **the tiers' benefits
add up** - a rank-3 Templar is carrying Squire's `+4` melee, Warden's `+8` and Paladin's
`+12` at once, for `+24`. The three goblin records must therefore be written as
**increments, not tier totals**.

### A faction cannot be lost - so the price has to be a quest, not a demotion

- Zero assignments to the null faction anywhere in the game.
- Zero negative writes to any rank attribute.
- `CAssignFactionToCharacterAction` is the **only** faction-related action class in the
  entire archive. There is no leave, clear, expel or demote action.

`Resources/Factions/!None.Faction` does exist, but it is an empty record - no plug-in
behaviors, blank display name. Assigning it would clear the *title* and nothing else: the
benefits are stamped `Modification is permanent=1`, and rank is a permanently modified
derived attribute rather than a property of the faction you currently hold, so neither
comes back off.

A negative record *is* expressible - `CCharacterModifierDerivedAttribute` takes any
`Constant Value`, including `-1` - but nothing ships one, so it is unproven.

**This settles strand 3e.** The Horde cannot be quit and the Templars cannot demote you,
so the price of joining has to be paid in **closed content**: Esteban dead, his tasks
unavailable, `LordJavier`'s three checks failing, and the mutual quest-failure wiring. That
was the plan already; it is now the plan because it is the only mechanism that exists.

### Merchants are map entities, and swapping them is a shipped pattern

`Hubglubs Store` is not a resource file. It is a `CEntityBase` inside
`Levels/Wilderness Maps/Goblin Vendor Interior.zax` carrying a `CMerchantAI` activity -
`Display Name=Goblin Vendor`, `Price Multiplier=1`, `Time Between Restock=900`, and a
13-entry stock array. There are **59 such entities** across the game and
`Price Multiplier` is hand-tuned from `0.75` to `2.0`.

Better still, the swap pattern already ships: `Lope Inventory low` / `Lope Inventory high`,
and `Vendor 2 Inventory low` / `high` / `especial`. `CDisplayMerchantWindowAction` names
its merchant entity, so a gated reply can open a *different* store.

**Strand 4's Barter work is therefore concrete**: add a second `CMerchantAI` entity to
`Goblin Vendor Interior.zax` at a lower `Price Multiplier` with friendlier stock, and point
a Barter- or rank-gated reply in `GoblinVendorHub` at it. Chum prices for a chum, built the
way the developers built Lope. `Inventory for Shaman` in `Goblin Warrens.zax` is the same
opportunity for Rakeb.

## Open questions still blocking parts of 0.1.0

- **Can a perk write to `Outwit` or `Charm`?** The folder name says yes and nothing in the
  shipped game does it, so it is untested. If it works, the perk-substitutes-for-stat
  pattern is available to every later release; if it does not, strand 4's gates still work
  as plain `IN`/`CH` checks and nothing is lost.
- **Does `Lock Pick Adjustment` on a chest have any dialogue-visible outcome?** Strand 4
  wants an NPC to react to a picked lock. Whether a `.can` can ask "was this opened by
  force, by key, or by skill" is unknown, and the `LK` check on `Khan Chest` depends on it.
