# Lionheart Fixt 0.30.0 - The Scourge of the Land

Named from the line that turned out to be the centre of it: *"Nonsense, we are Mongol-trained goblins,
the scourge of the land!"* Written for a goblin in 2003, and fired by nothing until now.

The goblins are the largest enemy population in the game. **780 of spawn capacity across 30 maps**,
more than the thieves, soldiers, Snakebreed and trolls put together, and until this release the only
major family with **no barks and no damage resistances at all**. Everything Fixt had done with goblins
was about *not* fighting them. This is the other half.

## GoblinVillager.DialogTree was a bark bank nobody wired

This was not a writing job. The tree has 55 nodes and **11 of them are fired by nothing in the entire
game** -- no map, no can, no tree, vanilla or Fixt -- with ten more reachable in exactly one map each.

The restored lines are referenced at their own vanilla node IDs rather than copied, so vanilla's dead
nodes start firing and no text is duplicated.

Dead until now: `100 dinner`, `100 take our meal`, `100 take brain`, `500 goblin confrontation 2`,
`500 Fleeing C`, `100 Combat Fight`, and the three `500 Attacking` nodes. Nearly dead: `500 Fleeing A`
and `B`, which only `Bounty Hunter Camp` ever fired, and which now play whenever any goblin is hurt.

## The argument written for three goblins and never cast

`500 Attacking A/B/C` are not three interchangeable barks. They are one exchange:

> *"They have butchered our brothers with alarming ease. Perhaps discretion would be the more prudent
> course of action?"*
>
> *"Nonsense, we are Mongol-trained goblins, the scourge of the land!"*
>
> *"Yes, Wumjup is right! Muster up your courage and attack! AIIIIiiiiIIII!"*

A coward, a boaster, and a third who sides with the boaster **by name** -- so B had to be Wumjup,
which is also why the rabble's barks keep mentioning a Wumjup nobody ever met. `Drubjub` and `Lumgrub`
are vanilla's names too: they are the two goblins talking to each other in `GoblinGuards` and
`GoblinLt`, trees whose entire content is a pair of goblins gossiping about Grumdjum's poetry and about
who has to go and kill the water witch. None of the three was an entity name anywhere in the game.

A can only knows itself, so this could never be a can edit. Vanilla's own `goblin attack banter` relay
in `Crossroads` turned out to be the pattern, and a better one than a timed burst: `CSeriesAction` with
`Next Action Index=0` advances **one item per trigger**, the index persisting between firings, which is
how vanilla gets six banter lines out of one relay.

So the trigger is a goblin dying, and the argument escalates as the fight goes worse -- the coward
speaks over the first body, the boaster over the second, the charge over the third. That is the shape
the text was written in, and it was only visible by reading how vanilla staged its own banter instead
of inventing a mechanism.

## 105 lines, in banks sized for how often they are heard

The same shape as 0.27.0's thieves -- a shared family bank plus a sub-bank per type, about one attack
in four, over the creature's own head, not in the combat log -- but much bigger, because the player
hears goblins more than every other family combined:

| bank | lines | |
|---|---|---|
| rabble | **40** | 18 shared + 16 its own + 6 restored |
| shamans | **37** | 18 shared + 16 its own + 3 reused from the `Goblin Shaman` tree |
| archers, officers | **34** | 18 shared + 16 its own |
| hurt, all tiers | **14** | 10 its own + 4 restored |

The shipped families run 11-14, where a repeat turns up after about five barks; at 34-40 it takes about
eight.

There is a second register 0.27.0 did not have: `Damaged Script Action`, goblins noticing they are
losing, about one hit in six, which is where the restored fleeing lines live.

Shamans bark on attack as well, which looked impossible at first because their `Shoot Completed` is
occupied. It is not an attack reaction -- it is a spell *picker* -- so the bark bank went in as a
fourth item and the spell distribution stayed proportional.

Seven cans deliberately carry nothing. The Khan, Rakeb and Grumdjum have whole trees of their own, and
the Crossroads Patrol Leader, Goblin Girl and Goblin Guard are ones Fixt made talkable. A named
character must not speak the rabble's lines.

## The damage profile every other family already had

This is the real answer to why every goblin fight felt the same. Animals resist slashing and crushing
38 and take extra from cold; English Enemies are armoured and fold to crushing at **-44**; wererats are
immune to fire; undead shrug off electricity. Across 417 races and nine damage types, the goblins' 19
races were **blank in all nine columns**.

| tier | Slash | Pierce | Crush | Fire | Cold | Elec | Poison | Disease |
|---|---|---|---|---|---|---|---|---|
| rabble, archers | -10 | - | -20 | **-25** | 20 | 15 | 100 | 100 |
| shamans | -10 | - | -20 | **-25** | 20 | **50** | 100 | 100 |
| hat officers | **20** | **20** | 0 | **-25** | 20 | 15 | 100 | 100 |
| Khan, Hat Super, Grumjun, Rakeb | 25 | 25 | 10 | **-10** | 25 | 25 / 50 | 100 | 100 |

**Burn them, do not poison them, and the officer needs a different weapon than the rabble around him.**

Fire is the family signature at every tier, and nothing else in the game is reliably fire-vulnerable.
Poison and Disease sit at 100 -- carrion and brain eaters -- which is vanilla's own immune value and
also the ceiling: above it the engine *heals* the target, which is what Wererat Boss's disease 125 has
always been doing. The officer tier inverts to armoured, so blades beat him where clubs beat the
rabble, and lightning is wasted on a shaman who throws it himself.

Fire tapers to -10 at the boss tier for two reasons, one honest and one practical: 200+ HP goblins are
thicker-hided, and `Goblin Grumjun` is Grumdjum's race -- he is a restored companion, and a companion
who dies to his own player's fire is a bug report, not a feature.

## The officer calls for help

Fixt's own troll idiom from 0.29.0, inverted, and the map forced it: a generator's `New Name` applies
to **every** creature it spawns, so a post holding two archers and a Hat cannot name the Hat alone
without being cloned. So the *post* is named and the *officer* is the trigger. `Ravine Cave East`'s
four archer posts become `Goblin Cave Post`, and a struck Hat raises them once.

It scales itself, which was discovered rather than designed: the Hat appears **only in the top party
tier, at weight 1 against the archer's 2**. No officer for a weak party, so no alarm. Worst case
measured at **12 creatures, once per level** -- against the troll pack alarm that would have woken
80-94 before it was rescoped.

`Respond to calls for reinforcements` is now on for all 16 hostile goblin cans; it was off on 21 of 23,
leaving goblins alone with the Animals and the Thugs while the Undead run it on 88 of 92.

## Two Wilderness scenes that had exactly one solution

**The hostage north of the Crossroads.** A goblin holds a woodcutter's daughter and vanilla offers only
ways to save her. She can be handed to the Khan now -- two routes, one gated on Horde standing and one
that earns it, the second tagged `<Lie>` on vanilla's own convention. Both grant the *Child Killer*
title and -50 Karma. Her father gets a failure state he can actually reach, and he can tell the
difference: the lie is a lie to *him*, and the Khan has a line waiting when you next stand in front of
him.

**The silver mine.** The Sacred Scimitar is a Knights of Saladin initiation step, and its first task
had one solution: kill the cave. One source of magnetized silver exists in the whole game, no merchant
sells it, `Ravine Cave West` had zero dialogue trees, and Eduardo closes every alternative in his own
voice. A foreman now holds the mouth of the cave with the archer post around him, bows up and not
firing, and there are four ways past him -- Horde standing, Barter 40, Speech 40, Schmooze 7 -- plus an
ungated demand that is refused with a warning rather than a fight, so the routes are discoverable. The
three deeper posts stay hostile until a parley succeeds, so a player who attacks gets the cave exactly
as vanilla built it. Negotiation moves the guards, never the ore.

## One repair, found by checking our own work before reusing it

**`CActionSelectSkill` is not a no-op.** The bark banks pad their random pick with it so that only one
attack in four speaks, and that padding is inert *only when it selects the skill the creature would
have used anyway*. Vanilla uses the same action in the same slot as the real mechanism for choosing the
next attack: `Priest Super` casts its shield, then randomly picks Fire Orb or Spike.

0.27.0 and the Snakebreed pass gave `Skills/Fighting/OneHandedMelee` to **21 archer cans whose races do
not preset that skill at all**. `Soldier4 Bow Super` has Ranged 97, no melee rating, and three of its
four attack slots told it to select melee. The trolls were already correct, having been given `Ranged`
because trolls throw. All 21 now resolve the filler from their own race's primary skill by lookup
rather than from an authored constant.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Goblin cans and races are global edits, so they reach creatures spawned after you install and not
anything already standing in a level you have loaded. `Ravine Cave East`, `Ravine Cave West` and
`Scar Ravine` are map changes, which a save that has already entered those levels will not pick up at
all. A fresh character, or one that has not been to the Wilderness, sees all of it.

## If you play it

Three things are worth reporting above everything else.

**Do the three balloons in the goblin argument appear over three *different* goblins?** If they stack
over one, the exchange has failed.

**How many goblins answer when you strike an officer in Ravine Cave East?** The budget is 12, and the
troll alarm in 0.29.0 had to be rescoped after exactly this measurement.

**Does anything actually come when you attack a lone goblin at the edge of a group?** The explicit
"call for help" action is registered in the engine and used zero times in all of vanilla, so either
being attacked calls implicitly -- and the undead have been swarming all along -- or the field does
nothing anywhere. Static analysis cannot tell those apart. One fight can.
