**Read this first.** Nothing in this release has been played, and neither has 0.16.0, 0.15.0, 0.14.0,
0.13.0 or 0.12.0 before it. Everything passes the automated gate and `docs/releases.md` records what
each piece was read against. If you would rather wait for a build somebody has walked, wait for 0.17.1.

## The Caverns of Nostradamus

Act 5. Ten maps, 5,178 level parts, **1,130 live enemy spawners** -- four times the Crypt -- and two
quests with **no way into either**.

Both hang on one conversation. `Player sides with the Hujark` fires from a single reply in the entire
game, in the Hujark General's tree; `Player sides with the English` fires from seven more of his nodes
and from a relay whose only callers are his generator and his guard's. **All of those were switched off
and activated by nothing.** So every player who has ever walked act 5 fought the Hujark, on a map set
built to be populated either way, and the Demesne's arrival trigger has been completing two quests that
could never be activated.

**Huko spawns now.** His generator is live, his guard has a name to be activated by, the arrival spawn
point calls him over, and his template's talk specifier -- which shipped with an empty action -- opens
the conversation. His return dialogue, seven replies including both ways to commit, was reachable from
nowhere.

## The army that was built and never placed

There is a folder in the shipped game called `Resources/Monster Cans/English in Caverns of Nostrodomus/`.
It holds fourteen units made for this act: `Nos Soldier1`, `Nos Soldier2`, `Nos Soldier2 Bow` and
`Nos Soldier3` in three tiers each, plus two English ogres -- complete templates, real XP, real races.
**Every one of them is placed nowhere.** The English army was designed, statted, tiered, given archers,
and never given a generator to come out of.

It has ninety-nine now, twinned from the generators that already field the Hujark so that every soldier
stands where the game already spawns a swordsman. And it is a **swap, not an addition**: each twin ships
inactive, and siding with the Hujark both raises the English and stops a hundred Hujark generators from
targeting you.

## Three ways through, instead of one

| | Hujark | English | escort | journal |
|---|---|---|---|---|
| help the Prophet | stand aside | hunting you | a Hujark soldier calling the advance | *Protect Nostradamus* |
| fight for the Lance | hunting you | off | an English soldier | *Defeat the Hujark defenders* |
| **safe conduct**, Speech 75 | stand aside | hunting you | none | nothing |

The third is new. Huko will sell you passage, and he is precise about what he is selling: *"My men will
not touch you, because I will tell them not to, and that is the only thing in this cave I am able to
promise you. The Druids are not mine to call off."* So the English come on exactly as they do for an
ally, and nobody narrates for you, and **the deal is revocable** -- raise a hand to one Hujark and the
word is in the next gallery before you are.

And if you are carrying the **Child Killer** title, he will not take your help at any price. There are
children in these caves. The passage is still for sale; the alliance is not.

## The seer defends himself

`Nostrodomus Attack Preparation` has always been live and fired by nothing. It turns Nostradamus
hostile, starts a timer, and calls a monster summoning; the timer drives four ranged spells, lightning
and celestial smites cast across the chamber. He has a taunt for being struck, one for the fight, and a
line for beating you. **Strike him in the shipped game and he stands there and takes it.** Not any more.

He also reads a great deal he never read: the spirit you carry -- he is a man joined with one and says
so -- your school, whether you have put spirits in bodies yourself, and whether you read the sky.

## Two tiers of summoning the act documented on its own checkers

A checker on nine maps carries a comment in the shipped game: *"This checker enables shield-helmet
swordsmen to summon snakes from the clone gen."* It was read zero times. A second checker,
`snakebreed summoning enabled`, was read zero times beside a generator that fields a Mongol archer, an
ogre, a bear, a vodyanoi, a wolf, a ghoul and, at the top of its table, a **Rock Titan**.

Both are wired. A shield-helmet swordsman or a cave shaman at half health calls a serpent; a snakebreed
summoner at a quarter health calls something much worse. **Carry Sahar's ring from 0.11.0 and the
serpents will not answer** -- they know her mark, and you are shown them refusing. The rock titan does
not care.

## Also

Forty-three traps, spotted and disarmed against Lockpick, in ten maps of caves that never held one. The
two maps with no voice of any kind now have four lines between them. The frightened apprentice stops
turning up alive on the next map after you have killed him, which his own relay was written to prevent
and nobody ever called. The battle commentary -- seventeen nodes of it, two of which vanilla ever opened
-- has a speaker on both paths. And the act reads race, spirit, magic school, perk and Speech, where it
read none of them.

## Installing

Download, unzip, run `Mod Manager.bat`. It installs over any earlier release. **Almost all of this is
level parts** -- Huko, the English army, the traps, the escorts, the summoning: they need a character
who has not yet entered act 5. The dialogue works on any save.
