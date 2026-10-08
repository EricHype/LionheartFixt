# Lionheart Fixt 0.35.0 - Caltrops

A question from play: *"do any enemies lay traps? Is that possible?"*

No, they never have. And yes, it turns out — because most of the machinery was already in the game,
just pointed the wrong way.

## What traps were

Every trap in Lionheart is a fixed part of a map — forty-four maps have them. Each sits invisible
until your Find Traps skill is good enough to spot it, after which you can disarm it. The damage
scales with how far into the game you are: 25-35 late, 15-25 in the middle, 10-20 early.

They are placed by the level designer and nothing in the game has ever created one while you played.

## But thirty-two enemies already carried one

This was the surprise. The **WarGolems** and some of the **Undead** — thirty-two types in all — walk
around inside their own hazard field. Stand next to a WarGolem and it burns you every couple of
seconds, because it has a trap attached to itself.

So an enemy with a damage field was never the hard part. The only thing missing was the ability to
**leave one behind**.

And that turned out to exist too: the game has a way to create something exactly where a character is
standing, and it already uses it seventy-three times.

## So the assassins and thieves scatter caltrops

**Forty-eight enemy types** — twelve assassins and all thirty-six ranks of thief, in both the city and
the sewers — now drop a patch of caltrops **once each**, the first time you wound them. A thief
scattering them to cover itself, which is what a thief would do.

The patch is **visible**. Walk through it and you take piercing damage, a bit over half what a real
map trap does, scaled to your progress the same way. Walk around it and nothing happens.

**That's the whole point.** Last release made you decide *who* to kill first. This one makes you think
about *where you're standing*. Nothing in this game has ever asked that before.

## You can see them, on purpose

I didn't hide these behind Find Traps, even though the machinery to do it was right there.

A map trap you have to find is fair — someone laid it in advance and you're walking into their
ground. A patch thrown down mid-fight that you can't see isn't a trap, it's just damage you have no
answer to. Visible means avoidable, and avoidable is what makes it a decision.

If you'd rather they were hidden, say so — it's a small change and the parts exist.

## Two things I checked before building

**They can't hurt anything but you.** Not other enemies, and — more importantly — **not your
companions**. The game's own traps only ever allow the player to set them off, and I copied that
exactly, then confirmed it in the finished files. A trap that killed Fernand would be a bad bug, so
please still check it.

**They outlive the enemy that laid them, then clean themselves up.** Kill a thief and its caltrops
still work. Step on them and they're gone.

## A fair warning

Forty-eight enemy types can lay these, so a crowded room — the Thieves Congregation, say — could end
up with five or six patches on the floor. Each one only fires once and then vanishes, so it should
sort itself out. But I haven't seen it, and if the floor becomes a mess I'd rather hear it than guess.
The fix would be a smaller radius or less damage, not fewer enemies carrying them.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Works on **any save** — this changes characters, not maps.

## If you play it

**The main one:** fight a thief or an assassin, wound it, and watch the floor. A patch should appear
at its feet. That has never happened in this game.

**The structural one:** keep hitting the same enemy. It must only ever lay **one**. If it carpets the
room, the mechanism is wrong and I need to know.

**The safety one:** walk a companion across a patch. It must not hurt them.

**And listen to the thieves** — their combat barks are the thing I broke and restored in the last
release, so if they've gone quiet that's where to look.

Still unplayed from two releases ago: the enemy healer. If you only have time for one thing, start a
new game and confirm nothing is strange in an ordinary fight — three releases of this now rest on
that check.
