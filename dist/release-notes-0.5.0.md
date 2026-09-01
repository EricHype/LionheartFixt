**Read this first: one of the three things in this release has been played.**

The final job has been walked end to end. The caught-in-the-act branch and the vault
job are built, verified against the automated gates, and **unplayed**. Everything here
is honest about which is which, and if you would rather wait for a signed-off build,
wait.

That warning is not boilerplate. While building this, four separate defects passed
every automated check the project has -- correct parse, byte-identical round-trip, 97
validator checks, verified deployment -- and were only visible in the running game.

## The thieves were thin, and it was measurable

Counted properly, Enrique offers the beggars **five** jobs and Juanita offers **four**.
He pays out around **600 gold** across his line. She has **seven** money-taking actions
and **not one** that gives. The biggest quest in the Sewers -- the wererat cure, five
states across three maps -- is on his side. Her jobs pay more XP each, 500 against 200,
but there is one fewer of them and they cost you money to take.

Her fifth job was written and left unreachable. The node that offers it is orphaned,
the quest's second state is activated by nothing, and the requirement written to gate
its turn-in is used nowhere in the game. The whole frame shipped with nowhere to
happen.

## What is in it

**The thieves' final job.** Juanita's last errand, restored and given a place to
happen: a walled yard at the far end of the Temple District, a house with a side door,
and a cache to lift. This is the project's first new map.

**Getting caught.** Skill decides the *cost*, not whether the job is possible.
Perception 5 or Find Traps 35 and you are out clean. Neither, and a guard is waiting
when you step outside. Surrender and you wake in the Inquisition's cell, where Sanchez
already knows what to charge you -- and you keep what you stole, so the job can still
be finished. Fight and Juanita takes you anyway, with a word about drawing the watch
onto the guild. Go to the cell on her errand and she will not take you at all; three
hundred buys your membership back, not her good opinion.

**The thieves' vault.** There is a 324KB map behind a secret door in the thieves' den
-- spike traps, archers, guard dogs, around 950 XP -- that no quest in the game points
at, guarded by a man who is switched off. You get shouted at twice by warning balloons
belonging to nobody and walk straight in. Skulker will now pay you to do it properly,
and taking the job switches the guard on. Five ways past him: standing with the guild,
a bluff, a hundred gold, a quiet moment, or steel. Draw steel and every thief in the
den comes for you -- that consequence was already built and never reachable.

**Juanita's fee is no longer avoidable.** Refuse her 70 gold for a lead, walk away and
come back, and she handed it over free. The code that charges you a late penalty was in
the file, unreachable, and the requirement written for it ships used nowhere.

**The night with her explains itself.** The aftermath is real text in nine nodes with
no replies in any of them, so it opens and closes on its own and does not register. If
your Charisma is under 9 she robs you of up to 500 gold and vanilla tells you only
through that box.

## Installing

Download, unzip, run `Mod Manager.bat`. It finds a GOG, Steam or retail install by
itself and `Uninstall` puts everything back. Install over 0.4.1 as normal.

**This one needs a new character.** Dialogue is read fresh every time you talk to
someone, but map contents are captured into your save the first time you enter a level,
and this release adds a new map and new entities to three existing ones. On an old save
the yard gate stays shut, the cache is not there, and the vault guard never appears.

## If you play it

`docs/qa.md` cases SR1 to SR42 are the checklist. The two that matter most are SR31 --
check your inventory in the cell, because if the cache is gone the quest cannot be
finished -- and SR39, which confirms that being jailed for anything unrelated leaves
Juanita indifferent.

The vault has no cases yet. That is deliberate: they should describe what play shows
rather than what the build intends.
