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
-- currently [0.50.0](https://github.com/EricHype/LionheartFixt/releases/tag/v0.50.0).

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
| **0.50.0** | Weng Choi's shop, the Gate District | **The one book of twelve that the finished game hands out nowhere.** `Inquisitor Feralkin Journal` is not a shell -- pickup and putdown sounds, icon, description, value, all complete -- it is simply unreachable. **Weng Choi's stock rotation holds ten** books as a `CSeriesAction` that gives one per visit and cycles; Shylocke sells the eleventh; this one was in neither, and in no map. It is now the **11th** entry in that rotation, cloned from his last entry and repointed so every surrounding field matches rather than being hand-written. It is also the **10th** check in `Weng Choi Have a rare book`, so he buys it as well as selling it and his existing `1000 Received Rare Book` node fires for it. **And an inquisitor notices you carrying it** -- a book that *"details the life and trials of a Feralkin at the hands of the Inquisition"* -- gated on actually having it in your pack, from the same generic-inquisitor tree 0.47.0 used. He demands it and **nothing takes it**: the threat is the content, and you keep your rare book. Also fixed: its display name was `Feralkin Journal.`, **the only one of the twelve with a trailing period** |
| **0.49.0** | the magic-wand loot pool | **Two `5 Unique` wands that existed only as descriptions are now built.** `Fire and Ice` was 1,036 bytes with `PlugIn Behaviors Item Count=0` and **value 0**; `The Mage` was 1,161 bytes of the same nothing. Both are implemented from `Swarm`'s shape -- the one wand in `Wands/Special/` that was ever finished -- and pooled at **weighting 5** beside it. **`Fire and Ice` casts two spells**, Fireball and Ice Storm on 5-10 shared charges, plus +15% fire and cold resistance: no vanilla wand has two `CPlugInBehaviorWand` entries and **no single spell in the game deals both fire and cold**, so this is the only route to its own text short of authoring a 93rd `.Skill`. **`The Mage`** gives Lightning Bolt x5 and Fear x5, **+4 to all twelve base magic skills** across the three categories, and +10% fire/cold/electrical resistance. **Two claims in this project's own survey were wrong and are corrected:** the "best single enchantment gives +8 to one skill" ceiling does not exist -- `Spikes Major` gives **+25** -- and the honest like-for-like is the Sceptre of Bone's +2 to eight base skills (+16) against The Mage's +4 to twelve (+48), so it is about three times a quest artifact rather than "the strongest item by a wide margin". **And a latent bug in Swarm was found while copying it:** its skill top-up is a bare `30 - skill`, which goes negative and quietly *nerfs* a caster already above 30. Both new wands guard it with a `CIfExpression` so the top-up is never a penalty |
| **0.48.0** | the English army, across acts 6 and 7 | **Seven one-time self-buffs, one per archetype, on 36 cans.** 0.33.0 and 0.34.0 gave twelve veteran soldiers a one-shot healing draught; the mechanism behind it -- a `CSeriesAction` whose first item does the thing and whose second is a `CSucceedAction` no-op that `Repeat Last Action` parks on forever -- turns out to be fully reusable, since only the payload differs. So the rest of the English army now reacts too: **Soldier1** closes ranks (+12 slashing/crushing/piercing resistance), **Soldier2 and the axemen** fight with both hands below half health (**+2 Strength**, +0.20 attack speed), **the archers** steady the draw (**+2 Perception**, +0.20 ranged speed), **the priests and priestesses** pray faster (+0.25 **cast** speed), and the **war golems** vent, rime or arc over at 40% health with +20 resistance to *their own element* and +0.15 attack speed. Every buff is **timed, not permanent**, so each one is a window to wait out rather than a step change; magnitudes come from vanilla, where a shipped enemy weapon slows the player by 0.03 per hit against a base multiplier of ~1.0 and `Gain Strength.Perk` is worth +1. Two trigger styles rather than one: the rank and file, archers and priests react to **being engaged at all**, the heavies and golems to **nearly dying**. **And the mechanism is no longer an assumption:** decompilation puts `Next Action Index` at offset `0x14` inside the `CSeriesAction` object, the engine exposes `Local Copy` against `Shared Global Instance` as an explicit choice, and vanilla ships this same one-shot idiom **350 times including inside monster cans** -- `Snakebreed Summoner` and four others run one-shot summon sequences that would fire only for the first creature ever spawned if the index were shared |

The **64 releases before those** are one line each in [`docs/changelog.md`](docs/changelog.md).

Everything the shipped game defines and then references from nothing -- unplaced quest items, 48 enemies that nothing spawns, two whole summon tiers, and which of them Fixt has since picked up -- is surveyed in [`docs/unused-content.md`](docs/unused-content.md), along with the four ways that survey was wrong before it was right.

Three things were **read and deliberately left alone**, and the reasoning is in the release
notes: Torquemada's *purify the shadow dryad* quest (she cannot be killed; unfinished, not
cut), the Mountain Pass's sealed door (no map behind it), and the Act 8 goblin companion
arcs (they return with Act 8).

## Status

**0.1.0 through 0.50.0 are published**, and every act of the game has been surveyed, built and
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
