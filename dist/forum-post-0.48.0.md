# Lionheart Fixt 0.48.0 - the English army fights back

Two earlier releases gave some English enemies a single clever trick: priests raise a shield once,
and veteran soldiers drink a healing draught once, when they're badly hurt.

It turns out the machinery behind that trick is completely general. Only the *thing it does* was
specific. So the rest of the English army gets one too — and each kind of soldier gets a different
one.

## What they do now

| | when | what happens |
|---|---|---|
| **Ordinary infantry** | the first time you wound one | closes ranks — harder to cut, crush or pierce |
| **Swordsmen and axemen** | below half health | fights with both hands — **stronger and faster** |
| **Archers** | the first time you wound one | steadies the draw — **sharper eye, faster shots** |
| **Priests and priestesses** | the first time you wound one | prays faster — **casts more quickly** |
| **War golems** | below 40% health | vents, rimes or arcs over — tougher against **its own element** |

Each one happens **once per creature**, and each one **wears off** after fifteen to twenty seconds.
That second part matters more than the first: these are windows you can wait out or push through,
not permanent upgrades you just have to absorb.

## Why two different triggers

The healing draught already fires when a soldier is nearly dead. If everything fired that way, every
English fight would have the same shape — a late-stage panic.

So the rank and file, the archers and the priests react to **being engaged at all**. They stiffen the
moment you reach them. The heavies and the golems react to **nearly dying**. One is a fight getting
harder as it starts, the other is a fight getting harder as it ends.

## The numbers aren't invented

Every value is scaled against something the original game already does:

- A shipped English weapon slows *you* by 0.03 per hit, against a base speed of about 1.0 — so a
  one-time +0.15 to +0.25 is a real step without being absurd.
- Enemy races are given around 15 points of damage resistance — so +12 to +20 roughly doubles it.
- The game's own strength perk is worth exactly +1 — so +2 is notable, not silly.

Each archetype gets exactly **one** buff. The twelve veteran soldiers that already drink a draught
get nothing new.

## The part I'd been unsure about, now settled

All of this — this release, and the two before it — rests on one assumption: that the "do this once"
machinery counts **per creature**, not once for the whole *type* of creature. If it counted per type,
the first soldier you wounded would use up the trick for every soldier in the game.

I'd written a test for it and never run it. **It's now answered without playing, by decompiling the
game.** The counter lives inside each copy of the action. Each creature carries its own copy. The
engine even offers "local copy" and "shared global instance" as two explicit alternatives, which
only makes sense because copying is the normal case.

And the clinching detail is in the game's own files: this exact pattern appears **350 times**,
including on monsters. The snake-woman summoner runs a one-shot summon sequence — and those arrive in
waves. If the count were shared, only the very first one in the game would ever summon anything.

So it works, and it has worked since 2003.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Works on **any save**, with the usual catch: creatures already spawned in a place you've visited
won't have the new behaviour. Somewhere you haven't been will.

## If you play it

**The one that proves it works:** hit any English soldier, archer, priest or golem and watch for an
effect flashing over its head. If that never happens for anything, nothing else here is worth
checking.

**The one I'd most want checked:** find a veteran soldier from the earlier release and wound it to
40%. It should **still drink and heal**, and should *not* do any of the new things. Those twelve were
meant to be left alone.

**The interesting one:** bring fire to a fire golem and keep using it after the golem flares. It's
supposed to get harder to burn specifically, not harder to hurt generally.

**And the judgement call:** does the army read as *reacting* to you, or as randomly getting stronger?
The two triggers were picked so that stiffening-on-contact and escalating-near-death feel like
different things. If you can't tell them apart in play, that's worth knowing — it means the triggers
need rethinking, not the numbers.
