# QA

Nothing ships without passing this. A build that is byte-correct on disk has proved only
that the files arrived, not that the game agrees with them -- so every release is a
**release candidate** until a human has played the gates below and signed off.

The order matters. Gates 0 and 1 are cheap and catch the failures that would otherwise
waste a whole play session; do not start Gate 2 until they are green.

The cases below are the authority. [`playtest-guide/`](playtest-guide/) is the same list arranged as a route to walk
in one sitting, and cites these IDs; its `build.py` refuses to build if it cites one
that no longer exists here, so renumbering a case cannot silently orphan the guide.

---

## Gate 0 - automated, before anyone plays

All of these are scripted in [`tools/validate.py`](../tools/validate.py) and must be
re-run after *any* change to `files/`:

```
python tools/validate.py
```

It exits non-zero on any problem, so it can gate a build. `--tools` and `--vanilla`
override the two paths it needs. Binary payloads -- `.mdl16` icon art and friends --
are skipped by extension and only checked for being non-empty; every other extension
is parsed, so a new *text* type cannot slip through by being unlisted.

| # | Check | Passes when |
|---|---|---|
| A0.1 | Every `.DialogTree` has its `CDialogTree` wrapper and balanced braces | no parse failures |
| A0.2 | Every `Go to node ID` resolves to a real node (case-insensitively) | zero dangling targets |
| A0.3 | Every named `Requirement=` resolves to a real `.can`, ours or vanilla's | zero unresolved |
| A0.4 | Reply count equals `Go to node ID` count per file | equal in every file |
| A0.5 | Every embedded `Custom Action` / `Custom Requirement` parses | no parse failures |
| A0.6 | Non-dialogue resources round-trip byte-identically through `resource_format` | canonical formatting |
| A0.7 | Both edited `.zax` files parse as `CLayerSaveData` and round-trip byte-identically | identical |
| A0.7b | **Every map -> dialogue node reference matches BYTE-EXACTLY** -- unstripped, including trailing spaces | zero mismatches. A miss here is a hard crash on map entry, not a silent failure, and it is how the Goblin Warrens crash shipped |
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
| F2 | -- | **Not testable.** `Goblin Sapper`'s `30 goblin name` has zero inbound links; the repair is correct but the node is unreachable | skip |
| F3 | -- | **Not testable.** `GoblinVillager`'s `500 wilderness banter` fires only as a balloon, and balloons have no reply list | skip |
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
| G7 | " | Do the eyes quest as your **first** goblin service ever | You become **`Goblin Chum`**, not Blooded -- the cascade grants the next rank you lack, so no service is wasted |
| G7b | Any two further services, in any order | e.g. the vodyanoi, then the Everlasting | Rank climbs 1 -> 2 -> 3 regardless of order, and **never past 3** |
| G7c | A fourth and fifth service after reaching rank 3 | Anything else pro-goblin | Nothing happens. No rank, no duplicate title perk |
| G7d | The Khan's *"I'm glad we see eye-to-eye"* reply | Take it at rank 2 | Exactly **one** rank. That reply both completes the bounty quest and grants rank, and briefly advanced twice |
| G8 | Goblin Khan | Hand over the Everlasting (any of the three price routes) at rank 2 | **Rank 3, `Goblin Champion`**, granted alongside the shipped `Goblin Champion` perk |
| G9 | " | Try the other two Everlasting routes afterwards | Rank does **not** increment again -- the rank==2 guard makes it idempotent |
| G10 | Character sheet at rank 3 | Sum the three tiers | Sneak +30, Barter +14, Poison res +35, Disease res +10, Agility +1, carry weight +30 |
| G11 | Character sheet after **each** rank | Check the perk list, not just the stats | A TITLE PERK appears at every rung: `Goblin Chum`, `Goblin Blooded`, `Goblin Champion` |

### 0.1.2 - the camp reacts to standing

| # | Where | Steps | Pass |
|---|---|---|---|
| T1 | A goblin villager in the Warrens | Talk to one at **rank 0** | The vanilla threat, and only the Speech way out |
| T2 | " | At **any rank** | *"Word travels, and your name has been in three mouths this week."* The spear comes down |
| T3 | " | At **rank 3** | The goblin kneels. *"Forgive it, Champion."* |
| T4 | Rakeb | At **rank 2** | *"Clan. Yes. The bones have been saying so for a while."* No tourist's price |
| T5 | " | At **rank 3** | He is not sure the clan should be glad -- *"a door left open, and doors are how weather gets in"* |
| T6 | The Khan, entering his cave | At **rank 3** | A different greeting: *"Not 'morsel'. Not today."* <span>If he still opens with the morsel line, the map-side rank gate failed</span> |
| T7 | " | At rank 3, when he demands entertainment | You can refuse: *"Ask the room whether the Khan's champion dances."* |
| T8 | " | At **rank 0-2** | Every vanilla greeting and the entertainment demand are unchanged |
| T9 | Goblin Girl, **first meeting**, with the River Dryad already dead | Talk to her | *"You're cute for a... whatever it is you are."* **Not** the snails line. Reported from play: she used to greet a stranger as an old friend |
| T10 | " | Same, with the **woodcutter** already dead | Still the first-meeting line. World state must never beat first contact |
| T11 | " | Talk again after that first meeting | *Now* the state greetings apply -- snails if the dryad is dead, the woodsman line if he is |
| T12 | The Khan, **first meeting at rank 3** earned without the Everlasting (spy + dryad + eyes) | Enter his cave | The **vanilla** greeting. He must not claim the Everlasting hangs on his wall |
| T13 | " | Then deliver the Everlasting and return | *Now* the Champion greeting |

### 0.1.4 - what playtesting found

Every case here exists because a play session found a defect that static checking could
not. All of these have now been seen working. They are kept because a regression in any of them
would be invisible to every static check the project has -- which is how each got here.

| # | Where | Do | Expect |
|---|---|---|---|
| F1 | Anywhere | Perform three goblin services | Standing reaches **rank 3**. Every tier granted `+1` and replaced the last, so it never passed 1 and the Crossroads contract refused players who had earned it. **Confirmed in play** |
| F2 | " | Compare each rank's bonuses to the one below | Each tier is the running total of everything beneath it. Champion used to cost you Blooded's disease resistance and drop Barter |
| F3 | Goblin Warrens | Rakeb, at three points in his errands | Eyes job taken, not delivered -> *"we do not see the eyes"*. Fish killed, second job untaken -> *"I have a job for you"*. All done -> *"the items have served you well"*. All three were unreachable. *"we do not see the eyes"* **confirmed in play**; the other two rungs are not. Needs a character new to the map |
| F4 | " | Ask the girl for a pie twice; ask Rakeb for the fish job twice | Neither is given twice. Both were farmable |
| F5 | Crossroads | Kill Esteban, return to the patrol leader | He pays, the quest completes, his own quests fail. A corpse still *exists*, so the check had to ask whether he was *alive* |
| F6 | Anywhere | Read the rank titles you hold | Each describes standing, not a deed you may not have done |
| F7 | Goblin Warrens | Talk to the goblin girl twice | The second visit is not the first-meeting line |
| F8 | " | Click every reply on her first-meeting node | No blank option that does nothing. Six such replies were repaired |

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
| R9 | Goblin Girl, **after killing the River Dryad** | Talk to her | She greets you with `110 New Hero in town` (the snails), not the first-meeting line |
| R10 | " | Talk again | `120 Player returns again after killing dryad...` |
| R11 | Goblin Girl, **after killing the woodcutter** | Talk to her | `200 Returning after killing the woodsman` -- this is the gateway to the whole pie chain, and it was unreachable until the generator learned to pick a greeting by state |

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

### 0.2 - the Goblin Girl follows, but only in the Warrens

Vanilla wrote three follow nodes for her and wired none of them. Restoring the behaviour
means restoring its boundary too: the point of this section is as much that she **stops**
as that she starts.

| # | Where | Steps | Pass |
|---|---|---|---|
| F1 | Goblin Warrens, at any follow node (`90`, `190`, `195`, `290`) | Take the accepting reply | She falls in behind you and keeps up across the cave |
| F2 | " | Take the declining reply instead | Conversation ends, she stays put, nothing else changes |
| F3 | " | Open the conversation and press Escape | Same as F2 -- decline is the default reply, so cancelling is never the committing path |
| F4 | Warrens main exit, **while she follows** | Click the exit | Node `295 goblin girl stays behind` opens instead of the map change |
| F5 | " | Take *"Not yet. There is more down here."* | **You do not leave the map.** She is still following |
| F6 | " | Take *"Wait here for me."* | She stays; you arrive at the Mongol Camp **alone** |
| F7 | Waterfall passage exit, while she follows | Same as F4-F6 | Node `296 goblin girl stays behind waterfall`; different line, same behaviour |
| F8 | Either exit, **not** following | Click the exit | Straight map change, no dialogue -- vanilla behaviour is untouched |
| F9 | Mongol Camp, after F6 | Walk around | **She is not with you.** This is the whole point; if she is here, the release lost its race with the relocate and Mongol Camp needs vanilla's remover entity |
| F10 | Warrens, kill her while she follows | Then click an exit | Straight map change, **no farewell from a corpse**. Her death script clears the marker, and the exit also checks `CIsAliveAction` |
| F11 | Warrens, leave and return while she followed | Talk to her | She is where you left her and still greets by quest state |

Confirmed in play: F1 and the main-exit farewell. **F2, F3, F5, F7, F9, F10 and F11 are
unobserved.** F9 and F10 are the two that matter -- they are the failure modes that turn a
bounded follower back into a full companion, or into a ghost saying goodbye.

### 0.2 - Esteban and the bandit you killed before he asked

Kill the Crossroads bandit before Esteban raises it, tell him so, and he verifies your
claim. The relay that brings him back opened `113 Thief success` -- *"Good work! Here is
your justly deserved reward"* -- congratulating you on an assignment he never made. The
node written for this path, `114 pre assigned thief success`, was reached by nothing.

The path is exclusive: `60 Thieves` sits behind `Esteban will not reassign thief quest`, so
the relay can only fire for a player he never asked.

| # | Where | Steps | Pass |
|---|---|---|---|
| E1 | Crossroads | Kill El Bandito Rie **before** taking any Esteban quest, then talk to him and ask about thieves | The reply *"I've already taken care of those thieves"* is offered |
| E2 | " | Take it | He verifies, screen fades, and he returns with *"**Really? Most excellent.** Here is your reward"* -- **not** *"Good work!"* |
| E3 | " | Check money and log | 150 gold and the XP from the verify step, `Find the Crossroads Bandit` completed. Unchanged from before this fix -- the payout was never the broken part |
| E4 | " | If the wasps are also dead, take *"I have also slain the wasps"* | Wasp quest completes, 100 gold, **and he now answers** with `103 wasps killed` -- *"Muy excelente!"* Before, the conversation ended silently |
| E5 | " | Take *"I should be on my way"*, or press Escape | `10 Goodbye`. This reply did not exist on the node before; its default used to push you on to `35 dangers 2` |
| E6 | Crossroads, the **assigned** route | Take the thief quest from Esteban normally, then complete it | Still reaches `113 Thief success` and *"Good work!"* -- 113 is reached from six other places and must be untouched |

E6 is the regression that matters. E3 and E4 guard against double-payment: the wasp
completion lives on the reply, and `103 wasps killed` pays nothing itself, so the
retarget cannot pay twice.

### 0.3 - the Knights of Saladin award the rank, not just the title

The Dream Djinni trials hand out `Dervish of the Crescent` -- whose own text says *"You have
become a Favored One of the Knights of Saladin"* -- or `Scholar of the Crescent`. Both are
perks, and perks confer only skills. `Dream Djinni Map.zax` performed **zero** faction
assignments, and the only place in the shipped game that assigned a Saladin faction was a
test map. So `Saladin IS` (Saladin Rank > 0) was never true and **20 replies across four
acts could never appear.**

Reaching it: complete the Dream Djinni trials in Barcelona, by combat (Dervish) or by wits
(Scholar).

| # | Where | Steps | Pass |
|---|---|---|---|
| S1 | Dream Djinni, Barcelona | Win the trials by **combat** | `Dervish of the Crescent` awarded **and** the character sheet shows the Aswaran modifiers: +10 One-Handed, +10 Two-Handed, +1 EN, +20 carry |
| S2 | " | Win by **wits** instead | `Scholar of the Crescent` awarded, same Aswaran modifiers |
| S3 | " | Re-trigger the trial reward if possible | Rank does **not** climb past 1. Faction tiers replace rather than stack, and only Aswaran is ever assigned |
| S4 | **Quinn the Herbalist**, Gate District | Talk to him as a Saladin | **6 replies** appear that were previously unreachable -- more than any other NPC in the game |
| S5 | Temple Entrance Guard, Gate District | Talk as a Saladin | 1 new reply |
| S6 | Brother Michel, Montaillou | " | 3 new replies |
| S7 | Joan of Arc, the Crypt | " | 3 new replies, including claiming the Bleeding Lance for the Order |
| S8 | Sir Roger, English Shrine | " | 7 new replies -- the largest single block |
| S9 | Any of the above, **not** a Saladin | " | All of those replies are **absent**. This is the gate-failing-open check |

S4 is the cheapest real test -- Quinn is metres from the Dream Djinni and carries six of the
twenty. S9 is the one that matters most.

**Not a bug:** the Aswaran description text says "+1 Endurance, carry weight increases by 10,
and both melee skills gain 4 points" while the record actually grants +10/+10/+1/+20. That
mismatch is vanilla's, in a description nobody could previously read because the faction was
never assigned. Left alone.

### 0.3 - the Sacred Scimitar, and Farshad

| # | Where | Steps | Pass |
|---|---|---|---|
| S10 | Amir, Gate District, at `202 make a scimitar` | Reach the second task **without** having taken the Shard | **Two** replies now: the Shard as before, and *"Eduardo the smith speaks of a sacred blade..."* |
| S11 | " | Take the scimitar arm | The `Forge a Sacred Scimitar` quest starts -- **from Amir**, not from the dead trigger in the smithy |
| S12 | " | Take the Shard arm instead, then return | The scimitar reply is **gone**. One arm or the other, never both |
| S13 | Eduardo, then Amir | Forge the blade, return to Amir | *"I have forged the Sacred Scimitar"* now reaches `210 have scimitar` instead of dead-ending. He hands it **back** -- the Shard is surrendered, the scimitar is kept |
| S14 | " | Continue | Both arms converge on `120 donate gem` and the trials |
| S15 | Eduardo, **retrieved his father's sword** | Take the scimitar | The **Sacred** Scimitar: +5 critical, +10 piercing resistance. Karma or 150 gold as vanilla, depending on whether you took payment |
| S16 | Eduardo, **talked or bartered past the test** | Take the scimitar | The **Crescent** Scimitar -- same art, no bonuses. The quest still completes and Amir still accepts it |
| S17 | Farshad, Gate District | Talk to him at all | **A conversation opens.** Before this he gave a one-line balloon and nothing else |
| S18 | " | As a male Saladin | *"Word of your deeds have come before you, brother. Welcome into the Order of Saladin."* |
| S19 | " | As a female Saladin | The sister variant of that greeting |
| S20 | " | Not a Saladin | `1 Conversation Start`, the ordinary entry -- unchanged |
| S21 | " | Carrying either scimitar, ask about the duel | He offers a lesson; accept for **+5 One-Handed Melee** after a fade |
| S22 | " | Ask again | The offer is **gone**. Once only |
| S23 | " | Carrying no scimitar, scimitar quest never done | The offer never appears |
| S24 | Dream Djinni, **carrying a scimitar you forged** | Win the combat trial | He does **not** hand you a second one. He enchants the one you have -- it gains **Flame**, fire damage |
| S25 | " | Took the **Shard** arm instead, so no forged blade | Vanilla: he hands you a Sacred Scimitar as always |
| S26 | Farshad, **after** the Djinni enchanted your blade | Ask about the duel | The lesson is **still offered**. The gate accepts the quest being completed as well as the item being carried, because re-granting the blade with an addition may not satisfy an item check |
| S27 | " | Compare the two blades | Sacred+Flame must still beat Crescent+Flame -- the Crescent never gains the base +5 critical or +10 piercing |

S16 is the one to argue about, not to bug-report: it is the release's only deliberate
balance change. S22 is the farming check.

### 0.2 - Grumdjum after the dryad

One field. The post-dryad Grumdjum's talk interaction opened `160 After Dryad death bubble`
-- a bark -- instead of `8 Return Dialogue Dryad Dead`. The bubble is still there; it is
node 8's exit reply, which is how we know 8 was meant to be the entry.

Reaching it: take the dryad quest from Grumdjum at the Lake, kill the River Dryad, return
and hand it in. He walks to her crystal and respawns there as a second entity.

| # | Where | Steps | Pass |
|---|---|---|---|
| G1 | Lake, after handing in the dryad kill | Find Grumdjum at the dryad's crystal and talk to him | *"It is always a pleasure to see you, my dryad slayer..."* and **three replies**. Before this fix he said one line about her brain and the conversation ended |
| G2 | " | Ask *"What is New Khara'Khorum?"* | `100 Goblin City` -- he says to seek it **through the waterfall to the east**. That is a real direction: the Warrens' second exit is `From Waterfall Passage` |
| G3 | " | Ask about poetry (needs `Player has heard Grumjun poetry` > 0, so hear a poem from him first) | `200 new poem`, then any of three reactions -> `200 new poem response` |
| G4 | " | Take the third reply, or press Escape | `160 After Dryad death bubble` -- the brain line, now working as the sign-off it reads as |
| G5 | " | Re-open the conversation | Repeats cleanly; no farming, since nothing here grants anything |
| G6 | Lake, **before** handing in the dryad kill | Talk to Grumdjum | Unchanged from vanilla -- the rotating `3` / `5` / `6` / `7` greetings, and the hand-in reply still pays the Ring of Fiery Death and advances rank |

G6 is the regression that matters: this edit sits next to the quest hand-in, which is
shipped and tested content.

**Not done, and reclassified as back-half work:** Grumdjum's `300 ...` companion arc (ten
nodes -- join, dismissal, rejoin, injury barks, combat quips, all in rhyme). His join line
is about Alamut, the Khan's `500 Start in Persia` is the matching cut goblin companion for
the same act, and neither has a companion generator on any map. One cut Act 8 feature, not
Wilderness work.

### 0.2 - the Khan's war campaign

Four orphaned vanilla nodes restored. `365` names Guard Esteban as step one of an invasion
of Nueva Barcelona, which is the motive the Esteban contract has never had.

Requires **Goblin Champion** (rank 3 -- the rank the Khan himself grants at `195 Charisma`
for bargaining well over the Everlasting), so this is late in his arc by design.

| # | Where | Steps | Pass |
|---|---|---|---|
| K1 | Goblin Khan, as **Champion** | Talk to him | New reply *"I would serve the Horde again. What does the war need?"* is offered |
| K2 | " | Take it | `350 next task` -- *"I have need of a strategist"* |
| K3 | " | Continue twice | `360 attack barcelona`, then `365 barcelona walls`, which names Esteban and the gate guards |
| K4 | " | Accept | Conversation ends peacefully. Nothing else changes -- the briefing grants no quest and no reward |
| K5 | " | At `350` or `360`, take the **Exit Icon** reply, or press Escape | Conversation ends, camp stays calm. **The default reply is never the fight** |
| K6 | " | Take a **Fight Icon** reply at any of the three | `400 Where are you going?` -- *"I did not say you could leave!"* -- and the Khan turns hostile |
| K7 | " | **Below Champion** (Chum or Blooded) | The entry reply is **absent**; his conversation is unchanged from 0.1.4 |
| K8 | Khan, **after already killing Esteban** | Reach `365` | A fourth reply appears: *"Esteban is already dead. I cut him down before you asked."* -> `370`, the Khan's reaction |
| K9 | " | Same, with Esteban **alive** | That reply is **absent** |
| K10 | Khan, **after killing Esteban**, on the greeting itself | Talk to him | A **second** Champion reply is offered: *"the gatekeeper Esteban is dead. I want you to hear it from me."* -> straight to `370`, without re-walking the briefing |
| K11 | " | With Esteban **alive** | That reply is absent; only the briefing entry shows |
| K12 | " | After reporting, talk again | The briefing entry is still there and still works. Re-hearing his plan is intended; nothing is granted, so there is nothing to farm |

K7 and K9 are the pair worth checking hardest -- either one failing open means a gate did
not resolve, which is this project's top recurring failure mode.

**Not a bug, do not report:** the horde never does attack Barcelona. Act 6 has essentially
no goblins in it. The briefing restores the Khan's stated plan, not a promise the game
keeps.

**Also deliberately not done**, so it is not proposed again. A quest object for the
campaign would put a rival Esteban entry in the log beside Fixt's own `Kill Guard Esteban
for the Goblin Patrol`. And wiring the second half of the order is buildable -- Barcelona's
Gate District really does hold nine `Gate Guard` entities and a `Barcelona Portcullis` --
but it would resolve to nothing, and a tracked objective that visibly fails to pay is worse
than a stated plan that never happens.

### 0.2 - the goblin jailor, and rank as an argument

The Darsh escort scene is **vanilla and works** -- it was surveyed as possible cut content
and it is not. Cases J1-J3 exist to confirm that reading is right, because the whole scene
has never been walked deliberately. J4 is the only Fixt change here.

Reaching it: free Darsh in the Mongol Camp jail, let him follow you, then walk him toward
the camp exit. The jailor challenges you about a second after Darsh crosses the line.

| # | Where | Steps | Pass |
|---|---|---|---|
| J1 | Mongol Camp, escorting Darsh | Walk Darsh toward the exit | The **Goblin Jailor** stops you: *"And just where do you think you are taking that prisoner?"* |
| J2 | " | Speech 25+, take *"The Khan has requested to eat this morsel"* | `400 jailor okays release`; **camp stays calm** and you leave with Darsh |
| J3 | " | Take either other reply, or press Escape | Camp turns hostile. This is vanilla's design, not a bug -- the bluff has no check behind it and the default reply is the bluff |
| J4 | " | **Goblin Blooded or Champion**, any Speech | New reply *"I am of the Horde, and this morsel is spoken for"* is offered **above** the Speech option, and reaches the same release |
| J5 | " | Goblin Chum (rank 1) only | The rank reply is **absent** -- the gate is `Goblin Rank > 1`, not merely "in the Horde" |
| J6 | " | Kill the jailor first, then escort Darsh out | No challenge at all; the trigger checks `CIsAliveAction` before firing |

J4 and J5 are the pair that matters: J5 failing open would mean the requirement did not
resolve, which is this project's top recurring failure mode.

### 0.1.1 - the Crossroads patrol

| # | Where | Steps | Pass |
|---|---|---|---|
| X1 | Crossroads | Ask Esteban about the dangers -- but **do not accept his goblin quest** -- then walk to the patrol | The goblins **do not attack**. They patrol and can be approached |
| X1b | " | Talk to the Patrol Leader | A conversation opens. **In vanilla and in the first 0.1.1 build the only interaction was an attack**; his `GetCloseThenTriggerAndFight` specifier was shadowing the conversation |
| X1c | " | Now accept Esteban's goblin quest | The patrol turns hostile -- vanilla's `goblin confrontation` relay. **This is the choice, not a bug**: you agreed to clear them out |
| X1d | " | Mouse over any goblin in the patrol before anything turns hostile | A **speech** cursor, not a sword. Clicking gets a line of banter |
| X2 | " | Attack one anyway | The full vanilla fight starts -- Patrol Leader, Scout **and** the corner goblins all turn. If any stands inert, `goblins attack` did not re-arm it |
| X3 | Goblin Patrol Leader | Talk to him with **no** Horde rank | The purge line, a `Speech 40` route, a fight and a walk-away. **No contract offered** |
| X4 | " | Talk carrying **rank 1 only**, before ever meeting the Khan | He recognises you but offers **no contract** -- he sends you to the Khan first |
| X4b | " | Meet the Khan, come back still at rank 1 | *"You are still only a chum."* He tells you to do the shaman's work. Still no contract |
| X4c | " | Come back at **rank 2** (after Rakeb's eyes quest) | Now the contract is offered. With IN 7+ you can also work out why he needs a *human* hand |
| X5 | " | With IN 7+ | The "you need a human hand" reply is visible and leads to the same offer |
| X6 | " | Accept the contract | Quest appears; karma drops 50. **Esteban is unaffected** -- he was not there and cannot know |
| X7 | Guard Esteban | Talk to him after accepting | He behaves **exactly as before**. Still offers his quests, still takes turn-ins |
| X8 | " | **With the contract accepted**, attack him | A real fight starts. **You are not sent to prison.** In vanilla any player damage triggers `Esteban Sends you to jail`. He is 200 HP / 200 AC / melee 90 and **spell-immune** -- roughly Goblin Khan tier, weapons only |
| X8a | " | As a caster, cast near him after accepting | Also no jail -- the 400-radius spellcast ward is removed too |
| X8c | " | Kill him | His two quests fail, the Templar step fails and rewinds to `F5BCFW6V`, karma drops 75, `Esteban Dead` is set |
| X8d | " | **Without** the contract, attack him | **Still jailed.** The wards are lifted only by taking the contract; vanilla behaviour is untouched for everyone else |
| X8e | " | Accept the contract, **leave the Crossroads and come back**, then attack | Still no jail. Every map entry re-clones a warded Esteban from the generator, so the fix has to survive that -- it disables the reset itself |
| X8b | " | If you find another way to kill him without the contract | Same consequences. Killing a Templar man-at-arms costs the same whoever asked |
| X9 | Goblin Patrol Leader | Return after killing Esteban | He pays 450 gold, completes the quest, karma drops another 75 |
| X10 | " | Talk again after payment | The `50 after` line, and **no second payment** |
| X11 | `LordJavier`, Temple District | Attempt the initiation after killing Esteban | The rung is closed. He requires state `AIFBMSWX` and the death rewound it, so failing the quest status alone would not have been enough |
| X11b | " | Do all Esteban's tasks, reach `AIFBMSWX`, **then** kill him | The rung still closes -- the rewind is unconditional. You keep the rewards you already earned |
| X12 | " | **Character B**, never took the contract | The whole Templar initiation still works exactly as vanilla |

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
| N5 | **The anti-goblin path still works through an edited file.** `GoblinKhan.DialogTree` carries Torquemada's `Slay the Goblin Khan` and Fixt edits it | Take the contract, kill the Khan, collect from Torquemada -- unchanged from vanilla |
| N6 | A **non-Horde** player hands the Khan the Everlasting | Quest completes and the shipped `Goblin Champion` perk is still granted. The rank guard fails silently; it must not swallow the perk |
| N7 | A **non-Horde** player brings Rakeb the woodcutter's eyes | Quest completes and the reward is paid as vanilla. No rank, no error |
| N8 | Kill Rakeb / the Khan **after** taking a rank from them | No script errors; the camp-hostility relay behaves normally |

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

- **Talking to Esteban about the local dangers arms the Crossroads goblin encounter, with
  no quest required. That is vanilla.** The path `30 Dangers` -> `500 goblins` ->
  `500 goblin continued` fires `Relay Name=goblin encounter` unconditionally (unless
  `Corner Goblins Dead`), and there is no quest gate anywhere along it. Fixt's only change
  to that file is a one-line repair to a dangling `Goodbye` target. Confirmed by testing
  in 0.1.0-rc1. **0.1.1 changes this**: the patrol now spawns neutral and the encounter is
  a conversation, so the X-cases below replace this behaviour. Attacking them still starts
  the vanilla fight.
- **`River Dryad Take Goblinkill quest Grumjun NOT dead High Outwit.can` is read by no
  conversation in the game.** Fixt repairs it alongside its twin for consistency, but
  nothing references it, so no test can observe the change. Do not hunt for it in play.
- ~~**The `Midlevel` / `Highlevel` / `NOT` gates are referenced nowhere yet.**~~ Stale as of
  0.2. `Midlevel` is read by the Goblin Patrol Leader and the goblin jailor, `Highlevel` by
  the Khan and the villagers. `NOT` is still referenced nowhere.
- The goblin and Torquemada quests still do not fail each other, and harvesting the
  woodcutter's eyes still moves no karma; neither is scheduled yet.
- **The captive child on Scar Ravine works, and needs nothing.** Investigated in 0.2 and
  cleared on three counts, recorded so nobody re-opens it. (1) `60 Boy freaks` looks
  orphaned in `Goblin guarding Woodcutter daughter.DialogTree`, but it is a stray duplicate
  -- the map correctly plays the child's own copy from `Woodcutterson.DialogTree`, and the
  balloon exchange runs. (2) The rescue pays off: `Woodcutter Forest.zax` selects
  three ways, and `daughter saved` reaches `6 saved daughter` and its reward. (3) The
  Woodcutter's `90 Player return A-1` through `160 Player Return G` are **superseded, not
  cut** -- `2 Return Dialogue angry` (11 replies) and `3 Return Dialogue happy` (10) are
  the consolidated greetings that absorbed that whole series through reply-level gates.
  What is genuinely unused there: three aggro barks (`100 dinner`, `100 take our meal`,
  `100 take brain`). Wiring `100 take our meal` would need a captive-death trigger on a map
  the mod does not own, for one line.
- **The Darsh jailor scene works too** -- see the 0.2 jailor section. Vanilla wires it end
  to end; only the rank reply is Fixt's.
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
| 0.1.4 | PASS (automated) | PASS | PASS | - | - | - | **published as full** |
| 0.2.0 | PASS (automated) | - | partial | - | - | - | **published as full** |
| 0.2.1 | PASS (automated) | - | - | - | - | - | **published as full** |
| 0.3.0 | PASS (automated) | PASS | partial | - | - | - | **published as full** |

0.2.0 was published as a full release on the maintainer's call, not because the gates were
green. Of its five items only the Goblin Girl's follow has been played; the Khan's
campaign, the report-back, the jailor's rank route and the Grumdjum fix are verified in the
built archive and unplayed. Gate 0 catches a broken reference, never a gate that resolves
wrongly, which is the failure mode this release carries most of.

Character B has never walked any release. That is the outstanding hole in the whole
project, not a 0.2.0 problem.
