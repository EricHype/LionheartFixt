# Design review — the combat AI, and three decisions that need a playtest

**Written 2026-09-28. All three decisions were taken the same day; the reasoning below is kept as the
record of how.** What changed as a result is summarised immediately under this line and marked through
the document.

## Decisions taken, 2026-09-28

1. **The Priestesses keep casting** -- but they now *cycle* rather than re-roll. `CRandomAction` picked
   fresh every attack and could hand out the same spell four times running, which reads as no variety at
   all. `CShuffledSeriesAction{When Done=Repeat Series}` deals the whole hand before reshuffling, so a
   Priestess Super visibly works through Fire Orb, Lightning Bolt, Spike and Static Charge. Built.
2. **The Old Man of the Mountain is left exactly as he is** -- because he turns into the dragon.
   `Chaos Dragon Generator` carries `Dragon_Chaos` at 25,000 XP, and its after-action fires
   `Player KILL Old Man in Combat` and arms `Dragon Health Checker`, so killing the dragon *is* killing
   the Old Man as far as the ending matrix is concerned. His 40 hit points are not an oversight, they are
   a stage direction. **No files changed.**
3. **The Bonecaller raises the dead**, using the game's own undead-summoner idiom -- `Ghoul Male Large`
   Tough and Super clone from a map part called `ghoul clone generator` behind a `ghoul summoning enabled`
   checker, and the Doomed Plateau already carries **both**, so this needed no map edit. One attack in
   four is a summon; the three tiers raise four, five and six ghouls. Built.

The tiers waiting behind these are unchanged and still wait on a playthrough.

Context: `releases.md` holds the 0.25.0 scope and what tier 1 actually built. This is the part that
is *not* settled.

---

## The state of it

Enemy behaviour in Lionheart is one field. `CNormalAttackAI.Minimum Attack Distance`, across all **478**
monster cans:

| value | cans | what it is |
|---|---|---|
| 100 | 391 | walk up and swing |
| 350 | 53 | stand off and shoot |
| `Do not move while attacking` | 22 | rooted caster |
| 250 | 1 | one oddity |

And `Shoot Completed` — the slot that decides what a creature *does* when it attacks — is empty or
skill-less in **400 of the 478**.

That slot is not a flag. It takes the same action vocabulary as every dialogue reply in the game, and a
minority of cans already prove what it can hold: 67 randomise their attack, 49 pick from two to four
skills, 30 switch weapon mode, 17 carry a secondary to switch to, 13 summon, 8 debuff, 24 wind up with a
delay before the hit.

What does **not** exist, and cannot be added from data: `CFleeAI` and `CRetreatAI` are referenced by
nothing. There is no morale, no retreat, no breaking. Target selection is not scriptable against the
player either. Focus-fire, flanking, kiting and formations are out of reach, and no decision below should
be taken on the assumption that they are coming.

---

## Decision 1 — do the Priestesses keep casting? **(yes, and they cycle)**

**Answered: yes, and they cycle.** Built, deployed, unplayed. It needed a verdict first because it was
already in the game and everything else waited behind it.

`Priest` and `Priestess` are the same creature with one field missing. A line-by-line diff of the two cans
differs in exactly one place: the Priest's `Shoot Completed` opens with a shield and then picks at random
from Fire Orb, Spike and Lightning Bolt; the Priestess's is **empty**. Same role, same attack distance,
same everything else. She closed to melee and swung.

Her race already knew the spells. Each tier now selects exactly what its own race presets, and nothing
more:

| can | race presets | now casts |
|---|---|---|
| Priestess | Spike 75 | Spike |
| Priestess Tough | Fire Orb 85, Spike 90 | both, alternating |
| Priestess Super | Fire Orb 95, Lightning Bolt 95, Spike 95, Static Charge 95 | all four, cycled |

**Why it might be too much.** The line is dense exactly where act 7 is thin: **fourteen** Priestesses in
the Inner Sanctum, **twelve** in the Secret Chamber, **eleven plus six Supers** in the Exalted Chambers --
the Druid Master's own room, and the fight 0.22.0 just rebuilt. Twenty-nine casters across three rooms
that previously closed to melee is not a small change to an act nobody has played since.

**What would decide it:** `PC6` and `PC7` in `qa.md`. Walk the Exalted Chambers approach and the Inner
Sanctum and judge whether the room is harder in an interesting way or simply harder.

**If the answer is "too much", the fix is small and graded**, in this order:

1. Drop `Priestess Super` from four spells to two (Fire Orb, Spike) — keeps the tier distinct, halves
   the volume of incoming magic in the worst room.
2. Leave `Priestess Super` alone but revert the base `Priestess` to melee, so only the elite tiers cast.
3. Revert all three. The change is three files and no map edits, so a full revert costs nothing but the
   commit.

**The argument for keeping it even if it stings:** the defect is real either way. A creature whose race
presets four offensive spells at 95 and who has never once cast them is not balance, it is an oversight,
and the Priests standing beside her have done it correctly since 2003.

---

## Decision 2 — does the Old Man of the Mountain get a fight? **(no: he is the dragon)**

**Answered: no. He is the dragon, and nothing was changed.**

The final antagonist of the game has **40 hit points**. His race is `Old Man Fleeing`, one skill
(OneHandedMelee 50), his `Shoot Completed` is empty, and there is no second Old Man asset anywhere in the
data — one can, one race. Whatever the finale feels like, it is not coming from him.

It is coming from `08 Final Encounter`, which is the most heavily scripted map in the game: two caged
prisoners with their own scripted attackers, a spike matrix, a siege tank, a summoned-monster loop, a
teleport trap behind the player, and a grid of ending relays keyed to who is still alive and what the
player's karma is.

**So this is not "fill an empty slot". It is a choice about the ending**, and there are three honest
positions:

- **Leave him.** The scripted arena *is* the boss fight; that is a legitimate design, and 40 HP is
  arguably deliberate — the Old Man is a manipulator who has spent the game having other people fight for
  him, and he dies like the frail old man he is. Restoring a spell rotation would argue with the story.
- **Give him the rotation only.** Data-only, no map edits, no HP change. He would still die fast, but he
  would do something on the way down. Lowest risk of the three.
- **Give him a real fight.** Rotation plus hit points. This means touching the ending matrix's
  assumptions about how long the fight runs, and the summon loop is timed. **High risk, and the one
  irreversible thing in this whole document** — a broken ending is not something a save recovers from.

**What decided it:** `Chaos Dragon Generator` spawns `Dragon_Chaos` at 25,000 XP and its after-action
fires `Player KILL Old Man in Combat` and arms `Dragon Health Checker` -- so killing the dragon is
killing the Old Man as far as the ending matrix is concerned. The first of the three positions above is
the right one, and his 40 hit points are a stage direction rather than an oversight.

---

## Decision 3 — does the Bonecaller cast? **(yes: he summons)**

**Answered: yes, he summons.** Ours to decide, which is why it needed asking.

0.21.0 created the Boss Lich line for the Doomed Plateau — 1,500 / 2,000 / 2,500 XP, HP 385 to 520, and
melee-only. That is **not** a regression from the clone: its source, `Magical Greater Skeleton`, sits on
the `Lance Guardian` race, which is also melee-only and also selects no skills, despite the word
"Magical" in its name.

So there is nothing to repair here. The question is whether to *author* new skill presets onto a Fixt
race, which crosses a line this project has mostly stayed behind: connecting what exists versus inventing
what does not.

**For:** a creature the mod named "Bonecaller", which can be talked into standing down and which commands
an undead army on the Plateau, swinging a sword and nothing else is a missed characterisation. Undead
casters exist in the game to copy from.

**Against:** it is a pure difficulty increase with no defect behind it, on an encounter that is itself
only a few weeks old and unplayed. Every other combat change in this document can point at something the
original authors did and did not finish. This one cannot.

**What was built:** not spells -- the game's own undead-summoner idiom. `Ghoul Male Large` Tough and
Super clone from a map part called `ghoul clone generator` behind a `ghoul summoning enabled` checker,
and the Doomed Plateau already carries **both**, so no map edit was needed. One attack in four is a
summon, and the three tiers raise four, five and six ghouls. The guard means a Bonecaller placed on a map
without the clone source simply fights normally.

---

## What is waiting behind these

The remaining 0.25.0 tiers are scoped in `releases.md`. Decision 1 is answered, but these still wait on
a playthrough rather than on a decision:

- **Telegraphs.** `CDelayAction` appears in 24 attack AIs out of 478. A wind-up before a heavy hit is the
  cheapest legibility win available and pairs with whatever decision 1 produces.
- **Phases.** `CAIHealthPercentThresholdTrigger` is used **twice in the entire game**, both in one map,
  both only to fire a relay — while AI swapping is routine at 493 removes and 952 adds. Held back
  deliberately: a boss that changes behaviour at 40% is not something a save can undo.
- **Archers, as a trial only.** 53 ranged cans, 17 cans carrying a secondary weapon, **overlap zero**. Bow
  enemies have nothing to draw, so this needs giving them a weapon before a swap means anything. Scope to
  `Assasin Bow` and its Tough and Super, play it, then decide about the other fifty.

---

## The standing caution

This is the first work in the project aimed at difficulty rather than content, and **0.21.0 through
0.24.0 have never been in front of a player.** That is four releases of new routes, new companions, new
prices and new refusals, none of it verified, and now a combat change layered on top.

The honest recommendation is that the next session is a playthrough, not a build.
