# Lionheart Fixt - the mod, and its releases

Status: **planning the first ship**. Nothing below is built yet.

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
| 0.3.0 | The Knights of Saladin | The second minor faction, all in act 1, and the template is now proven by 0.1.0 |
| 0.4.0 | Cut content into its right home | Titan quest, Guard Pablo, Isabella, the helpful wererat |
| 0.5.0+ | The back half - the Crypt's war, the two new areas, companions | The largest work, and it wants the faction and reactivity templates settled first |

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
