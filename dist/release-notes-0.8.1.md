**Repair only.** Three fixes to earlier features, found by playing them. Nothing new.

This is the first Fixt release in a while whose contents have a direct line to something a
player actually saw go wrong, and all three are the same kind of defect: content that was
byte-correct on disk and passed every automated check, and failed on a timing or state detail
that only the running game can show. That is the argument for playing the unplayed releases,
and it is why this one exists.

## The wrong bottle

Fernand gives you a healing potion for his brother. The rescue then checked your inventory for
*a potion* -- the engine's inventory check has no way to say "a healing potion", and any bottle
satisfied it. One tester lost a Potion of Master Thievery to a drowning sailor.

Fernand now gives **Fernand's Healing Draught**, a quest item that the rescue checks for by
name and nothing else will do for. It cannot be drunk, so it cannot be lost by accident either.

## Fernand forgets

Save Juan, report back, and Fernand thanked you. Talk to him again and he asked whether you'd
found his brother yet.

Reporting back completes the quest, and a completed quest has no current state -- the game
relies on exactly that elsewhere, to stop you claiming the same reward twice. The check that
was meant to remember the rescue sat *inside* the check for the quest's state, so it was never
consulted again. It is now the first thing he checks, and his thank-you is the greeting from
then on -- which is also the greeting that offers to let him join you, so a failed attempt at
that can be tried again.

## The troll that won the race

Make peace with the lava trolls and the whole pit stands down -- except, sometimes, one troll at
the far end.

Trolls spawn hostile and were pacified by a keeper on a two-second timer. A troll that spawns
right beside you, in the dead-end alcove at the far left of the pit, can lock onto you inside
those two seconds, and the game has no action that releases a target once locked. Every troll
generator now pacifies its troll at the instant it spawns, while the peace holds. The keeper
stays as a backstop, and refusing or breaking the peace works as before.

## The Helpful Wererat

Two small things. His conversation opened under the name *"Wererats Helpful Canned"* -- the
original writers' working title, which the game shows as the speaker. He is now **Helpful
Wererat**. And he stayed friendly after the rest of the beggars had turned on you; he now turns
with them, whether he was already standing there or arrives afterwards.

## Installing

Download, unzip, run `Mod Manager.bat`. It installs over 0.8.0 as normal.

**All three fixes need a character who has not yet entered the level in question** -- the Port
District, the Troll Pit, the Hall of Beggars -- because the game captures a level's scripts into
your save the first time you walk in. A save that already holds Fernand's old potion also cannot
complete the rescue on this build.
