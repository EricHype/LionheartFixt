Almost everything in 0.2.0 was written by Black Isle and never reached the game.

Lionheart shipped with dialogue its own scripters never wired up: nodes that exist, that
are finished, that nothing in the game can ever open. This release finds them in the goblin
thread and connects them. Two of the five items add nothing at all -- they change a single
field, or supply the player's half of a conversation whose other half was already written.

## Installing

1. Download `lionheart-fixt-0.2.0.zip` and unzip it somewhere with a **short path**.
2. Double-click **`Mod Manager.bat`**.
3. Click **Install Lionheart Fixt 0.2.0**.

Then **start a new game**. `Uninstall` in the same window puts everything back exactly as it
was. No Python, no separate mod manager, and administrator rights are usually not needed.

### Upgrading from 0.1.4

Uninstall the old one first, then install this. Two of the changes are in map data, which a
save records the first time it enters a level -- so a character who has already visited the
Goblin Warrens or the Lake keeps the old behaviour there whatever is installed.

## The Goblin Girl follows you

She always meant to. Vanilla shipped three nodes -- *"I'll just keep an eye on you and make
sure nobody else tries to eat you, okay?"* -- in which she announces she is coming along,
and none of them was ever connected to anything. Now she does.

She stays in the Warrens. Walk to either exit while she is with you and she stops at the
cave mouth and says so, and you can leave her there or turn back. She is not a companion
you take on the road; she is a goblin girl who follows you around her own cave.

## The Khan has a war plan

Reach **Goblin Champion** and he will explain it. He wants Nueva Barcelona, the walls are
the problem, and his answer is you: kill the guards outside the walls, starting with that
fool Guard Esteban, then the gate guards, and the horde pours through the portcullis.

Four nodes, all of them vanilla, none of them previously reachable -- including the one
where he objects to you walking out on him mid-briefing. If you have already killed Esteban
he notices, and if you kill him afterwards you can go back and say so.

The horde never does attack Barcelona. That is vanilla's unkept promise, not ours, and this
release does not pretend otherwise -- it restores the plan the Khan states, and leaves it
stated.

## Grumdjum talks to you after the dryad

One wrong field. After you bring him the River Dryad's death he moves to her body, and the
conversation there opened a one-line bark about how succulent her brain will be, instead of
the greeting written for that moment. Behind that greeting sat two more scenes nobody has
seen: he tells you where the goblin city is -- *through the waterfall to the east*, which is
a real direction and the only in-world signpost to the Warrens that exists -- and he recites
a new poem about your kill, with three ways to react.

## Standing counts with the jailor

Escorting Inquisitor Darsh out of the Mongol Camp, the goblin jailor stops you, and vanilla
gives you one way past that is not a fight: Speech 25. Blooded and Champion goblins can now
pull rank instead. The Speech route is untouched.

## Five dead replies

One dangling target in Inquisitor Darsh's tree, and four blank options that did nothing when
clicked -- two removed, two turned into the proper "end conversation" they were meant to be.

## What has been tested

**The Goblin Girl's follow has been seen working in play. Nothing else in this release
has.** Every change is verified in the built archive and against the shipped data, which
catches broken references but cannot catch a gate that resolves wrongly.

The things most worth reporting, in order:

- **A rank-gated reply appearing for the wrong rank.** The Khan's briefing needs Champion;
  the jailor's needs Blooded or better. If a Goblin Chum sees either, a gate failed open.
- **Grumdjum's dryad hand-in.** It sits immediately beside this release's edit and it pays
  the Ring of Fiery Death. It should behave exactly as it did in 0.1.4.
- **The Goblin Girl leaving the Warrens.** She should never reach the Mongol Camp. If she
  does, tell us and it gets a second guard.
- **Any vanilla route that stopped working.** This project's rule is that a check adds a
  route and never removes one, and only a low-Intelligence, low-Charisma character can
  prove it. That pass is still outstanding.

## This download contains no game content

Lionheart's engine reads no patch format, so a mod that changes an existing file would
normally have to ship the whole file. Instead the files this mod changes travel as **deltas
against your own copy** and are rebuilt locally during installation; only newly authored
files ship in full. 3.1 MB of the game's own content compresses to 97 KB of deltas, which
is why the download is 80 KB even though this release adds a 924 KB map.

Installing rebuilds your `data.dat` in about ten seconds, needs roughly 2 GB free while it
works, and validates the new archive before replacing the old one. If another mod has
already changed one of the same files, the installer names the file and stops without
changing anything.

## Verifying the download

    certutil -hashfile lionheart-fixt-0.2.0.zip SHA256

Compare against `lionheart-fixt-0.2.0.zip.sha256`.

## Reporting problems

Please include which character, their goblin rank, the exact line or reply, and whether the
vanilla route still worked. That last one separates "a check didn't fire" from "a check ate
the shipped content", which is the failure this project's own rule forbids.
