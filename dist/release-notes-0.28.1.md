# Lionheart Fixt 0.28.1 - what the overlay actually does

0.28.0 said Fernand Desoto could be taken back. He could not. This is the seventh attempt at that bug
and the first one aimed at the right thing, because the last of it was never in his dialogue at all.

## The overlay is a swap that remembers

0.28.0's notes said the engine "lays its own interaction specifier over the top" of a companion. That
is the behaviour, not the mechanism, and the difference is where the remaining bug lived.

`FUN_005e7870` does not append. It walks the entity's AI array for an existing
`CAIInteractionSpecifier`, **parks it**, and replaces it in place:

```
uVar4 = FUN_005b95e0(uVar6);     // the specifier already there
*(iStack_18 + 0x10) = uVar4;     // parked, to put back on release
...
FUN_005b9600(uVar7, piVar3);     // replaced at that index
```

Only if the entity has none does it append. And in the end no decompiling was needed, because the save
format names the slot out loud. Cervantes, while following:

```
Original AIInteractionSpecifier=CAIInteractionSpecifier
{
  Dialog Tree File=Levels/1 Barcelona/Dialog/Temple District/Cervantes
  Node ID=3 Return after release as a companion
}
```

One active specifier, his own parked, and the parked copy opens the **released**-state node. Reading
his data instead of his dialogue would have shortened this by several releases.

So there are two requirements, and 0.28.0 only met the second:

1. the NPC must **already carry** a specifier when the companion call runs, or nothing is parked;
2. the parked specifier must open the **released**-state node, since that is the only state anyone ever
   sees it in.

## The bug: a race in Fernand's own join node

```
Action=CTriggerRelayAction { Relay Name=fernand joins you }          // removes his specifier NOW,
                                                                    // re-adds it after Delay=0.1
Action=CDelayAction { Next Action=CSetCompanionAction ... Delay=0.1 }
```

Both land on the same tick, and two actions on the same delay are not ordered. The companion call won,
found an empty slot, appended the overlay and parked nothing — so release had nothing to restore, and
the generic *"What would you like your companion to do?"* menu stuck to him permanently, first in the
array, winning every interaction.

The save showed it exactly: **two** active specifiers where a working companion has one, no
`Original AIInteractionSpecifier` anywhere, and one *"companion has joined your party"* against three
*"has left"*.

**Cervantes never had a race to lose.** His specifier is standing map data, present before anyone
recruits him, so the engine always finds it, parks it, and puts it back. That — not the node naming —
is the deeper reason he has worked since 2003.

The companion call now waits `0.5s`, five times the relay's delay. The save then matches Cervantes
field for field: one active specifier at `X Radius=30`, and `Original AIInteractionSpecifier` holding
`103 fernand waiting`.

## A cheaper test than playing it

Two QA cases verify this from the save **immediately after recruiting, with no release needed**:

```
python tools/savecheck.py grep "Original AIInteractionSpecifier" --save latest
```

- **FN11** — present, and opening `103 fernand waiting`
- **FN12** — exactly **one** active specifier; two means the race is back

## What seven attempts on one bug taught

- Prove the code path **runs** before redesigning what is in it.
- Then verify the **state** it produced against a known-good example. A fix confirmed on behaviour
  alone is not confirmed, and a report of "acts the same" cannot distinguish two causes with one
  symptom — which is exactly what happened between 0.28.0 and here.
- Two actions on the same delay are not ordered. If one must observe the other's effect, separate them.
- Read the working example's data, not its dialogue.

## Known limit

A character who recruited him under 0.25.3 through 0.28.0 has the overlay appended with nothing parked,
and entity state is snapshotted on first visit, so **that save cannot be repaired** — nothing recorded
what should have been there. It needs a character who has not yet recruited him. A save from before
0.25.7 has a *balloon* specifier baked in and is likewise beyond reach.

Nothing else in 0.28.0 is affected; the Lava Troll Hide fix and Gate 0's A0.14 are unchanged.

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt.

Download, unzip, run `Mod Manager.bat`.

https://github.com/EricHype/LionheartFixt/releases/tag/v0.28.1
