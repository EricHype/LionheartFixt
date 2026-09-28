# Lionheart Fixt 0.21.1 - the Daeva

0.21.0 asked whether any of this work had actually made the game play better, and for the Crypt and England the
answer was no. This release is the same question pointed at the Pyrenees, and it found something worse: the best
thing in the region had never been touched at all.

The Shapeshifting Daeva follows you across three regions. It knows whether you met it in Barcelona, whether you
fought it in Toulouse, and which relic of Zarathustra you are carrying. It can be talked down at Speech 95,
which makes it one of only four encounters in the entire game with a talk-instead-of-fight resolution. Its two
trees carried **27 orphan nodes** and no previous release had opened one of them.

## Three things that were written and never played

**The Ring's reaction.** The confrontation triggers if you carry the Ring of the Prophet *or* the Amulet - and
then, whichever you held, it always played the Amulet's line. So the Ring had its own written reaction that no
player has ever seen. Worse: all six of the Speech entry points sit on relic nodes, and the Ring's was one of
them, so bringing the Ring instead of the Amulet silently cost you **the entire talk route**.

**Its escape from Montaillou.** Toulouse plays its parting line - *"you will find me in Montaillou, Lionheart,
away from these meddlesome titans!"* Montaillou already had the relay that does the same mechanical work and it
never spoke, so the creature left in silence. It now says what it was given: *"this exertion has left me
ravenous... that lake town has all of my favorite flavors."*

**And the fight cannot be won without a relic.** Killing the third or fourth disguised form fires a relay that
re-activates six clone generators with no condition and no item check of any kind, while the true form - the
only version that fires nothing on death and therefore stays dead - is raised by exactly one thing in the level:
the relic check. That is why it taunts that you do not have the power to truly defeat it. It was telling the
truth.

## The debt

Under a Barcelona church there is a Daeva of Pain in a cell, and if you free it, it says this:

> *"Ahhh...the shackles fall away and my power returns! My judgment will be swift and merciless, but to you, I
> have a debt to repay..."*

The game states the debt and never collects it. Now it does, and what it owes depends on which service you
actually did.

**Lure the wizard to him** and he comes to Montaillou himself. The camera moves, and the two of them trade barbs
before anything is swung - he opens with *"Still wearing other people's faces. Ninety years in this valley and
you have not once learned to be looked at"*, she answers by naming him, *"Aeshma. They kept you in a box under a
church and you came out of it grateful, running errands for the thing that opened the lid"*, and he closes it:
*"He will hear it from whichever of us is still standing, so tell it carefully."* Then he breaks the clone loop,
brings her true form up stripped of the twenty-odd hit points a second it heals, and fights her.

**Break the crosses yourself** and he does the lesser thing. He is waiting at the spot where your spirit
companion already tells you something is ahead, sitting on a broken wall: *"Spirits are good at that and no use
at all afterwards. I am here to be of use afterwards, and then we are done with each other."* He gives up her
true name, and a name is enough - *"a daeva cannot lie about its name and cannot stand to hear it said
correctly; say it to her face and she will have to stop and argue with you instead of eating you."* That opens
the talk route to a character who never found a relic at all.

Refuse him and it closes again. Kill him in Barcelona and none of it happens.

## What is still undone here

Most of the region. The Daeva has 23 orphan nodes left, and the twelve Toulouse trees between them carry roughly
846 replies with **not one gated on anything** - no faction, no race, no skill, no karma - in a region whose
whole subject is choosing a side in a war between ogres and titans. Act 1 carries two thousand such checks.
Toulouse carries none. That is a different kind of tier and it has not been built.

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt.

Download, unzip, run `Mod Manager.bat`. Needs a character who has not yet reached Montaillou's hamlet, and the
debt needs one who has not yet decided what to do about the demon in Barcelona. Unplayed; what you find goes
into 0.21.2.

https://github.com/EricHype/LionheartFixt/releases/tag/v0.21.1
