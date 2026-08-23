The first release of Lionheart Fixt that has been played rather than only built.

0.1.4 exists entirely because of that playtest. Eight defects, and the ones that mattered
most were invisible to every static check the project has: a rank that silently never rose
above 1, a contract that paid nothing, a girl who greeted you as a stranger forever. Every
fix here has since been seen working in a session.

## Installing

1. Download `lionheart-fixt-0.1.4.zip` and unzip it somewhere with a **short path**.
2. Double-click **`Mod Manager.bat`**.
3. Click **Install Lionheart Fixt 0.1.4**.

Then **start a new game**. `Uninstall` in the same window puts everything back exactly as it
was. No Python, no separate mod manager, and administrator rights are usually not needed.

### Upgrading from an earlier version

Uninstall the old one first, then install this. Several fixes are in map data, which a save
records the first time it enters a level -- so a character who has already visited the
Crossroads or the Goblin Warrens keeps the old behaviour there whatever is installed. A new
character is the only way to see all of it.

## What this fixes

**Goblin standing now rises.** Each rank of the Horde *replaced* the one before it rather
than adding to it, so standing never passed the first tier -- which is why the Crossroads
contract kept refusing players who had earned it. Each rank is also now strictly better than
the last; becoming Champion used to cost you the disease resistance you had as Blooded, and
drop your Barter.

**Killing Guard Esteban is noticed.** The contract pays, the quest completes, and the quests
he was running fail. Previously nothing happened at all.

**Rakeb reacts to what you have done for him.** Three greetings written for him could never
be seen, because he gave the same line whatever the state of his errands.

**The rank titles describe your standing, not a deed.** Goblin Blooded claimed you had
butchered a woodcutter for his eyes even if you earned it by killing the river dryad.

**The Goblin Girl remembers meeting you**, instead of greeting you as a stranger every time.

**Two rewards can no longer be farmed.** She handed out a liver pie every time you asked,
and Rakeb would re-issue the devil fish quest as often as you cared to ask.

**Six blank dialogue options that did nothing when clicked** are repaired -- two removed,
four turned into the proper "end conversation" they were meant to be.

## What has not been tested

One character has walked this, not two. The rule the whole project follows is that every
check adds a route and none removes one -- and a build that solves everything cannot
demonstrate that. Only a low-Intelligence, low-Charisma, high-Strength character can show
that a new skill check did not quietly *replace* the vanilla way through a scene. That pass
is still outstanding, and it is the failure most worth reporting if you find it.

Two of Rakeb's three restored greetings, and both farmable-reward fixes, are correct in the
built data but have not been watched directly in play.

## This download contains no game content

Lionheart's engine reads no patch format, so a mod that changes an existing file would
normally have to ship the whole file. Instead the files this mod changes travel as **deltas
against your own copy** and are rebuilt locally during installation; only newly authored
files ship in full. Installing rebuilds your `data.dat` in about ten seconds, needs roughly
2 GB free while it works, and validates the new archive before replacing the old one.

If another mod has already changed one of the same files, the installer names the file and
stops without changing anything. Several mods can be installed together as long as no two of
them change the same file.

## Verifying the download

    certutil -hashfile lionheart-fixt-0.1.4.zip SHA256

Compare against `lionheart-fixt-0.1.4.zip.sha256`.

## Reporting problems

Please include which character, their goblin rank, the exact line or reply, and whether the
vanilla route still worked. That last one separates "a check didn't fire" from "a check ate
the shipped content", which is the failure this project's own rule forbids.
