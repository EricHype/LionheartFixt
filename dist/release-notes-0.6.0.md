**Read this first: this is barely a played build.**

The rescue at the heart of it has been played, and works. Almost nothing else in this
release has been. The perk in particular rests on a mechanism **no perk in the shipped
game uses**, and if the engine ignores it the perk will simply do nothing. If you would
rather wait for a build that has been walked end to end, wait.

That warning is not boilerplate, and this project has earned it. While building 0.5,
four separate defects passed every automated check here -- correct parse, byte-identical
round-trip, every validator rule, verified deployment -- and were visible only in the
running game. Two more turned up in this release the same way: a rescue that worked but
looked like a teleport, and a ninety-second timer that silently never ran.

## The Port District had a fourth companion, and nothing could reach him

`Distressed Sailor.DialogTree` is Fernand Desoto: 31 nodes, **17 of them unreachable**,
and the unreachable half is the entire success branch. Node `80 companion` runs a real
`CSetCompanionAction` -- the same call that makes Cervantes, Cortes and Fang follow you,
and those three are the only companions in the shipped game. The map side is finished
too: a 14KB relay named `fernand joins you` that swaps his AI and gives him companion
banter, *"Where you go, I follow."*

None of it fires. The node the whole branch hangs off, `1 return after saving juan`, is
**defined once and referenced nowhere in the game**.

It is unreachable because his brother Juan cannot be saved. The trigger on the body plays
"he is dead" unconditionally, and the quest ships with two states, neither of them a
success. You get 150 XP for reporting a death, and that is the whole quest.

But the rescue was written. Juan has a thanks node and *"Mi hermano! You saved me!"*.
Fernand has `20 still breathing` and `30 saved juan`. And when you take the job he hands
you a potion of healing -- *"you might need it against those creatures"* -- while a
requirement file called `Player has a potion of healing.can` sits in the same folder,
checking for exactly that, referenced by nothing.

**Now it is wired.** Reach Juan with a potion and he can be saved. He is not dead when you
arrive; he is dying, and you have 45 seconds. Pour the potion into him and he gets up --
the same man, playing a get-up animation, not a fresh copy spawned where the corpse was.
Then he walks home to the ship, and Fernand can be told, paid, and asked to come with you.

Being late has a cost. If the clock runs out he dies for good, and the quest falls back to
the vanilla ending: report the death, take the shipped 150 XP and 100 gold.

## Also in it

**The Duke's murder now leaves a crime scene.** Blow up the Duke of Medina and a guard
already runs in shouting -- but the game deletes both him and the body two seconds later
and fades out, so the written aftermath had nowhere to happen. Two guards now hold the
scene afterwards and will tell you to move along, and what happened here.

**The fish monger buys skulls properly.** Selling him a vodyanoi skull took your skull,
paid your gold, and then ended the conversation mid-sentence; his acknowledgement was
written and unreachable. He now says it, and you can sell him another without starting
over. A reply of his that promised other questions and delivered a closed conversation is
fixed too.

**Brendan Michael Sullivan will tell you where he is from.** The Irish sailor in the
tavern has a whole answer about Ireland having *"sank some three hundred years ago during
the troubled times"* -- and no reply anywhere led to it. The missing line was sitting in an
unused duplicate of his dialogue. It is his own text, put back.

**Something for the skulls.** There is a reward for selling the fish monger a great many
vodyanoi skulls. It is not hinted, nothing tracks it, and it is not written down here.

## Installing

Download, unzip, run `Mod Manager.bat`. It finds a GOG, Steam or retail install by itself
and `Uninstall` puts everything back. Install over 0.5.1 as normal.

**This one needs a character who has never entered the Port District.** Dialogue is read
fresh every time you talk to someone, but map contents are captured into your save the
first time you enter a level, and this release adds entities to the Port District. On a
save that has already been there, Juan cannot be saved and the crime scene stays empty.

## If you play it

There are no QA cases for any of this yet, deliberately -- they should describe what play
shows rather than what the build intends. The four things most worth watching:

1. **The rescue.** Take the job, keep the potion, click the body. He should stand up, not
   appear.
2. **Arriving without a potion, or too late.** Should be indistinguishable from vanilla,
   and the log should not call him dead until he is.
3. **Recruiting Fernand.** The companion machinery has never run for this character.
4. **Whether leaving the map stops the clock.** Unknown. It may pause, resume, or be lost,
   and which one decides whether fetching a potion is a real option.

`docs/releases.md` has the full working notes, including what was deliberately left out
and why -- most notably a Cortes branch that looks like cut content and is a superseded
draft that would drop you into the middle of his quest.
