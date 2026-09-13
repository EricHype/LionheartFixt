**Read this first.** This release is the first to edit anything in Act 3, and unlike the last
three full releases, two of its pieces were played through to working before it shipped -- the
two in Act 3, which were also the two I'd have bet on breaking. The rest is built and unplayed.
Four of the earlier releases are still unplayed too. If you would rather wait for a build
somebody has walked end to end, wait.

## Machiavelli keeps his word, or his threat

Refuse to partner with Machiavelli in Barcelona and he tells you, in the shipped game, that
you've *"forced me to seek aid from those that seek to do us harm."* Save him and he promises
to repay his debt. Both endings were written for Montaillou -- and he isn't on any Montaillou
map. Nothing ever called either one.

He's at the inn now. Refuse him, and he gloats, walks out the door, and the Old Man's assassins
come in behind him. Save him, and he pays what he owes and warns you what's coming. Let him die,
or kill him yourself, and he isn't there.

The assassins are the real thing this time -- the Alamut model, and harder than Montaillou's own
guards. And the Inquisition agent at the far table will turn on you if you cast spirit magic
in front of him. That is not a bug. It is the Inquisition, and every one of its people in the
game reacts the same way.

## Na Roqua counts her friends

Promise the witch of Montaillou you'll spare the Cathars, and the game marks you a
`cathar friend` -- a flag it ships, checks, and never once sets. So the greeting written for
that state, *"Welcome spiritbearer and Cathar friend,"* could never play, and the two voiced
lines behind it could never be heard. In them she admits what she was: *"It is true that we once
hunted together,"* she says of the shapeshifting daeva, and tells you where the thing that can
kill it is kept.

All of that plays now, and the branch actually opens the cave it describes -- the shipped node
gave the advice and forgot the door.

## Torquemada acknowledges his own

Kill the Goblin Khan for the Inquisition as an Inquisitor and Torquemada gave you the speech
written for an outsider -- *"there is now hope for your soul."* The one written for a member
sat with no way to reach it. An Inquisitor now hears *"I have known, child. I felt the blight
lift from the forest,"* and is paid the same.

## What was read and left alone

Torquemada also has a second task written for you: purify the shadow dryad of Montaillou.
Three states, voiced, with a perk at the end. It was never wired, and reading it explains
why -- the shadow dryad is Na Roqua herself, and she **cannot be killed**. She has ten thousand
hit points behind an armour class of a thousand, and attacking her casts you out of her house.
The developers built a debug switch to skip the death because there was no other way to reach
it. The quest is unfinished, not cut, and finishing it would mean inventing what they didn't
build. It stays dark. The full account is in `docs/releases.md`.

## Smaller things

- Sir Auric now sponsors a tainted initiate in the words written for one, instead of the human's.
- Ask Lord Javier about joining with no sponsor and he tells you to seek Auric -- the entrance
  to a loop whose other end already existed.
- Javier will tell you about the Sacred Lance before you leave for Montserrat, as Jafar already
  could.
- Cervantes greets a returning player as a returning player.
- Also folded in from the repair releases since 0.8.0: Fernand's drinkable draught and his
  memory, Quinn's errands and reserve, the lava trolls' peace, the Helpful Wererat, Amir's
  directions for a Favored One, and the fish monger's perk.

## Installing

Download, unzip, run `Mod Manager.bat`. It finds a GOG, Steam or retail install by itself,
`Uninstall` puts everything back, and it installs over 0.8.4 as normal.

**The Montaillou pieces need a character who has not yet entered the inn or the witch's house**,
and the Cervantes fix a character who hasn't entered the Temple District -- a level's contents
are captured into your save the first time you walk in. The Khan report, Auric and Javier are
dialogue and work on any save.
