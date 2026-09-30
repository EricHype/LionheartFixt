# Lionheart Fixt 0.25.4 - Fernand's two replies know which one applies

Reported within minutes of 0.25.3: *"i still get the release companion dialog when i talk to him but
he's already been dismissed."*

Correct, and it was a bad trade on my part. 0.25.3 left both replies ungated so that a player who had
already released him could still rejoin, and accepted an offer to dismiss a companion who was not there
as the price. Paying that on every conversation is worse than the migration problem it avoided.

## Why the obvious fix does not work

The idiom this very map already uses for him is an `Active=0` marker entity plus
`CCheckExistenceAction`, exactly as `fernand gave barter` does.

But a marker is **map-local**, and Fernand travels. He can be dismissed anywhere in the game, and a Port
District entity is out of scope the moment he leaves it. Cross-map state belongs on the player, which is
what `Derived Character Attributes/Game Scripting Variables/*` exists for -- this project already ships
seven of them.

## So there is an eighth

`Fernand Is Waiting`:

| reply | shown when | does |
|---|---|---|
| Wait here, Fernand | the variable is **not** 1 | `CReleaseCompanionAction`, then **+1** |
| Walk with me again | the variable **is** 1 | `CSetCompanionAction`, then **-1** |

Each reply can only fire in the state its own gate describes, so the variable is confined to 0 or 1.
That is what removes the need for a conditional inside either action, and with it the accumulation drift
a naive +1/-1 pair would otherwise have.

**If your save was dismissed before this fix** the variable reads 0, so the dismiss line shows once.
Choosing it releases a companion who is not following -- a no-op -- and sets the variable, after which
the rejoin appears and the pair is correct forever. One extra step, once.

Nothing here is invented. The read is `CIsEqualTo{CVariableDerivedCharacterAttribute, ...}` copied from
`CedricAlsen.DialogTree`, the write is `CAddCharacterModifierToCharacterAction` copied from
`Herbalist Dialogue.DialogTree`, and `CExpressionNot{Operand1=...}` was already in Fernand's own tree.

## What this says about 0.25.3

The reasoning there -- that recoverability beats tidiness -- was right about the goal and wrong about
the means. It treated "map marker" and "no gate at all" as the only two options and never asked where
the state should actually live. The scripting variable gives recoverability *and* correct labels, and it
was available the whole time.

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt.

Download, unzip, run `Mod Manager.bat`. Dialogue and attribute repair; applies to any character,
including one with Fernand already following or already dismissed.

https://github.com/EricHype/LionheartFixt/releases/tag/v0.25.4
