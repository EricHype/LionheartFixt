The Dream Djinni tells you that you have become a **Favored One of the Knights of Saladin**,
and then never makes you one.

## The order awards the title and never the rank

The trials are reachable and completable. They hand out `Dervish of the Crescent` or
`Scholar of the Crescent` depending on whether you beat Kabool in combat or in a contest of
wits. Both are perks, and perks confer only skills.

The *rank* comes from a faction record -- and in the entire shipped game, a Saladin faction
is assigned in exactly one place: a test map that no player can reach. So the check every
Saladin reply depends on could never be true, and **twenty replies across four acts could
never appear**:

| Who | Replies |
|---|---|
| Sir Roger, English Shrine | 7 |
| Quinn the Herbalist, Barcelona | 6 |
| Brother Michel, Montaillou | 3 |
| Joan of Arc, the Crypt | 3 |
| Temple Entrance Guard, Barcelona | 1 |

Plus both Barcelona knights' *"Welcome, brother into the Order of Saladin"* greetings.

One faction assignment beside the two perk grants fixes all of it. You now also *feel* the
rank: +10 One-Handed, +10 Two-Handed, +1 Endurance, +20 carry weight.

## The Sacred Scimitar

A complete questline that could not be started. Eduardo the blacksmith has the whole thing
written -- a test of valour, a material hunt, six different ways to talk your way past the
test -- and the sword itself exists as an item. It was broken at all three ends at once:

- **The starter was switched off.** The only thing that begins the quest is a proximity
  trigger in the smithy with *both* `Active=0` and `X Radius=0`.
- **Amir never offered it.** His node is literally named `202 make a scimitar`, he
  deliberates -- *"Hmmm. Yes, yes, I have decided on your second task"* -- and then offers
  the Shard of Dreams. It is a fork that lost an arm.
- **Amir could not receive it.** *"I have forged the Sacred Scimitar"* pointed at a node
  that does not exist, and that reply carries the quest's completion.

Amir now genuinely chooses. Take the scimitar arm and you earn your own blade; take the
Shard and you recover a treasure for the Order. One or the other, not both.

We did **not** re-enable the dead trigger in the smithy. It is ungated, so it would hand the
quest to everyone who walks in, which is plausibly why it was switched off.

## Farshad has a conversation

Sixteen nodes, including two of the Saladin greetings above, hidden because his talk
interaction opened a one-line *balloon* and his dialogue tree was never opened as a tree
anywhere in the game. Walk up to a Knight of Saladin, talk to him, get a grunt.

He will also teach you, once you carry a blade worth teaching with. He is already duelling
his twin Farshid and says so himself -- *"He has much to learn in the ways of the blade, and
I have much to teach."*

## The scimitar remembers how you earned it

Eduardo argues the case himself: *"it requires a test of valor, of bravery on the part of
the owner to give the scimitar its strength, its spiritual center."* And then hands the same
blade to everyone, including the player who talked their way out of the test.

| How you got it | What you get |
|---|---|
| Retrieved his father's sword, refused payment | the Sacred Scimitar, and karma |
| Retrieved it, took the payment | the Sacred Scimitar, and 150 gold |
| Talked or bartered past the test | a Crescent Scimitar -- honestly made, and plain |

The first two are vanilla and unchanged. **The third is this release's only deliberate
balance change**, and it devalues a route rather than adding one. It does not close the
route: you still get a scimitar, the quest still completes, Amir still accepts it.

And if you have forged a blade before the trials, the Dream Djinni no longer hands you an
identical second one. He sets the one you have alight.

## Four things vanilla got wrong that only playing could find

Restoring a questline runs code that has never executed. Every one of these passed every
automated check:

- **The quest could move backwards.** The state Amir's gate requires is set in exactly one
  reply; the other reply at the same node handed over the blade and sent the quest back a
  step, with nothing anywhere to advance it again.
- **The hand-in was unreachable.** Its reply lives on Amir's "anything else?" hub, which you
  only land on after asking him about something unrelated first.
- **The trial reward was a duplicate** of the thing you just spent a questline forging.
- One near miss: enchanting the blade would have silently broken Farshad's lesson.

## Installing

1. Download `lionheart-fixt-0.3.0.zip`, unzip somewhere with a **short path**.
2. Double-click **`Mod Manager.bat`**, then **Install**.

Upgrading from 0.2.x: uninstall first. **You need a new character** -- this release edits
four maps, and a save records a map's contents the first time it enters.

## What has been tested

The Saladin questline has been played through the scimitar and the lesson, which is how four
of the bugs above were found. The faction payoff -- the twenty replies -- has **not** been
seen in play yet.

The single most useful thing you could report: **a rank-gated reply appearing for the wrong
rank.** If a character who is not a Saladin sees any of those twenty replies, a gate has
failed open, and that is the failure no automated check in this project can catch.

## Verifying the download

    certutil -hashfile lionheart-fixt-0.3.0.zip SHA256

Compare against `lionheart-fixt-0.3.0.zip.sha256`.
