**This is the first release that is mostly new content.** Everything before it repaired
what was broken or restored what was cut. This adds a questline that never existed.

That is a deliberate crossing, not a drift. The project's stated order is fix, then restore,
then extend, and 0.1 through 0.3 earned the right to the third. It is worth knowing which
kind of release you are installing.

## Quinn's reagents

Quinn the herbalist in the Gate District wants three things, in order:

| Errand | Reagent | Unlocks |
|---|---|---|
| 1 | three wolf pelts | **Great Healing** |
| 2 | five wasp stingers | **Superior Healing** |
| 3 | one lava troll hide | **Supreme Healing** |

Each one unlocks a tier above vanilla's Extra Healing, sold from a reserve he keeps under
the counter for people who bring him work instead of complaints. The tiers are cumulative --
finish all three and he stocks all three.

The order is not arbitrary. The tiers are **paced by where each reagent lives**, because
Supreme Healing is roughly four times Extra Healing and would ruin act 1 if it arrived
there. You will not get it until you are in the sewers under Barcelona.

## Almost none of this needed inventing

The wasp stinger already exists, with finished art, and already drops -- from the Cursed and
Tainted variants only, 6 of the 9 wasp types. **Nothing in the shipped game consumes one.**
It is vendor trash with a purpose now.

The lava troll hide already exists, with finished art, and is referenced by **nothing at
all**: no drop table, no quest, no dialogue, no map. A quest item for a quest nobody wrote.
And since trolls close their own wounds, the hide of a self-healing creature is the obvious
reagent for the best healing potion in the game.

The three potions were built too, in a separate mod, shipping into a test map where no
player could reach them.

## Three ways to get the hide

Vanilla wrote a diplomatic opening to the lava trolls and then closed it. Every branch of
their only conversation ends in a fight or in walking away, and killing one turns the whole
pit. Left alone, this errand would have forced you to slaughter a people the game plainly
means you to feel something about.

But the troll tells you his problem without being asked, and it is a practical problem:

> Too many dead Trolls. Wererats sneaky.

He does not care how that stops, only that it does. And the Beggars **are** the wererats.

- **Cure them** and the trolls will trade with you.
- **Wipe them out** and the trolls will trade with you.
- Or **kill a Lava Troll Boss** and take the hide off it.

Good path, evil path, or no diplomacy at all — nobody is locked out. The peaceful route is
deliberately not framed as the merciful one: vanilla's own cure quest makes you kill the
Prime Wererat for a patch of fur, so that framing would be a lie.

## The Wolf Trapper perk locked you out of the first errand

Every wolf branches on whether you took **Wolf Trapper**. Without it you get one plain
pelt; with it you get two better ones. The errand only accepted the plain kind — so taking
the perk handed you pelts your own quest would not take. Either counts now, and a mixed
three works.

## What has been tested

**Nothing.** This release has not been played at all. Everything is verified against the
built archive, which proves that every reference resolves and every file parses, and proves
nothing whatever about whether a quest advances.

Given that the last release turned up four vanilla bugs the moment someone actually played
it, treat this one accordingly. The most useful things to report:

- **The peaceful troll route appearing when it should not** — it must require the wererats
  to be settled, and must work whether you cured them or destroyed them.
- **The pelt errand refusing pelts**, on a character with the Trapper perk or without.
- Any turn-in that takes your reagents and does not advance.

## Installing

1. Download `lionheart-fixt-0.4.0.zip`, unzip somewhere with a **short path**.
2. Double-click **`Mod Manager.bat`**, then **Install**.

Upgrading from 0.3.0: uninstall first. **You need a new character** — this release edits
maps, and a save records a map's contents the first time it enters.

## Verifying the download

    certutil -hashfile lionheart-fixt-0.4.0.zip SHA256

Compare against `lionheart-fixt-0.4.0.zip.sha256`.
