**Read this first. This is a small release, and it is unplayed like the two before it.**

Nothing in 0.8.0 has been played, and neither has 0.7.0. If you are waiting for a build
somebody has walked end to end, keep waiting -- that warning is not boilerplate. Four
separate defects in 0.5 passed every automated check this project has and were visible only
in the running game, and two more did the same in 0.6.

What is different here is the size. 0.7.0 rewired a late-game promotion for every faction
combination; 0.8.0 changes one field in three places, adds four player replies, and touches
no quest logic anywhere. It is the smallest release this project has shipped. If you install
it, install it because you want the Gate District tidy, not because something was broken.

## What this is

The Gate District had 53 unreachable dialogue nodes carrying written replies. 0.3.0 and 0.7.0
took the narrative finds out of it -- the Knights of Saladin were the whole story there, and
0.7.0 spent them. This release works through everything that was left, and then stops.

**The district is finished.** It goes from 42 orphaned replies to 34, and the surviving 34 are
individually accounted for in `docs/releases.md`. None of them is a cut quest. Twelve are in
three dead trees no map opens and two nodes the authors themselves named `10 Don't use this
node`; six are alternate Dream Djinni trial variants the game chooses between; five are
superseded drafts; two are duplicates that 0.7.0's own summit work replaced; the rest are
flavour barks and nodes that would need invented conditions.

That last part is the point of the release as much as the fixes are. There is no further list.

## The one real restoration

**DaVinci's spirit gem is with the Inquisition, and you could not say so.** DaVinci sends you
to retrieve a gem the Inquisition confiscated. The quest state is set, by two different
sources. He has a node that responds to being told where it is -- and it is the root of a live
sub-branch, three nodes deep, containing the choice of whether to cross the Inquisition for
him.

No reply led to it. One player line restores the branch and the choice with it. The gate is
the shipped quest state, not something invented for this.

## The branch that collapsed to one outcome

Weng Choi has a greeting for a player who has given him the book: *"Welcome back spirit
bearer, how can Weng Choi help one of his most valued customers?"*

His shop was built to use it. There is a conditional on the greeting, it checks the right
thing, and **both of its outcomes open the same node** -- so the special-customer line could
never fire, no matter what you did for him. Only the destination of one arm was wrong. It is
the same shape as 0.7.0's Ways Crystal: the branch exists, the check works, and it decides
nothing.

## Four smaller ones

**A third way to stop Merchant Lope overcharging you.** He inflates his prices for a tainted
player, and vanilla offers two ways out: intimidate him, or beat him on Barter. A Perception
route was written -- a two-node haggle ending in the honest inventory -- and offered from
nowhere. It is now on all three nodes the other two approaches are on. The threshold is a
choice rather than a discovery, and `docs/releases.md` says why `PE 7+` and not another.

**The goblin sapper has a name.** *"I am Hrubjub of the Goblin Horde, on a secret mission to
serve my goblin lord."* You could not ask.

**Two guards and citizens who greeted you as a stranger forever.** The Temple gate guard has
a return conversation with nine replies in it, and his second meeting opened his first-meeting
node instead. Same bug on a Temple District citizen. This is the third and fourth time this
exact shape has turned up -- 0.3.0 found the first on Farshad.

## Ruled out, with reasons

Four candidates were read and deliberately left alone, which is most of the work in a release
like this. The Blacksmith's big orphaned turn-in hub pays nothing a reachable node does not
pay, so wiring it would have created a second way to be paid for the same two quests. Weng
Choi's dialogue-based scroll purchase was replaced by simply stocking the scroll in his shop,
which works today. A "wizard" return greeting is character-for-character identical to the
insulted one. And a repeat-beg brush-off is offered from eight parent nodes, which is eight
gated variants for two lines of dialogue.

`docs/releases.md` carries the evidence for each, including two intermediate readings of mine
that were wrong and how the correct test differs.

## Installing

Download, unzip, run `Mod Manager.bat`. It finds a GOG, Steam or retail install by itself,
`Uninstall` puts everything back, and it installs over 0.7.0 as normal.

**Two of these fixes land outside the Gate District** -- the citizen is in Temple District, and
DaVinci's tree is shared with Montaillou content -- so the blast radius is slightly wider than
the name suggests. Map contents are captured into your save the first time you enter a level,
so this wants a character who has not already been through those districts.

## If you play it

No QA cases, deliberately: they should describe what play shows rather than what the build
intends. In rough order of how much rests on each:

1. **Tell DaVinci his gem is with the Inquisitor**, once the errand is active. That branch is
   the only content in this release a player could notice missing.
2. **Give Weng Choi the book, leave, come back.** He should greet you as a valued customer.
3. **Haggle with Lope on a tainted character** with Perception 7 or better.
4. **Talk to the Temple gate guard twice.**

But the honest recommendation is the same one `docs/releases.md` has carried for two releases:
0.6.0 is unplayed past the rescue and 0.7.0 is unplayed entirely, and one of 0.7.0's changes
affects a late-game promotion for every faction combination. Playing those is worth more than
playing this.
