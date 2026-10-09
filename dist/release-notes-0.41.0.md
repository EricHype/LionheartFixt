# Lionheart Fixt 0.41.0 - the betrayal nobody could trigger

The rock titan blocking the road into Montaillou tells you his name is Andre. It isn't. He's
**Lucius**, he ran from his own tribe, and he's been hiding in the village pretending to protect it
from the very titans he's afraid of.

He'll ask you to keep his secret. He'll ask you to go to Toulouse and kill the elders who exiled
him. He'll pay you to stay quiet.

Or you can walk up the hill and tell the mayor.

**Telling the mayor has done nothing at all since 2003.** This release makes it matter.

## What was broken

When the mayor finds out, the game tries to set a marker recording that you betrayed Lucius.

**That marker was never put in the game.** The instruction fires into empty air. So the flag could
never be set, and everything that depended on it — Lucius's reaction, Brother Michel's reaction,
the different ending to his quest — was unreachable content.

The developers knew. The mayor's line still carries a note to themselves, left in the shipped game:

> *"work in progress — kick luscious out, seal of this branch"*

They never came back to it.

## What you can now do

**Betray him and then finish his dirty work anyway.** Bring him the four stone hearts after you've
told the mayor, and he knows:

> *"I've heard that you exposed me to the mayor despite the agreement we reached. I'll thank you for
> taking care of the problem for me, but you'll get not one more ounce of gold from me. Good day."*

**Face Brother Michel.** He is not impressed:

> *"Lucius, despite his flaws, was a harmless, lonely soul. Your meddling has cast him out of the
> only home he is likely ever to have. I have nothing to say to you."*

And if you go back a second time, he has even less to say.

## And a fix that helps you even if you're loyal

In the original game, **every** post-quest conversation with Andre used his bitter line — *"I think
our dealings are at an end, fleshling"* — whether you'd betrayed him or not. Keep his secret, do
everything he asked, and he'd still treat you like a traitor.

Now that line is reserved for people who earned it.

## 0.88 MB of voice acting you have never heard

Here's the part I didn't expect.

The game finds a character's recorded speech by matching the audio filename to the conversation's
internal name. There's no backup method — if the two don't match exactly, **the line is silent
forever.** No error, no warning, just a character whose mouth moves in silence.

Six recordings were in that state, and the cause is almost funny: **this one titan's name is
spelled eight different ways** across the game's files. Andre, Lucius, Lucious, Marcus, and more.
The voice actor recorded "Lucious". The conversation says "Lucius". So the files never found each
other.

Two of those recordings are nearly 300 KB — these are real speeches, not grunts. Fully performed,
sitting in the game you own, never once played. They play now.

One of them isn't even his: a Shylocke line in Barcelona was silent for the same reason.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Works on **any save**, but the betrayal flag is set when you talk to the mayor — so if you've
already finished this questline on a save, you won't see the new branches on it.

## If you play it

**The check that proves it:** tell the mayor about Lucius, kill the Toulouse titans, then bring
Andre the four hearts. He must call you out for it — and you must *hear* him do it. If the words
appear but there's no voice, the audio fix didn't take and I need to know.

**The check that matters more:** do it all **without** betraying him. He must be warm with you at
the end. If he gives you the cold shoulder, I've made it worse than the original and that needs
pulling immediately.

**Still missing, and I know:** Lucius has two angrier greetings for when you've betrayed him that
are still unreachable. They need a different and larger repair, and I'd rather ship what's
verified than guess.
