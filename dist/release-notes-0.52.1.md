# Lionheart Fixt 0.52.1 - the two barks that landed in the same place

A repair, reported from play right after 0.52.0: *an attack bark and a wounded bark sometimes play
over each other.*

0.52.0 didn't cause this. It made it easier to see, by thinning the chatter that was covering it up.

## What was wrong

A bark floats above the creature's head at a fixed offset. That offset was never varied by which
occasion triggered it — and the **twelve** creatures that bark on *both* occasions used **the same
offset for both**.

So a goblin that finished a swing and got wounded a moment later drew two balloons at exactly the
same point, one on top of the other.

It's the whole goblin set: the three Mongol Goblin tiers, the three Archers, the three Shamans, the
village Archer and the two Butu goblins. Every other creature that barks only barks on one occasion,
so it can't collide with itself — which is why this showed up where it did.

## What it is now

The wounded bark sits **forty higher**. Vanilla uses that exact value thirty-one times itself, so
there's established room up there.

That fixes it under both readings of the report — two balloons from *one* goblin landing on each
other, and two balloons from *two* goblins standing close together, since the two occasions now sit
at different heights whoever's head they're over.

168 balloons across 12 files, and **the change contains nothing but that one number.** Frequencies,
the lines themselves, and which spells each creature casts are all untouched.

## Being straight about the limit

**Both barks still happen.** They're readable and stacked now instead of piled up, but it's still two
lines at once.

Making one of them stay quiet while the other is showing needs a short-lived marker that the second
occasion can check for — and that's the same problem that stopped me building the better fix in
0.52.0. The original game never does it, so there's no working example to copy. If stacked-but-legible
still reads as too much, that's worth telling me, because it changes what's worth doing next.

## One note on how I got here

I went looking in the executable to confirm which direction "higher" is, and **didn't find it there** —
the trail ends in setup code, not the part that draws anything.

What actually answers it is the shipped game: goblins sit at 60, while humans, trolls and the
snake-folk all sit at 70. That's compensating for height, and it only works one way round — if the
number counted *downward*, the shorter creature would need the bigger one, not the smaller.

So I'm confident, but it's reasoning from the original game's own values rather than something I read
in the engine. **If the wounded bark turns up inside the goblin instead of above it, that's why**, and
it's a one-character fix.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Works on **any save**.

## If you play it

**The check:** fight one goblin and trade blows until you see both kinds of bark close together. Both
should be readable, with the wounded line clearly higher.

**The one that would mean I got it backwards:** the wounded bark should be **above** the goblin, not
inside it or below it. See the note above.

**And the judgement call:** is readable-but-stacked good enough, or does two at once still feel like
too much?
