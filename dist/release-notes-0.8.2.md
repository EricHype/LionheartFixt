**Repair only.** Quinn's reagent errands, played for the first time, and one follow-up to
0.8.1. Nothing new.

## Quinn's errands

Five things, all from one playthrough of the three errands 0.4.0 added.

**A test reply was live.** *"[TEST] Give me a small amount of XP"* sat under *"I have other
questions"* for every player, a leftover from the very first version of this mod. Gone.

**Errands came back after you finished them.** Complete the pelts and Quinn would offer the
pelts again. The check that was meant to say "not yet offered" stopped working the moment the
errand completed -- the same engine behaviour that bit Fernand in 0.8.1. Each errand is now
offered once, ever.

**Turning in too few cost you what you had.** Bring four stingers and Quinn would take them,
play the "five, and none of them spoiled" speech, pay nothing, and leave you with none. He now
counts first: bring the right number and the turn-in plays as written; bring fewer and he pushes
them back across the bench and tells you to come back with all of them.

**Trappers were refused on return visits.** 0.4.0 fixed the pelt turn-in to accept a Trapper's
quality pelts -- on one of the seven places the turn-in appears. Return to Quinn by any other
greeting and the old check refused you. All seven now accept either kind, in any mix.

**His reserve never opened.** Deliver the pelts and ask what he has set aside, and nothing was
there. Only one of those seven turn-in copies advanced the count that unlocks the reserve; the
other six -- every return visit, and the Inquisitor and Templar first greetings -- did not. The
count is fixed for new characters, and for characters already past the pelts the reserve now
opens on the errands themselves, so a save that carried the damage is repaired by installing
this.

## Fernand's draught can be drunk

0.8.1 made Fernand's healing potion a quest item that could not be drunk, which fixed the
wrong-bottle bug but removed the choice: a potion worth nothing to you costs nothing to give
away. It is now a real Extra Healing potion. Drink it and you cannot save Juan.

## Installing

Download, unzip, run `Mod Manager.bat`. It installs over 0.8.1 as normal. Dialogue changes
take effect on any save; the draught change needs a character who has not yet taken Fernand's
job.
