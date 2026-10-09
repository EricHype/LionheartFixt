# Lionheart Fixt 0.46.0 - the creatures sent after Machiavelli

There's a quest in act 1 where Machiavelli hires you to guard his house. It works. It has his
dialogue, an ambush that fires when you leave, a reward when you save him, and a callback much later
in Montaillou where he repays the favour.

The four creatures that attack him were never given any stats.

## What was wrong

Every monster in this game gets its hit points, armour class and weapon skill from a `Race` file.
All four attackers pointed at **`Races/Demokin`** — which is one of the *player* races, the one you
pick at character creation. It contains starting attribute ranges and nothing else: no hit points,
no armour class, no skills.

So they turned up with none of those things. And you could actually see it, because that race has a
display name — the creatures attacking Machiavelli were **labelled "Demokin"** on screen.

Three monster cans out of 478 point at a player race. This is the only one of the three that the
game actually spawns.

## What they were supposed to be

The can is named `Assassin Machiavelli`, which fooled me twice. It doesn't mean Machiavelli is an
assassin — it means *the assassins sent after him*. And they aren't assassins either. The game says
so, twice, in his own dialogue:

> *"Those were **creatures** sent by the infidel assassins from the East"*

> *"you must tell me about those **creatures**"*

Creatures *sent by* the assassins. And the can's model is the snake-woman used by the twelve
Snakebreed creatures that appear elsewhere in the game. So that's what they are.

This mattered. If I'd trusted the name over the model and the script, I'd have made them assassins —
roughly twice as tough as what they should be, in an act-1 house.

## The ambush now

| | |
|---|---|
| nearest the door | a **larger leader**, tougher than the rest |
| two in the middle | standard snake-women |
| farthest back | one that **spits venom at range** instead of closing |

**This isn't a difficulty increase for its own sake.** Act-1 Barcelona enemies run to a median of
around AC 125 / HP 43, and there are already creatures in act 1 tougher than any of these four. They
were simply the only ones in the area with nothing at all.

They also all talk now, the leader included — it was the only one in the group that couldn't.

## The part that actually needed fixing

Machiavelli has **35 hit points**. He is not protected the way the children and DaVinci are. He's a
breakable man standing in the middle of a four-way ambush.

And the quest was available the moment you first walked in.

That's why this one has a reputation for killing you or failing — not because the attackers were
dangerous, but because *he* is fragile and nothing stopped you taking the job at level 2. Giving the
creatures real stats without addressing that would have made it worse.

**So he won't hire you below level 5 now.** And he says why, rather than just not offering:

> *"Then we are both honest today, which is rarer than courage. A guardian who falls in the first
> moment buys me nothing but company in the grave. Harden yourself a while longer and return to me —
> my enemies have been patient this long, and so, it seems, must I be."*

**The quest is delayed, never taken away.** Every one of his return greetings still leads back to
the offer, so you come back at level 5 and it's waiting.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Works on **any save**, with one catch: the attackers only change for a save that hasn't already been
inside the House of Ilk, because the game remembers what was in a place the first time you went
there. The level gate works on any save.

## If you play it

**The check that matters, and it's two halves:** below level 5, Machiavelli should not offer you the
job, and you should get a new line about not being ready. Then at level 5, come back — the offer
should be there again. **Both halves matter.** If the offer is missing at level 5 too, then the level
check isn't working and I need to know.

**The judgement call:** level 5 was picked by comparing the creatures against what else act 1 throws
at you. It hasn't been proven in play. If Machiavelli still dies on you when you're fighting well,
the gate is too low and should go up.

**And watch the one at the back:** it attacks at range. See whether it can get at Machiavelli past
you — that's the only genuinely new threat here.
