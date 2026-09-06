# Lionheart Fixt 0.8.0 - the Gate District remainder

Leonardo DaVinci asks you to recover a spirit gem the Inquisition confiscated. When you find
out where it is, he has a node that answers you -- and that node is the root of a live branch,
three nodes deep, holding the choice of whether to cross the Inquisition on his behalf.

No reply in the game leads to it. The quest state that would gate such a reply is set, by two
different sources. One missing player line is the whole reason that choice never comes up.

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt: it fixes
what is broken, restores what was cut, and adds new content only where the game plainly ran
out.

This is the smallest release the project has shipped, and the last one for the Gate District.

## The branch that decided nothing

Weng Choi has a greeting for a player who has given him the book: *"Welcome back spirit bearer,
how can Weng Choi help one of his most valued customers?"*

His shop was built to use it. There is a conditional on his greeting, it checks the right
thing, and **both of its outcomes open the same node** - so that line could never fire, no
matter what you did for him. One destination was wrong. It is the same shape as 0.7.0's Ways
Crystal: the branch exists, the check works, and it decides nothing.

## Four smaller ones

**A third way to stop Merchant Lope overcharging you.** He inflates his prices for a tainted
player, and vanilla lets you intimidate him or beat him on Barter. A Perception route was
written - a two-node haggle ending in the honest inventory - and offered from nowhere. It is
now on all three nodes the other two approaches are on.

**The goblin sapper has a name.** *"I am Hrubjub of the Goblin Horde, on a secret mission to
serve my goblin lord."* You could not ask.

**Two people who greeted you as a stranger forever.** The Temple gate guard has a return
conversation with nine replies in it, and his second meeting opened his first-meeting node
instead. Same bug on a Temple District citizen. Third and fourth time this exact shape has
turned up - 0.3.0 found the first on Farshad.

## The district is finished

The Gate District had 53 unreachable nodes carrying written replies. 0.3.0 and 0.7.0 took the
narrative out of it - the Knights of Saladin were the whole story there. This release works
through the remainder and then stops: 42 orphaned replies down to 34, with the surviving 34
individually accounted for.

None of them is a cut quest. Twelve are in three dead trees no map opens anywhere, plus two
nodes the authors named `10 Don't use this node`. Six are alternate Dream Djinni trial variants
the game chooses between. Five are superseded drafts, four of which were read for this release
and deliberately left alone - the Blacksmith's big orphaned turn-in hub pays nothing a
reachable node does not already pay, and Weng Choi's dialogue-based scroll purchase was
replaced by simply stocking the scroll in his shop. Two are duplicates that 0.7.0's own summit
work replaced. The rest are flavour barks and nodes that would need conditions the files do not
contain.

There is no further list. That is as much the point of the release as the fixes are.

## Before you install

**This is unplayed, and so is 0.7.0.** If you would rather wait for a build somebody has walked
end to end, wait - four defects in 0.5 passed every automated check this project has and showed
up only in the running game.

That said, this one is small: one field changed in three places, four new player replies, no
quest logic touched anywhere. **Two of the fixes land outside the Gate District** - the citizen
is in Temple District, and DaVinci's tree is shared with Montaillou content. A level's contents
are captured into your save the first time you walk into it, so this wants a character who has
not already been through those districts.

Download, unzip, run `Mod Manager.bat`. It finds a GOG, Steam or retail install by itself,
`Uninstall` puts everything back, and it installs over 0.7.0 as normal.
