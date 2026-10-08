# Lionheart Fixt

A cumulative restoration-and-repair mod for *Lionheart: Legacy of the Crusader*, named
after Fallout Fixt and following the same discipline: one mod, one install, and every
release visible in all three registers - **fix**, **restore**, **extend**.

Lionheart shipped as a strong RPG for one act and a combat corridor for seven. That is
measurable rather than merely felt: Barcelona holds 88 quests and the Crypt holds one,
while combat density rises 35x. Fixt repairs what is broken, restores what was cut, and
writes new content only where the game plainly ran out - working from the shipped archive
rather than from opinion.

**This repository is the mod.** Its root is the mod package: `mod.json`, `files/`, and the
documents that explain every decision in it. Releases are on the
[releases page](https://github.com/EricHype/LionheartFixt/releases).

## Installing

**[Download the latest release](https://github.com/EricHype/LionheartFixt/releases/latest)**
-- currently [0.38.0](https://github.com/EricHype/LionheartFixt/releases/tag/v0.38.0).

Unzip it, then double-click **`Mod Manager.bat`**. The button names the mod; click it and
wait a few seconds.

Nothing else is needed -- no Python, no separate mod manager, no vanilla backup to make
first. The manager finds a GOG, Steam or retail install by itself, and `Uninstall` puts
everything back exactly as it was.

**Start a new game afterwards.** A save records a map's contents the first time it enters
and restores that recording rather than re-reading it, so characters this mod places will
not appear on an existing save. Dialogue changes *do* appear, which makes it worse rather
than better: half the mod seems to work.

Unzip somewhere with a **short path**. A few resource paths run to ~110 characters, and a
deep folder pushes them past Windows' 260-character limit, where the extractor drops files
without reporting it -- the install then fails for a reason that looks nothing like the
cause.

Building from a checkout instead, with [the tools](https://github.com/EricHype/LionheartModTools):

```
python modmanager.py install <path to this repo> "<game folder>"
python modmanager.py uninstall lionheart-fixt "<game folder>"
```

## What is in it

Every release is cumulative; the latest zip contains all of them. Each one is written up in
full -- the survey that found it, the reads behind every decision, what was left alone and
why -- in [`docs/releases.md`](docs/releases.md).

The three most recent:

| Release | Where | What |
|---|---|---|
| **0.38.0** Magic Items Now Drop | the random item generator, so everywhere that draws from it | **Magic equipment did not drop in this game.** Only the plain versions did. The `*selection MAGIC` cans -- the things that pair a base item **with an enchantment** -- were reachable for potions and scrolls only; **`Amulet`, `Belt`, `Bracer`, `Cloak`, `Helmet`, `Ring` and `Bolt` were referenced by nothing at all**, and `Wand selection MAGIC` was one dead link from the same fate. The enchantment half of the loot system was built and never wired to `1 MASTER ALL Items in the game`, which real maps do draw from. Now connected: a new `All Magic Equipment` can holds the six equipment pools at equal weighting and enters the misc branch **once at weighting 2**, matching scrolls and wands -- so magic equipment is **9%** of that branch rather than the **36%** six separate branches would have produced, with plain equipment untouched at 74%. **All 40 enchantments were verified implemented first.** The wand pool is connected too, bringing 16 enchantments into loot where vanilla placed only `Wand Lightning Major`, and **`Wand of Swarm`** -- `5 Unique`, summons insects, grants ranged resistance while charged -- joins it at the same weighting as `Rigor Mortis`. Its two shelf-mates **`Fire and Ice` and `Mage` are deliberately excluded**: both are description-only shells with no behaviours and no modifiers, promising effects that were never built |
| **0.37.0** A Rock Titan of Your Own | the Tribal summoning line, everywhere | **The top two tiers of Monster Summoning were finished and disconnected.** `Summoned Cans/Monster Summoning Level 4` and `Level 5` -- six cans, each with its own dedicated `.Race` and a working model -- are referenced by **nothing at all** in the shipped game. A Tribal mage's ceiling was a Wolf 03 forever. **The tier table is not in the skill**: `Monster Summoning.Skill` references no cans, it fires a `Spellcast` relay and selection lives in `Spell Projectiles/Monster Summoning Instant Hit Projectile`, which branches on single versus multi -- and **the two sides are shaped differently**, single being a skill ladder and multi having no gating at all. The single ladder now continues on vanilla's own 50-point spacing: **< 150** keeps tier 3 unchanged but bounded, **< 200** summons **Snake Women, an Ogre variant or a Wererat Boss**, and **200+** summons a **Rock Titan**, a Desert Beast or a Sand Spirit. The multi pool grows from 3 options to 9. Tier 4 and 5 are **clones of the tier-3 block with the can names swapped**, so each keeps its `CAddAIAction` mana upkeep byte-for-byte -- both verified at 3 mana, because a high summon that costs nothing to maintain would have been the obvious way to get this wrong. One thing to know in advance: all six races carry `Display Name=Black Wolf` in vanilla, copied from the wolf summon and never renamed, so a summoned Rock Titan is currently *called* a Black Wolf |
| **0.36.0** The Templar Set | act 3's burned hamlet, and the whole item survey | **Two unique items the shipped game defines and places nowhere -- and one of them was never finished.** `Helm of the Templars` is a `Head`-slot item that carried **shield art in every other field**: `LionShield_PU` on the ground, `Shield Large Better` for all three icons, and `Grouping Catagories/Shield Large`. Someone cloned the shield, changed the name, description and slot, and stopped. Repaired from the game's own `Inventory Items/Helmet`. **Then both turned out to have no stats at all** -- their only behaviours were the pickup and putdown *sounds*, so an item that *"shines with the power of the Templars"* was strictly worse than a helmet off any thug. They now carry **AC +6** and **+1 Luck** (helm) and **AC +8, Piercing +15, Slashing +12, Crushing +12, OneHandedMelee +5** (shield), priced against the *ceiling* for those two slots rather than against items of matching weight -- `ShieldLarge` is +7 at **twice** the encumbrance. Plus a **two-piece set bonus of +4 AC**, built on the Voodoo set's shipped pattern: each piece increments a counter and a computed attribute reads it, because the engine has **no equipment check at all**. Both pieces sit on `Dead Knight Templar 5`, the only dead-Templar template used just twice. And the whole survey behind it is now written down in [`docs/unused-content.md`](docs/unused-content.md) -- 8 quest items still unplaced, **48 enemies nothing spawns**, two whole **summon tiers** unreachable, 5 title perks nothing awards, and the six ways the survey was wrong before it was right |

The **51 releases before those** are one line each in [`docs/changelog.md`](docs/changelog.md).

Everything the shipped game defines and then references from nothing -- unplaced quest items, 48 enemies that nothing spawns, two whole summon tiers, and which of them Fixt has since picked up -- is surveyed in [`docs/unused-content.md`](docs/unused-content.md), along with the four ways that survey was wrong before it was right.

Three things were **read and deliberately left alone**, and the reasoning is in the release
notes: Torquemada's *purify the shadow dryad* quest (she cannot be killed; unfinished, not
cut), the Mountain Pass's sealed door (no map behind it), and the Act 8 goblin companion
arcs (they return with Act 8).

## Status

**0.1.0 through 0.38.0 are published**, and every act of the game has been surveyed, built and
released. The 0.21-0.25 line is the first work aimed at how the game *plays* rather than at what was
cut from it, with 0.25.0 the first to change how enemies fight; every release before and since is one
line in [`docs/changelog.md`](docs/changelog.md).

Most of what shipped after 0.4.0 has been played once, by one tester, which is how the 0.8.x repairs
were found. **From 0.11.0 onward much of the line is built and not yet played through**, which is a
deliberate trade rather than an oversight -- development runs ahead of testing and the backlog is
worked off in patches. Where a playthrough has reached the new work it has paid for itself: Fernand
Desoto's release-and-rejoin cycle took seven attempts before it was signed off in play at 0.28.1, and
a player's crash report is what found a bad class name that had been shipping since 0.13.0. Still
open: the Lava Troll Hide (`TH1`-`TH8`), Fernand's combat AI (`FA1`-`FA6`), the trolls
(`LT1`-`LT12`), and all of 0.30.0 (`GB`, `MF` and `GL`). What a playthrough finds is repaired on
`main` and cut as a patch release.

Every release's automated gates pass -- `tools/validate.py`, `tools/test_triggers.py` for the map
builders in `tools/lhbuild.py`, and `tools/test_md2bbcode.py` for the forum-post converter. The human
gates are recorded per release in [`docs/qa.md`](docs/qa.md), and as walkable cases in
[`docs/playtest-guide/`](docs/playtest-guide/).

## How it is made

Nothing here is guessed. A release starts with a survey of the shipped archive -- every
dialogue node nothing reaches, every level part that starts switched off and is never
switched on -- followed by reads of the exact shapes the game uses for the thing being
built, so that every relay, generator, polygon and requirement in Fixt is a shape the game
ships somewhere else. When a read overturns a plan, the plan is corrected in place beside
the wrong claim, not rewritten. When something is new content, it says so.

**A check adds a route. It never removes one.** Every scene here can still be solved
exactly the way vanilla solved it, by a character with none of these stats. That is also
the test: a check that silently replaced a shipped route is the bug to look for.

New lines follow the game's own lore order. Nothing at Montserrat names the Old Man of the
Mountain, because Act 4 does.

| | |
|---|---|
| [`docs/design.md`](docs/design.md) | the diagnosis, measured, and the phase plan |
| [`docs/plan.md`](docs/plan.md) | the work, section by section and map by map |
| [`docs/releases.md`](docs/releases.md) | every release: survey, tiers, decisions, what was built, what was left alone |
| [`docs/changelog.md`](docs/changelog.md) | every release in one line, newest first -- the history the README used to carry |
| [`docs/qa.md`](docs/qa.md) | every case a release has to pass, and which have |
| [`docs/playtest-guide/`](docs/playtest-guide/) | the same cases as a route to walk, built by `build.py` |
| [`dist/`](dist/) | release notes and forum posts per version; `README.txt` is what a player reads after unzipping |
| [`tools/`](tools/) | this repo's own scripts: `validate.py` is the gate every release passes, `lhbuild.py` emits map and dialogue-tree blocks, `md2bbcode.py` converts a forum post, `savecheck.py` reads a save so a playtest can be checked rather than remembered, and each has a test beside it |
| [`LICENSE`](LICENSE) / [`NOTICE`](NOTICE) | MIT, and what the MIT grant does and does not cover |

**The tooling lives separately**, in
[LionheartModTools](https://github.com/EricHype/LionheartModTools) - the archive packer,
the resource-format parser, `modmanager.py`, the map editor and the `lionheart-modding`
skill. You need that repo checked out to build or install this one. Fixt is content; the
tools are tools.

## Compatibility

Fixt is one mod and expects to be the only one editing these files. It installs over any
earlier Fixt release. New level parts do not appear on a save that has already visited
their map (see Installing); each release's notes say which map that means, and dialogue-only
changes work on any save.
