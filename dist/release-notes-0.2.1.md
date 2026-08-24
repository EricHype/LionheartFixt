A patch release. One fix, in a scene almost nobody reaches the interesting way.

## Esteban and the bandit you killed before he asked

Kill El Bandito Rie at the Crossroads **before** Guard Esteban ever raises the subject, tell
him so, and he goes off to verify your claim. He came back with:

> Good work! Here is your justly deserved reward.

That is the line for a job he gave you. He never gave you this one. The node written for
this path -- *"Really? Most excellent. Here is your reward. I see you joining our ranks
soon."* -- was in the game and reached by nothing, because the map relay that brings him
back opened the wrong one of the two.

The reward was never broken. 150 gold, the experience, and the quest completion all worked
before; what was wrong was which line he said afterwards.

Two smaller things came out of pointing the relay at the right node, both closed using
lines that already exist in that conversation:

- **Handing in the giant wasps on this path used to end the conversation silently.** Esteban
  now says *"Muy excelente!"* and pays, as he does on every other route. The payment was
  already happening; the acknowledgement was not.
- **The node had no way to say goodbye.** Its default reply pushed you further into the
  conversation instead of out of it. It now offers *"I should be on my way."* like its twin.

Nothing else changed. The ordinary route -- take the thief quest from Esteban, then complete
it -- is untouched and still gives *"Good work!"*

## Installing

1. Download `lionheart-fixt-0.2.1.zip` and unzip it somewhere with a **short path**.
2. Double-click **`Mod Manager.bat`**.
3. Click **Install Lionheart Fixt 0.2.1**.

Upgrading from 0.2.0: uninstall first, then install this.

**A new character is needed to see it.** The change is in `Crossroads.zax`, and a save
records a map's contents the first time it enters. It also needs an unusual play order --
you have to go and kill the bandit before ever asking Esteban what is troubling him -- which
is very likely why this went unnoticed for twenty-three years.

## What has been tested

Nothing in 0.2.0 or 0.2.1 has been played except the Goblin Girl's follow. Everything is
verified against the built archive, which catches a broken reference but never a gate that
resolves wrongly.

For this release specifically, the case worth checking is the **ordinary** thief quest:
take it from Esteban, complete it, and confirm he still says *"Good work!"* That node is
reached from six places and must be untouched.

## Verifying the download

    certutil -hashfile lionheart-fixt-0.2.1.zip SHA256

Compare against `lionheart-fixt-0.2.1.zip.sha256`.
