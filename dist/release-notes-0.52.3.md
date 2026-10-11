# Lionheart Fixt 0.52.3 - the skill level nine wands never managed to print

Reported twice, which is what moved this one from "noted" to "fixed". It's the last of three defects
found in a single generated wand — 0.52.2 took the other two.

## What was wrong

Nine wands tell you what level they cast their spell at. They worked it out by printing an
*adjustment* rather than the level itself:

| your own skill in that spell | what a level-5 wand printed |
|---|---|
| 0 | "at skill level 5" — right, and exactly why nobody caught it |
| 20 | "at skill level -15" |
| anything it couldn't read | **"(Could not evaluate expression)"** |

At zero skill the two numbers happen to be identical. Every one of these descriptions has been wrong
since release for anyone who'd put a point in the relevant spell.

## The second report changed my answer

I'd explained the error message as the wand having nobody to measure against — sitting on the ground,
or in a shop window. **That was wrong**, and the second report proved it: the wand was in the player's
hands, so there was obviously somebody to measure.

The text simply never has anything to measure against, wherever the wand is. Which means no amount of
cleverness about *when* the description gets read would have helped, and writing the level down as a
plain number was always the only fix.

## Why it wasn't a one-line change

The obvious fix — just make that number a constant — would have broken the wands outright.

That same piece of arithmetic is doing a second job: while the wand is selected it **pins** your skill
to the wand's level, so the wand casts at its own strength no matter who picks it up. Replacing it with
a plain number would have turned "pin my skill to 5" into "**add** 5 to my skill". A strong caster
would have been quietly handed a bonus, and the wands would all have stopped working the way they were
designed to.

So each wand got a **second** number, used only by the sentence, and the arithmetic was left exactly
as it was:

| wand | casts at | | wand | casts at |
|---|---|---|---|---|
| Lightning Bolts | 5 | | Greater Lightning Bolts | 25 |
| Fireballs | 5 | | Greater Fireballs | 25 |
| Spikes | 5 | | Poison Ring | 20 |
| Slow | 15 | | Fire Circle | 10 |
| The Swarm | 30 | | | |

**Nothing about how these wands behave has changed.** I checked that rather than assuming it: every
one of the nine files was compared against the original game, and the arithmetic is byte-for-byte
identical in all of them, with nothing outside the one sentence altered.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Works on **any save** — but **item descriptions are baked into the item**, so a wand already in your
pack keeps its old text. You need one that drops after installing.

## If you play it

**The check:** a newly dropped lightning, fireball, spike, slow, poison ring, fire circle or swarm
wand should read **"at skill level 5"** — or whichever number belongs to it. Seeing
"(Could not evaluate expression)" or a negative number now means something is wrong, where last
release it was expected.

**The check that matters more:** take one of these wands to a character who's already good at that
spell, select it, and look at the skill. It should be **pinned down to the wand's level, not raised
by it**. The number on the label and the number in the mechanism now come from two different places,
and this is what proves they didn't get crossed.
