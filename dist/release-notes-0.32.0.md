# Lionheart Fixt 0.32.0 - The Siege Ran Dry

This one came from a player report, and the player's own hedge turned out to be the most useful part
of it:

> *"During my old playthroughs I noticed that mag builds suffer from lack of mana during war with
> England and later on in the game. Possibly add more mana in cavern of Nostradamus and crypt? Idk
> about that - don't remember if it is a issue in these two spots."*

Right about the war. Wrong about the other two, and the hedge was the correct instinct.

## The Crypt and Nostradamus did not need it

They are the two **highest** drop-rate acts in the game -- **94%** and **97%** of enemy groups there
drop spirit energy. Their mana comes from kills instead of from orbs lying on the floor, so the
sparse placement is a trade rather than a gap. Adding founts there would have re-solved a solved
problem, so nothing was added.

## And the English Shrine has something no other act has

On placed mana alone, act 7 measured the **worst in the game** at 3,419. It stayed that way for two
passes of this investigation. Then the **Mana Tomes** turned up: **ten of them, only in the shrine,
and nothing like them anywhere else in the game.**

Read a tome and it gives 125-150 mana. Read it again: 75-100. Then 50-75, then 25-50, then 20-30,
and from then on it just tells you it is empty, forever. A canteen rather than a font -- worth
170-905 each depending on the tome, and **4,909 across the act.**

That more than doubles act 7 and takes it off the table.

## Which leaves the war with England alone at the bottom

Every other act in the game is generous in one of the two ways mana arrives. If the floor is bare,
the enemies drop it. If the enemies are stingy, the floor is covered.

Act 6 is neither, and the reason is worth seeing:

| the English | what they drop |
|---|---|
| their **19 WarGolems** | the **largest spirit charge in the game** |
| their **6 priests** | the second largest |
| their **24 soldiers** | **nothing at all** |

The English were not designed dry. The **soldiers** were skipped -- and the soldiers are nearly
everything you fight in the siege.

That would be the better repair, and it is not the one in this release. Every English soldier is
also used in act 3 Montaillou and in the English Shrine, so there is no way to change what they
drop without changing two acts that did not need it. It is written down in the QA notes as the
thing to do if a wider pass is ever wanted.

## What actually changed

The starvation turned out to be **two maps**, not the whole act:

| | mana per enemy |
|---|---|
| **Crossroads Siege** | **2.10** -> **7.17** |
| **Crossroads to England** | **1.20** -> **6.97** |
| Gate District Siege | 7.23 - *unchanged* |
| Temple District Siege | 13.55 - *unchanged* |

Crossroads Siege was carrying **40% of the act's enemies on fourteen pickups.** It now has
forty-three. Crossroads to England had **one**, for seventy-nine enemies; it now has eight.

Gate District and Temple District were already fine, so they were not touched at all, and the target
was not invented -- it is **Gate District's own ratio**, taken from inside the same act.

Every new pickup sits **inside an enemy spawn area**, so the mana is where the fighting is rather
than scattered in empty ground, and so it is standing on ground the game already walks enemies
across. Vanilla does the same thing, sometimes within six feet of a spawn point.

## And seven goblins who were talking to a friend who was not there

Reported while this was being built:

> *"one of the goblin barks is `<he looks for the goblin who was beside him a moment ago>` this keeps
> happening for solitary goblins"*

It does, and there were six more like it. Searching the bark bank for anything that assumed a second
goblin -- shoving the one beside him, checking who is behind him, holding a line -- turned up
**seven** lines out of ninety-two.

The reason it kept happening is that **goblins mostly fight alone.** The common goblin spawns by
itself in 48 of its 64 placements, the archer in 51 of 65 -- and the officer in his hat, the one
shouting *"Hold the line!"*, is alone in **twelve of his thirteen**. He has no line. He never did.

All seven are **reworded, not cut.** Removing them would have shrunk four banks to fix what was only
ever a phrasing problem, and the size of those banks is the only reason you are not hearing the same
goblin twice a minute. So the reported line is now *"He looks around for help, and takes his time
about believing there is none"* -- the same beat, minus the corpse that was never there -- and the
officer now points, and keeps pointing until something moves.

Still ninety-two barks. Nothing lost.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

**This one needs a save that has not been into the Crossroads yet.** The game writes a map's
contents into your save the first time you walk in, so new pickups cannot appear in a Crossroads you
have already fought through. Everything else Fixt has ever shipped still applies as normal.

## If you play it

**One row matters more than the rest, and it is a feel question, not a counting one.** Take a mage
into Crossroads Siege on a save that has never been into act 6, fight it the way you normally would,
and do not go hunting for pickups. Then say whether you still ran dry.

Please answer that rather than whether the orbs were visible -- the orbs are easy to confirm and
tell us nothing about whether the problem is actually fixed.

Two smaller ones: **Gate District and Temple District should feel exactly as they always have.** If
either of them is different, something went somewhere it should not have, and I would want to know.

And for the goblins: **hurt one that is fighting alone and read what it says.** Nothing should
mention a companion. If a reworded line now sounds wrong in a *crowd* instead, that is the half a
rewrite has to earn and a deletion would have got for free -- so say which one.
