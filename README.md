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
-- currently [0.40.0](https://github.com/EricHype/LionheartFixt/releases/tag/v0.40.0).

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
| **0.40.0** | the Gate District, La Calle Perdida | **`Convince DaVinci to Join the Dark Wielders` is implemented.** The quest shipped as a **stub -- `Item Count=0`, `Sub-Quest of=!None`**, no children, with **zero** mentions across DaVinci's 112 dialogue nodes and **zero** among his 127 recordings. Nothing was built, so this is implementation rather than restoration. It is **persuasion-only by necessity**: `Races/NPCs/Wielders/Leonardo DaVinci` is **AC 1000 / HP 10000**, the deliberate-immortality pattern used for the game's children, because `08 Final Encounter.zax` holds **232** DaVinci references and its endings are a matrix over {Old Man escapes / killed / talked to death} x {DaVinci alive or dead} x {Galileo alive or dead} x {player good or evil}. Quinn's *"convince him or destroy him"* shape therefore cannot be given to him -- the kill half is exactly what the developers engineered away -- making this the **only Dark Wielder task with no violent solution**. Three parallel routes, none required: `Speech 50`, a `COR` of vanilla's own `General Thought/Tribal Skills moreequal 80`, or holding the **Ring of the Trapped Spirit** from 0.39.0's pact. Refusing withdraws nothing -- he argues you off the path instead -- and **both outcomes complete the quest**, so no journal entry dangles. Offered on Relican's hub, outside the task 1-2-3 chain, so skipping it costs nothing |
| **0.39.0** | La Calle Perdida, the Trapped Ether Plane | **The Mad Enchanter can be allied with Relican, and the Dark Wielders get the bind-spirit step they shipped without.** `Trapped Wizard.can` and `Relican.can` are the **only two cans in the game** using `Races/NPCs/Relican` and `Characters/NPC/Barcelona/Wielders/Relican` -- same race, same model, same spells -- and nothing in the fiction ever connected them. Sparing the Enchanter paid **nothing** in vanilla while both lethal routes drop `Kublai Khans Sword`; now sparing him yields the **Amulet of the Trapped Spirit** and allying him to Relican adds the **Ring**, a set bonus, and his binding of the Sceptre. `Rod Bone NO Spirit` -- *"an empty shell without a spirit to power it"* -- was referenced by **nothing**; DaVinci's chamber now yields it and the spirit is bound at the ether plane using the Observatory's own machinery, with Relican binding it himself as a fallback so the initiation can never dead-end. Also grants **`Ruler of Calle Perdida`**, the "Dark Lord of Calle Perdida" title that described the Summoning Ring's evil ending and was granted by nothing. **And closes an unbounded exploit:** the shipped Sceptre granted +2 to eight disciplines from its *pickup* action with `permanent=1` and `Allow Accumulation=1`, so dropping and re-taking it stacked skill points without limit |
| **0.38.1** | the random item generator | **Repair: 0.38.0 connected the magic equipment pools with no progression gating at all.** A `5 Unique` ring could drop in act 1, where median party mojo is 3-10 -- the pools weight rarity only softly, and `Ring Metal Fist` and `Helmet Sylvant` are both Unique at weight 20. `All Magic Equipment` is now a **`CInventoryItemGeneratorMojoList`** on `CAverageMojo` at thresholds **7 / 16 / 999**, which are vanilla's own, copied from `All Armor` rather than invented. Each tiered pool follows the `Armor LOW Mojo` idiom -- it keeps **every entry its parent had** and sets `Weighting=0` on the too-good rarities, so a diff shows weights moving rather than entries vanishing. Below mojo 7 a player finds **amulet and ring enchantments only, nothing above Uncommon** (9 live of 40); the other four slots start at mojo 7, up to Rare (22 live); **Very Rare and Unique wait until mojo 16**, around the Crypt. Belt, Bracer, Cloak and Helmet have **no Common or Uncommon enchantment at all**, so they are absent from the lowest band by necessity rather than choice -- viability was checked before building rather than assumed |

The **54 releases before those** are one line each in [`docs/changelog.md`](docs/changelog.md).

Everything the shipped game defines and then references from nothing -- unplaced quest items, 48 enemies that nothing spawns, two whole summon tiers, and which of them Fixt has since picked up -- is surveyed in [`docs/unused-content.md`](docs/unused-content.md), along with the four ways that survey was wrong before it was right.

Three things were **read and deliberately left alone**, and the reasoning is in the release
notes: Torquemada's *purify the shadow dryad* quest (she cannot be killed; unfinished, not
cut), the Mountain Pass's sealed door (no map behind it), and the Act 8 goblin companion
arcs (they return with Act 8).

## Status

**0.1.0 through 0.40.0 are published**, and every act of the game has been surveyed, built and
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
