# Lionheart Fixt 0.52.0 - half as much shouting in a crowd

**This one exists because a playthrough asked for it.** Every release before it in this run came out
of a survey finding something missing. This one came out of someone playing the game and saying: the
barks are good, but when you're surrounded there are far too many of them.

They were right, and the reason is slightly more interesting than "the number was too high".

## Why crowds specifically

Enemies bark on two occasions: when one finishes an attack swing, and when one gets wounded. The
attack one fired on **one swing in four**.

That rate is **per creature**. One goblin barks every four swings. Six goblins swing six times as
often — so a group was producing barks faster than once per swing-round, while a single enemy was
perfectly reasonable. Nothing in the setup knew how many enemies were in the room.

## What changed

| | before | now |
|---|---|---|
| finishing an attack swing | 1 in 4 | **1 in 8** |
| being wounded | 1 in 6 | **1 in 6 — untouched** |

**The wounded one was deliberately left exactly as it shipped**, and that's half the point of this
release. It can't multiply with the crowd: you hit one creature at a time, so however many enemies
surround you, that rate is capped by *your* attack speed. It was never what made a crowded fight
loud. It's also the hook carrying the lines that answer something you just did, and leaving it is
what stops a one-on-one fight going silent while the crowded ones get quiet.

So — to be straight about it — **this isn't half the barks in every situation.** It's half the one
the crowd multiplies. In a mob, that's most of the noise. In a duel, much less changes, which is
intended, because duels weren't the complaint.

**No line was deleted and no bank was thinned.** Every bark written across the last twenty releases
is still in there, still picked at random from the same pool.

## The thing that nearly went wrong

The rate is set by padding, and the padding isn't inert — it's also what tells a creature which
attack to use next. This project has already shipped a bug from exactly that: twenty-one archers
once spent a release selecting a melee skill their race didn't have.

So the padding counts are a *distribution*. Three goblin shaman variants pad theirs in a ratio that
amounts to **one Spike for every two Static Charges** — that's their spell mix, written as a pad
count. Naively padding them out to the new number would have quietly turned them into Spike
specialists.

Every creature's padding was rebuilt by repeating its own existing pattern instead, so nothing's
attack selection moved. The shamans are the one exception to the new rate — they land on **1 in 7**
rather than 1 in 8, because the pad count is always the denominator *minus one*, and 7 doesn't
divide into their three-step pattern. Keeping their spell mix intact mattered more than a difference
you cannot perceive.

## The fix I wanted and didn't make

The genuinely correct version of this is a **shared cooldown** — one timer for the whole fight, so a
crowd barks at the same pace as a lone enemy instead of multiplying. That's better than halving,
because it fixes the actual cause rather than scaling around it.

Everything needed to build it exists and is used heavily by the original game. I didn't build it,
because of how it would fail: the cooldown has to be *released* when it expires, and the creature
holding it is most likely to die mid-fight — which is exactly when a bark cooldown is in use. If the
release doesn't survive its owner's death, the timer sticks on forever and **every combat bark in the
game goes permanently silent**, with nothing to indicate why.

The original game never does this, so there's no precedent to copy and no evidence it works. That's
answerable by digging into the executable, and until it's answered, halving is the version that
can't fail quietly.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Works on **any save**.

## If you play it

**The check that proves it:** get surrounded. A crowded fight should be noticeably quieter, and you
should rarely see two balloons up at once.

**The check that matters more:** barks should still *happen*. The way a rate cut goes wrong is by
cutting to zero. If you fight for several minutes across a few encounters and see no floating text at
all, that's a bug and not the new number, and I want to know immediately.

**Two smaller ones, if you're curious:** a goblin shaman should still cast both of its spells, with
Static Charge about twice as common as Spike; and archers should still be using their bows. Both of
those run through the same padding this release rewrote.

**And the judgement call:** if crowds are still loud, the attack number comes down again. If crowds
are right but the game overall now feels too quiet, the one to *raise* is the wounded one — it's
still at its original setting and it's the hook with the reactive lines on it.
