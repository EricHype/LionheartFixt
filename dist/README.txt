================================================================================
  LIONHEART FIXT 0.1.2
  A restoration and repair mod for Lionheart: Legacy of the Crusader
================================================================================

Lionheart ships with finished content that never made it into the game: characters
with no map placement, dialogue replies that lead nowhere, an item that cannot be
used. Fixt puts them back and repairs what is broken around them.

The rule the whole project follows: every check this mod adds opens a NEW route
through a scene, and none removes an existing one. If you solved something in
vanilla by talking your way out of it, that still works.

Release 0.1.0 - 0.1.2 covers the goblins of the Wilderness.


--------------------------------------------------------------------------------
  INSTALLING
--------------------------------------------------------------------------------

  1. Close Lionheart if it is running.
  2. Double-click Install.bat.
  3. Approve the administrator prompt. This is needed because the game normally
     lives under Program Files, and Windows will not let an ordinary program
     write there.

The installer finds your game automatically. If it cannot, it asks you to paste
the folder that contains Lionheart.exe.

It does NOT modify data.dat, the game's big archive file. It copies files into
the game's data\ folder, which the engine reads in preference to the archive.
That means installing takes a couple of seconds instead of several minutes, and
your original archive is never rewritten or at risk.


--------------------------------------------------------------------------------
  YOU MUST START A NEW GAME
--------------------------------------------------------------------------------

This is not a suggestion, and it is not about being careful -- it is how the
engine works.

The first time a save file enters a map, it records everything on that map into
itself. Re-entering later restores that recording; it does not re-read the map
from the game's files. Fixt places characters who were never on those maps
before, so on an existing save they simply will not be there. No error, no
warning -- an empty spot where a character should be.

Dialogue changes DO appear on an existing save, which makes this worse rather
than better: some of the mod will seem to work, which reads as a broken install
rather than an old save.

So: new game. A save made before installing will never show the new characters,
even after visiting the maps again.


--------------------------------------------------------------------------------
  UNINSTALLING
--------------------------------------------------------------------------------

Double-click Uninstall.bat.

Every file the installer replaced was backed up first, and every file it wrote
was recorded with a checksum. Uninstall puts the originals back and deletes the
files the mod added.

If another mod has changed one of the same files since you installed Fixt, that
file is reported and left alone rather than reverted -- undoing someone else's
mod silently would be worse than leaving it.

Saves made while the mod was installed may refer to characters that no longer
exist. Keep a save from before installing if you want a guaranteed way back.


--------------------------------------------------------------------------------
  IF SOMETHING GOES WRONG
--------------------------------------------------------------------------------

"Fatal Not Found Error" on entering a map
    A map is referring to a dialogue node that is not there. This should not
    happen in a release; please report the map name.

A new character is not where the notes say they are
    Almost always an existing save. See the section above.

The installer says it cannot find Lionheart
    Paste the full path to the folder holding Lionheart.exe when it asks.

The installer says access is denied
    It was not run as administrator. Right-click Install.bat and choose
    "Run as administrator".

Nothing seems different at all
    Check that the installer reported files copied, and that you started a new
    game rather than loading an old one.


--------------------------------------------------------------------------------
  WHAT IS IN THIS RELEASE
--------------------------------------------------------------------------------

0.1.0  The Horde
    Restores GoblinGirl and the goblin guards -- finished characters that ship
    with no map placement at all. Repairs four dialogue replies that dead-end.
    Makes the Goblin Horde a real faction with three ranks, built on the same
    pattern the game already uses for the Templars and the Knights of Saladin.
    Gives Hrubjub's evil path two more ways in, gives Hub'blub a second store at
    member prices, and makes the poisoned liver pie an item you can actually
    use. Adds skill and SPECIAL checks to a settlement that previously answered
    to almost nothing but Speech.

0.1.1  The Crossroads Patrol
    The goblin patrol at the Crossroads was an ambush with no way to talk to it.
    It is now a parley, with a contract you can take against the guard captain
    who has been hunting them -- and the captain can now actually be killed.

0.1.2  Standing
    The camp reacts to your rank. Villagers, Rakeb and the Khan all treat a
    Goblin Champion differently from a stranger, and your standing accumulates
    across every service you do for them rather than being granted once.


--------------------------------------------------------------------------------

Fixt is named after Fallout Fixt, in the same spirit: fix what is broken, restore
what was cut, and change as little else as possible.
