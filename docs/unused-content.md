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
- [Magic items](#magic-items-a-disconnected-pipeline)
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
| Magic item recipes (`Misc Items/*.can`) | 91 | 65 | **see below** -- the enchantment pools were never wired to the master generator |
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

### Still open - three items

Three came off this list in 0.39.0: both Trapped Spirit items and
`Wielder DARK Quest Rod Bone NO Spirit`.

| item | the game's own description | state |
|---|---|---|
| ~~`DaVinci Tank Gear`~~ | *"Odd chunk of metal needed by DaVinci to create one of his elaborate devices."* | **Done in 0.43.0** -- the gear comes from DaVinci's talking steam engine at three prices, one of which is a promise that outlives the quest |
| ~~`Hangover Cure Potion`~~ | *"Clears the mind and body after the consumption of excess alcohol."* | **Done in 0.44.0** -- the drunkard who teaches Drunken Boxing asks for it after Montserrat; Quinn brews it from nightshade root given by Na Roqua in Montaillou |
| `Titan Crystal` | *"Large and unwieldly. Smells bad."* | unused, but its **icon art is reused** by the live `LuciusMneme` |
| `Titan Sphere` | *"Spirit gem"* | unused, but its **icon art is reused** by all four live stone hearts |
| ~~`Inquisitor Feralkin Journal`~~ | *"details the life and trials of a Feralkin at the hands of the Inquisition"* | **done in 0.50.0.** It never needed a reader -- it needed a **shop**. The item was always complete; it was the only one of the twelve books obtainable nowhere |

**The two Titan items need classifying before building.** Their art survived into live items, and
the concepts they name are both covered by live content -- `LuciusMneme` for the crystal and
`Spirit Transfer Gem DaVinci` for the "spirit gem". That is the signature of a **superseded draft**,
the third category below, so check for a live replacement before writing anything.

Also at zero references: `Gem` and `Expensive Gem`. Those are generic loot rather than
hand-authored uniques, so they belong to a different question than this table.

---

## Magic items: a disconnected pipeline

`Specific Item Cans/Misc Items/` holds 91 `CCannedObject` **recipes**, each pairing a base item with
an enchantment -- `Inventory Items/Helmet` plus `Inventory Additions/Miscellaneous/Helmets/Eagle`, for
example. **65 are referenced by nothing.**

> **This section previously said 62 of those 65 were "redundant duplicates whose enchantments reach
> the player anyway through `Generator Combinations`."** That was wrong, and the error is worth
> keeping: the check confirmed that a `*selection MAGIC` can *listed* the enchantment, and never asked
> whether that selection can was itself reachable. Most of them are not.

### What the master generator actually yields

`1 MASTER ALL Items in the game` is drawn by real maps -- `04 Maw of the Assasin`,
`06 Chamber of Torment`, `07 Dark Temple`, `Cortez Cave`. Walking down from it:

```
1 MASTER ALL Items in the game
 |- All Armor and Shields
 |- All Weapons
 `- All Miscellaneous Items
     |- All Potions                     -> Potion selection MAGIC      (reachable)
     `- All Misc Items except Potions
         |- weighting 17: eight PLAIN base items --
         |                Amulet, Belt, Boots, Bracers, Gauntlet, Helmet, Necklace, Ring
         |- weighting  2: All Scrolls   -> Scroll selection MAGIC      (reachable)
         `- weighting  2: All Wands     -> Wand selection MAGIC        (added in 0.38.0)
```

So the misc branch yields **plain, unenchanted equipment**, magic potions and magic scrolls. The
`*selection MAGIC` pools -- which are the things that pair a base item *with* an enchantment -- are
reachable for potions and scrolls only.

### Which equipment pools are connected

| pool | reachable from | state |
|---|---|---|
| `Potion selection MAGIC` | the master, plus 3+ maps directly | fine |
| `Scroll selection MAGIC` | the master, via `All Scrolls` | fine |
| **`Wand selection MAGIC`** | `All Wands`, which **nothing drew from** | **connected in 0.38.0** |
| `Boot`, `Gauntlet` | one map each (`2 Retreat of Souls Entry`) | reachable, barely |
| `Necklace` | one map (`2 Retreat of Souls`) | reachable, barely |
| `Arrow` | one map (`01 Sewer Main Entrance`) | reachable, barely |
| **`Amulet`, `Belt`, `Bracer`, `Cloak`, `Helmet`, `Ring`** | `All Magic Equipment` | **connected in 0.38.0** |
| `Bolt` | nothing at all | still disconnected -- ammunition, see the note below |

**Seven pools are referenced by nothing whatsoever.** So magic rings, amulets, belts, bracers, cloaks
and helmets do not drop from the master generator at all -- their plain versions do, and the
enchantment half of the system was built and never wired in. That is the largest single finding in
this document and the one that would most change how the game plays.

**Fixed in 0.38.0** through a new `All Magic Equipment` intermediate can holding all six pools,
entering the misc branch once at weighting 2 -- so magic equipment is **9%** of that branch, matching
scrolls and wands, rather than the **36%** that six separate branches would have produced. All 40
enchantments across the six pools were verified implemented first. `WD1`-`WD16` in [`qa.md`](qa.md).

**And gated by mojo in 0.38.1**, which 0.38.0 shipped without. `All Magic Equipment` is a
`CInventoryItemGeneratorMojoList` on `CAverageMojo` at thresholds **7 / 16 / 999** -- vanilla's own,
copied from `All Armor` -- with each tiered pool keeping every entry and zeroing the too-good
rarities, the way `Armor LOW Mojo` does. Below mojo 7 only amulet and ring enchantments appear and
nothing above Uncommon; Very Rare and Unique start at mojo 16, around the Crypt. Belt, Bracer, Cloak
and Helmet have no Common or Uncommon enchantment at all, so they are absent from the lowest band by
necessity rather than choice.

---

## Wands as a system

Of 17 wand recipes only **`Wand Lightning Major`** was placed anywhere in vanilla, and the pool they
should have come from was disconnected -- so wands were effectively absent from the world.

The machinery is complete: `CPlugInBehaviorWand` with charge counters, a
`Wands/*.InventoryAddition` per wand, and a `Fake Wand Spells/*` skill stub per effect. Those stubs
are **862-byte shells** with no oval, no magnitude and no effect body; they are skill-shaped handles
that the InventoryAddition points at. (`ENEMY Magical Shield` borrows one as an unlistable parent,
which is the only other thing in the game that touches them.)

### The three in `Wands/Special/`, and why only one was restorable

The three enchantments no pool listed sit in a `Special/` subfolder. **They are not equivalent**:

| wand | rarity | value | implementation |
|---|---|---|---|
| **`Swarm`** | 5 Unique | 7500 | **complete** -- `CPlugInBehaviorWand` + `CPlugInBehaviorModifyCharacterWhenSelected`, modifying `Magic Tribal/Offensive/Insect Plague` and `Piercing Damage Resistance`. Summons insects; confers ranged-damage resistance while charges remain |
| `Fire and Ice` | 5 Unique | **0** | **shell.** 1,036 bytes, **no behaviours, no modifiers.** Its text promises Fireball *and* Ice Storm cast together plus 15% fire and cold resistance. None of it exists |
| `Mage` | 5 Unique | 10000 | **shell.** 1,161 bytes, **no behaviours, no modifiers.** Its text promises +4 skill points in every base magic skill across all three categories, five Lightning Bolts and five Fears at skill 20. None of it exists |

`Swarm` was wired into the pool in **0.38.0** at weighting 5, matching `Rigor Mortis` -- the one other
`5 Unique` already there, at value 6500 against Swarm's 7500.

### Built in 0.49.0 -- and two claims here were wrong

This section used to say the two shells were **deliberately left out** because restoring them "needs
a judgement first: `Wand of Mage` as described -- +4 to every magic skill, in a game where the best
single enchantment gives +8 to one skill -- would be the strongest item in Lionheart by a wide
margin." **Both halves of that are wrong.**

**The +8 ceiling does not exist.** Measured across every `.InventoryAddition` and `.InventoryItem`:

| | bonus | to |
|---|---|---|
| `Spikes Major` | **+25** | `Magic Tribal/Offensive/Spike` |
| `Undead Summoning` | +20 | `Raise Undead` |
| `Wyrm`, `Book of Death` | +15 | `Flame Thrower`, `Magic Tribal/Summoning` |

And for the **like-for-like** comparison -- a *base* (governing) magic skill rather than a single
spell -- the closest analogue is an item this project already repaired:

| | gives | total |
|---|---|---|
| `Book of Death` | +15 to one base skill | +15 |
| **Sceptre of Bone** (fixed in 0.39.0) | **+2 to eight** base skills | **+16** |
| **`The Mage` as described** | **+4 to twelve** base skills | **+48** |

So `The Mage` is roughly **three times the Sceptre of Bone**, which is a defensible place for a
`5 Unique` worth 10,000 -- the most expensive wand in the game -- and nothing like "the strongest item
by a wide margin against a +8 ceiling." Shipped as described, at +4.

**And "nothing but text" was wrong too.** Both were buildable from `Swarm`'s shape; what was actually
missing was the **design decision** about `The Mage`'s magnitude, not a mechanism. There are **12**
base magic skills -- four per category -- which is the number that makes the +4 meaningful:

| category | base skills |
|---|---|
| Magic Thought | Defensive, Electrical, Fire, Ice |
| Magic Tribal | Defensive, Domination, Summoning, Wounding |
| Magic Divine | Defensive, Divine Favor, Fortitude, Smite |

### What they are now

| | implementation |
|---|---|
| **`Fire and Ice`** | **two** `CPlugInBehaviorWand` entries -- Fireball *and* Ice Storm, 5-10 shared charges -- plus +15% fire and cold resistance. Value was **0**; now 8,500, the midpoint of its own already-written 5,000 / 8,500 / 12,000 band |
| **`The Mage`** | Lightning Bolt x5 and Fear x5 as two wand behaviours, **+4 to all twelve base magic skills**, and +10% fire, cold and electrical resistance. Value stays 10,000 |

Both are in `Wand selection MAGIC` at **weighting 5**, matching Swarm; the pool is now
`Array Count=18`.

**A two-spell wand has no vanilla precedent** -- all 16 implemented wands cast exactly one spell, and
no single spell in the game deals both fire and cold, so "at the same time in the same place" could
not come from an existing skill. The plugin array demonstrably holds multiple plugins (Swarm carries
two of different types), so two wand behaviours is the only route that delivers the text without
authoring a 93rd `.Skill` -- which is the structural risk `EH5` exists for. `FI2` is the row that
checks both spells actually surface.

### A latent bug in Swarm, found while copying it

Swarm tops the player's skill up with a bare subtraction:

```
skilllevel = CCacheFirstResult( 30 - CVariableSkill(Insect Plague) )
```

For a player whose Insect Plague is already above 30 that is **negative**, so the wand quietly
*reduces* a real caster's skill. Both new wands guard it instead -- lift the player to the stated
level only if they are below it, otherwise zero:

```
CIfExpression( skill < N ? (N - skill) : 0 )   wrapped in CCacheFirstResult
```

**Swarm itself is left alone for now**, since changing a shipped 0.38.0 item is a separate decision
from building two new ones. Recorded here so it is not lost.

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

### 0.37.0 - Monster Summoning levels 4 and 5

The six cans were wired into the spell's tier ladder. **The tier table is not in the skill** --
`Monster Summoning.Skill` references no cans at all; it fires a `Spellcast` relay and selection
happens in `Spell Projectiles/Monster Summoning Instant Hit Projectile.InventoryItem`. That file
branches on `single` versus `multi` and **the two sides are shaped differently**: single is a tier
ladder on skill value, multi has no skill gating at all and draws from two flat pools.

The single ladder now runs `< 50`, `< 100`, `< 150`, `< 200`, else -- keeping vanilla's own 50-point
spacing, where tier 3 previously covered skill 100 to the cap. The multi high pool grew from 3 to 9.
Tier 4 and 5 blocks are **clones of the tier-3 block with the can names swapped**, so each keeps its
`CAddAIAction` mana upkeep byte-for-byte; both verified at 3 mana.

Two instructive failures on the way: assuming the two branches were identical ladders, and getting
the conditional's fields wrong -- `CIfExpressionAction` takes **`If Expression`**, plus
`Character to get attributes from`, and has **no** `Return failure` tail, unlike `CConditionalAction`.

`SM1`-`SM14` in [`qa.md`](qa.md). **`SM10` is worth knowing in advance**: all six races carry
`Display Name=Black Wolf` in vanilla, so a summoned Rock Titan will probably be *called* a Black Wolf
until that is fixed deliberately.

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

Rewritten after 0.39.0-0.42.0; the previous version still listed items that have since shipped.

**Before picking anything up, classify it.** Three releases of chasing orphans produced the
taxonomy at the end of this document, and the first instinct was wrong every time. An orphan is
either **filename drift** (rename it), an **unreachable branch** (wire it), or a **superseded
draft** (leave it dead). Two superseded drafts have already been caught this way.

### Shipped since this list was last written

| | |
|---|---|
| 0.39.0 | both Trapped Spirit items, the Sceptre of Bone's missing bind step, `Ruler of Calle Perdida` |
| 0.40.0 | `Convince DaVinci to Join the Dark Wielders`, implemented from a 0-state stub |
| 0.41.0 | the Lucius betrayal marker, `1002`, Brother Michel's `400` pair, and six renamed recordings |
| 0.42.0 | Andre's two `900` greetings |

### Open, re-verified after 0.46.0

Re-counted against the **current Fixt build** (earlier releases' work counting as present), not
against vanilla. Two entries this list used to carry turned out to be shipped and two were wrong.

**Genuinely unreferenced, and the mechanism is already there:**

| | refs | what makes it cheap |
|---|---|---|
| **`Goblin Slayer`** | **0** | `Goblin Kill Counter.DerivedCharacterAttribute` is live and **7 maps write to it**. The perk exists with `Display Name=Goblin Slayer` and **no actions at all** -- a title granted by nothing. This is a threshold read away. **The trap:** `Bounty Hunter Camp.zax` looks like it references the perk, but the match is an entity named `Goblin Slayer Xp Giver` -- a substring collision, not a grant |
| **The three `FACTION * Killer` perks** | **0** each | Their display names are already written and good: *"Enemy of the Inquisition"*, *"Enemy of the Knights Templar"*, *"Enemy of the Wielders"*. A shipped pattern with a working quarter as reference. Needs a decision about where detection lives -- a per-member death slot rather than a map trigger -- but invents nothing |
| ~~`Inquisitor Feralkin Journal`~~ | -- | **done in 0.50.0** -- added to Weng Choi's rotation as its 11th book, to his rare-book check as its 10th, and noticed by an inquisitor |
| `Bolt selection MAGIC` | **0** | the last loose end in the magic pipeline. `Boot`, `Gauntlet`, `Necklace` and `Arrow selection MAGIC` each resolve from exactly **one** map, so only `Bolt` is truly adrift |

**Reachable only from a test map:**

| | refs | |
|---|---|---|
| ~~wands `Fire and Ice` and `Mage`~~ | -- | **built in 0.49.0** from `Swarm`'s shape, and pooled at weighting 5 |

**Open and real, but awkward:**

| | |
|---|---|
| `100 Respond ask about Tank` in `8 Alamut/Dialog/DaVinci Ending.DialogTree` | the node is present with **0 incoming links**. Act 8, and the act-8 `Siege Tank` part is `Active=0` and activated from elsewhere, so it is its own job rather than a tail of 0.43.0 |
| `GrandInquisitor / 120 combat.ogg` | 172 KB, and **statically undecidable** -- see below |

### The Grand Inquisitor's orphan recording cannot be placed from the files

Measured properly: the tree has **51 nodes and 48 recordings**. Exactly **one** recording has no
node (`120 combat`) and **four** nodes have no recording:

| nodes with no recording |
|---|
| `1100 Player attacks` |
| `1100 Spellcast detect` |
| `1200 do not bother me` |
| `413 rogue inquisitors` |

So this is **filename drift** in shape -- a renumbered node -- but there are **two** plausible combat
destinations for one combat recording, and attaching it to the wrong one silences the right node
forever while playing the wrong line. It cannot be resolved without listening to the file. Recorded
as blocked on that, not as buildable.

### Two corrections to this list

**The Titan items are superseded drafts -- do not restore them.** Their only references are to their
**inventory icon art** (`Items/Inventory Images/Quest Items/...`), not to the items, which is the
art-path/item-path collision this document warns about further down. Their own descriptions give them
away against the live items that reuse their icons:

| | description | superseded by |
|---|---|---|
| `Titan Crystal` | *"Large and unwieldly. Smells bad."* -- a dev joke | **`Lucius' Mneme`**, which uses the Titan Crystal icon |
| `Titan Sphere` | *"Spirit gem"* -- a bare label, not prose | **the four named stonehearts** (Lethos, Iapetus, Menoetius, Rhea), which use the Titan Sphere icon and have real prose: *"cold, heavy, and inert"* |

Same shape as the Horror: a generic draft replaced by named versions, with the art carried over.

**"The 17 Nostradamus English" was wrong -- it is 2.** There are **14** `Nos *` monster cans and
**12 of them spawn**. The only two that do not are `Nos Ogre2 English` and `Nos Ogre2 English Tough`,
and those are the same `Ogre strong`-model tier drafts already identified above -- not a lost
garrison. Nothing here needs level design after all.

### Shipped since the previous version of this list

| | |
|---|---|
| 0.43.0 | `DaVinci Tank Gear`, via the Magic Machine's three prices |
| 0.44.0 | `Hangover Cure Potion`, across two acts and three people |
| 0.45.0 | the horse |
| 0.46.0 | the creatures sent after Machiavelli, and the level gate on his quest |

### Settled: do not pick these up

| | why |
|---|---|
| `Help Andre the Titan with his tasks` | superseded by the live `Recover Lucius' Mneme` (6 states, 5 activated) |
| Blacksmith `80 Do You Have The Item I Need?` | superseded by the live `07 what more`, which has 15 replies against its 13 including a quest hand-in |
| `Juanita Suarez / 200 my fee`, `GoblinKhan / 400 Where are you going` | recordings exist but the nodes are `Should Have Voiceover=0`; possibly silenced deliberately |

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

### 6. Checking one link and calling the chain connected

The magic-items section originally reported that 62 of 65 orphaned recipes were redundant because
`Generator Combinations` reached their enchantments. It does -- but **nothing reached
`Generator Combinations`**. The check stopped one link short.

It was caught only because wiring three wands into `Wand selection MAGIC` would have been three
correct edits to a pool nothing draws from, and tracing the chain before building showed
`All Wands` had no referrers at all.

**The rule: trace a reference chain to something that actually runs** -- a map, a drop table, a
merchant -- not to the next file that mentions it.

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
- Trace a chain to something that **runs**, not to the next file that mentions it.

## Done in 0.39.0 - the Enchanter's Bargain

**The two Trapped Spirit items** shipped as shells: correct slot, art and grouping, but
`Is Magic=0`, value 0, only pickup/putdown behaviours, the placeholder description "The abilities
of this amulet are a mystery", and referenced by nothing. They are now the reward for the Trapped
Ether Plane's non-lethal resolution -- the one route of the three that vanilla paid nothing for,
while both lethal routes drop `Kublai Khans Sword`. Amulet for sparing the Enchanter, Ring as well
for allying him to Relican, and a counting set bonus on `Number of Trapped Spirit Items`.

**`Wielder DARK Quest Rod Bone NO Spirit`** was referenced by nothing at all, against 3 files for
the spirited version -- while the Wielder path's equivalent shell is referenced by 3 and has a whole
quest (`Bind Spirit to Rod`, Galileo and the Observatory) for filling it. The Dark Wielder
initiation had the same two items and no middle step. DaVinci's chamber now yields the shell and the
spirit is bound at the ether plane, with Relican binding it himself as a fallback so the initiation
can never dead-end.

**`Ruler of Calle Perdida`** -- "Dark Lord of Calle Perdida" -- was granted by nothing, though its
text describes the Summoning Ring's Yes branch word for word and its sibling
`Exposer of Calle Perdida` is granted by `InquisitorRaphael.DialogTree`. Now granted on that branch.

**Still open on this path:** `Convince DaVinci to Join the Dark Wielders` -- but see the
section below; calling it "an unreachable fifth Dark Wielder task", as this document first
did, overstates it badly. And
`Rod Spirits WITH Spirit`, the *Wielder* rod, advertises "2 skill points in the Divine and Thought
spell disciplines, as well as 25 to Mana Capacity" and implements none of it: zero
`CCharacterModifierSkill`, its only derived modifier being attack-animation speed.

**A method note worth keeping.** The Mad Enchanter was findable as Relican-adjacent only by reading
`Race=` and `Model=` rather than names or dialogue: `Trapped Wizard.can` and `Relican.can` are the
only two cans in the game using `Races/NPCs/Relican` and
`Characters/NPC/Barcelona/Wielders/Relican`. Searching the writing for a connection between them
finds nothing, because the connection was only ever made in the art and the statistics.


## Two method corrections, and what they cost

### An empty quest file is not evidence of a cut

**33 of the game's 151 quest definitions have `Item Count=0`** -- 22% of them. Three are
**containers** whose children carry the journal text (`Initiation Quest for the Inquisition` has 6
children, `Initiation Quest of the Knights Templar` has 7). The other 30 have no states *and* no
children.

But several of those 30 are content that is unquestionably **in the shipped game**:

| empty, orphaned quest file | yet in the game as |
|---|---|
| `Find the Hair of a Saint` | state `7PL8VY1D` of `Create a Rod of the Inquisitor` |
| `Discover the location of La Calle Perdida` | playable; tracked elsewhere |
| `Find and rescue Galileo` | playable; Galileo is rescued in the Inquisition chambers |
| `Find the Yellow Node within the Sewers` | named in `Lord Relican.DialogTree` |

So these 33 files are a **vestigial design-era quest list**, not an inventory of cut features. The
journal text for the live ones lives under *other* quest definitions.

**The cost of getting this wrong:** reference-counting flags an empty stub identically to genuinely
cut content such as `Wielder DARK Quest Rod Bone NO Spirit`, and the two are nothing alike. The
sceptre shell had a complete item definition, an authored description, art and a slot -- everything
but a placement. `Convince DaVinci to Join the Dark Wielders` has a filename. Do not report them in
the same breath, which this document did until 0.39.0.

### Orphaned voiceover is the strongest signal there is

VO lives in a `<TreeName> VOs/` folder beside each `.DialogTree`, one `.ogg` per node, named for the
node ID. So a recording whose node no longer exists is a line that was **written, cast and
performed**, and then unhooked.

**Method confidence, measured before trusting it:** across **1,330** recordings in **50** paired VO
folders, **1,314 (98.8%)** match a node by name. An orphan therefore means something.

**Result: 16 orphaned recordings across 11 trees.** The largest cluster is a coherent betrayal
storyline with no dialogue nodes at all:

| tree | orphaned recording | size |
|---|---|---|
| `TitanAndre` | `1001 Lucious Exposed` | **293 KB** |
| `TitanAndre` | `1002 Hearts in Hand but Lucious betrayed` | **306 KB** |
| `TitanAndre` | `1003 Return after the quest is complete but Lucious betrayed` | 55 KB |
| `BrotherMichel` | `400 Lucious thrown out of town` | **149 KB** |
| `BrotherMichel` | `400 Lucious thrown out of town 2` | 25 KB |

Five lines, roughly **830 KB of finished voice acting**, two named Montaillou characters, one plot.
Two of them are near 300 KB, so these are speeches rather than barks. Lucious exists as a character
besides: `Rock Titan Lucious.can`, three race files including two Toulouse variants, and his own
named combat set (`Lucious Titan_attk/death/hurt`).

**That reading was wrong, and the section below corrects it.** The nodes were never deleted; they
exist and most of them are reachable. The recordings are silent because their *filenames* kept an
older spelling of the character's name. See "The Lucius thread" below.

The other orphans, one or two per tree: `Captain Isabella` (2, Grace as a companion), `Shylocke` (2),
`Blacksmith`, `DaVinciBarcelona`, `Cervantes` (`500 convince don quixote 2`), `GrandInquisitor`
(`120 combat`), `SirAuric` (`400 attack auric alt`), `Juanita Suarez` (`200 my fee`), `GoblinKhan`
(`400 Where are you going`).

## Convince DaVinci to Join the Dark Wielders -- the verdict

Asked repeatedly whether this is restorable. It is not *restorable*, because nothing was built:

| evidence | finding |
|---|---|
| quest definition | `Item Count=0`, `Sub-Quest of=!None`, no children, registry-only reference |
| his dialogue | **112 nodes, zero** mentions of Relican, Dark Wielders, necromancy or the Dark Arts |
| his voiceover | 127 recordings, **none** dark; his single orphan is `1001 goodbye montaillou` |
| dark-path VO game-wide | **50 files**, every one Relican's, Cedric's, or Relican's combat grunts |
| Relican's dialogue | 27 nodes, never mentions DaVinci at all |

Compare its wired sibling `Convince Quinn the Herbalist to Join the Dark Wielders`: 3 states with
journal text, parented to the Dark Wielder initiation, a reply attached at **7** places in Quinn's
tree, and a `700`/`710`/`720` branch with three gated persuasion routes.

**And there are two reasons the design outgrew it.** DaVinci is already a Wielder with his own ether
pocket -- *"Wielders who know how to access this plane can learn to shape their own domains here -
though mine is modest, there are larger ethereal pockets"* -- and he is the **referral to the good
Wielders**: *"If you seek the Wielders, go to Quinn and mention that I sent you."*

More decisively, **`Races/NPCs/Wielders/Leonardo DaVinci` is AC 1000 / HP 10000**, the same
deliberate-immortality pattern as the game's children. He is unkillable on purpose, because
`08 Final Encounter.zax` carries **232** DaVinci references and its endings are a matrix over
{Old Man escapes / killed / talked to death} x {DaVinci alive or dead} x {Galileo alive or dead} x
{player good or evil}. His life is already an ending variable, resolved in act 8 by a scripted
attacker.

So Quinn's quest shape -- *"Convince him to join us or destroy him"* -- **cannot** be given to
DaVinci. The "or destroy him" half is precisely what the developers engineered away. Any
implementation has to be persuasion-only, which is also what makes it mechanically distinct: the
only Dark Wielder task that cannot be solved with a sword.

**Implemented in 0.40.0** as persuasion-only, with three parallel routes (`Speech moreequal 50`, a
`COR` of vanilla's `General Thought/Tribal Skills moreequal 80`, or holding the Ring of the Trapped
Spirit from 0.39.0's pact), an ungated attempt that fails, and a back-out that leaves it retryable.
Refusing withdraws nothing -- he argues the player off the path instead -- and both outcomes call
`CSetQuestSatusToCompletedAction` so no journal entry dangles. Offered on Relican's hub rather than
inside the task 1-2-3 chain, so it is genuinely optional. `LD1`-`LD16` in [`qa.md`](qa.md).

Still untouched on this path, and deliberately: no kill option, and nothing reaching act 8.


## The Lucius thread, and a bug class worth more than the thread

### Andre is Lucius, and his storyline ships complete

The first claim made about this -- five recorded lines with their nodes deleted -- was wrong in
every part. `Andre the Titan.can` has `Race=Races/Enemies/Toulouse/Rock Titan Lucious`. The
"Lucious" race files are **his own**. Lucius is Andre's real name, and his storyline is shipped,
wired and playable.

What it is: Andre is a rock titan hiding in Montaillou, passing himself off as the town's
protector. He asks the player to keep his secret and to kill the titans of Toulouse -- who are his
own tribe's elders, the ones who exiled him. They are all in the game under Greek titan names:
**Rhea, Lethos, Iapetus, Menoetius, Klao, Mathuo, Tereo, Baktron, Poimaino, ephebos**.

> **`820 PC Saves the day`:** *"you must slay all of the titans in Toulouse. You must do it
> quickly, and without mercy."*

> **`1000 Hearts in Hand`:** *"Ah, I see it is true, you have slain them. Ah, Rhea, I am sorry I
> had to do this to you, but it was you or me."*

> **`1001 Lucius Exposed`:** *"These cold hearts belonged to the other elders of my tribe, the ones
> who forced me to run for my life."*

The player can keep his secret for gold or expose him to the mayor, which changes his closing
lines. There are nodes for tricking him, convincing him, letting him flee, killing him, and him
being run out of town -- 151 mentions of Lucius in his tree alone.

### His name is spelled six ways

| where | spelling |
|---|---|
| character template, portrait | **Andre** |
| his race files, his monster can | Rock Titan **Lucious** |
| dialogue node IDs | **Lucius** |
| voice recordings | **Lucious** |
| quest journal `Name=` | Help **Marcus** the Titan |

### The bug class: a filename apart from its node is silent forever

There is **no VO-file field anywhere in any DialogTree** -- zero `Voiceover File`, `VO File` or
`Voice File` across all 131. Voiceover resolves purely as `<TreeName> VOs/<Node ID>.ogg`. So a
filename that disagrees with its node ID by one character is a line that can never play.

Measured against the **current** files rather than vanilla -- which matters, see the method note
below -- the 16 exact-match misses split four ways:

| | count | note |
|---|---|---|
| **silent, reachable node, recording misnamed** | **3** | fixed in 0.41.0 |
| silent, but the node is **unreachable in vanilla** anyway | 4 | renaming achieves nothing; needs wiring |
| flagged `Should Have Voiceover=0` | 2 | a rename alone would not play them; possibly silenced on purpose |
| spare alternate takes (`alt`, `2`) | 4 | the node has its own recording too; working as intended |
| no node resembles it at all | 1 | `GrandInquisitor / 120 combat`, 172 KB, unexplained |

Plus 2 that an **earlier Fixt release had already fixed** (`Captain Isabella`, where vanilla's
node names were `asks to return` and `rejoined companion`).

**The 4 unreachable ones are the interesting remainder**, because the audio is finished and waiting:
`1002 Hearts in Hand but Lucius betrayed` is the betrayal variant of Andre's ending;
`400 Lucius thrown out of town` and its `2` sibling are Brother Michel's reaction to it; and
`80 Do You Have The Item I Need?` is a Blacksmith line. Nothing links to any of them. Restoring
those is a wiring job, not a rename, and it needs a decision about where each should branch from.

### Two method corrections

**Run the VO diff against `files/`, not vanilla.** The first pass used `zf.read()` and so reported
two Captain Isabella lines as broken when an earlier Fixt release had already repaired them. This
is the mirror image of the rule that edits must be sourced through `lhbuild.read()`: sourcing an *edit* from vanilla
destroys work, and sourcing an *audit* from vanilla invents work.

**Renaming a node that was already orphaned in vanilla creates a false reachability failure.**
`reachability.py` tolerates 190 nodes that vanilla itself never links, matched **by name**. Renaming
one makes it look like a brand-new orphan. That is what flagged 4 of the 7 renames first attempted
here, and it is a useful signal rather than a nuisance: it distinguishes "silent line the player
could hear" from "silent line on a node the player can never reach."

### The quest that cannot start is a superseded duplicate -- leave it alone

`Help Andre the Titan with his tasks.Quest.txt` has two states, **`7LOVAAS1`** and **`3MGFA36C`**,
and nothing activates either, so it can never begin. Its journal name reads *"Help Marcus the
Titan"*, naming a character who is not in the game.

**It should stay dead.** Its two states describe *"Find Marcus' cousin and take sphere from him"*
and *"Return Sphere to Marcus"* -- and that material is covered by a **live** quest,
`Recover Lucius' Mneme.Quest.txt` (journal name *"Retrieve the Crystal Mneme from Lucius"*), which
has **6** states, **5** of them activated by real maps, cans and dialogue trees. Andre is "Memnos,
the Eater of Memories"; the Mneme quest is the finished version of the same idea, written after the
character stopped being called Marcus.

Wiring the old one would put a duplicate entry in the journal beside the live quest. The name fix
was built and then reverted for the same reason: on a quest that never activates it changes nothing
a player can see, and bringing the file into `files/` turns `validate.py` permanently red on the two
dead states.

One genuine loose end inside the live quest: state **`QYINZUKM`** (*"You have decided to allow
Lucius to live..."*) is activated by nothing, though its siblings `496ZH7F7` and `Q8U40TYQ` cover
the stay-out-of-it outcome, so the branch is not lost.


## Wired in 0.41.0 - the betrayal nobody could trigger

The root defect: `951 Furious Mayor` fires
`COtherMapAction{CActivateAction{Target Name=Lucius thrown out}}` into `01 Hamlet Exterior`, and
**no entity of that name was declared in any map in the game**. The flag could never be set, so
every consequence hanging off it was dead. The developers knew -- that reply carries the note
**`Action work in progress=kick luscious out, seal of this branch`** (an eighth spelling of the
name, after Andre, Lucious, Lucius, Marcus and `Lucious dead`).

Its sibling marker `Lucius extorted` **is** declared in that map and **is** read by `TitanAndre`,
which gave an exact template for both the entity and the check. The pattern is well attested: 40
vanilla markers are read positively by `CCheckExistenceAction`, declared `Active=0` with
`Model=Editor/Checker` and switched on by `CActivateAction` -- among them `Beggars dead`,
`Blacksmith offered payment`, `Darsh is Dead` and `Has Cervantes Been Jailed`. (The opposite
convention also exists: 30 markers start present and are **deactivated** to record an event, which
is how `Relican started giving quests already to player` works. Read which direction a marker uses
before writing a check for it.)

**What was connected:**

| | before | after |
|---|---|---|
| `Lucius thrown out` marker | declared nowhere | declared in `01 Hamlet Exterior`, `Active=0` |
| `1002 Hearts in Hand but Lucius betrayed` | 0 incoming links | 3, one beside each loyal hearts reply |
| `400 Lucius thrown out of town` (+ ` 2`) | 0 incoming, no replies | opened as a greeting pair, copying this tree's own `Lucious dead` -> `05`/`07` `CSeriesAction` shape |
| `1003 Return after ... betrayed` | opened for **every** post-quest return | now requires betrayal as well as quest completion |

That last row was a live defect in its own right: a player who kept Lucius's secret was given the
cold shoulder they never earned.

`reachability.py`'s tolerated vanilla-orphan count fell from **190 to 187**, which is exactly the
three nodes connected -- a cheap, precise confirmation that the wiring took.

**And then the renames became worth making.** Three recordings were renamed to match these nodes
earlier in the session and immediately reverted, correctly: while the nodes were unreachable,
matching their audio achieved nothing and merely disguised three known vanilla orphans from the
gate. With the nodes wired, the renames landed: **0.88 MB** of recorded dialogue across six lines
now plays that never did.

**Andre's own two post-betrayal greetings were wired next**, in 0.42.0 -- see below. The
Blacksmith's `80 Do You Have The Item I Need?` was investigated next and should **stay** dead -- see
below.

Also noted while here: `Titan Andre requires PC to have sphere from other titan.can` is an **empty
canned requirement** (`Object=` with no value), one of the 27 already on this list.


## Wired in 0.42.0 - Andre's own reaction to being sold

The last two orphans on this branch, both voiced and both with **0** incoming links in vanilla:

> **`900 Lucius thrown out of town`** (96 KB) -- *"You are a very, very bad man and you lead a trite
> and meaningless existence. Now leave me alone."*

> **`900 Lucius extorted and thrown out of town`** (84 KB) -- *"I paid you your blood money and
> still you betray me! I have had all I can stand from you, runt!"* -- and its reply carries
> **`CGoToCombatAction`**, so he attacks.

Unlike the six lines renamed in 0.41.0, **these two recordings were already correctly named**. They
were silent purely because nothing could reach the nodes. That is worth separating: filename drift
and unreachability are two different faults, and only the second one applies here.

Two flags decide between them and both now exist: `Lucius thrown out`, declared in 0.41.0, and
`Lucius extorted`, which is vanilla's own, set by five replies in `TitanAndre` that also hand over
gold.

**The ordering.** The shipped cascade in both `Lucius Wrasslin` and `Talked past Lucius` is kept
byte-for-byte and demoted inside two new tests:

| test | result |
|---|---|
| betrayed **and** extorted | `900 Lucius extorted and thrown out of town` -- he fights |
| betrayed **and** titan hunt unfinished | `900 Lucius thrown out of town` -- the brush-off |
| *the shipped cascade, unchanged* | quest complete + betrayed -> `1003`; else Mneme -> `03`; else `02` |

Taking his hush money and selling him anyway is the worst thing available on this branch, so it
outranks everything. The `NOT quest completed` on the second test is what keeps 0.41.0's `1003`
reachable -- a betrayer who finished the hunt still gets the terse post-quest dismissal rather than
the generic one.

`reachability.py`'s tolerated vanilla-orphan count fell **187 -> 185**, exactly the two nodes
connected.

**Running total for this one branch: 1.05 MB** of recorded dialogue across eight lines that the
shipped game could never play -- six silenced by filename drift, two by unreachable nodes.


## The Blacksmith's node 80 is a superseded draft -- do not wire it

`80 Do You Have The Item I Need?` in `Blacksmith.DialogTree` has 0 incoming links, no map opens it,
and an 81 KB recording sitting beside it under the name `80 Do You Have The Item I Need` (no
question mark). On the surface that is the same shape as the Lucius orphans. It is not.

**What it is.** The smith's answer when a commission is ready: *"Yes, I have finished it - que
aproveche! Is there anything else you wish to see while you are here?"* -- followed by a 13-reply
hub.

**Why it must stay dead.** That role is filled by **`07 what more`**, which is live, voiced,
reachable from both hand-over nodes, and **better content**:

| | `80` (orphan) | `07 what more` (live) |
|---|---|---|
| replies | 13 | **15** |
| reachable | no | yes, from `63 here is your shield` and `64 here is your scimitar` |
| recording | present but misnamed | present and correctly named |
| Red Ore hand-in reply | **absent** | *"Here is some Red Ore. Can you use it to complete Davinci's design"* |
| tainted-race variant reply | absent | present |

Nine of node 80's thirteen replies are identical to `07`'s. The four that differ are the ones `07`
has and `80` lacks -- including **a live quest hand-in** for the Red Ore that Cortes' arm needs.
Wiring node 80 would duplicate a working hub *and* hand the player a worse menu that silently drops
a quest step.

**And the premise was designed out.** Node 80's title is the player asking *"Do you have the item I
need?"*, which no reply anywhere asks -- because in the shipped flow the smith does not wait to be
asked. The map opens `63`/`64` directly when the commission is ready and he hands the item over
unprompted, closing with *"Is there anything else Eduardo can do for you?"* -> `07 what more`. The
question node 80 answers stopped existing.

## The three kinds of orphaned node

Three releases of chasing these has produced a taxonomy worth keeping, because the right action
differs completely:

| kind | evidence | action |
|---|---|---|
| **filename drift** | node reachable, recording present under a near-miss name | rename the node (0.41.0, 6 lines) |
| **unreachable branch** | node unreachable, flag or link missing, no live replacement | wire it (0.41.0 and 0.42.0, 5 nodes) |
| **superseded draft** | a *live* node fills the same role with equal or better content | **leave it dead** |

Two superseded drafts have now been found and correctly left alone: `Help Andre the Titan with his
tasks` (replaced by `Recover Lucius' Mneme`) and the Blacksmith's node 80 (replaced by
`07 what more`). In both cases the giveaway was the same -- finding the live node that does the job,
and checking whether it is *better*. Reference-counting alone cannot tell these three apart, and the
first instinct in every case was wrong.


## Done in 0.43.0 - the turret ring

`DaVinci Tank Gear` was the last hand-authored quest item referenced by nothing. **Cortes' arm did
not supplant it** -- the crossbow (`DaVinci Crossbow Gears`, live), the arm (`Cortez Arm Gears` +
`Cortez Arm Rod`, live) and the tank are three separate projects, and the tank was the only
unfinished one.

**Half the quest already shipped**, which is why this was the cheapest lead left: the hidden chamber
exists and is furnished, the war machines are modelled in it (`DaVinci Objects/Catapult`,
`DaVinci Objects/Death Machine`) and examinable through `1 Catapult` / `1 Sweeper` /
`1 Siege Tank` -- all three saying the machine is **incomplete** -- and DaVinci states on screen
that the engine needs a spirit, feeding the **live 4-state** `Obtain the Spirit Gem for DaVinci`.
Only the gear half was missing.

**Two drafts were discarded, and the reasons are the useful part.** The first sent the player to
Eduardo the blacksmith, which made the whole quest "go and talk to a man" -- and was wrong on the
content too, since gears in this game come from the talking steam engine, which already sells
`DaVinci Crossbow Gears` for a potion at `650 collect gears`. The second put the machine at the
centre but let the player keep or break its promise with two replies **at the hand-over**, in the
secret chamber: the machine is not in that room, and a promise breakable only by pressing a button
marked "break it" is a menu rather than a promise.

What shipped: three prices (a potion, consumed; `Barter moreequal 35`; or the promise), all
converging on one gear. The promise **outlives the quest** -- the gear is handed over and the quest
completes in the chamber, but the debt can only be settled afterwards at
`3 Return Dialogue Workshop`, with the engine in earshot, exactly where it demands. It is broken by
never going back; there is no betrayal option at all.

**Still open on this thread:** `100 Respond ask about Tank` in `DaVinci Ending.DialogTree`
(*"Time will tell if it does us any good..."*, 0 incoming links, act 8), and the act-8 `Siege Tank`
part is `Active=0` and activated from elsewhere. That is its own job on the far side of the game.


## Done in 0.44.0 - the morning after

The `Hangover Cure Potion` was a shell item referenced by nothing, and three live things could not
reach each other:

| what shipped | state |
|---|---|
| `1500 return after give gold` (the Drunken Boxing drunkard) | live, map-opened, **zero replies** |
| Quinn's `30 Special Order` | live: *"I can brew a concoction to cure many afflictions of the mind and body... come to me"* -- unacceptable by anything |
| `Gather Nightshade Root for Quinn` | a **0-state stub** |

Joined into: he asks after Montserrat -> Quinn needs nightshade, which *"does not grow south of the
mountains"* -> **Na Roqua in Montaillou** gives it free with a warning about the dose -> Quinn brews
it -> he drinks it and teaches **`Clear Head`** (+3 Find Traps and Secret Doors). The third entry in
Fixt's own Quinn ingredient series, after `Troll Hide` and `Wasp Stingers`, and the only one with a
scene at both ends.

**Montaillou rather than Montserrat** because Montserrat's grove has no containers and no
herbalist -- its druids are act 7 content -- so the root would have needed placing by coordinate in
an 1,087-part map. **No new art:** the root reuses `RareHerb_PU`, which `Darkwood` already uses.
**The perk is authored, not restored** -- all nine NPC-given perks are already granted -- and mirrors
`Drunken Boxing.Perk` including its impossible level-up guard.

### A method rule this release produced: requirement cans do not resolve across levels

Measured rather than assumed, because the first build put Barcelona gates in reach of an act-3 tree:

| a bare `Requirement=` name resolves from | vanilla cases |
|---|---|
| the global `Resources/Dialog/Requirements` | **335** |
| the dialogue tree's own folder | 220 |
| a different district in the **same level** | **26** -- e.g. `Magic Machine` reading a Port District can |
| a different **level** | **0** |
| unresolved | 0 |

Cross-district is shipped practice, so 0.40.0's `Fixt DaVinci *` cans in Gate District read from La
Calle Perdida are fine. **Cross-level never occurs**, and `validate.py` does not check it: the gate
would evaluate as nothing and silently hide its reply with no error anywhere. For any chain spanning
acts, put the cans in the global root. Every Fixt dialogue tree has since been audited -- zero
cross-level or unresolved references.


## Done in 0.45.0 - the horse, and what the "unused enemies" number actually means

### The horse

`Monster Cans/Animals/Horse.can` -- a complete 54 KB can with a 36 KB model, a cached render and
its own 27 KB death sound -- was placed in **zero** maps. Its animation set is **Idle, Walk, Death**
and nothing else (the Deer has four, the War Golem ten including two attacks), so it was built as an
**ambient animal**, and it was the only one of them never used:

| Wolf Gray | Deer | Chicken 01 / 02 | Horse |
|---|---|---|---|
| 16 maps | 5 maps | 3 maps each | **0** |

Its `Race=Wolf Gray` was first read as evidence of being unfinished. **Wrong** -- the other ambient
animals borrow stat blocks the same way. Now Alvaro's cart horse at the Crossroads, with
`CSetDamagedScriptActionAction` -> a relay -> `CGoToCombatAction{Enemy Name=Alvaro}`, copied from
Alvaro's own generator. `HR1`-`HR12` in [`qa.md`](qa.md).

### The "48 enemy cans spawned nowhere" entry was misleading and is replaced

Recounted against every reference form, not just map `Entity=`: **56** of 611 monster cans are
referenced by nothing. But sorted properly, almost none of it is lost content:

| kind | roughly | what it actually is |
|---|---|---|
| **tier variants** of live families | ~30 | `Super` / `Tough` cans whose base spawns normally. The generators' mojo bands never reach them -- a **balance** observation, not cut content |
| **duplicates** of live cans | ~15 | `Mongol Goblin Grum` and `Goblin Grumdjum` share race **and** model; same for `Mongol Goblin Rakeb` / `Rakeb`. `Sewers/Sewer Theif Boss` ×3 duplicates `Thugs/Theif Boss` ×3, which is spawned |
| **test / broken** | 2 | `Simon Spell Cast Test`; and `Horse`, now placed |
| **draft cans with no unique art** | **4** | see below -- I called these "genuinely distinct" and that was **wrong** |

### Correction: the four "genuinely distinct" cans are drafts, and none has its own art

0.45.0 claimed **`Horror`** was "the only unused enemy in the game with a dedicated mesh" and "the
best remaining enemy lead by far." **Both halves are false.** I matched a *folder name*
(`Models3D/Enemies/Horror/`) and reported it as a dedicated asset -- the exact inverse of this
file's own **find cut content by asset, not by name** rule. Hashing the meshes settles it:

| mesh | sha256 (12) | also at |
|---|---|---|
| `Enemies/Horror/Terror.MODEL.gr2` | `0a42036b5b1b` | `Terrors/Models/Terror/`, `English Priestess/`, `Mimic/` -- **4 byte-identical copies** |

**`Horror` is an early draft of the shipped `Terror`**, and the Terror is one of the most-used
enemies in the game: 21 live cans spawning **823** times across 200 maps. Horror spawns 0 times. The
proof is layered:

| | Horror (unused) | Terror (live) |
|---|---|---|
| mesh | byte-identical to the Terror's | same file |
| animations | byte-identical to `Terrors/Shared Animations/original/` | **points at that same `original/` folder** |
| `Race=` | `Races/Demokin` -- a **player** `CRace`, no presets | `Races/Enemies/Undead/Terror` |
| death sound in `.mdl16` | `Enemies/Orc Death.ogg` -- an **orc** sound on an undead | `Terror Death` + `Death2` + `activate` |
| model cache | 8,630 bytes / 79 strings | 37,991 bytes / 540 strings |
| behaviour | none | `CPatrolAreaAI`, `Can Be Knocked Around`, Medium Disease damage/duration |
| can size | 42,978 bytes | 57,518 bytes |

The live Terror's own cache still loads `Shared Animations/original/` -- so `Enemies/Horror/` is not a
leftover beside the real art, it **is** the pre-reorganisation copy of art that is still in service.
This is kind three of [the orphan taxonomy](qa.md): a **superseded draft**, and the action for those
is to **leave it dead**. There is nothing here to restore.

Two signals were tested and **discarded** rather than relied on, because both looked damning and
neither is:

- **`Sound=...wav` paths that do not exist.** Horror has three. So do **147 of 1,698** cans, live
  ones among them (`Terror Super`, `Goblin King`, `Old Man of the Mountain`). A vanilla wart, not a
  dating artifact.
- **`Display Name=unnamed`.** Horror has it. So do **421 of 478** monster cans. Not a signal at all.

The other three fall the same way -- all four share art with live families:

| can | model | shared with | verdict |
|---|---|---|---|
| `Horror` | `Monsters/Horror` | the live Terror's mesh, 4 copies | draft of Terror |
| `Caster` | `Rock Titan` | **15** cans incl. `Andre the Titan` | tier draft; the titans are live |
| `Nos Ogre2 English` ×2 | `Ogre strong` | 6 cans, all live ogres | tier draft |
| `Assasin EarlyLevels` | `Assasin` | 6 cans, all live assassins | tier draft |

**So the honest count of genuinely distinct unused enemies with their own art is 0, not 4.** Every
unreferenced monster can in this game is a tier variant, a duplicate, a draft, or a test.

### What the Horror hunt actually turned up: a live act-1 quest shipped broken

The one signal that survived was rare: **`Race=` pointing at a *player* race**. Only **3** of 478
monster cans do it -- and the third is spawned.

| can | refs | |
|---|---|---|
| `Horror` | 0 | draft |
| `Assasin EarlyLevels` | 0 | draft |
| **`Assassin Machiavelli`** | **1** | **live, in `1 Barcelona/House of Ilk map.zax`** |

**The name misled me twice and the map settled it.** `Assassin Machiavelli` is not Machiavelli-the-
assassin; it is *the assassins sent after Machiavelli*. `House of Ilk map.zax` holds a complete
**act-1 escort quest** -- `Machiavelli generator`, `Protect Mach`, `Mach Reward`, `saved machiavelli`,
`Swap Mach Dialogue`, `gavekarma`, four `Machiavelli Exit` parts -- and all of it is **live**:

| part | state |
|---|---|
| `Machiavelli generator` | `Active=1`, spawns `Character Templates/Temple District/Machiavelli` |
| `Protect Mach` / `Mach Reward` / `saved machiavelli` | `Active=1` |
| `Trigger Assassins Relay` | `Active=0`, armed by the quest -- correct |
| `Machiavelli Door` in `Temple District.zax` | `Active=1`, dialogue hooked up |

Machiavelli hires you as a guardian (node `75 Task 2`: *"These plans have earned me dangerous
opponents that seek to end my ambitions and my life"*), the ambush fires as you leave
(node `150 Machiavelli Attacked when you leave his building`), and saving him pays out in Barcelona
and again in Montaillou (node `300 machiavelli helps you in montaillou`). It ties into the Slaver
Cells opening and the Master of Assassins.

**The four attackers arrive with no stats at all.** All four generators spawn the one can, whose
`Race=Races/Demokin` is a plain **`CRace`**: character-creation attribute ranges, no
`DerivedCharacterAttribute` array, no `Skill` array, so there is nothing to inherit. The player can
even see it -- `Races/Demokin` has `Display Name=Demokin`, so the creatures attacking Machiavelli are
**labelled "Demokin"** in-game.

**The control that makes this airtight:** `Assasin.can`, which has a correct race, *also* carries
`(HP) Hit Points=0`, `(AC) Armor Class=0` and `OneHandedMelee=0` in the can itself. Can values are
placeholders filled from `Race=` at spawn, so a race with no presets yields nothing. Same class as
the four self-referential wererat/thief templates; same symptom -- dies in a couple of hits for no
visible reason.

#### Which family -- settled by vanilla's own words, not by the name

The can's `Model=Characters/Monsters/Snake Women` is the same model the **12 live `Snakebreed*`
cans** use, so the asset says snake-women. The authored dialogue says the same thing twice, which is
what makes it certain rather than inferred:

> **`210 Assassins`:** *"Those were **creatures** sent by the infidel assassins from the East"*
> **`200 Saved Machiavelli Return Greeting`:** *"you must tell me about those **creatures**"*

Creatures *sent by* the assassins -- not assassins. So the Snakebreed family is correct and the
assassin races are not. Had I gone by the can's name I would have given them AC 280 / HP 150 /
melee 75 instead of the Snakebreed's gentler band, and made a wrong guess permanent.

| | `Races/Demokin` (shipped) | `Snakebreed` | `Snakebreed Boss` | `Snakebreed Venom` |
|---|---|---|---|---|
| (AC) Armor Class | **nothing** | 150 | 175 | 160 |
| (HP) Hit Points | **nothing** | 60 | 100 | 50 |
| skill | **nothing** | melee 30 | melee 35 | **ranged 25** |

**Fixed in 0.46.0** as 1 Boss leader + 2 base + 1 ranged Venom, placed by distance from the entry at
(600,676): the Boss nearest at (551,517), the venom-spitter farthest at (447,317). Machiavelli's own
can keeps its name and becomes the leader (race and model repointed to the Boss tier, matching the
family's own model/race pairing); the other three generators point at shipped `Snakebreed` and
`Snakebreed Venom` cans, so **no new can was authored**. Five changed lines in total: two in the can,
three `Entity=` values in the map.

Two traps checked and cleared rather than assumed:

- **Mojo budget.** The groups cap `Max Party Mojo=3`, and a costlier can would silently fail to
  spawn. **No race in the game sets a Mojo preset**, so the cap binds nothing here.
- **The name `Assassin`.** All four generators set `New Name=Assassin`, and names broadcast in this
  engine. Nothing in the map targets that name, so `New Name=` was left untouched.

#### One genuinely empty stub, left alone

`Mach Sets Ambush Relay` (`Active=0`, named by nothing) has **`Action=` empty**. It suggests the
ambush was once meant to be armed by Machiavelli himself rather than on exit, but there is no payload
to restore -- writing one would be authoring new content, not restoring it. Recorded, not touched.


## Settled by decompilation: `CSeriesAction`'s index is per-instance

Three releases of one-shot enemy behaviour -- 0.33.0's priest shield, 0.34.0's twelve veteran
draughts, and 0.48.0's thirty-six self-buffs -- all rest on one assumption: that a `CSeriesAction`
used as a one-shot advances its counter **per spawned creature** rather than once for the whole can.
`PO2` was written as the row that decides it, and it was never played. **It is now settled without
playing it**, and the answer is per-instance.

### What the binary says

| finding | where |
|---|---|
| `CSeriesAction` registers with parent `CMultipleActionsAction` and instance size **0x20** | `0x0056fb30` |
| **`Debug/Next Action Index` is a field at offset `0x14` *inside the object*** -- the counter is object state, not a global | field table at `0x0056fbe0` |
| `Require Success To Advance` at `0x18`, `When Done` at `0x1c` (default `Repeat Series`) | same |
| `Damaged Script Action` is a **pointer field at offset `0x90` on the entity** (with `Destroyed Script Action` at `0x88`, `Destroyed Effect Action` at `0x84`) -- so each entity points at its own action tree | `FUN_00535b00` |
| The engine offers exactly **two** options for a canned object: `Shared Global Instance` (1) and **`Local Copy` (2)** | enum table at `0x007051d4` |

That last one matters twice. Sharing is an **opt-in**, which is only worth offering if copying is the
norm -- and it is a standing caution for this project's own work: every Fixt requirement can is
written `Use=Shared Global Instance`, which is right for a stateless predicate and **would be wrong
for anything carrying state.** Never put a `CSeriesAction` inside a shared canned object.

### What the shipped data says, which is what actually closes it

- **755** `Next Action Index` fields across **155** vanilla maps: every *placed* entity serialises
  its own copy of its action tree.
- Vanilla ships the exact one-shot idiom -- `When Done=Repeat Last Action` with
  `Require Success To Advance=1` -- **350 times**, and **in monster cans**, not just maps:
  `Snakebreed Summoner`, `Greater Titan Summoner`, `Rhea`, `Ghoul Male Large` and
  `Swordsman ShieldHelmet` each run a one-shot `CCloneAction` summon sequence out of
  `Shoot Completed`.

**That is the clincher.** If the index were shared per can, only the *first* Snakebreed Summoner ever
spawned would summon anything -- and they arrive in waves. Vanilla's own design depends on
per-instance series state, in a monster can, which is exactly where this project's one-shots live.

### A route that does not work, and one correction

**The save file cannot answer this.** `Autosave.sav` is 3.2 MB and contains **zero** plain-text
entity fields -- no `CEntityBase`, no `Damaged Script Action`, no `Next Action Index`. Only the
current level's top-level stats are plain text; every entity tree lives in the binary `TempFile`
blobs, so there is nothing to grep.

**And a correction made mid-investigation:** `DjinnArenaMonster4` looked at first like vanilla
shipping a one-time *self*-buff, which would have been perfect precedent. It is not --
its `CAddCharacterModifierToCharacterAction` targets **`$Instigator`**, so it slows the *player*, and
the `CDisplayAffectingPlayerIconAction` beside it puts a HUD icon on the player. So vanilla has no
one-time self-buff on a creature; 0.48.0's are new in that respect, even though the mechanism around
them is vanilla's. It also means `CDisplayAffectingPlayerIconAction` is the wrong tell for an enemy
buffing itself -- that is a player-HUD action -- and `CSpawnEffectAction` is right.

