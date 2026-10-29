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
| **0.81.0** | Sahar in red | **She is red.** Her texture is genuinely repainted inside her own mesh, after three releases that tried to do it with an engine colour feature that turns out not to reach monsters at all. The game's own graphics library does the encoding, which means **any character in the game can now be recoloured** -- the first time this project has been able to change what something looks like rather than only what it does |
| **0.80.2** | the garrison holds, and she stands still to say so | **The garrison was never going to leave.** Four releases went into making the snakebreed march out of the abbey once Sahar gives you her ring, and that was the wrong idea: they have taken the abbey and are **holding** it, which is the whole reason her ring is worth carrying -- she cannot spare a guard, so she gives you a token instead. They now stand down and stay where they are. **She also stands still while she talks** instead of wandering off mid-sentence. And **0.80.0's claim that she is no longer green was wrong**; that is corrected here, and the recolour is still being worked on |
| **0.80.1** | the summit picked the wrong cutscene | **[Issue #14.](https://github.com/EricHype/LionheartFixt/issues/14)** Finish the Knights of Saladin initiation, accept Amir's invitation to the Cathedral, and the cutscene **stalls on Lord Javier's welcome**. The Cathedral chooses which summit to play from the route you took, but Amir's route never told it anything, so it fell back to whichever faction you already belonged to and played that one instead. Every faction member who finishes the Saladin initiation hit this. The summit itself is original-game content that **the original game shipped unreachable** |
| **0.80.0** | the captain in red, and what Machiavelli makes of her | **Sahar stops being a reskinned rank-and-file boss.** She has **her own model**. *(0.80.0 also claimed she was no longer green. She is -- see 0.80.2: her model is genuinely hers, but the engine's hue remapper does not reach a monster's texture.)* **She rallies her garrison** rather than hitting harder, so killing her should visibly weaken what is left standing. And **act 3 finally remembers what you did at the sanctum**: killing her used to be indistinguishable from never going, and Machiavelli now has four reactions where he had two -- he admires taking her safe conduct and then using it, and has rather less to say about simply killing her |
| **0.79.9** | the captain, and a staff on a narrow canvas | **Six fixes from one afternoon of play, two of them mine from 0.79.3 and 0.79.6.** The warden **skated and drifted into Brother Pau's cell door**, because 0.79.3 moved his spawn onto the marker he was supposed to walk to and left the walk behind. **Sahar's conversation could be lost to a stray keypress** and never recovered; she now has the gate sentry's talk interaction so she can be hailed again, and a dismissive line once you carry her ring. **Her confrontation watched 271 units of a 1,974-unit gap**, so coming up the prison stair and heading east walked past her and she was never spawned at all. Plus a camera on the escort scene, and **the staff skill icon centred** -- it sat on a 19x48 canvas where 85 of 87 skill icons are 48x48 |
| **0.79.8** | the garrison finally leaves | **The rout has never worked.** All three abbey maps told the garrison to walk to an exit marker with an **empty** movement block, which vanilla fills 4,735 times out of 4,735 -- so they walked at the marker through the walls, never arrived, and were never removed. The standing-down worked, which is why two players could describe the symptom exactly and nobody could name the cause. Also: **pressing Escape on the jailer cloned a companion in Barcelona**, closing his conversation once deleted the Speech route out of the cell, walking down the prison stair early silently destroyed the whole prison scene, and arriving up it left Level 1's great door dead. Two new gate checks for the classes behind all of it |
| **0.79.7** | what the cellar costs you | **Two Karma penalties: breaking Sahar's truce at -100, killing Brother Pau at -200.** Set against the game's own scale, where -50 is the price of raising a hand to a civilian and the deliberate betrayals run -200 to -800. Pau's had to go on his generator rather than his can, because a generator replaces the can's death slot -- the same defect that made the Lava Troll Hide dead code. Attacking a calmed creature during the parley still costs the fight and not Karma, since you have given no word yet |
| **0.79.6** | a truce you could not break | **Attacking a calmed snakebreed cost you nothing, because only two entities in the whole act react to being hit** -- the Grove Sentry and the warden. Everything else that gets pacified cannot fight back and nothing notices it dying, which is Mixxer5's issue #11 report word for word. The garrison now carries the sentry's own damaged script, and Sahar carries one pointing at a new `truce broken` relay. Only Level 2 needs it, because the rout deletes everyone else and she deliberately stays. Also found: **the parley pacifier was short a whole family**, since the accept block calms `Assassin` and the parley block did not |
| **0.79.5** | the warden's memory | **Escape by the drain, walk back to the warden, and he greets you with "Still here. Good. Sit."** The pen's timers all stop when you get out; his conversation never checked. Since the pen's design already says a quiet escape leaves the abbey calm and being **caught** makes it hostile, presenting yourself to him now counts as being caught: he draws, using the relay his damaged script already fires. No new line, no new entity. The cost is that clicking him out of curiosity loses the calm abbey |
| **0.79.4** | Sahar's garrison | **A snakebreed attacking during the parley exposed that three quarters of the garrison was never addressable by name.** A spawn with a blank `New Name` is called what its can calls it, and the snakebreed cans are not named after their files: Venom is **Snakebreed Viper**, Boss is **Snakebreed Crusher**. Every list in the three Montserrat maps was written from the filenames, so **eleven targeted names match nothing in the game** and `Snakebreed Summoner` was never addressed at all. The same lists pacify, rout and re-aggro, so the parley stood down one family while the rest kept attacking, and the rout left them standing. Names only, 36 sites. Map-side, so it needs a save that has not been to Montserrat |
| **0.79.3** | the Montserrat pen | **Two defects found in play.** The warden stood **inside the wall**: 0.71.10 moved him next to the cell door by coordinate alone, and a save shows the engine put him exactly there, embedded. Nothing in a map file carries collision, so rather than guess again he returns to the stool he occupied for sixty releases and his reach goes 110 to 320, which is ordinary -- 380 shipped interaction specifiers use 300 or more. And **the drain could not be found after Brother Pau described it**: finding it with Perception shows a Secret Icon over the grate, while being told only made it usable, so the player who asked was worse off than the player who stumbled. Pau now shows it too |
| **0.79.2** | the Sceptre of Bone | **Reported as the second defect in issue #12 by Przemyslaw92pl: Relican will not complete the Sceptre of Bone quest, and the sceptre cannot be used. Both are right, and the reporter's guess -- picking it up before the dialogue -- is the diagnosis.** 0.39.0's middle quest state for the empty shell is set in **one** place, the shell's own pickup action, and only if Relican has already named the errand -- while **all three** bind routes require it. Loot DaVinci's secret chamber early and the shell can never be filled, so the Dark Wielder initiation cannot pass task 1. Vanilla was robust to the same early loot. All three gates now ask whether the errand was ever opened, which reaches saves that are already stuck; dropping and re-taking the sceptre also works without the patch. Second, **the shell was built in the wrong shape**: the Wielder shell with the same authored description is a weapon-slot club doing 1-3 where its spirited twin does 2-8, and ours was slotless with no attack at all. Rebuilt from the spirited sceptre under that rule, minus what the spirit paid for -- the eight skill bonuses and the Karma penalty |
| **0.79.1** | four trinkets | **Four trinket additions whose curve was never filled in, the same defect class 0.75.3 addressed on ten others.** Raised by Laz Sundays on the rpgcodex thread. Under 0.75.3's rule -- integers only, today's value as the floor and the middle, ceiling one step above -- `Voodoo` belt and necklace go to **1/1/2** across four Tribal branches, `Divine Attunement` to **2/2/3** across four Divine branches, `the Sylvant` to **4/4/5** on melee. A plain piece is unchanged; the extra point appears only when the item carries another enchantment, because **a flat addition pins its value band to its own declared price contribution** -- the fact 0.79.0 turned up and the reason these never travelled. No item's price moves. Two modifiers stay literal on purpose: the `Number of Voodoo Items` **set counter**, which would break the pair's bonus if it scaled, and the Sylvant's race-gated bonuses. **"Magery" was dropped because it is not weak** -- it adds +0.4 to a mana-rate attribute based at 0.0334, about thirteen times the base |
| **0.79.0** | the mage's armour | **The first armour work: a flat expression inside an otherwise scaling addition, and two value ceilings no armour reaches.** Raised by Laz Sundays on the rpgcodex thread. **`of the Mage` carries a flat expression beside four scaling ones** -- its four resistances climb 5 to 20 with the item's value while `skillbonus`, shared by twelve skill modifiers, is a literal 1, so a **5 Unique** armour gives +1 skill point per magical branch forever. Same defect as Venom's in 0.77.0. It now scales 1 to 5, the floor untouched, and the description's hardcoded "+1" becomes the interpolated token so it cannot drift again. Second, **two ceilings are out of reach**: generated armour runs to a dearest-ever **10,025** gold, while `of the Mage` topped at 11,000 and `Deepest Winter` at 11,500, so neither ever paid its maximum. Both come to 9,000. Deliberately left: `Feral Power`, whose value band is **inert**; `Deepest Winter`'s amount, already 7 where the post asked for 5; and "Magery", which turns out to be `Mana Stream` and belongs with the flat conversions |
| **0.78.1** | Snakebiting and Venom, again | **Supersedes 0.78.0, after a player asked whether other weapons already have damage-over-time. They do, and I had not counted them** -- 111 resources use `CXRPGDamageOverTime`, not the 23 I reported, and `Double Biting` is one of them despite my calling it instant. **The game has its own scale**, in shared canned expressions every monster poison resolves through: Weak 0.20, Medium 0.40, Strong 0.60 damage a second, with the weapon suffixes at 0.35 to 1.20. **0.78.0 put both poisons at 5.4 -- four and a half times anything in the game.** The state before it was already right, both at 1.20 a second, so the magnitudes are reverted. Kept: 0.77.3's reachable value ceilings, Venom's chance finally reaching the 50% 0.77.0 set, its damage scaling with its band at all, and the decompiled refresh finding |

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
