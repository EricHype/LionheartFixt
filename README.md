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
-- currently [0.15.0](https://github.com/EricHype/LionheartFixt/releases/tag/v0.15.0).

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

| Release | Where | What |
|---|---|---|
| **0.1.0 - 0.1.4** The Horde | Wilderness | The goblins become a faction you can join, with three ranks that accumulate across services on the shipped Saladin/Templar pattern; the camp reads your rank, your build and your history; two finished characters that shipped with zero map references are placed; the Crossroads patrol is disarmed and carries a counter-contract on Esteban |
| **0.2.0** What Was Written | Wilderness | Dialogue Black Isle finished and never wired -- the Goblin Girl's follow behaviour, the Khan's war campaign against Barcelona, Grumdjum after the dryad, Rakeb's return greetings |
| **0.3.0** The Knights of Saladin | four acts | The Dream Djinni trials award the rank, not just the title, which unlocks twenty replies; the Sacred Scimitar questline -- fully authored, unstartable, broken at all three ends -- restored |
| **0.4.0 / 0.4.1** Quinn's Reagents | Gate District | The first new content: three errands for the herbalist, each opening a healing tier above vanilla's Extra Healing, built almost entirely from items and potions the game shipped and never used. 0.4.1 repaired a structural DialogTree defect that had been silently disabling 47 replies |
| **0.5.0 / 0.5.1** The Thieves' Guild | Sewers | Juanita's cut final job, in a house built for it (the project's first new map); the thieves' vault as a real heist with five ways past its door; peace with the lava trolls; the Helpful Wererat. 0.5.1 fixed two crashes and added the `Model=` / `Cur Sequence=` checks to `validate.py` |
| **0.6.0** The Port District | Port District | Fernand Desoto -- the game's fourth companion, written and wired on both sides and reachable by nothing -- becomes reachable because his brother Juan can finally be saved; the fish monger's hidden perk for the vodyanoi skulls |
| **0.7.0** The Road North | Gate District, Temple District | The Knights of Saladin can be served, not only joined: Amir's Montserrat directions get the one action that reveals the abbey; the rank ladder; the Cathedral summit's three deleted parts rebuilt for the callers that survived them |
| **0.8.0** The Gate District Remainder | Gate District | DaVinci's spirit-gem branch, Weng Choi's special customer, Merchant Lope's Perception haggle, two return greetings, the goblin sapper's name; the district's 42 orphaned replies accounted for one by one |
| **0.8.1 - 0.8.4** repairs | | What the first playthrough found: Fernand's draught, Quinn's errands, the trolls' peace, the wererat's name, Amir's directions for a Favored One, every skull counting toward the fish monger's perk. Each cut on a branch from the previous tag with only the repair |
| **0.9.0** The Temple District | Temple District, Montaillou | Machiavelli keeps his promise or his threat at the Montaillou inn (he was on no map at all); Na Roqua greets a friend of the Cathars as one, on two voiced nodes nothing reached; Torquemada acknowledges his own Inquisitor for the Khan; Auric, Javier and Cervantes remember who they are talking to |
| **0.9.1** Around Barcelona | Mongol Camp, Port tavern | The gate guard greets a welcomed player instead of falling silent for the rest of the game; Brendan Sullivan's clover -- a line, an icon and a Luck check the game shipped and never connected |
| **0.10.0** Montserrat | Montserrat, Montaillou | The act was five maps and one conversation. Now: human assassins and Summoners in the packs; Sir Tomas de Vilanova's journal at the gate; a wounded assassin who talks; Sahar, the rearguard's captain, with phases before Montgomerie; a mid-hall ambush, a needle trap, a sentry who calls for help, a trapped chest; the sanctum re-dressed as an abbey with ten hover-text stops; and seven build levers, from Sneak to the Inquisition's sealed order |
| **0.10.1 - 0.10.3** repairs | | The thieves' stash chests say what they do and need a witness; the Inquisition jailor's Rites of Confession can be passed; the Templar initiation survives Esteban; Auric and Javier remember being attacked |
| **0.11.0** The Prisoner of Montserrat | Montserrat, Montaillou, the Crypt | A way through the invasion that is not a fight against every pack: give yourself up at the gate; wake in the abbey's undercroft (a new map) with five ways out of the cell; a garrison that stands down for a delivery; Sahar with three ends and a ring that three people read differently; the rout. Also the trolls' ore chest and a Wasp Queen |
| **0.12.0** La Calle Perdida | La Calle Perdida, the Ether Plane, the four Magic Nodes, Galileo's cell | The Enchanter can be told the truth; the wizards know you killed Relican; Cedric, Relican and Galileo remember being attacked; a Dark Wielder can break with Relican and fight him; the red Magic Nodes get Cedric's quest, a hover line and a ward; the wipeout kills the Wielders it generates. Also Fernand's reach |
| **0.13.0** The Road North | The Plains, the Mountain Pass, the ogre caves, the Abandoned Cave | The spirits' warning about the Dark Inquisitors; the rogues' ritual finishes; Shylocke's collector says whose men they are and can be haggled, talked or perk-routed past; the crosses read; a Wielder and a Dark Wielder greeted as such; an Inquisitor helps Diego as a brother and reports to Torquemada; the ogres' charm ends when Aka Manah does; Tremblethorn's dark half; and Bernat Sicre, stuck six weeks in the Abandoned Cave |
| **0.14.0** Montaillou | Montaillou, Toulouse, the witch's hut, the grove | The gate challenge that reads your order; the titans of Toulouse talked out of killing their fugitive, and the fugitive talked into going home; Na Roqua's Inquisitor greeting, her chicken, her secret stash and her past; the Bishop's third lead; Andre's corpse scene; the warden, the shepherd's warning and Lethos's errand. Then the village reads you: the guild, the Horde, the necromancer, the Wielder, the tainted face, the trader and the shepherd's careful eyes |
| **0.15.0** Toulouse | Toulouse, the titan camp, the prisoner pen | The two flags the act read and never set, which cost the bluff at the pen and everything the prisoners know about the fugitive; the guard's mercury bribe; the warning he never gave; Menoetius, whose generator named him Rhea; and the news of the titans' leaving, which never reached Montaillou. Then Toulouse reads you -- the spirit you carry, the titles you earned, a necromancer on the eater of memories, an Inquisitor on the man who drowned the world -- and the child of the tribe, the pen, and the ogres get voices |

Three things were **read and deliberately left alone**, and the reasoning is in the release
notes: Torquemada's *purify the shadow dryad* quest (she cannot be killed; unfinished, not
cut), the Mountain Pass's sealed door (no map behind it), and the Act 8 goblin companion
arcs (they return with Act 8).

## Status

**0.1.0 through 0.15.0 are published.** The last four -- 0.15.0 Toulouse, 0.14.0 Montaillou,
0.13.0 The Road North and 0.12.0 La Calle Perdida -- are built and entirely unplayed, as are
0.11.0's Sahar, ring and rout. What the playthrough finds is repaired on `main` and cut as
patch releases. Every release's
automated gate (`tools/validate.py`) passes; the human gates are recorded per release in
[`docs/qa.md`](docs/qa.md), and most of what shipped after 0.4.0 has been played once by one
tester, which is how the 0.8.x repairs were found.

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
| [`docs/qa.md`](docs/qa.md) | every case a release has to pass, and which have |
| [`docs/playtest-guide/`](docs/playtest-guide/) | the same cases as a route to walk, built by `build.py` |
| [`dist/`](dist/) | release notes and forum posts per version; `README.txt` is what a player reads after unzipping |
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
