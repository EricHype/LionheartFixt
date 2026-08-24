# Lionheart Fixt 0.2.0 - what was written

Lionheart shipped with dialogue its own scripters never wired up. Not cut lines sitting in
a leftover file somewhere - finished nodes, in the files the game loads, that nothing in
the game can ever open. The Goblin Girl has three of them in which she tells you she is
coming along. The Khan has four in which he explains how he intends to take Barcelona.

**Fixt** is a restoration-and-repair mod, named after Fallout Fixt and following the same
discipline. It fixes what is broken, restores what was cut, and writes new content only
where the game plainly ran out - working from the shipped archive rather than from opinion.

**Download:** https://github.com/EricHype/LionheartFixt/releases/latest
**Source:** https://github.com/EricHype/LionheartFixt (MIT)

---

## What is in 0.2.0

**The Goblin Girl follows you around the Warrens.** Vanilla wrote the moment she decides to
- *"I'll just keep an eye on you and make sure nobody else tries to eat you, okay?"* - and
never connected it. She stays in her cave: walk to either exit while she is with you and
she stops at the mouth of it and tells you she will wait.

**The Khan explains his war.** Reach Goblin Champion and he lays out the invasion of Nueva
Barcelona: kill the guards outside the walls, starting with *that fool Guard Esteban*, then
the gate guards, and the horde comes through the portcullis. Four vanilla nodes, none of
them previously reachable, including the one where he objects to you leaving mid-briefing.

That is also the motive the Esteban contract never had. Fixt made killing him pay out in
0.1.4; this is the reason it matters.

**Grumdjum talks to you after the dryad.** One wrong field in the map. Standing over her
body he gave a one-line bark instead of the greeting written for that moment - and behind
that greeting sit two more scenes nobody has ever seen. He tells you where the goblin city
is, *through the waterfall to the east*, which turns out to be the only in-world direction
to the Warrens in the entire game. And he has written a poem about your kill.

**Goblin standing counts with the jailor.** Walking Inquisitor Darsh out of the Mongol Camp,
vanilla gives you exactly one way past the jailor that is not a fight: Speech 25. Blooded
and Champion goblins can pull rank instead. The Speech route is untouched, as always.

**Five dead replies** repaired - one dangling target, four blank options that did nothing
when clicked.

---

## What 0.1.x did, if you are new

The **goblins of the Wilderness** are the most developed evil content in the game, and in
vanilla they feed nothing. Fixt makes the Horde a real faction with three accumulating
ranks, built on the machinery the game already uses for the Templars and the Knights of
Saladin, and the camp reads your standing. It puts back **two finished characters that ship
with complete dialogue and zero map references** - nobody has ever met them. It repairs the
dead-end replies through the goblin thread, gives Hub'blub a second set of prices for
members, and turns the Crossroads patrol from a charge-on-sight encounter into a parley.

The rule the whole project follows: **every check adds a route and none removes one.** If
you solved a scene in vanilla by talking your way out of it, that still works.

---

## Installing

Unzip somewhere with a short path, double-click **`Mod Manager.bat`**, click the button that
names the mod. About ten seconds. `Uninstall` puts everything back exactly as it was.

No Python, no separate mod manager, no vanilla backup to make first. Windows only; works
with the GOG, Steam and retail installs.

**You must start a new game.** Not caution - mechanics. A save records a map's contents the
first time it enters, so characters and map changes will simply not be there on an existing
character.

### The download contains no game content

Files that already exist in your installation travel as **deltas against your own copy** and
are rebuilt locally during installation - 3.1 MB of the game's own content down to 97 KB.
Only newly authored files ship in full. That is why the download is 80 KB even though this
release adds a 924 KB map to the mod.

---

## What has not been tested

**The Goblin Girl's follow has been played. Nothing else in 0.2.0 has.** Everything is
verified against the built archive, which catches a broken reference but not a gate that
resolves wrongly.

If you find a rank-gated reply showing up for the wrong rank - the Khan's briefing wants
Champion, the jailor wants Blooded - that is the single most useful thing you could report.
The same goes for any vanilla route that stopped working: this project's rule is that a
check adds a route and never removes one, and only a low-Intelligence, low-Charisma
character can prove it.

Please include which character, their goblin standing, the exact line, and whether the
vanilla route still worked.

---

## Coming next

The back half. Two goblin companions were written and cut for Act 8 - Grumdjum, who speaks
in rhyming couplets and wants to eat the Old Man of the Mountain's brain, and a Khan who
turns up in the Persian dunes offering to travel with you. Neither has so much as a spawn
point. That is where this goes after the Wilderness is finished.

Issues and reports: https://github.com/EricHype/LionheartFixt/issues
