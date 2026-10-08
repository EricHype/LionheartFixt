# Unused content - the survey and the backlog

Everything the shipped game defines and then references from nothing: items, enemies, skills and
summons. This exists so the survey is not re-derived every time the question comes up, and so that a
claim about it can be **checked** rather than trusted.

Measured against `data.dat.vanilla.bak` and cross-checked against Fixt's own `files/`, because
several of these have already been used by Fixt and would otherwise read as still open.

**Read [How this was measured](#how-this-was-measured) before acting on any number here.** Four of the
findings in this document were wrong on the first attempt, one of them badly, and the ways they were
wrong are more reusable than the results.

---

## Contents

- [Summary](#summary)
- [Quest items](#quest-items-hand-authored-uniques)
- [Magic items](#magic-items-mostly-a-false-alarm)
- [Wands as a system](#wands-as-a-system)
- [Enemies](#enemies-48-cans-spawned-nowhere)
- [The summon tiers](#the-summon-tiers-the-best-single-find)
- [Skills](#skills-nothing-was-cut)
- [Perks](#perks-five-titles-nothing-awards)
- [Factions](#factions-all-thirteen-reachable)
- [Counters and set bonuses](#counters-and-set-bonuses-the-mechanism-i-said-did-not-exist)
- [Done so far](#done-so-far)
- [What to pick up next](#what-to-pick-up-next)
- [How this was measured](#how-this-was-measured)

---

## Summary

| category | defined | referenced by nothing | genuinely lost content |
|---|---|---|---|
| Quest items (`.InventoryItem`) | 14 unique | 14 | **8** (Fixt has used 6) |
| Magic item recipes (`Misc Items/*.can`) | 91 | 65 | **3** -- the rest are redundant duplicates |
| Monster cans | 478 | **48** | 48, all with working art |
| Skills (`.Skill`) | 92 | - | **0** -- nothing was cut |
| Summon tiers | 5 | 2 | **2** -- levels 4 and 5, six cans |
| Perks (`.Perk`) | 98 | 5 | **5** title perks nothing awards |
| Factions (`.Faction`) | 13 | 0 | **0** -- one was restored by Fixt |

**Nothing in the unused set is missing art.** Across all 478 monster cans there are **zero**
unresolvable models and **zero** unresolvable races. The unused creatures are complete; they are
simply not placed.

---

## Quest items: hand-authored uniques

Fourteen `.InventoryItem` definitions under `Quest Items/` that vanilla places nowhere. Each carries
written flavour text, which is the tell that someone built it for something.

### Already used by Fixt

| item | where |
|---|---|
| `Frogs` | Rakeb, `GoblinVillager`, `Lake.zax` |
| `Lava Troll Hide` | 0.28.0 -- the chief's reward, `05 Troll Pit`, the Herbalist |
| `Silver Mine Deed` | 0.31.1 -- Butu's heir hands it over; Shylocke buys it; the Mine Foreman honours it |
| `Woodsman Liver Pie Goblins` | `Give the Liver Pie.can` |
| `Helm of the Templars` | 0.36.0 -- **was unfinished**, see [Done so far](#done-so-far) |
| `Spirit Templar Shield` | 0.36.0 |

### Still open - eight items

| item | the game's own description | the hook it suggests |
|---|---|---|
| `DaVinci Tank Gear` | *"Odd chunk of metal needed by DaVinci to create one of his elaborate devices."* | **names its own quest-giver**, who is a live NPC with dialogue in the Gate District |
| `Hangover Cure Potion` | *"Clears the mind and body after the consumption of excess alcohol."* | the smallest possible scene -- a tavern favour |
| `Trapped Spirit Amulet` | *"The abilities of this amulet are a mystery."* | pairs with the ring; La Calle Perdida's trapped spirits exist as NPCs with their own trees |
| `Trapped Spirit Ring` | *"The abilities of this ring are a mystery."* | the other half of that pair |
| `Titan Crystal` | *"Large and unwieldly. Smells bad."* | Toulouse; the titans are a whole act of live content Fixt has already worked in |
| `Titan Sphere` | *"Spirit gem"* | pairs with the crystal |
| `Inquisitor Feralkin Journal` | *"details the life and trials of a Feralkin at the hands of the Inquisition"* | a readable book; needs a reader more than a quest |
| `Wielder DARK Quest Rod Bone NO Spirit` | *"darkwood that is but an empty shell without a spirit to power it"* | **names its own missing half**; the most invention required |

**Four of the eight are explicitly paired** -- the two Trapped Spirit items and the two Titan items --
so they were cut as *scenes* rather than as individual objects.

---

## Magic items: mostly a false alarm

`Specific Item Cans/Misc Items/` holds 91 `CCannedObject` **recipes**, each combining a base item with
an enchantment -- `Inventory Items/Helmet` plus `Inventory Additions/Miscellaneous/Helmets/Eagle`, for
example. **65 are referenced by nothing.**

They are mostly **not** lost content. The route drop tables actually use is
`Inventory/Generator Combinations/`, which reaches **98 distinct enchantments** directly:

| | count | meaning |
|---|---|---|
| enchantment reachable via `Generator Combinations` | **62** | redundant duplicate recipes; the item can still occur in play |
| enchantment reachable nowhere | **3** | genuinely unreachable |

### The three that are genuinely lost

| recipe | enchantment |
|---|---|
| `Misc Items/Wand Fire Ice` | `Miscellaneous/Wands/Fire and Ice` |
| `Misc Items/Wand Mage` | `Miscellaneous/Wands/Mage` |
| `Misc Items/Wand Swarm` | `Miscellaneous/Wands/Swarm` |

Three wand enchantments that exist, work, and no generator includes. Adding each to a
`Generator Combinations` selection is a one-line change; the open question is which loot tier.

One oddity worth keeping: **`Shakerspeare's Ring`** sits in the generic magic-items folder under a
unique name, and Shakespeare is already in the game -- Shylocke holds his muse as collateral. Its
enchantment is reachable, so it is not lost content, but the *name* is a hook nothing uses.

---

## Wands as a system

Worth stating separately, because it reads as a cut feature rather than an oversight: of 17 wand
recipes, only **`Wand Lightning Major`** is placed anywhere.

The machinery is complete -- `CPlugInBehaviorWand` with charge counters, a `Wands/*.InventoryAddition`
per wand, and a `Fake Wand Spells/*` skill stub per effect -- but the wands are almost absent from the
world.

The `Fake Wand Spells` skills are **862-byte stubs** with no oval, no magnitude and no effect body;
they are skill-shaped handles that the InventoryAddition points at. (`ENEMY Magical Shield` borrows one
as a convenient unlistable parent, which is the only other thing in the game that touches them.)

---

## Enemies: 48 cans spawned nowhere

Of 478 monster cans, **48 are referenced by nothing** -- no map generator, no character template, no
script. They cluster, which is the informative part:

| group | count | what it is |
|---|---|---|
| **`English in Caverns of Nostrodomus`** | **17** | the *entire* act 5 English garrison -- the `Nos Soldier1/2/3` ladders, the bow variants, `Nos Ogre2`, the Priests |
| **Sewers thieves** | **11** | `Sewer Theif Boss` x3, `Theif3 Mace` x3, `Theif4 Bow` x3, `Theif4 Sword` Super/Tough |
| **`Summoned Cans/Monster Summoning Level 4` and `5`** | **6** | see [the summon tiers](#the-summon-tiers-the-best-single-find) |
| goblin named and elite | 4 | `Grum`, `Hat Super`, `Khan`, `Rakeb` -- Fixt used `Hat Super` in 0.31.0 and built Rakeb dialogue |
| singles | 10 | `Rabid Wolf Tough`, `Assasin EarlyLevels`, `Priestess Tough`, `Sand Spirit2 Super`, `Wererat boss Super`, `Hired Goon` x2, `Theif Pale` x2, `Vodyanoi 01` |

**All 48 have working models and working races.** Nothing here needs art.

**Confidence note.** These are matched by full path *or* bare basename, because references go both
ways -- `Prime wererat.can` spawns `Wererat PRIME` by bare name and `Andre the Titan.can` spawns
`Rock Titan Lucious` the same way. Bare-name matching means short or common names can produce a false
"used" reading (`Caster` matches `SPELLCASTER`). **The group totals are sound; verify an individual
single before acting on it.**

---

## The summon tiers: the best single find

**Nothing anywhere in the game references `Monster Summoning Level 4` or `Monster Summoning Level 5`.**
Six cans, each with its own dedicated race file, fully built and unreachable:

| tier | model | HP |
|---|---|---|
| Level 4 01 | `Characters/Monsters/Snake Women` | 90 |
| Level 4 02 | `Characters/Monsters/Ogre variant` | 120 |
| Level 4 03 | `Characters/Monsters/Wererat boss` | 90 |
| Level 5 01 | **`Characters/Monsters/Rock Titan Blue`** | **170** |
| Level 5 02 | `Characters/Monsters/Desert Beast` | 120 |
| Level 5 03 | `Characters/Monsters/Sand Spirit` | 120 |

A Tribal mage's `Monster Summoning` can never produce any of them, so the top two tiers of the
summoning line are content that was finished and then disconnected. A level-5 summon that puts a
**Rock Titan** on the field is a real capstone for the school.

`Rock Titan Blue` resolves to both a `Cache/Models/*.mdl16` and a
`Models3D/Enemies/Rock Titan/Models/Rock Titan Blue/Rock Titan Blue.MODEL.GR2`, so **no art is
needed** -- this is a wiring job.

**One tell that they were abandoned mid-polish:** all six races carry `Display Name=Black Wolf`,
copied from the wolf summon and never renamed. That is the same signature as the Templar helm keeping
its shield art.

---

## Skills: nothing was cut

All 92 `.Skill` files are accounted for. Only **six** are hidden from the player, and each is hidden
deliberately by an **always-false display requirement** (`CIsEqualTo` of two different constants):

| skill | parent | why it is hidden |
|---|---|---|
| `Fake Wand Spells/Cure Major Wounds` | `Thieving/Barter` | a handle for the wand item's own effect |
| `Fake Wand Spells/Cure Small Wounds` | `Thieving/Barter` | " |
| `Fake Wand Spells/Poison Touch` | `Thieving/Barter` | " |
| `Fake Wand Spells/Rigor Mortis` | `Thieving/Barter` | " |
| `Fake Wand Spells/Secret Reveal` | `Thieving/Barter` | " |
| `Magic Thought/Defensive/ENEMY Magical Shield` | `Fake Wand Spells/Cure Major Wounds` | the enemy-variant spell |

The nonsensical parents are part of the hiding -- a wand stub is filed under Barter so it cannot
appear in a magic tree.

The other **86 are ordinary player skills** sitting in the tree with real icons. **No spell line was
cut and no school is orphaned.**

> An earlier pass of this survey reported *"75 of 92 skills that nothing presets or selects."* That
> measured **enemy** usage and so counted Barter, Sneak, Speech and Healing as unused. The right test
> is player reachability, and it gives six.

---

## Perks: five titles nothing awards

98 `.Perk` files, and the split is structural rather than accidental:

| | count |
|---|---|
| selectable at level-up | **85** |
| title perks, unselectable by design | **13** |

The 13 title perks carry a deliberately **impossible requirement** --
`CIsGreaterThanOrEqual` of the constants `0` and `1`, so `0 >= 1` can never be true. They can only
ever be *granted* by script, through `CGiveCharacterPerkAction`. This is the same hiding trick the
`ENEMY` skills use, and recognising it is what makes the survey possible: a title perk that nothing
grants is unreachable, whereas a *selectable* perk needs no grant at all.

### The five nothing grants

| perk | title awarded | its own text |
|---|---|---|
| `FACTION Inquisitor Killer` | **Enemy of the Inquisition** | *"You have slain an agent of the Inquisition."* |
| `FACTION Templar Killer` | **Enemy of the Knights Templar** | *"You have slain a Knight Templar."* |
| `FACTION Wielder Killer` | **Enemy of the Wielders** | *"You have slain one of the Wielders of Barcelona."* |
| `Goblin Slayer` | **Goblin Slayer** | *"...slain a great number of goblins. Your brave actions have kept their population in check..."* |
| `Ruler of Calle Perdida` | **Dark Lord of Calle Perdida** | *"...mastered the Dark Arts under the tutelage of Relican and delivered La Calle Perdida to the cruel..."* |

Vanilla had **six**. Fixt has since wired up `Child Killer`, which is why the figure is five now.

### The faction-killer three are the clearest repair in the whole survey

There are **four** `FACTION * Killer` perks and **exactly one works**:
`FACTION Saladin Killer`, granted in `Levels/1 Barcelona/Gate District.zax` by a
`CAIInteractionSpecifier` whose action is a plain `CGiveCharacterPerkAction`:

```
Action=CGiveCharacterPerkAction
{
    Character to give perk to=$Instigator
    Perk to give=Perks/!Event Title Perks/FACTION Saladin Killer
}
```

The Inquisitor, Templar and Wielder equivalents exist, read identically, and nothing fires them. This
is not cut content -- it is **three quarters of a shipped pattern left unconnected**, with the working
quarter sitting beside it as a reference implementation. All three name live factions whose members
the player can already kill.

**The scope caveat matters, though.** The Saladin version is granted by a *trigger in one map*, not by
a death hook on the faction's members. Wiring the other three properly means deciding where detection
lives, and a per-member `Destroyed Script Action` -- the approach the goblin work used -- is the robust
answer rather than copying one line. And a death hook has a known trap: a generator's
`CSetDestroyedScriptActionAction` **replaces** the can's death slot rather than adding to it, which is
how the Lava Troll Hide was dead code from 0.10.0 until 0.30.1 caught it. Any death-hook approach must
check the generators that spawn those members, not just the cans.

### The other two are different in kind

**`Goblin Slayer`** wants a *kill count* -- *"a great number of goblins"* -- and **the counter
already exists and already works.** `Derived Character Attributes/Goblin Kill Counter` is written and
read by six shipped files: `Goblin Warrens.zax`, `Mongol Camp.zax`, `Goblin King.can`, `Rakeb.can`,
`Mongol Archer Village.can` and `Mongol SwordsmanVillage.can`. So this needs a **threshold read**
granting the perk, not a mechanism built -- which makes it one of the cheapest items on this list
rather than one of the most expensive.

> An earlier version of this document said *"no counter mechanism has turned up in the engine."* That
> was wrong, and wrong twice over: a general counter pattern exists (see
> [below](#counters-and-set-bonuses-the-mechanism-i-said-did-not-exist)) **and** a goblin-specific
> counter is already live.

**`Ruler of Calle Perdida`** is the dark-path ending of a questline whose *other* outcome,
`Exposer of Calle Perdida`, **is** granted. So this is a missing **branch**, not a missing hook -- the
questline resolves one way and not the other.

---

## Counters and set bonuses: the mechanism I said did not exist

An earlier version of this document, and the conversation that produced it, stated that **no
set-bonus mechanism exists in the engine** -- having searched for `CHasItemEquipped`,
`CCheckEquipped`, `CHasInventoryItem`, `CIsWearing`, "Set Bonus" and "Matched Set", none of which
appear anywhere. That conclusion was wrong, and the error is instructive: the mechanism does not
*check* equipment at all, so no query shaped like a check could ever find it.

**It counts.** The **Voodoo set** is the shipped reference:

| piece | what it does |
|---|---|
| `Inventory Additions/Miscellaneous/Necklaces/Voodoo` | +1 to all four Tribal branches, **and `Number of Voodoo Items` +1** |
| `Inventory Additions/Miscellaneous/Belts/Voodoo` | the same four branches, **and `Number of Voodoo Items` +1** |

Each piece increments a derived character attribute through `CCharacterModifierDerivedAttribute` with
**`Allow Accumulation=1`**. The *bonus* then lives in a different, **computed** derived attribute that
reads the total. `Skill Points Per Level` is literally:

```
10 + Intelligence + (Number of Voodoo Items == 2 ? 1 : 0)
```

Wear one piece and the counter reads 1 and nothing happens; wear both and it reads 2 and you gain a
skill point every level. Both items say so in their own description text, and both are
`Addition Rarity/4 Very Rare` at 850 value.

**So the pattern is: an equipped item writes a counter, and a computed attribute reads it.** That
single pattern covers set bonuses, kill counts, and any "how many of X" condition. Of the 129 computed
derived attributes in the game, any can host such a term.

### Orphaned counters worth knowing about

| attribute | state |
|---|---|
| `Goblin Kill Counter` | **live** -- written and read by six files; the hook `Goblin Slayer` needs |
| `FACTION LEADERS KILLED` | **orphan** -- defined, written by nothing, read by nothing |
| `Is Wearing Necklace of Voodoo` | **orphan** -- defined and read by nothing; superseded by the counter |

`FACTION LEADERS KILLED` is suggestive next to the three ungranted `FACTION * Killer` perks, though
nothing proves they were meant to connect.

---

## Factions: all thirteen reachable

Every one of the 13 `.Faction` files is assigned by something, through
`CAssignFactionToCharacterAction`. **No unused factions.**

| faction line | ranks | assigned by |
|---|---|---|
| Inquisitor | `Acolyte`, `Hallowed`, `Inquisitor` | vanilla |
| Templar | `Squire`, `Warden`, `Paladin` | vanilla |
| Wielder | `Mage`, `Conjurer`, `Wizard` | vanilla |
| Saladin | `Aswaran`, `Exalted` | vanilla |
| Saladin | `Blessed` | **Fixt only** -- `Jafar.DialogTree` |

`Saladin Blessed` is the one worth knowing about: vanilla defines it and never assigns it, so it was
already an orphan that Fixt restored. It is also the file Fixt's own goblin factions were modelled on,
which is why that line matters beyond its own rank.

This is a useful **control group** for the method. A survey that reports "nothing is used" is
measuring itself; factions coming back 13-for-13 is evidence the grant detection works.

---

## Done so far

### 0.36.0 - the Templar set

**`Helm of the Templars` was unfinished, which is very likely why nobody placed it.** A
`Character Slot Types/Head` item carrying **shield art in every other field**:

| field | vanilla | repaired from `Inventory Items/Helmet.InventoryItem` |
|---|---|---|
| `On the ground` | `Special Items/LionShield_PU` | `Items/PickUps/Misc Items/Helmet_PU` |
| `Basic` / `Better` / `Special` | `Armor/Shield Large Better` | `Items/Inventory Images/Armor/Helmet1` |
| `Catagory for display Grouping` | `Grouping Catagories/Shield Large` | `Inventory/Grouping Catagories/Armor` |

Someone cloned the shield, changed the name, description and slot, and stopped. `Encumbrance=2` and `Value=100` are untouched.

**The art repair was only half the problem.** Both pieces shipped with **no mechanical effect at
all** -- their only behaviours were the pickup and putdown *sounds*. No armour class, no resistances,
no `Wearing a Helmet` flag, and `Inventory Addition Group=!None` so neither could ever be enchanted.
An item described as *"shines with the power of the Templars"* was strictly worse than a plain helmet
off any thug.

Stats were added, and then **retuned once** -- the first pass matched the vanilla item of the same
*encumbrance*, which priced a unique set at mid-tier and left it outclassed by gear from acts 1 and 2.
Encumbrance is the wrong yardstick; the ceiling for the two slots is:

| | the set | the best alternative for that slot |
|---|---|---|
| Helm, enc 2 | AC **+6** | `Helmet` AC **+3** -- the best base, and `Helmets/Protection` adds **+0** AC, so nothing in the game beats +3 in the head slot |
| Shield, enc 5 | AC **+8**, Piercing **+15**, Slashing **+12**, Crushing **+12**, speed **-0.03** | `ShieldLarge` AC **+7**, P15 S10 C10 -- but at encumbrance **10** and speed **-0.08** |
| both worn | **+4** AC more | the best AC *enchantments* in the game are +4 to +6, rarity 3 Rare |

**Pair total: +18 AC** against the roughly **+10** those two slots otherwise allow. For scale, base AC
is `2*(Agility+10) + 10 + Evasion` -- about 42 at Agility 6 -- and upgrading body armour from Hard
Leather to Hauberk Mail is +10. So the set is a strong reward for committing two slots to it, without
rewriting the character.

The distinguishing feature is **weight**: it protects like a great shield and carries like a medium
one, which is what a blessed Templar kit should feel like. Encumbrance and value stay at vanilla's 2
and 5, and 100.

**Two more bonuses were added on request**, and neither could be a *set* bonus. The +4 AC works
because `(AC) Armor Class` is a **computed** derived attribute, so a conditional term in its
expression re-evaluates when the counter changes. `Skills/Fighting/OneHandedMelee` is a Skill and
`Character Attributes/(LK) Luck` is plain storage with no `Expression=`, so neither has an expression
to host a condition. Both sit on the pieces unconditionally:

| | | calibration |
|---|---|---|
| Shield | `OneHandedMelee` **+5** | unique weapons give +10 to +20 (`Kublai Khans Sword` +10, `TRUE CROSS` +10, `Axe Unholy Smite` +20 Evasion) and enchantments +8 to +15 (`Falcon` +8, `Evader` +15). +5 sits below the enchantment floor, which is right for armour rather than a weapon. A Templar fights sword-and-shield, so it belongs on the shield |
| Helm | `(LK) Luck` **+1** | the blessing |

**The Luck point has no unconditional precedent, and that is worth knowing.** Of the 18
`InventoryItem`s that use `CCharacterModifierAttribute`, the shape is always *conditional* --
`Crossbow` grants +1 Perception only with the `Sharpshooter` perk. So this is the only flat attribute
bonus on any item in the game, and Luck is not a cheap stat: `Fortune`, `CriticalChance` and the Cold,
Fire and Electrical resistances all read it. The field shape is copied from the Crossbow exactly; it
is the *unconditional* part that is new, and that is a balance judgement rather than a technical one.

The Helm also sets the `Wearing a Helmet` flag that three shipped files read.

**And a two-piece set bonus of +4 AC**, built on the Voodoo pattern described
[above](#counters-and-set-bonuses-the-mechanism-i-said-did-not-exist): each piece increments a new
`Number of Templar Items` counter, and `(AC) Armor Class` gains a conditional term reading it at
`== 2`. That edits a core attribute, so `TS12` and `TS13` exist to prove it is inert for anyone
without both pieces.

**`Spirit Templar Shield` needed nothing**: `Hand` slot, `LionShield_PU`, `Shield Large` icon and
grouping, `Encumbrance=5`. Coherent in vanilla; it only ever lacked a placement.

**Both are carried by `Dead Knight Templar 5`**, inlined as full `CInventoryItem` blocks inside the
corpse's `CAIInventory` -- which is how the amulet those corpses already carry is stored, since the
array holds definitions rather than paths. Of the five dead-Templar templates that is the only one
used just **twice**, both in act 3's `02 Hamlet Burned` where Templars died; the others serve 9 to 15
corpses each and would have scattered a unique set far too widely. Editing the template rather than
the map means **no new map entity**, so this reaches any save that has not yet entered that map.

Tested by `TS1`-`TS10` in [`qa.md`](qa.md).

---

## What to pick up next

In rough order of how little invention each needs:

1. **The two summon tiers.** Six finished cans with dedicated races and working art, gated behind a
   missing reference in the skill's tier table. Nothing to design. The only real question is what the
   level-4 and level-5 thresholds should be.
2. **`DaVinci Tank Gear`** -- names its own quest-giver, who is a live NPC with dialogue.
3. **`Goblin Slayer`.** `Goblin Kill Counter` is already live and already written by six files;
   this is a threshold read away. Moved up from last place after the counter claim was corrected.
4. **The three `FACTION * Killer` perks.** A shipped pattern with one working quarter as the
   reference. Needs a decision about where detection lives -- per-member death slot rather than a map
   trigger -- but invents nothing.
5. **The three lost wand enchantments** -- `Fire and Ice`, `Mage`, `Swarm`; one line each into a
   `Generator Combinations` selection.
6. **`Hangover Cure Potion`** -- the smallest possible scene.
7. **The two Trapped Spirit items** -- the spirits already exist as NPCs with dialogue, so the scene
   is half-built.
8. **The two Titan items** -- Toulouse is live content Fixt has worked in before.
9. **The 17 Nostradamus English** -- a whole garrison with art, but placing them is level design
   rather than restoration, and act 5 is already populated.
10. **`Inquisitor Feralkin Journal`** -- needs a reader.
11. **`Wielder DARK Quest Rod Bone NO Spirit`** -- its missing half has to be designed.
12. **`Ruler of Calle Perdida`** -- a missing questline branch, so it needs writing, not wiring.

---

## How this was measured

The method matters more than usual here, because **four** answers were wrong on the first attempt in
ways that all looked plausible. Each failure is a reusable lesson, so they are recorded rather than
quietly fixed.

### 1. A quadratic scan that never finished

The first item survey searched the whole archive once per item and was killed after two minutes.
Rewritten to index every referenced value in a **single pass** over the archive, then test membership.

### 2. Excluding `.txt`

The second attempt skipped `.txt` files -- which is exactly where `Inventory Addition Groups`,
`Grouping Catagories` and `Addition Shopping Strategies` live. Had the item pools been listed there,
every result would have been a false positive.

### 3. Matching one field name

The third attempt counted enchantments reached through `Addition=` and reported 65 orphaned magic
items with **four whole equipment categories unplaced**. That was wrong:
`CInventoryItemGeneratorMiscellaneousMagic` spells the same relationship **`Additional Magic=`**, and
once both are counted, 62 of those 65 are redundant duplicates.

Same shape as `Requirement=` versus `Custom Requirement=`, and as `Name=` inside `Relay Name=`.

### 4. A case-sensitive extension - the worst one

A check for dangling `Race=` references reported **93 monster cans with an unresolvable race**, broken
down by folder, framed as a live vanilla defect affecting spawned content. **That was entirely a bug
in the check.** Race files ship under **two extension spellings -- 427 `.Race` and 76 `.race`** -- and
the check required the capitalised form. Every one of the 93 resolves once case is folded.

The true figure is **zero** unresolvable races and **zero** unresolvable models across all 478 cans.

This one is the most instructive because the project already carries a note titled *"name audits must
fold case"*, recorded after a case-sensitive sweep invented four Toulouse defects. The lesson was
known and the extension was still matched case-sensitively.

It did surface one genuine thing: `Races/Enemies/Thugs/` contains **both** `Thug3 Mace.race` and
`Thief3 Mace.Race` -- two parallel spellings of the same ladder. Worth knowing before editing anything
in that folder, since a careless edit could hit the wrong file.

### 5. Two reachability routes, not one

Perks nearly produced a false result in the opposite direction. A first instinct is to ask what
*grants* each perk -- but 85 of the 98 are **selected by the player at level-up** and are granted by
nothing, by design. Reporting those as unused would have been the mirror image of the skills mistake,
where enemy usage was measured and Barter came back "unused".

The test that works is the **impossible requirement**: `CIsGreaterThanOrEqual` of the constants 0 and
1 marks a perk as unselectable, and only those need a grant. Two routes, and a perk is reachable by
either.

### 6. Querying for a shape instead of examining a case

The worst of the six, because the evidence was already in hand. Asked whether a two-item set bonus was
possible, the search was for class names that *sounded* like equipment checks -- `CHasItemEquipped`,
`CIsWearing`, "Set Bonus" -- and when none existed the answer given was "the engine has no hook."

The Voodoo belt and necklace had appeared in this document's own orphan list an hour earlier. Opening
either one would have shown the mechanism immediately, because the mechanism is a **counter**, not a
check, and no query shaped like a check could find it.

**The rule: when asked whether a mechanism exists, find a case that works and read it.** Do not
enumerate guesses at its name. `one query is not proof of absence` applies to class names as much as
to content.

### What makes the final numbers trustworthy

**The control groups.** A survey that comes back "everything is unused" is measuring itself:

- **All 13 potions are placed.** When the designers wanted a consumable in the world, they placed it
  -- so a category coming back empty means something.
- **86 of 92 skills are player-reachable.** The skill system is complete, which is what a correct
  method should say about a system that visibly works in play.
- **Zero unresolvable models or races.** If the resolution logic were wrong, this number would be
  large -- as it was, wrongly, at 93.

### Rules for the next pass

- Fold case on **both sides**, including file extensions.
- Match a reference by **full path and bare basename**, since the game uses both.
- Never trust a single field name; check whether a sibling spelling exists.
- Include `.txt`, which holds the pools and groups.
- Cross-check against **Fixt's own `files/`**, or already-restored content reads as still open.
- State a control group. A result with no category coming back "fully used" is not yet believable.
- Ask how many ways content can be reached **before** testing one of them. Perks have two;
  skills have two; items have three.
- To ask whether a mechanism exists, **open a case that works**. Searching for a plausible
  class name finds nothing when the mechanism is shaped differently than expected.
