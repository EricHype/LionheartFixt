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
-- currently [0.57.3](https://github.com/EricHype/LionheartFixt/releases/tag/v0.57.3).

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
| **0.57.0** | the witch's interior in Montaillou, and seven maps Cortes leaves on | **Na Roqua answers the wrong spirit, and Cortes says nothing at all to a woman.** Two defects in the shipped game, both found by the voiceover sweep and both with the mechanism already placed. `06 Witch Interior.zax` branches on `CHasSpirit` three ways, and **the Beastial arm fires `200 nis weird woman respond to elemental`** -- the same node id as the Ancestral arm, copy-pasted and never changed -- so a beast-spirit player hears the line written for the elemental spirit, and `respond to beast` (230 KB) and `respond to demon` (176 KB) are fired by **nothing**. The reconstruction is not a guess: all three spirits name her **Druj** and call her a *creature*, all three of her answers open *"I have not heard that name in many ages"*, and `conclusion` -- *"I am no longer Druj, the creature that your spirit named"* -- answers exactly that, while vanilla plays it in the demon arm only. So every arm now runs **spirit names her, her answer to that spirit, then both closing lines**, with the demon keeping his own parting shot, `1000 nis weird woman demon departs`. `conclusion` goes from one arm to three and `conclusion 2` from none. **Second**, `800 cortes leaves MALE pc` is fired from **seven** maps and `800 cortes leaves FEMALE pc` from none, so half of all players lose a companion who walks off in silence. The seven sites now branch on `CIsGender`, testing **Female** with the male line in the `Else`, so a test that fails to resolve degrades to exactly what ships today rather than giving a man the wrong line. Each witch arm still releases its non-interactive sequence exactly once, asserted, because 0.55.0 was a hang caused by precisely this kind of edit |
| **0.56.0** | the Crypt, the Wilderness, Montserrat, Barcelona Coast | **Fifteen recorded lines that nothing in the game fired, and not one new word written.** The first release aimed at a sweep that had been run in only one direction: the old voiceover audit asked whether every recording is named after a node (1,314 of 1,330, so it read as closed) and never asked whether the player can **reach** the node a recording sits on. Vanilla ships **204** such nodes carrying **19.27 MB** of performed audio. The companions are the cleanest group: **Joan of Arc** had five combat calls and one was wired, as a beat inside the plateau cutscene; **Cortes** had four battle cries and two cries for help; **Cervantes** had an attack line and two wounded lines. Their cans leave `Shoot Completed` and `Damaged Script Action` empty, so the banks hang there in the shape Fixt's own 95 bark cans already use, padded with `CActionSelectSkill` on the one skill every one of these races lists. **Rates are set by pool size, not copied**: 1 in 8 over Joan's five lines, 1 in 10 over Cortes's four, 1 in 16 for Cervantes's single line, 1 in 12 on the wounded banks, so no line repeats sooner than roughly every 40 attacks. Cervantes's damaged slot is **occupied** by the relay that makes the Temple district care when you hit him, so his bank is **wrapped beside** it, never over it. Two more lines needed no bank at all: `01 Grove Exterior` and `Barcelona Coast` already fire their siblings, so the Cortes remark alternates two lines and Cervantes's approach cycles three. **Balloons do play voiceover** -- 325 vanilla balloon firings land on recorded nodes -- which was checked before any of this was built. The release's one real defect was caught by its own gate: `800 general attack ` carries a trailing space, a can-to-node reference is matched **byte-exactly**, and a mismatch is a hard crash on map entry |
| **0.55.0** | the Montaillou tavern, three snakebreed summoners, the Crypt | **Reported from play: paying the Cathar toughs 150 gold locked the game with the gears spinning.** The ambush runs inside a `CBeginNonInteractiveSequenceAction`, so every exit must call the matching End, and the tree had **five reachable exits and only four Ends**. The fifth is vanilla's `100 Welcome`, and it is **not a broken exit** -- it is `Cathar tough guy 3`'s `GetCloseThenTalk` greeting, hung on the generator's `AIs to Add` with `Trigger Only Once=0`, and it rightly carries no actions because nothing is running when you greet somebody. **0.14.0 pointed `Wielder IS` at that greeting and 0.24.0 pointed the Templar's 150-gold reply at it**, because nothing in the tree linked to it so it read as cut content. The greeting is now **byte-identical to vanilla** and both replies reach a new exit carrying the resolution of the one peaceful ending that already worked. Giving the greeting that block instead, which was this release's first attempt, would have let a friendly hello end a sequence that was not running, re-award the encounter XP and delete all three toughs, repeatably. **A0.16** now fails any exit this mod makes reachable in a tree that runs wholly inside a sequence, scoped against the shipped copy so inherited shapes stay quiet. Running it honestly exposed **seven unreachable nodes of our own**: the four `summoner` barks were never attached because those three cans, unlike every can the bark release touched, have `Shoot Completed` **already occupied** -- that bank *is* the summon-rate mechanism -- so the lines now hang **inside** the summon branch and the rate, clone count, skill selections and animations are byte-identical to vanilla; and three `3 tide` drafts in `The Fronts` are deleted, superseded by `Garrison Camp` 60/61/62 |

The **70 releases before those** are one line each in [`docs/changelog.md`](docs/changelog.md).

Everything the shipped game defines and then references from nothing -- unplaced quest items, 48 enemies that nothing spawns, two whole summon tiers, and which of them Fixt has since picked up -- is surveyed in [`docs/unused-content.md`](docs/unused-content.md), along with the four ways that survey was wrong before it was right.

Three things were **read and deliberately left alone**, and the reasoning is in the release
notes: Torquemada's *purify the shadow dryad* quest (she cannot be killed; unfinished, not
cut), the Mountain Pass's sealed door (no map behind it), and the Act 8 goblin companion
arcs (they return with Act 8).

## Status

**0.1.0 through 0.52.3 are published**, and every act of the game has been surveyed, built and
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
