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

**The two shells were deliberately left out.** Putting a description-only item into the loot pool would
ship a unique wand that does nothing, which is worse than leaving it unobtainable. `Fire and Ice`
carrying **value 0** alongside 1,036 bytes of nothing is the giveaway: these were written as design
intent and never built.

Restoring them means **implementing them from their descriptions**, which is authoring rather than
wiring, and it needs a judgement first: `Wand of Mage` as described -- +4 to every magic skill, in a
game where the best single enchantment gives +8 to one skill -- would be the strongest item in
Lionheart by a wide margin. That is a design decision, not a restoration.

This is the same trap as the Templar helm, and worse. The helm at least had the correct *slot*; these
have nothing but text.

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

In rough order of how little invention each needs:

1. ~~**The two summon tiers.**~~ **Done in 0.37.0** -- see below.
2. ~~**The six disconnected equipment pools.**~~ **Done in 0.38.0** -- connected through a new
   `All Magic Equipment` intermediate can at weighting 2, so magic equipment is 9% of the misc branch
   rather than the 36% six separate branches would have given. **`Boot`, `Gauntlet` and
   `Necklace selection MAGIC` are still only reachable from one map each**, and `Bolt` and `Arrow` are
   in the same position -- one entry each if that inconsistency is worth closing.
3. **`DaVinci Tank Gear`** -- names its own quest-giver, who is a live NPC with dialogue.
4. **`Goblin Slayer`.** `Goblin Kill Counter` is already live and already written by six files;
   this is a threshold read away. Moved up from last place after the counter claim was corrected.
5. **The three `FACTION * Killer` perks.** A shipped pattern with one working quarter as the
   reference. Needs a decision about where detection lives -- per-member death slot rather than a map
   trigger -- but invents nothing.
6. **The two wand shells** -- `Fire and Ice` and `Mage` have descriptions and **no
   implementation at all**, so these need building from their text, not wiring. `Swarm`, the only one
   of the three that was real, went in with 0.38.0.
7. **`Hangover Cure Potion`** -- the smallest possible scene.
8. **The two Trapped Spirit items** -- the spirits already exist as NPCs with dialogue, so the scene
   is half-built.
9. **The two Titan items** -- Toulouse is live content Fixt has worked in before.
10. **The 17 Nostradamus English** -- a whole garrison with art, but placing them is level design
   rather than restoration, and act 5 is already populated.
11. **`Inquisitor Feralkin Journal`** -- needs a reader.
12. **`Wielder DARK Quest Rod Bone NO Spirit`** -- its missing half has to be designed.
13. **`Ruler of Calle Perdida`** -- a missing questline branch, so it needs writing, not wiring.

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

**Still silent, and recorded as such rather than guessed:** `900 Lucius thrown out of town` and
`900 Lucius extorted and thrown out of town` are Andre's own post-betrayal greetings, and they need
the same treatment inside `01 Hamlet Exterior`'s much larger node-selection chain in
`Lucius Wrasslin` and `Talked past Lucius`; the extorted variant also needs the `Lucius extorted`
marker read alongside the new one. `80 Do You Have The Item I Need?` on the Blacksmith stays
unreachable for the same reason -- nothing links to it, so renaming its recording would be
cosmetic. Both are wiring jobs, not renames.

Also noted while here: `Titan Andre requires PC to have sphere from other titan.can` is an **empty
canned requirement** (`Object=` with no value), one of the 27 already on this list.
