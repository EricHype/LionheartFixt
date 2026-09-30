# Lionheart Fixt 0.25.6 - the marker for the verified build

**This release changes no game file.** `git diff v0.25.5..v0.25.6 -- files/` is empty, and the zip
differs from 0.25.5's only in the version string. **If you have 0.25.5, installing this gains you
nothing.**

It exists so that the build the first playtest of the 0.25.x line actually validated has a number to
point at. Five patches landed in a single day, and "which of these is the one that was played?" had no
answer otherwise.

## What the playtest established, 29 September

**The enemy backstab of 0.25.0 fires.** From a save taken in the preorder bonus level while surrounded
by three:

> Thief Swordsman sneaks up on Antonio Gula and hits for 8 (9 Slashing Damage) (25 percent backstab
> bonus)

The thief is the attacker and the bonus is the base tier's 25 percent, so the whole chain works: the
race preset, `Sneak Enabled` and `Is Backstab Mode Enabled`, the facing gate, the damage and the log
line. In that fight **7 melee thief attacks landed and 1 was a backstab** -- about one in seven, which
is the facing condition behaving as intended rather than firing constantly or never.

That also answers empirically what reading the executable could not: the gate compares the angle the
damage pipeline supplies against the **defender's** facing, and an attacker behind the defender
qualifies.

**The thieves render and move normally.** This was the single most important thing to check, and it
confirms the reasoning the whole approach rested on: a race preset writes the attribute the gate reads
and leaves the engine's own sneak-state field at `+0x134` alone, so an NPC with `Sneak Enabled` preset
does not creep, vanish or change appearance.

It is easy to miss in play. The message log wraps long lines and the backstab template is much longer
than an ordinary hit, so on screen it reads as two rows with the recognisable bonus text on the second,
among ordinary hits.

## What is in this build

| | |
|---|---|
| 0.25.0 | the Priestesses cast, the Bonecaller summons, the thieves backstab |
| 0.25.1 | the startup crash -- 0.19.0 through 0.25.0 could not reach the main menu |
| 0.25.2 | eleven dialogue trees that named their own file and hung the loader |
| 0.25.3 | Fernand Desoto could be dismissed but never taken back |
| 0.25.4 | and his two replies now know which one applies |
| 0.25.5 | the same for the Knight of Saladin, after an audit cleared the other companions |

## Still open

Three of the backstab gate's four callers were not read, so "attack types 1 and 3 are melee" is inferred
from the perk text rather than traced. And it is not known whether the engine can ever deliver the
stop-sneaking message to one of these NPCs, which would drop the preset to 0 permanently.

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt.

Download, unzip, run `Mod Manager.bat` -- though if you are already on 0.25.5 there is nothing here to
install.

https://github.com/EricHype/LionheartFixt/releases/tag/v0.25.6
