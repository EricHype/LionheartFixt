# Lionheart Fixt - the mod, and its releases

Status: **0.1.0 through 0.38.0 are published.** Every act is surveyed, built and released, and the 0.21-0.24 line is the first work aimed at how the game plays rather than at what was cut from it. 0.6.0 is played only as far as the Juan rescue; **0.7.0 and 0.8.0 are entirely unplayed**, and 0.7.0 changed a late-game promotion for every faction combination. 0.9.0 is scoped below and not started. 0.5.0 was built and never published; its artifact crashes on entering the vault and is superseded by 0.5.1. The sections below are in reverse release order, newest first.

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

## 0.15.1 - one regression from 0.15.0's review pass (fixed, shipped in 0.16.0)

The review pass repaired three canned-expression paths that resolve to nothing. Two were clean.
The third was not: `Gate District.zax` referenced
`Dialog/Requirements/**Requirements/**Faction/Saladin Favored`, and I searched *vanilla* for a
`Saladin Favored` can, found none, and repointed Farshad's gate at `Faction/Saladin IS`. But
`Saladin Favored.can` is **a file this project added in 0.9.0** -- "Saladin content gates on being
a Favored One" -- and it checks for the Dervish or Scholar of the Crescent perks, not mere
membership. The only thing wrong with the reference was the doubled `Requirements/` segment.

So 0.15.0 shipped Farshad's two "Welcome into the Order of Saladin" greetings opening for any
Saladin member rather than an initiated one. The path is now corrected to
`Dialog/Requirements/Faction/Saladin Favored`, which is both resolvable and the gate 0.9.0
intended. **Third instance of the same lesson**: search the mod's own files, not only vanilla,
before concluding a resource does not exist.

## 0.38.0 - Magic Items Now Drop

This one began as "add three wand enchantments to a pool", which would have been three correct edits
achieving nothing at all.

### Magic equipment did not drop in this game

`1 MASTER ALL Items in the game` is the random item generator that real maps draw from --
`04 Maw of the Assasin`, `06 Chamber of Torment`, `07 Dark Temple`, `Cortez Cave`. Walking down from
it, the miscellaneous branch yielded exactly two things:

| weighting | |
|---|---|
| **17** | eight **plain, unenchanted** base items -- Amulet, Belt, Boots, Bracers, Gauntlet, Helmet, Necklace, Ring |
| **2** | `All Scrolls` -> `Scroll selection MAGIC` |

And nothing else. The `*selection MAGIC` cans -- the things that pair a base item **with an
enchantment** -- were reachable for potions and scrolls only. Seven were referenced by **nothing at
all**: `Amulet`, `Belt`, `Bracer`, `Cloak`, `Helmet`, `Ring` and `Bolt`. `Wand selection MAGIC` was
one dead link from the same fate -- drawn only by `All Wands`, which nothing drew from.

So the enchantment half of the loot system was built and never connected. A player found plain rings
and plain helmets, and the 40 enchantments written for those slots were unreachable.

**This also corrects a claim made two releases ago.** `unused-content.md` said 62 of the 65 orphaned
magic recipes were *"redundant duplicates whose enchantments reach the player anyway through
`Generator Combinations`."* That check confirmed a selection can **listed** an enchantment and never
asked whether the selection can was itself reachable. Most were not. The document now records the
chain and the error.

### What was connected, and the one decision that mattered

| | |
|---|---|
| `All Wands` -> `All Misc Items except Potions` | weighting **2**, copying the `All Scrolls` entry's shape exactly |
| **`Wand of Swarm`** into `Wand selection MAGIC` | weighting **5**, matching `Rigor Mortis`, the one other `5 Unique` in that pool |
| new **`All Magic Equipment.can`** | the six orphaned pools at weighting **10 each** -- the same equal weighting the eight plain base items already use |
| `All Magic Equipment` -> `All Misc Items except Potions` | weighting **2**, matching scrolls and wands |

**One intermediate can, not six branches.** Adding the six pools directly at weighting 2 each would
have made magic equipment **12 of 33** -- about 36% of misc drops, against the ~9% that scrolls and
wands each get. Routing them through a single can keeps the shift proportionate:

| branch | share |
|---|---|
| plain equipment | **74%** |
| scrolls | 9% |
| wands | 9% |
| **magic equipment** | **9%** |

All **40** enchantments across the six pools were checked before wiring, and **every one is
implemented** -- real behaviours and modifiers, no shells.

### Two wands deliberately left out

`Wands/Special/` holds three enchantments no pool listed, and they are **not equivalent**:

| | |
|---|---|
| **`Swarm`** -- 5 Unique, 7500 | **complete.** `CPlugInBehaviorWand` plus a modifier touching `Magic Tribal/Offensive/Insect Plague` and `Piercing Damage Resistance`. Summons insects; grants ranged-damage resistance while charges remain. **Wired in** |
| `Fire and Ice` -- 5 Unique, **value 0** | **shell.** 1,036 bytes, **no behaviours, no modifiers.** Promises Fireball and Ice Storm cast together plus 15% fire and cold resistance. None of it exists |
| `Mage` -- 5 Unique, 10000 | **shell.** 1,161 bytes, **no behaviours, no modifiers.** Promises +4 skill points in every base magic skill across all three categories, plus five Lightning Bolts and five Fears. None of it exists |

Wiring a shell would ship a unique wand that does nothing, which is worse than leaving it
unobtainable. `Fire and Ice` carrying **value 0** beside 1,036 bytes of nothing is the giveaway: these
were written as design intent and never built. Restoring them means implementing them from their
descriptions, and `Wand of Mage` as written -- +4 to every magic skill, where the best single
enchantment in the game gives +8 to one -- would be the strongest item in Lionheart by a distance.
That is a design decision, not a restoration.

Same trap as the Templar helm in 0.36.0, and worse: the helm at least had the correct slot.

### Also left alone, on purpose

`Boot`, `Gauntlet` and `Necklace selection MAGIC` are each already reachable from **one specific
map**, so they are narrowly available rather than absent. Changing a rate that functions is a
different decision from connecting something unreachable. `Bolt` and `Arrow` are ammunition in the
same position. All five are recorded in [`unused-content.md`](unused-content.md) -- one entry each if
that inconsistency is worth closing.

### The method failure worth keeping

This is the seventh recorded in `unused-content.md`, and the pattern is familiar: **the check stopped
one link short.** Confirming that `Generator Combinations` reached an enchantment said nothing about
whether anything reached `Generator Combinations`.

It was caught only because wiring three wands into `Wand selection MAGIC` meant tracing what drew from
that pool first -- and the answer was `All Wands`, which had no referrers at all. The rule now in the
document: **trace a chain to something that runs** -- a map, a drop table, a merchant -- not to the
next file that mentions it.

### What needs playing

`WD1`-`WD16` in [`qa.md`](qa.md). **`WD1`** is the find: play act 4 or act 8 and look for magic rings,
amulets, belts, bracers, cloaks and helmets, none of which have ever dropped. **`WD6`** is the balance
row and the one most likely to need adjusting -- magic equipment is 9% of one branch, and that share
is the dial. **`WD8`** asks the harder question: no mojo gating was added, so a Very Rare ring could
appear early. **`WD13`** confirms the two shells never drop.

## 0.37.0 - A Rock Titan of Your Own

The top pick off [`unused-content.md`](unused-content.md), taken one release after the list was
written.

**`Summoned Cans/Monster Summoning Level 4 01/02/03` and `Level 5 01/02/03` are referenced by nothing
at all** in the shipped game. Six cans, each with its own dedicated `.Race` and a working model:

| tier | creature | HP |
|---|---|---|
| Level 4 01 | `Characters/Monsters/Snake Women` | 90 |
| Level 4 02 | `Characters/Monsters/Ogre variant` | 120 |
| Level 4 03 | `Characters/Monsters/Wererat boss` | 90 |
| Level 5 01 | **`Characters/Monsters/Rock Titan Blue`** | **170** |
| Level 5 02 | `Characters/Monsters/Desert Beast` | 120 |
| Level 5 03 | `Characters/Monsters/Sand Spirit` | 120 |

So a Tribal mage's summon ceiling was a **Wolf 03**, forever, no matter how far the skill went. This
is content that was finished and then disconnected -- not cut, not unfinished, just unwired.

### The tier table is not in the skill

`Monster Summoning.Skill` references **no cans at all**. It fires a `Spellcast` relay, and selection
happens in `Spell Projectiles/Monster Summoning Instant Hit Projectile.InventoryItem`, which branches
on `CSkillsNamedExpressionExpression(Monster Summoning, "single")`.

**The two sides of that branch are shaped completely differently**, which is the thing worth
recording:

| branch | shape |
|---|---|
| **single** | a tier ladder on skill value -- `CIsLessThan 50`, `CIsLessThan 100`, else |
| **multi** | **no skill gating at all** -- two sequential draws, a low/mid pool of 5 and a high pool of 3 |

Tier 3 previously covered skill **100 all the way to the cap** -- two thirds of the range on a single
tier, which is itself the clue that the ladder was meant to continue.

### What changed

**The single ladder now continues**, on vanilla's own 50-point spacing:

| skill | summons |
|---|---|
| < 50 | Guard Dog 01, Wolf 01 |
| < 100 | Guard Dog 02, Vodyanoi 02, Wolf 02 |
| **< 150** | Guard Dog 03, Vodyanoi 03, Wolf 03 -- *contents unchanged, now bounded above* |
| **< 200** | Snake Women, Ogre variant, Wererat Boss |
| **200+** | **Rock Titan Blue**, Desert Beast, Sand Spirit |

**The multi high pool grew from 3 to 9**, taking all six new cans. No new threshold there: multi is
already gated behind high skill by the spell's own `multi` expression, and turning that side into a
ladder would be a far larger change for no gameplay gain.

**Tier 4 and tier 5 are clones of the tier-3 block with the can names swapped.** Every tier carries a
`CAddAIAction` that drains mana for upkeep -- the thing that makes a summon cost something -- and
cloning preserves it byte-for-byte rather than rebuilding it by hand. Both new tiers verified at
**3 mana**, the same as every existing tier. A high-tier summon that cost nothing to maintain would
have been the obvious way to get this wrong.

### Three attempts, two instructive failures

**The first assumed the two branches were identical ladders.** They are not, and the assertion that
caught it was a content check -- the second "ladder" turned out to be a 1,304-byte block with no
tier-3 cans in it at all.

**The second got the conditional's fields wrong.** In this game `CIfExpressionAction` takes
**`If Expression`** (not `Expression`), plus `Character to get attributes from`, and carries **no**
`Return failure` tail -- unlike `CConditionalAction`, which does. Reading the first
`CIfExpressionAction` in the file was misleading, because that one is the single/multi branch and uses
a `CSkillsNamedExpressionExpression` condition rather than a skill comparison.

Both failures are the same shape as the ones recorded in `unused-content.md`: assuming a structure
rather than reading a working instance of it.

### What needs playing

`SM1`-`SM14` in [`qa.md`](qa.md). **`SM1`** is the row this exists for -- summon at skill 200+ and see
a Rock Titan. **`SM5`** is the one that matters structurally: watch mana drain while a tier-5 summon
is alive, because if a high summon is free to maintain then the cloned upkeep did not come across.
**`SM3`** confirms tier 3's contents did not move.

And **`SM10` is worth knowing in advance**: all six races carry `Display Name=Black Wolf` in vanilla,
copied from the wolf summon and never renamed, so a summoned Rock Titan is currently *called* a Black
Wolf. That is pre-existing rather than new, and is left for a deliberate fix rather than folded in
here.

## 0.36.0 - The Templar Set

Asked in play: *"what are the other unused items? I didn't know the mine deed existed. We should be
able to find usages for all of them eventually."*

So the first thing this release contains is not content at all -- it is
**[`docs/unused-content.md`](unused-content.md)**, a survey of everything the shipped game defines and
then references from nothing, so the question does not have to be re-answered. The second thing is the
first pair of items taken off that list.

### The survey, in brief

| category | defined | referenced by nothing | genuinely lost |
|---|---|---|---|
| quest items | 14 unique | 14 | **8** (Fixt had already used 6) |
| magic-item recipes | 91 | 65 | **3** -- the other 62 are redundant duplicates |
| monster cans | 478 | **48** | 48, **all with working art** |
| skills | 92 | - | **0** -- nothing was cut |
| summon tiers | 5 | 2 | **2** -- levels 4 and 5, six finished cans |
| perks | 98 | 5 | **5** title perks nothing awards |
| factions | 13 | 0 | **0** |

The headline finds: **`Monster Summoning` levels 4 and 5 are unreachable** -- six cans with dedicated
races and working models, including a level-5 summon that puts a **Rock Titan** on the field -- and
**three of the four `FACTION * Killer` perks are unconnected** while the fourth works and sits beside
them as a reference implementation.

The document also records **the six ways the survey was wrong before it was right**, because those are
more reusable than the results. The worst reported *93 monster cans with dangling races* as a live
vanilla defect; race files ship as **427 `.Race` and 76 `.race`** and the check was case-sensitive on
the extension. The true figure is zero.

### The helm was not unplaced, it was unfinished

`Helm of the Templars` -- *"This battle-weary helm shines with the power of the Templars."* -- is a
`Character Slot Types/Head` item that carried **shield art in every other field**:

| field | vanilla | repaired from `Inventory Items/Helmet.InventoryItem` |
|---|---|---|
| `On the ground` | `Special Items/LionShield_PU` | `Items/PickUps/Misc Items/Helmet_PU` |
| `Basic` / `Better` / `Special` | `Armor/Shield Large Better` | `Items/Inventory Images/Armor/Helmet1` |
| `Catagory for display Grouping` | `Grouping Catagories/Shield Large` | `Inventory/Grouping Catagories/Armor` |

Someone cloned the shield, changed the name, description and slot, and stopped. That is very likely
why it was never placed anywhere, and it is the same signature as the six unreachable summon races all
still being named `Black Wolf`.

`Spirit Templar Shield` needed no art repair at all.

### And then both turned out to be hollow

This only surfaced because the question was asked directly: *what are the stats on the gear?*

**Neither piece had any mechanical effect.** Their only behaviours were
`CPlugInBehaviorPickUpAction` and `CPlugInBehaviorPutDownAction` -- the *sounds* they make when
handled. No armour class, no resistances, no `Wearing a Helmet` flag, no model override, and
`Inventory Addition Group=!None` so neither could ever be enchanted. An item that *"shines with the
power of the Templars"* was **strictly worse than a plain helmet off any thug**.

The first attempt at stats was also wrong, and for an instructive reason: it copied the vanilla item
of matching **encumbrance** -- `Helmet` +3 and `ShieldMedium` +4 -- which prices a unique at mid-tier.
A player reaching act 3 already carries `ShieldLarge` at +7 and can stack a Rare AC addition worth +4
to +6, so the set was outclassed by gear from acts 1 and 2. **Encumbrance is the wrong yardstick.** The
right one is the ceiling for the two slots the set occupies:

| | the set | the best alternative for that slot |
|---|---|---|
| **Helm**, enc 2 | AC **+6**, **`(LK) Luck` +1** | `Helmet` AC +3 is the best base, and `Helmets/Protection` adds **+0** AC -- nothing in the game beats +3 in the head slot |
| **Shield**, enc 5 | AC **+8**, Piercing **+15**, Slashing **+12**, Crushing **+12**, `OneHandedMelee` **+5**, speed -0.03 | `ShieldLarge` AC +7, P15 S10 C10 -- at encumbrance **10** and speed **-0.08** |
| **both worn** | **+4 AC** | the best AC *enchantments* in the game are +4 to +6, rarity 3 Rare |

**Pair total: +18 AC** against the roughly +10 those slots otherwise allow. Base AC is
`2*(Agility+10) + 10 + Evasion`, about 42 at Agility 6, and a body-armour upgrade from Hard Leather to
Hauberk Mail is +10 -- so this is a strong reward for committing two slots, not a rewrite of the
character. The set's identity is **weight**: it protects like a great shield and carries like a medium
one.

`OneHandedMelee +5` sits below the +8 that enchantments give, which is right for armour rather than a
weapon, and it is on the shield because a Templar fights sword-and-shield.

### The set bonus, and the mechanism that nearly got missed

Asked whether a two-piece bonus was possible, the first answer given was **no** -- having searched for
`CHasItemEquipped`, `CCheckEquipped`, `CHasInventoryItem`, `CIsWearing`, "Set Bonus" and "Matched
Set", none of which appear anywhere in the game.

That was wrong, and the correction came from being told so. **The engine does not check equipment; it
counts it.** The **Voodoo** belt and necklace are the shipped reference: each increments
`Number of Voodoo Items` through `CCharacterModifierDerivedAttribute` with `Allow Accumulation=1`, and
the bonus lives in a *computed* derived attribute that reads the total. `Skill Points Per Level` is
literally `10 + Intelligence + (Number of Voodoo Items == 2 ? 1 : 0)`.

No query shaped like a *check* could ever have found a *counter*. Both Voodoo items had appeared in
this release's own orphan list an hour earlier; opening either would have shown it.

The Templar bonus copies that pattern exactly -- a new `Number of Templar Items` counter cloned from
the Voodoo one, and a conditional term added to `(AC) Armor Class`. Structural parity was verified
against `Skill Points Per Level`: one `CIfExpression`, one `CIsEqualTo`, threshold 2.

**That discovery also moved `Goblin Slayer` from last place on the backlog to third**, because the
same realisation turned up `Goblin Kill Counter` -- a derived attribute that is already live and
already written by six shipped files. The perk needs a threshold read, not a mechanism built.

### Where they are

Both pieces are carried by **`Dead Knight Templar 5`**, inlined as full `CInventoryItem` blocks inside
the corpse's `CAIInventory` -- which is how the amulet those corpses already carry is stored, since the
array holds definitions rather than paths. Of the five dead-Templar templates that is the only one
used just **twice**, both in act 3's `02 Hamlet Burned` where Templars died; the others serve 9 to 15
corpses each and would have scattered a unique set far too widely.

Editing the template rather than the map means **no new map entity**, so this reaches any save that
has not yet entered that map.

**Gate 0 caught two faults in the first splice.** The inventory array closes at **4 tabs** while each
item closes at **5**, so a reverse search for a 4-tab brace matched *inside* the 5-tab one and spliced
the new items into the previous item -- the array then declared 3 and held 1. Fixed with `balanced()`
plus the start of that brace's own line, and a round-trip through `resource_format` so the formatting
is canonical by construction.

### Two risks worth naming

**The set bonus edits `(AC) Armor Class`**, a core attribute every character and creature uses. The
conditional returns 0 for anyone without both pieces, and the original Agility and Evasion terms were
verified intact in the shipped bytes -- but `TS12` and `TS13` exist to prove it in play.

**And `+1 Luck` has no unconditional precedent.** Of the 18 `InventoryItem`s using
`CCharacterModifierAttribute`, every one is *conditional* -- `Crossbow` grants +1 Perception only with
the `Sharpshooter` perk. This is the only flat attribute bonus on any item in the game, and Luck is
not cheap: `Fortune`, `CriticalChance` and the Cold, Fire and Electrical resistances all read it. The
field shape is copied from the Crossbow; the unconditional part is new. `TS16` asks whether it feels
disproportionate.

### What needs playing

`TS1`-`TS17` in [`qa.md`](qa.md). **`TS1`** is the find itself. **`TS7`**-**`TS7d`** are the numbers,
including whether removing a piece correctly removes the set bonus. **`TS12`** and **`TS13`** are the
blast-radius rows for the AC edit. **`TS14`** is the calibration question -- compare the set against a
`ShieldLarge` and the best helmet you can find, and if it still feels outclassed the numbers are the
dial.

## 0.35.0 - Caltrops

Asked in play: *"do any enemies lay traps? Is that possible?"*

No, and yes.

### What a trap is in this game

Traps are **static map features**: a `CRenderablePolygon` placed in **44 maps**, carrying two
activities. A `CTouchingPolygonTriggerAI` with `Triggered By Players=1` and every other flag at 0, and
a `CAISecretReveal` that hides the trap until Find Traps beats `Skill Adjustment=15`, then fires
`Found Trap` and attaches a `GetCloseThen Disarm Trap` specifier so it can be disarmed.

The damage is **mojo-scaled** through nested `CConditionalAction`s -- 25-35 at mojo >= 16, 15-25 at
>= 10, else 10-20 -- which is the same progression-aware pattern the rest of the game uses.

Nothing places one at runtime. No enemy lays a trap.

### But 32 cans already carried the machinery

This was the surprise, and it is what made the rest straightforward. The **18 WarGolems** and **14
Undead** -- `Disedira`, `Festering Undead Walk`, `Second Guardian` -- each carry a
`CTouchingOvalTriggerAI` as an activity **on themselves**: `X Radius=125`, `Triggered By Players=1`,
spawning a Fire Circle when the player enters and doing 1-2 damage every 2 seconds while they stand
in it.

So an enemy-attached proximity hazard is shipped, working behaviour. It simply walks around with the
golem instead of being left on the floor.

An earlier pass of this survey reported **all 478** cans carrying trap machinery. That was a false
positive -- `Trap` matches `Wolf Trapper Perk Checker`, which every can's attribute map lists. It is
the third pattern of that shape this session, after the healing one in 0.33.0, and the lesson is the
same: a query that returns everything is a bug in the query.

### And the missing primitive existed

`CCreateEntityFromCanAction` takes **`New Location=$Trigger`** -- it creates an entity exactly where
the creator stands. Vanilla uses it **73 times**, including to drop a quest mana pickup at a trigger's
feet. That is the whole of "lay a trap at my position".

Everything needed was therefore already shipping:

| piece | vanilla precedent |
|---|---|
| spawn at my own feet | `CCreateEntityFromCanAction{New Location=$Trigger}`, 73 uses |
| the trigger | `CTouchingOvalTriggerAI`, on 32 enemy cans |
| the damage | `CActionDoDamage` + `CXRPGDamage`, mojo-scaled, as in every map trap |
| once per enemy | the `CSeriesAction` one-shot, as the Priest's shield and 0.34.0's draughts |
| cleanup | `CDeleteAction`, how vanilla's spawned pickups remove themselves |

### The two questions, answered before building

**Can it hurt other enemies, or the player's companions?** **No.** The map trap and the golem aura
share one pattern: `Triggered By Players=1` with `Anything`, `Player Friends`, `Enemies`,
`Projectiles` and `Companions` all **0**. Since only the player can trigger it,
`Character To Damage=$instigator` can only ever resolve to the player. Copied field for field and
confirmed in the deployed bytes as `(0, 1, 0, 0, 0)`. `CT3` and `CT4` test it in play anyway, because
a trap that killed Fernand would be a serious fault.

**Does it outlive its layer, and does it clean up?** Yes to both. A spawned entity is independent of
its creator, and vanilla's spawnable pickup can uses `CDeleteAction` to remove itself after use. The
patch is `Trigger Only Once=1` and then deletes itself -- with the delete placed **last**, because an
action after a `CDeleteAction` silently never runs.

### What was built

`Resources/Common Objects and Scripts/Fixt Caltrops Entity.can`, cloned from vanilla's spawnable
spirit-pickup can so it carries every field the engine writes, with the template's 32KB mana
specifier replaced by the trigger. `X Radius=55`, `Damage Types/Piercing`, on vanilla's own three
mojo tiers at about half a map trap's numbers -- these are improvised, and a fight can hold several:

| player mojo | caltrops | a map trap |
|---|---|---|
| >= 16 | 12-18 | 25-35 |
| >= 10 | 8-12 | 15-25 |
| below | 5-9 | 10-20 |

**48 cans lay one, each exactly once**, from a `Damaged Script Action` that was empty on every one of
them: **12 assassins** (`Assasin`, `Assasin Bow`, `Assasin Zealot`, `Assasin Master`, three tiers
each) and **36 thieves** (the `Thugs/Theif` and `Sewers/Sewer Theif` ladders in full).

It is laid on **first being hurt** rather than on engage. That is better flavour -- a thief scattering
caltrops to cover itself -- and it keeps the unknowns down, since unlike 0.34.0's draughts no health
gate is involved.

**The patch is visible, and deliberately carries no `CAISecretReveal`.** A dedicated map trap you must
find with Find Traps is fair because it was laid in advance; one dropped mid-fight that you cannot see
would only be a damage tax. Visible is what makes **position** matter -- 0.33.0's healer made target
priority matter, and this makes ground matter. `CT11` and `CT12` record that the hide-and-disarm
machinery exists and was passed over, in case that reads as the wrong call.

### A balance concern, raised once

Forty-eight layers means a crowded sewer room could produce five or six patches at once. Each is
one-shot, small and self-deleting, so it should self-limit. **`CT9`** is the row that will say
otherwise, and the dials are the radius and the damage rather than the number of layers.

### What needs playing

`CT1`-`CT14` in [`qa.md`](qa.md). **`CT1`** is the row this exists for -- wound a thief and watch the
ground. **`CT2`** is the structural one: wound it repeatedly and confirm it only ever lays one, the
same one-shot assumption `PO2` watches. **`CT4`** is the safety row, and **`CT13`** the bark
regression on the 36 thief cans.

And the standing debt is now substantial: **`EH5` and `EH1` from 0.33.0 have still never been played**,
and three releases of enemy behaviour now rest on them.

## 0.34.0 - One Draught Each

Asked in play, right after the enemy healer went in: *"can we give enemies a skill they can only use
once to mimic an item?"*

Yes -- and vanilla has been shipping one the whole time.

### Enemies cannot use items, and never could

Worth stating plainly first, because it is the reason a mimic is needed at all. **No item-use action
class exists in the game data.** `CUseItemAction`, `CUseInventoryItemAction`, `CConsumeItemAction`,
`CDrinkPotionAction`, `CEquipItemAction`, `CApplyInventoryAdditionAction` -- zero files, every one.

An item's effect is **welded to the item**: a healing wand is `CPlugInBehaviorWand` wrapping a
`CPlugInBehaviorLaunchAction` whose payload is `CGiveHealthToCharacterAction`, metered by a `Charges`
expression and fired from the player's inventory screen. Nothing an AI does can reach it. And enemies
carry no consumables -- **no monster can references a potion, scroll or wand**; the 35 that touch
`CGenerateInventoryItemAction` are generating *drops*, which is the opposite direction.

The `Fake Wand Spells` skills look like a way in and are not: `Cure Major Wounds` is an **862-byte
stub** with no oval, no heal amount and no effect body, which is also why `ENEMY Magical Shield`
borrows it as a convenient unlistable parent.

### The one-shot was already there

The Priest's shield is an item mimic and nobody had named it as one:

```
Shoot Completed=CSeriesAction
  [1] CActionSelectSkill -> ENEMY Magical Shield     fires exactly ONCE
  [2] CRandomAction      -> Fire Orb / Spike / Lightning Bolt
  When Done=Repeat Last Action
  Next Action Index=0
```

`CSeriesAction` advances **one item per execution**, and `When Done=Repeat Last Action` then loops the
final item forever. So **anything in a non-final slot fires once**. The same mechanism walks a Mana
Tome down its six declining grants before repeating an *empty* message.

Two things had to be settled before building on it.

**Health gating works.** There is no health-test *action* anywhere -- `CCheckHealthAction`,
`CIsHurtAction`, `CVariableHealth` and `CCheckHitPointsAction` are all zero files. But
**`CExpressionHealthPercent`** exists with **33 uses**, including the `Die Hard`, `Adrenaline Rush`,
`Grace Under Fire` and `Displacement` perks and the Jafar duel, always in one shape: a
`CExpressionAction` wrapping `CIsLessThanOrEqual{CExpressionHealthPercent, CConstant}`. Separately,
`(HP) Hit Points` is the **maximum** and `CExpressionHitPointsRemaining` the **current** -- vanilla
subtracts one from the other to heal to full in the Gate District, which is how the two were told
apart.

**And the series index is per instance, not per can.** `Next Action Index`, `Executed Action`,
`Number Of Times Triggered` and `Has Triggered At Least Once` are all written into the template as
zeroed mutable counters. If the index were shared, only the very first Priest in the game would ever
shield.

### What the veterans carry

The twelve **veteran** English soldier cans -- `Soldier3` and `Soldier4` in all their variants -- now
carry one healing draught each, in a `Damaged Script Action` that was **empty on all twelve**, a free
hook that fires when the soldier is hurt.

| can | max HP | drinks at | restores |
|---|---|---|---|
| `Soldier3` | 100 | 40 | 35 |
| `Soldier3 Tough` | 123 | 49 | 43 |
| `Soldier3 Super` | 148 | 59 | 52 |
| `Soldier4` / `Soldier4 Mace` | 147 | 59 | 51 |
| `Soldier4 Tough` / `Mace Tough` | 173 | 69 | 61 |
| `Soldier4 Super` / `Mace Super` | 206 | 82 | 72 |
| `Soldier4 Bow` | 115 | 46 | 40 |
| `Soldier4 Bow Tough` | 137 | 55 | 48 |
| `Soldier4 Bow Super` | 168 | 67 | 59 |

It fires at or below **40%** health and restores **35% of that soldier's own maximum**, which
self-scales across the ladder rather than needing a number per can, with a `Divine Strength` effect so
the player can see it happen. **Burst damage beats it entirely** -- a soldier killed from full health
never drops below the threshold while alive and never drinks.

`Soldier1` and `Soldier2` carry nothing, and are byte-identical to what they were. That is also the
in-fiction reason: a conscript does not have a draught.

### A structure that was rejected

The obvious build puts the health test *inside* the series, as a `CIfAction` with
`Return failure if the If failes=1` so a failed test does not advance it. **That value has zero uses
in vanilla** -- all **2,526** are `=0` -- so it was avoided rather than trusted.

Instead the test sits *outside* the series. The series only executes when the soldier is already low,
so its first execution is the drink and every execution afterwards lands on an inert `CSucceedAction`.
Identical semantics, and every field value used is one vanilla exercises.

### And the other two Priest tiers

0.33.0 gave `ENEMY Healing` to the base `Priest` alone so that one can could prove the mechanism
first. `Priest Tough` and `Priest Super` now carry it too, preset on **vanilla's own ladder for these
exact cans**: `ENEMY Magical Shield` is 150 / 200 / 250 across the three, so the heal matches it --
about **11-18**, **14-22** and **17-26 HP** per trigger.

Three priests are deliberately excluded. `Priest Near Death` selects no skill at all and is a scripted
one-off. The **Nostradamus Priest trio** is a separate act 5 family that casts the plain
`Magical Shield` and rotates six selections rather than four, so it needs its own pass. And the
**Priestess** line never had a shield.

### A mistake, and why Gate 0 did not catch it

The first build of the draughts sourced each can from the **vanilla archive** rather than through
`lhbuild.read()`, which prefers `files/`. All twelve were already Fixt overrides carrying **13 bark
references** and an attack bank from the bark release, and all of it was destroyed on twelve files at
once.

**Gate 0 passed.** It checks structure, canonical formatting, `Item Count` agreement and line endings
-- none of which notices that content from an earlier release is simply gone. The only reason it was
caught is that regenerating `mod.json`'s file list reported *"added: 0"* where twelve additions were
expected.

The files were restored from `HEAD` and the build now asserts that the bark count is unchanged and
that the only textual difference is the hurt slot itself. `PO7` is the row that proves it in play
rather than in a diff.

### What needs playing

`PO1`-`PO12` and `EH12`-`EH15` in [`qa.md`](qa.md), and **the backlog now matters more than usual**:
`EH5` and `EH1` from 0.33.0 are still unplayed, so this release stacks three priest tiers and twelve
soldier cans on top of an unverified foundation. That is a deliberate trade, but if `EH5` fails then
rather more comes back out than before.

**`PO2` is the structural row**: keep fighting a soldier after it drinks. If it drinks twice, the
series index is not per-instance and this whole mechanism needs rethinking. **`PO4`** confirms burst
damage beats the draught. **`PO7`** is the bark regression. And **`PO10`** is the one nobody can
predict -- a Priest healing soldiers who *also* drink their own draught. That stacking is intended,
but it has never been seen.

## 0.33.0 - The Priest Heals

Asked in play: *"are there any enemy healers? I've never seen that."*

There are none, and the answer is exhaustive rather than a spot check. Across all **478** vanilla
monster cans, the complete set of skills any enemy ever selects is ten entries:

| skill | cans | | skill | cans |
|---|---|---|---|---|
| `Fighting/OneHandedMelee` | 104 | | `…/Ice Javelin` | 13 |
| `Magic Thought/Offensive/Lightning Bolt` | 42 | | `…/Ice Missile` | 11 |
| `…/Spike` | 37 | | **`Defensive/ENEMY Magical Shield`** | **3** |
| `…/Fire Orb` | 28 | | **`Defensive/Magical Shield`** | **3** |
| `…/Static Charge` | 26 | | `Magic Divine/Offensive/Celestial Smite` | 2 |

Eight are damage. Two are a defensive buff. Nothing heals, nothing cures.

An earlier pass of this survey reported all 478 cans referencing healing. That was wrong and worth
recording as a method failure: the pattern matched enemy **drop tables** carrying `Potion Mass
Healing`. Dropping a healing potion is not casting one, and a query that returns *everything* is a
bug in the query rather than a finding.

### Two things blocked it, and neither is an engine limit

`Magic Divine/Defensive/Healing` refuses enemies twice over:

1. A single `CCheckCategoryAction` on `Target Name=$Trigger` checking **`Player,Player Friend`**. The
   skill's area oval actually carries `Trigger Anything=1` -- it catches *everyone* with hit points in
   radius -- so that one category test is the only thing deciding who benefits.
2. Its magnitude reads `CVariableSkill` on the **caster's own** Healing value, with *Output 0 if input
   is below input base=1*. An enemy has no Healing skill, so even fully ungated it would heal **zero**.

The second only surfaced on reading the magnitude expressions, after the first looked like the whole
answer. It is the more important of the two, because removing the gate alone would have shipped a
healer that visibly cast and healed nothing.

### Vanilla already ships the recipe

`ENEMY Magical Shield` is the only enemy-variant spell in the game, and diffing it against the player's
`Magical Shield` gives the transformation exactly -- five changes, 140 differing lines:

| | |
|---|---|
| drop the bookkeeping | the `CAddCharacterModifierToCharacterAction` setting `Player has cast a spell` goes, `Item Count` 4 to 1 |
| flip the oval | `Trigger if Player=1 / Enemy=0` becomes `Player=0 / Enemy=1` |
| drop the category gate | the `CIfAction` wrapping `CCheckCategoryAction` on `Player` is removed outright |
| make it unlistable | `Parent Skill` reparented to `Fake Wand Spells/Cure Major Wounds`, `Image=!None`, `Initial Minimum & Maximum` zeroed |
| make it uncastable | an **always-false** `Display and Cast Requirement`: `CIsEqualTo` of `0` and `1` |

That last one answered a question I would otherwise have had to guess at. The Priest casts
`ENEMY Magical Shield` *despite* it carrying an impossible cast requirement, which proves enemy
selection through `CActionSelectSkill` bypasses display and cast requirements entirely.

`Skills/Magic Divine/Defensive/ENEMY Healing` follows the recipe, keeping the heal's own oval design --
`Trigger Anything=1` with the inner category test flipped from `Player,Player Friend` to **`Enemy`** --
rather than flipping the trigger flags, because that is how this particular skill was built.

**One deliberate departure.** `ENEMY Magical Shield` left all its magnitude expressions pointing at
the *player* skill's name, so on a Priest they read 0 and the race's `=150` preset does nothing but
make the skill selectable. Rather than copy that inconsistency, all **13** self-references here are
repointed to `ENEMY Healing`, so the preset is what the heal actually scales from: `MinHeal` base 3
step 17 and `MaxHeal` base 6 step 24 over an input range of 1 to 300 give about **11-18 HP** at a
preset of 150, and the oval's `Max Times To Trigger=2` allows it twice.

### The carrier was already the mechanism this project was hunting

The last survey of enemy behaviour concluded that 99 of 104 cans select exactly one skill, that no
`CFleeAction`, `CRetreatAction` or `CCallForReinforcementsAction` exists anywhere in the game, and
that the only real lever left was giving an enemy a second thing to do. The Priest already had it:

```
Shoot Completed=CSeriesAction
  [1] CActionSelectSkill  -> ENEMY Magical Shield     (once)
  [2] CRandomAction       -> Fire Orb / Spike / Lightning Bolt
  When Done=Repeat Last Action
```

It shields itself once, then repeats the random picker forever. The heal is a **fourth entry in that
bank**, so roughly one cast in four, and nothing else about the can changes.

Only the **base `Priest`** carries it. `Priest Tough` and `Priest Super` are left alone on purpose
until `EH1` is played -- one tier to prove the mechanism before five more get it.

### Will it reach anyone

The radius is a flat `CConstant` of **200**. The Priest never shares a generator *group* with other
cans -- all 24 of its groups are Priests only -- so this is a question of proximity rather than
composition. Of those 24 generators, **17 sit within 200 of a soldier or golem generator**, median
**135**:

| | distance to nearest soldier generator |
|---|---|
| Crossroads to England | 40 |
| Gate District Siege | 57, 121 |
| Temple District Siege | 84, 100, 112, 192 |
| 02 Hamlet Burned | 119, 121, 140 |
| Crossroads Siege | **308, 311** -- out of reach, heals only itself |

### The one unverified assumption

This is the **93rd** `.Skill` file in a game that shipped **92**, and every character can carries a
`Skill Values` map enumerating all 92 at zero. That map declares **no `Item Count`** -- it is a keyed
map, like `Tree List=CSortList2D` -- so a missing key should default to 0, which is exactly what every
can already holds for every skill it does not use. The race preset supplies the value by path at
spawn, which is how `ENEMY Magical Shield` reaches 150 on a Priest whose can lists it at 0.

That is sound reasoning and not a verified fact, which is why **`EH5` is written to be run first**:
start a new game, fight something ordinary, confirm nothing is strange. If it is, this comes back out.

### Enemies cannot use items, and what that rules out

Asked alongside the above: what about enemies drinking a healing potion or a buff potion? They
cannot, and the reason is structural rather than an oversight.

**No item-use action class exists in the game data at all.** `CUseItemAction`,
`CUseInventoryItemAction`, `CConsumeItemAction`, `CDrinkPotionAction`, `CEquipItemAction`,
`CApplyInventoryAdditionAction` -- **zero files**, every one of them. There is no action an AI could
run to consume something.

**An item's effect is a plug-in behaviour bound to the item, not an action anything can call.** A
healing wand is `CPlugInBehaviorWand` wrapping a `CPlugInBehaviorLaunchAction` whose launch action is
`CGiveHealthToCharacterAction` with `Character to give health to=$trigger`, metered by a `Charges`
expression. It fires when the item is used from the player's inventory. Nothing in an AI can reach it.

**And enemies carry no usable items.** Of the 478 monster cans, **none** references a potion, scroll
or wand. The 35 that touch `CGenerateInventoryItemAction` are generating **drops** on death, which is
the opposite direction -- items leaving the enemy, not being used by it.

The `Fake Wand Spells` skills look like a way in and are not: `Cure Major Wounds` is an 862-byte
**stub** with no oval, no heal amount and no effect body at all. It is a skill-shaped handle the wand's
InventoryAddition points at, which is also why `ENEMY Magical Shield` borrows it as a convenient
unlistable parent.

**But the primitive underneath is reachable, and it matters as a contingency.**
`CGiveHealthToCharacterAction` is an ordinary action taking a target. Fired from a can it resolves
`$Trigger` to the caster, so it can make an enemy **heal itself** -- no new skill file, no 93rd-skill
question, and available to any melee enemy rather than only a caster. It cannot reach a wounded ally,
which is why the area-healing route in this release went through a skill and its oval instead.

If `EH5` fails and the 93rd skill turns out not to be viable, that is the fallback: a self-healing
enemy, built from an action the game already ships, with none of the structural risk.

### What needs playing

`EH1`-`EH12` in [`qa.md`](qa.md). **`EH5` before anything else** for the reason above. Then **`EH1`**,
the row the release exists for: wound a soldier next to a Priest and watch its health go back up.

**`EH3` is the safety row** -- your own Healing must still heal only you and your friends. The vanilla
skill was not touched and is still gated, and that was verified in the shipped bytes, but it is worth
one look.

And **`EH7`** is the question this all came from: fight the same Priest-and-soldiers encounter twice,
once ignoring the Priest and once killing it first. If killing it first is clearly better, that is
target priority -- the first thing in this game that makes *the player's* behaviour change rather
than the enemy's.

## 0.32.0 - The Siege Ran Dry

A player report, relayed: *"during my old playthroughs I noticed that mag builds suffer from lack of
mana during war with England and later on in the game. Possibly add more mana in cavern of
Nostradamus and crypt? Idk about that -- don't remember if it is a issue in these two spots."*

The hedge in that last sentence turned out to be the right instinct. **The report is correct about
the war and wrong about the other two**, and the measurement is what says so.

### Three sources, and two of them were missed on the first pass

Mana reaches the player two ways -- `Spirit N Generator` founts placed in a map, and spirit energy
dropped on death -- and the first survey only counted drops, which made act 3 Montaillou look like
the worst act in the game. Counting placed founts changed the answer. Then counting a third source
changed it again:

| | founts | placed | tomes | **total** | drop rate |
|---|---|---|---|---|---|
| act 1 Barcelona | 182 | 10,070 | - | 10,070 | - |
| act 2-3 Wilderness | 440 | 25,374 | - | 25,374 | - |
| act 3 Montaillou | 129 | 7,171 | - | 7,171 | 11% |
| act 4 Crypt | 171 | 9,733 | - | 9,733 | **94%** |
| act 5 Nostradamus | 122 | 6,895 | - | 6,895 | **97%** |
| **act 6 war with England** | **64** | **4,156** | - | **4,156** | **10%** |
| act 7 English Shrine | 46 | 3,419 | **4,909** | 8,328 | 19% |
| act 8 Alamut | 183 | 14,207 | - | 14,207 | 73% |

**The Crypt and Nostradamus are the two highest drop-rate acts in the game.** Their thin fount
placement is a deliberate trade, not a gap -- the mana comes from kills instead -- so adding founts
there would have re-solved a solved problem. The player's own hedge was right and the suggestion
was not taken.

**And act 7 is a mechanic that exists nowhere else in the game.** On placed mana alone it measured
worst of all at 3,419, which is what it looked like for two passes. Then the `Mana Tome` entities
turned up: **ten of them, only in the shrine's seven maps.** Each is a `CAIInteractionSpecifier` with
`Trigger Only Once=0` over a `CSeriesAction` of declining grants -- 125-150, then 75-100, 50-75,
25-50, 20-30 -- whose last item is a balloon carrying **no mana at all** (`Node ID=03 Empty`), and
`When Done=Repeat Last Action` repeats *that* forever. So a tome is a canteen rather than a font,
worth 170-905 each depending on how many steps it has, and **4,909 across the act**. That more than
doubles act 7 and settles it. Nine ship `Active=1`; the tenth is switched on by `secret area1
trigger` in its own map, so none of it is dead content.

Which leaves **act 6 alone at the bottom of both axes.** Every other act that is fount-poor is
kill-rich and every act that is kill-poor is fount-rich. Act 6 is neither.

### Why act 6 is a 10% act

The drop half has an exact and rather telling shape. Of the 50 `Monster Cans/English Enemies` cans:

| | spirit drop |
|---|---|
| 19 **WarGolem** cans | `5Huge Spirit Charge Drop Action` -- **174, the largest charge in the game** |
| 6 **Priest / Priestess** cans | `4Large Spirit Charge Drop Action` -- 95 |
| **24 Soldier** cans (and `Priest Near Death`) | **none at all** |

The English were not designed dry. Their golems drop the biggest charge in the game and their priests
the second biggest; **the soldiers specifically were skipped**, and the soldiers are the bulk of every
English fight. That reads as an oversight rather than a decision, and vanilla even ships the mechanism
to repair it -- `Chance 1 in 2 Small2 Spirit Charge Drop Action.can` and `Chance 1 in 3 XtraSmall1
Spirit Drop Action.can`, so chance-gated tiered drops are the engine's own idiom.

**It was still rejected, on scope rather than merit.** Of the 52 monster cans act 6 spawns, **not one
is exclusive to act 6** -- every English can is shared with act 3 Montaillou and act 7. A drop-table
edit cannot be confined to the siege: it would land in an act deliberately left alone and in the act
the tomes already fix. Map founts are the only lever that is act-6-only. If a wider pass is ever
wanted, the 24 soldier cans are the better repair, and `MN1`-`MN12` in [`qa.md`](qa.md) carry the note
that says why.

### The starvation is two maps, not the act

| act 6 map | spawns | founts | mana | per spawn |
|---|---|---|---|---|
| **Crossroads Siege** | 427 | 14 -> **43** | 897 -> **3,061** | 2.10 -> **7.17** |
| **Crossroads to England map** | 79 | 1 -> **8** | 95 -> **551** | 1.20 -> **6.97** |
| Gate District Siege | 149 | 19 | 1,077 | 7.23 -- *untouched* |
| Temple District Siege | 154 | 30 | 2,087 | 13.55 -- *untouched* |

**Crossroads Siege was carrying 40% of the act's enemies on fourteen founts.** Gate District and
Temple District were already healthy, so they were left exactly as they were, and **Gate District's
own 7.23 is the target** -- an in-act reference rather than a number invented for the occasion. Act 6
placed mana goes 4,156 to 6,776.

Two decisions about how the founts were built, both of which exist to avoid a mistake this project
has made before:

* Each new fount is templated from the **verbatim vanilla fount block**, so it carries every field
  vanilla writes -- including the `Dynamic Properties` comment that sits *above* `Name=` and that the
  library's `entity()` builder cannot emit. A generated block that carries only the load-bearing
  fields has shipped a defect here before.
* Each is placed **inside an enemy generator's own oval**, which is walkable by construction because
  the engine spawns enemies across that area. That replaces guessing at coordinates, which fails
  silently. Vanilla itself puts founts as close as **6 units** to a spawn point in these maps; the new
  ones run 0-134, well inside its own range.

The edit is **provably additive**: every original byte of both maps is unchanged, with 29 and 7 blocks
inserted into the `Tree List`, which declares no `Item Count` and so needed none bumped. All 36 sit
inside an oval, every model and comment matches its level, and all 36 positions are distinct and
checked against the founts already there.

### What was deliberately left alone

**Act 3 Montaillou** measures 7.6 mana per kill at an 11% drop rate -- worse on drops than the act
that was actually reported. It is left alone, because that figure counts generator groups only and
excludes individually placed named enemies, so the number is not trusted, and nobody has reported it.

**Act 6 health pickups.** All four siege maps carry **zero** `Health N Generate Action` founts, which
is its own anomaly. It is outside what was asked for and is recorded rather than fixed.

### And seven barks that assumed a friend

Reported from play, while this release was being built:

> *"one of the goblin barks is `<he looks for the goblin who was beside him a moment ago>` this keeps
> happening for solitary goblins"*

It does, and the class is wider than the line that was noticed. Searching the bark tree for anything
presupposing a second goblin present -- or recently present -- found **seven** of the 92:

| node | bank | the line |
|---|---|---|
| 32 | rabble | `<He shoves the goblin beside him forward.>` |
| 39 | rabble | `<He checks that someone is behind him before he steps forward.>` |
| 73 | officer | `<He strikes the goblin nearest him and points.>` |
| 79 | officer | `<He does not raise his voice, and the line tightens anyway.>` |
| 82 | officer | *"Hold the line! Hold it, or we all go in a pot!"* |
| 111 | hurt | `<He looks for the goblin who was beside him a moment ago.>` |
| 113 | hurt | *"Not me. Take the other one, take the other one!"* |

**Solitary spawns are the norm, not the exception** -- which is why this reads as a mistake in the
barks rather than bad luck in the spawning. Counting `Quantity to generate max` across every group
that spawns a bark-carrying can:

| can | groups | spawn alone |
|---|---|---|
| `Mongol Goblin` | 64 | **48** |
| `Mongol Goblin Archer` | 65 | **51** |
| `Mongol Goblin Tough` | 55 | 16 |
| `Mongol Archer Village` | 32 | 22 |
| **`Mongol Goblin Hat`** (officer) | 13 | **12** |
| `Goblin Bludjund`, `Goblin Hrubjub` | 1 each | always |

So the officer's *"Hold the line!"* was the **most** frequently wrong of the seven: that can is alone
in twelve of its thirteen groups, and a lone goblin has no line to hold.

**All seven are reworded, not removed.** Deleting them would have thinned four banks for a problem
that is one of phrasing, and the bank size is what keeps 105 distinct lines from repeating. Each
replacement is true alone and still true in a crowd -- the reported one becomes `<He looks around for
help, and takes his time about believing there is none.>`, which is the same beat without the body
that was never there, and the officer gets `<He points, and keeps pointing until something moves.>`,
which is funnier when nothing does.

The bark count stays at 92, every file stays ASCII, and no node gained a second stage direction.

**One thing nearly shipped wrong here.** The first attempt read the tree with `read_text`, which on
Windows applies universal newlines and silently rewrote the whole file from CRLF to LF. Gate 0 caught
it as *mixed line endings* -- the check exists because a re-indent defect shipped a map crash in
0.9.1 -- and the rewrite was redone on bytes, asserting the CRLF count is unchanged at 375 and that
no bare LF survived.

### What needs playing

`MN1`-`MN12` in [`qa.md`](qa.md). **`MN1` is the row the release exists for** and it is a feel
question: play Crossroads Siege as a mage on a save that has never entered act 6, and report whether
you still run dry rather than whether you saw the orbs.

**`MN4` and `MN5` are the leak detectors** -- Gate District and Temple District must feel exactly as
they did. If either is different, something went where it should not have.

And **`MN12` is the engine, not a bug**: a map's entity list is baked into a save on first visit, so
the new founts are absent on any save that has already been into Crossroads Siege. The same caveat
0.31.0 carried for the Ravine Cave.

For the barks, `GB39`-`GB42`. The one that matters is the simplest: **find a goblin fighting alone,
hurt it, and read what it says.** Nothing should refer to a companion, a line, or anyone standing
behind it.

## 0.31.1 - what betraying a Khan is worth

0.31.0 shipped three faults, all found by being asked the right questions rather than by any gate.

### The horde never reacted

You could be Plumjum's Champion and his betrayer at once, and he never learned. The `Butu alliance`
relay stood down *Butu's* goblins and set the act 8 marker; the Warrens, the Mongol Camp, the Khan,
Rakeb and every `Goblin Horde IS` route were untouched.

`Make Goblins Hostile Relay` already existed in **fourteen** goblin maps, fired over a hundred times
in vanilla including from `GoblinEntranceGuard`, `GoblinVillager` and `Rakeb`. The alliance now throws
it in **the Goblin Warrens and the Mongol Camp** by `COtherMapAction`, and deliberately leaves the
outlying villages: the horde is large and news travels slowly.

### The errand could dead-end

`Butu Khan's Poems` could become unwinnable, and the ordering made it likely rather than unlikely --
Weng Choi's rare-books job is an act 1 Gate District errand and the heir does not exist until after
Montserrat. Measured rather than assumed: the turn-in runs `CActionRemoveInventoryItem`, Weng Choi's
two merchant inventories hold **6 and 18 items and no books**, and the Goblin Warrens copy is the only
placement in the game. An earlier QA row claimed the player could buy it back. They cannot.

Vanilla already drew the distinction the scene needed. The quest is called **`Complete Weng Choi's
Book Collection`** and its own text calls him *"an avid collector of unique tomes"*, so giving a dead
Khan's poems to a collector is not the same act as selling them by weight, and the heir cares which:

| | |
|---|---|
| you kept the book | he takes it in both hands and does not open it. Still the best of the three |
| you gave it to the collector | *"A human who keeps words he cannot eat… Then Butu is read in a city that never heard of him, which is further than Plumjum has ever carried anything."* Gated on that quest, so it can only be said if true |
| you sold it | he puts his hand out and **takes the 250 vanilla paid you**. *"I did not pick the number. A human did, and you took it."* |

Three ways to close it, no dead end, and the insult in the third is the price rather than a refusal.

### And the reward was nothing

Siding with the heir paid XP and a cave whose Hidden Treasure is **a single Potion**, against losing
`Goblin Rank`, the Warrens, the Mongol Camp and Grumdjum as a late-game companion. It was strictly
worse than killing him, which is backwards.

**The standing now swaps rather than vanishing.** The goblin bonus was never a title: Fixt's own
goblin factions, modelled on vanilla's `Saladin Aswaran`, apply real modifiers through
`CPlugInBehaviorModifyCharacterWhenSelected` with `Modification is permanent=1` -- a Champion carries
Sneak +30 and poison resistance +35 off the Khan's goodwill.

And it is tiered, because an untiered version made betrayal a free upgrade for a rank-1 player, and
because Hrargrub gains more by taking the Khan's Champion than by taking a chum:

| rank given up | assigned | grants |
|---|---|---|
| none | **Goblin Traitor - Foe** | OneHandedMelee +10 |
| Chum or Blooded | **Goblin Traitor - Bad Blood** | OneHandedMelee +20, Crushing +15 |
| Champion | **Goblin Traitor - Fallen Champion** | OneHandedMelee +35, Crushing +30, Slashing +20, Carry +20 |

The horde pays in sneaking and poison because it is Mongol-trained; Butu's line were never trained by
anyone and only ever had what they killed, so they pay in melee and in not going down. The middle
tier is deliberately **not** a strict improvement -- a Chum gives up poison resistance and carry
weight entirely for melee and armour, which is a different build rather than a better one.

**A whole mechanism was deleted on the way.** An earlier version of this patch stripped the goblin
bonus with sixteen negative modifiers in a `Revoke Goblin Standing.can`, built because the engine has
**no remove-perk and no remove-faction class**. It is gone: `Advance Goblin Rank` branches on
`rank == 0 / 1 / 2` against factions that set rank to an absolute 1 / 2 / 3, and a Blooded player
would read rank 3 if those stacked, so the Champion branch could never fire. Selecting a faction must
replace the previous one's contribution, and the engine takes the bonus back by itself.

That inference is the one thing in this release that static analysis cannot finish. `BU43` settles it
in one look at a character sheet, and is written to ask for the numbers rather than a yes or no.

### A use for the deed, and two that were wrong

`Inventory/Specific Item Cans/Quest Items/Silver Mine Deed` is one of **twelve unique item cans the
shipped game references from nothing**: *"Legal document proscribing ownership of the Silver Mine."*

Two uses were proposed and dropped as **mistimed**: having Eduardo accept it in place of the silver,
and opening the mine with it. Both are act 1 problems, and the deed does not exist until after
Montserrat, so for most players they would answer a question already settled. The mine route is kept
anyway, since it costs nothing and helps a player who delayed -- and it matters more than it looks,
because betraying Plumjum closes the `Goblin Horde IS` route past the foreman and the deed is what
reopens it. A player who sides with the heir is not locked out of the Sacred Scimitar.

Shylocke is not time-locked. He is reachable from act 1 until the expiry door, he holds Shakespeare's
muse as collateral and sues Cortes over a clause in their contract, and a mine deed is his actual
trade. He also opens low, because he is Shylocke:

| | |
|---|---|
| no check | **1200** -- *"Twelve hundred, and I will never visit it."* |
| Barter 40 | **1800** -- *"It pays whether you go or not."* |
| Barter 70 | **2500** -- vanilla's own ceiling for a dialogue payout |

> *"Then it is mine, and the goblins in it are mine, and I shall do what I have always done with
> property I cannot visit. Nothing whatsoever, at a profit."*

### What needs playing

`BU1`-`BU62` in [`qa.md`](qa.md). **`BU43` first**: as a Goblin Champion, write the sheet down, side
with the heir, read it again, and report the numbers. It decides whether the faction swap works the
way this release assumes.

After that, `BU20` (side with him and the act 8 Khan and Grumdjum stay away), `BU49`-`BU50` (the
Warrens and Mongol Camp hostile, the outlying villages not), and `BU59` (the deed reopening the mine
route the betrayal closed).

## 0.31.0 - Butu's Heir

The one goblin vanilla never placed, put to work -- and a mid-game choice in an optional cave that
costs a late-game companion.

### Two things vanilla left on the table

`Mongol Goblin Hat Super` is **placed nowhere in the game**, and its race is the most interesting
statline in the family:

| race | HP | AC |
|---|---|---|
| Goblin Hat | 60 | 125 |
| Goblin Hat Tough | 80 | 150 |
| **Goblin Hat Super** | **250** | **225** |
| Goblin Khan | 210 | 175 |

**The toughest goblin in the game, harder than the Khan himself.** The hat line steps 60 to 80 to 250
where every other goblin ladder steps about a quarter per rung, so it was never a third tier: it is a
boss statline filed under hats, and vanilla used it as one, lending it to `Mongol Goblin Khan` for its
numbers. 0.30.1 gave that can a race of its own, which freed it.

And vanilla names a second Khan, **exactly once in the whole game**, in a flavour line on an item:

> *"Collected by Butu Khan, this book of poetry contains many free verses of Goblin Poetry."*

The `Butu Khan Poetry Book` sits in the **Goblin Warrens** -- in Plumjum Khan's own cave -- and
`WengChoi.DialogTree` will buy it off the player as a rare book, give, check and remove machinery
already written, without anyone ever saying whose it was. A second goblin dynasty exists in the
fiction, its Khan's book is a curio on the floor of the goblin who outlasted him, and the player can
sell his heritage to a human shopkeeper by weight.

### The cave changes hands

Act 1 is untouched: the Khan's goblins, 0.30.0's four posts, the officer alarm, the three-goblin
argument. After Montserrat, entering `Ravine Cave East` flips it once -- deactivate `Khan Goblins`
and `Goblin Cave Post`, delete them and the arguers, activate eight Butu posts and the heir.

Every piece is shipped idiom. **848 generators already ship `Active=0`**, and the
deactivate-and-delete swap is at **101 sites**, among them `Calle Perdida`'s *"RESET MAP for
Invulnerable Cedric"*, which deactivates and deletes `Pedro Generator` and `Generic Wielder
Generator` -- vanilla resetting a map's population, which is exactly this. The gate is
`CWasQuestEverActivatedAction` OR'd over the three Montserrat quests `Brother Montgomerie` hands out;
`Calle Perdida.zax` already uses that class on one of them as a progression gate.

**24 of capacity plus the heir**, against act 1's 93. The point is that it changed hands, not that it
got bigger. The tribe is recoloured `07 Red`, and of the engine's **seventeen hue palettes sixteen are
used nowhere in vanilla** -- only `01 Dark Blue` appears, six times, in `06 Chamber of Torment`. The
heir wears `Characters/Monsters/Mongol Goblin King`, which in the whole game belongs only to the
Warrens Khan and the Rumjun Khan. **He already looks like a Khan, which is the argument he is
making.**

Calibration, measured rather than assumed: act 1's hardest enemy is a `Lava Troll Boss Super` at 111
HP; act 2's is a `Snakebreed Boss Super` at 160 HP and AC **250**, so the heir hits harder and is
easier to hit; and act 3 already fields `Cathar Warden Bearform Super` at exactly 250 / 225 as
ordinary opposition.

### He reads what you did about the Khan

Five ways in, every one from a can or quest that already existed:

| what you did | what he reads |
|---|---|
| killed Plumjum | *"You emptied the chair. I am standing in it. I had six winters of reasons and you did it in an afternoon"* |
| his **Champion** | *"Take the mark off and we will talk about his cave. Leave it on and I will take it off the usual way."* |
| his chum or blooded | *"He gives ranks the way he gives speeches, and both cost him nothing. Butu gave his goblins poems."* |
| cleared the dryad's forest | *"You have killed more of his than I have. I am not fond of you. I am extremely interested in you."* |
| nothing at all | *"He has drawn plans for six winters. Have you seen the plans? They are very good plans."* |

He is pacified at spawn on the Troll Chief and Mine Foreman pattern, so he challenges first and the
250 HP fight is chosen.

### Two quests, and they fork

| quest | |
|---|---|
| **`Butu Khan's Poems`** | his errand. The book is in Plumjum's warren, and `WengChoi` may already have bought it off you; return it and the cave stands down |
| **`The Goblin of Butu's Line`** | Plumjum's contract. Kill the heir and **`Goblin Rank` advances**, invoked through `Advance Goblin Rank` with `CUseCannedActionAction`, the way the Khan's own tree already invokes it |

They are mutually exclusive, and both ends pay -- which they did not in the first build of this
release. It was a boss fight with one untracked errand, and an earlier draft of the plan called
authoring a `.Quest.txt` risky new territory. **Fixt has authored fourteen of them**, including
`Speak for the Trolls` and `Kill Guard Esteban for the Goblin Patrol`, so there was never a reason the
heir's errand should not be tracked. State IDs follow Fixt's own `TRD4K8ZM` convention.

The book check is a one-line requirement can of its own, because
`Weng Choi Have a rare book.can` ORs nine different books with a Weng Choi quest state and cannot be
reused. The heir's death hook sits in `Destroyed Script Action`, the one slot still free on his can,
guarded on the contract having been taken so that killing him on your own account pays nothing.

### The late game remembers

`01 Desert Sprawl`'s `Fixt goblin gate` already decided whether Plumjum Khan meets the player in
Persia and whether **Grumdjum joins as a companion**, on two conditions: you are his Champion, and he
is alive. It now has a third. **Hand the heir the book and neither of them turns up.**

The marker lives in `01 Desert Sprawl` itself rather than the Wilderness, for a reason worth recording
outside this release.

### The door, and what expiry actually does

A spawn point in `3 Montaillou/02 Hamlet Burned` named **`From Crypt or Nostro Portal`** carries
**130 `CExpireMapAction`s**, closing Barcelona, the Sewers, every Wilderness map, Montserrat,
Montaillou, the Crypt and Nostradamus. The engine is blunt: *"Attempting to load expired map...
(--Loren)"*. It fires on returning to the burned hamlet from the Crypt or the Nostradamus portal.

What expiry does was then settled from the save files rather than guessed:

* **`Has Expired` is a per-layer flag, not a deletion.** The mapping and its `Current Temp File` stay
  in `CSwappedLayerFilenameMappingTable`; the engine simply refuses to touch it.
* **Across all 65 saves in the development install, exactly one map has ever been expired** --
  `Slave Pit Exterior INTRO MOVIE`, retired at the start of every game. The 130-map block has never
  fired in any of them, and the furthest-progressed save is in Montaillou with the door still shut.
* `CCheckExistenceAction` **is** a global lookup rather than map-local: vanilla does it across maps
  **124 times**, for instance `Church Interior` checking `Torquemada irritated`, which lives in
  `Inquisition Chambers2`.

So the idiom is sound and the door is narrower in practice than it first looked -- a one-time reclaim
on one specific transition. But whether a *flagged* layer still answers a name lookup is untested, and
Fixt's own act 8 gate reads two markers out of maps that door closes, so `BU22` exists to find out
whether that gate has ever worked.

### The pointer, because otherwise nobody would go

The heir sat in a cave the game never sends anyone to: the Sacred Scimitar needs the silver in
**West**, East has its own entrance off `Scar Ravine`, and the halves connect only by a crystal-node
teleport. Plumjum points the player east himself, from both of his entry nodes, gated on the same
quests that flip the cave -- and **never says the heir's name**.

> *"Butu's line were nobodies when I was young and they are nobodies with a cave. He has my east rock
> and my shiny and he tells my goblins that I draw maps."*

### Corrections carried in this release

**0.30.0 claimed the officer alarm scales itself.** It does not. `Max Party Mojo` is a threshold and
the engine picks the group the party falls *under*, so Ravine Cave East's top group opens at a party
mojo of about **11**, not 50 -- which act 1 parties reach. The tiering makes officers uncommon; it
does not gate them behind strength. The twelve-creature worst case stands.

**0.30.1's QA described the cave wrongly.** `Ravine Cave East` is not behind the mine, and `GB30` told
a tester to fight in from a passage that does not exist.

**Found and not fixed:** vanilla's own `GoblinKhan.DialogTree` points at a node `130 the job` that is
not in the tree. One dangling reply, vanilla's, left for `reachability.py`.

### What needs playing

`BU1`-`BU28` in [`qa.md`](qa.md). **`BU2` needs a save that had not entered `Ravine Cave East` when
the mod was installed** -- the snapshot rule cuts the wrong way here, because the players most likely
to walk back in are the ones who were there in act 1. **`BU20` is the row the release exists for**:
side with the heir and the act 8 Khan and his companion stay away. And **`BU22`** settles whether the
older act 8 markers were ever readable at all.

## 0.30.1 - what the combat log calls people

Repair only, from a player report: **Fernand Desoto is logged as "Sailor" when he takes damage.**

### The log names a creature by its race, not by itself

The line is `<Attacker> hit <Defender> for ...`, and the defender's name comes from the **race**. All
**753 cans** in the game say `Display Name=unnamed` and **not one sets a real name**; **58 races** do,
which is why a wolf reads *Black Wolf* rather than *Wolf Black Super*. When a race leaves the field
empty the engine falls back to the race's own name -- so `Races/NPCs/Sailor` produced "Sailor", and a
companion who fights beside you for most of the game was labelled by his costume.

`CSetCharacterDisplayNameAction` exists in the exe and is used **zero** times in all of vanilla, so
there was no runtime route to take; the fix is the mechanism 58 vanilla races already use.

### Twelve characters were wrong, and the sweep is what found eleven of them

| who | was logged as | now |
|---|---|---|
| Fernand Desoto | **Sailor** | Fernand Desoto |
| every goblin officer, including the Mine Foreman | **Goblin Grumjun** | Mongol Goblin Officer |
| the Warrens' Goblin King | *Goblin Grumjun* | Goblin Khan |
| Fixt's Rumjun Khan in `01 Desert Sprawl` | *Goblin Grumjun* | Rumjun Khan |
| Grumdjum, the companion | *Goblin Grumjun* | Goblin Grumdjum, with the d |
| Leonardo da Vinci | **River Dryad** | Leonardo DaVinci |
| Galileo, in Barcelona and in `08 Final Encounter` | *River Dryad*, then *Leo* | Galileo |
| the endgame Leonardo | *Leo* | Leonardo DaVinci |
| Sir Roger Templeton | **Knight Templar 5** | Sir Roger Templeton |
| Guard Esteban | *Knight Templar 5* | Guard Esteban |
| Sir Jorge | *Knight Templar 3* | Sir Jorge |
| every dead, burned, siege and bar-patron Templar | *Knight Templar 1* through *5* | Knight Templar |
| an unused English priest race | **Jerk** | Priest |

"Goblin Grumjun" is a copy-paste of Grumdjum's own race name onto all four hat and khan races. It is
reachable in six maps and it became Fixt's problem in particular one release ago: 0.30.0 gave those
officers barks and the post alarm, and `Mongol Goblin Hat Tough` is the Mine Foreman at Ravine Cave
West.

### Shared races are cloned, never renamed in place

This is the whole discipline of the patch. `Races/NPCs/Sailor` is used by **five** cans -- the tavern
drunks, the mute sailor, the ship's crew and two more -- so naming it after Fernand would have renamed
every sailor in Barcelona. It was cloned, and the clone carries its three stat presets verbatim.

The same applied to Galileo, who shared Leonardo's race in Barcelona and the endgame pair race at the
end; to Sir Roger, Esteban and Sir Jorge, who shared tier races with dead, burned and siege Templars
and two bar patrons; and to the Rumjun Khan, who shared `Goblin Hat Super` with a can placed nowhere
in the game. Where a race serves exactly one character it was edited in place instead -- the four
goblin hat and khan races, which Fixt already owned from 0.30.0's damage profile.

**No stats changed anywhere.** Every clone asserts its source's full preset list comes through
unchanged before it is written.

### The regression this nearly shipped

Vanilla already contains `Races/NPCs/Knights Templar/Guard Esteban.Race`, used by nothing. It looks
like exactly the right place to point him, and it is a trap: it presets **AC 1000 and HP 10000**, the
same deliberate invulnerability the game gives children.

Pointing Esteban at it would have made him unkillable and silently broken three earlier pieces of
work -- 0.1.1's counter-contract on him, 0.1.4's `Esteban Death Consequences`, and the 0.10.3 repair
that exists *because* the Templar initiation died with him. That file is instead overridden with
`Knight Templar 5`'s own stats and his name, so the label changes and nothing else does. `DN14` and
`DN15` exist to confirm he is still killable and his death still has consequences.

### Two claims corrected rather than left standing

**Nothing in the game ever read "Jerk".** No can points at that race. The first pass of this sweep
recorded it as placed in four maps, which was wrong -- those cans use `English Enemies/Priest`, whose
empty Display Name correctly falls back to "Priest". It is fixed because the string is one edit away,
not because anyone was seeing it.

**`Mongol Goblin Hat Super` is placed nowhere in the game.** It was one of the sixteen cans given
barks in 0.30.0, so that can's 34 attack lines reach nothing; 15 of the 16 are live. Its race still
mattered, because `Mongol Goblin Khan` was borrowing it, which is how Fixt's own Rumjun Khan ended up
called "Goblin Grumjun".

### What needs playing

`DN1`-`DN18` in [`qa.md`](qa.md). Race and can edits, so they reach creatures spawned after install;
a name still wrong on an old save is worth retrying on a fresh character before reporting, and `DN1`
is written to settle whether display names are resolved at log time or baked into the save's entity
snapshot.

`DN14` is the row that matters most: **Guard Esteban must still be killable.**

## 0.30.0 - The Scourge of the Land

Named from the line that turned out to be the centre of it: *"Nonsense, we are Mongol-trained
goblins, the scourge of the land!"* -- written for a goblin in 2003, fired by nothing until now.

The goblins are the largest enemy population in the game. 780 of spawn capacity across 30 maps, more
than the thieves, soldiers, Snakebreed and trolls put together, and until this release the only major
family with **no barks and no damage resistances at all**. Everything Fixt had done with goblins was
about *not* fighting them -- the Crossroads scouts stood down, the Warrens' Khan and Rakeb made
talkable, Grumdjum restored as a companion, the mine foreman given a tongue. This is the other half.

### GoblinVillager.DialogTree was a bark bank nobody wired

Not a writing job. 55 nodes, and **11 of them are fired by nothing in the entire game** -- no `.zax`,
no `.can`, no tree, vanilla or Fixt -- with ten more reachable in exactly one map each.

The restored lines are referenced at their own vanilla node IDs rather than copied, so vanilla's dead
nodes start firing and no text is duplicated. The IDs are lifted byte-exact, because the Goblin
Warrens crash in the 0.1.x line was a node ID differing by one trailing space.

What was dead: `100 dinner`, `100 take our meal`, `100 take brain`, `500 goblin confrontation 2`,
`500 Fleeing C`, `100 Combat Fight`, `500 wilderness banter 3` (a verbatim duplicate of `banter 4`),
and the three `500 Attacking` nodes. What was nearly dead: `500 Fleeing A` and `B`, which only
`Bounty Hunter Camp` ever fired, and which now play whenever any goblin is hurt.

### The argument written for three goblins and never cast

`500 Attacking A/B/C` are not three interchangeable barks. They are one exchange:

> *"They have butchered our brothers with alarming ease. Perhaps discretion would be the more
> prudent course of action?"*
> *"Nonsense, we are Mongol-trained goblins, the scourge of the land!"*
> *"Yes, Wumjup is right! Muster up your courage and attack! AIIIIiiiiIIII!"*

A coward, a boaster, and a third who sides with the boaster **by name** -- so B had to be Wumjup,
which is also why the rabble's barks keep mentioning a Wumjup nobody ever met. `Drubjub` and
`Lumgrub` are vanilla's names too: they are the two goblins talking to each other in `GoblinGuards`
and `GoblinLt`, trees whose entire content is a pair of goblins gossiping about Grumdjum's poetry and
about who has to go and kill the water witch. None of the three was an entity name anywhere in the
game.

A can only knows itself, so this could never be a can edit. Vanilla's own `goblin attack banter`
relay in `Crossroads` is the pattern, and it is better than the timed burst the plan had assumed:
`CSeriesAction` with `Next Action Index=0` advances **one item per trigger**, the index persisting
between firings -- which is how vanilla gets six banter lines out of one relay. So the trigger is a
goblin dying, and the argument escalates as the fight goes worse: the coward speaks over the first
body, the boaster over the second, the charge over the third. That is the shape the text was written
in, and it was only visible by reading how vanilla staged its own banter instead of inventing a
mechanism.

`Require Success To Advance=0` rather than `1`, so a speaker already dead skips his line instead of
jamming the series on it forever. The death trigger is guarded on the relay entity's own existence
rather than on any goblin's, so which of them died first cannot matter, and it is an explicit no-op in
the other fifteen maps that spawn those cans.

### 105 lines, in banks sized for how often they are heard

0.27.0's shape exactly -- a shared family bank plus a sub-bank per type, about one attack in four,
`Include In Log=0`, over the creature's own head -- but much bigger, because the player hears goblins
more than every other family combined:

| bank | lines | |
|---|---|---|
| rabble | **40** | 18 shared + 16 its own + 6 restored |
| shamans | **37** | 18 shared + 16 its own + 3 reused from the `Goblin Shaman` tree |
| archers, officers | **34** | 18 shared + 16 its own |
| hurt, all tiers | **14** | 10 its own + 4 restored |

The shipped families run 11-14, where a repeat turns up after about five barks; at 34-40 it takes
about eight. A second register was added that 0.27.0 did not have: `Damaged Script Action`, goblins
noticing they are losing, about one hit in six, which is where the restored fleeing lines live.

Shamans bark on attack too, which looked impossible at first because their `Shoot Completed` is
occupied. It is not an attack reaction -- it is a spell *picker*, `CRandomAction` over Spike, Static
Charge, Static Charge -- so the bark bank went in as a fourth item and the spell distribution stayed
proportional.

Seven cans deliberately carry nothing: the Khan, Rakeb and Grumdjum have whole trees of their own, and
the Crossroads Patrol Leader, Goblin Girl and Goblin Guard are ones Fixt made talkable. A named
character must not speak the rabble's lines.

### The damage profile every other family already had

This is the real answer to why every goblin fight felt the same. Animals resist slashing and crushing
38 and take extra from cold; English Enemies are armoured and fold to crushing at **-44**; wererats
are immune to fire; undead shrug off electricity. Across 417 races and nine damage types, the goblins'
19 races were **blank in all nine columns**.

| tier | Slash | Pierce | Crush | Fire | Cold | Elec | Poison | Disease |
|---|---|---|---|---|---|---|---|---|
| rabble, archers | -10 | - | -20 | **-25** | 20 | 15 | 100 | 100 |
| shamans | -10 | - | -20 | **-25** | 20 | **50** | 100 | 100 |
| hat officers | **20** | **20** | 0 | **-25** | 20 | 15 | 100 | 100 |
| Khan, Hat Super, Grumjun, Rakeb | 25 | 25 | 10 | **-10** | 25 | 25 / 50 | 100 | 100 |

**Burn them, do not poison them, and the officer needs a different weapon than the rabble around
him.** Fire is the family signature at every tier, and nothing else in the game is reliably
fire-vulnerable. Poison and Disease are 100 -- carrion and brain eaters -- which is vanilla's own
immune value and also the ceiling: above it the engine *heals* the target, which is what Wererat
Boss's disease 125 has always been doing. The officer tier inverts to armoured, so blades beat him
where clubs beat the rabble, and lightning is wasted on a shaman who throws it himself.

Fire tapers to -10 at the boss tier for two reasons, one honest and one practical: 200+ HP goblins are
thicker-hided, and `Goblin Grumjun` is Grumdjum's race -- he is a restored companion, and a companion
who dies to his own player's fire is a bug report, not a feature.

### The officer calls for help, and the map forced the design

Fixt's own 0.29.0 troll idiom, inverted. A generator's `New Name` applies to **every** creature it
spawns, so a post holding two archers and a Hat cannot name the Hat alone without being cloned --
so the *post* is named and the *officer* is the trigger. `Ravine Cave East`'s four archer posts become
`Goblin Cave Post`, and a struck Hat raises them once.

The Hat appears **only in the generator's top `Max Party Mojo` group, at weight 1 against the
archer's 2**, so about one spawn slot in three is an officer. An earlier draft of these notes went
further and said the alarm therefore scales itself -- no officer for a weak party, no alarm. That is
wrong, and worth correcting rather than leaving: the bound at those posts is 50, but the engine picks
the group whose bound the party falls *under*, and the next one down is 10. The top group is entered
at a party mojo of about **11**, which act 1 parties reach. It makes officers uncommon; it does not
gate them behind strength.
Worst case measured at **12 creatures, once per level** -- against the troll pack alarm that would have
woken 80-94 before it was rescoped. Guarded on the name existing rather than trusting
`CGoToCombatAction` to tolerate a missing target, because `Mongol Goblin Hat Tough` is also the Mine
Foreman next door.

`Respond to calls for reinforcements` is now `1` on all 16 hostile goblin cans; it was `0` on 21 of
23, leaving goblins alone with the Animals and the Thugs while the Undead run it on 88 of 92. One
caveat recorded rather than smoothed over: `CCallForReinforcementsAction` is registered in the exe and
used **zero** times in all of vanilla, so either being attacked calls implicitly and the undead have
swarmed all along, or the field is inert everywhere. Static analysis cannot separate those two; a
playtest can, and it is harmless under both.

### Two Wilderness scenes that had exactly one solution

**The hostage north of the Crossroads.** A goblin holds a woodcutter's daughter and vanilla offers only
ways to save her. She can be handed to the Khan now -- two routes, one gated on Horde standing and one
that earns it, the second tagged `<Lie>` on vanilla's own convention. Both grant the `Child Killer`
title and -50 Karma. Her father is given a failure state he can actually reach, and he can tell the
difference: the lie is a lie to *him*, and the Khan has a line waiting when you next stand in front of
him. The goblin is disposed of with node 70's verbatim 1752-byte disposal, because leaving him standing
after the handover is exactly the kind of thing that ships.

**The silver mine.** The Sacred Scimitar is a Knights of Saladin initiation step and its first task had
one solution: kill the cave. One source of magnetized silver exists in the whole game, no merchant
sells it, `Ravine Cave West` had zero dialogue trees, and Eduardo closes every alternative in his own
voice. A foreman now holds the mouth with the archer post around him, bows up and not firing, and
there are four ways past him -- Horde standing, Barter 40, Speech 40, Schmooze 7 -- plus an ungated
demand refused with a warning rather than a fight, so the routes are discoverable. The three deeper
posts stay hostile until a parley succeeds, so a player who attacks gets the cave exactly as vanilla
built it. Negotiation moves the guards, never the ore.

### One repair, found by checking my own work before reusing it

**`CActionSelectSkill` is not a no-op.** The bark banks pad their `CRandomAction` with it so that only
one attack in four speaks, and that padding is inert *only when it selects the skill the creature
would have used anyway*. Vanilla uses the same action in the same slot as the real mechanism for
choosing the next attack: `Priest Super` casts its shield, then randomly picks Fire Orb or Spike.

0.27.0 and the Snakebreed pass gave `Skills/Fighting/OneHandedMelee` to **21 archer cans whose races
do not preset that skill at all**. `Soldier4 Bow Super` has Ranged 97, no melee rating, and three of
its four attack slots told it to select melee. The trolls were already correct, having been given
`Ranged` because trolls throw. All 21 now resolve the filler from their own race's primary skill by
lookup rather than from an authored constant.

### What needs playing

`GB1`-`GB38`, `MF1`-`MF15` and `GL1`-`GL18` in [`qa.md`](qa.md). Can and race edits throughout, so
every goblin row needs a save that has **not** entered the area; `Ravine Cave East`, `Ravine Cave West`
and `Scar Ravine` are map changes and need the same.

Three rows carry the weight. **`GB34`**: the three balloons must appear over three *different*
goblins -- if they stack over one, `Name of Position` is not resolving by name and the exchange has
failed. **`GB19`**: count the goblins that answer the officer and report the number, because the
budget is 12 and the troll alarm had to be rescoped after exactly this measurement. **`GB25`**: does
anything actually answer a call for help, which settles a question static analysis cannot.

## 0.29.0 - What the Trolls Say

Numbered a minor rather than 0.28.3 deliberately: the release carries a new bark family,
regeneration and a restored effect alongside the repair, and a patch number would misdescribe it.
The crash leads anyway, because it has been shipping since 0.13.0.

### A player found a crash we had shipped 27 times

> Invalid class type -- Tried to use an unknown class "ClsQuestStatusCompletedAction" for a "Action"
> (CAction). Last file opened = "Resources/Levels/1 Barcelona/Dialog/Temple
> District/GrandInquisitor.DialogTree:Node:Reply:Custom Requirement:Operand2:Operand1"

The report was accurate and the class name in it is only disguised by the crash dialog's font, where a
capital I renders as a lowercase l. The file named `CIsQuestStatusCompletedAction`. No such class
exists.

`CIsQuestCompletedAction` is real and takes exactly one field, `Quest=`, which is exactly what all
three sites already carried -- so **only the name was wrong**. It reads like a blend with
`CSetQuestSatusToCompletedAction`, whose "Satus" typo is vanilla's own, and the neighbourhood is
genuinely treacherous: `CIsQuestStateCompleatedAction` is also real, also misspelled, and takes
different fields.

Introduced in **0.13.0** and present in **27 tagged releases**, through 0.28.2. It survived because the
three sites are the Grand Inquisitor's *return* nodes gated on a Wilderness quest -- `2 Irritated
Return Dialogue`, `3 Return Dialogue` and `5 Favored Return`. A player has to get that far and then
come back, and the unplayed backlog is exactly where that kind of path hides.

### Gate 0 gains A0.15, and why nothing else caught it

Every `=CSomething` must name a class the engine registers. The authorities are the C-prefixed strings
in `Lionheart.exe`, which is how the engine registers them, plus every class vanilla's own data uses.

The tree parsed, round-tripped byte-exact, had balanced braces, no dangling targets, correct blank
lines before every `Requirement=`, and the right field set for the class it *meant*. Every existing
gate passed. Class names had simply never been checked. The whole repository was swept and this was
the only genuine offender.

Two details the check had to get right. Quest state IDs are written `State=CHF3M8QW`, which a naive
regex reads as a class, so they are excluded twice -- by key, and by requiring a lowercase letter,
which every real CamelCase class has and no state ID does. And the first version cost 9.3 seconds,
more than the rest of Gate 0 combined, because a leading `[^\r\n=]*` backtracked over every line of
every `.zax`; the field name is now recovered only when reporting a failure, which is almost never.

### The lava trolls

Left out of 0.27.0's barks, and they had more waiting than any other family.

**A voice they already had.** `Shoot Completed` was empty on all six cans, and `Warning Troll.DialogTree`
already gives them two registers. Drones are broken, terse and sometimes wordless; the chief is
fluent, measured and forever counting. 20 lines, 8 shared plus 6 per role, so each troll draws from 14
and no drone speaks in the chief's register. The no-op padding selects `Skills/Fighting/Ranged`, taken
from `Lavatroll Boss.Race` rather than guessed -- naming a skill that does not exist is what made
0.19.0 through 0.25.0 unlaunchable.

**The Troll Stomp was never cut.** `Troll Stomp.mdl16` is referenced by nothing, which looks like a cut
mechanic and is not one. Every troll's projectile already ends in `CAIAreaOvalManager` radius 120,
firing twice, doing Fire 6-16. They have been stomping since 2003 with no visual; the model just had
no caller. Added through `CSpawnEffectAction` on both the hit and graze branch. The proof is that the
troll damage in save logs (5-12) matches the drone projectile's area range of 5-12 exactly -- those
log lines always were the pulses.

**Regeneration, and the constant that decides it.** `Troll Hide for Quinn` calls the troll *"a creature
that closes its own wounds"* and it closed nothing. The units are the whole problem:
**HP per second = HealingRate x 0.1**, from the virtual entity update at `0x0043f7d0` --
`fmul [0x6b9e30]`, float32 `cdcccc3d`, then `fmul dt`. Read with `capstone` and a PE section mapper,
because ReVa would not connect. Without that constant the same value looked like a choice between an
inert attribute and an unkillable boss; with it, drones at 0.6 HP/sec and the chief at 1.0 cost the
player about fourteen points of win rate against the player's own 0.37. Their counter already shipped
in 2003: `Cold Damage Resistance=-15` on every troll race.

**A drone that calls for help, after a correction.** The first build broadcast
`CGoToCombatAction { Enemy Name=Lava Troll }` on damage -- the group call this map already uses. Then
the consequence got measured: 80 to 94 trolls in the pit, on a `Max dist from home` of 4000. Ninety
trolls converging on the first blow landed. Rescoped so a wounded **drone** fetches `Troll Chief` and
nothing else, guarded by `COnlyOnceAction` and a `Troll Peace Keeper` check.

`CCallForReinforcementsAction` was the obvious route and is a dead end: registered in the exe, used
**zero** times in the shipped game, while 698 creatures carry
`Respond to calls for reinforcements=1`. Half the bestiary is listening to a radio nobody transmits on.

### The habit that paid off twice here

Both halves came from measuring a consequence before shipping it. The alarm was built, measured, and
cut back by an order of magnitude. The regeneration was built, pulled when its units could not be
pinned, and restored once the constant was read. Neither correction needed a playtest to find, and
neither would have survived one kindly.

## 0.28.2 - a companion built out of sentry parts

Reported from play, once he could finally be kept: *"Ferdnand's AI often has him freezing in place
after he defeats an enemy. He only seems to react when another enemy attacks him."*

He is the **only companion in the game whose skeleton AI is hand-assembled in a map relay** rather
than inherited from a creature can, and vanilla gave that relay target-acquisition values no other
companion has.

| field | Fernand | Cervantes | across the shipped archive |
|---|---|---|---|
| **Vision Cone** | **90** | 360 | `360` in **1317** uses, `90` in 145 |
| **Max Distance** | **300** | 550 | `550` in **1019** uses, the dominant value |
| Retreat when | 40 | 0 | -- |
| Max dist from home | 500 | 1200 | -- |
| Patrol AI | `CGaurdNearMovingPosAI` | `CScanAreaAI` | -- |

`Vision Cone=90` is the entire symptom. When his target dies the skeleton re-runs acquisition through
`CEntityBehaviorStateSetClosestTarget`, which only considers entities inside that 90-degree arc of his
facing -- so an enemy beside or behind him does not exist and he stands still. `Target shooter if
hit=1` bypasses acquisition altogether, which is why *being hit* woke him, and why the fault read as
apathy rather than blindness. `Max Distance=300` compounds it: he could not see a target at a range
where every other creature in the game can.

**What that cone is actually for.** Its 145 uses concentrate in the siege maps -- Temple District Siege
63, Gate District Siege 35, Crossroads Siege 9 -- guards set to watch one direction. Exactly **one**
creature can in the whole game uses it. It is a sentry value, and a companion was built out of sentry
parts.

Nobody could have met this in vanilla: Fernand was unrecruitable until Fixt restored him in 0.6.0, so
the AI had never run. It took 0.28.1 making him keepable before anyone could watch him fight for long
enough to notice.

Set to `360` / `550`, matching Cervantes and the game's dominant values.

### Two fields deliberately not touched

**`Valid Targets=Enemy`** -- changing it would do nothing. `FUN_005e7e50` derives a companion's target
categories from the player's on join and stores the previous ones as `Original Skeleton Targeting
Flags`. It saves *flags* only, which is also why the cone and the range survive the join and were ours
to set. Cervantes' own template leaves `Valid Targets` empty, which would read as "targets nothing" if
the template value decided anything.

**`Retreat when=40`** -- raised as a balance question rather than repaired, and kept at the project
owner's choice. He breaks off at 40 percent health where Cervantes never flees. `FA4` records that as
deliberate, so the next reader does not file it as the same defect and flatten it.

Needs a **fresh recruit**: the relay writes his AI at join time, so an existing companion keeps the old
eyes.

## 0.28.1 - what the overlay actually does

0.28.0 said Fernand Desoto could be taken back. He could not, and the report came back the same day:
*"check the quick save, still the same with ferdnand."*

The save said the 0.28.0 half had landed -- his own specifier did open `103 fernand waiting` -- and
that he was carrying **two** interaction specifiers:

```
Activity=CAIInteractionSpecifier   Generic Companion Dialog     X Radius=30   Was Triggered=1
Activity=CAIInteractionSpecifier   Distressed Sailor  node=103   X Radius=80
```

The generic one is first, so it wins, and it was still there after three releases -- one
*"companion has joined your party"* in the log against three *"has left"*.

### The overlay is a swap that remembers

"The engine lays its own specifier over the top" is the behaviour, not the mechanism, and the
difference is where the second bug lived. `FUN_005e7870` does not append. It walks the entity's AI
array for an existing `CAIInteractionSpecifier`, **parks it**, and replaces it in place:

```
uVar4 = FUN_005b95e0(uVar6);     // the specifier already there
*(iStack_18 + 0x10) = uVar4;     // parked, to put back on release
...
FUN_005b9600(uVar7, piVar3);     // replaced at that index
```

and only if the entity has none does it append:

```
if ((*(iStack_4 + 0x40) == 0) || (uVar7 == 0xffffffff)) FUN_005b98f0(piVar3);
```

No inference was needed in the end, because the save format names the slot out loud. Cervantes, while
following:

```
Original AIInteractionSpecifier=CAIInteractionSpecifier
{
  Dialog Tree File=Levels/1 Barcelona/Dialog/Temple District/Cervantes
  Node ID=3 Return after release as a companion
}
```

One active specifier, his own parked, and the parked copy opens the **released**-state node. Reading
his *data* rather than his dialogue would have shortened this whole saga by several releases.

### The race, in our own join node

```
Action=CTriggerRelayAction { Relay Name=fernand joins you }          // removes his specifier NOW,
                                                                    // re-adds it after Delay=0.1
Action=CDelayAction { Next Action=CSetCompanionAction ... Delay=0.1 }
```

Both land on the same tick, and two actions on the same delay are not ordered. The companion call won,
found an empty slot, appended the overlay and parked nothing -- so release had nothing to restore and
the generic menu stuck to him permanently. Fixed by making the companion call wait `0.5s`, five times
the relay's delay.

**Cervantes never had a race to lose.** His specifier is standing map data, present before anyone
recruits him, so the engine always finds it, always parks it, and always puts it back. That, and not
the node naming, is the deeper reason he has worked since 2003.

The save taken after the fix matches him field for field: one active specifier at `X Radius=30`, and
`Original AIInteractionSpecifier` holding `103 fernand waiting`.

### A cheaper test, and the method rules

Two new QA cases verify this from the save **immediately after recruiting, with no release needed**:

| # | check |
|---|---|
| FN11 | `Original AIInteractionSpecifier` present, and opening `103 fernand waiting` |
| FN12 | exactly **one** active specifier -- two means the race is back |

Seven attempts on one bug produced four rules worth keeping:

- prove the code path *runs* before redesigning what is in it;
- then verify the **state** it produced against a known-good example -- a fix confirmed on behaviour
  alone is not confirmed, and "acts the same" cannot distinguish two causes with one symptom;
- two actions on the same delay are not ordered; if one must observe the other's effect, separate them;
- read the working example's data, not its dialogue.

### Known limit

A character who recruited him under 0.25.3-0.28.0 has the overlay appended with nothing parked, and
entity state is snapshotted, so that save cannot be repaired -- nothing recorded what should have been
there. It needs a character who has not yet recruited him. A save from before 0.25.7 has a *balloon*
baked in and is likewise beyond reach.

## 0.28.0 - The Hide and the Way Back

Two repairs a playthrough found. Both were invisible to every static check for the same reason: the
data was correct, and something else overrode it at runtime.

### Fernand Desoto, and the five attempts that could never have worked

The project owner reported it a fifth time: *"ferdnand acts the same, see the quick save."*

Rather than redesign the reply a sixth time, a diagnostic went in first -- a `CPrintCombatTextAction`
placed **first** in the reply's action array, which lands in the combat log where `savecheck events`
can read it. It did not appear. Not once in 234 events. The reply was never running.

The same save said why, in its own message log:

```
Companion: <What would you like your companion to do?>
Antonio Gula: Release Companion
```

That is not Fernand's dialogue. `Player Data/Companion AI Interaction Specifier.can` wraps a
`CAIInteractionSpecifier` marked **`Use=Shared Global Instance`**, opening `Levels/Generic Companion
Dialog` node `01 Conversation Start` with `Speaker=$trigger`. The engine lays it over a companion's own
interaction specifier for as long as it follows. So:

- talking to a follower opens **the generic menu**, never the NPC's tree;
- release drops the overlay and exposes whatever specifier the NPC had underneath;
- an NPC's own specifier is therefore **only ever seen while it is not following**.

Fernand's standing specifier pointed at `100 companion banter` -- the *following*-state node, whose
only offer was *"Wait here"*. A released companion was greeted with another dismissal and no way back.

| attempt | what it did | why it failed |
|---|---|---|
| 0.25.3 | gave node 100 a dismiss and a rejoin, ungated | a dismissed Fernand still offered to be dismissed |
| 0.25.4 | gated the pair on a new scripting variable | the variable was never written -- the save proved it absent |
| 0.25.7 | found node 100 was a *balloon* with no reply list and made it a conversation | necessary, and still not enough |
| 0.27.0 | a dedicated released-state node, with specifier swaps fired from canned objects | the swap never ran |
| (unreleased) | the diagnostic probe | **did not fire** -- which was the finding |

All five edited the contents of a reply the player could not reach.

### Cervantes was showing the answer, and it is the opposite of what was built

`0.27.0`'s notes quoted him correctly and drew the wrong conclusion from it. His standing map
specifiers -- seven of them -- point at `3 Return after release as a companion` and
`1500 cervantes leaves party dialogue`. Those are **released**-state nodes. The standing wiring is for
when he is *not* with you, because that is the only time anything sees it.

So the fix is one reference. The `fernand joins you` relay installs his standing specifier on
`103 fernand waiting` instead of `100 companion banter`. The canned specifier swaps are deleted: the
engine already swaps, earlier and more reliably than a reply action can.

Node 100 now offers the same way back, because it is in exactly the same position -- unreachable while
he follows -- so it should behave the same. That silently repairs saves already stuck pointing at it.
A save that recruited him before 0.25.7 still has a *balloon* baked in and needs a fresh recruit;
nothing can be done for those from our side.

### The Lava Troll Hide has been unobtainable by killing since 0.10.0

Also reported from play: *"I'm killing the lava troll boss and all trolls, but I'm not getting a
hide."* Accurate, and no amount of killing would have worked.

0.10.0 put `Destroyed Script Action=CGenerateInventoryItemAction` on all three `Lava Troll Boss` cans,
copied field for field from Iapetus and Lethos. That is correct, and it has been installed ever since.
But the chief is not spawned raw from the can -- `05 Troll Pit.zax` spawns him through a `CGeneratorAI`
whose `After Action` runs `CSetDestroyedScriptActionAction`, described in the executable as:

> "**Changes** the 'Destroyed Action' of any entity on the map to make the entity perform the specified
> action when the entitiy is destroyed or dies"

It replaces. The generator overwrote the can's slot the instant the chief spawned, leaving only the
vanilla bookkeeping -- the `Trolls dead quest` relay and the ambient SFX swap. The hide was dead code
from the day it shipped.

Vanilla settles the replacement reading rather than an additive one: the four Titan bosses carry the
**same** quest item in both their can's `Destroyed Script Action` and their generator's
`New Destroyed Action`, which would hand out two stonehearts apiece if the slots stacked.

The galling part is that the **peace** route already handed a hide over, in two separate nodes, using
exactly the right action. Only the kill route never got it.

Both generators that produce a `Troll Chief` now use `CActionGiveStandardInventoryItem` -- the Titans'
own idiom, 374 uses across the game -- which puts the item **straight in the killer's pack with a
notification**. That also removes a hazard nobody had noticed: the can's `Generate Within Radius=128`
scatters a quest item on the floor, and that floor is a lava pit.

| generator | change |
|---|---|
| `Lava Troll Generator` (the ordinary chief; boss, tough or super by difficulty) | appended to its destroyed-action array, 3 items to 4. Relay and SFX swap untouched |
| `Troll answer chief` (the angry chief, after the field is desecrated) | `CSetDestroyedScriptActionAction` appended to its After Action, 2 items to 3. His hostility reset intact |

One wrong turn is worth recording, because it was the same mistake a second time: the first version of
this fix wrote `New Destroyed Action` as a direct field of `CGeneratorAI`. It is not one -- it belongs
to `CSetDestroyedScriptActionAction` -- so that version would have been silently ignored exactly as the
can was. The parent chain is now asserted on both.

### Gate 0 gains A0.14

For every quest item a Fixt can drops from its own destroyed slot, find the generators that spawn that
can and fail if one overrides the slot without re-offering the item. Negative test: with the map
reverted it names all three cans, the map and the generator; silent once fixed.

Nothing else in Gate 0 could have caught this. The can parsed, round-tripped byte-exact, named a real
item, used a field with 3960 occurrences, and matched a working vanilla boss line for line. Only the
interaction between the can and the map that spawns it was wrong.

### The method rule both halves share

Prove the code path **executes** before redesigning what is in it. Five releases and one dead quest
item were spent on edits that were individually sound and could never run. One probe, placed first,
answers it in a single playtest -- reach for it on the second failure, not the fifth.

## 0.27.0 - What the Thieves Say

Reported again after 0.25.7: he still cannot rejoin. The save says why -- **`Fernand Is Waiting` is
absent**, so 0.25.4's variable was never written once, and the gate that hides the dismiss line also
hides the rejoin line whenever the variable is 0, which is every state except "dismissed through that
exact reply".

### Three attempts, one wrong assumption

All three tried to make **one node** serve both states.

| release | what it did | why it failed |
|---|---|---|
| 0.25.3 | gave node 100 a dismiss and a rejoin, ungated | a dismissed Fernand still offered to be dismissed |
| 0.25.4 | gated the pair on a new scripting variable | the variable never got written |
| 0.25.7 | found node 100 was a *balloon* with no reply list and made it a conversation | correct and necessary, but the gating above still broke it |

### Cervantes has worked the whole time, and does none of it

The project owner asked how Cervantes manages it. He has a node called
`3 Return after release as a companion`, **both replies ungated**, and `Temple District.zax` and
`Inquisition Pit3.zax` each carry an interaction specifier pointing straight at it with
`Speaker=$trigger` and `Player Being Spoken To=$Instigator`.

**The state is encoded by which node the specifier opens, not by a flag.** Grumdjum and the Knight of
Saladin both use the same shape; `666 Rejoin` is the knight's version. Fernand had a node for
*following* and none for *released*, which is the whole defect, and three releases of gating were an
attempt to simulate the missing node.

### What Fernand has now

| state | specifier opens | replies |
|---|---|---|
| following | `100 companion banter` | *Wait here* -> release, then point the specifier at 103 |
| released | `103 fernand waiting` | *Walk with me again* -> set companion, then point it back at 100 |

Each swap runs from a `CCannedObject` fired by `CUseCannedActionAction`, because a tree may not name
its own file -- the 0.25.2 rule -- and the swap itself is copied field for field from the
`fernand joins you` relay already working in `Port District.zax`.

`Fernand Is Waiting` is deleted. Nothing now depends on `$Instigator` resolving in that conversation,
on a new attribute being writable against an existing character, or on *how* the player dismissed him.
If he is not following, his specifier opens the node that offers to take him back.

### What the audit missed

The companion audit of 2026-09-29 cleared Grace, the Goblin Girl and Grumdjum and found one defect. It
never looked at Cervantes, because it scanned **only Fixt's files** -- and Cervantes is pure vanilla.
The working reference implementation for the exact problem being solved was sitting outside the search
path for three releases. **A sweep for "how does this game do X" has to include vanilla, not just what
this project has already touched.**

### The barks, one voice per family and a sub-bank per type

Item 3 of the reactive plan. **67 cans, 71 lines, three families, and a sub-bank per creature type.**

| family | shared | sub-banks | cans |
|---|---|---|---|
| thieves | 8 | boss 5, archer 5, melee 5 | 34 (boss 6, archer 10, melee 18) |
| English soldiers | 8 | officer 5, archer 5, melee 5 | 24 (officer 8, archer 4, melee 12) |
| Snakebreed | 7 | venom 5, summoner 4, boss 4, drone 5 | 9 (venom 3, boss 3, drone 3) |

So a thief archer draws from 13 lines -- the eight every thief shares plus five only archers say -- and
a thief boss draws from a different 13. A soldier officer shouts *"Not one step back, do you hear
me!"*; a soldier archer says *"Nock and draw!"*; neither says the other's line, and no thief says
either.

### Two faults in the first attempt, both reported and both real

The bank was **four lines per family**, and each can was assigned exactly **one** of them -- so an
individual thief repeated the same line forever. Four lines across a family is not four lines from a
thief.

Then "every creature draws from the whole bank" was itself the wrong goal. Family separation was
already guaranteed by giving each family its own tree, so the real gap was *within* a family. The fix
is the sub-bank: shared lines carry the family's voice, the sub-bank carries the role's.

### Shape

    Shoot Completed = CRandomAction          <- 1 attack in 4 barks
    {
      select skill, select skill, select skill,
      CRandomAction { balloon x13 }          <- drawn fresh from shared + this type's sub-bank
    }

Nested `CRandomAction` is the composite shape the Boss Lich already ships. `Include In Log=0`
throughout: the log is where the game puts narration, so speech there reads as the narrator.

**Skipped, deliberately:** probe A's archer, whose attack AI *is* an experiment and must stay a single
variable; probe B's archer, whose slot holds the move-relative test; and the three
`Snakebreed Summoner` cans, whose slot already carries a `CAddTemporaryAIAction`. The summoner
sub-bank is written into the tree but currently unused -- it will be wanted if those three are ever
given barks, and an unused node costs nothing.

### Two mistakes worth recording

**Reading vanilla instead of Fixt.** The first build read every can from the vanilla archive and
silently discarded the backstab repoints, the Sniper repoints and both probes across 36 thief cans.
`tools/lhbuild.py` has had the right helper the whole time -- `read()` takes Fixt's file if one exists
and falls back to vanilla -- and the script simply did not use it. Caught by checking four known
markers straight after the run, restored from git. **Any script that edits a shipped file must read
through `read()`, never `zf.read()`.**

**A rebuild is not a reset.** The second and third attempts produced 0 barked cans for two whole
families, because `git checkout <old> -- <path>` restores tracked files but does **not** delete files
added since -- so the previous attempt's cans survived with their slots already full, and every one
was skipped as "already in use". The fix is to enumerate what the old commit tracked and delete
everything else under the path first. Gate 0 caught the related half of this honestly: it failed on
`exact node ref '12 wrong alley' into Fixt Thief Barks (no such node)` once the trees were regenerated
with new node ids, which is precisely the check added after 0.25.2.

## 0.26.0 - What They Were Built To Do, part two

The five-item combat plan, built. **Four shipped, one did not survive contact with the data**, and the
sweep that was meant to be a repair pass turned out to have nothing to repair. Each part is separately
revertible and has its own QA rows, because the plan's own stopping rule -- ship one at a time -- is
being set aside at the project owner's call, and attribution has to come from somewhere.

### 1. Sniper on the thief archers (built)

`Is Sniper Mode Enabled` forces a critical on a ranged attack, read in `FUN_0049b030` through the same
generic accessor on the same attacker object as the backstab gate, no player test, callers adjacent in
the same damage pipeline. Backstab is the proven sibling.

Scoped exactly as planned: **Super tier only**, two races and four cans. `Thief3 Bow Super` and
`Thief4 Bow Super` -- two of the six races left unreferenced by 0.25.0 -- now carry the attribute, and
the four Super bow-thief cans point at them. Thugs untouched, as before.

### 2. The weapon-skill mismatch sweep (nothing to repair)

The plan said to widen the name-based sweep to read inventory first, and warned the count might grow.
It shrank to zero, and the name-based findings turned out to be **false positives**:

| can | name-based verdict | what it actually equips |
|---|---|---|
| `Hired Goon Sword` and tiers | "carries a sword, race knows only Unarmed" | `Inventory Items/!None` -- **nothing**. The sword is a death *drop*, not equipment, so `Unarmed 10` is correct |
| `Thug3 Mace Elite` | same | same |
| `Vodyanoi`, `Vodyanoi Green` | not flagged by name | `Spit Voydyanoi`, a real ranged weapon, with `Ranged 0` |

Weapons declare their skill through `Hit Or Miss=Damage Types/Damage Hit Or Miss/<skill>` -- 88 items
do, split Ranged 47, OneHandedMelee 18, TwoHandedMelee 9, AlwaysHit 14. Reading that instead of the
can name is what cleared the goons.

The Vodyanoi were **read and deliberately left alone**. `Ranged 0` looks like a defect until the tiers
line up: 0, then 5, then 10. It is a ramp that starts at zero, and only 11 of 623 skill presets in the
whole game are zero-valued, so it is rare but not unique. A creature whose weakest tier is hopeless
with its own attack is a coherent design, and it stands on 32 and 16 maps.

So this item ships no file change. That is the right outcome for a repair pass that finds nothing, and
the measurement is worth more than the four cans it would otherwise have "fixed".

### 3. A telegraphed heavy strike for the Assassin Masters (built)

All three `Assasin Master` cans had an **empty `Shoot Completed`** -- the Priestess situation again --
and `Assasin Master Super` is the heaviest thing in act 1 at 650 hit points, standing in the Slave
Pits.

One attack in four now spawns a visible warning, waits a second, then lands an extra 6-12, 9-16 or
12-22 slashing by tier. The shape is `Swordsman Dual Super`'s -- something visible, `CDelayAction`,
then the payload -- with the `Vilify` effect on its shipped path and `CActionDoDamage` copied from
`Andre the Titan 2`. No animation was invented: a `CPlayAnimationAction` was considered and dropped
because it needs an animation the assassin model is known to have, and that was not verified.

**What a telegraph can honestly be.** `Shoot Completed` fires when a shot *finishes*, so a delay there
cannot slow the blow already landing. What it can do is occasionally wind up and land an extra one.
That is a telegraphed special attack, not a slowed normal swing, and these notes say so rather than
implying the other thing.

### 4. Archer secondaries (NOT BUILT -- blocked, and the measurement says why)

The plan was a melee secondary for `Assasin Bow` and its tiers, with a switch when the player closes.
Two measured facts kill it:

- **No distance-check action exists.** Sweeping every `.can` and `.zax` for a class matching distance,
  range, near, close or proximity returns `CFreeRangePoly` (geometry), guard AIs and door checks.
  Nothing an attack AI can ask "is the player on top of me". So any switch would be random, and a
  random switch means archers that stop shooting at range -- strictly worse than today.
- **There is no blade to give them.** The melee assassins -- `Assasin`, `Assasin Super`,
  `Assasin Master Super` -- equip **nothing at all**. There is no assassin melee weapon item in the
  game to hand the archers as a secondary.

A partial exists and was not taken: give the three `Assassin Bow` races an `Unarmed` preset so they are
not swinging with a skill they lack when cornered. One line per race -- but whether a bow-equipped
character melees at all is unverified, and shipping an unverified guess inside a release that already
carries three behaviour changes is exactly how attribution gets lost. Offered, not shipped.

### 5. The Bonecaller raises a wave when wounded (built)

`CAIHealthPercentThresholdTrigger` is used **twice in the entire game**, both in
`Ogre Conjurer Cave.zax`, both `When Health Percent Crosses Below` firing a relay. The shape is copied
exactly and only the action differs: it fires `CUseCannedActionAction` on a new canned object rather
than a relay, which is the 0.25.2 indirection and means **no map edit**.

Crossing below 40% raises 3, 4 or 5 ghouls by tier, using the same clone-and-checker beat as the
0.25.0 per-attack summon and guarded by `ghoul summoning enabled`, so a Bonecaller without a clone
source simply does not. It is a moment, not a behaviour swap: swapping its whole attack AI mid-fight
would need `CRemoveAIAction`/`CAddAIAction` inside a can, which is far more than the item ranked last
justifies.

### The honest caution

Three behaviour changes and a crit-forcing attribute land together, against a plan that said not to do
that. The QA rows are split per item so a playthrough can still attribute, and each part reverts on its
own -- two preset lines for item 1, three `Shoot Completed` blocks for item 3, one Activity entry and
three canned objects for item 5. If the next playthrough can only report "combat got harder", that is
the cost being paid.

## 0.25.7 - Fernand's conversation actually opens

**0.25.3 and 0.25.4 fixed nothing.** Reported: hitting release on Fernand says *"a companion has left
your party"* and talking to him again gives the same thing again. Reading the save showed
`Fernand Is Waiting` absent entirely -- the variable had never been written once.

The cause sits upstream of everything those two releases touched. The `fernand joins you` relay in
`Port District.zax` adds an interaction specifier whose action is:

    Action=CDisplayDialogBalloonAction
    {
    Dialog Tree File=.../Distressed Sailor
    Node ID=100 companion banter

A **balloon**. It floats "Where you go, I follow." over his head and closes. A balloon has no reply
list, so the dismiss and rejoin replies added to node 100 were never displayed at all, and the release
the player was clicking was the game's own party UI, which fires the engine message and touches no
script of ours.

### What went wrong in the diagnosis

The finding in 0.25.3 -- node 100 is his only interaction and offers no way back -- was correct. The
repair was aimed at the node instead of at the thing that opens it.

The evidence was there and was misread twice. `100 companion banter` having no replies was treated as an
authoring omission, and then, when a sweep found **49** reply-less nodes opened as conversations across
the game, that was taken as proof the shape was normal and the node fine. Both readings missed the
actual question: *what class of action opens this node?* The sweep even recorded the answer -- it
collected entry points from `CDisplayDialogTreeAction` only, so node 100 should never have appeared in
its results, and it did not. Nobody asked why.

A reply-less node **is** normal for a balloon. That is what balloons are. The defect was that his
post-join interaction was a balloon at all, when every other companion in the game uses a conversation:
Grumdjum's post-join specifier is a `CDisplayDialogTreeAction`, and so is the Knight of Saladin's
`3 Return`, which is why 0.25.5 worked first time.

### The fix

The specifier now opens node 100 as a conversation, with `Speaker=$trigger` and
`Player Being Spoken To=$Instigator` copied from the working specifiers in the same map. That second
field is also what makes `Character to modify=$Instigator` resolve in the reply's modifier action, which
is the other half of why the variable never moved.

One behaviour changes deliberately: walking up to Fernand while he follows now opens a short
conversation instead of floating a line over him. That is the cost of him having replies at all.

### This one needs a save that has not recruited him

Unlike 0.25.3 and 0.25.4, this is an **entity** change, and entity state is snapshotted per save on
first visit. The reporting save carries the old balloon in both its Port District layer and the live
layer that travels with him, confirmed by reading it. So this repair reaches a character who has not yet
triggered `fernand joins you` -- not one already partway through.

### The stat-bar follow toggle is not hooked, and cannot be

Stopping a companion following from the stat bar does not touch `Fernand Is Waiting`, and the attribute
it does write, `Companion Follow Enabled`, is a single global flag for the whole party rather than a
per-companion one. So it cannot be read as "is Fernand my companion". If it is used, the pair self-heals
in one step: the dismiss reply shows, choosing it releases a companion who is not following -- a no-op --
and sets the variable, after which the rejoin appears and the two stay correct.

## What the stat-bar control actually is

0.25.7's notes said the player had clicked "the game's own party UI". **There is no party UI**, and that
was asserted without checking. What the game has is a stat-bar control -- the executable carries
`"Companion Follow / Stop Following"`, `"Stop Companion Follow"` and `"Start Companion Follow"`, handled
by `CXrpgStatBar::Server_HandleCompanionFollowStateChangeMessageFromClient`.

It toggles **following**, not membership. It does not release anybody, and it writes the engine's own
`Companion Follow Enabled` attribute, whose description is *"Modified by game engine to have a value of
1 when companions are following and 0 when not"* -- note the plural. It is a single global toggle for
the whole party, so it cannot answer "is Fernand specifically my companion" and is no substitute for
`Fernand Is Waiting`.

Nor does it print *"A companion has left your party"*. That string is not in the executable at all; it
is a `Text to print=` in map scripts, and the one in `Port District.zax` belongs to the **Lost Knight**
leaving after he is saved, nothing to do with Fernand. The reporting quicksave's event log does not
contain the line either, so whatever produced it is further back than the 300 events the log keeps.

None of this changes the 0.25.7 repair, which rests on a verified fact: node `100 companion banter` was
opened by a `CDisplayDialogBalloonAction`, and a balloon has no reply list. What it does change is the
account of what the player was clicking, which should not have been stated as known.

## 0.25.6 - the marker for the verified build

**No game file changes.** `git diff v0.25.5..v0.25.6 -- files/` is empty, and the zip differs from
0.25.5's only in the version string. Installing it over 0.25.5 gains nothing.

It exists so the build the first playtest validated has a number to point at. What that playtest
established, on 2026-09-29:

- **The enemy backstab of 0.25.0 fires.** `Thief Swordsman sneaks up on Antonio Gula and hits for 8
  (9 Slashing Damage) (25 percent backstab bonus)`, at roughly **one in seven** landed melee thief
  attacks while surrounded. The gate compares the supplied angle against the **defender's** facing, and
  an attacker behind the defender qualifies -- which the decompilation alone could not settle.
- **The thieves render and move normally**, confirming the reasoning that a race preset writes the
  attribute the gate reads and leaves the engine's own sneak-state field at `+0x134` untouched.
- The 0.25.1 startup crash, the 0.25.2 self-referencing trees, and the 0.25.3-0.25.5 companion repairs
  are all in this build.

Cutting a no-change release is not something to make a habit of. It is justified here because five
patches landed in a day and the one that matters to a player -- "which of these is the build that was
actually played?" -- had no answer otherwise.

## 0.25.5 - the Knight of Saladin knows whether he is with you

The one finding of the companion audit, fixed. His node `3 Return` offered both "Hold this ground and
wait for me." and "Let's go." ungated, and `02 Shifting Dunes.zax` points his specifier there **twice**
-- from the initial map wiring and from the `Knight AI switcher` relay fired on joining -- so the node
is reached before recruitment and while following, and one reply was always wrong.

**Fernand's variable would not have worked here.** His node is only reached after joining, so "is
waiting" splits it cleanly in two. The knight's is reached in *three* states -- never recruited,
following, waiting -- and "is waiting" cannot tell the first from the second, since both read 0. Gating
his join on it would have made him unrecruitable. So the variable tracks the other thing:
**`Saladin Knight Follows`**, 1 while he is with you.

| site | gate | does |
|---|---|---|
| `3 Return` "Let's go." | **not** 1 | join, then +1 |
| `3 Return` "Hold this ground and wait for me." | **is** 1 | release, then -1 |
| `30 go`, the first recruitment | none | join, then +1 |
| `666 Rejoin` "Yes, please rejoin me." | none | join, then +1 |

The two gated replies can each only fire from the side that makes them legal, which confines the
variable to 0 and 1 without needing set-rather-than-accumulate semantics. `Allow Accumulation=0` does
exist in vanilla, 37 times, but what it means is not established and this did not need to find out.

The other two sites are ungated deliberately. **`30 go` has exactly one reply**, the default, so a gate
that hid it would leave the node with nothing to click -- and it is unreachable while following anyway,
since `3 Return` offers no path to it and the specifier moves to `3 Return` the moment he joins.
`666 Rejoin` is only ever reached at 0, because the release is the only thing that points the specifier
there.

Existing actions were **wrapped**, not edited: each `Custom Action=X` became
`CMultipleActionsAction{Action=Array{Item Count=2, Action=X, Action=<bump>}}`. That avoids renumbering
an `Item Count` inside a live array, a splice this project has got wrong before.

## The companion audit, 2026-09-29

After Fernand, every companion was checked for the same two failures: a rejoin that cannot be reached
after dismissal, and a dismiss/rejoin pair that does not know which state it is in.

Ten trees carry `CSetCompanionAction`. Five of them are **pure vanilla, untouched by this project** --
Joan of Arc, Sir Roger, Diego, Inquisitor Darsh and the Trapped Conquistador -- and all five join with
no release at all. That is vanilla's design for story companions who leave by script, not a defect to
repair here.

Of the five this project built or extended:

| companion | verdict |
|---|---|
| **Fernand Desoto** | fixed in 0.25.3 and gated in 0.25.4 |
| **Grace O'Malley** | **correct, and better than Fernand was.** `01 Outside Shrine.zax` holds a part named `Switch Interaction Specifier when Grace becomes a companion` whose `CConditionalAction` tests the `Grace has been left behind` marker: if she is waiting, simply talking to her fires `CSetCompanionAction`, clears the marker and plays a balloon. The no-op "Stay close to me." reply sits on the other branch, where she is already following and it correctly does nothing |
| **the Goblin Girl** | **correct.** Same design -- a `Goblin Girl is a companion` marker, read map-side by `Goblin Warrens.zax` |
| **Grumdjum** | **not a defect.** Nodes `300 companion` and `300 kill old man` each offer a join and a release together, but those are his *recruitment* nodes: the release reply is "I work alone. Leave.", a refusal, and the `CReleaseCompanionAction` on it is defensive -- a no-op when he is not following |
| **the Knight of Saladin** | **the one real finding.** See below |

### The Knight of Saladin, node `3 Return`

His return conversation offers both **"Hold this ground and wait for me."** (release) and **"Let's go."**
(join), neither gated -- and `02 Shifting Dunes.zax` points his specifier at `3 Return` in **two**
places: the initial map wiring, and the `Knight AI switcher` relay fired when he joins. So that node is
reached both before he is recruited and while he is following, and one of the two replies is always
wrong.

It is milder than Fernand's was. His rejoin is not lost: dismissing him swaps his specifier to
`666 Rejoin` via the canned object 0.25.2 added, and "Yes, please rejoin me." lives there. So this is
the cosmetic half of the complaint -- being offered the option you have already taken -- not a
companion who cannot come back.

**Not fixed yet.** The repair is the same scripting-variable pattern 0.25.4 used, and it touches act 8
content nobody has reached. Worth doing, but as a considered change rather than a fifth same-day patch.

### What the audit method was worth

Two of the four candidates the crude sweep flagged were not defects at all, and one companion that
looked broken turned out to be the best-designed of them. A count of "ungated companion replies" said
six trees were at fault; reading what each node actually is said one. The signal that mattered was not
whether a reply was gated but **whether the node it lives on can be reached in more than one state** --
Grace and the Goblin Girl gate by map-side condition, Grumdjum gates by position, and only the Knight of
Saladin gates by nothing.

## 0.25.4 - Fernand's two replies know which one applies

Reported within minutes of 0.25.3: *"i still get the release companion dialog when i talk to him but
he's already been dismissed."* Correct, and it was a bad trade on my part. 0.25.3 left both replies
ungated so that a player who had already released him could still rejoin, and accepted an offer to
dismiss a companion who was not there as the price. Paying that on every conversation is worse than the
migration problem it avoided.

**Why the obvious fix does not work.** The idiom this very map uses for him is an `Active=0` entity plus
`CCheckExistenceAction`, exactly as `fernand gave barter` does. But a marker is **map-local**, and
Fernand travels -- he can be dismissed anywhere in the game, and a Port District entity is out of scope
the moment he leaves it. Cross-map state belongs on the player, which is what
`Derived Character Attributes/Game Scripting Variables/*` exists for; this project already ships seven.

So there is an eighth now, `Fernand Is Waiting`:

| reply | shown when | does |
|---|---|---|
| Wait here, Fernand | the variable is **not** 1 | `CReleaseCompanionAction`, then **+1** |
| Walk with me again | the variable **is** 1 | `CSetCompanionAction`, then **-1** |

Each reply can only fire in the state its own gate describes, so the variable is confined to 0 or 1.
That is what removes the need for a conditional inside either action, and with it the accumulation drift
a naive +1/-1 pair would have had.

**A save dismissed before this fix** reads 0, so the dismiss line shows once. Choosing it releases a
companion who is not following -- a no-op -- and sets the variable, after which the rejoin appears and
the pair is correct forever. One extra step, once, only for saves that predate the fix.

Nothing here is invented: the read is `CIsEqualTo{CVariableDerivedCharacterAttribute, ...}` copied from
`CedricAlsen.DialogTree`, the write is `CAddCharacterModifierToCharacterAction` copied from
`Herbalist Dialogue.DialogTree`, and `CExpressionNot{Operand1=...}` was already in Fernand's own tree.

### What this says about 0.25.3

The reasoning in 0.25.3 -- that recoverability beats tidiness -- was right about the goal and wrong
about the means. It treated "marker" and "no gate" as the only options and never asked where the state
should live. The scripting variable gives recoverability *and* correct labels, and it was available the
whole time.

## 0.25.3 - Fernand can be taken back

Reported from play: *"fernand cannot rejoin the party if we release companion."*

Recruiting Fernand Desoto fires the `fernand joins you` relay in `Port District.zax`, which swaps his
`CSkeletonAI` for a follow AI and **replaces his `CAIInteractionSpecifier`** with one that opens his
tree at node `100 companion banter`. That node is, in full:

    Node ID=100 companion banter
    Text=Where you go, I follow.
    Should Have Voiceover=0

**No replies.** And nothing anywhere restores his original specifier.

A reply-less conversation node is not itself a defect -- a sweep found **49** of them opened as
conversations, and most are vanilla's own ambient one-liners (`Bar Patrons`, `ToulouseOgres`,
`ShylockeGoons`'s shop loop). The engine shows the line and closes. So node 100 on its own was working
as the game intends.

The defect is narrower and worse: that node is his **only** interaction for the rest of the game, and it
offers no path anywhere. Once he is released there is no route back to `1 return after saving juan`,
where the recruit reply lives, because his specifier no longer points there and nothing restores it. He
was lost for the rest of the run.

Node 100 now carries the route back: dismiss, rejoin, and a default goodbye. Two new nodes carry his
answers. Adding replies is the fix precisely because that node is the only place the game will ever put
the player in front of him again.

**Both replies are deliberately ungated.** A marker set on dismissal would be tidier, and is the idiom
this project uses elsewhere (`Grace has been left behind`), but it only works when the release goes
through dialogue -- and this was reported by a player who had *already* released him. A marker-gated
rejoin would have left exactly the people who hit the bug unable to use the fix. Releasing someone who
is not following, and recruiting someone who already is, are both no-ops, so the cost is one slightly
odd line and the benefit is that he is recoverable from any state.

The recruit gate at node `40 companion` -- Speech 20 or Barter 20 -- is **not** re-applied on rejoin. He
was persuaded once and says himself the debt is unpaid; charging it twice would strand a character who
spent those points earlier.

No map edit: the specifier already points at node 100, which is now a node worth arriving at.

### A note on the same shape elsewhere

This is the third companion in three releases whose dismissal or rejoin was incomplete -- Grumdjum's and
the Alamut knight's rejoins were the self-referencing trees of 0.25.2, and Grace's dismissal balloon was
one of the eleven. The pattern is consistent: the joining half gets built and tested, and the leaving
half is written but never walked. Every remaining companion should be checked the same way before the
next feature release.

## 0.25.2 - the trees that named themselves

A second fatal, found by the playtest that 0.25.1 made possible:

> Got stuck in an infinite loop while trying to load
> `"Levels/1 Barcelona/Dialog/Port District/Captain Isabella"`. This is usually caused by that file
> refering to itself. The actions in this file need to be re-scripted to go through a canned object or
> relay or some other indirect method.

A `.DialogTree` may not name its own file. When it does, the loader recurses and the game dies -- so the
NPC cannot be spoken to at all.

**Vanilla never does it.** Its four in-tree `Dialog Tree File=` references all name a *different* tree:
cortes to Shylocke, SewerEntranceBeggar to Find Enrique, SewerEntranceThief to Find Juanita, and Rakeb
to Woodcutter. Pointing at another tree is ordinary; pointing at your own is the defect. All **eleven**
offenders were this project's, across four characters:

| tree | sites | what it was doing | shipped in |
|---|---|---|---|
| `GoblinGrumdjum` | 6 | rewiring his interaction specifier so the next approach opens at the companion nodes | 0.20.0 |
| `Brambles` | 3 | three random thank-you balloons | 0.12.0 |
| `Captain Isabella` | 1 | Grace's "wait here" balloon on being left behind | 0.19.0 |
| `alamutknightsaladin` | 1 | the knight's rejoin node | 0.20.0 |

### The fix is the one the engine asks for

Each offending `CDisplayDialogTreeAction` or `CDisplayDialogBalloonAction` block is moved **verbatim**
into a `CCannedObject` and replaced in place by `CUseCannedActionAction{Canned Object=...}`. Nothing
around it changes -- the `CAddAIAction`, the interaction specifier, the delays and relays all stay as
they were -- so behaviour is preserved and only the indirection is added. Eleven sites collapse to seven
canned objects, since Grumdjum's six sites reuse two nodes.

Every piece has precedent in the shipped game. `Common Objects and Scripts/Detect Spellcast.can` is a
`CCannedObject` holding a `CAddAIAction` that names a dialogue tree, which is exactly the shape being
built; `CUseCannedActionAction{Canned Object=...}` is how the game fires such an object, **107** times;
and `$Trigger` and `$Instigator` survive that indirection there, which is what the Grumdjum and Alamut
blocks depend on. The canned object naming the tree is legal because it is a different file -- the cycle
is broken by the hop, which is precisely what the error message asks for.

No map edits, and no dialogue nodes moved.

### Gate 0 again

`check_self_reference` is added: for every `.DialogTree` and `.dialogtree` in the mod, any
`Dialog Tree File=` naming its own path fails the gate. Proved by reintroducing the Captain Isabella
reference, which exits 1 with the file named, and passing again once restored.

That is the second startup-class defect in two releases that the gate could not see. Both were reference
integrity, and both are now checked: 0.25.1 added race skill and attribute references, this adds tree
self-reference.

### The sweep afterwards: nothing more, and two gate gaps

Self-reference was the reported defect, so the rest of the dialogue were swept for the same class.
**Nothing new was found**, and the negative results are worth recording because each was a plausible
place for another fatal:

| swept | result |
|---|---|
| exact `Node ID=` references from trees and canned objects | **clean** -- including the seven canned objects added an hour earlier |
| `Dialog Tree File=` naming a tree that does not exist | none |
| `Requirement=` not preceded by its structural blank line | none |
| reference **loops of any length**, over all 367 vanilla and Fixt trees | none; only five trees reference another tree at all |
| whitespace inside a node id | 38, and **all 38 are vanilla's own**, shipped working since 2003 -- zero new |
| `Go to node ID=` differing from its node only by case | 135, and a non-issue: the engine folds case on node lookup, which is why the dangling-target check has always folded it too |

The last two rows are the reason the sweep compared against the shipped copy of every file rather than
reporting raw counts. On the raw count this looked like 181 defects; measured against vanilla it is
none. That is the same trap a case-sensitive sweep fell into once before, when it invented four
Toulouse defects.

**Two gate gaps did turn up, and both are closed.**

`check_map_node_refs` -- which resolves an exact `Node ID=` against the target tree and is described in
its own message as catching a CRASH -- ran on `.zax` **only**. A tree or a canned object carrying the
same reference was unchecked, which is precisely the shape that had just shipped broken. It now runs on
`.dialogtree` and `.can` as well.

`check_self_reference` only looked for a tree naming itself, but the engine detects a *loop*: `A -> B
-> A` hangs identically. It is now a cycle search of any length over the combined vanilla-and-Fixt
graph, since a Fixt tree can point into a shipped tree that points back.

Both were proved by construction rather than assumed: typing a node id wrong inside a canned object
fails the gate naming the file and the node, and wiring Grumdjum to Rakeb and Rakeb back to Grumdjum
fails it with `goblingrumdjum -> rakeb -> goblingrumdjum`.

### Why four characters went out broken

The same reason as 0.25.1. Three of the four shipped in 0.19.0 and 0.20.0, and **the game could not
reach the main menu from 0.19.0 onward** -- so none of this content had ever been loaded by anyone. The
crash that made the mod unplayable also hid every defect behind it. This is what the backlog of unplayed
releases actually costs, and it is why `tools/savecheck.py` was written the same day.

## Tooling - reading a playtest instead of remembering it

The startup crash made the cost of the finish-then-playtest trade concrete, so this is the first step at
shortening the loop: `tools/savecheck.py`, which reads the state the game already writes to disk.

**Saves are not opaque.** The modding notes long described a save's swapped layers as raw binary. They
are zlib. So is the character file. Decompressed, both are the same `TypeName { Key=Value }` grammar as
every resource file -- one quicksave holds a 778 KB `CLayerSaveData` and a 2.8 MB `CLayerHolder`, and a
late-game save holds **63 streams**, one per level visited.

Four things had to be got right, each of which was got wrong first:

| trap | what happens if you miss it |
|---|---|
| only some streams sit behind `#### BEGIN TEMPORARY FILE ####` | scanning for the marker finds the levels you have **left** and misses the live one, which is the only stream holding the player |
| a stale copy of the player survives in swapped-out layers | you read the player as they were several maps ago |
| `Karma` appears **twice** in the player's window | the `Temporary Modifiers` copy read -46 where the real karma was 25 |
| `Character Level` read from the whole stream | you get the first NPC serialised -- Signor Leo, level 4 |

The player is anchored on `Uber Perks`, which no NPC carries, with candidates scored so the live
`CLayerHolder` wins over stale copies. Two anchors that look better and are not: the nearest
`User Assigned Name=` above the ranks can be 17 KB away and belong to a Goblin Archer, and
`Name=Player1` occurs up to five times per stream as a script target.

**What it can answer.** Name, level, experience, karma, the five faction ranks, selected perks, and the
35 `Game Scripting Variables` -- which include all seven this project added. That is most of what the
`docs/qa.md` rows actually ask.

**What it cannot, and says so.** The permanent-modifier array stores only values **changed from
default**, so a character who has joined no order has no `Uber Perks` line and therefore no anchor --
**38 of the 60 saves on this machine are in that state.** There the tool reports that all five ranks are
0, which is the true answer, rather than guessing at the rest. Separately,
`Characters/Last Character.RPG` is written at character creation, not on every save: in testing its
mtime trailed the quicksave by sixteen minutes and it read level 1 where the save read level 2. It is
the starting state, and the tool labels it as such.

The workflow it exists for is `snapshot` then `diff`: park a copy of a save, play the scene, and ask
what moved. Against two real saves that prints `rank/Goblin Rank 0/absent -> 1`,
`perk/Eloquence -> yes`, `Experience Points 250 -> 1350`.

`tools/test_savecheck.py` runs the reader over every save on the machine -- 60 of them -- asserting that
each stream inflates to the brace grammar, that the stream count is never below the marker count, that
karma never comes from the temporary array, and that the level comes from the player's own window. It
skips cleanly where the game is not installed. It is what caught the Goblin Archer anchor.

## 0.25.1 - the startup crash

**v0.19.0 through v0.25.0 could not reach the main menu.** Seven published releases. The game reported it
precisely and fatally:

> The item we are looking for is `Skills/Fighting/Melee` [...] It was referenced by
> `Resources/Races/NPCs/Grace OMalley.Race:Skill Preset:Skill`

There is no `Skills/Fighting/Melee` in the game and there never was. The real skill is
`Skills/Fighting/OneHandedMelee`, which the crash dialog even lists as item 9 of the skills it did find.
Grace's race was authored in `aa3ecaa` (2026-09-26, shipped in 0.19.0) during a review that found she
could not have survived the fight she is dropped into, and the melee preset that fixed that named a skill
that does not exist.

The engine resolves race skill presets **at load**, before the menu, so this was not a latent defect that
needed the right save to hit. It was every launch.

### Why seven releases went out with it

`tools/validate.py` has resolved resource references since early on -- it is what caught the wrong
requirement paths in 0.22.0 -- but it had two gaps that lined up exactly:

| gap | effect |
|---|---|
| `check_references` scanned only `.dialogtree`, `.zax` and `.can` | `.race` files were **never** examined |
| `REFERENCE_KINDS` had no entry for `Skill=`, `Race=` or `Derived Character Attribute=` | even a scanned file would not have had these checked |

Either gap alone would have caught it. Both together meant the single most load-bearing reference kind in
a race file -- the one the engine kills the process over -- was the one nothing looked at.

That it went unnoticed for seven releases is a direct consequence of the standing trade recorded in
`docs/design.md`: finish development, then playtest. Nothing here had been launched since 0.19.0, and a
crash before the main menu is invisible to every automated gate that reads files rather than running
them.

### The fix, and closing the gap

One byte-level change to Grace's race, `Melee` to `OneHandedMelee`, keeping the preset value of 110.

Then the gap: `.race` is added to the scanned suffixes and three reference kinds are added --
`Skill=` / `Skill to select=` (`.Skill`), `Derived Character Attribute=`
(`.DerivedCharacterAttribute`), and `Race=` (`.Race` / `.race`, since the archive is inconsistent about
the case). Reintroducing the bug and re-running the gate was confirmed to fail with exit 1 and the
message *"Grace OMalley.Race: reference does not resolve to any file: 'Skills/Fighting/Melee'"*.

A sweep of all 279 Fixt resource files across **376** references of these kinds found **exactly one**
unresolved, which is the one above. Notably that includes the 36 derived-attribute references added by
0.25.0's twelve thief races the day before -- they resolve, but nothing had proved it until now.

## 0.25.0 - What They Were Built To Do (the combat AI, tier 1)

Every release in the 0.21-0.24 line changed what the game *says*. This one would change how it *plays*,
which is a different kind of risk and is why it is scoped in full before anything is built.

The question that started it: enemies come in four or five shapes and mostly run up and swing until
somebody dies. That is measurably true, and the reason is one field.

### What the engine actually gives us

`CNormalAttackAI.Minimum Attack Distance` is the entire archetype system, across all **478** monster cans:

| value | cans | what it is |
|---|---|---|
| 100 | **391** | walk up and swing |
| 350 | 53 | stand off and shoot |
| `Do not move while attacking` | 22 | rooted caster |
| 250 | 1 | one oddity |

And `Shoot Completed`, the slot that decides what a creature *does* on each attack, is **empty or skill-less
in 400 of the 478**. They swing whatever the race handed them, forever.

But that slot is not a behaviour flag -- it takes the same action vocabulary as every dialogue reply and
relay in the game, and a minority of cans prove it:

| already in use | cans |
|---|---|
| randomised attack pick (`CRandomAction`) | 67 |
| picks from 2-4 skills (`CActionSelectSkill`) | 49 |
| switches weapon mode mid-fight (`CActionSetWeaponMode`) | 30 |
| carries a secondary weapon to switch **to** | 17 |
| summons reinforcements | 13 |
| applies a debuff (slow, AC down) | 8 |
| wind-up delay before the hit (`CDelayAction`) | 24 |

`CScanAreaAI` separately exposes the detection cone (plus or minus 20, 45 or 10 degrees) and
`Go Home Range=300`, the leash.

**What does not exist: `CFleeAI` and `CRetreatAI` are referenced by nothing.** There is no morale, no
retreat, no breaking. Target selection is not scriptable against the player either -- `CSetTargetAction`
has 17 uses, all NPC-versus-NPC with literal names. So focus-fire, flanking, kiting and formations are out
of reach without code, and this plan does not pretend otherwise.

### The finding that orders the tiers

| boss | XP | its attack AI |
|---|---|---|
| Dragon_Chaos | 25,000 | **no `CNormalAttackAI` at all** |
| Old Man of the Mountain | 5,000 | rooted, `Shoot Completed` **empty**, no skills |
| Nostradamus | 1,500 | **none** |
| Priestess / Tough / Super | 1,949 | no skills |
| Boss Lich, Tough, Super (ours, 0.21.0) | 1,500-2,500 | no skills |
| **Wizard Tremblethorn** | 2,500 | rooted, `CRandomAction` over **four** skills, plus a relay |

**The best-built combat AI in the game is on an optional wizard in the Wilderness, and the final boss's
attack slot is empty.** Tremblethorn is the template for everything below.

### Tier 1, built: the Priestesses cast

Tier 1 was scoped as "fill the empty slots on the boss tier", naming four targets. Measuring them first
turned three of the four into something other than what the plan assumed, and found a fourth thing that
is not a buff at all but a plain defect.

**`Priest` and `Priestess` are the same creature with one field missing.** A line-by-line diff of
`Priest.can` against `Priestess.can` differs in exactly one place: the Priest's `Shoot Completed` opens
with `ENEMY Magical Shield` and then picks at random from Fire Orb, Spike and Lightning Bolt, and the
Priestess's `Shoot Completed` is **empty**. Same role, same `Minimum Attack Distance=100`, same
everything else. She walks up and hits you with a stick.

And her race already knows the spells:

| can | its race presets | it cast | it casts now |
|---|---|---|---|
| Priestess | Spike 75 | nothing | Spike |
| Priestess Tough | Fire Orb 85, Spike 90 | nothing | either, at random |
| Priestess Super | Fire Orb 95, Lightning Bolt 95, Spike 95, Static Charge 95 | nothing | any of the four, at random |

Each selects **exactly** what its own race presets and nothing else, so no creature is handed a spell it
was not already built to know. The Priests' shield opener is deliberately not copied: no Priestess race
presets `ENEMY Magical Shield`, and granting one would be inventing rather than connecting.

They are not obscure. The line stands in act 7: **fourteen** Priestesses in the Inner Sanctum, **twelve**
in the Secret Chamber, **eleven** plus **six Supers** in the Exalted Chambers, which is the Druid Master's
own room. Act 7 is the act 0.22.0 just worked on, and every one of those casters was swinging.

### The three decisions, answered 2026-09-28

**1. The Priestesses keep casting, and now cycle rather than re-roll.** `CRandomAction` picks fresh on
every attack, which can hand out the same spell four times running and read as no variety at all.
`CShuffledSeriesAction{When Done=Repeat Series}` -- 67 files in the shipped game use it -- deals the whole
hand before reshuffling, so a Priestess Super visibly works through Fire Orb, Lightning Bolt, Spike and
Static Charge. The base Priestess knows one spell and is untouched; there is nothing to cycle.

**2. The Old Man of the Mountain is left exactly as he is, because he turns into the dragon.**
`Chaos Dragon Generator` spawns `Dragon_Chaos` at 25,000 XP, and its after-action fires
`Player KILL Old Man in Combat` and arms `Dragon Health Checker` -- so killing the dragon **is** killing
the Old Man as far as the ending matrix is concerned. His 40 hit points are not an oversight, they are a
stage direction, and the riskiest item in the review is retired without a file being touched.
`Dragon_Chaos` itself has no AI components at all: the dragon is driven entirely by that map's script.

**3. The Bonecaller raises the dead**, and not with spells. `Ghoul Male Large` Tough and Super summon by
cloning from a map part called `ghoul clone generator`, guarded by a `ghoul summoning enabled` checker,
with a spellcast animation, a 1.5 second delay, a summoning effect and a cleanup delete. The Doomed
Plateau -- where our Boss Lich stands -- already carries **both** the clone source and the checker, so
this needed **no map edit**. The idiom is copied field for field: one attack in four is a summon, and the
three tiers raise four, five and six ghouls. The checker guard means a Bonecaller placed on a map without
a clone source simply fights normally.

The decision reasoning, including the two positions rejected for the Old Man, is kept in
[`design-review-combat.md`](design-review-combat.md).

### Tier 1, built: the thieves of Barcelona backstab

The question that opened this was why no thief, in Barcelona or the sewers, has ever attempted a
backstab -- the perk's whole premise is their job description. The resource files cannot answer it, so it
went to Ghidra. **The gate is not player-only.** Full trace is in the modding reference under "A race can
preset ANY derived attribute"; the short form is that the gate at `0x0049a1b0` is four conditions on
whoever is attacking -- a sneak flag read from the attacker's `Sneak Enabled`, the attacker's
`Is Backstab Mode Enabled`, a melee attack type, and a facing difference of at least pi/2 -- and every
read goes through one accessor that indexes the attribute array on the character object in ECX. No party
check, no `Player1`. The perk is player-only **by data**: no enemy race presets either attribute.

Two data problems had to be solved to act on it.

**Scope, and why the obvious lever was wrong.** All 36 thief cans point at the shared `Thug*` races --
and those races are also worn by `Thug Boss` in **act 8 Alamut**, the Slaver Captain, Shylocke's goons,
the Jewel Thug, the Crossroads Bandit and the Wilderness Traveler. Presetting the attributes there would
have handed backstab to most of the game's human enemies, in four acts, for a change asked about two.

**What made a tight scope possible.** Vanilla ships **18 `Thief*.race` files that nothing references** --
a 1:1 name match with the 18 thief cans, structurally identical to the thug races (same
`!Unknown Model`, so the can still supplies the model) and differing only in numbers: consistently higher
AC and hit points, slightly lower weapon skill. `Thief Pale` differs from `Thug Pale` in exactly one
line, AC 120 against 90. Someone built a thief race line -- evasive but less trained than a thug, which
is what a thief should be -- and never repointed the cans. So this repoints them, which restores that
orphaned line and gives the thieves a race of their own to carry the presets.

| repointed | from | to | AC | HP |
|---|---|---|---|---|
| `Theif4 Sword` + `Sewer Theif4 Sword` | `Thug4 Sword` | `Thief4 Sword` | 95 -> 135 | 25 -> 38 |
| `Theif4 Sword Tough` + Sewer | `Thug4 Sword Tough` | `Thief4 Sword Tough` | 105 -> 149 | 29 -> 54 |
| `Theif4 Sword Super` + Sewer | `Thug4 Sword Super` | `Thief4 Sword Super` | 125 -> 169 | 34 -> 68 |
| `Theif Boss` / `Pale` / `3 Mace` lines, all three tiers, both folders | `Thug *` | `Thief *` | +25 to +65 | +0 to +34 |

**24 cans repointed, 12 races given the presets**, each race gaining three:

| | `Sneak Enabled` | `Is Backstab Mode Enabled` | extra damage |
|---|---|---|---|
| base | 1 | 1 | 0.25 |
| Tough | 1 | 1 | 0.35 |
| Super | 1 | 1 | 0.5 |

The percentage is graded because the player's own perk gives 0.5 per rank and these enemies stand in
act 1; the Super tier matches rank 1 and the base tier is half of it. Presetting an arbitrary derived
attribute is ordinary -- vanilla races preset 21 different ones, including `Lance Guardian`'s
`Melee Damage Percentage Gives Health To Attacker Zero To One` at 0.4/0.45/0.6, which is the same
`Zero To One` shape as the backstab percentage.

**Bow thieves are deliberately untouched.** The gate requires attack type 1 or 3 and the perk text says
melee weapons, so a preset on an archer would be inert. That leaves **6 of the 18 orphan races still
unreferenced** (`Thief3 Bow` and `Thief4 Bow`, three tiers each) -- recorded, not fixed, because
repointing them would be a pure stat buff with no mechanism behind it.

**Where it lands. CORRECTED 2026-09-28**, the same day, after a tester fought thieves in the preorder
bonus level and asked whether they backstab. The first pass said "only six real maps, all act 1" and
dismissed `Global/Secret Red File Level` as a debug map. **That was wrong.** It is the RED FILE preorder
bonus content -- it has its own `RED FILE Presell Pack Installed.can`, its own boss line
(`Thug Boss RED FILE` and its Tough and Super), its own three artefacts, and an entrance scripted from
the Gate District -- and it is the **densest** thief map in the game:

| map | spawns carrying the new races |
|---|---|
| `Global/Secret Red File Level` (preorder bonus) | **90** -- Theif Pale x33, Theif4 Sword x23, Theif3 Mace x12, Theif3 Mace Tough x11, Theif4 Sword Tough x11 |
| `Sewers/02 Thieves Congregation` | 51 total thief spawns |
| `Sewers/01 Sewer Main Entrance` | 43 |
| `Sewers/09 Secret Quest` | 45 |
| `1 Barcelona/Slave Pits` | 21 |
| `Wilderness Maps/Slave Pit Exterior` | 7 |
| `Sewers/05 Troll Pit` | 2 |

That map also fields 100 bow thieves, which are deliberately untouched. So the release reaches **seven**
real maps, and the bonus level carries more backstabbing thieves than any two sewer levels together --
which makes it the best place in the game to test the feature, not a map to exclude.

The error came from filtering the map census on "does this look like shipped content" by name, where
`Global/` and `Test Maps/` were swept together. `Test Maps/` genuinely is developer scratch; `Global/`
is not.

**Why `Sneak Enabled` is safe to preset, despite its own description.** The attribute says *"Modified by
game engine to have a value of 1 when sneeking and 0 when not sneaking"*, which looked fatal. It is not:
the setter `FUN_004420c0` writes the engine's real sneak-state field at `+0x134` **and separately**
adjusts the attribute modifier array at `+0xe0` by a delta of plus or minus one -- the same array a perk
modifier writes. A preset sets the attribute the gate reads and leaves `+0x134` at zero, and movement and
rendering key on the state field, not the attribute. So the thieves should not creep, vanish, or look
different. That is the single most important thing for a playtest to confirm.

**CONFIRMED IN PLAY, 2026-09-29.** The open question was whether an NPC's facing ever satisfies the
pi/2 condition, given that enemies turn to face their target -- and whether the feature was therefore
inert. It is not. From a save taken in the preorder bonus level while surrounded:

    `Thief Swordsman sneaks up on Antonio Gula and hits for 8 (9 Slashing Damage) (25 percent backstab bonus)`

The thief is the attacker, the bonus is the base tier's 25 percent, and the whole chain works: race
preset, `Sneak Enabled` and `Is Backstab Mode Enabled`, the facing gate, the damage, the log line. In
that fight **7 melee thief attacks landed and 1 was a backstab** -- about one in seven while surrounded
by three, which is the facing condition behaving exactly as intended rather than firing constantly or
never.

That also answers empirically what the decompilation left ambiguous: the gate compares an angle supplied
by the damage pipeline against the **defender's** facing, and an attacker behind the defender qualifies.

It took a while to see because the message log **wraps** long lines, and the backstab template is much
longer than an ordinary hit -- on screen it reads as two rows with the recognisable
"(25 percent backstab bonus)" on the second, among ordinary hits. The first two saves checked had no
backstab in them at all, which was a true negative and not a filter error.

**Still unverified.** Three of the gate's four callers were not read, so which ones pass attack type 1
or 3 is inferred from the perk text rather than traced. And if the engine ever delivers the
stop-sneaking message to one of these NPCs, the preset drops to 0 permanently.

**Two variables moved at once**, which the QA rows separate as far as they can: the repoint raised AC and
hit points as well as adding backstab. If the sewers play badly, the revert path is one line per can --
point `Race=` back at the `Thug*` name -- and it can be done without touching the races.

### Tier 1, not built, and why

The three open decisions below, and the tiers waiting behind them, are written up for a
post-playtest verdict in [`design-review-combat.md`](design-review-combat.md).

**The Old Man of the Mountain has 40 hit points.** His race is `Old Man Fleeing`, HP 40, one skill
(OneHandedMelee 50), and there is no second Old Man asset anywhere in the game -- one can, one race. So
his empty `Shoot Completed` is not the reason the finale is what it is; the fight is carried entirely by
`08 Final Encounter`'s script -- the spike matrix, the teleport traps, the summoned-monster loop, the
Chaos Dragon. Filling his attack slot would not repair an oversight, it would **redesign the ending**, and
the plan's own promise for tier 1 was "data only, no redesign". Left alone pending a decision.

**Our own Boss Lich is melee-only, and that is not a regression.** 0.21.0 cloned it from
`Magical Greater Skeleton`, whose race is `Lance Guardian` -- also melee-only, also selecting no skills,
despite the word "Magical" in its name. So nothing was lost in the cloning. Making the Bonecaller cast
means **authoring new skill presets onto a Fixt race**, which is a design change rather than a connection,
and it is the one creature in the list whose difficulty this project owns outright. Pending a decision.

**Andre the Titan 2 needed nothing.** His race presets OneHandedMelee 50 and Lightning Bolt 50, and his
attack AI already selects both. He was on the list because a skill count of 2 looked low; it is complete.

### A second tooling note: the forum-post converter moved into the repo

The bbcode half of every forum post had been retyped by hand for twenty-one releases, so this release's
was generated instead -- and the rules had to be recovered by diffing the shipped pairs, which turned out
to disagree with each other:

| drift | where |
|---|---|
| `## X` as `[size=125][b]X[/b][/size]` rather than plain `[b]X[/b]` | 0.4.1 through 0.10.0 |
| `*emphasis*` converted to `[i]...[/i]` | up to 0.21.1; left as asterisks from 0.22.0 |
| backticks **deleted** rather than italicised | 0.16.0, 0.18.0, 0.20.0 |
| an inverted `[i]`/`[/i]` pair mid-sentence | 0.21.1, where a `*"..."*` quote straddled a line break |

That last one is the reason `md2bbcode.py` substitutes bold and code spans over the **whole document**
before doing anything per line: a per-line substitution closes the span on the wrong side of the words
when a quote wraps, which is exactly the defect sitting in 0.21.1's shipped post.

So there is no single house rule to implement. `tools/md2bbcode.py` implements the convention that has
held since **0.22.0**, the only self-consistent stretch, and it was proved by regenerating 0.24.0's
bbcode and diffing it against the shipped file before being used on 0.25.0.
`tools/test_md2bbcode.py` holds that as a hard requirement for 0.22.0 and later -- 4 of 4 -- and pins a
floor of 15 for how many posts reproduce overall, so a change that quietly alters behaviour on the older
ones is still caught. The older posts are deliberately not reproducible and must not be regenerated.

### A tooling note

The spliced `.can` blocks failed Gate 0 with *"not in canonical engine formatting"* until they were
round-tripped through `resource_format` before writing -- which is exactly what `write_map()` does for
maps, and what a hand-splice into a `.can` does not do for free. Worth remembering the next time this
project edits a can rather than a map.

### Tiers, in the order they should be built

1. **Fill the empty slots on the boss tier.** Copy Tremblethorn's shape -- `Shoot Completed=CRandomAction`
   over a few `CActionSelectSkill` entries -- onto the bosses that have none, in payoff order: the **Old
   Man of the Mountain** first, then our own **Boss Lich** line, then the **Priestess** line (three tiers,
   and the Druid Master's own race), then **Andre the Titan 2**, which has two skills and could carry four.
   Data only, one file per creature, no map edits.
2. **Telegraphs.** `CDelayAction` appears in 24 attack AIs and `CPlayAnimationAction` in 81, out of 478. A
   wind-up animation and a delay before a heavy hit is the cheapest thing in this whole document and the
   one most likely to make a fight readable rather than a blur. Same files as tier 1, so it should be the
   same editing pass: the boss tier, the WarGolem line, the Greater Titans.
3. **Phases.** `CAIHealthPercentThresholdTrigger` fires when a creature crosses a health percentage and is
   used **twice in the entire game** -- both in `Ogre Conjurer Cave`, both only to trigger a relay --
   while AI swapping is routine at 493 `CRemoveAIAction` and 952 `CAddAIAction`. At a threshold: swap the
   attack AI, speak a line, call the summon its kind already has. **This tier does not go in until tier 1
   has been played**, because a boss that changes behaviour at 40% is not something a save can undo.
4. **Archers that do not stand and plink -- as a trial only.** The easy version is impossible: 53 ranged
   cans, 17 cans carrying a secondary weapon, and **the overlap is zero**. Bow enemies have nothing to
   draw. Making this work means *giving* them a melee weapon, a race and inventory change that alters
   difficulty for every archer in the game. Scope it to **`Assasin Bow` and its Tough and Super** in act 8,
   play that, and only then decide about `Soldier2 Bow`, `Mongol Goblin Archer`, `Nos Soldier2 Bow` and
   the rest.

### Retired before building

**"Turn on the summon gates."** The three summoning checkers -- `ghoul summoning enabled` (11 maps),
`hujark summoning enabled` (11) and `snakebreed summoning enabled` (4) -- are **all `Active=1` already**.
Summoning fires everywhere it exists and there is nothing to switch on. The lever is real but points the
other way: those checkers can be switched **off** per encounter, which is a tool for making one fight
readable, not for adding threat. Recorded so it is not proposed a third time.

### The standing caution

This is the first work in this project aimed at difficulty rather than content, and **none of 0.21.0
through 0.24.0 has been played**. Tier 1 should be in front of a player before tier 3 is written.

## 0.24.0 - the register

**Released 2026-09-28. Unplayed.** 0.23.0 gave the Knights of Saladin a rank that is read, an escort, a
merchant discount and a fourth route through the bird men. Which raised a fair objection: nothing in this
game should be only a benefit, and that allegiance had become the purest upside in it.

### The audit, for every order

| allegiance | what it opens | what it actually costs you |
|---|---|---|
| Inquisitor | 251 `Inquisitor IS` gates | **+25%** at the Herbalist, **+50%** at the Weird Woman, +10% at the Rogue Inquisitor; the Cathars, the shepherd and the weird woman all withhold |
| Wielder | 54 | the Montaillou mayor (6 `Wielder NOT`), Beatrice, the Crypt captains |
| Templar | 119 | **+25% at the Herbalist.** That is the whole list |
| Goblin Horde | 11 | the Montaillou guard's hand never leaves his hilt -- our own 0.14.0 |
| **Knights of Saladin** | 42 | **nothing** |

**And a correction to the metric I reached for first.** Counting `X NOT` gates as "costs of being X" is
wrong: almost all of them are *"I would like to know more about the Knights Templar"* -- replies offered
to people who are **not** members, which is flavour, not a penalty. On that bad metric Templar and Goblin
looked more lopsided than Saladin. Read properly, every one of the eleven `Saladin NOT` uses is
informational and every one of the forty-two `Saladin IS` uses is a welcome, a thanks or extra
information. Nothing anywhere charged it, refused it or watched it.

### The constraint

Vanilla states the relationship outright, in the Montaillou guard's own mouth: *"A Knight of Saladin? You
don't have the look of a saracen, but if you serve that order, then you are an ally of the Templars - and
thus welcome here."* So a blanket "Christian Europe distrusts you" would contradict the game. The seam
that does not is the **Inquisition**, which distrusts everyone who is not theirs.

The Bishop of Pamiers lets you introduce yourself as a Knight Templar or as an Inquisitor on three of his
four opening nodes. **There is no third option** -- and he is in Montaillou doing exactly one thing, which
the guard describes precisely: *"a man with a book, asking questions, and every soul in Montaillou
answering him one at a time."*

### What it builds

**The Order may finally introduce itself, and the introduction is the cost.**

> *"A Knight of Saladin. <He does not look up. The quill keeps moving.> The Temple vouches for your order,
> so I will not have you stopped at the gate. You will forgive an old man his thoroughness, though: a
> sworn brother of an order named for a Saracen sultan, arriving in a village I am in the middle of
> emptying of heretics, in the same week. There. You are written down. Now - what was it you wanted?"*

The reply sets a checker on the church map and, through `COtherMapAction`, on the hamlet. It is offered on
all four openings, the untainted one included -- where vanilla offers no order introduction at all, to
anybody.

**And the gate guard stops being glad to see you.** His Saladin welcome now has two versions, gated on
that checker by ANDing his existing canned `Saladin IS` expression with an existence test:

> *"A Knight of Saladin. <His hand settles on his belt and stays there.> Aye. His grace named your order
> to us this week, and he does not trouble to name orders he has no use for. You are an ally of the Temple
> and you may pass - I am not the man who decides otherwise. Do your business in the daylight, and be seen
> doing it."*

**The gate does not close**, because the alliance is real and the game says so. What you lose is the
warmth, and you lose it by your own choice -- nobody makes you tell the Bishop who you are.

### Two vanilla observations, neither of them defects

- `MontailluInquisitor` has five `Go to node ID=` values whose case does not match their node
  (`10 goodbye`, `20 audience`, `70 tasks`, `667 gem inquisitor`, `15 Confront Goodbye`). The engine folds
  case on node lookup, so all five resolve. An exact-match orphan check on this tree reports five false
  positives; the check here folds case, and every build script from now on should.
- That tree's own text is unbalanced on angle brackets -- eight `<` against nine `>` -- so a whole-file
  stage-direction check can never pass on it. The check is scoped to the new nodes instead.

### The Templars pay for their board

The Temple had exactly one cost in the entire shipped game -- the Barcelona herbalist's 25 percent --
against 119 places the allegiance opens something. Its seam was already written, in two places that never
meet.

The Cathar toughs in the Montaillou tavern pick their fight over precisely one grievance:

> *"Oh, so it isn't enough you and your priest friends eat our food and tax our farms? That you come here
> and eat *meat* in our own tavern?"*

And three rooms away, in the mayor's house, the gate guards' own idle banter is the knights doing exactly
that: *"What kind of host are you, Pierre? I am **starving**!"*, *"Why don't you roast one of those
delicious chickens you have outside?"*, *"Bring more food! And more ale!"*, and the justification --
*"You must provide food and shelter to any knight who asks for aid."*

A Knight Templar walking into that tavern **is the man they are complaining about**, and the tree never
noticed. It tests `Inquisitor IS` three times and `Wielder IS` once and Templar not at all, so a Templar
could use the line everyone else uses -- *"I'm not a priest, nor are they my friends"* -- which is true,
and beside the point.

Now the disclaimer is closed to the Temple (`Templar NOT` on all three of its appearances), and an honest
reply takes its place:

> *"No. I am a knight of the Temple, and I have eaten at the mayor's table this week."*
>
> *"Not a priest. Worse. You are one of the knights who sleeps in Pierre's house and eats what is in it
> and calls it his right by the code. Your lot went through my brother's winter stores in three days and
> left him a blessing for them. So. What is a winter worth, brother?"*

Paying is the only way out of that tavern that is not a brawl, and it costs **150 gold** in an act where
that is real money. The reply is gated on actually having it (`CHasMoneyAction`, the idiom Felgnash and
the Shylocke goons use), and the other two answers go where every other wrong answer in that tree goes.

Note what this does **not** do: it takes nothing away from the Templar player except the ability to
pretend. Vanilla's Wielder gets past these men for free with one line, because the Church burns their kind
first. The Temple does not get a line. It gets a bill.

### The Crossroads charges the Horde for the carts

The Horde's benefit was already priced and the bill was not. `Hubglubs Chum Store` sells to sworn goblins
at **0.75** where `Hubglubs Store` charges everyone else 1, and nothing anywhere charged the other way.
Of its eleven `Goblin Horde IS` gates, nine are goblin-facing -- the warren vendor, the patrol leader, the
villagers, the entrance guard -- and the only two that are not are Joan of Arc and the Montaillou guard,
whose hand on his hilt is this project's own 0.14.0.

That guard also names the reason out loud: *"We have had word of what the Horde did at the Crossroads."*
The Crossroads is a real map with four merchant entities standing on it, and Alvaro sells supplies there
at a multiplier of 1, to anybody, with no idea who he is talking to.

He is the right man for the bill, too. Vanilla already has him sort beggars by race -- *"You have some
nerve begging from me, you tainted lout!"* -- so this is not a new opinion, only an informed one:

> *"Si. I sell to you. I sell to everyone, amigo, that is the business. But last spring your Khan's boys
> came through this crossroads and took what they liked off three of my carts and left me the axles, and
> somebody has to pay for the carts. So it is my price, and then it is your price, and they are not the
> same price. There is another merchant four days south if you do not care for mine."*

**1.5**, matching the steepest surcharge in the game -- what the Weird Woman charges an Inquisitor. Sworn
to the Horde you now buy at **0.75** from your own and **1.5** from the people whose carts you took.

Both of Alvaro's shop nodes are gated, the high-karma one included, so a Horde player with a hero's
reputation does not slip past the surcharge through the special stock. That is deliberate: the good-karma
store exists because *"word of your good deeds has not avoided my ears"*, and the same ears heard about
the Crossroads.

### Still owed

Nothing, for the first time in this line of work. All five allegiances now cost something:

| allegiance | what it costs |
|---|---|
| Inquisitor | +25% Herbalist, +50% Weird Woman, +10% Rogue Inquisitor, and the Cathars, shepherd and weird woman withhold |
| Wielder | the Montaillou mayor, Beatrice, the Crypt captains |
| Templar | +25% Herbalist, **and 150 gold to the Cathars or a brawl** |
| Goblin Horde | the Montaillou guard's hand on his hilt, **and 1.5 at the Crossroads** |
| Knights of Saladin | **the Bishop's register, and a gate guard who stops being glad to see you** |

What is left is the other direction: the two orders whose ladders nothing reads, `Templar Highlevel` and
`Inquisitor Highlevel`, still referenced by nothing at all.

## 0.23.0 - what the Crescent is worth

**Released 2026-09-28. Unplayed.** Act 8 is the Knights of Saladin's own country -- the Old Man of the
Mountain, the Assassins, the Levant -- and choosing that order buys less there than choosing any other.

**The count.** Act 8's identity gates: `Templar IS` 13, `Inquisitor IS` 12, `Goblin Horde Highlevel` 4,
**`Saladin IS` 6** -- and three of those six are the companion's greeting selector while two more are the
Ways Crystal promotion. The Knight of Saladin companion at the dunes is **unconditional**: everyone gets
him. Membership buys a salutation ("Brother"/"Sister" instead of the generic) and one extra reply, which
0.20.0 added.

### The ladder nobody reads

Every order has three rungs, each a `.Faction` granting permanent modifiers **and `+1` to its rank
attribute**, so the rank counts how many promotions you took:

| | Saladin | how you get it |
|---|---|---|
| 1 | **Aswaran** | the Dream Djinni trials, which also grant `Dervish of the Crescent` or `Scholar of the Crescent` |
| 2 | **Blessed** | Jafar, on taking the Montaillou or Montserrat errand |
| 3 | **Exalted** | all five green Way Crystals -- `+13/+13` melee, `+12` Turn Undead, `+5%` crushing, `+5%` slashing, `+20` carry |

Exalted is the strongest faction perk in the game, and reaching it means the initiation, Jafar's errand
and the crystal hunt. `Saladin Highlevel` is the canned requirement that tests for it, `Rank > 2`, exactly
as `Goblin Horde Highlevel` tests `Goblin Rank > 2`.

**`Saladin Highlevel` is referenced by nothing in the shipped game.** Neither is `Templar Favored`,
`Templar Highlevel`, `Inquisitor Favored` or `Inquisitor Highlevel`. `Saladin Favored` has five uses, all
Jafar, back in act 1. The only faction ladder anything in this game reads is the Goblin Horde's -- and
that is **our** work, from 0.1.0.

The asymmetry is sharpest at the Old Man. He answers a Goblin Champion by rank -- *"The Great Khan sent
proud warriors after you once and not one of them came home. The Horde calls me Champion now."* -- and
answers the highest-ranking knight of the order whose Sultan he twice tried to murder with the same line
he gives a week-old initiate.

### What this tier builds

**The companion knows what he is standing next to.** His greeting chain tested Templar, then Saladin, then
default. A rank test now sits between the first two, gender-split like vanilla's:

> *"Salaam - Exalted. Nine days I have held this sand, and I had begun to think the order had forgotten
> the fortress. It has not forgotten. It sent the highest of us. Command me, Brother, and I will not ask
> twice what for."*

And an Exalted can ask him what the order actually says about Alamut, which is the point of the rank:

> *"The order does not speak of Alamut in the chapter houses, so I will speak of it here, in the sand,
> where there is nobody to be shocked. Every Aswaran is told one thing on the day of the oath and never
> told it again: if the Old Man moves against the Sultan's house a third time, the highest of us who is
> nearest rides, and does not wait for permission, and does not come back with prisoners. In eighty years
> nobody has ever been nearest. You are nearest."*

**The Old Man reads the rank**, in a reply placed beside the one he already has for the Horde's:

> *"Twice you put knives in Saladin's tent. The order wrote a standing order that same year and has spent
> eighty of them waiting for one of us to be near enough to carry it out. I am the nearest. That is the
> whole of the parley."*

An Exalted knight sees that **and** the plain `Saladin IS` line, deliberately: one is personal (*"I am
what came back"*), the other is the order's. They are different arguments, and picking between them is
the point.

### The order rides

A greeting is not a reward, and the reason the rank could not easily be more than a greeting turned out
to be worth finding: **the Knight of Saladin exists on exactly one map.** `02 Shifting Dunes` names him
eleven times. The seven maps past it name him **zero**. He says *"my sword is yours"*, walks you to the
door of the fortress, and stops there for the rest of the game.

So an Exalted can now tell him to come in:

> *"Then come the whole way in. Not to the door - in, to the chamber where he sits."*
>
> *"In. Yes. I had been told to hold the sand and I have held it for nine days, and I had begun to be
> afraid that holding the sand was the whole of my part in it. Lead, then. Through the Maw, through the
> wash, through whatever he keeps in the dark below it - and at the door of his chamber I stop, because
> the order does not come back with prisoners and somebody has to be outside it to be sure that nobody
> does."*

That reply arms a checker on five maps through `COtherMapAction`, and each map's arrival spawn point
raises an escort generator **cloned from the dunes knight himself** -- same character template, same race
(the 220 HP / 215 AC companion race 0.20.0 raised from 150/145), same `Companion` category, with the
greeting chain replaced by `3 Return` because the introductions happened in the sand.

| leg | raised from | the map he now fights on |
|---|---|---|
| 03 Sand Dragon | `From Shifting Dunes` | 4 spawn entries |
| 04 Maw of the Assasin | `From Sand Dragon` | **177** |
| 05 Acid Wash | `From Maw of the Assassin` | 27 |
| 06 Chamber of Torment | `From Acid Wash` | **210** |
| 07 Dark Temple | `From Chamber of Torment` | **152** |

Every hook was checked against the transition that actually lands there rather than against the spawn
point's name: `02` sends you to `From Shifting Dunes`, `03` to `From Sand Dragon`, and so on. A hook on
the wrong arrival point fails silently, which is the standard way this kind of work dies.

**He does not follow into `08 Final Encounter`, and that is deliberate twice over.** `07` sends you to
that map's `Start Here`, which is the one arrival left unhooked. The map is the most tightly scripted in
the game -- two caged prisoners with their own scripted attackers, a spike matrix, a siege tank, a
summoned-monster loop and a grid of ending relays keyed to who is still alive and what the player's karma
is -- and an extra body in it risks the ending rather than improving it. It is also the better reading of
the oath he quotes.

### The desert merchant

The last shop before the fortress sits in `01 Desert Sprawl` and he is, by a distance, **the most
expensive merchant in the game**: `Price Multiplier=2`, where the next worst is 1.7 and the median across
every shop is 1. Defensible -- he is the only trader for a hundred miles on an Assassin road -- but he had
nothing to say to a Knight of Saladin, and he did not stock the potions this project unlocked seven acts
earlier.

**He now knows the order.** A `Saladin IS` reply on both his openings, guarded by a checker so it lands
once:

> *"Ah. Ah, forgive me - I took you for one more westerner with a sword. The Assassins pay me well and
> they pay me because they must pass, but it is your order that keeps the road open south of here, and a
> man who trades on a road owes something to whoever sweeps it. My prices are my prices. For you they are
> not."*

That is a `CAdjustMerchantPriceMultiplierAction` of **-0.5**, taking him from 2.0 to 1.5, and it stacks
with his haggling the way the two haggle steps stack with each other:

| | base | after haggling twice |
|---|---|---|
| anyone | 2.0 | 1.8 |
| Knight of Saladin | **1.5** | **1.3** |

**And he stocks Quinn's tiers.** `Great Healing`, `Superior Healing` and `Supreme Healing` -- the three
potion tiers 0.4.0 unlocked through the herbalist's errands -- existed only in Barcelona, which by act 8
is seven acts behind the player. They are on his shelf now at 3, 2 and 1, stocked through
`CInventoryItemGeneratorAdditionalMagic` exactly as the herbalist stocks them, since they are
`InventoryAddition`s applied to a base potion rather than items in their own right.

**A correction that changed the build.** The first pass read his haggling nodes -- a promised 10 percent
at `20 Haggling Step 1`, 15 at `25 Haggling Step 2` -- saw that there is exactly one `CMerchantAI` on the
map, and concluded the discount was dialogue only. It is not. Each haggle reply carries
`CAdjustMerchantPriceMultiplierAction{Price Multiplier Adjustment=-0.1}`, guarded by a
`Merchant Player selected Haggle Option` checker and paying XP through two anchors. It is a complete
little system and it works. Three cloned shops at 1.8/1.7/1.4 had already been built on the wrong premise
and were removed; **the mechanism was in the game the whole time, one field below the text I read.**

### The bird men, and the enemy they already shared

Fazeem's encounter in `01 Desert Sprawl` is one of the better things in act 8, and it is a confidence
trick. To get through it you must first hear about the bird men **from the desert merchant**, then pass
**Speech 70** to claim you know secrets about rain, then **Barter** to be paid for them (either side of
50 -- both branches work, they just change the excuse), and finally **IN 6+** to invent the detail that
does the real work: that the blood of an Assassin makes rain. They believe it, and
`Talked Fazeem into attacking Assassins` retargets Fazeem and the bird men near him onto
`Scripted Custom 1`, which is the Assassins.

**There is no other way out.** `10 Money` buys you off for 30 gold and sends you away, and every other
reply in the tree -- including *"I think I'll be going now"* -- fires `Make All Bird Men Attack`.

Faction tests in that tree: **none**. Which is odd, because the con's entire payoff is pointing these
creatures at the Assassins, and there is a faction in this game whose reason for being in this desert is
that the Old Man twice sent knives into Saladin's tent.

So a Knight of Saladin now has a fourth route to the same relay, and it is not a bonus line on the
existing one -- it is the encounter done without the trick:

> *"I am not here about rain. I am here about the men in black who use this road - the ones who sent
> knives into the Sultan's tent. Do they take from you as well?"*
>
> *"Knife. Men. Wear. Black. Take. Our. Eggs. Take. Our. Water. Take. Our. Young. For. Sport. You. Hunt.
> Them? True? Lie. And. We. Eat. You. Now."*
>
> *"True. My order crossed a sea and a desert to end them and will not leave until it is done. Kill them
> wherever you find them. The bodies are yours."*
>
> *"Black. Knives. Bleed. Same. As. Men. Bleed. We. Watch. Road. We. Take. Them. All. Go. Kill. Your.
> Share. Leave. Ours."*

It fires the same three actions the con fires, the XP anchor included, and it is asserted equal to them
rather than reimplemented.

**What it costs, so the faction is a trade and not a discount.** The con *pays*: `21 Rain Secrets
continued` hands over gold on both Barter branches, because you are selling something. The honest route
earns nothing but the alliance. The trickster gets the money; the knight skips four gates -- the
merchant's tip, Speech 70, Barter and IN 6+ -- and gets certainty. A knight who also has the Speech can
still run the con instead; the reply sits above it, it does not replace it.

### Recorded, not built

- **Backtracking does not retro-fit him.** The checker is read by each map's arrival, so a map you
  walked through *before* telling the order to ride has no escort on it until you leave and come back.
- **There is no `Saladin Midlevel`.** The goblins have one; Saladin has `IS` and `Highlevel` and nothing
  between, so Blessed cannot be distinguished from Aswaran without authoring a new can. This tier reads
  two steps, not three.
- **Exalted has nothing to do with the order.** It is granted by the Way Crystal collection, which just
  promotes you inside whatever order you belong to; the same block hands Templars Paladin and Inquisitors
  Hallowed. An order-specific route to the top rung is a separate question from reading it.
- **`Templar Highlevel`, `Inquisitor Favored` and `Inquisitor Highlevel` are still referenced by nothing.**
  This tier spends Saladin's because act 8 is Saladin's country; the other two orders have the same hole
  in their own.

**The `balanced()` trailing-newline trap bit for the fourth time.** Wrapping the vanilla greeting chain in
a new conditional produced a line reading `}}`, because the slice ends at the closing brace and excludes
the newline after it. The rule is now written into `tools/lhbuild.py`'s header, where it did not stop me
reading it and then doing it anyway.

## 0.22.0 - the Talker and the Thief

**Released 2026-09-27. Unplayed.** One release for a week's work that all came out of a single question:
what does act 7 offer a character who did not build for combat? It is recorded in four sections below --
[0.21.2](#0212---the-druid-master-hears-you-shipped-in-0220) the faction refusals,
[0.21.3](#0213---act-7s-speech-route-and-the-three-sneak-cans-shipped-in-0220) the Speech route and the
Sneak cans, [0.21.4](#0214---toulouse-was-already-finished) the Toulouse audit, and
[0.21.5](#0215---the-field-the-builder-forgot-in-twenty-three-places-shipped-in-0220) the trigger repair.
In short:

| | |
|---|---|
| **The Druid Master can be talked down** | Speech 130, on her lore branch only, for 3,000 XP against the 2,500 her corpse is worth. She was the only act boss in the game with no alternative to the fight |
| **She reads who is refusing her** | Four gated refusals, one each for Inquisitor, Wielder, Templar and Knight of Saladin. She had been offering to destroy the Holy Office in identical words to a sworn officer of it |
| **Sneak works, for the first time since the Sewers** | The game's three unreferenced `Sneak moreequal` cans now open the temple's secret passage -- skipping 03 Stone Chamber and 04 Antechamber of Lore, 1,030 spawn entries -- and spot the ambush behind the last chamber's wall |
| **A repair of our own making** | Twelve Fixt triggers shipped without `Auto-Flip Switch`, the field that lets a trigger re-arm. Ten are the charm sweeps that are meant to fire on a **second** visit, after the ogre charm is broken |
| **And a retraction** | Toulouse was carried here since 0.21.1 as the largest reactivity gap in the game. It has 121 gates, 31 of them ours. The claim was a measurement error and is withdrawn in place |

**The finding under all of it.** Act 7 is not combat-gated anywhere: every transition poly on the
critical path is open at map load, the four shut ones are optional side rooms opened by walking up to a
door, `Stop the Druids` completes on the Alamut crossing poly, and nothing in the game records or checks
whether the Druid Master died. A pacifist could already walk past the boss to Alamut and be told they
stopped the druids. What was missing was never a route -- it was any reason to have built a talker or a
thief, in an act that had **zero** Speech, Barter, Lockpick or Sneak checks anywhere inside the shrine.

## 0.21.5 - the field the builder forgot, in twenty-three places (shipped in 0.22.0)

**Released 2026-09-27 in 0.22.0. Unplayed.** Revising act 7's ambush check to Toulouse's mechanic meant making a
trigger polygon repeatable, and that turned up a defect in this project's own builder rather than in the
game.

`lhbuild.touch_poly()` writes a `CTouchingPolygonTriggerAI` and omitted six of the nineteen fields vanilla
gives one. Five are inert defaults. The sixth is **`Auto-Flip Switch`**, which governs whether a trigger
re-arms after the player walks out of it.

**Vanilla writes the field on 756 touching triggers out of 756, and sets it to 1 on 286 of the 294 that
are repeatable.** Not one omits it. Fixt had twenty-three triggers built with the short helper, and
**twelve of them were repeatable** -- meaning twelve polygons that are supposed to fire again on a later
visit were shipped without the field that lets them.

The twelve are exactly the case the field exists for. `charm sweep 1` in `Mountain Pass` fires
`the charm lifts` **only if** `ogre charm broken` already exists, so the intended order of events is: walk
in and nothing happens, go and break the charm, walk back in and it lifts. That second visit is the one
the missing switch puts at risk. Ten of the twelve are charm sweeps across Mountain Pass, Ogre Cave and
Ogre Sprawl; the other two are `guard room poly` in `4 Undercroft` and `Jehanne sees the relic secured` in
`9 Burial Chamber`.

All twenty-three now carry vanilla's full field set in vanilla's order -- the eleven one-shots included,
so that the helper's output and the shipped files agree from here on. Fifteen maps, +209 bytes each.

**The helper is fixed at the source**, and the fix is checked against the game rather than against a list
typed from memory: a test parses the field names out of `Eavesdrop trigger` (polygon),
`Mathuo-Iapetus Bubble trigger` (oval) and `To Exalted Chambers poly` (interaction specifier) and asserts
the helper's output matches, name for name and in order. A `touch_oval()` was added alongside, since the
oval form is what watches for a named NPC rather than the player. A post-fix sweep confirms **0 of 538**
touching triggers across the mod's maps are missing the field.

**What this does not claim.** Eight vanilla repeatable triggers ship with `Auto-Flip Switch=0`, so the
value is not simply "always 1" -- zero is a real mode, not a mistake. What is not defensible is *omitting*
a field the game writes 756 times out of 756, and the twelve affected triggers all want the re-arm.
ReVa was unavailable this session, so the exact engine semantics are inferred from that distribution
rather than read out of the binary.

### And the builder now lives in the repo

`lhbuild.py` -- the module every build script in this project imports -- had been living in a session
scratchpad under `AppData\Local\Temp` ever since it was extracted from the Montserrat prisoner build,
which is also why its docstring still described that one build rather than the library. A helper that can
ship twelve broken triggers should not be untracked and one `%TEMP%` sweep from gone.

It is now `tools/lhbuild.py`, with:

- a header that says what it is, and records the two rules that have each cost a release -- an `Array`
  must declare the count it actually holds, and a generated block must carry **every** field vanilla
  writes, not only the load-bearing-looking ones;
- paths off the environment instead of one machine's: `LIONHEART_MODTOOLS` and `LIONHEART_VANILLA`, with
  the `files/` root derived from the module's own location rather than `Path.home()`;
- `tools/test_triggers.py` beside it, which parses the field lists out of three real vanilla triggers
  (`Eavesdrop trigger`, `Mathuo-Iapetus Bubble trigger`, `To Exalted Chambers poly`), asserts the
  builders match name for name and in order, and then sweeps every `.zax` the mod ships to confirm no
  touching trigger is missing the re-arm field. It is the check that would have caught 0.21.5 at the
  moment the bug was written.

The Montserrat constants at the top are kept -- `hover_poly()` still reads `HOVER_TREE` -- but they are
now labelled as leftovers rather than passing for library API. The scratchpad path keeps a two-line shim
that executes the repo copy, so older scratch scripts cannot silently import a stale fork.

## 0.21.4 - Toulouse was already finished (shipped in 0.22.0)

**Audit only, 2026-09-27. No game files changed.** Toulouse has been carried in this log since 0.21.1 as the
largest reactivity gap left in the game -- "roughly 846 replies with not one gated on anything." It was
opened for work and the claim did not survive ten minutes of measurement.

### What is actually there

| | vanilla | with Fixt |
|---|---|---|
| replies across the twelve Toulouse trees | 424 | 552 |
| `Custom Requirement=` blocks | 90 | **121** |

Inside those blocks: `Demokin IS`, `Sylvant IS`, `Feralkin IS`, `Feralkin NOT`, `Human IS`, `Human NOT`,
`Tainted race - feralkin or sylvant`, `Wielder IS`, `Inquisitor IS`, `Templar IS`, Speech at 25/40/45/50/55/95
**and** `Speech lessthan` at 040/050/055/095/100, Barter at 35/40/50 and `Barter less than 50`, `IN 4+`, `IN 5-`,
`IN 6+`, `IN 7+`, `PE 7+`, `Outwit 7 greater or equal`, `Outwit 8 greater or equal`. `ToulouseLethos` alone
carries 61 of them on 157 replies.

**Thirty-one of those 121 are 0.15.0's own work.** So the measurement did not just miss the shipped game --
it missed a ten-tier Fixt release in the same region, and then recommended building it again.

### Why the number came out zero

Every one of them is a `Custom Requirement=`, and the census counted `Requirement=`. That is the **fourth**
time this session the same mistake has produced a confident wrong answer about reactivity:

| claim | where the gating actually was |
|---|---|
| "the Knight of Saladin's tree has zero orphan nodes" | `20 alamut` was there, differing only by case |
| "the Druid Master has 25 replies and no gates" | her race chain is map-side, in `conversation trigger` |
| "act 7 is the emptiest act in the game" | true per spawn, false per reply -- it is the most gated |
| "Toulouse: 846 replies, not one gated" | 121 `Custom Requirement=` blocks, 31 of them ours |

### The corrected census

Replies gated by **either** field, per region, playable content only:

| region | replies | named | custom | gated |
|---|---|---|---|---|
| 2 Montserrat | 331 | 28 | 27 | 17% |
| 5 Nostradamus | 485 | 39 | 43 | 17% |
| 6 Barcelona Attack | 475 | 27 | 54 | 17% |
| 8 Alamut | 1,161 | 99 | 100 | 17% |
| 4 Crypt | 518 | 46 | 57 | 20% |
| **3 Montaillou (Toulouse included)** | **3,629** | **182** | **779** | **26%** |
| Wilderness | 1,867 | 252 | 323 | 31% |
| Sewers | 372 | 76 | 50 | 34% |
| 1 Barcelona | 6,814 | 1,156 | 1,254 | 35% |
| 7 English Shrine | 219 | 47 | 38 | **39%** |

Toulouse is in the second-most-gated region in the game. The four thinnest are Montserrat, Nostradamus, the
Barcelona Attack and Alamut, all within a point of each other -- and that ranking is a starting point for a
real audit, **not** a finding. Two attempts at ranking regions by identity-awareness inside this same session
both came out wrong, in opposite directions, because the grep behind them kept sampling one of the two fields
a gate can live in. No region goes on the backlog again on the strength of a count alone.

### What Toulouse actually has left

Every node in the twelve trees was walked from every map that fires one, following replies:

- **38 nodes** are never reached.
- **32 of those are duplicates** -- the same bark text sitting in two sibling trees, where the map happens to
  name the other copy. `50 Ogre 1` and `50 Ogre 2` exist in both `ToulouseGeneral` and `ToulouseOgres`; the
  player hears them either way.
- **Six are genuinely unused**, in full: two of those duplicate ogre hovers, `100 Mercury goodbye`
  (*"Hmmm, perhaps you are right. Goodbye, fleshling."*), and `103 Noise 1`, `2` and `3`, each of which reads
  **"Crap."**

That is the whole of it. `cortes` and `Cervantes`, logged here as cut Toulouse companion arcs, are Barcelona
companions -- their trees live under `1 Barcelona`, and Titan Village only carries their leaves-the-party
node, exactly as five other region maps do. Their orphans belong to act 1 and are counted there.

**Toulouse is finished.** It was finished in 0.15.0.

### And it contains the best stealth encounter in the game

The question that opened Toulouse was whether it uses Sneak well. It does -- better than act 7 now does,
and better than anywhere else, because it does not use the `Sneak moreequal N` cans at all. It reads the
**live sneak toggle**, `Derived Character Attributes/Sneak Enabled`, and those are the **only three checks
against that attribute in the entire shipped game**, all three inside one polygon on one map.

The setup: Mathuo guards the trail west out of the prison village with Poimaino. Talk Mathuo into sharing
his flask of quicksilver and the two of them walk off their post to drink it, which is the **non-combat
route** to the escape -- the alternative is killing both, and Alexander's escape node tests for exactly
those two outcomes (`Path is clear`, or neither guard alive).

While they drink they hold a six-line conversation, and `Eavesdrop trigger` -- a polygon around the
drinking spot, armed when the scene starts -- decides whether you get to hear it:

| slot | what it does |
|---|---|
| **Enter** | `CIfAction` on `Sneak Enabled > 0`. Sneaking: **nothing happens** and you listen. Not sneaking: `eavesdrop relay` fires |
| **Repeat** | re-tests `Sneak Enabled < 1` continuously, so dropping out of sneak part-way through still catches you |
| **Exit** | if you were seen, *"Stupid runt. Now where were we?"* -- and the scene resets so you can try again |

Getting caught is not a fail state either, it is a countdown: *"Wait, I think we have an eavesdropper. By
Atlas I wish I could squash that bug, but Lethos would have my head"*, then *"if you aren't gone by the
time I count to three I'll squash you"*, then 1... 2... 3... *"To arms! The fleshling is trying to release
the prisoners!"* Back out before three and you keep the option.

And it has a second act. Once the prisoners are gone the two guards panic on camera -- *"If the elders
find out they'll have us chewing gravel for months"* -- and agree a trap: *"I know, I'll hide in the pen
and make human noises. You go stand guard and see if you can lure that damn fleshling into the pen."*
`Poimaino kill box` is that trap, a polygon around the pen; step inside and both titans retarget onto the
player, step out and they go back to `Scripted Custom 2`. The bait plays: `103 Noise 1`, `2` and `3`, which
are a stone giant doing an impression of a human -- *"Umm... ahem... Why are these titans so mean?"*,
*"Boo-hoo, it is so hard being a puny human creature."*

**The implication for 0.21.3.** Act 7's three new Sneak checks use skill thresholds, which is right for
reading wear on a flagstone but is the weaker of the two mechanics for the ambush, where the fiction is a
character moving quietly enough to hear a man breathe. `Sneak Enabled` is the better instrument and the
game already proves it works. That is a candidate revision, not a defect.

## 0.21.3 - act 7's Speech route and the three Sneak cans (shipped in 0.22.0)

**Released 2026-09-27 in 0.22.0. Unplayed.** 0.21.2 asked what act 7 gives a character who did not build for
combat. The answer was nothing, and the reason was not the one expected.

**Act 7 is not combat-gated anywhere.** The critical path is 01 Outside Shrine, 02 Temple Initiate,
03 Stone Chamber, 04 Antechamber of Lore, 05 Exalted Chambers, then the Alamut crossing -- and every
transition poly on it is **open at map load**. The only four shut ones are optional side rooms
(Meditation 2 and 3, the Secret Chamber, the Inner Sanctum) and each is opened by walking up to a
door and using it, not by clearing a room. `Stop the Druids` is completed by the crossing poly
itself, and **nothing in the game records or checks whether the Druid Master died** -- no checker,
no quest state, no reference to her outside `05 Exalted Chambers` and her own tree. A character who
never swings a weapon can already walk past the boss to Alamut and be told they stopped the druids.

What was missing was not a route. It was any reason to have built a talker or a thief:

| skill | checks inside the shrine (maps 02-10) | checks in the whole act |
|---|---|---|
| Speech | **0** | 1, on Captain Isabella, on the approach map |
| Barter | **0** | 4, same NPC |
| Lockpick / Sneak / anything else | **0** | **0** |

### The Druid Master can be talked off the ley lines

She was the only act boss in the game with no alternative to the fight: all 29 of her replies, the
four 0.21.2 added included, fired the same relay. The argument is built out of her own lore node --
*"your ancestor, Richard the Lionhearted, sealed the Disjunction... Ironically, Richard is buried in
the next chamber"* -- so the route opens only after asking how the ritual works, and only at
**Speech 130**, the tier act 8 uses for the Old Man:

> *"You have it backwards. Richard did not seal the Disjunction from a distance - he closed it with
> his own blood, in this hill, and whatever is under the floor learned that blood by heart. You mean
> to open the lines nine paces from his grave with the only living Lionheart in England standing in
> the room."*

She does not fold on one line. `50 the bloodline` puts it back: *"Finish it. If you are wrong I lose
a night of work. If you are right I lose the hill and everyone standing on it."* Press it home and
she calls the fires out, for **3,000 XP** against the 2,500 her corpse is worth.

**The teardown is the whole trick.** The conversation runs inside a `CBeginNonInteractiveSequence`
opened by her trigger poly, and the **only** thing in the level that ends it is the fight relay --
so a reply that simply declines to fight would leave the player standing with the controls disabled
and the camera locked on her. The stand-down relay therefore reproduces the fight relay's first
three actions exactly (end the sequence, drop `Druid conversation camera`, `CSendAIDoneMessage` to
release her from the scripted task) before doing anything of its own. After that it is small: her
line, the award, `CRemoveCategoryAction` taking `Enemy` off her, a cleared target type, and a
checker. Nothing else is needed, because the ambush and the summoned golems are armed **only** by
the fight relay, and the last chamber's sole other live spawns are the Assassin Master and the
Galileo prisoner. Stand her down and the room stays quiet.

### Sneak does something, for the first time since the Sewers

Four `Sneak moreequal` requirement cans ship with the game. Exactly **one** is referenced, twice,
both in act 1 (`Waterfall Passage`, `SecretQuestGuard`); **10, 20 and 25 are referenced by nothing
in the entire game**. All three are spent here.

**25 and 10, on the temple secret door.** Behind it is a strongbox and a passage running straight
through to the Exalted Chambers. Vanilla opens both -- and this is the part worth recording -- from
the `From Last Level` **spawn point**, which only fires when you come *back* into 02 from 05. So the
shortcut exists purely as a return convenience and cannot be found going forward at all. A Sneak 25
character opening that door now reads the floor and gets both, which skips 03 Stone Chamber and 04
Antechamber of Lore: **1,030 spawn entries**. Sneak 10 gets the draught and nothing else. The check
hangs on the door's own `After Opened` slot, where 54 vanilla doors already read `$Instigator` as
the player, and the success path fires vanilla's own relay rather than a reimplementation of it.

**20, on the ambush.** The fight relay opens `Secret Door Ambush` and switches on the soldier
generator behind it in the same breath as the fight. A touch poly using **the boss conversation's own
polygon** -- so the geometry is provably walked over -- now sets a checker, and each of
her four opening nodes gains a reply that spends it: *"there are men behind that wall to your left,
close enough that I can hear one of them breathing, and somebody has cut a summoning ring into the
floor between us."* It fires a variant of the fight relay that leaves the ambush in the wall. Her
summoned golems still come, and she answers: *"Stay where you are, all of you. Nobody springs a trap
that has already been counted."* 500 XP.

**Revised after the Toulouse audit.** That check first shipped as `Sneak moreequal 20` alone, which fired
on anyone who walked past with the right number on their sheet. Titan Village holds the only three checks
in the game against the **live** sneak toggle, `Derived Character Attributes/Sneak Enabled`, and uses them
for precisely this kind of moment, so the ambush check now wants **both**: the threshold, which keeps it a
build reward, and the toggle, which makes it something the player does. The poly also became repeatable
(`Trigger Only Once=0`), so a character who crosses it walking can step back, sneak, and cross again --
Toulouse resets its eavesdrop scene for the same reason.

That change surfaced a gap in this project's own tooling. `lhbuild.touch_poly()` writes a short
`CTouchingPolygonTriggerAI` and omits **`Auto-Flip Switch`**, the field that lets a trigger re-arm after
the player leaves; vanilla's `Eavesdrop trigger` sets it to 1. Every previous use of the helper wanted a
one-shot, so it never mattered, and a `Trigger Only Once=0` poly written with it would not have retried
reliably. The trigger's field set and order are now asserted equal, name for name, to Titan Village's.

Act 7 finishes at **219 replies and 47 named gates**.

### Two claims withdrawn on the way

- The 02-to-05 shortcut was described here as a secret with one key to find. It is not findable at
  all in vanilla; it is a return convenience. The Sneak check is its **first** forward key, not a
  second one.
- The Sylvant opening node looked like it was missing its `Is Default Reply=1`. It carries the
  marker on its third reply rather than its last. Both replies fire the same relay, so nothing is
  wrong with it, and it was left exactly as vanilla wrote it.

Gate 0 earned its keep: the three canned Sneak references were first written as
`Dialog/Requirements/Sneak moreequal 25`, and the real path is
`Dialog/Requirements/Skills/Sneak/...`. The reference check caught all three before deploy.

## 0.21.2 - the Druid Master hears you (shipped in 0.22.0)

**Released 2026-09-27 in 0.22.0. Unplayed.** Act 7 reviewed under the lens that found the Daeva, with a very different
result: **the act is finished.** All thirteen trees it opens carry **zero orphan nodes and zero
voice-recorded orphans**, nothing in its folders is unplaced -- no unopened tree, no unfielded template --
so 0.19.0 closed it out properly, where the Pyrenees had 27 recorded orphans nobody had touched.

**And a correction to this project's own headline about act 7.** It has been called the emptiest act in the
game, and per spawn it is -- 9.6 replies per 100 spawn entries, still the worst. But by proportion of
reactivity it is the **best in the game, by a factor of two**:

| act | replies | gated | gated % | replies per 100 spawns |
|---|---|---|---|---|
| **act 7** | 208 | 42 | **20%** | 9.6 |
| act 8 | 1,161 | 99 | 9% | 125.6 |
| act 4 | 518 | 46 | 9% | 18.0 |
| act 6 | 475 | 27 | 6% | 25.9 |
| act 3 | 3,629 | 182 | 5% | 328.4 |

So act 7's problem was never that it fails to react. It is that there is so little of it to react with: 208
replies where act 3 has 3,629. That is a different criticism from the one this project has been making.

**A second correction, and the same mistake as the Knight of Saladin.** An earlier read here recorded that
the Druid Master has 25 replies and no gates. She is in fact **already race-reactive** -- her map part
`conversation trigger` chains `Demokin IS`, `Feralkin IS` and `Sylvant IS` to pick between four greetings,
each with its own temptation and its own refusal: *"A sylvant I may be, but even the elemental part of me can
sense the danger in what you are doing."* The gating is map-side, so counting `Requirement=` in her tree
found none. **Third time this session that a selector's reactivity was missed by measuring the tree.**

### What was actually missing

Her temptation is an explicitly political offer, and she made it in identical words to everyone:

> *"Power beyond belief! The dragon will allow us to crush our enemies utterly! Think -- the Inquisition, at
> last, destroyed, and all those touched by magic allowed to walk freely in the world again."*

Faction tests in her tree: **none.** On her map part: **none.** So she pitched the destruction of the Holy
Office to a sworn Inquisitor in the same breath she used on a Wielder who wants precisely that, and a
Templar and a Knight of Saladin heard it unchanged. Four gated refusals now answer the same sentence from
four positions, joining the three refusals already on the node and leaving its default last:

| gate | the answer |
|---|---|
| `Inquisitor IS` | *"You have just offered the destruction of the Holy Office to a sworn officer of it. I will repeat that at your trial, if enough of you survives to have one."* |
| `Wielder IS` | *"You are offering me the one thing I have ever wanted, and you are offering it with a dragon. I have carried a spirit long enough to know what asks a price that size."* |
| `Templar IS` | *"My Order crossed a sea to keep a relic out of your hands, and you have just told me why. I am no longer curious about you."* |
| `Saladin IS` | *"You are promising to settle a quarrel I am not in. Saladin's men did not ride this far to watch a dragon arbitrate Europe."* |

All four fire the vanilla `Fighting the Druids Last Chamber` relay with an empty goto and a Fight Icon, which
is exactly what her three existing refusals do, so nothing about the encounter's flow changes -- only who is
speaking. Act 7's gated share rises from 42 of 208 to **46 of 212**.

**The deploy check earned its keep.** The new tree pushed the file count from 325 to 326 and the first install
ran against a stale manifest, so `data.dat` came out older than the files it was supposed to contain. The
verifier refused it and named the fix. That is the third time this session that check has caught something a
Gate 0 pass would have let through.

## 0.21.1 - the Daeva

**Released 2026-09-27. Unplayed.** A review of the Pyrenees region asked whether 0.15.0 had done enough
there. It had not, and the Shapeshifting Daeva was the clearest miss: **both its trees are untouched by Fixt**,
31 nodes and 69 replies each, with **nine replies gated at Speech 95-110** -- one of only four
talk-instead-of-fight encounters in the game -- and **27 orphan nodes** between them. It is a recurring nemesis
that tracks the player across Barcelona, Toulouse and Montaillou and reacts to which relic of Zarathustra they
carry. Two of those orphans are fixed here.

**`4 Ring` was written and never used.** `Prophet Polygon` on `01 Hamlet Exterior` gates the whole confrontation
on a `COrAction` of two item checks -- `Amulet of the Prophet` **or** `Ring of the Prophet` -- and then, whichever
you hold, always opened Trueform's `4 Amulet`: *"Ah, you have a bauble from that accursed prophet."* So the Ring
had its own written reaction -- *"You bear a powerful relic, mortal. Something of the prophet Zarathustra's if
I'm not mistaken"* -- and no player ever heard it. The opener is now a `CConditionalAction` on which relic is
actually in the pack, so the Amulet keeps its line and the Ring gets the one written for it. Both relics are
real items; the Ring is found in `15 Witch SecretCave`.

**`3 Undefeated` is the Montaillou escape, and nothing fired it.** Titan Village plays the matching Toulouse
line, `35 teleport out of toulouse` -- *"you will find me in Montaillou, Lionheart, away from these meddlesome
titans!"* -- from a `daeva deactivator` poly. Montaillou already had a `shapeshifter deactivator` relay doing
the same mechanical work and never speaking, so the creature left without a word. It now says the line it was
given: *"this exertion has left me ravenous... that lake town has all of my favorite flavors."* Appended to that
relay's existing action array, Item Count 6 to 7.

**The build error, third instance in one day.** Lifting the `4 Amulet` opener out of its `Then=` slot produced a
slice ending at `}` with **no trailing newline**, so the next line ran onto the brace and
`resource_format` failed inside `CSortList2D`. The same mistake broke act 8's tier 1 and tier 5. All three
passed a brace-count assert first -- equal `{` and `}` do not prove correct nesting -- and only the round-trip
parse caught them. Written up in the array-splice memory with the fix: after any slice taken to
`balanced()`, terminate it.

### What this release does not fix, and it is most of it

The region still has **43 orphan nodes** across twelve Toulouse trees, and -- the larger finding -- **not one
gated reply in the whole region.** `TitanAndre` carries 229 replies, `ToulouseLethos` 157, `ToulouseRhea` 132,
`ToulouseIapetus` 85, `ToulouseTereo` 75: roughly **846 replies, zero faction, race, skill or karma checks**, in
a region whose entire subject is choosing a side in a war between ogres and titans. Act 1 carries 2,000
state-gates; Toulouse carries none. That is a reactivity tier, and it would be the first one built in a region
that already has all the words.

> **This paragraph is wrong, and it is left standing because the claim shipped in 0.21.1's release notes
> and forum post.** It was produced by counting the `Requirement=` field and nothing else. The twelve
> Toulouse trees carry **121 `Custom Requirement=` blocks**, and inside them are race checks (Demokin,
> Sylvant, Feralkin, Tainted, Human and their negations), faction checks (Wielder, Inquisitor, Templar),
> Speech from 25 to 95 tested in **both** directions, Barter 35 to 50, Intelligence 4/5/6/7, Perception 7
> and Outwit 7/8. Ninety of those are vanilla's own; **0.15.0 added the other thirty-one**, which means the
> measurement did not merely miss the shipped game, it missed this project's own Toulouse release. Act 3
> as a whole sits at **26% of replies gated** -- above Alamut, the Crypt, Nostradamus, Montserrat and the
> Barcelona Attack, all of which are near 17%. Toulouse was never the reactivity gap. See
> [0.21.4](#0214---toulouse-was-already-finished) for the audit that retired the claim.

### The Daeva of Pain collects on a debt the game already promised

**Two corrections came out of building this, and the second one changed the design.**

First: the relics do **not** stop the shapeshifter healing. `Ring of the Prophet` and `Amulet of the Prophet`
both grant `+3` AC, `+4` to a second attribute, and Slashing Damage Resistance -- `+10` on the Ring,
permanent, and `+100` on the Amulet, temporary. Defensive items with a dialogue trigger attached.

Second, and this is the one that matters: **without a relic the fight cannot be won at all.** Killing
`form 3` or `form 4` fires `Form Relay`, which re-activates `clone generator 2/3/4` and
`demon clone 2/3/4` with **no conditional and no item check of any kind**. Meanwhile the
`true form generator` -- the only version of the creature that fires nothing on death and therefore stays
dead -- is activated by exactly one thing in the level, `Prophet Polygon`, which is the relic check. So a
relic-less player fights an unbreakable loop, and `2000 using speech` says so out loud: *"The relic of the
Prophet renders you vulnerable."* The true form additionally heals **20-25 HP every second** from a
`CGiveHealthToCharacterAction` inside its `CSkeletonAI`.

**And the Daeva of Pain in Barcelona's Inquisition Pit already promises to pay for this.** Node
`300 Free Demon yourself`, vanilla's own text: *"Ahhh...the shackles fall away and my power returns! My
judgment will be swift and merciless, but to you, **I have a debt to repay**..."* The game states the debt
and never collects it. This does.

Barcelona now records **which** service was done, because the two are not equal work:

| how he was freed | Barcelona hook | what he owes |
|---|---|---|
| you lured the wizard to him | `Wielder Pan Take down Demon Crosses` -> `Fixt Faust freed the Daeva of Pain` | breaks the loop, the true form comes up **bound** (no heal), **and he arrives and fights it with you** |
| you broke the crosses yourself | `Player Take down Demon Crosses` -> `Fixt freed the Daeva of Pain alone` | breaks the loop and the bound true form -- or, if you can use it, **Nanghaithya's true name** instead |

The loop-breaking is a new template rather than a runtime edit: the heal cannot be pulled out of a spawned
creature without removing its brain, so `Fixt Shapeshifting Daeva bound.can` is the true form with the
`CGiveHealthToCharacterAction` deleted -- same race, same 2750 XP, same everything else, and it round-trips
through the parser clean. `Form Relay` now asks first whether the debt is owed; if it is, a relay deactivates
`Form Relay` so the clones stop coming and puts up the bound form instead. On the Faust route it also spawns
`Monster Cans/Extraplanar Inquisition Jail` -- whose `User Assigned Name` is, already, **Daeva of Pain**, at
HP 900 / AC 200 -- tagged `Player Friend` and pointed at `Enemy`.

**Where he arrives, and a placement bug caught by the tester asking.** Because his generator is a clone of
`true form generator`, he inherited its position: **(375,326), radius 15 -- the shapeshifter's own spawn
point.** He would have materialised inside the creature he came to fight. He now arrives at **(280,260)**,
which is `From Giants Cave`, a real player spawn point and therefore proven walkable ground: 116 units from the
true form, on the side the player approaches from, so he comes in at the cave mouth behind you rather than on
top of the target, facing turned to look at the fight. The two true-form generators keep (375,326) between
them, which is correct -- only one ever activates, and the bound one inherits ground vanilla already proved.

For the record, the whole encounter sits in the hamlet's north-west corner: the four disguised forms at
(564,218), (652,219), (556,290) and (654,291), the true form at (375,326), and the nearest player arrival
`From Giants Cave` at (280,260). Toulouse's copy is on `Titan Village` at (902,230) and (1000,217).

**Each route is now a scene rather than a spawn.** The first version had him teleport in silently with no
dialogue and no companion action, and an inherited `GetCloseThenTriggerAndFight` specifier that had no business
on an ally. Both routes were rebuilt on the tester's direction.

**Helping route: they trade barbs first.** `Fixt Pain and Nanghaithya trade barbs` runs a proper
non-interactive sequence on `Demon camera attractor` at (421,345), beside the true form -- begin NIS, camera up,
three balloons at 1, 4.5 and 9 seconds anchored alternately on `Daeva of Pain` and `True Form`, then end NIS and
the camera drops and they fight. The barbs turn on names, which is what this whole encounter is about. He opens
with *"Nanghaithya. Still wearing other people's faces. Ninety years in this valley and you have not once
learned to be looked at."* She answers by naming him -- *"Aeshma. They kept you in a box under a church and you
came out of it grateful, running errands for the thing that opened the lid. Ahriman will hear which of us was
the coward."* -- and he closes it: *"He will hear it from whichever of us is still standing, so tell it
carefully."* Aeshma is the daeva of wrath, and naming him that way follows the game's own habit: it already
names Nanghaithya, Aka Manah and Druj.

**Other route: he is sitting on the wall where your spirit warns you.** `Daeva Top scene relay` at (1311,1052)
is the part that has the spirit companion say something is ahead -- *"There is a very powerful spirit near to
us. Be wary!"*, or *"Something just ahead would like to separate your head from your body"*, depending which
spirit you carry. That relay now also seats him at (1377,1058), **only when the lesser debt is owed and the
larger is not**, with a `GetCloseThenTalk` specifier and no target type at all, so he waits rather than fights.
Talking gets `1 the warning`: *"Your spirit has already told you there is something ahead. Spirits are good at
that and no use at all afterwards. I am here to be of use afterwards, and then we are done with each other."*

**And the name is earned in that conversation, not assumed from the flag.** `2 the name` is where he gives it
up -- *"A daeva cannot lie about its name and cannot stand to hear it said correctly; say it to her face and
she will have to stop and argue with you instead of eating you"* -- and sets a third checker,
`Fixt knows Nanghaithyas name`. The three Speech replies on the relic-less nodes now gate on **that**, so
refusing him at `3 declined` costs the route: *"I paid in the only coin I had and you have left it on the
wall."*

**The true name is the more interesting half.** All six of the shapeshifter's `Speech moreequal 95` entry
points sit on relic-only nodes, so a talker without a relic has no route at all. The name supplies what the
relic supplied: three new replies on `1 Introduction`, `10 Montaillou if fought in Toulouse` and
`20 Montaillou met in Barcelona`, gated on Speech 95 **and** the lesser-debt checker, opening
`2000 using speech` -- *"Nanghaithya. A demon in a Barcelona cell gave me your name, and it owed me the
favour."* So mercy in act 1 becomes a capability in act 3, and which capability depends on the character you
built.

**One pacing question for the playtest, stated rather than hidden.** The debt check is the first action in
`Form Relay`, but deactivating a relay part-way through its own array does not appear to abort the rest of it,
so the final wave of clones probably still spawns alongside the true form. That reads as the shapeshifter
throwing its last bodies and then dropping the disguise, which may be better than a clean switch -- but it is
a guess about engine behaviour, not a verified outcome.

The remaining 23 Daeva orphans, and the region's 43, are still open.

## 0.21.0 - the Doomed Plateau

**Released 2026-09-27. Opened, measured and built the same day after a review asked whether the Crypt and England additions actually broke up their combat -- they did not, and the measurement is recorded below. Unplayed.**

### Why this release exists

A review of 0.19.0 and 0.20.0 asked the question the project had never measured: is the game more *fun*, and
did the act-4 and act-7 additions break up the monotony they were meant to break up. Counted by placement
rather than volume, **no**:

| act | Fixt parts | conversations | merchants/heals | reply-less balloons | spawn variety added |
|---|---|---|---|---|---|
| 4, the Crypt | 18 across 11 maps | **1** | **0 / 0** | **22 of 26 placements** | **+0** |
| 7, England | 14 across 11 maps | 5 | 3 / 3 | 4 | +201 |

And the placement was the problem. `10 Garrison Camp` -- a genuinely new map, 63 parts, a real 31-reply
conversation -- hangs off `1 Crypt Entrance` and exits only back to it, so it is a dead-end side room reached
at **cumulative 2% of the act's combat**. Everything after it -- `2 Retreat of Souls` at 782 spawn entries,
`7 Doomed Plateau` at 1,055, `8 Ante Chamber` at 328, `9 Burial Chamber` at 218 -- got reply-less balloons and
nothing else. **Effectively 100% of the Crypt's combat happens after its last respite.** England's Templar
camp sits at maps 02 and 04 of 11, and maps 03 and 05-09 received **zero** Fixt parts between them, 1,010
spawn entries including `03 Stone Chamber` at 547.

A balloon on a corpse pile is a subtitle on the monotony. It makes the grind legible; it does not shorten,
vary, or make it optional. **Act 2's `4 Undercroft` -- 130 parts, 3 spawn entries, five conversations, spawn
points named `Pen Start`, `escaped loud`, `escorted`, `delivered` -- is the one time this project built the
thing properly, and it was never repeated.**

### The tester's better idea, and what it turned up

The first plan was a mid-act respite room off each act's combat midpoint. The tester replaced it with
something better: **the Plateau is a battle between armies, so give the undead captains -- unique fights, some
of which can be talked out of it.** That is a better fit, because the Plateau's problem is not a missing
rest stop, it is 1,055 spawn entries of the same fifty-six templates.

**The map's retarget machinery does exactly what the idea needs** -- `CSetTargetTypeAction` appears **118
times** on it. Every horde generator -- `Zombie Skeleton` x16, `Festering Undead` x10, `Soul Reaver` x10,
`Terror` x5, `Activated Ghoul` x5 and a dozen more, **81 placements in all** -- sets
`Valid Targets=Player,Scripted Custom 2`, and **every horde can carries `Category=Enemy,Undead`**, checked
across eleven templates. So retagging a single creature as `Scripted Custom 2` turns the entire horde onto it,
and pointing it at `Enemy` turns it onto them. That is the Fazeem retarget from act 8, and it is the map's own
idiom.

**A claim of mine to withdraw, and it matters for the evil route.** The first version of this section called
the Plateau "a real two-army fight already" and treated the Templar garrison as a faction a defector could
join. **It is not.** The garrison's twenty generators set `Valid Targets=Player,Player Friend` -- the undead
Templars **attack the player and the player's companions** -- and their cans carry `Category=Undead` with no
`Enemy`. `Scripted Custom 1` and `Scripted Custom 2` are carried as categories by exactly **six actors each**,
all of them `NonInteractiveSequence Actor`s in the Joan of Arc intro; the 81 and 22 target counts are
generators pointing at tags that nothing outside that cutscene wears. So the Plateau holds **two mutually
indifferent hostile factions that both attack the player**, plus a scripted skirmish at the door.

What survives that correction is the part the tier depends on: the horde does target `Scripted Custom 2`, and
the horde does carry `Enemy`, so the turn works exactly as built. What changes is the reading of the garrison
-- and it makes the *evil* route the better-supported one, since the knights are hostile to you already.

And the fiction was already written. The Templar garrison **does not know it is dead** -- *"Another monster
seeking to capture the holy relic? You too will be destroyed!"* -- recruits the player on `Templar IS` /
`Templar NOT` with a `<Lie>` option, and ends with *"Find Jehanne, she can help you."* Joan of Arc is on the
map with **53 nodes and 157 replies** gated on all four orders, all five races, sex, and Speech 45 and 80.

### The captain content was already in the files

**`Boss Lich`, three tiers, is the largest piece of finished-but-unfielded creature content this project has
found.** Three races under `Races/Enemies/Undead/`, a sprite at
`Cache/Models/Characters/Monsters/Undead/Boss Lich.mdl16`, and **seventeen GR2 files** in
`Models3D/Enemies/Boss Lich/` -- `Idle`, `Death`, `GetUp`, `Hit`, `Hit_Shield`, `Fidget`, `Punch`,
`OneHandedSwing_01/02`, `Bow_Attack`, `CrossBow_Attack`, three body models. `Ghoul Male HUGE`, a creature the
game *does* field, has **one**. And **no character template anywhere in the game points at any of it**, so
nothing could ever spawn it.

The races are a designed encounter, not a stat bump:

| | HP | AC | melee | Cold | Poison | Disease | Electrical | Piercing | **Fire** |
|---|---|---|---|---|---|---|---|---|---|
| Boss Lich | 385 | 80 | 80 | 100 | 100 | 100 | 20 | 20 | **10** |
| Tough | 462 | 80 | 80 | 100 | 100 | 100 | 85 | 65 | **25** |
| Super | 520 | 80 | 90 | 100 | 100 | 100 | 95 | 75 | **35** |

An enormous pool that is trivial to hit, immune to cold, poison and disease, hardening against electrical and
piercing as it tiers -- and fire deliberately left weakest at every tier.

**And `Second Guardian` is the Druid Master defect again.** Its three cans exist and are fielded -- all three
tiers on `2 Retreat of Souls` at weight 1, plus Bryce Folly and two random maps -- but they run on
`Races/Enemies/Undead/Ghoul Male Large` at HP 150/200/275, while `Races/Enemies/Undead/Second Guardian` at
**HP 250/400/600, AC 175/215/300** is used by nothing. The Lance's second guardian shipped at roughly half
its designed strength on a generic ghoul block. Three `Race=` lines repoint it.

One thing checked and **not** available: the `Summoned *` races are the player's summoning-spell fodder, not
free for a lich. An earlier read of mine called them unused; that was a bad query, which counted only races
whose cans get placed on maps.

### What was built

Three captains on `7 Doomed Plateau`, each an edit of the map's own smallest horde generator,
`Festering Undead Generator` -- whose three `Max Party Mojo` groups give a captain **tier-scaling with party
level for free**, and whose `After Action` already tags spawns into the battle.

- **The Bonecaller** (`Boss Lich`, 1500/2000/2500 XP) -- the only captain that can be reasoned with, because a
  lich commands and remembers, **and the only one with two outcomes**: it can be released, or recruited. Three ways into its real conversation, `Wielder IS`, `General Divine Skills
  moreequal 80`, or `Speech moreequal 80`; two ways out of the fight, `Speech moreequal 110` or Divine 80. It
  is bound to a siege whose author is long dead: *"the pointing has outlived the hand. I cannot put the order
  down."* Talk it down and it is retagged `Scripted Custom 2,Undead` and pointed at `Enemy` -- **the horde
  turns on it and it turns on the horde**, using the map's own tags, and *"I have raised every one of them
  twice and I know exactly where the joints are."*
#### Both sides of the Bonecaller, forked on karma the way the Old Man's is

Once the two-army claim was withdrawn the design got better rather than worse, because the garrison is
**hostile to the player already** -- its twenty generators target `Player,Player Friend`. So taking the Lich's
side needs no invented faction, and the tags fall out cleanly. Vanilla forks the Old Man's own talk-down on
karma at 600 into `250 beyond` and `251 beyond EVIL`; this is the same fork on the same node.

| | retag | it targets | the garrison | the horde | XP anchor |
|---|---|---|---|---|---|
| **release** -- Speech 110 or Divine 80, **ungated by karma** | `Scripted Custom 2,Undead` | `Enemy` | ignores it | **turns on it**, it fights back | `Fixt Talked the Bonecaller Down XP`, 2000 |
| **ally** -- `Karma LESS 600` | `Player Friend,Undead` | **turns on it** (it targets `Player,Player Friend`) | ignores its own commander | it attacks all undead, the knights first | `Fixt Sworn to the Bonecaller XP`, 2000 |

**Anyone can free it; only the wicked can recruit it.** The release arm is deliberately left ungated by karma,
against vanilla's habit of gating both arms, so mercy stays available to every character and the alliance is
the distinctly evil act rather than merely the other half of a menu. `21 the bargain` is where it lands:
*"Then we are two things with an order each, and yours is newer. Break the door and I will walk in behind you,
and what the knights have been dying for ninety years to keep will be handed to me by something still
breathing. That is better than the siege. That is very nearly a joke."*

**And swearing to it costs the garrison.** All three of `UndeadTemplar`'s recruitment replies -- the
`Templar IS` one, the `<Lie>` one, and *"No, but I must help you protect the relic"* -- now carry a
`Custom Requirement` that fails once `Fixt sworn to the Bonecaller` is set, so *"Are you a Knight? Have you
been sent to reinforce us?"* has no good answer left and *"Find Jehanne, she can help you"* is closed. The
Fight Icon reply stays ungated, because the door to violence should never be the one that shuts. Both patterns
are vanilla's: a reply carrying **both** a named `Requirement` and a `Custom Requirement` occurs eight times in
the shipped trees, and `CActionExpression` wrapping `CNotAction` around `CCheckExistenceAction` is exactly how
`torquemada requires Goblin Khan alive.can` is built.

- **The Bonewright** (`Second Guardian`, restored to HP 600 / AC 300 at the top tier) -- **while it stands,
  the fallen keep getting up.** A `CRepeatTimerTriggerAI` on the creature fires a relay every 22 seconds give
  or take 6 that activates a wave generator and deactivates it six seconds later; its
  `CSetDestroyedScriptActionAction` shuts the relay and the generator off for good. So the endless stream has
  a source and a lever, which is the single most useful thing that can be said to a player standing in 1,055
  spawn entries.
- **The Revenant Sergeant** (`Lance Guardian`, HP 475 / AC 275 at the top) -- three phases. It opens fighting
  the knights and ignoring you; at **66%** it whistles its section off the knights and onto you; at **33%** it
  drops the hand signals and `CSetTargetTypeAction` narrows it to `Valid Targets=Player`, so it abandons the
  battle and comes for you alone, through its own dead.

Every position is an existing generator's coordinates, which is the strongest spawn-and-reach evidence the
map offers. Neither of the two mute captains gets dialogue it cannot use: they get balloons that make their
mechanics legible, which is the difference between a subtitle and an explanation.

**Two build errors, both caught by Gate 0.** The clone base carries a `Dynamic Properties` `Comment` repeating
its own name, so three captains shipped still calling themselves Festering Undead until an assert caught it.
And the `Item Count` bump after splicing into `After Action` used a first-occurrence replace, which hit the
**Activity** array instead -- Gate 0 reported *"Array at /Activity says 3 items, holds 2"*. Fixed by bumping
the count at the matched offset. That is the fourth instance of the array-splice rule this project has
recorded, and the first where the wrong array was an outer one.

### Still open

- The Bonecaller's turn is the first time this project has made an enemy change sides. It wants a playtest
  more than anything else here: if the retag does not take, the Lich simply stops fighting, which is a
  degraded but not broken outcome.
- **XP for talking it down: done 2026-09-27.** In vanilla's own idiom --
  `CGiveExperiencePointsToAllPlayersAction{Get XP Frome=<anchor>, Experience Points To Add=1}`, where the
  anchor part carries the real amount in `Dynamic Properties` and the literal stays 1. That shape is used
  **728 times** in the game, so this also settles the bird-men read: `Experience Points To Add=1` beside a
  named anchor is not a placeholder. The new anchor `Fixt Talked the Bonecaller Down XP` carries **2000** --
  the same value vanilla puts on its own talk-solution, `Talked Fazeem into Fighting Assassins XP`, and a
  figure sitting between the Bonecaller's 1500 kill award and its Super tier's 2500. Note that if the horde
  finishes the turned Lich, the kill XP goes to the horde and not to the player, so 2000 is the whole of what
  the peaceful route pays.
- The other four acts' midpoints are still bare. `03 Tourniquet of Pain` (act 5, 604 spawns, **0 merchants, 0
  heals**) and `03 Stone Chamber` (act 7, 547 spawns) are the next two candidates, and both already carry four
  map transitions, so a room hangs off proven ground.

## 0.20.0 - Alamut

**Released 2026-09-27. Surveyed, swept, built across six tiers and reviewed the same day, unplayed.** Act 8, `Levels/8 Alamut`. The last unsurveyed act, and by a distance the
biggest: **eleven maps, 15,498 level parts** -- more than acts 6 and 7 together -- 1,218 live combatants,
26 dialogue trees, 202 player replies, 34 of them gated.

| map | parts | combatants | trees | balloons | traps | hidden areas | containers | MB |
|---|---|---|---|---|---|---|---|---|
| 01 Desert Sprawl | 4,230 | 122 | 4 | 3 | 0 | 1 | 1 | 2.57 |
| 02 Shifting Dunes | 5,650 | 186 | 5 | 2 | 0 | 2 | 3 | 3.31 |
| 03 Sand Dragon | 489 | 13 | 1 | 0 | 0 | 0 | 0 | 0.34 |
| 04 Maw of the Assasin | 1,378 | 199 | 1 | 0 | 21 | 11 | 16 | 1.49 |
| 05 Acid Wash | 334 | 40 | **0** | **0** | 7 | 7 | 4 | 0.38 |
| 06 Chamber of Torment | 1,408 | 261 | 1 | 2 | 24 | 9 | 19 | 1.54 |
| 07 Dark Temple | 946 | 170 | 4 | 12 | 11 | 14 | 7 | 1.14 |
| 08 Final Encounter | 346 | 143 | 6 | 57 | 0 | 0 | 0 | 0.81 |
| END GAME Calle Perdida | 269 | 50 | 9 | 17 | 0 | 0 | 1 | 0.75 |
| END GAME Nostrodomus Demesne | 147 | 1 | 1 | 0 | 0 | 0 | 0 | 0.11 |
| END GAME Siege Map | 301 | 33 | 2 | 4 | 0 | 0 | 0 | 0.49 |

### It is the opposite of act 7

Where the English Shrine was 19 enemy families with `Soldier` at 73% of everything, Alamut is **88 families
across 131 distinct templates, with a top-4 share of 53%** -- second only to the Crypt's 82 families at 43%,
and the most varied act in the second half of the game. Assassins, guard dogs, desert beasts, zealots,
assassin masters and spellcasters, and two dragons. It also ships **63 real traps and 46 hidden areas** --
counted as mechanisms, not regex hits, which is the mistake act 7's first survey made.

### A finding I had to withdraw, and it is the important one

Twelve ending trees are **opened by nothing**, with zero references anywhere in the game -- not from a map, a
tree, a can, or their own VO folders:

`GoodEndingAllDie`, `GoodEndingAllSurvive`, `GoodEndingDavinciDies`, `GoodEndingGalileoDies`,
`GoodEndingOldManEscapesAllDie`, `GoodEndingOldManEscapesAllLive`, `GoodEndingOldManEscapesDaVinciDies`,
`GoodEndingOldManEscapesGalileoDies`, `GoodEnding PLAYER TALK ENDING`, `EvilEndingAllDie`, `EvilEndingAllLive`,
`Evil Ending PLAYER TALK ENDING`.

For about ten minutes that read as *the game's entire ending matrix is dead*. **It is not.** The matrix is
alive and lives inside the trees `08 Final Encounter` does open, and those orphan files are its superseded
predecessor -- an earlier implementation as separate files, replaced by nodes inside the character and spirit
ending trees. Their node names are the giveaway: the orphaned `GoodEnding PLAYER TALK ENDING` holds
`15 Galileo Talk Amazed` and `17 DaVinci Talk Evil1`, and **both of those exist and are wired inside
`Galileo Ending` and `DaVinci Ending`.**

The live machine is **fourteen named relays on `08 Final Encounter`**, one per outcome, and **every one of them
is fired** -- checked on `Relay Name=`, which is the field relays actually use:

| | DaVinci and Galileo live | DaVinci dies | Galileo dies | both die |
|---|---|---|---|---|
| Old Man killed | GOOD / EVIL | GOOD | GOOD | GOOD |
| Old Man escapes | GOOD / EVIL | GOOD | GOOD | GOOD |
| talked to death | GOOD / EVIL | -- | -- | -- |

So the ending does vary by who survived, by whether the Old Man escaped or was killed or was talked into his
own defeat, and by whether the player took the good or the evil road. **Act 8's ending is intact**, and those
twelve files are the fifth superseded draft this project has found -- the same shape as
`defenders hate player trigger` and the `Prevent the Druids` quest husk. They want recording, not wiring.

**This is the third time in two acts that "opened by nothing" meant "superseded", and the second time I
counted the wrong field before checking what a working example uses.** Any tier built here should start from
that assumption.

### A review pass over 0.19.0 and 0.20.0, 2026-09-27

Five classes of defect that Gate 0 and the structural audits cannot see, checked across all 78 files the two
releases touched: a dialogue reply firing a relay that lives on one map while the conversation can happen
elsewhere; references that do not resolve; companion release names that do not match a generator's `New Name`;
reply-less nodes opened as trees and reply-bearing nodes opened as balloons; and Fixt-authored nodes with more
than one stage direction.

**One real finding, and it is the companion machinery in both releases' newest work.**

A `CTriggerRelayAction` names a relay, and a relay is a **part on a map**. Grumdjum's and the knight's specifier
swaps were fired from nodes a companion *carries with him* -- `300 player speaks to goblin as companion`,
`300 companion joins you`, and the knight's dismissal on `3 Return` -- while the relays sat on
`01 Desert Sprawl` and `02 Shifting Dunes`. So the one map the companion is least likely to be standing on when
you dismiss him is the only map where the swap could fire. Dismissing Grumdjum in the Dark Temple would have
released him and left his interaction pointing at *"What can Grumdjum do for you?"* for someone who was no
longer his employer, with the rejoin node unreachable.

**Fixed by putting the swap inline in the reply, which is what vanilla's own `3 Return` does for this exact
operation** -- `CRemoveAIAction` and `CAddAIAction` on `$Trigger`, in a `Custom Action`, with no relay in it.
Seven relay triggers inlined: six in Grumdjum's tree, one in the knight's. Inline actions have no home map.

**And the honest qualifier: firing a relay cross-map is routine vanilla practice, so this was never proven
broken.** `Guard Esteban` does it 22 times, and `Machiavelli`, `Jafar`, `Lord Relican` and two Toulouse trees do
it too. The engine may well resolve relays globally. The change was made because the dependency was
unnecessary, not because the pattern is known to fail -- and the three now-unfired `Fixt ...` relay parts are
**deliberately left in place, inert**: if inlining misbehaves in play, re-pointing the tree back at them is a
one-line fix, and removing them cost two failed attempts already. They are no-ops, recorded here so a later
cut-content sweep does not mistake them for something unwired.

**Grace was flagged and is fine; the check was too coarse.** Her two switch relays looked reachable from
`Port District.zax` in act 1. They are not: the replies that fire them sit on `502 arrive in england grace
relived 2` and `503 druids`, both **goto-only**, reached only from the arrival conversation on
`01 Outside Shrine` where both relays live -- and her `CReleaseCompanionAction` is on
`502 grace companion asked to return`, which that same map opens. The check asked which maps open *any* node of
a tree; the question was which maps can reach *that reply*. **0.19.0 needs no change.**

**Two of the five classes turn out not to be defect classes at all.** Vanilla routinely opens reply-less nodes
as trees -- `GoblinVillager / 1 Greeting N Demokin` on ten maps, `Wilderness Traveler Banter`, `ShylockeGoons`
-- and routinely opens reply-bearing nodes as balloons, including `OldMan / 1 Conversation Start` in act 8's own
opening cinematic and every `Ogre Canned` line in the Wilderness. So neither shape is evidence of anything, and
act 7's tier 5 note that called the first one a defect overstated it: the change made there was still right for
that scene, but the pattern is not broken in general.

**The rest came back clean.** Every `CReleaseCompanionAction` names a companion some generator actually spawns
(`Grace`, `Knight of Saladin`, `Goblin Grumdjum`). No `Dialog Tree File`, `Perk`, `Canned Expression`, `Race`
or `Requirement` reference in any touched file fails to resolve. Every specifier swapped in by the new inline
blocks points at a node that exists. And the six nodes carrying more than one stage direction are **all from
releases before 0.19.0** -- three in Grumdjum's tree, one in the Khan's, one in Rakeb's, one on the goblin
guarding the Woodcutter's daughter -- already on the recorded backlog, and none from these two releases.

### Tier 6, built 2026-09-27: the last act learns who arrived at it

**Counted properly, act 8's reactivity is thinner than the survey's headline suggested.** The survey put it at
34 of 202 replies gated and called it the best ratio in the back half of the game. Counting only the fifteen
trees a map actually opens -- the twelve superseded ending files are not among them -- it is **30 of 176, 17%**,
and the shape matters more than the ratio: **every single gate is a skill or karma threshold.** Barter 40, 50,
95; Speech 70, 100, 130, 180; Karma above or below 400 and 600. Not one reply in the act reads a faction, a
title, a quest, or anything the player chose in the seven acts before it.

Two numbers make the absence concrete. Of the **17 title perks** in the game, exactly **one** -- `Merchant
Slayer` -- is read anywhere in act 8. And the four order cans *are* read, but only **map-side**, to pick which
greeting the Knight of Saladin speaks; no reply in any tree reads them at all. **The last act of the game does
not know who arrived at it.**

#### The Old Man reads who came for him

`40 ruse` is his first confrontation node and it already offers five ways to answer, four of them ungated and
all saying the same thing in different words. It gets one more per order, each drawn from that order's own
history with the Assassins, and each going where the rest go -- `45 combat`, where he answers *"You are no
champion, and you are certainly not King Richard's equal."*

| gate | the line |
|---|---|
| `Saladin IS` | *"Twice your knives found Saladin's tent, and twice they found nothing in it. I am what came back."* |
| `Templar IS` | *"The Temple has sent you coin for sixty years to keep your knives out of our chapter houses. I have come to close the account."* |
| `Inquisitor IS` | *"I have put men to the fire for a tenth of the heresy you have spoken since I walked in. You will not be burned. You will simply be ended."* |
| `Wielder IS` | *"Something else lives in me, and it has never once lied to me about what it wants. Can you say as much for the thing that lives in you?"* |
| `Goblin Horde Highlevel` | *"The Great Khan sent proud warriors after you once and not one of them came home. The Horde calls me Champion now. Count this as their second attempt."* |

The goblin line is not invention: **`300 kill old man`, in Grumdjum's own recorded tree, is where it comes
from** -- *"Many years ago, the Great Khan sent proud warriors to slay the Old Man of the Mountain. None
survived that ill-fated encounter."* Tier 4 made a Goblin Champion the only player who can bring a goblin to
Alamut; this lets that player say why. And the collision with `45 combat`'s *"You are no champion"* is free.

**No mechanical benefit is attached to any of them.** They are recognition, which is what this tier is for, and
they all end in the same fight. The talk-him-down path stays exactly as demanding as it shipped -- Speech 100,
then 130, then 180, with karma branching at 600 and a check that the Weird Woman told you about him, which is
genuinely good reactivity and wanted nothing from us.

#### The Knight of Saladin answers the order he greets

His three greeting variants differ properly -- a Templar is told *"it is an honor to stand with one of the
Knights Templar"*, a Knight of Saladin is called *Brother* -- and then **all three offer the identical three
replies**, so the recognition dies in his opening line. Two gated replies and two nodes fix that:

- **`Templar IS`** -> *"Our orders have been paying this man's order to leave us alone. Does that sit in you the
  way it sits in me?"* -> `22 the tribute`: *"Coin sent to a killer is a promise that he may go on killing, only
  somewhere else and to someone poorer. Today we send him something other than coin."*
- **`Saladin IS`**, on both the male and female greeting -> *"They sent knives into Saladin's own tent.
  Twice."* -> `23 the tent`: *"Both times the guard woke before the blade came down. Saladin forgave a great
  many things in his life and he never forgave that. You carry his name into the one house he could not reach."*

His tree carries **no recordings at all**, so new nodes cost nothing in voice consistency -- which is why the
answers are his rather than the player's.

#### What this tier deliberately did not do

The other three live trees with ungated replies were left alone: `AlamutAssassinCan` (7 replies), the five
spirit and character ending trees (3 each, all inside non-interactive sequences), and the `Desert Merchant`,
whose four Barter gates are already the right kind of check for a merchant. Adding order lines to an ending
cutscene would mean writing around a camera; adding them to a merchant would mean a merchant who cares about
crusading orders. Neither is what the act is short of.

**Act 8's six tiers are done.** The act had the thinnest reactivity in the game and the largest single piece of
finished-but-unwired content left in it; both are addressed, and nothing in it is unplayed for want of
building.

### Tier 5, built 2026-09-27: the Knight of Saladin's companion arc, and no bonus

**The read stands: act 8 has no faction-differentiated reward, and none is invented here.** What the tier
turned out to contain is a companion arc that half works, plus a defensive pass that stopped halfway -- all
repair, no new content beyond one player line that dismissal could not exist without.

**Correction first, because it is mine.** The tier-5 read recorded that his tree has **zero orphan nodes**.
It has one: `20 alamut`. Five replies -- *"What is inside Alamut?"*, on all four greeting variants and on
`3 Return` -- point at **`20 Alamut`** with a capital A, and the node is lowercase. That is the **second**
case-mismatched goto found in this act, after Grumdjum's two `70 Accept the Offer`. Case-folding may resolve
both on its own, since the engine folds case for entity names, so these are normalisations rather than proven
repairs -- but the orphan claim was wrong either way, and the question *"what is inside Alamut?"* asked of a
Saladin knight in front of Alamut is too obviously the first thing a player says to leave on a guess.

**The two recruit paths were not equal, and the first-time one was the broken one.**

| | escort AI | companion flag | what talking to him then opens |
|---|---|---|---|
| `3 Return` -> *"Let's go."* (a return visit) | **yes** -- swaps `CSkeletonAI` for one built on `CGaurdNearMovingPosAI` | yes | `3 Return` again, which is coherent |
| `30 go` (the **first** meeting) | **no** | yes, after 0.5s | `666 Rejoin` -- *"Do you need my help again?"* |

So a player who recruited him the first time they met him got a companion who **kept his standing guard AI**
and, on being spoken to, asked whether he should rejoin -- while already recruited, and following nobody.
`30 go` now carries the same escort swap `3 Return` does, lifted verbatim from it, and the switcher that fires
alongside it points at `3 Return` instead of the rejoin prompt.

**And he could not be dismissed at all.** `666 Rejoin`'s second reply, *"No, wait here."*, carried **no action
whatsoever** -- the same dead-reply shape as tier 3's `WizardCan1` and tier 4's two Fight Icons, fifth instance
in this act. There was no `CReleaseCompanionAction` anywhere in his tree. `3 Return` gains one reply --
*"Hold this ground and wait for me."* -- which releases him and fires a new `Fixt Knight dismissed` relay that
arms `666 Rejoin`, so the rejoin prompt is finally the thing its text says it is. Rejoining restores the escort
AI too, which the vanilla reply did not: it set the companion flag and left him rooted.

The cycle is now: greeting -> `30 go` -> escorts you; talk -> `3 Return` -> *"Hold this ground"* -> released
and waiting; talk -> `666 Rejoin` -> *"Yes, please rejoin me"* -> escorts you again, or *"No, wait here"* which
is correct at last, because now he **is** waiting.

**The defensive pass he never got.** His companion race carried `OneHandedMelee 200` -- a finished, strong
offence -- against **HP 150 / AC 145**, which is the weakest companion in the game placed in the last act:

| companion | act | HP | AC |
|---|---|---|---|
| Knight of Saladin, as shipped | 8 | 150 | **145** |
| Grace O'Malley (0.19.0) | 7 | 165 | 190 |
| Grumdjum (tier 4) | 8 | 225 | 200 |
| **Knight of Saladin, repaired** | 8 | **220** | **215** |

The plain `Knight of Saladin` race is AC 100, so the companion race **was** an upgrade -- the pass started and
stopped, exactly as the Priestess ladder did in 0.19.0. Melee 200 is kept untouched, the same way the
Priestess's spell identity was kept: repair the half that is unfinished, not the half that works. He ends
slightly better armoured than Grumdjum and slightly less tough, which is a knight beside a goblin brute, and
neither dominates.

**One thing checked and left alone.** `Fake Companion Generator` on `02 Shifting Dunes` spawns a second
`Knight of Saladin` with an empty `New Name`, no interaction specifier, and a `CSetCompanionAction` in its
`After Action` -- a nameless, mute companion clone. It is **activated by exactly one thing in the game: a part
named `warp`**, which is the `Editor/Test Interaction` developer furniture the cleared-leads sweep counted 758
of. So it is a dev shortcut for testing the companion state, not a shipped path, and wiring it would produce a
companion nobody can address or talk to. Recorded, not touched.

#### Two build errors worth recording, both caught by Gate 0

The escort block was lifted out of `3 Return` by slicing to its closing braces and stitching a new action onto
the tail. That **dropped a brace level**, and Gate 0 said so: *"brace imbalance"*. Rebuilt by inserting the
new action after `Item Count` and bumping the count -- the same rule the array-splice memory already
records, ignored here because the target looked like a tail rather than an array. Then the rebuilt block ended
at its closing brace with **no trailing newline**, because `balanced()` stops *at* the brace, and Gate 0 caught
that too: *"reply not separated by a blank line, in node '666 Rejoin'"*. Both are the same underlying mistake
as tier 1's `05 Acid Wash` parts running together on one line: **a slice that ends at a delimiter does not
include the delimiter's line ending.** Gate 0 caught all three; nothing reached a playtest.

### Tier 4, built 2026-09-27: the goblin companion 0.2.0 deferred to this act

**Grumdjum's twelve `300`-series nodes are all reachable now, and all twelve are voice-recorded.** The arc
was written, recorded, and given no mechanism: `CSetCompanionAction` in his tree counted **zero**, and
`300 companion` -- the entry the whole cluster hangs off -- was opened by nothing, so `300 kill old man`,
`300 companion quips 3` and `300 companion leaves you` were goto-reachable only through a door that did not
exist. 41 of his 42 recordings are now on reachable nodes.

**The tester's call was Grumdjum as the companion and the Khan as a cameo**, and the writing supports it:
Grumdjum arrives as the Khan's emissary -- *"since my Khan has tasked me to aid with your quest, let us seek
the Old Man in Alamut, the Eagles Nest"* -- while the Khan's own `500 Start in Persia` is three nodes of a
man passing through: *"Without a doubt you are surprised to see Rumjun Khan here amidst the sandy dunes. I am
here to cause destruction in this part of the world...and assist you on your journey of bloodshed."* Accept
and he goes off to sow it himself; decline and he takes his brethren east, *"China is very rich and my belly
is very empty."* No companion machinery is invented for him, because none was written for him.

**Both require the player to be a Goblin Champion, and the Khan to be alive.** The tester caught the first
version of this gate, which was wrong, and the correction is recorded below because the reasoning is the
useful part.

`Goblin Horde Highlevel` -- `Goblin Rank > 2` on the `Uber Perks/Goblin Rank` attribute -- **is** Goblin
Champion, the top of the three-tier ladder Fixt built and confirmed in play: Chum 1, Blooded 2, Champion 3.
The Khan gates his own top-tier replies on that exact can, three of them, and it is read all over the
Wilderness by Rakeb, the Patrol Leader, the villagers, the vendor, the entrance guard, and by Joan of Arc and
a Montaillou guard two acts later. Map-side it is wrapped the way `Dream Djinni Map` wraps it:
`CExpressionAction{Expression=CUseCannedExpressionExpression{Canned Expression=.../Goblin Horde Highlevel},
Character to get attributes from=$Instigator}`.

That is the right currency because **Grumdjum's own line says so**: *"since my Khan has **tasked** me to aid
with your quest"*, and he opens with *"Greetings, **goblin friend**"* -- which is precisely how the Khan
addresses a player with standing, against the *"morsel"* he calls everyone else. The Khan detaching one of his
warriors to escort you is the largest favour in that chain, so it costs the top of it.

**The first version gated Grumdjum on having paid him for the River Dryad instead, and that was simply the
wrong thing to read.** The Dryad is Grumdjum's *personal* errand, run at a lake in the Wilderness; it buys
nothing with the Khan, it can be done without ever entering the Warrens, and a player who does only that has
no standing for the Khan to task anybody on their behalf. The invented `Player has met Grumdjum` checker is
removed from the Lake and from the tree's two reward nodes, and `Lake.zax` is byte-identical to its
pre-tier-4 state again.

The Khan's death still blocks both, and that half was right: `Goblin Khan is Dead` is an `Editor/Checker` on
`Inquisition Chambers2` carrying its designer's comment -- *"if this is active, PC killed Goblin Khan before
speking with Torqemada"* -- activated from `Goblin Warrens` and read by `CCheckExistenceAction`, the idiom
vanilla uses **1246** times. So **be the Horde's Champion and leave their Khan breathing, or no goblin comes
to Alamut at all.** Grumdjum additionally has to be alive, via `Grumdjum Dead`, the marker his own Lake
generator sets on his death.

**The lesson, and it is the fifth time this shape has bitten:** the state I reached for was the one I had just
been reading, not the one the content is about. Grumdjum's tree was open in front of me, so his quest looked
like the relationship; the relationship the line actually names lives on a different NPC in a different cave,
in an attribute Fixt itself had built and proved. Before gating restored content, ask what standing the
*writing* claims, then go and find the shipped measure of it.

**What was built.** Five parts on `01 Desert Sprawl`, the act's front door:

| part | what it does |
|---|---|
| `Fixt goblin gate` | an oval on the player's own arrival spawn: Goblin Champion and the Khan alive -> the Khan's cameo, and if Grumdjum also lives -> Grumdjum |
| `Fixt Grumdjum generator` | an edit of **vanilla's own Lake `CGeneratorAI` for this exact character**, with the Lake-specific `After Action` replaced by a death marker and three AIs added beside its interaction specifier |
| `Fixt Khan generator` | the same, on `Monster Cans/Mongol Goblin Khan`, opening `500 Start in Persia` |
| `Fixt Grumdjum is a companion` | swaps his interaction specifier to `300 player speaks to goblin as companion` |
| `Fixt Grumdjum is dismissed` | swaps it to `300 companion joins you`, and has him call `300 grumdjum asks to rejoin` after you |

Both generators sit **within 80 units of `From England to Alamut`**, the spawn the player arrives on, which is
the strongest reachability evidence available and the `walkable is not reachable` lesson applied rather than
re-learned. The generator class is `CGeneratorAI` -- the documented-correct class for an interactable NPC, and
the one vanilla uses for Grumdjum himself -- deliberately **not** the `CSimpleGeneratorForCannedEntitiesAI`
that 0.19.0's Grace generator uses. If Simple turns out not to spawn interactable NPCs, Grumdjum still works
and the difference diagnoses Grace; putting both on one unverified assumption would have risked losing both.

**The barks play at last.** `300 companion quips 1/2/3` run on a `CRepeatTimerTriggerAI` wrapping a
`CShuffledSeriesAction{When Done=Repeat Series}` every 13 seconds give or take 5, and the two injury lines
sit on `CAIHealthPercentThresholdTrigger` ladders at **50%** -- *"If my blood continues to flow, to the
stewpot beyond I will go!"* -- and **20%** -- *"My time is nearly past, I need healing fast!"* All are
anchored `Name of Position=$Trigger`, the companion-bark fix 0.19.0 had to make twice.

**And he can be dismissed and taken back.** Three replies release him (`CReleaseCompanionAction`), after which
he stands where he was and asks after you; `300 companion joins you` -- recorded, and reply-less, so it asked
*"Would you like Grumdjum to join you again?"* with no way to answer -- has its two answers now, and
`300 grumdjum rejoins` confirms: *"At last dark knight, you have come to your senses, now let us beat these
assassins senseless!"*

#### Four defects fixed on the way through, three of them vanilla's

- **`Go to node ID=300 companion leaves you `** carried a **trailing space** on `300 companion`'s dismissal
  reply. Normalised.
- **Two replies pointed at `70 Accept the Offer`** where the node is `70 Accept the offer`. Case-folding may
  well resolve this on its own -- the engine folds case for entity names -- so this is recorded as a
  normalisation rather than a repair, and both are now exact.
- **Two `300`-series replies carried a `Fight Icon` with no action**, offering a fight and closing the
  conversation instead: the same shape tier 3 finished in `WizardCan1` an hour earlier, third and fourth
  instance. Both now call `CGoToCombatAction{Enemy Name=$Trigger}`, which is what vanilla's own `50 Goodbye`
  does two nodes away.
- **The Khan's three Persia nodes shipped `Should Have Voiceover=0` with all three recordings present.** The
  flag was set before the lines were recorded and never updated. Unmuted.

#### One recording with nowhere to go, left alone

`OldMan`-style: `GOBLINGRUMDJUM VOs/130 No more poetry not accepted dryad quest alt.ogg` has **no node of that
name** -- only `130 No more poetry not accepted dryad quest` exists, without the `alt`. An alternate take that
outlived its node. Nothing to wire it to, so nothing is done; recorded here so it is not mistaken for a gap.

#### A near-miss worth recording, because it cost real work

Reverting a failed build, I deleted `files/Levels/Wilderness Maps/Lake.zax` as though it were a file this tier
had created. **It was already a tracked Fixt file**, and the rerun regenerated it from vanilla -- silently
dropping **4,569 bytes** of an earlier release's work on that map. It was caught only because the second run's
byte counts started from a different number than the first. `git checkout` restored it. **The revert procedure
for a partial write must distinguish untracked files from modified ones**: `git status --short` marks them
differently, `??` against ` M`, and only the first are safe to delete.

### Tier 1, built 2026-09-26: the Acid Wash says what it is

`05 Acid Wash` shipped with no dialogue tree and no balloon: 334 parts, 40 combatants, and not one word.
What the silence was hiding is a better piece of design than the act's reputation suggests.

**The map is a sluice.** The floor is cut into a channel with a fall to the west. Step into
`First Trap Trigger` -- an oval of radius 68 at (2947,872) -- and `First Acid Wash Start` clones `acid 01`
onto `First Acid Wash Start Point` at (3316,829), up-slope and behind you. The clone is a `CEntityWalking`
carrying four AIs at once: `CLandscapeAI` cuts the ground away as it travels, `CGoToAI` walks it down the
channel, and a `CLimitedTimeAI` wrapping a `CRepeatTimerTriggerAI` keeps spawning acid steam around the
moving front, each spawn doing `CXRPGDamage` of **20 to 40 Acid, `Defend Against=1`**, scattered on a
`Random Location Delta` of 72.5. Six seconds in, `Clear Ground 01` is cloned behind it to put the floor
back. The relay then deactivates itself and `Activates First Acid Wash Trigger` re-arms it **ten seconds
later**, so the hazard cycles for as long as the player is in the channel. A second gate does the same
thing further west off `Activate Second Acid Wash Poly`.

**And the opposition is ranged-only, by design.** The map fields 15 `Assasin Bow` and 12
`Assasin Master SPELLCASTER` across three tiers each, and **no melee enemy at all** -- they shoot from
terraces and never come down into the channel. A hazard that punishes standing still, and enemies who
make standing still the only way to shoot back. None of which the player was told.

**So the tier is words, and only words -- five balloon nodes in a new `The Acid Wash` tree, and no
mechanism touched.** `1 the channel` names the place and the bowmen on the approach; `2 the first sluice`
fires as the wash launches and states the ten seconds; `3 the second sluice` does the same at the western
gate; `4 the sluice control` says that the switch at the spiked gates is what runs the sluices; and
`5 the gates open` reports what pressing it did.

Every trigger is placed on geometry vanilla already proves the player reaches, which is the
`walkable is not reachable` lesson applied rather than re-learned. Two of the four are **concentric with
`First Trap Trigger` itself** -- radius 300 for the approach and radius 68 matching vanilla exactly for
the wash -- so the naming balloon necessarily fires before the warning, guaranteed by the radii and not by
guesswork about the floor. The third clones the polygon of `Activate Second Acid Wash Poly` verbatim,
`1532, 926, 1815, 981, 1513, 898`. The fourth is centred on the switch, which is interactable and so
reachable by construction. All four are `Trigger Only Once=1` against vanilla's `0`, so the hazard still
cycles while the words do not repeat.

#### A claim I made and withdrew, and it is the one worth recording

For about twenty minutes this tier had a much bigger headline: that the disarm switch's relay,
`End level switch turn traps off`, shipped **five actions of which three were empty stubs** --
`COpenDoorAction{}`, `CPlaySoundAction{}` and `CPrintCombatTextAction{}` -- so that the switch worked and
reported nothing. **That was wrong, and it was my own instrument, not the file.** The relay is complete:

```
COpenDoorAction        Door Name=Spike Door near Switch
CPlaySoundAction       Sound=Doors/Crypt Vyka Coffin.ogg
CDeactivateAction      Target Name=First Trap Trigger
CDeactivateAction      Target Name=Activate Second Acid Wash Poly
CPrintCombatTextAction Text to print=Disarmed trap, Emphasize=1
```

The switch opens the gates it names, plays a sound, disarms both washes and prints its own confirmation.
It reads as three empty braces only because the dump I was reading was skeletonised by a field
allow-list, and the fields inside those three actions were not on the list. **A filter that hides fields
makes every action look empty**, which is the same failure as counting the wrong field, one layer up: the
tool answered a question I had not asked. Checking the raw bytes of the block took one query and settled
it. So the finding shrank to its true size -- the switch is fine, and what was missing was any reason to
believe a disarm switch existed to look for, which is what `4 the sluice control` supplies.

#### Two counting corrections for the survey table above

- **`05 Acid Wash` has seven hidden areas, not zero.** Seven `Activity=CAISecretReveal` parts, at
  (1267-1357, 964-1128), (1554-1693, 1414-1530), (1793-1921, 644-738), (2210-2346, 1422-1483),
  (2621-2704, 1841-1909), (2650-2769, 1075-1280) and (2981-3124, 586-761). The row is corrected. Three
  other rows look low against the same measure -- `04 Maw of the Assasin` counts 31 reveals against a
  recorded 11, `06 Chamber of Torment` 23 against 9, `07 Dark Temple` 22 against 14 -- which is probably
  reveals-per-area rather than an error, since `01` and `02` agree exactly. Re-count those three when
  their tiers are built rather than trusting either number now.
- **Act 8 has no `CTrapAI` anywhere.** Its traps are `CDoorAI` spike gates on the `Trap Spike 1` model,
  opened by `COpenDoorAction` -- 11 on this map, 131 on `04`, 300 on `07 Dark Temple`. A `CTrapAI` sweep
  of this act returns zero and means nothing.

### Leads cleared, so none of these is re-opened

Act 8 was swept for cut content on 2026-09-26 -- unplaced templates, orphan nodes, quest husks, and every
inactive part nothing activates, across all eleven maps. **Seven leads were chased and all seven were
intact.** Recorded the way 0.2.0 recorded the goblin jailor, the captive child on Scar Ravine and the
Woodcutter greeting matrix: these are answered, and re-investigating them is waste.

1. **The ending matrix.** Twelve ending trees are opened by nothing, but they are a superseded
   implementation-as-separate-files, replaced by nodes inside the character and spirit ending trees. The live
   machine is fourteen named relays on `08 Final Encounter` and **all fourteen fire**. Detailed above.
2. **The Knight of Saladin.** Already a working companion recruitable by anyone, zero orphan nodes,
   `666 Rejoin` opened by `02 Shifting Dunes`, on a dedicated `Races/NPCs/Knight of Saladin Companion`.
   Detailed in tier 5.
3. **The Ways Crystal's seven faction conditionals.** `CAssignFactionToCharacterAction` housekeeping that
   re-stamps the player's own order, not a faction reward with empty Fail arms. Its actual reward is flat for
   everybody and completes the Green Way Crystal chain. Detailed in tier 5.
4. **The bird men on `01 Desert Sprawl`.** `Bird Beast Leader in Desert.DialogTree` has **zero orphan
   nodes**, and the whole chain works: Speech 70 opens `20 Rain Secrets`, Barter 50 opens
   `22 Rain Secrets Concluded`, then `25 Looking for Assassins`. Talking Fazeem into attacking the Assassins
   sets `Valid Targets=Scripted Custom 1` on both `Fazeem` and `Bird Man Near Fazeem`, and the map's sole
   assassin generator, `Assassin Generator PILE`, covers all seven assassin types and stamps
   `New Category=Enemy,Scripted Custom 1` -- so the retarget reaches every assassin on the map. Two things
   that look like defects and are not: the reply's `Experience Points To Add=1` is not a placeholder, because
   the anchor part `Talked Fazeem into Fighting Assassins XP` carries `Experience Points=2000`; and the
   shipped designer TODO `Action work in progress=(Change their target to Assassins, Add return dialog to
   Fazeem)` is **stale**, since both halves were implemented -- the retarget in that relay, the return
   dialogue through `Put Return AI NICE on Fazeem` opening `3 Return`.
5. **Both dragons are placed and fought.** `Dragon_Chaos` at 25,000 XP is on `08 Final Encounter` in all
   three tiers; `Dragon_Sand` at 11,000 is on `03 Sand Dragon` in all four. The two templates placed
   nowhere -- `Sand Dragon Hasharid` and `Chaos Dragon Final Scene` -- are **discarded drafts, not lost
   content**: both carry `Experience Points=0` against the placed `Dragon_Sand` can's 11,000, both drop
   nothing, and both point at the `Dragon_Sand` race, so the one called *Chaos* Dragon is not even a chaos
   dragon. Placing either would field a 900-HP dragon worth no experience. Nothing here to restore.
6. **`05 Acid Wash`'s acid works.** Four parts on the map looked dead -- `acid 01`, `acid 02 Landscaper`,
   `Clear Ground 01`, `Clear Ground 02 Landscaper`, all `Active=0` and named by no `Target Name=` or
   `Relay Name=` anywhere. They are **clone sources**, named by `Source Name=`, which is a sixth activation
   field this project had not counted. Nine further Acid Steam parts on the map are `Active=1` and four live
   relays drive them: `First Acid Wash Start` and `Second Acid Wash Start`, each firing its own trigger. The
   known-good confirms the load state too: `04 Clan of the Skull B` has six `Steam Spot` parts and **all six
   ship `Active=0`**.
7. **The remaining inactive parts are shipped debug furniture.** Of the 29 act-8 parts still unexplained after
   `Source Name=` was folded in, every one is an `Editor/Test Interaction` or `Editor/Character Picker` part
   named `warp` -- a developer teleport carrying `CLabelPrinterAI` -- and there are **758 of them game-wide
   across every act**, so they are not act-8 content. The three exceptions are equally empty: a
   `CSpawnPointAI` holding a teleport visual on `08 Final Encounter`, and `prophet provoked` on the
   Nostradamus map, an `Editor/Checker` with **no activities and no actions at all** -- 558 bytes of designer
   marker, with nothing in it to restore.

**The method lesson, which is now the fifth instance of the same one.** Three of these seven -- the ending
matrix, the acid wash, and the bird men -- read as dead only because the sweep counted a field the mechanism
does not use. Relays are named by `Relay Name=`, parts and cameras by `Target Name=`, **clone sources by
`Source Name=`**, nodes by `Node ID=` under `Dialog Tree File=`, quests by `Quest=`. And `Active=0` is the
normal shipped load state for relays, cameras, spawn points and effect clone sources alike, so it is never
evidence on its own. Check a known-good example of the same part type before calling anything dead.

**So the answer on act 8 is that it has no recoverable cut content beyond the tiers below.** The only
genuinely orphaned dialogue in the act is `OldMan`'s `50 old man escapes`, which is tier 2, and the goblin
companion arc, which is tier 4.

### Tiers, in the order they should be built

1. **`05 Acid Wash` has no dialogue tree and no balloon at all** -- 334 parts, 40 combatants, seven traps and
   four locks, and not one word. The same shape as act 7's Inner Sanctum, which turned out to be a vault
   nobody could see. **The acid itself is not the problem** -- it is alive and driven by two relays, per the
   cleared leads above -- so this tier is the map's silence only: a hazard that washes over the player with no
   warning, no name, and nothing said about it before or after.
2. **`OldMan`'s `50 old man escapes`. Read 2026-09-26: CLOSED, it is a superseded draft and must not be
   wired.** The tier is kept at its own number rather than renumbered, because tier 1 is already built and
   referenced by number; only the dragon tier, retired before any building began, was removed outright.

   **The escape is a complete cinematic, and one of the most carefully built sequences in the act.**
   `Old Man Escaping Start Trigger` runs, in order: clear away Galileo's and DaVinci's attackers and the
   spawned enemies; begin a non-interactive sequence; **if the Chaos Dragon is still alive, pacify it** --
   `CRemoveCategoryAction`, `CSetTargetTypeAction` and `CSetCollidableAction`, so it cannot wander into the
   scene, its empty Fail arm being correct since a dead dragon needs no handling; activate
   `Old Man Getaway Portal`; activate `Old Man of the Mountain Fleeing`, whose generator spawns him as
   `Old Man Fleeing` with a `CSkeletonAI` patrol that walks him to `Old Man goto point for escape`; drop the
   spikes; cut to `Old Man is escaping Camera1`; **play `520 Good Ending Old Man Escapes All`**; end the
   sequence; then cut to `Old Man is escaping Camera2` and branch on who survived and on good or evil into
   one of the six `ESCAPE Old Man ...` relays, each of which plays the three spirit endings and hands off
   through `COtherMapAction` to `Good Ending Old Man escapes NIS continue` on the Nostradamus map. Nothing in
   that chain is broken, and `520` plays in **all six** escape outcomes, because the trunk speaks it before
   it branches.

   **So `50 old man escapes` has no slot left, and the reason it has none is the interesting part.** It is a
   draft of the line `520` now carries -- the same beat in different words, *"I live and thus the struggle
   will continue"* against *"do not doubt that my master will return"* -- and **both are voice-recorded**,
   `OldMan VOs/50 old man escapes.ogg` beside `OldMan VOs/520 Good Ending Old Man Escapes All.ogg`. Two
   recordings of one goodbye is what a rewrite after recording looks like, which this project has seen twice
   before in Grace O'Malley's renamed nodes and in the twelve superseded ending trees.

   Two details settle which of the two is the draft. First, **the numbering**: `50` sits in the combat block
   with `45 combat`, `47 combat talk` and `60 old man killed`, while every other closing voice is a `5xx`
   -- so the escape's closing line was renumbered into the ending family as `520`. Second, and decisively,
   **`50` opens with the stage direction `<A dark, ethereal voice surrounds you>`, and in the shipped scene
   the Old Man is not disembodied at all**: he has been spawned as a walking entity and is leaving on
   camera. An ethereal-voice framing is simply wrong for a shot of the man himself, so the line was rewritten
   as him speaking in person. **Wiring `50` would play two contradictory goodbyes**, one of them insisting on
   a bodiless voice while the body walks out of frame.

   One asymmetry that looks like a gap and is not: the **kill** outcomes get two lines, `60 old man killed`
   as he dies and then `500` or `510` in the dark ethereal voice at the head of the ending, while the
   **escape** outcome gets only `520`, in person, and no ethereal line at all. That is the writing working
   rather than failing -- when he is dead something else has to speak for him, and when he is alive he speaks
   for himself. Nor is the both-die escape relay defective for activating no camera where the other five
   activate one: the camera those five add is a DaVinci or Galileo speech camera, and in that outcome there is
   neither of them left to look at.

   **Recorded here so the tier is not re-opened. Act 8's only genuinely orphaned dialogue is now the goblin
   companion arc.**
3. **What acts 6 and 7 left here. Checked 2026-09-26: both hooks are correct and stay, Grace needs nothing,
   and the check found a half-applied fix of Fixt's own instead.**

   **Act 6's two quest hooks are right where they are.** `08 Final Encounter` carries three quest actions and
   all three are properly placed: `Find Galileo and DaVinci` completes on `Galileo Generator`, in the
   generator's own `After Action` -- verified as the generator slot by the field that follows it,
   `New Facing Angle=`, which is the test 0.18.1 exists to enforce; act 8's own
   `Prevent the Old Man of the Mountain...` completes on `Start Here`; and the True Cross pursuit completes on
   `Cross Regret for Player generator`, the `CActionAI` part that hands the item over.

   Two things make the reach-forward correct rather than merely tolerable. **The quest genuinely resolves
   there**: the Old Man's own line is *"Now witness these holy relics undo the prison of creation and restore
   the dark master, Ahriman"* -- the stolen relics **are** the ritual's components, so the Cross is recovered
   at the ritual, and vanilla put the only `TRUE CROSS` in the game on that map. The act-6 half is the
   activation, `CActivateQuestStateAction` with state `BA1CROSS` on the part `The Druids are falling back
   west`, so the quest begins at the crossroads and ends in Alamut exactly as its name describes. **The
   act-6 table above said it ended on the crossroads map; that was wrong and is corrected.**

   **And the bare completions are vanilla practice, not an omission.** A completion fired for a quest the
   player never started looked like something to guard, until the count settled it: of **475**
   `CSetQuestSatusToCompletedAction` in the game, **475 are bare** -- not one is guarded by a quest-status
   check, and the only status class the engine offers is `CIsQuestStatusCompletedAction`, which tests
   *completed*. There is no in-progress expression to guard with, so nothing to add.

   **Grace O'Malley's absence from act 8 is parity, and giving her lines would be invention.** She appears
   nowhere in the act -- the fourteen hits a name sweep finds on `06 Chamber of Torment` are the Tribal skill
   `Animal Grace`. **But neither does Sir Roger**, vanilla's own act-7 companion, who is absent from all
   eleven maps and every tree. Both act-7 companions walk into Alamut with nothing to say, and her tree has
   zero orphan nodes left after 0.19.0, so there is no written act-8 beat of hers going unplayed. Writing one
   would make the Fixt-restored companion more present than the shipped one, which is the same call the
   Saladin bonus got and for the same reason.

   **What the sweep did find is Fixt's own, and it is fixed here.** Checking whether the endgame's reuse of
   act-1 content is safe -- `END GAME Calle Perdida` opens three Fixt-edited trees, `CedricAlsen`,
   `Lord Relican` and `WizardCan1` -- turned up that **every node the endgame opens is untouched by Fixt**, so
   that reuse is clean. But `WizardCan1` was 97 bytes *smaller* than vanilla, and the reason is a
   **half-applied fix**. Vanilla ships a dead reply -- *"Save your flattery and begone."* with a `Fight Icon`,
   an empty `Go to node ID=` and no action, so it promises a fight and closes the conversation -- on **two**
   nodes, `50 Spirit` and `60 Membership`. The 0.1.4-era notes recorded the decision explicitly: *"`60
   Membership` carries a 'Save your flattery and begone' reply with a Fight Icon and no action -- the 0.1.4
   blank-reply shape. Give it the generic wizards' existing hostile relay, or drop it. Recommend dropping
   it."* **It was dropped from `50 Spirit` instead**, and `60 Membership` -- which is the node Fixt itself
   wired into the killed-Relican branch, reachable by goto and opened via
   `01 Conversation Start Wielder Killed Relican` -- still had it. Removed now; the node keeps its four live
   replies and its `Exit Icon` goodbye.

   The lesson is narrow and worth keeping: **a recorded decision is not an applied one.** The note named the
   node, the fix went to its twin, and nothing caught it for nineteen releases because both nodes are in the
   same file and the file's byte count moved in the expected direction.
4. **The goblin companions, which 0.2.0 deferred to this act by name. BUILT 2026-09-27 -- see the tier 4
   write-up above.** The 0.2.0 notes put it plainly:
   *"Grumdjum's companion arc -- ten nodes covering join, dismissal, rejoin, injury barks and combat quips,
   all in rhyming couplets. His join line is about Alamut, the Khan's `500 Start in Persia` is a matching cut
   goblin companion for the same act, and neither has a companion generator on any map. One cut Act 8 feature,
   and it should return with Act 8."*

   It is **twelve** `300`-series nodes in `GoblinGrumdjum.dialogtree`, and **every one of them is
   voice-recorded**: `300 companion` (4 replies), `300 kill old man` (3), `300 player speaks to goblin as
   companion` (2), `grumdjum asks to rejoin`, `grumdjum rejoins`, `grumdjum hurting`, `grumdjum hurting 2`,
   `companion quips 1/2/3`, `companion joins you`, `companion leaves you`. **`CSetCompanionAction` in his tree:
   zero.** Written, recorded, and given no mechanism -- the same shape as Grace O'Malley in 0.19.0, with the
   same fix available: clone a working companion's generator and switch relays.

   `300 kill old man` is his line about killing the Old Man of the Mountain, so the arc is explicitly act-8
   content. Two differences from Grace, both of which make this bigger than her tier: **none of the twelve is
   opened by any map** and only three are reachable by goto, so this needs a spawn point in act 8 as well as
   the machinery; and there is a **second** goblin companion in the same state, the Khan's
   `500 Start in Persia`. A decision comes with it that is the tester's, not mine: whether a goblin walks into
   the Assassins' Persia at all, or arrives with the Khan's war party.

5. **What a Knight of Saladin gets in act 8. BUILT 2026-09-27 as repair, not as a bonus -- see the tier 5 write-up above, which also corrects the zero-orphans claim below. Read 2026-09-27, and the answer is: a greeting, and that is
   genuinely all.** The read corrected two guesses of mine, so both are recorded.

   **He is already a working companion, and anyone can recruit him.** `30 go` -- *"Let's carry the battle to
   Alamut, then."* -- fires `CSetCompanionAction` on `$Trigger` plus a `Knight AI switcher` relay, `3 Return`
   does the AI swap, and `666 Rejoin` is **not an orphan**: `02 Shifting Dunes` opens it, and *"Yes, please
   rejoin me"* re-recruits. His tree has **zero orphan nodes**. His race is a dedicated
   `Races/NPCs/Knight of Saladin Companion`, so he was always meant to be one. **So recruiting him cannot be
   the Saladin bonus** -- a plain human with no order gets exactly the same companion.

   **And the Ways Crystal is not a faction reward either.** Its four faction conditionals -- `Saladin IS`,
   `Inquisitor IS`, `Templar IS`, `Wielder IS`, seven of them in all, every Fail arm empty -- call
   `CAssignFactionToCharacterAction`: they re-stamp the player's own order, which is housekeeping, not a boon.
   The crystal's actual reward is **flat for everybody**: thieving powers, +5 Cold and Electrical Damage
   Resistance, and the flags `Green Way Crystal 5` and `Green Way Crystals ALL FOUND` -- so this is the fifth
   and last of the Green Way Crystals, and the completion of that chain. I had this down as the same
   same-node-on-both-arms defect 0.7.0 and 0.8.0 fixed. **It is not that defect.**

   So the finding is a plain absence rather than a broken mechanism: **act 8 contains no
   faction-differentiated reward of any kind.** `Saladin IS` is read in exactly two places on one map -- to
   choose a greeting, and to re-stamp a faction -- and `Inquisitor IS`, `Templar IS` and `Wielder IS` are read
   only in that same housekeeping. Every order finishes the game on identical terms.

   **A Saladin bonus here would therefore be new content, not restoration, and the tier should say so.** The
   project has added content before -- Quinn's errands, the Templar camp -- but this is not a cut feature being
   put back, and it should not be dressed as one.

   Two restoration-shaped things did turn up beside it, and they are worth having either way:

   - `02 Shifting Dunes` spawns **two `Knight of Saladin` entities and has one talking part**, so the second
     knight cannot be spoken to at all.
   - The knight is **HP 150 / AC 145** on his companion race -- below Sir Roger at 200/200 and below Grace at
     165/190, in a **later** act than either. Whether that is deliberate restraint or the same unfinished
     defensive pass the Priestess ladder had wants checking against act 8's enemies before anything is changed.

6. **Reactivity. BUILT 2026-09-27 -- see the tier 6 write-up above, which corrects this count: it is 30 of 176 across the trees a map actually opens, and every gate is a skill or karma check.** 34 of 202 replies are gated, the best ratio in the back half of the game, so this is a
   smaller job here than it was in acts 6 and 7.

## 0.19.0 - the English Shrine

**Released 2026-09-26. Surveyed and built the same day, unplayed.** Act 7,
`Levels/7 English Shrine`. Eleven maps, 3,481 level parts, 2,035 live combatants, nine dialogue trees,
91 player replies.

### The first version of this survey was wrong, and how it went wrong

It opened by calling act 7 "the best-finished act in the game" on the strength of 47 secrets, ~190 trap
references, 16 locks and 96 containers. The tester's verdict, from having played it, is the opposite:
*"the worst section of the game, it's all combat with the same 3-4 enemies, and there's nothing to do but
wander and fight."* That is correct, and the counts that contradicted it were regex noise counted off my
own greps:

| I claimed | actually | why the first number was wrong |
|---|---|---|
| ~190 traps | **37 traps** | `(?i)trap` also matches `Found Trap`, `Disarm Trap`, `firetrap` and `Lockpick Disarm Traps` -- every trap contains four or five of its own name |
| 96 containers | **40 containers** | `(?i)chest` matches `Secret door1 chest`, `Chest Generator Good` and every model reference |
| 47 secrets | **10 hidden areas** | 47 is the `CAISecretReveal` count, but **37 of them are traps being spotted**, which is the same mechanic as the traps already counted |

Ten hidden areas across eleven maps, 37 traps, 40 containers. For comparison, 0.16.0 *added* 66 traps to
the Crypt and 0.17.0 added 43 to the Caverns. Act 7 does not ship more hidden content than they now have;
it ships less. **Measuring mechanisms is not measuring variety**, and where a metric and a playthrough
disagree, the playthrough is the evidence.

### What the act actually offers, counted properly

**Enemy variety is the worst in the game, by a wide margin.**

| act | spawn entries | distinct templates | families | top-4 families' share |
|---|---|---|---|---|
| 4 Crypt | 3,141 | 159 | **82** | 43% |
| 5 Nostrodomus | 2,524 | 84 | 36 | 71% |
| 2 Montserrat | 667 | 58 | 26 | 71% |
| 6 Barcelona Attack | 1,450 | 68 | 23 | 85% |
| **7 English Shrine** | **2,035** | **58** | **19** | **86%** |

And the concentration is worse than the table shows: **`Soldier` alone is 1,496 of 2,035 spawn
entries -- 74% of everything in the act.** The rest is three flavours of War Golem and some priests. The
tester's "same 3-4 enemies" is literally the case.

**And there is nothing to do between fights.** Across eleven maps:

- **two conversations.** `SirRoger.DialogTree` (66 replies) and `DruidMaste.DialogTree` (25). Every other
  tree in the act is barks or hover text.
- **one quest, with one state** (`Stop the Druids`, `EZIX7Q9L`).
- **one unique item**: the `Ring of Richard Lionheart`, from the statue in `05 Exalted Chambers`.
- **`10 Inner Sanctum`** -- 210 parts, 88 combatants -- has **no dialogue tree, no balloon and no label
  printer**: not one word anywhere on the map. *(Corrected in tier 4 below: it is **not** the act's final
  room, which is `05 Exalted Chambers`, and it is **not** contentless -- it is an unmarked three-switch
  vault. "No secrets" here counted `CAISecretReveal`, the Traps-skill spotting mechanism, which is not how
  its doors open.)*
- the three **Meditation Chambers** are one `ManaTomes` shelf each, plus golems and priests.

### Tiers, in the order they should be built

**1. ~~Give the act its own enemies.~~ Built.** They existed, and they were placed nowhere.

This is restoration, not rebalancing, and it goes first because it is the complaint:

| template | race | fielded |
|---|---|---|
| `Levels/7 English Shrine/Character Templates/Druid` | `Soldier1` | **nowhere** |
| `Monster Cans/English Enemies/Priestess` | `Priestess` | **nowhere, anywhere in the game** |
| `Monster Cans/English Enemies/Priestess Tough` | `Priestess Tough` | **nowhere** |
| `Monster Cans/English Enemies/Priestess Super` | `Priestess Super` | **nowhere** |

Read what that list means. The act is the **English Shrine**; its enemy faction is the **Druids**; the one
line a rank-and-file enemy speaks is `DruidCan1`'s *"Intruder! You won't stop us from awakening the
dragon!"* -- and **the `Druid` template is placed nowhere, so every druid in the act is a generic English
soldier.** Worse, the act's boss, `Druid Master`, has the race **`Priestess Super`** -- she is a
priestess -- and all three Priestess templates are unfielded, so the order she leads does not appear in
its own shrine. (`Levels/7 English Shrine/Character Templates/Knight Templar`, race `Knight Templar 3`, is
also placed nowhere; it is spent on the allied side in tier 2 rather than here.)

Following the 0.17.0 pattern, these go in by twinning existing Soldier generators so every new enemy
stands where the game already spawns one, and it is a **swap, not an addition**: the tester prefers variety
over thinning, and this raises variety without raising the count.

**What went in.** 195 new `Thing to Generate` entries across nine maps, added to existing generator groups
with weights rather than as new generators, so no spawner count changes and every vanilla entry is kept --
audited per map, nothing lost. Placement is **deepest-first**: the front of the act stays an English army
holding a shrine, and the further in you go the more it is actually the cult.

| map | added | on |
|---|---|---|
| 02 Temple Initiate | Druid, weight 1 | 21 of 124 groups |
| 03 Stone Chamber | Druid, weight 1 | 31 of 124 |
| 04 Antechamber of Lore | Druid, weight 1 | 32 of 96 |
| 05 Exalted Chambers | Druid w2, Priestess w1, **Priestess Super** w1 | 16 / 11 / 6 of 32 |
| 06-08 Meditation Chambers | Druid, weight 2 | half the groups in each |
| 09 Secret Chamber | Druid w2, Priestess w1 | 18 / 12 of 36 |
| 10 Inner Sanctum | Druid w2, Priestess w1 | 14 / 14 of 28 |

**The variety metric, computed the same way as the survey table:**

| | before | after |
|---|---|---|
| spawn entries | 2,048 | 2,243 |
| families | 19 | **21** |
| top-4 families' share | 94% | **87%** |
| `Soldier`'s share of everything | 73% | **67%** |

For reference the Crypt is 82 families at 43%. Act 7 is still the least varied act in the game; it is no
longer the least varied by the margin it was, and the change is concentrated where the player is deepest in
the shrine.

### Two balance findings this tier raised, and what was done about each

**The swaps are not XP-neutral, so the placement is weighted rather than uniform.** `Druid` has the *same
race as `Soldier1`* -- HP 75, AC 230 -- and pays **950 XP against Soldier1's 348**. `Priestess` pays 1,949
against `Priest`'s 746. A uniform swap across 1,280 soldier entries would have inflated the act's XP roughly
2.7x. The projected shift as built:

| map | mean XP per spawn | |
|---|---|---|
| 02 / 03 / 04 -- the three big front maps | +4% / +6% / +8% | they carry most of the act's spawns and are touched lightest |
| 06 / 07 / 08 Meditation Chambers | +13% / +15% / +10% | |
| 05 Exalted Chambers | **+54%** | the Druid Master's own chamber, 120 entries |
| 09 Secret Chamber / 10 Inner Sanctum | **+40% / +41%** | 140 and 88 entries |
| **act-wide, over the maps touched** | **+15%** | |

The deep maps move most and are the smallest, which is the trade this placement makes on purpose. It is a
dial, not a fact: the weights are one table in the build script and can come down.

**The Priestess race ladder is unfinished, and the act's boss runs on it.** The Priest line is a finished
three-tier ladder; the Priestess line is not:

| | HP | AC | cold / electrical / fire resistance |
|---|---|---|---|
| Priest -> Tough -> Super | 80 / 110 / 150 | 230 / 250 / 280 | 50 / 60 / 65% |
| Priestess -> Tough -> Super | 75 / 84 / 95 | **260 / 80 / 150** | **none, at any tier** |

The AC falls 180 points from base to Tough and never recovers, and no tier has any damage resistance. So
**`Priestess Tough` is not fielded** -- `Priestess`, at AC 260 the strongest of the three, carries the order,
and `Priestess Super` appears only in the Druid Master's chamber where a set-piece can carry it.
(Superseded below: the ladder was repaired in the same release, so `Priestess Tough` is fielded after all.)

**Both were then repaired, on the tester's instruction**, in the same release.

The priestess line's **spell** identity turned out to be the finished half, and genuinely distinct: the
Super carries four offensive spells at 95 including `Static Charge`, which no priest gets, plus
`Fighting/Evasion`. Only the defensive pass was never done -- and `Priestess Tough` does not even share a
spell with the other two tiers. So the repair keeps the identity and fixes the ladder. The shipped base
already says a priestess is harder to hit than a priest (AC 260 against 230) and slightly frailer (75
against 80), so that is carried up the line: **+30 AC over the priest at every tier, about 90% of his HP,
and his resistance values.** `ENEMY Magical Shield` is deliberately *not* added -- it is the priests'
signature, and withholding it keeps the two lines apart: priests shield, priestesses out-damage and dodge.

| | HP | AC | resist | Magical Shield | spells |
|---|---|---|---|---|---|
| Priest / Tough / Super | 80 / 110 / 150 | 230 / 250 / 280 | 50 / 60 / 65% | yes | 4 |
| Priestess, shipped | 75 / 84 / 95 | **260 / 80 / 150** | **none** | no | 1 / 1 / 5 |
| Priestess, repaired | 75 / **100** / **135** | 260 / **280** / **310** | **50 / 60 / 65%** | no | 1 / **2** / 5 |

Both ladders are now monotonic in HP and AC, and `Priestess Tough` gains Spike 90 so all three tiers share
a spell. **`Priestess Tough` is therefore fielded after all**, and the placement table above is unchanged
otherwise.

**And the Druid Master got her own race, because sharing one was the root of it.** She shipped on
`Priestess Super` -- the rank-and-file race -- which is why she was HP 95 / AC 150 / no resistance, against
the `Assasin Master` **on her own map** at HP 400 / AC 305, and act 5's Nostradamus at HP 500. Her attendant
priestesses even paid **1,949 XP where she paid 1,100.** Fixing the ladder alone would have left a boss on a
rank-and-file race, so `Races/Enemies/English Enemies/Priestess Master.Race` is new: **HP 350, AC 300, 65%
resistance, her four spells at 130 and Evasion 60** -- just under the Assassin Master in HP, above him in
resistance, and a caster where he is a blade. Her XP goes to **2,500**, above her own priestesses and level
with Tremblethorn.

Nothing else moved onto the new race: `Priestess Super.Race` still exists and the rank-and-file
`Priestess Super.can` still uses it.

**2. ~~The Templars' help becomes substantial.~~ Built:** a quartermaster and a field surgeon. Designed with the
tester 2026-09-26; decisions below are theirs, not defaults.

What the alliance currently amounts to is **three knights and Sir Roger** -- each of the three
`Templar Generator` parts spawns exactly one `Cathedral knight Guard`. And **act 7 has no merchant on any
of its eleven maps**, with 2, 8, 1 and 7 potion references on the first four and almost none after, so a
player who runs dry in the Stone Chamber has eight maps to go and no way to restock. Sir Roger's own
acceptance line already promises more than the act delivers: *"Superb! Together we shall vanquish the
heretics. **My men will spread out and clear the area** while we proceed."*

**Two posts**, at the two ends of the act's spine. The graph is `02 -> 03 -> 04`, with `05` looping back to
both and holding the exit to Alamut, and every side chamber returning to the spine (`06`->02, `07`/`08`->03,
`09`/`10`->04). A post on `02 Temple Initiate` and a second on `04 Antechamber of Lore` leaves the player
never more than one map from resupply, including from the Inner Sanctum and the Secret Chamber.

The `02` post goes on ground the map itself proves walkable: the Templars already cluster at
2669-3137 x 1099-1494, the player arrives at `Start Here` 2531,1013, `Accept Templars Help XP` sits at
2886,1256, Sir Roger at 2919,1476, and the map's own non-interactive sequence walks templars to 2975,1493,
3137,1402 and 3091,1494.

**Both staff are the act's own unplaced `Knight Templar` template**, so the bodies are restored rather than
invented. Both services are copies of shipped mechanisms:

| piece | precedent |
|---|---|
| the shop | `CMerchantAI{Display Name, Items}` on its own entity, opened by `CDisplayMerchantWindowAction{Merchant=...}` on a reply. The Herbalist already carries a **`Templar and Inquisition Inventory`** in four tiers (30/25/20/15 items); `Inquisitor Fournier` in Montaillou's church is the "a church sells things" model |
| the healing | `CGiveHealthToCharacterAction` targets `$instigator` **30 times** in the shipped game -- five in `Inquisitoragent.DialogTree`, three in `dreamdjinn`, nine on `02 Thieves Congregation`. Full heal is the `CSubtract{max HP - current}` form used on Farshad |
| the fee | `CHasMoneyAction` (170 uses) and `CTakeMoneyAction` (106) |
| the guards' voice | **`EnglishKnightTemplarCan1.DialogTree`** -- *"My sword is yours."* -- the one tree in the act that nothing opens, given to the knights standing at the post |

**The surgeon heals free for a knight, and charges everyone else.** `Templar IS` or `Saladin IS` pays
nothing -- they are orders of knights and he treats them as brothers. Everyone else pays, **including a
sworn Inquisitor**: the Inquisition is Spanish and ecclesiastical, not his brotherhood, and making that
distinction is more interesting than one blanket faction check. Sir Roger already reads all three orders
across seven nodes, so the vocabulary exists.

**The quartermaster's stock improves in tiers, and one of them reaches back six acts.** Quinn the
herbalist's reserve is chosen by three `CIsQuestCompletedAction` checks -- *Wolf Pelts for Quinn*,
*Wasp Stingers for Quinn*, *Troll Hide for Quinn* -- which is 0.4.0's own work, and **quest completion is
global state readable from any map with no cross-map flag to mirror.** So the Templars stock the healing
potions those errands unlocked, gated on the same three checks Quinn uses: run his errands in act 1 and the
Order is still selling what you unlocked in act 7. A second axis raises the stock once the shrine's inner
chambers fall, giving three windows in all, exactly as Quinn has three.

**And the whole post is gated on having accepted Sir Roger's help.** Refuse him -- *"I am not interested in
help from any Englishman"* -- and there is no camp, no shop and no surgeon. That reply currently costs the
player nothing at all; this is the first time it costs something.

**What went in.** Two posts, `02 Temple Initiate` at 2820,1300 and `04 Antechamber of Lore` at 5880,1560 --
the two ends of the act's spine, so no room is more than one map from resupply. Three staff at each, all on
the act's own **`Knight Templar`** template, which shipped placed nowhere: a quartermaster, a field surgeon,
and a guard who finally speaks `EnglishKnightTemplarCan1`'s *"My sword is yours."* -- the one tree in the act
that nothing opened. `Templar Camp.DialogTree` is new: five nodes, thirteen replies.

**Everything copies a shipped shape**, which is why the tier is small: `CMerchantAI` on its own
`Editor/Store Inventory` entity opened by `CDisplayMerchantWindowAction` (the `Raylark` store in the Bounty
Hunter Camp is the minimal model); the Farshad full-heal,
`CGiveHealthToCharacterAction` with `CSubtract{(HP) Hit Points - CExpressionHitPointsRemaining}`;
`CHasMoneyAction` and `CTakeMoneyAction` for the fee.

**Gated on Sir Roger's help.** His `10 accept` already fired a relay called
`Accept Sir Roger Offer of Help`, so that relay now also activates all six staff -- the `04` post through a
`COtherMapAction`. Refuse him -- *"I am not interested in help from any Englishman"* -- and neither post
exists. **That reply cost the player nothing before this.**

**The surgeon heals free for a knight and charges everyone else 200**, `Templar IS` or `Saladin IS` free,
*including a sworn Inquisitor paying* -- the Inquisition is Spanish and ecclesiastical, not his brotherhood.
He also answers how many he has lost: *"Twenty at the gate, and I knew nineteen of them by name... The druids
do not take wounded, so there is no one to trade for and nothing to negotiate."*

**The stock reaches back six acts.** Three windows, chosen by the same quests Quinn uses for his own reserve
-- *Wolf Pelts*, *Wasp Stingers*, *Troll Hide* -- because quest completion is global state readable from any
map with no flag to mirror:

| window | offered when | carries |
|---|---|---|
| `Templar Stores field` | no errand done | potions, 40 bolts, 40 arrows, hard leather, a medium shield |
| `Templar Stores good` | **any** errand AND **not all three** | the above plus **Great Healing** |
| `Templar Stores full` | **all three** errands | the above plus **Superior** and **Supreme Healing** |

The potion lines copy `Quinn Reserve Three` exactly -- a base `Inventory Items/Potion` under
`CInventoryItemGeneratorAdditionalMagic` carrying one of the three `.InventoryAddition` files 0.4.0
authored. So Quinn's errands in act 1 are still paying out in act 7.

Two things the audit caught before this shipped. The first draft stocked an **`Antidote`**, which does not
exist in `Resources/Inventory Items/` -- the same class of mistake as the invented model path that crashed
0.5.0, so every item and addition path is now verified present. And the three stock windows were **not
mutually exclusive**: a player who had done all three errands would have seen *three identical "Show me what
you have" replies*. The engine has `CAndAction`, `COrAction` and `CNotAction` all in use (245 / 164 / 579),
so the windows are now `all three` / `any and not all three` / `not any`, order-independent, and the two
better replies say *why* the stock is better so they read as different offers.

**3. ~~The allegiance to England, stored at last.~~ Built** -- and read in the country it was sworn to. Scoped
2026-09-26 after the tester asked what helping Guy Fawkes does once you reach England. The answer was:
nothing, anywhere.

Act 1's *Help the Conspirator against the Spanish Armada* is a **ten-state** thread. You can drink with a
sailor, learn he is Gerald de Guitterez and then that he is **Guy Fawkes**, declare for England, get the
Armada's plans out of Captain Isabella, and murder the Duke of Medina to behead the defence of Barcelona.
The shipped dialogue promises a great deal in return:

> Do you mean to say that you **serve the Queen of England and renounce the Spanish Inquisition**?

> Your service to England is appreciated and **will not be forgotten**.

> I will see to it that **the Queen Mother herself knows of your valor**.

> With the Duke gone, the Inquisition will proceed with the plan to invade England without proper
> leadership -- **and we will be prepared for them.** ... It is **gold from the Queen herself**.

And then:

| question | answer |
|---|---|
| Is the allegiance stored anywhere? | **No.** No perk, no checker, no requirement can. `Conspirator generator` is set twice and read by nobody. |
| Who reads the quest? | Seven files. **Six are act 1.** |
| The seventh? | `6 Barcelona Attack/Temple District Siege.zax`, whose only action on it is `CSetQuestSatusToFailedIfActiveAction`, inside a bulk list failing every outstanding act-1 sidequest when the city falls. **Act 6's sole engagement with the player's English allegiance is to delete the record of it.** |
| Acts 7 and 8? | Never read the player's stance on England at all. Act 7 gates only on `Templar IS` / `Saladin IS` / `Inquisitor IS` / `Templar NOT`; act 8 on Barter, Karma and Speech. |
| Does Fawkes reappear? | No. Four files mention him, all act 1. |

So a player can renounce the Inquisition, swear to the Queen and kill a Spanish duke to cripple Barcelona's
defence -- and then watch England sack Barcelona in act 6 with nobody mentioning it, and walk into England
itself in act 7 with nobody knowing.

**The game already drew the connection this act needs.** Fawkes' `1000 opposed crown` explains why he is in
Barcelona: *"I supported a revolt to overthrow the Queen and formed a plot to detonate explosives below the
Parliament building of London. **Through the magic of her treacherous Druids**, the Queen learned of the
plot and imprisoned my fellow conspirators and my family in the Tower of London."* **The Queen's Druids
betrayed Guy Fawkes.** Act 7 is a Druid shrine in England where the player fights Druids beside an English
Templar who says *"Not all of England stands against you. The druids orchestrated the attacks against you
as a ruse."* The thread and the act are about the same faction and neither knows the other exists.

**The missing piece is one perk**, and everything else follows from it. Three mechanics were checked first:

- **A granted perk cannot be taken away.** Only `CGiveCharacterPerkAction` exists in the engine; there is no
  remove. So the perk must be granted at a point the player can no longer betray, not at the first
  *"my allegiance is with England"*.
- **The two good endings both complete the quest.** `200 not accept the plan` (*"will not be forgotten"*)
  and `200 destroyed church 2` (*"gold from the Queen herself"*) each fire
  `CSetQuestSatusToCompletedAction`, and both sit past every betrayal branch.
- **A completed quest survives act 6**, because the bulk fail is `IfActive`. So the quest's own completion
  stays readable even after Barcelona falls.

So: `Perks/!NPC or Event Given Perks/Servant of the Queen`, granted on those two nodes only -- the folder
that already holds `Dervish of the Crescent`, `Stargazer` and `Weng Choi Perk`, following `Stargazer.Perk`
as the file model. Then it is read where it means most:

- **Sir Roger**, whose enemy is the Queen's own Druids, meeting someone the Queen owes a favour.
- **The Templar camp** from tier 2 -- the surgeon and the quartermaster treat a sworn servant of England
  the way they treat a brother knight.

**Deliberately scoped and not committed:** a second perk for having actually killed the Duke of Medina.
`duke is dead` is a Port District checker and cannot be read from another map, so distinguishing the deeper
ending needs its own perk. Sir Roger is a Templar and might reasonably recoil from a player who murdered a
Spanish noble -- which is a good scene and a separate decision, so it is recorded here rather than assumed.

**What went in.** `Perks/!Event Title Perks/Servant of the Queen.Perk` is new -- a **title with no
mechanical effect** (`PlugIn Behaviors` `Item Count=0`), on the `Beggar Friend` model, because this is a
reputation and not a stat. It is granted at exactly the two act-1 endings where Fawkes parts on good terms
and the quest completes, both of which sit past every betrayal branch, which matters because **the engine has
no remove-perk action**:

- `200 not accept the plan` -- *"Your service to England is appreciated and will not be forgotten."*
- `200 destroyed church 2` -- *"It is gold from the Queen herself."*

**Sir Roger reads it on all six of his entry nodes** -- the three first greetings and the three returns --
and the answer is the one thing that ties act 1's conspiracy to act 7's enemy. Fawkes said the Queen learned
of the Gunpowder Plot *"through the magic of her treacherous Druids"*; Sir Roger confirms what that means:

> <He is quiet for long enough that you can hear the fighting two chambers away.> Then you know more of this
> than I was going to tell you. **The Queen keeps druids, Lionheart.** She has kept them since before she had
> a throne, and what they bring her she does not ask twice about. **My Order came to this shrine without her
> leave** and we will be told off for it if we live. <He sets his shield straight.> So we are both here doing
> England a service she has not asked for. Come on.

Pressed further, he does not lower his voice: *"Whatever they are raising in there, she will call it hers when
it is done, and the men who stopped it will have been brigands."* Both new nodes route into `10 accept`, so the
reveal is a way *into* the alliance rather than a detour around it.

**And tier 2's field surgeon counts it as a knighthood.** A servant of the Queen is treated free, beside
`Templar IS` and `Saladin IS` -- four routes now, of which one still pays.

### The act-1 repair that came with it

`200 kill duke 6` -- *"If this deed is done, you will be remembered forever in English history as one of
it's most heroic patriots. When the deed is done, return here."* -- was reached by nothing. The reply it
belongs to, **"I'll lure the Duke to the trap."** on `200 kill duke 5`, had an **empty `Go to node ID=`**, so
accepting the darkest job in act 1 ended the conversation without a word. Pointing that reply at node 6 was
the entire fix.

`Conspirator.DialogTree` now has one orphan left, `100 Guy Fawkes`, which is a **blank node** -- no text, no
replies -- and stays recorded as a stub. Its two remaining dangling `Go to node ID=` targets are vanilla's:
`5 Goodbye` resolves to the node `5 goodbye` once case is folded, and `10 no thanks` points at nothing in the
shipped file too.

**4. ~~Something else to do in eleven rooms of fighting.~~ Built** -- starting with the one the survey misread. The Inner Sanctum first, since the act ends there
and currently ends in silence. Then the Meditation Chambers, which are named for contemplation and contain
golems. The Crypt's four Misc Crypts and act 6's `Crossroads Siege` are the pattern: say what the place is,
and give one lever per room that is not a sword.

**The survey was wrong about this map twice, and the corrections are the tier.**

It is **not the act's final room** -- `05 Exalted Chambers` is, holding the Druid Master, the Assassin Master,
Galileo and the exit to `England to Alamut`. `10 Inner Sanctum` is a dead-end side chamber off `04`.

And it is **not contentless**. It is a three-switch vault:

| switch | opens | behind it |
|---|---|---|
| 1620,1364 | `Secret door1` at 2269,1176 | two ambush generators -- soldiers, bowmen, and now druids |
| 1482,1379 | `Secret door2` at 2307,1501 | **two chests on `Chest Generator Good`** -- the all-weapons and all-arrows lists |
| 1508,1471 | `Secret door3` at 1573,2195 | four ambush generators -- war golems, a priest, a druid, a priestess |

What the survey counted as "no secrets" was `CAISecretReveal`, the **Traps-skill spotting** mechanism. These
doors are not spotted, they are **switched**: three worn stones clustered in one west corner, opening three
doors scattered across the room, one of which holds the only good loot in the act outside a boss.

**And the map has no dialogue tree, no balloon and no label printer.** Three unmarked wall switches in a room
of 88 enemies, with the doors they open up to 800 units away -- so a player who does find a switch and click
it gets **no feedback at all**. That is the tester's complaint in miniature: the doing is there, and it is
invisible.

**So this tier adds no content. It makes what shipped findable.** `The Inner Sanctum.DialogTree` is new, five
nodes, all five opened:

- **on arrival:** *"This is not a chamber the druids use... What there is, is a great deal of wall for a room
  this size -- and the wall does not ring the same all the way round."*
- **a hover over the switch corner**, a polygon spanning 1430-1670 x 1320-1520, which contains all three
  switches: *"Three stones are set into the wall here at shoulder height, worn paler than the rest by hands
  that knew exactly where to reach. Three stones, and a very long way between them and whatever they open."*
- **a line on each switch**, appended to its own relay so the feedback arrives with the click rather than
  across the room: stone grinding to the north and *"a great many boots"*; the eastern panel opening on *"two
  strongboxes with the Temple's mark still on the lids -- taken off the Order on the way in, and never opened
  by whoever took them"*; and to the south, *"a smell of hot iron and wet stone... something in there that
  does not need feeding."* Each closes with how many stones are left, so a player who finds one knows to look
  for the others.

Every vanilla action on all three relays is intact -- audited per relay, nothing lost.

**Left alone:** the three Meditation Chambers. The survey called them one `ManaTomes` shelf each plus golems,
which is right, but each already carries five or six balloons off that tree -- they are the one thing in the
act that does talk. They want a reason to exist more than they want narration, and that is a bigger question
than this tier.

**5. ~~Captain Isabella never arrives at the shrine.~~ Built --** and she is not who the survey thought, and neither is what she was for.
`01 Outside Shrine` is the landing beach, and it carries `Captain Isabella generator` (`Active=0`, nothing
activates it) and `Captain Isabella fled`. The **"fled" part is activated**, by `COtherMapAction` reaching
into this map from two act-1 nodes:

| act-1 outcome | from | does |
|---|---|---|
| she refuses Spanish law over Morales' murder -- *"The next time you attempt to cross my path, there will be blood."* | `Captain Isabella.DialogTree`, `220 isabella flees` | activates `Captain Isabella fled` **at the shrine**, activates `Isabella Fled` in the Gate District, opens *Solve the Murder of Captain Morales*, fails *Find a Wind Scroll for Captain Isabella* |
| you report her to the Duke | `Duke.DialogTree`, `122 wait` | activates `Captain Isabella fled` **at the shrine**, deletes `Ship Captain`, sets `told on isabella` |

Both *bad* endings of the Isabella thread were wired forward three acts. **The good one was never staged**:
her generator is off and nothing switches it on, so the captain who sails you to England is absent whether
you parted as allies or not. Her generator has no `New Name=` and no dialogue tree, so switching her on is
restoration and giving her something to say at the beach is new writing; the tier should say which is which.

**The survey said switching her on would be restoration and giving her something to say would be new
writing. The second half was wrong.** Her tree carries a complete, authored arrival-in-England arc, and
**eleven of its forty-three nodes were orphaned** -- every one of them part of it:

| node | |
|---|---|
| `500 arrive in england isabella hates you` | *"You nearly foiled my plans in Barcelona... if I can't kill the English, I will settle the score with you."* -- with a `CGoToCombatAction` |
| `502 arrive in england grace friendly` | *"You have found me! First you spared me in Barcelona and now you have come so far to rescue me."* |
| `502 grace joined romantic` | *"Together we cannot fail. My heart and my sword are yours!"* |
| `502 grace rejoined companion`, `asks to return`, `left behind` | the release-and-rejoin cycle |
| `502 grace companion near death`, `hurting`, `600 wild add 1/2/3` | her combat barks, including **"For Ireland."** |

**She is Grace O'Malley**, the Irish pirate, posing as Captain Isabella: `300 isabella explains murder` has her
admit she has *"pretended to be Captain Isabella"* for two years, and `310 against england` gives the reason.
So the woman who sails the player to England is an Irish rebel against it -- which makes her the third leg of
a thread this project has been assembling without knowing it, beside Brendan Sullivan's clover from drowned
Ireland (0.9.1) and Surrey O'Connell pressed into England's supply train (0.18.0).

**And `503 druids` says what tier 3 had me invent for Sir Roger:** *"Once they fought the English with us, but
now they have formed an alliance with the Queen."* The game already said the Queen keeps druids. Tier 3's
reveal is corroborated by the shipped text rather than merely consistent with it.

**The gate is a quest state, which is global.** `JMBN5402` -- *"after hearing the explanation for the crime,
you have agreed to keep her secret"* -- is activated **and the quest completed** by `310 against england`'s
reply *"You have persuaded me to silence."* Lie instead and you get `26K1T1IB`; take her bribe and you get
`FMYEYT9D`. So the beach reads three ways:

| act 1 | at the shrine |
|---|---|
| she fled, or you gave her to the Duke | **not there at all** -- which is what the shipped `Captain Isabella fled` checker already meant |
| you heard her out and kept her secret (`JMBN5402`) | `502 arrive in england grace friendly`, and she can join |
| anything else -- bribed, lied, never asked | `500`, and she attacks |

**Her body is Sir Roger's, sliced.** He is a working companion on this act, so his generator -- the full AI
stack of `CSkeletonAI`, `CNormalAttackAI`, `CScanAreaAI`, `CScanInvestigateAI`, `CChaseInvestigateAI`,
`CChasePursueAI` and an interaction specifier -- and two of his three switch relays are lifted and renamed
rather than authored. His third, `Sir Roger Switch Talk AI`, is skipped: it has zero callers even for him.
His specifier ships with an **empty `Action=`** (his tree is opened by a relay, not the generator), so hers is
filled with the three-way conditional instead of replacing something.

The three blank `Go to node ID=` fields on `502 arrive in england grace relived 2` and the one on
`503 druids` are pointed at the nodes already written for them, and the two joining replies carry
`CSetCompanionAction`. **The vanilla `Captain Isabella generator` is left inert exactly as it shipped** --
it has no name, no AI and no specifier, so it could never have worked; the new one sits beside it.

Gate 0 caught one invented path on the way: the first draft pointed at
`Character Templates/**Port District**/Port Ship Captain`, and the template is at
`Character Templates/Port Ship Captain` -- the path the beach's own inactive generator already used.

### The beat act 1 was missing, added on the tester's call

Her act-1 arc is political and confessional throughout -- the accusation, the real name, the grievance about
England's navy -- and the only warmth in it is one line: *"You could have turned me in, but you chose to
listen to me. I will not forget your kindness."* Act 7 then opens with **"My love, know that my blade and my
heart are yours"**, which is a long way to travel on one remembered kindness. The tester's call was to build
the beat rather than leave the jump or soften her, and to make it the prerequisite.

**`350 grace relieved` is reached by two replies, not one:** *"You have persuaded me to silence."* and the
`<Lie>` variant. The truthful one activates `JMBN5402` and completes the quest; the lie activates
`26K1T1IB`. Its single "continue" reply had **no destination at all**, so it now leads to the beat -- which
plays for both, because a woman opening up to someone who is deceiving her is better than skipping it -- and
**the reply that answers her is gated on `JMBN5402`.** A liar hears it and cannot reply in kind.

> <She turns away and busies her hands with a rope that does not need coiling.> Two years I have been
> Isabella. Two years of being careful in a language that is not mine, and in all that time not one person
> has asked me why -- they only ever asked me whether. You asked why. <The rope goes down, and when she looks
> back the captain has gone out of her face and something a good deal less careful has come into it.> I have
> sunk ships over smaller kindnesses than that.

Answer *"Then I will hope to see the ship and not the sinking"* and she gives you her name and the line that
sets up the whole of act 7:

> Grace, then. Not Captain, and not Isabella. Grace. <She says the name as though handing you something
> breakable.> The Armada sails within the month and I sail with it, so this is a poor harbour for hoping in.
> But **if the sea ever gives me back to you somewhere that is not Barcelona**, I will remember which of us
> listened first.

Decline, either warmly or coldly, and `380 grace steady` puts the captain back in her face: *"You have my
thanks, which is not nothing from me, and you have my silence about your having had it."*

`Perks/!Event Title Perks/Graces Regard.Perk` records it -- in the title folder rather than
`!NPC or Event Given Perks`, because **every perk in that folder carries a mechanical effect** and this one
carries none. It is a reputation, like `Beggar Friend` and `Servant of the Queen`.

**Act 7 then requires it for the romantic acceptance only**, on both `502 arrive in england grace relived 2`
and `503 druids`. Her own declaration is left exactly as recorded -- she is voiced, and a woman just
shipwrecked and found by the one person who ever listened to her is allowed to be forward. What the perk
gates is whether the *player* can answer in kind. Without it the two remaining routes are the sword without
the heart, and refusal.

**And the arc was recorded, which is worth stating plainly:** 38 VO files for 43 nodes, and the England branch
is among them -- `502 grace joined romantic`, `502 grace companion near death`, `hurting`, `left behind`,
`503 druids`. Voice acting is the most expensive thing in a game of this era, so this was **cut at the wiring
stage, not abandoned in draft**. Two VO files also have no matching node (`502 grace joined companion`, and
`502 grace companion asked to return` against the tree's *asks*), which is a late rename; tier 6 handles it.

**Seven orphans remain in her tree**, and they are all companion-state lines: `rejoined companion`,
`companion left behind`, `near death`, `hurting`, and `600 wild add 1/2/3`. Those are the same shape as Sir
Roger's own unwired barks, so tier 6 does both in one pass.

**6. ~~Sir Roger's five combat barks.~~ Built** -- both companions' voices, and two recordings made playable. **All six tiers of act 7 are built.** `100`-`104 Random Attack Ballon` -- *"For England!"*, *"For The
Queen!"*, *"For The Templars!"*, *"We shall Prevail!"*, *"On my honor!"* -- reached by nothing and opened by
nothing. He is a companion (`CSetCompanionAction`), so these are his fighting lines, and the act already
runs three `CShuffledSeriesAction` doing exactly this for the generic templars' eight bubbles.

**Two recorded lines had been renamed out of reach.** VO lookup is by node ID -- 36 of Captain Isabella's
38 VO files match a node exactly -- and the two that did not were late renames:

| recording | the node as it shipped |
|---|---|
| `502 grace companion asked to return` | `502 grace companion **asks** to return` |
| `502 grace **joined** companion` | `502 grace **rejoined** companion` |

Both nodes carry `Should Have Voiceover=1`, so the game looked for audio and found none. Renaming the nodes
back to the recordings makes both audible. Nothing in the shipped game referenced either id.
**All 38 of her recordings are now reachable.**

**Eight barks had never played.** Sir Roger's `100`-`104 Random Attack Ballon` -- *"For England!"*, *"For The
Queen!"*, *"For The Templars!"*, *"We shall Prevail!"*, *"On my honor!"* -- and Grace's `600 wild add 1/2/3` --
*"I need healing!"*, **"For Ireland."**, *"We cannot fail."* Both go on act 6's `Attackers dialog balloons`
pattern with one change that matters: **a companion walks between maps**, so the `CShuffledSeriesAction` goes
inline in a `CRepeatTimerTriggerAI` on the character's own AI list rather than behind a map relay, which would
only exist where the companion spawned.

**And her two health barks got the trigger they were written for.** `502 grace companion hurting` and
`near death`, both recorded, now fire off a `CAIHealthPercentThresholdTrigger` crossing below 60% and 25% --
the shape act 5's snakebreed summoner uses.

**The release-and-rejoin cycle** is wired both ways. Tell her to wait and she says the recorded
*"If that is your desire. I will await your return here."*; come back and she says *"Let us continue our
quest."* and rejoins, on a `Grace has been left behind` checker. Her `asked to return` node shipped with **no
replies at all**, so the two player lines there are the only new writing in this tier.

**Two defects of my own, both caught by this tier's audit:**

- Tier 5 pointed her post-join specifier at a reply-less node with a `CDisplayDialogTreeAction`, which would
  have opened a conversation the player could not answer. It is a balloon line and is now shown as one.
- The first draft of these barks anchored the balloons on `$Instigator`. Act 6's working pattern uses
  `$Trigger` -- the entity whose timer fired -- and in a timer on a character's own AI list `$Instigator` is
  not the character. All ten balloons repointed.

**Both companions' trees now have zero orphan nodes**, which is where act 7 finishes: Sir Roger's 17 nodes and
Captain Isabella's 46 are all reachable.

### What a review pass found after all six tiers were built

Two defects, both **semantic rather than structural** -- which is why six rounds of per-tier auditing missed
them. Every tier audit asked "does it round-trip, is the node reachable, did any vanilla action get lost".
Neither question catches an action that is well-formed and means the wrong thing.

**Grace could not have survived a single fight.** Her template `Port Ship Captain` uses the race `Sailor`:
**HP 36, AC 90.** Act 7's *weakest* rank-and-file enemy is `Soldier1` at HP 75 / AC 230, and the act's other
companion, Sir Roger, is HP 200 / AC 200. She would have died in seconds, which would have made the whole arc
-- the barks, the health thresholds, the romance -- unreachable in play. Her act-1 self has to stay at HP 36,
because the player can kill her in the Port District and that is act 1's balance, so act 7 gets **its own
template on its own race**: `Levels/7 English Shrine/Character Templates/Grace OMalley` on
`Races/NPCs/Grace OMalley` -- **HP 165, AC 190, Melee 110, Evasion 55.** Under Sir Roger, over the rank and
file, and a blade rather than a knight's wall.

**And the release did nothing.** "Wait here. I will come back for you." used `CSetCompanionAction` with an
empty `Companion=`. **No shipped use of that action has an empty Companion** -- all sixty-two name someone --
and the engine's dismiss action is `CReleaseCompanionAction{Companion To Release=<name>}`, used forty times.
That is what the reply does now.

Both are the same lesson as the cameras earlier in the act: **check what a working example of the mechanism
does before assuming a field means what it reads like.** A sweep of every action class this release writes
against vanilla's own usage turned up no others -- and no class used here is absent from the shipped game.

### Two other findings I had to withdraw

- The first sweep reported **two dead 24-soldier ambushes** and a **dead second `Secret Area1`**. All three
  are wired: `Target Name=Ambush area` against the part `ambush area`, `ambush generator` against
  `Ambush generator`, and `secret area1` five times beside `Secret Area1` twice on one map. **Engine name
  lookup folds case**, which this project has known since 0.15.0. Fourth occurrence; the recorded sweep is
  case-folded, comma-split and run against every activation in the game.
- `Find All 5 Green Crystals.DialogTree` looked like an orphaned reward. It lives under act 8 and is opened
  twice -- from `09 Secret Chamber` here and `02 Shifting Dunes` in act 8. It works.

`EnglishKnightTemplarCan1.DialogTree` was also listed as a candidate to leave alone, as possibly Sir
Roger's superseded draft. The tester's call is to spend it on the camp's guards instead, which is the
better use: it is shipped writing, and the alternative was leaving the act's one unopened tree unopened.

### Read and deliberately left alone

- **`Prevent the Druids from completing the dark rites.Quest.txt`**: `Item Count=0`, no state IDs, zero
  references game-wide, and its display name is carried by the working `Stop the Druids.Quest.txt`. A
  renamed file's abandoned predecessor, not a dropped quest.
- **Three `warp` / `Warp` parts** on `01 Outside Shrine` and `05 Exalted Chambers`, inactive, activated by
  nothing, self-triggering polygons with no entities. Developer teleports; they stay off.

### And a correction owed to 0.17.0

0.17.0's notes say the `English in Caverns of Nostrodomus` folder's **fourteen** units are now fielded. Six
of them are still placed nowhere: `Nos Ogre2 English`, `Nos Ogre2 English Tough`, `Ogre2 English Super`,
and the folder's own `Priest`, `Priest Tough` and `Priest Super`. Eight were fielded, not fourteen -- the
two English ogres in particular are named in the notes and are not in the game. They belong in a 0.17.1
alongside this act's work, since the same twinning pass handles them.

## Surrey O'Connell's third route (built, shipping in 0.19.0)

0.18.0 gave Surrey O'Connell two new ways past the Regent's chest: the **Clover from the drowned fields of
Ireland**, and the **Holy Office**. **Both stay exactly as they shipped.** This adds a third, for a player
carrying `Servant of the Queen` from act 1's conspiracy (see 0.19.0 tier 3), and it is deliberately the
coldest of the three.

Surrey is a pressed Irishman who is sarcastic about the work -- *"Happy I am to serve the English as
supplies master"*, which the act's own `PE 8+` reply calls out as sarcasm. **A player wearing the Queen's
favour is precisely the person who could hang him for saying it.** So the three routes are three different
reasons, not three flavours of the same one:

| route | why he helps | how he parts |
|---|---|---|
| the clover | kinship in grief -- *"Drowned. The whole of it drowned, and I am out here weighin' out bolts for the men that let it."* | warmly: *"Surrey O'Connell never saw a thing, and never heard a lid."* |
| the Holy Office | terror of Spain, from his own *"dont... send me to the Spanish Inquisition"* | panicking, and already unbuckling the crate |
| **Servant of the Queen** | self-preservation. He has been overheard mocking the Crown by somebody the Crown owes a favour | **coldly.** He complies, and he is worse off for having met you -- the only one of the three where helping the player costs him something |

Mechanically all three end in `Surrey looks away`, so the chest alarm work from 0.18.0 is reused unchanged
and **there is no map edit at all** -- one gated reply on each of his three entry nodes, and two new nodes.

**It ships in 0.19.0 rather than as a 0.18.2**, because the perk it reads is act 7's work and a patch to
0.18.x would have had to carry that file forward on its own.

> <Everything friendly goes out of him at once, and what is left is a man doing sums.> I said nothing,
> guvna'. I said I was happy in the work and I am happy in the work. Ye'll want the Regent's chest. Take it,
> and take it quick, and when they ask me I will say a Spaniard came through here and I could not stop him,
> because that is a thing they will believe of me. **Do not say my name where anybody writes things down.**

Tell him he has nothing to fear from you and he gives up the only honest thing he says to anybody: *"No. No,
I have not, and I have not from the last four either, and here I still am weighin' out bolts on the wrong
road."*

### And a convention repair across this release

The project's rule is **at most one `<...>` stage direction per dialogue node** -- speech should not read like
a screenplay. Nine nodes authored in this release broke it, three of them already shipped in 0.18.0
(`200 the clover`, `210 the inquisition`, `50 the reports`). All nine are cut to the stage direction that does
the most work, with what the other carried folded into the speech where it was worth keeping.

A sweep of every Fixt-authored node in the mod found **43 more in releases 0.1.0 through 0.17.0**, so the
drift long predates this release. Those are left alone here -- rewriting authored prose across eight published
releases is not something to fold into a release cut -- and recorded as a backlog item.

## 0.18.1 - Slayer of Innocents, on the hooks the designers built for it

0.18.0's award reads the perk's description -- *killing the helpless* -- and hangs the title on a murdered
citizen, because children cannot be killed. That was the best reading available without knowing about the
mechanism the designers *did* build, which a question about the game's three child-rescue quests turned up:
**each child's generator carries a working `CSetDamagedScriptActionAction`.** Children cannot be killed,
but hitting one has always been detected, and always had consequences.

| child | map | what the hook already did |
|---|---|---|
| Woodcutter's daughter | `Scar Ravine` | screams `70 Ahhh!`, flees to `girl leave safe`, turns `Goblin guarding girl` on you, deletes the entire peaceful-resolution script set, fails *Find the Woodcutter's lost son*, activates `daughter attacked` -- which `Woodcutter.DialogTree` reads, so the father knows -- and runs a `COtherMapAction` deleting her generator at the house so she never turns up home |
| Woodcutter's daughter | `Woodcutter Home interior` | the same, at home |
| Marisol | `Port District` | screams `90 Ahhh!`, flees to `Marisol disappear location`, fails *Find the lost boy Tomas in the Sewers* |
| Tomas | `05 Troll Pit` | screams `70 Ahhh!`, strips his talk specifier, flees |
| Shepherd's son | `01 Hamlet Exterior` | screams `40 Ahhh!`, activates `Player hurt the son` and `Make Maury mad for hurting son` |
| Barcelona Boy | `Gate District` | the `Child Leaving` boy, switched on by two comma-list activators |

Five children, six placements, every hook doing real work -- and **not one of them touching the title the
game wrote for exactly this.** The grant now sits in each of those six, on the same
`CHasPerkExpression`-guarded shape, appended to the hook's own action array with every vanilla action left
in place: the quest failures, the flags, the fleeing and the goblin all still happen.

**Everything downstream already worked.** The grant reaches the guards' `2 Childkiller Intro`, and its
*"I am the killer. You should back down before I kill you."* reply fires both
`Damage a guard in the city district` and `Child killer bubble text` -- the guard shouting *"Have at thee,
monster!"* That bubble part looked like a seventh orphan when counted in `.zax` files alone; its caller is
in the DialogTree. The grant was the only link missing since release.

**These hooks cannot misfire.** On all four maps involved every `Valid Targets` is some combination of
`Player`, `Player Friend`, `Enemy` and `Scripted Custom N`; nothing can target a neutral, which is what
every child is. So only the player can ever trigger one, and the goblin standing over the daughter and the
trolls standing over Tomas cannot earn the player a title.

The citizen grant stays alongside: a murdered citizen is one of the helpless too, it is the
`Merchant Slayer` precedent, and it is what gives act 6's witness scene its consequence. **40 grants in
total** -- 34 citizen generators and 6 child hooks.

**Released 2026-09-26. Surveyed and built 2026-09-25, unplayed.** Act 6, `Levels/6 Barcelona Attack`. Eight maps, 2,897 level
parts, 1,304 live spawner entries -- of which **415 are corpses** and 889 are combatants -- six dialogue trees of its own, and **28 player replies in total**.

| map | parts | live spawners | conversations | balloons | MB |
|---|---|---|---|---|---|
| Temple District Siege | 920 | 310 | 0 | 26 | 1.57 |
| Gate District Siege | 791 | 393 | 1 | 33 | 1.08 |
| Crossroads Siege | 910 | **490** | **0** | **0** | 0.77 |
| Crossroads to England map | 149 | 93 | 3 | 7 | 0.20 |
| Church Interior ruined | 47 | 6 | 0 | 1 | 0.08 |
| Weng Choi Shop Siege | 39 | 9 | 2 | 5 | 0.07 |
| Blacksmith map | 28 | 2 | 3 | 0 | 0.04 |
| Church Crypt Interior Siege | 13 | 1 | **0** | **0** | 0.02 |

**The act's signature is different from act 5's.** Act 5 was content built and never switched on. Act 6
is seven **re-dressed act-1 maps**: the siege versions kept the peacetime parts and dropped most of the
wiring. Comparing each against its peacetime original -- 41 named parts on the besieged Gate District
against 400 on the peaceful one -- most of that difference is deliberate, because a sacked city should
not still have its shopkeepers standing about. What matters is the handful of things left present, live,
and no longer connected to anything.

### Nobody in the sack of Barcelona says a word

Three relays exist `Active=1` on `Gate District Siege`, `Temple District Siege` **and**
`02 Hamlet Burned` (act 3), and are **fired by nothing anywhere in the game**:

| relay | speaks |
|---|---|
| `Defenders dialog balloons` | `Defenders.DialogTree` -- *"To Hell with these accursed druids!"*, *"God save Barcelona!"*, six lines |
| `Defenders dialog balloons for interactionspecifier` | the same, on being spoken to |
| `defender winner dialog balloons` | `Defenders win a fight.DialogTree` -- *"I'll secure this area."*, *"The gall of these druids!"*, six more |

And the fourth, `Attackers dialog balloons`, **is** called -- only from `fight1`, `fight4` and `fight5`
parts that are all `Active=0`, plus a switched-off `fight5` on `Bryce Folly`. So the English have seven
lines (*"Attack! For England!"*, *"Let us crush these Inquisitors!"*, *"For the Queen!"*) with nobody live
to call them either.

**Nineteen barks across three trees, and the sack of Barcelona is silent on both sides.** The two 1 MB
maps hold 33 and 26 balloon actions between them, every one inside a relay nothing fires.

`02 Hamlet Burned` carries the same three dead relays, which makes it a **0.14.1** item: Montaillou
shipped in 0.14.0 with the same silence.

### Two quests, neither of which exists

| file | inside |
|---|---|
| `Find Galileo and DaVinci.Quest.txt` | `Name=` **blank**, `Item Count=0`. An empty husk -- the file was created and never written |
| `Pursue the retreating English forces and recover the True Cross.Quest.txt` | `Name=Pursue the Retreating Druid Forces and Recover the True Cross`, `Item Count=0` |

**Neither is referenced by any map or any dialogue tree in the game.** The act's one working quest,
`Defend Barcelona from the Forces of the Druids`, has a single state and is activated on
`Temple District Siege`. So the act announces one objective and silently drops the two that frame it:
finding the two men the player has spent the game working with, and the pursuit that hands over to act 7.

Worth noting for the writing: the files say **English**, the quest names say **Druids**. The invaders
were renamed late and the filenames were not, which is also why act 5's unused English roster lives in a
folder called `English in Caverns of Nostrodomus` while Huko calls them Druids throughout.

### The densest map in the project has nothing in it but soldiers

`Crossroads Siege` holds **490 live spawners** -- `Soldier1` through `Soldier4` and their bowmen, from
twenty `English BIG PILE Generator` parts and fourteen `English Archer Generator` parts, plus a
`Fire Golem Generator`, two `English Priest Generator`s and two wolves. For scale, the Crypt's Doomed
Plateau, which this project spent a tier making bearable, has 112.

It has **no conversation, no balloon and no dialogue tree**, and its only other content is a
`don quixote actions relay` (`Active=0`, called only by its own dead `warp`) and an `Assasin goto point3`.
`Church Crypt Interior Siege` is silent too, at thirteen parts.

### What the re-dress stripped and left behind

| on the siege map | peacetime references | under siege |
|---|---|---|
| `Player is a child killer` (checker, `Active=1`) | **33** | **0** |
| `Player gotten child killer dialog` (checker, `Active=1`) | **25** | **0** |
| `Shy Girl requests help` (relay, `Active=1`) | 2 | 0, and its speaker `Shy Girl Near Murder` is never created on the siege map |

The child-killer system is a real one in act 1 -- thirty-three references, read by the gate guards' own
canned trees -- and the besieged district still carries both checkers, live, with nothing to set or read
them. `Random Contacts in Barcelona` has the line that fits: `21 Children`, *"Leave me alone! Haven't
you done enough?!"*, which the siege map does open. What it cannot do is tell whether the player is the
reason.

And two death lines are unopened, of seven in that tree:

- `31 Spanish Body on Ground`: *"Stranger...here...take my gold. Don't let those English have it..."* --
  the only one of three Spanish death lines that is unwired, and the only one that offers the player
  something.
- `42 English Body on Ground`: a dying invader who does not know why he came.

### What the act asks about the player: two Speech checks

| gate | count |
|---|---|
| Speech | 2 (the Surrey Vendor, a captured Irish quartermaster) |
| faction, race, spirit, karma, gender, perk, magic school, Barter, attribute | **0 each** |
| trap or lockpick checks, on replies **or** on map triggers | **0** |
| `CAISecretReveal` secrets across all eight maps | **0** |

The act's only real conversation is `Surrey Vendor` -- twelve nodes, twenty-three replies, an English
supply clerk from Surrey who is very frightened of the Supplies Regent and will sell to the player
anyway. He has male and female opening variants, which is the one thing in act 6 that reads the player
at all.

### Checked and not defects

- **The blacksmith works.** `Blacksmith after Siege.dialogtree` has three recorded voice-overs and his
  generator is `Active=1` and opens it. My first pass flagged it because the generator is unreferenced,
  which is normal for a generator that fires on map load -- the same false positive the dead-part sweeps
  are built to exclude.
- **Weng Choi works**, with siege-specific nodes of his own (`500 Start Siege`, `502 Siege Return`) and
  five scurrying balloons.
- **The Temple District's unreferenced doors, polygons and goto markers** (`Shylocke Door`,
  `Inquisition door on left`, `cervantes target`) are scenery left standing after the NPCs who used them
  were removed. Correct for a siege.
- **`Church Interior ruined` and `Church Crypt Interior Siege`** have nothing wired in peacetime and
  unwired under siege.
- **Don Quixote's relay** on `Crossroads Siege` is `Active=0` and called only by a dead `warp`; his
  entity spawns on `Barcelona Coast`, not the Crossroads. Probably a deliberate cut, and not worth
  restoring without a reason.

### Tier 1 - the sack of Barcelona gets its voice (built)

Four bark relays sit `Active=1` on the two big siege maps and hold nineteen written lines between them:
`Defenders dialog balloons` and its interaction-specifier twin (six battle cries), `defender winner
dialog balloons` (six steadier ones) and `Attackers dialog balloons` (seven English). Three are fired by
nothing anywhere in the game; the fourth is called only from inside `fight4`, a reserve wave that is
`Active=0`.

All four position their balloons on **`$Trigger`**, which says how they were meant to be driven: by the
speaker's own AI, exactly as `Hujark dialog balloons` is driven in act 5 by a `CRepeatTimerTriggerAI` in
the general's generator. So the repair is a timer on a handful of soldiers.

**A handful, deliberately.** Arming every generator would be a wall of text rather than a battlefield:

| map | defenders armed | attackers armed |
|---|---|---|
| Gate District Siege | 4 of 4 | 6 of 13 |
| Temple District Siege | 1 of 1 | 3 of 3 |

Sides are decided by what a generator **fields**, not by what the part is called, because `fightN` parts
hold both armies: anything spawning `Gate Guard Siege`, `Inquisitor Generic Siege`, `spanish defender` or
a siege Templar is a defender, anything spawning from `English Enemies` is an attacker, and
`Fixed Dead Body Generator` parts are skipped -- corpses do not shout.

The defenders carry two timers because they have two trees: the six cries every eight seconds, and the
six steadier lines every twenty-four. That slow timer is also the **only** way
`defender winner dialog balloons` can be reached at all -- these maps raise exactly one kind of message,
`GoToCombat`, so there is no end-of-fight event to hang a victory line on. The consequence is that one of
its six lines, *"I'll secure this area."*, can land while the area is plainly not secure. Better than a
tree nobody has ever heard, and worth revisiting if a fight-end hook turns up.

**A correction to this survey's own headline number.** The 1,304 "live enemy spawners" counted every
active spawn entry, and **415 of them are corpses** -- `Fixed Dead Body Generator` parts, 237 of them on
the Temple District alone against 73 combatants. So the besieged Temple District is mostly a field of
dead bodies with a handful of fighters still standing, which is a different and better-observed map than
the raw figure suggested. The real combatant count is 889, and the densest map is still
`Crossroads Siege` at 472 with 18 corpses.

### Tier 2 - the two quests that did not exist (built)

`Find Galileo and DaVinci.Quest.txt` shipped with a **blank `Name=`** and `Item Count=0`: the file was
created and never written. `Pursue the retreating English forces and recover the True Cross.Quest.txt`
has a name -- `Pursue the Retreating Druid Forces and Recover the True Cross` -- and no states either.
Neither was referenced by any map or dialogue tree in the game, so the act announced one objective and
silently dropped the two that frame it.

Both have a state now, and both are driven from places the act can actually reach:

| quest | begins | ends |
|---|---|---|
| Find Galileo and DaVinci | the blacksmith, asked where the two inventors went | `8 Alamut/08 Final Encounter`, at `Galileo Generator` |
| Pursue the Retreating Druid Forces | arriving at `Crossroads to England map`, which is what the Druids are retreating through | **`8 Alamut/08 Final Encounter`**, at `Cross Regret for Player generator` -- the part that hands the player the `TRUE CROSS`. This row said "the same map" until act 8's tier 3 checked it; the part is on the final map, not the crossroads, and that is the right place -- see 0.20.0 tier 3 |

**The blacksmith is the right man to ask**, and he was already there: his post-siege conversation has
three recorded voice-overs and opens by asking the player what they are doing indoors while the city
burns. He now also answers what happened to the two men who used to buy his work:

> Gone, my friend. <He puts the hammer down, which he has not done since you came in.> The Druids came
> up that street with a list, and they did not stop to sack either workshop -- they went in, they took
> the two of them, and they went out the west gate with them walking. Men do not carry off a glassmaker
> and a painter unless somebody has told them what those two can build.

**Both completions land where the game already put the pieces.** `08 Final Encounter` spawns
`Galileo Generator` and `DaVinci Generator` live and holds the only `TRUE CROSS` in the game. Reaching
two acts ahead is worth flagging: when act 8 is surveyed these hooks may want moving, but a quest that
completes somewhere is better than a quest with no states at all.

**One state each, not two.** The first draft gave both quests a second state describing what the player
learns at the English shrine -- and Gate 0 rejected it, correctly: *"state 'BA2FINDG' is never activated
-- the quest can be offered but never starts."* Activating a second state means an act-7 hook, and act 7
is not surveyed. One state matches what the act's own working quest does.

### And the front half of the True Cross thread, which is act 1's

Inquisitor Raphael's tree in **act 1** carries the lines this quest was written for, and neither is
reached by anything or opened by any map:

- `320 chapter 2 mission`: *"Unknown enemies have attempted to steal the True Cross and other sacred
  relics. I would like you to accompany me to the Cathedral..."*
- `350 cross stolen`: *"They have stolen the True Cross from the Cathedral! You must not let them get
  away! They are retreating to the west. Hurry!"*

Raphael's tree drives dozens of quests and **not one of them is about the Cross**, and the only True
Cross quest file in the game is act 6's. So the theft, the pursuit and the recovery were written as one
thread across acts 1, 6 and 8, and only the item at the far end was ever wired. The act-1 half is
released content and wants its own tier rather than a quiet edit here.

### Tier 3 - the crossroads says what it is, and the road remembers the column (built)

`Crossroads Siege` is 910 parts and **472 live combatants** -- four times the Crypt's Doomed Plateau,
the densest map in the project -- with **no conversation, no balloon and no dialogue tree**. It is also
the purest battlefield in the act: twenty `English BIG PILE Generator` parts, fourteen
`English Archer Generator`, two priests, a fire golem, two cold war golems and a pair of wolves, strung
along a corridor from the Gate District arrival at 3253,1631 to the road to England at 892,1561, with
the crowds heaviest at the western end.

**The field speaks**, on the pattern the Misc Crypts got in 0.16.0 -- three narration lines along the
corridor, each on ground the map already proves walkable:

| where | from | says |
|---|---|---|
| arriving from the city | the `From Gate District` spawn point | *"The crossroads is not a crossroads any more. The English have put an army across it the way you would put a hand across a doorway, and the road west -- the only road west -- runs out from under the middle of them."* |
| the centre | a polygon on the peacetime `Assasin goto point3` marker | *"Somebody has driven a standard into the stones at the centre of it, and the men around the standard are not watching Barcelona at all. They are facing west, waiting to be told to move."* |
| the road out | a polygon on the England exit, which the player has to stand on to leave | *"The road west, and the ruts in it are fresh. An army came through here going the other way not long ago, and everything it did not want is still lying where it was dropped."* |

**The army speaks.** `Attackers dialog balloons` exists on both district maps and **not on this one** --
the map the English army is actually on. It is ported here and driven by timers on six of the
thirty-four English generators, exactly as tier 1 does it.

**And the road remembers the column.** Tier 2 has the blacksmith say that Galileo and Leonardo were
marched out the west gate walking, with a guard who had a list. *This is that road.* With
`Find Galileo and DaVinci` active, the line at the western end becomes the evidence instead:

> The road west, and the ruts in it are fresh. In the churned mud at the verge there is a cracked lens,
> ground finer than any glazier in Barcelona could manage, and beside it a wax tablet pressed with a hand
> you have watched draw. Two men went down this road with a guard who had a list, and they left the only
> message they were able to leave.

It pays 1500 XP, once, for having looked -- on the `CGiveExperiencePointsToAllPlayersAction` canned
object the Crypt's doomed knights already use. A player without the quest gets the plain line and no
reward, which is the right way round: the blacksmith is what turns ruts into evidence.

The map goes from 0 balloons and 0 trees to 11 and 2, for 8 KB.

### Tier 4 - Slayer of Innocents, and the boy in the red cap (built)

`Perks/!Event Title Perks/Child Killer` ships complete: a display name -- **Slayer of Innocents** -- a
description (*"TITLE PERK: Killing the helpless is what you like to do."*), and a `Requirements` array
holding a deliberately false expression (`0 >= 1`), which is how the game marks a perk that only script
can grant. **`CGiveCharacterPerkAction` for it, anywhere in the game: zero.** It is read **eight times**
on the peacetime `Gate District`, and those reads drive five fully authored dialogue nodes, each with
two replies -- deny it, or *"I am the killer. You should back down before I kill you."*:

| tree | nodes |
|---|---|
| `Gate Guard Generic1` | `2 Childkiller Intro`, `2 Childkiller Return`, `2 Childkiller Return2` |
| `Gate Guard Generic2` | `2 Childkiller Intro`, `2 Childkiller Return` |

None of it has ever fired, in any playthrough, because the title is never awarded. Act 6 is where the
consequence was meant to land: the two checker parts the whole mechanism runs on --
`Player is a child killer` and `Player gotten child killer dialog`, with the designers' own comments on
the polarity (*"Active Player NOT child killer. Inactive player IS"*) -- **are sitting on
`Gate District Siege`**, both active, and act 6 neither reads nor writes either one.

**Children are not made killable, and that is not what the perk says.** `Races/NPCs/Generic Child` is
HP 10000 / AC 1000, and **every child in the game uses that one race** -- the woodcutter's daughter,
Marisol, Tomas, the shepherd's son and the Gate District boy alike. The invulnerability is deliberate and
it stays.

> *Corrected after release:* this section originally also cited `Barcelona Boy.can` setting
> `Has Hit Points=0` as a second layer of protection. It is not one. **All 247 character templates in the
> game set `Has Hit Points=0`**, including the HP-12 citizens this release makes killable for the title
> and the HP-1 barstool patron. It is a level-part field about object hit points, not character
> invulnerability. The race presets are the only thing protecting children. The perk's own words are *killing the helpless*, and the helpless who can actually be killed
are the ordinary citizens at HP 12 / AC 60. So the title is awarded for murdering an unarmed citizen in
peacetime Barcelona, on the exact idiom `Merchant Slayer` already uses 28 times: a
`CSetDestroyedScriptActionAction` in the generator's `After Action`, whose destroyed action gives the
perk to `$Instigator` if they do not already hold it. **34 citizen generators** across the Gate, Temple
and Port districts; the two `Barcelona Vendor` cans are left out, being merchants who already grant
`Merchant Slayer`. Like that precedent it fires on the first kill, so a player who lets a spell land in
a crowd can earn it by accident -- which is the shipped behaviour for merchants and reads correctly
either way: the guards say there have been *reports*, not that they watched you do it.

The first pass put 22 of the 34 hooks in the wrong slot, and it is worth recording why:
`CDisplayDialogBalloonAction` has a field called `After Action` too, so a helper that takes the first
`After Action=` in the part lands inside a balloon whenever a balloon action appears before the
generator's own slot. There `$Instigator` is the player rather than the spawned citizen, so the hook
would have armed **the player's own death** to grant them the title. Both generator classes end
`... | Canned AIs to Add | After Action | New Facing Angle | ...`, so the correct slot is the one whose
value is followed by `New Facing Angle=`; all 34 are now verified to sit on a `CGeneratorAI` or
`CSimpleGeneratorForCannedEntitiesAI`.

**Then act 6 reads it.** All five spawn points on `Gate District Siege` now run the peacetime
`From Temple District` check -- if the player holds the title, `Player is a child killer` is deactivated
-- and the man searching the district for his son reads the flag:

- **A child killer** gets `21 Children` exactly as shipped: *"Leave me alone! Haven't you done
  enough?!"* This was the line every player got, unconditionally, for walking up to a frightened
  father.
- **Anyone else** gets `22 Children`, new: *"Phillipe! <He has your arm before he sees who has it, and
  lets go.> My son. Seven years old, a red cap his mother made him. He was up at the gate with the
  other boys when the horns went... If you are going anywhere near that gate -- look for a red cap."*

**And there is a red cap to find.** Phillipe is placed at 2694,1251, a vertex of the citizens' own
`Loop Path around town`, so the ground under him is walkable by the map's own evidence. He is a
`Barcelona Boy` -- invulnerable, as every child in this game is -- wedged behind a barrel, and the one
reply that matters is gated on having spoken to his father:

> <A boy is wedged in behind a barrel with his knees up, and he does not come out when you crouch.>
> Are you one of ours? Papa said stay where you are put, so I am put. Everybody who ran past me was
> running the wrong way. Is he coming?

Tell him and he goes -- *"Two streets, keep to the walls, I know it, I know the way --"* -- for **1000
XP, once**, and a closing line the player reads rather than watches, because by then the father has
walked his own path off the top of the street.

### Tier 5 - the witness with nobody to witness, and the two men nobody could hear (built)

`Gate District Siege` carries a relay called **`Shy Girl requests help`**, active and once-only, which
balloons `115 Citizen Attacked` -- *"Ayudame! Help me! Guards!"* -- over an entity named
`Shy Girl Near Murder`, waits two seconds, and fires `Damage a guard in the city district`. On that map:

- nothing calls `Shy Girl requests help`. **Zero callers.**
- `Shy Girl Near Murder` does not exist, and was the map's only dangling name reference.
- `Damage a guard in the city district` does not exist either.

It is a copy-paste remnant of a scene the peacetime `Gate District` has in full: a
`Barcelona Female Citizen` generator named `Shy Girl Near Murder`, whose destroyed action fires the
relay if she is still there to see it, and a `Damage a guard in the city district` relay that turns the
district's guards on the player. All three pieces are put back.

**The consequence end is the map's own, not an invention.** Every `spaniard` generator already adds a
`CHandleMessageAI{Message To Handle=GoToCombat, Action=Spaniards Attack Player}` to its spawn, so
attacking a defender turns the whole garrison **and hands the player +40% AC for the trouble** -- a
working vanilla mechanism. Murdering an unarmed civilian produces no `GoToCombat` to hang that on, which
is exactly what the witness is for, so `Damage a guard in the city district` is rebuilt as a thin relay
that delegates to `Spaniards Attack Player`. Both shipped names keep their shipped meaning, and the
scene ends in the shipped consequence.

**Only civilians arm it.** A destroyed script fires whoever the killer was, and the English kill
defenders all through the siege, so hanging the scream on a guard's death would turn the garrison on the
player for something the English did. Civilians are on nobody's target list, so a civilian only dies if
the player kills one. She and the man searching for Phillipe are the two people on the map she can watch
die -- which is the peacetime scene exactly.

**Left alone deliberately:** `defenders hate player trigger`, on both siege maps, `Active=0`, activated
by nothing, and pointed at the name `defender`, which no entity on either map carries. Its own comment
-- *"When a player attacks a defender, this becomes active and makes the defenders nearby attack players
as well"* -- describes the localized draft that `Spaniards Attack Player` replaced and wired. That is a
superseded draft, not a defect, and it stays as it is.

### The two men nobody could hear

`Random Contacts in Barcelona` holds six dying-soldier lines; the act opens four. The two it never
opened are the two best ones:

| node | line | now |
|---|---|---|
| `31 Spanish Body on Ground` | *"Stranger...here...take my gold. Don't let those English have it..."* | a `Generic Gaurd NPC` at 1618,845, and **he hands over the 250 gold he is talking about** |
| `42 English Body on Ground` | *"I am sorry Espana...I do not know why we came with swords drawn and bloodlust in our hearts..."* | a `Soldier1` at 1678,2914 |

Both go on the generator's own `After Action` in the same `CAddAIAction` + `GetCloseThenTalk` shape the
map's three talking bodies already use.

And **`Temple District Siege` has 62 dead bodies and not one of them speaks** -- the whole map opens a
single node of this tree, its arrival bark, and has zero talkable parts. Six of its bodies get voices
now, each matched to its side: three Spanish and three English, spread west to east rather than
clustered, and its dying Spaniard pays the same 250.

## 0.18.0 - the Barcelona Attack


### Tier 6 - the act learns to read you, and the crypt stops being an empty room (built)

Across eight maps act 6 read the player **three times**: `PE 8+` and `Speech moreequal 70` on Surrey
O'Connell, and a `Sneak < 100` check on the chest he is guarding. Nothing else in the act looked at who
was standing there -- not the blacksmith's eight replies, not one node of the other seven trees. And
across eight maps there was **not one trap, not one secret and not one locked container** besides that
same chest.

**Surrey O'Connell** is the act's one negotiation and its best-written character: an Irish supplies
master pressed into feeding the army that took his country, who opens by grovelling, calls himself
*"happy I am to serve the English"*, and begs not to be sent to the Spanish Inquisition. Two things he
says out loud are levers the act never pulled.

| lever | who has it | what he does |
|---|---|---|
| the **Clover from the drowned fields of Ireland**, which the Irish sailor in the Port District hands over in 0.9.1 | anyone who took it | the performance stops -- *"Drowned. The whole of it drowned, and I am out here weighin' out bolts for the men that let it."* |
| **the Holy Office** | a sworn Inquisitor | *"I said it as a manner of speakin', it is a thing a man says!"* -- and the strap is already off the nearest crate |

Either one and he looks the other way. `Surrey looks away` is a checker, and `Open Chest of Surrey` --
the relay that makes him shout `150 Open Chest`, wake the `chest guards generator` and turn on the player
-- now guards on `CAndAction[Surrey is alive, NOT Surrey looks away]`. That is **two new routes past the
act's one guarded prize**, beside the Sneak 100 vanilla shipped, and they cost the player nothing but
having listened to an Irishman in a bar two acts ago.

**The blacksmith** gets three reads on the conversation that had none:

- `Templar IS` / `Inquisitor IS` -- *"The Temple put twenty at the Gate and the Holy Office put its own at
  the Temple crossing, and both lines held until the golems came up the street, and then neither of them
  did. I shod horses for half those men."*
- `Tainted race - feralkin or sylvant` -- *"This morning I watched a thing made out of ice walk through
  the front of the Alvarez house with the family still in it. You are a man with a face."*
- **Slayer of Innocents**, reaching back to tier 4 -- he has heard the reports, weighs the hammer, sets it
  aside, and sells to you anyway: *"Do not come back after the city is standing."*

**And the Church Crypt** was the emptiest map in the project: thirteen parts -- three wall pieces, a
lamp, a broken door, one dead city guard, and nothing else at all. It gets the act's **first secret,
first trap, first hidden lock and first voice**: one slab in the wall newer than the rest, grey mortar
where everything else is black, put in from this side by somebody who knew the English were on the road;
behind it the sacristan's plate in a chest at `Lock Pick Adjustment=-40`; and poison gas on the slab at
`Skill Adjustment=10`, so a thief can see it coming and a Lockpick 40 can take it out. The guard on the
stair can be looked at, with his sword still in his hand and his feet toward the stair.

Both the trap and the chest are **sliced out of working parts** -- the poison gas trap from
`2 Retreat of Souls` and the locked chest from `9 Burial Chamber` -- then repositioned and retuned,
rather than authored from scratch. Gate 0 caught the two things that were authored: `Requirement=` takes
a can's **basename** as vanilla writes it (`Templar IS`, not a lowercase path), and every `Requirement=`
needs a blank line in front of it.

### Tiers, in the order they should be built

1. ~~**The silence.**~~ **Built** -- see above. The reserve waves `fight2` and `fight4`, whose
   `activate fightN` relays are live and called by nothing, are a separate question and deliberately
   untouched: the Gate District already fields 249 combatants.
2. ~~**The two quests that do not exist.**~~ **Built** -- one state each, begun in act 6 and completed
   at act 8's final encounter. Raphael's act-1 half of the same thread is still open.
3. ~~**`Crossroads Siege`.**~~ **Built** -- three narration lines, the army's seven barks ported in,
   and the trail of the column for a player who asked the blacksmith first.
4. ~~**The child-killer reaction.**~~ **Built** -- the title is granted for the first time in the
   game's history, act 6 arms the flag it was already carrying, and the father searching for Phillipe
   stops accusing strangers. Phillipe himself is now on the map.
5. ~~**The shy girl with no speaker, and the two death lines.**~~ **Built** -- the witness exists, her
   scream resolves, and it ends in the garrison relay vanilla already wired. Both dying men can be
   heard, the Spaniard hands over his purse, and the Temple District's 62 corpses are no longer mute.
6. ~~**Reactivity.**~~ **Built** -- Surrey reads the clover and the Holy Office, the blacksmith reads
   your order, your face and your reputation, and the Church Crypt gets the act's first secret, trap,
   lock and voice. **All six tiers of act 6 are built.**

Also from this survey, for a patch rather than this release: **0.14.1** -- `02 Hamlet Burned` carries the
same three dead defender relays, so Montaillou's burned hamlet is silent for the same reason.

And from the Guy Fawkes trace: **an act-1 repair**. `Conspirator.DialogTree` has two orphan nodes.
`200 kill duke 6` -- *"If this deed is done, you will be remembered forever in English history as one of
it's most heroic patriots. When the deed is done, return here."* -- is reached by nothing and opened by
nothing, so part of the thread's own payoff text never plays even inside act 1. `100 Guy Fawkes` is a
**blank node** (no text, no replies) and should be recorded as a stub rather than wired.

## 0.17.0 - the Caverns of Nostradamus

**Published.** Cut from `main` 2026-09-25, entirely unplayed. Surveyed and built the same day, eleven tiers. Tier 3b places an English army the shipped game built and never deployed; tier 8 gives its commentary a speaker; tier 9 adds a third way through the act. Act 5, `Levels/5 Nostrodomus` -- misspelled in the
shipped game, and left that way here because every reference in every map spells it the same.

**The act.** Ten maps, 5,178 level parts, **1,130 live enemy spawners**, 8 dialogue trees, 103
nodes, 176 player replies, two quests. For scale: the Crypt, which this project has just spent ten
tiers on, has 273 live spawners. This act has **four times** as many, and the fewest voices of any
act surveyed -- **eight of its ten maps open no conversation at all**, and two of them (`07 Cave 2`,
`09 Cave 4`) have no balloon, no bark and no tree either.

| map | parts | live spawners | conversations | balloons |
|---|---|---|---|---|
| 01 Heart Entrance | 517 | 216 | 5 | 19 |
| 02 Clan of the Hand A | 1283 | 266 | 0 | 3 |
| 03 Tourniquet of Pain | 662 | 272 | 0 | 4 |
| 04 Clan of the Skull B | 1024 | 168 | 0 | 4 |
| 05 Nostrodomus Demesne | 187 | 10 | 9 | 6 |
| 06 Cave 1 | 124 | 6 | 0 | 5 |
| 07 Cave 2 | 387 | 44 | **0** | **0** |
| 08 Cave 3 | 430 | 72 | 0 | 4 |
| 09 Cave 4 | 448 | 52 | **0** | **0** |
| 10 Cave 5 | 116 | 24 | 0 | 2 |
| **total** | **5178** | **1130** | **14** | **47** |

### The act has a side to choose, and neither side can be chosen

The English are storming the Hujark caves to reach the seer, and act 5 is built to let the player
pick a side. Two quests, one per side, both with exactly one state:

| quest | activated by | completed by |
|---|---|---|
| `Defeat the Hujark defenders and capture Nostradamus` | the relay `Player sides with the English` | arriving at `05 Nostrodomus Demesne` |
| `Protect Nostradamus from the invading English forces` | the relay `Player sides with the Hujark` | the same arrival |

Both are failed if the player leaves through the Hamlet portal. Each quest's own machinery is
sound. What is not sound is that **neither flag can ever fire**, traced backwards through every
`Relay Name` and `Target Name` in every map and every dialogue tree:

| flag | fired from | reachable? |
|---|---|---|
| `Player sides with the Hujark` | one reply in the entire game: *"I have come to help the Prophet"* at `50 help prophet` in `hujarkgeneral.dialogtree` | only if the general exists |
| `Player sides with the English` | seven more nodes of the same conversation, **and** the relay `Player attacks any of the Hujark in this fight` | that relay's only two callers are `Hujark General Generator` and an unnamed generator, **both `Active=0`** |

So the whole of act 5's branching -- both quests -- hangs on one conversation with one character who
never spawns. `05 Nostrodomus Demesne`'s `Start Here` completes both quests on arrival, and in the
shipped game it completes nothing, because neither was ever activated.

**The two named Hujark are disabled together.** `Hujark General Generator` (`New Name=Hujark
General`) and the unnamed generator that produces `Swordsman ShieldHelmet` as `Hujark Guard` are
both `Active=0`, and the second is what would have fired *"player attacks any of the Hujark"*. The
roughly two hundred Hujark who **do** spawn live on that map -- swordsmen and lesser shamans in
five flavours each -- are all anonymous, with no `New Name` at all, so attacking them fires nothing.
The relay was only ever wired to the two named ones.

`60 Harm Prophet dialog balloon` is dead for the same reason -- it is fired only from the general's
own conversation -- and so are the eight `Hujark dialog balloons` that position over his head, which
are fired from inside his own disabled generator.

**Correction to an earlier reading of this map.** `Start Wielder intro scene` was listed here as
`Active=1` and fired by nothing. It is a `CTouchingPolygonTriggerAI` **polygon**, which needs no
caller -- the player walking into it is the trigger -- and it fires `Wielder Start NIS` normally. The
Wielder intro at the Heart Entrance works in the shipped game. Self-triggering polygons are the same
false-positive class as unreferenced generators, and belong in `deadparts.py`'s exclusions.

**And a complication that turned out not to be one.** Both disabled generators are
`CSimpleGeneratorForCannedEntitiesAI`, which this project's notes call the ambient-background class,
not the `CGeneratorAI` that real interactable NPCs use -- so the survey expected the general to need
rebuilding. He does not. The counter-example is two maps away: the **Frightened Apprentice** on
`06 Cave 1` is a scripted, talkable NPC spawned by `CSimpleGeneratorForCannedEntitiesAI` with a
`CAIInteractionSpecifier` in its `AIs to Add`, and it works in the shipped game. The note's warning
applies to *persistent* NPCs, not to a scripted one that appears for a single scene.

**And the Hujark General never spawns.** `Hujark General Generator` on `01 Heart Entrance` is the
only thing in the game that would produce him -- `Entity=Levels/5 Nostrodomus/Character
Templates/Hujark General`, `New Name=Hujark General` -- and it is `Active=0` with **no reference to
it anywhere**, checked case-folded and comma-aware across every map and every dialogue tree. Yet
eleven live parts on that map address him by name: `General talks to player`, which both opens his
conversation and assigns him a combat AI; eight `Hujark dialog balloons` positioned over his head;
`60 Harm Prophet dialog balloon`; and `Player attacks any of the Hujark in this fight`, which
names him in a comma list with `Hujark Guard`. Two position markers, `General goto` and
`Guard goto`, mark where he and his guard were to walk.

So the Hujark side of act 5 -- a 41-reply conversation, the choice to defend the seer, and one of
the act's two quests -- is unreachable in the shipped game, and the only path through is to attack.
This is the Guard Pablo pattern at the scale of an act branch.

His conversation has a second, smaller fault behind that one: `3 Return Dialogue` -- *"You return?
Have you changed your stance?"*, seven replies including both ways to commit -- is reached by
nothing and opened by nothing, so even with him spawned you could talk to him once. The idiom for
this is on the map next door: Jehanne's `Joan Add talk AI after she talks first`.

### The one mechanic that would make 1,130 spawners vary was specified and never connected

Nine of the ten maps carry a checker named `hujark summoning enabled`, `Active=1`, with a designer
comment on the part itself:

> This checker enables shield-helmet swordsmen to summon snakes from the clone gen

`02 Clan of the Hand A` and `04 Clan of the Skull B` carry `snakebreed summoning enabled` as well.
Every one of those eleven checkers is read **zero times** -- by any key, in any map, in any
dialogue tree, case-folded and comma-aware. The clone sources they were to gate are placed too:
`Snakebreed Clone Generator` on nine maps and `Snakebreed Summoner Clone Generator` on two, all
`Active=0`, and **named by nothing**, so no `CCloneAction` ever copies them.

The engine supports exactly this, and the game does it elsewhere. `Ogre Conjurer Cave.zax` has
`Aka Manah Illusion relay`, which fires `CCloneAction{Source Name=Wizard Tremblethorn Illusion
100%/70%/35% Generator}` off a `CHealthPercentThresholdTrigger` -- a boss that summons copies of
itself as it loses health, in three tiers. There are 371 `CCloneAction` sites naming a source
across 45 maps, so the primitive is thoroughly precedented; act 5 simply never called it.

This is the act's largest single opportunity. Every fight in it is a static wave, and the fix was
placed, switched on, commented, and left unplugged.

### The battle you are fighting alongside barely speaks

`Losing side wins a fight.DialogTree` is seventeen nodes of running commentary from whichever side
the player joined -- *"You must get to the Seer before the Druids do!"*, *"We are breaking through
their defenses!"*, six escalating lines per side, plus `150 Final encounter`,
`155 Final encounter shaman` and `157 go now` for the seer's door. **Two of the seventeen are ever
opened**: `30 Hurry` and `40 Quick`, both from `03 Tourniquet of Pain`, by
`Are English3 alive?` and `Are Hujark3 alive?2`. The escalation series and all three
final-encounter lines are fired by nothing, on an act where the player crosses ten maps of
identical fighting with no sense of progress.

The barks are lopsided the same way. All eight nodes of `HujarkWarriorCanned` are wired to
`Hujark dialog balloons`; only four of `EnglishMonsterWarriorCanned`'s eight are, leaving
`10 Hey`, `11 wise`, `20` and `50` unused -- so the side you are most likely to be fighting
alongside is the quieter one.

### The seer's own lost answers

`Nostradamus.DialogTree` is the act's real conversation: 38 nodes, 108 replies, four prophecies,
and a karma-split farewell that works. Three nodes are stranded.

| node | text | why it is stranded |
|---|---|---|
| `10 Nostradamus` | *"To the Hujark, I am a prophet, a power they revere and worship. But I was not always like this."* | Its reply returns to `5 questions`, exactly like every other answer, but nothing points at it. `5 questions` asks *"What are you?"* and routes to `35 Prophet` instead |
| ~~`100 Dragon Prophecy`~~ | *"Uncaged by the Betrayer, the demon of storms waits for you in its forsaken lair."* | **Not stranded -- this was an artefact of a case-sensitive audit.** `70 dangers` reaches it with *"Tell me about the serpent."*, spelled `100 dragon prophecy` in lowercase. Tier 4 makes the casing exact anyway |
| `30 Combat` | *"<A voice laughs inside your head> Fool, you cannot fight your *fate*."* | The seer's line for being attacked, opened by no map |

`40 Ingame Movie Opening Line` -- *"But before the spinning coin can land, it will be caught by the
slaver's hand"* -- is also unopened, and belongs to a cinematic that is not in the retail build.
Left alone.

### What the act asks about the player: almost nothing

| gate | act 5 |
|---|---|
| faction | 7 |
| karma | 3 |
| attribute | 3 |
| race, Speech, Barter, magic school, perk, spirit, gender | **0 each** |
| trap / lockpick, on replies **and** on map triggers | **0** |

Ten maps of caves and tunnels, and not one trap or lock in any of them. The Crypt got 67 such
checks in one tier and they changed a thief's whole route; this act has nothing for a thief, nothing
for a talker, and nothing for any of the three spirits.

### The assassin at the seer is a different character, and works

Easy to confuse with the general, so recorded: `05 Nostrodomus Demesne` spawns `NIS Assassin1
Generator` live (`Assasin` / Tough / Super, `New Name=Assassin`), and he speaks four nodes of the
**Crypt's** `Assassin.DialogTree` -- `100 Silence`, `100 seer`, `100 lies` and
`100 scion of lionheart` -- as balloons fired by `NIS Start` and `NIS Relay 2`. That is the Old Man
of the Mountain's thread, which runs from the Slave Pits intro through Montserrat's wounded
assassin, the Crypt and the English Shrine to Alamut, and it ships working.

He carries **no interaction specifier at all**, only combat AIs, so he talks at the player in the
opening sequence and is then fought; he is not a conversation. The talkable NPCs at the Demesne are
Nostradamus himself, after `Kill all 3 guys get AI added to Nostrodamus` adds his talk AI, and the
`Monk` (a `Wielder Apprentice` spawned under that name, using the La Calle Perdida Wizard trees).
Hujark named NPCs do exist elsewhere in the act -- `Hujark Guard` and `Hujark Shaman` both spawn
live at the Demesne. It is specifically the pair at the entrance that is switched off.

### Checked and not defects

- **The Ways Crystal works.** `01 Heart Entrance` holds a live one that writes `Green Way Crystal 3`
  and can complete the Calle Perdida chain's `ALL FOUND` flag. The act-5 end of that quest is sound.
- **Both quest files are well formed** and their completion and failure wiring is correct; the
  fault is entirely upstream, in the fact that nothing can activate them.
- **The karma farewells work.** `determine goodbye relay` on the Demesne picks between
  `11 evil karma goodbye`, `12 neutral` and `13 good`.
- **The Hujark Assassin's `4 sneak`, `5 barter` and `6 No`** looked like a cut alternative to the
  ambush -- sneak past, or pay a ransom. They are **byte-identical copies of the Frightened
  Apprentice's lines** in a tree that shares its node IDs, and the apprentice's own five-step series
  on `06 Cave 1` is fully built. A copy-paste artifact, not cut content.

### Tier 1 - Huko, and the two quests behind him (built)

The set-piece is fully built and rather good, which is what makes its being switched off worth
undoing rather than replacing. Huko, General to the Hujark, spawns **passive** -- `Valid Targets=` is
empty in his template -- barks his eight lines on a five-second timer, and `General talks to player`
hands him a `CSkeletonAI` whose `Trigger=First Time` transition into Attack fires
`CDisplayDialogTreeAction` instead of a swing: he crosses the ground as though to attack and speaks
instead. `CSendAIDoneMessage` then ends the temporary task and he reverts to his passive template AI.
Hit him first and a damaged-script set in his generator's `After Action` fires the English flag. Side
with him and he and his guard walk to `General goto` and `Guard goto`, fade over a second, and delete
themselves.

Three things were missing, and all three are one-line absences rather than missing content:

| what was missing | what it cost | the repair |
|---|---|---|
| nothing activated `Hujark General Generator` | Huko never existed | `Active=1` |
| nothing activated the **unnamed** generator that spawns `Swordsman ShieldHelmet` as `Hujark Guard` | his guard never existed, and with him the only non-dialogue caller of the English flag | `Active=1`, and a name -- `Hujark Guard Generator` -- so something can address it |
| nothing fired `General talks to player` except the attack path | he could not open the conversation even if he existed | the arrival spawn point |
| his template's `GetCloseThenTalk` specifier has an empty `Action=` | the player could never start a conversation, and `3 Return Dialogue` -- seven replies, both ways to commit -- was reachable from nowhere | the specifier now opens `1 Conversation Start`, and the talk transition swaps it to `3 Return Dialogue` afterwards |

**The hook is the arrival point's empty `Per Party Spawn Action`.** `start here` at 1077,2552 is where
the player lands coming in from the wilderness, and its spawn action was blank; `crystal start here`
seventeen units away uses its own for the autosave and the Barcelona-companion cleanup, so the idiom
is on this map already. It now activates both generators in one comma-listed `CActivateAction` and,
half a second later, fires `General talks to player`. No new polygon and no geometry to get wrong,
and because both generators have `Already Generated=0`, leaving the act and returning does not
produce a second Huko.

**The return conversation** uses Jehanne's idiom from the Crypt: the same `Trigger=First Time`
transition that opens the conversation also swaps his specifier, so after he has spoken once,
clicking him opens `3 Return Dialogue` -- *"You return? Have you changed your stance?"* -- with
`Allow Interact If Has Target=0`, so a Huko who is trying to kill the player cannot be chatted to.

**What it opens up.** Traced forwards, every link now has a live caller, and for the first time both
of the act's quests can be entered:

| step | reached from |
|---|---|
| `Hujark General Generator`, `Hujark Guard Generator` | `start here`, on arrival |
| `General talks to player` | `start here`; still also the attack path |
| `Player attacks any of the Hujark in this fight` | both generators' damaged-scripts, and seven fight replies |
| `Player sides with the Hujark` -> quest state `DH253J5T` | *"I have come to help the Prophet"* |
| `Player sides with the English` -> quest state `I4QTGAGA` | seven replies, and hitting either named Hujark |
| `60 Harm Prophet dialog balloon`, `Hujark dialog balloons` | the conversation, and his spawn timer |

Two things deliberately left for later tiers. The `Hujark dialog balloons` relay has two further
callers on `03 Tourniquet of Pain` -- `English Generator` and `Hujark Generator`, both `Active=0`
there -- which belong with tier 3's commentary. And the roughly two hundred **anonymous** Hujark on
the entrance map still fire nothing when attacked: only the two named ones carry the damaged-script.
Whether swinging at the rank and file should also commit the player to the English is a design
question, not a defect, and it is tier 3's to answer.

**Position is the one thing static reading cannot settle.** Huko's generator sits at 1316,2210, about
350 units up the path from the arrival point, and `General goto` is at 734,2179. Those are the
designers' own coordinates, but a spawn point that has never run is a spawn point nobody has watched.
First thing to look at in play is whether he appears on the floor and can reach the player.

### Tier 2 - the summoning the checker was placed to enable (built)

The comment is on the part itself, in the shipped game, on nine of the ten maps:

> This checker enables shield-helmet swordsmen to summon snakes from the clone gen

`hujark summoning enabled` is `Active=1` on all nine and read **zero times** anywhere. The
`Snakebreed Clone Generator` it points at is placed on the same nine, `Active=0`, and named by
nothing, so no `CCloneAction` ever copies it. The act has 1,130 live spawners and not one of them
behaves differently from any other.

Every piece needed is precedented, in three different places:

| piece | where vanilla does it |
|---|---|
| fire an action when a monster crosses a health percent | `Ogre Conjurer Cave`: a `CAIHealthPercentThresholdTrigger` in a generator's `AIs to Add`, so every spawned entity carries its own |
| put a monster on the ground at a moment's notice | `4 Misc Crypt 2`: `CCloneAction{Source Name=<a generator>, Random Location Delta=75, New Name=used clone gen}` then a delayed `CDeleteAction`. The clone is **never activated** -- cloning a generator is what makes it run, and the temporary copy is swept up 0.3s later |
| aim that clone at the entity whose own AI fired it | `Barcelona Coast`'s `Wave Cloner`, which clones at `$Trigger` from a per-part timer AI |

So a shield-helmet swordsman driven below **half** health calls a snake out of the floor beside him,
if this map's checker says he may. The snake is vanilla's own generator, whose four
`Max Party Mojo` groups scale it from a `Snakebreed Venom` to a `Venom Tough` with the party's
strength -- so it is a threat at the level the player actually arrives at.

**Thirty-one generators, on five maps:**

| map | summoning generators | which |
|---|---|---|
| 01 Heart Entrance | 9 | `Hujark Generator` |
| 02 Clan of the Hand A | 5 | `Shield Helmet Swordsman Generator`, `apprentice generator` |
| 03 Tourniquet of Pain | 13 | `Hujark Generator` |
| 04 Clan of the Skull B | 3 | `Shield Helmet Swordsman Generator` |
| 07 Cave 2 | 1 | `Fight` |

**Named characters do not summon.** A generator that gives its spawn a `New Name` is making a
character, not a battlefield swordsman, and three were excluded on that rule: Huko's own
`Hujark Guard` from tier 1, `xloserx` in the Cave 1 set-piece, and `xhujark1x` on Cave 3. The first
draft of this tier caught all three, which is what the rule came out of.

**This adds enemies to the grindiest act in the game, and that was the honest objection to it.** The
argument for doing it anyway is that it changes the *shape* of a fight rather than its length: the
helmeted swordsman is now the one to kill first, and a player who ignores him fights the snake he
called. The objection was put and **the summoning is kept, by decision, 2026-09-25** -- the same call
as the Crypt's spawner counts in 0.16.0, where thinning was considered and rejected in favour of
making the place more interesting. Do not quietly tune it away.

**And tier 2b puts the dial in the player's hands instead of the modder's** -- see below. The
modder's dials still exist if *play* says otherwise, and both are one-line changes: the threshold is
a single `Constant Value=50`, and each map's checker is its own off switch, which is what the
designers built those nine checkers to do. `NO19` is the row that reads the balance in play; nothing
changes before somebody has walked it.

**Left for later, deliberately.** `05 Nostrodomus Demesne`, `09 Cave 4` and `10 Cave 5` carry the
checker and the clone source but have **no anonymous shield-helmet swordsman** to hang a trigger on
-- only lesser shamans. A shaman summoning a snake is arguably a better fit than a swordsman doing
it, and extending the filter is one line, but the comment names shield-helmet swordsmen and this tier
does what the comment says. `snakebreed summoning enabled` on maps 02 and 04, and the
`Snakebreed Summoner Clone Generator` it presumably gates -- which spawns a `Mongol Goblin Archer
Super`, an `Ogre1 Ranged` and a `Bear Super`, an odd set -- are still unwired.

**If `$Trigger` does not resolve the way the Wave Cloner implies**, the clone does not happen and the
act fights exactly as it does today. The failure mode is silence, not breakage, which is the main
reason this was worth building before anybody has walked the act.

### Tier 2b - the serpents know Sahar's mark (built)

The snakebreed are the Old Man of the Mountain's serpents, and the game says so without ever saying
it out loud:

- `02 Druid Council Level1`, the Montserrat map where the **wounded assassin** is found, is held
  almost entirely by them -- Snakebreed, Snakebreed Venom and Snakebreed Boss, in three tiers each,
  more than a hundred spawns between them.
- the bestiary carries a `Snakebreed Assassin.can` that **spawns nowhere** in the shipped game.
- Sahar's ring, taken at `50 her word` for accepting her word, is already read as a safe-conduct by
  the Crypt's assassin: *"Sahar's mark. Then she let you go, and sent you to us wearing it, and
  thought that would be the end of it."*

So a Hujark swordsman can call all he likes. If the player wears her mark, the serpents do not come:

> The Hujark strikes the floor with the flat of his blade and calls, the way the others have been
> calling all along this corridor. Nothing comes up out of it. He looks at the ring on your hand, and
> he does not understand what he is looking at, and he goes back to fighting.

**It is visible, which is the point.** A silent buff that removes content the player never knew was
there is not reactivity; being shown the swordsman call and the floor not answer is. The line plays
**once per map** -- a second checker, `the mark has been read`, holds it after the first time -- so
five corridors give five readings of the same fact rather than thirty-one.

**Two checkers per summoning map carry it**, and no self-reference is needed anywhere in the monster's
AI, which is what makes it safe: `serpents know the mark`, switched on at the mouth of the caves, and
`the mark has been read`, switched on by the first unanswered call. The summon now asks three
questions in order -- is summoning enabled on this map, do the serpents know the mark, has that been
explained yet -- and only the first path reaches the clone.

**The ring is read where vanilla reads inventory from a spawn point.** `Calle Perdida`'s
`From Gate District` does exactly this in its own `Per Party Spawn Action`, with
`Who to give check=$instigator`, so the check sits in a context the shipped game already proves out.
Arriving at the Heart Entrance carrying the ring activates the mark on this map and, through four
`COtherMapAction`s, on the other four summoning maps at once.

**What it means for the act.** A player who spared Sahar at Montserrat and kept her ring walks act 5
the way it shipped, with the fights he expects; a player who did not gets the act the designers
commented into the margin and never wired. The reward for a two-act-old mercy is that the serpents
will not bite you, and nobody in the Caverns can explain why.

### Tier 3 - the English get a voice, and the seer's door reads which side you took (built)

Two more silences with the same cause as Huko: a part addressed by name that nobody creates.

**The English have never said a word.** `English dialog balloons` on the Heart Entrance is a
`CShuffledSeriesAction` of four `EnglishMonsterWarriorCanned` barks, every one positioned on an
entity called `English loser` -- **created by nothing, anywhere in the game** -- and the relay itself
is fired by nothing. Meanwhile the Hujark's eight barks work, because `Hujark General Generator`
names `Hujark General` and drives them from a `CRepeatTimerTriggerAI` in its own `AIs to Add`. Tier 1
brought those eight to life by activating that generator; this does the same for the English by the
same means:

| | Hujark (vanilla, live since tier 1) | English (this tier) |
|---|---|---|
| speaker | `Hujark General Generator` names `Hujark General` | one live `Big Fight` at 2096,1418 now names its ogre `English loser` |
| driver | `CRepeatTimerTriggerAI`, 5s +/- 2, in `AIs to Add` | the same AI, the same timing |
| lines | 8 of 8 | **4 of 8 -> 8 of 8** |

`10 Hey`, `11 wise`, `20` and `50` were in the tree and in no relay. `EnglishMonsterWarriorCanned`
now has **no unopened nodes**.

**The seer's door turned three friends into enemies.** `NIS Relay 2` closes the arrival cutscene by
firing `CGoToCombatAction` at the assassin, the `Hujark Shaman` and the `Hujark Guard` --
unconditionally, including for a player who agreed with Huko to defend the Prophet an hour earlier.
The commentary tree has had the line for the other case all along:

> The Seer has been expecting you. You may enter now.

So the closing array now asks first. Side with the English, or never commit, and it behaves exactly
as it shipped -- the `Fail Action` is vanilla's two actions, in vanilla's order, with vanilla's
1.5-second delay. Side with the Hujark and the shaman stands aside with `155 Final encounter shaman`,
the guard follows with `150 Final encounter` -- *"Thank you! Now quickly come with me."* -- and twelve
seconds later, if you are still standing about, `157 go now`: *"Do not keep the Seer waiting."* The
assassin still attacks either way; he is the Old Man's, not the Hujark's.

**The plumbing is vanilla's own.** `Player sides with the Hujark` already fires
`Activate English generators` at all nine other maps through `COtherMapAction`, and that relay part
exists on **none** of them. Creating it on the Demesne -- where its one action activates a
`sided with the Hujark` checker -- makes vanilla's own cross-map call land for the first time, and
costs nothing anywhere else.

### What tier 3 found: the act's two armies

The two side relays are extensively commented, and the comments describe a system far larger than the
quest flags:

> `Player sides with the Hujark`: This relay activates the English generators which can spawn both
> types of enemies (english and hujark)

Each relay holds twelve actions: the quest state, a local activation, and **nine
`COtherMapAction`s** firing `Activate English generators` / `Activate Hujark generators` at every
other map in the act. The design is plain -- **the act populates itself with whichever enemy you
chose to fight**. That is also why `03 Tourniquet of Pain` has 21 `Hujark Generator` parts and
`04 Clan of the Skull B` has none of either name: the armies were meant to be switched on by choice,
and the Hujark half was simply left on by default.

None of it exists:

| named target | where it exists |
|---|---|
| `Activate English generators` | **no map in the game** |
| `Activate Hujark generators` | **no map in the game** |
| `English Generator` | one part, on `03`, `Active=0`, with an **empty entity list** -- it spawns nothing |
| `england`, `Druid defaulter` | **no map in the game** |
| `English3`, `English3a`, `English3b`, `Hujark3`, `Hujark3a`, `Hujark3b` | **created by nothing** -- the paired-skirmish cast the four live `Are ... alive?` relays on `03` were written to test |

So every player who has ever walked act 5 has fought the Hujark, on a map set built to be populated
either way, and the "battle between two sides" is one army plus six English ogres on the first two
maps.

**It looked like missing content. It is not: the army exists and was never placed** -- see tier 3b
below, which builds it.

The same absence is why fourteen of the commentary tree's seventeen nodes are still unopened:
`10 Hujark underdogs win`, `20 English underdogs win`, `30 Hurry`, `40 Quick` and the two escalation
series need an **allied speaker per map**, and the act has no allied entity anywhere outside the
Heart Entrance. Tier 3 opened the three that had a speaker available.

### Tier 3b - the English army that was built and never placed (built)

There is a folder in the shipped game called
**`Resources/Monster Cans/English in Caverns of Nostrodomus/`**. It holds fourteen units made for
this act and placed **nowhere**:

| unit | tiers |
|---|---|
| `Nos Soldier1` | base, Tough, Super |
| `Nos Soldier2` | base, Tough, Super |
| `Nos Soldier2 Bow` | base, Tough, Super |
| `Nos Soldier3` | base, Tough, Super |
| `Nos Ogre2 English` | base, Tough |

They are complete templates -- the same five activities as the `Ogre2 English` the act already fields,
`Category=Enemy`, real XP values, backed by real races under `Races/Enemies/English Enemies/`. So the
English army for act 5 was designed, statted, tiered, given archers, and then never given a generator
to come out of. That reframes the whole thing: this is not authoring content, it is placing content.

**The act is already trying to switch it on.** `Player sides with the Hujark` does
`CActivateAction{Target Name=English Generator}` locally on the Heart Entrance and fires
`Activate English generators` at the nine other maps. So the build is simply to create what those
calls are reaching for, and the shape is dictated: twin the generators that already field the Hujark,
at the same coordinates, with the English roster.

**Ninety-nine English generator parts, on nine of the ten maps:**

| map | English parts | from | size |
|---|---|---|---|
| 01 Heart Entrance | 12 | `Hujark Generator` | +101 KB |
| 02 Clan of the Hand A | 34 | `Swordsman`/`Shield`/`Dual`/`Shaman` generators | +201 KB |
| 03 Tourniquet of Pain | 16 | `Hujark Generator` | +136 KB |
| 04 Clan of the Skull B | 16 | the same swordsman set | +95 KB |
| 05 Nostrodomus Demesne | 1 | `Hujark Generator` | +19 KB |
| 07-10 the caves | 20 | shamans and `Fight` sets | +122 KB |
| 06 Cave 1 | -- | fields no Hujark at all, only fauna | -- |
| **total** | **99** | | **+675 KB** |

Twinning means the coordinates are the designers' own -- every English soldier stands where the game
already spawns a swordsman, so there is no placement to get wrong. Tier 2's snake-summoning trigger is
stripped from every copy: the English do not call serpents.

**It is a swap, not a doubling, which is what makes it honest.** Each twin ships `Active=0`. Side with
the English, or never commit, and **nothing changes from vanilla at all**. Side with the Hujark and
two things happen at once: the ninety-nine English parts come on, and the hundred Hujark generators
they were twinned from stop targeting you -- each one's `After Action` now asks
`CCheckExistenceAction{sided with the Hujark}` and, if so, sets the spawned swordsman's targets to
`Scripted Custom 2`, the English, instead of the player. So the enemy count stays about where it was;
what changes is who is shooting at whom.

**The two sides were already modelled and this just uses it.** Hujark carry `Scripted Custom 1` and
target `Player,Player Friend,Scripted Custom 2`; the `Big Fight` English ogres carry
`Scripted Custom 2` and target `Scripted Custom 1` only, which is why they have always ignored the
player and fought the Hujark. Every twin now states its side outright in its own `After Action` --
`Scripted Custom 2`, hunting `Player,Player Friend,Scripted Custom 1` -- because two of the maps set
no categories at all and one `Hujark Generator` on `03` is itself configured for the English side, so
copying its numbers blind produced a twin that fought its own army. Stating it beats inheriting it.

The cave fauna is untouched everywhere. Snakebreed, spirits and vodyanoi answer to nobody and go on
trying to kill everything.

**Eight of vanilla's nine cross-map calls now land** -- the ninth is Cave 1, which has no Hujark to
switch. On the Heart Entrance no new relay was needed, because vanilla already activates
`English Generator` there by name.

**What this makes of act 5.** Refuse Huko, or kill him, and the act is exactly the game that shipped.
Agree to defend the Prophet and it becomes the other act: English soldiers and bowmen holding the
corridors, Hujark swordsmen fighting beside you instead of at you, and at the end a shaman who stands
aside and says the Seer has been expecting you. Both halves were in the box.

### Tier 4 - the seer defends himself (built)

**Nostradamus was built to fight back, and nothing ever started it.**
`Nostrodomus Attack Preparation` is `Active=1` and fired by **nothing**. It turns him hostile, waits
four seconds, activates `Nostro Attacks Player timer`, and calls `Monster summoning`. The timer drives
`Nostradamus attacks` -- a `CShuffledSeriesAction` of four ranged spells, lightning bolts and celestial
smites for 3 to 15 electrical damage, cast from across the chamber. His generator already carries a
destroyed-script that opens the portal when he falls. He has his own taunt for being struck
(`30 Combat`: *"<A voice laughs inside your head> Fool, you cannot fight your fate. Did you think that
I would not anticipate your actions?"*), a second for the fight itself (`1001 Goto combat`), and a line
for beating you (`30 Combat Nostradamus Defeated`: *"I have already transcended this mortal coil. You
will not prevent my transformation. Your failure has been foreseen."*).

All of it was switched off. Strike the seer in the shipped game and he stands there and takes it.

The trigger is the idiom this very act already uses on Huko: a `CSetDamagedScriptActionAction` that
asks whether the damager is a player. His generator's `After Action` already sets a destroyed script, so
the damaged script goes in beside it, and the sequence reads:

| when | what |
|---|---|
| the first blow lands | `30 Combat` opens as a conversation -- he laughs inside your head -- then `1001 Goto combat` over him, and `Nostrodomus Attack Preparation` fires |
| four seconds later | the spell timer starts, and he begins casting |
| every blow after the first | the relay only, guarded by a `the seer has laughed once` checker, so the taunt does not repeat |
| when he dies | `30 Combat Nostradamus Defeated`, then vanilla's `Portal Relay` as before |

**`10 Nostradamus` answers a question nobody asked.** *"To the Hujark, I am a prophet, a power they
revere and worship. But I was not always like this."* Its replies return to `5 questions` like every
other answer of his, and nothing pointed at it; `5 questions` asks *"What are you?"* and routes to
`35 Prophet`, which is the answer about the spirit he merged with -- a different question. Both of his
hubs now also ask **"The Hujark call you their Prophet. What are you to them?"**

**Two of his links were spelled in the wrong case** -- `70 dangers` offering *"Tell me about the
Betrayer."* to `70 betrayer` and *"Tell me about the serpent."* to `100 dragon prophecy`, against nodes
named `70 Betrayer` and `100 Dragon Prophecy`. Part names resolve case-insensitively in this engine and
node IDs almost certainly do too, so these probably always worked; both are exact now, which costs
nothing and repairs two replies and the Dragon Prophecy if they did not.

**Where act 5's unreachable dialogue stands after this tier.** Case-folded, the act had twenty nodes
that nothing reached and nothing opened. Tier 3 opened three, tier 4 opens four, and what is left is:

| still unreachable | why, and what it would take |
|---|---|
| 12 nodes of `Losing side wins a fight` | the two escalation series and both *"thank you for your help"* lines need an **allied speaker per map**, and the paired-skirmish cast they were written for (`English3`, `Hujark3a`, `Hujark3b`) is created by nothing |
| 3 nodes of `Generic Hujark` | `4 sneak`, `5 barter`, `6 No` are **byte-identical copies** of the Frightened Apprentice's lines in a tree that shares his node IDs. A copy-paste artefact, not content |
| `40 Ingame Movie Opening Line` | belongs to a cinematic that is not in the retail build |

### Tier 5 - forty-three traps, and the two maps that said nothing (built)

**There is no door on any of act 5's ten maps**, so there was never anything to lock -- and there was
never a trap either, on a reply or on a trigger, anywhere in the act. Ten maps of caves and tunnels
with nothing in them for a thief to do. The Crypt got 67 trap checks in 0.16.0 and they changed a
thief's route through it completely.

**The trap is not composed from scratch.** It is the Crypt's own trap part, read back out of
`10 Garrison Camp` and edited -- a `CRenderablePolygon` carrying two activities:

| activity | what it does |
|---|---|
| `CTouchingPolygonTriggerAI`, `Trigger Only Once=1` | the effect, then damage scaled by the player's Mojo: 30-45 above 30, 22-35 above 20, 15-25 below that |
| `CAISecretReveal`, `Skill Adjustment=15` | a thief spots it (`Common Objects and Scripts/Found Trap`), which adds a `GetCloseThen Disarm Trap` specifier checking `Skills/Thieving/Lockpick Disarm Traps` against 50 -- pass and it is disarmed for 250 XP, fail and *"The mechanism is beyond you"* |

Three flavours, each with an effect model that actually exists and a damage type that matches it: a
**fire trap** (`Fire Circle Medium`), a **shaman ward** that discharges electricity
(`Electrical Burst Med`), and a **cold snare** (`Ice Ring`). The Crypt's numbers were retiered upward
for an act this late -- and positionally rather than by value, because `20` appears three times in the
template and a value-based edit silently moved the wrong constants. The first cut of this tier did
exactly that and shipped traps weaker than its own table claimed; it was reverted.

| map | traps | | map | traps |
|---|---|---|---|---|
| 01 Heart Entrance | 5 | | 06 Cave 1 | 3 |
| 02 Clan of the Hand A | 6 | | 07 Cave 2 | 4 |
| 03 Tourniquet of Pain | 5 | | 08 Cave 3 | 5 |
| 04 Clan of the Skull B | 5 | | 09 Cave 4 | 5 |
| 05 Nostrodomus Demesne | 2 | | 10 Cave 5 | 3 |
| | | | **total** | **43** |

**Every trap sits on ground the shipped game already spawns a monster on** -- the same trick the
English twins used in tier 3b. No trap is placed on a guess about what is walkable.

### The two maps that said nothing

`07 Cave 2` and `09 Cave 4` are dead-end caves off the main line: 393 and 458 level parts, forty-four
and fifty-two live spawners, one drop of loot each, and between them not one conversation, balloon or
dialogue tree. They were **the only two maps in the act with no voice of any kind**, and now there are
none.

Two lines each. The arrival line is fired from the spawn points rather than a polygon, so there is no
geometry to get wrong, and a checker holds it after the first time:

- **Cave 2**: *"The passage narrows and keeps narrowing. Snakebreed have nested in the cracks of it,
  and the Hujark have left their own dead where they fell rather than come this far in to fetch them."*
- **Cave 4**: *"A store cave, or it was. The shelves cut into the rock have been swept clean, the
  sweepings are underfoot, and something has been breeding in the dark at the back of it."*

And one at the loot each cave was built around -- on Cave 4 that is the part vanilla itself named
`Hidden Treasure`: *"Somebody hid this and did not come back for it. The dust on it is the same dust
as on everything else, which means nobody has looked here in a very long time."*

### Tier 6 - the act reads the player (built)

Act 5 asked about faction thirteen times and karma three, and about nothing else whatsoever: no race,
no Speech, no Barter, no magic school, no perk, no spirit, no gender. Two of its voices were sitting
directly on top of the questions they should have been asking.

**Nostradamus is a man joined with a spirit.** The node is his, word for word:

> I am what a spirit and a man become when a divide is breached and the two are made whole.

The player is that sentence with the words in a worse order -- a spirit put into them at a sword's
point -- and in the shipped game he never once notices. Three `CHasSpirit` replies, the act's first,
and he answers each as the only other person in the game who has done what the player had done to
them:

- **Ancestral**: *"What I carry chose me, and I chose it, and we are becoming one thing. What you carry
  was put into you at a sword's point and is still a guest in a house it does not own. You are two,
  coinspinner, and you will be two until one of you gives way. I cannot see which."*
- **Beastial**: *"It cannot agree to anything, which means it cannot betray you either, and there is a
  safety in that which I do not have -- mine argues. When your own sight comes, it will arrive as
  hunger rather than as pictures, and you will have to learn to read hunger."*
- **Demonic**: *"It looked out of you as you entered, and it knows what I am becoming, and does not
  care for it... Whether what results is you or it is not decided by either of you. It is decided by
  which of you is the more patient."*

**The Hujark are outsiders driven out for being touched by magic** -- Huko's own words at `40 people`.
A Feralkin, Sylvant or Demokin Scion has heard those words in whatever town their own people were
made to leave; a Human has not. Four race-gated replies, the act's first, and two answers:

- the driven-out: *"Then you have heard the same words we heard... The Prophet took us in when no one
  else would have us. If you have come to take him from the people who took you in, I will not say the
  rest of that out loud."*
- the Human: *"Your face is one they let through their gates, and you have never had to explain it to a
  man with a spear. I say that without envy. It means you came down here by choosing to, which is worth
  more than being driven."*

**And Huko is a general deciding whether to believe a stranger**, which is what `10 explanation` is
for. Two karma gates on the same cans Brother Michel's five use: above 1300 he finds he believes you
and says so with his hand coming off the hilt; at 700 or below, *"I see hands, and yours have been
busy. It makes no difference to me whose side that puts you on. Only which side you say."*

Every new node routes back into vanilla's own choice -- help the Prophet, hear more, or fight, with the
Inquisitor's variant where vanilla has one -- so none of this adds a way through the act that the act
did not already have.

**The census, on the same basis before and after:**

| gate | vanilla | now |
|---|---|---|
| faction | 13 | 21 |
| karma | 3 | 5 |
| attribute | 3 | 3 |
| **race** | **0** | **4** |
| **spirit** | **0** | **3** |
| replies in the act's trees | 149 | 185 |

Still zero: gender, Barter, perk, magic school, and Speech. The act has no merchant and no lock, which
covers Barter; the rest are open.

### Tier 7 - he ain't no Lazarus, except he was (built)

`06 Cave 1` carries a relay named `You killed the apprentice`, `Active=1`, fired by nothing, and its
own comment is the specification:

> If you kill the apprentice after he's activated his generator on the next map, this deactivates it.
> He ain't no Lazarus!

The Frightened Apprentice runs from the player through a five-step scripted series on Cave 1 and
reappears on `02 Clan of the Hand A` from an `apprentice generator` waiting there. Kill him in the cave
and **nothing notices** -- his generator installs no destroyed script -- so he is standing on the next
map, alive, having died in front of the player a minute earlier. The relay that deletes the second copy
has been there the whole time with nobody to call it.

One `CSetDestroyedScriptActionAction` on the generator that produced him, the same hook the seer got in
tier 4 and Huko has carried all along.

### Tier 7b - the rest of the summoning the act documented on itself (built)

Tier 2 left two pieces open, and both were the act's own checkers going unread.

**Three caves had the apparatus and nothing to trigger it.** `08 Cave 3`, `09 Cave 4` and `10 Cave 5`
each carry `hujark summoning enabled` and a `Snakebreed Clone Generator`, and none has an anonymous
shield-helmet swordsman -- they field shamans, and a shaman calling a serpent is a better fit than a
swordsman doing it. Four generators between them now do, on the same gate as tier 2b, so Sahar's mark
silences these too. `06 Cave 1` is left alone: it fields no Hujark at all.

**And `snakebreed summoning enabled` had never been read once.** It sits on `02 Clan of the Hand A`
and `04 Clan of the Skull B`, `Active=1`, beside a `Snakebreed Summoner Clone Generator` that nothing
clones -- and that generator is not a snake. Across four `Max Party Mojo` tiers it fields a Mongol
Goblin Archer Super, an Ogre1 Ranged, a Bear Super, a Vodyanoi Cave Super, a Mongol Goblin Shaman
Super, a Wolf Black Super, a Festering Undead, a Desert Beast, a Ghoul Male Large Super and, at the
top of the table, a **Rock Titan**. The `Snakebreed Summoner` that fields it was already on both maps.

So there are two tiers of summoning in the act now, and they are not the same thing:

| tier | who | at | calls | stopped by Sahar's ring |
|---|---|---|---|---|
| snakes | shield-helmet swordsmen and cave shamans, 35 generators | 50% health | one `Snakebreed Venom`, scaled by party mojo | **yes** |
| summoners | `Snakebreed Summoner`, 7 generators | 25% health | whatever the four-tier table gives, up to a Rock Titan | **no** |

**The ring is not a blanket off-switch**, and that is the point of the distinction. The serpents know
Sahar's mark. A rock titan does not.

### Tier 8 - the commentary finally has somebody to say it (built)

`Losing side wins a fight` is seventeen nodes of running narration from whichever side the player
joined, and vanilla opened **two** of them. Tier 3 opened three more at the seer's door, where a named
shaman and guard already existed. The remaining twelve needed the one thing the act has never had: an
**allied entity, present and named, on each map**. The paired-skirmish cast they were written for --
`English3`, `Hujark3a`, `Hujark3b` -- is created by nothing anywhere in the game.

Tier 3b had already supplied the bodies. On the Hujark path every Hujark generator's spawn is pacified
and fights the English instead of the player; on the English path the ninety-nine twins exist and are
simply not switched on. What was missing was a name to hang a balloon on, and a reason for one of each
side to be an escort rather than an enemy.

Six maps now carry two escorts each, neither of which the player ever fights:

| escort | copied from | raised by | targets |
|---|---|---|---|
| `Hujark voice Generator` | a live Hujark generator on that map | `Activate English generators` -- vanilla's own name for the Hujark-path call | `Scripted Custom 2`, the English |
| `English voice Generator` | one of that map's English twins | `Activate Hujark generators` -- vanilla's name for the English-path call, which **existed on no map in the game** until now | `Scripted Custom 1`, the Hujark |

Both ship `Active=0`, so a player who never commits sees neither. Six of vanilla's nine
`Activate Hujark generators` calls now land; the other three are maps with no English twin to raise.

**And the line is the stage of the advance that map represents**, spoken a second and a half after the
player lands, once, by whichever escort belongs to the side they took:

| map | Hujark path | English path |
|---|---|---|
| 02 Clan of the Hand A | *"Thank you for your help! You must get to the Seer quickly."* | *"Thank you for your help! We will secure this area. You keep moving."* |
| 03 Tourniquet of Pain | *"You must get to the Seer before the Druids do!"* | *"We must bring the savages to their knees!"* |
| 04 Clan of the Skull B | *"Stop the Druids before they reach the Seer!"* | *"We are breaking through their defenses!"* |
| 08 Cave 3 | *"The Druids have entered the caves. You must hurry!"* | *"Soon we will prevail!"* |
| 09 Cave 4 | *"Get to the Seer quickly! Time is running short."* | *"Death to the Hujark!"* |
| 10 Cave 5 | *"Protect the Seer! The Druids must be stoped!"* | *"Hurry! We have almost broken through."* |

`Losing side wins a fight` now has **no unopened node**, and crossing the act reads as an advance
rather than ten rooms of the same fight.

A corrective pass followed the audit: two of the six `Hujark voice` escorts still carried a bare
`Valid Targets=Player` inside the AI copied from their source generator. Their `After Action` sets
targets at spawn and would have overridden it, but a copy that still names the player is the sort of
leftover that bites two tiers later, so every `Valid Targets` line in an escort now agrees with its
side.

### Act 5's unreachable dialogue, closed out

Case-folded, the act had twenty nodes that nothing reached and nothing opened. What is left:

| | nodes | why |
|---|---|---|
| tier 3 opened | 3 | the seer's door |
| tier 4 opened | 4 | the seer's stranded answer and his combat lines |
| tier 8 opened | 12 | the commentary, both series and both thanks |
| **left** | **1** | `40 Ingame Movie Opening Line`, which belongs to a cinematic that is not in the retail build |

Plus the three `Generic Hujark` nodes that are byte-identical copies of the Frightened Apprentice's
lines in a tree that shares his node IDs -- a copy-paste artefact, not content, and correctly left
alone.

### Tier 9 - safe conduct, and a way to lose it (built)

Huko has always offered two doors -- help the Prophet, or fight him for it -- and every other piece of
this act hangs off which one the player takes. A Speech check at 75 buys a third, offered at all three
places he demands a side:

> I am not here for your Prophet and not here for the Druids. Let me pass and you will not see me
> again.

**The hollow version of this would have been an empty act**, and one map proves it: `03 Tourniquet of
Pain` has twenty Hujark-side generators and **no cave fauna at all**, so a genuinely peaceful path
would walk its middle map through a silent corridor. So neutrality is not peace. Huko can promise that
his own men will not touch the player; he cannot promise anything about the army currently storming his
caves, and he says so:

> My men will not touch you, because I will tell them not to, and that is the only thing in this cave I
> am able to promise you. The Druids are not mine to call off. And if you raise a hand to one of my
> people, the word will be in the next gallery before you are.

So the safe conduct raises the ninety-nine English generators from tier 3b exactly as the alliance
does -- and they were already built targeting `Player, Player Friend, Scripted Custom 1`, because to the
English a neutral is a body in the way. Three states now come out of two flags:

| path | Hujark | English | escort | in the journal |
|---|---|---|---|---|
| help the Prophet | stand aside | hunting you | a Hujark soldier, calling the advance | *Protect Nostradamus* |
| fight for the Lance | hunting you | off | an English soldier | *Defeat the Hujark defenders* |
| **safe conduct** | **stand aside** | **hunting you** | **none** | **nothing** |

The difference between the first and the third is that **nobody narrates for you**. Tier 8's commentary
tests the two side flags and a neutral holds neither, so the act goes quiet around you while remaining
extremely dangerous -- which is not the same thing as empty.

**The plumbing is one gate and two relays.** The pacify branch on 104 Hujark generators used to read
`sided with the Hujark`; it now reads `the Hujark let you live`, which the alliance and the safe conduct
both open. `Player buys safe passage` raises the English and calls off the Hujark on the Heart Entrance
and, through nine `COtherMapAction`s, on every other map. The commentary deliberately still reads the
old flag: an escort is for somebody who picked a side.

**And the deal is revocable.** All 104 pacified Hujark now carry a damaged script: raise a hand to one
and `Passage revoked` voids the arrangement here and, through nine more cross-map calls, everywhere --
so the next gallery already knows, exactly as Huko said. The struck man fights back, and every Hujark
that spawns from then on comes up hostile. This applies to the **alliance** path too, which it always
should have: side with Huko and then cut his men down and you have chosen again.

A corrective pass after the audit: the seer's door still read the alliance flag, so the shaman and
guard turned on a player Huko had personally guaranteed. They are his men and his word covers them, so
the door reads the same gate now -- and *"The Seer has been expecting you"* sits as well on a neutral as
on an ally, because being expected is the seer's whole business.

**Nostradamus notices.** A player carrying safe conduct can ask whether it shows in his visions:

> It shows. Everyone who has ever come down that passage arrived belonging to something, and the
> belonging is the first thing I see; it sits on a man like a coat. You came in wearing nothing, which
> is rarer than you know and worth less than you hope. A coin that refuses to be flipped is still a
> coin, coinspinner, and the hand will come for it anyway.

### Tier 10 - what a general refuses, and four things only a specialist can say (built)

**The Child Killer title costs the Hujark alliance.** The perk is a reputation rather than a secret --
vanilla reads it in the Gate District -- so Huko does not wait to be told, and he does not wait for the
player to speak either. Both of his talk hooks now branch on it: the `GetCloseThenTalk` specifier in his
template, and the `Trigger=First Time` transition that makes him cross the ground to meet you. A player
carrying the title never reaches `1 Conversation Start` at all.

> Stop there. <He has the sword up before you have finished walking.> I know what you are called. The
> word of it came down the valley a long way ahead of you, and there are children in these caves. You
> will not be helping us hold anything, at any price you care to name. Say what you actually want, and
> then be gone.

What remains open to that player is the **safe conduct** from tier 9 -- a man who wants you gone will
still take that deal -- and the fight. What is closed is the alliance, and it is closed properly: the
first cut of this tier let the refusal route to `30 Prophet`, which offers to help, so the refusal
leaked straight back into the thing being refused. All **fifteen** replies in his tree that reach
`50 help prophet` now carry `CExpressionNot` around the Child Killer check, on the shape
`Brambles.DialogTree` uses. One of the act's three routes closes on a title the player earned two acts
earlier.

**And four gates only one kind of character can open**, every one of them on a can or perk vanilla
already uses:

| gate | node | the line |
|---|---|---|
| `General Tribal Skills moreequal 80` | Huko, `48 your magic is ours` | *"You work it the way we work it -- out of the ground and out of the blood, not out of a licence and a shelf of books... Then I do not have to explain to you why the Druids want him."* |
| `General Divine Skills moreequal 80` | the seer, `51 the church would burn you` | *"By your doctrine I am the thing your order was founded to end, and by mine you are a man who was handed a lit torch and told which house to carry it to. We are both instruments, coinspinner. Mine at least asked me first."* |
| `General Thought Skills moreequal 80` | the seer, `52 what you are becoming` | *"You do not get a man with a spirit in him. You get a third thing, and the third thing remembers being both. Your schools will not write that down, because a scholar who writes it down has to consider doing it."* |
| `Perks/!Event Title Perks/Necromancer` | the seer, `53 the same trade` | *"You have put them into bodies that were not willing, that were not yours... The difference is not skill and it is certainly not mercy. It is that I asked."* |
| `Perks/!NPC or Event Given Perks/Stargazer` | the seer, `54 the stars you read` | *"The sky is a clock, astronomer. A clock can tell you when and it can never tell you what. I am telling you what. Be glad the sky is all you have -- the when is bearable."* |

Stargazer is worth singling out: it is checked in **exactly one place in the whole game**, Galileo's
solarium, and the game's own astrologer-prophet has never read it.

### Gender stays at zero in act 5, deliberately

There are no women in this act. Huko, Nostradamus, the Monk, the assassin and the apprentice are all
men, and the Hujark are written as an undifferentiated tribe. Gender worked in the Crypt because Jehanne
is the one character in the game's history for whom it is the whole story. Here it would mean inventing
a Hujark custom to manufacture a reader, which is worse than the gap. Left for act 7 or 8, where there
may be a real one.

### The act's gate census, finally

| gate | vanilla | now |
|---|---|---|
| faction | 13 | 21 |
| karma | 3 | 5 |
| race | 0 | 4 |
| spirit | 0 | 3 |
| magic school | 0 | 3 |
| perk | 0 | 3 |
| Speech | 0 | 4 |
| attribute | 3 | 3 |
| gender | 0 | 0 |

### Tiers, in the order they should be built

1. ~~**The general who never spawns, and the two quests behind him.**~~ **Built** -- see above.
2. ~~**The summoning.**~~ **Built** -- see above. Extending it to the lesser shamans, and wiring
   `snakebreed summoning enabled`, are still open.
3. ~~**The commentary.**~~ **Partly built** -- the English side's four missing barks and the three
   door lines are in; the other fourteen need an allied speaker per map, which needs the English
   army below. Also still open: whether attacking the anonymous Hujark should commit the player to
   the English, which is what `Player attacks any of the Hujark in this fight` is named for.
3b. ~~**The act's two armies.**~~ **Built** -- 99 English generator parts from the act's own unused
   roster, as a swap rather than an addition.
4. ~~**The seer's three stranded nodes.**~~ **Built** -- and they turned out to be a boss defence
   that was never switched on.
5. ~~**The two silent maps and the ten trapless ones.**~~ **Built** -- 43 traps, and neither map is
   silent any more. There is no door anywhere in the act, so locks were never available.
6. ~~**Reactivity.**~~ **Built** -- the seer reads the spirit you carry, and Huko reads your race and
   your reputation. Gender, perk, magic school and Speech are still untouched in this act.

## 0.16.0 - the Crypt

**Published.** Cut from `main` 2026-09-25, entirely unplayed. Surveyed 2026-09-24, ten tiers built 2026-09-24 and 2026-09-25. Tier 4 adds the project's third new map; tier 8 came out of measuring the other seven. `plan.md` has carried a Crypt design since the back-half
planning, including the new area; this survey measures the act as it actually stands and prices
that plan.

**The act.** Ten maps, 9 dialogue trees, 95 nodes, **194 player replies**, 4,206 level parts, and
one quest. Four of the ten maps are called "Misc Crypt" and hold no conversation at all.
`1 Crypt Entrance` is the only hub; `7 Doomed Plateau` is the densest map in the game.

### Tier 1 - the quest that was only a name (built)

`Release the Doomed Knights from their Torment` shipped with `Item Count=0` and was touched by
exactly one thing in the game: `02 Hamlet Burned`, which fails it if Montaillou burns. The act's
spine was a title in a journal. Everything it should be made of was already written and reachable,
so this tier is three journal entries and five hooks, with no new scenes.

| State | ID | Set by |
|---|---|---|
| The Templar dead are still holding the line two hundred years on, and their commander could use another sword | `CRY1KNGT` | `UndeadTemplar / 40 knight` (*"Excellent. We can use more swords. Find Jehanne"*) and `UndeadTemplar2 / 40 help`, each gaining one reply |
| The knights were cursed into undeath by a wish a Saracen made on their behalf, and only the efreet who granted it can undo it | `CRY2CURS` | the Spirit Council's *"I will see what I can do"* on `40 Pious Child` and `30 Efreet` -- the node where it asks, in as many words, that the curse be lifted |
| The lamp of Jah'roosh is in your hands. Word the wish carefully: the knights of this garrison are undead too | `CRY3LAMP` | a new reply on the Efreeti's `01 Conversation Start` and `10 efreeti`, *"&lt;Say nothing yet, and look at the lamp.&gt;"* |

**Completed** on `Efreeti / 100 save inga`, the wish that frees them -- its existing
`CMultipleActionsAction` gains the completion and a 2,500 XP award through a
`Doomed Knights XP.can` on the pattern this project already uses. **Failed** on the Spirit
Council's `1 Conversation Start Joan Dead`, the greeting it gives a player who killed Jehanne:
*"May you see the death of your children and your childrens' children..."* Two hundred years of
siege end either way, and now the journal says which.

The third state carries the act's sharpest warning into the interface, which is the point of
writing it there: *"all my enemies here would die"* is the other ungated wish, and the garrison is
tagged `Undead`.

**Two splice bugs Gate 0 caught before they shipped.** `UndeadTemplar2 / 40 help` is the last node
in its file, so appending a reply after the node put it after the tree's closing brace -- caught as
"missing closing brace". And the Efreeti insert produced a reply with no blank line before the next
one, which is the separator the parser needs -- caught by the check added in 0.15.0's tier 4. Both
were rebuilt through one last-node-safe helper.

### The war is placed, running, and has no result

Both armies exist and are already hostile to each other -- not through factions, which is why a
faction search misses them, but through scripted-combat categories. The necromancer's horde
carries `Categories to add=Scripted Custom 1` with `Valid Targets=Player,Scripted Custom 2`: it
fights the player **and** the Templars. The Templar dead carry `Scripted Custom 2` with
`Valid Targets=Scripted Custom 1`: they fight the horde and **never target the player**. Thirty-odd
horde generators are live across `2 Retreat of Souls` and `7 Doomed Plateau`.

What is missing is an outcome. Nothing anywhere records which side won, every generator in all ten
maps is `Repeat Every=0`, and the quest built to hold the result --
**`Release the Doomed Knights from their Torment`** -- has `Item Count=0`: **zero states**, touched
only by Montaillou's failure sweep when the town burns. Nothing in any dialogue in the game
mentions the Doomed Knights or the Retreat of Souls.

**And the staged battle around Jehanne never runs.** On `7 Doomed Plateau`, `Joan Skeleton
Generator` (whose category is `NonInteractiveSequence Actor,Scripted Custom 1`), `Joan Spirit1`,
`Joan Spirit2`, `Joan Spirit3`, `Ghoul Male attacking Joan bottom Generator`, `Ghoul Generator` and
`Zombie Skeleton Generator` are all **Active=0 with nothing anywhere activating them**. The
set-piece that would show the player what this place is was built and never switched on.

### Dead parts worth naming - corrected

**The first version of this table was mostly wrong, and the error is worth recording because it
is the fourth of its family.** A `Target Name=` may name **several parts, comma-separated**:

```
Action=CActivateAction
{
    Target Name=Ghoul Male attacking Joan bottom Generator, Joan Skeleton Generator
```

My sweep split activation targets on lines only, so every part activated as part of a list looked
unreferenced. That is how the Doomed Plateau set-piece came to be described here as "built and
switched off" when it runs: `MASTER NIS top` and `MASTER NIS bottom` are both Active=1, they
activate the Joan skeleton and ghoul generators through exactly such a list, and they are fired by
`Joan NIS Poly top` / `Joan NIS Poly bottom`, two live trigger polygons the player walks into. The
same error cleared `switch to trap ghouls`, `True Entrance`, the `Crypt18/19/20` ambush doors,
`secret door6`, `2nd Main door monster` and both assassin generators -- all of them live.

**`tools/deadparts.py` now does this sweep properly**, folding case, splitting comma lists, and
excluding clone prototypes and `CAISecretReveal` secrets. It prints candidates rather than
verdicts, because it still cannot tell whether the thing that activates a part is itself
reachable. Run against act 4 it reports 23 parts, of which 21 are developer `warp` markers, a
`ghoul clone generator` that appears once per map, two `tabview` debug parts and an `s48` action
AI. What survives as content:

| Part | Map | Note |
|---|---|---|
| `Joan Likes Player through dialog` | `7 Doomed Plateau` | the real defect -- tier 2, below |
| `Ghoul Generator`, `Zombie Skeleton Generator` | `7 Doomed Plateau` | two spare spawn points at the map's east edge with no categories set, most likely deliberate reserves; left alone |
| `Door1` | `2 Retreat of Souls` | a door nothing opens, with no ambush or checker behind it; left alone |

### Tier 2 - Jehanne never remembers being convinced (built)

`7 Doomed Plateau` chooses her greeting for a returning player by testing two checkers together:
`Joan Likes Player through dialog` **and** `Joan player spoken to Spirit Council`. The second is
set in two places. **The first is set nowhere in the game**, so the test can never pass:
`3 Return Dialogue Likes Player` -- *"You have returned"*, with its five civil replies including
*"Do you know where the efreet is?"* -- and the warm farewell `5 Goodbye Joan Likes You` are
unreachable, and a player who has just proved to her that she is cursed gets *"I warn you,
monster, leave this crypt with haste"* the next time they walk up to her.

The author marked the spot. The reply out of `140 speech convinces joan`, the node where she says
*"You could not have known that unless you *have* spoken with them! That means you speak the
truth..."*, carries `Action work in progress=(joan likes player)` and no action at all. Tier 2 is
that note wired: one `CActivateAction`, and the whole warm branch behind it opens.

**One thing deliberately not done.** The next node's reply *"I have come to lift your curse and
protect the Lance"* carries the note `(have quest from spirit)`, and with tier 1's quest written it
could now be gated on that state. It is left ungated: it is the reply that makes her raise the
blocking gate, and narrowing a progression route on the strength of a designer note is not worth
the risk when the alternatives are a Speech check and killing her.

### Tier 3 - placing the garrison (built)

**Nine barks, one used.** `UndeadTemplar` carries `100 Random Knight` through `180 Random Knight`
-- *"We are ever vigilant"*, *"We stand strong against the black tide"*, *"Fighting the undead
hordes is our task, even if it is unpleasant..."*, *"I would lay down my life to protect the
Lance!"* -- and `Adds Dialog knight beginning`, the relay that gives the knight his talk AI, held a
`CSeriesAction` of **one** balloon, `150 Random Knight`, with `When Done=Repeat Last Action`. So the
garrison had one line and repeated it forever. That series is now a `CRandomAction` over all nine,
which is what nodes named "Random Knight" were written for, and `CRandomAction` is a shipped class
the Calle Perdida uses.

**And the garrison was only ever met after the war was over.** `UndeadTemplar` appears on
`7 Doomed Plateau` and `9 Burial Chamber` and nowhere else. A player walks the Crypt Entrance, both
Retreats and four Misc Crypts first -- `2 Retreat of Souls` alone holds **873 spawns and not one
`Scripted Custom 2`** -- so the entire first half of the act is undead killing a player who has no
idea there are two sides down here, and the knights' *"Have you been sent to reinforce us?"* lands
only once the player is already at the plateau.

One knight is now posted forward, on the route in: `Undead Templar Dialog 1 Generator` cloned onto
`2 Retreat of Souls` as `Knight of the forward post`, at (3060, 2140) -- inside the spawn radius of
the nearest live horde generator, so the footing is ground the map already walks monsters across,
and the fiction is a man holding the corridor the player is coming down. He carries the garrison's
own `Scripted Custom 2` category and `Valid Targets=Scripted Custom 1`, so the horde fights him and
he never targets the player, and his talk interaction opens `01 Conversation Start` -- the challenge
that leads to *"Are you a Knight? Have you been sent to reinforce us?"* and, with tier 1, to the
quest.

**And he defends himself.** The clone's damaged script fired `Make Knights at Level Start attack`,
a relay that exists only on the plateau, so struck he would have stood there and been cut down.
His damaged script now does directly what that relay does: `CGoToCombatAction` on himself plus the
garrison's own `20 monster` line. Three references in the cloned After Action still point at
plateau-only names (`Joan is a companion`, `Joan leaves party and attacks player`) and are left
alone: both sit behind conditions that cannot be true on this map.

### What is written and unreachable

Only **one** reply-carrying orphan: `UndeadTemplar / 03 return dialogue` (3 replies). The rest of
the loss is at the placement layer, not the tree layer:

* `UndeadTemplar` has **nine `Random Knight` barks and the maps fire one of them.** Eight lines of
  garrison voice -- *"We are ever vigilant"*, *"We stand strong against the black tide"* -- never
  play.
* The friendly branch (`10 relic` *"Have you been sent to reinforce us?"*, `40 knight` *"We can use
  more swords. Find Jehanne, she can help you"*) is reachable by reply, but `UndeadTemplar` is
  placed **seven times in the whole act**, only on `7 Doomed Plateau` and `9 Burial Chamber`, so
  most players meet the hostile greeting and never learn there are two sides.
* Jehanne has 38 nodes and can be recruited (`600 Companion Continue Again`), can turn on the
  player (`601 Joan Leaves party and Attacks Player`), and has **race-specific** versions of the
  demand for the lance (human, feralkin, sylvant, demokin).

### 66 trap events, no trap checks

The act carries **66 `GetCloseThen Disarm Trap`** specifiers, and every one calls `Disarm Trap.can`
or `Disarm Trap on Chest.can`, which are pure action bundles: play a sound, delete the trap, print
"Disarmed Trap", award 75 XP. **No skill is consulted** -- a character with nothing in
`Lockpick Disarm Traps` disarms all 66 by clicking them. (An earlier draft of this survey said
they fire automatically on approach. They are `GetCloseThen ...` interactions, so the player
clicks and the character walks over: the point stands, but the mechanism is a click.) There are also 87 `CAISecretReveal`
activities and 8 named secret doors, and the environmental vocabulary is placed and barely used:
`Switch Barricade` x7, `last coffin protect wall` x13, `Center Trap Spike` x10, two corpse bombs, a
fire trap, `Switch for Joan Pillars`, and the pulley whose entire dialogue is *"&lt;You hear a faint
click from the north wall&gt;"*.

### Tier 5 - 66 traps that finally test something (built)

Each disarm interaction fired a `CMultipleActionsAction` that played a sound, deactivated the
trap's trigger polygon, removed the disarm option and paid 75 XP. No check, anywhere: a character
with nothing in `Lockpick Disarm Traps` cleared all 66 and collected **4,950 XP** for clicking on
them.

Every one of those 67 actions -- the 66 in vanilla plus the one trapped chest the new camp
inherited from its base map -- is now the **Succeed** branch of a `CConditionalAction` testing
`Skills/Thieving/Lockpick Disarm Traps` against 40, built on the shape `Gate District.zax` already
uses to test `Skills/Fighting/Ranged`, with `CVariableSkill` (20 vanilla maps) as the primitive.
Fail prints *"The mechanism is beyond you"* and leaves the trap armed, and `Trigger Only Once` goes
to 0 on these interactions so a character who comes back better at it may try again -- which the
vanilla value of 1 would have prevented.

**The shared cans are deliberately untouched.** `Common Objects and Scripts/Disarm Trap` and
`Disarm Trap on Chest` are invoked **241 times across every act in the game** -- Alamut 54, the
English Shrine 37, the Sewers 34, the Wilderness 24, and so on -- and they are only the sound, the
text and the XP; the actual disarming is the `CDeactivateAction` in each map. Turning all 241 into
skill checks is a whole-game balance decision, not part of one act's release, so the change is made
at the 67 Crypt sites and nowhere else.

**What this costs a non-thief**, stated plainly because it is a real balance change: a character
under 40 in that skill can no longer clear the Crypt's traps or collect their XP, and must route
around them or eat them. That is the intent -- the act had 66 trap events and no trap checks -- but
it is the first change in this project that takes something away from a build, and the threshold is
the one number here worth arguing about.

**Not done:** the other half of the survey's proposal, `Find Traps Secret Doors` deciding whether
the player *sees* a trap before it fires, and the re-laying of a disarmed trap to face the horde.
Both need the trap parts themselves reworked rather than their disarm interaction wrapped.

### What the act asks about the player

194 replies. Corrected for named requirements, which an earlier pass of this survey missed:

| gate | replies |
|---|---|
| quest / state / item | 24 |
| faction (Templar 5, Templar NOT 3, Inquisitor 3, Saladin 3, Wielder 3) | 17 |
| Speech (45, 65, 80) | 5 |
| attributes (IN 7+ x2) | 5 |
| race (human / feralkin / sylvant / demokin, all on Jehanne's lance demand) | 4 |
| karma, gender, perk, spirit, magic school, trap skill | **0** |

At 8.8% faction-gated it is the **most faction-aware act measured so far** -- Montaillou managed
2.4% and Toulouse 1.2%. What it never asks about is a perk, a spirit, a karma score, or any of the
three magic-school skills, which is notable because Brother Michel says the entrance was sealed by
*"Sorcerers from the Order of Saladin"* and that the seals *"are not impregnable -- they can be
broken"*, and the `General Divine/Thought/Tribal Skills moreequal 80` gates exist and are used in
exactly one composite expression in Barcelona.

### Tier 6 - the magic schools, and reading the dead (built)

**There are no seals.** The survey proposed the three magic-school gates for Brother Michel's
Saracen seals, and act 4 has **no part called a seal anywhere**: the way in is `Door opener for
Crypt`, a live relay that opens the door and activates the transition polygon. Michel's *"the seals
they devised are powerful, but they are not impregnable -- they can be broken"* is backstory, not an
obstacle, and inventing one would put the entrance to an act behind a skill check. So the magic
gates went where the magic actually is.

* **Thought 80 is a second key to a door the Efreeti's tree already has.** `211 true wish` -- the
  wish granted straight instead of twisted -- was reachable by IN 6 with Speech 95, or 80 from the
  return node, and a Thought-magic adept can now reach the same node by reading the wording of the
  Saracen's wish instead of talking the efreet round: *"The wording has a seam in it, and I can see
  it. Grant mine straight."* No new outcome, and no new node: a different key to the same door,
  which is the cheapest honest way to spend a skill.
* **Divine or Tribal 80 answers Michel** at `160 The Seals` and its Saladin variant, the only place
  the seals are discussed -- *"a seal like that is not a wall, it is a promise, and promises can be
  answered"* -- and he admits what the order has been praying about for forty years: they sealed the
  complex with borrowed desert magic because they had nothing of their own that would hold, and they
  hoped nobody who understood it would ever turn up.

**And the dead can be read.** `Necrosage` -- *"your morbid fascination with the countless corpses
you've left in your wake"* -- and the `Necromancer` title now get something out of four broken
coffins, one each on `2 Retreat of Souls`, `7 Doomed Plateau`, `8 Ante Chamber` and
`9 Burial Chamber` (`Dialog/The Dead`, 8 nodes). Anyone else sees bones and dust. A reader learns
that the corpse in the retreat **died twice** and fought for the other side the second time; that
the man on the plateau has been killed nine times in the same spot and the part of him that should
have moved on is wound through the rock; that the coffin in the antechamber was opened **from the
inside** and bears a mark older and cruder than the besieging necromancer's, which nobody in the act
mentions; and that the crypt's original tenants are untouched, because *"a wish only binds what it
was asked about, and these were not asked about."* That last one is the act's own fiction read back
to it, which is what the perk is for.

**Gate 0 caught a bad path of mine, again.** The magic-school cans are not at
`Dialog/Requirements/Skills/General X Skills moreequal 80` but under per-school folders --
`Skills/Magic Thought/General Thought Skills moreequal 80`, and likewise Divine and Tribal. All six
references were wrong on the first build and the resolver added in 0.15.0's review pass failed them
before they could ship, which is the second time that check has paid for itself.

### The Efreeti already is the war's control panel

Eight wishes across `01 Conversation Start` and `10 efreeti`, and the two that settle the war are
both `!None`: *"I wish to undo the curse laid upon Jehanne's soul and the souls of her fellow
knights"* -> `100 save inga` (*"The souls of these Templars have been freed"*) and *"I wish that
all my enemies here would die"*. The wish-for-a-wish needs IN 6+ with Speech 95 from the greeting
or 80 from the return node; `210 get lost` needs IN 7+. Free, ungated, and currently the outcome of
nothing the player did with the place.

### Tier 4 - the garrison's camp (built)

`Levels/4 Crypt/10 Garrison Camp.zax`, the third map this project has added to the game, and the
first built the way the survey said to build it: **a copy of the act's own smallest map.**
`3 Misc Crypt 1` is one of the four the act's writers left unnamed, unpopulated and silent -- 42
entities, no conversation, four live horde spawners -- and copying it means the tileset, the
`CPlasmaTileMap` floor, the lighting, the `VykaCrypt` textures and the waypointing are the Crypt's
own rather than authored from nothing. That is also why no `.frm16` or `.way` is needed, which
answers the question the survey left open: `4 Undercroft` shipped without them because its floor
lives in the map's own `Plasma Ground`, and so does this one.

What changed from the copy:

* `Partial File Name` and `Map Description` renamed; the four live horde spawners **stood down**,
  because the camp is behind the line, not on it. The two that were already inactive are left as
  they were.
* `Start Here` cloned into an arrival spawn, `From 1 Crypt Entrance`; the map's existing transition
  polygon retargeted from `2 Retreat of Souls` to `1 Crypt Entrance`, landing at a new
  `From 10 Garrison Camp` spawn there. So the camp has one way in and one way out, both using the
  act's own polygon-and-relocate idiom rather than the inactive developer `warp` parts.
* On `1 Crypt Entrance`, a stairwell -- `To Maps/StairWell One/StairWell1 F`, a model the Crypt
  already places, with the sequence it already uses -- stands beside the sealed shrine door, inside
  the walk polygon the player must cross to reach that door, with the transition polygon on it.
* **Three of the garrison muster there**, cloned from `Undead Templar Dialog 1 Generator`: a sentry
  on `01 Conversation Start`, so the act's *"Are you a Knight? Have you been sent to reinforce
  us?"* finally lands somewhere a player will reach early, and two who speak for the camp. All
  three carry `Scripted Custom 2` and `Valid Targets=Scripted Custom 1`, and all three defend
  themselves the way tier 3's forward knight does.

**And the camp has its own voices** (`Dialog/Garrison Camp`, 10 nodes, 21 replies -- the one piece
of substantial new writing in this tier). The knight at the fire has counted: *"Two hundred and
eleven years. I keep the count because somebody must, and because the elders cannot and Jehanne
will not."* He is the one who says out loud what the act never does -- *"we are not besieged. We
are the siege. Neither side can finish, so both of us keep count instead"* -- and he would rather
be a knight than a corpse, so he says knight. The one on the wall has refused to count, holds
because he was told to hold and has not been relieved, and *"whatever else is true about me can
wait for the man who comes with the order."* Four of the tree's replies read tier 1's quest states,
so the camp knows how far the player has got, and one reads `Joan player spoken to Spirit Council`,
after which the man at the fire will admit that the voices have gone quiet on her -- *"Do not tell
her I said it."*

### The new area: the ghost garrison's camp

`plan.md` settled this and the survey supports it: the Crypt is already a war camp and the game
never shows it. `UndeadTemplar` 14 nodes, `UndeadTemplar2` 5, Jehanne 38, the Spirit Council 10 and
the Efreeti 10 -- roughly 77 nodes of written garrison against an act whose maps average 34
reachable nodes -- and no muster point anywhere.

**The precedent is established twice.** The project has already shipped two maps that vanilla does
not have: `Temple Ilk Store Room` (0.5) at 16 parts and 24 KB, with a rendered `.frm16` and a
`.way` waypoint graph in `Cache/`, linked from Temple District by a single `New Map Name`; and
`4 Undercroft` (0.11.0) at 130 parts and 117 KB, linked from the Druid Council, which shipped
**without** cache files. So the cost of the camp is known: one `.zax` built from the Crypt's own
tileset, one arrival spawn, one `New Map Name` transition on `1 Crypt Entrance` or
`7 Doomed Plateau`, and a decision about whether it needs the `.frm16`/`.way` pair -- the two
shipped maps disagree, and that question should be settled against the Undercroft before building.

### Tiers, in the order they should be built

1. **Write the quest.** `Release the Doomed Knights from their Torment` exists with zero states
   against content that is entirely in place: Michel sets it, the garrison confirms it, Jehanne
   carries it, the Efreeti resolves it. Highest value in the act, no new writing.
2. **The checker behind Jehanne's warm greeting** -- the one genuine dead part in the act, and
   the only survivor of what this tier was originally scoped to be. Built.
3. **Place the garrison.** Built: nine barks instead of one, and a knight posted forward on
   `2 Retreat of Souls`.
4. **The camp.** Built as `10 Garrison Camp`. Jehanne stays on the plateau, where she is placed
   with 38 nodes and a companion flow: moving her would break more than it gained, and the camp
   sends the player to her instead.
5. **Give the 66 traps a skill.** Built, at `Lockpick Disarm Traps` 40. Seeing a trap before it
   fires, and re-laying one to face the horde, are still open.
6. **The seals, and reading the dead.** Built, with the seals relocated: there is no seal in the
   act to gate, so Thought 80 became a second key to the Efreeti's true wish and Divine or Tribal
   80 answers Michel instead.
7. **What each order actually means here.** Built: six claimants, six answers, and the vanilla
   dead link the warm greeting was hiding.

### Did it break up the monotony? The measurement, and what it changed

After tier 7 the act was measured per map rather than asserted about, counting live spawners
against everything that is not combat. The answer was **at the ends, yes; in the middle, no**:

| map | live spawners | conversations | balloons | trees | skill checks |
|---|---|---|---|---|---|
| 1 Crypt Entrance | 6 | - | - | 3 | - |
| 2 Retreat of Souls Entry | 1 | 1 | 1 | 1 | 0 -> 1 |
| 2 Retreat of Souls | 56 -> 57 | **0 -> 1** | 5 -> 8 | 4 -> 6 | 0 -> 20 |
| 3 Misc Crypt 1 | 4 | 0 | **0 -> 2** | 0 -> 1 | 0 -> 1 |
| 4 Misc Crypt 2 | 17 | 0 | **0 -> 2** | 0 -> 1 | 0 -> 5 |
| 5 Misc Crypt 3 | 17 | 0 | **0 -> 2** | 0 -> 1 | 0 -> 6 |
| 6 Misc Crypt 4 | 1 | 0 | **0 -> 2** | 0 -> 1 | 0 -> 2 |
| 7 Doomed Plateau | 112 | 6 | 12 -> 22 | 4 -> 5 | 0 -> 15 |
| 8 Ante Chamber | 34 | 0 | 1 -> 3 | 1 -> 2 | 0 -> 5 |
| 9 Burial Chamber | 21 | 1 | 3 -> 5 | 4 -> 5 | 0 -> 11 |
| 10 Garrison Camp | *new: 3* | *new: 3* | *new: 3* | *new: 2* | *new: 1* |
| **act total** | 269 -> 273 | 8 -> 12 | **22 -> 50** | 17 -> 28 | **0 -> 67** |

The bold column in the Misc Crypt rows is tier 8. Before it, those four maps held **zero
conversations, zero balloons and zero dialogue trees between them** -- the act had five maps with no
voice at all, and still had five after seven tiers of work. It has **one** now, and that one is the
Crypt Entrance, whose three conversations are opened by relays rather than by talk interactions, so
the metric undercounts it.

Two things the measurement said that tier 8 deliberately did **not** fix. Live spawners went 269 ->
273: this release added four knights and thinned nothing, and 112 live spawners on the Doomed
Plateau remain the engine of the grind -- thinning was considered and rejected in favour of making
the place more interesting. And the 67 skill checks transform a thief's route through the act while
giving a fighter nothing but a loss, so how much less monotonous the act feels still depends on the
build.

### The gate census, and the two tiers it asked for

Tier 8 measured combat against everything that is not combat. This measured the other axis: of
the act's 281 player replies, which ones the game looks at the *character* to decide. Every gate
the engine offers, counted across all twelve act-4 trees:

| gate | after tier 8 | after tier 10 |
|---|---|---|
| faction | 26 | 26 |
| quest state / item | 29 | 29 |
| attribute | 8 | 8 |
| perk | 5 | 5 |
| Speech | 5 | 5 |
| race | 4 | 4 |
| war tide | 3 | 3 |
| magic school | 2 | 2 |
| **spirit** | **0** | **3** |
| **karma** | **0** | **2** |
| **gender** | **0** | **2** |
| replies in the act | 281 | 305 |

Tier 5's 67 trap and lockpick checks are all on map triggers -- walking into a thing -- so a
thief's route through the act changed, but no *conversation* in the act knew a skill existed and
none knew what the player was.

Two things the census said that were checked and turned out not to be defects. The Crypt's
assassin already recognises Sahar's mark, on a reply gated on the `Sahar Ring` this project added
in 0.11.0, so act 4 does read act 2. And the three companions who can be carried this far --
Darsh, Cervantes and Cortes -- are not mute at the Crypt Entrance: vanilla gives each of them a
scripted farewell there (`10001 Darsh leaving for good`, `1500 cervantes leaves party`,
`800 cortes leaves MALE pc`), fired by relays on `1 Crypt Entrance`.

### Tier 9 - the companion nobody hears (built)

Jehanne can be recruited on the Doomed Plateau, and vanilla wrote her four companion nodes. One
of them has ever been reachable.

| node | vanilla state | now |
|---|---|---|
| `600 Companion Continue Again` | opened by `Switch Joan of Arc interactions specifier for companion mode` | unchanged |
| `600 Companion Wait` | answers the reply *"No, wait here for my return"*, which had `Go to node ID=` blank | that reply now reaches it, and it has an exit of its own so the conversation can close |
| `600 Companion Banter General` | *"Let us cleanse this place of evil."* Fired by **no map in the game** | a ninth action on the companion-mode switch: she says it over her own head the moment she joins |
| `600 Companion Quest Done Relic Safe` | *"the relic is safe at last. I may finally...rest"* Fired by no map | a polygon at the Lance's plinth in the Burial Chamber, on its **exit** action, so it lands when the player walks away carrying it with her beside them -- once, guarded by a checker |

**And the garrison can tell who you brought.** In the Burial Chamber, four checks inside
`Undead Templar Generator` and `Undead Templar Dialog 2 Generator` fire
`Joan leaves party and attacks player` when the player attacks a garrison knight *while she is a
companion* -- her whole loyalty turning on whether you cut down the men she has held a door with
for two centuries. All four read `Joan is a companion`, a checker that is map-local, `Active=0`
on this map, and switched on only back on the plateau. So it has never once been true here: you
could kill her knights in front of her and she would keep following you.

The fix is vanilla's own idiom for a carried companion. `1 Crypt Entrance` asks whether Darsh,
Cervantes and Cortes came with you using `CIsAliveAction{Name To Check For=Darsh}` -- against the
companion's own name, with no local part of that name anywhere on the map. Her generator lives on
the plateau, so alive-in-the-Burial-Chamber means carried there, and the four checks now ask that.
The now-unreferenced vanilla checker part is left in place.

The Ante Chamber has the same `Joan leaves party and attacks player` relay and no caller for it,
and it stays that way on purpose: that map spawns ghouls and zombies, not garrison knights, so
there is nobody there for her to be betrayed over.

### Tier 10 - what the Council sees, and what she was tried for (built)

The Spirit Council's answer to *"Who do you think I am?"* was always about the player's soul --
*"that which has no soul, save one borrowed from another, which was taken from yet another at the
point of a sword"* -- and it said it in one voice to all three kinds of Scion. Now the player can
make it say which, on the act's first three `CHasSpirit` gates:

- **Ancestral**: *"A crowd stands where your soul should be, and every one of them is wearing your face... a thing you inherited cannot be put down. It also means that when this crypt asks you for something, it will be asking a creature that understands a debt."*
- **Beastial**: *"It does not trouble us. It troubles the bargain. What you carry cannot hold a promise in its head, and every wrong thing in this place began as a promise made carelessly by someone who could."*
- **Demonic**: *"The thing riding you was made by the same trade that made this crypt: a request granted exactly as it was worded. You, of all creatures walking, should be able to read a contract."*

**And the Council can see who it is begging.** Its plea at `40 Pious Child` now reads karma --
`Karma moreequal 1200` and `Karma equalless 800`, the act's first karma gates and the sixth and
seventh in the game after Brother Michel's five. Good: *"we have watched a great many armed
strangers cross that gallery without once seeing it... lift this, and it will be the largest thing
on the page."* Bad: *"We see it, and we are asking anyway... the dead do not get to be particular.
Do this one thing and we will not pretend it balances anything."*

**Jehanne introduces herself as a maiden who commanded an army, and was burned by a court for
it.** A female Scion has carried a sword through three acts to reach her, and act 4 had no gender
gate anywhere -- against 37 uses in `KnightsTemplarCanned` alone. Two replies on `10 jehanne`,
one subject, two ways in:

- **Female**: *"They burned you for wearing a man's armour. I have worn one since Barcelona."* -> *"Then you know the part of it that nobody writes down. They asked me about the armour for three days and about the English for one, and the word they wrote at the end of it was heresy. Wear more of it than I did when you go into the lower galleries, and do not wait to be thanked for the sight of you."*
- **Male**: *"What was the charge, in the end?"* -> *"Heresy, on paper. In the room it was the clothes... and nobody ever asked whether the army had held. I do not suppose you have ever been made to account for what you wear."*

### Tier 8 - four fronts, and a war with a result (built)

`plan.md` said what the Misc Crypts are for -- each is a **front** in a siege that is already being
fought, with 248 generators between them expressing nothing -- and that the vocabulary to fight it
with is already placed. Each corridor now has one lever that moves the war and one voice that says
what the corridor is:

| corridor | lever | what it does | tide |
|---|---|---|---|
| 3 Misc Crypt 1 | bar the rear door | closes the door the garrison falls back through, which had no name until this release | **+1** |
| 4 Misc Crypt 2 | bolt the stone door | shuts `Door1` behind the player, so the horde takes the long way round, which is where the knights are | **+1** |
| 5 Misc Crypt 3 | open the protect walls | opens all thirteen `last coffin protect wall` doors at once -- the way to the last coffin, and the way to it from the galleries | **-1** |
| 6 Misc Crypt 4 | the crypt-opening switch already there | vanilla's own `switch to open crypts` releases Crypt01 to 03 and their occupants; it now costs the garrison for doing it | **-1** |

**The tide** is `Game Scripting Variables/Crypt War Tide`, a derived character attribute on the
pattern vanilla uses for `DaVinci Tell player about Wielders` and this project uses for six flags of
its own -- written with `CAddCharacterModifierToCharacterAction` and `Allow Accumulation=1`, read with
`CVariableDerivedCharacterAttribute`. It rides on the character, so a lever thrown in one corridor is
legible two maps away.

**And it is legible**, which is the difference between a mechanic and bookkeeping. The knight at the
fire in the camp -- who has been counting for two hundred and eleven years -- reports the line three
ways: *"the corridors behind us are shut... the count moved for the first time since the seals
closed"*; or *"something is loose in the lower galleries that was not loose last week, and the room
where we kept our dead is open to the corridor now. I will not ask whether that was you"*; or the
stalemate, *"which is a stalemate and not a defence, and if you want to change that you will have to
change it out there rather than asking me about it in here."* Admit to the bad one and he will not
thank you for it, and tells you to look at Jehanne when you say it to her.

**The act's one real outcome now reads the war it ends.** The Efreeti's wish that frees the knights
pays out three ways: freed *in good order*, going out like lamps from the corridors the player shut
first, the last of them the man at the fire, who stops counting; freed *into a ruin*, where what is
left holding the corridors is the thing they were holding it against, and *"you have freed a garrison
out of a crypt you made worse, and both of those are true at once"*; or freed *from a stalemate*,
all at once, mid-step, and *"the siege does not end. It simply stops having two sides."*

### Tier 7 - six claimants, six answers (built)

**Her rejection is kept.** *"You lie! ... your spirit betrays you as the monster you are"* is the
right line for Jehanne -- she calls everything with a spirit in it a monster, and she is not
entirely wrong -- so nothing shipped was rewritten. What each order gets is the reply that presses
the point she has just refused to hear, and the two claims that had no answer node at all now have
one. Eleven new nodes on her, one on the Spirit Council.

* **Templar** (`43 the successor`, `44 what we became`) -- *"look at the shield properly,
  commander. It is your order's, and I am what is left of it."* She looks, and stops for the first
  time in the conversation: *"Two hundred years. Then the order stands, and there are still men who
  wear that, and somebody has been paying for masses I will never hear."* She still will not hand
  over the Lance -- she is not permitted and *"you would not thank me"* -- but she will not call him
  a liar again, and she asks what the order has become. Her verdict on her own two centuries:
  *"either faithfulness or the deepest stupidity in Christendom, and I have had two hundred years to
  decide and I have not."*
* **Inquisition** (`45 jurisdiction`, `46 the same enemy`) -- the writ over the unquiet dead, met
  with the one fact that disarms it: *"I was tried by a court of the Church in Rouen and burned by
  it, and I am told that the same Church has since decided it was mistaken."* Then the practical
  truth: judge away, and when you are finished the necromancer's army is still in the lower
  galleries.
* **Saladin** (`47 the lamp`, `48 undo it`) -- *"A Saracen of my order stood where I am standing and
  offered you his lamp. Ask me how that ended, commander -- you were there."* Everything in her face
  closes: *"He asked me to trust desert magic and I was desperate enough to say yes, and the thing
  in his lamp heard exactly what I said and gave me precisely that."* If his order sent him to undo
  it, she has waited a long time to hear somebody say so plainly.
* **Wielder** (`49 the binder`) -- the craft, named by somebody who practises it: *"It was not a
  curse. It was a contract, badly worded."* She turns the word over like a relic handed to her, and
  concludes it is worse than a curse, *"because a curse has a caster you can hunt."*
* **Dark Wielder** (`50 she was right`, `51 not your knights`) -- `Faction/Wielder IS` **with** the
  `Necromancer` title, which is the whole distinction, since Relican assigns `Wielder Mage` and
  Cedric `Wielder Conjurer` on the same rank ladder. He agrees with her accusation, and she is
  almost relieved: *"Everything that has come down that corridor for two hundred years has told me
  it was here to help, and you are the first one to stand there and admit what it is."* The army
  below would take him gladly -- *"it is short of officers and long of corpses"* -- and if he raises
  one of her knights she will find him wherever the Council has to carry her.
* **Goblin Champion** (`52 the khan`, `53 nothing to weigh`) -- `Faction/Goblin Horde IS` or the
  title. She says "the Horde" the way a soldier says a word she has not been briefed on: *"I
  commanded the army of France and I have never heard of your Khan, which means either he is very new
  or I have been down here a very long time, and I know which."* There is nothing in the claim for
  her to weigh, and that is the point -- the one act where the Khan's honours buy nothing. Told as
  much, she gives the act's best line about itself: names were what she had, *"maid, commander,
  witch, saint, whatever the year required -- and down here I am a corpse holding a door, and so are
  they."*
* **And the Spirit Council tells a Knight of Saladin whose magic it was** (`31 the Saracen was
  yours`): brave, the only man in the sanctum with a weapon that might work, and *"the man who did
  not read what he was signing"* -- which the voices have had two hundred years to decide is worse
  than treachery. *"If his order has sent another of its sons, let this one read."*

**And a vanilla dead link that tier 2 uncovered.** `3 Return Dialogue Likes Player`, the warm
greeting tier 2 made reachable, offers *"I have recovered the Bleeding Lance"* and points at
`200 have lance` -- **a node that does not exist in the shipped game.** Vanilla never had to answer
for it because the greeting was unreachable. It exists now (`200 have lance`, `201 what now`): she
does not reach for the Lance, tells the player to guard it *"not with a wall, because walls are what
we tried"*, and warns that the thing in the lamp grants exactly what it is given. That is the third
defect this release found by making something reachable, which is the pattern the project keeps
running into: repairs expose the next layer down.

**And it is worth checking whether `if dark wielder` should be promoted.** The only other marker
for Relican's path is a checker of that name on `Church Interior.zax`, set from Calle Perdida by a
same-map `COtherMapAction` -- Barcelona-local, so nothing outside act 1 can read it. The Necromancer
perk covers the Crypt, but if a later act needs "sided with Relican" distinct from "raises the
dead", the durable pattern this project already uses is a
`Derived Character Attributes/Game Scripting Variables/` flag, of which the mod ships six.


## 0.15.0 also - what the review pass found

**Read back over the nine tiers on 2026-09-24, and audited rather than re-read.** Four things
came out of it, three of them defects of mine in *earlier* releases.

### A canned expression path is not a requirement name, and three references had it wrong

A named `Requirement=` is resolved by the engine by name, searching the Requirements folders; a
`Canned Expression=` is an explicit path under `Resources/`. Writing a level-specific can's
*name* in the path form produces an expression that cannot evaluate true, silently, forever --
every branch behind it takes the Else. A resolver run over all 11,552 path-shaped references in
the mod found exactly three that do not resolve, all written by this project:

| Where | Wrote | Should be | Cost |
|---|---|---|---|
| `Calle Perdida.zax` x10 | `Dialog/Requirements/Cedric Player has defeated Relican` | `Levels/1 Barcelona/Dialog/Requirements/...` | ten gates in 0.12.0's Calle Perdida |
| `Gate District.zax` | `Dialog/Requirements/Requirements/Faction/Saladin Favored` | `Dialog/Requirements/Faction/Saladin IS` | Farshad's two "Welcome into the Order of Saladin" return greetings, the thing 0.3.0 restored him for |
| `LordJavier.DialogTree` x2 | `Dialog/Requirements/Javier requires initiate quest NOT begun` | `Levels/1 Barcelona/Dialog/Temple District/Requirements/...` | Javier's initiate gate |

The Farshad one is the worst of the three: the prefix was doubled *and* no `Saladin Favored`
can exists anywhere in the game, so his interaction has been falling through to the stranger's
opening for every player since 0.3.0 -- which is the exact bug shape 0.3.0 was written to fix.

**`validate.py` now resolves every path-shaped reference** -- `Canned Expression`,
`Canned Object`, `Perk To Check For`, the three inventory-item fields, `Dialog Tree File`,
`Entity` and `Quest` -- against the mod and vanilla, and fails if one points at nothing.
Verified by injecting a bad path and watching it fail. All three repairs above are in.

### Two of my own new hints pointed at a flask that was not there

Tier 7 gave Ephebos and the ogres lines that name the cul-de-sac where Mathuo's stash is, but
only Mathuo's own conversation fires `mercury relay`, which is what puts the flask in the rocks.
So both new hints sent the player to an empty dead end. Both replies now fire the relay, the
same way Mathuo's do.

### The Child Killer gate is honest but unprovable

Tereo's reply for a player carrying the **Child Killer** title is gated on a perk that
**nothing in the game awards** -- and vanilla checks that same perk eight times, on five of the
Gate District's spawn points, which means the designers expected it to exist on arrival and
almost certainly left it to the engine to award when a child dies. The reply is therefore in
exactly the position vanilla's own eight checks are in, and it is flagged in the test list
rather than quietly trusted: if it never appears after killing a child, the perk is dead and the
reply should be repointed at `Goblin Slayer` or `Merchant Slayer`, both of which are demonstrably
awarded. `Goblin Champion`, on the same node, is awarded by the Goblin Khan.

### What the audit confirmed

* Every one of the 47 nodes authored this session holds the prose rules: no node over 700
  characters, at most one stage direction each (19 across 47 nodes), ASCII throughout.
* All 232 mod files are byte-identical in the built `data.dat` except `Jafar` and
  `Merchant Lope`, which the playtest kit overrides by design, and every archive entry is stored
  uncompressed.
* No node carrying a player reply is unreachable anywhere in the Toulouse trees; every node
  added this session is reachable.
* `Barcelona Boy`, the template the new child in the pen uses, exists and carries
  `Races/NPCs/Generic Child` -- not one of the four templates whose `Race` dangles.

## 0.15.0 - Toulouse

**Published.** Cut from `main` 2026-09-24, entirely unplayed. Surveyed and built the same day, nine tiers. Tiers 1-6 finished the act's repairs; 7-9 are enrichment, added because the act turned out to be in good enough shape to deserve it. The sacked town in the
northeast corner of act 3, where a tribe of rock titans is camped in the ruins with a pen full
of human prisoners behind their guard. One map (`Levels/3 Montaillou/Titan Village.zax`, 959
level parts), 24 dialogue trees, **739 player replies**, and five quests: *Kill the Titans of
Toulouse*, *Recover Lucius' Mneme*, *Rescue the people of Toulouse*, *Destroy the shapeshifting
Daeva*, and the release of Inquisitor Darsh, who is a companion carried in from act 1.

0.14.0 already opened this map's biggest piece of cut content -- the negotiated ending, where
the titans are talked into hearing Lucius out and Lucius is talked into going back to them.
What was left is small, and all of it is broken wiring rather than unwritten content.

### Two false alarms, and what they cost

The first pass of this survey made two claims that were wrong, and they are recorded here
because both came from the same flaw in the audit rather than from the game.

**The mercury is obtainable.** I reported Titan Mercury unreachable because the proximity
trigger beside the rock that holds it (`triggers mercury relay`, Active=0, at 1760,2248) is
referenced nowhere in the game. But `mercury relay` is fired from dialogue instead: the reply
*"Where were you when the attack occurred?"* on `ToulouseMathuo / 10 Shapeshifter` carries
`CTriggerRelayAction{Relay Name=mercury relay}`, which swaps the plain rock (`no mercury rock`)
for the interactive one. The proximity trigger is an abandoned first attempt at the same thing.
Everything downstream of it -- Mathuo takes the mercury, the two titans talk each other into a
drink across six balloons, both walk off to their drinking spots, the prisoners escape, and the
pair panic in six more balloons while Poimaino tries to lure the player back into the empty pen
-- is live, map-driven and reachable.

**Thierry's treasure and the chickens are fine too.** The sweep that found them "dead"
compared part names to activation targets **case-sensitively**, and the designers were not
consistent: the reward is activated as `Thierry Reward` and named `thierry reward`, and
`eavesdrop relay` activates `Interrupted relay` while firing `interrupted relay`. Folding case
and excluding the two other idioms that hide activation -- generators are *cloned*
(`CCloneAction{Source Name=}`) rather than activated, and `CAISecretReveal` runs on the
engine's own secret mechanic -- takes the list of genuinely dead Toulouse parts from 28 to
four: the two flags below, the abandoned mercury trigger, one unused generator prototype
(`clone gen`), and thirteen developer warp markers. In particular `200 Montaillou Greeting`
already does exactly what I proposed as a repair: `COtherMapAction{CActivateAction{Target
Name=Thierry Reward}}`, the quest state, `COtherMapAction{CDeactivateAction{Target
Name=Thierry Reward hard}}` and the XP, all on one reply.

### Tier 1 - the two flags the act reads and never sets (built)

**The prisoners can be asked about Lucius.** `ToulouseAlexander` -- the tree for Thierry, who
speaks for the penned villagers -- gates the same reply on two nodes: *"The titans said this
town was harboring one of their kind, is that true?"* It needs `PC is told Toulouse was
harboring Lucius`, which is the name of a checker part sitting on the map. Lethos's reply
activates **`PC was told Toulouse was harboring Lucius`** -- one word off, a name that exists
nowhere in the game, and its own designer note says *"activate flag 1 PC was told Toulouse was
harboring Lucius"*, so the typo is in the note as well. Both copies of that activation (node
`22 Sacking Toulouse was appropriate` and its tainted twin) now target the part that exists,
and the same activation was added to every reply that reaches `50 Lucius is the fugitive` --
the node that actually says a titan was hidden here -- from nodes 20, 22, 22-tainted, 23 and
24, so the question opens on any path through the conversation rather than only the one that
scolds him. Behind it: `30 Lucius`, `32 Lucius 2` and `34 Alexander eaten`, the story of the
farmer who sheltered the fugitive on a secluded farm, loved a bottle, and was one of the first
bodies found half-eaten.

**The bluff at the pen can be told.** `ToulousePoimaino / 01 Greeting` carries two
Speech-gated replies -- *"It's okay, Iapetus said I could speak with the prisoners"* -- one to
`30 bluff SUCCESS` at Speech 95 or better and one to `30 bluff FAILURE` below it, both
requiring `PC has spoken to Iapetus`. Nothing in the game sets it, and unlike the Lucius flag
there is no typo twin: it has no setter at all. It now goes on the reply where the player asks
Iapetus for exactly the permission the bluff claims to have -- *"I want to talk to the
prisoners"* on `35 Humans not informed`, which he refuses in `37 Not allowed to talk to the
prisoners` (*"Who knows what you might incite them to do?"*). He says no, and then you go and
tell his guard he said yes. Poimaino keeps a `GetCloseThenTalk` interaction on `01 Greeting`
for as long as he is on duty, so the lie can be told on any later approach.

### Tier 2 - the guard's own bribe (built)

`40 Mercury SUCCESS` was the only reply-carrying orphan in the act: Poimaino taking the flask
himself rather than having it routed through Mathuo. *"Haw haw, you puny fleshlings. Can't
stand a little mercury, can you? ... Very well, I will do you a favor and take it off of
you."* The reply that should have reached it carries the spec in its own designer note --
*"Speech greater than/equal to 50, must have the mercury"* -- and shipped checking
`Inventory Items/Wine` and pointing at `40 Mercury FAILURE`, so the success text was
unreachable and the failure was the only outcome.

The reply is now gated as its note says, and split on Speech the way the bluff above it is:
`Quest Items/Titan Mercury` with Speech 50 or better reaches SUCCESS, and the same flask below
50 reaches FAILURE, whose text was already written for exactly that case and even points the
player at the route that does work (*"You'll have more luck with Mathuo than with me"*). The
SUCCESS node's blank reply got the action its note asks for -- *"take mercury away, have guard
go away somehow"*: remove the mercury, activate `Titans gone drinking`, and deactivate
`Poimaino kill box` and `trigger guard dialogue`. That is the same surrender the shipped
`30 bluff SUCCESS` performs, plus the drinking flag, which is what the map's own
`replace poimaino AI Interaction spec` polygon reads to decide that Poimaino is off duty and
should answer with `102 Drinking` (*"Leave me alone, runt"*) instead of his guard challenge.
Access to the pen is the whole prize: the rescue itself runs from Thierry's `100 See you in
Montaillou`, which fires `Prisoners escape`.

After both tiers the Toulouse trees have **no reply-carrying unreachable nodes left** (13
trees, 315 nodes, 38 unreachable, all of them map-fired balloons and barks).

### Tier 4 - the act reads the player back (built)

Nine replies and nine nodes across the three trees that had the least to say about who the
player is. Each one turns a subject the act already wrote on its head, rather than inventing a
new scene.

**Iapetus.** He explains that a Daeva feeds on a titan's magical aura, *"our souls"* -- and
says it to somebody carrying a bound spirit in the open. A spirit-bearer can now ask whether it
would feed on that as readily (`61 your spirit`): it would, and the hunter is also the bait.
A Feralkin or Sylvant can ask the question nine titans in a trampled cul-de-sac did not think
to ask -- what was on the ground (`66 tracks`) -- and gets the one piece of physical evidence
in the act, spoor by the rocks belonging to nothing that walks there. And his reward for the
hunt, *"a collection of gems that I think one of your persuasion would find quite pleasing"*,
can be haggled at Barter 40 into gems **and** coin (`77 haggle`): the bargain sets a new
checker, `bargained with Iapetus`, and `250 Killed the Daeva` pays 2,000 gold on top of the
three gems when it is set. That is the act's first Barter branch of any kind.

**Mathuo.** He says the Daeva took him while he was *"...unready..."*; Iapetus says he was
*"deep into the mercury"*. At Perception 7 the player can say so to his face (`11 drunk`): he
admits it, threatens to bury anyone who repeats it to Lethos, and names the cul-de-sac where he
keeps his stash. The reply also fires `mercury relay`, the same relay his polite branch fires,
so a sharp eye reaches the flask by the short road.

**Rhea.** Her history of the world turns on humans learning *"to bind spirits and wield
magic"* until magic grew a mind of its own and Utnapishtim drowned the world to be rid of it.
Three replies, one per spirit, let the player hold up what they are carrying: an Ancestral
spirit is *"the gentlest theft ... you keep your grandmother in a jar and call it
inheritance"*; a Beastial one is older than the player's line and she warns them to be careful
which of the two turns out to be the rider; a Demonic one makes her look up for the first time
-- *"that is the binding that pulled the sky down on Atlantis, and you wear it into a human
village like a travelling coat."* An Inquisitor can call Utnapishtim the first of his order and
the only one who finished the work (`31 the first inquisitor`), which she declines to take as a
compliment to either of them. And a Necromancer, hearing that the tribe cuts a crystal out of a
living elder so the dead keep speaking, can say what his own art calls that (`53 necromancer`):
she steps back, tells him the air around him is crowded, and draws the distinction that matters
to her -- titans carry their dead so the tribe stays itself, and he carries his so they will
fetch and dig.

These are the first uses of `CHasSpirit` in a dialogue requirement anywhere in the game --
vanilla uses it only inside map actions, wrapped in `CExpressionAction` -- so the bare
expression as a `Custom Requirement`, on the pattern of vanilla's three
`Custom Requirement=CHasPerkExpression` uses, is the one thing here that the automated gate
cannot prove. `Spirits/Demonic` is likewise extrapolated from the model name: vanilla's maps
only ever check Ancestral and Beastial. TO12 and TO13 exist to catch both.

**One defect this tier introduced and `validate.py` now catches.** The first build of the
Iapetus bargain put a blank line inside the `CIfAction` block, because the block helper was
handed an already-rendered child block and appended its own terminator after it. Vanilla has
zero blank lines inside a block in 10,915 replies, and the reply separator *is* a blank line,
so a stray one inside a Custom Action is exactly the shape of the bug that silently broke 47
replies between 0.2.0 and 0.5. It was reverted, rebuilt by passing the child as a field rather
than a string, and `validate.py` grew a check for it, verified by injecting the pattern and
watching it fail.

### Tier 5 - the gatekeeper and the elder (built)

**Tereo** is the titan the player meets first: the one whose name means *"guard"* because a
titan is called by his function until he earns the right to choose a name, and whose stated job
is to decide what the player's motives are. Fifty-four replies, one character gate. He gets
four.

The shipped tree lets a **Templar** announce himself at the gate (*"I've come to avenge the
deaths of the Knights Templar that guarded this town"*) and has nothing for the Church's own
investigator; an **Inquisitor** can now say so (`51 the Inquisition`), and Tereo -- who has been
set here to decide what a thing is before anyone kills it -- recognises the office as very
nearly his own.

His speech about earning a name (`24 A titan must earn his name`) now hears back from players
who have earned one. A **Child Killer** offers the title the game gave him: Tereo takes a step
back, says no titan would carry it, and asks not to be told the player's birth-name, since he
will remember them by the one they just gave him. A **Goblin Champion** offers a name given for
a deed by the people the deed was done for, which is exactly the custom Tereo believes in, and
he says he would not have expected it of goblins. These are the first uses anywhere in the game
of the title perks as *conversation*, rather than as a score the issuing faction reads back to
itself.

A **Feralkin, Sylvant or Demokin** can answer his puzzlement at humans being named at birth
(`23 named twice`) with the fact that their kind was named twice, the second time by the Church
-- and he draws the conclusion a titan would: a name chosen for you by creatures afraid of you
is no name at all, so go and earn another.

And his one visible lie -- *"perhaps our servants ate one, possibly two humans ... Strictly
mutton"* -- can be caught at Outwit 7 (`43 counting`): two, perhaps three, the ogres are not
watched as closely as he would watch them, he has said so to Iapetus, and an ogre's appetite is
low on an elder's list.

**Lethos** was already the most reactive tree in the act, with race-specific versions of the
oracle's prophecy, Speech-gated lies, Intelligence checks and a Barter split on the reward. He
gets the two things he lacked. The negotiated ending 0.14.0 opened has exactly one door, a
Speech 50 reply on `101 Lucius must die`; a **tainted** player now has a second, arguing from
the one position in the story that matches Memnos's -- *"your tribe decided what he is, and now
his duty is to die of it. Mine had that decided for us as well."* It lands on the same
`120 Nonviolent help` node, so nothing new had to be written to make the act's best content
reachable by a second kind of character. And a **Wielder**, hearing the mneme described as a
crystal in a living chest that holds what is left of the dead, can say that his order binds
spirits into stones and this is the same craft under another name (`141 a Wielder reads the
mneme`) -- which Lethos denies, with the distinction that matters to him: a bound spirit is put
in a box and made to work, and a mneme is what the tribe has been, kept where it cannot be
argued with.

### The empty canned requirements - 18 replies across the game, and one of them here

Reading Tereo turned up a defect class the project had not measured. A reply can be gated by a
named `Requirement=`, which resolves to a `.can` file holding one expression; **28 of the game's
609 requirement cans are empty shells** -- `Object=` with nothing after it -- and 18 replies are
gated on one.

Twelve of the empty ones sit under act 3, nine of them named for Titan Andre's schmooze and
outwit checks, and those nine are referenced by nothing at all: shells the designers created,
named, and never filled or used. Andre gates his real branches inline instead.

The one live case in this act is the Bishop of Pamiers. Two of his quest reports on
`02 Return Dialogue` -- *"I have found the witch you seek"*, which completes **Find the Witch
for the Inquisitor** and pays its XP, and *"I have spoken to the Mayor - he is a heretic and an
adulterer"* -- carry named requirements pointing at empty cans, and the first of them is
`Shephered Maury requires Titan to be alive`, which belongs to a different NPC and a different
quest entirely: a copy-paste from the neighbouring reply. Both replies also carry precise
`Custom Requirement` expressions that already encode the real condition, so the witch report's
named requirement is now `!None` and the Custom Requirement decides. Whether an empty can fails
open or closed cannot be settled without playing -- if it fails closed, this repairs a
main-quest report that could not be made; if it fails open, the change is a no-op that removes a
misfiled reference. Either way the Custom Requirement is strictly more precise than an empty
shell. The mayor report's named requirement (`Montaillou Inquisitor requires PC to have accepted
Mayors quest`) is left alone for now: unlike the witch report it is at least named for the thing
it gates, and its own Custom Requirement is the same shape, so it is the cleaner test case for
which way an empty can resolves. **MO31 and MO32 exist to answer that.**

**The other 17 replies are Guard Pablo's, and they are not a defect -- they are cut content.**
This is a correction to what the previous pass of this survey claimed. I reported the Temple
District gate as broken on every playthrough, having read the tree and not the spawner.
`Guard Pablo generator` on `Levels/1 Barcelona/Temple District.zax` is **Active=0 with no
reference anywhere in the game** -- nothing activates it, nothing clones it -- so Pablo never
appeared in the shipped game at all.

His tree is an earlier draft of a scene that shipped finished on somebody else: the Gate
District's `Temple Entrance Guard`, standing at the outside of the same gate, has the same node
IDs (`20 Temple District`, `100 Bribe`, `110 Welcome to Temple`, `55 Normal Denial`,
`60 Permission Granted`), the same 100-gold donation, and then everything the draft lacks --
Speech, Charisma and Barter gates on every branch, separate tainted variants for Sylvant,
Feralkin and Demokin, a Knight of Saladin branch, Barter discounts that bring the bribe down to
75 and then 50 gold, and `CTriggerRelayAction{Relay to open Temple District gate}` on both payoff
nodes, which is the part Pablo's draft never had: his `110 Welcome to Temple` and
`60 Permission Granted` carry no action at all, so paying him could never have opened anything.
The six empty cans are that draft's unfinished gates. Note also that the finished guard's own
`Player come through from Temple District` checker, which gates his entry replies, **is** Active=1
at map load and is deactivated only when the player arrives from the Temple District side or once
the gate opens -- so the live gate scene is intact, and there was never anything to repair there.

**What was built instead: Pablo restored as a greeter.** He is activated where the designers
placed him, at (1724, 2933), a few steps inside the gate the player has just been let through,
and his conversation is rebuilt from his own written lines in a new tree of his own
(`Dialog/Temple District/Guard Pablo`): his greeting, the rule he stands there to enforce, and
his explanation of what the Church means by tainted -- *"pointed teeth and ears, cat-like eyes,
and other mystical marks"* -- which is the only place in the game that spells out how a tainted
citizen is recognised on sight. The gate challenge is deliberately **not** restored: a second
challenge inside a gate the player has already passed would contradict the guard who passed
them, and an existence check cannot see across maps, so Pablo has no way to know they paid. A
Feralkin, Sylvant or Demokin gets the one piece of new writing in the restoration (`30 tainted`),
in which he looks at their face, declines to make anything of it, and asks that if an Inquisitor
should ask, the two of them have not spoken. His generator already carried a full skeleton AI and
the district's guard-reaction wiring (spellcast detection, the damaged-guard relay), so he
behaves exactly like the Temple Guard around him.

### Tier 6 - the warning the pen guard never gave (built)

`ToulousePoimaino / 100 Busted by the guard` -- *"Stop, you are entering the human pen. If you
insist on proceeding I'll have the pleasure of squashing you."* -- was fired by nothing in the
game. `Poimaino kill box` is Active=1 and triggered by players, and its Enter Action was two
`CSetTargetTypeAction`s: cross the line and both titans turn on you, in silence. The one line the
guard was written to say before he attacks was the one line he never said. It now plays from the
same Enter Action, ahead of the two switches.

### What a full sweep of the act found, and what it did not

The survey closed with three sweeps rather than one, because the first two each produced a
phantom.

**Dead level parts.** Folding case, and excluding parts that are cloned rather than activated and
secrets the engine switches on itself, the act has four genuinely dead parts left and all four are
deliberate: `triggers mercury relay` (the abandoned proximity trigger beside the flask, replaced
by the relay Mathuo's dialogue fires), `clone gen` (an unused generator prototype), and thirteen
developer `warp` markers. The two dead flags are fixed in tier 1.

**Unreachable dialogue.** All 13 Toulouse trees, 330 nodes: **no node carrying a player reply is
unreachable**, down from one at the start of the release. The 38 remaining unreachable nodes are
all balloons, and 36 of them are only "unreachable" to the tool, which reads the node named in a
map action but does not follow the `After Action` chains that fire the rest of a two-sided
exchange -- the six mercury bubbles, the six prisoners-escaped bubbles, the ogres' mutton
complaints, Rhea's lecture to Ephebos. Two were genuinely unfired: `100 Busted by the guard`,
which tier 6 wires, and `99 Tereo Bubble 2`, which is **not** a defect -- the middle line of the
Tereo-and-Ephebos exchange is fired from `ToulouseEphebos / Tereo Bubble 2`, and the copy in
Tereo's own tree is a duplicate nobody uses. That one was two minutes from being "fixed" before
the check that found the real copy.

**What is deliberately left.** After the bribe at the pen, Poimaino stops guarding but does not
walk away, exactly as he does after the shipped Speech bluff. Sending him off to
`Poimaino Drinking` (1280, 1707) the way the Mathuo route does needs a patrol authored on the
map and a save that has never entered Toulouse to test it, and it changes nothing the player
cannot already do. It is the only piece of Toulouse work left, and it is polish.

### Tier 7 - the people nobody could talk to (built)

**Ephebos.** The tribe's child is a live, talkable NPC whose entire player-facing content was one
line and no replies: *"I don't talk to disgusting fleshlings."* He now has a conversation built
out of what the map already says about him. He repeats Rhea's chain of being and gets it slightly
wrong (he asked where ogres go and Tereo laughed for a long time, so he does not think anybody
truly knows). He is one hundred and forty years old, has no name yet, intends to be Atlas, and has
stopped announcing it because Tereo told him nobody ever earned a name by announcing it -- which
is Tereo's tier 5 scene seen from the other side. If the player has overheard Rhea catching him at
Mathuo's mercury, he protests that it was one mouthful and gives away where the stash is. If the
player is carrying the flask, **he will take it** -- the third use for a single flask, against
Mathuo's route and Poimaino's bribe -- and pays for it with the one piece of intelligence a child
who is ignored all day would have: Baktron and Klao at the north end saying the elders are cowards.
And asked about the pen, he says Rhea calls them a herd, Tereo calls them unlucky people, and the
one who cries at night is smaller than he is, and he has not worked out what that means yet. Told
what it means, he asks the player not to tell him the plan first, so that he will not have lied to
anybody.

**The pen speaks.** The two prisoners were look-at descriptions with no replies, and the child's
description (`60 Villager Child 1`) was written and placed nowhere at all. The man explains what
the night visits are for -- the titans point at somebody, the ogres carry him over the fence as
bait, none has come back, *"so either it is a very clever thing or they are very poor fishermen.
My brother went out on Tuesday"* -- and says plainly that being afraid is not the same as being
cattle. The woman describes what came to the fence: her neighbour's shape, speaking with Grazide's
voice, three days after Grazide died; pressed, she remembers a deer at the treeline that did not
run when the ogres shouted. To a tainted player she explains that she looked away because the
player was the first thing at that fence in a week that was not hungry. And the child, who has
nothing to do in there but count, has counted the thing that matters: *"Another one brings him
silver to drink and then they both go away and nobody watches us at all. I have counted it four
times."* That is the mercury route, discoverable by talking to the people it is meant to free.

**The ogres.** Fifteen days of mutton and a bark that says *"Tasty people under thumb and we eat
sheep"*. A skin of wine buys the thing the titans never got out of them: the ogres carry the bait
to the treeline, nothing comes while they stand there, and when they retreat to the rocks in the
southeast it arrives -- a deer that walked on two legs when it thought they had gone. The ogre told
the guard-titan, and the guard-titan said ogres cannot count.

**And a way to pin the Daeva down.** Iapetus can now be asked whether anything holds a
shapeshifter in one shape, and answers with the old stories: a relic of Zarathustra's making
strips the shape off a Daeva and holds it in its own face. The Daeva's own tree already branches on
the Amulet of the Prophet in eight places, and `31 amulet speech` is written for exactly that
moment; until now nothing in the game told the player the connection existed.

### Tier 8 - the child, the ground, and Menoetius' own name (built)

Three map changes, two of them repairs:

* A third villager generator puts the written-and-unplaced child in the pen, using the
  `Barcelona Boy` template and his own node.
* `triggers mercury relay`, the designers' abandoned proximity trigger, sits in the cul-de-sac
  where the ogres and the woman in the pen both say the ground is trampled. It is renamed
  `spoor in the cul-de-sac`, switched on, and fires a one-time balloon about churned ground -- and
  at Perception 7 a second line: *"Deer slots, pressed deep, with no stride between them."* Three
  independent sources now point at the same dead end, and the ground confirms them.
* **`Monoetius Generator` names its titan `Rhea`.** Nothing on the map was called Menoetius, so
  the `Titan deactivator` that empties Toulouse at the end and the `Titan alarm relay` that turns
  the tribe on an attacker both missed him entirely, while their two `Rhea` entries hit whichever
  of the two identically-named titans the engine found first. His spawn now takes his own name.

### Tier 9 - the news that never reached Montaillou (built)

All three endings of Toulouse -- the mneme handed over, Memnos walked home on his own feet, or the
tribe killed to the last -- finish by firing
`COtherMapAction{CActivateAction{Target Name=titans are gone}}` at `01 Hamlet Exterior`. **No part
of that name exists on the Hamlet**, so the signal landed nowhere and the village the titans were
arguing about marching on never learned that they had gone. The checker is added, which switches on
wiring that has been sitting there since release, and three people who would care are given
something to say:

* **The mayor**, whose position rests on Andre's lie that he struck a deal with them, sits down
  without being invited to, asks *"Gone where, exactly -- home, or down the valley towards us?"*,
  and then asks the player to say nothing whatever about bargains. Pressing him goes to his own
  `951 Furious Mayor`.
* **Maury**, who has watched that road every morning since the smoke and counted his sheep twice a
  day, will still count them twice -- but the flock goes up to the high pasture this week and his
  son goes with him, *"and that is the first thing I have decided for myself since the spring."*
* **The Templar knights at the gate**, whose hand comes off the sword for the first time in the
  conversation: a rider goes to the commandery within the hour, and the Marshal will want to know
  how a thing that size leaves a valley without anyone seeing it go.

And **Baktron and Klao**, who stand at the north end arguing that the elders are cowards and get
caught at it (*"it seems we have a little spy"*), had no replies at all. The relay that plays their
argument now records that the player heard it, and each can be asked what he meant. Baktron, the
eager one, would take Montaillou between sunrise and noon and is unimpressed that the tribe is
waiting on an oracle and a runt in boots. Klao, who told him to be patient, is the more dangerous
answer: patience is not the same as agreement, and when the elders' plan fails the tribe will
remember who counselled waiting and who counselled running down a valley.

### How little Toulouse knows about the player

| gate | replies | share |
|---|---|---|
| quest / state / item | 162 | 21.9% |
| Speech | 26 | 3.5% |
| attributes | 21 | 2.8% |
| faction | 9 | 1.2% |
| race | 8 | 1.1% |
| Barter | 8 | 1.1% |
| **chosen perks** | **0** | |
| **which spirit you carry** | **0** | |
| **karma** | **0** | |
| **gender** | **0** | |

Toulouse tracks what you have *done* about as well as Montaillou does, and knows even less
about who you are: 1.2% of its replies read a faction against Montaillou's 2.4%, and not one
reply in the act reads a perk, a spirit, a karma score or the player's sex. **Iapetus is the
act's largest completely un-gated tree** -- 70 replies, none of them character-aware -- and he
is the elder who explains the daeva, the mercury, and why the humans are caged. Mathuo's 29
replies have none either. This is the place whose plot is a stolen crystal of collective
memory and a shapeshifting demon that feeds on titan magic, and it never asks what the player
carries or what the player is.

### What is left

3. **The chickens, reconsidered.** Not a defect: the three `Chicken Generator` parts are
   activated elsewhere. Nothing to do.
4. **The 27 other empty canned requirements.** Twelve are act 3 shells nothing references, six
   are Pablo's draft, and the rest sit on the Duke's demokin witness and two other Barcelona
   scenes. Each needs the same treatment the Bishop's got: check whether the NPC spawns and the
   reply is reachable *before* calling it a defect.
5. **Poimaino walks off** after the bribe (see above). The last Toulouse item, and polish.
6. **Andre's two betrayal variants** (`900`, `1002`), carried over from 0.14.0 and still
   needing the extortion path walked before they can be read honestly.

## 0.14.0 - Montaillou

**Published.** Cut from `main` 2026-09-24, entirely unplayed. Eight tiers built 2026-09-23 and 2026-09-24; Tier 6 was a read that ended in building nothing. Surveyed 2026-09-23. The second-largest act in the game after Barcelona and the
densest writing left in it: **17 maps, 51 dialogue trees, 17 quests, 1,087 dialogue nodes.** 140
of those nodes are unreachable and **49 of them carry replies** -- the largest block of authored,
unreachable branching the project has found anywhere, the Gate District included.

### What the act is

A Cathar village of a hundred souls with an Inquisitor sitting in it, questioning people one at a
time; a mayor standing between them and the worst of it; a witch in the woods who is a shadow
daeva; a fugitive rock titan hiding in the village under a human name while his own people camp
at Toulouse and demand him back; Nostradamus somewhere past it all; and the English coming.
Every one of those threads has live content and at least one cut branch.

### Tier 1 - the gate challenge (built 2026-09-23, unplayed)

`MontaillouGuard` has **13 unreachable nodes**, and three of them are a complete entry challenge
that nothing opens: `100 stop player` -- *"You there! What business do you have in Montaillou?"*
-- with **seven** replies, and its follow-ups `100 challenge` and `100 traveler`. The answers are
faction-aware in a way almost nothing else in the game is: the Inquisition, the Templars (with a
separate line for a woman -- *"Forgive me sister"*), the **Knights of Saladin** (*"You don't have
the look of a saracen, but if you serve that order, then you are an ally of the Templars"*), a
generic relic-hunter, a trader, and *"My business is my own"*, which gets you told the town is
under investigation for heresy and that arriving suspiciously is itself suspicious. The map opens
only `01 Conversation Start`, `03 Return Dialogue` and the knights' food banter.

This is the strongest single find in the act: it is the arrival scene, it is written, it reads
the four factions Fixt has spent five releases making real, and it is reachable by nothing.
`100 heresy` has **no text** -- one node would have to be ours.

**Built.** Reading it for the build answered why it was never wired: **three of its targets do
not exist.** `100 relics knights` (a node by that name is not in the tree -- there are only the
male and female variants), `100 relics` (nothing), and `100 heresy`, which is a node with an
empty `Text=`. A scripter wiring this scene would have hit a dead link on the first Templar
reply.

- The strip: the knights stand at (4943,1260) and (4971,1432), the road in arrives at
  (5451,1133), and a trip poly across it at x 5180-5320 fires `100 stop player` once, spoken by
  Knight 1, with a `CActionResetPointClickAI` so the player stops walking. It is guarded on
  Knight 1 being alive.
- The faction claims are gated as the rest of the tree gates its gendered lines: `Inquisitor IS`,
  `Templar IS` AND `Male IS` / `Female IS` (which also repairs the dangling `100 relics knights`
  by splitting it the way the two answer nodes already assume), and `Saladin IS`. The generic
  relic-hunter, the trader and *"My business is my own"* stay open to anyone.
- `100 challenge`'s *"My business is my own"* looped back to `100 challenge` itself; it now
  reaches `100 traveler`, which is where the heresy warning is.
- Two nodes are ours, and only because the game left holes where they go: `100 heresy` (the
  answer to *"Why is this town under investigation?"* -- Cathars, a man with a book, every soul
  answering one at a time) and `100 relics` (what a knight says to an unaffiliated relic-hunter).
- Having been stopped at the gate, a later click on either knight opens `03 Return Dialogue`
  instead of `01 Conversation Start`, so he does not demand your business twice.


### Tier 2 - the titans of Toulouse can be talked out of it (built 2026-09-23, unplayed)

`ToulouseLethos`, the titan envoy: `110 Good help` (kill Memnos, bring his mneme) and `130
Mercenary help` (kill him or trick him into coming) are live. **`120 Nonviolent help` -- "What do
you propose, small one?" -- and its two outcomes `121 Nonviolent success` and `122 Nonviolent
failure` are not.** Read them and the whole third route is there: the titans agree to let the
fugitive *make his case* for why he should outlive his office, or failing that to spare him if he
comes back of his own will -- and both then run into the same live reward menu (freedom for the
town, gold, magic, or both). What is missing is the player's proposal: `120`'s only live reply is
*"Nevermind, perhaps I will do it your way."*

The fugitive is Andre the Titan, the "human" in the village. So this is the peaceful end of the
act's central conflict, three nodes short.

**Built, both halves.** Andre's side is the four nodes flagged `[REMOVED FROM GAME]` in their
display text -- `960 Trick Lucius` and `965 convince Lucius`, each with a success and a failure.
The failures already pointed at live nodes; only the success had nowhere to go, which is what
the flag is about: Lethos's own live `130` still offers *"or trick him into coming here"*, so the
game shipped advertising a route whose ending was cut. The judgement recorded here is that the
writing was finished and the consequence was not, and the map next door had every piece of one.

- *Lethos.* His live `100 Return from Rhea` already lets you ask whether this can end without
  killing; `101 Lucius must die` is the refusal. Pressing him (Speech 50+) now reaches the
  written `120 Nonviolent help` -- *"What do you propose, small one?"* -- and the proposal itself
  splits on Outwit 8+ into the two written outcomes: `121`, where the tribe will hear Memnos out,
  and `122`, where they will spare him if he comes back of his own will. Both already ran into
  the live reward menu, so the negotiated route is paid at the same rates as the violent one.
- *Andre.* `950 Talk with Memnos` -- *"What do you propose to do?"* -- gains the two routes:
  persuade him (Speech 50+) and trick him with a truce that the titans have in fact agreed to
  (Outwit 8+), each falling to its written failure without the skill. The four removal markers
  are stripped from the node texts and nothing else in those nodes changed.
- *The ending.* The success reply now sets the mneme quest to its own shipped state `QYINZUKM`
  (*"You have decided to allow Lucius to live"*), completes *Kill the Titans of Toulouse*, pays
  the `pacifist` XP part the live mercy ending uses, fires `Lucius flees` to walk him out of
  Montaillou, and sets a checker on Titan Village through `COtherMapAction`.
- *And the titans go home.* With that checker set, Lethos's return greetings offer *"Memnos is
  coming back to you. He will speak for himself."* -> `502` (ours, one node): *"Coming back. On
  his own feet... You have done a strange thing today, fleshling, and I do not know yet whether
  it was a kindness."* It fires a new relay that pays the XP and then runs the **cloned**
  send-the-titans-home block out of the vanilla `Quest complete relay`, so the army leaves
  Toulouse exactly as it does when you bring the crystal.

Six player lines and one NPC node are ours; everything else is the game's.

### Tier 3 - Andre's other dark nodes (built 2026-09-23, unplayed)

`TitanAndre` is 83 nodes, 10 unreachable, 9 carrying replies: `02 corpse` (nine replies), `20
Introductory` (six), `800 Both lies`, `900 Lucius extorted and thrown out of town`, `1002 Hearts
in Hand but Lucius betrayed`. **Four of them begin `[REMOVED FROM GAME]`** -- the trick-Lucius and
convince-Lucius routes -- which is the authors saying so in the text, and the project leaves what
the authors deliberately cut. The rest is a read: how much of the lie-to-the-mayor branch is
reachable, and whether `02 corpse` is the scene that starts it.

**Built, and the answer to the read is that two of them were mis-pointed, not cut.**

- `02 corpse` is the *return* version of the corpse scene: same opening -- *"My people have the
  memory of a formless Daeva who drains the blood of its victims"* -- but with the hearts, the
  three accusations and Brother Michel still on the menu, where `01 corpse` (the first-meeting
  version) has only the three tail replies. **Both greetings pointed at `01 Corpse`.** The return
  greeting now reaches `02 corpse`, which also makes `800 Both lies` reachable: the accusation
  that catches him in the mayor's version *and* Esclarmonde's at once, and the only one where he
  breaks and admits it -- *"I knew I would be caught eventually."*
- `20 Introductory` is the first-meeting twin of the live `20 Introductory 2`. The return greeting
  has *"I want to talk to you"*; the first meeting did not, so his deeper menu -- the gatekeeper,
  the gullible line, his own story -- was return-only. The reply is added to `01 Conversation
  Start`.

`TitanAndre` goes from 10 unreachable nodes to 3, two with replies, and **both of those are
variants of live nodes for a state we cannot yet locate**: `1002 Hearts in Hand but Lucius
betrayed` and `900 Lucius extorted and thrown out of town` belong to the path where you extort
him and then tell the mayor anyway. `Lucius extorted` is a real checker the tree sets, but the
map chooses the betrayed return (`1003`) from a scene we have not traced, and guessing wrong
would play the wrong line at the delivery. Left for a playthrough of the extortion path.

### Tier 4 - Na Roqua (built 2026-09-23, unplayed)

11 unreachable, 7 with replies, and 0.9.0 deliberately left them because it was a Barcelona
release: her return greetings after the chicken and the shapeshifted Beatrice, **`5 Return if
Inquisitor`** (a sworn Inquisitor who has been told the Cathars are innocent -- five replies),
**`60 Stash in Caverns`** (*"There is a place I keep secret, where items of power are stored.
These things could be yours if you are a friend to the cathars"* -- a whole reward the game never
offers), `100 Return`, and `300 confront the weird woman 1`, where she admits her past.

**Built.** 0.9.0 had already wired her Cathar-friend greeting and the promise that sets
`cathar friend`; what remained needed two more checkers her own map carries and **nothing in the
game ever set**, the same shape as Tremblethorn's `angry at second visit`:

- `Beatrice present` is now set by `Beatrice Relay` -- the moment she turns the chicken back into
  the mayor's wife -- and the greeting selector reads it, so both *"No chickens this time?"*
  variants play. They sit inside 0.9.0's structure: Cathar friend first, then the chicken, then
  the Inquisition, then the plain return.
- `5 Return if Inquisitor` gets its arm: a sworn Inquisitor is greeted *"Greetings your holiness.
  I trust your investigation in Montaillou goes well, and you are closer to discovering the
  innocence of the Cathars"*, which is the game quietly taking a side.
- `60 Stash in Caverns` -- *"There is a place I keep secret, where items of power are stored"* --
  hangs off a node the writers left with the literal ID `Unknown`, whose text is her answer about
  the Cathars' allies. One reply on the live Cathar explanation reaches it, and the stash with it.
- `300 confront the weird woman 1` -- *"Then you know of my past, that I once led a very different
  life"* -- is offered on her return greetings to a player who has `spoke with seer about weird
  woman`, the checker the seer's own scene sets.

Her tree goes from 11 unreachable nodes to 5, one carrying replies: `100 Return` is a duplicate
of `03 Return Dialogue if Heard 50` with one reply changed, and stays dark as a superseded draft.

**Worth noting for the act's antagonist.** `100 Favorable Return` is the only node that reaches
`100 Shapeshifting Daeva`, whose answer is *"Within my cave, there is an old periapt -- it will
let you see the daeva's true form and strike it down. Forever."* That periapt is the Zarathustra
relic the **two** Shapeshifting Daeva trees switch on -- the 26 "duplicate" nodes recorded in the
survey are its half of the encounter. The directions have been reachable since 0.9.0 and the
route was **played and confirmed working in that release**: through the fire, into her cave, and
the true-form encounter follows. Nothing further is needed here.

### Tier 5 - the Inquisitor's third lead (built 2026-09-23, unplayed)

`MontailluInquisitor`: `300 cave` and `300 cave into` are unreachable -- *"On the outskirts of
town there is some kind of door barring entry to what we assume to be a cave... Most disturbing
is the aura of magic coming from the cave."* Two small maps exist and have nothing in them: `08
Secret Cave` (22 parts: two spirit generators, a way back, a spawn point) and `15 Witch
SecretCave` (12 parts, a relocater and a *"Secret area up top"*). `200 Tainted Audience` -- his
offer of service to a tainted character -- is also dark. Read whether the cave task was cut or
merely unwired before deciding.

**Built, and the read says half-written rather than cut.** `300 cave into` -- *"Now that you
have proven yourself to be a capable servant of our work, I would ask of you another favor for
the Inquisition, something of great importance"* -- ships with **two replies whose text is
blank**: the offer exists and the player's side of it was never typed. `300 cave` is what he has
to say when asked, and its own replies already return to his hub, so the pair is an offer and a
piece of intelligence, not a quest object -- there is no quest file, no state and no reward for
it anywhere in the game.

So it is restored as what it is: after you take the witch task or bring him word of the mayor,
*"Is there anything else in this district that troubles the Inquisition?"* reaches the offer, and
*"What is it, your grace?"* reaches the cave -- a barred door on the outskirts with an aura of
magic coming off it, which the Bishop's men have not opened. No quest is invented for it; the
player is pointed at a cave the act already has, and the two blank replies are ours.

`200 Tainted Audience` -- *"Well then tainted one, have you come to cleanse yourself of sin?
Acting in the service of the Inquisition could be the only salvation for your very soul"* -- is
now reached from all three tainted greetings, where the only replies were to claim a faction, to
threaten him, or to leave. His tree goes to **zero unreachable nodes**.

### Tier 6 - the stateless quests (read 2026-09-23; all five left, with reasons)

`Defend Montaillou from the invaders` and `Find the portals used by the English forces` have zero
states **and zero references anywhere in the game**. `Prevent the Inquisitor from killing the
Cathars` and `Root out the heretic Cathars` -- the two sides of the act's central conflict -- have
zero states and are referenced only by `02 Hamlet Burned`'s cleanup sweep. `Help Andre the Titan
with his tasks` has two written states (*"Find Marcus' cousin and take sphere from him"*, *"Return
Sphere to Marcus"*) and **no references at all**. Whether any of these has content behind it, or
whether they are names for threads that ship under other quests, is the first thing to read.

**Read, and the answer is that every one of them is an empty container for a thread that ships
without it.** Nothing here is buildable as a quest without inventing the quest, and in four of
the five cases the content it would describe is already live and working.

- `Defend Montaillou from the invaders` -- the file has **no name at all**, `Name=` is blank and
  `Item Count=0`: it was never written. What it would describe is `02 Hamlet Burned`, 1,487 parts
  of live invasion with its own `Attackers`, `Defenders` and `Defenders win a fight` trees. The
  battle ships; the quest container does not, and never did.
- `Find the portals used by the English forces` -- zero states, zero references, and the thread
  is live without it: the burned hamlet has `Hamlet Burned Knight near portal` -- *"You go ahead
  through the portal. I must remain here to fend off the Druids"* -- and the portals themselves
  are wired in the Burial Chamber, the church and Nostradamus's demesne.
- `Prevent the Inquisitor from killing the Cathars` and `Root out the heretic Cathars` -- the two
  sides of the act's central conflict, zero states each, and referenced only by the burned
  hamlet's cleanup sweep, which fails whatever is active when the village goes up. Their content
  ships under two quests that **do** have states and are fully live: `Find the Witch for the
  Inquisitor` and `Talk with The Mayor for the Inquisitor`. Giving these two states would put
  entries in the journal that nothing advances and nothing completes.
- `Help Andre the Titan with his tasks` -- two written states and no references, and the read
  explains why: its name is *"Help **Marcus** the Titan with his tasks"* and its states are *"Find
  Marcus' cousin and take sphere from him"* / *"Return Sphere to Marcus"*. **Marcus appears
  nowhere else in the game.** It is a draft from before the character became Andre-who-is-really-
  Lucius, and his errand became the four stone hearts of the Toulouse elders, which is live and
  pays 2,000 gold on `666 Done`. A matching orphan sits beside it: `Titan Sphere.InventoryItem`
  (*"Spirit gem"*, value 200) exists complete, with an inventory icon and a pick-up model, and is
  referenced by no can, map or tree.

So Tier 6 adds nothing to the release, which is the right outcome: the act's conflict is already
told, and these are the shelf the designers never filled.

### Tier 7 - the act's last readable orphans (built 2026-09-23, unplayed)

- **The Cathar Warden** greeted everyone with *"How long have you been there? What did you
  **see**?"* -- even a player who never watched him change out of the bear. `1 Conversation Start
  Not Saw Bear` is the other version and nothing opened it. A checker, `saw the warden change`,
  is set by the bear-to-cathar sequence itself, and the greeting now picks on it. His return
  greetings (bribed, friendly, unfriendly) are untouched.
- **Maury the shepherd** gains a topic on his information hub -- *"Is there anyone here I should
  be careful of?"* -- which reaches `260 Guillaume`: Guillaume Belibaste, *"a former friend of
  mine. He may treat you well at first, but it is only to abuse you at some later date. He cost
  me a half dozen sheep once."* Guillaume the con man is standing in the square.
- **Lethos** told nobody to go and see Rhea: `60 Go speak to Rhea` -- *"It would be best if you
  spoke to Rhea about our society and customs and then returned to me"* -- was reachable from
  nothing, while his greeting selector keys the whole conversation on `PC has spoken to Rhea`.
  *"What is it you want of me, then?"* now reaches it from his first meeting, his question hub
  and both returns, and accepting sets `told to see Rhea`. His two return greetings were dark for
  the same reason -- before Rhea, a second visit replayed the first meeting -- so the pre-Rhea
  branch is now a series: the introduction once, then `2 Return`, or `2 Return told to speak to
  Rhea but haven't` if you said you would go.

The act's reply-carrying orphans go from 27 to 22, and **16 of those 22 are the Shapeshifting
Daeva duplication**. What is left after that is six: Andre's two betrayal variants, Na Roqua's
duplicate `100 Return`, Beatrice's `50 come with me`, the Templar's `03 Return Dialogue` in the
mayor's house, and `ToulousePoimaino / 40 Mercury SUCCESS` -- the success half of a mercury-laced
drink offered to the titan guarding the prisoners, whose live half (`101 Mercury bubble` 1-6,
`102 Drinking`) is driven from the map. That one needs the item traced before it can be wired,
and is left for a read.

### Tier 8 - how Montaillou reads the player (first three built 2026-09-24, unplayed)

**Measured 2026-09-23 across all 51 trees and 2,281 player replies.** The act tracks what you
have *done* reasonably well and who you *are* barely:

| gate | replies | share |
|---|---|---|
| quest / state / item | 403 | 17.7% |
| Speech | 79 | 3.5% |
| faction | 55 | 2.4% |
| attributes | 43 | 1.9% |
| race | 27 | 1.2% |
| Barter | 24 | 1.1% |
| gender | 14 | 0.6% |
| karma | 5 | 0.2% |
| Outwit / Schmooze | 4 | 0.2% |
| **chosen perks** | **0** | |
| **which spirit you carry** | **0** | |

About one reply in nine is gated on a trait, and not one on a perk or on the spirit -- in the act
whose antagonist is a shapeshifting daeva, whose most important NPC is a spirit-witch, and whose
key item is a relic of Zarathustra. Brother Michel carries more character reactivity on his own
(21 attribute, 16 faction, 15 race, 4 karma -- the only karma checks in the act) than the rest of
the village put together.

**Eighteen trees and 357 replies have no character gating at all.** In order of size: the
shepherd (95 replies -- the act's information hub), Iapetus at Toulouse (70), the generic
villagers (32), the Cathar toughs (29), Mathuo (29), the gravestone puzzle (18), the town guards
(15), the Inquisition's agent in the inn (15), Menoetius (13), the Templar in the mayor's house
(10), Aidan the weapon-seller (10), Fabrisse (9), and the rest small.

**What Tier 8 would be.** Not new scenes: the act's own vocabulary applied where the writing
already forks, so that being a Feralkin, an Inquisitor, a Wielder, a brawler or a thief changes
what you can say. The candidates the reading turned up, each one reply or two on an existing
node:

- **The Cathar toughs' loyalty test** -- *"Well, whose side are you on? The goodmen or the
  Church?"* -- has three ungated answers. A sworn Inquisitor answering *"The Church"* should be
  a different scene from a stranger's opinion, and a Cathar-friendly player (`cathar friend`,
  which Na Roqua's promise now sets) should be recognised rather than tested.
- **The Relaxed Thug in the square** -- the act's mugger, who opens as a beggar and escalates to
  *"I *really* need some gold... from you"*. His tree already reads the player once, with a PE 7+
  line -- *"Your hands do not look like the hands of a farmer"* -- and it already has a
  `thug likes you` state and a `999 Return Friend` greeting to land on. What it does not read is
  the obvious one: a **Thief** or **Master Thief**, or a friend of Juanita's guild (`Thief Friend`,
  the title perk 0.13.0's collector already keys on), should not be shaken down by a colleague.
  One reply each, into the existing friendly state. **Note for the build:** the game has **no
  rest or sleep mechanic anywhere** -- no inn in Lionheart lets you stay the night, and nothing
  in the act steals from a sleeping player -- so this is the thief the square actually has.

- **The Inquisition's agent in the inn** offers you meat in a Cathar village to see whether you
  take it -- the game's own entrapment scene -- with no reaction to the player being an
  Inquisitor, a Templar, or a tainted soul who has already been threatened by the Church.
- **Fabrisse** greets everyone as a city stranger, including a Feralkin or Sylvant walking
  through a village under investigation for consorting with the unnatural.
- **Aidan** sells blades to everyone at one price, in a tree with a Barter branch nowhere.
- **The shepherd's information hub** is the act's biggest un-gated tree: 95 replies, and a
  Perception or an Outwit read of what Maury is not saying about his neighbours costs one reply.
- **The spirit** has nothing to say anywhere in the act -- `CHasSpirit` is used in 0.13.0's Plains
  warning and in the game's own Witch Interior scene, so the primitive is proven; Na Roqua, the
  daeva and the periapt are the obvious places.
- **Perks**: 0.13.0's collector showed the shape (a bare `CHasPerkExpression` as the Custom
  Requirement, as Galileo's Necromancer line does). *Thief* and *Master Thief* around the
  gravestone treasure, *Educated* on the Inquisitor's statistics of heresy, *Dark Majesty* or
  *Brutish Hulk* on the Cathar toughs' challenge, *Snake Eater* or *Fortune Finder* where the
  act's caves are discussed.

**The allegiances the act cannot see.** Montaillou checks a faction 55 times and every one of
them is Inquisitor, Templar, Saladin or Wielder. Its five Wielder-aware replies are two of
Brother Michel's demokin lines, the Bishop being threatened with undeath over the gem, and two
of Andre's *"I am a powerful wizard"* bluffs. Nothing in the act knows that the player is a
**Dark Wielder** (`Necromancer`), a friend of the **beggars** or the **thieves**, or anything at
all to the **Goblin Horde** -- and the reason generalises past this act:

| title the player can earn | awarded by | read by |
|---|---|---|
| Beggar Friend | the Beggar Captain | the Beggar Captain |
| Thief Friend | Juanita | Juanita (and 0.13.0's collector) |
| Exposer of Calle Perdida | Inquisitor Raphael | Inquisitor Raphael |
| Goblin Champion | the Goblin Khan | **nobody** |
| Ruler of Calle Perdida | **nobody** | **nobody** |

**Why nothing awards `Ruler of Calle Perdida`: it is `Necromancer` under an earlier name.** The
two perks carry the same description word for word -- *"You have mastered the Dark Arts under the
tutelage of Relican and delivered La Calle Perdida to the cruel whims of your mentor"* -- and
differ only in display name: **Dark Lord of Calle Perdida** against **Necromancer**. The pairing
was deliberate: exposing the street to the Inquisition is displayed as **Hero of the
Inquisition**, so delivering it to Relican was to be **Dark Lord of Calle Perdida**. The shipped
version keeps the Inquisition's deed-title and replaces the Dark Wielder's with a class label
whose own description still describes the deed. Not renamed here -- five readers depend on
`Necromancer` and the gain would be cosmetic -- but it is evidence that the dark ending was meant
to be a public title, which is the case for Montaillou noticing it.
| Necromancer | Relican, the Pit | five places, including 0.12.0's and 0.13.0's work |

**Every allegiance title in the game except Necromancer is read only by the faction that issued
it.** They are receipts, not reputations. The checks to change that already exist: the four
vanilla faction cans, Fixt's own `Goblin Horde IS / Midlevel / Highlevel` and `Thief Friend IS`
from 0.1.x and 0.13.0, and a bare `CHasPerkExpression` for the rest.

Montaillou is the right place to start because it is the first act after Barcelona and the
Wilderness, and the obvious readers are already written: the gate knights ask your business and
would have something to say to a man wearing goblin honours into a Templar garrison; the Bishop
of Pamiers hunts wizards and would know a necromancer standing in his church; Na Roqua is a
spirit-witch who should recognise a Wielder before he speaks; the Relaxed Thug, Guillaume the con
man and the Bartender all live on the guild's side of the law.

**Built: the three allegiance readers whose scenes were already written.**

- **The Relaxed Thug.** Three replies on his beggar's opening, his escalation and his return, for
  a friend of Juanita's guild (`Thief Friend`), a **Master Thief** and a **Thief**, each in its own
  register -- the guild one names Juanita, the master one is contemptuous about his tradecraft,
  the plain thief just notes it. All three reach `80 guild` (ours): the farmer goes out of him
  all at once, he keeps the theatre, you keep your coins, and he warns you off his patch on a
  feast day. It sets the `thug likes you` state his own tree already uses, so he greets you
  afterwards with the shipped *"I hope you are well, friend."*
- **The gate knights.** A seventh answer to Tier 1's challenge, for a member of the **Goblin
  Horde**: *"I ride with the Horde of the Khan, and my business is my own."* `100 horde` (ours) is
  the Templar answer -- he will not draw on the Scion in the open street, and you will be watched
  every hour you are in the village. Its two replies land on the shipped goodbye and the shipped
  traveller warning, so nothing new hangs off it.
- **The Bishop of Pamiers.** He recites his statistics of heresy -- ninety-eight cases, five
  hundred and seventy-eight depositions -- and a **Necromancer** can now answer *"You have missed
  one, your grace, and he is standing in front of you."* `61 the ninety-ninth` (ours) is the only
  place in the act that knows what Relican made of you: he sets down his pen, says he has neither
  the men nor the fire for you today, and gives his word before God that he will find both. Its
  replies land on his shipped goodbye and his shipped `10 Combat`.

**And the village itself:**

- **The Cathar toughs' loyalty test** -- *"Whose side are you on? The goodmen or the Church?"* --
  had three answers that anyone could give. A sworn **Inquisitor** can now answer honestly, *"The
  Church. I am the Inquisition, and I am standing in your tavern,"* into their own hostile node;
  and on *"Give us one good reason to believe you"* a **Wielder** has the reason the scene was
  asking for -- *"Because the Church burns my kind long before it gets around to yours"* -- into
  their own welcome.
- **The Inquisition's agent in the inn** eats roast meat in a Cathar village and watches who
  flinches. A fellow **Inquisitor** can now name the trick, and `36 brother` (ours) is him not
  bothering to deny it: *"It is a good test and it costs the Church nothing: a Cathar perfect
  would sooner starve than eat what I am eating, and half of them cannot help saying so."*
- **Fabrisse** greeted every stranger as a visitor from the city, including one a village under
  investigation might be expected to fear. A **Feralkin, Sylvant or Demokin** can say so, and
  `25 tainted` (ours) is a villager who does not step back: *"Half this village is on a list for
  what it eats on a Friday, monsieur. If they start on faces as well there will be nobody left
  to bring the hay in."*
- **Aidan** sold blades at one price with no Barter branch anywhere in his tree. At **Barter 40+**
  he gives the peace price -- a real `CAdjustMerchantPriceMultiplierAction` of -0.2 on his store,
  the shape Mauldo's karma greeting uses -- and opens the shop in the same reply.
- **Maury the shepherd**, the act's information hub, is the one tree where the reactivity is a
  read rather than a claim: at **PE 7+**, *"You look at the church door every time you say the
  Bishop's name."* `131 careful` (ours) drops his voice: the mayor has been called in, and the
  baker, and a woman who has not left her house since; he has told the Bishop's clerk nothing but
  the weather and would be obliged if you did the same about him.

Eight nodes and twelve replies of ours across the tier; every landing node is the game's. **Not
built and recorded instead:** the spirit. `CHasSpirit` works in dialogue and 0.13.0 proved the
primitive, but no scene in Montaillou is written for it -- putting the spirit's voice in would be
inventing a character's lines rather than reaching the game's, which is the line this project
does not cross without a draft to stand on.

**Sizing.** Every item above is one or two replies on a node the game already wrote, plus an
answer node only where the existing answers would not fit. That is the same shape and roughly
the same size as 0.13.0's collector tier. It is also the most *authored* work the project would
have done in a single tier, so it should be scoped tightly and cut first if the release is
getting long.

### Also standing

- `Cathar Warden / 1 Conversation Start Not Saw Bear` (six replies) -- the grove warden's other
  greeting.
- `shepherd / 260 Guillaume` -- a former friend who *"may treat you well at first"*.
- `Mayor Interior Templar / 03 Return Dialogue`.
- The two **Shapeshifting Daeva** trees are 31 nodes each and carry the same scenes twice, one
  set for a player with the Zarathustra amulet and one without; each map picks a tree and asks it
  for the matching node, so 26 nodes across the pair are the unused half of a deliberate
  duplication. Recorded, not a defect.

### Sequencing

Tier 1 first: it is the act's front door, it is entirely the game's own writing, and it pays off
every faction the project has built. Tier 2 next, as the largest piece of cut *design* rather
than cut text. Tiers 4 and 5 are reads that will each end in a decision. Tier 6 governs how big
this release gets, and should be read before any of the building starts.

## 0.13.0 - the Road North

**Published.** Cut from `main` 2026-09-23, entirely unplayed. Surveyed 2026-09-21 from the question "the Plains feels barren", then 2026-09-22 from "this is the second combat area in a row"; ten tiers built 2026-09-21 to 2026-09-23. The maps between Montserrat and Montaillou: the Plains, the Mountain Pass,
and the ogre caves off it.

### What the Plains is

1,111 parts, four trees, two quests, and all of it reachable: every node in `RogueInquisitor`,
`Diego`, `ShylockeGoons` and `Wilderness Merchant` is opened by something, both quests have
their states and their XP parts, and nothing on the map is inactive-and-never-activated except
the red node's undead generators, which are meant to be. What is there: the **Dark Inquisitors'
camp** in the north-west (five rogues, a pentagram, eight torches, a chant loop, a hidden
treasure) against **Bishop Diego** on the south road -- help him, or kill him for them and their
shop opens; **Shylocke's goons** if the Barcelona debt was skipped; **Mauldo** the wilderness
merchant with an evil greeting; 39 poison pods; wolves, goblin patrols, soul reavers; the red
node; a trapped chest; the three Barcelona companions' dismissal points.

Diego at the kill is already built: the kill relay releases him, gives him a temporary skeleton
AI that walks to the player, and the Attack-state transition plays `150 Congratulations` with
the XP, gold and potions, then fades him out. The checker `Bishop is near player when the rogues
are killed` (`Active=0`, referenced by nothing) and the four empty action slots ahead of that
release are leftovers of the same scene, not a missing one.

**Why it feels barren.** The camp promises a thing that never happens. Diego: *"they perform
rituals to summon the ilk of demons ... plotting to start another ritual soon"*; the rogues:
*"we have demons to summon"*; a pentagram and a chant. No demon template, no ritual relay, no
timer. Five men standing around a drawing. That is not a file with writing in it; it is a
scene the map dresses and the script never wrote.

### Tier 1 - the spirit's warning (restoration)

All three spirit companions carry `45 Rogue Inquisitors` -- *"Beware, the dark inquisitors
wield the power to cancel magic by touch, so do not let them get close to us"* -- voiced in all
three, opened by nothing. **Built:** a strip across the south-east approach, ahead of the
rogues' own `Rogue inquisitor dialog starter` poly, fires `spirit senses the rogues` once: the
game's own manifestation (Witch Interior / Dark Temple shape) -- `CHasSpirit` picks Ancestral,
Beastial or Demonic; the spirit-call effect at a marker; the spirit model appears; the balloon;
a 3 s fade and delete. The third arm checks too rather than falling through, so a Pureblood,
who has no spirit, gets nothing. Not a non-interactive sequence: the player is not locked on a
wilderness map for a warning.

### Tier 2 - the ritual (authoring)

**Built 2026-09-21, unplayed.** The rogues' ritual, so the camp does what everyone on the map
says it does. What rises is a *Terror Tough* (HP 60, AC 260, melee 45, slashing 2-8, the Terror
family's resistances -- 65% to fire, cold and lightning; 136 XP of its own). The Terror is what
the Inquisition's own cells summon in Inquisition Pit3, so it is the right ilk. The tier was
chosen against the road's own scale: the Plains' natives sit at AC 125-150, Montserrat's packs
at 150-220, the Mountain Pass's ogres and rock titans at 240-256, and the Terror Super first
built here at 325 was above all of it -- Crypt scale, and with 2-10 damage not a danger but a
whiff-fest. To-hit is d100 + skill/speed-factor + Fortune against AC, so 260 is a coin flip
for a fighter around 130 in their weapon at the default speed, or 100 swinging slow, and a
character who cannot hit it can walk away from it: it hits for 2-8. Two risings from one circle, a marker on the pentagram:

- **Fight the camp** and the circle finishes what the men began. Every rogue's death already
  fires `Killed all of the Rogue Inquisitors`, whose series shipped with four empty slots; the
  first now fires `ritual rogue falls`: no bound demon, fewer than two rogues standing -> `ritual
  answers` (once): the Monster Summoning flare, 1.5 s, the generator, *"<The men stop. The circle
  does not; it finishes what they began, and something answers it.>"*; the Terror goes to combat.
- **Side with them** (`30 join`, after the reward store closes -- its `After Closed Action`) and
  `ritual bound` sets `ritual done`, flares, and raises it passive: *"<The circle flares and
  holds what it called. It is theirs, and it knows you for a friend of theirs.>"* Turn on them
  after that and `Piss off Rogue Inquisitors` sends the Summoned Terror to combat with them.

No new model, no timer: the timer punishes exploring. Every line is ours and there are two.

### Tier 3 - Shylocke's collector (repair, and the road's best-written scene given its other half)

The "Hired Beastman": Shylocke's collector, a Hired Goon Plate leader and two swordsmen camped
mid-Plains with two once-only trip polys on the road. One scene with two faces, chosen by the
`Player owes debt to Shylocke` checker the Port District loan sets: the **shakedown** (750 with
interest and his fee; pay, stall, fight, or threaten him into the game's best intimidation menu --
magic 75, forty-inch arms, *"I am feralkin, so you know my heart is fierce"*, a bluff of hidden
archers -- and he stammers off) and, for a player who never borrowed, the **robbery** (*"Quickly!
Give me 250 gold, or die!"*: pay or fight, nothing else, and not a word of who they are). Reported
from play as a bandit met without ever having taken the loan.

**Built 2026-09-22, unplayed. All dialogue, any save.**

- *Repair.* `210 intimidate` -- *"Consider your debt forgiven!"* -- cleared the Plains' checker
  and not the two on Shylocke's own map that his tree reads, so a forgiven debtor went home to a
  Shylocke still offering repayment and refusing a new loan. Paying the goons (`90`) cleared
  them through `COtherMapAction`; scaring them off now does the same.
- *The robbery gets the talk-out.* The `ST 10+` threat on `3` / `230` / `232` into `201 bold
  threat robbery` -- `200`'s menu verbatim, with the pay line taking 250 and the two failures on
  the robbery relay -- and its own stammer, `211`, that keeps your gold without a debt to forgive.
- *Barter 40+.* Robbery: *"A hundred, and we both walk"* -> `240`, takes 100. Debt: *"Shylocke's
  rate is six hundred"* -> `245`, takes 600 (one of the four figures Shylocke's own tree accepts)
  and clears the debt on both maps. The collectors lose their fee; Shylocke is paid at his rate.
- *Outwit 7+* (robbery): the hand that never cleared leather -> `243`, they let you pass.
- *Thief Friend* and *Templar / Inquisitor*: robbery -> `241` / `242`, they stand down (it is their
  purse to forgo). Debt -> `247` / `246`: they will not put hands on you, **and the debt stands**
  -- a moneylender's ledger does not close for a cross or a guild, and only the goons' own fear
  ever forgave it. The trip polys are once-only, so they do not waylay you twice.
- *Speech 30+* on the `<Lie>`, which was offered when you had the gold and led to the same
  disbelief as the truth: he buys it (`231`); without Speech, as before.
- *"Who sends you?"* -> `232`: Shylocke's name, so the camp is a place on the road home and not
  random highwaymen. Its replies are the robbery's.

Fourteen nodes of ours, one tree. Selectable perks were first left out -- vanilla gates dialogue
on attributes, skills, Outwit/Schmooze, races, factions, karma and title perks, and almost never
on chosen perks -- and then put in at the user's call, on the one shape vanilla does use for it
(Galileo's Necromancer line: a bare `CHasPerkExpression` as the Custom Requirement):

- *Salesman* opens both Barter haggles (Master Trader requires Salesman, so it is covered).
- *Eloquence*: robbery -> `244`, the traders between here and Montaillou will hear you were
  civil, they let you pass; debt -> `248`, you will bring it to Shylocke yourself, they let you
  pass **and the debt stands**.
- *Educated*: the usury argument -> `245`, Shylocke's own rate.
- *Thief* / *Master Thief*: pay, and the purse comes back while he laughs -> `249` (`220`'s
  text with a trailing *"Eh? Where did I put that--"*); the Thief keeps the 250, the Master
  Thief gains 50 of his besides. Each shows only for its own rank.
- *Brutish Hulk*, *Dark Majesty*, *Blademaster*, *Summoning*: four more lines on both
  intimidation menus, each into the stammer.

### Tier 4 - the crosses (texture)

Mauldo's `50 Crosses`: a witch scattered her blood on the rocks to wake demons; the Inquisition
marked the spots with crosses *"where her foul magic was the strongest"*; *"many people have
come over the years to harness this power."* The crosses are thirteen ground-stake props, eight
around Mauldo's pitch and five ringing the pentagram -- the designers put the Inquisition's
markers exactly where the Dark Inquisitors drew their circle -- and none carried anything.
**Built 2026-09-22, unplayed:** a hover on the pair at Mauldo's pitch (*"The Inquisition's mark.
The ground at its foot is darker than the ground around it"*) and one on the ring's east stake
with a PE 7+ read that the stakes were pulled and re-set to fit the circle. Two polys, once
each; a new `Plains Hover` tree with two nodes of ours.

### Tier 5 - the rogues know a wizard when they see one

The Dark Inquisitors are apostate priests, not wizards: their race still casts Fire Orb and
Celestial Smite, the Church's own Thought and Divine schools, and they are using them at a blood
site the Inquisition itself marked. To a Wielder of Cedric's street they are the men who hunt his
kind, doing his art badly in the open -- and a demon loose on the Barcelona road means another
purge, which the Calle pays for and they do not. To a Dark Wielder they are five apostates with a
circle and no teacher. Vanilla greets both with *"How dare you disturb our ritual!"* and offers
the same recruitment: *"I sense power in you, definitely, but will you serve us or betray us?"*

**Built 2026-09-22, unplayed.** The camp's selector gains two arms ahead of the plain greeting,
after the Diego-companion check: `Necromancer` (Relican's title perk, granted on the dark
initiation and already the check Galileo's tree uses) -> `1 dark wielder`; `Wielder IS` -> `1
wielder`; else as before.

- `1 wielder` -- *"How dare you disturb our-- No. Stand easy. I know that look. You are off the
  hidden street in Barcelona, and you have come to watch priests do your art badly."* Its own
  reply warns them what they are calling down on Barcelona's wizards, and `21 wielder warning`
  answers it: *"They burned us out of our own order; there is nothing left of us for them to
  take... that is your trouble, wizard, not ours."* Node 1's replies otherwise, so the study,
  the fight and the exit are unchanged.
- `1 dark wielder` -- *"...hold. That mark on you is not ours, and it is not the Church's."* Its
  reply, *"I know what the circle is for. You are doing it badly,"* reaches `22 dark tribute`,
  where the Diego contract is offered as fealty rather than as a test: *"Then take the circle,
  and take us with it... Bring us his head and we are yours."* Its four replies are `20 ally`'s
  verbatim machinery (the quest, the friend checker, the fight) re-voiced, except that walking
  away is allowed rather than treated as betrayal -- they have just sworn to you.

Four nodes of ours. Note the shape: the second arm is `Wielder IS` without the perk, so a Dark
Wielder never sees the Wielder greeting.

### Tier 6 - the Inquisitor's thread, and Mauldo hears it

Diego opens with *"If you are a friend of the Inquisition, perhaps you would like to help me"*
and closes with *"The Grand Inquisitor will be most pleased!"*, and neither line knows whether
you **are** the Inquisition; Torquemada never hears of it. The 0.9.0 shape.

**Built 2026-09-22, unplayed.**

- *Diego.* An `Inquisitor IS` reply on `20 name` -- *"I am of the Order myself... it is mine as
  much as yours"* -- into `21 brother`: *"A brother. Then God is kind today, for I had resigned
  myself to hiring a sword and praying it stayed bought. What I have is not a hiring. It is our
  work."* Both replies land on his own `30 quest` and `40 rejection`, so the quest machinery is
  untouched.
- *Torquemada.* A reply on all three return greetings -- the hub where the Khan's report already
  sits -- gated on `Inquisitor IS` AND the quest completed AND not already told: *"There was a
  cult on the northern plains wearing our habit, your grace."* `413` answers it: *"Then they
  were ours once, and the rot came from inside the house... It is finished, and it will not be
  written down."* 800 XP from a part cloned off `Killed Khan` on Inquisition Chambers2 (which is
  where his XP parts live, not the Temple District), 250 gold, and a checker so it is told once.
- *Mauldo.* His return greeting becomes conditional: after either rising, `4 Return after the
  ritual` -- *"Something answered on the north road; I heard it from here and my mule has not
  been right since. The crosses did not hold it, whatever it was."* Both ritual relays now set
  a `ritual was answered` checker; the karma greeting and the shop are untouched.

Three nodes of ours. Build note: `add_parts` splices before the first `Level Part=`, and a part
sliced with `balanced()` ends **at** its closing brace -- the XP clone had to be terminated with
a newline or the map would not re-parse. Caught by validate.py at once.

### The Mountain Pass, and why it is not more combat

Surveyed 2026-09-22, after the observation that the Pass is the second combat area in a row.
It is: 1,173 parts of rock titans (60 spawns), ogres (24) and grey wolves (20) with **no
dialogue of its own** -- the only speech on the map is Marco Polo's boots quipping and the
Barcelona companions' departure. The Abandoned Cave off it is 506 parts of wolves, one hidden
treasure and nothing else. The Sprawl and the Ogre Cave are ogres; the Conjurer Cave at the end
is Aka Manah.

Three things in the map say the fighting is **a curse, not a nature**: the Woozy Ogre, who is
reachable -- *"Voices in my head... Aka Manah demands that I destroy you... He tricked our tribe
into helping him, cursed us with a charm... I must try to warn my tribe!"* -- Tremblethorn's
unreachable `50 Ogre Spells` -- *"I have spent a great deal of time and effort charming these
Ogres... They have proven effective combatants against the Titans"* -- and the Daeva himself.
And nothing lifts it: the only `RemoveCategory Enemy` on those maps is the Woozy Ogre pacifying
himself and Aka Manah pacifying himself as he teleports out. So restoring Tremblethorn's old
branch would have added a conversation to the end of a corridor without touching the corridor.

### Tier 7 - the charm has an end

**Built 2026-09-22, unplayed.** `Deactivate Teleport Trap` is fired by **both** of the Daeva's
endings -- the destroyed hook on his last phase and `Aka Manah Leaves`, the Speech route -- so
it is the game's own "he is gone" signal. It now also fires `the charm breaks`, which reaches
the Mountain Pass, the Ogre Sprawl and the Ogre Cave through `COtherMapAction` (which works on
maps never loaded): each gets an `ogre charm broken` checker and a `the charm lifts` relay that
stands the ogres down by name -- `Ogre`, `Brutish Ogre`, `Ogre Hurler`, with vanilla's full
idiom, empty target type **and** `CRemoveCategoryAction{Enemy}`, the shape the troll peace uses.
Entrance sweeps at every spawn point re-run it when you walk back in, and all 43 ogre generators
pacify what they spawn while the checker stands, so nothing spawns hostile behind you. One line,
ours, over the tribe: *"<The ogre stops mid-swing, and its arms come down. Whatever was in its
head is not there any more.>"*

Rock titans and wolves are untouched. The mountains stay dangerous; the cursed stop fighting.

### Tier 8 - the Pass reads as a crossing

**Built 2026-09-22, unplayed.** Three hovers along the road, placed on waypoints (the corridor
runs south to north): the ogre dead and the stones that killed them at the lower switchback, the
titans' quarried and *stacked* rock higher up, and a cairn at the top -- *"Aragon behind you, and
the counts of Toulouse ahead."* The cairn has a second version for a player who has broken the
charm, when the road is quiet. Four nodes of ours in a new `Mountain Pass Hover` tree.

**Corrected on the way:** the companions' departure is **not** a Pass event. `Remover of
Barcelona Companions` is a clone-based relay that exists on the Grove, the Plains, the Pass,
Montaillou, Titan Village, the Crypt entrance and the Heart entrance alike -- Cervantes, Cortes
and Darsh leave at whichever of those you reach first, which is the Grove. A "Barcelona lets go
of you at the border" beat was scoped and dropped for that reason.

### Tier 9 - Bernat's caravan (new content)

The Abandoned Cave is the emptiest map on the road: 506 parts, eight grey wolf generators, two
hidden treasures, no dialogue at all, and nothing that forces you in. **Built 2026-09-22,
unplayed,** from the user's idea: a wool and cloth merchant out of Toulouse, six weeks into a
two-day crossing, who turned back into the first hole he could find when the ogres and the
titans started killing each other across the only road. Two hired swords, **Guilhem** and
**Peire**, have held the mouth in shifts since, which is why the wolves have not had him.

Why here: it explains what the map is (wolves circling a hole someone is living in), it puts the
road's one traveller coming the *other* way in front of you, so Montaillou stops arriving cold,
and it gives Tier 7 a second place to show. The war is what shut the pass -- the titans were
always there -- so breaking Aka Manah's charm opens Bernat's road home. `the charm breaks` now
reaches the Abandoned Cave as well.

- **Trade.** `Inventory for Bernat`, cloned off Mauldo's and trimmed: potions, arrows, armour.
  Mauldo's two unique magic weapons were cut -- a wool man does not carry them.
- **News.** Montaillou with an Inquisitor sitting in it, calling people in one at a time; the
  mayor standing between them and the worst of it; the woman past the fields the shepherds go
  to when a ewe will not take her lamb. Every line points at live Act 3 content and invents
  nothing.
- **Peire.** The second sword took a wolf on his arm in the second week and it has not closed.
  A healing potion out of your own pack is the errand; he has his colour back afterwards, and
  Bernat sells at cost.
- **The road is open.** Gated on the `ogre charm broken` checker rather than on a claim, so it
  cannot be bluffed: he pays 400 gold, hands over a book he took in trade at Foix (the Tome of
  Geomancy, which Weng Choi buys), 600 XP, and goes. The camp is deleted and the cold-fire hover
  is left where it was.
- The three wolf generators within 700 px of the camp stand off so the scene is not fought
  through; the other five are untouched.

- **The bodies.** The cave is dressed with **56 wrapped cocoon bodies** -- a model set the game
  uses in only two other places, the Crypt's Retreat of Souls and a test map -- four of them
  within 180 px of the fire. They are what this map *is*, so neither they nor the camp moved;
  instead the scene notices them. A hover on the nearest cluster, and a reply on every one of
  Bernat's hub nodes: *"They were here when I crawled in... I counted forty in the first week
  and then I stopped counting. Whatever did that has not been back -- the wolves would not come
  to the mouth if it had... We keep the fire between us and the dark end."* Grey wolves do not
  wrap bodies, so the cave already implied something else had lived there; this says so without
  inventing it.

Fourteen nodes of ours, three character templates cloned (Wilderness Merchant, and the Montaillou
Guard twice), one shop, one XP part, four checkers, a departure relay, and the camp dressing --
which the user placed in the map editor. Two repairs came out of reading that back: `BottleBroke
A` has a model file but appears on no shipped map, so no `Cur Sequence` is known safe for it (the
0.5.1 check) and it became `BottleBroke B`, which vanilla places; and the placeholder campfire
this script had dropped was removed in favour of the placed `CampFireNewBig A`, with Bernat's and
Peire's lines changed from a dead fire to a live one to match what is on screen.

### Also read on the Pass

- `Deactivate Teleport Trap` activates `Remove Blue Color` on the Ogre Sprawl; the part there is
  named `remove blue color`. If the engine's name lookup is case-sensitive the Sprawl's blue
  overlay never clears. Not reproduced, not changed; recorded.
- The Speech route is **live**, not cut: `160 tricked aka manah` -> `Aka Manah Leaves` -> XP from
  `Talked Aka Manah into leaving through speech`, and a `COtherMapAction` into Alamut's Dark
  Temple so the Old Man's house knows he is loose.
### Tier 10 - Tremblethorn's dark half

**Built 2026-09-23, unplayed.** Nineteen nodes, eight unreachable and every one of them carrying
replies: an earlier draft in which he is a human wizard charming ogres for a master who means to
attack *"Nueva Barcelona"*. The shipped character is Aka Manah, a Daeva whose master is the Old
Man of the Mountain (`170 Master`, live), so the master nodes are superseded -- but the rest of
the draft is still true of the Daeva, and one of its lines is the only place the game explains
the whole area: *"I have spent a great deal of time and effort charming these Ogres... They have
proven effective combatants against the Titans."*

The two second greetings carry the authors' own comments -- `130` *"only show this if player
parted ways after node 70"*, `140` *"only if player parted ways after node 90"* -- and `90`'s
peaceful exit already activates the checker `140` is selected on. Neither node could be reached,
so `130` played on **every** second meeting, about a warning that could not have happened.

- *The hub.* `What do you want with me?` on the greeting reaches `30 Destruction`, and through it
  `50 Ogre Spells` and `40 a few ogres`. `30`'s *"Who is your master?"* was repointed from the
  dead `60 Barcelona` to the live `170 Master`, so the question can be asked and gets the
  shipped answer. `60` stays dark: its master attacks a city by a name nothing else in the game
  uses.
- *The relic.* A tainted character (the spirit in the blood is the relic of Zarathushtra he
  senses) can make him say what he senses -- `80` -- and then ask to walk out, which is `70`:
  he warns you off, and the reply now stands him down by name as well as ending the sequence, so
  you can actually leave. It sets `Tremblethorn let you go`. **The charm stays on**: the coward's
  exit leaves the ogres charmed and Bernat stuck, which is the price of it.
- *The lie.* Speech 40+ offers the Titan alliance -- *"Your master has made terms with the Titans
  of Toulouse"* -- into `90`, where he breaks off to go and see for himself; the same reply
  without the Speech reaches `120`, where he sees through it (*"Anyone who hates Titans would not
  be travelling in the direction you are travelling nor would you have killed so many ogres!"*)
  and attacks. `90`'s exit fires `Aka Manah Leaves`, the relay his other departure already uses,
  so the lie is a third way to clear the mountain -- and it breaks the charm.
- *The second greeting.* The selector now reads: angry (the lie) -> `140`; let you go -> `130`;
  otherwise the first greeting again, instead of a stranger being accused of ignoring a warning.

Four player lines of ours; every NPC line is the game's. `140` is reachable only in principle --
the lie sends him away for good -- and is left in the selector as the authors wired it.

### Also read

- `Inquisitor Darsh / 100 attack` -- *"Before I die in this place, I will send you to your
  fate!"* -- a bark with no attack machinery on any map; leave.
- The spirits' `35 undead encounter` (all three) -- written for the Crypt approach, not this
  road; carry to the Crypt's release.

### Gates

- Gate 0 as ever. Tiers 1, 2 and 4 are level parts: **a character who has not entered the
  Plains.** Tier 3 is dialogue: any save that has not tripped the goons.
- Tiers 7 and 8 are level parts on four more maps: **a character who has not entered the
  Mountain Pass, the Ogre Sprawl, the Ogre Cave or the Ogre Conjurer Cave.**
- Tier 9 is the Abandoned Cave: **a character who has not entered it.**
- Gate 1: walk to the camp from the south-east with each spirit; the spirit appears, speaks its
  line, fades; once only. A Pureblood sees nothing.
- Gate 1, Tier 2: kill the camp -> the flare and the Terror as the last rogues fall, hostile,
  once; join them -> the store, then the flare and a Terror that stands; attack them after and
  it fights. Gate 3: the hostile rising must never follow the bound one.
- Gate 1, Tier 3 (any save that has not tripped the goons): the robbery with a Barter 40 /
  ST 10 / Outwit 7 / guild / Church / Speech 30 character, each ending as written; the debt with
  Barter 40 (600 taken, Shylocke satisfied in Barcelona) and with the Church (debt stands);
  scaring them off then visiting Shylocke shows no repayment offer. Gate 3: 250 must never be
  taken twice; the Church must never clear a debt.

## 0.12.0 - La Calle Perdida

**Published.** Cut from `main` 2026-09-20, entirely unplayed. All tiers built 2026-09-17; Tier 4 and 4b decided for; Tier 5's six reads each ended in a decision; Fernand's reach and Galileo's return line added 2026-09-20 (build log). What follows is the scope as written, then the build log. Surveyed 2026-09-14.

### What the district is

La Calle Perdida is the Wielders' hidden street: 499 parts on `Calle Perdida.zax` plus the
248-part `TrappedEtherPlane.zax` behind the crystal, 21 dialogue trees. The map carries three
complete routes and the machinery to switch between them: the **Wielder initiation** (Cedric's
tasks, *Hunt down Relican*), the **Dark Wielder initiation** (Relican's tasks after he takes
the street -- 14 `Relican Take over Calle Generator` parts, a fake Relican, two conquest
cameras), and the **Inquisition wipeout** (Raphael's *find and enter* quest; `Player has
turned Calle over to Inquisition` fires from `Start Here`, force-generates the Wielders as
targets, posts six Inquisition guard generators, breaks the bridge, deletes Cedric). All three
are live. The district was never surveyed as a district -- 0.9.0 touched Cedric for the
journal and nothing else -- and the survey finds **24 orphaned nodes, 8 carrying replies**,
plus four map parts nothing reaches. The Weng Choi / Auric shapes recur; one find is the
cleanest of its kind in the project.

Tools note from the survey: entity-name matching in the engine is case-insensitive (69
case-only mismatches in shipped content that demonstrably work -- `Auric Generator` /
`Auric generator`, the Port District thug, the tavern conspirators); the map scan now
compares lower-cased. `CForceGenerateAction{Generator Name=}` is a reference the scan
missed and now counts. Two false positives recorded so nobody re-reads them: Marco Polo's
seven travel quips are opened by six maps through the duplicate `MarcoPoloSpirit Boots`
tree, and `Marco Pick up his boots` is fired by the boots' own `.InventoryItem`.

### Tier 1 - the honest way out of the Mad Enchanter

**Build.** In the Trapped Ether Plane the Enchanter's `50 Escape` offers two ways past him:
a lie (Speech 35, then 45 at `60 Lie Speech`) or the crystal -- and the crystal reply,
*"the crystal you fashioned before you lost your mind"*, goes to `53 Whoops`: he takes
offence at *lost your mind* and attacks. The honest continuation was written and is reached
by nothing: `55 Escape 2` (*"You tell me nothing I do not already know"*) -> `57 Escape 3`
(*"none of them possess the power that you speak of. Perhaps it is another of your clever
lies?"*) -> `59 Winner` (*"Very well. I shall grant you your life to test your theory - but
my undead servants are another matter. Now leave - and know that I will be watching
you."*). `59`'s reply fires `Pacify Enchanter in Dialog`, a relay **on the map, fired by
nothing**, which strips his talk specifier and gives him a `GetCloseThenTalk` opening
`05 Return Dialogue 1`. Both ends built, entrance orphaned: the Weng Choi shape, with the
map half already in place.

- One new reply on `50 Escape`, the same claim without the insult -- *"The crystal you
  fashioned. It only needs enough energy to power it, and it can take us both out of
  here."* -- `Go to node ID=55 Escape 2`. No skill gate: the route's cost is that `55` and
  `57` each offer two fight replies beside the one that continues, and `57` calls it a lie
  to your face. The player who holds their nerve gets out without a roll.
- Keep `53 Whoops` and its reply exactly as shipped; the insult stays a trap.
- Read before build: `05 Return Dialogue 1` (what he says afterwards) and what the undead
  do once he is pacified -- *"my undead servants are another matter"* says they stay
  hostile; confirm the relay does not touch them.
- Dialogue-only, so any save that has not yet resolved the Enchanter.

### Tier 2 - the Wielders know you killed Relican

**Build.** `WizardCan1 / 01 Conversation Start Wielder Killed Relican` -- *"Welcome, fellow
Wielder. We have heard much of your victory over Relican, and much about the strength of
the spirit that resides within you"* -- with a new branch `60 Membership` (*"we did not have
one such as Relican to contend with. You were truly brave to face him"*). The five `Generic
Wielder Generator` parts choose between `01 Conversation Start` and `01 Conversation Start
Wielder` on `Faction/Wielder NOT` and nothing else; `Cedric Player has defeated Relican.can`
already exists as the requirement. Third arm on each of the five selectors: Wielder AND
defeated Relican -> the killed-Relican greeting. Map-side (the generators are level parts):
a character who has not entered the street. Decision: `60 Membership` carries a
*"Save your flattery and begone"* reply with a Fight Icon and no action -- the 0.1.4 blank-
reply shape. Give it the generic wizards' existing hostile relay, or drop it. Recommend
dropping it; the wizards are the player's own faction by then.

### Tier 3 - Cedric and Relican remember being attacked

**Build.** The shape 0.10.3 built for Auric and Javier, third and fourth instance. Attack
Cedric and `Cedric sends you to a random map` plays `600 Attack Cedric`, has him cast, and
relocates you; `RESET MAP for Invulnerable Cedric` re-clones him on entry and forgets. `600
After Attack Cedric` -- *"You have strained what little welcome you had in this place. We
will tolerate no more aggression from you."* -- is **voiced** and orphaned. Relican has the
same pair: `Relican sends you to a random map` / `RESET MAP for Invulnerable Relican` (both
inactive until his takeover) and `500 After Attack Relican` -- *"I trust you have come to
your senses? Let us continue with our plans."* -- unvoiced, orphaned. One checker each, set
by the attack relay, played once by the reset over the re-cloned man. Map-side. Read
before build: Relican's reset is `Active=0` and is switched on by the takeover; the
checker must be set only while he is the one standing there, and the Dark Wielder's
`Relican Clone Generator` is what the reset clones.

### Tier 4 - the break with Relican (decide)

`Lord Relican / 50 relican mad` -> `60 reconcile` / `80 war`. *"You would be wise to
reconsider your words, brother. You would discover me to be a terrible opponent. Tell me now
where your loyalties lie."* / *"Very well. There is much work to do"* / *"So be it. I had
hoped you would have quelled your traitorous instincts long enough for me to have betrayed
you, but a quick resolution is logical. Goodbye, scion of Lionheart."* -> `CGoToCombatAction`.
A written confrontation for a Dark Wielder who turns on him, with the reconcile exit and the
war exit both authored on his side. What is missing is the player's side: `30 power` (*"Of
course, Power is everything"*) has no defiant reply into `50`, and `50` has only the
reconcile reply, so `80 war` needs a line. Two authored player lines, both short. The
consequence is the question: fighting Relican inside his own initiation means the Dark
Wielder route ends and Cedric's *defeated Relican* state should follow, and Relican in the
Dark Wielder route is a clone with a reset behind it. **Read the takeover machinery before
deciding**; if the consequence cannot be made honest, leave the branch dark and record it,
as 0.9.0 did with the shadow dryad.

### Tier 4b - the Magic Nodes get their quest (new content; decide)

The red crystals are Magic Nodes: four of them (Barcelona Coast, the Plains, the Lake,
Montserrat's Grove), each ringed by seven inactive generators, five Spirit Energy pickups
and an ambient hum. Click: a summoning effect and two skeletons; again: two greater
skeletons; a third time: three soul reavers -- the Crypt's undead, in Act 1 -- and the node
strips its own click, deletes its hum and goes dark. A voluntary escalating undead trial with
no quest, no reward past the drops, and no line that says what it is. (The other colours are
all wired: blue are the Ways Crystals, yellow the cave teleports, green the Wielders' own.)

Two quest files say what the nodes were for, and both shipped with **zero states**:
`Calle Perdida/Determine the Nature of the Magic Crystal` (a Cedric quest) and `Wielder
Initiation Quests/Find the Yellow Node within the Sewers` (a Dark Wielder task; the Wererat
Cave has a yellow node). Their only reference is the Siege map failing them in its cleanup
sweep beside the live Calle quests. The River Dryad's live reply *"I was exploring and
happened upon the magic crystal to the east"* treats the Lake's node as a landmark. The
trials were built on the map; the quests never got their states or their dialogue.

This is authoring, and the project does it only where the game plainly ran out. Here it did,
with the encounter already standing. Proposed shape, smallest first:

- **Cedric's node.** *Determine the Nature of the Magic Crystal* gets three states -- sent
  to the Lake's node (nearest the Crossroads, and the one the dryad already points at),
  the node's nature learned (set by the node's own third wave: a relay the script does not
  have yet, fired when the click is stripped), report to Cedric. Cedric's ask sits beside
  his live initiation tasks and reads as the Wielders' curiosity about their own lore; his
  reaction is one node, the answer being that the crystal draws the dead to it, and a
  Wielder with a spirit can feel it. XP from a part on his map. Every line ours; Cedric is
  unvoiced on his live task nodes too, so the register matches.
- **Relican's yellow node.** *Find the Yellow Node within the Sewers* is the Dark Wielder
  mirror and needs only a walk: the Wererat Cave's yellow crystal gets a once-only click
  that sets the state, Relican's task list gains the ask and the acknowledgement. Only if
  the Dark Wielder tasks have a slot that reads naturally; they are tightly sequenced
  (Sceptre, Quinn, the Church, the relics) and the read may say no.
- **The nodes say what they are.** Independently of either quest: a hover line on each red
  node (*"<A crystal the colour of old blood. The ground around it is disturbed.>"*), PE
  reading the buried dead, a Wielder reading the pull. The 0.10.0 hover primitive; four maps.

Decide after Tiers 1-3 are built. If only the hover line ships, the nodes at least stop
being a mystery with no answer.

### Tier 5 - reads, each to end in a decision

- **`Lord Relican / 1 Conversation Start NOT WIELDER`** and `5 Return Dialogue NOT WIELDER`
  -- *"Our partnership has worked out well for you and I. Getting rid of the Wielders has
  served both our purposes. Now leave me to my dark contemplations."* A greeting for a
  non-Wielder who partnered with Relican. The takeover relay force-generates `Wielder to
  Kill When Relican and Inquisition enter`, whose name says Relican enters *with* the
  Inquisition. Does he, and can he be spoken to? If the wipeout puts a silent Relican on the
  map, these two nodes are his half of that scene and belong on a fourth selector arm. If he
  is not there at all, they are a draft of a cut alliance and stay dark.
- **`Gives Pain to Wielders for Inquisition`** -- a relay nothing fires, whose job is to
  switch on the two relays that make Wielders hostile on generation in the wipeout
  (`Gives XtraPain to Cedric n Pedro...`, `Gives Pain to Wielder when generate for
  Inquisiton and Relican`, both `Active=0`). If the wipeout's generated Wielders stand
  passive while the Inquisition cuts them down, this is the missing call and a live defect,
  not cut content. Needs a fresh Inquisitor run to the street to know; `Make All Calle
  Wielders mad at Player` may already cover it.
- **`Cedric / 60 too much`** -- *"if you are in any way affiliated with the Inquisition, you
  will not pass our initiation"*, reached by nothing; its join reply is gated on Templar AND
  Inquisitor, which no character can be. Five live replies reach `50 warning` instead.
  Superseded draft, unless a read of the first-meeting path (`Trigger Cedric To Talk`) shows
  the Inquisition warning was meant to precede the initiation offer for a sworn Inquisitor.
- **`Brambles / 150-152 Random thanks dialog`** -- three barks after the cure; the map opens
  `140 cure relican` and `160 dark wielder greeting` but never these. A `CRandomAction` over
  the three on the cure relay is a five-minute wire if the cure scene has a moment for it.
- **`Has talked to Cedric already`** -- a checker nothing sets. His selector keys on `Took
  Wielder Quests from Cedric` instead; probably vestigial, confirm and leave.
- **`Cedric / 25 Attack`** -- *"Wielders, to me! La Calle Perdida is under attack!"* -- a bark;
  `600 Attack Cedric` plays instead. Duplicate; leave.

### Build log

**Tiers 1-3, built 2026-09-17, unplayed.** *Tier 1:* one reply on `50 Escape` -- the crystal
without the insult -- into the shipped `55 -> 57 -> 59 Winner` chain; the reads held (the
pacify relay touches only the Enchanter; `05 Return Dialogue 1` is his greeting after). The
tree drops out of the orphan survey entirely. *Tier 2:* the five `Generic Wielder Generator`
selectors gained a third arm on `Cedric Player has defeated Relican` (the shipped can reads
the `Relican Dead` scripting variable, so no map checker), and `60 Membership` lost its blank
Fight-icon reply. *Tier 3:* the Auric shape twice -- `Cedric jailed you` / `Relican jailed you`
set first thing in the attack relays, played once by the resets 1.5 s after the re-clone.
Relican's relay and reset are inactive until his takeover, so his checker cannot be set while
Cedric stands there. One workflow slip recorded: resetting the map with `git checkout` to
rerun Tier 3 also discarded Tier 2's edit to the same file; both re-applied and checked.

**Tier 4, built 2026-09-17, unplayed.** The takeover machinery read: Relican on the Calle is a
clone from `Relican Clone Generator`, built to be unkillable -- `Spell Immunity`, a damaged hook
and a `gotocombat` message handler that both fire `Relican sends you to a random map`. The two
player lines are ours: on `30 power`, *"Power is what you took from the Wielders, and it is all
you are. I did not come here to be your pupil"* into `50 relican mad`; on `50`, *"With the ones
you drove out of here. This is their street, and I am taking it back"* into `80 war`. `80 war`
fires one relay, `dark wielder war`, which strips the clone by name before anything else --
removes the message handler, empties the damaged hook (the Duke of Medina shape), removes both
categories, hooks his death -- and only then sends him, the Undead Guard and Brambles the Man to
combat. The vanilla `$Trigger` GoToCombat had to go: it would have hit the handler first and the
war would have ended as a relocation. His death (`relican clone dies`) sets `Relican Dead`, fails
the four Dark Wielder quests, plays `81 dies` and pays the shipped `Kill Relican` XP part. One
build slip: the death hook first landed on a balloon's `After Action` inside the same generator,
where `$Instigator` is the player; caught reading the part back, moved to the relay.

**Tier 4b, built 2026-09-17, unplayed.** *Determine the Nature of the Magic Crystal* gets its
three states (sent, learned, reported). The Lake's node advances it from its own third wave, on
the same action that strips the click. Cedric's `100 Secondary Greeting` gains the ask for a
Wielder who has not been asked (`140 the crystal`, sent to the Lake's node, the one the dryad
points at) and the report for a player who has learned (`141 the crystal report`: *"Then it is
not ours and never was"*; complete, 400 XP from `Node quest XP`, and *Cedric's Ward* -- a scroll
on the Clover's item, no slot, no effect). Four hover polys on the red nodes (Plains, Coast,
Lake, the Grove), a PE 7+ line, a Wielder line, a spent line once the node's SFX part is gone.
Relican's yellow node stays dark: the Dark Wielder tasks have no slot that reads.

**Tier 5, read 2026-09-17.** *`NOT WIELDER` greetings:* `Relican NIS Generator` is referenced
only by `Start Dark Wielder NIS`; the wipeout puts no Relican on the map. A draft of a cut
alliance; dark. *`Gives Pain to Wielders for Inquisition`:* the wipeout's generator fires the
200-damage kill-on-generate relay directly, but that relay ships `Active=0` and nothing ever
activated it, so the Wielders it re-generates stood while the Inquisition cut down only the ones
already there. A live defect: `Player has turned Calle over to Inquisition` now fires the
activating relay as its thirteenth action. *`Brambles / 150-152`:* wired -- `140 cure relican`'s
action gains a `CRandomAction` over the three, each a balloon over Brambles the Man 1.5 s on.
*`60 too much`, `Has talked to Cedric already`, `25 Attack`:* left, as the read said.

**Also, 2026-09-20: Fernand swings from spellcasting range.** Reported from play: the Port
District companion lands mace hits from much further than his reach. The AI `fernand joins you`
installs on him when he joins (vanilla) was copied from a caster: `Attack/Max Dist=350`, the
range at which pursuit ends and attacking begins, where every melee template including his own
says 70 (the 52 templates that pair a melee `Minimum Attack Distance` with 350 are the Wielders,
shamans, priests and vodyanoi). NPC attacks have no reach check (`Check Range When Firing` is 0
on all 1,510 attack AIs and does something else), so once the attack state begins the swing
lands. Cervantes gets 75 from the same machinery. One value, 350 -> 70. Level part: a character
who has not entered the Port District, and a companion already in the party keeps the AI he
was given.

**Also, 2026-09-20: Galileo remembers being attacked.** The sweep for Wielder content outside
the Calle found one authored line: `Galileo / 400 return after attack Galileo` -- *"Beware
braggart, I have less tolerance now for your idiocy"* -- voiced, and Inquisition Pit3 has the
whole Auric machinery (`Galileo sends you to a random map`, `RESET map for invulnerable Galileo`
fired from the spawn points) playing `400 attack Galileo` on the attack and nothing on the
return. Fifth instance of the shape: `Galileo jailed you` set first thing in the attack relay,
played once by the reset 1.5 s after the re-clone. The rest of that sweep -- the six zero-state
Wielder quests (names only; what they describe is live under another name or has no dialogue),
the four unawarded *Enemy of the ...* titles, the Blacksmith's duplicate Wizard return, the
Wilderness Relican's death bark -- is recorded and left.

### Out now, with reasons

Marco Polo's quips and boots (false positives, above). The Wielder and Dark Wielder
initiations themselves and the Inquisition wipeout: live, and large enough that anything
found in them is a repair release, not this one.

### What is new, plainly

One reply on the Enchanter; a third arm on five wizard selectors; two checkers, two
activates and two balloons on the attack/reset pairs; two player lines for the break
with Relican and one relay that makes him killable; one random bark on Brambles' cure; one call
that makes the wipeout's pain relay live. The Magic Nodes: three quest states, two Cedric nodes,
an advance on the Lake's node, an XP part, a ward, and four hover lines -- the most authoring in
the release. Every NPC line is the game's except Cedric's two node nodes and the hovers; the
player lines are ours and there are four.

### Gates

- Gate 0 as ever. Tier 1 is dialogue-only: any save that has not passed the Enchanter.
  Tiers 2 and 3 are level parts: **a character who has not entered La Calle Perdida.**
  Tier 4 and the hovers are level parts too: the Calle, and each node's map (Plains, Coast,
  Lake, Grove) needs a character who has not entered it.
- Gate 1: the honest route walked to `59 Winner` and the Enchanter passive afterwards, the
  undead still hostile; the lie route unchanged; `53 Whoops` still a fight. A Wielder who
  killed Relican greeted as such by every generic wizard, a Wielder who has not greeted as
  before, a non-Wielder unchanged. Cedric attacked, the random-map relocate, the return with
  the voiced line once; Relican the same after his takeover.
- Gate 3: a Wielder who has *not* killed Relican must never see the victory greeting (the
  `defeated Relican` can is the one Cedric's own tree trusts); the pacified Enchanter must
  not re-arm on a second visit; Cedric's after-attack line must not play on a first entry.

## 0.11.0 - the Prisoner of Montserrat

**Published.** Cut from `main` 2026-09-17. All five stages built; A, B and C played and repaired as they were built, D and E (Sahar's prisoner talk, her word, the rout) and the ring's three readers unplayed. What follows is the scope as written, then the build log. Planned from the 0.10.0 playthrough. The tester's finding: Montserrat is an
invasion -- 75 generators, about 150 enemies at the *solo* party-mojo tier, three to eight
times any Act 1 area, tuned for parties -- and that is right for what it is. What the act lacks
is any way through it that is not a fight against every pack in turn. The 0.10.0 levers (Sneak
past one ambush, Outwit at the boss) are two rolls that skip an act, which is a shortcut, not a
route. This release builds the route.

**The premise is the game's.** Machiavelli's contract was *"to find one such as yourself"*;
Sahar says the arrangement predates the slavers' cells. The garrison wants the Scion alive.
So a character can give themselves up -- and be treated as what they are to the occupiers: a
delivery. Nothing in this release removes an enemy. It changes how many a player *must* fight.

### The route, stage by stage

**1. The gate.** *"Take me to your captain."* The sentry (Tier 4's, given a talk specifier)
does not need convincing; he has been told to expect this. What the stage decides is how you
go: hand over your weapon (into a chest at the gate, recoverable), keep it on Outwit 6 (*"I
was told to arrive armed. Ask her."*), or be looked at differently as a Demokin or Sylvant
(*"One of the Master's own?"*) and not searched. A fade, and you are delivered -- not to
Sahar. To the den.

**2. The den -- the holding pen.** The Animal Den is a separate cave off the Grove with its own
door, 78 placed parts, three bears and nothing else; a garrison with prisoners to keep would use
exactly that. It gains a cage door across the mouth (the shipped `cage door` model on a locked
`CDoorAI`, `cagebar` and `cagebarframe` pieces beside it), a bored handler outside, one bear
still chained at the back, and what the monks left behind: a rosary, a tally scratched on the
rock, a cowl. Noted; still not explained. Ways out, no two alike:

| Way | Check | What it costs |
|---|---|---|
| The lock | Lockpick / Disarm 35 | nothing; you come out behind the handler |
| The hinge | Strength 8 | loud: the handler fights, and the Grove's nearest pack hears |
| The handler | Speech 40, or Charisma 7 | *"Tell her the Scion is bored."* He fetches an escort; you walk under guard |
| The bear | Sylvant, or meat from the kitchens | the bear goes through the handler and the door and the first pack it meets |
| Waiting | none | a timer; the escort comes anyway, and you go under guard with nothing kept |

The no-build path exists. The builds buy initiative.

**3. The hall -- through the occupation.** Escorted or escaped, Level 1 is crossed with the
packs passive (a `delivered` checker the generators read at spawn -- the troll-peace shape --
and a name-based stand-down for what has already spawned), and the hover trail turns inward:
the assassins eating the abbey's stores, the priestesses lighting candles, handlers dicing over
the knights' gear. An escaped character can do what an escorted one cannot -- backstab a
priestess and watch her pack drift, take the weapon back from the gate chest, doctor the well
-- each of which can wake the hall. An escorted one pays a toll at the sanctum door: the
handler takes the purse, *"the captain's share"*, unless Barter 45 keeps it.

**4. Sahar -- on her terms or yours.** Delivered and unarmed, her talk opens differently
(*"You walked in. Good. It saves rope."*), and there are three ends, not two: fight her with
what you kept or took back; the courier bluff (Outwit 7, built in 0.10.0); or **accept her
offer** -- carry her word north to the Master and go free. That is the cunning ending: the
invasion stands, the Crown is gone, you leave under her seal, Michel has a line for it, and it
is the one route that leaves her alive for the Crypt to remember.

**5. Out.** Kill her and the garrison routs -- every pack still standing goes passive and
walks north off the map on the walk-off shape, because the captain was the contract. Bluff or
accept and it stays, unalert, and you leave by Montgomerie's doors under her word. No route
fights its way out. A player who wants to can strike a departing pack, and it turns.

### The stealth layer, folded in

- **Unalert garrison.** Sneak 40+ has packs spawn passive; they wake within a few paces, at a
  drawn weapon, or when anything on the map is struck -- except inside the sanctum once
  delivered, where the fight is Sahar's alone. Generator After Action reads Sneak at spawn (the
  Khan-chest threshold); a proximity oval per pack; a Damaged Script per pack waking all by name.
- **Their own tripwires.** The seven vanilla trap polygons and the needle trap are `Triggered
  By Players` only; `Triggered By Enemies=1` and a chasing pack runs through its own poison.
- **The bell.** The sanctum's bell, clickable: everything in the room walks to it (name-based
  go-to to a marker) and the corridor past is open for twenty seconds. The Grove's woodpile,
  kicked, does the same for the camp.
- **The priestess.** A Summoner's Destroyed Script pacifies her own pack by name; the packs get
  their own names so it can.
- **Perception routes.** At PE 7+ the hover trail also says where the packs are thick.

### Not in it, with reasons

Fire in the treeline (a map cost that deserves its own decision), poisoning the well (a second
poison idea; the priestess is the thief's multiplier already), and raising the dead knights
(a set piece for its own release). Disarming by inventory: the engine removes items by name,
not by slot, so "hand over your weapon" takes the *equipped* item only if a check for the
equipped slot exists -- to read before build; the fallback is the chest taking a named class.

### What is new, plainly

The cage door and the den's dressing (shipped models on the pew envelope); one handler on the
`Assasin EarlyLevels` can with a small tree; a gate chest; a timer relay; the escort handlers
at two doors; the `delivered` and `routed` checkers and the generators reading them; Sahar's
opening variant and her offer; Michel's line; the rout relay; four or five hover texts; the
bell and woodpile parts. Every line of dialogue is ours. No new map.

### Build log

**Two reads before anything, both changed the scope.**

*The weapon handover.* The engine has no notion of the equipped item a script can reach:
`CActionRemoveInventoryItem` names a base can, `CActionSelectInventoryItemSlot` and
`CActionSetWeaponMode` only switch the active slot (Andre the Titan and the daeva use them
mid-fight), and nothing drops, transfers or ejects an item to the ground -- the inventory
vocabulary is exactly check, give, remove, generate. The chest-takes-your-gear idea is dead
(a chest generates loot; it cannot hold the player's). What *can* be done, and is: the search
runs `CConditionalAction{Try: remove X; Succeed: generate X at the gear pile}` per item --
first the fourteen hand-authored named weapons (the Everlasting, the Sacred Scimitar, the
uniques...), which are specific cans and come back exactly; then the sixteen weapon bases
and the two ammunitions, three passes for stacks, which come back as plain bases (a rolled
"Longsword of Flame" is the LongSword can plus additions the script cannot read); then two
rolls from the good random-weapon table as compensation. The pile is at the gate in the
Grove, under the sentry's nose, where it was taken. Whether a magic sword matches its base
on removal is unknowable from the files and does not matter: matched, it returns plain;
unmatched, it was never taken. The sentry says the price before the reply commits, and
Outwit 6 keeps everything. Decided with the tester: named weapons preserved exactly, the
rest replaced with similar.

*The den floor.* The waypoint graph decodes (`Cache/.../3 Animal Den.way`: 3713 nodes,
28-byte records plus an edge list; positions reliable, connectivity not). The cave floor
runs x 760-1460, y 740-1130; the mouth climbs north-west from the arrival spawn (802,755)
through a throat about a hundred units wide at (720-820, 680-720) to the exit region, whose
lower edge crosses the throat at y ~ 684. So the cage line sits at (770,700) with a bar each
side at (803,678) and (737,722), the whole cave is the pen, and there is no ground outside
the door that is not the exit trigger -- the handler stands in it (NPCs do not trigger it),
the prisoner talks to him across the bars at radius 90, and stepping out of the cage *is*
leaving. Which is why the gear pile is in the Grove. The arrival spawn is inside the line,
so the door is closed and unlocked for anyone who wanders in, and the delivery is what
locks it. The Slave Pits' `cage door b` on `CDoorAI` is the door -- the slavers' cells
Sahar mentions -- with the Chambers2 cell-door shape (the lock on a `GetCloseThen
OpenDoor` specifier, `Lock Pick Adjustment=35`), swapped in by the delivery.

**Stage A, the Grove.** `gate parley poly` (2350-2950 x 950-1450) once, unless `delivered`:
force-generates the sentry and opens `Montserrat Sentry / 1 halt` on him after 0.8 s -- the
Sahar approach shape. The sentry generator's After Action now spawns him passive with a talk
specifier (he can be re-opened by a click); `sentry draws` (the fight reply, the walk-away,
the damaged script) sends him to combat and calls the reinforcements as Tier 4 did.
`sentry search` is the search above. `deliver` activates `delivered` here and by
`COtherMapAction` on the den and both interiors, stands the garrison down by name (eleven
names, target type blanked and `Enemy` removed), and fades to `Pen Start`. All 21 invader
generators gained an After Action that reads `delivered` at spawn and comes up passive with
a *"Keep walking, Scion"* click -- the troll-peace shape. Wolves and vodyanoi are not the
garrison and stay wild.

**Stage B, the den.** Both spawn points fire `pen setup` once when `delivered` exists: close
the door, swap in the locked specifier, retire the three bear generators (now named `Bear
Generator`), raise `Chained Bear` at the back (passive, talkable) and `Handler` outside the
door (passive, `Montserrat Handler`, first greeting then *"Still here"*), and start the
300-second timer that fires `escort` if `escorted` is not yet set. Ways out: the door's
lock (Lockpick 35); the south bar's hinge, a Strength 8 click that opens the door and fires
`loud` (handler to combat, `escaped loud` set); the handler's Speech 40 / CH 7 replies ->
`escort` (door open, `escorted`, his *"Walk"* over him); the bear's Sylvant reply -> `bear
loosed` (door open, bear and handler set on each other, his alarm, `escaped loud`); and
waiting. Hover: the cage from inside, a tally of forty-one on the back wall, a cowl in the
corner. Not yet: the escort as a walking guard (he stays; the checker is what the later
stages read), the Grove's alarm on a loud escape, any hall behaviour (stage C).

**The den did not work, and the pen moved.** Tested the same evening: the Slave Pits' cage
pieces are 200-300 px fence sections built for room-sized cells, so two of them across a
100-unit throat were a wall; swapped for stalagmite posts, still a wall; the door alone,
placed by hotspot into the tunnel base, was *"a wooden door floating in space"* -- because
the mouth is a single tunnel with open floor beside it, and no arrangement of shipped
pieces reads as a pen there. The tester opened the editor to lay it out and found the same:
there is no room in that cave. Two lessons kept: **a sprite's hotspot is where the entity
stands, not the sprite's centre** (`cage door b` anchors at its top-left corner; every
placement must be rendered before it is believed), and the editor's overlap rule now
ignores overlaps the file already had when opened, or a cave map shows 281 errors that
are nobody's.

**The undercroft.** The abbey has no cells on any map, and the jailor's hover already said it
kept them. So the cells are a new map, `4 Undercroft.zax`, and it is not invented: it is the
Inquisition Chambers' south-west cell block -- Prisoner3's cell, Prisoner2's, the room
between with the stocks, the north-east wall with its doorway -- lifted verbatim (walls,
bars, door frames, torches, chains, the black masks, the collision polygons and the
waypoint hints), the terrain tile map cropped from the same region with the cell floors
painted stone, and two doors placed fresh on the jail's own door shape. 1280 x 1152, 89
scenery parts, nothing scripted survives the copy. It is reached by a stair (`Outpost/Dwarf
Region/Stairs/Down 03 A`) in the crook of the west wall of Level 1's south-west room at
(1470,2420), beside the two candle sconces and before the jailor's body: the doorway in the
undercroft's north-east wall is the foot of that stair, and a prisoner who comes up it has
the ambush and the wounded assassin behind them and the needle trap and Level 2 ahead --
the two-thirds the delivery should buy.

**Stage B, second attempt.** `Pen Start` inside cell A; `pen setup` on both spawn points
locks the cell door (the jail's `GetCloseThen OpenDoor` specifier with `Lock Pick
Adjustment=35`), seats the handler in the guard room by the stocks, raises the monk in cell
B, and starts the 300-second timer. The bear is gone and the fourth way out is **Brother
Pau**, the cellarer, the first living monk in the act, legless in the next cell: he says
where the monks went (*"up the stair and out, with their hands tied... North, with the
wagons, the way the snakes came"*), why he was kept (*"somebody has to answer the door
when the next one comes"*), and about the drain under the straw that runs under the wall
into his cell -- *"and my door was never locked. They did not think an old man needed
locking."* Talking to him sets `drain known`; the straw in cell A is a click that, with that
or Perception 7, moves you to `Drain Out` in his cell (a same-map `CRelocateAction`, the
Final Encounter's shape), and his door opens. Otherwise: the lock, the pins (Strength 8,
`loud`), the handler (Speech 40 / CH 7, `escort`), the timer. The handler's tree lost its
bears and gained the keys on his belt and *"Do not talk to him. He lies."* Hovers: the
tally, the cowl, the straw, the pins, the stair from above. The den is vanilla again.

**First test of A+B (2026-09-16), three findings.** *The undercroft crashed on entry*:
`"Idle" is missing... closed / open / opening`. Not the doors -- two barrel props I dressed
the room with were `Barrel Explode`, art no shipped map ever places (it exists for an
exploding-barrel effect and has no `Idle`), and `validate.py`'s sequence check had nothing
vanilla to compare it to and passed it. Both swapped for plain barrels; the check now fails
any model no vanilla map places, which also caught the stair (`Down 03 A`, never placed;
now `Down 02 A`). *The snakebreed attacked during the sentry's talk*: the parley forced the
dialogue but the three packs around the gate were spawned and hunting. The parley now does
what Sahar's approach does first -- target types blanked and `Enemy` removed on every
snakebreed name, the three gate generators (now named `Gate Pack West/Boss/East`) switched
off -- and `sentry draws` switches them back on and sends them to combat. *Sir Tomas was
out of reach*: he lies at (2730,705), beyond the sentry from the road, so a fresh character
meets the parley first and a prisoner is taken before reaching him. That is right -- the
invaders do not let a prisoner root through their dead -- and he is there for anyone who
fights, keeps their arms, or comes back out of the abbey through a passive garrison.

**Second and third tests of B (2026-09-16).** Pau was a Templar knight (Montgomerie's template is
`Knight 3`); now a Montserrat clone of the generic Inquisition monk, robed and unarmed. The
drain crawl in a cutscene wrapper did nothing; the plain fade and relocate does, with a line
on arrival. The drain went to Pau's own cell, which is a passage to nowhere (his door was
"never locked", so what was it for?); it now surfaces in the stair passage behind the
handler's stool, on the Druid Grove's own well grate (the tester's swap, the same fitting
the hall upstairs uses), Pau's door is locked like yours, and his legs are why forty years
of knowing did him no good. `Find Traps/Secret Doors` reveals the drain too (the
hidden-treasure `CAISecretReveal`, adjustment 20), so a thief never has to ask him. The
handler was passive and let anyone out of the cell walk past, which made every route the
same: a watch polygon across the guard room now catches an unescorted prisoner who did not
come up the drain unless Sneak 30; every fight with him brings two assassins in from the
passage mouth, and *those* stood still twice -- a `CGoToAI` temporary task replaces the
skeleton AI on the way and the arrival hook does not restore it (recorded; the shape the
Grove's reinforcements use, plain spawn close by, is what works). The 300-second escort
never fired; vanilla's longest relay delay is 120, so it is 100 now with a visible glance
at 45. The tester's own layout pass, two hidden treasures on vanilla's reveal shape, two
spirit orbs, and the torture set out and the abbey's stores in -- with three Rethgorad house
props whose hotspots sit hundreds of pixels off their sprites swapped for ones that anchor
where they draw.

**Stage C, as played.** The escort's *"Up the stair, ahead of me"* opened the door and left you
to walk a hostile hall. Now it fades and relocates you to `Escort Arrival` on Level 2, just
west of Sahar's approach strip, with the walk as a line (*"the knife at your back the whole
way. He stops at the sanctum door and does not come in"*). The arrival runs the strip's own
actions while the screen is still black -- crowd paused, generators off, Sahar raised -- and
switches the strip off, because she had popped into view. Level 1's sixteen and Level 2's ten
pack generators read `delivered AND NOT escaped loud` at spawn (the Grove's twenty-one gained
the NOT) and come up passive with the *"Keep walking, Scion"* click: a quiet escape walks the
abbey as a delivery; a loud one is hunted. Sahar's crew, the hall ambush and the runner stay
scripted.

**Stages D and E, built 2026-09-17, unplayed.** *D.* A delivered prisoner gets `1 delivered`
(*"You walked in. Good. It saves rope"*) on both the arrival point and the strip, with the
Outwit 7 courier bluff kept and a new reply -- *"Then send me north. Your word for my life, and
I carry whatever you want carried"* -- into `50 her word`: an iron ring, a snake eating its
tail, *"give it to whoever asks you for it; do not give it to anyone who does not"*, the sanctum
stood down, `sahar word` set here, on the Grove and on Michel's map, and the Montaillou quest
state given, since Montgomerie will not speak with her alive beside him. The ring is a quest
item on the clover's envelope (finger slot, no effect). Brother Michel has a line for it,
gated on the checker: *"Whoever asks you for that is the one who sent them... take it off
before you walk into the Inquisition's sight."* The offer is also on her three question nodes
for a delivered player who asks first. *E.* Her destroyed script now also fires `sahar dies`:
`routed` on all three maps, and every pack still standing goes passive and runs for an exit
marker (the walk-off shape, `CSetPatrolAIAction` on fourteen names) and is deleted on
arrival -- *"every one of them, everywhere, turning for the door."* Generators on all three maps
read `routed` as well, so nothing fresh spawns hostile on the way out. Under her word the
garrison is already passive and you leave by the doors.

**The ring's contract (decided 2026-09-17).** What Sahar's ring is worth was left vague and
then argued to the bone. It is not a safe-conduct: by Act 4 the Old Man has ordered the
Scion dead (`Assassin / 20 threat`), and no assassin honours a captain's mark over the
master's order. Her line now says exactly what it buys -- *"nothing of ours on the road
north will touch you... Past Montaillou it is his country, and I do not speak for him"* --
and her motive is in her own words: no wagons, no sisters to spare, a parcel that carries
itself, and then she can leave. Who sees it: **Michel** (*"take it off before you walk into
the Inquisition's sight"*); **Machiavelli**, the man who brokered the arrangement, if you
meet him -- saved, `301 the ring` (*"I did not think anyone would come out of it wearing
that"*) and `302 the name`; refused, `232 the ring` at the inn, where the ambush he paid for
collapses (*"I have paid them for nothing... Get out of my sight before I decide which of us
they are here for"*) and he walks out alone on `machiavelli leaves`; and the **Crypt's
Burial Chamber assassin** (`21 her mark`, a ring-gated reply on his greeting into the same
exit as `20 threat`): *"She will answer for the ring. You will answer to me"* -- the cunning
route's late cost, built the same day. Nobody stands down for
it. A player who meets none of them has what the ring is: her word, worth one abbey. Stage
directions across the act cut to one per node at most, on the tester's note.

**The Wasp Queen (2026-09-17, unplayed).** The tester's ask: a new enemy in the Grove's
second cave -- the wasp nest, eight posts of two -- on the cursed wasp's model at three
times its size. The game ships no spare wasp manifest (all three `Wasp*.mdl16` are in use),
so this is the project's first authored model manifest: `Characters/Monsters/WaspQ` is
`Wasp2.mdl16` with its model path and short name rewritten to same-length strings
(`Wasp2` -> `WaspQ`, so no length prefix moves), pointing at a byte copy of Wasp2's
`MODEL.gr2` under `Models3D/Enemies/WaspQ/` whose sidecar says `Render Scaling=0.9` --
Wasp2's is 0.3, and the field is live across 250 shipped sidecars (the wererat tiers are
1 / 1.15 / 1.5). The animations stay Wasp2's. Race from Wasp Cursed Super: 200 HP, AC 115 (170 was untouchable for a level-9 brawler),
piercing threshold 5, melee 45; 900 XP; two stingers for Quinn's errand. She stands in the
deep west chamber at (900,1050); a hover at the entrance says the nest is made of the
abbey's timber. Played the same day: the manifest loads and **Render Scaling is live** -- she was three
times a wasp, which the tester called too big; now 0.6, twice. The nest line was a click
zone nobody clicked; it plays once on arrival from the Grove instead.

**Unknowns the first test settles, in order:** whether the undercroft loads at all and its
floor and walls read (a new map; the engine generates its own pathing); whether the
cell's door and bars hold a player as they hold the jail's prisoners; whether a passive sentry with a talk specifier
lets the forced dialog open before his pack sees you; whether `COtherMapAction` activations
reach a map the save has never loaded (the sewers' `Thief enemy trigger` says yes); whether
the same-map relocate through the drain lands in cell B; whether magic weapons match their
base on removal.

### Gates

- Gate 0 as ever; the den, the Grove and both interiors are level parts, so **a character who
  has never entered Montserrat**.
- Gate 1, in order: give up at the gate; each of the five ways out of the den on the build
  that has it; the hall passive; the toll; each of Sahar's three ends; the rout and the
  unbroken garrison both walked out through.
- Gate 3: the delivered state must not be reachable twice (the sentry's reply hides once
  `delivered` exists); striking Sahar must not wake the Grove; the bear must not turn on the
  player who freed it (its target type is the invaders').
## 0.11.0 also - the trolls' ore chest

**The chief pays from the chest, and the chest is theirs.** The tester's read: a chest of red
ore stands in the pit, and taking from it should cost the peace. Vanilla's chest at (3958,1164)
had no such idea -- animation, one ore, the drop sound, and the peace held; a player at peace
could take a second ore free. Now the chief's payment (`102 word carried`) sets `ore paid` and
fires `ore chest opens` (the chest's own open, moved to a once-only relay), and his line sends
you across the pit to take it *"with your own hands, and they will watch you do it and not
move"*. Opening the chest unpaid, with `Troll Peace Keeper` standing and the chief alive, is
theft: *"That is ours. <And the room is moving.>"* over the chief and the map's own `Troll
desecration relay`. Without the peace (fought in) it is a plain chest. The chest is a level
part; the chief's node is dialogue.

## 0.10.3 - repairs

**Published.** Cut on a branch from `v0.10.2`. The cathedral and the Templar armory, and a check.

### The cathedral

**The initiation died with Esteban, and Javier had the line that saves it.** The Templar
initiation's second step is *Seek out Guard Esteban* at the Crossroads. If Esteban dies -- a
goblin patrol, or the counter-contract 0.1.1 built -- 0.1.4's `Esteban Death Consequences`
fails that quest, and Javier's only way forward (`Javier req complete esteban quest`) needs
it current. Vanilla left the quest hanging; Fixt made the lockout clean, and clean meant a
character who lost Esteban could never be a Templar. `LordJavier / 400 Esteban Slain` --
*"This news weighs heavy on my heart. I pray Sir Esteban's killer suffers for this deed. My
one comfort is that one day you might fill the void he has left. To that end, you must seek
out Sir Auric"* -- feeds the live `305 speak with auric 2`, which gives the Auric step. 0.9.0
deferred it as wanting a map relay on the death; 0.1.4 had already given us the flag,
`Esteban Dead`, a game-scripting variable. So it is a dialogue wire: *"Sir Esteban is dead."*
on Javier's three greetings, gated on `Esteban Dead > 0`, the Esteban step ever given and
not completed, and the Auric step not yet given. Any save. A player who killed Esteban for
the goblins hears the line to their face and is admitted; the game cannot know, vanilla's
text reads as irony either way, and the Horde's standing already prices the choice.

**Javier remembers being attacked, with the guard the map built for it.** The Auric shape:
`600 attack javier` sends you to the cell, `RESET MAP for Invulnerable Javier` re-clones
everyone on entry and forgets. `600 return after attack` -- *"If you blaspheme this cathedral
again, you will regret it."* -- was orphaned (flagged voiced, no recording). And the map went
further than the armory: a generator named `Guards After Attack` stands at (721,724) beside
Javier's spot, the cathedral's own three-tier guard set, inactive, never cloned by the reset.
Now: `Javier jailed you`, set by the jail relay and permanent; on every later entry the reset
clones the extra post beside him; the line plays once (`Javier warned you`). Map-side.

**Read and left alone.** `500 pyrenees` (0.9.0's out-list); `Temple Guard Gen`, a fifth post
the reset never clones; `Jafar Generator Wielder NIS`, unreferenced since 0.9.4 replaced it.
The scan's "never activated" on `Auric generator` was a false positive: the relay writes
`Auric Generator`, and 69 such case-only mismatches in shipped content that demonstrably
work show entity names are case-insensitive.

**And a bug of mine, in both reset relays.** The array's closing brace is indented one deeper
than `Action=Array`, so an `rfind` for the shallower brace matched the tail of the last
item's deeper one, and the new delayed action landed *inside* the previous `CDeleteAction`
as an unknown field, with the count bumped and no item added. The Auric commit shipped that
way on `main` (unreleased). Both repaired; `validate.py` now fails any Array whose count
disagrees with its items -- vanilla never does -- and names the bad file when run against
it.

### The Knights Templar armory

The barracks is one of the tightest maps in the game: 50 parts, every relay fired, every
checker set, and its dialogue covered by the 0.9.0 survey. Three orphans remain in Auric's
tree; one is worth wiring.

**Auric remembers being attacked.** Draw on him and `400 attack auric` sends you to the
Inquisition's cell. Walk back in and the map's `Start Here` fires `RESET MAP for Invulnerable
Auric`, which deletes and re-clones him and the guards -- and nothing remembers what you did;
he gives the ordinary return greeting. The line for that moment, `400 return after attack
auric` -- *"Save your belligerence for the creatures of the wilderness. I will not tolerate
your foolishness."* -- is written, **recorded**, and reached by nothing. Now: a checker `Auric
jailed you` beside the map's others, activated by the jail relay before it fades (the reset
deletes only the people, so it survives), and the reset, 1.5 seconds after Auric is back,
plays the balloon over him and clears the checker -- once per jailing. Map-side: a character
who has not entered the armory.

**Read and left alone.** `105 join feralkin` offers a Feralkin sponsorship *without*
Benito's task, contradicting the tainted route the game shipped (bias to overcome, task to
do, `100 join tainted` at the end); flagged as voiced, no recording exists -- a superseded
draft. `11 please return` (*"this will not help your chances"*) is a walk-out rebuke for a
`Default Canceled Node Action` the tree leaves empty, unrecorded; hooking it would scold every
player who presses Escape.

## 0.10.2 - repairs

**Published.** Cut on a branch from `v0.10.1`. The Inquisition dungeon's map side, and one of ours.

The dungeon's dialogue was surveyed for 0.9.0 (Torquemada's dryad quest, Sanchez's leniency
arms). Its four maps never were, and the map side is where the one real piece was.

**The Rites of Confession: an Inquisitor's lesson nobody could pass.** The jailor in the
Inquisition Chambers has a training arc for a member of the Inquisition, greeted as
*"recruit"* on a faction-selected greeting. Ask for *"training on the Rites of Confession"*
(`30`/`31`) and he hands over the cell keys and sends you to talk to the damned. Three
prisoners -- the dying wizard, the Wielder, the rogue Inquisitor -- each flip the map
checker `Talked to at least 1 person` when spoken to. Come back and *"I have spoken with the
possessed and heard their lamentations"* opens `50 Undergone Rites`: *"What did you learn?"*,
three Speech tiers (45/30/15) and a fallback, four XP parts on the map (250/100/25/5), a belt
as the trinket at the top -- *"don't forget about me when you make Monsignor!"* -- and a
`Done` checker so it cannot repeat. All of it built, none of it reachable: the return reply
also requires `Inquisitor Jailor Player Undergone Training Rites Confession`, whose editor
comment reads *"Active HAS undergone it. Inactive NOT undergone it"*, and **nothing in the
game activates it**. `31` fires only the keys relay. So every Inquisitor who took the training
and did the work came back to a jailor offering the training again. The reachability survey
could not see it -- every node is reachable by `Go to`; it is a requirement that can never be
true. `31`'s reply now activates the checker. Dialogue-side, so it works on any save.

**The same omission on the inspection route.** `Inquisitor Jailor Player use high speech
entry` (*"Active HAS tried it"*) was never activated either, so the Templar / Speech 30
inspection reply (`10 Knights Sent Me`), written to be once-only, was not, and a player who had
been given keys that way was then told at `40 Inside Cells NOT Inquisitor` that they may not
open the cells. `10`'s reply now activates it.

**Read and left alone.** `Galileo Attacked` (Pit) is a relay nothing fires and Galileo's
`400 return after attack` its orphaned greeting -- an attacked-and-came-back consequence never
wired; the engine already makes him hostile, and the relay adds only a door effect. The
inactive `Sanchez Generator`, the Foyer's four inactive guard generators and the Pit's
`Trapped Demon Clone Generator` are clone sources, inactive by design. `Scepter Pickup Mod
Cross AI` is fired by the scepter item, not dead. Sanchez's reduced-fine arms remain the 0.9.0
Tier 3 item: a new money-ladder arm in the map, not a wire.

**And one of ours, caught by the gate.** 0.10.0's needle trap authored a sprung bark --
`Montserrat Barks / 21 tripwire`, *"<Something gives under your foot, and a needle finds your
ankle.>"* -- and never opened it; the trap fired its poison and vanilla's generic trap message
only. The build gate (`reachability.py`) named it. Wired as the first action of the trap's
sprung branch, beside the found-bark on the other arm. Map-side: a character who has not
entered Level 1.

## 0.10.1 - repairs

**Published.** Cut on a branch from `v0.10.0`. One repair, from the playthrough's sewers.

**The thieves turned hostile at a chest, and nothing said why.** Five chests in the guild's
two secret stashes -- three behind the top-left secret door of the Sewer Main Entrance, two
behind `secret door1` in the Thieves' Congregation -- run a silent `Sneak < 25` / `< 30` check
*after* the loot drops. Fail it and `Thief enemy trigger` fires: every thief, guard dog and
Juanita go to combat, every later spawn arrives hostile, the guard's warning dialogue is
deleted, and the relay propagates to the other two thief maps. No line of sight, no distance,
no roll shown; Lockpick does not enter into it. Every *other* stealing chest in the game barks
on failure -- Khan's *"Thief! You would steal from the Great Khan?"*, the goblins' *"Thief!"*,
Auric's arrest, the Montaillou Templar -- and most bark on success with the shared
*"<You pick the lock without attracting anybody's attention.>"*; these five had neither. Now
they do, on the goblin-house shape: failure plays *"Oi! Hands off the guild's take! Thief in
the stash - get them!"* over `Sewer Thief` before the relay, success plays *"<Nobody is
looking your way. You help yourself to the guild's take.>"* over the chest. Both log. And the
check has a witness now, as the goblin house's does: `CIsAliveAction{Sewer Thief}` around the
failure branch, so a stash emptied after every thief on the map is dead raises no alarm. The
threshold itself is untouched. Chests are level parts: this takes effect on a character who
has not entered the sewers.

## 0.10.0 - Montserrat

**Published.** Played in part before the cut -- the Grove, the wounded assassin, Sahar's approach, the journal's return -- and repaired from what that found; the rest built and unplayed. What follows is the scope as written; "What was built" at the end records where the build departed from it and why.

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

**The sanctum attacked during Sahar's talk.** Its vanilla generators spawn on approach and do
not know a conversation is happening. The approach strip now pauses every snakebreed already on
the map (empty target type, the name-based action the troll peace uses) and switches the ten
`Snakebreed Generator` parts off; both fight relays switch them back on and send everything
standing to combat.

**The journal had nowhere to go.** "Javier reacts" assumed Javier could be reached, and he
exists only in the cathedral -- the summit map, which a Saladin cannot re-enter. The 500-XP
part was on the wrong map even for a Templar (his node plays in the cathedral). Now every
patron's Montserrat report-back takes the book -- Amir, Raphael, Cedric, and Javier -- each in
his own register, each paying from an XP part on his own map, each returning to the report
node so the vanilla reply still gives the quest state. And it is a quest now, *Sir Tomas's
Journal*, given at the body and closed at any patron, whose log entry names all four; the item
and Montgomerie stop pointing only at Javier.

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
