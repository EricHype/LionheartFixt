# Lionheart Fixt 0.72.0 - what the Inquisition knows

Three scenes in the Inquisition's own questline that were written, recorded and never played, and a
repair to the release before this one.

## The Grand Inquisitor was taking orders from the villain, silently

Walk past the illusion wall into the Grand Inquisitor's chamber and a cutscene plays that the game
has always played: fog gathers, and the Old Man of the Mountain appears as a translucent apparition.

> The Cathars are a grave threat to you and to the Inquisition. I sense that they are gathering to
> oppose you in France. You need to move against them.

Then he dissolves, and Torquemada says nothing at all.

He was written to answer, and the line was recorded. It is four words long and it is the whole
meaning of the scene:

> *It is a great honor to speak with you again, Asha.*

Asha is the Old Man's true name. Nostradamus tells you his story, the woman in Montaillou calls him
her twin and her eternal foe, and a persuasive enough character can name him to his face at the end
of the game. So the beat that never played is the one where the head of the Inquisition greets the
man behind everything, by name, with deference, and is handed the order that the whole Cathar hunt in
Montaillou turns out to be carrying out.

He speaks now, before the apparition gives its instruction.

## The fire that did not burn you

When Torquemada tries to purify a magic user with fire, he used to go straight from the spell to *"I
do not know whether divine providence or fiendish charms guard your body from the fire."*

The line in between was recorded and skipped:

> *You resist? The flames do not harm you. Truly, I have not seen such a phenomenon. But is this a
> miracle or the work of demons?*

It is the moment the Inquisition finds out what you are, which is what the rest of the scene is about.

## Raphael remembers the cell

Draw a weapon on Inquisitor Raphael and his guards put you in a cell. Come back afterwards and he
greeted you with *"Welcome back, child. What do you seek now?"*, as though nothing had happened. His
own line for the occasion had been recorded and never used:

> *For your sake, I pray your time in prison has soothed your belligerence.*

The Grand Inquisitor has always said his version of this. Raphael says his now.

## Companions now grow as you level

Your companions never improved. Cervantes joins in act 1 with 60 hit points and still has 60 in
Alamut, where the things you are fighting have three hundred. The worst case is Fernand Desoto, the
sailor, who travels with you on 36.

From now on, every time you gain a level, each companion travelling with you gains hit points,
armour class and skill, and tells you so in their own words:

> *The poets will need a longer verse for me now.* (Grumdjum)
> *Salaam. I am less clumsy than the man you met.* (the Knight of Saladin)
> *The Lord sharpens what He intends to use, my child.* (Bishop Diego)
> *<Fang's ears go flat, and he circles wider than he used to.>*

The ten who join weak grow faster than the six who arrive already strong, so Joan of Arc and Sir
Roger stay recognisably themselves instead of ending the game as giants. Beatrice is deliberately
left out. A companion only earns the levels you gain **while they are with you**, so leaving someone
behind for an act means they fall behind, and a late recruit never catches up to an old friend.

**You have to click a companion once for this to start**, which is also what makes it work on a save
you have already been playing. Click any companion, choose anything, and from then on they grow.

## A repair: the warden in 0.71.10 was broken

0.71.10 was built so the warden of the Montserrat cellar walks to your cell bars after about
seventy-five seconds and starts talking, which restores one of the six ways out of the pen. That part
of the release did not work. A bug in the tool that built it turned the conversation into seven dead
lines, and the automated checks passed it because the damage was structurally valid.

It is fixed, and a new check now catches that whole class of defect. If you installed 0.71.10 and the
warden never came over, that was this, and this is the release that fixes it.

## What needs a new game, and what does not

**Companion growth works on a save you are already playing.** Click a companion once and it starts.

The other four changes are in map files, and the game bakes a map's contents into your save the first
time you enter it. The Inquisition chambers and foyer are in act 1 and the cellar is in act 2, so
seeing those needs a save that has not been to those places yet.
