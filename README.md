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
-- currently [0.43.0](https://github.com/EricHype/LionheartFixt/releases/tag/v0.43.0).

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
| **0.43.0** | the Gate District | **`DaVinci Tank Gear` is the last hand-authored quest item that was referenced by nothing, and half its quest already ships.** DaVinci's hidden chamber exists, furnished, with his war machines modelled in it (`DaVinci Objects/Catapult`, `DaVinci Objects/Death Machine`) and examinable through `1 Catapult` / `1 Sweeper` / `1 Siege Tank`, each of which says the machine is **incomplete**. He tells the player on screen that the engine needs *a special spirit*, which feeds the **live 4-state** `Obtain the Spirit Gem for DaVinci`. Nobody ever asked about the gears, and `Create Mechanical Gears for DaVinci's Siege Tank` was a **0-state stub**. The gear now comes from the character who already sells gears -- DaVinci's talking steam engine, which hands over `DaVinci Crossbow Gears` for a potion at `650 collect gears` -- at **three prices**: a potion (consumed), `Barter moreequal 35`, or a **promise to tell DaVinci, out loud, who built it**. Only the promise creates anything, and it **outlives the quest**: it is settled at `3 Return Dialogue Workshop` with the engine in earshot, exactly where the machine demands, and it is broken by never going back rather than by a button. Cortes' arm did **not** supplant this -- the crossbow, the arm and the tank are three separate projects and the tank is the only unfinished one |
| **0.42.0** | Montaillou | **Finishes the branch 0.41.0 opened: Andre's own two reactions to being sold.** `900 Lucius thrown out of town` and `900 Lucius extorted and thrown out of town` both had **0 incoming links** in vanilla, and the second carries **`CGoToCombatAction`** -- take his hush money, then betray him anyway, and he attacks. Both are decided by two markers that now exist: `Lucius thrown out` (declared in 0.41.0) and vanilla's own `Lucius extorted`. The shipped cascade in `Lucius Wrasslin` and `Talked past Lucius` is kept **byte-for-byte** and demoted inside two new tests, ordered so that extortion-then-betrayal outranks everything, and so that the `NOT quest completed` guard keeps 0.41.0's `1003` reachable rather than shadowing it. **Unlike 0.41.0's six lines, these two recordings were already correctly named** -- they were silent purely because nothing could reach the nodes, which is a different fault from filename drift. `reachability.py`'s tolerated orphan count fell **187 -> 185**, exactly the two nodes. Also records a verdict: the Blacksmith's `80 Do You Have The Item I Need?` is a **superseded draft**, not cut content -- `07 what more` fills that role with 15 replies against its 13, including a live Red Ore quest hand-in node 80 lacks -- so it is deliberately left dead |
| **0.41.0** | Montaillou | **A whole betrayal branch could never fire, and 0.88 MB of recorded dialogue never played.** `951 Furious Mayor` activates a marker named `Lucius thrown out` -- and **no entity of that name was declared in any map in the game**, so the flag could never be set. The developers knew: that reply still carries the note **`Action work in progress=kick luscious out, seal of this branch`**. The marker is now declared (`Active=0`, `Model=Editor/Checker`, copying its working sibling `Lucius extorted`), so Andre's four-stone-hearts reward branches to **`1002 Hearts in Hand but Lucius betrayed`** (previously **0** incoming links), Brother Michel greets a betrayer with his **`400`** pair (0 incoming, no replies -- terminal greetings, wired with the same `CSeriesAction` shape his own `Lucious dead` branch uses), and **`1003`** now requires betrayal rather than firing for *every* post-quest return, which had been giving loyal players a cold shoulder they never earned. With the nodes reachable, six recordings were renamed to match them -- voiceover resolves purely as `<Tree> VOs/<Node ID>.ogg` with no indirection, so a filename one character off is silent forever. `reachability.py`'s tolerated orphan count fell **190 -> 187**, exactly the three nodes connected |

The **57 releases before those** are one line each in [`docs/changelog.md`](docs/changelog.md).

Everything the shipped game defines and then references from nothing -- unplaced quest items, 48 enemies that nothing spawns, two whole summon tiers, and which of them Fixt has since picked up -- is surveyed in [`docs/unused-content.md`](docs/unused-content.md), along with the four ways that survey was wrong before it was right.

Three things were **read and deliberately left alone**, and the reasoning is in the release
notes: Torquemada's *purify the shadow dryad* quest (she cannot be killed; unfinished, not
cut), the Mountain Pass's sealed door (no map behind it), and the Act 8 goblin companion
arcs (they return with Act 8).

## Status

**0.1.0 through 0.43.0 are published**, and every act of the game has been surveyed, built and
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
