# Lionheart Fixt 0.25.2 - the trees that named themselves

**Install this over any earlier release.** Five characters could not be spoken to at all: Captain
Isabella, Grace O'Malley, Brambles, Grumdjum and the Knight of Saladin. Talking to any of them killed the
game.

> Got stuck in an infinite loop while trying to load
> `"Levels/1 Barcelona/Dialog/Port District/Captain Isabella"`. This is usually caused by that file
> refering to itself. The actions in this file need to be re-scripted to go through a canned object or
> relay or some other indirect method.

A `.DialogTree` may not name its own file. When it does, the loader recurses and the process dies.

## Vanilla never does this

Its four in-tree `Dialog Tree File=` references all name a **different** tree -- cortes to Shylocke,
SewerEntranceBeggar to Find Enrique, SewerEntranceThief to Find Juanita, Rakeb to Woodcutter. Pointing at
another tree is ordinary. Pointing at your own is the defect, and all **eleven** offenders were this
project's:

| tree | sites | what it was doing | shipped in |
|---|---|---|---|
| `GoblinGrumdjum` | 6 | rewiring his interaction specifier so the next approach opens at the companion nodes | 0.20.0 |
| `Brambles` | 3 | three random thank-you balloons | 0.12.0 |
| `Captain Isabella` | 1 | Grace's "wait here" balloon on being left behind | 0.19.0 |
| `alamutknightsaladin` | 1 | the knight's rejoin node | 0.20.0 |

## The fix is the one the engine asks for

Each offending `CDisplayDialogTreeAction` or `CDisplayDialogBalloonAction` block is moved **verbatim**
into a `CCannedObject`, and replaced in place by `CUseCannedActionAction{Canned Object=...}`. Nothing
around it changes: the `CAddAIAction`, the interaction specifier, the delays and the relays all stay
exactly as they were, so the behaviour is identical and only the indirection is added. Eleven sites
collapse to seven canned objects, because Grumdjum's six reuse two nodes.

Every piece of that has precedent in the shipped game:

- `Common Objects and Scripts/Detect Spellcast.can` is a `CCannedObject` holding a `CAddAIAction` that
  names a dialogue tree -- the exact shape being built here.
- `CUseCannedActionAction{Canned Object=...}` is how the game fires such an object, **107 times**.
- `$Trigger` and `$Instigator` survive that indirection there, which is what the Grumdjum and Alamut
  blocks rely on.

The canned object still names the tree, and that is fine: it is a different file, so the cycle is broken
by the hop. That is precisely what the error message asks for.

**No map edits, and no dialogue nodes moved.**

## Gate 0, again

`check_self_reference` is added: for every tree in the mod, a `Dialog Tree File=` naming its own path
fails the gate. Proved rather than assumed -- reintroducing the Captain Isabella reference exits 1 with
the file named, and restoring it passes.

That is the second fatal in two releases that the gate could not see, and both were reference integrity.
0.25.1 added race skill and attribute references; this adds tree self-reference.

## Why five characters shipped broken

The same reason as 0.25.1, and it compounds. Three of the four trees shipped in 0.19.0 and 0.20.0 -- and
**the game could not reach the main menu from 0.19.0 onward.** The crash that made the mod unplayable
also hid every defect behind it. Nobody could get far enough in to find these, because nobody could get
in at all.

This is what a backlog of unplayed releases actually costs, and it is why `tools/savecheck.py` was
written the same day: so that when a scene *is* played, the state it leaves behind can be checked
instead of remembered.

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt.

Download, unzip, run `Mod Manager.bat`. No save requirements -- these are dialogue and script repairs
and apply to any character. If you have any earlier release installed, replace it.

https://github.com/EricHype/LionheartFixt/releases/tag/v0.25.2
