# Lionheart Fixt 0.3.0 - the Knights of Saladin

The Dream Djinni tells you that you have become a **Favored One of the Knights of Saladin**.
Then it never makes you one.

The trials award a perk. The *rank* comes from a faction record - and in the whole shipped
game, a Saladin faction is assigned in exactly one place: a test map no player can reach. So
the check every Saladin reply depends on could never be true, and **twenty replies across
four acts have never been seen by anyone**. Seven of them belong to Sir Roger in the English
Shrine. Six to Quinn the Herbalist, standing about forty feet from the Djinni.

One faction assignment, beside the two perk grants that already fire, fixes all of it.

**Fixt** is a restoration-and-repair mod, named after Fallout Fixt and following the same
discipline. It fixes what is broken, restores what was cut, and writes new content only
where the game plainly ran out - working from the shipped archive rather than from opinion.

**Download:** https://github.com/EricHype/LionheartFixt/releases/latest
**Source:** https://github.com/EricHype/LionheartFixt (MIT)

---

## The Sacred Scimitar

A complete questline that could not be started.

Eduardo the blacksmith has all of it written - a test of valour, a material hunt, six
separate ways to talk your way past the test - and the sword exists as an item. It was
broken at three ends simultaneously. The starter is a proximity trigger with *both*
`Active=0` and `X Radius=0`. Amir's node is named `202 make a scimitar`, he visibly
deliberates over your second task, and then offers something else entirely. And the reply
that hands the finished blade over points at a node that does not exist - while carrying the
quest's completion action.

That middle one is the interesting one. `202` is not a mis-named passthrough; it is a fork
that lost an arm. There is nothing to deliberate over if only one task exists, and the
missing node shares its number with the surviving one, which is what happens when a branch
is written over rather than beside.

Amir now genuinely chooses. Earn your own blade, or recover a treasure for the Order.

## Farshad has a conversation

Sixteen nodes, two of them Saladin greetings, hidden because his talk interaction opened a
one-line balloon and his dialogue tree was never opened as a tree anywhere in the game. Walk
up to a Knight of Saladin, talk to him, get a grunt.

He will also teach you to use a sword, once you own one worth teaching with. He is already
duelling his twin brother and says so himself.

## The scimitar remembers how you earned it

Eduardo argues the case: *"it requires a test of valor, of bravery on the part of the owner
to give the scimitar its strength, its spiritual center."* Then he hands the same blade to
everyone, including the player who bartered their way out of the test. Now he does not.

And if you forged a blade before the trials, the Djinni no longer hands you an identical
second one. He sets the one you have alight.

---

## What playing found that reading could not

Restoring a questline runs code that has never executed. Four vanilla defects surfaced the
moment this one became completable, and every one of them passed every automated check the
project has:

- The quest could move **backwards**. The state the hand-in requires is set by exactly one
  reply; its sibling handed over the blade and sent the quest back a step, permanently.
- The hand-in reply lives on Amir's *"anything else?"* hub - reachable from seventeen
  unrelated topics and never from the greeting the game actually opens.
- The combat trial's reward is a **duplicate** of the blade you just forged. Almost
  certainly the cut quest's payoff, relocated when the quest was dropped.

That is the argument for playtesting each restoration rather than batching them.

---

## What 0.1.x and 0.2.x did, if you are new

The **goblins of the Wilderness** become a real faction with three accumulating ranks, and
the camp reads your standing. Two finished characters that shipped with complete dialogue
and zero map references are put back. The Goblin Girl's cut follow behaviour is restored,
bounded to her own cave. The Khan explains his war on Barcelona. Dead-end replies throughout
the goblin thread are repaired.

The rule the whole project follows: **every check adds a route and none removes one.** If
you solved a scene in vanilla by talking your way out of it, that still works.

---

## Installing

Unzip somewhere with a short path, double-click **`Mod Manager.bat`**, click the button that
names the mod. `Uninstall` puts everything back exactly as it was. No Python, no separate
mod manager. Windows only; GOG, Steam and retail.

**You must start a new game.** A save records a map's contents the first time it enters.

The download contains no game content: files that already exist in your installation travel
as deltas against your own copy and are rebuilt locally during installation.

---

## What has not been tested

The questline has been played through the scimitar and the lesson - that is how the four
bugs above were found. **The twenty replies have not been seen in play yet.**

If you find a rank-gated reply showing up for the wrong rank, that is the single most useful
thing you could report. It is the failure mode no automated check here can catch.

Issues: https://github.com/EricHype/LionheartFixt/issues
