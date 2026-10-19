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
-- currently [0.71.0](https://github.com/EricHype/LionheartFixt/releases/tag/v0.71.0).

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
| **0.71.0** | the last screen of the game | **0.70.0 is withdrawn and replaced.** It closed the game with fourteen Nostradamus prophecies; they were not his voice, and they were barely readable. These are **27 slides spoken by nobody** -- an unnamed, portraitless narrator, which is a shipped form (thirteen vanilla trees have no name and no portrait), so a recording can be anyone's voice with no performance to match. Each one covers **your faction's standing, what you did to them, and what became of them next**, at the length and cadence of the *Fallout: New Vegas* ending slides. **And the faction's fate now changes, not just your rank in it.** The Wielders have three endings: La Calle Perdida is never found, or the Inquisition is let into it because **you told them where to look**, or there is nothing left to find because **you turned Relican's ring on it yourself** and they called you Dark Lord of a place that no longer existed. The Horde reads five ways including `Goblin Traitor`, the one where you handed the Khan's east rock to Butu's heir and *the word they kept for you was not Champion*. **0.47.0 is what makes the hostile readings possible:** its four *Enemy of the ...* titles, wired onto 568 spawn points, mean a Templar who killed Templars gets told so. The **Savage Heart** joins as a faction of its own, on quest history rather than a rank, with a slide for taking Raylark's contract and another for taking it and then killing him for the Khan. **England too**, on `Servant of the Queen` and `Grace's Regard`. Every lever is a perk, a rank attribute or quest history -- all of which live on the **character**, so all 27 work on a save made before Fixt was installed; a map flag could not, because an existence check is local to its map. Nostradamus goes back to vanilla except for the one empty field 0.70.0 found, a `Default Canceled Node Action` that would have stalled the credits on the last screen of the game |
| **0.69.0** | the Mountain Pass | **The other cut titan item, and the disassembly that 0.68.0 said it needed.** 0.68.0 shipped the sphere and reported that `Titan Crystal` could not be recoloured, because its colour was in buffer 4 and the tool only touched buffer 1. **That was wrong, and in a more useful way than it looked:** the colour is in **buffer 5**, and the tool had buffers 4 and 5 swapped. Read out of `Lionheart.exe` with capstone, since ReVa was down: the loader fills buffer N's data and row table as pairs (`+0x0c/+0x18` through `+0x34/+0x38`), and `GetColorAt`'s fallback at `0x0055ed2c` takes its opcodes **and its 2-byte colour values** from `+0x34`, which is buffer 5, while reading **one byte per pixel** from `+0x2c`, buffer 4, as an alpha. Buffer 5 then walks clean under buffer 1's own grammar on **257/257** icons that have one; buffer 4 is not an opcode stream at all, which is what that earlier failed grammar search was really saying. So the crystal now recolours across **all 11616** of its stored values -- 1510 in buffer 1 and 10106 in buffer 5 -- violet to green, where a buffer-1-only pass reached 13%. It drops 1 in 4 from the **basic** `Rock Titan Blue`, so each of the three tiers yields something and which titan you killed tells you which stone you got. 200 gold, like the sphere |
| **0.68.0** | the Mountain Pass | **A cut item, recoloured, as loot off the Pyrenees rock titans.** `Titan Sphere` -- *"Spirit gem"*, 200 gold -- is referenced by nothing, and 0.67.0 settled why: it is the generic predecessor of the four named stone hearts, which **share its icon**. So it cannot come back as a quest item, but Andre's own live line says what it is -- *"Inside the chest of each elder titan you will find a sphere"* -- and the Mountain Pass has `Rock Titan Blue` in three tiers. **The icon is recoloured because the original is in use:** `recolor_icon_in_place`, the function Quinn's three potion tiers were made with, swaps the red and blue channels and turns its amber to blue -- mean rgb (121, 99, 62) to (62, 99, 121) over the same **3623** opaque pixels, file length and header byte-identical. **Blue because the monster is called Rock Titan Blue**, so the colour is the game's choice. The drop is the game's own idiom, a `Chance 1 in 4` can of the kind `Enemy Drop Items Cans` holds 105 of, hung on the two higher tiers' **`Destroyed Effect Action`** -- not the Script slot a generator's `CSetDestroyedScriptActionAction` replaces, which is how the Lava Troll Hide was dead code from 0.10.0. Vanilla's 200 gold is kept: a wolf pelt is 10, a high-quality pelt or a lava troll hide 25, and the `Expensive Gem` 200. And it puts `TitanSphere_PU` on screen, a ground model **no player has ever seen** |

The **108 releases around those** are one line each in [`docs/changelog.md`](docs/changelog.md).

Everything the shipped game defines and then references from nothing -- unplaced quest items, the enemy cans that nothing spawns, and why that count was first reported as 48 and is honestly zero, two whole summon tiers, and which of them Fixt has since picked up -- is surveyed in [`docs/unused-content.md`](docs/unused-content.md), along with the four ways that survey was wrong before it was right.

Three things were **read and deliberately left alone**, and the reasoning is in the release
notes: Torquemada's *purify the shadow dryad* quest (she cannot be killed; unfinished, not
cut), the Mountain Pass's sealed door (no map behind it), and the Act 8 goblin companion
arcs (they return with Act 8).

## Status

**0.1.0 through 0.71.0 are published**, and every act of the game has been surveyed, built and
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
