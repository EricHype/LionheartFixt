**Release candidate.** Everything in this release came from someone playing the mod and
reporting what went wrong, which makes it the first version whose contents could not have
been planned. Two items are fixed but not yet re-confirmed in play; they are named at the
bottom.

## Installing

1. Download `lionheart-fixt-0.1.4-rc1.zip` and unzip it somewhere with a **short path**.
2. Double-click **`Mod Manager.bat`**.
3. Click **Install Lionheart Fixt 0.1.4-rc1**.

Then **start a new game**. `Uninstall` in the same window puts everything back exactly as it
was. No Python, no separate mod manager, and administrator rights are usually not needed.

### Upgrading from 0.1.2

Uninstall the old version first, then install this one. Several fixes here are in map data,
which a save records the first time it enters a level -- so a character who has already been
to the Crossroads or the Goblin Warrens will keep the old behaviour on those maps no matter
what is installed. A new character is the only way to see all of it.

## What changed

**Goblin standing now actually rises.** Each rank of the Horde *replaced* the one before it
rather than adding to it, so your standing never passed the first tier -- which is why the
Crossroads contract kept refusing players who had earned it. Each rank is also now strictly
better than the last; becoming Champion used to cost you the disease resistance you had as
Blooded, and drop your Barter.

**Killing Guard Esteban is noticed.** The contract pays, the quest completes, and the quests
he was running fail. Previously nothing happened at all.

**Rakeb reacts to what you have done for him.** Three greetings written for him could never
be seen, because he gave the same generic line whatever the state of his errands.

**The rank titles no longer describe a deed you may not have done.** Goblin Blooded claimed
you had butchered a woodcutter for his eyes even if you had earned it by killing the river
dryad.

**The Goblin Girl remembers meeting you**, instead of greeting you as a stranger every time.

**Two rewards can no longer be farmed.** She handed out a liver pie every time you asked,
and Rakeb would re-issue the devil fish quest as often as you cared to ask for it.

**Six blank dialogue options that did nothing when clicked** are repaired -- two removed,
four turned into the proper "end conversation" they were meant to be.

## Not yet re-confirmed in play

The rank fix and Rakeb's new greetings are both verified in the built data and neither has
been seen working in a full session yet. If your standing still refuses to pass the first
tier, or Rakeb still gives the generic greeting when he should have something specific to
say, that is the most useful thing you could report.

## This download contains no game content

Lionheart's engine reads no patch format, so a mod that changes an existing file would
normally have to ship the whole file. Instead the files this mod changes travel as **deltas
against your own copy** and are rebuilt locally during installation; only newly authored
files ship in full. Installing rebuilds your `data.dat` in about ten seconds, needs roughly
2 GB free while it works, and validates the new archive before replacing the old one.

If another mod has already changed one of the same files, the installer names the file and
stops without changing anything. Several mods can be installed together as long as no two
of them change the same file.

## Verifying the download

    certutil -hashfile lionheart-fixt-0.1.4-rc1.zip SHA256

Compare against `lionheart-fixt-0.1.4-rc1.zip.sha256`.

## Reporting problems

Please include which character, their goblin rank, the exact line or reply, and whether the
vanilla route still worked. That last one separates "a check didn't fire" from "a check ate
the shipped content", which is the failure this project's own rule forbids.
