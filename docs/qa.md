# QA

Nothing ships without passing this. A build that is byte-correct on disk has proved only
that the files arrived, not that the game agrees with them -- so every release is a
**release candidate** until a human has played the gates below and signed off.

The order matters. Gates 0 and 1 are cheap and catch the failures that would otherwise
waste a whole play session; do not start Gate 2 until they are green.

---

## Gate 0 - automated, before anyone plays

All of these are scripted and must be re-run after *any* change to `files/`.

| # | Check | Passes when |
|---|---|---|
| A0.1 | Every `.DialogTree` has its `CDialogTree` wrapper and balanced braces | no parse failures |
| A0.2 | Every `Go to node ID` resolves to a real node (case-insensitively) | zero dangling targets |
| A0.3 | Every named `Requirement=` resolves to a real `.can`, ours or vanilla's | zero unresolved |
| A0.4 | Reply count equals `Go to node ID` count per file | equal in every file |
| A0.5 | Every embedded `Custom Action` / `Custom Requirement` parses | no parse failures |
| A0.6 | Non-dialogue resources round-trip byte-identically through `resource_format` | canonical formatting |
| A0.7 | Both edited `.zax` files parse as `CLayerSaveData` and round-trip byte-identically | identical |
| A0.8 | Every `Sound=`, `On the ground=`, icon and `Damage Type=` reference exists in the archive | zero unresolved |
| A0.9 | All files are latin-1 clean and pure CRLF | no mixed endings |
| A0.10 | `mod.json` file list exactly matches what is on disk | sets equal |
| A0.11 | After build: all payload files byte-identical in `data.dat` **and** the loose `data\` mirror | identical in both |
| A0.12 | `data.dat` passes `testzip()` and every entry is `compress_type == 0` | store-only |

**A0.11 is the one that has bitten this project before.** The loose `data\` tree shadows
`data.dat`; a correct archive with a stale mirror is a mod that silently does nothing.

The validator must itself be negative-tested -- feed it a known-bad file and confirm it
fails. A checker that passes everything is worse than no checker.

---

## Gate 1 - is it actually live?

Five minutes, and it invalidates the whole session if skipped.

| # | Check | How |
|---|---|---|
| L1.1 | A **new game**, not a save | see *Why a new game* below |
| L1.2 | Fixt is enabled and **last** in load order | `modmanager.py list <game-dir>` |
| L1.3 | The build is newer than the last source edit | re-run `install` then `build` |
| L1.4 | One cheap in-game tell fires | talk to Hrubjub; the `PE 7+` reply is visible on a PE 7+ character |

### Why a new game

Two independent blockers, both confirmed the hard way:

- **New map entities never appear on a save that already entered that level.** The entity
  list is captured into the save the first time the level is visited and restored from
  that snapshot forever after, never re-derived from the `.zax`. This hides Goblin Girl,
  the Goblin Guards and Hub'blub's second store.
- **New dialogue nodes do not retrofit** onto a conversation a character has already had.

Dialogue *text* edits to existing nodes *are* picked up on revisit, which is exactly what
makes this trap dangerous: it builds false confidence that revisiting is a valid test.

### Staging saves

Walk to the threshold of each area once and save there. Reuse those saves for every
iteration in that zone. Suggested set: outside Hrubjub's wall (Gate District), the
Crossroads, the goblin camp entrance, inside Goblin Warrens, the Lake.

---

## The test characters

Fixt 0.1.0's rule is **a check adds a route and never removes one**. One character cannot
prove that: a build that passes everything cannot show whether the vanilla path survived.
Two are the minimum.

| | **Character A - "the noticer"** | **Character B - "the bruiser"** |
|---|---|---|
| IN | 8+ (drives `Outwit 7+`) | 3 |
| CH | 8+ (drives `Schmooze 7+`) | 3 |
| PE | 8+ | 3 |
| ST | 5 | 9+ (drives `ST 8+`) |
| Speech | 55+ by the goblin camp | as low as the build allows |
| Barter | 60+ before Hub'blub | low |
| Tribal | 80+ before Rakeb | none |
| Proves | every new route is reachable | every vanilla route still works and no new route is wrongly offered |

`Outwit` and `Schmooze` are pass-through derived attributes over IN and CH, so those two
stats are what actually move them. Tribal 80 and Barter 60 need deliberate investment;
plan character A around them or the two checks that need them cannot be tested.

---

## Gate 2 - the feature checklist

Each row: what to do, and what "pass" looks like. Run all of these on **character A**
unless the row says otherwise.

### Fix - the repaired dead ends

| # | Where | Steps | Pass |
|---|---|---|---|
| F1 | Hrubjub, node `20 ate a poet` | Ask what he is, compliment his poetry, then *"I've heard enough. Goodbye."* | Reaches `5 goodbye` ("you must earn your reprieve"), not a dead stop |
| F2 | Hrubjub, node `30 goblin name` | Same farewell reply from the goblin-name branch | Reaches `5 goodbye` |
| F3 | `GoblinVillager` (Crossroads or camp), banter node | With Speech 15+, *"My brain is far too porous and small for your tastes."* | Goblin replies "I do have a delicate stomach..." and disengages |
| F4 | Guard Esteban, Crossroads, node `50 Monsters` | Ask about monsters, then "Goodbye." | Reaches `10 Goodbye` ("Be safe traveler.") |

### Extend - the way into the Horde

| # | Where | Steps | Pass |
|---|---|---|---|
| H1 | Hrubjub, first conversation | PE 7+ character approaches | Reply *"You are no scavenger..."* is **visible** |
| H2 | " | Choose it | Node `15 spotted the sap` plays; three replies offered |
| H3 | " | Choose *"I am no friend to these city guards"* | Reaches `100 bad karma`; karma drops 25 |
| H4 | " | Instead choose *"I will be reporting every stone of it"* | Reaches `40 combat threat` |
| H5 | " | Instead choose *"I will keep my observations to myself"* | Reaches `5 goodbye` |
| H6 | Hrubjub, after Speech 20 talk-down (`60 used speech`) | Choose *"You and I may have more in common..."* | Reaches `100 bad karma`; karma drops 25 |
| H7 | Hrubjub, vanilla route | Ask *"Did you kill this town guard?"* then admire his handiwork | Still works exactly as vanilla |
| H8 | Spy quest | Accept, scout the gate, return and report | Quest completes |
| H9 | " | On completion, read his line | Names the warrens beyond the western wood and tells you to use his name |
| H10 | " | Check character sheet after completion | Sneak +10, carry weight +10, Poison resistance +10 |

### Extend - the faction gates

| # | Where | Steps | Pass |
|---|---|---|---|
| G1 | Goblin camp entrance guard | Arrive **after** H8, before any Speech option | Reply *"Hrubjub of the Horde sent me..."* is visible |
| G2 | " | Choose it | Reaches `30 khan`; the camp does not turn hostile |
| G3 | " | Character B, no Horde rank | That reply is **absent** |
| G4 | " | Character A with CH 7+ | The `Schmooze` gate reply is visible and also reaches `30 khan` |
| G5 | " | Vanilla Speech 40 route | Still present and still works |
| G6 | Rakeb | Bring the woodcutter's eyes and liver; hand them over (either the Barter 35 route or the plain one) | **Rank 2, `Goblin Blooded`**: Sneak and Barter each +8, Poison and Disease resistance each +10 |
| G7 | " | Do it **before** the Hrubjub spy quest | Rank is **not** granted -- the guard requires rank 1 first |
| G8 | Goblin Khan | Hand over the Everlasting (any of the three price routes) at rank 2 | **Rank 3, `Goblin Champion`**, granted alongside the shipped `Goblin Champion` perk |
| G9 | " | Try the other two Everlasting routes afterwards | Rank does **not** increment again -- the rank==2 guard makes it idempotent |
| G10 | Character sheet at rank 3 | Sum the three tiers | Sneak +30, Barter +14, Poison res +35, Disease res +10, Agility +1, carry weight +30 |

### Extend - the checks

| # | Where | Steps | Pass |
|---|---|---|---|
| C1 | Trapped Conquistador (Lake) | Character A, CH 7+ | Herald reply visible; leads to `35 herald` then `40 Return Barcelona` |
| C2 | " | Character A, IN 7+, on any of the three argument nodes | Deduction reply visible; goes straight to `40 Return Barcelona` |
| C3 | " | Character B, ST 8+ | *"I am your next challenger..."* visible; goes to `40 Return Barcelona` |
| C4 | " | **Character B** | The vanilla "Where is your home?" route still works, and CH/IN replies are absent |
| C5 | " | From `40 Return Barcelona`, recruit him | He joins as a companion, XP awarded |
| C6 | Rakeb (Goblin Warrens) | Tribal 80+, at node `30 Explanation` | Reply about frogs/mirrors/entrails visible; reaches `35 fellow practitioner` |
| C7 | " | Character B | That reply absent; *"I don't speak Goblin"* still there |
| C8 | Goblin Khan | CH 7+, at `11 Earn Goodbye` | Charm reply visible; reaches `16 flattered khan`; XP awarded |
| C9 | " | Character B with Speech 25 | Vanilla flattery reply still works |
| C10 | Grumdjum, dryad branch | IN 7+, **Speech below 20** | The dryad reply is now visible (it was Speech-only before) |
| C11 | " | Speech 20+, IN below 7 | Still visible -- the Speech route was not removed |
| C12 | Grumdjum (Lake), `10 Smart Goblins` | IN 7+ | The Bonecrusher reply is visible; reaches `11 fellow pedant`, which returns cleanly to `20 The Offer` |
| C13 | Grumdjum, `81 Magic Node` | Thought 80+ | The reservoirs reply is visible; reaches `82 the residue theory` |
| C14 | Grumdjum, `91 Dryad Magic` | IN 7+ | The "you are afraid I will listen to her" reply is visible; reaches `92 why silence her` |
| C15 | " | From `92`, choose *"I will hear her out first"* | Conversation ends without accepting the kill contract; the dryad can still be talked to |
| C16 | Grumdjum, `110 Goblin Poetry` | CH 7+ | The craft-praise reply is visible; reaches `120 More pun-ishment` |
| C17 | " | After C16, talk to the Goblin Khan | The "I could tell you a Goblin poem" option is available -- the Schmooze route sets the same flag the vanilla routes do |
| C18 | Grumdjum | **Character B** | All four new replies absent; every vanilla route through his tree still works |
| C19 | Bludjund (Barcelona wall), `10 brain` | ST 8+ | The wrist reply is visible; reaches `30 used speech` and he backs off |
| C20 | Bludjund, `50 secret mission` | IN 7+ | The "what else are you not telling me" reply is visible; reaches `55 not telling`, which returns cleanly |
| C21 | Bludjund, after the spy quest (`1 start likes you`) | CH 7+ | The full couplet reply is visible; reaches `1 he likes poem`. The vanilla `IN 4` reply is still there too |
| C22 | Daughter's guard (Scar Ravine) | ST 8+ | The "Try." reply is visible; reaches `70 scared`, the child is freed, XP awarded |
| C23 | " | Horde rank | The Khan's-favour reply is visible; same outcome, no Speech needed |
| C24 | " | Any character | *"What would you take for her?"* is visible and reaches `40 goblin offers trade` -- **unreachable in vanilla** |
| C25 | " | From `40`, Barter 55+ | The salt-pork offer is visible; reaches `70 scared` and the child is freed |
| C26 | " | From `40`, **Character B** | Only the fight and the walk-away replies; both still behave as vanilla |
| C27 | " | **Character B**, whole scene | The Speech 55 route and every combat route work exactly as vanilla |

### Restore - the cut characters

| # | Where | Steps | Pass |
|---|---|---|---|
| R1 | Goblin Warrens, near the Khan's court | Enter the map on a fresh save | **Goblin Girl is present and talkable** |
| R2 | " | Talk to her the first time | Node `1 First time PC enters village` plays |
| R3 | " | Talk again | Node `2 PC Enters the village again...` plays |
| R4 | " | *"give me some sugar"* -> insult her complexion | `7 sugar part 2` -> `90 Follow` |
| R5 | " | Rebuff her instead | `80 Rebuffed`, conversation ends cleanly |
| R6 | " | After killing the woodsman, choose *"why don't you find a nice goblin man"* | Node `250 Rejection` plays and **ends cleanly** (this node did not exist in vanilla) |
| R7 | Goblin Warrens, southern approach | Enter the map | **Two guards present**, conversation auto-advances through all four nodes to *"Shhh, did you hear something?"* |
| R8 | " | Attack the camp / trip the hostility relay | Both new NPCs turn hostile with everyone else |

### Restore - the poisoned pie

| # | Where | Steps | Pass |
|---|---|---|---|
| P1 | Goblin Girl, after bringing the woodsman's liver | Take the plain reply | Node `290 follow 3` plays; **pie appears in inventory** |
| P2 | " | Check the inventory entry | Named "Liver Pie", correct pie icon, description unchanged from vanilla |
| P3 | " | PE 7+ character | *"a sharp green smell"* reply visible; reaches `227 momma's seasoning` |
| P4 | " | IN 7+ character | The "measuring me for a pot" reply visible; reaches `227` |
| P5 | " | From `227`, accept | Still receive the pie, then `290 follow 3` |
| P6 | Inventory | Move the pie to a HotKey slot | It is accepted (vanilla could not be slotted at all) |
| P7 | " | Eat it at full health | Poison damage ticks over roughly a minute; not instantly lethal |
| P8 | " | Drop it | Ground pickup model appears and can be picked back up |

### Extend - Hub'blub's two prices

| # | Where | Steps | Pass |
|---|---|---|---|
| V1 | Goblin Vendor Interior | Character B | Only the vanilla *"I would like to see what you have for sale"* is offered; store opens normally |
| V2 | " | Character A with Horde rank | Chum-price reply visible; `25 chum vendor` plays; store opens |
| V3 | " | Character A with Barter 60+, no rank | Barter reply visible; same store opens |
| V4 | " | Compare a specific item's price between V1 and V2 | **Noticeably cheaper** in the chum store |

---

## Gate 3 - negative testing

The most important gate, and the easiest to skip.

| # | Check | Pass |
|---|---|---|
| N1 | Character B completes every scene above | Every vanilla solution still reachable |
| N2 | No new reply appears for a character who fails its gate | Confirmed per row in Gate 2 |
| N3 | No scene became *unsolvable* for a low-stat build | Confirmed |
| N4 | Nothing outside the goblin thread changed | Spot-check Barcelona quest givers, the Templar/Inquisition initiations |

---

## Gate 4 - regression and stability

| # | Check | Pass |
|---|---|---|
| S1 | Save and reload after gaining Goblin Chum | Rank and bonuses survive |
| S2 | The other mods in the tools repo still work when enabled alongside | No conflict on any shared file |
| S3 | No conversation crashes or shows "the executable or data file has become corrupted" | Clean |
| S4 | Leaving and re-entering Goblin Warrens on the same save | Girl and Guards persist |
| S5 | Killing the Girl / the Guards | No script errors; camp hostility behaves normally |

---

## Known gaps in 0.1.0 - not bugs, do not report

- **The `Midlevel` / `Highlevel` / `NOT` gates are referenced nowhere yet.** The records
  they read are granted, but no conversation branches on rank 2 or 3 in this release. That
  reactivity pass is 0.2.0. The gates exist so the pass has something to read.
- **The Crossroads patrol makes no counter-offer**, the goblin and Torquemada quests still
  do not fail each other, and harvesting the woodcutter's eyes still moves no karma. All
  0.2.0.
- **Every goblin conversation with player replies is now touched.** `GoblinCrier`,
  `GoblinLt`, `Goblin Hut Ritual Sayings` and `Goblin Shaman` remain vanilla: they are
  balloon banks with no player replies at all, and are correctly left alone.
- **`GoblinGuards` is an overheard exchange**, not a branching conversation. Four nodes,
  no player replies -- that is how it shipped.

---

## Triage - symptom to likely cause

| Symptom | Look here first |
|---|---|
| A gated reply never appears, on any build | The `Requirement=` name did not resolve. **This is the release's top known risk**: `Outwit 7+`, `Schmooze 7+` and `Tribal 80+` were re-authored into `Requirements/Attributes/` because no shipped DialogTree references their original folders. Reasoned from precedent, not proven. |
| A gated reply appears for *everyone* | The requirement resolved to nothing and defaulted open -- same root cause as above |
| An NPC is missing entirely | Save staleness first (L1.1), then the generator's `Position X/Y`. Bad positions fail as silently as a bad spawner class |
| NPC present but not talkable | `Interaction Type` should be `GetCloseThenTalk`; check the `CDisplayDialogTreeAction` node ID matches a real node |
| Conversation opens then immediately errors | "executable or data file has become corrupted" almost always means a malformed DialogTree -- check the wrapper and brace balance |
| Faction bonuses never granted | `CAssignFactionToCharacterAction` on Hrubjub's completion reply. Field names are `Faction To Assign` and `Character To assign` -- the lower-case `a` is authentic and must not be "fixed" |
| Change does not appear at all despite a clean build | The loose `data\` mirror (A0.11). Re-run `build`, which syncs it |
| Prices identical in both Hub'blub stores | The gated reply is opening `Hubglubs Store` rather than `Hubglubs Chum Store` |

---

## Sign-off

A release stops being a candidate when Gates 0-4 are green and the two characters have
both completed Gate 2. Record the result here per release.

| Release | Gate 0 | Gate 1 | Gate 2 (A) | Gate 2 (B) | Gate 3 | Gate 4 | Signed off |
|---|---|---|---|---|---|---|---|
| 0.1.0-rc1 | PASS (automated) | - | - | - | - | - | **not yet** |
