# A second opening for the wounded assassin

For review. Nothing is in the tree.

This is the other half of the fix for *"the wounded assassin pleads as though abandoned while his
allies stand around him"*, reported on
[issue #11](https://github.com/EricHype/LionheartFixt/issues/11). The first half is a gate repair,
described at the bottom. **Neither half works alone**, which is the thing worth reading first.

---

## Why a gate alone is not the fix

0.71.7 gated his conversation on `CIsAliveAction{Name To Check For=Assassin}`. Exactly one
generator in the map carries that name:

| distance from him | generator | active at load | spawns | the gate sees it |
|---|---|---|---|---|
| **291** | unnamed | **yes** | up to 6 | **no** |
| 450 | `Hall Ambush Generator` | no | up to 3 | yes |
| **682** | unnamed | **yes** | up to 5 | **no** |

The two that are standing there when the player arrives are the two it cannot see, because they
have no `New Name` and `CIsAliveAction` matches by name. So the gate currently does nothing on the
route where it matters, and he says *"They have gone on without me"* to a player who just walked
past six of his own side.

**But naming those packs and extending the gate deletes his scene.** The condition is "has his side
been cleared off this floor", and on the peaceful route the player killed nobody, so it is false for
the whole route. A correct gate would silence him from first entry to last. Mixxer5 would go from
hearing a wrong line to finding a body that does not speak.

So the gate should not decide *whether* he talks. It should decide *which true thing* he says.

## His register, so you can hold me to it

Measured off his eight existing lines:

| | |
|---|---|
| shape | stage direction in angle brackets, then short declaratives. Fragments are normal |
| the stage directions | almost all about what speaking costs him: *"the laugh costs him"*, *"it is mostly blood"*, *"it costs him more than the last one"* |
| tone | wry, never self-pitying. He laughs at his own situation in his first line |
| contractions | no verb contractions. Possessives only: *Master's*, *Templar's*, *East's* |
| dashes | spaced hyphen, *"Lionheart - he has paid a great deal for it"* |
| length | stage directions 4 to 28 words, spoken 3 to 35 |

---

## The new node

### new node: 2 left

> &lt;A man in black lies propped against a dead knight, a Templar's sword still through his side.
> The men down the hall do not look over.&gt; You are late. They can see me from there. I am not
> worth the walk - failure earns no coin or sympathy.

Stage direction 26 words, spoken 22. Both inside his range.

**The first sentence is byte-identical to `1 found`.** Same body, same wound, same tableau -- only
the second sentence changes, and it changes to the thing the player can confirm by turning round.

*"You are late"* is kept because it is his greeting in both versions, so the two openings read as
one man rather than two drafts.

*"I am not worth the walk - failure earns no coin or sympathy"* is the whole point of the line. It
answers the question the scene raises -- why does nobody help him -- in the faction's own logic
rather than with bitterness. These are people a trader on the road describes as *"a bit gruff, but
they pay well"*, who take tribute and deliver cargo; Pau has just told the player they carried off
every monk who could not walk. They carried the monks and left their own man, because the monks
were worth carrying.

**The second clause is yours and it is the better half** -- it names the economy instead of leaving
me to imply it, and *coin* is the exact in-world word for it.

Two notes on how it is punctuated here. It arrived as *"I am not worth the walk, failure earns no
coin or sympathy"*, which is a comma splice, and he does not write those: his short declaratives
take full stops. **The spaced hyphen is his own join for exactly this move**, a statement followed
by its reason, and he uses it twice -- *"Lionheart - he has paid a great deal for it"* and *"what
did the monks want with them - to pray at?"* So the comma became ` - `, which is the house dash in
this tree.

*"or sympathy"* I left alone, though it is the one word I would question. *Coin* is specific and
cold; *sympathy* names the feeling he is conspicuously not asking for, which slightly softens him.
It also reads as a bleak joke at his own side's expense, and he is wry, so it may well be right.
Cutting it gives *"failure earns no coin"* at 19 words.

It also gives him a reason to talk that the abandoned version does not have. Being written off is
why he answers questions about where they went.

**Replies: copied verbatim from `1 found`**, gates and all. He knows the same things either way, and
cloning the block rather than reauthoring it keeps the two openings in step if either is edited
later.

### `3 return` is unchanged

> &lt;He is still breathing.&gt; Still here? Finish it, or go.

Neutral in both cases, so a player who leaves and comes back gets the right line without a second
variant.

---

## The gate repair, for completeness

Not dialogue, so it is listed here rather than drafted:

1. Give the pack standing nearest him a `New Name`: `Hall Snakebreed` at (1904,1625). The name is
   unused in Level 1, and nothing references that generator today because an unnamed generator
   cannot be targeted, so this cannot break anything that exists.
2. Widen the existing test from one `CIsAliveAction` to a `COr` of two: `Assassin` and
   `Hall Snakebreed`.

   **Corrected at build time.** This section first named a second pack at (2006,2476). That
   coordinate was wrong -- it is a `Fixed Dead Body Generator`, not a spawner -- and a proper sweep
   finds **five** unnamed pacifying generators within 900 of him: at 291, 682, 716, 841 and 841
   units. Gating on all five would make a player who fought their way in clear the entire floor,
   including packs in rooms they may never enter, before he would say his original line. So the
   gate takes only what stands nearer to him than the hall ambush 0.71.7 already judged relevant:
   the ambush at 450, and the one pack at 291. That is a rule that can be stated rather than a
   radius picked to fit, and the four packs beyond 450 are left out on purpose -- men in another
   room are not standing over him.
3. Point the true branch at `2 left` and the false branch at `1 found`, each still checking
   `questioned the assassin` first so the return node keeps working.

The empty `Then=` goes away as a side effect. At the moment, clicking him while the ambush lives
does nothing at all -- no balloon, no refusal -- so the player cannot tell whether he is a character
or scenery.

## What this does not do

It does not make the packs react to him, and it does not move them. They stand where they stand.
The line works because they are visible and indifferent, which is the complaint restated as
characterisation rather than contradicted.
