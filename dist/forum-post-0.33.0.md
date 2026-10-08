# Lionheart Fixt 0.33.0 - The Priest Heals

A question from play: *"are there any enemy healers? I've never seen that."*

You never saw one because there are none. In the entire shipped game, across all **478** enemy
definitions, here is every spell or attack any enemy has ever been able to choose:

- a melee swing
- Lightning Bolt, Spike, Fire Orb, Static Charge, Ice Javelin, Ice Missile
- Celestial Smite
- a defensive shield, on six priests

Eight ways to hurt you, one way to protect themselves, and nothing else. Nothing heals. Nothing
cures. No enemy in Lionheart has ever put a hit point back on another enemy.

Now one does.

## Why there were none

Not an engine limitation. The game's own Healing spell is blocked from enemies by **two** things, and
the second is the interesting one.

The first is a single category check: the spell asks whether its target is "the player or a friend of
the player," and heals only if the answer is yes. Its area effect actually sweeps up *everyone*
standing nearby — that one test is the only thing deciding who benefits.

The second would have made a healer that cast and healed nothing. The amount healed scales off **the
caster's own Healing skill**, and explicitly returns **zero** if the caster has none. An enemy has
none. Remove the gate alone and you get a priest who makes the gesture and achieves nothing.

## The game already showed how to do it

There is exactly one enemy version of a player spell in Lionheart: the English Priests' shield. Laid
side by side with the player's version of the same spell, it gives the whole recipe — five changes,
including an **always-false requirement** so the spell can never appear in your own skill list.

That detail answered something I'd otherwise have guessed at. The Priest casts that shield *despite*
it being flagged as impossible to cast, which proves enemies bypass those restrictions entirely.

So `ENEMY Healing` follows the same recipe, with one deliberate improvement: the shield's authors left
its numbers pointing at the player's version of the spell, where they read as zero. These point at
their own, so the Priest heals **11–18 hit points**, up to twice a cast.

## What carries it

The Priest was already built for this and nobody noticed. His routine is: **shield himself once, then
pick at random from three attack spells, forever.** The heal is simply a **fourth option in that
pick** — so roughly one cast in four, and nothing else about him changes.

**Only the ordinary Priest has it.** The tougher two are deliberately left alone until someone
confirms this works. One priest to prove it; five more can follow.

His heal reaches **200 feet**, and of the 24 places a Priest is placed in this game, **17 have a
soldier within that range** — Gate District at 57, Temple District at 84, Crossroads to England at 40.
In the other seven he can only reach himself.

## What this is actually for

Every enemy in Lionheart does the same thing until it dies or you do. There is no retreating, no
regrouping, no calling for help — I checked, and the game contains no mechanism for any of it.

A healer is the one thing that changes that without needing any of it. Not because the priest behaves
cleverly, but because **you** have to: kill him first, or out-pace him. That is a decision you did not
have to make before.

## And no, enemies still cannot drink potions

Asked at the same time. They can't, and it isn't an oversight — there is **no "use an item" action
anywhere in the game**, for anyone. An item's effect is welded to the item and fires from your
inventory screen; nothing an enemy does can reach it. Enemies don't even carry potions. The only items
they have are the ones they drop when they die.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

This one works on **any save** — it changes a character and a spell, not a map, so you don't need a
fresh game.

## If you play it

**Please do this one first.** Start a new game and fight something ordinary — the thugs in the Port
District are fine. This release adds a **93rd spell to a game that shipped with 92**, and while
everything says that's safe, nobody has ever done it. If enemies act strangely or the game won't load,
that's why, and it comes straight back out. Five minutes here protects the rest of your playthrough.

**Then the one that matters:** find a Priest fighting alongside soldiers, wound a soldier, don't kill
it, and watch. Its health should go back up. That has never happened in this game before.

**And a safety check:** cast your own Healing with enemies nearby. It must still heal only you and
your friends. The original spell wasn't touched and I verified that in the shipped files — but if your
heal is topping up enemies, stop and tell me immediately.

Last, the interesting one: fight the same priest-and-soldiers encounter twice. Once ignoring him, once
killing him first. If killing him first is clearly better, then this worked.
