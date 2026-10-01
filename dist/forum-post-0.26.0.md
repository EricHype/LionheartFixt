# Lionheart Fixt 0.26.0 - What They Were Built To Do, part two

The five-item combat plan, built. **Four shipped, one did not survive contact with the data**, and the
sweep that was meant to be a repair pass turned out to have nothing to repair.

Each part is separately revertible and has its own QA rows, because the plan's own stopping rule --
ship one at a time and play it -- is being set aside, and attribution has to come from somewhere.

## 1. Sniper on the thief archers

`Is Sniper Mode Enabled` forces a critical on a ranged attack. It is read in `FUN_0049b030`, the
critical-hit resolver, through the **same generic accessor on the same attacker object** as the
backstab gate -- no player test, and its callers sit adjacent to the backstab gate's in the same damage
pipeline. Backstab is the proven sibling, confirmed in play on 29 September.

Scoped exactly as planned: **Super tier only**, two races and four cans. `Thief3 Bow Super` and
`Thief4 Bow Super` -- two of the six races left unreferenced by 0.25.0 -- now carry the attribute, and
the four Super bow-thief cans point at them. Thugs are untouched, as before.

## 2. The weapon-skill mismatch sweep: nothing to repair

The plan said to widen the name-based sweep to read equipment first, and warned the count might grow.
It shrank to zero, and the name-based findings turned out to be **false positives**:

| can | name-based verdict | what it actually equips |
|---|---|---|
| `Hired Goon Sword` and tiers | "carries a sword, race knows only Unarmed" | `Inventory Items/!None` -- **nothing**. The sword is a death *drop*, so `Unarmed 10` is correct |
| `Thug3 Mace Elite` | same | same |
| `Vodyanoi`, `Vodyanoi Green` | not flagged by name | `Spit Voydyanoi`, a real ranged weapon, with `Ranged 0` |

Weapons declare their skill through `Hit Or Miss=Damage Types/Damage Hit Or Miss/<skill>` -- 88 items
do, split Ranged 47, OneHandedMelee 18, TwoHandedMelee 9, AlwaysHit 14. Reading that instead of the can
name is what cleared the goons.

The Vodyanoi were **read and deliberately left alone**. `Ranged 0` looks like a defect until the tiers
line up: 0, then 5, then 10. It is a ramp that starts at zero, and only 11 of 623 skill presets in the
whole game are zero-valued -- rare, but not unique. A creature whose weakest tier is hopeless with its
own attack is a coherent design, and it stands on 32 and 16 maps.

So this item ships no file change. That is the right outcome for a repair pass that finds nothing, and
the measurement is worth more than the four cans it would otherwise have "fixed".

## 3. A telegraphed heavy strike for the Assassin Masters

All three `Assasin Master` cans had an **empty `Shoot Completed`** -- the Priestess situation again --
and `Assasin Master Super` is the heaviest thing in act 1 at 650 hit points, standing in the Slave Pits.

One attack in four now spawns a visible warning, waits a second, then lands an extra 6-12, 9-16 or
12-22 slashing by tier. The shape is `Swordsman Dual Super`'s -- something visible, `CDelayAction`,
then the payload -- with the `Vilify` effect on its shipped path and `CActionDoDamage` copied from
`Andre the Titan 2`. No animation was invented: a `CPlayAnimationAction` was considered and dropped
because it needs an animation the assassin model is known to have, and that was not verified.

**What a telegraph can honestly be.** `Shoot Completed` fires when a shot *finishes*, so a delay there
cannot slow the blow that is already landing. What it can do is occasionally wind up and land an extra
one. That is a telegraphed special attack, not a slowed normal swing.

## 4. Archer secondaries: NOT BUILT, and the measurement says why

The plan was a melee secondary for `Assasin Bow` and its tiers, with a switch when the player closes.
Two measured facts kill it:

- **No distance-check action exists.** Sweeping every `.can` and `.zax` for a class matching distance,
  range, near, close or proximity returns `CFreeRangePoly` (geometry), guard AIs and door checks.
  Nothing an attack AI can ask "is the player on top of me". Any switch would therefore be random, and
  a random switch means archers that stop shooting at range -- strictly worse than today.
- **There is no blade to give them.** The melee assassins -- `Assasin`, `Assasin Super`,
  `Assasin Master Super` -- equip **nothing at all**. There is no assassin melee weapon item in the
  game to hand the archers as a secondary.

A partial exists and was not taken: give the three `Assassin Bow` races an `Unarmed` preset so they are
not swinging with a skill they lack when cornered. One line per race -- but whether a bow-equipped
character melees at all is unverified, and shipping an unverified guess inside a release that already
carries three behaviour changes is how attribution gets lost. Offered, not shipped.

## 5. The Bonecaller raises a wave when wounded

`CAIHealthPercentThresholdTrigger` is used **twice in the entire game**, both in
`Ogre Conjurer Cave.zax`, both `When Health Percent Crosses Below` firing a relay. The shape is copied
exactly and only the action differs: it fires `CUseCannedActionAction` on a new canned object rather
than a relay, which is the 0.25.2 indirection and means **no map edit**.

Crossing below 40% raises 3, 4 or 5 ghouls by tier, using the same clone-and-checker beat as the 0.25.0
per-attack summon and guarded by `ghoul summoning enabled`, so a Bonecaller standing anywhere without a
clone source simply does not. It is a moment, not a behaviour swap: swapping its whole attack AI
mid-fight would need `CRemoveAIAction`/`CAddAIAction` inside a can, far more than the item ranked last
justifies.

## The honest caution

Three behaviour changes and a crit-forcing attribute land together, against a plan that said not to do
that. The QA rows are split per item so a playthrough can still attribute, and each part reverts on its
own -- two preset lines for item 1, three `Shoot Completed` blocks for item 3, one Activity entry and
three canned objects for item 5.

If the next playthrough can only report that combat got harder, that is the cost being paid.

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt.

Download, unzip, run `Mod Manager.bat`. Items 1 and 5 reach creatures **spawned after the install**, so
they want a save that has not entered the sewers, the bonus level or the Doomed Plateau. Item 3 is in
the Slave Pits.

https://github.com/EricHype/LionheartFixt/releases/tag/v0.26.0
