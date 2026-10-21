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
-- currently [0.71.10](https://github.com/EricHype/LionheartFixt/releases/tag/v0.71.10).

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
| **0.71.10** | Montserrat, the cellar | **The warden's whole conversation could never be reached, and one of the six ways out of the pen went with it.** His tree is written for a man at the bars talking to a prisoner -- *"&lt;A ring of keys hangs from his belt, where you cannot reach it.&gt; ... nobody opens that door until she sends for you. So sit"* -- and four of its replies, behind Speech 40 and Charisma 7, reach the node that fires `escort`. **That is the speech route out of the cellar.** His only interaction was `GetCloseThenTalk` at reach 110 on a generator across the guard room; the nearest spot a prisoner can stand is **298** away, so the scene and the route could never be entered. Mixxer5 reported it as *"you can't talk to either of the NPCs from inside of the cell"*; 0.71.8 fixed Brother Pau and left this one, and then 0.71.9's own routes table listed the speech route as working. He now spawns at the cell door, **walks over at t=75** and opens the scene himself, and goes back to his stool when you dismiss him, so the position he has always sat in becomes the result of a scene instead of an unexplained starting state. **Not at t=2, which is the trap:** `escort` fades at three seconds and relocates at four, so a Speech 40 character offered the deal on waking would be out of the cellar before reaching Pau, and the best talkers would be the ones who skipped the one character written to explain what these people do with prisoners. The t=45 glance stays where it is, the automatic escort stays at t=100, and all three carry the same four-way escaped guard |
| **0.71.9** | Montserrat, the gate and the hall | **The peaceful route stops reading as the player being stupid.** Mixxer5's second report on issue #11 is not a wiring fault, it is that surrendering at the gate *derails the story*, and the check bears them out: all three patrons send you to **look**, not to fight -- Javier's *"see what has happened"*, Cedric's *"see what you can discover"*, Jafar's *"see if our enemies have stolen the Crown of Thorns"*. Walking in to be taken to whoever is in charge carries out that brief exactly. **The game simply never let the player say so.** Of the four ways through the sentry's challenge, a deceptive character got a bluff and a Demokin or Sylvant got a racial out, and everybody else had four words of bare compliance with no reason attached. Two new replies fix that, neither of them gated: one states the brief, and one names the trap out loud, which the sentry answers without softening it -- *"I was told to bring you up alive. That is the whole of my orders, and I do not ask after the rest."* **And the wounded assassin stops being abandoned by men who are standing in the room.** 0.71.7 gated his plea on `Assassin`, which is one generator 450 away that starts switched off, while the pack 291 away carries no name at all and so was invisible to the gate. But a correct gate alone would have **deleted his scene** on the peaceful route, where the player kills nobody and his side is alive by definition. So he gets a second opening for when they are still standing, and the gate now chooses which true thing he says rather than whether he exists |
| **0.71.8** | Montserrat, the cellar | **A bug 0.71.7 shipped, and the cell Brother Pau always said he was in.** 0.71.7 connected Montserrat's loud escape. It also wired the wrong branch. `guard room poly` rolls Sneak 30 when you cross the warden's room after picking the lock, and **on success** it fired the relay that tells the abbey -- so beating the check turned all of Montserrat hostile while the balloon told you that you had slipped past unseen, and because being caught reached the same flag through `handler fights`, **the skill check decided only whether the warden swung at you**. Success now sets its own checker, `Fixt slipped out`. It had to be a new flag and not a deletion: `pen setup` waits 100 seconds and escorts you upstairs unless one of those flags is set, so removing the bad call on its own would have traded a wrong flag for a wrong teleport. **And the gap that bug was hiding:** a player who picked the lock and then stayed in the cell block set nothing, so at 100 seconds the warden escorted a prisoner standing in an open doorway. The escort now asks `CIsDoorOpenAction` first, which is the actual question and needs no new state -- whereas setting `Fixt slipped out` when the lock is picked would have made `guard room poly` skip the Sneak check entirely and delete the lockpick route's whole risk. **The pen itself is rebuilt.** Pau's opening line has read *"In the next cell, an old man in what was a habit sits with his back to the bars"* since 0.11.0, while he sat in the open outside the cells; he now has a compartment of his own behind the player's east barred wall, 64 from the nearest spot inside the cell against a reach of 110, with his own door, and a poly at the bars starts the conversation so the player is not left guessing that the floor is clickable. **And a map crash:** that door had been cloned as a plain `CEntityBase` carrying `Cur Sequence=Idle`, which `Door2` has no animation for. The south of the cellar is dressed as the larder it is, with one chest |

The **115 releases around those** are one line each in [`docs/changelog.md`](docs/changelog.md).

Everything the shipped game defines and then references from nothing -- unplaced quest items, the enemy cans that nothing spawns, and why that count was first reported as 48 and is honestly zero, two whole summon tiers, and which of them Fixt has since picked up -- is surveyed in [`docs/unused-content.md`](docs/unused-content.md), along with the four ways that survey was wrong before it was right.

Three things were **read and deliberately left alone**, and the reasoning is in the release
notes: Torquemada's *purify the shadow dryad* quest (she cannot be killed; unfinished, not
cut), the Mountain Pass's sealed door (no map behind it), and the Act 8 goblin companion
arcs (they return with Act 8).

## Status

**0.1.0 through 0.71.10 are published**, and every act of the game has been surveyed, built and
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
