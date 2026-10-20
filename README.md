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
-- currently [0.71.3](https://github.com/EricHype/LionheartFixt/releases/tag/v0.71.3).

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
| **0.71.3** | Montserrat, the sanctum | **0.71.2 made Montserrat's peaceful route work. This makes it make sense.** Two sentences, both Sahar's, both appended to lines she already has. **Why the player would ever agree:** *Then send me north* is offered straight off her prisoner greeting with no question asked, so the likeliest path through the route had the player agreeing to walk into Ahriman's hands having been told nothing about why north mattered. She only explained it if you happened to ask about the Crown first. Now she closes that greeting with **The Crown you came for is already over the mountains, if that helps you decide anything** -- a shrug, not an offer, which is how she treats everything else about the player. **And why a player who fought in gets nothing:** `1 too late` carried none of her motive, so someone who cut their way to the sanctum saw no trace that a deal had ever been possible. She now adds **I had wagons for this once, and sisters I could spare. You have spent both on your way in** -- reusing her own two nouns from the prisoner greeting, so the absence of the offer becomes a **consequence** rather than an omission. The route stays gated on having been delivered; what changes is that the game finally says why. Register measured off her nine existing lines and asserted by the build: 14 to 60 words, **no contractions anywhere**, no new stage direction. The text ships out of [`sahar-lines.md`](docs/sahar-lines.md), the file that was reviewed |
| **0.71.2** | Montserrat, the peaceful route | **Reported as issue #11 by Mixxer5. The route stays; it was the ending that was missing.** 0.11.0 built the peaceful way through Montserrat and shipped its last two stages -- Sahar's prisoner talk, her word, and the rout -- **explicitly unplayed**. Sahar's own line promises the garrison will stand down: *"nothing of ours on the road north will touch you ... Go. You are the last thing I was told to send, and then I can leave this place."* **It never did.** Taking her ring activated a checker called `sahar word` in three maps that **nothing in the game reads**, pacified the two names standing in the sanctum, and left the rest of the abbey hostile around a player who had been delivered to it as an unarmed prisoner. That is the reported dead end. The branch beside it already had the whole mechanism: killing her activates `routed`, fires `garrison routs` into the Grove and Level 1, and walks every survivor to a rout marker to be deleted. **Her word now does exactly what her death did**, and the fix is on the reply rather than in the map relay, so it reaches a save standing in the sanctum right now. **And you can no longer invoke a man you have never met:** the *"I carry Machiavelli's word"* reply was gated on Outwit 7 and nothing else, so it now also requires his task to have been activated. **And Outwit 7 no longer costs you the ending:** her sharpest line led to a node whose only reply was `<Draw.>`, so seven points of Outwit forfeited the ring with no way back. It now returns to her questions |
| **0.71.1** | the Cathedral, act 2 | **Reported as issue #10 by Mixxer5, with a save attached, and the save is what proved it.** Joining a second order sent the player to the Cathedral a second time, into a scene whose cast had been deleted at the end of the first: **Lord Javier alone in an empty room, controls disabled, the sequence never ending**. Escaping left the character stranded at a hidden spawn point. In the reporter's stored Cathedral all four faction checkers read `Active=0`, `Auric Generator`, `Auric`, `Knight` and `Jafar` were gone, and `Knight Generator` still carried `Has Started Generating=1` -- so re-activating the generators could never spawn anybody. **Vanilla's own bug, and vanilla left the hook for it unfinished:** Javier's tree activates `joined other faction`, which nothing in the game checks and for which no checker entity exists. Now the second order still briefs you and still gives you its Montserrat quest, but does not run the cutscene again. The guard is a character attribute, so it lives in **dialogue trees** rather than a map and reaches a save already in progress. **And a second defect fell out of the same save:** `Wielders Start Church Movie` sets the `if wielder` checker inside the Cathedral with a `COtherMapAction` and relocates the player there a second later -- for a player who has never loaded that map the relocate lands and **the remote activation does not stick**, so `Choose NIS Player` falls through every test to its last resort. This Wielder watched Jafar's **Saladin** summit and was handed the *Knights Saladin* Montserrat quest. Vanilla sent that case to the Templar scene; 0.7.0 had repointed it to Saladin. The chooser now falls back to **faction rank**, which lives on the character and cannot be lost in transit, which also means 0.7.0's restored Saladin summit is finally reached by actual Knights of Saladin instead of by accident |

The **111 releases around those** are one line each in [`docs/changelog.md`](docs/changelog.md).

Everything the shipped game defines and then references from nothing -- unplaced quest items, the enemy cans that nothing spawns, and why that count was first reported as 48 and is honestly zero, two whole summon tiers, and which of them Fixt has since picked up -- is surveyed in [`docs/unused-content.md`](docs/unused-content.md), along with the four ways that survey was wrong before it was right.

Three things were **read and deliberately left alone**, and the reasoning is in the release
notes: Torquemada's *purify the shadow dryad* quest (she cannot be killed; unfinished, not
cut), the Mountain Pass's sealed door (no map behind it), and the Act 8 goblin companion
arcs (they return with Act 8).

## Status

**0.1.0 through 0.71.3 are published**, and every act of the game has been surveyed, built and
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
