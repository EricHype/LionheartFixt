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
-- currently [0.74.0](https://github.com/EricHype/LionheartFixt/releases/tag/v0.74.0).

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
| **0.74.0** | the magic-wand loot pool | **Five wands have never worked, and for one reason.** `Skills/Fake Wand Spells/*` all carry `Display and Cast Requirements=CIsEqualTo(0,1)`, permanently false, and a spell that cannot be displayed can never be equipped or cast. `Open Locks` was the barest of them, a description and nothing else, pooled at **3 Rare** where it could drop. **`Rigor Mortis` turned out to be finished**, 5.4 KB of working freeze that has never run, carrying `Target=%trigger`, **the only one in the archive** against 32,021 correct references, and a sign error that made its victim **75% faster** where the text promised slowed to 75%. Each wand now has its own spell at **`ManaUse=CConstant 0`** in a new top-level group, **Wand Magic**, castable only while the wand is held. **`CPlugInBehaviorWand` is used by none of it**: its charge count is re-read rather than kept, so it never decrements, and it disables its own spell when it believes the count is zero. A wand's limit is a **Wand Charge** instead, a stackable item the spell removes one of per cast, sold rarely by Quinn and Weng Choi and dropping at a wand's own weight. All **18** wand additions leave their group so no wand can carry two spells. Also fixed: **450** baked into all eight pre-made characters, which made every wand spell free; fifteen effect numbers read off the item rather than the spell, so Lesser Healing healed nothing; and `Value Differential` being **the row a spell is drawn in**, not merely a gate |
| **0.73.1** | Montserrat, and the three patrons | **Brother Montgomerie is credited to players who never met him.** He fires only when the snakebreed are all dead, which is false by definition on the peaceful route, and that is **correct**: `sahar word given` already activates the handoff quest, his own scene carries no quest actions or states at all, and Brother Pau has already said the monks were taken north alive, so a monk crawling out of the sanctum while Sahar's snakebreed coil around the reliquary is an incoherent scene rather than a missing one. Mixxer5's report of his absence is therefore **adjudicated, not fixed**. What is a defect is the attribution: Javier, Cedric, Raphael and the quest log all told a peaceful player that a man they never met gave them their orders. The state could not be split -- **13** `CIsQuestStateTheCurrentStateAction` checks across four trees test `SAXRA7U2` as the current state, **seven of them Brother Michel's act 3 entry**, so a separate peaceful state would lock him out of act 3 -- so its wording is neutral now and the dialogue branches instead, on a record written where Sahar gives her word. Each patron gets a variant of his own line crediting the assassin, cloned from the original node with one sentence substituted so the replies cannot drift, and **11 replies** are split by route |
| **0.73.0** | the ending, and everyone who travelled with you | **Your companions vanished at the credits.** The ending slides covered the five orders, England, and exactly one person -- Grace O'Malley -- while Cervantes, Cortes, Jehanne, Grumdjum and the rest simply stopped existing. **47 slides** now say what became of each of them, in the register the 27 faction slides use, and the branch is not merely alive-or-dead: a companion is tracked as **never met, travelled with you, died without you, or died in your service**, and where the game already recorded more than that the slide reads it. So Jehanne has five endings including **released from the curse** and **killed for the Lance**; Cortes has five including all three verdicts in the Shylocke dispute; Diego has one for being **sold to the cult that wanted him dead**; Darsh has one for never coming out of the goblin camp, after which the Warrens argue for a fortnight about the red spice against the grey; and Fernand's turns on whether Juan lived. **And it repairs 0.72.0's own companion growth, which was gated on `CCheckExistenceAction` -- presence in a map, not companionship.** There is no companionship test in the engine, so Joan of Arc, hostile in the Crypt until talked down, was being handed +5 HP and +3 AC every time the player levelled in her gallery. **Two beats restored that have never played in any copy of the game:** `500 feather`, Don Quixote dissolving after you talk him out of existing, and `206 cervantes dies`, **39 KB recorded**, the shade thanking you for killing the author |

The **122 releases around those** are one line each in [`docs/changelog.md`](docs/changelog.md).

Everything the shipped game defines and then references from nothing -- unplaced quest items, the enemy cans that nothing spawns, and why that count was first reported as 48 and is honestly zero, two whole summon tiers, and which of them Fixt has since picked up -- is surveyed in [`docs/unused-content.md`](docs/unused-content.md), along with the four ways that survey was wrong before it was right.

Three things were **read and deliberately left alone**, and the reasoning is in the release
notes: Torquemada's *purify the shadow dryad* quest (she cannot be killed; unfinished, not
cut), the Mountain Pass's sealed door (no map behind it), and the Act 8 goblin companion
arcs (they return with Act 8).

## Status

**0.1.0 through 0.74.0 are published**, and every act of the game has been surveyed, built and
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
a cutscene that could not end, a horse built on a wolf, and a crash. What a playthrough finds is repaired on
`main` and cut as a patch release.

**The backlog is countable rather than impressionistic.** Of the 2,051 rows in
[`docs/qa.md`](docs/qa.md), **750 across 72 of its 100 release sections carry no pass or fail note at
all**, and they concentrate in everything after 0.55.0. Worth playing first, in this order: companion
growth (`CG1`, which decides whether an engine hook nothing in the shipped game ever used actually
fires), the Montserrat cellar (`UC`, `SN`, `WA`, `HW`, `WD`), the Inquisition chambers (`TQ`, `RJ`),
the ending slides, the Lava Troll Hide (`TH1`-`TH8`), Fernand's combat AI (`FA1`-`FA6`), the trolls
(`LT1`-`LT12`) and all of 0.30.0 (`GB`, `MF`, `GL`).

**What a playthrough does not find, a static rule sometimes can.** 0.71.10's headline shipped
broken: its builder wrote a field name into a block's indentation, so the scene that release existed
for was seven dead lines, and every automated gate passed it -- `resource_format` round-tripped it,
the array counts agreed, and the class name on the first line was real. It was found a release later
by **A0.18**, a rule that rejects a value which is itself an assignment, measured against the
**4,035,942** `key=value` lines of the shipped game to prove it could not misfire. 0.72.0 carries
both the rule and the repair.

Every release's automated gates pass -- `tools/validate.py`, `tools/reachability.py`, which checks
that every node this mod adds can still be arrived at, `tools/test_triggers.py` for the map builders
in `tools/lhbuild.py`, and `tools/test_md2bbcode.py` for the forum-post converter. The human
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

Measured, so you can judge an upgrade mid-playthrough: Fixt touches **98 map files** (95 edited, 3
created) and **624 non-map files**. A save already in progress picks up all 624 of the second
kind -- dialogue, items, races, quests, perks, requirement checks -- and picks up a map's changes
only for the maps it has not yet entered. Where there is a choice, this mod now prefers the dialogue
side for that reason: companion growth installs from the tree every companion opens on a click rather
than from a map, precisely so that it reaches a game you are already playing.
