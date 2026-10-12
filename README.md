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
-- currently [0.54.0](https://github.com/EricHype/LionheartFixt/releases/tag/v0.54.0).

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
| **0.54.0** | Eduardo's forge and Jafar's tents, the Gate District | **Reported from play: ask Eduardo for the Lion Shield or the Sacred Scimitar and you get one, with no way back for the other.** Two dead ends, both in the Knights of Saladin, both exposed by 0.3.0 restoring a line vanilla had cut. **The silver is the bottleneck**: there is exactly **one** Magnetized Silver in the game -- one chest in `Ravine Cave West` at `Trigger Only Once=1` -- the tree consumes it, and **both** deliveries gate on holding it *and* on `Recover a Supply of Silver` sitting at its return state, so the second order is unreachable forever. Vanilla never showed this because **all fifteen** of Eduardo's scimitar replies *require* `53F5R12P` and none of them sets it, and the only setter in the shipped game is an `Active=0` dev warp -- his scimitar half is complete and byte-identical, and only Jafar's offer was missing. The requirement cans even read *"Scimitar **or** Lionshield seeker"*, so the author's model was one-or-the-other; the game disagrees out loud, because Jafar offers **Favored One** and a stage direction tells the player it *"will not fulfill DaVinci's quest to join a faction"*. **He keeps the remainder** and charges for the weeks, not the metal: 1000 gold, or 600 at Barter 50+, his own threshold. The silver path is byte-unchanged. **Second, the Shard of Dreams**: Jafar's two tasks are one-shot (the only door consumes Ali Huban's letter) and that stays, but taking the scimitar left the relic unreturnable -- its pickup sets the turn-in state only `If` the quest is already running and its `Else` is empty, and **Jafar is the only consumer in the game**, so it became a weightless worthless stone. He now takes it unasked for karma and coin, below the quest's own reward, with **no** quest entry and **no** advance to the Dream Djinn trials |
| **0.53.0** | the Troll Pit, the Gate District forge, the Hall of Beggars | **Reported from play: broker the peace with the lava trolls, then kill them for experience, and only the troll you clicked fights back.** Pacifying a troll blanks its `Valid Targets=`, so its neighbours' `CEntityBehaviorStateSetClosestTarget` has nothing to acquire, while `Target shooter if hit=1` lets the one you struck retaliate -- and the engine has no call for help at all. **The alarm that would have covered it existed and was switched off on purpose**, behind a `Troll Peace Keeper` check written in 0.29.0 so an accidental swing could not blow the peace; `qa.md` recorded that as a passing row, and play showed it was a hole. **The chief now comes and names what you spent** -- one of three variants, picked from whether you stood the rite, carried the ore terms, or only argued their case upstairs -- and then the pit becomes a pit again. **Deliberately not a `CGoToCombatAction` broadcast**: 0.29.0 measured that at 80-94 trolls converging and cut it, so this restores target type, the `Enemy` category and each troll's own hostile specifier and lets them acquire you at their shipped `Max Distance=550`, which scales engagement with distance instead of pushing the whole pit. The speech lands first and hostility follows six seconds later, the way the shipped desecration relay already does it. **Two men above ever find out**: Eduardo's trade was secured by nothing but the chief's word and your face, so it dies with him and he learns it from a man knocking on rock that has stopped answering -- recorded whether you admit it or lie -- and Enrique, who withdrew the contract because you argued at him and then watched it happen for free, tells you he could ask which kind of fool that makes him and is choosing not to |
| **0.52.0** | every creature that barks, game-wide | **A playthrough reported that the barks are good but a crowded fight never stops talking, and the arithmetic agreed.** A bark is diluted by padding inside a `CRandomAction`: the engine picks one array entry uniformly and only one of them is the bark bank. Across all **96 cans** `Shoot Completed` sat at **one in four** -- and **that hook is per-creature**, so six enemies swing six times as often and the group barked more than once per swing-round, which is exactly the complaint. It is now **1/8**. **The wounded hook is left byte-for-byte as it shipped** at 1/6: the player strikes one creature at a time, so its rate cannot multiply with the crowd, it was never the reported problem, and it is what keeps a solitary fight from going silent. **The padding turned out to be load-bearing**: `CActionSelectSkill` is not a no-op, it chooses the creature's next attack, and the three shaman cans encode a **1 Spike : 2 Static Charge** spell mix in theirs. So every pad count was set by cycling each can's *own* sequence and snapping the target to a multiple of its period -- the shamans sit at **1/7** rather than 1/8 for that reason, since the pad count is the denominator *minus one* and 7 is not a multiple of 3. **No can's skill selection changed.** The better design, one shared cooldown so a crowd barks at a lone enemy's rate, was **measured and rejected**: all four primitives are heavy vanilla idiom, but vanilla's 13 death-hook delays all use `Delay=0` or `0.1` and **none** delays a delete past a death, and a lock whose holder dies mid-cooldown would silence every bark in the game |

The **67 releases before those** are one line each in [`docs/changelog.md`](docs/changelog.md).

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
