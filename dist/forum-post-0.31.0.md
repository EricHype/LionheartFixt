# Lionheart Fixt 0.31.0 - Butu's Heir

The one goblin vanilla never placed, put to work — and a choice in an optional cave in act 2 that
costs you a companion in act 8.

## Two things vanilla left on the table

`Mongol Goblin Hat Super` is **placed nowhere in the game**, and its race is the most interesting
statline in the family:

| race | HP | AC |
|---|---|---|
| Goblin Hat | 60 | 125 |
| Goblin Hat Tough | 80 | 150 |
| **Goblin Hat Super** | **250** | **225** |
| Goblin Khan | 210 | 175 |

**The toughest goblin in the game, harder than the Khan himself.** The hat line steps 60 to 80 to 250
where every other goblin ladder steps about a quarter per rung, so it was never a third tier: it is a
boss statline filed under hats, and vanilla used it as one, lending it to the Khan's own can for its
numbers. 0.30.1 gave that can a race of its own, which freed it.

And vanilla names a second Khan, **exactly once in the whole game**, in a flavour line on an item:

> *"Collected by Butu Khan, this book of poetry contains many free verses of Goblin Poetry."*

That book sits in the **Goblin Warrens** — in Plumjum Khan's own cave — and Weng Choi will buy it off
you as a rare book without anyone ever saying whose it was. A second goblin dynasty exists in the
fiction, its Khan's poems are a trinket on the floor of the goblin who outlasted him, and you can sell
his heritage to a human shopkeeper by weight.

## The Ravine Cave changes hands

Act 1 is untouched: the Khan's goblins, the four posts, the officer alarm, the three-goblin argument
from 0.30.0. **After Montserrat, the east half belongs to Butu's heir.**

A tribe recoloured red — one of the **sixteen hue palettes the engine ships and vanilla never
touches** — holding the same four posts, led by a goblin wearing the Goblin King model that in the
whole game belongs only to the two Khans. **He already looks like a Khan, which is the argument he is
making.**

About 24 of them plus the heir, against act 1's 93. The point is that it changed hands, not that it
got bigger.

For calibration: act 1's hardest enemy is a troll boss at 111 HP; act 2's is a Snakebreed boss at 160
HP and AC **250**, so the heir hits harder and is easier to hit; and act 3 already fields a creature
with his exact statline as ordinary opposition.

## He reads what you did about the Khan

Five ways in, every one from something the game already had:

| what you did | what he says |
|---|---|
| killed Plumjum | *"You emptied the chair. I am standing in it. I had six winters of reasons and you did it in an afternoon"* |
| his **Champion** | *"Take the mark off and we will talk about his cave. Leave it on and I will take it off the usual way."* |
| his chum or blooded | *"He gives ranks the way he gives speeches, and both cost him nothing. Butu gave his goblins poems."* |
| cleared the dryad's forest | *"You have killed more of his than I have. I am not fond of you. I am extremely interested in you."* |
| nothing at all | *"He has drawn plans for six winters. Have you seen the plans? They are very good plans."* |

He talks before he fights.

## Two quests, and they fork

| | |
|---|---|
| **Butu Khan's Poems** | his errand. The book is in Plumjum's warren, and you may already have sold it to Weng Choi. Return it and the cave stands down |
| **The Goblin of Butu's Line** | Plumjum's contract. Kill the heir and your **goblin rank advances** |

They are mutually exclusive. Kill him without ever taking the contract and you get nothing for it,
which is the right answer.

## The late game remembers

Whether Plumjum Khan meets you in Persia — and whether **Grumdjum joins you as a companion** — already
depended on being the Khan's Champion and on his being alive. It now has a third condition.

**Hand Butu's heir the poems and neither of them turns up.**

An optional cave in act 2, costing a companion in act 8.

## The Khan points you east himself

The heir sat somewhere the game never sends anyone: the Sacred Scimitar needs the silver in the *west*
half, the east half has its own entrance off Scar Ravine, and the two only connect by a crystal node.
So Plumjum tells you, and never says the heir's name.

> *"Butu's line were nobodies when I was young and they are nobodies with a cave. He has my east rock
> and my shiny and he tells my goblins that I draw maps. Go and make him a nobody again, morsel, and
> do not come back to tell me his name."*

There is a reply that repeats the heir's line about the maps back to his face. Nothing bad happens,
which is the joke.

## Corrections carried in this release

**0.30.0 claimed the troll-style officer alarm "scales itself" — no officer for a weak party, no
alarm.** It does not. Party-strength thresholds are upper bounds and the engine picks the group you
fall *under*, so the group carrying the officer opens much earlier than the number suggests. The
tiering makes officers uncommon; it does not gate them behind strength. The worst-case figure of
twelve creatures stands.

**0.30.1's test notes described the Ravine Cave wrongly** and told a tester to fight in through a
passage between the two halves that does not exist.

**Found and not fixed:** vanilla's own Goblin Khan dialogue points at a node that is not in the tree.
One dangling reply, vanilla's, recorded rather than patched blind.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

**This one genuinely needs a save that has not been in the Ravine Cave's east half.** New map
entities only exist for a save that had not entered the map when you installed, and the whole conceit
here is walking back in to find it changed — so the players most likely to want it are exactly the
ones it will not reach. A character who has not been to that cave gets all of it.

## If you play it

Three things are worth reporting above everything else.

**Does the cave actually change hands**, and do the red goblins read as a different tribe in that
lighting?

**Side with the heir, then reach Persia in act 8** — the Khan and Grumdjum should both be absent. That
is the row this release exists for.

**And one older question it would settle:** kill Plumjum Khan back in act 1, then reach Persia as his
Champion. He should not appear. If he does anyway, a gate that has been shipping for a while has never
worked, and knowing that is worth more than this whole release.
