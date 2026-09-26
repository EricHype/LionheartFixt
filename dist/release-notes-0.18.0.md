**Read this first.** Nothing in this release has been played, and neither has 0.17.0, 0.16.0, 0.15.0,
0.14.0, 0.13.0 or 0.12.0 before it. Everything passes the automated gate and `docs/releases.md` records
what each piece was read against. If you would rather wait for a build somebody has walked, wait for
0.18.1.

## The Barcelona Attack

Act 6. Eight maps, 2,897 level parts, 889 live combatants -- and **28 player replies in the whole act**,
of which two were gated on anything. It is the shortest act in the game and the one with the least left
in it, so this release is less about unreachable branching than about a city that never reacted to the
person walking through it.

## The densest map in the project had nothing to say

`Crossroads Siege` is 910 parts and **472 live combatants** -- four times the Crypt's Doomed Plateau --
with no conversation, no balloon and no dialogue tree at all. It has three narration lines now, each on
ground the map itself proves walkable: what the field is when you arrive from the city, what the standard
driven into the stones at the centre is, and what the road west looks like.

`Attackers dialog balloons` -- the relay that makes English soldiers shout while they fight -- exists on
both district maps and **did not exist on the one map the English army is actually on**. It is ported
there, on timers on six of the thirty-four English generators.

## Two quests that were never written, and one that was

`Find Galileo and DaVinci.Quest.txt` shipped with a **blank `Name=`** and `Item Count=0`: the file was
created and never filled in. The True Cross pursuit has a name and no states. Neither was referenced by
any map or tree in the game, so the act announced one objective and silently dropped the two that frame
it.

The blacksmith is the man to ask, and he was already there. He now also answers what happened to the two
men who used to buy his work:

> Gone, my friend. *He puts the hammer down, which he has not done since you came in.* The Druids came
> up that street with a list, and they did not stop to sack either workshop -- they went in, they took
> the two of them, and they went out the west gate with them walking.

*This is that road.* With the quest active, the line at the western end of `Crossroads Siege` becomes the
evidence instead: a cracked lens ground finer than any glazier in Barcelona could manage, and beside it a
wax tablet pressed with a hand you have watched draw. 1500 XP, once, for having looked. Without the
blacksmith's answer you get the plain line and no reward, which is the right way round.

Recorded and not built here: **Inquisitor Raphael's act-1 half of the same thread** -- *"They have stolen
the True Cross from the Cathedral! ... They are retreating to the west. Hurry!"* -- which is reached by
nothing and opened by nothing. The theft, the pursuit and the recovery were written as one thread across
acts 1, 6 and 8, and only the item at the far end was ever wired.

## Slayer of Innocents

`Perks/!Event Title Perks/Child Killer` ships complete: a display name -- **Slayer of Innocents** -- a
description, and a `Requirements` array holding a deliberately false expression, which is how this game
marks a perk only script can grant. **Nothing in the game grants it.** It is read eight times on the
peacetime Gate District, and those reads drive five fully authored dialogue nodes with two replies each --
deny it, or *"I am the killer. You should back down before I kill you."* None of it has ever fired, in
any playthrough.

Children are **not** made killable and that is not what the perk says: `Generic Child` is HP 10000 /
AC 1000, `Barcelona Boy` sets `Has Hit Points=0` on top of that, and the Gate District's only boy sits on
a part named `Child Leaving` with `Active=0`. The invulnerability is deliberate and it stays. The perk's
own words are *killing the helpless*, and the helpless who can be killed are the citizens at HP 12. So the
title is awarded from **34 citizen generators** across the Gate, Temple and Port districts, on the exact
idiom `Merchant Slayer` already uses 28 times.

Then act 6 reads it. The two checker parts the whole mechanism runs on were **already sitting on
`Gate District Siege`**, active, carrying the designers' own comments on the polarity -- and act 6 neither
read nor wrote either one. All five spawn points run the peacetime check now, and the man searching the
district for his son reads the result:

- **a child killer** gets `21 Children` as shipped: *"Leave me alone! Haven't you done enough?!"*
- **anyone else** gets a father asking you to look for a boy in a red cap

**And there is a red cap to find.** Phillipe is behind a barrel on a vertex of the citizens' own patrol
path, told to stay where he was put. *"Papa said stay where you are put, so I am put. Everybody who ran
past me was running the wrong way. Is he coming?"* Tell him where his father is and he goes, for 1000 XP.

## A witness with nobody to witness

`Gate District Siege` carries a relay called `Shy Girl requests help` -- active, once-only, which balloons
*"Ayudame! Help me! Guards!"* over an entity named `Shy Girl Near Murder` and then fires
`Damage a guard in the city district`. Nothing called it. **Neither of the two names it needs existed on
the map.** It is a remnant of a scene the peacetime Gate District has in full.

All three pieces are back, and the consequence end is the map's own: every defender generator already
adds a `GoToCombat` handler that fires `Spaniards Attack Player`, so attacking a guard turns the garrison
and hands you +40% AC for the trouble. Murdering an unarmed civilian produces no such message -- which is
exactly what a witness is for. Only civilians arm the scream, because the English kill defenders all
siege long and the garrison should not blame you for the siege.

Left alone deliberately, with the reasoning recorded: `defenders hate player trigger`, on both siege maps,
inactive, activated by nothing, pointed at a name no entity carries. Its own comment describes the
localized draft that `Spaniards Attack Player` replaced and wired.

## The men nobody could hear

Six dying-soldier lines; the act opened four. The two it never opened are the two best:

> Stranger...here...take my gold. Don't let those English have it...

> I am sorry Espana...I do not know why we came with swords drawn and bloodlust in our hearts...

The Spaniard hands over the 250 gold he is talking about. And `Temple District Siege` had **62 dead
bodies and not one of them speaks** -- the whole map opened a single node of that tree, its arrival bark.
Six of its bodies have voices now, three Spanish and three English, spread west to east.

## The act learns to read you

Across eight maps act 6 read the player three times: `PE 8+` and `Speech 70` on Surrey O'Connell, and a
`Sneak < 100` check on the chest he guards.

Surrey is the act's one negotiation and its best-written character: an Irish supplies master pressed into
feeding the army that took his country, who calls himself *"happy I am to serve the English"* and begs not
to be sent to the Spanish Inquisition. Two things he says out loud are levers the act never pulled.

**The Clover from the drowned fields of Ireland** -- the token the Port District's Irish sailor hands over
in 0.9.1 -- stops the performance dead:

> *He does not take it, and he does not look away from it either.* Ah. Ah, now. Where did a body like you
> come by that. Drowned. The whole of it drowned, and I am out here weighin' out bolts for the men that
> let it. Go on then. Take what ye need off the Regent's pile, and Surrey O'Connell never saw a thing,
> and never heard a lid.

A **sworn Inquisitor** gets the same look-away by a shorter road. Either one and the alarm on the Regent's
chest -- the relay that makes him shout, wake the chest guards and turn on you -- simply does not fire.
Two new routes past the act's one guarded prize, beside the Sneak 100 vanilla shipped.

The **blacksmith** gets three reads on a conversation that had none: a Templar or an Inquisitor hears what
the two orders lost in the district (*"I shod horses for half those men"*), a tainted face meets a man
with no attention left to flinch (*"This morning I watched a thing made out of ice walk through the front
of the Alvarez house with the family still in it. You are a man with a face."*), and a player carrying
Slayer of Innocents gets him weighing the hammer, setting it aside, and selling to you anyway: *"Do not
come back after the city is standing."*

## The emptiest map in the project

`Church Crypt Interior Siege` was thirteen parts: three wall pieces, a lamp, a broken door, one dead city
guard, nothing else. It has the act's **first secret, first trap, first hidden lock and first voice**: one
slab in the wall newer than the others, grey mortar where the rest is black, put in from this side by
somebody who knew the English were on the road; the sacristan's plate in a chest behind it; and poison gas
on the slab, set so that a thief can see it coming and take it out. The guard on the stair can be looked
at, sword still in his hand, feet toward the stair.

---

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt. Every check adds a
route and none removes one, so the vanilla solution to every scene still works.

Download, unzip, double-click `Mod Manager.bat`. Most of this is level parts, so it needs a character who
has not yet entered act 6 -- and the Slayer of Innocents title needs one who has not yet entered the
peacetime Gate, Temple or Port districts either. Test list: `docs/qa.md`, rows BA1-BA56.
