# Lionheart Fixt 0.49.0 - the two wands that were only a description

There are three unique wands tucked away in their own folder in this game. One of them works.

The other two have a name, an icon, a rarity, and a paragraph telling you exactly what they do — sat
on top of nothing at all. No spell, no bonus, no effect. `Fire and Ice` is even worth **zero gold**,
which is how you can tell nobody ever finished it.

## What they were supposed to be

> **Fire and Ice** — *"This wand has the ability to cast Fireball at Skill level 10 and Ice Storm at
> Skill level 10 at the same time in the same place. It also confers 15% Fire and Cold Resistance."*

> **The Mage** — *"This will give 4 skill points in all base magic skills that the player possesses
> in all 3 spell categories. In addition, the item gives the player the ability to cast Lightning
> Bolt 5 times (at skill level 20), Fear 5 times (at skill level 20) and confers 10% Fire, Cold and
> Electrical Resistances."*

Both now do all of that.

## Fire and Ice casts two spells, which nothing else in this game does

Every working wand in Lionheart casts exactly one spell. And no single spell in the game deals both
fire *and* cold damage — so "at the same time in the same place" couldn't be delivered by pointing at
something that already existed.

So it carries **two** spell behaviours, Fireball and Ice Storm, sharing a pool of five to ten
charges, plus the 15% fire and cold resistance while it's in your hand. It's also no longer worth
nothing: 8,500, the middle of the price range the item already had written into it.

**That's the part most likely to go wrong**, and it's the one thing I'd ask you to check. If only one
of the two spells shows up, the approach doesn't work and that wand needs rebuilding.

## The Mage is a genuine artifact

Five Lightning Bolts, five castings of Fear, 10% resistance to fire, cold and electricity — and **+4
to all twelve base magic skills**: four in each of the three schools.

That's a lot, and it's deliberate. For comparison, the Sceptre of Bone — a major quest item — gives
+2 to eight of those skills. This gives +4 to all twelve. It's also the most expensive wand in the
game at 10,000 gold, and it's called *The Mage*.

**I'd genuinely like to know if it's too strong.** It was chosen on paper, by comparing it to what
else exists, and it has never been felt in play.

## I'd written down two things about these that were wrong

My own notes said these should be left alone, because *"The Mage as described — +4 to every magic
skill, in a game where the best single enchantment gives +8 to one skill — would be the strongest
item in Lionheart by a wide margin."*

**There's no +8 ceiling.** A shipped enchantment called Spikes Major gives **+25** to a spell skill.
Others give +20 and +15. So the thing I'd used to rule this out didn't exist.

The notes also said these wands had "nothing but text" and would need inventing from scratch. They
didn't — the working wand beside them is a complete, copyable pattern. What was actually missing was a
*decision* about how strong The Mage should be, not a mechanism.

## And copying the working wand turned up a bug in it

The Swarm raises your skill with the spell it casts. It does that by subtracting your skill from 30 —
which is fine if you're a novice, and **actively harmful if you're not**. A caster whose skill is
already above 30 gets a *negative* bonus from it. The wand quietly makes them worse.

Both new wands guard against that: they lift you to the stated level only if you're below it, and do
nothing otherwise.

**I've left Swarm alone.** Changing an item that shipped two releases ago is a separate decision from
building two new ones, and I'd rather raise it than silently alter it.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Works on **any save**. These are loot, so they appear in magic wand drops from here on.

## If you play it

**These are rare on purpose** — unique, at the lowest weighting, in a pool of eighteen. Hunting them
honestly will take a while. The Playtest Kit is the sensible way to see them.

**The check that matters:** select Fire and Ice and see whether you can cast **both** Fireball and
Ice Storm from it.

**The judgement call:** put The Mage on a caster, look at the twelve skills it touches, and tell me
whether that's an artifact or an exploit.

**And the one that would be easy to miss:** take Fire and Ice to a character who's *already good* at
Fireball, and make sure the wand doesn't make them worse. That's the bug I found in Swarm, and the
reason these two are built differently.
