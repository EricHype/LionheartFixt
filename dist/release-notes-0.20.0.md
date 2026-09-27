# Lionheart Fixt 0.20.0 - Alamut

This is the last act, and the largest: eleven maps and 15,498 level parts, more than acts 6 and 7 together. It
is also the opposite of act 7. Where the English Shrine fielded nineteen enemy families with Soldier at 73% of
every spawn, Alamut fields 88 families across 131 templates with a top-four share of 53% - the most varied act
in the back half of the game - plus 63 real traps and 46 hidden areas. What it was short of was words, and
wiring.

## The map with no words

`05 Acid Wash` shipped with no dialogue tree and no balloon at all. 334 parts, 40 combatants, not one line. What
the silence was hiding is a better piece of design than the act's reputation suggests: the floor is a sluice.
Crossing a trigger clones a walking acid front that cuts the ground away as it travels and keeps spawning
20-to-40 Acid steam around itself; six seconds later a second clone restores the floor; the gate re-arms ten
seconds after that and runs again for as long as you are in the channel. The opposition is fifteen archers and
twelve master spellcasters and no melee enemy at all - they shoot from terraces and never come down into it.

None of which the player was told. The channel names itself now, warns as each wash lets go, says the ten
seconds out loud, and reports what the switch at the spiked gates shut off. The hazard itself is untouched.

## The goblin who was promised two releases ago

0.2.0's notes deferred Grumdjum's companion arc to this act by name. It is twelve `300`-series nodes and **every
one of them is voice-recorded** - join, dismissal, rejoin, two injury barks, three combat quips, all in rhyming
couplets. `CSetCompanionAction` in his tree counted zero, and `300 companion`, the node the whole cluster hangs
off, was opened by nothing at all. So it was written, recorded, and given no mechanism.

He joins now, follows, quips about every thirteen seconds, calls for healing at half his health and again at a
fifth, can be dismissed, stands where you left him and asks after you, and can be taken back - `300 companion
joins you` was recorded asking "Would you like Grumdjum to join you again?" with no way on earth to answer it,
and has its answers now. And the goblin Khan turns up in the sandy dunes himself as a three-node cameo, offering
to come and sow destruction of his own; those three lines were recorded and shipped with the voiceover flag
switched off.

Both goblins answer to goblin rank. Be the Horde's Champion with their Khan still breathing and they come. Kill
that Khan for Torquemada back in act 1 and **no goblin comes to Alamut at all** - a choice made six acts and
many hours earlier, answered here.

## The knight whose arc half worked

Recruiting the Knight of Saladin on a return visit swapped his AI for an escort and worked properly. Recruiting
him **the first time you met him** set the companion flag without that swap, so he stood exactly where he was -
and pointed his conversation at "Do you need my help again?", asked of someone who had just recruited him.
Nothing anywhere in his tree could dismiss him: the reply that says "No, wait here" carried no action at all.
Both fixed, and rejoining now restores the escort AI too.

His companion race carried melee 200 - a finished, strong offence - against HP 150 and AC 145, which made him
the weakest companion in the game, placed in the final act, behind Grace at 165/190 an act earlier. The plain
Knight of Saladin race is AC 100, so the upgrade had started and stopped, exactly as the Priestess line had. The
defence is repaired and the offence left alone.

## The last act learns who arrived at it

Every gate in act 8 was a skill or karma threshold. Of seventeen title perks in the game, one was read anywhere
in the act. The four crusading orders were read only to choose which greeting the Knight of Saladin spoke.

So the Old Man gets a line of defiance per order, each out of that order's own history with the Assassins:
Saladin's tent and the two knives that found nothing in it; the Temple's sixty years of tribute paid to keep
those knives away from its chapter houses; the Inquisitor who has burned men for a tenth of the heresy he has
just heard; the Wielder whose own passenger has at least never lied to it; and the Goblin Champion, counting
himself the Great Khan's second attempt after the warriors who never came home. And the Knight of Saladin
finally answers the order he already greets.

## Three things that turned out to be fine

Not everything that looks cut is cut, and saying so is part of the job. Twelve ending trees are opened by
nothing - and the ending matrix is entirely alive inside the trees the final map does open, with all fourteen of
its outcome relays firing. The Old Man's orphaned escape line is a superseded draft of the one that does play,
recorded twice because it was rewritten after recording. And both dragons are placed and fought; the two dragon
templates placed nowhere are discarded drafts worth no experience, one of them not even a chaos dragon despite
the name.

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt.

Download, unzip, run `Mod Manager.bat`. Most of this is level parts, so it needs a character who has not yet
entered act 8 - and the goblins need one who reached Goblin Champion out in the Wilderness. Unplayed; what you
find goes into 0.20.1.

With this release every act in the game is surveyed, built and published.

https://github.com/EricHype/LionheartFixt/releases/tag/v0.20.0
