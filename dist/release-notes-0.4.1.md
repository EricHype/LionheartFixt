**This release contains no new content.** Every line of it repairs something already
shipped, and most of it repairs releases you already have installed.

Two of the three items were found the way these things usually are: by a player walking a
path nobody had walked before, and something not happening.

## Two of Quinn's three errands could never be started

If you installed 0.4.0 and tried to bring Quinn his wasp stingers or a lava troll hide, you
could not. He asks, you agree, and the quest never activates -- so the turn-in reply never
appears and the errand cannot be completed. **Two thirds of 0.4.0's content.**

The offer replies carried the requirement deciding whether to *show* them, and no action to
actually start them. The wolf pelts errand was wired correctly, which is why it worked and
the other two silently did not.

The same missing state also gated the peaceful route to a lava troll hide, so that was dead
too.

## A structural defect that has been shipping since 0.2.0

A reply in a Lionheart conversation file must be preceded by a blank line. The shipped game
holds that without a single exception -- 10,915 replies, zero violations -- and the parser
needs it. Without the separator a reply is swallowed into the one before it: it never becomes
its own choice, and whatever it was supposed to *do* never runs.

It fails silently, and it looks nothing like its cause. The conversation plays normally and a
quest just does not advance.

Fixt had **47 of them, across six conversations**, because every tool used to reorder or add
replies rebuilt the node without putting the blank line back:

| Conversation | Sites | Shipped in |
|---|---|---|
| Quinn the herbalist | 21 | 0.4.0 |
| The Goblin Khan | 5 | 0.2.0 |
| Amir | 2 | 0.3.0 |
| A Saladin knight | 1 | 0.3.0 |
| Guard Esteban | 1 | 0.2.0 |

If you play a Saladin character, one of these is worth knowing about. Amir's return
conversation is the node the **Sacred Scimitar hand-in** was moved to in 0.3.0 after being
reported unreachable twice. The move was correct both times; it was very likely landing in a
malformed node the whole way. That diagnosis was wrong, and this is the actual fix.

## Esteban's contract never updated its journal

Kill Guard Esteban for the goblin patrol and your log still said to kill him. The quest was
always completable -- the hand-in checks whether he is dead, not the journal state -- but the
entry telling you to go and collect never fired. It does now, and only for a character who
actually took the goblins' contract.

## The gates that should have caught all this

`tools/validate.py` now fails on a reply missing its blank line, naming the node, and on any
quest state this mod defines that nothing ever activates. Both were verified by deliberately
breaking them first.

Neither check existed before, which is exactly why three releases shipped with these defects
in them. The second check found the Esteban bug on its first run.

## Installing

Install over 0.4.0 as normal; the manager replaces the previous version. **These repairs
apply to conversations, so they take effect on an existing save** -- unlike new characters or
map changes, dialogue is read fresh every time you talk to someone.

If you were stuck on Quinn's wasp stingers or troll hide, you will need to ask him again.
