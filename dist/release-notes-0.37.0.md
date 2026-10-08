# Lionheart Fixt 0.37.0 - A Rock Titan of Your Own

If you've ever played a Tribal summoner, you'll know the ceiling: a wolf. A slightly better wolf. A
slightly better wolf than that. And then nothing, forever, no matter how high you pushed the skill.

That's because **the top two tiers of Monster Summoning were finished and then never connected to
anything.**

## Six creatures that were already in the box

The original game contains six summonable creatures that nothing in it can summon:

| | |
|---|---|
| **Snake Woman** | 90 HP |
| **Ogre** | 120 HP |
| **Wererat Boss** | 90 HP |
| **Rock Titan** | **170 HP** |
| **Desert Beast** | 120 HP |
| **Sand Spirit** | 120 HP |

They aren't half-built. Each has its own stat sheet and its own working model. Someone made them,
grouped them into two tiers, and then the spell was never pointed at them.

## Now the ladder goes all the way up

| your skill | what answers |
|---|---|
| under 50 | a guard dog or a wolf |
| 50 – 99 | tougher versions of the same |
| 100 – 149 | the toughest wolves — **unchanged**, this was the old ceiling |
| **150 – 199** | **a snake woman, an ogre, or a wererat boss** |
| **200 and up** | **a Rock Titan, a desert beast, or a sand spirit** |

The thresholds follow the game's own spacing — it already stepped at 50 and 100, so this continues at
150 and 200.

**Multi-summoning benefits too:** its high-tier pool went from 3 possible creatures to 9.

## They still cost you

Each tier of summon drains your mana while the creature is alive. I built the two new tiers by
**copying the existing top tier and changing only which creature it calls** — specifically so the
upkeep machinery came across untouched rather than being rebuilt from scratch.

A Rock Titan that was free to maintain would have been the obvious way to get this wrong. It drains
at the same rate as a guard dog: both new tiers verified at 3 mana.

## One thing you'll notice, and it isn't new

**Your Rock Titan is called a Black Wolf.**

All six of these creatures were given the display name "Black Wolf" in the original game — copied from
the wolf summon and never changed. It's a leftover from whoever built them, and it's the same kind of
fingerprint as the Templar helm in the last release still carrying a shield's artwork.

I've left it alone deliberately rather than quietly renaming six things in a release that's meant to
be about wiring. If you'd like them named properly, that's a small follow-up.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Works on **any save** — this changes a spell, not a map.

## If you play it

**The headline:** get Monster Summoning to 200 and cast it. Nothing above the wolf tier has ever
appeared in this game.

**The one that actually matters:** keep an eye on your mana while a high-tier summon is out. It must
drain, and at the same rate as a cheap summon. If a Rock Titan is free to keep, tell me — that means
the upkeep didn't survive the copy and I need to fix it.

**And a sanity check:** at skill 100–149 you should still get exactly the wolves you always did. That
tier's contents weren't changed, only capped. If they changed, I spliced the wrong thing.

Last question, and it's a judgement call I'd rather you made: **is a 170 HP Rock Titan too strong as a
summon?** The creature is the original game's own, but nobody has ever fought alongside one. If it
makes fights trivial, say so and I'll look at the tier threshold.
