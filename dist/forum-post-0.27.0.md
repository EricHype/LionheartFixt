# Lionheart Fixt 0.27.0 - What the Thieves Say

Enemies get something to say, and Fernand Desoto finally gets a way back.

## Hover text, one voice per family and a sub-bank per role

**67 cans, 71 lines, three families.** The text floats over the creature's head, not in the combat log.

| family | shared | sub-banks | cans |
|---|---|---|---|
| thieves | 8 | boss 5, archer 5, melee 5 | 36 |
| English soldiers | 8 | officer 5, archer 5, melee 5 | 24 |
| Snakebreed | 7 | venom 5, summoner 4, boss 4, drone 5 | 9 |

A creature draws from its family's shared lines **plus the sub-bank for its own role**, so a thief
archer picks from thirteen and a thief boss from a different thirteen. The boss gives orders -- *"Hold
him! He is worth more breathing!"* -- while the archer talks about range -- *"Keep your distance from
him!"*. An English officer shouts *"Not one step back, do you hear me!"*; his archers call *"Nock and
draw!"*. The Snakebreed hiss: *"Ssssoft thing. Warm thing."*

Roughly **one attack in four** carries a bark, and the line is drawn fresh each time.

**The mechanism is the game's own.** 21 shipped cans already float a dialogue node over a creature with
`CDisplayDialogBalloonAction` -- 18 sewer thieves and three guard dogs. Those guard dogs showing
`Guarddog` node `10 Growls` are also the precedent for a creature with **no speech** and for a stage
direction as the whole line, which is what the Snakebreed use.

`Include In Log=0` throughout, deliberately. The log is where this game puts narration -- 222 uses of
`CPrintCombatTextAction` saying things like *"You discover a treasure buried in the ground"* -- so
creature speech there would read as the narrator rather than the enemy.

The three `Snakebreed Summoner` cans are skipped: their attack slot already carries a
`CAddTemporaryAIAction`. Their sub-bank sits in the tree unused, against the day they get one.

## Fernand Desoto can be taken back

Three earlier releases tried to fix this and all three failed the same way: they tried to make **one
dialogue node** serve both the following and the released state.

| | what it did | why it failed |
|---|---|---|
| 0.25.3 | gave the node a dismiss and a rejoin, ungated | a dismissed Fernand still offered to be dismissed |
| 0.25.4 | gated the pair on a new scripting variable | the variable was never written -- the save proves it absent |
| 0.25.7 | found the node was a **balloon** with no reply list at all, and made it a conversation | necessary, but the broken gating survived it |

**Cervantes has worked since 2003 and does none of that.** He has a node called `3 Return after release
as a companion`, both replies ungated, and two maps carry an interaction specifier pointing straight at
it. The state is encoded by **which node the specifier opens**, not by a flag. Grumdjum uses the same
shape, and `666 Rejoin` is the Knight of Saladin's version.

Fernand had a node for *following* and none for *released*. Three releases of gating were an attempt to
simulate a node that was simply missing.

Now:

| state | his interaction opens | what it offers |
|---|---|---|
| following | `100 companion banter` | *Wait here, Fernand* -- releases him, then points his specifier at 103 |
| released | `103 fernand waiting` | *Walk with me again* -- recruits him, then points it back at 100 |

Each swap runs from a `CCannedObject` fired by `CUseCannedActionAction`, because a tree may not name
its own file, and the swap is copied field for field from the `fernand joins you` relay already working
in the same map. The scripting variable is deleted.

Nothing now depends on `$Instigator` resolving in that conversation, on a new attribute being writable
against an existing character, or on how the player dismissed him.

## What the companion audit missed, and why it matters

The audit that cleared Grace, the Goblin Girl and Grumdjum scanned **only this project's files**.
Cervantes is pure vanilla, so the working reference implementation for exactly this problem sat outside
the search path while three worse answers were invented against it.

A sweep asking *"how does this game do X"* has to include vanilla, not just what the mod has already
touched. That is now written into the project's own notes.

## Needs a fresh approach to those areas

Both halves are **can and entity changes**, so they reach creatures and interactions created after the
install:

- the barks want a save that has not entered the sewers, the Slave Pits, the bonus level, act 7's
  shrine or the Snakebreed's ground
- **Fernand needs a character who has not yet recruited him** -- his interaction specifier is entity
  state and is snapshotted on first visit

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt.

Download, unzip, run `Mod Manager.bat`.

https://github.com/EricHype/LionheartFixt/releases/tag/v0.27.0
