# Lionheart Fixt 0.4.0 - Quinn's Reagents

There is a `Lava Troll Hide` in Lionheart's archive. It has a name, a description and
finished inventory art. Nothing in the shipped game drops it, asks for it, mentions it, or
places it anywhere. It is a quest item for a quest nobody wrote.

This release writes the quest.

**Fixt** is a restoration-and-repair mod, named after Fallout Fixt and following the same
discipline. It fixes what is broken, restores what was cut, and writes new content only
where the game plainly ran out.

**This is the first release that is mostly that third thing**, and it is worth saying so
plainly rather than letting it look like more restoration.

**Download:** https://github.com/EricHype/LionheartFixt/releases/latest
**Source:** https://github.com/EricHype/LionheartFixt (MIT)

---

## Three errands, three healing tiers

Quinn the herbalist in the Gate District wants three wolf pelts, then five wasp stingers,
then the hide of a lava troll. Each unlocks a tier of healing potion above vanilla's Extra
Healing, sold from a reserve he keeps under the counter.

The order is the point. The tiers are paced by **where each reagent lives**, not by a level
check, because the top tier is roughly four times Extra Healing and would ruin act 1 if it
turned up there. You will not see it until you are in the sewers.

Almost none of it needed inventing. The wasp stinger already exists and already drops -
from the Cursed and Tainted wasps only - and nothing in the game consumes one. The hide, as
above, existed and did nothing. The three potions were built already and were shipping into
a test map no player could reach.

## Three ways to get the hide

Vanilla wrote a diplomatic opening to the lava trolls and closed it. Every branch of their
only conversation ends in a fight or in leaving, and killing one turns the whole pit. So
this errand would have forced you to wipe out a people the game plainly means you to feel
something about.

Except the troll tells you his problem without being asked, and it is a practical one:

> Too many dead Trolls. Wererats sneaky.

He does not care how that stops. And the Beggars **are** the wererats. So: cure them and the
trolls will trade with you. Wipe them out and the trolls will trade with you. Or kill a Lava
Troll Boss and take it off him.

Good path, evil path, or no diplomacy at all. The top potion tier is never gated behind a
morality choice - and the peaceful route is deliberately not written as the merciful one,
because vanilla's own cure quest makes you kill the Prime Wererat for a patch of fur.

## A perk that locked you out of content

Every wolf in the game branches on whether you took **Wolf Trapper**. Without it you get one
plain pelt; with it, two better ones. The errand only accepted the plain kind - so the perk
handed you pelts your own quest would refuse. Either counts now.

---

## What 0.1 through 0.3 did, if you are new

The **goblins of the Wilderness** become a real faction with three accumulating ranks, and
the camp reads your standing. Two finished characters that shipped with complete dialogue
and zero map references are put back. The **Knights of Saladin** award you their rank
instead of only the title, which unlocks twenty replies across four acts that no player has
ever seen. The **Sacred Scimitar** questline - fully written, unstartable, broken at three
ends at once - can be started and finished.

The rule the whole project follows: **every check adds a route and none removes one.**

---

## What has not been tested

**None of 0.4.0 has been played.** Everything is verified against the built archive, which
proves every reference resolves and every file parses, and proves nothing about whether a
quest actually advances.

The previous release turned up four separate vanilla bugs the moment someone played it -
including a quest that could move backwards and a hand-in reachable from seventeen wrong
places. Treat this one the same way.

Most useful to report: the peaceful troll route appearing when the wererats are *not*
settled, the pelt errand refusing pelts, or any turn-in that takes your reagents without
advancing.

Issues: https://github.com/EricHype/LionheartFixt/issues
