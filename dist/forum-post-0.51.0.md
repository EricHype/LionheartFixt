# Lionheart Fixt 0.51.0 - magic ammunition that could never drop

This game has six enchantments for arrows and bolts: acid, cold, fire, poison, extra damage, and a
better chance to hit. They're fully implemented. They work.

**Enchanted bolts have never dropped anywhere in Lionheart.** Enchanted arrows drop in exactly one
place: a single sewer entrance.

## Two identical pools, both orphaned

There's a loot pool for magic arrows and another for magic bolts, and they're twins — the same base
ammunition drawn against the same six enchantments at the same odds. The arrow pool is used by one
map. The bolt pool is used by nothing whatsoever.

## But the real problem was somewhere else

I'd written this down as "the last loose end" — one unreferenced file, a quick fix.

**That was too narrow.** The file those two pools are supposed to feed is the one that handles
ammunition loot for **thirty-eight maps**. And it contained only this:

| | how often |
|---|---|
| a plain arrow | 60 |
| a plain bolt | 40 |

Ordinary ammunition and nothing else, with two complete magic pools sitting right beside it, wired to
nothing at all. Fixing just the bolt pool would have left *both* of them effectively dead — the arrow
pool at one map in two hundred is barely better than zero.

## What it is now

| | how often |
|---|---|
| a plain arrow | 60 |
| a plain bolt | 40 |
| **an enchanted arrow** | **6** |
| **an enchanted bolt** | **4** |

So about **one ammunition drop in eleven** is now enchanted. The pools always add an enchantment
rather than sometimes doing so, which means that weighting is the *only* thing setting the rate — if
it turns out too generous or too stingy, it's one number to change.

The sewer generator that used to give only magic arrows now gives either, so the twins match there
too.

## Fair warning: this one reaches further than the rest

Everything else in the recent run of releases touched one encounter, one item, or one conversation.
**This touches a file that thirty-eight maps draw on.** What it changes is the loot economy, not a
scene.

So the question I care about isn't "do magic bolts appear" — it's **"do ordinary arrows still turn up
as often as they used to"**. If most of your ammunition is suddenly enchanted, the number's wrong and
I want to know.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Works on **any save**.

## If you play it

**The check that proves it:** collect ammunition for a while and see an enchanted bolt. That's a
thing this game has never produced.

**The check that matters more:** keep an eye on whether plain arrows and bolts are still the normal
case. Roughly ten in eleven should be ordinary.

**And the judgement call:** after a few hours, does one in eleven feel right? Too many and elemental
ammunition stops being interesting; too few and these six enchantments stay as good as missing.
