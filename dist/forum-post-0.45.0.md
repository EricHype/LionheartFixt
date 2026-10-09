# Lionheart Fixt 0.45.0 - Alvaro's horse

There is a horse in this game. It has a model, it has a cached render, it has an idle animation, a
walking animation, a death animation, and somebody sat down and recorded the sound it makes when it
dies.

It appears in **no maps at all**. Not one. It has been sitting in the files since 2003, finished, and
nobody ever put it anywhere.

## What it was for

The animation list tells you. Idle, Walk, Death — and nothing else. No attack, no flinch, no run.

Compare the war golems, which have ten animations including two separate attacks. The horse was never
meant to fight anything. It was meant to stand somewhere and be looked at, like the deer and the
chickens in Montaillou.

Except those got placed:

| | appears in |
|---|---|
| grey wolves | 16 maps |
| deer | 5 maps |
| chickens | 3 maps each |
| **the horse** | **none** |

## Where it is now

The Crossroads, next to **Alvaro**, the merchant who stands out there selling to anyone passing
between Barcelona and the wilderness. It's his. It pulls his cart.

And if you take a swing at it, he is not philosophical about it:

> *"Away from her! She has pulled my cart these nine years and you raise a hand to her?"*

Then he comes for you, and you've lost your merchant.

That part isn't invented either — the map already had everything needed to make him hostile, because
the game already handles you robbing him. I just gave it a second reason to fire, with a line that
fits the actual offence. **Robbing him still gets the original reaction**, where he runs off to the
guard captain shouting "Thief!"

## Two things I left alone on purpose

**There's no cart.** The cart art exists, but **no map in the entire game places one**, which means
the path to it has never been tested by anybody. I'm not putting an untested model into a map to
decorate a joke — if it silently failed to load you'd get an invisible nothing and no error. The cart
is in what he says instead.

**The horse may fight back badly.** It has no attack animation, so if you hit it and it tries to
retaliate, it'll probably look stiff. I could have stripped its combat behaviour out, but nothing in
the original game does that to a creature, and I'd rather ship it behaving like itself than invent a
pattern the engine has never been asked to do.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Works on **any save** — but a save that has already visited the Crossroads won't have the horse,
because the game remembers what was in a place the first time you went there.

## If you play it

**The check that matters:** go to the Crossroads and look. Is there a horse standing near Alvaro, on
the ground, not hovering and not sunk into the dirt? Everything else is decoration if that's wrong,
and placing things in maps is the part of this mod I trust least.

**The fun one:** hit it once and see what he does.

**And listen for it:** if you kill the horse, you should hear a sound no player of this game has ever
heard.
