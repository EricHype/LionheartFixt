**Read this first.** Nothing in this release has been played, and neither has 0.15.0, 0.14.0,
0.13.0 or 0.12.0 before it. Everything passes the automated gate and `docs/releases.md` records
what each piece was read against. If you would rather wait for a build somebody has walked, wait
for 0.16.1.

## The Crypt of the Bleeding Lance

Act 4. Ten maps, 4,206 level parts, 269 live enemy spawners, **one quest -- and the quest was only
a name.** `Release the Doomed Knights from their torment` had no states, so it could never be
entered in the journal, never advanced and never completed; it existed only to be failed if you
killed Jehanne. Four of the ten maps are called "Misc Crypt" and held no conversation, no balloon
and no dialogue tree between them. And the act is built around a siege that has been running for
two hundred and eleven years, which nothing in the shipped game let the player touch.

**The quest works.** Three states -- the knights found, the curse understood, the lamp -- and 2500
XP when the efreet's wish frees them.

**Jehanne never remembered being convinced.** Convince her with Speech that her Council has been
lying to her, walk away, come back, and she greets you as the monster she met at the gate. The
flag that records the conversation was set nowhere.

**Her garrison was placed where nobody meets it.** The undead Templars who hold the line are all
on the Doomed Plateau, the densest map in the game, where the player arrives already in a fight.
A knight now holds a forward post in the Retreat of Souls, where you meet him before the shooting
starts, and behind the lines there is **a camp** -- the project's third new map -- built around
the man who has kept the tally since the seals closed: *"two hundred and eleven years. I have kept
the count."*

**66 traps that finally test something.** The act had 67 trap and lockpick checks after this pass
and none before it. A thief's route through the Crypt is now a different act from a fighter's.

**The six claimants, each answered.** Templar, Inquisitor, Knight of Saladin, Wielder, Dark
Wielder and Goblin Champion each have their own way through Jehanne, and she was tried by a court
of the Church and burned by it, so she has something specific to say to the one carrying its writ.
The magic schools read the seals; Divine or Tribal 80 gets Brother Michel to explain how a seal is
broken.

## The war you can actually fight

The four Misc Crypts are **four fronts**, with 248 generators between them that expressed nothing.
Each corridor now says what it is, and each has one lever that moves the line: bar the door the
garrison falls back through, bolt the stone door so the horde takes the long way round, throw open
the last coffin's thirteen protect walls, or release the three crypts with vanilla's own switch.
Two of those help the knights and two cost them.

**The tide is legible.** The knight at the fire reports it three ways -- *"the count moved for the
first time since the seals closed"*, or *"something is loose in the lower galleries that was not
loose last week... I will not ask whether that was you"*, or the stalemate. Admit to the bad one
and he will not thank you for it.

**And the act's one real outcome reads the war it ends.** The wish that frees the knights pays out
three ways: freed *in good order*, going out like lamps from the corridors you shut first, the last
of them the man at the fire, who stops counting; freed *into a ruin*, where *"you have freed a
garrison out of a crypt you made worse, and both of those are true at once"*; or freed *from a
stalemate*, all at once, mid-step, and *"the siege does not end. It simply stops having two
sides."*

## The companion nobody hears

Jehanne can join you, and vanilla wrote her four companion nodes. **One of them has ever been
reachable.** *"No, wait here for my return"* pointed at nothing; `600 Companion Banter General` and
`600 Companion Quest Done Relic Safe` were fired by no map in the game. All four work now -- she
speaks as she joins, and when you walk away from the plinth carrying the Lance with her beside you:
*"the relic is safe at last. I may finally...rest..."*

**And the garrison can tell who you brought.** In the Burial Chamber, four checks turn her against
a player who cuts down her own knights -- and all four read a checker that is switched on two maps
away, so they have never once been true. You could kill the men she has held a door with for two
centuries, in front of her, and she would keep following you.

## What the Council sees

The Spirit Council's answer to *"Who do you think I am?"* was always about the player's soul --
*"that which has no soul, save one borrowed from another, which was taken from yet another at the
point of a sword"* -- and it said it in one voice to all three kinds of Scion. Now it says which:
the inherited crowd that cannot be put down, the beast that cannot hold a promise, or the thing
made by the same trade that made this crypt. And when it begs you to lift the curse, it can see
whom it is begging.

## Also

Carries the one regression 0.15.0's review pass introduced: Farshad's two "Welcome into the Order
of Saladin" greetings were opening for any Saladin member instead of an initiated one, because a
`Saladin Favored` gate was repointed after searching only vanilla for a can **this project itself
added in 0.9.0.**

## Installing

Download, unzip, run `Mod Manager.bat`. It installs over any earlier release. Almost everything in
this release is level parts -- the camp, the forward post, the traps, the levers, the corridor
voices: **they need a character who has not yet entered the Crypt.** The dialogue works on any
save.
