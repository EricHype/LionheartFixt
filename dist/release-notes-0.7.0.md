**Read this first. This one is unplayed, and it reaches further than the last.**

Nothing in this release has been played. That has been true of a Fixt release before, but
two things here are different, and you should know both before installing:

- It touches **four maps across Acts 1, 7 and 8** -- the first time this project has edited
  anything past Barcelona.
- **Two of its changes affect playthroughs that have nothing to do with the Knights of
  Saladin.** A late-game promotion now works differently for every faction combination, and
  the Cathedral summit now behaves differently for a player who serves no order at all.

If you would rather wait for a build somebody has walked end to end, wait. That warning is
not boilerplate: while building 0.5, four separate defects passed every automated check this
project has and were visible only in the running game, and two more did the same during 0.6.

## The Knights of Saladin could be joined and never served

0.3.0 got the player into the order. The Dream Djinni trials made you, in Amir's words, *"a
Favored One of the Knights of Saladin"*.

And then nothing. The order had no second rank, no errand, and no road out of Barcelona. It
was a title you collected and never used.

It turns out that was not the design. It was the wreckage of one.

## The road north

Three patrons send you to Montserrat -- Lord Javier, Cedric Alsen, Lord Relican -- and each
does it in plain conversation, marking the abbey on your map. Amir has the whole speech for
it. His own line reads:

> *"Montserrat Abbey lies some fifty miles to the northeast. **I shall mark the path on your
> map.** You must travel with all speed to Montserrat..."*

His node sets the quest and contains no map-marking action at all. The other three patrons
all have one. That single omission is why the Saladin route dead-ended, and it is now
repaired -- so Amir can send you north like anyone else, and follow it up when you return.

## The ranks

The order has three ranks written and costed: **Aswaran**, **Blessed**, **Exalted**. Vanilla
grants the last two in exactly one place in the entire game -- a developer test map.

They are increments, not alternatives, so a full ladder is the largest melee progression in
the game: **+29 one-handed, +29 two-handed, +50 carry weight**, and Turn Undead at the top,
which no other order gets. Blessed is now earned by serving the order; Exalted comes from
the Ways Crystal in the late acts, the same relic that crowns the Templars and the
Inquisition.

**And that fixes something 0.3.0 broke.** The crystal promotes whichever order you serve,
except its final branch was unguarded -- so it made a Knight of Saladin into a *Wielder*.
Nobody could be a Knight of Saladin in vanilla, so the fault lay dormant until 0.3.0 made
membership possible. Since that release, Fixt has been quietly converting Saladin knights
into Wielders in Act 7. It no longer does, and the crystal now honours **every** order you
have served rather than only the first it happens to check.

## The summit

The Knights Templar call a council in the Cathedral, and in the shipped game a Knight of
Saladin is not at it. Amir is spoken *to* in that scene and spoken *about* -- Lord Javier
delivers Amir's report on his behalf, in the third person, from a node still named for
Jafar.

The Cathedral map calls three relays that do not exist. Two of its dispatchers still route
to them, with Saladin as the default. A complete Knight of Saladin stands in that room,
placed and given dialogue, switched on by nothing.

Amir now summons you to the council himself, attends it, and speaks. And because those
dispatchers were already looking for the missing pieces, a player who serves **no** order --
who currently reaches two parts that were deleted, and gets a scene with no conversation and
no ending -- gets a working one for the first time.

## Installing

Download, unzip, run `Mod Manager.bat`. It finds a GOG, Steam or retail install by itself,
`Uninstall` puts everything back, and it installs over 0.6.0 as normal.

**This needs a character who joins the Knights of Saladin** -- the Dream Djinni trials, in
the Gate District. Map contents are captured into your save the first time you enter a level,
so the Cathedral work wants a character who has not already been there.

## If you play it

No QA cases yet, deliberately: they should describe what play shows rather than what the
build intends. In rough order of how much rests on each:

1. **Take Amir's directions and look at your world map.** Montserrat should appear. The
   whole road-north premise is that one check.
2. **The Ways Crystal**, in Act 7's Secret Chamber or Act 8's Shifting Dunes. This is the
   change that can affect a playthrough with no Saladin content in it at all, so it is worth
   testing as a Templar, as a Wielder, and as someone unaffiliated.
3. **The summit**, summoned by Amir. It is a cutscene, and 0.5 established that scripted
   sequences fail in ways no static check catches.
4. **Report back to Amir after Montserrat** -- he should promote you and send you to
   Montaillou.

`docs/releases.md` carries the full working notes, including what was deliberately left
alone and why. The short version: promotion has no dialogue because nobody ever wrote a line
granting a rank, and the order has no quests of its own after the initiation because none
exist in any form. Those are not oversights.
