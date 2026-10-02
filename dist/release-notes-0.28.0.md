# Lionheart Fixt 0.28.0 - The Hide and the Way Back

Two bugs a playthrough found. Both were invisible to every automated check for the same reason: the
data was correct, and something else overrode it at runtime.

## Fernand Desoto can be taken back

Reported five times. Four releases tried to fix it. All four were edits to a reply the player could
never reach.

The sixth attempt started with a diagnostic instead of a redesign: one `CPrintCombatTextAction` placed
**first** in the reply's action array, which lands in the combat log where the save can be read. It
never appeared -- not once in 234 events. The reply was not running at all.

The same save said why, in its own message log:

```
Companion: <What would you like your companion to do?>
Antonio Gula: Release Companion
```

That is not Fernand's dialogue. **While an NPC is a companion, the engine lays its own interaction
specifier over the top** -- `Player Data/Companion AI Interaction Specifier.can`, marked
`Use=Shared Global Instance`, opening `Levels/Generic Companion Dialog`. Talking to a follower opens
the generic companion menu, and the NPC's own conversation is unreachable for as long as it follows.

Release drops the overlay and exposes the specifier underneath. Fernand's pointed at his
*following*-state node, whose only offer was *"Wait here"* -- so a released companion was greeted with
another dismissal and no way back.

| attempt | what it did | why it failed |
|---|---|---|
| 0.25.3 | gave the node a dismiss and a rejoin, ungated | a dismissed Fernand still offered to be dismissed |
| 0.25.4 | gated the pair on a new scripting variable | the variable was never written -- the save proved it absent |
| 0.25.7 | found the node was a *balloon* with no reply list, and made it a conversation | necessary, and still not enough |
| 0.27.0 | a dedicated released-state node, reached by specifier swaps from canned objects | the swap never ran |

**Cervantes was showing the answer the whole time, and it is the opposite of what was built.** His
seven standing map specifiers point at `3 Return after release as a companion` and
`1500 cervantes leaves party dialogue` -- *released*-state nodes. The standing wiring is for when he is
not with you, because that is the only time anything sees it.

So the fix is one reference: the relay that recruits Fernand now installs his standing specifier on the
released-state node. The canned swaps are deleted -- the engine already swaps, earlier and more
reliably than a reply action can.

The old following-state node now offers the same way back, since it is in exactly the same position.
That repairs saves already stuck on it. **A save that recruited him before 0.25.7 has a balloon baked
in** and needs a fresh recruit; nothing can be done for those.

## The Lava Troll Hide drops when you kill the chief

Also from play: *"I'm killing the lava troll boss and all trolls, but I'm not getting a hide."*

Accurate, and no amount of killing would have worked. 0.10.0 put the drop on all three
`Lava Troll Boss` cans, copied field for field from Iapetus and Lethos, and it has been installed ever
since. But the chief is not spawned raw from the can. `05 Troll Pit.zax` spawns him through a generator
whose `After Action` runs `CSetDestroyedScriptActionAction`, which the executable describes as:

> "**Changes** the 'Destroyed Action' of any entity on the map to make the entity perform the specified
> action when the entitiy is destroyed or dies"

It replaces. The generator overwrote the can's slot the instant the chief spawned, leaving only the
vanilla bookkeeping. **The hide was dead code from the day it shipped.**

Vanilla settles that reading: the four Titan bosses carry the *same* quest item in both their can's slot
and their generator's, which would hand out two stonehearts apiece if the two stacked.

The galling part is that the **peace** route already handed a hide over in two separate nodes, using
exactly the right action. Only the kill route never got it.

Both generators that produce a troll chief now use `CActionGiveStandardInventoryItem` -- the Titans' own
idiom -- which puts it **straight in the killer's pack with a notification**. That also removes a hazard
nobody had noticed: the can's `Generate Within Radius=128` scatters a quest item on the floor, and that
floor is a lava pit.

Only the chief carries one. The ordinary trolls, tough and super included, still drop nothing.

## A new gate for the whole class of bug

`tools/validate.py` check **A0.14**: for every quest item a can drops from its own destroyed slot, find
the generators that spawn that can and fail if one overrides the slot without re-offering the item.

Nothing else in Gate 0 could have caught this. The can parsed, round-tripped byte-exact, named a real
item, used a field with 3960 occurrences, and matched a working vanilla boss line for line. Only the
interaction between the can and the map that spawns it was wrong.

## The method rule both halves share

Prove the code path **executes** before redesigning what is in it. Five releases and one dead quest
item went on edits that were individually sound and could never run. One probe, placed first, settles
it in a single playtest -- so reach for it on the second failure, not the fifth.

## Needs a fresh approach to those areas

Both halves are entity and map changes, so they reach things created after the install:

- **Fernand needs a character who has not yet recruited him** -- his interaction specifier is entity
  state, snapshotted on first visit. The exception is a save that already *released* him under
  0.25.3-0.27.0, which this repairs
- **the hide needs a character who has not yet entered the Troll Pit** -- the entity list is
  snapshotted on first visit too

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt.

Download, unzip, run `Mod Manager.bat`.

https://github.com/EricHype/LionheartFixt/releases/tag/v0.28.0
