# Lionheart Fixt 0.34.0 - One Draught Each

A question from play, right after the enemy healer went in: *"can we give enemies a skill they can
only use once, to mimic an item?"*

Yes. And it turns out the game has been doing exactly that the whole time.

## First, why a mimic is needed at all

Enemies in Lionheart cannot use items. Not "don't" — **cannot**. There is no "use an item" action
anywhere in the game, for anyone. An item's effect is welded to the item itself and fires from your
inventory screen; nothing an enemy does can reach it. They don't even carry potions. The only items
an enemy has are the ones that fall on the floor when it dies.

So a potion-drinking soldier has to be built out of something else.

## The trick was already in the game

The English Priest shields himself at the start of a fight, once, and then never again. That is a
one-shot ability, and it is a potion in everything but name — he may as well be drinking a buff
draught before the first swing.

The mechanism behind it works like a list that advances one step each time it runs, and sticks on the
last step forever. So **anything that isn't the last step happens exactly once per enemy.** It's the
same machinery that makes the Mana Tomes in the English Shrine give less each time you read them
before going dry.

Two things had to be checked before building on it.

**Can it wait until the enemy is actually hurt?** Yes — the game can read a character's health as a
percentage, and already does it in four of your own perks, including Die Hard and Adrenaline Rush.

**Is "once" once per enemy, or once ever?** Per enemy. The counters that track it are stored on each
individual creature, not on the type. If it were otherwise, only the very first Priest in the game
would ever shield himself.

## So the veterans carry a draught

The twelve **veteran** English soldier types now each carry one healing draught:

| | drinks at | restores |
|---|---|---|
| the weakest veteran | 40 HP | 35 |
| a tough one | ~55-69 HP | 48-61 |
| the toughest | 82 HP | 72 |

Each drinks **once**, when it drops to **40% health or below**, and heals a bit over a third of its
total. There is a flash of light so you can see it happen.

**It can be denied.** A soldier killed quickly from full health never gets low enough to drink, and
never does. Burst damage beats it outright — that's the counterplay, and it's deliberate.

**And the raw conscripts carry nothing.** The `Soldier1` and `Soldier2` ranks are untouched, which is
also the sensible answer in fiction: a new recruit doesn't get a healing draught.

## Also: the other two Priests now heal

0.33.0 gave the healing spell to the ordinary Priest alone, so one of them could prove it worked
before the rest got it. The tougher two now have it as well, scaled the way their shield already
scales — about 11-18, 14-22 and 17-26 hit points across the three ranks.

Still nothing for `Priest Near Death`, who casts nothing at all in the original game, or the Priests
down in the Caverns of Nostradamus, who are built differently enough to need their own pass.

## Something I got wrong

Worth telling you, because it nearly shipped.

The first version of the draughts was built from the **original** game files instead of Fixt's own. All
twelve of those soldiers already had Fixt work on them — their combat barks, from an earlier release —
and I wiped it out on all twelve at once.

**Every automated check passed.** They look for broken structure, bad formatting, wrong counts, wrong
line endings. None of them can tell that something from a previous release has silently gone missing.
It was caught by an unrelated accident: a file count came out twelve short of what I expected.

All twelve were restored and rebuilt properly, and the build now refuses to run unless the bark work
is still there afterwards. But `PO7` below exists because a diff proving it isn't the same as hearing
it in a fight.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Works on **any save** — this release changes characters and a spell, not maps.

## If you play it

**The backlog matters more than usual this time.** 0.33.0's two most important checks were never run,
and this release stacks three Priests and twelve soldiers on top of them. If the foundation turns out
to be wrong, rather more comes out than before. So: **start a new game, fight something ordinary, and
confirm nothing is strange** before anything else.

Then the structural one: **keep hitting a veteran soldier after it drinks.** It must not drink twice.
If it does, the whole mechanism is wrong and I need to know.

Then kill one fast from full health — it should never drink at all.

**And listen to them.** The soldiers' barks are the thing I broke and restored. If they've gone quiet,
that's the reason.

Last, the one nobody can predict: find a Priest fighting alongside veteran soldiers, so the Priest is
healing them *while* they drink their own draughts. That stacking is intended, but it has never been
seen by anyone. If it makes a group feel unkillable, say so and I'll pull one of the two numbers down.
