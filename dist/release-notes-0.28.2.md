# Lionheart Fixt 0.28.2 - a companion built out of sentry parts

Fernand Desoto stops freezing in place after a kill.

Reported from play, once 0.28.1 finally made him keepable: *"Ferdnand's AI often has him freezing in
place after he defeats an enemy. He only seems to react when another enemy attacks him."*

## He is the only companion built this way

Every other companion inherits its skeleton AI from a creature can. Fernand's is **hand-assembled in a
map relay**, and vanilla gave that relay target-acquisition values no other companion has.

| field | Fernand | Cervantes | across the shipped archive |
|---|---|---|---|
| **Vision Cone** | **90** | 360 | `360` in **1317** uses, `90` in 145 |
| **Max Distance** | **300** | 550 | `550` in **1019** uses, the dominant value |
| Retreat when | 40 | 0 | -- |
| Max dist from home | 500 | 1200 | -- |
| Patrol AI | `CGaurdNearMovingPosAI` | `CScanAreaAI` | -- |

`Vision Cone=90` is the whole symptom. When his target dies the skeleton re-runs acquisition through
`CEntityBehaviorStateSetClosestTarget`, which only considers entities inside that 90-degree arc of his
facing — so an enemy beside or behind him does not exist, and he stands there.

`Target shooter if hit=1` bypasses acquisition altogether. That is why **being hit woke him**, and why
the fault read as apathy when it was blindness.

`Max Distance=300` compounds it: he could not see a target at a range where every other creature in the
game can.

**What that cone is actually for.** Its 145 uses concentrate in the siege maps — Temple District Siege
63, Gate District Siege 35, Crossroads Siege 9 — guards set to watch one direction. Exactly **one**
creature can in the whole game uses it. It is a sentry value, and a companion was built out of sentry
parts.

Nobody could have met this in vanilla, where he was unrecruitable until Fixt restored him in 0.6.0. It
took 0.28.1 making him keepable before anyone could watch him fight long enough to notice.

Now `360` / `550`, matching Cervantes and the game's dominant values.

## Two fields deliberately left alone

**`Valid Targets=Enemy`** — changing it would do nothing. `FUN_005e7e50` derives a companion's target
categories from the player's on join and stores the previous ones as `Original Skeleton Targeting
Flags`. It saves *flags* only, which is also why the cone and the range survive the join and were ours
to set. Cervantes' own template leaves `Valid Targets` empty, which would read as "targets nothing" if
the template value decided anything.

**`Retreat when=40`** — a real difference from Cervantes, who never flees, and kept on purpose. Fernand
still breaks off when badly hurt. The QA case records that as deliberate so it does not get filed as
the same defect later.

## Needs a fresh recruit

The relay writes his AI at join time, so a companion you are already travelling with keeps the old
eyes. Recruit him again on a character who has not yet taken him, and the north-island Vodyanoi fight
is the natural place to watch it: after a kill he should turn to the next enemy on his own, including
one behind him.

Nothing else in 0.28.x is affected.

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt.

Download, unzip, run `Mod Manager.bat`.

https://github.com/EricHype/LionheartFixt/releases/tag/v0.28.2
