**Repair only.** Nothing new is added and nothing is removed. If you are already on 0.18.0 you can install
this over it; the only change is where one title comes from.

## Slayer of Innocents, on the hooks the designers built for it

0.18.0 restored a title the game describes, reads eight times, and had never once awarded:
`Perks/!Event Title Perks/Child Killer` -- display name **Slayer of Innocents**, *"TITLE PERK: Killing the
helpless is what you like to do."* It hung the award on murdering an unarmed citizen, because children
cannot be killed: `Races/NPCs/Generic Child` is AC 1000 / HP 10000, and **every child in the game uses that
one race** -- the woodcutter's daughter, Marisol, Tomas, the shepherd's son and the Gate District boy alike.

That reading was the best one available without knowing about the mechanism the designers *did* build, which
a question about the game's three child-rescue quests turned up. **Each child's generator carries a working
`CSetDamagedScriptActionAction`.** Children cannot be killed, but hitting one has always been detected, and
always had consequences:

| child | map | what the hook already did |
|---|---|---|
| Woodcutter's daughter | Scar Ravine | screams *"Ahhh!"*, flees to `girl leave safe`, turns `Goblin guarding girl` on you, deletes the entire peaceful-resolution script set, fails *Find the Woodcutter's lost son*, activates `daughter attacked` -- which the woodcutter's own dialogue reads -- and reaches across maps to delete her generator at the house, so she never turns up home |
| Woodcutter's daughter | Woodcutter Home interior | the same, at home |
| Marisol | Port District | screams, flees to `Marisol disappear location`, fails *Find the lost boy Tomas in the Sewers* |
| Tomas | 05 Troll Pit | screams, strips his talk specifier, flees |
| Shepherd's son | 01 Hamlet Exterior | screams, activates `Player hurt the son` and `Make Maury mad for hurting son` |
| Barcelona Boy | Gate District | the `Child Leaving` boy |

Five children, six placements, every hook doing real work -- and **not one of them touching the title the
game wrote for exactly this.** The grant sits in all six now, appended to each hook's own action array with
every vanilla action left in place: the quest failures, the flags, the fleeing and the goblin all still
happen, in the same order.

**Everything downstream already worked.** The grant reaches the Gate District guards' `2 Childkiller Intro`
-- *"There have been reports of a monstrous killer of helpless children...you loosely fit the description.
Why should I not bring you before the Inquisition?"* -- and its second reply, *"I am the killer. You should
back down before I kill you."*, fires both `Damage a guard in the city district` and `Child killer bubble
text`, the guard shouting **"Have at thee, monster!"** before the district turns on you. Five authored nodes
across two guard trees, and the grant was the only link missing since release.

**The hooks cannot misfire.** On all four maps involved, every `Valid Targets` is some combination of
`Player`, `Player Friend`, `Enemy` and `Scripted Custom N`. Nothing can target a neutral, which is what
every child is -- so only the player can ever trigger one, and the goblin standing over the daughter and
the trolls standing over Tomas cannot earn you a title.

**Children are still unkillable, and still will be.** That invulnerability is a deliberate shipped decision
and this mod does not touch it. The perk's own words are *killing the helpless*, and the citizen grant from
0.18.0 stays alongside the new hooks for that reason -- a murdered citizen is one of the helpless too, it is
the idiom `Merchant Slayer` already uses 28 times, and it is what gives act 6's witness scene its
consequence. **40 grants in total**: 34 citizen generators and 6 child hooks.

## And one correction to 0.18.0's notes

0.18.0 said that `Barcelona Boy.can` sets `Has Hit Points=0` "on top of" the race presets, as though it were
a second layer of protection. It is not. **All 247 character templates in the game set `Has Hit Points=0`**,
including the HP-12 citizens that release makes killable for the title and the HP-1 barstool patron in the
Port District tavern. It is a level-part field about object hit points, not character invulnerability. The
race presets are the only thing protecting children, and `docs/releases.md` now says so.

---

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt.

Download, unzip, double-click `Mod Manager.bat`. These are level parts, so the new hooks need a character
who has not yet entered Scar Ravine, the Port District, the Troll Pit or Montaillou. Test list:
`docs/qa.md`, rows BA26a-BA26h.
