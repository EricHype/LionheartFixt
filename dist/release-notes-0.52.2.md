# Lionheart Fixt 0.52.2 - what the wand actually does

A player found a wand whose description was nonsense and asked a fair question: how does a wand that
shoots lightning at someone *and* teaches them to find traps make any sense?

It doesn't. But the wand was never the problem — the writing was.

## What the description said

> ...as if using the thought spell lightning bolt at skill level **(Could not evaluate expression)**
>
> all physical attacks done by **the target** of this wand do **$i[damagebonus]** points of poison damage

Three things wrong there, all of them in the original game, in files this mod had never touched. Two
are fixed here.

## The one-character one

That `$` should be a `%`. Every substitution token in the game uses `%`, including the one sitting a
few words later in the same sentence — which is why the duration came out as "120 seconds" and the
damage came out as raw markup.

I checked all **286** of the game's item-addition files. It's the only one like it anywhere.

## The one that made the wand look mad

The description said **the target** gets the trapfinding bonus. It doesn't — **you** do.

Every single bonus in every wand in the game goes to the person holding it. And the original game
proves it in the same breath: the poison wand says the damage is dealt *by* one party *to* another,
using the two different names for wielder and target, so there's no ambiguity about which is which.

Nine wands in that same folder already say **"the wielder of this wand"** for the identical thing.
Two didn't. They do now.

**So here's what your wand was really doing all along:**

| | |
|---|---|
| Lightning Bolts | shoots lightning at an enemy |
| Revelation | gives **you** +60 trapfinding for 30 seconds |
| Poisonous Touch | makes **your** melee hits poison whatever you strike |

An adventurer's tool. It was described as if you point it at somebody to make *them* a better
trapfinder.

## What I left alone, deliberately

The two **Cure** wands also say "the target of this wand" — and for them that's **correct**. They
really do heal whoever you point them at. They're also the two that proved the rule, so leaving them
is the whole finding rather than an oversight.

**No mechanics changed in this release.** Both wands always worked properly. Only the words were
wrong.

## Still broken, on purpose

The **"(Could not evaluate expression)"** half is a third, deeper problem and it's still there.

Nine wands describe their power level by printing an *adjustment* instead of the level itself. With
nothing to measure against it fails outright; and even when it works it prints the wrong number for
anyone whose skill isn't zero — a level-5 wand would tell a skilled caster *"at skill level -15"*. At
zero skill the two happen to coincide, which is exactly how it shipped unnoticed.

Fixing it properly means rewriting nine descriptions, so it's a separate decision rather than
something to slip into a patch. **If you see it, it's known.**

## And a correction of my own

Chasing this turned up that something I claimed in 0.52.0's predecessor was wrong. I'd recorded one
wand as having a bug where it *reduces* a skilled caster's ability. It doesn't — it deliberately
**fixes** the casting level to a set number regardless of who's holding it, which is how all nine of
these wands work.

Which means the two wands I built in 0.49.0 don't follow that rule. They only ever raise your skill,
never pin it, so a strong caster gets more out of them than out of any other wand in the game. That's
a judgement call rather than a fault, and it's now written down as one instead of being dressed up as
a fix.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Works on **any save**.

## If you play it

**The checks:** a Poisonous Touch wand should show a real number for its poison damage, and both it
and Revelation should say **"the wielder"**.

**The check that matters more:** a **Cure** wand should *still* say "the target of this wand is
healed". If that one changed too, I was careless.

**And expect to still see** `(Could not evaluate expression)` on lightning, fireball, spike, slow,
poison ring and fire circle wands. That's the parked one, not a new one.
