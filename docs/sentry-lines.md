# Two replies for the Grove Sentry

For review. Nothing is in the tree.

These are about the complaint in [issue #11](https://github.com/EricHype/LionheartFixt/issues/11)
that the peaceful route *derails the story* -- that an assassin invites you in, you simply accept,
and it reads as the player character behaving stupidly. The route itself is not the problem and
nothing here changes it.

---

## The gap

Mixxer5 says the route runs *"completely against directions you were given by a guildmaster"*. It
does not. All three patrons send you to look, not to fight:

| who | what they say |
|---|---|
| Lord Javier | *"travel to Montserrat at once and see what has happened"* |
| Cedric Alsen | *"travel to the abbey and see what you can discover"* |
| Jafar | *"travel with all speed to Montserrat to see if our enemies have stolen the Crown of Thorns"* |

Surrendering to be taken to whoever is in charge is a direct way to carry out that brief. **The
problem is that the game never lets the player say so.** Here is every way through `1 halt`:

| reply | gate | what it gives the player |
|---|---|---|
| *"I am. Take me to your captain."* | none | bare compliance, no stated reason |
| *"I am, and I was told to come as I am. Armed..."* | Outwit 6 | a bluff |
| *"Look at me. Do I look like one of theirs?"* | Demokin or Sylvant | a racial out |
| *"I am not. <Draw.>"* | none | the fight |

A deceptive character gets a line. A Demokin or Sylvant gets a line. **Everyone else's only way in
is four words of compliance with no reason attached**, which is exactly why it reads as a lapse
rather than a decision. Mixxer5 conceded the deceptive case unprompted -- that is the one path that
already has a voice.

And nowhere can the player say the obvious thing: that this is a trap.

## His register, so you can hold me to it

Measured off his five lines and seven existing replies:

| | |
|---|---|
| sentence shape | short declaratives, orders last. Three of his five lines end on *"Walk."* |
| contractions | **none, anywhere in the tree.** Same as Sahar |
| what he is | a guard with narrow orders, not a zealot. *"it is your neck and not mine"* |
| how he treats the player | as freight to be moved. He never threatens personally; others do it for him |
| length | his lines 12 to 31 words; player replies 2 to 25 |

---

## Reply 1 -- the player states the brief

The missing plain option. No skill gate, no race gate: this is the one a straightforward character
has been lacking, and its absence is the whole complaint.

### node id: 1 halt -- new reply

> I came to learn what happened to this house. Your captain knows. Take me to them.

16 words. Goes to `10 steel`, exactly as the existing compliance reply does, so the disarm beat is
unchanged. No icon, because it is neither a skill line nor a fight line.

It claims nothing the player cannot know standing at that gate, and it names no patron, so it is
true whether Javier, Cedric or Jafar sent them. *"Them"* also keeps the captain ungendered, which
the player has no way to know yet -- the sentry says only *"the captain"*, and her *"she"* does not
arrive until `20 armed`.

---

## Reply 2 -- the player names the trap

So that walking in is a thing the character does with their eyes open. The point is not that the
sentry reassures them. It is that he does not.

### node id: 1 halt -- new reply

> This is a trap, but I suppose I have no choice. You have your orders, I have mine.

18 words. Goes to the new node below. Yours, not mine.

My draft was *"This is a trap. Take me to your captain anyway."* -- flat, and it worked, but the
only idea in it was the word *anyway*. The one before that was *"Your people killed the knights at
this gate. Now I walk in on my own feet. I know what that is."*, which reached for an echo of his
*"come up the road on their own feet"* and let the echo do the work the meaning should have done.

**"You have your orders, I have mine" is the clause that earns the scene.** It says the player is
executing a brief rather than submitting, which is the whole answer to the complaint, and it turns
`15 seen` from a shrug into a reply: the player invokes orders, and the sentry confirms his are
narrow and incurious. The two lines now work as a pair rather than as a statement and a response.

One tension worth knowing about, since it is a judgement call and not a defect: *"I suppose I have
no choice"* says the player is compelled, while *"I have mine"* says the player is acting on
purpose, and the second is the stronger idea. If you ever want it sharper, cutting the middle
clause gives *"This is a trap. You have your orders, I have mine."* at 12 words. Left as written.

### new node: 15 seen

> I was told to bring you up alive. That is the whole of my orders, and I do not ask after the rest.

23 words, inside his 12 to 31. He does not deny it, does not soften it, and does not engage with the
drama, which is more in character than a retort and funnier for being flat.

Two replies, mirroring `10 steel` so there is still a way out:

| reply | goes to | icon |
|---|---|---|
| *"Then let us go."* | `10 steel` | none |
| *"I have changed my mind."* | ends, fires `sentry draws` | Fight, default reply |

---

## What does not change

- No mechanics. Both new replies reach `deliver` through `10 steel`, the path the existing
  compliance reply already takes.
- No existing line is edited. Two replies and one node are added.
- No route is removed, and no route is made easier. The fight is still one click away at every
  step, and `Default Canceled Node Action` still fires `sentry draws` if the player walks off.

## Why two and not three

A third line gated on faith, or on the Crown, would overlap Reply 1 -- the brief is the reason, and
Reply 1 states it. The clever path already has the Outwit bluff. And a reply keyed to Sir Tomas's
journal is impossible here: his body lies at (2730,705), past the gate, so the player cannot have
read it yet.

Say the word if you want the third anyway and I will measure one.
