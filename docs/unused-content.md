# Unused content - the survey and the backlog

Everything the shipped game defines and then references from nothing: items, enemies, skills and
summons. This exists so the survey is not re-derived every time the question comes up, and so that a
claim about it can be **checked** rather than trusted.

Measured against `data.dat.vanilla.bak` and cross-checked against Fixt's own `files/`, because
several of these have already been used by Fixt and would otherwise read as still open.

**The current state is [Re-measured at 0.94.0](#re-measured-at-0940----the-live-list).** Anything built,
ruled out or adjudicated is in [`unused-content-resolved.md`](unused-content-resolved.md), which is where
older release notes' references to this file now lead. **Search it before calling a lead new.**

**Read [How this was measured](#how-this-was-measured) before acting on any number here.** Four of the
findings in this document were wrong on the first attempt, one of them badly, and the ways they were
wrong are more reusable than the results.

---

## Contents

- [**Re-measured at 0.94.0**](#re-measured-at-0940----the-live-list) -- what is open, what came back clean, orphaned audio, the misrouted reply
- [Summary](#summary)
- [Open leads in detail](#open-leads-in-detail) -- the Shadow Dryad, inert attributes
- [Voiceover on nodes nobody can reach](#voiceover-on-nodes-nobody-can-reach----the-sweep-the-first-one-inverted)
- [Orphaned art](#orphaned-art----the-axis-this-survey-never-looked-at)
- [The three kinds of orphaned node](#the-three-kinds-of-orphaned-node) -- classify before building
- [How this was measured](#how-this-was-measured)
- [**Resolved**](unused-content-resolved.md) -- everything built, ruled out or adjudicated, with the reasoning

---


## Re-measured at 0.94.0 -- the live list

**Start here.** Everything in this section was measured against the 0.94.0 build on 2026-11-04.

### What came back open

| lead | size | what it needs |
|---|---|---|
| `MX_FACT_KNIGHTTEMPLAR1` | 13 s | a Templar moment. Every other faction's theme plays somewhere |
| named combat voice sets | 24 files | `Lucious Titan_*`, `DRUID_*`, `Goblin Grumjum_*`, `River Dryad_death_*`, `DRUNKARD_death_*`. Nothing names them, so those characters may be fighting in someone else's voice. Unclassified |
| `200 beast compliment`, `200 divine compliment` | 124 KB | a trigger on fighting well |
| `Purify the Shadow Dryad` | 732 KB | a policy decision, see entry 1 below. The biggest story thread left |

### Planned, not yet built

| item | what it needs |
|---|---|
| **Killing tree Brambles as an evil act for the Dark Wielders** | The author's request. His tree has no way to be attacked: `Brambles Roots` is scenery with no scripts, and `Brambles Head` is named by scripts but not defined as a part in `Calle Perdida.zax`, so find it first. It needs a reachable attack, a death flag, and a Dark Wielder slide line to replace *"Brambles stayed a tree"* |
| Curing Brambles and then killing the man | `Brambles as Wizard.can` has no death script, so the slides still send him home to his grandchildren. A flag through `CForEachPlayerAction`, plus a variant of each slide that mentions the cure. It would fire for any death of his, including `80 war` |
| A Dark Wielder turning on Relican at `80 war` | The Relican slide does not read it, and covering it doubles the nine Dark Wielder versions |

### What came back clean, which is why the list is short

| check | result |
|---|---|
| quests with a live state that nothing can close | **0** of 163 |
| maps nothing names | **1**, `Test Maps/Lars/polygons` |
| additions no item can roll | **0** of 552 |
| equipment nothing hands out | **1**, `Unarmed`, which is the fists |
| weapon pools | all 16 bases populated. The three Great weapons were filled in 0.89.0, and [they are handled](unused-content-resolved.md#great-weapons-enchantable-since-0890) despite how rarely they drop |

### Orphaned audio -- a new axis

The art survey never had an audio twin. `tools/orphan_audio.py` runs it:

| | tracks | named by nothing |
|---|---|---|
| music and ambient | 262 | **9**, 1.5 MB, after 0.94.0 placed `MX_CHAMB_MED` |
| all non-voiceover audio | 1,542 | **129**, 3.06 MB |

**The first pass said 457 files and 15.5 MB, and most of that was false.** It searched text field
values, and spell and creature sounds are referenced from inside binary `.mdl16` caches. A byte search
of every entry, every Fixt file and the exe is the only version to trust, and even it over-reports:
the 32 footsteps are surface folders of identically named `Zax Footstep...` files, and 14 weapon sounds
are numbered sets, so both are probably names the engine builds at runtime.

**The ten tracks are the reliable part**, because maps and trees name music in full, through
`CMixInSongAndPlayAmbientTrackAction{Song To Mix In=...}`, and that action works from a dialogue
reply as well as a map. Placing one is a single action, or a single field in a map's own
`Music Mix`. **The nine left:** `MX_FACT_KNIGHTTEMPLAR1`, `ForestAmbient01`, `ForestAmbient05`, `DesertWindAmbient02`,
`DesertWindAmbient03`, `OutsidePeopleAmbient`, `BarAmbient`, `FireEmbersAmbient02`, `Wolf Howl startgame`.

**`MX_CHAMB_MED` went to the cathedral crypt in 0.94.0**, on the author's ear: it is monks chanting,
2:18 long. That is a new placement and not a restoration. Nothing says where it was meant to go, and
"CHAMB" may well mean the Inquisition Chambers, whose Medium slot is also the `Main Menu` default.

**Each map has a `Music Mix` of three slots,** `Ambiant Song`, `Med Mix Song` and `Full Mix Song`.
Nothing here settles what selects between them; danger or combat is a guess from the names. `Main
Menu.ogg` fills the Medium slot on **46** maps and the Full slot on 24, so in those slots it reads as
an unset default rather than a choice. Barcelona's Medium slot is that default on 20 maps.

### The misrouted reply -- a fifth kind of orphan

The taxonomy below has unreachable branches, where no reply points at a node. 0.94.0 found the
neighbouring case, where a reply exists, asks exactly the right question, and goes somewhere else:

> **Reply:** *"I could try to speak with the Inquisition about the gem."* -> `10 Goodbye`
> **Unreachable, recorded, beside it:** `320 speak to inquisition`, *"Ah, I would owe you a great debt
> if you would speak to the Inquisition. Grazie!"*

`vo_reach.py` reports the node and has no way to suggest the reply, because a recording with nothing
pointing at it looks the same either way. `tools/misrouted_replies.py` ranks replies against
unreachable nodes by shared words. It is noisy, one real hit in 21 on its first run, so read both ends.

---

## Summary

| category | defined | still open |
|---|---|---|
| Quest items (`.InventoryItem`) | 14 unique | **0**. All used, or superseded drafts |
| Magic item recipes (`Misc Items/*.can`) | 91 | **0**. The enchantment pools were never wired to the master generator, fixed in 0.38.0 and 0.51.0 |
| Monster cans | 611 | **0** with art of their own. 56 are unreferenced, all tier variants, duplicates, drafts or tests |
| Skills (`.Skill`) | 92 | **0**. Nothing was cut |
| Summon tiers | 5 | **0**. Levels 4 and 5 restored in 0.37.0 |
| Perks (`.Perk`) | 98 | **0**. All five orphans awarded in 0.47.0 |
| Factions (`.Faction`) | 13 | **0**. One restored by Fixt |
| Voiced dialogue nodes | 1,573 recordings | **66** unreachable, **5.14 MB**, most of it now classified as draft or adjudicated (vanilla 204 / 19.27 MB) |
| Music and ambient | 262 tracks | **9**, **1.5 MB**, new in 0.94.0 -- see [the live list](#orphaned-audio----a-new-axis) |

The voiceover row was [measured backwards until
2026-10-11](#voiceover-on-nodes-nobody-can-reach----the-sweep-the-first-one-inverted). Its size no
longer measures what is missing: what remains is mostly recorded and replaced.

**Nothing in the unused set is missing art.** Across all 478 monster cans there are **zero**
unresolvable models and **zero** unresolvable races. The unused creatures are complete; they are
simply not placed.

---

## Open leads in detail

### 1. Purify the Shadow Dryad -- re-found here, and ruled out by 0.9.0

**Read this entry as a correction of the sweep, not as a lead.** The chain below is real and the
numbers are right, and **the conclusion drawn from them the first time was wrong**: this was called
"the best remaining lead in the game" by a reading that had not checked the project's own release
notes. 0.9.0 had already built the reachable half, measured the rest, and cut it for a reason the
voiceover join cannot see.

| 0.9.0's finding | |
|---|---|
| `407 killed khan`, the Inquisitor's own Khan report | **built by 0.9.0** -- so the dangling *"Are you ready for another task?"* in the current build is **this mod's own doing**, recorded there as permanent rather than pending |
| `401 already dead` and `402 tasks 3`'s pre-emptive report | **deliberately left orphaned**, because the only thing they lead to is a quest with no ending |
| `Weird Woman dead`, the flag the completion gates on | **a debug switch.** Its one setter in the shipped game is a part named `warp`, `Active=0`, commented *"This is to kill the Weird woman to test what happens when you kill her"*, beside an `Editor/Test Interaction`. No Montaillou map references it under any spelling |
| Na Roqua | **built to be unkillable**, three independent ways: `Has Hit Points=0`, a race carrying **AC 1000 / HP 10000** with full resistances across 11 presets, and a `Gotocombat` handler firing the `kicks you` relay that banishes the player to `01 Hamlet Exterior`. `CGoToCombatAction` naming her occurs **zero** times |
| being banished | **not a failure state but a written beat** -- the live Fournier questline ships dialogue for it: *"when I confronted her she used her magic to send me to a den of wolves"* |

So the two claims that made this look cheap are both wrong. **"Kill detection already exists" is
not usable detection**: the `V3X8REJC` reference in `Inquisition Chambers2.zax` covers only the
player who killed her *before* meeting Torquemada, and nothing legitimate can set the flag it keys
on. And **wiring `410` -> `411` and stopping** yields a quest the player can accept and never
finish, with the perk still unreachable, which is precisely what 0.9.0's scope would have shipped
before it was corrected.

**What this sweep adds is one fact, and it is a small one:** the reward perk's content. `Torquemada
Divine Boon` grants **+7 skill points to all four Divine branches** (Defensive, Divine Favor,
Fortitude, Smite), permanently, with an authored description -- and **the only file in the archive
that names it is this tree**, so no other route grants it. 0.9.0 recorded that node 412 "grants a
perk" without pricing it.

**What the work would actually be, if it is ever taken:** not a reply. Giving Na Roqua hit points,
conditioning or removing the banish, and writing a resolution -- which is authoring over a live
scene. 0.9.0 ruled that out when the project's standing rule was restore, do not author. **That rule
no longer holds** -- 0.53.0 wrote a scene and three quest-gated branches, 0.54.0 wrote a second
commission and a karma trade -- so this is now a **policy question for the author rather than a
measurement question**, and it is the only entry in this section that is. The cheaper shapes worth
weighing first, both of which leave her alive: resolve on the **banish** the game already writes
rather than on a death, or let a Speech-gated reply **lie** to Torquemada, which the node's own
*"I have already made arrangements to deal with the witch"* text already sounds like.

Everything below is the evidence, kept because it is accurate and was expensive to assemble twice:

| piece | state |
|---|---|

| piece | state |
|---|---|
| quest file | `Levels/1 Barcelona/Quests/Temple District/Purify the Shadow Dryad`, **3 authored states** |
| voiceover | `410` 148 KB, `411` 199 KB, `412` 217 KB, `401 already dead` 168 KB -- **732 KB** |
| the briefing | nodes `410 shadow dryad` and `411 shadow dryad 2`, written |
| the activation | `CActivateQuestStateAction{State=AM6C3B5E}`, written on node 411 |
| the gates | three requirement cans: `Torquemade requires Shadow Dryad NOT killed yet`, `Torquemada Requires Shadow Dryad Dead before meeting`, `Torquemade requires Shadow Dryad killed` |
| the completion | `CSetQuestSatusToCompletedAction` + `Get XP Frome=Killed Weird Woman`, written on node 411's second reply |
| ~~kill detection~~ | `Inquisition Chambers2.zax` references the return state `V3X8REJC`, **but only for the player who killed her before meeting Torquemada**, and it keys on a flag nothing legitimate sets. Not usable detection |
| the reward | `Perks/!NPC or Event Given Perks/Torquemada Divine Boon` -- **+7 skill points to all four Divine branches** (Defensive, Divine Favor, Fortitude, Smite), permanent, with an authored description. **Granted nowhere else in the game**: the only file in the archive that names it is this tree |
| the target | **Na Roqua**, live, helpful and talkable in Montaillou, masquerading as a Cathar perfecti -- **and unkillable by construction**, per the table above |

**The break the player can hear.** Node `407 killed khan` is reachable, and ends:

> I have known, child. I felt the blight lift from the forest as the beast drew its last breath. You
> have my gratitude. **Are you ready for another task?**

Its **only** reply is *"Thank you, Grand Inquisitor. I shall take my leave of you now."* The node that
**does** answer it, `401 already dead`, asks the same question in almost the same words and sends
*"Yes."* to `410 shadow dryad`, and nothing reaches `401 already dead` either. **Both of those facts
are 0.9.0's decisions, not vanilla's oversight** -- in vanilla `407` is unreachable too, so the
question is never asked. A first reading here also offered the id collision with the live
`401 tasks 2` as a plausible cause; it is not the cause, and that guess was made with the answer
already written down in releases.md.

Tracing the three quest states is what settles it:

| state | its text, abbreviated | referenced by |
|---|---|---|
| `AM6C3B5E` | Torquemada asks you to find and eliminate the shadow dryad | **only** `GrandInquisitor.DialogTree`, on the unreachable node |
| `S6JH3MKG` | "you must slay the shadow dryad" | **nothing at all** |
| `V3X8REJC` | return and tell him you have purified her | `Inquisition Chambers2.zax` **and** a requirement can |

So the mission is wired at the **end** and dead at the **start** -- except that the end it is wired
to cannot occur, which is the whole of 0.9.0's finding. The third checker,
`Torquemade requires Shadow Dryad killed`, is used by nobody and is exactly the gate a report-back
reply would need, so even the missing piece was pre-cut.

The shipped file even carries the developers' own markers next to all of it --
`Action work in progress=(shadow dryad quest not completed, then add shadow dryad quest)` and
`Action work in progress=(grant kickass Grand Inquisitor perk - add to exorcism and detection)`.

It is also a **real choice** rather than a chore: the Inquisition is asking the player to murder the
woman who helps them, and the tree already branches for having killed her before being asked. Na
Roqua's own `100 Return` greeting (9 replies, 63 KB recorded) is unreachable too, in the same vein.

**Na Roqua's own `100 Return`** greeting (9 replies, 63 KB recorded) is unreachable as well, and is a
**separate and open** lead: it needs no kill, no flag and no policy decision, only an entry. It is
listed in entry 4 and should not be bundled with the quest above.

**The orphan taxonomy is not what settles this one.** `Torquemada Divine Boon` is granted nowhere
else and nothing else activates this quest, so it is not a superseded draft -- it is the fourth
thing, which this document had not needed a name for until now: **adjudicated.** Finished content,
correctly identified, deliberately left dead by this mod for a recorded reason. Those look exactly
like leads, and only the release notes tell them apart.

### Derived attributes that no resource reads or writes

Fourteen of 184. **Stated precisely:** nothing outside each attribute's own definition names it in
a `Derived character attribute to modify=` or a `Character Attribute=`. That is not the same as
"the game ignores it" -- a positional attribute array means every character's cache file lists
every attribute name, so a plain text search finds ~765 false hits for each, and several of these
are plainly read by the engine rather than by data.

**Probably engine-internal, not findings:** `Action Points`, `Combat Speed`, `Magic Speed`,
`Sneak Speed Factor`.

**Designed mechanisms with no wiring at either end, which is the interesting list:**

* **`Backlash Fire Damage To Give Attacker`** and **`Should Give Backlash Fire Damage To Attacker
  Percentage`** -- a *second* retaliation mechanic, in fire, beside the physical one that works.
  The physical reflect is live (`Dragon Scales` 10%, the `Backlash` skill 20-35%); its fire twin
  is written by nothing. A pair of attributes, named consistently, wired to nothing.
* **`Is Wearing Necklace of Voodoo`** -- a set flag of exactly the shape `Number of Templar Items`
  uses, for a set that otherwise counts itself with `Number of Voodoo Items`. Nothing raises it
  and nothing reads it.
* **`FACTION LEADERS KILLED`** -- a Game Scripting Variable, the category Fixt uses for
  cross-act state, that no map or dialogue ever sets.
* **`Fast Talk Dialog Enhancer`** -- under `Perk and Trait Support/`, so a perk was meant to feed
  it and a dialogue check was meant to read it. Neither exists.
* **`Acid Damage Multiplier for Reverse Heal`** and **`Disease Damage Multiplier for Reverse
  Heal`** -- reverse-heal support for two damage schools, where the other schools are wired.
* **`Additional Poison Damage Minimum`** / **`Maximum`** -- a damage band nothing contributes to.
* **`Companion Follow Enabled`** -- worth a look against the companion work, since the overlay
  machinery is already understood.

None of these is restorable on its own: an attribute with no writer and no reader is a mechanism
that was specified and then not built, so using one means designing both ends. They are recorded
here as **design space that the engine already has a name for**, not as a repair backlog.

---

## Voiceover on nodes nobody can reach -- the sweep the first one inverted

Added 2026-10-11, after 0.55.0. With the original survey's open list empty, the question *"what else
is there?"* needed a new axis. This is that axis, and it is the largest one yet.

**The first voiceover sweep asked the wrong question.** It asked *"is every recording named after a
node?"* -- 1,314 of 1,330 matched, **98.8%**, so the corpus looked clean, and the 16 misses were
chased to the end and are [documented above](unused-content-resolved.md#orphaned-voiceover-is-the-strongest-signal-there-is).
It never asked the other direction: ***"can the player reach the node a recording sits on?"***

A line that was written, cast and performed, whose node is spelled perfectly and which nothing in the
game can enter, **passes the first test and fails the second**. Both tests are one cheap join over
the same two lists. Only one of them was run, for five releases.

Reproduce with the tool this finding produced, which crosses `reachability.py`'s entry-point
resolution with the voiceover corpus:

```
python tools/vo_reach.py                   # the game as this mod leaves it
python tools/vo_reach.py --as-shipped      # vanilla alone
python tools/vo_reach.py --replies-only --min-kb 100
```

### The headline

| | unreachable nodes carrying a recording | performed audio | trees |
|---|---|---|---|
| **vanilla as shipped** | **204** (97 carry replies) | **19.27 MB** | 33 |
| **as Fixt left it after 0.55.0** | **132** (53 carry replies) | **11.48 MB** | 25 |
| **as Fixt leaves it after 0.56.0** | **117** (53 carry replies) | **11.18 MB** | 25 |
| **as Fixt leaves it after 0.94.0** | **66** (34 carry replies) | **5.14 MB** | 23 |

Earlier releases had already recovered **72 nodes and 7.79 MB** of it, every one as a side effect
of chasing something else. Nobody was aiming at this number, because nobody had taken it. 0.56.0
is the first release aimed at it directly and it brought back **15 lines**, which is where the
117 comes from -- re-measured with the tool, not subtracted on paper.

Recorded voiceover is the top of this document's own signal ranking -- **recorded VO > authored
item/dialogue definition > quest states > a filename** -- because a recording means the line survived
all the way to a studio session. 11.48 MB of it sits behind replies that were never written.

### Rules this sweep adds

- **Measure a join in both directions.** Names-to-nodes and nodes-to-reachable are the same two
  lists and different questions. Asking one and reporting the category closed is how 19 MB of
  performed audio stayed invisible for five releases.
- **A recording is the strongest lead, and still not a verdict.** Classify every one of these against
  the [orphan taxonomy](#the-three-kinds-of-orphaned-node) before building. Two of the loudest
  entries in a raw survey are already-settled superseded drafts.
- **Prefer the sibling.** When a name family has wired members and one dead one, the mechanism is
  already placed and the repair is an entry, not a design.
- **Grep releases.md and qa.md for a lead's own node ids before calling it open.** `--with-mod`
  subtracts what this mod **built**; nothing subtracts what it **considered and cut**, and the two
  are indistinguishable in the data. Adjudicated content is a fourth kind of orphan, and the only
  one that cannot be recognised from the files at all.

---

## Orphaned art -- the axis this survey never looked at

Everything above surveys cut **script** content: items, enemies, wands, skills, perks, factions. Art
was never surveyed, and art orphans are a different shape -- an asset that exists, loads, and is
named by nothing. `tools/orphan_art.py` runs it. The find that prompted it was a player noticing
that the **Gauntlets of La Mancha** is the only unique gauntlet wearing the generic gauntlet icon.

As of 0.94.0: **7 inventory icons, 8 ground pickups and 21 meshes** are named by nothing. It was
13, 10 and 21 at 0.89.0. **0.90.0 built the stranded table below, 0.91.0 the buckler, 0.92.0 the
bracers, and 0.93.x the Holy Shield**, so what remains is the nameless list and the drafts.

### The method correction that has to come first

The first run of this survey read vanilla only, which answers *"was this unused in 2003"*. That is
the wrong question and it produced a wrong plan. The `Clover` icon looks orphaned in vanilla and is
in use now: a Port District bar patron offers it to a low-Luck character -- *"perhaps this will
bring you some good fortune, it's clover, plucked from the last patch of dry ground 'afore me island
sank"* -- and the item that reply hands over **did not exist in vanilla at all**. Fixt authored it.
The same correction removed `Gem Onyx` and the Inquisitor's rod pickup from the list.

This is the `zf.read()` versus `lhbuild.read()` distinction, in a new place. The tool now scans both
and the numbers above are post-correction.

### Art with no thread

**Nameless** -- art naming something with no other trace. The write-up is the deliverable.

| art | trace | read |
|---|---|---|
| `Quest Items/Esteban Knife` + `Special Items/EstebanDagger_PU` | **Guard Esteban exists**, with his own dialogue tree and five maps | A matched icon-and-pickup pair for a named, living character. No knife is mentioned in his tree, so the hook is gone and only the art remains |
| `Special Items/HammerBjon_PU` | **none** -- see below | A character cut so completely that only his weapon's ground sprite survived |
| `Misc Items/ScrollTregethia` | `Shylocke Key` uses `Key Tregethia`, a *different* asset | A Tregethia **scroll** was planned beside the key that shipped |
| `Quest Items/Rare Herb`, `Quest Items/Potion Wolf`, `Misc Items/Key Skeleton`, `Misc Items/Gem Ruby`, `Armor/Bracers Defense`, `Armor/Shield Holy`, `Weapons/Sword Undead Bane` | none | Art without a thread. `Sword Undead Bane` is the odd one: the Sword of Undead Ice ships and uses a *different* icon under `Images for RED file`, so this is a superseded draft rather than a gap |

### What to skip

The 21 orphaned meshes are almost all duplicate or draft creature parts -- `Terror 02` and `Terror 03`
under three different folders, `Dwarf_Body` under two generic NPCs, two `SoulReaver` variants. That is
the pattern [0.45.0 already settled](unused-content-resolved.md#done-in-0450---the-horse-and-what-the-unused-enemies-number-actually-means):
a draft beside its finished version is not cut content. `Models3D/Gizmo/Gizmo` is the only curiosity,
and a mesh called Gizmo with no script trace is not a lead.

The remaining pickups are generic duplicates: `Bow_Pickup` beside the used `Bow_PU`, `Sword1`,
`PU Chainmail` beside `ChainMail_PU`, `SacredScimitar_PU` beside the used `ScimitarSacred_PU`, and two
spirit-energy ground lights. Superseded naming, not content.

---

## The three kinds of orphaned node

Three releases of chasing these has produced a taxonomy worth keeping, because the right action
differs completely:

| kind | evidence | action |
|---|---|---|
| **filename drift** | node reachable, recording present under a near-miss name | rename the node (0.41.0, 6 lines) |
| **unreachable branch** | node unreachable, flag or link missing, no live replacement | wire it (0.41.0 and 0.42.0, 5 nodes) |
| **superseded draft** | a *live* node fills the same role with equal or better content | **leave it dead** |

Two superseded drafts have now been found and correctly left alone: `Help Andre the Titan with his
tasks` (replaced by `Recover Lucius' Mneme`) and the Blacksmith's node 80 (replaced by
`07 what more`). In both cases the giveaway was the same -- finding the live node that does the job,
and checking whether it is *better*. Reference-counting alone cannot tell these three apart, and the
first instinct in every case was wrong.

---

## How this was measured

The method matters more than usual here, because **four** answers were wrong on the first attempt in
ways that all looked plausible. Each failure is a reusable lesson, so they are recorded rather than
quietly fixed.

### 1. A quadratic scan that never finished

The first item survey searched the whole archive once per item and was killed after two minutes.
Rewritten to index every referenced value in a **single pass** over the archive, then test membership.

### 2. Excluding `.txt`

The second attempt skipped `.txt` files -- which is exactly where `Inventory Addition Groups`,
`Grouping Catagories` and `Addition Shopping Strategies` live. Had the item pools been listed there,
every result would have been a false positive.

### 3. Matching one field name

The third attempt counted enchantments reached through `Addition=` and reported 65 orphaned magic
items with **four whole equipment categories unplaced**. That was wrong:
`CInventoryItemGeneratorMiscellaneousMagic` spells the same relationship **`Additional Magic=`**, and
once both are counted, 62 of those 65 are redundant duplicates.

Same shape as `Requirement=` versus `Custom Requirement=`, and as `Name=` inside `Relay Name=`.

### 4. A case-sensitive extension - the worst one

A check for dangling `Race=` references reported **93 monster cans with an unresolvable race**, broken
down by folder, framed as a live vanilla defect affecting spawned content. **That was entirely a bug
in the check.** Race files ship under **two extension spellings -- 427 `.Race` and 76 `.race`** -- and
the check required the capitalised form. Every one of the 93 resolves once case is folded.

The true figure is **zero** unresolvable races and **zero** unresolvable models across all 478 cans.

This one is the most instructive because the project already carries a note titled *"name audits must
fold case"*, recorded after a case-sensitive sweep invented four Toulouse defects. The lesson was
known and the extension was still matched case-sensitively.

It did surface one genuine thing: `Races/Enemies/Thugs/` contains **both** `Thug3 Mace.race` and
`Thief3 Mace.Race` -- two parallel spellings of the same ladder. Worth knowing before editing anything
in that folder, since a careless edit could hit the wrong file.

### 5. Two reachability routes, not one

Perks nearly produced a false result in the opposite direction. A first instinct is to ask what
*grants* each perk -- but 85 of the 98 are **selected by the player at level-up** and are granted by
nothing, by design. Reporting those as unused would have been the mirror image of the skills mistake,
where enemy usage was measured and Barter came back "unused".

The test that works is the **impossible requirement**: `CIsGreaterThanOrEqual` of the constants 0 and
1 marks a perk as unselectable, and only those need a grant. Two routes, and a perk is reachable by
either.

### 6. Checking one link and calling the chain connected

The magic-items section originally reported that 62 of 65 orphaned recipes were redundant because
`Generator Combinations` reached their enchantments. It does -- but **nothing reached
`Generator Combinations`**. The check stopped one link short.

It was caught only because wiring three wands into `Wand selection MAGIC` would have been three
correct edits to a pool nothing draws from, and tracing the chain before building showed
`All Wands` had no referrers at all.

**The rule: trace a reference chain to something that actually runs** -- a map, a drop table, a
merchant -- not to the next file that mentions it.

### 6. Querying for a shape instead of examining a case

The worst of the six, because the evidence was already in hand. Asked whether a two-item set bonus was
possible, the search was for class names that *sounded* like equipment checks -- `CHasItemEquipped`,
`CIsWearing`, "Set Bonus" -- and when none existed the answer given was "the engine has no hook."

The Voodoo belt and necklace had appeared in this document's own orphan list an hour earlier. Opening
either one would have shown the mechanism immediately, because the mechanism is a **counter**, not a
check, and no query shaped like a check could find it.

**The rule: when asked whether a mechanism exists, find a case that works and read it.** Do not
enumerate guesses at its name. `one query is not proof of absence` applies to class names as much as
to content.

### What makes the final numbers trustworthy

**The control groups.** A survey that comes back "everything is unused" is measuring itself:

- **All 13 potions are placed.** When the designers wanted a consumable in the world, they placed it
  -- so a category coming back empty means something.
- **86 of 92 skills are player-reachable.** The skill system is complete, which is what a correct
  method should say about a system that visibly works in play.
- **Zero unresolvable models or races.** If the resolution logic were wrong, this number would be
  large -- as it was, wrongly, at 93.

### Rules for the next pass

- Fold case on **both sides**, including file extensions.
- Match a reference by **full path and bare basename**, since the game uses both.
- Never trust a single field name; check whether a sibling spelling exists.
- Include `.txt`, which holds the pools and groups.
- Cross-check against **Fixt's own `files/`**, or already-restored content reads as still open.
- State a control group. A result with no category coming back "fully used" is not yet believable.
- Ask how many ways content can be reached **before** testing one of them. Perks have two;
  skills have two; items have three.
- To ask whether a mechanism exists, **open a case that works**. Searching for a plausible
  class name finds nothing when the mechanism is shaped differently than expected.
- Trace a chain to something that **runs**, not to the next file that mentions it.
- An empty quest file is not evidence of a cut. 33 of 151 have `Item Count=0`, and several of those are
  content in the shipped game under another quest's journal text.
