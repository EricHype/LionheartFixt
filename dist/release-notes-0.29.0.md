# Lionheart Fixt 0.29.0 - What the Trolls Say

A crash to desktop that has been shipping since 0.13.0, and the lava trolls finally getting a voice.

## The Inquisition Chambers crash

Reported by a player:

> Invalid class type -- Tried to use an unknown class "ClsQuestStatusCompletedAction" for a "Action"
> (CAction). Last file opened = "Resources/Levels/1 Barcelona/Dialog/Temple
> District/GrandInquisitor.DialogTree:Node:Reply:Custom Requirement:Operand2:Operand1"

The report is accurate; the name in it is only disguised by the crash dialog's font, where a capital I
renders as a lowercase l. The file named **`CIsQuestStatusCompletedAction`**, and no such class exists.

The real class is `CIsQuestCompletedAction`, and all three sites already carried its exact field set --
a lone `Quest=` -- so **only the name was wrong**. It looks like a blend with
`CSetQuestSatusToCompletedAction`, whose "Satus" typo is vanilla's own. The neighbourhood is a
minefield: `CIsQuestStateCompleatedAction` is also real, also misspelled, and takes different fields.

**It shipped in 0.13.0 and was present in 27 tagged releases.** It survived that long because the three
sites are the Grand Inquisitor's *return* nodes, gated on a Wilderness quest -- a player has to get
that far and then come back.

A dialogue-tree change, so it needs no fresh save.

### Gate 0 gains A0.15

Every `=CSomething` must now name a class the engine registers, checked against the C-prefixed strings
in `Lionheart.exe` plus every class vanilla's own data uses.

Nothing else in Gate 0 could have caught this. The tree parsed, round-tripped byte-exact, had balanced
braces, no dangling targets, correct blank lines, and the right fields for the class it *meant*. Class
names were simply never checked. The whole repository was swept; this was the only offender.

## The lava trolls

They were left out of 0.27.0's barks, and they turned out to have more waiting than any other family.

### A voice they already had

`Shoot Completed` was empty on all six cans, so the slot the other three families use was free -- and
the voice needed no inventing. The trolls already speak in two clearly different registers in their own
dialogue. Drones are broken and terse, sometimes wordless: *"You no belong!"*, *"Hot now, yes?"*,
*"<It grunts, and keeps coming.>"* The chief is fluent, measured and forever counting: *"I will count
you with the others."*, *"Hold him. He is one and we are many."*

20 lines -- 8 shared, 6 drone, 6 chief -- so each troll draws from 14 and **no drone ever speaks in the
chief's register**.

### The Troll Stomp was never cut content

`Troll Stomp.mdl16` sits in the archive referenced by nothing, which looks like a cut mechanic. It
isn't. Every troll's attack already ends in an area pulse of radius 120, firing twice, burning
everything in it -- and it has always been *invisible*. The model simply had no caller.

The confirmation is that the troll damage in save logs (5-12) matches the drone projectile's
area-of-effect range of 5-12 exactly: those log lines always were the stomp.

So the trolls have been stomping for twenty-three years and you could never see it. Now you can.

### Regeneration, and the number that decides it

`Troll Hide for Quinn` calls the troll *"a creature that closes its own wounds"*, and it closed
nothing. The obvious fix was nearly a disaster, because the units are not what they look like:

**HP per second = HealingRate x 0.1.**

That 0.1 is a constant in the executable, and without it the same value looks either inert or
fight-breaking. Simulated against numbers measured from real saves and combat logs, the chief's rate
costs a player about fourteen points of win rate -- a real cost, not a wall. Drones regain 0.6 HP a
second, the chief 1.0, against the player's 0.37 at that point in the game.

Their counter already shipped in 2003 and needed nothing: every troll race carries
`Cold Damage Resistance=-15`. Bring cold.

### A drone that calls for help

A wounded drone now fetches the **chief** -- one ally, the biggest one, which also reads like the
character already written. Once per troll, and never while you are at peace with them.

The first build of this broadcast to every troll by name, which the Troll Pit answers with **80 to 94
of them on a 4000-unit leash**. That is not a pack, it is the level, and it was cut back after being
measured rather than after being played.

## Needs a fresh approach to those areas

- the **crash fix** needs nothing: it is a dialogue tree, so an existing character is fine
- the **trolls** are can, race and item changes, so they want a character who has not yet entered the
  Troll Pit -- the same save that 0.28.0's Lava Troll Hide is still waiting on

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt.

Download, unzip, run `Mod Manager.bat`.

https://github.com/EricHype/LionheartFixt/releases/tag/v0.29.0
