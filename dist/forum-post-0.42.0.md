# Lionheart Fixt 0.42.0 - what Andre had to say about it

Last release let you betray the rock titan guarding the road into Montaillou. It didn't let him
answer.

He had two answers recorded, and you could never hear either.

## He has opinions

**If you simply told the mayor:**

> *"You are a very, very bad man and you lead a trite and meaningless existence. Now leave me
> alone."*

**If you took his hush money first and then told the mayor anyway:**

> *"I paid you your blood money and still you betray me! I have had all I can stand from you,
> runt!"*

And then he attacks you.

That fight was written into the original game. A rock titan who has decided he's done with you,
standing on the only road into town. **It has never once happened** — the line it hangs off was
unreachable, so the attack never fired.

## A different fault from last time

Last release's six silent lines were a *filename* problem: the recordings and the conversations
disagreed about how to spell this character's name, so they never found each other.

These two aren't that. **Their filenames were always correct.** They were silent because nothing in
the game could reach them. Same symptom, completely different cause — renaming would have achieved
nothing here, and only rewiring helps.

That's the whole reason the order mattered. Three of last release's renames were done, undone, and
only redone once the wiring made them reachable.

## The bit I nearly broke

Betraying him now triggers these lines — but last release added a *different* line for betrayers who
had already finished the titan hunt (*"I think our dealings are at an end, fleshling"*).

If I'd checked only for betrayal, that line would have been shadowed and last release's work quietly
undone. The new checks are ordered so both survive:

- took his money **and** betrayed him → he fights you
- betrayed him, hunt unfinished → the brush-off
- betrayed him, hunt finished → last release's dismissal
- loyal → everything exactly as it always was

**That's the thing I'd most like confirmed**, because it's the kind of mistake that doesn't show up
until someone plays the whole sequence.

**This one branch now accounts for 1.05 MB of recorded voice acting across eight lines** that the
game you bought could never play.

## And one thing I decided *not* to do

There's an orphaned conversation on the Barcelona blacksmith that looks exactly like these: no way
in, a recording sitting beside it under a slightly wrong name. I was ready to fix it.

It turned out to be an **early draft**. The game already has a better version of that same
conversation — more options, including one for handing in an item a quest actually needs. Wiring the
old one would have duplicated a working menu and quietly dropped a quest step.

So it stays dead, and I wrote down why. Not every disconnected thing is a loss; some of it was
replaced on purpose, and this is the second time this month I nearly "restored" something the
developers had deliberately moved past.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Works on **any save**, but the betrayal is recorded when you talk to the mayor — so a save that has
already finished this questline won't show the new reactions.

## If you play it

**The one to try:** accept his gold, then go tell the mayor, then walk back to him. He should be
furious, you should hear it, and he should attack.

**The one that matters more:** betray him, then finish the Toulouse titans, then return. He should
give you the short, cold dismissal — *not* the longer brush-off. If you get the brush-off, I've
broken last release and need to know straight away.

**And the control:** keep his secret, and check nothing about him has changed at all.
