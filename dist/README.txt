================================================================================
  LIONHEART FIXT 0.1.3
  A restoration and repair mod for Lionheart: Legacy of the Crusader
================================================================================

Lionheart ships with finished content that never made it into the game: characters
with no map placement, dialogue replies that lead nowhere, an item that cannot be
used. Fixt puts them back and repairs what is broken around them.

The rule the whole project follows: every check this mod adds opens a NEW route
through a scene, and none removes an existing one. If you solved something in
vanilla by talking your way out of it, that still works.

Release 0.1.0 - 0.1.3 covers the goblins of the Wilderness.


--------------------------------------------------------------------------------
  INSTALLING
--------------------------------------------------------------------------------

  1. Close Lionheart if it is running.
  2. Double-click "Mod Manager.bat" in this folder.
  3. Click "Install Lionheart Fixt 0.1.3-rc1" and wait a few seconds.

Nothing to download separately and nothing to install first: the mod manager is
in this folder, and the button names the mod it will install.

The manager finds your game by itself. If it cannot, click Change... and point it
at the folder containing Lionheart.exe. Uninstall puts everything back, and you
can install other mods with it too -- "Other mod..." opens a file picker, or drag
a release .zip onto the window.

Administrator rights are usually NOT needed -- a GOG install lets you write to its
own folder. If yours does not, the manager says so and you can right-click
"Mod Manager.bat" and choose "Run as administrator".

Prefer no window? Install.bat and Uninstall.bat do the same job from a console.

Installing rebuilds data.dat, the game's archive: your copy is read, the files
Fixt changes are replaced, the ones it adds are added, and the result is written
back. It takes about ten seconds. The new archive is checked before it replaces
the old one, so a failure part way through leaves your game as it was.

This download contains none of the game's own files. Where Fixt changes
something the game already has, it ships only the difference and rebuilds the
file from your copy during installation. That keeps the download to 60 KB rather
than 2 MB, and means nothing here is redistributed content.

One consequence: the installer needs your original files to patch. If another mod
has already changed one of the same files, it will say exactly which file it
could not rebuild and stop without changing anything. Remove the other mod, or
verify your game files, and run it again.

You need about 2 GB of free disk space during installation, since the new
archive is written before the old one is replaced. The installer checks first
and stops if there is not enough.


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
  USING OTHER MODS AT THE SAME TIME
--------------------------------------------------------------------------------

Yes, as long as no two of them change the same file. Install them one after
another; each is listed separately and each can be removed on its own, in any
order, without disturbing the others.

If two mods do want the same file, the second one refuses to install and tells
you which file clashed. It does not merge them and it does not overwrite the
first -- nothing is changed at all. There is no way to combine two mods that
edit the same file; you have to choose one.


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

It cannot find Lionheart
    Click Change... in the manager and select the folder holding Lionheart.exe.

It says it cannot write to the game folder
    Right-click "Mod Manager.bat" (or Install.bat) and choose "Run as
    administrator". Nothing is changed when this happens.

Nothing seems different at all
    Check that the installer reported files written, and that you started a new
    game rather than loading an old one.

"Could not rebuild <some file>"
    Fixt patches your own game files rather than shipping copies of them, so it
    needs the originals. Another mod has almost certainly changed that file
    first. Remove it, or verify/reinstall the game, then try again. Nothing was
    changed by the failed attempt.

Windows or your antivirus warns about it
    Everything here is an unsigned .bat and .ps1. That is a shape worth being
    suspicious of, so: they are plain text and you can read every line of them
    before running anything. A SHA-256 of the zip is published alongside the
    download.


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

0.1.3  What Playtesting Found
    Goblin standing now actually rises. Each rank of the Horde replaced the
    last rather than adding to it, so your standing never passed the first
    tier and the crossroads contract kept refusing you. Each rank is also
    now strictly better than the one below it; becoming Champion used to
    cost you the disease resistance you had as Blooded.
    Rakeb the shaman now reacts to what you have done for him. Three
    greetings that were written for him could never be seen, because he
    gave the same generic line whatever the state of his errands.
    The goblin girl no longer hands out an endless supply of liver pies,
    and Rakeb will not re-issue the devil fish quest once you have taken it.
    Killing Guard Esteban is now noticed: the goblin patrol pays the
    contract, the quest completes, and the quests he was running fail. The
    goblin rank titles no longer describe a deed you may not have done. Six
    blank dialogue options that did nothing when clicked are repaired.

0.1.2  Standing
    The camp reacts to your rank. Villagers, Rakeb and the Khan all treat a
    Goblin Champion differently from a stranger, and your standing accumulates
    across every service you do for them rather than being granted once.


--------------------------------------------------------------------------------

Fixt is named after Fallout Fixt, in the same spirit: fix what is broken, restore
what was cut, and change as little else as possible.

Updates, older versions and the source:
  https://github.com/EricHype/LionheartFixt/releases
