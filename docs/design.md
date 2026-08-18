# Lionheart Fixt — design notes

Status: **planning**. Nothing below is built yet.

A large restoration-and-repair mod for Lionheart. Three goals, in priority order:

1. Fix what is outright broken.
2. Restore cut content that is good enough to ship.
3. Address the game's central design failure — the collapse of RPG content after Barcelona
   — including by writing new content.

This document records the diagnosis, which is measured rather than asserted, and the phase
plan. The work itself is broken down section by section and map by map in
[`lionheart-fixt-plan.md`](lionheart-fixt-plan.md). What actually gets packaged, under what
version, in what order, is in [`lionheart-fixt-releases.md`](lionheart-fixt-releases.md).
Content inventory lives in [`cut-content.md`](cut-content.md); modding technique lives in
the `lionheart-modding` skill.

**Two corrections to the table below, from the per-map survey.** The act table omits the
**Wilderness**, which is 43 maps -- more than any single act -- holding 825 authored nodes
and 31 quests, and is where the cut goblin content belongs. And its "dialogue nodes/map"
counts nodes *filed under* an act's folder; a player also meets whatever their companions
carry in, which roughly doubles the figure in the late acts. Both measures are in the plan
document, reconciled.

## The diagnosis, measured

Lionheart's reputation is that it opens as a strong RPG and becomes a combat corridor.
That is visible in the shipped data, taken from `data.dat.vanilla.bak`:

| Act | Maps | Dialogue nodes/map | Quests | Enemy spawns/map | Spawns per dialogue node |
|---|---|---|---|---|---|
| 1 Barcelona | 36 | **73** | **88** | 8 | **0.1** |
| Sewers | 9 | 19 | 16 | 133 | 6.9 |
| 2 Montserrat | 5 | 2 | 2 | 105 | **47.6** |
| 3 Montaillou | 17 | 64 | 17 | 51 | 0.8 |
| 4 Crypt | 10 | 9 | **1** | **284** | 30.2 |
| 5 Nostrodomus | 10 | 10 | 2 | 148 | 14.4 |
| 6 Barcelona Attack | 8 | 5 | 3 | 189 | 35.2 |
| 7 English Shrine | 11 | 4 | 2 | 180 | 40.4 |
| 8 Alamut | 11 | 14 | 1 | 86 | 6.2 |

Barcelona holds 88 quests; the Crypt holds one. Combat density rises 35× while dialogue
falls 8×. Montaillou is the one late act that holds its shape, which matches its
reputation as a brief return to form — and makes it the realistic bar to aim at, not
Barcelona.

### One correction to the usual framing

"Your character build stops mattering after Barcelona" is not quite what happened. The
*rate* of skill- and faction-gated replies barely moves:

| Act | Replies | Gated | Share |
|---|---|---|---|
| 1 Barcelona | 5820 | 2203 | 38% |
| 3 Montaillou | 2243 | 666 | 30% |
| 4 Crypt | 192 | 52 | 27% |
| 7 English Shrine | 91 | 21 | 23% |
| 8 Alamut | 202 | 34 | 17% |

The design did not change. **The content ran out.** 2203 gated replies in Barcelona
against 52 in the Crypt. This matters for the plan: the fix is more conversations, not a
reworked system. Speech, Barter, faction and gender gates already work everywhere.

## Principles

- **Measure before changing.** Every claim in this document came from parsing the vanilla
  archive. Do the same for any new one; three separate conclusions in this project were
  wrong until re-measured.
- **Vanilla is the baseline, not the install.** `data.dat` carries our own mods. Compare
  against `data.dat.vanilla.bak`.
- **Restore before inventing.** Cut content carries the original writers' voice, which is
  most of what makes an addition feel like it belongs.
- **Subtract carefully, add freely.** Removing enemies changes pacing and difficulty in
  ways that only play-testing reveals. Adding a conversation cannot break a build.
- **Every phase ships alone.** Each is a usable mod on its own and none invalidates
  another's work.

## Phase 1 — Repair the link rot

**84 replies point at node IDs that do not exist.** Choosing one advances to nothing: the
conversation silently stops responding, with no error. This is link rot — nodes renamed or
deleted late in development, links not updated.

| Count | Failure | Example | Repair |
|---|---|---|---|
| 27 | Node renamed; exactly one node shares the ID's number | Jafar: *"I have forged the Sacred Scimitar."* → `210 have scimitar`; node is `210 give shard quest` | Automatic, with review |
| 32 | Same, but two nodes share the number | Goblin Sapper → `5 goobye`; candidates `5 goodbye`, `5 goodbye ok` | Read the conversation, pick |
| 22 | Target deleted; no node with that number | Inquisitor Port: *"I'm leaving."* → `5 goodbye`, no node 5 exists | Retarget to an equivalent, or end the conversation |
| 3 | Target is not an ID | Fish Monger → `I'll be leaving now.` — reply text in the target field | Obvious slips |

Only the first 27 are safely automatic. The rest need someone to read the surrounding
conversation, which is what the dialogue editor's Problems dock and click-to-retarget were
built for.

Note the figure is 84, not the 96 first reported: twelve replies target a single space,
and since 2263 replies (21%) legitimately end a conversation with an empty target, a space
plainly does the same. `dialogtree_format.goto` now trims, which moves those twelve out of
"broken" and into "ends the conversation" where they belong.

**Ships as:** `lionheart-fixt-dialogue-repair`, useful standalone.

## Phase 2 — Restore cut content

Everything here already exists in the shipped archive. See [`cut-content.md`](cut-content.md)
for the full inventory and how it was established.

**The Goblin Girl.** 19 nodes, 28 replies of finished, characterful writing for an NPC
never placed — *"You're cute for a... whatever it is you are."* Node IDs describe a design
that was worked out: `1 First time PC enters village`, `2 PC Enters the village again,
before completing any quest`, `5 Give me some sugar` → *"you'll have to prove yourself"*.
`goblinguards` (4 nodes) sits beside it, so the village was planned as a set. Needs a
character template, a placement, and quest wiring. Two dangling targets to repair first.

**The Titan quest.** `Help Andre the Titan with his tasks` — the only cut quest with
authored states: *"Find Marcus' cousin and take sphere from him"* (`ID=7LOVAAS1`) and
*"Return Sphere to Marcus"*. The character was renamed mid-development, Andre in the
filename and Marcus in the contents; pick one. Montaillou, which is already the strongest
late act, so this reinforces a success rather than propping up a failure.

**Guard Pablo at the Temple District.** 11 nodes, 23 replies, zero dangling — a complete
bribe-the-guard interaction, and a genuine use for Speech and Barter in an act that has
them.

**The unused enemy tiers.** 25 templates across two coherent, difficulty-tiered sets: 14
for `English in Caverns of Nostrodomus` and 11 for the Sewer Thieves. These give phase 3
somewhere to go — encounters can become more varied while becoming less frequent.

**Deliberately not restored:** the Start Game opening sequence (seven templates, no
dialogue, and the opening is a fixed cinematic), and the single-node stubs
(`MadEnchanter`, `knighttemplar`, `rocktitancanned1`), which are placeholders rather than
content.

## Phase 3 — Thin the grind

Enemies are placed through `CGeneratorAIGroup`, of which the game has 7675, holding 15240
`CSpawnableCannedEntity` entries. Each group carries `Quantity to generate min` / `max`, a
weighted list of what to spawn, and `Max Party Mojo` — which appears to gate on party
strength and wants understanding before anything is touched.

So thinning is a data edit, not a redesign: reduce quantities, drop whole groups, and
substitute varied templates from phase 2 for repeated ones.

Provisional targets, to be revised by play-testing — the aim is Montaillou's feel, not
Barcelona's:

| Act | Spawns/map now | Target | Means |
|---|---|---|---|
| 4 Crypt | 284 | ~120 | Fewer, larger, more varied encounters |
| 7 English Shrine | 180 | ~90 | |
| 6 Barcelona Attack | 189 | ~120 | A siege should stay dense |
| 5 Nostrodomus | 148 | ~90 | Field the cut English force for variety |
| 2 Montserrat | 105 | ~70 | |

This is the most subjective phase and the easiest to get wrong. It should land after
phases 1 and 2 so that the acts already have more to do before they have less to fight.

## Phase 4 — New writing

The largest phase, and the only one that addresses the central complaint. The problem is
structural: acts 4–8 are dungeons, and dungeons have no townsfolk to talk to. Four
vehicles that fit, in order of cost:

**Companion banter — cheapest and highest value.** The machinery already exists:
`Companion Joined.can`, `Start`/`Stop Companion Follow`, a `Companion Follow Enabled`
attribute, and Captain Isabella already has companion voice lines. But
`Generic Companion Dialog` is a single node — *"What would you like your companion to
do?"* — referenced once. There is no banter at all. `CDisplayDialogBalloonAction` (1974
uses across the game) delivers floating speech, so proximity triggers can fire companion
lines on entering a room, finding a body, or meeting a boss. This adds voice and reaction
without a single new NPC.

**Non-combatants who belong in a dungeon.** Prisoners, survivors, dying English soldiers,
a trapped merchant, ghosts. Each is a character template plus a DialogTree plus a
placement — a pattern this project has already executed end to end.

**Quests that use the existing geography.** The Crypt has 10 maps and one quest. Even
three or four objectives that send the player back through it with a purpose would change
how the act reads.

**Skill and faction gates on all of the above.** Free, since the gates already work
everywhere. The Barcelona rate is 38%; matching it costs nothing but authoring.

Scale, to be honest about it: reaching Montaillou's 64 nodes/map across acts 4–8 means
roughly 2500 new nodes against the 442 those acts have today. That is a long-running
project, not a release. It should be delivered act by act, each shipping on its own.

## Explicitly not doing

- **Interaction zones.** `CFreeRangePoly` hover has never worked in a hand-built map; four
  construction variants were tried. Use model-based doors instead.
- **Engine behaviour.** No exe patching. Everything here is data.
- **Rebalancing spells or items wholesale.** Tempting — `.Skill` files expose damage
  scaling cleanly — but it is a separate mod with a separate audience.
- **The Alamut endings.** They are reachable and the branch logic is engine-side.

## Tooling this needs that does not exist yet

The editors cover placement, entity scripts and dialogue *editing*, but not authoring:

1. ~~**Add and delete nodes and replies in the dialogue editor.**~~ **Done.** `Ctrl+N`,
   `Ctrl+R`, `Ctrl+Shift+Del`, and a rename field that retargets every reply pointing at
   the node — a rename that doesn't is how the 84 broken links happened.
2. **A quest editor.** `.Quest.txt` is the brace format `resource_format` already
   round-trips; the state IDs are opaque 8-character codes that want generating and
   cross-referencing against the maps that activate them.
3. **A character template editor.** All 247 `.can` files parse and round-trip
   byte-identically already, so this is UI over a solved format.
4. **Bulk generator editing.** Phase 3 means touching thousands of `CGeneratorAIGroup`
   nodes; that wants a headless script with a report, not hand-editing.
5. **A cross-file reference checker.** Every `Race=`, `Dialog Tree File=`, `Node ID`,
   `Quest` and `Model` path resolved against what exists. Dangling references are the
   failure mode that has cost this project the most time, and a mod this size will
   generate them faster than anything so far.

## Open questions

1. **What is `Max Party Mojo`?** It gates generator groups and looks like party-strength
   scaling. Phase 3 cannot be done responsibly without knowing.
2. **Andre or Marcus?** The cut Titan quest disagrees with itself.
3. ~~**Where was the goblin village meant to be?**~~ **Answered, as well as it can be.**
   The Wilderness does have maps of its own — 43 of them — and `Goblin Warrens` is already
   a working village: 15 conversations, 9 quests, 304 reachable nodes, with nine
   `Goblin House Interior` maps hanging off it. `goblingirl` was cut from there.
4. **Does companion banter need the companion present?** Whether a balloon action can be
   fired from a proximity trigger against a companion who may or may not be following.
5. **How much can be thinned before difficulty breaks?** Only play-testing answers this,
   and the answer probably differs per build.
