# Lionheart Fixt 0.38.1 - magic loot now respects where you are

0.38.0 made magic equipment drop for the first time. It also shipped it **completely ungated** — a
legendary ring could have turned up in the Gate District in the first hour.

That was in 0.38.0's own test notes as an open worry rather than something I'd fixed. This fixes it.

## Why it needed fixing

The original game's enchantment lists do make rare things rarer — but only gently. A `Unique` ring and
a `Common` ring sit at the **same weight** in a couple of cases. Nothing stopped the best items in
their slot appearing immediately.

## How it works now

Magic equipment steps up at **exactly the same points armour already did** — I read the thresholds off
the game's own armour generator rather than picking numbers.

| where you are | what magic equipment you can find |
|---|---|
| **early — Barcelona, the sewers** | **amulets and rings only**, nothing above Uncommon |
| **mid — Montserrat, Montaillou** | all six slots, up to Rare |
| **the Crypt onward** | everything, including Very Rare and Unique |

Nine of the forty enchantments are available early. Twenty-two by mid-game. All forty from the Crypt.

I also used the game's own technique for this: its low-tier armour list doesn't *remove* plate mail,
it keeps it listed at zero chance. These do the same, so the tiers stay comparable to what they came
from.

## Why no magic belts or helmets early

You'll find magic amulets and rings in act 1, but no belts, bracers, cloaks or helmets — and that
isn't me being stingy.

**Every single enchantment for those four slots is Rare or better in the original game.** There is no
such thing as a plain Uncommon belt enchantment. So those slots simply have nothing to offer at low
level, and they start appearing once Rare items do.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Works on **any save**. If you installed 0.38.0, this replaces it and you want it.

## If you play it

**The check that matters:** find any magic equipment in act 1 and look at its rarity. It must never
read above **Uncommon**. If something Very Rare or Unique turns up early, the gate isn't working and I
need to know.

**And the judgement call:** do magic items and armour now feel like they improve together as you go?
They share thresholds exactly, so they should — but that's the sort of thing you only notice by
playing it.
