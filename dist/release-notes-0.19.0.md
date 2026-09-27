**Read this first.** Nothing in this release has been played, and neither has 0.18.1, 0.18.0, 0.17.0, 0.16.0,
0.15.0, 0.14.0, 0.13.0 or 0.12.0 before it. Everything passes the automated gate and `docs/releases.md`
records what each piece was read against. If you would rather wait for a build somebody has walked, wait for
0.19.1.

## The English Shrine

Act 7. Eleven maps, 3,481 level parts, 2,035 live combatants — and the tester who has played it calls it the
worst section in the game: *all combat with the same 3-4 enemies, and nothing to do but wander and fight.*

That is measurably true. **`Soldier` alone is 1,496 of the act's 2,048 spawn entries — 73% of everything in
it** — and the act fields 19 enemy families against the Crypt's 82. Between fights there were two
conversations in eleven maps, one quest with one state, and one unique item.

My first survey of this act said the opposite, on a count of 47 secrets and 190 traps. Both numbers were my
own greps' noise: `(?i)trap` matches `Found Trap` and `Disarm Trap`, so every trap counted itself four times,
and 37 of the 47 "secrets" were **traps being spotted** rather than hidden areas. The real figures are 37
traps and 10 hidden areas across eleven maps. Where a metric and a playthrough disagree, the playthrough is
the evidence.

## The act's own enemies were placed nowhere

The shrine's enemy faction is the **Druids**. The one line a rank-and-file enemy speaks is *"Intruder! You
won't stop us from awakening the dragon!"* And the `Druid` template in act 7's own folder is **fielded
nowhere**, so every druid in the act is a generic English soldier. `Monster Cans/English Enemies` holds three
**`Priestess`** templates placed nowhere in the entire game — while `Druid Master`, the act's boss, has the
race `Priestess Super`. The order she leads did not appear in its own shrine.

They are in now: 195 weighted entries added to existing generator groups across nine maps, so **no spawner
count changes and no vanilla spawn was dropped**. Placement is deepest-first — the front of the act stays an
English army holding a shrine, and the further in you go the more it is actually the cult. Families 19 → 21,
`Soldier`'s share 73% → 67%.

**This raises XP by about 15%** over the maps touched, concentrated in the deep rooms (+40–54% on the three
smallest). A `Druid` has the *identical race* to a `Soldier1` and pays 950 XP against its 348. The weights are
one table and can come down if it plays too rich.

## The boss was weaker than her own guards

The Priestess line shipped unfinished. The Priest ladder runs HP 80/110/150, AC 230/250/280, resistances
50/60/65%. The Priestess ladder ran HP 75/84/95, AC **260/80/150**, and **no damage resistance at any tier** —
the AC falls 180 points from base to Tough and never recovers.

Their *spell* identity was the finished half, and a good one: `Priestess Super` carries four offensive spells
including `Static Charge`, which no priest gets, plus Evasion. So the repair keeps that and fixes only the
defences — +30 AC over the priest at every tier, about 90% of his HP, his resistance values, and deliberately
**not** his `ENEMY Magical Shield`, so priests shield and priestesses out-damage and dodge.

And the Druid Master shipped **sharing the rank-and-file race**: HP 95, AC 150, no resistance — against an
`Assasin Master` on her own map at HP 400 / AC 305, and act 5's Nostradamus at HP 500. Her attendants paid
1,949 XP to her 1,100. She now has her own race at **HP 350, AC 300, 65% resistance**, her four spells at 130,
and 2,500 XP.

## Eleven maps with no shop

The Templar alliance amounted to **three knights and Sir Roger** — and act 7 had no merchant on any of its
eleven maps, so a player who ran dry in the Stone Chamber had eight maps to go and nothing to restock from.
Sir Roger's own acceptance line already promised more: *"My men will spread out and clear the area."*

Two Templar posts now, at the ends of the act's spine, staffed from the act's own unplaced `Knight Templar`
template: a quartermaster, a field surgeon, and a guard who finally speaks the one dialogue tree in the act
that nothing opened — *"My sword is yours."*

- **The surgeon heals free for a Templar or a Knight of Saladin**, and charges everyone else 200, *including a
  sworn Inquisitor* — the Inquisition is Spanish and ecclesiastical, not his brotherhood.
- **The stock reaches back six acts.** Three windows, chosen by the same three quest checks Quinn the
  herbalist uses for his own reserve. Run his errands in act 1 and the Order is still selling what you
  unlocked — Great, Superior and Supreme Healing — in act 7.
- **The whole post is gated on having accepted Sir Roger's help.** Refuse him — *"I am not interested in help
  from any Englishman"* — and there is no camp, no shop and no surgeon. That reply cost the player nothing
  before this.

## Helping Guy Fawkes finally means something

Act 1's conspiracy is a ten-state thread in which you can renounce the Inquisition, swear to the Queen, take
the Armada's plans off Captain Isabella and murder the Duke of Medina. It promises a great deal — *"your
service to England will not be forgotten"*, *"the Queen Mother herself knows of your valor"*, *"gold from the
Queen herself"* — and the allegiance was **stored nowhere**. No perk, no checker. The only later act that
touched the quest was act 6, whose sole action on it is to fail it in a bulk list: the one downstream reference
deleted the record.

**Servant of the Queen** is granted now, at the two endings where Fawkes parts on good terms, and read in the
country it was sworn to. Sir Roger — an English Templar whose enemy is the Queen's own druids — tells a player
who carries it what that means:

> Then you know more of this than I was going to tell you. **The Queen keeps druids, Lionheart.** She has kept
> them since before she had a throne, and what they bring her she does not ask twice about. My Order came to
> this shrine without her leave and we will be told off for it if we live.

And **Surrey O'Connell** gets a third route past the Regent's chest, beside 0.18.0's clover and Holy Office —
deliberately the coldest of the three. He is a pressed Irishman who mocks the Crown, and a player wearing the
Queen's favour is who could hang him for it: *"Do not say my name where anybody writes things down."*

Also repaired in act 1: *"I'll lure the Duke to the trap."* had an **empty destination**, so accepting the
darkest job in the act ended the conversation without a word. The answer written for it — *"you will be
remembered forever in English history"* — plays.

## Grace O'Malley comes ashore in England

The largest find in the act. `Captain Isabella generator` sits inactive on the landing beach, and her tree
carries a complete, **voice-recorded** arrival-in-England arc whose **eleven orphaned nodes** nobody could
reach: the hostile arrival, the friendly one, a romance, a release-and-rejoin cycle, and combat barks including
**"For Ireland."**

She is **Grace O'Malley**, the Irish pirate, posing as Captain Isabella for two years — so the woman who sails
you to England is an Irish rebel against it. And her `503 druids` says what act 7 needed: *"Once they fought
the English with us, but now they have formed an alliance with the Queen."*

The beach reads three ways off act 1: drive her off or turn her in to the Duke and she is not there at all;
hear her out and keep her secret and she is glad to see you, and can join; anything else and she attacks.
Her body is Sir Roger's companion machinery, cloned — and act 7 spawns her on **her own race at HP 165 / AC
190**, because her act-1 template is HP 36 and every enemy in act 7 would have killed her in seconds.

**And act 1 got the beat the romance was missing.** Her arc there is political throughout, and the only
warmth in it was one line, so *"My love, know that my blade and my heart are yours"* was a long way to travel.
There is now a scene after she is spared — *"in all that time not one person has asked me why — they only ever
asked me whether"* — and answering it is what act 7's romance requires. Take her bribe, lie to her, or never
ask, and it is not offered.

**Two recorded lines were also renamed out of reach.** VO lookup is by node ID; 36 of her 38 files matched a
node and two did not, so the game looked for audio and found none. Renamed back, **all 38 of her recordings
are reachable** — and both companions' trees now have **zero orphan nodes**.

## Eight barks that had never played

Sir Roger's *"For England!"*, *"For The Queen!"*, *"For The Templars!"*, *"We shall Prevail!"*, *"On my
honor!"* — and Grace's *"I need healing!"*, *"For Ireland."*, *"We cannot fail."* Plus her two recorded health
barks, on a threshold trigger at 60% and 25%. A companion walks between maps, so these ride on the character's
own AI list rather than a map relay.

## And the Inner Sanctum was a vault nobody could see

210 parts, 88 combatants, and **not one word on the map** — no tree, no balloon, no label printer. It is a
three-switch vault: three worn stones in one corner opening three doors scattered across the room, two of them
ambushes and one of them **two chests of the best loot in the act outside a boss**. The doors are up to 800
units from their switches, so a player who found one and pressed it got no feedback at all. It says what it is
now, the switch corner says what is in the wall, and each stone reports what it opened and how many are left.

---

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt. Every check adds a
route and none removes one, so the vanilla solution to every scene still works.

Download, unzip, double-click `Mod Manager.bat`. Most of this is level parts, so it needs a character who has
not yet entered act 7 — and Grace's arc and the England allegiance need one who has not yet finished act 1's
Port District either. Test list: `docs/qa.md`, rows ES1–ES58.
