# Lionheart Fixt 0.1.4 - restoring the goblin thread

Lionheart: Legacy of the Crusader is a good RPG for one act and a combat corridor for
seven. That is measurable rather than a matter of taste: Barcelona holds 88 quests, the
Crypt holds one, and combat density rises about 35x across that boundary.

**Fixt** is a restoration-and-repair mod, named after Fallout Fixt and following the same
discipline. It fixes what is broken, restores what was cut, and writes new content only
where the game plainly ran out - working from the shipped archive rather than from opinion.

**Download:** https://github.com/EricHype/LionheartFixt/releases/latest
**Source:** https://github.com/EricHype/LionheartFixt (MIT)

---

## What 0.1.x does

This first arc is about the **goblins of the Wilderness** - the most developed evil content
in the game, and in vanilla it feeds nothing. No faction, no rank, no standing, and a
settlement that answers to almost nothing but Speech.

**Two finished characters are put back in the game.** GoblinGirl and the goblin guards ship
with complete dialogue trees, portraits and all - and zero map references. Nobody has ever
met them. They are in the Warrens now, and her truncated tree is finished.

**The Horde becomes a faction with three ranks.** Chum, Blooded, Champion, built on the same
machinery the game already uses for the Templars and the Knights of Saladin. Your standing
accumulates across every service you do for them, and the camp reads it: villagers, the
shaman and the Khan all treat a Champion differently from a stranger.

**Four dialogue replies that dead-ended now lead somewhere.** Hrubjub's evil path has two
more ways in and an onward pointer. Hub'blub keeps a second set of prices for members. The
poisoned liver pie - which already existed, fully implemented, and could not be used - works.

**The Crossroads patrol will talk to you.** In vanilla it charges on sight. It is now a
parley, with a contract against the Templar guardsman who has been paying travellers to thin
them out. He can now actually be killed; vanilla made him invulnerable and had him call the
guards on you instead.

**Skill and SPECIAL checks where the game had none.** Perception, Intelligence, Barter,
Outwit, Schmooze, Tribal lore. The rule the whole project follows: **every check adds a route
and none removes one.** If you solved a scene in vanilla by talking your way out of it, that
still works.

---

## What is actually new in 0.1.4

0.1.4 is the first release made entirely of things a playtest found, and the interesting
ones were invisible to every static check:

- **Goblin standing never rose above 1.** Each rank of the faction *replaced* the one before
  it rather than adding to it - so the contract kept refusing players who had earned it.
  Vanilla has the same defect in its own Templar and Saladin ranks, incidentally: all three
  tiers grant +1 to the same counter, so their "rank 3" gates can never fire.
- **Killing the guardsman did nothing** - no payment, no quest completion, no consequences.
  It turns out a killed NPC leaves a corpse, so "does he still exist" answers yes forever.
- **The goblin girl greeted you as a stranger every time.**
- Six blank dialogue options that did nothing when clicked, all of them vanilla's.

---

## Installing

Unzip somewhere with a short path, double-click **`Mod Manager.bat`**, click the button that
names the mod. About ten seconds. `Uninstall` puts everything back exactly as it was.

No Python, no separate mod manager, no vanilla backup to make first. Windows only; works
with the GOG, Steam and retail installs.

**You must start a new game.** Not caution - mechanics. A save records a map's contents the
first time it enters, so characters this mod places will simply not be there on an existing
character. Dialogue changes *do* apply to an old save, which makes it worse rather than
better: half the mod appears to work.

### The download contains no game content

The engine reads no patch format, so a mod that changes an existing file would normally have
to redistribute it - a forty-line edit to a map would mean shipping 1.2 MB of Black Isle's
work. Instead, files that already exist in your installation travel as **deltas against your
own copy** and are rebuilt locally during installation. Only newly authored files ship in
full. That is why the download is 75 KB.

---

## What has not been tested

One character has walked this, not two. The project's own rule is that every check adds a
route and none removes one, and a build that solves everything cannot demonstrate that -
only a low-Intelligence, low-Charisma character can show that a new skill check did not
quietly *replace* the vanilla way through a scene.

If you find that, it is the single most useful thing you could report. Please include which
character, their goblin standing, the exact line, and whether the vanilla route still worked.

---

## Coming next

Link repair across the whole game - 84 true dead ends, no new writing required. Then the
Knights of Saladin as a second faction, cut content returned to its right home, and
eventually the back half: the Crypt's war, the two unfinished areas, companions.

Issues and reports: https://github.com/EricHype/LionheartFixt/issues
