# Lionheart Fixt 0.54.0 - one supply, one thing

Reported from play, by the same person who reported the troll peace. One issue with two halves, which
turned out to be the same questline:

> So, when you get back Eduardo's sword to him, you can ask him either to fashion shield for Knight
> Templar's quest or Scimitar for Saladin Order quest. (both dialog options are present, but after
> picking one, you end up with one item only, when you try to talk to him again, there is no option
> to ask for another). Since Order of Saladin is minor faction, player should be able to do quests
> for them without problems.

> Also, I have shard of dreams item in inventory without option to give it to Amir.

Both correct. Both have been true since the Saladin line was restored.

## First: are you even supposed to do both?

Worth settling before fixing anything, because if the two orders were meant to be alternatives then
this is a choice, not a bug. And there's real evidence for that reading — there is only **one** supply
of magnetized silver in the entire game, one shared errand to fetch it, and the internal names treat
the two quests as alternatives.

But the game says the opposite, out loud. Jafar tells you plainly that you cannot *join* his order —
you can only become what he calls a **Favored One** — and there's a whole scene whose only job is to
warn you that this will not satisfy DaVinci's demand that you join a faction, because the Knights of
Saladin lack the influence of the major ones.

So the Saladin tasks are built to be done *alongside* the Templars or the Inquisition. The reporter
worked that out from playing; the designers wrote it down. Whoever shared that silver was assuming
you'd only ever be on one of the two quests, and there's a clean reason nobody caught it: **the
scimitar was uncollectable in the original game.** Eduardo's half of it is finished and untouched —
every line, every step — but nothing in the shipped game could ever start it. The task was cut on
Jafar's side only. Nobody could reach the combination, so nobody hit the wall.

## The silver

Eduardo needs magnetized silver to forge either item. There is exactly one supply of it, in one chest
in a goblin-held mine, and it does not come back. The first commission consumes it — and **both**
commissions check that you're carrying it. So whichever order you served second was never served at
all, silently, with no hint that anything had gone wrong.

**He keeps the sweepings now.** Come back for the second piece and there's a new conversation:

> The silver, si. I used it. You brought me one supply and I made you one thing out of it, because one
> supply makes one thing. [...] There is a little left. Filings, the skin off the pour, what I swept up
> because I am not a man who sweeps silver into the fire.

He charges for the work rather than the metal, which he refuses to bill you for on the grounds that you
walked into a goblin mine to get it:

| | |
|---|---|
| **1000 gold** | flat |
| **600 gold** | if your Barter is good enough to argue him down |

It's meant to hurt a little. The first item was the reward for an errand; the second is a purchase.

**The original path is untouched** — byte for byte. If the first item behaves any differently than it
did last release, that's a bug and I want to hear about it.

## The Shard of Dreams

Jafar sets you one second task, and which one you get is a real either/or: the conversation that offers
it can only happen once. **That stays as it is** — it's how the scene was written, and the choice is the
point.

What doesn't stay is what happened to the relic. Take the scimitar task and the Shard quest can never
start — but the Shard is still sitting in the slavers' lair where anyone can pick it up. And **Jafar is
the only person in the game who will accept it.** It weighs nothing, it's worth nothing, it does
nothing. You just carry it forever.

He'll take it now, unasked, and he won't take it as a gift:

> I did not set you this task. I set you another and you took it, and that was yours to take, and I had
> made my peace with never holding this again. [...] So there was nothing in it for you. You carried it
> up out of there anyway.
>
> No. Not a gift. I will not have the Order take a sacred thing as a gift from someone who owes us
> nothing. Take it, and do not argue with an old man about his own customs.

Karma, and coin he presses on you. Less than the task would have paid, because you traded the task away
— you just aren't left holding a worthless stone. No quest appears in your log, and he doesn't send you
on to the trials you skipped.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

**Both fixes work on a save you're already playing** — they're conversation changes, not map changes. If
you're the person who filed this and you're currently carrying a dead Shard with one item you can't
collect, this release is aimed exactly at you and you don't need to start over.

## If you play it

Go back to Eduardo after collecting one of the two items. There should be a new line about the silver
being gone, and a price. Pay it and **check your purse** — the gold has to actually leave.

Then, if you took Jafar's scimitar task and have the Shard, go and see him. And one deliberate
non-event worth confirming: if you're carrying the Shard but *haven't* reached his fork yet, he should
**not** offer to take it. Handing it over early would let him send you to find something you'd already
given him, which would be a new dead end in place of the old one.
