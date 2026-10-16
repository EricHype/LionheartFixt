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
-- currently [0.64.0](https://github.com/EricHype/LionheartFixt/releases/tag/v0.64.0).

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

The three most recent pieces of restored content. The patches between and after them -- including **0.60.1**, a soft lock this mod introduced in 0.9.0 and did not find for a year, and **0.60.6**, a crash this mod shipped and fixed the same evening -- are one line each in the changelog:

| Release | Where | What |
|---|---|---|
| **0.64.0** | four NPCs and a playwright | **Five named NPCs recorded a line for being attacked and none of them could say it.** Torquemada: *"Arrogant fool! Guards! Restrain this heretic!"* Cedric Alsen: *"Wielders, to me! La Calle Perdida is under attack! The intruder must not leave here alive!"* Joan of Arc: *"So be it, monster. We will send you back to the fires of perdition."* Raphael: *"To the hellfire with you, heathen!"* Shakespeare: *"Time to make an honorable retreat rather than face a dishonorable foe!"* **The hook is the most common one in the game and the slot was already in every one of their cans, empty.** `CSkeletonTransition` with `To State=Attack` ships **461** times across 337 files, 33 of them firing a dialogue node, and each of these five templates holds one `CSkeletonAI` with `Transition=Array { Array Count=0 }` at the same place in the same order. `Brother Michel.can` is the same file with `Array Count=1`, which is why his *"Brothers! Help me!"* plays and theirs did not. **And Torquemada's node id carries a trailing space:** `1000 attack torquemada ` is how his tree spells it, and a can naming a node is matched **byte-exactly**, where a mismatch is a crash on map entry rather than a silent miss |
| **0.63.0** | your own spirit | **The spirit never got to say its name.** `1 Exit Skill Tutorial` is the companion spirit's hub in all three trees, reached **13 ways** in each, and it is the conversation every player opens. It asks *"What exactly are you?"*, *"Why do you call me Scion of Lionheart?"* and *"Who is hunting us?"*, and never *"What is your name?"* -- which is **573 KB** of recorded answer across the three spirits: *"Far to the east I was called Raiju, the thunder beast"*, *"I am the patron saint of discontentment, the demon of little white lies... know me as Saurva"*, *"I am Armati, one of the amesha spentas of fertility of the earth"*. The Beast has a second unreached answer on the subject its own name speech ends by naming, `750 good and evil`, **248 KB**. **The shape was not invented:** `10 hunted`, the hub's third answer, is one node with one blank reply back to the hub, so each new answer gets that and nothing else -- and that is why none of them needs the cutscene exit 0.62.0 had to add, since the player still leaves through the hub's own goodbyes |
| **0.62.0** | the road out of Barcelona | **The act 6 story turn, and no map opened any of it.** `1000 druid finale` exists in all three spirit trees, and **13 nodes and 1.31 MB** of performed voiceover hang off it: *"Now the wolf has shed its false coat and our *true* enemy is revealed"*, *"the Old Man of the Mountain has moved his pawns brilliantly, placing the world in *check*"*, then `1000 adversary`, the Disjunction and three karma answers. Every follow-on's only way in is the finale, so **one trigger reaches all of it**, and the shape is vanilla's: `700 old man warning` has zero inbound replies too and plays because `07 Dark Temple` opens it the same way, twelve wirings in one map. It fires on the **Crossroads-to-England road**, walking up to the portal, which is the road out of the sacked city and the quest **0.32.0 restored** on it already says *"Follow it"*. **Three defects came out with it:** the beast finale answered *"Agreed, we must pursue our enemy"* with *"Be wary! Such instincts have led many to ruin"*, because both its replies fired the evil node; the elemental's default reply named a node that **does not exist in that tree**; and four terminals carried no exit at all, which inside a cutscene means the controls never come back. **A fourth is reachable today:** the beast spirit's *"I tire of your counsel. Begone"* names `5 goodbye angry`, which the other two trees have and **the beast tree does not** |

The **100 releases around those** are one line each in [`docs/changelog.md`](docs/changelog.md).

Everything the shipped game defines and then references from nothing -- unplaced quest items, the enemy cans that nothing spawns, and why that count was first reported as 48 and is honestly zero, two whole summon tiers, and which of them Fixt has since picked up -- is surveyed in [`docs/unused-content.md`](docs/unused-content.md), along with the four ways that survey was wrong before it was right.

Three things were **read and deliberately left alone**, and the reasoning is in the release
notes: Torquemada's *purify the shadow dryad* quest (she cannot be killed; unfinished, not
cut), the Mountain Pass's sealed door (no map behind it), and the Act 8 goblin companion
arcs (they return with Act 8).

## Status

**0.1.0 through 0.64.0 are published**, and every act of the game has been surveyed, built and
released. The 0.21-0.25 line is the first work aimed at how the game *plays* rather than at what was
cut from it, with 0.25.0 the first to change how enemies fight; every release before and since is one
line in [`docs/changelog.md`](docs/changelog.md).

Most of what shipped after 0.4.0 has been played once, by one tester, which is how the 0.8.x repairs
were found. **From 0.11.0 onward much of the line is built and not yet played through**, which is a
deliberate trade rather than an oversight -- development runs ahead of testing and the backlog is
worked off in patches. Where a playthrough has reached the new work it has paid for itself: Fernand
Desoto's release-and-rejoin cycle took seven attempts before it was signed off in play at 0.28.1, and
a player's crash report is what found a bad class name that had been shipping since 0.13.0. A fortnight of reports from one playthrough closed the siege tank quest, DaVinci's
parting gift and Alvaro's cart horse, and opened three defects this mod had shipped:
a cutscene that could not end, a horse built on a wolf, and a crash. Still open: the
Lava Troll Hide (`TH1`-`TH8`), Fernand's combat AI (`FA1`-`FA6`), the trolls
(`LT1`-`LT12`), all of 0.30.0 (`GB`, `MF` and `GL`), and the newest restorations --
Shakespeare (`SW`), the undead warning (`UE`) and the parting gift (`GF`). What a playthrough finds is repaired on
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
| [`docs/engine-notes.md`](docs/engine-notes.md) | what the engine actually does: how content is reached, what reaches a save, the four shapes that crash, and the method rules each mistake paid for |
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
