# Lionheart Fixt 0.55.0 - no way out, no way in

Reported from play, by the same person who found the troll peace and the blacksmith's silver:

> During conversation you can give them 150 gold pieces to presumably avoid fighting with them, but
> we never now as game is unresponsive (metal gears icon in top left corner still spins and nothing
> happens). I waited for 30min for no result.

The spinning gears are the game holding your input while a scripted scene plays. Something has to
tell it the scene is over, and in this case nothing did. There is no timeout, so the thirty minutes
were never going to help, and I am sorry about them.

## This one is mine

The Cathar ambush has five ways out and only four of them released you.

The fifth was never meant to be a way out at all. The dialogue file does two unrelated jobs: it holds
the ambush, and it also holds a set of greetings and drunk-patron lines that the maps open directly,
with no scene running. The line you landed on by paying, "Welcome to town.", belongs to that second
group. In the original game it is what one of those three toughs says if you walk up and talk to him
afterwards. It correctly does nothing, because nothing is holding you when you simply greet someone.

Four releases ago I needed a peaceful ending for a Wielder character. That line read exactly like the
right destination, and nothing in the file pointed at it, so it looked like finished content nobody
had ever wired up. It was wired, just from a map rather than from a reply. Then the Templar scene you
used sent its payment reply to the same place.

**So there is no version of the original game where this hangs.** It is a misuse of a line that was
working fine.

## The fix, and the fix I nearly shipped instead

The greeting is left exactly as the original game wrote it. Both replies now reach a proper ending,
where the three toughs stand down and walk away, copied from the one peaceful ending that always
worked.

My first attempt put that ending onto the greeting itself. Twelve checks passed, because every one of
them tested the way out and not one asked what else used that line. Walking up to a tough to say
hello would have ended a scene that was not running, paid the encounter's experience again, and made
all three Cathars vanish. Repeatably.

What was missing was a single question: a map can open a conversation at any line, so "nothing in
this file points here" says nothing about whether a line is in use. One of this project's own tools
has known that for months. I did not ask it.

**Caught before shipping, and there is now an automatic check** so this class of mistake cannot reach
a release again. It catches the original bug and stays quiet on everything else.

## Then the new check made me look properly

Running the reachability gate honestly showed it had been failing for several releases on **seven
lines of this mod's own that nothing in the game can reach.** Two groups, needing opposite answers.

**Four taunts for the snakebreed summoners.** These creatures appear across eight maps in act two and
have been silent since the bark release, while four lines written for them sat unused. The reason is
a good one: every creature that got barks had a free slot in its attack script, and the summoners'
slot is already in use, for the summoning itself. Dropping a taunt in beside it would have made them
summon less often.

So the taunts are hung **inside** the summoning instead, which is what they were written for:

> Come, my brood. Come.
>
> `<It calls, and the dark answers>`

They now speak exactly when they call, and how often they summon is unchanged. I checked that against
the original files rather than trusting myself: rate, clone count, skill choices and animations are
identical in all three.

**Three drafts of the same report, deleted.** An early, terser version of the crypt-war status report
was left behind when a later release wrote a better one and gave it to the knight at the fire. His
version is the one you have been hearing. The drafts were duplicates nothing could reach.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

**The Cathar fix works on the save you are playing now**, since it is a conversation change. If you
are the person who filed this, you do not need to start over. The summoner taunts are creature
changes, so they apply to summoners that appear after installing.

## If you play it

Pay the Cathars and make sure you get control back. That is the whole report.

Then one deliberate non-event worth confirming: after any peaceful ending, walk up to a Cathar tough
and talk to him. He should say "Welcome to town." and **nothing else should happen.** No experience,
nobody vanishing. That line is supposed to be inert, and making it inert again is half of this
release.

And if you have an older save, compare how often a snakebreed summoner calls for help. It should be
exactly as before. If summoning feels rarer, I put the taunt in the wrong place.
