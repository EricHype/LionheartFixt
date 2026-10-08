# Lionheart Fixt 0.38.0 - Magic Items Now Drop

If you've ever felt that Lionheart's loot was thin — that you found an awful lot of plain rings and
plain helmets and not much else — you were right, and here's why.

## Magic equipment didn't drop in this game

Not "rarely". **Didn't.**

The original game has a random item generator that most dungeons draw from. Follow it down to the
"miscellaneous items" branch and it gives you exactly two things: eight kinds of **plain,
unenchanted** equipment, and magic scrolls.

The parts that attach an enchantment to a ring, an amulet, a belt, a bracer, a cloak or a helmet all
exist. They're written, they work, and **nothing in the game pointed at them.** Forty enchantments,
built for those six slots, that no player has ever seen.

Wands were one broken link from the same fate — their pool was pointed at by one file, and nothing
pointed at *that*.

## Now they're connected

Magic rings, amulets, belts, bracers, cloaks and helmets can drop. Wands can drop — sixteen different
kinds, where the original game only ever placed one by hand.

**I kept the change proportionate on purpose.** The obvious approach — connect all six pools
separately — would have made magic equipment about **36%** of that branch's drops. Instead they go
through a single gate that gets the same share scrolls and wands get:

| what drops from that branch | share |
|---|---|
| plain equipment | **74%** |
| scrolls | 9% |
| wands | 9% |
| **magic equipment** | **9%** |

Plain gear still dominates, exactly as before. And I checked all forty enchantments are genuinely
implemented before wiring any of them in — which turned out to matter, because some other things in
that folder aren't.

## A new unique wand

**Wand of Swarm** — summons a swarm of insects, and protects you from arrows while it still has
charges. It's the rarest tier, so don't expect to find one quickly.

## Two wands I left alone, and I want to be straight about why

There are two more unique wands in the same folder, with tempting descriptions:

- **Wand of Fire and Ice** — *"cast Fireball and Ice Storm at the same time in the same place"*
- **Wand of Mage** — *"4 skill points in all base magic skills in all 3 spell categories"*

**Neither of them does anything.** They're descriptions with nothing behind them — no effect, no
mechanism, nothing. The Fire and Ice wand is even priced at **zero gold**, which is the tell. Someone
wrote down what they wanted and the work never happened.

I could have added them to the loot pool. You'd have found a legendary wand, equipped it, and
discovered it was a paperweight. That's worse than never finding it.

Making them real means *building* them from those descriptions, and the Mage wand as written would be
the strongest item in the game by a wide margin — the best enchantment in Lionheart gives +8 to one
skill, and that wand promises +4 to **all** of them. That's a design decision, and it's yours to make,
not mine to slip into a release about wiring.

## Installing

Unzip and double-click **`Mod Manager.bat`**, then click the button that names the mod.

Works on **any save**.

## If you play it

**The headline:** play the Crypt or Alamut and watch the floor. Magic rings, amulets, belts, bracers,
cloaks and helmets. None of these have ever dropped.

**The one I most expect to need tuning:** does loot now feel *too* generous? Magic equipment is 9% of
one branch of one generator, and that number is the dial. Tell me if it rains.

**And a harder question I don't have an answer to:** I didn't add any level-gating. The enchantments
carry the original game's own rarity tiers, but nothing stops a Very Rare ring turning up early. If
you find something absurd in act 1, that's worth reporting — the armour and weapon lists gate by
progression, and this branch doesn't.

Two sanity checks if you have the patience: plain equipment should still be the common case, and
potions and scrolls should be exactly as they were.
