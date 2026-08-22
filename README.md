# Lionheart Fixt

A cumulative restoration-and-repair mod for *Lionheart: Legacy of the Crusader*, named
after Fallout Fixt and following the same discipline: one mod, one install, and every
release visible in all three registers - **fix**, **restore**, **extend**.

Lionheart shipped as a strong RPG for one act and a combat corridor for seven. That is
measurable rather than merely felt: Barcelona holds 88 quests and the Crypt holds one,
while combat density rises 35x. Fixt repairs what is broken, restores what was cut, and
writes new content where the game simply ran out - working from the shipped archive rather
than from opinion.

**This repository is the mod.** Its root is the mod package: `mod.json`, `files/`, and the
documents that explain every decision in it.

| | |
|---|---|
| [`docs/design.md`](docs/design.md) | the diagnosis, measured, and the phase plan |
| [`docs/plan.md`](docs/plan.md) | the work, section by section and map by map |
| [`docs/releases.md`](docs/releases.md) | what ships, in what version, in what order |
| [`docs/qa.md`](docs/qa.md) | every case a release candidate has to pass |
| [`docs/playtest-guide/`](docs/playtest-guide/) | the same cases as a route to walk, built by `build.py` |
| [`dist/README.txt`](dist/README.txt) | what a player reads after unzipping a release |

**The tooling lives separately**, in
[LionheartModTools](https://github.com/EricHype/LionheartModTools) - the archive
packer, the resource-format parser, `modmanager.py`, the map editor and the
`lionheart-modding` skill. You need that repo checked out to build or install this one.
Fixt is content; the tools are tools.

## Current release candidate: 0.1.2-rc1

Release 0.1.0 is about the goblins. The pro-goblin thread in the Wilderness is the game's
most developed evil content and in vanilla it feeds nothing: no faction, no rank, no
standing, and a settlement that answers to almost nothing but Speech.

It carries three releases' worth of work: **0.1.0 "The Horde"**, below, **0.1.1 "The
Crossroads Patrol"**, and **0.1.2 "Standing"**, both described next.

**Not yet tested in-game, so this is a release candidate, not a release.** It is built,
deployed, and verified byte-identical in both `data.dat` and the loose `data\` mirror --
but nobody has played it. [`docs/qa.md`](docs/qa.md) is the checklist it has to pass
first, and it needs two differently-built characters to pass honestly.

### First meetings, and greetings that assume too much

Two bugs of the same shape, one found in play and one found by looking for its twin.

**The Goblin Girl greeted a stranger like an old friend.** Arriving having already killed
the River Dryad, she opened with `110 New Hero in town` -- *"I picked you a boquet of
snails, the really juicy kind!"* -- on first meeting. The greeting selector keyed purely on
world state and never asked whether she had met you. All three of her state greetings
presume acquaintance, and the shipped node names say so: `120 Player returns again after
killing dryad`, `200 Returning after killing the woodsman`. `1 First time PC enters
village` has to win regardless of what is dead in the wider world. It now does, via a
`Met the Goblin Girl` flag checked first and set *after* the greeting is chosen.

**The Khan could thank you for a gift you never gave him.** His Champion greeting says
*"The Everlasting hangs on my wall because you put it there"* and was conditioned only on
`Goblin Rank > 2`. That was safe while rank 3 could only come from handing him the
Everlasting, and stopped being safe the moment standing began accumulating -- spy, dryad
and eyes now reach rank 3 without him. It now requires rank 3 **and** the bounty-hunter
quest completed.

The general lesson, worth stating because it will recur: **a greeting keyed on a proxy for
an event rather than on the event itself will eventually greet the wrong person.** Both of
these were correct when written and became wrong when something else changed.

### 0.1.2 - the camp reacts to your standing

Rank had been earnable since 0.1.0 and read almost nowhere: four gates on
`Goblin Horde IS`, one on `Midlevel`, and **`Highlevel` referenced by nothing at all**. The
Khan has 41 nodes and calls the player *"morsel"* **17 times** -- including after they have
handed him the Everlasting and been named Champion of the Horde. Rakeb has 31 nodes and no
standing check. The villagers threaten to eat a man the Khan calls champion.

| Who | At what standing | What changes |
|---|---|---|
| **The Khan** | Champion | A different greeting at the cave mouth. *"Not 'morsel'. Not today. The Everlasting hangs on my wall because you put it there."* |
| **The Khan** | Champion | He stops shaking his own champion down for a poem at `11 Earn Goodbye` |
| **Rakeb** | Blooded | *"Clan. Yes. The bones have been saying so for a while and I have been pretending not to hear them."* No tourist's price |
| **Rakeb** | Champion | He is not sure the clan should be glad -- *"a human champion is a door left open, and doors are how weather gets in"* |
| **A villager** | Member | The spear comes down. *"Word travels, and your name has been in three mouths this week."* |
| **A villager** | Champion | The spear goes all the way down, and so does the goblin |

The villagers matter most, because they are what makes the *place* feel different rather
than one conversation: both of the threatening greetings -- *"You look like a walking meal
to me"* and the one accusing you of plotting -- now have a way out that is not Speech.

`Goblin Horde Highlevel` went from zero uses to five.

### 0.1.1 - the Crossroads patrol, and a contract on a Templar

In vanilla, asking Guard Esteban about the local dangers makes the goblin patrol attack --
no quest required, no way to talk to them, and no way back. The chain is
`30 Dangers` -> `500 goblins` -> `500 goblin continued`, which fires the `goblin encounter`
relay unconditionally.

**The relay was never the problem.** It force-generates the patrol, sets a route and fades
in the Patrol Leader, and contains no combat action at all. The hostility is in the
template: `Mongol Gate District` ships with `Valid Targets=Player,Player Friend` and
`Category=Enemy,Goblin`, so it aggroes on sight.

The proof of the fix is in Goblin Warrens, whose peaceful villagers spawn from *equally
hostile* templates. Two actions in the generator's `After Action` neutralise them at spawn
-- clear targeting, drop the `Enemy` category. **Five** Crossroads generators now do the
same, and the shared template is untouched, because it is used elsewhere. The sixth,
`Scout Generator`, already did it in vanilla; the Patrol Leader was never the aggressive
one.

**He was, however, unclickable.** `Scout Generator` shipped with a
`GetCloseThenTriggerAndFight` interaction specifier carrying an empty action, so the only
thing you could do to a peaceful patrol leader was swing at him. That specifier is removed
and the conversation takes its place. Combat still works: `CGoToCombatAction` converts
whatever specifier an entity holds into a fight one, which is how `goblins attack` reaches
him.

**The peaceful goblins also stopped offering a sword.** They kept vanilla's
`GetCloseThenTriggerAndFight` specifier, which is what draws the attack cursor -- correct
for an ambush, wrong for a patrol you can walk past. All five now use `GetCloseThenTalk`
with a balloon, the same treatment the Goblin Warrens villagers get, so hovering offers
speech and clicking gets a line of banter. Turn them hostile and `CGoToCombatAction`
converts the specifier back, so the cursor corrects itself.

`goblins attack` had to grow to match: it only ever re-armed `Goblin Scout` and
`Goblin Patrol Leader`, so with the corner goblins neutral it would have started a fight
against three statues. It now re-arms them too. **Attack the patrol and you still get the
vanilla fight** -- what changed is that you are no longer given it unasked.

**The Patrol Leader now talks.** He was balloon-only, which is why the counter-contract
could never have been written where the plan first put it: balloons have no reply list.
He is a real conversation now, with four state-based entry points, and he offers work:

| Check | What it opens |
|---|---|
| `Goblin Horde IS` | He recognises the human who carried word to the Khan |
| `Goblin Horde Midlevel` | The contract itself -- rank 2 only, see below |
| `Speech 40` | Talk your way past without fighting or dealing |
| `Outwit 7` | See why he needs a *human* hand: goblin spears on a Templar bring white cloaks, a human killer brings a manhunt for a human |

**Taking Esteban's own goblin contract closes this route, and that is the point.** His
`500 eliminate the goblins` reply fires the vanilla `goblin confrontation` relay, which
turns the patrol hostile -- you agreed to clear them out, so they stop being available to
talk to. Ask him about the dangers and the patrol appears peacefully; accept his job and
you have chosen. Both relays are fired from Esteban's tree and nowhere else, so the
sequence is entirely in the player's hands.

**Esteban has to be made killable first, and that took finding out why he wasn't.** He is
not invulnerable -- he is *jail-warded*, three times over, by machinery his generator
installs at spawn:

| Ward | Fires when |
|---|---|
| A `CHandleMessageAI` on the message `gotocombat` | **you attack him** -- this is the one that actually arrests you |
| His Damaged Action, *"if the instigator is a Player, trigger `Esteban Sends you to jail`"* | any damage reaches him |
| `Esteban hostile`, a 400-radius area manager | you cast a spell near him |

**All three are a guard rail, not a plot lock.** Esteban is not narratively load-bearing:
he never physically appears outside the Crossroads, in any later act or any ending. Act 6's
`Temple District Siege` mentions him only to fail his outstanding quests when Barcelona
falls -- it does not spawn him. What he *is* load-bearing for is one rung of the Knights
Templar initiation, and he stands alone in a wilderness crossroads where the player will
fight bandits, wasps and a goblin patrol. A stray area effect or a mis-click would have
silently destroyed that questline with no warning and no way back. Prison is the forgiving
alternative to a broken initiation.

That matters for whether lifting the wards is legitimate. It is: nothing downstream needs
him alive, and the case the rail exists to prevent -- killing him by accident -- is exactly
the case a deliberate contract is not.

**And he is built as a real fight, not a prop.** His template uses the `Knight Templar 5`
preset: **200 HP, 200 AC, one-handed melee 90** -- tougher than the Goblin Khan (210 HP,
175 AC, melee 60) and a shade under Joan of Arc. His template also carries
`Category=Spell Immunity`, so **magic cannot touch him at all**; he has to be killed with a
weapon.

The telling detail is that a `Guard Esteban.Race` exists at **10,000 HP and 1,000 AC** --
the statline Lionheart gives NPCs it genuinely never wants dead, shared by DaVinci, Lord
Javier, Sir Auric, the Grand Inquisitor and the Blacksmith -- and **his template does not
use it**. Somebody moved him off the unkillable preset onto a fightable one and protected
him with the jail instead. The contract is only finishing a thought the shipped data
already started.

**So the contract is gated on rank 2, and the Patrol Leader says why.** He would otherwise
offer it the moment you finished Hrubjub's errand in Barcelona -- around level 4 against a
man who needs level 9-12 to kill -- and accepting cost 50 karma up front for a quest you
could not finish and could not hand back. Rank 2 comes from Rakeb's eyes quest, deep in the
Wilderness, which is a natural level proxy and needed no new machinery.

He has three things to say to a Horde member, so the gate signposts rather than just
refusing:

| Your standing | What he tells you |
|---|---|
| Rank 1, never met the Khan | Go and stand in front of the Great Khan first, and come back along this road when you have |
| Rank 1, met the Khan | *"You have stood in front of the Khan and you are still only a chum. That tells me what he thought."* Do the shaman's work and earn a name |
| Rank 2, `Goblin Blooded` | The contract |

The middle one points at Rakeb without naming him, which is exactly where rank 2 comes
from. Knowing you have met the Khan needed a new flag, because everything his tree sets is
a map-entity activation on Goblin Warrens that the Crossroads cannot read; it is recorded
from his interaction specifier, which fires whenever you talk to him.

**Stripping them off the entity is not enough, and two failed attempts proved it.**
`RESET MAP for Invulnerable Esteban` is fired from *every spawn point on the map* -- ten of
them, including every road in. Its Per Party Spawn Action deletes Guard Esteban, clones the
generator to make a fresh one, and re-activates the jail relay. **Every entry to the
Crossroads restores a pristine, fully warded Esteban**, so anything removed from the live
entity is undone the next time you walk in.

So accepting the contract disables the two relay *entities* rather than chasing their
triggers. It does not matter how many things fire `Esteban Sends you to jail` if the relay
is inactive, and the reset cannot restore him if it is inactive too. The per-entity strips
stay as well, for the instance already standing there. Nothing about Esteban changes -- he still stands
there peacefully, and still defends himself only once you swing. What is removed is a guard
rail, in the one case it was never meant to cover: a deliberate contract on the man's life.
`RESET MAP for Invulnerable Esteban`, which deletes and re-clones him, is left alone; it
reads as post-jail cleanup, and if you are never jailed it never fires.

**The contract is on Esteban**, and everything it costs is paid at the corpse, not at the
handshake. Accepting costs 50 karma -- a decision you made, in your own head -- and
changes nothing about Esteban, because he was not there and has no way to know. Killing
him fails his two quests, fails the Templar initiation step he existed for, and costs
another 75 karma.

That timing is the shipped game's own grammar rather than a preference. Vanilla fails
quests on a *dialogue choice* when the choice is a public allegiance switch -- Cedric
Alsen's "Yes, I will join the Wielders" fails five quests at once, and the Inquisition
would obviously learn of it -- and on *death* when the giver is simply gone, as with
Shylocke, Cervantes, the Mayor, Andre the Titan and the Conspirator. A secret contract
whispered to a goblin on a road is the second shape.

Closing the Templar rung needed one subtlety. `LordJavier` requires
`Assist Sir Esteban at the Crossroads` to be at state `AIFBMSWX`, "return to Lord Javier" --
and quest **status** and **state** are independent axes, so failing the quest alone would
have left his check passing. Esteban's death rewinds the state to `F5BCFW6V`, *"You must
complete any tasks Sir Esteban asks of you"*, which is now impossible and says so in the
quest log.

One consequence worth knowing: the price scales with when you strike. Kill him early and
you lose his whole questline and the Templar rung. Do his work first and you keep what you
banked -- the initiation step is still voided, but you were paid for the tasks. Late
betrayal is cheaper than early betrayal, which is how betrayal usually works.

Nothing in the shipped game recorded Esteban's death, so 0.1.1 adds an `Esteban Dead` flag
set from his generator, which is what lets the Patrol Leader know to pay you.

### Fix - the goblin thread's dead ends

Four replies pointed at node IDs that do not exist. Choosing one advanced to nothing.

| Conversation | Reply | Went to | Now goes to |
|---|---|---|---|
| Hrubjub (`Goblin Sapper`), `20 ate a poet` | "I've heard enough. Goodbye." | `5 goobye` | `5 goodbye` |
| `Guard Esteban`, `50 Monsters` | "Goodbye." | `5 Goodbye` | `10 Goodbye` |
| Hrubjub, `30 goblin name` | same typo | `5 goobye` | `5 goodbye` -- **but see below** |
| `GoblinVillager`, `500 wilderness banter` | "My brain is far too porous and small for your tastes." | `100 avoid dinner` | `20 used speech to avoid digestion` -- **but see below** |

Esteban is included because a later release puts a contract on his head, and a man whose
farewell dead-ends is a poor advertisement. His other fifteen goodbye replies already
pointed at `10 Goodbye`; this was a one-character typo.

**Two of these four repairs cannot be observed in play, and that is worth stating plainly.**
Both fix genuine dangling targets, but the nodes containing them are unreachable in the
shipped game:

- `Goblin Sapper`'s `30 goblin name` has **zero inbound links** -- an orphan node in
  vanilla. Nothing can navigate to it, so its repaired reply never renders.
- `GoblinVillager`'s `500 wilderness banter` is fired **only as a balloon**, once, at the
  Crossroads. Balloons render an NPC's line with no reply list at all, so a repaired reply
  inside one is invisible. The node has no inbound links either, and none of
  `GoblinVillager`'s four conversation entry points can reach it.

They are kept because they are correct, cost nothing, and will work if a later release
gives either node a way in. They are not kept because you can see them.

### Extend - the Goblin Horde becomes a faction

Three rank records on the shipped `Saladin Aswaran` / Templar pattern, plus the rank
counter and the gates that read it.

| Rank | Faction | Earned by | Grants |
|---|---|---|---|
| 1 | `Goblin Chum` | Spying on Barcelona's gate for Hrubjub | Sneak +10, Poison resistance +10, carry weight +10 |
| 2 | `Goblin Blooded` | Bringing Rakeb the woodcutter's eyes | Sneak +8, Barter +8, Poison +10, Disease +10 |
| 3 | `Goblin Champion` | Handing the Khan the Everlasting | Sneak +12, Barter +6, Poison +15, Agility +1, carry weight +20 |

**The ladder is made of quests the game already shipped.** Only rung one needed new
writing (Hrubjub had no onward pointer); the shaman's eyes quest and the Khan's bounty
hunter both already existed, already served the Horde, and already completed inside
conversations this mod was editing anyway. Rank 3 is granted in the same action array as
the shipped `Goblin Champion` perk, at all three prices you can haggle the Khan to.

Each rung also grants an Event Title Perk, so the rank is visible on the character sheet
rather than only in the stat totals. Rank 3's (`Goblin Champion`) ships with the game and
is granted by the Khan in vanilla; ranks 1 and 2 needed new perk files built on that
pattern. No shipped faction join announces itself in any other way -- the Templar, Wielder
and Inquisition assignments fire XP and quest actions and nothing else -- so this is the
game's own idiom for "you have earned a title", not an invented one.

Each grant is guarded on holding the previous rank, because Lionheart's quests can be done
in any order and these are tiers rather than a counter. Reach the Khan first and you are
not titled Champion at rank one; you simply do not advance until you have earned the rung
below.

Benefits are written as **increments**, not tier totals, because the shipped ladders
accumulate: every vanilla faction record grants `+1` to its rank counter with
`Allow Accumulation=1`, and the `Highlevel` gates test `Rank > 2`, so a rank-3 Templar is
carrying Squire's `+4`, Warden's `+8` and Paladin's `+12` simultaneously. At rank 3 a
Horde player therefore has Sneak +30, Barter +14, Poison resistance +35, Disease +10,
Agility +1 and carry weight +30.

New gates: `Goblin Horde IS`, `Goblin Horde Midlevel`, `Goblin Horde Highlevel`,
`Goblin Horde NOT`, in `Resources/Dialog/Requirements/Faction/` beside the shipped ones.
These are deliberately *not* the existing `Monster Races/Goblin IS.can`, which tests the
player's race rather than their loyalty.

### Extend - Hrubjub is findable, and leads somewhere

In vanilla the entire Horde path hangs off one reply, behind a question about a corpse.
Answer "This doesn't concern me" and you never learn the option existed.

- **A Perception route.** `PE 7+` on the opening node: *"You are no scavenger. You have
  been sounding that wall for a weak course."* He is a sapper, and an observant character
  can see it before saying a word about the body.
- **A second door after talking him down.** Reaching `60 used speech` no longer dead-ends
  the recruitment; you can ask what his business at the wall is.
- **An onward pointer.** He used to say the Khan would be pleased and stop. He now names
  the warrens beyond the western wood and tells you to use his name - which is what makes
  the spy quest rung one of a ladder rather than an errand.
- **Rank 1.** Completing `Spy for Hrubjub the Goblin` assigns `Goblin Chum`, on the same
  `CAssignFactionToCharacterAction` pattern Cedric Alsen uses to recruit you to the
  Wielders.

Both new doors cost the same -25 karma as the shipped one, copied verbatim so no route is
a cheaper way to the same place.

### Extend - the camp reads your build

Vanilla's goblin camp has 23 skill and attribute gates and **19 of them are Speech**. Most
of what is added here costs no new requirement files, because the game already ships them
and references them nowhere: 18 Lockpick gates, 7 Schmooze, 6 Outwit, and five each for
Agility, Endurance and Luck - 46 finished files that nothing in Lionheart reads.

| Where | Check | What it opens |
|---|---|---|
| Trapped Conquistador (25 replies, **0 gates** in vanilla) | `Schmooze 7` | Play along. Announce yourself as the herald and move his imaginary tourney to Barcelona |
| same | `Outwit 7` | See the arrangement for what it is: he is fed, housed and matched against prisoners, which makes him livestock rather than a champion |
| same | `ST 8+` | He respects exactly one argument, and it is not an argument |
| Hrubjub | `PE 7+` | The way into the Horde, above |
| `Rakeb` | `Tribal 80` | He explains his craft in real divination vocabulary and vanilla's only reply is "I don't speak Goblin". A practitioner can answer him - and he drops the performance |
| `GoblinKhan` | `Schmooze 7` | Charm rather than trained Speech as a way to satisfy his demand to be entertained |
| `GoblinEntranceGuard` | `Schmooze 7` | Talk your way through the gate on charisma |
| `GoblinEntranceGuard` | `Goblin Horde IS` | Name-drop Hrubjub. The pointer he gives you is the thing the guard checks |
| `GoblinGrumdjum`, `10 Smart Goblins` | `Outwit 7` | He brags about goblin philosophers "beyond the ken of your average human intellect". Call the bluff: Bonecrusher wrote nothing down, and Brain-Gnasher was a general |
| `GoblinGrumdjum`, `81 Magic Node` | `Thought 80` | He theorises the mana obelisks are the residue of old spells. A Thought mage knows they are reservoirs, and he takes the correction beautifully |
| `GoblinGrumdjum`, `91 Dryad Magic` | `Outwit 7` | He warns you about the dryad's healing, her wards, and her tongue -- the tongue twice. He is not afraid you will lose to her |
| `GoblinGrumdjum`, `110 Goblin Poetry` | `Schmooze 7` | Praise the haiku on its craft rather than gushing. Feeds the same "told the Khan about the poetry" flag the vanilla routes do |
| `Goblin Henchman` (Bludjund) | `ST 8+` | He is a squire who has never eaten a brain and would like it to be yours. Loom at him |
| same | `Outwit 7` | He insists he is not telling you the Khan sent them to spy, having just told you. Ask what else he is not telling you |
| same | `Schmooze 7` | Finish his rhyme properly instead of scraping past the `IN 4` bar |
| `Goblin guarding Woodcutter daughter` | `ST 8+` | Step over him and pick the child up |
| same | `Goblin Horde IS` | The shipped Speech line is a *bluff* about knowing the Khan. If you serve him it is not a bluff |
| same | `Barter 55` | Buy her, through the restored trade node below |

**Grumdjum is the largest goblin conversation in the game** -- 42 nodes, 105 replies, and
in vanilla every one of its 33 gates is quest state, not one skill or attribute among
them. He is also the goblin who reads philosophy, theorises about magic and writes haiku,
so the four checks above are all about meeting him at his own level rather than getting
past him. The dryad one is load-bearing: the tree already supports talking to her instead
of killing her -- that is what its `Dryad talked to NOT killed` gate is for -- and vanilla
never hints the option exists.

**Two shipped requirement files are named for Outwit and test Speech instead** -
`Grumdjun Dryad talked to NOT killed Player high Outwit.can` and
`River Dryad Take Goblinkill quest Grumjun NOT dead High Outwit.can`. Somebody meant to
gate Grumdjum's dryad branch on intelligence, named the files for it, and shipped Speech.
Both now test `COR(Speech >= 20, Outwit >= 7)`, so the intelligence route is added and the
Speech route is untouched.

Only the first of the two has any effect in play: `River Dryad Take Goblinkill quest
Grumjun NOT dead High Outwit.can` is referenced by **no conversation in the game**. It is
repaired for consistency and because a later release may want it, but nothing reads it
today and no test can observe it.

**Three gates are re-authored rather than referenced where they sit.** Vanilla's own
`Outwit 7 greater or equal`, `Schmooze 7 greater or equal` and
`General Tribal Skills moreequal 80` live in `Requirements/Derived Attributes/` and
`Requirements/Skills/Magic Tribal/`, and **no shipped DialogTree names a gate from either
folder** - because nothing ever used those gates at all. No shipped DialogTree uses a
path-qualified `Requirement=` either, so both ways of reaching them were unproven.

Bare names demonstrably resolve from fifteen different folders, so resolution is almost
certainly a global search and either form would probably work. "Probably" is not a good
enough foundation for eight replies, so this mod ships `Outwit 7+`, `Schmooze 7+` and
`Tribal 80+` in `Requirements/Attributes/` instead - the folder sixteen vanilla bare names
already resolve from, and where `PE 7+` and `ST 8+` live. The expressions are copied from
the shipped files verbatim; only the location and the stem differ.

`Outwit` and `Schmooze` are used in preference to raw `IN` and `CH` wherever both would
work. They are pass-through derived attributes living under `Perk and Trait Support` -
which is what that folder is for - so gating on them leaves a socket open for a later perk
to grant the reading without touching the stat. Raw attributes are used only where no perk
should ever substitute: `ST 8+` to face down the conquistador is strength, not cleverness
about strength.

### Restore - a negotiation nobody could reach

`Goblin guarding Woodcutter daughter` contains `40 goblin offers trade`, a written
negotiation node with **no inbound link and no replies of its own** - cut content sitting
in the shipped file. It is wired back in, which is what gives Barter something to do in a
scene that otherwise offers a Speech roll or a fight.

That scene needed it. In vanilla it has eleven replies and **exactly one non-combat
exit**; even "It's no concern of mine what you do with her" ends with the goblin deciding
you are the appetiser. It now has four ways out that do not involve killing him, and the
child lives in all of them.

### Restore - two characters who were written and never placed

`GoblinGirl` (19 nodes) and `GoblinGuards` (4 nodes) ship finished in the archive with
**zero map references**. Both are now in `Goblin Warrens`.

- **The Khan's daughter** stands beside her father's court. She has a first-meeting node
  and a return node, and the whole flirtation-and-prove-yourself arc the writers gave her.
- **The two gossiping guards** are on the southern approach, arguing about how bad
  Grumdjum's latest poem is until one of them says *"Shhh, did you hear something?"*

**Her tree was also truncated.** Two replies point at `250 Rejection` and `290 follow 3`,
and the vanilla file simply ends before either node was written - two of the game's 21
"no way out" dead ends. Both are authored here, because placing her without fixing them
would ship a character who can strand you.

Neither NPC needed a new character template. A Character Template carries no reference to
its dialogue - the generator does - so both reuse shipped villager cans and take their
identity from `New Name` and the tree's own `Name=`. The Girl uses `Mongol Vendor Village`
(race `Goblin Tough`, the weakest of the three villager presets), which suits the Khan's
daughter better than a warrior statline, and means she turns on you with the rest of the
camp if you give the camp a reason.

### Restore - the poisoned pie, which also already existed

`Woodsman Liver Pie Goblins.InventoryItem` ships in the archive with its own inventory
icon (`Goblin Pie.mdl16`), its own ground pickup model (`Goblin Pie_PU.mdl16`), a display
name and a description - and **nothing in the entire game refers to it**. It was cut with
its art finished. No new art was needed here, and none was made.

It also could not be used: `PlugIn Behaviors=Array{Item Count=0}` and
`Slot Used In=Character Slot Types/!None`. It is now a real consumable on the shipped
`Potion Luck` pattern - UseAction, PickUp, PutDown, `HotKey` slot, and the Array form of
the icon field, which all eleven shipped HotKey items use and no non-usable item does.

**What it does is what the file asks for.** The Girl says her mother's ingredients "would
help you if you were ever badly hurt". The designer's note on the same reply says
*"girl give PC a poison pie"*. Those do not contradict each other - one is the lie and one
is the truth - so both are kept. The description stays byte-for-byte as shipped, trailing
whitespace and all, and the pie poisons: 2-5 Poison damage over 60 seconds, calibrated
against the shipped Poison Touch wand's 1-4 over 120. Even the sound it plays on use is
the healing-potion sound, which is the pie's whole argument.

And you can catch it. `PE 7+` smells the apothecary's back room under the liver;
`Outwit 7+` simply knows what her mother thinks of you. Either one opens
`227 momma's seasoning`, where the Girl folds immediately and suggests, hopefully, that
you could just carry it around and not eat it. You still get the pie. You just know.

### Extend - Hub'blub keeps two sets of prices

Vanilla ships one merchant entity at `Price Multiplier=1` and a vendor conversation with
no Barter check at all. Barter can only mean something if there is a cheaper store to
reach, so there is now a second `CMerchantAI` entity at `Price Multiplier=0.75` - the low
end of the shipped 0.75-to-2.0 range - with identical stock. It opens two ways:

- `Goblin Horde IS` - *"Chum prices, Hub'blub. I did not walk into a goblin warren to be
  charged like a tourist."*
- `Barter moreequal 60` - the damp-bolts-and-no-other-customers argument.

This is the pattern the developers already use for `Lope Inventory low`/`high` and
`Vendor 2 Inventory low`/`high`/`especial`: same vendor, second entity, different number.

## The rule this release follows

**A check adds a route. It never removes one.** Every scene here can still be solved
exactly the way vanilla solved it, by a character with none of these stats. That is worth
stating because it is also the test: a check that silently replaced a shipped route is the
bug to look for.

## Not in this release

- **The Crossroads patrol** -- disarming its spawn-hostility and adding the counter-contract
  on Esteban. Scheduled as **0.1.1**, which finishes the goblin theme.
- **The mutual quest-failure wiring** (Torquemada's contract against the Khan's), **karma
  for the Woodcutter's eyes**, and **dialogue that branches on rank 2 or 3**. All are
  goblin follow-ups and **none is scheduled yet** -- they are deliberately not called
  0.2.0, because 0.2.0 is whole-game link repair that needs no new writing.
- Nothing else from the 0.1.0 scope. The Girl's poisoned pie, briefly cut for needing a
  new item, turned out not to need one - see below.

## Installing

```
python modmanager.py install <path-to-this-repo> "<game-dir>"
python modmanager.py build "<game-dir>"
```

`install` must be rerun before every `build` if anything under `files/` changed - `build`
reads from the installed copy, not from this folder.

**Enable it last.** Fixt should win any conflict with the scratch mods in the tools repo.

## Compatibility

New dialogue nodes and new faction records do not retrofit cleanly onto a save that has
already had these conversations. Start a new game, or at least a character who has not yet
met Hrubjub.
