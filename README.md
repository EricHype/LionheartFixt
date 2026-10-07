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
-- currently [0.30.0](https://github.com/EricHype/LionheartFixt/releases/tag/v0.30.0).

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
| **0.30.0** The Scourge of the Land | the Wilderness: Scar Ravine, Ravine Cave, the Crossroads, every goblin in the game | **The goblins get a voice, a weakness, and two scenes that no longer have one solution.** They are the largest enemy population in the game -- 780 of spawn capacity across 30 maps -- and were the only major family with **no barks and no damage resistances at all**. 105 lines in two registers, and 13 of them are vanilla's: `GoblinVillager.DialogTree` is a goblin bark bank nobody wired, 11 of its 55 nodes fired by nothing in the entire game. One of them is an argument written for **three** goblins and never cast -- a coward, a boaster, and a third who sides with the boaster by name -- now staged across three goblin deaths over three named goblins, `Drubjub`, `Wumjup` and `Lumgrub`, whose names are vanilla's own too. The damage profile every other family already had: **burn them, do not poison them**, and the officer in the hat inverts, so blades beat him where clubs beat the rabble. Strike that officer and his post answers, once. The hostage north of the Crossroads can be handed to the Khan now, and her father finds out; the silver mine in Ravine Cave can be talked past four ways instead of only cleared. Plus one repair: **21 archer cans have been selecting a melee skill their race does not have since 0.27.0** -- `CActionSelectSkill` is not a no-op, vanilla uses it to pick the next attack |
| **0.29.0** What the Trolls Say | Temple District, the Troll Pit | **A reported crash to desktop, fixed.** Entering the Inquisition Chambers killed the game -- *Invalid class type* -- because the Grand Inquisitor's tree named `CIsQuestStatusCompletedAction`, which does not exist. The real class is `CIsQuestCompletedAction`, and the three sites already had its exact field set, so only the name was wrong. **It shipped in 0.13.0 and survived 27 releases**, surviving because those are his *return* nodes gated on a Wilderness quest. Gate 0 gains A0.15 for the whole class of bug. And the lava trolls get what the other three families got, and more: 20 bark lines in two registers drawn from the voice they already had; the **Troll Stomp** effect, which was never cut content -- their attack has always pulsed an unseen radius-120 area-of-effect and the model had no caller; regeneration, making *a creature that closes its own wounds* true at 1.0 HP/sec against the player's 0.37; and a wounded drone that fetches the chief instead of all ninety trolls in the pit |
| **0.28.2** | Port District | **Fernand stops freezing in place after a kill.** He is the only companion whose skeleton AI is hand-built in a map relay instead of inherited from a creature can, and vanilla gave it a sentry's eyes -- `Vision Cone=90` where every other companion and 1317 uses across the game have `360`, and an acquisition range of 300 where 1019 have `550`. With his target dead, re-acquisition saw only a 90-degree arc of his facing, so an enemy beside or behind him did not exist; `Target shooter if hit=1` bypasses acquisition, which is why being attacked woke him and made blindness look like apathy. The other 145 uses of that cone are almost all siege-map guards watching one direction. Unmeetable in vanilla, where he could not be recruited at all. His 40 percent retreat threshold is kept on purpose |

The **41 releases before those** are one line each in [`docs/changelog.md`](docs/changelog.md).

Three things were **read and deliberately left alone**, and the reasoning is in the release
notes: Torquemada's *purify the shadow dryad* quest (she cannot be killed; unfinished, not
cut), the Mountain Pass's sealed door (no map behind it), and the Act 8 goblin companion
arcs (they return with Act 8).

## Status

**0.1.0 through 0.30.0 are published**, and every act of the game has been surveyed, built and
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
