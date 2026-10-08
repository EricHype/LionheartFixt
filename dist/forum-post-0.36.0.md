# Lionheart Fixt 0.36.0 - The Templar Set

This started with a question: *"what are the other unused items? I didn't know the mine deed existed.
We should be able to find usages for all of them eventually."*

So the first thing in this release isn't content. It's a **written survey** of everything the shipped
game defines and then never uses, so nobody has to work it out again — and the second thing is the
first pair of items taken off that list.

## What's actually unused in Lionheart

| | |
|---|---|
| **8 quest items** | hand-written, with descriptions, placed nowhere |
| **48 enemies** | nothing in the game spawns them — and **all of them have working art** |
| **2 whole summon tiers** | `Monster Summoning` levels 4 and 5, six finished creatures |
| **5 title perks** | nothing in the game awards them |
| **3 wand enchantments** | the only magic items genuinely lost |
| **0 skills** | nothing was cut — the spell system is complete |

The two that stand out: **a level-5 summon that puts a Rock Titan on the field**, finished and
unreachable — and **three of four "Enemy of the…" title perks are unconnected** while the fourth works
perfectly, sitting right beside them.

It's all in `docs/unused-content.md`, including the parts I got wrong on the way. One early pass
claimed 93 creatures had broken stat references and that it was a bug in the original game. It wasn't
— it was a bug in *my check*, which was case-sensitive about a file extension. The real number is
zero. That's in there too.

## The helm was never finished

`Helm of the Templars` — *"This battle-weary helm shines with the power of the Templars."*

It's a **helmet** that was wearing a shield's clothes. Its ground model was a shield. All three of its
inventory icons were a shield. It sorted with shields in your bag. Someone cloned the shield item,
changed the name and the slot, and stopped — which is almost certainly why it was never placed
anywhere in the game.

Repaired using the game's own ordinary helmet as the reference, so it now looks like, sorts like, and
behaves like a helmet.

## Then it turned out both pieces did nothing at all

I only found this because I was asked what the stats were.

**Neither item had any effect whatsoever.** The only thing either of them did was make a noise when
you picked it up. No armour. No resistances. Nothing. An item described as shining with the power of
the Templars was **worse than a plain helmet off a dead thug**.

My first attempt at fixing that was also too timid — I matched them to ordinary gear of the same
weight, and was rightly told they'd be outclassed by things you find in act 1. Second attempt, priced
against the **best** gear those slots can hold:

| | |
|---|---|
| **Helm of the Templars** | **+6 armour**, **+1 Luck** |
| **Spirit Templar Shield** | **+8 armour**, strong piercing, slashing and crushing protection, **+5 one-handed skill** |
| **wearing both** | **+4 more armour** |

**+18 armour for the pair**, where those two slots would normally cap out around +10. The shield beats
the largest shield in the game while weighing **half** as much — that's the set's character: it
protects like a tower shield and carries like a buckler.

## There is a real set bonus, and I nearly missed it

Asked whether the two pieces could reward you for wearing them together, I said the game had no way to
do it. I was wrong, and I was told so.

**The Voodoo belt and necklace already do exactly this.** Wear one, nothing; wear both, you get an
extra skill point every level. The game doesn't check what you're wearing — it *counts* it, and reads
the total. I'd been searching for the wrong kind of thing entirely.

The Templar bonus is built the same way, from the same pattern. And finding it had a bonus
consequence: it turned up a **goblin kill counter** that's already live in the game, which means the
unawarded `Goblin Slayer` title is far easier to restore than I'd thought.

## Where to find them

On a **dead Knight Templar in the burned hamlet**, act 3. There are two such corpses and no others,
which keeps the set rare.

This works on **any save that hasn't been into that map yet** — it changes a character, not the map
itself.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

## If you play it

**The main thing:** find them, wear both, and tell me whether +18 armour and a set bonus feels right
for act 3, or whether it's too much. I priced it against the best gear in those slots, but that's a
judgement and you're the one playing it.

**One number has no precedent and I'd like a second opinion on it:** the **+1 Luck** on the helm. No
other item in this game grants a flat attribute point — and Luck quietly feeds your critical chance,
your fortune, and three of your resistances. One point moves several things at once. If it feels
disproportionate, say so and I'll pull it.

**Two safety checks, please.** Make a character wearing neither piece and confirm your armour class is
exactly what it always was — the set bonus had to be wired into a core stat every character shares.
And take the helm **off** and confirm your Luck goes back down.
