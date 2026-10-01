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

## The reactive layer: what else is available, measured 2026-10-01

Everything above is about what a creature *does on its own*. There is a second layer the review had not
looked at at all -- what a creature does **in response to something** -- and it is large, shipped and
barely touched by this project.

| primitive | uses in shipped data | what it is |
|---|---|---|
| `CEntityBehaviorStateSetClosestTarget` | **1510** | how targets are chosen: the **closest** valid one |
| `CAddAIAction` / `CRemoveAIAction` | 952 / 493 | swap a creature's AI at runtime |
| `CSetTargetTypeAction` | **813** | set what a creature is willing to target |
| `CHandleMessageAI` | **554** | react to a named message |
| `CGoToCombatAction` | **403** | put a creature into combat **by name** |
| `CAssignTemporaryTaskAction` | 196 | give a creature a temporary AI, then return it |
| `CAddTemporaryAIAction` | 117 | the same, additively |
| `CSendMessageAction` | 37 | send an arbitrary named message to a target |

### 1. Calling for help is proven, 403 times over

`CGoToCombatAction` takes an **`Enemy Name`**, and the shipped game routinely passes a *group* name
rather than one creature -- `Enemy Name=Inquisition`. Combined with the confirmed-in-play behaviour that
`Entity Name=` broadcasts to **every** entity sharing that name, a single sentry can put a whole room
into combat.

That is the "calling for reinforcements" the project owner asked for, available now, with no new
mechanism. A thief lookout who pulls the room is a different encounter from four thieves who aggro one
at a time as you walk into their individual radii -- which is what every fight in the game currently
is.

### 2. Enemies can react to what the player does

`CHandleMessageAI` listens for a named message. What the shipped game already listens for:

| message | listeners |
|---|---|
| `GoToCombat` and its casings | **426** |
| **`Spellcast`** | **114** |
| `After Death Spell` | 5 |
| `Released companion` | 3 |
| **`CDamagedMessage`** | **2** |

`Spellcast` is the interesting one: 114 places already react to the player casting, which is how
`Detect Spellcast.can` lets the Inquisition hunt casters. Generalising it gives enemies that **change
behaviour when you cast** -- close the distance, interrupt, call for help. Nothing new is needed.

`CDamagedMessage` has **two** listeners in the entire game. A creature that reacts to being hurt --
rather than to crossing a health threshold, which is what 0.26.0's Bonecaller does -- is wide open.

### 3. Targeting is controllable by category, and selection is by proximity

The earlier claim that "target selection is not scriptable" is too broad, like the flanking one was.
`CSetTargetTypeAction` has 813 uses and its `Valid Targets` field takes real values:

| value | uses |
|---|---|
| `Player,Player Friend` | 606 |
| `Player` | 96 |
| `Enemy` | 68 |
| `Summoned Creature` | 58 |
| `Scripted Custom 1` / `Scripted Custom 2` | 113 / 44 |

So **which categories a creature will attack is fully controllable** -- including making one ignore
companions and come only for the player, or turning a creature against other enemies. `Scripted Custom
1` and `2` are arbitrary factions the data can define.

What is *not* controllable is which specific entity it picks from among valid targets:
`CEntityBehaviorStateSetClosestTarget` appears **1510** times, so the rule is "the closest one".
Focus-fire on a chosen party member stays out of reach. But note what that implies -- **positioning
decides aggro**, which is a second reason the move-relative probe matters.

`CSetTargetAction`, which names an attacker and a victim outright, has 17 uses and **every one is
NPC against NPC with literal names**. That part of the original claim holds.

### 4. Temporary AI is a staple, and nothing uses it on enemies interestingly

`CAssignTemporaryTaskAction` (196) and `CAddTemporaryAIAction` (117) give a creature an AI for a while
and then give it back. What the shipped game assigns: `CPlaySequenceOnceAI` 78, `CGoToAI` 50,
`CSkeletonAI` 34, `CScanAreaAI` 18, `CWaitAI` 13, `CIdleAI` 2. All staging -- cutscenes, walking NPCs
to marks.

Assigning `CWaitAI` or `CIdleAI` to an **enemy** for a second is a stagger. Assigning `CGoToAI` is a
reposition. The primitive is proven 313 times over; it has simply never been pointed at combat.

### Where this ranks against the probes

If `CStrafeAttackAI` turns out to be a stub, this layer is where the interesting work is, and none of
it depends on an unused class: every primitive above is in heavy shipped use. The alarm in particular
needs no probe at all -- it is the same action the game fires 403 times, pointed at a shared name.

## Correction: flanking is not impossible, and the primitive is shipped

This review has twice listed flanking as out of reach, on the grounds that "target selection is not
scriptable against the player". The project owner pointed out the hole: the backstab gate proves the
engine computes where the attacker is relative to the defender, so why can nothing be told to move
there?

**The objection is right, and the claim conflated two different things.** Target *selection* -- choosing
whom to attack -- is indeed not scriptable. Moving *relative to a target* is a separate capability, and
the engine has it, and the shipped game uses it.

```
CAssignMoveRelativeAction
{
Target=$Trigger
Move Relative AI=CAIMoveRelative
{
Angle to move=0
Distance to move=50
Additional distance to move=CConstant { Constant Value=0 }
Speed=800
Time Left To Move=0
}
Push Away From Instigator=1
}
```

That is `Sand Dragon Hasharid.can`, verbatim. `CAssignMoveRelativeAction` appears **10 times in shipped
content** -- the Sand Dragon, `Chaos Dragon Final Scene.can` and `DDan.zax` -- so it is working, tested
code, not a registered-but-unused class like `CStrafeAttackAI`.

It takes an **angle**, a **distance** and a **speed**, and a flag for whether the displacement is
measured away from the instigator. The dragons use it as a knockback: you hit them, they shove you.

### What is still unknown, and what would settle it

Two things stand between this and an enemy that circles behind you, and neither needs more
decompilation:

1. **Is `Angle to move` relative to the instigator, to the mover, or absolute?** If it is relative to
   the instigator -- the player, in a combat use -- then an angle near 180 with a modest distance is
   literally "step round behind him".
2. **Does it pathfind, or slide?** `Speed=800` with a `Time Left To Move` counter reads like a timed
   displacement rather than a navigated move. A knockback does not need to respect walls; a flank does.

Both are answered by one probe: put it on a creature with `Push Away From Instigator=0` and a few
angles, and watch what happens.

### What this changes

The earlier line -- "focus-fire, flanking, kiting and formations are out of reach without touching the
executable" -- is withdrawn. Focus-fire and formations still need target selection and remain out of
reach. **Flanking and kiting are movement**, the engine has a shipped movement primitive that takes an
angle relative to a target, and the only open questions are about its semantics.

Set against the other finding above -- that every creature in the game runs the same `CNormalAttackAI`
and four alternative attack AIs ship unused -- this is now the most promising thread in the whole combat
review, and the cheapest to settle.

## Why every enemy feels the same: there is only one combat AI

Measured 2026-09-30, after the project owner put it plainly -- damage types are not the problem,
**"they all run up and just hit you until they die"** is.

That is literally true, and the counts say so. Every creature in the game runs the identical AI stack:

| AI | cans | maps |
|---|---|---|
| `CScanAreaAI` | **716** | 110 |
| `CChasePursueAI` | **713** | 106 |
| `CChaseInvestigateAI` | **713** | 106 |
| `CScanInvestigateAI` | **713** | 106 |
| `CNormalAttackAI` | **701** | 101 |
| `CPatrolAreaAI` | 366 | 45 |

Out of roughly 716 creature definitions. There is one combat behaviour in Lionheart and everything
uses it; the only variation the shipped data has is `Minimum Attack Distance` and whatever sits in
`Shoot Completed`. No amount of work on damage types changes that, which is why the earlier answer
about family identity missed the question being asked.

### The engine ships alternatives that nothing uses

| AI class | uses in all shipped data |
|---|---|
| **`CStrafeAttackAI`** | **0** |
| **`CChargeAttackAI`** | **0** |
| **`CStandGroundAttackAI`** | **0** |
| **`CStandStillAttackAI`** | **0** |
| `CPursueAI`, `CApproachTargetAI` | 0 |
| `CInvestigateAI`, `CInvestigateAreaAI`, `CTenaciousInvestigateAI` | 0 |
| `CStandGuardPatrolAI`, `CShootOverAI`, `CWalkingUpperBodyAI` | 0 |

**These are not dead strings.** Both `CStrafeAttackAI` and `CChargeAttackAI` have a class registration
of exactly the shape every working AI has -- allocate a 0x70-byte instance, build a type descriptor,
register it in the factory by name:

```
if ((DAT_0072e5a8 == 0) && (iVar1 = FUN_005fdc00(0x70), iVar1 != 0)) {
  uVar2 = FUN_00449dd0(0x10, 1, FUN_00628c10, FUN_00628c10, FUN_004665d0);
  FUN_00415b60(&DAT_0072e5a8, s_CChargeAttackAI_006f4adc, 0x3f800000, uVar2, ...);
}
```

That is materially stronger evidence than the F6 editor had. There the menu strings survived and **no
code anywhere consumed the keypress**; here the class is registered in the factory with a real instance
size, so the resource loader will accept `Activity=CStrafeAttackAI` instead of rejecting it.

**What this does not prove** is that the behaviour code is complete. Registration means it loads, not
that it strafes. The honest next step is not more decompilation -- it is the probe this project already
knows to reach for: swap one creature's `CNormalAttackAI` for `CStrafeAttackAI`, play it once, and look.
If it circles, four new archetypes become available at the cost of a field. If it loads and stands
still, it is a stub and the question is closed in ten minutes rather than a week.

### Falling back is genuinely not available

`CFleeAI` and `CRetreatAI` have been named in this review before as "referenced by nothing". That
understates it: **no string matching `CFlee*`, `CRetreat*`, `CCower*`, `CPanic*` or `CMorale*` exists in
the executable at all.** There is no retreat class to reference. Enemies cannot be made to fall back,
and nothing in the data will change that.

### What is available for the rest of the list

| asked for | available? |
|---|---|
| better movement | **yes, probably** -- strafe and charge are registered, unused, untested |
| falling back | **no** -- no such class exists in the binary |
| flanking | **no** -- requires target selection, which is not scriptable |
| calling for reinforcements | **yes, proven** -- the clone-and-checker idiom, already used by the Bonecaller and two shipped ghouls |
| hurling insults | **yes** -- `CPrintCombatTextAction`, used 222 times in maps but in only **3 of 478 cans**, all three the same Mana Reaver line |
| grunts and noises | **yes** -- `CAmbientSoundAI`, used in 8 cans and 13 maps |

So of the six, three are open, one is probable and worth a ten-minute probe, and two are impossible.

## Correction: attack behaviour lives in three places, not one

Recorded 2026-09-30 after a wrong claim, because the wrong claim is the useful part.

Asked whether enemy families could be made to feel more different, this review's first answer was that
they are mechanically identical -- same two skills, nothing in the attack slot, so a thief and a snake
and an English soldier are the same creature in different art. It named the Snakebreed as an example of
a family whose name promises venom the data never delivers.

**That was wrong, and the project owner said so.** The Snakebreed do poison on attack.

The error was looking only at `Shoot Completed`. Attack behaviour lives in **three** places and only one
of them had been checked:

| where | what it is |
|---|---|
| `Shoot Completed` | the attack AI -- what the creature *decides* to do. Empty in 400 of 478 |
| an **equipped weapon** | `Inventory Items/...`, whose `Hit Or Miss` names the skill and whose damages name the types. `Snakebreed Venom` spits `Piercing + Poison` |
| a **natural weapon** on the can | `CPlugInBehaviorDamage` directly on the creature, no inventory needed. `Snakebreed Boss Super` bites `Slashing 3-14` **plus** `CXRPGDamageOverTime` Poison, with canned expressions for damage and duration |

**333 of 478 cans carry a natural weapon**, and the families are differentiated by it far more than the
attack slot suggested:

| family | natural weapons | damage-over-time | what its bite actually deals |
|---|---|---|---|
| Undead | 69 of 92 | **41** | Slashing, **Disease x36**, Fire, Cold, Acid |
| Animals | 37 of 50 | 15 | Slashing, **Poison x9**, Disease |
| Sewers | 30 of 42 | 15 | Slashing, **Disease x15** |
| English Enemies | 28 of 50 | 0 | Slashing, **Cold / Electrical / Fire x6 each** |
| Cursed Elves | 15 of 23 | 0 | Slashing + **Fire x15** |
| Toulouse | 17 of 20 | 0 | **Crushing x17**, Electrical |
| **Thugs (the thieves)** | 35 of 49 | **0** | **Slashing x19, Crushing x16 -- and nothing else** |

So the Undead rot you, the animals poison you, the cursed elves burn you, the Toulouse ogres crush you.
That identity was there all along.

**What survives of the original finding, now properly scoped.** The thieves are the one family blank on
**all three** axes: no attack behaviour, no damage resistances whatsoever, and a natural weapon that
deals plain Slashing or Crushing with no element and no damage over time. Every other family has a
signature. They have none -- which is why the backstab landed on them so well, and where any further
work on making families feel distinct should start.

**The method lesson, which is the third time this one has cost something.** `Hired Goon Sword` was
called defective for carrying a sword with no sword skill, until reading its equipment showed it equips
nothing and merely drops one. The Snakebreed were called toothless until reading their natural weapon
showed the venom. Both times the measurement looked in one place and the answer lived in another. Before
reporting that a creature "does nothing", check the attack slot, the equipped weapon **and**
`CPlugInBehaviorDamage`.

## The combat AI build plan, 2026-09-30

Five items, measured and ordered. Each says what it touches, what precedent it copies, how it reverts,
and what would make it wrong. The ordering constraint matters more than any single item: **do not put
more in front of a playthrough than it can attribute.** The only reason the backstab can be called
working is that it was the single combat change in play when the tester fought those thieves.

The route all of this rests on was proved by that result -- **a race preset can reach engine mechanics
that were player-only by data rather than by code** -- and the question that found it generalises: *is
this gate keyed to the player, or does it just happen that only the player has the attribute?*

---

### 1. Sniper on the thief archers -- the trial

**What.** `Is Sniper Mode Enabled` forces a critical result on a ranged attack. It is read in
`FUN_0049b030`, the critical-hit resolver, through the **same generic accessor on the same attacker
object** as the backstab gate, with no player test, and its two callers sit adjacent to two of the
backstab gate's in the same damage pipeline. Only three perks in the game set an `Is X Mode Enabled`
attribute -- Backstab, Slayer, Sniper -- and one of the three is now proven on enemies.

**Why the thief archers.** 77 cans across 30 families have a race presetting `Ranged` and no melee, and
most are the wrong vehicle for a trial: `Soldier2 Bow` and `Soldier4 Bow` are on 34 real maps each,
`Vodyanoi` on 32. The thief bows are on five, all of them act 1 or the bonus level, which is content the
tester is in right now and where 100 bow thieves stand in one room.

Better still, the scoping problem solves itself the way it did for the backstab. The bow thief cans
point at the shared `Thug3/4 Bow` races, which thugs also wear -- but **the six `Thief*Bow` races left
unreferenced by 0.25.0 are still sitting there**, name-matched and evasive:

| orphan race | AC | Ranged |
|---|---|---|
| `Thief3 Bow` / Tough / Super | 120 / 135 / 155 | 10 / 18 / 29 |
| `Thief4 Bow` / Tough / Super | 130 / 144 / 163 | 9 / 19 / 30 |

**Build.** Repoint the bow thief cans onto those six races and preset `Is Sniper Mode Enabled=1`.
Finishes the job 0.25.0 deliberately left half-done and uses the identical pattern.

**Scope it to Super first.** Forced criticals are the strongest thing on this list. Two cans before
twelve.

**Risk.** Unknown how often a critical lands in practice, and `Ranged 9` on a base-tier thief may mean
they rarely hit at all, critical or not. Also unverified whether the resolver's ranged branch
(`local_2a`) is set for a bow or for something narrower.

**Revert.** Delete one preset line per race, or point `Race=` back at `Thug*`.

**QA.** The combat log names criticals, so `savecheck events --combat` answers it the way it answered
the backstab.

---

### 2. The weapon-skill mismatch sweep -- a repair, not a buff

**What.** Enemies carrying a weapon their race has no skill for. Measured by matching weapon words in
can names against the race's preset skills: **5 cans, 4 of them real**.

| can | race presets | carries |
|---|---|---|
| `Hired Goon Sword`, Tough, Super | `Unarmed 10` only | a sword, and **drops one on death** |
| `Thug3 Mace Elite` | `Unarmed` only | a mace |
| `Simon Bow Fire Test` | `Celestial Smite` | a bow -- test map, ignore |

This is the Priestess defect inverted: there the race knew spells the can never used, here the can
carries a weapon the race cannot use.

**Also fold in zero-valued presets.** `Vodyanoi` and `Vodyanoi Green` base tiers preset `Ranged 0`,
which is a skill in name only, and they are on 32 and 16 maps. Whether that is deliberate (a creature
meant to be feeble at range) or the same oversight needs reading before touching.

**Method limit, stated up front.** The sweep matched weapon *names*, not inventory contents. A can
carrying a sword without "Sword" in its name is invisible to it. Widening it to read the actual
inventory block is the first task of this item, not an afterthought -- the count may well grow.

**Risk.** Low, and it is a repair: giving `Hired Goon Sword` a melee skill makes him fight the way his
own equipment says he should.

---

### 3. Telegraphs

**What.** A wind-up before a heavy blow, so a hit can be seen coming. `CDelayAction` already appears
inside the attack AI of **26 of 478** cans -- `Swordsman Dual`, `Swordsman ShieldHelmet`,
`DjinnArenaMonster4` and others -- so the shape is shipped and can be copied rather than designed.

**Build.** Pick one heavy-hitting family, wrap its `Shoot Completed` in the shipped delay shape, and
play it. Bosses and Supers only; a telegraph on a trash mob is noise.

**Risk.** Lowest of the five, and the only one that makes the game *easier* in exchange for making it
legible. That is the point, but it means the balance question cuts the other way.

**Revert.** Restore the can's `Shoot Completed`.

---

### 4. A secondary weapon for archers

**What.** 30 cans switch weapon mode with `CActionSetWeaponMode`; 75 cans have a race that knows
`Ranged`. The **overlap is zero**. Every weapon-mode switcher is a melee creature -- `Swordsman Dual`,
the WarGolems. No archer in the game has anything to do when you close the distance.

**Build.** Give one archer family a melee secondary and the switch, copying `Swordsman Dual`'s shape.
This is the structural fix for ranged enemies and it pairs naturally with item 1: Sniper rewards them
for shooting, the secondary stops them being free kills once you are on top of them.

**Risk.** Higher than it looks. It needs the race to have a melee skill as well, so it is item 2's
machinery applied deliberately rather than as a repair, and it changes the basic shape of every fight
with archers in it.

---

### 5. Phases -- last, or never

**What.** A boss that changes behaviour at a health threshold. `CAIHealthPercentThresholdTrigger` is
used **twice in the entire game, both in `Ogre Conjurer Cave.zax`**, and both only to fire a relay --
while AI swapping is routine at **482 removes and 921 adds** across all maps. So the parts exist and
the pattern does not.

**Why last.** A boss that changes at 40% is not something a save can undo, and this project has just
spent seven releases learning what unplayed changes cost. It also has the least precedent of anything
here: two uses, one map, neither doing what we would want.

---

### The order, and the stopping rule

1. **Sniper on `Thief*Bow Super` only** -- proven route, two cans, immediately testable where the
   tester already is.
2. **The mismatch sweep**, widened to read inventory first. A repair, and repairs have produced this
   project's best findings.
3. **Telegraphs** on one boss family.
4. **Archer secondaries**, only after 1 and 3 have been played.
5. **Phases**, only if the first four have been played and the appetite is still there.

**Ship one at a time and play it.** Each of the first four is revertible in a few lines; none of that
helps if three land together and the tester can only report that the game got harder.

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

## The question for the decompiler, answered 2026-09-28

Everything above was settled from the data files. One thing cannot be, and it gates whether the Sewers'
thieves can ever behave like thieves.

**The finding.** No enemy in the game has ever attempted a backstab, for three reasons that compound:

- `Is Backstab Mode Enabled` is set non-zero in **exactly one file in the game**, `Perks/Backstab.Perk`.
  Every other appearance, in all 478 cans and every race, is the zeroed attribute table each character
  carries.
- **No race presets a Sneak skill or `Sneak Enabled`** -- none of the 700+ of them. The perk's condition
  is "while in sneak mode from behind", and enemies never enter sneak mode.
- **The thieves have no thief skills at all.** Every Thief and Thug race presets exactly one thing:
  `OneHandedMelee` 9-45 or `Ranged` 9-30. No Sneak, no Steal, no Lockpick. `Thug3 Mace Elite` has
  `Unarmed 45`, which is as exotic as the roster gets, and the act 8 Assassins sit at
  `OneHandedMelee 75-105`. "Thief" is a name and a model, not a behaviour.

**What to ask ReVa**, once Ghidra is up with `lionheart-decompile` open:

1. `get-strings` for the two derived-attribute names, then `find-cross-references` on the reads of
   `Is Backstab Mode Enabled` and `Successful Backstab Attack Extra Damage Percentage Zero To One`.
2. `get-decompilation` of whatever consumes them, to answer two things: **(a)** does the gate test the
   *attacker's* sneak state and relative facing, or something else; and **(b)** is it player-only --
   keyed to the party, to `Player1`, or to a controllable-character check?

**What each answer means.** If the gate is generic, a thief race can preset the two attributes and the
bonus becomes reachable -- though the sneak-mode half would still need solving, since no enemy sneaks. If
it is player-only, the idea is dead as a race preset, and the honest substitute is scripting the effect:
`CActionDoDamage` already appears in 12 cans' attack AI, so an ambush opener that does extra damage is
data-only and verifiable.

### The answer: the gate is not player-only

Read out of `Lionheart.exe` in Ghidra. The backstab gate lives in `FUN_0049a1b0`, the damage-resolution
routine, and it is four conditions on **whoever is attacking**:

1. `[this+0x6d] != 0` -- a flag set earlier in the same function from `FUN_00442050()`, which reads the
   attacker's **`Sneak Enabled`** attribute and returns `0 < round(value)`.
2. The attacker's **`Is Backstab Mode Enabled`** attribute, resolved once into a global and read at
   `0x0049a36f`, with magnitude at least 0.01.
3. `param_1 == 1 || param_1 == 3` -- the attack type. One caller passes 0 and so can never backstab,
   which fits the perk text saying melee only.
4. A facing comparison: the absolute difference between the two angles must be **at least pi/2**
   (`1.5707964` at `0x0049a3ac`), otherwise line 118 clears the flag again.

**The decisive part is how the attributes are read.** Both go through `FUN_00441ea0`, which is a thiscall:

```
MOV EDX, dword ptr [EDI + 0x138]     ; the character's derived-attribute array
MOV ESI, dword ptr [EDX + EBP*0x4]   ; indexed by the attribute handle
```

It indexes the attribute array hanging off **the character object in ECX**. There is no party check, no
`Player1`, no controllable-character test -- not in the accessor, not in the sneak helper, and not in the
damage-pipeline caller at `0x0048cce0`, which is a generic hit-resolution sequence.

**So the perk is player-only by data, not by code.** Nothing in the engine refuses an NPC the bonus. The
reason no thief has ever backstabbed is entirely that no enemy race presets either attribute and nothing
puts an NPC into sneak mode -- both of which are `.Race` fields this project can write, since a race can
preset a derived attribute exactly as Wizard Tremblethorn's presets its hit points.

**What is still unverified, and should be before anything ships:**

- Only one of the four callers of `FUN_0049a1b0` was read. Attack types 1 and 3 come from the other
  three; the one opened passes 0.
- `Sneak Enabled` held permanently at 1 on an NPC has unknown side effects. The sneak system feeds enemy
  detection -- there is a `Target/Sneak Adjustment` property described as *"the number of skill points
  that will be added to the players sneak skill during the check"* -- and an always-sneaking NPC is a
  state the game was never asked to render.
- ~~Whether an NPC's facing satisfies condition 4 in practice~~ -- **answered in play 2026-09-29: yes.** A Thief Swordsman backstabbed for the base tier's 25 percent while the player was surrounded by three, at a rate of 1 in 7 landed melee thief attacks. The gate compares the supplied angle against the *defender's* facing, and an attacker behind the defender qualifies.

### Acted on: the thieves of Barcelona now carry it

Built the same day. The tight scope came from a second finding: all 36 thief cans point at the shared
`Thug*` races, which are also worn by `Thug Boss` in act 8 Alamut, the Slaver Captain, Shylocke's goons
and the Crossroads Bandit -- so the races in use were the wrong lever. But vanilla ships **18
`Thief*.race` files that nothing references**, a 1:1 name match with the 18 thief cans, evasive where the
thug races are sturdy. So 24 melee thief cans were repointed onto 12 of those restored races, and those
races carry `Sneak Enabled=1`, `Is Backstab Mode Enabled=1` and 0.25/0.35/0.5 extra damage by tier.
Archers were left out, since the gate needs a melee attack type -- which leaves 6 orphan races still
unreferenced. Full record in `releases.md`; the playtest rows are `BS1`-`BS10` in `qa.md`, and `BS1` is
the one that matters, because it checks that presetting an engine-owned attribute did not break the
creature.

**There is a clean way to verify it.** The combat-log format strings are generic `[Attacker]` and
`[Defender]` templates, not player-specific:

> *"%s[Attacker] sneaks up on %s[Defender] and hits for %s[Damage] ... (%s[BackstabBonus] percent
> backstab bonus)"*

and the save file logs every hit. So a thief race with both attributes preset can be tested by reading
the combat log for that line with an enemy as the attacker. That is a real experiment, not a guess.

**Bringing ReVa up**, since this cost a while: the MCP server needs the **ReVa Application Plugin**
enabled in the **project window** (File > Configure > the plug icon), not only the ReVa Plugin in the Code
Browser. With only the latter the log says *"RevaMcpService not available"* and nothing binds. With both,
it listens on `http://127.0.0.1:8080/mcp/message`. The Claude Code client only connects at launch, so
Ghidra must be up **before** the session starts.

## The standing caution

This is the first work in the project aimed at difficulty rather than content, and **0.21.0 through
0.24.0 have never been in front of a player.** That is four releases of new routes, new companions, new
prices and new refusals, none of it verified, and now a combat change layered on top.

The honest recommendation is that the next session is a playthrough, not a build.
