# Lionheart Fixt 0.8.1 - repairs

Repair only, nothing new. Three fixes to earlier features, all found by playing them.

**Fernand's potion.** The rescue of his brother checked your pack for *a potion* -- the engine
cannot say "a healing potion" -- and took whatever it found first. One tester lost a Potion of
Master Thievery. Fernand now gives a named quest draught that the rescue checks for and nothing
else will do for; it cannot be drunk, so it cannot be lost by accident.

**Fernand's memory.** He thanked you for the rescue once and then asked, forever after, whether
you'd found his brother yet. Reporting back completes the quest, a completed quest has no current
state, and the flag meant to remember the rescue was nested inside a check that could never pass
again. His thank-you is now the greeting from then on -- and it is the greeting that lets him join
you, so a failed attempt can be retried.

**The troll at the far end.** Make peace with the lava trolls and the pit stands down -- except,
sometimes, one troll in the dead-end at the far left. Trolls spawn hostile and were pacified on a
two-second timer; one that spawns beside you can lock on inside that window, and nothing in the
game releases a locked target. Every generator now pacifies its troll the instant it spawns while
the peace holds. Refusing or breaking the peace works as before.

**The Helpful Wererat.** His conversation opened under the writers' working title, *"Wererats
Helpful Canned"*. He is now **Helpful Wererat**. And he stayed friendly after the other beggars
turned on you; he now turns with them.

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt.

## Before you install

All three fixes need a character who has **not yet entered** the Port District, the Troll Pit or
the Hall of Beggars respectively -- a level's scripts are captured into your save the first time
you walk in. A save that already holds Fernand's old potion cannot complete the rescue on this
build either.

Download, unzip, run `Mod Manager.bat`. It installs over 0.8.0 as normal.
