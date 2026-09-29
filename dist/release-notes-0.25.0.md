# Lionheart Fixt 0.25.0 - What They Were Built To Do

Every release from 0.21.0 to 0.24.0 changed what the game *says*. This one changes how it *fights*, which
is a different kind of risk, so it was scoped in full and written up as a design review before anything
was built.

The question that started it: enemies come in four or five shapes and mostly run up and swing until
somebody dies. That is measurably true, and it comes down to one field.

## The whole archetype system is one number

`CNormalAttackAI.Minimum Attack Distance`, across all **478** monster cans in the shipped game:

| value | cans | what it is |
|---|---|---|
| 100 | **391** | walk up and swing |
| 350 | 53 | stand off and shoot |
| `Do not move while attacking` | 22 | rooted caster |
| 250 | 1 | one oddity |

And `Shoot Completed` -- the slot deciding what a creature actually *does* when it attacks -- is empty or
skill-less in **400 of the 478**. They swing whatever the race handed them, forever.

That slot is not a behaviour flag. It takes the same action vocabulary as every dialogue reply in the
game, and a minority of cans already prove what it will hold: 67 randomise their attack, 49 pick from two
to four skills, 30 switch weapon mode, 17 carry a secondary to switch to, 13 summon reinforcements, 8
apply a debuff, and 24 wind up with a delay before the blow lands.

So nothing here is new machinery. **Every piece of this release is a creature using an ability it already
had.**

## The Priestess is the Priest with one field missing

A line-by-line diff of `Priest.can` against `Priestess.can` differs in **exactly one place**. The Priest's
`Shoot Completed` opens with a magical shield and then picks at random from Fire Orb, Spike and Lightning
Bolt. The Priestess's is **empty**. Same role, same `Minimum Attack Distance=100`, same everything else.
She closed to melee and hit you with a stick.

Her race already knew the spells, at values as high as the Priests':

| can | its race presets | it cast | it casts now |
|---|---|---|---|
| Priestess | Spike 75 | nothing | Spike |
| Priestess Tough | Fire Orb 85, Spike 90 | nothing | both, alternating |
| Priestess Super | Fire Orb 95, Lightning Bolt 95, Spike 95, Static Charge 95 | nothing | all four, cycled |

Each tier selects **exactly** what its own race presets and nothing more, so no creature is handed a
spell it was not already built to know. The Priests' shield opener is deliberately not copied across: no
Priestess race presets it, and granting one would be inventing rather than connecting.

They **cycle** rather than re-roll. `CRandomAction` picks fresh on every attack, which means it can hand
out the same spell four times running and read as no variety at all;
`CShuffledSeriesAction{When Done=Repeat Series}` -- which 67 shipped files use -- deals the whole hand
before reshuffling, so a Priestess Super visibly works through all four.

They are not obscure. **Fourteen** Priestesses stand in the Inner Sanctum, **twelve** in the Secret
Chamber, and **eleven plus six Supers** in the Exalted Chambers, which is the Druid Master's own room --
the fight 0.22.0 rebuilt. Twenty-nine casters across three rooms that previously closed to melee.

## The Bonecaller raises the dead

0.21.0 fielded the Boss Lich -- three races with a sprite and seventeen animations and no template
anywhere in the game -- as the Bonecaller on the Doomed Plateau. It was melee-only, which was not a
regression: its source, `Magical Greater Skeleton`, sits on the `Lance Guardian` race, also melee-only
despite the word "Magical" in its name.

Rather than author spell presets onto a race this project owns, it summons, using the game's own
undead-summoner idiom: `Ghoul Male Large` Tough and Super raise reinforcements by cloning from a map part
called `ghoul clone generator`, guarded by a `ghoul summoning enabled` checker, with a spellcast
animation, a delay, a summoning effect and a cleanup. **The Doomed Plateau already carried both parts**,
so this needed no map edit at all. One attack in four is a summon; the three tiers raise four, five and
six ghouls. The checker guard means a Bonecaller placed on a map without a clone source simply fights
normally.

## The thieves of Barcelona backstab

The Backstab perk's premise is a thief's job description, and no thief in Barcelona or the sewers has
ever used it. The resource files cannot say why, so the question went to the decompiler.

**The gate is not player-only.** It lives in the damage-resolution routine at `0x0049a1b0` and is four
conditions on whoever is attacking:

1. a sneak flag set from the attacker's **`Sneak Enabled`** attribute
2. the attacker's **`Is Backstab Mode Enabled`** attribute
3. an attack type of 1 or 3 -- melee, which matches the perk text
4. a facing difference of at least **pi/2**, or the flag is cleared again

Both attribute reads go through one generic accessor that indexes the attribute array hanging off
whatever character object is in ECX. There is no party check, no `Player1`, no controllable-character
test -- not in the accessor, not in the sneak helper, not in the damage pipeline. **The perk was
player-only by data, not by code:** no enemy race presets either attribute.

Two data problems stood between that and shipping it.

**Scope.** All 36 thief cans point at the shared `Thug*` races -- and those races are also worn by
`Thug Boss` in **act 8 Alamut**, the Slaver Captain, Shylocke's goons, the Jewel Thug, the Crossroads
Bandit and the Wilderness Traveler. Presetting there would have handed backstab to most of the game's
human enemies across four acts, for a change asked about one.

**What made a tight scope possible.** Vanilla ships **18 `Thief*.race` files that nothing references** --
a name-for-name match with the 18 thief cans, structurally identical to the thug races including the
`!Unknown Model` that leaves the model to the can, and differing only in numbers: consistently higher AC
and hit points, slightly lower weapon skill. `Thief Pale` differs from `Thug Pale` in exactly one line,
AC 120 against 90. Someone built a thief race line -- evasive where a thug is sturdy, which is what a
thief should be -- and never repointed the cans.

So **24 melee thief cans are repointed onto 12 of those restored races**, and those races carry the two
attributes the gate reads plus extra damage graded by tier:

| | `Sneak Enabled` | `Is Backstab Mode Enabled` | extra damage |
|---|---|---|---|
| base | 1 | 1 | 25% |
| Tough | 1 | 1 | 35% |
| Super | 1 | 1 | 50% |

Graded because the player's own perk gives 50% per rank and these enemies stand in act 1. Presetting an
arbitrary derived attribute is ordinary: vanilla races preset 21 different ones, including
`Lance Guardian`'s `Melee Damage Percentage Gives Health To Attacker Zero To One` at 0.4, 0.45 and 0.6 --
the same `Zero To One` shape as the backstab percentage.

**Archers are deliberately left out.** The gate needs a melee attack type, so a preset on a bow would be
inert. Six of the eighteen orphan races therefore stay unreferenced, recorded rather than repointed,
because moving them would be a pure stat buff with no mechanism behind it.

It reaches **seven** real maps. Six are act 1: the Slave Pits (21 spawns), Slave Pit Exterior (7), and
sewer levels 01 (43), 02 (51), 05 (2) and 09 (45).

**Corrected after publication:** the seventh is the **RED FILE preorder bonus level**, which this note
originally dismissed as a debug map. It is not -- it has its own installed-pack check, its own boss line
and artefacts, and an entrance scripted from the Gate District. It fields **90** spawns carrying the new
thief races (Theif Pale x33, Theif4 Sword x23, Theif3 Mace x12, plus Tough variants), which is more
backstabbing thieves than any two sewer levels together, and a further 100 bow thieves that are
deliberately untouched. It is the best place in the game to test this feature.

Thugs keep their 95 AC and no backstab.

The combat log will say so when it fires -- the templates are generic `[Attacker]` and `[Defender]`, so
*"... sneaks up on ... and hits for ... (25 percent backstab bonus)"* can name a thief.

## The Old Man of the Mountain was read and left alone

The final antagonist of the game has **40 hit points**, one skill, and an empty attack slot. That looked
like the largest unfinished thing in the game, and it is not: **he turns into the dragon.**
`Chaos Dragon Generator` spawns `Dragon_Chaos` at 25,000 XP, and its after-action fires
`Player KILL Old Man in Combat` and arms `Dragon Health Checker` -- so killing the dragon *is* killing the
Old Man as far as the ending matrix is concerned. His forty hit points are a stage direction, not an
oversight. **No file was changed for this**, and the riskiest item on the list retired without anything
being built.

## What cannot be done from data, so it is not promised

`CFleeAI` and `CRetreatAI` are referenced by nothing in the shipped game -- there is no morale system and
nothing breaks. Target selection is not scriptable against the player either. Focus-fire, flanking,
kiting and formations are out of reach without touching the executable, and no future release should
imply otherwise.

## The honest caution

This is the first work in the project aimed at difficulty rather than content, and **0.21.0 through
0.24.0 have never been in front of a player.** That is four releases of new routes, companions, prices
and refusals, unverified, with a combat change now layered on top.

Three things in particular need a playthrough rather than a gate:

- **Whether the Exalted Chambers approach is now harder in an interesting way or simply harder.** Twenty-
  nine casters is not a small change to an act nobody has played since it was rebuilt. If it is too much,
  the fallback is graded: drop the Super from four spells to two, or revert the base tier to melee, or
  revert all three -- three files, no map edits.
- **Whether the thieves still look and move normally.** `Sneak Enabled` is described as engine-modified,
  and the reason a preset is expected to hold is that the setter writes the engine's real sneak-state
  field separately from the attribute, and only the attribute is preset. If thieves turn up invisible or
  creeping, that reasoning was wrong and the repoint should be reverted.
- **Whether an enemy's facing ever satisfies the pi/2 condition.** Enemies turn toward their target, so
  the bonus may only fire when you are already engaged and a second thief closes from behind -- which is
  the intended emergent behaviour, but it may equally mean it fires rarely.

The repoint also raised thief AC and hit points alongside adding backstab, so two variables moved at
once. The revert path is one `Race=` line per can.

Playtest rows are `PC1`-`PC7` and `BS1`-`BS10` in [`docs/qa.md`](../docs/qa.md). The full reasoning,
including the three decisions and what settled each, is in
[`docs/design-review-combat.md`](../docs/design-review-combat.md), and the engine trace is recorded in
the `lionheart-modding` reference under "A race can preset ANY derived attribute".

## Still scoped, not built

- **Telegraphs.** `CDelayAction` appears in 24 attack AIs out of 478. A wind-up before a heavy hit is the
  cheapest legibility win available.
- **Phases.** `CAIHealthPercentThresholdTrigger` is used **twice in the entire game**, both in one map,
  both only to fire a relay -- while AI swapping is routine at 493 removes and 952 adds. Held back
  deliberately: a boss that changes behaviour at 40% is not something a save can undo.
- **Archers, as a trial only.** 53 ranged cans, 17 cans carrying a secondary weapon, **overlap zero**.
  Bow enemies have nothing to draw, so this needs giving them a weapon before a swap means anything.

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt.

Download, unzip, run `Mod Manager.bat`. Can and race edits reach only creatures **spawned after the
install**, so this needs a character who has **not yet entered** the Exalted Chambers, the Inner Sanctum,
the Secret Chamber, the Doomed Plateau, the Slave Pits or the sewers. Unplayed; what you find goes into
0.25.1.

https://github.com/EricHype/LionheartFixt/releases/tag/v0.25.0
