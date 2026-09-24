**Read this first.** Nothing in this release has been played, and neither has 0.13.0 or 0.12.0
before it. Every change passes the automated gate and the build log in `docs/releases.md` says
what each piece was read against. If you would rather wait for a build somebody has walked, wait
for 0.14.1.

## Montaillou

A Cathar village of a hundred souls with an Inquisitor sitting in it, writing down what everyone
eats on a Friday. It is the second-largest act in the game and it had the largest block of
finished, unreachable writing the project has found: **49 dialogue nodes carrying player replies
that nothing in the game could open.** That is now 22, and 16 of those are one scene deliberately
written twice.

**The gate.** The Templar knights stop you on the road in and ask your business, in the scene the
act shipped and never opened -- and it reads the orders the project has spent five releases
making real: the Inquisition, the Templars (with a line for a woman), the Knights of Saladin, a
relic-hunter, a trader, or *"My business is my own"*, which gets you told what the town is under
investigation for. It was never wired because three of its answers pointed at nodes that do not
exist; those are repaired.

**Toulouse.** The rock titans camped at the ruin want the fugitive who was their Memnos, and the
game offers two ways to settle it: kill him, or trick him into walking back to them -- a route
Lethos advertises in live dialogue and that the game could not deliver, because the four nodes
that finish it are flagged `[REMOVED FROM GAME]` in their own text. Both halves were written.
Now the titans can be talked into hearing him out, he can be persuaded or tricked into going, and
the army leaves Toulouse exactly as it does when you bring them his heart.

**Na Roqua.** The witch in the woods answers a sworn Inquisitor as one; remembers the chicken she
turned back into the mayor's wife; offers her secret stash of *"items of power"* to a friend of
the Cathars; and can be told to her face what the seer says she used to be.

**The village.** The Bishop of Pamiers offers his third lead and his service to the tainted.
Andre's corpse scene and his deeper first-meeting menu are reachable. The Cathar Warden stops
demanding to know what you saw from strangers who saw nothing. Maury names the man in the square
who is not to be trusted. And Lethos finally tells anyone to go and speak to Rhea, which his own
conversation has always assumed you did.

**Then the village learns to read you.** Montaillou checked a faction fifty-five times and never
once asked about a perk, a spirit, or anything you did outside the Church's world. Now the
square's mugger recognises one of Juanita's guild and stands down; the gate knights have
something to say to a man wearing the Goblin Khan's honours into a Templar garrison; the Bishop,
reciting his ninety-eight cases of heresy, can be told by a necromancer that he has missed one;
the Cathar toughs hear an Inquisitor's confession and a Wielder's reason; the Inquisition's agent
explains his plate of meat to a brother; a villager looks a tainted face in the eye and does not
step back; Aidan gives a trader the peace price; and the shepherd admits what he is watching when
he says the Bishop's name.

## Installing

Download, unzip, run `Mod Manager.bat`. It installs over any earlier release. The gate challenge,
the warden and Na Roqua's greetings are level parts: **they need a character who has not entered
Montaillou.** The rest is dialogue and works on any save that has not already passed those
conversations.
