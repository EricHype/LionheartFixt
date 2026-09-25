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

A0.1-A0.12 are scripted in [`tools/validate.py`](../tools/validate.py); A0.13 is
[`tools/reachability.py`](../tools/reachability.py), which needs the vanilla archive to
tell our orphans from the shipped game's. Both must be re-run after *any* change to
`files/`:

```
python tools/validate.py
python tools/reachability.py
```

`reachability.py` also has a survey mode - `--survey "Port District"`, `--survey ""` for
the whole game - which reports what the *developers* wrote and never connected. That is
a content-discovery tool rather than a gate, and it is how 0.6.0 was scoped.

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
| A0.13 | Every node this mod adds is reachable -- `python tools/reachability.py` | zero unreachable. Nodes already orphaned in the shipped tree are tolerated; a Fixt tree is usually a shipped tree with nodes spliced in, and should not inherit the blame for what it copied |

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

### 0.5 - buying Tomas out

The lost boy is in the Troll Pit and the rescue already worked peacefully in vanilla --
nothing about Tomas is gated on killing trolls. The fighting was only ever about *reaching*
him. This makes that reachable without a fight, by settling what he owes.

One invented fact, and only one: he was caught stealing Red Ore. It explains the capture
without making the trolls monsters, it explains why the Eduardo trade broke, and it turns
Tomas's own shipped line into a caught thief's account rather than testimony.

| # | Where | Steps | Pass |
|---|---|---|---|
| B1 | Troll Pit, **on** the Tomas quest | Talk to the alpha | A new reply: *"There is a child of my kind shut in your rock"* |
| B2 | " | Not on the quest | That reply is **absent** |
| B3 | " | Ask his price | Two hundred gold -- *"Not for the boy. For the times before, when we did not catch him"* |
| B4 | " | Pay it (needs 200) | 200 taken, the pit stands down, XP |
| B5 | " | **Barter 40+**, with 100 gold | 100 taken instead. The reply is absent below Barter 40 or under 100 gold |
| B6 | " | **Speech 45+** | He concedes for nothing -- *"A child. Yes. Sent by men who are not"* |
| B7 | " | Refuse and threaten him | Combat, and the peace switches **off** |
| B8 | After settling any way | Walk the pit and find Tomas | No fighting needed. He leaves under his own power, as vanilla |
| B9 | " | Tell Tomas you did **not** kill the trolls | *"That's too bad. I was looking forward to getting revenge."* Vanilla's own line, and the sting the peaceful route earns |
| B10 | " | Talk to the alpha again | The offer is gone -- it is gated on the debt being unsettled |
| B11 | " | Check gold after B4/B5 | Taken exactly once. Reloading and re-settling must not charge twice |

B9 is the point of the whole thing: you buy the boy out, and he resents you for it. That is
in the shipped text -- nothing was added to Tomas.

**B12-B16: the parley, and the deadlock it fixes.** Found in play. The negotiation above
lives on `95 the chief`; the chief is talkable *only* while `Troll Peace Keeper` runs
(his generator carries no interaction specifier of its own); and the peacekeeper was
started by exactly two things -- node `30 troll trade`, which requires the wererats to be
dead already, and nodes `97`/`98`, which **are** the chief's negotiation. The only road to
peace ran through the chief and the only road to the chief ran through peace. A player who
had not exterminated the wererats could not reach any of it. The negotiation was built and
the door was never cut.

The Warning Troll grants the parley, because he is the one vanilla already put at the
entrance to decide whether you go further. It buys safe passage, not the boy.

| # | Where | Steps | Pass |
|---|---|---|---|
| B12 | Sewers entrance, **on** the Tomas quest | Talk to the Warning Troll | *"There is a child of my kind shut in your rock. Who do I speak to about it?"* on **both** `01 Greeting` and `20 no trust` |
| B13 | " | Not on the quest, or debt already settled | Both are absent |
| B14 | " | Take the parley | He points you deep, past the water. Peace comes on. `make troll mad` is switched off, so he does not re-aggro as you walk away |
| B15 | " | Walk to the chief and negotiate | B1-B11 all reachable now |
| B16 | " | Open with *"I come in peace, Eduardo said..."* | `20 no trust` is no longer a fight-or-leave dead end -- parley and the wererat route are both there |

B14's `make troll mad` clause is the specific thing to watch. That trigger is what caused
the earlier *"if I walk by the greeting troll he turns hostile"* report, and node
`30 troll trade` switches it off. The parley now does the same; if the gatekeeper turns on
you after granting passage, that is the cause.

Reply **order** on `01 Greeting` changed as a side effect: the menu now reads talk, leave,
wererats, parley, fight, where vanilla read talk, fight, leave. Which reply carries
`Is Default Reply=1` is unchanged -- vanilla marks the *combat* reply as the default on
that node, and that has been left alone rather than quietly rewritten.

B5 and B6 are the gate checks. If either reply shows up for a character who does not have
the skill, a gate has failed open.

### 0.5 - the Red Ore trade

Vanilla writes four ways to get Eduardo his Red Ore -- buy it, steal it, fight for it, or
just go -- and every one of them ends on the same line: set `3KL9W1JQ`, walk to the pit.
Node `75 Red Iron Barter or Speech` has Eduardo say *"if you can do so peaceably, then that
would be the best for all"*, and the game then provides no peaceable path at all, because
until 0.5 nothing could stop the trolls attacking.

This keeps that promise. The chief's grievance was already written -- *"Your city has eaten
this rock for years and paid us in nothing"* -- and `98 talked down` ends on *"tell the men
who sent him that we counted every time."* The player carries that word.

Cross-map state is a **quest**, not a marker: `CCheckExistenceAction` only sees the loaded
map, and Eduardo is in Barcelona while the chief is in the Sewers. The one marker is *"the
chief has already given his terms"*, read only in the pit, and its whole job is to stop the
offer reappearing and dragging the quest backwards.

| # | Where | Steps | Pass |
|---|---|---|---|
| O1 | Troll Pit, peace **not** made | Talk to the chief | The ore reply is **absent** -- it is gated on the peace being live |
| O2 | " | Make peace (either route), talk to the chief | *"You said my city has eaten this rock for years..."* |
| O3 | " | Hear him out | Node 100, then his four terms: dig and stack, one man in daylight, paid in **iron not coin**, the same face each time |
| O4 | " | Accept | Quest **The Red Ore Trade** appears at state 1 |
| O5 | " | Talk to the chief again | The offer is **gone**. If it reappears the marker gate failed and the quest can be walked backwards |
| O6 | Gate District, Eduardo | Open the conversation, any greeting | The reply *"Their chief sends you terms"* is on **every** opening, not buried in a topic |
| O7 | " | As a Demokin / Sylvant / Feralkin / wizard / after insulting him | Still present -- all eight openings carry it |
| O8 | " | Give the terms | He sets down the tongs. *"Fourteen years I have sent boys down there in the dark"* |
| O9 | " | Agree | Quest moves to state 2. He names **Tomas** as the runner |
| O10 | " | **Barter 35+** | The second acceptance reply is present; absent below it |
| O11 | Troll Pit | Return to the chief | New reply gated on state 2. Node 102 -- a younger troll hands you the ore himself |
| O12 | " | Take it | **Red Ore** in inventory, quest state 3, **1509 XP** |
| O13 | " | Talk to him again | Nothing repeats. No second ore, no second grant |
| O14 | " | Check Davinci's quest | The ore behaves exactly as looted ore does -- this adds an item, it does not touch `3KL9W1JQ` |
| O15 | Any | Never talk to the trolls at all | All four vanilla routes unchanged. Eduardo's node count is vanilla + 3 |

O9 is the payoff and the reason the quest is worth writing: the runner Eduardo names is the
boy you just bought out of that same pit, paid properly this time. It closes the debt quest
without a line of new Tomas dialogue.

O14 is the risk case. The chief's ore must not activate a Davinci state -- a player who
never took that quest would have it moved for them. It gives the item and nothing else.

**XP, and why the numbers moved.** A lava troll is worth **1509**, and the pit holds far
more of them than any quest can offset -- the peaceful route is XP-negative by construction
and always will be. But it should not be *punitive*. The Tomas debt was paying **200** for
talking a chief out of a hostage, less than a seventh of what stabbing one troll pays. That
is not a choice offered to the player, it is a tax on taking it. So:

| Grant | Was | Now | Precedent |
|---|---|---|---|
| Tomas debt settled | 200 | **1003** | vanilla grants 1003 exactly 36 times |
| The Red Ore trade | - | **1509** | one lava troll; vanilla grants 1509 exactly 36 times |

Both are native vanilla figures rather than numbers invented for the mod, and both sit well
under the 4004 ceiling. Two more allied quests at this scale are specced in `plan.md` (the
chief's spirit, and speaking for the trolls to Enrique).

### 0.5 - the missing blank line: 47 broken replies across three releases

Found in play: the Eduardo ore conversation completed on the Barter path, the quest did not
advance, and returning to the chief did nothing.

**A blank line before every reply is structural.** Vanilla holds this without a single
exception -- 10915 replies, 0 violations. Without it the reply is swallowed into the one
before it: it never appears as its own choice and its `Custom Action=` never runs. Node
`792 agreed` had two replies separated by nothing, so the `CActivateQuestStateAction` that
advances The Red Ore Trade was never reached.

The cause is systemic, not local. Every helper this project used to reorder or append
replies rebuilt the node with `CR.join(r.rstrip(CR) for r in reps)`, which strips the
separator and never restores it. That helper has been copied forward since 0.2.0:

| File | Sites | Shipped in |
|---|---|---|
| Herbalist Dialogue | 21 | 0.4.0 -- Quinn's reagents, unplayed |
| Warning Troll | 16 | 0.5 |
| GoblinKhan | 5 | 0.2.0 |
| Jafar | 2 | 0.3.0 -- the scimitar |
| Blacksmith | 1 | 0.5 |
| saladinknightcan | 1 | 0.3.0 |
| Guard Esteban | 1 | 0.2.0 |

Plus one in the playtest kit's own `Merchant Lope` menu hook, which means the test kit has
been partly broken as a testing instrument.

**Jafar's `3 Return Dialogue` is on that list**, and that is the node the Sacred Scimitar
hand-in was spliced into after being reported unreachable *twice*. The splice was correct
both times. It may well have been landing in a malformed node the whole way.

| # | Where | Steps | Pass |
|---|---|---|---|
| BL1 | Eduardo, ore terms | Agree on the **plain** path | Quest reaches state 2. Chief's return reply appears |
| BL2 | " | Agree on the **Barter 35** path | Same -- this is the reported failure |
| BL3 | Amir, with the Sacred Scimitar | Open the conversation | The hand-in reply is reachable from the greeting |
| BL4 | Quinn | Each of the three reagent turn-ins | All 21 repaired sites are in this tree; every turn-in reply must be selectable |
| BL5 | Goblin Khan / Esteban | Re-walk 0.2.0's branches | 6 repaired sites |
| BL6 | Any | `python tools/validate.py` | Gate 0 now fails on a missing separator and names the node |

BL6 is the real remedy. Gate 0 never checked this and so never saw any of it; it does now,
and the check was verified by deliberately breaking a node and confirming the gate caught it.
BL3-BL5 are regression passes over content that was signed off while quietly damaged.

### 0.5 - continuity audit of the whole troll faction

Every Fixt-authored node across the three trees was walked with the check in the modding
skill: enumerate every arrival, ask what the player has actually been *told* on each, and
compare that against what their reply claims. Six things came out. Gate 0 passed all of them
before and after -- a reference checker cannot see that a sentence is false.

| # | Where | Steps | Pass |
|---|---|---|---|
| AU1 | Warning Troll, `20 no trust` | Character who has done **nothing** about the wererats | The *"wererats are finished"* reply is **absent**. Before this it was ungated -- see below |
| AU2 | " | On Quinn's hide quest, wererats resolved, no hide held | It appears, exactly as on `01 Greeting` |
| AU3 | Troll chief, ore offer | Never took Eduardo's or DaVinci's Red Ore quest | *"Is there anything your people need from the city?"* -- the player claims nothing. The **chief** names the ore and names Eduardo |
| AU4 | " | Then hear the terms | *"The smith sends one man"* now has an antecedent |
| AU5 | " | Rite offer | *"There is a dead troll out on the rock bigger than any I have seen standing. Who was he?"* -- an observation. Node 110's *"You have seen it. Good"* now answers something |
| AU6 | " | Speak-for-us offer, **never having met Enrique** | The player asks who sent the bodies; the chief answers *"Enrique Garcia. The one who keeps the beggars."* That is also how the player learns where to go |
| AU7 | Eduardo, node 792 | Never took Marisol's quest | He does **not** name Tomas |
| AU8 | " | Tomas rescued | A gated player reply offers him, and node 793 is Eduardo realising who he had been sending down there |

**AU1 was an exploit, not a wording slip.** When the wererat reply was spliced into
`20 no trust` last turn the text was copied and its requirement was not. The copy on
`01 Greeting` carries a real gate -- `CAND(CAND(on Quinn's hide quest, do not already hold a
hide), COR(wererat cure done, COR(Beggar Master killed, Beggars destroyed)))`. Ungated, any
character at any time could claim the wererats were dead and collect **peace and a free Lava
Troll Hide**. Both copies now carry the identical gate, and the build asserts they match.

AU3-AU6 are all the same shape as the three continuity bugs already on record: a **player's
own line** asserting something they only learn on one route in. The repair in every case was
to let the NPC supply the fact instead, which reads better as well -- an NPC answering a
question beats an NPC agreeing with an accusation.

CAND nests (210 vanilla uses) and COR exists (121), so multi-condition gates were available
the whole time.

### 0.5 - the chief's errands are tiered, not offered all at once

Found in play: peace lands and a troll who has never met you offers a trade negotiation, a
burial rite and political representation in the same breath. That is a quest dispenser,
which is the one thing a faction is not supposed to read as.

Each errand now needs the one before it:

| Tier | Errand | Available once | Why there |
|---|---|---|---|
| 1 | **The Red Ore Trade** | peace, however you got it | Business, not trust. He has been robbed for years and would say so to anyone who could carry it upstairs |
| 2 | **The Chief Before** | the ore trade is complete | He has watched you carry his word honestly and come back -- which is the whole of what the rite asks for. Handing a stranger his predecessor's body is not |
| 3 | **Speak for the Trolls** | the rite is complete | Being their voice in the city is the deepest of the three, and node 132 lands hardest once you have buried the chief that day made |

This is a **deliberate departure from `plan.md`**, which wanted the errands parallel so that
"none of them is a toll on the one before". In play that reads as a dispenser. Play wins.

The tier gates drop the peace operand on purpose: the chief cannot be spoken to at all
unless the peacekeeper is running, so a completed ore trade already implies peace.

| # | Where | Steps | Pass |
|---|---|---|---|
| TR1 | Troll chief, first conversation | Peace just made, nothing done | **Exactly one** errand offered -- the ore trade. Plus the Tomas reply if you are on that quest, the flavor replies, and the goodbye |
| TR2 | " | Take the ore trade, return before finishing | No new offers. The ore offer itself is gone |
| TR3 | " | Finish the ore trade | The rite appears. Speak-for-us does **not** |
| TR4 | " | Finish the rite | Speak-for-us appears |
| TR5 | " | Finish all three | No offers left. Only flavor and the goodbye |
| TR6 | " | Reach peace via the **wererat** route, never taking the Tomas quest | The ore trade is still offered -- tier 1 keys on peace, not on Tomas |

TR6 also covers a continuity fix of the same class as the Eduardo/scimitar error. The ore
offer used to open *"You said my city has eaten this rock for years and paid you nothing"*,
quoting node 96 -- the **Tomas** negotiation. A player who reached peace by exterminating
the wererats never heard that line. It now stands on its own either way.

### 0.5 - the chief before

`05 Troll Pit` holds **thirteen corpses in one tight cluster**, x 4265-4939, y 2500-3089:
four dead lava trolls, one dead `Lava Troll Boss`, and the eight who killed him -- two
wererats, two guard dogs, two thieves, a thug and a prisoner. The living chief stands at
(5185, 2640), a couple of hundred units off the lip of that field. The map author staged a
battlefield, put the new chief on the edge of it, and wrote not one line about any of it.

This is also a **correction to `plan.md`**, which proposed a spirit quest on the grounds
that the pit holds "30 Spirit generators" and the trolls' dead are unquiet. Those
generators create `Inventory/Enemy Drop Items Cans/Spirit Energy/Spirit 5 Huge Entity` --
they are mana pickups, not ghosts. The corpses are the real content, and they are better.

The invented fact is one line of custom: a chief must be counted by someone who was not
there. It is what makes the errand impossible for the trolls and possible for the player,
and it is why the bodies have lain untouched rather than the trolls simply not caring.

| # | Where | Steps | Pass |
|---|---|---|---|
| CB1 | Troll Pit, peace made | Talk to the chief | *"There are bodies at the far end of this rock, and none of them are being fetched"* |
| CB2 | " | Peace **not** made | That reply is absent |
| CB3 | " | Hear him out | Node 111: a chief is counted by one who was not there. Quest **The Chief Before** at state 1 |
| CB4 | " | Talk to him again | The offer is gone -- marker-gated, cannot run backwards |
| CB5 | Troll Pit, far east end | Walk to (4736, 3014) | The old chief's body. **It can be clicked and it talks** |
| CB6 | " | Read node 120 | It names what is lying around him, and does not arrange them |
| CB7 | " | **Not** on the quest | Node 120 still opens; the rite reply is absent, the look-and-leave reply is not |
| CB8 | " | Stand the rite | Node 121. Quest to state 2 |
| CB9 | Back at the chief | Tell him | Node 112 -- the trolls move east *en masse*. **1509 XP**, quest state 3 |
| CB10 | " | Talk again | Nothing repeats |

**CB11-CB14: the rite has to change the field.** Node 112 says a great many trolls begin
moving east and that they will fetch their dead now, and originally nothing changed -- the
line was something the player could walk back and disprove. Vanilla's idiom for a change the
player should not watch happen (`Blacksmith map.zax`) is `CFadeScreenDownAction{Time Until
Auto Fade Up=2}` with a `CDelayAction` making the change inside the dark; the fade restores
itself, which is why `CFadeScreenUpAction` has exactly one use in the whole game.

| # | Where | Steps | Pass |
|---|---|---|---|
| CB11 | Troll chief | Turn in the rite | The screen fades down and comes back by itself |
| CB12 | The field | Walk back in | **The five troll bodies are gone.** The eight raiders are still lying there |
| CB13 | " | Read what fires now | Node 125, not 120 -- it describes the drag marks and what was left. Node 120 must **not** fire, it describes a body that no longer exists |
| CB14 | " | Before the rite | Node 120 still fires normally |

CB12 is the point. Only the trolls' own dead are taken, which is what node 112 actually says
-- "we will go and fetch them now, all of them" means all of *theirs*. The thieves, the dogs
and the two Barcelona men stay on the rock, which is a better image than clearing the field.

**CB15-CB19: desecrating the body.** `Absorb Spirit` (Tribal, offensive) is cast on a
corpse: it heals the caster -- much more with the Demokin `Vampiric Fury` trait -- fades the
body out, deletes it, and sends `Message=After Death Spell` to it. `Corpse Bomb` and
`Raise Enemy` send the same message, so one handler catches all three.

Listening for it is vanilla's own idiom (5 uses); `Gate House Near Thieves` has a corpse that
deactivates its walk-in poly when consumed. This goes further on the maintainer's call: the
peace ends and the tribe turns on you. They could not go to him themselves, they asked you
precisely because you owed him nothing, and you ate him.

| # | Where | Steps | Pass |
|---|---|---|---|
| CB15 | The field | Cast **Absorb Spirit** on the old chief | You are healed and the body is consumed -- vanilla behaviour, unchanged |
| CB16 | " | Immediately after | **The chief speaks** -- node 127 -- and then peace ends and Lava Troll, Troll Chief and the gatekeeper all turn hostile |
| CB16b | " | **Without ever being given the errand** | Same reaction -- he still arrives, they still turn. But the line is node **128**, not 127 |
| CB16c | " | With the errand given | Node **127** -- the only case where "I asked you because you owed him nothing" is a sentence he can say |
| CB16d | " | Having fought your way east through a hostile pit | Node 128 still reads correctly. It says nothing about alliance or permission |
| CB17 | " | Check the journal | **The Chief Before** is failed. No-op if it was never taken |
| CB18 | " | Walk back into the field | Node **126**, not 120 -- a shape in the dust, and the eight raiders left. Node 120 must not fire |
| CB19 | " | Do it having never taken the rite | Same reaction. Peace still ends; the errand is simply never offered |

**How it is staged.** The corpse's message handler does nothing but trigger a `CRelayAI`,
`Troll desecration relay`, which owns the whole scene in thirteen actions: begin a
non-interactive sequence, swap the field trigger, delete the chief from his post, force-
generate him and four Lava Troll Supers **north of the player** at (4790, 2690) and
(4790, 2670), end the sequence at 4s, open his line at 4s, switch off the peacekeeper, turn
everyone at 10s, and fail the rite.

The arrivals are pacified at their generators -- `CRemoveCategoryAction` off Enemy, then
`CSetTargetTypeAction` -- so they cannot swing while he is talking, and each carries a
`GetCloseThenTalk` specifier because `CGoToCombatAction` works by *converting* an existing
specifier and silently does nothing without one.

**The hostility is on the relay's timer, not on the reply, and that is deliberate.** A reply's
`Custom Action` does not execute when the conversation was opened by a script rather than by
an interaction specifier -- proven twice with a 500 XP probe placed first in the array, under
both `Speaker=Troll Chief` and `Speaker=$trigger`. Anything that must happen when this line
closes has to be timed instead. The reply keeps `Icon=Fight Icon` as the player's only warning.

There is no walk and no camera. Both were built and removed: `CAssignMoveRelativeAction` is a
dragon knockback rather than a walk, `CGoToAI` skated them and left them on the wrong side, and
the `CAIAttractCamera` chain never tracked. Node 127's text was always written for an arrival
nobody witnesses -- "You do not see him come. He is simply there" -- so spawning them in place
is what the prose already describes.

CB16 is the whole reason node 127 exists. Without it the sequence read as: cast a spell, the entire pit goes red, no reason given -- node 126 was the only explanation and it needs the player to walk back into the field, which mid-fight they will not.

**CB18 is the prose check** and the reason this was built at all: without it the player walks
into an empty patch of rock and is told about a troll bigger than any they have seen standing.

**Known and accepted:** `Corpse Bomb` has a radius, so a Tribal caster fighting near the
field can destroy the body without intending to, losing the errand *and* the alliance. That
is a deliberate call, not an oversight -- but it is the most likely way a player meets this
without understanding why.

**CB5 is the risk case and the reason this needs a playtest.** The specifier is hung on the
corpse generator's `AIs to Add`, which is the documented way every generated NPC in the game
gets its dialogue -- but it has never been done on a *corpse* here, and a dead body already
carries a loot interaction. If the body cannot be clicked, the fix is known and proven: move
the specifier onto the `Troll Peace Keeper`'s two-second tick, which already does
remove-then-add on named entities and was verified in play for the trolls themselves.

### 0.5 - speaking for the trolls

Enrique pays the player to exterminate the trolls (`141 Lava Trolls 2`, quest `Destroy the
Lava Trolls`). **Vanilla offers no way to decline** -- both replies on that node either
accept the contract or report it already done. Trolls cannot walk into his hall to argue.
The player can.

`CSetQuestSatusToFailedIfActiveAction` retires the contract: 239 vanilla uses, and a no-op
for a player who never took it.

| # | Where | Steps | Pass |
|---|---|---|---|
| SF1 | Troll Pit, peace made | Talk to the chief | *"There is a man above who is paying to have you killed"* |
| SF2 | " | Hear him out | He gives you the exact words. Quest **Speak for the Trolls** at state 1 |
| SF3 | Hall of Beggars, Enrique | Open the conversation, either greeting | The reply is on **both** openings, not buried in a topic |
| SF4 | " | Deliver it | Node 701 -- he gets faster and less comfortable |
| SF5 | " | **Speech 50+** | *"You are paying to create the problem you are paying to solve"* |
| SF6 | " | **Barter 45+** | The ledger argument. Both absent below the thresholds |
| SF7 | " | With **The Red Ore Trade** complete | A third door, no skill needed -- the trade is worth more than the trolls are dead. **PASSED**, once the gate was made `completed OR current(final)` |
| SF8 | " | Without it | That third reply is absent |
| SF9 | " | Any of the three | Contract withdrawn. `Destroy the Lava Trolls` shows **failed** if it was active, untouched if not |
| SF10 | " | Say nothing (node 703) | He keeps the offer open. Nothing is lost |
| SF11 | " | Back at the chief | Node 132 -- he sits down. **1509 XP**, quest state 3 |
| SF12 | Hall of Beggars | On `141 Lava Trolls 2`, decline | **New in Fixt**: *"No. I will not hunt them for you."* Node 704 keeps a way back to the contract |
| SF13 | " | Take the contract, kill the trolls anyway | Vanilla's route is entirely unchanged |

SF9 is the gate that matters. If the contract shows failed for a player who never accepted
it, `FailedIfActive` is not behaving as its 239 vanilla uses suggest.

SF12 repairs a real vanilla defect, and repairs it without cost: node 704 offers the contract
back, so declining can never strand the beggar chain.

### 0.5 - variance: stat, race and faction checks

Flavor only. Nothing in this block moves a quest, takes an item, grants XP or changes a
reward -- the build test asserts the absence of every one of those actions inside these
nodes. Each reply returns to the node it came from, so none of them can strand a player
mid-negotiation, and none is Trigger Only Once, so all can be re-read.

Every gate is a stock requirement can referenced by bare basename, and every one is proven
in vanilla *dialogue* rather than merely present on disk: `PE 7+` (6 uses), `IN 6+` (6),
`IN below 4` (3), `ST 8+` (5), `CH lessthan 6` (7), `Templar IS` (45), `Inquisitor IS`
(106), `Tainted race - feralkin or sylvant`.

| # | Where | Gate | Pass |
|---|---|---|---|
| VR1 | The corpse field, node 120 | `PE 7+` | The four trolls are in a line, all facing his way -- they were still coming when it ended. A bow with no arrow nocked. The dogs are the only ones who ran |
| VR2 | " | `IN 6+` | Wererats *and* thieves in one party -- two ends of a war that has run for years. Somebody bought both halves for the same night and told neither |
| VR3 | " | `IN below 4` | *"Thirteen. That is a lot."* Short and flat, not comic |
| VR4 | " | PE 6 or less / IN 4-5 | VR1 and VR2 absent. The plain description is all you get |
| VR5 | " | After any of VR1-VR3 | Returns to node 120. The rite is still available |
| VR6 | Troll chief, node 95 | `ST 8+` | He looks away first, and makes it a courtesy. *"Big is common down here"* |
| VR7 | " | Feralkin or Sylvant | He sees it. They have a word for you up there and it is the same word the trolls get |
| VR8 | " | Human / Demokin, ST 7 or less | Both absent |
| VR9 | Enrique, node 701 | `Templar IS` | *"I am being lectured about mercy toward monsters. By a Templar."* And: you are the first one who asked them first |
| VR10 | " | `Inquisitor IS` | He checks the chair for a trap. *"I am extremely listening."* |
| VR11 | " | `CH lessthan 6` | The blunt version lands *better* -- he was braced for cleverness and got a fact |
| VR12 | " | Any of VR9-VR11 | Returns to node 701. Speech / Barter / ore-trade routes all still reachable |

VR3 and VR11 are the **Character B** cases -- the low-INT, low-CHA, high-STR build that has
never had a release walked with it. They are deliberately written short and flat rather
than played for laughs: the joke wears out in ten minutes and the character still has to be
playable for forty hours.

VR7 is the one worth reading in place. A Feralkin or Sylvant player and a lava troll are
both things Barcelona rings a bell about, and the chief is the only character in the game
who says so.

### 0.5 - the thieves' final job, and the first new map

**This is the first map Fixt has added**, though not the first this project has built:
`test-pocket` in the tools repo is a from-scratch map with hand-laid wall runs, a door,
NPCs and a quest, and it works. So "will the engine mount a map that did not ship" is
already answered -- yes, and with no registration anywhere.

`test-pocket` also settles something this build got wrong. It ships **no cache files at
all** -- no `.way` waypoint graph, no `.frm16` automaps -- and still plays, so the engine
generates them when they are missing (`Calculating Way Point Map` in the exe, gated by
`Levels/WayPointVersion.txt`). This map was instead built as a byte-identical geometry
clone of `Port House Near Warehouse` specifically so the donor's caches would stay valid,
and no prop was moved or added for the same reason. **That constraint was unnecessary.**
It is why the room is a visual twin of a Port District house, and that can be undone by
dropping the three cache files and letting the engine build them.

Nothing about the constraint makes the current build *wrong* -- the geometry really is
identical, so the cloned caches really are correct for it -- but the room did not have to
look like that.

The entrance took three attempts, and the two failures are worth recording because
both looked fine in the files.

First try: an unnamed door in the Temple District with a `CDoorAI` and an empty
`After Opened` -- it opened, closed, and did nothing, which read as an unused
entrance. It is neither. It sits at 48% across and 49% down the House Of Ilk's
1464x877 sprite -- the building's visual middle -- and since depth is `y`, the
building draws over it and swallows clicks on it. Across every Barcelona map it is
the **only** door that draws behind its own building. It is also fenced off. Both
are why it shipped dead.

Second try assumed walkable ground meant reachable ground. The `.way` waypoint
positions decode reliably, but connectivity lives in the edge lists, which do not.
"There is floor here" is not "the player can get here".

What shipped: the walled yard at the far end of the district. Its gate at
(3365.25, 2504) becomes passable -- `FenceDoor2` / `Cur Sequence=Open` /
`Collideable=0`, matching the open gate already in this map at (800, 2519), because
all 45 lettered `FenceDoor A..H` in the game are solid scenery with no open frame.
The entrance itself is the arch **painted into** `house2 c`; the house carries no
door entity, so it is a walk-into `GetCloseThen Enter Area` poly over the arch at
(3454, 2491). That position came from decoding the sprite: the arch is at pixel
(118,400), hotspot (199,181), anchor (3535.08, 2272.25). Crucially **y 2491 is
greater than the house's 2272**, so it draws in front of the building -- the test
the first attempt failed.

The quest itself shipped with the game and was never reachable: node `130 Final Job`
is the only thing that activates `Thieve in Temple District`, and nothing reached
node 130. That quest's second state, and the requirement `.can` written to gate its
turn-in, were both unused -- the same fingerprint as the Juanita fee bug.

| # | Where | Steps | Pass |
|---|---|---|---|
| SR1 | Temple District, the walled yard | Walk through the iron gate at the far end of the district and into the arched doorway of the house inside | You load into a room. **A crash, a hang or a black screen here is the whole test failing** |
| SR2 | Inside | Look around | A furnished Barcelona interior, walls and floor drawn normally, no missing geometry or holes |
| SR3 | " | Walk to each corner, and around the table and shelves | Pathing works and the character routes around furniture. Getting stuck, walking through a prop, or refusing to move is a **navmesh mismatch** -- report it |
| SR4 | " | Open the map / minimap | The automap draws. A blank or garbage automap is a `.frm16` problem, not a quest problem |
| SR5 | " | Leave by the exit at the edge of the room | You land back inside the yard, on walkable ground, near the doorway you came in by -- not outside the fence |
| SR6 | " | Walk into the doorway again | You go back in. It is not a one-shot |

Only once SR1-SR6 are green does the quest matter.

| # | Where | Steps | Pass |
|---|---|---|---|
| SR7 | Juanita, after handing over the Port District dues | Take the reward | She still gives the **Bracers of Stealthy Cunning** and the **Thief Friend** perk, and prints "You have become a friend of the thieves." The rewards come *before* the new job and cannot be missed |
| SR8 | " | Continue | She offers the final job: *"Now, for the final task. In the Temple District there is a prime location"* |
| SR9 | " | Choose *"Another time. I have business elsewhere."* | Goes straight to the seduction, exactly as it did before this change. **This is the regression case** -- declining must lose nothing |
| SR10 | " | Choose *"Consider it done. Where am I going?"* | She names a walled yard with an iron gate at the far end of the district, says the gate stands open, mentions a guard, and warns that what she wants will not be sitting out on a table |
| SR11 | Journal | After SR10 | A quest **Steal from A Noble of the Temple District** with the entry *"Find location in Temple district to thieve"* |
| SR12 | The store room | Look at the floor **just south of the bookshelf** | A glint at (568,509). Click it: **250 coin**, **50 XP**, and the journal advances to *"Tell Juanita about Temple District success"* |
| SR12b | " | Check it does not fight the exit | It sits 138 units clear of the exit area. It previously sat at (486,681), inside that area, so clicking it competed with leaving the room -- found in play |
| SR13 | " | Do SR12 on **any** build, however low PE and Find Traps | It is there and it is clickable. Finding the cache is not skill-gated at all; skill only decides whether the guard is waiting outside (SR26/SR27) |
| SR13b | " | Enter the room with **no quest at all**, any skill | **There is no secret in the room.** The cache is `Active=0` until the spawn point sees the quest state. A passer-by finds the bookshelf potion and has no reason to think anything of the place |
| SR14 | " | The bookshelf, on any character | Gives a random potion, exactly as it does in `Port House Near Warehouse`. It is byte-identical to vanilla and carries no quest wiring |

| SR15 | Juanita | Return after SR12 | A new reply: *"The house by the flags is lighter than it was. This was in it."* |
| SR16 | " | Take it | Quest completes, **500 XP** (the same as her other jobs), and the conversation moves to the seduction |
| SR17 | " | Talk to her again | The turn-in reply is gone. No double completion, no double XP |

Regressions, because `Temple District.zax` was edited and it is a 2.2MB hub:

| # | Where | Steps | Pass |
|---|---|---|---|
| SR18 | Temple District | Enter the district at all | Loads normally. Two entities were added to a map with 1028 |
| SR19 | " | Machiavelli's door, and the **unnamed door at (1034,499)** the first attempt used | Machiavelli's still opens into the House of Ilk map. The other is inert and unnamed again, exactly as vanilla ships it |
| SR20 | " | The Cathedral, Shylocke, the Inquisition doors, the sewer entrance | All still work |
| SR21 | " | The **other** Temple District robbery -- Juanita's node 124 job with her key | Unaffected. It is a different house and a different quest |
| SR22 | Juanita | The henchman shakedown: refuse to pay the 150, meet the thug in the Port District, pay him, return | Node 230 still opens and still leads to the seduction |
| SR23 | Temple District, the yard gate | Walk up to the iron gate at (3365, 2504) | It is passable. The swapped `FenceDoor2` sprite is 3x wider than the piece it replaced, so also check it sits in the fence run rather than overhanging it |
| SR24 | " | Walk from the gate to the house doorway | A continuous walkable route, without going round the outside. The waypoints show a band at y 2483-2540 and nothing between 2363 and 2483, which should be the house itself |
| SR25 | " | Rob the house cleanly, then walk the district | **No** guards appear anywhere. There are **27** entities named `Temple Guard Reserves` and name-targeted actions broadcast, so a mistake here spawns guards across the whole district, not just at the yard. The new post is uniquely named to avoid that |

**Known, and now avoidable:** the store room is a visual twin of `Port House Near
Warehouse`, because its geometry is that map's. The shipped game reuses these shells
across maps -- `Temple Home near Ilk` and `Port House Near Merchant` are both
House1/Rotation E -- but it always varies the furniture, and this room does not. That was
done to keep the cloned navmesh valid, which `test-pocket` shows was never required. The
fix is to delete the three cache files and rearrange the props; the engine will build a
navmesh to match. Not done yet, and not a blocker for testing.

**Also accepted:** the entrance is a walk-into trigger, not a click. The house has no
door entity -- the arch is painted into the wall -- and `CFreeRangePoly` hover has never
worked in a hand-built map, so the shipped relocate-fallback idiom is what this uses.
If the trigger fires while merely walking past, the polygon is too far out; if walking
into the arch does nothing, it is too far into the wall.

### 0.5 - getting caught, and what Juanita makes of it

Skill decides the *cost*, not whether the job is possible. Vanilla's own equivalent
robbery has no gate at all -- the entity called `hidden poly reveaked if perception
check passed` is `Active=1` with zero activations anywhere, so the name is aspirational
and anyone who walks near it triggers it. Rather than copy that, or hard-wall the quest
behind a stat a player cannot see, the skill buys you a quiet exit:

| | |
|---|---|
| **PE 5+ or Find Traps 35+** | nobody notices |
| **neither** | a guard is waiting when you step out |

The consequence is assembled from shipped parts. The transport is a copy of
`Eduardo Sends you to jail`, which fades, disables controls and relocates the party to
`Inquisition Chambers2 @ Jail Start`; **Sanchez is already there** with an 18-node tree
covering the fine, `Speech 35` and `Speech 50` negotiation, a Templar route and a
repeat-visit greeting. **Nothing in that flow strips inventory** -- verified across
`Jail Start` and Sanchez both -- so the treasure survives a sentence and the quest stays
completable. That was the one thing that could have sunk this design.

| # | Where | Steps | Pass |
|---|---|---|---|
| SR26 | The store room | Take the cache with **PE 5+ or Find Traps 35+** | You leave unchallenged. No guard, no dialogue. This is a separate, scripted check from the one that reveals the cache -- finding it is the engine's job, being *seen* is this one |
| SR27 | " | Take it with **PE 4 or lower and Find Traps under 35** | Step outside and a guard is there: *"You came out of a house that is not yours, carrying something that is not yours, and you did not even have the sense to do it quietly."* |
| SR27b | " | Rob the house **before** Juanita ever mentions it, then take the job and go back | The cache is there when you return. It was never present to be consumed early -- this was a genuine soft-lock until the cache was gated on the quest |
| SR28 | " | Same, but check the timing | He appears at the doorway you came out of, not somewhere across the yard, and the conversation opens by itself |
| SR29 | The guard | *"You will not take me anywhere."* | He turns hostile and fights. Killing him leaves you free, and you keep the cache |
| SR30 | " | *"I will come quietly."* | Screen fades, controls lock, and you wake in the Inquisition prison with Sanchez talking at you |
| SR31 | The cell | Check your inventory | **You still have what you stole.** If it is gone, stop -- the quest can no longer be completed |
| SR32 | " | Get out via any of Sanchez's routes -- pay the fine, `Speech 35`, `Speech 50`, or Templar | All work as they always did. Nothing here is new |
| SR33 | Juanita, after being jailed | Hand in the job | She is disgusted -- *"you sat in Sanchez's prison with my name in your mouth and my errand in your pocket"* -- and demands **300** |
| SR34 | " | Pay the 300 | You stay a member. The debt does not come up again |
| SR35 | " | Say you do not have it, leave, come back | The debt is still there as a reply on her hub. It does not quietly vanish |
| SR36 | " | With the debt unpaid or paid, try for the seduction | **She refuses either way.** Being jailed on her errand ends that possibility permanently -- the fee buys membership, not forgiveness |
| SR37 | Juanita, after fighting the guard off | Hand in the job | She takes you to bed as normal, but first: *"a dead guard at a rich man's gate is a thing people ask questions about. Next time you go quiet or you do not go."* |
| SR38 | Juanita, clean job | Hand in the job | Neither speech appears. Straight to the seduction, exactly as before this branch existed |

**Three failed attempts at one object, all invisible to every automated check.**
The advance first sat on the donor's hidden perception polygon, which shares a
footprint with a solid bookshelf, so the shelf took the click. Then the spawn point
turned out to be a `CSeriesAction`, which the engine describes as *"execute a
different action each time this action is executed"* -- one item per firing, so the
quest gate appended as item three never ran once. Then the replacement used
`CAISecretReveal`, whose search behaviour, radius and timing live entirely in the exe
(`CAISearchForTrapsAndSecrets` and `Secret Search Radius` appear nowhere in the game
data), and it still did not show.

It is now the same kind of object as the bookshelf -- visible, `Active=0` until the
spawn point sees the quest state, plain `GetCloseThenTrigger` -- because that is the
one thing in this room that has worked every single time. Every one of those three
builds parsed, round-tripped byte-identically, passed all 91 Gate 0 checks and
deployed correctly. They were all semantic, and only the running game showed them.

One correction that survives from that: `Skills/Thieving/Find Traps Secret Doors` is
**not** unused, as an earlier note here claimed. No script reads it via
`CVariableSkill`, but the engine consumes it through 443 `CAISecretReveal` instances,
and its own property text calls it *"the percentage chance you will find a trap within
X seconds"* -- a rate, not a threshold. It is still used here, but only for the
scripted were-you-seen check.

**The regression case that matters most:**

| # | Where | Steps | Pass |
|---|---|---|---|
| SR39 | Anywhere | Get jailed for something **unrelated** -- provoke Eduardo, the Church, Inquisition Foyer1, the Knights Templar or the Crossroads -- then go and see Juanita | **She does not care at all.** No disgust, no fee, seduction still available |
| SR40 | Juanita, after the seduction | Sleep with her on **CH 9 or better** | An on-screen line: *"You wake refreshed, and alone. Juanita has gone about her business."* Without it she simply vanishes and nothing explains it -- found in play |
| SR41 | " | Sleep with her on **CH under 9** | *"You wake refreshed, and alone. Your purse feels lighter than it did."* **She robs you**, scaled to what you carry -- up to 500 gold |
| SR42 | " | Count your gold before and after SR41 | The loss matches one of vanilla's brackets: 500 / 400 / 300 / 200 / 100 / 50 / 25, or nothing under 25 |

**SR40-SR42 are a vanilla defect, not one of ours.** Both seduction relays are
byte-identical to the shipped ones and the tree they open, `Juanita Seduction`, ships
with correct node names and real text in all nine nodes. But every node in it has **no
replies at all**, so it is a narration box that opens and closes by itself three
seconds after the relay fires, with no speaker and no portrait -- and in play it does
not register. The low-charisma path quietly takes up to 500 gold and tells you only
through that box. Fixt leaves the vanilla dialogue alone and adds a
`CPrintCombatTextAction` beside it, the same mechanism node 139 uses for "You have
become a friend of the thieves", which does show.

SR39 is guarding against a specific mistake. Vanilla sets a marker called
`been in jail before`, and keying Juanita off it would have made her hostile over a
Templar scuffle in another district. It is set and read **only inside**
`Inquisition Chambers2.zax`, purely to choose Sanchez's greeting, and **six** shipped
routes lead to that cell. Juanita reads two new markers instead, set only by this
arrest, and the build asserts that none of those six routes touches them.
### 0.5 - peace with the lava trolls

Settle the wererats -- cure them or destroy the Beggars, the trolls do not care which -- and
the Warning Troll will trade. That branch now also stands the pit down.

Four things were established in play before any of this shipped: a name-based action reaches
**every** entity sharing that name; it only reaches what has **already spawned**; the pit's
generators spawn lazily as you approach, so peace has to be maintained rather than declared;
and stripping an interaction specifier must be paired with adding one back or the trolls
become completely uninteractable.

| # | Where | Steps | Pass |
|---|---|---|---|
| T1 | Troll Pit, wererats **not** settled | Walk in | Vanilla: the Warning Troll confronts you, the pit is hostile |
| T2 | " | Take a Fight-icon reply | Combat, exactly as vanilla |
| T3 | Troll Pit, wererats **settled** | Talk to the Warning Troll, take the trade | He gives the hide **and the pit stands down** |
| T4 | " | Walk the **whole** pit, southern path included | Trolls spawning ahead of you settle within a second or two. None of them attacks |
| T5 | " | Click an ordinary troll | It **grumbles** -- one of three lines. It does not attack, and it is not inert |
| T6 | " | Click the **alpha** (taller, different model) | A conversation, not a grumble |
| T7 | " | Force-attack a troll | It works. Peace is refusable |
| T8 | " | After breaking it, walk on | Newly spawned trolls stay hostile -- the keeper is off |
| T9 | " | Look for the dead boss corpse | Still lying there, untouched by any of this |

T4 is the case the whole mechanism exists for, and the one that failed first time: a
one-shot pacify only calms what has already spawned. T5 is the regression on my own fix --
removing the attack cursor originally removed *all* interaction.

### 0.5 - the Helpful Wererat

A finished character the game never placed: `Helpful wererat.can` and
`wereratwarriorcan.DialogTree` both exist, both are complete, and **neither is referenced by
any file in the archive**. Same shape as the Goblin Girl in 0.1.0.

| # | Where | Steps | Pass |
|---|---|---|---|
| W1 | Sewers, Hall of Beggars, near Enrique Garcia | Enter the map on a fresh character | A wererat stands apart from the swarm and **does not attack** |
| W2 | " | Talk to him | *"Since you are a friend of beasts, I'll give you some advice. Never trust a thief and beware of the lava trolls."* |
| W3 | " | Ask where the thieves are | The eastern corridors, and a warning about traps |
| W4 | " | Ask where the lava trolls are | The lower levels, and advice to avoid them |
| W5 | " | Leave and return | He is still there and still talks |
| W6 | " | Attack him | He fights back like any wererat. Nothing else in the map changes |

W1 is the one to watch. He is `Team Number=Nutral` with `GetCloseThenTalk` on his own
template, so he should be approachable by construction -- but he stands in a hall full of
hostile Afflicted, and if the swarm's AI drags him into the fight before you can speak, the
placement needs moving rather than the character changing.

### 0.4 - Quinn's reagents

Three errands, in order, each unlocking a healing tier above vanilla's Extra Healing. Quinn
is in the Gate District; the offers sit under *"I have other questions"*.

| # | Where | Steps | Pass |
|---|---|---|---|
| Q1 | Quinn | Ask what you can help with | He asks for **three wolf pelts** |
| Q2 | Wilderness | Kill wolves **without** the Wolf Trapper perk, return | The plain pelts are accepted -- this is the vanilla-perk path and it worked before this release too |
| Q3 | " | Same **with** the Trapper perk | The quality pelts are accepted too. **This is the case that was broken**: a Trapper gets `Wolf Pelt Perk Quality` and the turn-in only took the plain pelt, so the perk locked you out of the errand |
| Q3b | " | Mix them -- some plain, some quality | Any three count, in any combination |
| Q4 | Quinn, after Q2/Q3 | Ask again | He asks for **five wasp stingers**. The pelt errand is gone |
| Q5 | " | Try to turn in with four | He counts, pushes them back, and says to bring all five. **No stingers are taken** -- 0.8.2; before it, four were consumed and the success speech played |
| Q6 | Ravine Cave West / Scar Ravine | Kill **Cursed or Tainted** wasps | Stingers drop. Plain wasps give none -- 6 of the 9 cans carry it |
| Q7 | Quinn | Turn in five | Accepted; the errand advances |
| Q8 | " | Ask again | He asks for a **lava troll hide**, and mentions the trolls are not animals |
| Q9 | Sewers, Troll Pit | Kill a **Lava Troll Boss** | It drops the hide. Ordinary trolls do not |
| Q10 | " | **Or**: settle the wererats first (cure them, or destroy the Beggars either way), then talk to the Warning Troll | A new reply appears and he **gives** you a hide. The pit does not turn hostile |
| Q11 | " | Same, wererats unresolved | That reply is absent. Killing remains the only route |
| Q12 | Quinn, after each turn-in | Ask what he set aside | **Great** after one, **Great + Superior** after two, **all three** after three |
| Q13 | " | Buy and drink each | Great heals more than Extra Healing; Superior more than Great; Supreme most |

Q10 and Q11 are the pair that matters: the peaceful route must appear only once the
wererats are settled, and it must work whether you cured them or exterminated them -- the
troll's grievance is pragmatic, not moral.

Q3 is the regression check on the bug this release fixes -- not Q2. The wolf cans branch
on `Wolf Trapper Perk Checker`: without the perk you get one plain `Wolf Pelt` through a
canned list, with it you get two `Wolf Pelt Perk Quality`. So the errand always worked
for ordinary characters and only ever failed for trappers, who were handed pelts their
own quest would not take.

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

### 0.9.0 - the Temple District

Eight items across three acts. **Two land in `3 Montaillou`, which no release has touched
before**, so Gate 1 for this release needs a character who has not entered Act 3 -- not merely
one who has not entered the affected level.

Reaching it: the Inquisition cases want a character who joins the Inquisition and kills the
Goblin Khan for Torquemada. The Machiavelli cases want his Barcelona bodyguard job played to a
conclusion. The Auric and Javier cases want a Templar initiate route.

| # | Where | Steps | Pass |
|---|---|---|---|
| TD1 | Torquemada, Inquisition Chambers | Join the Inquisition, take the Khan task, kill him, report | You reach **`407 killed khan`** -- *"I have known, child... Are you ready for another task?"* -- and are paid 150 gold |
| TD2 | " | Same, as a **non**-Inquisitor | You still reach `408` -> `409`, *"I feel there is now hope for your soul"*, and are paid 150 gold. **Unchanged from vanilla** |
| TD3 | " | Report as an Inquisitor and read the reply list | Exactly **one** Khan report reply is offered, not two |
| TD4 | Na Roqua, Montaillou witch hovel | Promise no harm will come to the Cathars, leave the hut, return | She greets you with **`100 Favorable Return`** -- *"Welcome spiritbearer and Cathar friend"*. **PASSED** |
| TD5 | " | Same, as an Inquisitor using *"I am willing to spare the Cathars"* | Same greeting. An Inquisitor who spares them counts as a friend. **PASSED** (the reporting character is an Inquisitor) |
| TD6 | " | Refuse or never make the promise | You get `03 Return Dialogue if Heard 50` as before. **Unchanged from vanilla** |
| TD7 | " | On the favourable greeting, ask about the shapeshifting Daeva your spirit named | She admits *"we once hunted together"* and describes the periapt in her cave. **PASSED**. The ask needs `met the demon` and vanishes once the cave is open |
| TD8 | " | Take that branch to its end | The **cave opens** -- she says *"Step through the fire"* -- exactly as the other phrasing of the question already does. **PASSED** -- the relay fires |
| TD9 | Witch cave | Walk through the fire, open the chest | You get the **Ring of the Prophet**, and it kills the shapeshifting Daeva permanently. **PASSED** as far as the Ring; the permanent kill is vanilla and untested here |
| TD10 | Montaillou inn | Save Machiavelli in Barcelona, then enter the inn | He is **at the bar**, greets you with `300`, and the speech runs through to *"Beware the Old Man from the east"*. **500 gold** is paid |
| TD11 | " | Refuse his partnership in Barcelona (`215 reject offer`), then enter the inn | He is at the bar on the customer side. He gloats -- *"you forced me to seek aid from those that seek to do us harm"* -- then **walks out the door**, and **two assassins** come in behind him and attack at once. They wear the game's assassin model, not the snake-women, and hit harder than Montaillou's guards. **PASSED** on the reporting save |
| TD11b | " | During that fight, cast spirit magic within sight of the Inquisition agent at the far table | He shouts *"Heretic!"* (or one of its variants) and **turns hostile**. **This is expected, not a bug**: the agent runs the shipped `Detect Spellcast` reaction that 107 Inquisitors and guards across the game share, and no vanilla spell-detect exempts an Inquisition member. Fight with steel and he stays a bystander |
| TD12 | " | Let him die, or kill him yourself, then enter the inn | He is **absent**. No ghost, no error |
| TD13 | " | Never take his bodyguard job at all | He is absent |
| TD14 | Sir Auric | Complete his first task as a **tainted** character | You get **`100 join tainted`** -- *"I didn't think someone like you could have completed the task"* -- and the sponsorship is granted |
| TD15 | " | Same as a **human** | You get `100 join`, the vanilla wording. Only one of the two is ever offered |
| TD16 | Lord Javier | Ask to become an initiate with **no** sponsorship and no second chance | **`190 need sponsor`** -- *"you'll need a sponsor. Perhaps Sir Auric will do it"* -- and the reply sets the *Seek out Sir Auric* quest |
| TD17 | " | Same **with** Auric's sponsorship | The old route to `100 auric initiate` still fires, and the no-sponsor reply is absent |
| TD18 | " | On his Montserrat directions, ask about the Sacred Lance | The lore node plays and its reply still leads to *Leave for Montserrat* |
| TD19 | Cervantes, Temple District | Talk to him, walk away, talk again | The **second** conversation opens `3 Return Dialogue` -- *"It was just here! Perhaps you saw it this time?"* -- with its four replies |

TD4, TD5, TD7, TD8 and TD9 have passed on the reporting save -- the whole Cathar-friend chain through to the Ring. TD11 has now been played through to working -- see the commit history for the six passes it took, each a vanilla idiom replacing an assumption. TD8 still carries risk. TD8 is a relay this release added to a node that
shipped without one, and if it fails the player gets advice about a cave whose door never opens.
TD11 is a **scripted fight in a map this project has never edited** -- new generators, new
positions, and enemies that must aggro on spawn. `Monster Cans/Assassin Machiavelli` is copied
from House of Ilk's working generator, including its empty `After Action`, but that is an
inference from one working case and only play can confirm it.

TD12 and TD13 are the negative cases for TD10/TD11 and matter as much: an arrival trigger that
fires unconditionally would put a dead man in the inn.

**Not in this release, deliberately** -- do not test for them:

- `Purify the Shadow Dryad` cannot be completed and is not wired. Na Roqua cannot be killed:
  AC 1000, HP 10000, full damage resistances, and a `Gotocombat` handler that banishes the
  player. Being banished is vanilla, and the live Fournier questline has dialogue for it.
- `401 already dead` and `402 tasks 3`'s pre-emptive Khan report stay orphaned, because the only
  thing they lead to is that chain.
- `105 join feralkin` is left alone: it carries no reply records, so a Feralkin gets the tainted
  variant.
- `ShylockeChests / 600 gold chest opened 2` is a superseded draft -- `... 3` already contains
  the whole verse.

### 0.9.1 - the areas around Barcelona

Two items. The gate wants a character who has not entered the Mongol Camp; the clover works
on any save but wants a character with Luck 3 or less who has not yet taken Brendan's drink.

| # | Where | Steps | Pass |
|---|---|---|---|
| AB1 | Mongol Camp gate | Enter the camp for the first time; take any of the four peaceful routes past the guard (Grumdjum's friend, Horde messenger, Schmooze, Speech) | The challenge plays once as before. Leave the camp and come back through the gate: **`3 Return Dialogue`** -- *"Greetings goblin friend. What do you want?"* -- with the audience ask (Speech 40), the Darsh ask only while the Darsh quest is current, and *"Nothing today. I will be on my way."* |
| AB2 | Mongol Camp gate | On the return greeting, pick *"I have come to rid this forest of your existence, monster."* | The camp turns hostile, exactly as the same line does on the first meeting |
| AB3 | Mongol Camp gate, negative | Enter, get challenged, and leave without being welcomed or fighting (e.g. *"I come in peace"* goes hostile, so this needs the Darsh route or a quick exit); come back | Silence at the gate, as vanilla. No second challenge |
| AB4 | Mongol Camp gate, negative | Make the camp hostile by any route, then cross the gate again | Nothing fires |
| AB5 | Port District tavern, Brendan (Luck <= 3) | Take his drink | After *"Take a healthy tug from the Serpent's Bile..."* he notices your luck (`200 low luck`, or the `lass` twin for a woman), and you receive **Sullivan's Clover**; then *"Grand. Now, what can I do fer ye?"*. The clover equips at the neck and shows +1 Luck |
| AB6 | Port District tavern, Brendan (Luck >= 4) | Take his drink | Straight to *"Grand. Now, what can I do fer ye?"*; no clover |
| AB7 | Brendan, negative | Talk to him again after the clover | The drink is not offered again (vanilla `took irish drink`), so no second clover |

### 0.10.0 - Montserrat

**Needs a character who has never entered Montserrat**; Tier 0 (MS1) and the Javier and
Michel replies are dialogue and work on any save. Play order: Grove -> Level 1 -> Level 2 ->
Barcelona (Javier) -> Montaillou (Michel). Positions were chosen from the maps' own body
clusters without a walk mesh, so the first pass is as much about *where things landed* as
whether they work; note any body, polygon or prop that is off the floor or in a wall.

| # | Where | Steps | Pass |
|---|---|---|---|
| MS1 | Montgomerie | Reach `45 prophecy 2` | *"How long ago did they come?"* plays the voiced `60 not long`, then Michel |
| MS2 | Grove gate fight (2730,705) | Click the knight | `<...shield still on his arm...>`; Read -> three entries -> Take. Second click: `2 taken`, Read it again offered, Take not |
| MS3 | Grove | Walk the ruins | Packs are mixed: snakebreed, a human assassin in most packs of three, a Summoner in packs of four. One assassin near (2650,1150) calls *"The Scion! To me!"* on his first wound and two packs arrive |
| MS4 | Grove, negative | Kill the sentry in one blow | No call, no reinforcements |
| MS5 | Grove hovers | Click the campfire (near 4400,3400), the dead snakebreed at the gate | Balloons; the campfire's second line at PE 7+ |
| MS6 | Level 1, y=1700 | Cross the hall southward | `<Behind you...>` and three assassins fade in north of you. With Sneak 40+: nothing |
| MS7 | Level 1 (2000,1900) | Click the man in black among the dead | Laughs; who (Speech 40 / *"Ask the snakes"*), where, why; Demokin and Saladin lines if applicable; Finish him -> pain sound, corpse, polygon gone, +100 XP; questions +150 XP once |
| MS8 | Level 1, before the inner door (y~2800) | Cross it | Poison and the needle line; at Find Traps 35+ the tripwire line and no damage |
| MS9 | Level 1 (2450,2450) | Approach | One assassin breaks and runs for the inner door and vanishes there |
| MS10 | Level 1 hovers | Barricade at the entrance, jailor body (2312,2450), a candle stand (2479,1263), the druid gate | Balloons; jailor and candles have PE 7+ lines; the gate reads four ways (Wielder / Sylvant / IN 6 or Educated / plain) |
| MS11 | Level 2, west chest (1143,365) | Open it | Two assassins fade in a second later; at Lockpick/Disarm 35+ the needle line and no assassins |
| MS12 | Level 2, sanctum threshold (x~3500) | Cross | Sahar spawns and speaks; nothing else in the sanctum attacks during the talk; Outwit 7 offers the courier line. Enough talk / closing the window -> she and two Venom and a Summoner fight, and the sanctum's own snakebreed rejoin (courier: she fights alone) |
| MS13 | Sahar at 60% and 25% | Fight her | *"To me!"* and two assassins at the threshold (three if MS9's runner got through); at 25% the heal effect and *"The Master is not done with me"* |
| MS14 | After Sahar | Kill everything near Montgomerie | He speaks (vanilla gate). Templar: *"I am of the Temple, brother"*; journal: `21 the captain` |
| MS15 | Level 2 hovers | Altar (3900,2200), the dead at (3975,2365), the Inquisitor at (2685,1020) | The reliquary line; the missing-monks line; Inquisitor IS sees the sealed order |
| MS16 | Whoever sent you: Amir, Raphael, Cedric, or Javier (cathedral) | Report Montserrat carrying the journal | *"Sir Tomas de Vilanova led the Templars..."* -> the patron's own node, book taken, +500 XP, *Sir Tomas's Journal* closes, back to the report node for the vanilla reply |
| MS17 | Michel, Montaillou | After questioning the assassin | *"I know who attacked Montserrat..."* replaces the vanilla question; `141 out of the east` |
| MS18 | Negative | Sahar's tree cancelled with Escape | The fight starts anyway |
| MS19 | Port District, Fernand and Juan | Take Fernand's job; go to Juan | Fernand hands over *Fernand's Draught* (not a plain potion); Juan shows the interaction cursor, and Absorb Spirit cannot target him from any range; the draught saves him: he stands, walks to Fernand, and six balloons play -- three vanilla, three of Fernand chiding him -- before he walks to the ship. Leave him instead: *fading* at 20 seconds, the too-late line and the failed state at 45. The Mute Sailor's reward is a plain potion again. **PASSED** on a fresh Port District |
| MS20 | Scar Ravine, the goblin holding the girl | ST 8+: *Try.* / Barter 55: the salt-pork offer | The goblin backs down (`71`) or takes the trade (`72`) in his own words; neither mentions the Khan. The Horde and Speech routes still get *"Y-you know the Khan?"* |
| MS21 | Any vodyanoi spawned after install, with the Anatomist perk | Hit one | A second damage entry per landed hit, 4-10 Piercing, in the combat log and on screen. **PASSED** from the save's log |
| MS22 | Amir, as a Favored One | *"What troubles the Order, Amir?"* -> *"Of course, I will accompany you"* | The cathedral summit plays for Saladin: Javier's opening, Amir's two lines, the exchange, the directions, *"May the Prophet guide you"*, fade, and back to the Gate District with Montserrat on the map. Amir never hostile. **PASSED**, on a save that had not entered the cathedral |
| MS23 | Troll chief, after *Speak for the Trolls* completes, Quinn's hide errand open, no hide held | Talk to him | *"The herbalist in the city needs the hide of a lava troll..."* -> he gives one from his dead. Absent with a hide in hand or the errand turned in |
| MS24 | Enrique, after the contract is withdrawn | Either greeting | *"You said there was one thing more you needed, before the trolls came between us."* -> his confession -> the cure quest, exactly as the kill route gives it. Absent once the cure quest has ever been given |
| MS25 | Quinn, fresh shop | Complete an errand, then *"Can I see what you have for sale?"* | One shop window with the earned tiers in it (Great Healing after pelts; Superior after stingers; Supreme after the hide); no reserve reply anywhere. On a save that entered the shop before 0.10.0: the plain shop, and *"What have you set aside for me?"* on the greeting |
| MS26 | Quinn, any greeting | *"Is there anything around here I could help you with?"* | `805 errands`: the next open errand offered; the reply gone once the troll errand has been given |
| MS27 | Thieves' stash chest (Main Entrance top-left, or Congregation SA1), Sneak below 25/30 | Open it | Loot drops, then *"Oi! Hands off the guild's take!"* over a thief, then the guild turns; the line is in the log |
| MS28 | Same chest, Sneak at or above the threshold | Open it | Loot drops and *"<Nobody is looking your way...>"* over the chest; nobody turns |
| MS29 | Same chest, Sneak below the threshold, every `Sewer Thief` on the map dead | Open it | Loot drops, no bark, nobody turns (Juanita and the dogs stay as they were) |
| MS30 | Inquisition Chambers jailor, as an Inquisitor | *"I am eagerly awaiting training on the Rites of Confession"*, take the keys, talk to any cell prisoner, return | *"I have spoken with the possessed..."* offered; the lesson pays 250/100/25/5 XP by Speech, the belt at the top; not offered again |
| MS31 | Same jailor, as a Templar or with Speech 30, not an Inquisitor | *"I'm here on important business from the Knights Templar"* | Keys given; the reply is gone on the next greeting, and *"How do you get inside these cells?"* is not offered |
| MS32 | Montserrat Level 1 needle trap, Find Traps below 35, fresh map | Walk the strip before the inner door | Poison, the generic trap message, and *"<Something gives under your foot...>"* over the character |
| MS33 | Knights Templar armory, fresh map | Attack Auric, wake in the cell, walk back to the armory | About a second after entering, *"Save your belligerence..."* (voiced) over Auric, logged; not again on the next entry; he talks normally after |
| MS34 | Javier, after Esteban has died with the Esteban step given and not done | Any greeting | *"Sir Esteban is dead."* -> the weighs-heavy line -> the Auric step given; the reply gone once Seek out Sir Auric exists |
| MS35 | Cathedral, fresh map | Attack Javier, wake in the cell, walk back in | About a second after entering, *"If you blaspheme this cathedral again..."* over Javier once; an extra guard beside him on this and every later visit |
| PM1 | Grove, fresh Montserrat, walk to the gate | Enter the gate area | The sentry appears passive and *"Far enough..."* opens on him; no pack attacks during the talk |
| PM2 | PM1, *"I am not. <Draw.>"* or Escape | - | He draws, *"The Scion! To me!"*, both reinforcement packs come (Tier 4 unchanged) |
| PM3 | PM1, *"Take me to your captain"* -> *"Take it"*, carrying a named weapon and a rolled magic one | - | Every weapon and all ammunition gone from the inventory; fade; wake in the den at the back |
| PM4 | After PM3, get out and return to the gate | Look at the ground by the sentry | The named weapon itself, a plain base for each rolled one, and two good weapons; the garrison passive, *"Keep walking, Scion"* on a click |
| PM5 | PM1 with Outwit 6 | The armed reply | Delivered with everything kept |
| PM6 | PM1 as Demokin or Sylvant | *"Look at me..."* | Delivered unsearched |
| PM7 | In the cell | Click the door | Locked; with Lockpick 35 it opens; the guard room, the stair, Level 1's south-west room |
| PM8 | In the cell, ST 8 | Click the floor by the door's pins | *"The lower pin shears..."*, the door opens, the handler attacks; with ST below 8, *"Old iron, old stone"* |
| PM9 | In the cell, Speech 40 or CH 7 | Talk to the handler through the bars | *"...Fine. Ahead of me, and slow"*, the door opens, *"Up the stair"* over him; the monks and the old man questions answer |
| PM10 | In the cell | Talk to Brother Pau through the bars, ask how to get out | The drain; click the straw -> *"a square of darkness"* and you are in his cell; his door opens on a click |
| PM10b | In the cell, PE 7, without talking to him | Click the straw | The same, unaided; below PE 7 and untold, *"Straw, old and flat"* |
| PM11 | In the cell, do nothing for five minutes | - | The door opens and *"The captain will see you now"* plays |
| PM12 | Level 1, never delivered | Walk down the stair in the south-west room | The undercroft: two cells, doors closed and unlocked, no handler, no monk; the stair hover reads |
| PM13 | Any of PM7-PM11, then walk back down | - | The pen state persists; no second setup; no timer restart |
| PM14 | The Animal Den | Enter | Vanilla: three bears, no door |
| TP1 | Troll Pit, at peace, the Red Ore Trade carried to the chief | *"I will see he keeps to it. <Go and take it.>"* | The chest across the pit opens with the ore sound; one Red Ore on it; the trolls do not move |
| TP2 | Troll Pit, at peace, chief alive, ore not yet paid | Open the ore chest | *"That is ours"* over the chief, then the desecration scene and the trolls turn |
| TP3 | Troll Pit, fought in, no peace | Open the ore chest | Plain: animation, one ore, no reaction |
| PM15 | Delivered, arrive at Sahar (escort or walk) | - | *"You walked in. Good. It saves rope"*; the offer reply present; a fighter who walked in gets *"You are late"* as before |
| PM16 | PM15, *"Then send me north..."* -> *"<Take the ring.>"* | - | Sahar's Ring in inventory; nothing in the sanctum attacks; the Montaillou quest in the journal; walk out by the doors through a passive garrison |
| PM17 | PM16, Montaillou, Brother Michel, Advice | *"...Their captain sent me north with this"* | *"A snake eating its tail..."*; the reply absent without the ring |
| PM18 | Kill Sahar by any route | - | *"...every one of them, everywhere, turning for the door"*; every pack on Level 2 runs for the Grove exit; on Level 1 and the Grove the same; nothing new spawns hostile |
| PM19 | Delivered, quiet escape (lock + Sneak, or drain), walk Level 1 | - | Packs passive with the Keep-walking click |
| PM20 | Delivered, loud escape (pins, or caught) | Walk Level 1 | Packs that spawn after are hostile |
| PM21 | Holding the ring, Montaillou inn, saved Machiavelli | After his supplies line, *"You have seen this before"* | `301`/`302`; the reply absent without the ring |
| PM22 | Holding the ring, Montaillou inn, refused Machiavelli | *"Before your friends come in"* | `232`; he walks out alone, no assassins; without the ring the 0.9.0 ambush as before |
| PM23 | Holding the ring, Crypt Burial Chamber assassin | *"Your captain at Montserrat sent me north under this"* | `21 her mark`, then the vanilla vanish-and-fight exactly as `20 threat`; the reply absent without the ring |
| PM24 | Grove, the second cave (wasp nest), fresh | Enter; the hover at the mouth; go to the deep west chamber | The cave loads; *"The floor of the cave is paper..."* a second after arriving; a cursed wasp twice the size, named Wasp Queen, 200 HP; two stingers on death |
| CP1 | Trapped Ether Plane, the Enchanter, `50 Escape` | *"The crystal you fashioned. It only needs enough energy..."* -> the continue replies at 55 and 57 | `59 Winner`; he stands down and *"I am still watching you"* on a click; the undead stay hostile; the lie route and `53 Whoops` unchanged |
| CP2 | La Calle Perdida, fresh, a Wielder who killed Relican | Talk to any generic wizard | *"Welcome, fellow Wielder. We have heard much of your victory over Relican"*; `60 Membership` has no fight reply |
| CP3 | La Calle Perdida, fresh, a Wielder who has not, and a non-Wielder | Talk to a wizard | The greetings as before |
| CP4 | La Calle Perdida, fresh | Attack Cedric, the random map, walk back in | *"You have strained what little welcome you had..."* (voiced) once over him; not on a first entry |
| CP5 | After Relican's takeover | Attack Relican, the random map, walk back in | *"I trust you have come to your senses?"* once over him |
| CP6 | Dark Wielder, Relican's `30 power` | *"Power is what you took from the Wielders..."* -> *"With the ones you drove out of here..."* | `80 war`; Relican, the Undead Guard and Brambles the Man attack; Relican takes damage and spells; no random-map relocate |
| CP7 | CP6, kill Relican | - | *"<He goes down the way he stood...>"*; XP; the four Dark Wielder quests failed in the journal; a generic wizard then greets you as the one who killed Relican |
| CP8 | Wielder, Cedric's secondary greeting | *"Is there anything else the Wielders need?"* | `140`; accept -> the crystal quest in the journal; the reply gone after; a non-Wielder never sees it |
| CP9 | Fresh Lake map, quest active | Click the node three times, kill the waves | The journal advances to *"The crystal draws the dead..."* when the third wave strips the click |
| CP10 | CP9, Cedric | *"I went to the crystal by the lake. It raises the dead."* | `141`; quest complete; 400 XP; Cedric's Ward in inventory (no slot, sellable) |
| CP11 | Fresh Plains / Coast / Lake / Grove, walk near the red node | - | *"<A crystal the colour of old blood...>"*; the PE 7+ and Wielder variants; after the third wave the spent line |
| CP12 | Inquisitor, turn the Calle over | Watch the wipeout | Wielders that appear during it die on generation as the shipped relay intends |
| CP13 | Brambles, pour the potion, the man | - | After his thanks, one of three random barks over him 1.5 s later |
| CP14 | Fresh Port District, recruit Fernand, fight beside him | - | He closes to arm's length before swinging; no hits from across the room |
| CP15 | Fresh Inquisition Pit3 (Galileo's cell) | Attack Galileo, the random map, walk back in | *"Beware braggart, I have less tolerance now for your idiocy"* (voiced) once over him; not on a first entry |
| CR7 | Crypt `7 Doomed Plateau`: talk to Jehanne, reach `50 Counsel` then `100 spoke to counsel`, and convince her (*"Jehanne, I speak for the Council..."*) | Walk away, leave the map or let the conversation end, then talk to her again | *"You have returned"* -- the civil greeting, with *"Do you know where the efreet is?"* among the replies. **Before this release every return was *"I warn you, monster"* even after convincing her**, because the checker was set nowhere |
| CR8 | CR7, then say goodbye from the civil greeting | *"No, I will return when I do. Goodbye."* | `5 Goodbye Joan Likes You`: *"Dieu est avec vous."* Unreachable before this release |
| CR9 | Do **not** convince her; return and talk again | - | Still *"I warn you, monster, leave this crypt with haste"*. The warm greeting must not open for a player who never spoke for the Council |
| CR10 | **A save that has never entered `2 Retreat of Souls`.** Walk in from the Retreat of Souls Entry and head south-east towards the first zombies | - | A Templar knight is standing at (3060, 2140), in the open ground the zombies spawn into. **Check he is on floor and reachable, and that the horde attacks him** |
| CR11 | CR10, talk to him | *"I'm not here to steal the relic, I'm here to protect it."* | `10 relic`: *"Are you a Knight? Have you been sent to reinforce us?"* -- then the Templar answer, the lie, or the honest refusal, and the quest opens (CR1) |
| CR12 | CR10, attack him instead | - | He goes to combat and says *"You will be destroyed!"* (`20 monster`). **Before this release the clone's damaged script fired a relay that does not exist on this map, so he would have died without fighting** |
| CR13 | Doomed Plateau, talk to the knight by the entrance repeatedly | - | The barks vary across the nine written lines rather than repeating *"Evil things lurk in the darkness"* every time |
| CR14 | **A save that has never entered `1 Crypt Entrance`.** Walk to the sealed shrine door; a stairwell now stands beside it | Step onto the stair | You arrive in **The Garrison's Camp**. **Check the stair is visible, reachable, and not inside the door's own polygon** |
| CR15 | In the camp, walk back into the transition polygon | - | You return to `1 Crypt Entrance` at the stair, not at `Start Here` and not into a wall |
| CR16 | In the camp, look around | - | No zombies, terrors or festering undead spawn: the four horde spawners inherited from `3 Misc Crypt 1` are stood down. Three Templar knights are standing there |
| CR17 | Talk to the camp sentry | *"I'm not here to steal the relic, I'm here to protect it."* | `10 relic` -> *"Are you a Knight? Have you been sent to reinforce us?"* -> the quest opens (CR1), now reachable **before** the Doomed Plateau |
| CR18 | Talk to the knight at the fire, and to the one on the wall | Each branch in turn | `1 the fire` through `12 Jehanne`, and `1 the wall` through `41 what we are`. He sends you to Jehanne on the plateau and tells you to speak to her Council first |
| CR19 | CR18 after taking the quest from the Spirit Council (state `CRY2CURS`) | *"I am here to end it."* / *"I may be him."* | `30 end it` and `42 the order` -- both absent without the quest state |
| CR20 | CR18 after speaking to the Spirit Council at all | *"Your commander says the Council has not spoken to her in a long while."* | `20 the council`; absent to a player who has not been to the Council |
| CR21 | Attack any of the three camp knights | - | He goes to combat and gives the garrison's *"You will be destroyed!"*, as the forward knight does |
| CR22 | Crypt, any trap, with `Lockpick Disarm Traps` **40 or better** | Click the trap | It disarms as before: the sound, *"Disarmed Trap"*, 75 XP, and the trap's polygon goes dead |
| CR23 | The same trap with the skill **under 40** | Click the trap | *"The mechanism is beyond you"*, and the trap is still armed -- walking over it still triggers it |
| CR24 | CR23, then raise the skill to 40+ and click the same trap again | - | It disarms. **`Trigger Only Once` was 1 in vanilla, so without this release's change to 0 the failed attempt would have locked the trap forever** |
| CR25 | A trap in any act **outside** the Crypt (the Sewers, Alamut, the Shrine) with no skill at all | Click it | It still disarms for free: the 241 shared-can uses elsewhere in the game are untouched |
| CR26 | Crypt, the Efreeti, with any Thought magic skill at 80+ | *"<Read the wish itself.>... Grant mine straight."* | `211 true wish` -- the same node IN 6 + Speech 95 reaches. Below 80 the reply is absent, and the social route still works |
| CR27 | Montaillou, Brother Michel, ask how the complex was sealed, with Divine **or** Tribal magic at 80+ | *"A seal like that is not a wall, it is a promise..."* | `161 how a seal is broken`; he admits the order used borrowed desert magic. Absent below 80 in both schools; present from either of his two seal nodes |
| CR28 | Crypt, find the broken coffins on `2 Retreat of Souls`, `7 Doomed Plateau`, `8 Ante Chamber`, `9 Burial Chamber` **without** Necrosage or the Necromancer title | Click each | Bones and dust -- one plain line each. **Check each marker is visible and clickable where it stands** |
| CR29 | CR28 carrying **Necrosage** | Click each | The four readings: died twice, killed nine times, opened from the inside, and the untouched original tenants |
| CR30 | CR28 carrying the **Necromancer** title instead | Click each | The same four readings: the check is Necrosage OR Necromancer |
| CR31 | Crypt, Jehanne, as a **Templar**: claim the Lance for the order, then press her | *"look at the shield properly, commander"* | `43 the successor` -> `44 what we became`. She stops, will not call you a liar again, and still refuses the Lance |
| CR32 | As an **Inquisitor** | *"I hold the Church's writ over the unquiet dead"* | `45 jurisdiction`: Rouen, and then the practical point. `46 the same enemy` from the conciliatory reply |
| CR33 | As a **Knight of Saladin** | *"A Saracen of my order stood where I am standing"* | `47 the lamp` -> `48 undo it`. Then the Spirit Council's `31 the Saracen was yours` from its wish account |
| CR34 | As a **Wielder without** the Necromancer title | *"It was not a curse. It was a contract, badly worded."* | `49 the binder`. The Dark Wielder reply must **not** be offered |
| CR35 | As a **Wielder carrying** the Necromancer title | *"Your Council is right about me."* | `50 she was right` -> `51 not your knights`. The plain Wielder reply must **not** be offered: the two are mutually exclusive |
| CR36 | As a member of the **Goblin Horde**, or carrying Goblin Champion | *"I ride with the Horde of the Khan"* | `52 the khan` -> `53 nothing to weigh`; offered from her first meeting, her hostile return and `10 jehanne` |
| CR37 | Carrying the Bleeding Lance, talk to Jehanne from her **civil** greeting (needs CR7) | *"I have recovered the Bleeding Lance."* | `200 have lance` -> `201 what now`. **Vanilla pointed at a node that does not exist; before this release the reply led nowhere** |
| CR38 | **A save that has never entered the Misc Crypts.** Walk into each of the four | - | Each map now says what it is, once, as you enter: the rear passage, the stone door, the last coffin's walls, the three crypts. **Check each voice fires where the polygon is and not through a wall** |
| CR39 | `3 Misc Crypt 1`: throw the lever by the wooden door | - | *"The bar drops into its brackets"*; the door closes visibly (it starts Open); tide +1 |
| CR40 | `4 Misc Crypt 2`: pass the stone door, then throw the lever behind it | - | *"The counterweight drops and the stone seats itself"*; `Door1` closes; tide +1. **Check the door can still be reopened normally so nobody is sealed in** |
| CR41 | `5 Misc Crypt 3`: throw the lever by the last coffin | - | All thirteen protect walls open at once; tide -1 |
| CR42 | `6 Misc Crypt 4`: throw vanilla's crypt-opening switch | - | The three crypts open and spawn as they always did, plus *"whatever the garrison was keeping in here is loose"*; tide -1 |
| CR43 | With tide **positive**, ask the knight at the fire how the line stands | *"How does the line stand today?"* | `60 the line has moved`. With tide negative, `61 the line has slipped`; at zero, `62 the line is where it was`. Exactly one of the three replies should ever be offered |
| CR44 | Free the knights (CR4) with tide **positive** | - | *"freed in good order"* -- they go out from the corridors you shut first |
| CR45 | CR44 with tide **negative** | - | *"freed into a ruin"* |
| CR46 | CR44 having touched no lever at all | - | *"freed from a stalemate"* -- the siege stops having two sides. **This is the vanilla-equivalent path: confirm a player who ignores tier 8 entirely still completes the quest normally** |
| CR47 | Recruit Jehanne on the Doomed Plateau | - | She says *"Let us cleanse this place of evil."* over her own head as she joins -- **the first time this line has ever played** |
| CR48 | Talk to her as a companion, answer *"No, wait here for my return"* | - | `600 Companion Wait`: *"If that is your order, I will wait and guard here until you return."* Then the reply *"Hold this ground until I return."* closes the conversation. **Check it closes cleanly rather than hanging** |
| CR49 | Take her into the Burial Chamber and **attack a garrison templar** | - | She turns on the player (`601 Joan Leaves party and Attacks Player`). **This has never fired in vanilla; it is the one thing in tier 9 most worth watching** |
| CR50 | CR49 without her -- enter the Burial Chamber alone and attack a templar | - | Nothing of hers fires, no error. The check now asks whether she is alive on the map, so an absent companion must read as absent |
| CR51 | Take the Bleeding Lance with her beside you, then walk away from the plinth | - | *"the relic is *safe* at last. I may finally...rest..."* Fires **once**: walk back in and out again and it must not repeat |
| CR52 | CR51 without her, and CR51 without picking up the Lance | - | Silence in both cases |
| CR53 | Ask the Spirit Council *"Who do you think I am?"* as each spirit | - | Ancestral -> `11 we see your dead`; Beastial -> `12 we see the beast`; Demonic -> `13 we see the pit`. **Exactly one of the three should ever be offered** |
| CR54 | CR53, then *"Then tell me the rest of it."* | - | Lands on `20 The Wish Explained` and the vanilla story runs normally from there |
| CR55 | Reach `40 Pious Child` with karma **1200+** | *"You are asking a great deal of a stranger."* | `41 we know what you are`. With karma **800 or less**, `42 we asked anyway`. Between the two, neither reply is offered and the node is exactly as vanilla left it |
| CR56 | CR55 -> *"I will see what I can do."* | - | Quest state `CRY2CURS` activates, same as vanilla's own reply on that node |
| CR57 | Ask Jehanne *"Tell me about yourself"* as a **female** Scion | *"They burned you for wearing a man's armour..."* | `54 the same armour`. As a **male** Scion, *"What was the charge, in the end?"* -> `55 the charge`. Never both |
| CR58 | From `54`/`55`, take each of the three routes out | - | `100 spoke to counsel` (only when the Council has been spoken to), `50 Counsel`, `5 Goodbye` |
| NO1 | **A save that has never entered act 5.** Walk in from the wilderness | - | Huko, General to the Hujark, and his guard are standing up the path. **Check first that he is on the floor and can walk to you** -- this spawn point has never run in the shipped game |
| NO2 | Stand still after arriving | - | Within a second or two he crosses the ground towards you and opens *"Where do you stand, stranger? Have you come to harm the Prophet, or help us save him from the Druids?"* He must **talk, not attack** |
| NO3 | Walk away before he reaches you, then click him | - | Same conversation, `1 Conversation Start`. His talk specifier had no action at all in vanilla |
| NO4 | Close the conversation without choosing, then click him again | - | `3 Return Dialogue`: *"You return? Have you changed your stance?"* -- **never reachable in the shipped game** |
| NO5 | Answer *"I have come to help the Prophet"* | - | *"Good to hear, friend."* The quest **Protect Nostradamus from the invading English forces** enters the journal, and Huko and his guard walk off, fade and vanish. Neither quest could be entered at all before this release |
| NO6 | Instead answer *"If getting to the Prophet means killing you, then you're my enemy"* | - | The quest **Defeat the Hujark defenders and capture Nostradamus** enters the journal, he says *"Then I will kill you with my own hands!"*, and the fight starts |
| NO7 | As an **Inquisitor**, reach any of his nodes | *"In the name of the Inquisition, your cult dies here."* | Replaces the ordinary fight reply -- the two are gated `Inquisitor IS` / `Inquisitor NOT` and never both |
| NO8 | Attack Huko or his guard without talking at all | - | The damaged-script fires: the English quest enters the journal and both turn on you |
| NO9 | After NO5 or NO6, reach `05 Nostrodomus Demesne` | - | The active quest completes on arrival. **In vanilla this completion fired against a quest that had never been activated** |
| NO10 | Leave the act to the wilderness and come back | - | Exactly one Huko. `Already Generated=0` must not produce a second |
| NO11 | Stand near Huko for half a minute before talking | - | He barks the Hujark lines every five seconds or so (`HujarkWarriorCanned`, eight nodes). Confirm they position over **his** head |
| NO12 | **A save that has never entered act 5.** Fight the Hujark on the Heart Entrance and wound a **helmeted** swordsman past half health | - | A snake erupts from the floor within about 75 units of him and joins the fight. **This is the whole of tier 2: if no snake ever appears, the clone is not resolving `$Trigger` and the act simply fights as it always did** |
| NO13 | NO12 on `02 Clan of the Hand A`, `03 Tourniquet of Pain`, `04 Clan of the Skull B` and `07 Cave 2` | - | The same. 03 has the most summoners of any map (13 generators) |
| NO14 | Wound an **unhelmeted** swordsman, a shaman, or a snakebreed past half health | - | Nothing. Only shield-helmet swordsmen summon |
| NO15 | Wound **Huko's guard** past half health during the opening conversation | - | Nothing -- he is a named character and was deliberately excluded. A snake appearing mid-conversation would be the bug |
| NO16 | Kill a helmeted swordsman in one blow from full health | - | No snake: the trigger is a crossing below 50%, not a death |
| NO17 | Let the same swordsman summon, then check he does not summon again | - | One snake per swordsman per crossing |
| NO18 | Watch the party level a snake is summoned at | - | `Snakebreed Venom` for a weak party, `Venom Tough` for a stronger one -- the source generator's four `Max Party Mojo` groups should still scale |
| NO19 | **Balance read.** Cross a whole map fighting normally and count the snakes | - | If the act feels longer rather than more varied, the fix is one number (`Constant Value=50`) or one checker per map. Record which map felt worst |
| NO20 | **Carrying Sahar's ring**, enter act 5 and wound a helmeted swordsman past half health | - | No snake. Instead, once per map: *"The Hujark strikes the floor with the flat of his blade and calls... Nothing comes up out of it."* |
| NO21 | NO20, then wound a second and third helmeted swordsman on the same map | - | No snake and **no repeat of the line** -- `the mark has been read` holds it after the first |
| NO22 | NO20, then cross into `02 Clan of the Hand A` and wound a helmeted swordsman | - | The line plays once there too. The mark is set on all five summoning maps from the Heart Entrance, through `COtherMapAction` |
| NO23 | Enter act 5 **without** the ring | - | Snakes as in NO12. This is the path that must stay unchanged |
| NO24 | Sell or drop the ring before entering act 5, then enter | - | Snakes. The check is made on arrival at the Heart Entrance, so what matters is what you are carrying when you walk in |
| NO25 | Enter act 5 with the ring, having **killed** Sahar rather than taken her word | - | Not reachable: the ring is only given at `50 her word`. Worth confirming there is no other source |
| CR1 | Crypt, reach a talking Templar knight (`7 Doomed Plateau` or `9 Burial Chamber`), answer that you are a Knight or will help | *"Then I am at your orders. Where is she?"* | The journal opens **Release the Doomed Knights from their Torment** at state 1. Before this release the quest had no states at all |
| CR2 | CR1, then the Spirit Council on `7 Doomed Plateau`, hear the wish out to `40 Pious Child` | *"I will see what I can do."* | State 2. Also reachable from `30 Efreet`. A player who never talks to a knight should still get the quest here |
| CR3 | CR2, find the lamp of Jah'roosh in `9 Burial Chamber` and talk to the Efreeti | *"<Say nothing yet, and look at the lamp.>"* | State 3, whose text warns that the garrison is undead too. The reply loops back so the wish menu is still available |
| CR4 | CR3, wish the curse undone | *"I wish to undo the curse laid upon Jehanne's soul..."* | `100 save inga`; the quest completes and pays 2,500 XP; the existing relays (`Wished to Save Inga and Knights`, `Efreet goes away`) still fire |
| CR5 | Kill Jehanne, then talk to the Spirit Council | - | Its Joan-dead curse plays and the quest **fails** if it was active. If she dies before you ever met a knight, the quest was never active and nothing should appear in the journal |
| CR6 | Take the quest, then let Montaillou burn (`02 Hamlet Burned`) | - | The vanilla failure sweep fails it, as it always tried to -- now against a quest that has states to fail |
| TO1 | Toulouse, Lethos, reach `50 Lucius is the fugitive` by any of the five routes (nodes 20, 22, 22-tainted, 23, 24) | - | Nothing visible; the flag `PC is told Toulouse was harboring Lucius` is now set on every one of them |
| TO2 | TO1, then reach Thierry in the pen and ask about the town harbouring one of their kind | *"The titans said this town was harboring one of their kind, is that true?"* | `30 Lucius` -> `32 Lucius 2` -> `34 Alexander eaten`; offered from both `20 Questions` and `25 The rest of the townspeople`; absent to a player who never heard Lethos say it |
| TO3 | Toulouse, Iapetus, walk the caged-humans chain to `35 Humans not informed` | *"I want to talk to the prisoners."* | He refuses (`37`); afterwards Poimaino offers the bluff. Without asking Iapetus, the bluff reply is absent |
| TO4 | TO3, then Poimaino at Speech 95+ / below 95 | *"It's okay, Iapetus said I could speak with the prisoners."* | `30 bluff SUCCESS` -- he stands down and the pen is enterable without him turning hostile / `30 bluff FAILURE`, he refuses; exactly one of the two replies is ever offered |
| TO5 | Toulouse, get the flask from the rock (Mathuo's `10 Shapeshifter` -> *"Where were you when the attack occurred?"* first), then Poimaino at Speech 50+ | *"...Wouldn't a little mercury be good right about now?"* | `40 Mercury SUCCESS`; the mercury leaves inventory; he stops challenging you and answers *"Leave me alone, runt"*; the pen is enterable |
| TO6 | TO5 with Speech under 50 | The same reply | `40 Mercury FAILURE` -- *"I won't take a drink from the likes of *you*... You'll have more luck with Mathuo"*; the flask is **not** taken and the Mathuo route still works |
| TO7 | Carrying no mercury, talk to Poimaino | - | Neither mercury reply is offered (the old Wine-gated version is gone) |
| TO8 | TO5, then free the prisoners through Thierry (`100 See you in Montaillou`) | - | `Prisoners escape` runs as it does on the Mathuo route; the rescue completes and Thierry can be met in Montaillou |
| TO9 | Toulouse, Iapetus, reach `60 It feeds off titan magic` as any spirit-bearing character | *"I carry a bound spirit of my own..."* | `61 your spirit`: it would take the spirit and leave you standing empty; the three replies out all work. A Pureblood must not see the reply |
| TO10 | Toulouse, Iapetus, `65 Forms`, as a Feralkin or Sylvant | *"A bear leaves a bear's tracks..."* | `66 tracks`: the spoor by the rocks in the southeast cul-de-sac; a human or Demokin never sees the reply |
| TO11 | Toulouse, Iapetus, `75 Mercenary help`, at Barter 40+ | *"Put gold beside the gems..."* | `77 haggle`, then *"Agreed"*; kill the Daeva and return: three Expensive Gems **and** 2,000 gold. Below Barter 40 the reply is absent, and without the bargain the payout is gems only |
| TO12 | Toulouse, Rhea, walk the History branch to `30 History 3`, as an Ancestral / Beastial / Demonic spirit-bearer | The matching reply | Exactly one of the three is offered, matching your spirit, each with its own answer, then back to `30 Utnapishtim`. **This is the first `CHasSpirit` in a dialogue requirement in the game: check it fires at all, and that it fires for the right spirit** |
| TO13 | TO12 as a Demokin with a Demonic spirit | *"The thing bound to me is neither an ancestor nor a beast."* | `30 spirit demonic`. `Spirits/Demonic` is extrapolated from the model name -- if this reply never appears while TO12's other two do, that value is wrong |
| TO14 | Toulouse, Rhea, `30 Utnapishtim`, as a sworn Inquisitor | *"Utnapishtim was the first Inquisitor, then."* | `31 the first inquisitor`; absent to everyone else |
| TO15 | Toulouse, Rhea, Memory branch to `53 Sacrifice`, carrying the Necromancer title | *"You cut a crystal out of a living elder..."* | `53 necromancer`; she steps back; the three replies out all land; absent without the title |
| TO16 | Toulouse, Mathuo, `10 Shapeshifter`, at PE 7+ | *"Unready. You were deep in the mercury..."* | `11 drunk`; afterwards the flask is in the rocks (the reply fires `mercury relay`), so `25 Mercury` and the pickup both work. Below PE 7 the reply is absent |
| TO17 | Toulouse, Tereo's first challenge, as a sworn Inquisitor | *"I am the Inquisition..."* | `51 the Inquisition`; he grants the offices are alike; the four replies out all land. Absent to anyone not of the Inquisition |
| TO18 | Toulouse, Tereo, reach `24 A titan must earn his name`, carrying the Child Killer title | *"They call me a killer of children."* | `25 the name you have earned`; he steps back and refuses your birth-name |
| TO19 | TO18 carrying Goblin Champion instead | *"The goblins of the Crossroads named me their champion."* | `25 a name that was earned`; he approves. Carrying both titles, both replies show; carrying neither, neither does |
| TO20 | Toulouse, Tereo, `22 Titans aren't named at birth`, as a Feralkin, Sylvant or Demokin | *"My kind was named twice..."* | `23 named twice`; a human never sees the reply |
| TO21 | Toulouse, Tereo, `41 Ogres`, at Outwit 7+ | *"One human, or two?"* | `43 counting`: two, perhaps three, and the ogres are not watched closely. Below Outwit 7 the reply is absent |
| TO22 | Toulouse, Lethos, `101 Lucius must die`, as a tainted or demokin character with Speech under 50 | *"Your tribe decided what he is..."* | `120 Nonviolent help` -- the negotiated ending opens without the Speech check; a human under Speech 50 still cannot get there |
| TO23 | Toulouse, Lethos, `140 Explanation for the very dim`, as a Wielder | *"My order binds spirits into stones..."* | `141 a Wielder reads the mneme`; he denies the comparison; the three replies out land. Absent to non-Wielders |
| MO31 | Montaillou, accept the Inquisitor's witch task, find the weird woman, return to the Bishop | *"I have found the witch you seek..."* | The reply appears, the quest completes and pays XP. **It was gated on an empty canned object belonging to another NPC; if it never appeared before this release, that is the bug this fixed** |
| MO32 | Montaillou, accept the Inquisitor's mayor task, speak to the mayor, return to the Bishop | *"I have spoken to the Mayor - he is a heretic and an adulterer."* | Whether this reply appears answers whether an empty canned requirement fails open or closed -- it is still gated on one, deliberately, as the control case. Report which |
| TD1 | **A save that has never entered the Temple District.** Enter it from the Gate District | - | A named guard stands a few steps inside the gate; talking to him gives *"Greetings stranger. I hope your day in the Temple District is a pleasant one."* Leave the map and come back: *"Hello again citizen."* |
| TD2 | TD1, ask who is allowed inside | *"Who is allowed inside these walls?"* | The restriction speech, then *"What do you mean by tainted citizens?"* gives the pointed-teeth-and-cat-eyes explanation |
| TD3 | TD1 as a Feralkin, Sylvant or Demokin | *"You are looking at a tainted citizen standing on holy ground."* | `30 tainted`: he does not challenge or attack; he asks that an Inquisitor not hear of it. A human never sees the reply |
| TD4 | TD1, then cast a spell or strike a guard in the district | - | Pablo reacts exactly as the other Temple Guards do (spellcast detected, the damaged-guard relay); he must not be the only guard who ignores it |
| TD5 | TD1, walk past him repeatedly and leave the district and return | - | He never blocks passage, never demands a donation, and the outer gate guard's scene is unchanged |
| TO24 | **Fresh Toulouse.** Walk into the prisoner pen past Poimaino without the bluff or the bribe | - | *"Stop, you are entering the human pen. If you insist on proceeding I'll have the pleasure of squashing you."* over Poimaino, and then he and Mathuo turn on you as before. After the bluff or the bribe, crossing the line does neither |
| TO18a | TO18, if the Child Killer reply never appears even after killing a child | - | Then nothing awards that perk and the engine does not either; repoint the reply at `Goblin Slayer` or `Merchant Slayer`. **Vanilla checks Child Killer on five Gate District spawn points, so this also settles whether those eight vanilla checks are live** |
| CP16 | Fresh Calle Perdida, as a player who has defeated Relican | Walk the Cedric-gated content | Ten canned gates in the Calle pointed at a nonexistent expression until this release and were taking the Else; confirm the defeated-Relican branches now open |
| GD1 | Gate District, Farshad, as a Knight of Saladin (male and female) | Talk to him after joining | `3 Return Knight of Saladin Male` / `3 Retun Knight of Saladin Sister` -- the two "Welcome into the Order of Saladin" greetings. **Before this release his check pointed at a can that does not exist, so every player got the stranger's opening** |
| TD6 | Temple District, Lord Javier, before beginning the initiate quest | His initiate replies | The gate that reads "initiate quest NOT begun" now resolves; check the pre-quest and post-quest branches differ |
| TO25 | Toulouse, talk to Ephebos (the young titan beside Rhea) | Each of his four openings in turn | `10 the chain` / `11 no name yet` / `12 Tereo` / `40 the pen` / `41 like me` all land; the mercury reply is absent without the flask, and the *"Rhea caught you"* reply is absent until you have overheard Rhea's lecture |
| TO26 | TO25 carrying Titan Mercury, give it to Ephebos | *"I am carrying a flask of quicksilver..."* | `30 mercury`: he takes it, the flask leaves inventory, and he gives up Baktron and Klao. Mathuo and Poimaino can then **not** be given it |
| TO27 | Toulouse, the prisoner pen: talk to the man, the woman, and the child | Each reply in turn | The man on the bait and on running; the woman on her neighbour's voice at the fence and the deer that did not run; the child's count of when nobody is watching. **The child is a new placement -- check he is in the pen and not standing outside it** |
| TO28 | TO27 as a Feralkin, Sylvant or Demokin | The woman's and the child's extra replies | `64 the face` and `66 the child and the devil`; a human sees neither |
| TO29 | Toulouse, carrying a skin of wine, talk to an ogre | *"I have a skin of wine. What is it worth to you?"* | The wine leaves inventory, `51 wine` -> `52 what the ogre saw` -> `53 where`: the deer that walked on two legs, and the rocks in the southeast. Without wine the reply is absent |
| TO30 | Toulouse, walk into the cul-de-sac in the south-east | - | One balloon about churned ground; at PE 7+ a second line about deer slots with no stride. Fires once only |
| TO31 | Toulouse, Iapetus, `65 Forms` | *"Is there anything that can pin such a thing into one shape?"* | `67 the prophets`: a relic of Zarathustra strips a Daeva's shape. Then fight the Daeva **carrying the Amulet of the Prophet** and confirm its own `31 amulet speech` branch fires |
| TO32 | Toulouse, kill the titans or hand over the mneme, then watch the camp empty | - | Menoetius leaves with the rest. **Before this release his generator named him Rhea, so he stayed behind while one of the two Rheas vanished** |
| TO33 | Toulouse, attack any titan | - | Menoetius turns hostile with the rest of the tribe (the alarm relay could not reach him before) |
| TO34 | Toulouse, walk past Baktron and Klao at the north end until their argument plays, then talk to each | Their new replies | `02 the plot` / `03 patience` from Baktron, `02 patience is not obedience` from Klao. Before overhearing them, neither reply is offered |
| MO33 | **End Toulouse any of the three ways, then return to Montaillou** | Tell the mayor, Maury, and a gate knight | `941 the titans have left`, `270 the road is quiet`, `110 the titans have left`. **Before this release the cross-map flag had no part to land on, so none of the village could be told** |
| MO1 | Fresh Montaillou, walk in from the east | - | A knight stops you: *"You there! What business do you have in Montaillou?"*; once only |
| MO2 | MO1 as an Inquisitor / male Templar / female Templar / Knight of Saladin | The matching claim | *"Forgive me Inquisitor"* / *"Forgive me brother"* / *"Forgive me sister"* / *"A Knight of Saladin? ... then you are an ally of the Templars"*; each claim is offered only to that faction |
| MO3 | MO1 as anyone | *"I'm on an urgent mission to protect the relics of this region."* | The relic answer, no dead link |
| MO4 | MO1 | *"My business is my own."* -> *"Why is this town under investigation?"* | The heresy answer, then the goodbye; the reply never loops back on itself |
| MO5 | After MO1, click either knight | - | *"What can I help you with, stranger?"*, not *"Halt, and state your business"* |
| MO6 | Titan Village, after Rhea, Speech 50+ | Ask if it can end without killing -> *"Hear a proposal before you spend him."* | `120 Nonviolent help`; the press is absent below Speech 50 |
| MO7 | MO6, Outwit 8+ / under 8 | The proposal | `121 Nonviolent success` / `122 Nonviolent failure`; both then let you name your price as the killing route does |
| MO8 | Montaillou, Andre, Lethos quest accepted, Speech 50+ / Outwit 8+ | *"Go back to them and say it to their faces"* / *"Walk in under a truce"* | The success nodes, with no [REMOVED FROM GAME] in the text; below the skill, the written refusals, which still offer the fight |
| MO9 | MO8 success | - | Andre leaves Montaillou; the mneme quest reads *"allow Lucius to live"*; *Kill the Titans of Toulouse* completes; pacifist XP |
| MO10 | MO9, back to Lethos | *"Memnos is coming back to you."* | `502`; the reward paid; the titans pack up and leave Toulouse as they do for the crystal |
| MO11 | Montaillou, Andre, first meeting | *"I want to talk to you."* | `20 Introductory`, with the gatekeeper, the gullible line and his story |
| MO12 | Andre, a return visit, having seen the corpse | *"There is a gruesome corpse..."* | `02 corpse` -- the same answer, but the hearts, the accusations and Michel are still offered |
| MO13 | MO12 having heard both the mayor's story and Esclarmonde's | *"I spoke to a woman from Toulouse... and the mayor..."* | `800 Both lies`: he admits the lie and asks you to keep his secret |
| MO14 | Witch hut, after she restores Beatrice | Talk to her again | *"No chickens this time? Perhaps a weasel or stoat who is really the King of Persia..."*; the not-promised variant if you never promised |
| MO15 | Witch hut as a sworn Inquisitor, having promised | - | *"Greetings your holiness..."* rather than the plain return |
| MO16 | Witch hut, ask about the Cathars | *"And when the Inquisition has finished writing its book...?"* -> *"I must know what sort of *aid* you intend to give."* | Her answer about the allies, then the secret stash offer |
| MO17 | Witch hut after speaking to Nostradamus about her | *"The seer told me what you were, and what you did."* | `300 confront the weird woman 1`; the reply is absent before the seer |
| MO18 | Montaillou church, take the witch task or report the mayor | *"Is there anything else in this district that troubles the Inquisition?"* -> *"What is it, your grace?"* | The offer, then the barred cave with the aura of magic; both replies return to his hub |
| MO19 | Montaillou church as a Sylvant / Feralkin / Demokin, no faction | *"My blood is what it is. Is there nothing a tainted soul can do for the Church?"* | *"Well then tainted one, have you come to cleanse yourself of sin?"* and the offer of service |
| MO20 | Montaillou grove, approach the warden without watching the bear change | - | *"What are you doing here? I do not take kindly to trespassers in my grove."*; after watching the change, the *"What did you see?"* greeting instead |
| MO21 | Maury the shepherd, his questions hub | *"Is there anyone here I should be careful of?"* | The warning about Guillaume Belibaste |
| MO22 | Toulouse, Lethos, before Rhea | *"What is it you want of me, then?"* -> *"I will speak with Rhea."* | `60 Go speak to Rhea`; a second visit then opens *"Hello again"* rather than the first meeting again |
| MO23 | Montaillou square, the Relaxed Thug, as a friend of Juanita's guild / a Master Thief / a Thief | The matching reply | `80 guild`; he stands down, keeps his coins-speech, warns you off his patch; afterwards he greets you as a friend. Only one of the three replies is ever offered |
| MO24 | Arrive at Montaillou as a member of the Goblin Horde | *"I ride with the Horde of the Khan..."* | `100 horde`; the knight does not draw but says you will be watched; the reply is absent to anyone not of the Horde |
| MO25 | Montaillou church as a Necromancer, ask about the heresy | *"You have missed one, your grace..."* | `61 the ninety-ninth`; leaving ends it, *"Find them now, then"* starts the fight; the reply is absent without the title |
| MO26 | The Cathar toughs' challenge, as an Inquisitor / as a Wielder | *"I am the Inquisition, and I am standing in your tavern"* / *"the Church burns my kind first"* | Their own hostile node / their own welcome; neither reply shows to anyone else |
| MO27 | The inn's Inquisition agent, as an Inquisitor | *"Who are you reporting to, brother?"* | `36 brother`: he explains the meat test and tells you to stop drawing eyes |
| MO28 | Fabrisse as a Feralkin, Sylvant or Demokin | *"...a face like mine on your street"* | `25 tainted`; she does not step back; a human never sees the reply |
| MO29 | Aidan at Barter 40+ | *"...you are already charging war prices."* | The peace price, then the shop opens 20% cheaper; below Barter 40 the reply is absent |
| MO30 | Maury at PE 7+, asking about the Inquisition | *"You look at the church door every time you say the Bishop's name."* | `131 careful`, his voice dropped, then back to his questions hub |
| RN1 | Fresh Plains, any spirit-bearing race, walk to the rogue camp from the south-east | - | The spirit manifests ahead of you and says *"Beware, the dark inquisitors wield the power to cancel magic by touch..."* (voiced), fades; once; a Pureblood sees nothing |
| RN2 | Fresh Plains, fight the rogue camp | Kill them | As the last one or two fall: the summoning flare on the pentagram, *"<The men stop. The circle does not...>"*, a Terror rises and attacks; once |
| RN3 | Fresh Plains, kill Diego, tell the rogues | `30 join`, close the store | The flare, *"<The circle flares and holds what it called...>"*, a Terror that stands in the circle and does not attack |
| RN4 | RN3, then attack a rogue | - | The Terror joins the fight; no second rising when the rogues die |
| RN5 | Plains, no loan, trip the goons | *"Who sends you?"*; then Barter 40 / Outwit 7 / guild / Church / ST 10 threat / Speech 30 lie | Shylocke's name; 100 taken; let pass; stand down; stand down; the intimidation menu then *"K-keep your gold"*; *"A pauper"* -- each once, the leader silent after |
| RN6 | Plains, in debt, trip the goons | Barter 40 *"Shylocke's rate is six hundred"* | 600 taken; in Barcelona Shylocke offers no repayment and will lend again |
| RN7 | Plains, in debt, a Templar or Inquisitor | *"You'd put hands on a sworn brother..."* | *"...his ledger doesn't close for a cross"*; they let you pass; Shylocke still expects payment |
| RN8 | Plains, in debt, scare them off (any of the four) | Then Shylocke | No repayment offer; a new loan possible |
| RN9 | Plains, the goons, a character with Salesman / Eloquence / Educated / Thief / Master Thief / Brutish Hulk / Dark Majesty / Blademaster / Summoning | The perk line | The haggle without Barter 40; let pass; the 600; the purse back (Thief +0, Master Thief +50); the four intimidations into the stammer; each once |
| RN10 | Fresh Plains, walk to Mauldo's stall, then to the camp's east stake | - | *"<A stake cut into a rough cross...>"* once at each; at the camp a PE 7+ character reads the re-set ring instead |
| RN11 | Fresh Plains, a Wielder of Cedric's (no Necromancer), walk into the camp | - | *"...You are off the hidden street in Barcelona"*; the warning reply -> `21`; study/fight/leave as before |
| RN12 | Fresh Plains, a Dark Wielder (Necromancer) | *"I know what the circle is for..."* | `22 dark tribute`; accepting arms the Diego quest as before; *"Keep your circle. I have my own."* lets you walk |
| RN13 | Fresh Plains, a non-Wielder, and a Wielder with Diego in tow | - | The vanilla greeting and `50 Player Has Diego` respectively |
| RN14 | Plains, a sworn Inquisitor, talk to Diego | *"I am of the Order myself, Inquisitor."* | `21 brother`; "Tell me." reaches his own quest offer unchanged; a non-Inquisitor never sees the reply |
| RN15 | RN14, kill the rogues, return to Torquemada | *"There was a cult on the northern plains wearing our habit"* | `413`; 800 XP and 250 gold; the reply gone afterwards; never offered to a non-Inquisitor or before the quest completes |
| RN16 | Plains, after either rising, talk to Mauldo again | - | *"Something answered on the north road..."*; before the rising, the plain return greeting; the low-karma greeting and his shop unchanged |
| RN17 | Fresh ogre maps, kill Aka Manah | Walk back out through the Cave, the Sprawl and the Pass | Every ogre stands down, once, with *"<The ogre stops mid-swing...>"*; rock titans and wolves still attack; ogres spawning near you afterwards are passive |
| RN18 | RN17 by the Speech route instead (`160 tricked aka manah`) | - | The same stand-down; the XP and Alamut hook as before |
| RN19 | Fresh Pass, walk the road south to north | - | The dead ground, the titans' quarry and the cairn, once each; after the charm breaks the cairn reads its quiet version |
| RN20 | Fresh Abandoned Cave, walk west to the camp | Talk to Bernat | *"Hold -- hold! Guilhem, down."*; who/news/shop all answer; Guilhem and Peire have their own barks; no wolves spawn on top of the camp; a second visit opens `3 return dialogue` |
| RN21 | RN20 carrying a healing potion | *"Your man by the fire is hurt..."* | The potion is taken, Peire's bark changes to *"The arm holds. My thanks."*, XP once; the reply gone afterwards |
| RN22 | RN20 before beating Aka Manah | - | The "road south is open" reply is absent |
| RN23 | RN20 after the charm breaks | *"The road south is open."* | 400 gold, the Tome of Geomancy, 600 XP; Bernat, Guilhem and Peire and the camp props are gone; the cold-camp hover plays where they were |
| RN24 | Fresh Abandoned Cave, the camp | Walk to the bodies north-west of the fire; ask Bernat *"There are bodies in here."* | The hover once; his answer on every greeting; the fire is lit and his opening line matches it |
| RN25 | Ogre Conjurer Cave, fresh | *"What do you want with me?"* -> *"So, I have you to thank for all the Ogres in this cave?"* | `30` then `50 Ogre Spells`; *"Who is your master?"* reaches `170 Master`, not the Nueva Barcelona node |
| RN26 | As a tainted character | *"You have felt what I carry..."* -> *"Then let me walk out..."* | `80`, then `70`; he does not attack, you can leave the cave; a second visit opens `130`; the ogres are still hostile and Bernat is still stuck |
| RN27 | Speech 40+ | *"Your master has made terms with the Titans of Toulouse."* | `90`; *"Fair enough, and farewell"* makes him leave as the Speech route does -- XP, and the ogres stand down |
| RN28 | Speech under 40 | The same reply | `120`, and he attacks |
| RN29 | Flee the fight and come back without either outcome | - | The first greeting again, not *"Was my warning not sufficient?"* |

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
| 0.4.0 | PASS (automated) | - | - | - | - | - | **published as full, entirely unplayed** |
| 0.4.1 | PASS (automated) | - | partial | - | - | - | **published as repair** |
| 0.5.0 | PASS (automated) | - | - | - | - | - | **superseded, crashes on entering the vault** |
| 0.5.1 | PASS (automated) | - | - | - | - | - | **published as repair, unplayed** |
| 0.6.0 | PASS (automated) | PASS | partial | - | - | - | **published; played only as far as the Juan rescue** |
| 0.7.0 | PASS (automated) | - | - | - | - | - | **published, entirely unplayed** |
| 0.8.0 | PASS (automated) | - | - | - | - | - | **published, entirely unplayed** |
| 0.8.1 | PASS (automated) | - | - | - | - | - | **published as repair; fixes three played defects, itself unplayed** |
| 0.8.2 | PASS (automated) | - | - | - | - | - | **published as repair; five played Quinn defects, itself unplayed** |
| 0.8.3 | PASS (automated) | - | - | - | - | - | **published as repair; Amir's fix played on the reporting save** |
| 0.8.4 | PASS (automated) | - | - | - | - | - | **published as repair; the fifteenth sale itself not yet played** |
| 0.9.0 | PASS (automated) | PASS | partial | - | - | - | **published; Na Roqua chain and Machiavelli's refused branch played and passing, the rest unplayed** |
| 0.9.1 | PASS (automated) | - | - | - | - | - | **published, entirely unplayed** |
| 0.9.2 | PASS (automated) | PASS | PASS | - | - | - | **published as repair; every piece played on a fresh Port District** |
| 0.9.3 | PASS (automated) | PASS | PASS | - | - | - | **published as repair; the perk proven from the combat log, the goblin's answers played** |
| 0.9.4 | PASS (automated) | PASS | PASS | - | - | - | **published as hotfix; the crash reproduced from the screenshot, every repair played** |
| 0.10.0 | PASS (automated) | PASS | partial | - | - | - | **published; Grove, wounded assassin, Sahar's approach and the journal played on one run, the rest unplayed** |
| 0.10.1 | PASS (automated) | - | - | - | - | - | **published; the stash barks built and unplayed (MS27-MS29)** |
| 0.10.2 | PASS (automated) | - | - | - | - | - | **published; the jailor's lesson and the sprung bark built and unplayed (MS30-MS32)** |
| 0.10.3 | PASS (automated) | - | - | - | - | - | **published; Esteban's line, the two returns-after-attack and the extra guard built and unplayed (MS33-MS35)** |
| 0.11.0 | PASS (automated) | PASS | partial | - | - | - | **published; the gate, the undercroft's five exits, the escort, the hall's stand-down and the Wasp Queen played (PM1-PM14, PM24); Sahar's prisoner talk, the ring and the rout unplayed (PM15-PM23)** |
| 0.12.0 | PASS (automated) | PASS | - | - | - | - | **published, entirely unplayed (CP1-CP15); repairs go to 0.12.1** |
| 0.13.0 | PASS (automated) | PASS | - | - | - | - | **published, entirely unplayed (RN1-RN29); repairs go to 0.13.1** |
| 0.14.0 | PASS (automated) | PASS | - | - | - | - | **published, entirely unplayed (MO1-MO30); repairs go to 0.14.1** |
| 0.15.0 | PASS (automated) | PASS | - | - | - | - | **published, entirely unplayed (TO1-TO34, TD1-TD6, MO31-MO33, CP16, GD1); repairs go to 0.15.1** |
| 0.16.0 | PASS (automated) | PASS | - | - | - | - | **published, entirely unplayed (CR1-CR58); carries 0.15.1's Saladin Favored fix; repairs go to 0.16.1** |

0.2.0 was published as a full release on the maintainer's call, not because the gates were
green. Of its five items only the Goblin Girl's follow has been played; the Khan's
campaign, the report-back, the jailor's rank route and the Grumdjum fix are verified in the
built archive and unplayed. Gate 0 catches a broken reference, never a gate that resolves
wrongly, which is the failure mode this release carries most of.

Character B has never walked any release. That is the outstanding hole in the whole
project, not a 0.2.0 problem.

**Four consecutive releases are now unplayed, and the debt compounds.** 0.6.0 stops at the Juan
rescue; 0.7.0, 0.8.0 and 0.9.0 have never been launched. 0.7.0 changed a late-game promotion for
every faction combination and 0.9.0 edits two maps in Act 3, so the untested surface is no longer
confined to the features each release names. Gate 0 has caught real defects throughout -- a brace
on the wrong line, a missing structural blank line, two map parts that lost their indentation --
but it has never once caught a check that resolves *wrongly*, which is the failure mode all four
of these releases carry.

**0.6.0, 0.7.0 and 0.8.0 have no Gate 2 cases in this document.** That is a gap, not a claim that
they need none: their features are described in `docs/releases.md` and were never translated into
cases here. 0.9.0 is the first release since 0.5 to get a section.
