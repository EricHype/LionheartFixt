# Lionheart Fixt 0.47.0 - the five titles nothing awarded

This game has thirteen **titles** — perks you can't choose at level-up, only earn. Things like
*Necromancer*, *Servant of the Queen*, *Goblin Champion*. They're written, they have descriptions,
and the game hands them out when you do something that deserves one.

**Five of them it never hands out at all.**

| | |
|---|---|
| **Goblin Slayer** | *"...slain a great number of goblins."* |
| **Enemy of the Inquisition** | *"You have slain an agent of the Inquisition."* |
| **Enemy of the Knights Templar** | *"You have slain a Knight Templar."* |
| **Enemy of the Wielders** | *"You have slain one of the Wielders of Barcelona."* |
| the Knights of Saladin equivalent | same shape |

You can do all of those things. You can kill inquisitors, Templars, Wielders and Knights of Saladin,
and you can kill a very great number of goblins. Nothing was ever watching.

## Goblin Slayer didn't need anything built

The game already counts your goblin kills, and already notices when you hit twelve — that's how the
Raylark bounty pays out and how the Savage Heart quest advances. **Ten** places across six files do
that arithmetic.

So the title is now awarded right there, in the same breath. No new counter, no new threshold, no
number I picked myself.

## The faction titles watch the victims, not the places

Those four factions have **707** places where a member can appear. Rather than touch all of them, the
hook goes on each *kind* of member — so one change covers everywhere that kind shows up. **33 kinds,
568 appearances.**

That part had a trap in it that this project has been bitten by before: some of these members are
spawned by machinery that *overwrites* whatever their death was supposed to do. Overwriting it back
would have broken things quietly. So the original action is **kept and the new one added beside it**,
which is why killing **Inquisitor Fournier** still fails his three quests *and* now marks you.

I then wrote a separate audit that walked all 568 appearances to check none of them was silently
dead. **It found two the first pass had missed**, because that pass only checked the first appearance
of each member in each map.

## The Saladin one was broken too, and I'd said otherwise

My own notes called the Saladin title "the working one" and treated it as the example to copy from.
**It doesn't work.** Its grant sits on a switch that is turned off, is one of thirty-four switches in
that map sharing the same name, and nothing anywhere turns it on.

So all four were dead, not three. It's now wired like its siblings — including through **Jafar**, who
turns out to be the faction's leader.

## Who counts as a member

Decided by looking at what things actually are, not what they're called. Corpse props, crypt undead,
an extraplanar jailer and the inquisitor from the slaver scene are all excluded.

So are the **rogue** inquisitors — a rogue has *left* the order, and the Grand Inquisitor has his own
dialogue about hunting them down. Killing one shouldn't make you the Inquisition's enemy. That's a
judgement call and I'd like to know if it reads wrong.

## And now people notice

Every one of the five gets answered. Each reaction sits on that faction's *ordinary member*
conversation, so it reaches all of them — and three of the four hang off a greeting that calls you a
friend, which is the whole point.

The Inquisition, from *"Greetings, child. How might I help you this day?"*:

> *"I know it, child. Your name is written in a ledger in the Temple District, beside a number, and
> the number is not small. ⟨He does not reach for a weapon.⟩ We are a patient order. We are also a
> very good one at arithmetic."*

The Templars — including on *"Well met, brother"*:

> *"Then I will not call you brother again, and that costs me more than I expected it to. We bury
> ours with their swords on their chests and their names read aloud. ⟨He does not look away.⟩ Yours
> were read. Go, before I learn which of my vows is the louder one."*

The Wielders — including on *"Welcome, fellow Wielder"*:

> *"We felt each one go out, like candles down a long hall. And still you walk in here and expect the
> passage to open. ⟨The cold in the room arrives, and stays.⟩ It will open. We have not finished
> counting, and the lost street keeps a long memory."*

The Knights of Saladin — including on *"Word of your deeds have come before you, brother"*:

> *"Salaam — and may God forgive what I say next to a guest. My brothers rode from Persia to guard a
> relic, not to be buried in a foreign street. I will not strike you while the truce holds. But do
> not come to our fire, do not take our bread, and do not call me brother where the others can hear
> you."*

And the goblins answer **Goblin Slayer** three ways. The villagers first — and every *other* thing a
goblin villager says to you is about eating you:

> *"You are the one from the vale. ⟨It does not offer to eat you.⟩ We have stopped counting. The young
> ones are told you are weather — a thing that happens to goblins, and cannot be fought."*

Then **Raylark**, who paid for it and is annoyed about the bounties he's no longer collecting. And
**the Khan**, but only if you're in the horde *and* have been slaughtering it:

> *"Both are true, and it troubles you far more than it troubles me. I did not raise you up to be
> gentle, morsel — I raised you to be useful."*

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Works on **any save**, with the usual catch: a member who has already been spawned in a place you've
already visited won't carry the new hook. Somewhere you haven't been yet will.

## If you play it

**Do this one even if you do nothing else:** kill Inquisitor Fournier in Montaillou's church while
one of his quests is active, and check that **his quests still fail**. If they stopped failing, I
broke something while adding to it — and that's the kind of break you'd never notice otherwise.

**The two halves:** kill twelve goblins and check your sheet for *Goblin Slayer*; kill one inquisitor
and check it for *Enemy of the Inquisition*.

**The best one to actually see:** anger the Templars or the Wielders *while being one of them*, then
go and talk to one.
