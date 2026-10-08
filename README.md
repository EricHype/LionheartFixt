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
-- currently [0.31.1](https://github.com/EricHype/LionheartFixt/releases/tag/v0.31.1).

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
| **0.31.1** | the Wilderness, the Temple District | **Siding with Butu's heir now costs something, and the errand can no longer be unwinnable.** 0.31.0 shipped three faults a playthrough would have found. **The horde never reacted** -- you could be Plumjum's Champion and his betrayer at once and he never learned; the Goblin Warrens and the Mongol Camp now turn on you through `Make Goblins Hostile Relay`, which already sat in fourteen goblin maps and is fired over a hundred times in vanilla. **The quest could dead-end** -- Weng Choi's rare-books errand is act 1 and removes the book, his shop stocks no books at all, and the Goblin Warrens copy is the only one in the game, so a player who sold it could never finish; vanilla's own quest calls him *"an avid collector of unique tomes"*, so the heir now cares **whether his Khan's poems went to a reader or by weight** -- a collector is accepted, a sale costs you the 250 you took. **And the reward was nothing** -- XP and a cave with one Potion in it, against losing a companion. Now the betrayal **swaps your standing** for one of three tiers scaled to what you gave up: `Goblin Traitor - Foe`, `- Bad Blood`, or `- Fallen Champion`, trading the horde's sneak-and-poison profile for melee and armour. Plus a use for the **Silver Mine Deed**, one of twelve unique items the shipped game references from nothing: open the mine with it, or sell it to Shylocke for 1200, 1800 at Barter 40, or 2500 at Barter 70 |
| **0.31.0** Butu's Heir | the Wilderness: Ravine Cave East, the Goblin Warrens, act 8's desert | **The Ravine Cave changes hands, and a mid-game choice costs a late-game companion.** `Mongol Goblin Hat Super` was **placed nowhere in the game**, and its race is the toughest goblin statline there is -- 250 HP, AC 225, harder than the Khan himself, because the hat line steps 60 to 80 to **250** where every other goblin ladder steps about 1.25x. It was never a third tier; it is a boss statline filed under hats. And vanilla names a second Khan **exactly once**, in a flavour line on an item: *"Collected by **Butu Khan**, this book of poetry contains many free verses of Goblin Poetry."* That book sits in Plumjum Khan's own warren, and Weng Choi buys it as a curio without anyone saying whose it was. So after Montserrat, **Butu's heir holds the east cave** -- a tribe recoloured red, of the engine's 17 hue palettes **16 of which are used nowhere in vanilla**, led by a goblin wearing the King model that in the whole game belongs only to the two Khans. He already looks like a Khan, which is the argument he is making. He carries **two mutually exclusive quests** -- return his Khan's poems and the cave stands down, or take Plumjum's contract on him and **`Goblin Rank` advances** when he dies. He **reads what you did about Plumjum** five ways -- killed him, his Champion, merely ranked, a goblin-killer, or nothing -- talks before he fights, and wants his Khan's poems back. Side with him and the act 8 gate that brings Plumjum to Persia **and gives you Grumdjum as a companion** stays shut. Plumjum himself points you east, and never says the heir's name |
| **0.30.1** | the Port District, the Wilderness, the Temple District, act 7, act 8 | **Repair only, from play: the combat log called people by the wrong name.** A player reported Fernand Desoto logged as *Sailor*. The log takes a creature's name from its **race**, not its can -- all 753 cans say `Display Name=unnamed` and **not one sets a real name**, while 58 races do, which is why a wolf reads *Black Wolf* and not *Wolf Black Super*. `Races/NPCs/Sailor` has an empty one, so the engine fell back to the race's own name. That race is shared by five cans, so it was **cloned, not edited** -- naming it in place would have renamed every sailor in Barcelona to Fernand Desoto. Sweeping the class found eleven more: every goblin officer and both Khans read *Goblin Grumjun*, a copy-paste of Grumdjum's race name; **Leonardo da Vinci read *River Dryad***; Galileo read *River Dryad* and then *Leo*; Sir Roger Templeton, **Guard Esteban** and Sir Jorge all read their tier, *Knight Templar 5* and *3*; every anonymous Templar leaked its tier number; and an unused English priest race read **Jerk**, developer placeholder text that shipped in the retail game. Esteban nearly took a regression with him: vanilla ships a `Guard Esteban` race used by nothing that presets **AC 1000 / HP 10000**, so pointing him at it would have made him unkillable and silently broken 0.1.1's counter-contract and the 0.10.3 repair that exists because the initiation died with him. No stats changed anywhere -- every clone carries its source's presets verbatim |

The **44 releases before those** are one line each in [`docs/changelog.md`](docs/changelog.md).

Three things were **read and deliberately left alone**, and the reasoning is in the release
notes: Torquemada's *purify the shadow dryad* quest (she cannot be killed; unfinished, not
cut), the Mountain Pass's sealed door (no map behind it), and the Act 8 goblin companion
arcs (they return with Act 8).

## Status

**0.1.0 through 0.31.1 are published**, and every act of the game has been surveyed, built and
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
