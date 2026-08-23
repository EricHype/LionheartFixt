**Release candidate.** Built, verified and installed end to end, but most of the content
below has not yet been played. Expect to find things.

## Installing

1. Download `lionheart-fixt-0.1.2-rc1.zip` and unzip it somewhere with a **short path**.
2. Double-click **`Mod Manager.bat`**.
3. Click **Install Lionheart Fixt 0.1.2-rc1**.

Then **start a new game** -- this matters, see below. `Uninstall` in the same window puts
everything back exactly as it was.

Nothing to install first: no Python, no separate mod manager, no vanilla backup to make.
The manager finds a GOG, Steam or retail install by itself. Administrator rights are
usually not needed. `Install.bat` and `Uninstall.bat` do the same job without a window.

### You must start a new game

Not caution -- mechanics. A save records a map's contents the first time it enters, and
restores that recording rather than re-reading it, so characters this mod places will
simply not be there on an existing save. Dialogue changes *do* appear on an old save,
which makes it worse rather than better: half the mod seems to work, which reads as a
broken install.

### Unzip somewhere with a short path

A few resource paths run to ~110 characters. A deep folder pushes them past Windows'
260-character limit, where the extractor drops files **without reporting it**, and the
install then fails for a reason that looks nothing like the cause.

## What's in it

**0.1.0 The Horde.** Restores GoblinGirl and the goblin guards -- finished characters that
ship with no map placement at all -- and repairs four dialogue replies that dead-end. Makes
the Goblin Horde a real faction with three ranks, built on the pattern the game already
uses for the Templars and the Knights of Saladin. Gives Hrubjub's evil path two more ways
in, gives Hub'blub a second store at member prices, and makes the poisoned liver pie an
item you can actually use. Adds skill and SPECIAL checks to a settlement that previously
answered to almost nothing but Speech.

**0.1.1 The Crossroads Patrol.** The goblin patrol at the Crossroads was an ambush with no
way to talk to it. It is now a parley, with a contract you can take against the guard
captain who has been hunting them -- and the captain can now actually be killed.

**0.1.2 Standing.** The camp reacts to your rank. Villagers, Rakeb and the Khan treat a
Goblin Champion differently from a stranger, and your standing accumulates across every
service you do for them rather than being granted once.

The rule the whole project follows: **every check adds a route and none removes one.** If
you solved a scene in vanilla by talking your way out of it, that still works.

## This download contains no game content

Lionheart's engine reads no patch format, so a mod that changes an existing file would
normally have to ship the whole file -- a forty-line edit to `Crossroads.zax` would mean
redistributing 1.2 MB of Black Isle's map. Instead, the 18 files Fixt changes travel as
**deltas against your own copy** and are rebuilt locally during installation; only the 21
newly authored files ship verbatim. That is 2.2 MB of shipped game content reduced to
76 KB of difference, and a 70 KB download.

Installing rebuilds your `data.dat` with the mod applied, in about ten seconds. It needs
roughly 2 GB of free space while it works, and the new archive is validated before it
replaces the old one.

One consequence: the installer needs your original files to patch. If another mod has
already changed one of the same files, it names the file and stops **without changing
anything**. Several mods can be installed together as long as no two of them change the
same file.

## Known limitations

- Windows only.
- The `.bat` and `.ps1` files are unsigned, so SmartScreen or antivirus may object. They
  are plain text and you can read every line before running them. A SHA-256 of the zip is
  published below.
- This is a release candidate. The goblin faction ranks are confirmed working in play; the
  greeting reactivity added in 0.1.2 is not yet play-tested.

## Verifying the download

    certutil -hashfile lionheart-fixt-0.1.2-rc1.zip SHA256

Compare against `lionheart-fixt-0.1.2-rc1.zip.sha256`.

## Reporting problems

Please include which character, their goblin rank, the exact line or reply, and whether
the vanilla route still worked. That last one separates "a check didn't fire" from "a check
ate the shipped content", which is the failure this project's own rule forbids.
