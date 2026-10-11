# Lionheart Fixt 0.53.0 - the peace you brokered

Reported from play, and the report came with its own verdict:

> After peaceful resolution of Lava Troll quest lines, when decided to kill them for XP, only
> targeted troll is fighting back, rest is idle. You can pick them one by one in this way - too easy.

That's exactly right, and it had been true since the troll peace shipped.

## Why only one troll fought back

Nothing was broken. It was three correct mechanisms adding up to a hole.

Making peace with the trolls empties the list of things each troll is willing to treat as a target.
A pacified troll standing six feet from a murder isn't ignoring it — it genuinely cannot see it as
something to attack. The one you hit *does* fight back, because every creature in this game hits
back when struck personally, and that's a separate path that doesn't consult the list at all.

And there is no "call for help" in Lionheart. Not disabled, not broken — it doesn't exist. The
action is sitting there in the executable, used **zero** times in the whole shipped game, while 698
creatures are flagged to respond to a call nobody ever makes.

So the pit was an eighty-troll experience farm, killed one at a time, at no risk.

## The guard that turned out to be the hole

The alarm that would have covered this *did* exist. I wrote it four releases ago — hit a troll and
its chief comes — and then deliberately switched it off while the peace held, so that an accidental
swing couldn't blow a peace the player had worked for.

My own QA notes recorded that as a **passing** test: "no alarm at all." It was the second time in
three releases I'd written a test from the implementation instead of from play, which means it could
only ever agree with itself. The protection was real and it was worth less than the exploit it
opened. Nothing happening is now a **failure**.

## What happens instead

**The chief comes, and he names what you spent.** There are three versions of the scene, picked by
how much of your own word went into the peace:

| if you had | he answers with |
|---|---|
| stood the rite over the chief who came before him | *"I told you a chief must be counted by one who was not there."* |
| carried his ore terms up to the smith | *"The same man each time. So we know the face."* |
| argued their case to the man paying to have them killed | *"Tell the men who sent you that we counted every time... There are none."* |

That last one is the one most people will get, and it's the one the writing is aimed at. The usual
way to make this peace is to tell the chief his quarrel is with the men above, not with the child
they sent down to steal his ore. He gives you that back.

**There's no talking out of it.** One reply, no persuasion check, no second chance. Speech is what
you spent — it isn't also the exit.

**Then the pit becomes a pit again.** Not a stampede: the trolls get their hostility back and notice
you the ordinary way, at the range they always had. The ones near you come. The far side of the pit
waits until you go to it. I'd built the version where all ninety charge at once, measured it, and
thrown it away four releases ago; this is the thing in between.

## Two men ever find out

**Eduardo's ore trade dies with the chief.** It was secured by nothing but a troll's word and a face
they'd agreed to recognise, and he learns what happened the only way he can: the man he sent knocked
on the rock in daylight, three days running, and *"the dark has stopped answering."* You can admit
it or lie to him. Both are written. The lie is worse.

**Enrique pulled the contract because you talked him into it**, and then it happened anyway, for
free. He doesn't accuse you of anything:

> So either I am a fool who was talked out of his money, or I am something worse that I was talked
> into. I am not going to ask you which. I want you to understand that I could, and that I am not,
> and that those are two different things.

Nobody else ever knows. Nothing above ground changes. The pit going quiet is a quiet thing, and
that's deliberate.

## What didn't change

**You still don't have to do any of this.** The chief already hands you the Lava Troll Hide for
Quinn's errand if you make peace and stand his rite — so the peaceful route pays that quest in full,
and killing them is greed with nothing riding on it. The game now treats it as exactly that instead
of quietly rewarding it.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

**This one needs a character who hasn't been down to the Troll Pit yet.** A save records what's in a
map the first time you walk into it, so everything here is invisible on a save that has already been
there. A new game, or a character still above ground, will see it.

## If you play it

Make the peace, then swing on one of them, and the chief should be standing there. If nothing at all
happens, that's the bug this release is about and I got it wrong.

Then two things worth watching. **Count what comes at you** — it should be a handful, not the whole
level. And **let the fight run past half a minute**: nobody should quietly go back to standing around.
There's a timer in that map that re-pacifies the trolls every twenty-four seconds, and stopping it
first is the first thing the new code does. If a troll stops fighting and wanders off, that timer is
still running.
