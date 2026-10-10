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

A0.1-A0.12, A0.14 and A0.15 are scripted in [`tools/validate.py`](../tools/validate.py); A0.13 is
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
| A0.14 | No can-level quest-item drop is overridden by the generator that spawns it | zero overridden drops. `CSetDestroyedScriptActionAction` in a generator's `After Action` **replaces** the can's `Destroyed Script Action`, so a drop written only on the can is dead code -- this is how the Lava Troll Hide was unobtainable from 0.10.0 |
| A0.15 | Every `=CSomething` names a class the engine registers | zero unknown classes. Checked against the C-prefixed strings in `Lionheart.exe` plus every class vanilla's data uses. An invented class is a hard CTD -- *"Invalid class type"* -- and `CIsQuestStatusCompletedAction` in the Grand Inquisitor's tree shipped in **0.13.0 and survived 27 tagged releases** before a player walked into it |

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
| NO26 | **A save that has never entered act 5.** Stand near the English ogres on the Heart Entrance for a minute | - | They bark every five seconds or so, eight lines shuffled: *"Engage the savages!"*, *"Press on for England, men!"*, *"For the Queen!"* and so on. **None of these has ever played -- their speaker did not exist and the relay was fired by nothing** |
| NO27 | Watch where the English barks appear | - | Over one particular ogre (`English loser`, from the `Big Fight` at 2096,1418), not over the player and not over a Hujark |
| NO28 | Side with Huko (NO5), then fight through to `05 Nostrodomus Demesne` | - | After the arrival cutscene the assassin attacks **alone**. The Hujark Shaman says *"The Seer has been expecting you. You may enter now."*, the guard follows with *"Thank you! Now quickly come with me."* |
| NO29 | NO28, then stand around for twelve seconds without entering | - | The shaman adds *"Do not keep the Seer waiting."* |
| NO30 | Reach the Demesne having sided with the **English** (NO6/NO8) | - | Vanilla behaviour exactly: assassin, then the shaman 1.5s later, then the guard, all hostile |
| NO31 | Reach the Demesne having **never met Huko** | - | Same as NO30. The checker is off unless the Hujark flag fired |
| NO32 | NO28, then check the journal | - | Only *Protect Nostradamus from the invading English forces* should be active -- confirm siding with the Hujark has not also activated the English quest |
| NO33 | **A save that has never entered act 5.** Refuse Huko or kill him, then cross the whole act | - | **Vanilla, exactly**: Hujark everywhere, no English soldiers anywhere. This is the row that proves the swap is opt-in |
| NO34 | Side with Huko (NO5), then fight through `01`, `02`, `03`, `04` and the caves | - | **English soldiers and bowmen** (`Nos Soldier1/2/3`, `Nos Soldier2 Bow`) instead of Hujark swordsmen. 99 generator parts across nine maps; `02` has the most (34) |
| NO35 | NO34: watch what the Hujark do when you walk past them | - | They ignore you and fight the English. Their targets are set to `Scripted Custom 2` at spawn when the flag is set. **A Hujark still swinging at an allied player is the bug to report** |
| NO36 | NO34: count enemies against NO33 on the same map | - | Roughly the same. If the Hujark path feels heavier, the pacify branch is not firing; if much lighter, the English parts are not activating |
| NO37 | NO34 on `06 Cave 1` | - | Unchanged -- that map fields no Hujark, only the apprentice set-piece and fauna |
| NO38 | NO34 anywhere: wound an English soldier past half health | - | **No snake.** Tier 2's trigger is stripped from every English twin |
| NO39 | NO34: check the cave fauna | - | Snakebreed, spirits and vodyanoi attack you on both paths. They were deliberately left alone |
| NO40 | NO34 then reload a save from before the choice and side with the English instead | - | The English parts stay off. The checker is per-map and set only by the Hujark relay |
| NO41 | **A save that has never entered act 5.** Reach Nostradamus and hit him once | - | He opens `30 Combat` -- *"Fool, you cannot fight your fate"* -- then taunts with `1001 Goto combat`, and four seconds later starts casting lightning at you from across the room. **In the shipped game he stood there and took it** |
| NO42 | NO41, then hit him again several times | - | No repeat of the opening conversation. The `the seer has laughed once` checker holds it |
| NO43 | NO41, then kill him | - | *"I have already transcended this mortal coil... Your failure has been foreseen."* and then the portal opens as it always did |
| NO44 | Talk to him without ever attacking | - | No combat, no taunt. The whole thread hangs off the first blow |
| NO45 | Ask him **"The Hujark call you their Prophet. What are you to them?"** | - | `10 Nostradamus`: *"To the Hujark, I am a prophet... But I was not always like this."* Offered from both `5 questions` and `3 Return Dialog`, and **never reachable before** |
| NO46 | Ask *"What are you?"* as well | - | Still `35 Prophet` -> `35 prophet 2` -> `45 element of prophecy`, unchanged |
| NO47 | From `70 dangers`, take *"Tell me about the Betrayer."* and *"Tell me about the serpent."* | - | `70 Betrayer` and `100 Dragon Prophecy`. These were spelled in lowercase in vanilla; if they worked before they still work, and if they did not they do now |
| NO48 | NO41 while **sided with the Hujark** (NO28) | - | The shaman and guard stood aside at the door, and the seer still defends himself. Confirm attacking him does not un-pacify the Hujark |
| NO49 | **A save that has never entered act 5**, with a **low** Find Traps / Lockpick skill. Cross any map | - | Traps fire: a fire circle, an electrical burst or an ice ring, then damage scaled by Mojo. **Act 5 has never had a trap of any kind** |
| NO50 | The same ground with **Lockpick Disarm Traps at 50 or better** | - | The trap is spotted before it fires, and can be disarmed for 250 XP. Below 50 on the disarm attempt: *"The mechanism is beyond you"* |
| NO51 | Walk back over a trap that has already fired | - | Nothing. `Trigger Only Once=1` |
| NO52 | Count traps per map against the table in the notes | - | 43 across ten maps, heaviest on `02` (6). If a trap seems to be inside rock or unreachable, report the map and rough position -- they are placed on monster spawn points, which should all be walkable |
| NO53 | Compare trap damage against a Mojo-30 and a Mojo-15 character | - | 30-45 versus 15-25. The first cut of this tier shipped the Crypt's weaker numbers by mistake; these should be the higher ones |
| NO54 | Enter `07 Cave 2` from either direction | - | *"The passage narrows and keeps narrowing..."* -- **once**, then never again on that save |
| NO55 | Reach the far end of `07 Cave 2` where the loot is | - | *"The crack ends. Whatever the Hujark wanted out of this cave they stopped wanting some time ago..."* |
| NO56 | Enter `09 Cave 4`, then find the `Hidden Treasure` | - | *"A store cave, or it was..."* on arrival, and at the cache *"Somebody hid this and did not come back for it."* |
| NO57 | Re-enter either cave a second time | - | No repeat of the arrival line |
| NO58 | Reach `45 element of prophecy` with each of the three spirits | - | Ancestral -> `46 the crowded joining`; Beastial -> `47 the unspeaking joining`; Demonic -> `48 the burning joining`. **Exactly one of the three should ever be offered**, and act 5 has never had a spirit check |
| NO59 | NO58, then take each route out | - | `60 visions`, `5 questions`, and goodbye. No dead ends |
| NO60 | Ask Huko *"Who are the Hujark?"* as a **Feralkin**, **Sylvant** or **Demokin** | - | `41 driven out as we were` -- he looks at you properly for the first time |
| NO61 | The same as a **Human** | - | `42 you wear a face they accept`. Never both, and never neither |
| NO62 | Reach `10 explanation` with karma **1300+** | *"Then let me say where I stand, and judge it as you like."* | `43 you ask to be believed`. At **700 or below**, `44 you ask to be believed anyway`. Between them, neither reply is offered and the node is exactly as vanilla left it |
| NO63 | From each of Huko's four new nodes, take *"I have come to help the Prophet."* | - | `50 help prophet`, and the Hujark quest activates as in NO5 |
| NO64 | From each of them, take the fight reply | - | The English quest activates and the fight starts, as in NO6. As an **Inquisitor** the reply is the Inquisition's version instead -- never both |
| NO65 | **A save that has never entered act 5.** On `06 Cave 1`, let the Frightened Apprentice flee, then go to `02 Clan of the Hand A` | - | He is there, as he always was. That path is unchanged |
| NO66 | NO65 but **kill him on Cave 1**, then go to `02 Clan of the Hand A` | - | He is **not** there. In the shipped game he was waiting on the next map having just died in front of you |
| NO67 | Wound a **shaman** past half health on `08 Cave 3`, `09 Cave 4` or `10 Cave 5` | - | A snake erupts beside it. Those three maps carried the checker and the clone source and had nothing to trigger them |
| NO68 | NO67 while carrying **Sahar's ring** | - | No snake, and the *"nothing comes up out of it"* line once per map. Shamans are gated exactly as the swordsmen are |
| NO69 | Wound a **Snakebreed Summoner** to a quarter health on `02 Clan of the Hand A` or `04 Clan of the Skull B` | - | It calls in something much worse than a snake -- a Mongol archer or an ogre for a weak party, up to a **Rock Titan** for a strong one |
| NO70 | NO69 while carrying **Sahar's ring** | - | It still summons. The ring stops serpents, not rock titans. **If the ring silences the summoners too, the gate has been put in the wrong place** |
| NO71 | Kill a summoner outright from above a quarter health | - | Nothing. The trigger is a crossing below 25% |
| NO72 | **A save that has never entered act 5.** Side with Huko, then enter `02`, `03`, `04`, `08`, `09` and `10` in turn | - | A Hujark soldier is standing with you on each, and about a second and a half after you land he calls the stage of the advance -- *"Thank you for your help!"*, then *"You must get to the Seer before the Druids do!"*, and so on to *"Protect the Seer!"*. **Twelve of these lines have never played** |
| NO73 | NO72: watch what the escort does | - | He fights the English and **never the player**. An escort swinging at you is the bug to report |
| NO74 | Side with the English instead, then cross the same six maps | - | An English soldier escorts you and calls the English series -- *"We must bring the savages to their knees!"* through *"Hurry! We have almost broken through."* |
| NO75 | Never commit to either side, then cross those maps | - | Neither escort appears and no line plays. Both ship inactive |
| NO76 | Re-enter any of the six maps after hearing its line | - | No repeat. `the advance has been called` holds it per map |
| NO77 | NO72 and NO74: confirm you only ever hear one side's line on a map | - | The Hujark line if you sided with Huko, the English line if you sided against him, never both |
| NO78 | **A save that has never entered act 5**, with Speech **below 75**. Talk to Huko | - | Only the two vanilla doors. The third reply must not be offered |
| NO79 | The same with Speech **75 or better** | *"I am not here for your Prophet and not here for the Druids."* | `46 safe conduct`. Offered from `1 Conversation Start`, `3 Return Dialogue` and `10 explanation` |
| NO80 | Take it, then cross `01`, `02`, `03`, `04` and the caves | - | **The Hujark ignore you and the English hunt you.** No escort, no commentary line, and **nothing in the journal** -- neither quest activates |
| NO81 | NO80 on `03 Tourniquet of Pain` specifically | - | The map is **full of English**. It has no cave fauna at all, so if the English are not coming on, this is the map that will be empty and the whole design has failed |
| NO82 | NO80, then reach the Demesne | - | The shaman stands aside and says the Seer has been expecting you, exactly as for an ally. Huko's word covers his own men all the way to the door |
| NO83 | NO80, then ask Nostradamus *"I took no side to get in here. Does that show, in your visions?"* | - | `49 the one who owed nobody`. Offered only while the safe conduct holds |
| NO84 | NO80, then **strike any Hujark** | - | He fights back, and from then on every Hujark that spawns is hostile again -- on this map **and the next one**. The reply NO83 unlocks should also stop being offered |
| NO85 | Side with Huko normally (NO5), then strike one of his men | - | The same revocation. Siding with him and then cutting his men down has to cost the alliance |
| NO86 | Side with the English (NO6), then cross the act | - | Unchanged from tier 3b: Hujark hostile, no English, an English escort, the capture quest |
| NO87 | **A save that has never entered act 5**, carrying the **Child Killer** title. Let Huko approach, or click him | - | `47 not from you` -- he has the sword up before a word is said. He must **never** open `1 Conversation Start` for this character, from either hook |
| NO88 | NO87: look for any way to offer him help, from every node you can reach including `30 Prophet` | - | There is none. All fifteen replies that reach `50 help prophet` are closed to the title. **The first cut of this tier leaked through `30 Prophet`** |
| NO89 | NO87 with Speech 75+ | - | The safe conduct is still offered and still works -- he wants you gone, and that is a deal he will take |
| NO90 | NO87 without Speech | - | Ask about the Prophet, or fight. Those are the only doors left |
| NO91 | Without the title, talk to Huko | - | `1 Conversation Start`, exactly as before. Nothing about the ordinary path changes |
| NO92 | Ask Huko *"Who are the Hujark?"* with **Tribal magic at 80+** | - | `48 your magic is ours` -- he looks at your hands rather than your face |
| NO93 | Ask the seer his questions with **Divine 80+**, then **Thought 80+** | - | `51 the church would burn you` and `52 what you are becoming`. Each offered only to its own specialist |
| NO94 | The same carrying the **Necromancer** title | - | `53 the same trade`: *"The difference is not skill and it is certainly not mercy. It is that I asked."* |
| NO95 | Ask him about his visions carrying **Stargazer** | - | `54 the stars you read`. This perk is read in exactly one other place in the game |
| NO96 | Reach the seer with none of those four | - | None of the four replies is offered and his conversation is exactly as vanilla left it |
## The five titles nothing awarded

Five finished title perks that the shipped game grants to nobody, now granted -- and answered. The
grants are idempotent, so re-killing cannot double-award.

**`PK13` is the regression that matters most in this release.** Several member cans are spawned by
generators that set their own destroyed script, which **replaces** the can's death slot rather than
adding to it -- the bug that left the Lava Troll Hide dead from 0.10.0 to 0.30.1. Those actions were
**wrapped**, not overwritten. If a wrap went wrong, the symptom is not a missing perk: it is a
**quest that silently stops failing** when it should. `PK13` is the cheapest way to see that.

**`PK1` and `PK5` prove the two halves** -- the counter-driven title and the death-hook titles.

**`PK16` is a judgement row.** The rogue inquisitors were deliberately excluded, on the grounds that
a rogue has left the order and the Grand Inquisitor's own tree has a `413 rogue inquisitors` node
about hunting them. If that reads wrong in play, it is a one-line change.

| # | Where | Steps | Pass |
|---|---|---|---|
| PK1 | **Proves half one.** Kill goblins in the Goblin Warrens or the Mongol Camp until the Raylark bounty or the Savage Heart quest ticks over (twelve) | Check the character sheet | The title **Goblin Slayer** is now listed. It should arrive at the same moment the bounty or quest advances, because it hangs off that same branch |
| PK2 | After `PK1`, talk to any goblin villager | - | A new reply is offered: *"You know what I am. Say it."* Taking it gets the *"you are weather"* speech, and notably **the villager does not offer to eat you**, which every one of its other 17 greetings does |
| PK3 | After `PK1`, return to **Raylark** | - | A new reply about the vale being quieter. He approves, and complains that every goblin you take is a bounty he never collects |
| PK4 | **The contradiction.** Hold `Goblin Slayer` **and** goblin rank (be in the horde), then speak to the **Goblin Khan** | - | A reply appears admitting you wear his mark and have killed his people. His answer should be approval, not condemnation. **With no goblin rank this reply must not appear at all** |
| PK5 | **Proves half two.** Kill any ordinary Inquisition member -- a generic inquisitor in the Temple District will do | Check the sheet | **Enemy of the Inquisition** is listed |
| PK6 | After `PK5`, talk to any other inquisitor | - | From *"Greetings, child"*, a new reply leads to the ledger-and-arithmetic line |
| PK7 | Kill a Knight Templar (the Port District has them) | Check the sheet | **Enemy of the Knights Templar** is listed |
| PK8 | After `PK7`, talk to a Templar -- **and if you are a Templar yourself, use that path** | - | The reaction is reachable from the ordinary greeting *and* from *"Well met, brother"* / *"Well met, sister"*. The *"I will not call you brother again"* line should land hardest there |
| PK9 | Kill a Wielder in La Calle Perdida | Check the sheet | **Enemy of the Wielders** is listed |
| PK10 | After `PK9`, talk to a Wielder wizard there -- **especially if you are a Wielder**, so you get *"Welcome, fellow Wielder"* | - | The candles-down-a-long-hall reply is offered, and the room turning cold is in the line |
| PK11 | Kill a Knight of Saladin, or **Jafar** | Check the sheet | The Saladin title is listed. **This one was dead in vanilla too** -- its shipped grant sits on an inactive part that nothing activates |
| PK12 | After `PK11`, talk to a Knight of Saladin, ideally one who greets you with *"Word of your deeds have come before you, brother"* | - | The *"do not call me brother where the others can hear you"* reply is offered |
| PK13 | **The regression. Do this one first if you only do one.** Kill **Inquisitor Fournier** in Montaillou's church while at least one of his three quests is active | Check the quest log | **All three quests still fail** -- `Find the Witch for the Inquisitor`, `Talk with The Mayor for the Inquisitor`, `Purify the Shadow Dryad` -- **and** you gain Enemy of the Inquisition. If the quests no longer fail, a wrap replaced an action instead of adding to it |
| PK14 | Kill a **second** member of a faction you have already angered | - | Nothing happens twice: no duplicate title, no error, no message. The grant checks for the perk before giving it |
| PK15 | **The control.** Play Barcelona normally, killing none of these factions | - | No faction title appears, none of the new replies is offered, and every one of these NPCs behaves exactly as before |
| PK16 | **The judgement row.** Kill a **rogue** inquisitor (the Inquisition Chambers and Plains have them) | Check the sheet | Enemy of the Inquisition should **not** be granted. A rogue has left the order. Decide whether that reads correctly -- the Grand Inquisitor hunts them himself |

## The creatures sent after Machiavelli, and the level gate

An act-1 escort quest that works end to end, whose four attackers spawned from a can pointing at a
**player** race -- no armour class, no hit points, no weapon skill, and labelled *"Demokin"* on
screen. They are now a tiered Snakebreed group, and the quest is gated at **character level 5**
because the man you protect is **AC 40 / HP 35** and the fight was available immediately.

**`MA2` and `MA3` prove the release together.** They are the two halves of the gate, and the gate
uses `CVariableCharacterLevel`, which has **60 shipped uses in perk requirements and zero in a
dialogue requirement can**. If it fails to resolve, the symptom is `MA2` passing for the wrong
reason -- the offer absent at *every* level -- so `MA3` is what distinguishes a working gate from a
broken one. Do not report `MA2` without `MA3`.

**`MA9` is the judgement row.** Level 5 was chosen against act-1's enemy band, not measured in play.
If Machiavelli still dies at level 5 with a competent player, the threshold is wrong and should go
up; if he never comes close, it can come down.

| # | Where | Steps | Pass |
|---|---|---|---|
| MA1 | Temple District, Machiavelli's door. Talk to him on a **new game**, below level 5 | Pick any of mercenary / soldier / general, reach his task offer | He describes his dangerous opponents as shipped. The conversation works exactly as before |
| MA2 | **Half one of the gate.** Same conversation, still **under level 5** | Read every reply on the task offer | *"I'm interested. You can count on me for support."* is **absent**, and a new reply *"I could not protect you as I am. Not yet."* is present. Choosing it gives his refusal line about buying company in the grave. **Not a pass on its own -- see MA3** |
| MA3 | **Half two, and the one that matters.** Reach **level 5**, return and talk to him again | Use his return greeting, then ask about work | *"I'm interested..."* is now **present** with its quest icon, and the *"I could not protect you"* reply is **gone**. If the offer is still missing at level 5, the level check is not resolving and the release must be pulled |
| MA4 | After `MA3`, accept the task | - | The quest `Task for Machiavelli` activates in your log exactly as it always did |
| MA5 | **The lockout check.** Before reaching 5, exhaust his conversation -- refuse, leave, come back, refuse again | - | He never runs out of replies, the goodbye option is always there, and returning later still leads back to the offer. The quest must never become permanently unavailable |
| MA6 | **The composition.** Accept at level 5+, then leave the house to trigger the ambush | Look at the four attackers | Four snake-women, not four identical ones: **one visibly larger** leader near the door, two of the same smaller build, and one that **attacks from range** rather than closing |
| MA7 | During the ambush, read the name under any attacker | - | It is **no longer "Demokin"**. That label was the player race leaking through |
| MA8 | Fight them | - | They take a real number of hits rather than dropping instantly, and they land real blows. Before this release they had no armour class or hit points at all |
| MA9 | **The judgement row.** Play the ambush properly at level 5 and try to keep Machiavelli alive | - | He survives if you play well. He has **AC 40 / HP 35**, so he is meant to be genuinely at risk -- but if he dies even when you fight well, level 5 is too low and the gate needs raising |
| MA10 | Watch the ranged one specifically | - | It spits at range for piercing and poison damage. Judge whether it can reach Machiavelli past you from the far corner -- that is the one new threat vector this release adds |
| MA11 | Listen during the fight | - | All four speak, the leader included -- hissing barks over their heads. Before this release the leader was the only mute one |
| MA12 | Save Machiavelli, then talk to him | - | His thank-you plays, he asks you to let him go, and the Barcelona reward is paid as shipped |
| MA13 | **The Montaillou payoff.** Much later, meet him again in Montaillou | - | `300 machiavelli helps you in montaillou` still fires. Nothing in this release touches that chain, and it must not have broken |
| MA14 | **The control.** Deliberately let him die, or refuse the task entirely and continue the game | - | The failure and refusal paths behave exactly as they always have. Only the enemies and the gate changed |

## Alvaro's horse at the Crossroads

The game shipped a complete horse -- 54 KB can, 36 KB model, cached render, its own death sound --
with an animation set of **Idle, Walk, Death and nothing else**, and placed it in **zero** maps. It
is now the Crossroads merchant's cart horse.

**`HR1` is the row that matters.** Everything else is consequence; first the horse has to actually
be standing there, on the ground, rendered. It is placed at 1356,1848 inside a quad bounded by two
working spawn points in the same map, but a position being proven for one entity is not proof for
another -- this project has made that mistake before.

**`HR9` is the honest one:** the horse has no attack or get-hit animation, because it was never
built to fight. Its can's AI was left intact rather than stripped (zero vanilla precedent for
that), so it may try to retaliate and look stiff doing it. That is a known cost, not a bug to
report -- unless it looks bad enough to be worth stripping after all.

| # | Where | Steps | Pass |
|---|---|---|---|
| HR1 | **The row that matters.** Travel to the Crossroads in the Wilderness and look near Alvaro the merchant | - | A **horse** is standing there, rendered, on the ground, close to him. If it is absent, floating, or sunk into the terrain, the placement is wrong and nothing else in this section can be tested |
| HR2 | Walk around it | - | It is solid and does not drift. Its can is `Stationary=1`, so it should hold its spot rather than wander |
| HR3 | Watch it for a while | - | It idles. It has an Idle and a Walk animation and nothing else, so expect stillness, not grazing or tail-flicking -- there is no Fidget |
| HR4 | **The consequence.** Attack the horse once | - | Alvaro shouts *"Away from her! She has pulled my cart these nine years and you raise a hand to her?"* in a balloon over his head, **and then turns hostile and attacks you** |
| HR5 | After HR4, try to trade with him | - | You cannot. He is hostile. This is a real cost for a petty act, which is the point |
| HR6 | Reload and instead **rob** Alvaro (pickpocket/steal), without touching the horse | - | The **shipped** reaction still happens: he cries *"Thief! THIEF!"*, walks to the guard captain, and goes hostile. The new relay must not have replaced or broken that one |
| HR7 | Reload and attack **Alvaro** directly, leaving the horse alone | - | His own vanilla damaged script still fires `Merchant1 requests help`. Unchanged |
| HR8 | Reload and kill the horse outright | - | It dies, plays its death animation, and you should **hear the horse death sound** -- a 27 KB recording that has never played in this game |
| HR9 | **The honest look.** During HR4, watch the horse itself rather than Alvaro | - | It has no attack and no get-hit animation. If it tries to fight back it will look stiff or freeze mid-pose. Judge whether that is acceptable or whether its AI should be stripped in a follow-up |
| HR10 | Leave the Crossroads and return | - | The horse is still there, and if you had already angered Alvaro he is still hostile. The relay is `Trigger Only Once=1`, so the shout must not repeat endlessly |
| HR11 | **The ignore case.** Play the Crossroads normally without touching the horse at all | - | Everything is exactly as it was before this release. Alvaro trades, the bandits behave, nothing else changed |
| HR12 | Judge the **fiction**, which no check can settle | - | Does a cart horse with no cart read as odd? No map in the game places a cart model, so the cart exists only in his line. If the absence is glaring, that is worth knowing -- the alternative is placing an unverified model |

## The hangover cure, across two acts and three people

The drunkard who teaches **Drunken Boxing** had a live, map-opened return node with **no replies on
it at all**. Quinn's `30 Special Order` has always offered to brew for "any affliction of the mind
and body" with nothing in the game able to bring him one. `Gather Nightshade Root for Quinn` was a
**0-state stub**. This chain joins them.

**`NR3` is the row that proves the gate fix.** The gates began in Barcelona's Gate District folder
and the witch is in **act 3** -- and cross-level requirement resolution **never happens in vanilla**
(0 cases against 335 global and 26 cross-district). A Barcelona can read from Montaillou would
evaluate as nothing and silently hide the reply, with no error from any gate. All five moved to the
global root. If NR3 fails, that fix did not take.

**`NR12` is the timing gate** -- he must not ask before Montserrat.

| # | Where | Steps | Pass |
|---|---|---|---|
| NR1 | **Baseline.** In the Port District tavern before Montserrat, spare the drunkard a gold and learn Drunken Boxing | - | Unchanged vanilla. He teaches the style; your Unarmed goes up 3 |
| NR2 | Speak to him again, still before Montserrat | - | *"Good to see you again, friend. Grab an ale and enjoy yourself"* and **nothing else**. In vanilla this node had no replies at all and before Montserrat it still must not |
| NR3 | **The row that proves the gate fix.** Get the quest to the nightshade step, travel to **Montaillou**, and talk to the weird woman | - | A `Quest Icon` reply about nightshade root appears. **This is a gate file living in Barcelona's global requirements folder being read by an act-3 dialogue tree** -- if the reply is missing, the gate is resolving as nothing |
| NR4 | **The ask.** After Montserrat, return to the drunkard | - | He admits he has been drinking since the news from the abbey and asks you to see Quinn. The journal gains `Gather Nightshade Root for Quinn`, which in vanilla had no states and could never appear |
| NR5 | Decline him (*"Drink less."*) | - | Conversation ends, no quest, and the ask is still offered next time |
| NR6 | **Quinn.** Take the ask to Quinn in the Gate District | - | He knows the affliction, explains nightshade does not grow south of the mountains, and points you at a woman in Montaillou -- asking you not to say he sent you. Try this from several of his greetings; the reply is on **7** of his hubs |
| NR7 | Check the journal after NR6 | - | It names Montaillou and the unlicensed woman, not a vague "find an ingredient" |
| NR8 | **The root.** Take the witch's reply | - | She gives it **free** -- *"a thing like this is given or it is nothing"* -- with the warning that a thimble quiets a man and a spoon quiets him permanently. You receive **Nightshade Root** |
| NR9 | Check the root in your inventory | - | It has proper art and a real description. It reuses the rare-herb model `Darkwood` uses, so it must not appear as a missing-art placeholder |
| NR10 | **The brew.** Carry the root back to Quinn | - | He takes it without asking where it came from, grinds it, and gives you the **Hangover Cure Potion** -- an item referenced by nothing in the shipped game. The root is **consumed** |
| NR11 | **The delivery.** Take the potion to the drunkard | - | He drinks it in one go, goes quiet, and teaches **Clear Head**: +3 Find Traps and Secret Doors. The potion is consumed and the quest completes |
| NR12 | **The timing gate.** On a fresh character, try to reach any of the above **before** Montserrat | - | The drunkard's ask is absent, Quinn's reply is absent, the witch's reply is absent. Nothing in the chain is reachable early |
| NR13 | **No double perk.** After NR11, check your perk list, then talk to him again | - | **One** `Clear Head`, and he does not re-offer. The grant is guarded by a `CHasPerkExpression` |
| NR14 | **Nothing shipped disturbed.** Run Quinn's own `Troll Hide` and `Wasp Stingers` fetches and his shop tiers; run the witch's Nostradamus, caverns and Cathar branches | - | All unchanged. Three heavily-used trees were edited and none of their existing content may shift |
| NR15 | Check the drunkard still works for a character who **never** gave him gold | - | He stays in his gibberish state. The whole chain hangs off the kindness in NR1 |
| NR16 | Judge the **writing**, which no check can settle | - | Does the drunkard read as pitiable rather than comic? Is Na Roqua's warning about the dose unsettling? And is `Clear Head` a joke that lands, or one that explains itself too much? |

## The turret ring, and a promise that outlives its quest

`DaVinci Tank Gear` was the last hand-authored quest item nothing referenced. Half its quest already
ships: the hidden chamber, the machines modelled and examinable in it, and DaVinci saying the engine
needs a spirit -- which feeds the **live** `Obtain the Spirit Gem for DaVinci`. These rows cover the
gear half.

**The gear comes from the talking steam engine in the workshop**, not the blacksmith. An early draft
of this release used Eduardo and was discarded for making the quest a conversation; if any row below
sends you to the blacksmith, something shipped that should not have.

**`MC9` and `MC12` are the rows that prove the design.** The promise deliberately outlives the
quest: the gear is handed over and the quest completes in the chamber, but the debt can only be
settled afterwards in the workshop where the engine can hear it. There is **no betrayal option** --
it is broken by never going back.

| # | Where | Steps | Pass |
|---|---|---|---|
| MC1 | **The setup.** Reach DaVinci's hidden chamber and talk to him | - | Unchanged from vanilla, plus a new reply asking whether the gears are finished -> `901`. He sends you to his engine, **not** to a blacksmith |
| MC2 | Examine the machines in the chamber | - | `1 Catapult`, `1 Sweeper`, `1 Siege Tank` all still work and still say the machines are incomplete. Untouched vanilla |
| MC3 | Check the quest log after MC1 | - | `Create Mechanical Gears for DaVinci's Siege Tank` appears and names the steam engine. In vanilla this quest had **no states at all** and could never appear |
| MC4 | **The machine.** In the workshop, pull the lever and raise the turret gear | - | `700` -- it sizes the job up at forty-one teeth and asks what you are bringing. Three replies plus a walk-away |
| MC5 | **Route 1, pay.** Carry any potion and offer it | - | The gear is cut, **and the potion is gone from your inventory**. If you keep the potion, the cost is not being charged |
| MC6 | **Route 2, haggle.** At Barter 35+, out-argue it | - | `704` -- it concedes, resentfully, and cuts the gear for nothing. Below Barter 35 this reply is absent |
| MC7 | **Route 3, promise.** Offer to tell DaVinci who built it | - | `702` -- it names its terms: say it to him, **in that room**, out loud. The gear is free |
| MC8 | All three routes | - | Each ends at `705`, you receive one Rotary Gear, and the journal advances. **Never more than one gear** |
| MC9 | **The row that proves the design.** Take route 3, hand the gear to DaVinci in the chamber, then leave and come back to the workshop | - | The quest is **complete** and paid, but the engine is **still owed**. A new reply to DaVinci in the workshop offers to say it. The debt survived the quest ending |
| MC10 | After MC9, take that reply | - | `903` -- DaVinci stops, is embarrassed rather than angry, and says he has been too proud to walk ten feet for thirty years. He credits the crossbow gears too |
| MC11 | After MC10, go back to the machine | - | It no longer raises the subject. The debt is settled and it returns to its normal hissing |
| MC12 | **The other row that proves it. Never go back.** Take route 3, finish the quest, and simply never credit the engine. Talk to it a few times | - | `706` every time -- *"One sentence, where I can hear it. Until then I have nothing to say to you that is not this."* There is **no reply anywhere that betrays the promise on purpose**; it breaks by neglect |
| MC13 | Take routes 1 or 2 instead, then talk to DaVinci in the workshop | - | **No** crediting reply appears, and the machine never reproaches you. The obligation only exists if you made it |
| MC14 | **The crossbow must be untouched.** Run the vanilla crossbow-gear trade at `650 collect gears` | - | Still works exactly as before, still gives `DaVinci Crossbow Gears` for a potion |
| MC15 | **The spirit half must be untouched.** Ask him why the engine needs a spirit, and run `Obtain the Spirit Gem for DaVinci` | - | Unchanged. The two halves of the machine are independent and neither blocks the other |
| MC16 | Judge the **writing**, which no check can settle | - | Does the engine read as aggrieved rather than merely rude? Does DaVinci's embarrassment land? And is the promise worth keeping when nothing mechanical rewards it? That last one is the whole point of the release |

## Andre's own reaction to being sold

0.41.0 made the betrayal possible. These rows cover Andre answering it -- his two post-betrayal
greetings, both voiced, both with **0** incoming links in vanilla.

**Unlike 0.41.0, nothing here is a rename.** These two recordings were always correctly named; they
were silent because nothing could reach the nodes. If a line is subtitled and silent in these rows,
that is a *different* bug from the one 0.41.0 fixed and worth saying so in the report.

**`AG4` is the row to walk** -- it ends in a fight that has never happened in this game.
**`AG8` is the regression guard**: betrayal alone must not shadow 0.41.0's `1003`. If AG8 fails,
0.42.0 has undone 0.41.0.

Two markers drive it: `Lucius thrown out` (declared in 0.41.0, set by the mayor) and
`Lucius extorted` (vanilla's own, set by the five replies that take his gold).

| # | Where | Steps | Pass |
|---|---|---|---|
| AG1 | **Baseline, no betrayal.** Meet Andre on the Montaillou road, keep his secret, come and go several times | - | Normal dialogue throughout -- `02 Return Dialogue`, or `03 Return accepted Lethos quest` once the Mneme quest is active. **Neither `900` line appears** |
| AG2 | **Betray him, no money taken.** Never accept his gold; tell the mayor; return to Andre | - | *"You are a very, very bad man and you lead a trite and meaningless existence. Now leave me alone."* **And you should hear it** -- 96 KB that never played |
| AG3 | After AG2, approach him repeatedly | - | Same brush-off each time. He does not attack and does not revert to normal dialogue |
| AG4 | **The row to walk. Take his money, then betray him.** Accept gold at `830 Extortion`, then tell the mayor, then return to Andre | - | *"I paid you your blood money and still you betray me! I have had all I can stand from you, runt!"* -- audible (84 KB) -- **and then he attacks you.** That `CGoToCombatAction` has never fired in this game |
| AG5 | Survive or flee AG4, then re-approach | - | He stays hostile. He must not fall back into dialogue mid-fight |
| AG6 | **Both map paths.** Repeat AG2 and AG4 having reached him by the *other* route -- fighting past him versus talking past him | - | Identical behaviour. The two selectors (`Lucius Wrasslin`, `Talked past Lucius`) were edited identically and must agree |
| AG7 | **Order check.** Take his gold **and** betray him, with the titan hunt **unfinished** | - | The extorted line wins, not the generic brush-off. Extortion-then-betrayal outranks everything |
| AG8 | **The regression guard.** Betray him (no gold taken), **complete `Kill the Titans of Toulouse`**, then return | - | He uses **`1003`** -- *"I think our dealings are at an end, fleshling"* -- **not** the generic `900` brush-off. If the brush-off appears instead, 0.42.0 has shadowed 0.41.0's wiring and must be pulled |
| AG9 | As AG8 but **with** gold taken | - | The extorted line and the fight still win. Combat outranks the post-quest dismissal |
| AG10 | **The shipped cascade survived.** Without betraying him, verify `02 Return Dialogue`, `03 Return accepted Lethos quest`, `1100 Surrender`, `120 Andre Defeated` and `3000 Unlocked the door` all still work as before | - | Unchanged. The whole shipped chain was demoted inside the new tests and must be byte-identical in behaviour |
| AG11 | **Hand over the hearts** after betraying him, where he is not hostile (AG2 path) | - | `1002 Hearts in Hand but Lucius betrayed` still fires, as 0.41.0 intended. The two releases must compose |
| AG12 | **The Blacksmith, which must NOT have changed.** In the Gate District, commission a Lion Shield or Sacred Scimitar, collect it, and take *"Yes, I need the shield and something else"* | - | You reach `07 what more` with its full menu **including the Red Ore hand-in**. Node `80 Do You Have The Item I Need?` is a superseded draft and was deliberately left unreachable -- if it appears, something was wired that should not have been |

## The Lucius betrayal, and six silent recordings

Andre the rock titan on the Montaillou road is really **Lucius**. He hides in the village
pretending to protect it, and asks the player to kill the elders of his own tribe in Toulouse. The
player can keep his secret or tell the mayor.

**Telling the mayor did nothing in vanilla.** `951 Furious Mayor` activates a marker named
`Lucius thrown out`, and no entity of that name was declared in any map, so the flag could never be
set. Everything below hangs off declaring it.

**`LU5` proves the release. `LU9` is the regression that matters most** -- in vanilla *every*
post-quest return used the "our dealings are at an end" line, so a loyal player got a cold shoulder
they never earned. If LU9 fails, the gate is worse than before.

**Voiceover is the other half.** Audio resolves purely as `<Tree> VOs/<Node ID>.ogg` with no
indirection, so these lines were silent because filenames and node IDs disagreed by a letter. Rows
that say *you should hear him* are testing exactly that -- if the line is subtitled but mute, the
rename did not take.

| # | Where | Steps | Pass |
|---|---|---|---|
| LU1 | **The secret.** Meet Andre on the Montaillou road, get through to `805 Sticky Situation` and hear his story | - | Unchanged from vanilla. He asks you to keep his secret and kill the Toulouse titans |
| LU2 | **Keep the secret.** Take `820 PC Saves the day`, never speak to the mayor | - | Unchanged |
| LU3 | **Take his money.** `830 Extortion` | - | You get gold and the `Lucius extorted` marker sets, as in vanilla |
| LU4 | **Betray him.** Go to the mayor, take *"I've spoken with Lucius. He has been lying"* through to `951 Furious Mayor` and the reply that gets you hired | - | The mayor is furious. **This now sets a flag that persists** -- in vanilla it activated nothing |
| LU5 | **The row that proves it.** After LU4, kill the four Toulouse titans, return to Andre and hand over the four stone hearts | - | He uses **`1002 Hearts in Hand but Lucius betrayed`**: *"I've heard that you exposed me to the mayor despite the agreement we reached... you'll get not one more ounce of gold from me."* **And you should hear him say it** -- 306 KB of recording that never played |
| LU6 | Do LU5 **without** betraying him | - | He uses `1000 Hearts in Hand` and pays you, exactly as vanilla did. The two replies are mutually exclusive -- **never both** |
| LU7 | **Brother Michel.** After LU4, find him in the house interior and talk to him | - | He meets you with *"Lucius, despite his flaws, was a harmless, lonely soul. Your meddling has cast him out of the only home he is likely ever to have."* Audible (149 KB). Talk again: *"Leave. Now."* (25 KB) |
| LU8 | Talk to Brother Michel **without** betraying Lucius | - | Normal dialogue. And if Andre is dead, his shipped `05`/`07` Andre-Slain greetings must still work -- that chain was demoted to the `Else` and must be intact |
| LU9 | **The regression that matters.** Keep the secret, complete `Kill the Titans of Toulouse`, then return to Andre | - | He must **not** say *"I think our dealings are at an end, fleshling."* In vanilla he always did. A loyal player gets normal return dialogue |
| LU10 | Do LU9 **after** betraying him | - | Now he **does** use `1003` -- and you should hear it (55 KB) |
| LU11 | **`1001 Lucious Exposed`.** Reach the node where he explains whose hearts you brought | - | Audible -- 293 KB that never played. *"These cold hearts belonged to the other elders of my tribe, the ones who forced me to run for my life."* |
| LU12 | **Shylocke**, Temple District. Reach his *favors you* return greeting | - | Audible -- 91 KB. Unrelated to Lucius; same filename-drift cause |
| LU13 | **No duplicate journal.** Check the quest log through all of the above | - | Only `Retrieve the Crystal Mneme from Lucius` appears. `Help Andre the Titan with his tasks` is a superseded duplicate and must **stay** dormant |
| LU14 | **The extortion combination.** Take his gold (LU3) **and then** betray him (LU4), then return with hearts | - | `1002` fires. Note that Andre's own angrier `900 Lucius extorted and thrown out of town` greeting is **still not wired** -- that is known and deliberate, not a failure of this row |

## Convince DaVinci to Join the Dark Wielders

Implemented rather than restored -- the quest shipped as a stub with **no states**, and DaVinci's
112 dialogue nodes and 127 recordings contain **nothing** about the dark path. So there is no
vanilla behaviour to regress against here; every row below is new ground.

**Persuasion-only, by necessity.** `Races/NPCs/Wielders/Leonardo DaVinci` is **AC 1000 / HP 10000**
-- the deliberate-immortality pattern used for the game's children -- because `08 Final
Encounter.zax` holds 232 DaVinci references and its endings are a matrix over {Old Man escapes /
killed / talked to death} x {DaVinci alive or dead} x {Galileo alive or dead} x {player good or
evil}. **Do not test for a kill option; there is none, and adding one was rejected on the merits.**

**The task is optional and offered on Relican's hub**, outside the task 1-2-3 chain. A player who
never speaks to DaVinci should notice no difference at all -- `LD15` checks exactly that.

**`LD4` is the row that matters most**, and `LD9` is the only place 0.40.0 and 0.39.0 interlock.

**Expect silence.** 106 of DaVinci's 112 nodes are voiced; the three new ones are not. That is a
known, unfixable gap, not a bug to report.

| # | Where | Steps | Pass |
|---|---|---|---|
| LD1 | **The offer.** On Relican's path, talk to Lord Relican at his hub | - | A `Quest Icon` reply asks about Leonardo in the Gate District -> `90 Fixt DaVinci task`. He says he will not have him killed, *"a corpse invents nothing"*. The journal gains `Convince DaVinci to Join the Dark Wielders` |
| LD2 | Decline the task (*"Leave the tinker to his toys"*) | - | Conversation ends, no quest activated, and the reply is still offered next time |
| LD3 | **The approach.** With the task active, talk to DaVinci | - | A `Quest Icon` reply about carrying another man's words -> `800 Fixt Relican Offer`. It must appear from **all five** of his entry nodes: first meeting, the two other first-meeting variants, `3 Return Dialogue`, and `3 Return Dialogue Workshop` |
| LD4 | **The row that matters. Refuse him** -- take the ungated *"Relican is offering you power"* reply -> `802` -- then check everything he still does: his shop talk, the Wielder referral to Quinn, and `Build DaVinci's Repeating Crossbow` if you have it | - | **Nothing is withdrawn.** He argues you off the path and takes nothing away. If his crossbow quest breaks or the Quinn referral vanishes, the refusal has teeth it was explicitly not meant to have |
| LD5 | After LD4, talk to him again | - | He does **not** re-offer the conversion; the quest has moved to the refused state. He is cold but functional |
| LD6 | **The ideological route.** At Speech 50 or above, take the reply about the man left in the ether pocket | - | He concedes -> `801 Fixt DaVinci Joins`, journal advances to "return to Relican" |
| LD7 | Try LD6 **below** Speech 50 | - | That reply is absent. Only the ungated attempt and the back-out remain |
| LD8 | **The arcane route.** With General Thought **or** General Tribal at 80+, take the mastery reply | - | Present and it works. Check **both** disciplines independently -- the gate is a `COR` of vanilla's two 80-threshold cans, so either alone must suffice |
| LD9 | **Where 0.39.0 interlocks.** Carrying the **Ring of the Trapped Spirit** from the Enchanter's pact, talk to DaVinci | - | A third route appears -- *"I have been down the well... He wears my bargain now"* -- and succeeds. Without the ring it must be absent |
| LD10 | Take the back-out reply (*"Nothing. Forget that I raised it"*) | - | Conversation ends and the quest stays open: the approach reply is offered again next time. **This must be retryable** |
| LD11 | **Report success.** After LD6/LD8/LD9, return to Relican | - | A reply reports Leonardo will not stand against him -> `91 Fixt DaVinci joined`. Quest **completes** and you gain **650 XP** |
| LD12 | **Report the refusal.** After LD4, return to Relican | - | A reply reports Leonardo refused -> `92 Fixt DaVinci refused`. Quest **completes** -- it must not sit open or show as failed -- and pays **no** XP |
| LD13 | Check the journal after both LD11 and LD12 | - | No dangling entry in either case. Both paths close the quest |
| LD14 | **No interference.** Run the Quinn task and `40 dark wielder task 3` with the DaVinci quest active, and again after completing it | - | Unchanged. The DaVinci task sits on the hub, not in the numbered chain |
| LD15 | **The ignore case.** Play the whole Dark Wielder initiation and never speak to DaVinci about Relican | - | Identical to 0.39.0. The task is optional and nothing waits on it |
| LD16 | Judge the **writing**, which no check can verify | - | Does Relican's refusal to have him killed read as his own judgement rather than an engine limit? Does DaVinci's warning land as concern rather than a lecture? This is the only row that can fail on craft |

## The Enchanter's Bargain, and the Dark Wielders' missing bind step

The Trapped Ether Plane is reached through a well in La Calle Perdida -- `Well 5 door`,
`Trigger Only Once=0`, `Is Locked=0`, no key and no requirement, so it is freely re-enterable.
**Everything in this section is in a questline that has never been played**, so treat the whole
Dark Wielder path as new ground rather than as a regression surface.

The non-lethal resolution of the Enchanter is **ungated** -- `Requirement=!None` at every step of
`03 Conversation Start at Island` -> `50 Escape` -> `55 Escape 2` -> `57 Escape 3` -> `59 Winner`.
At `50 Escape` two replies read almost identically; the one mentioning that he *lost his mind*
routes to `53 Whoops` and a fight. That is vanilla behaviour, not a new trap, but it is the easiest
way to fail these rows by accident.

**`EB7` and `EB12` are the rows that prove the release.** EB7 is the Relican fallback, the only
thing standing between the DaVinci swap and an unfinishable questline. EB12 is the bind itself.

| # | Where | Steps | Pass |
|---|---|---|---|
| EB1 | **The well.** La Calle Perdida, find and enter the well | - | You reach the Trapped Ether Plane. Re-enter it a second time to confirm the door is not once-only |
| EB2 | **Kill him.** Fight the Enchanter to death as in vanilla | - | He drops `Kublai Khans Sword` and gold, exactly as before. **Nothing in this release may change this route** |
| EB3 | **Talk him to death.** The `63/65 Self Destruct` route | - | Unchanged from vanilla; he destroys himself and the crystal powers |
| EB4 | **Spare him.** Take `50 Escape` -> `55` -> `57` -> `59 Winner` without insulting him | - | He spares you, then **`61 Fixt Bound Token`** fires and you receive the **Amulet of the Trapped Spirit** |
| EB5 | After EB4, leave the plane by powering the crystal from the spirits | - | You get out **with the Enchanter still alive**. This is the shipped route; confirm 0.39.0 did not break it |
| EB6 | After EB4, re-enter the plane and talk to him | - | He is non-hostile and opens at `05 Return Dialogue 1` |
| EB7 | **The fallback, and the row that matters most.** On Relican's path, take the Sceptre shell from DaVinci's secret chamber, then **kill the Enchanter** (or never enter the plane), then talk to Relican | - | A reply offers *"I have the Sceptre, but it is a dead thing"* -> **`47 Fixt Relican Binds Shell`**. He binds it, you receive `Rod Bone WITH Spirit`, the quest completes and you continue to `40 dark wielder task 2`. **If this reply does not appear, the Dark Wielder initiation is unfinishable and the release must be pulled** |
| EB8 | **The shell is now the drop.** Open DaVinci's secret chamber | - | You get the **empty** Sceptre of Bone -- *"Fashioned darkwood that is but an empty shell without a spirit to power it"* -- not the finished one |
| EB9 | Check the quest journal after EB8 | - | `Create a Rod Of Bone` reads the new middle state about the sceptre being lifeless, not still "recover the Sceptre" |
| EB10 | **The pact.** On Relican's path, with the Enchanter spared, talk to him | - | A `Quest Icon` reply offers the hidden city of wielders -> `70 Fixt Pact 1` -> `71 Fixt Pact 2`. You receive the **Ring of the Trapped Spirit** |
| EB11 | Try EB10 **without** having joined Relican | - | The pact reply is **absent**. It is gated on the Dark Wielder initiation having been activated |
| EB12 | **The bind.** After the pact, carrying the shell, talk to him again | - | A reply offers the empty sceptre -> **`75 Fixt Sceptre`**. The shell is removed, `Rod Bone WITH Spirit` arrives, and the journal advances to "deliver the Sceptre to Lord Relican" |
| EB13 | Try EB12 **without** the shell in inventory | - | The reply is absent. It is gated on holding the shell *and* being at the bind step |
| EB14 | **The exploit, which must be gone.** Equip `Rod Bone WITH Spirit`, note Thought and Tribal, then **drop it and pick it up** five times | - | Skills do **not** climb. As shipped this granted +2 to eight disciplines per pickup, without limit. If they still climb, the fix did not take |
| EB15 | Equip and unequip the spirited Sceptre | - | The +2 to each Thought and Tribal discipline appears **only while equipped**, and is fully removed on unequip |
| EB16 | **The set bonus.** Wear the Amulet alone, then the Ring alone, then both, noting Mana Capacity each time | - | +20, +10, and **+40** -- the pair is worth 10 more than the sum. Spell Resistance +5 comes from the amulet only |
| EB17 | **The bluff route completes the pair.** Resolve him by the `40 Barter` -> `43` -> `45 Barter 3` bluff instead of `59 Winner`, then take the pact | - | You receive **both** items, not just the ring. `Trigger Only Once=1` must yield **exactly one** amulet -- if two arrive, the guard failed |
| EB18 | **The title.** Finish the dark path and answer **Yes** to Relican's Summoning Ring | - | You gain **`Ruler of Calle Perdida`** / "Dark Lord of Calle Perdida". Karma still drops 800 and the three good quests still fail, exactly as before -- the only change is that the ending now names you |

## The magic loot pipeline was never connected

From the unused-content survey, and it took tracing a chain to the end rather than one link.

`1 MASTER ALL Items in the game` is drawn by real maps -- `04 Maw of the Assasin`,
`06 Chamber of Torment`, `07 Dark Temple`, `Cortez Cave`. Walking down from it, the miscellaneous
branch yielded:

| | |
|---|---|
| weighting 17 | eight **plain, unenchanted** base items -- Amulet, Belt, Boots, Bracers, Gauntlet, Helmet, Necklace, Ring |
| weighting 2 | `All Scrolls` -> `Scroll selection MAGIC` |

And nothing else. The `*selection MAGIC` cans -- the things that pair a base item **with an
enchantment** -- were reachable for potions and scrolls only. Seven were referenced by **nothing at
all**: `Amulet`, `Belt`, `Bracer`, `Cloak`, `Helmet`, `Ring` and `Bolt`. `Wand selection MAGIC` was one
dead link from the same fate, reachable only through `All Wands`, which nothing drew from.

So **magic equipment did not drop in this game.** Only its plain versions did. The enchantment half of
the system was built and never wired in.

> This section replaces an earlier claim in the survey that 62 of 65 orphaned magic recipes were
> "redundant duplicates whose enchantments reach the player anyway." That check confirmed a selection
> can *listed* an enchantment and never asked whether the selection can was itself reachable.

### What was connected

| | |
|---|---|
| `All Wands` -> `All Misc Items except Potions` | weighting **2**, copying the `All Scrolls` entry's exact shape |
| **`Wand of Swarm`** into `Wand selection MAGIC` | weighting **5**, matching `Rigor Mortis` -- the one other `5 Unique` already in that pool |
| new `All Magic Equipment.can` | the six orphaned pools at weighting **10 each**, the same equal weighting the eight plain base items use |
| `All Magic Equipment` -> `All Misc Items except Potions` | weighting **2**, matching scrolls and wands |

**One intermediate can rather than six branches**, which is the decision worth recording. Six separate
branches at weighting 2 each would have made magic equipment **12 of 33** -- about 36% of misc drops,
against the ~9% scrolls and wands each get. The composition is now:

| branch | share |
|---|---|
| plain equipment | **74%** |
| scrolls | 9% |
| wands | 9% |
| **magic equipment** | **9%** |

All **40** enchantments across the six pools were checked before wiring and every one is implemented.

### Mojo gating, added in 0.38.1

0.38.0 connected the pools with **no progression gating**, so a `5 Unique` ring could drop in act 1
where median party mojo is 3-10. The pools weight rarity only softly -- mean weight falls Common 22.5,
Uncommon 17.1, Rare 13.7, Very Rare 12.1, Unique 8.6 -- but `Ring Metal Fist` and `Helmet Sylvant` are
both `5 Unique` at weight **20**.

`All Magic Equipment` is now a **`CInventoryItemGeneratorMojoList`** with
`Mojo Expression=CAverageMojo`, at thresholds **7 / 16 / 999** -- the same thresholds vanilla's
`All Armor` uses, not invented ones. And each tiered pool follows the `Armor LOW Mojo` idiom: it keeps
**every entry its parent had** and sets `Weighting=0` on the too-good rarities, so a diff shows weights
moving rather than entries disappearing.

| average party mojo | pools | live enchantments | rarities |
|---|---|---|---|
| **<= 7** | 2 -- Amulet, Ring | **9** | Common, Uncommon |
| **<= 16** | 6 -- all | **22** | + Rare |
| **> 16** | 6 -- all | **40** | + Very Rare, Unique |

**Belt, Bracer, Cloak and Helmet have no Common or Uncommon enchantment at all** -- every one is Rare
or above -- so at the LOW band all four would have been pools with every weight zeroed. Viability was
checked before building and they are left out of that band rather than shipped empty. That is a
property of vanilla's rarity assignments, not a design choice.

For scale, from the mana survey: act 1 median mojo is 3-10, the Crypt 18, Nostradamus 26, Alamut 40.

### What was deliberately left out

**`Fire and Ice` and `Mage`**, the other two wands in `Wands/Special/`, are **description-only
shells** -- 1,036 and 1,161 bytes with **no behaviours and no modifiers at all**. Their text promises
Fireball-and-Ice-Storm-together and +4 skill points in every magic skill; none of it exists. Wiring
them would ship unique wands that do nothing. `Fire and Ice` also carries **value 0**.

**`Boot`, `Gauntlet` and `Necklace selection MAGIC`** are each already reachable from one specific map
-- narrowly available rather than absent -- so changing their rate is a different decision from
connecting something unreachable. `Bolt` and `Arrow` are ammunition in the same position.

| # | Step | Say | Expect |
|---|---|---|---|
| WD1 | **The row this exists for.** Play act 4 or act 8 -- the Crypt, Alamut's Maw of the Assasin, Chamber of Torment, Dark Temple -- and look at what drops | - | **Magic rings, amulets, belts, bracers, cloaks and helmets.** 40 enchantments that have never appeared on those slots in this game. Previously only the plain versions dropped |
| WD2 | Compare against a vanilla install in the same maps | - | Plain equipment still dominates -- it keeps its weighting of 17 against the magic branch's 2. If plain gear has become scarce, the weighting is wrong |
| WD3 | **Wands.** Watch for any wand at all dropping | - | Wands now appear. In vanilla only `Wand Lightning Major` was placed anywhere, and the random pool was disconnected, so this is 16 enchantments appearing for the first time |
| WD4 | Specifically: a **Wand of Swarm** | - | `5 Unique`, summons insects via `Insect Plague`, and confers ranged-damage resistance while it still has charges. Weighting 5 of 255 in the wand pool, so rare -- do not expect it quickly |
| WD5 | Try a wand you find | - | It casts, and spends a charge. The `CPlugInBehaviorWand` machinery was always complete; only the placement was missing |
| WD6 | **The balance row.** Judge whether loot now feels too generous | - | Magic equipment is **9%** of one branch of one generator. If the game now rains magic items, that share is the dial. This is the row I would most expect to need adjusting |
| WD7 | Check whether magic equipment appears in **shops** as well as drops | - | Whatever vanilla does. Merchant inventories were not touched, so if shops draw from the same generator they will stock it too -- worth knowing either way |
| WD8 | Judge the **power** of the new enchantments at the act you find them | - | **Gated as of 0.38.1** -- see the three bands below. 0.38.0 shipped this branch with no progression gating at all, which was the one real defect in it |
| WD8a | **Act 1, low mojo.** Play the Gate District, Port District and sewers and watch magic equipment | - | **Amulets and rings only**, and nothing rarer than Uncommon -- 9 live enchantments. No magic belts, bracers, cloaks or helmets at all, because none of those has a Common or Uncommon enchantment to offer |
| WD8b | **Mid game, mojo 7-16.** Montserrat, Montaillou | - | All six slots now, up to **Rare** -- 22 live enchantments. Still nothing Very Rare or Unique |
| WD8c | **The Crypt onward, mojo above 16** | - | The full **40**, including Very Rare and Unique. A `Ring Metal Fist` or `Helmet Sylvant` is fair here and was not in act 1 |
| WD8d | **The row that proves the gate is real.** Find any magic equipment in act 1 and check its rarity in the item description | - | Never above Uncommon. If a Very Rare or Unique turns up early, the mojo list is not being consulted and the gating has failed |
| WD8e | Compare against **vanilla armour** drops at the same points | - | They should feel consistent -- the thresholds are literally vanilla's own 7 / 16 / 999 from `All Armor`, so magic equipment and armour now step up together |
| WD9 | Look for an item that appears **unenchanted but named** as if magic | - | None. All 40 enchantments were verified implemented before wiring, unlike the two wand shells |
| WD10 | Fight in act 1 and 2 and watch drops | - | Changed only as much as those acts draw from `1 MASTER ALL Items in the game`. Most early maps use their own tables, so the shift should be smaller there |
| WD11 | **Potions and scrolls** | - | **Unchanged.** Both branches were already connected and their weightings were not touched |
| WD12 | The eight **plain** base items | - | All still present and still at weighting 17. Verified in the shipped bytes, but this is the row that proves it in play |
| WD13 | Look for a **Wand of Mage** or a **Wand of Fire and Ice** | - | **Neither should ever drop.** They are shells with no implementation and were deliberately excluded. If one appears, something wired them by accident |
| WD14 | Boots, gauntlets and necklaces | - | Their magic versions still only come from the one map each that references them. Unchanged by design -- if that inconsistency is annoying, it is one entry each to fix |
| WD15 | Sell a new magic item to a merchant | - | It prices by its enchantment's own value. Nothing here set a price; all values are vanilla's |
| WD16 | **The regression row.** Confirm armour and weapon drops are untouched | - | `All Armor and Shields` and `All Weapons` are separate branches of the master and were not edited |

## Monster Summoning: the top two tiers were unreachable

From the unused-content survey: **`Summoned Cans/Monster Summoning Level 4 01/02/03` and
`Level 5 01/02/03` are referenced by nothing at all.** Six cans, each with its own dedicated `.Race`
and a working model, finished and disconnected -- the top two tiers of the Tribal summoning line.

One tell that they were abandoned mid-polish: **all six races are named `Black Wolf`**, copied from
the wolf summon and never renamed. The same signature as the Templar helm keeping its shield art.

### Where the tier table actually lives

Not in the skill. `Monster Summoning.Skill` references **no cans at all** -- it fires a `Spellcast`
relay, and selection happens in
`Spell Projectiles/Monster Summoning Instant Hit Projectile.InventoryItem`. That file branches on
`CSkillsNamedExpressionExpression(Monster Summoning, "single")`, and **the two sides are shaped
completely differently**:

| branch | shape |
|---|---|
| **single** | a tier ladder on skill value -- `CIsLessThan 50`, `CIsLessThan 100`, else |
| **multi** | **no skill gating at all** -- two sequential draws, a low/mid pool of 5 and a high pool of 3 |

Tier 3 previously covered skill **100 all the way to the cap**, two thirds of the range on one tier,
which is itself a sign the ladder was meant to continue.

### What changed

**The single ladder now continues**, keeping vanilla's own 50-point spacing:

| skill | summons |
|---|---|
| < 50 | Guard Dog 01, Wolf 01 |
| < 100 | Guard Dog 02, Vodyanoi 02, Wolf 02 |
| **< 150** | Guard Dog 03, Vodyanoi 03, Wolf 03 -- *contents unchanged, now bounded* |
| **< 200** | **Snake Women** (90 HP), **Ogre variant** (120), **Wererat Boss** (90) |
| **200+** | **Rock Titan Blue** (170 HP), **Desert Beast** (120), **Sand Spirit** (120) |

**The multi pool grew from 3 to 9**, adding all six new cans to the high draw. No new threshold there:
multi is already gated behind high skill by the spell's own `multi` expression, and restructuring that
side into a ladder would be a much larger change for no gameplay gain.

**The tier-4 and tier-5 blocks are clones of the tier-3 block with the can names swapped.** Every tier
carries a `CAddAIAction` that drains mana for upkeep -- the thing that makes a summon cost something --
and cloning preserves it byte-for-byte rather than rebuilding it by hand. Both new tiers verified at
**3 mana** upkeep, the same as every existing tier.

**Three attempts, two instructive failures.** The first assumed the single and multi branches were
identical ladders; they are not. The second got the conditional's fields wrong -- in this game
`CIfExpressionAction` takes **`If Expression`** (not `Expression`), plus
`Character to get attributes from`, and carries **no** `Return failure` tail, unlike
`CConditionalAction`.

| # | Step | Say | Expect |
|---|---|---|---|
| SM1 | **The row this exists for.** A Tribal caster with **Monster Summoning at 200+**. Cast it | - | A **Rock Titan**, a Desert Beast or a Sand Spirit. No summon above tier 3 has ever appeared in this game |
| SM2 | The same caster at **150-199** | - | Snake Women, an Ogre variant or a Wererat Boss -- tier 4 |
| SM3 | At **100-149** | - | Guard Dog 03 / Vodyanoi 03 / Wolf 03, exactly as before. **This tier's contents did not change**, it is only bounded above now. If it changed, the splice hit the wrong block |
| SM4 | At **under 50**, and then **50-99** | - | The two lowest tiers, unchanged. These were not touched at all |
| SM5 | **The upkeep row.** Watch your mana while a tier-4 or tier-5 summon is alive | - | It drains, at the same rate as a low-tier summon -- **3 mana** per tick. If a high summon is free to maintain, the cloned `CAddAIAction` did not come across and that is a real bug |
| SM6 | Let a tier-5 summon expire or die | - | It vanishes cleanly like any other summon, and the drain stops. The clone carried the whole lifecycle, not just the creation |
| SM7 | **The multi row.** Cast with multi-summon available (high skill) | - | Two creatures, and the second draw can now roll any of **9** options including the new six. Previously it drew from 3 |
| SM8 | Cast single, then multi, then single again | - | No interference. The two branches are separate structures in the same file and the edit touched each independently |
| SM9 | Judge whether a **Rock Titan** is too strong as a summon | - | It is 170 HP against the previous ceiling of a Wolf 03. This is the one number worth arguing about -- the cans are vanilla's own, but nobody has ever fought alongside one. If it trivialises fights, say so |
| SM10 | Check the summon's name in the combat log and on hover | - | It will probably read **"Black Wolf"** -- all six races carry that display name in vanilla, copied from the wolf summon and never renamed. **Expected, not a new bug**, but worth confirming so it can be fixed deliberately rather than found by surprise |
| SM11 | Try to maintain two summoning spells at once | - | Still refused. `CDisableRecastingOfSpellForSpellsDuration` was untouched, and the skill description says you may not |
| SM12 | Cast `Raise Undead` and `Spiritual Knight` | - | **Unchanged.** They use their own projectiles -- `Raise Undead Instant Hit Projectile` draws `Zombie 01`, `Spiritual Knight` draws the five `Knight Templar` cans. Only Monster Summoning's projectile was edited |
| SM13 | A **non-Tribal** character | - | Nothing changes. The edit is inside one spell's projectile |
| SM14 | Watch for a summon appearing with no model or dropping through the floor | - | None. All six cans resolve to real `Cache/Models/*.mdl16` files and `Rock Titan Blue` also has a `Models3D/.../Rock Titan Blue.MODEL.GR2`, so no art is missing. But these have never been spawned, so this is the row that proves it |

## The Templar set - two items, one of them broken

Asked in play: *"what are the other unused items? I didn't know the mine deed existed."* The full
survey is in [`unused-content.md`](unused-content.md); this is the first item pair taken off it.

**`Helm of the Templars` was unfinished, not merely unplaced** -- which is very likely why nobody ever
placed it. It is a `Character Slot Types/Head` item that carried **shield art in every other field**:

| field | vanilla | repaired from `Inventory Items/Helmet.InventoryItem` |
|---|---|---|
| `On the ground` | `Special Items/LionShield_PU` | `Items/PickUps/Misc Items/Helmet_PU` |
| `Basic` / `Better` / `Special` | `Armor/Shield Large Better` | `Items/Inventory Images/Armor/Helmet1` |
| `Catagory for display Grouping` | `Grouping Catagories/Shield Large` | `Inventory/Grouping Catagories/Armor` |

Someone cloned the shield, changed the name, description and slot, and stopped. `Encumbrance=2` and `Value=100` are untouched.

**And then they were given stats, because they had none.** As shipped, both pieces' only behaviours
were `CPlugInBehaviorPickUpAction` and `CPlugInBehaviorPutDownAction` -- the *sounds* they make when
handled. No armour class, no resistances, no `Wearing a Helmet` flag, no model override, and
`Inventory Addition Group=!None` so they could never be enchanted. An item described as *"shines with
the power of the Templars"* was **strictly worse than a plain helmet off any thug**.

Every number is taken from the vanilla item of the same weight rather than invented:

**The first pass of these numbers was wrong and was retuned.** It copied `Helmet` (+3) and
`ShieldMedium` (+4) because they match the pieces' encumbrance -- but encumbrance is the wrong
yardstick for a unique. A player reaching act 3 already carries `ShieldLarge` at +7 and can stack a
Rare AC addition worth +4 to +6, so the set was outclassed by gear found in acts 1 and 2. The
yardstick that matters is the **ceiling for the two slots the set occupies**:

| | the set | the best alternative for that slot |
|---|---|---|
| Helm, enc 2 | AC **+6** | `Helmet` AC **+3** -- the best base, and `Helmets/Protection` adds **+0** AC, so nothing in the game beats +3 in the head slot |
| Shield, enc 5 | AC **+8**, Piercing **+15**, Slashing **+12**, Crushing **+12**, speed **-0.03** | `ShieldLarge` AC **+7**, P15 S10 C10 -- but at encumbrance **10** and speed **-0.08** |
| both worn | **+4** AC more | the best AC *enchantments* in the game are +4 to +6, rarity 3 Rare |

**Pair total: +18 AC** against the roughly **+10** those two slots otherwise allow. For scale, base AC
is `2*(Agility+10) + 10 + Evasion` -- about 42 at Agility 6 -- and upgrading body armour from Hard
Leather to Hauberk Mail is +10. So the set is a strong reward for committing two slots to it, without
rewriting the character.

The distinguishing feature is **weight**: it protects like a great shield and carries like a medium
one, which is what a blessed Templar kit should feel like. Encumbrance and value stay at vanilla's 2
and 5, and 100.

**Two more bonuses were added on request**, and neither could be a *set* bonus. The +4 AC works
because `(AC) Armor Class` is a **computed** derived attribute, so a conditional term in its
expression re-evaluates when the counter changes. `Skills/Fighting/OneHandedMelee` is a Skill and
`Character Attributes/(LK) Luck` is plain storage with no `Expression=`, so neither has an expression
to host a condition. Both sit on the pieces unconditionally:

| | | calibration |
|---|---|---|
| Shield | `OneHandedMelee` **+5** | unique weapons give +10 to +20 (`Kublai Khans Sword` +10, `TRUE CROSS` +10, `Axe Unholy Smite` +20 Evasion) and enchantments +8 to +15 (`Falcon` +8, `Evader` +15). +5 sits below the enchantment floor, which is right for armour rather than a weapon. A Templar fights sword-and-shield, so it belongs on the shield |
| Helm | `(LK) Luck` **+1** | the blessing |

**The Luck point has no unconditional precedent, and that is worth knowing.** Of the 18
`InventoryItem`s that use `CCharacterModifierAttribute`, the shape is always *conditional* --
`Crossbow` grants +1 Perception only with the `Sharpshooter` perk. So this is the only flat attribute
bonus on any item in the game, and Luck is not a cheap stat: `Fortune`, `CriticalChance` and the Cold,
Fire and Electrical resistances all read it. The field shape is copied from the Crossbow exactly; it
is the *unconditional* part that is new, and that is a balance judgement rather than a technical one.

**The set bonus follows the Voodoo set exactly**, which is the engine's only shipped precedent. There
is no equipment *check* in this game -- `CHasItemEquipped` and every similar class return zero files.
Instead each piece increments a derived attribute with `Allow Accumulation=1`, and a **computed**
attribute reads the total. `Skill Points Per Level` is literally
`10 + Intelligence + (Number of Voodoo Items == 2 ? 1 : 0)`; the Templar bonus is the same shape added
to `(AC) Armor Class`, with a new `Number of Templar Items` counter cloned from the Voodoo one.

**Two risks worth naming.** The set bonus edits `(AC) Armor Class`, a core attribute every character
and creature uses -- `TS12` and `TS13` exist to prove the conditional is inert for everyone without
both pieces. And this adds a **130th** derived character attribute to a game that ships 129, the same
residual risk as the 93rd `.Skill` file in 0.33.0: every can carries a keyed attribute map with no
`Item Count`, so a missing key should default to 0.

**`Spirit Templar Shield` needed nothing.** `Hand` slot, `LionShield_PU`, `Shield Large` icon and
grouping, `Encumbrance=5`. It is coherent in vanilla and only ever lacked a placement.

**Both are carried by `Dead Knight Templar 5`**, inlined as full `CInventoryItem` blocks inside the
corpse's `CAIInventory` -- which is how the Amulet those corpses already carry is stored, since the
array holds definitions rather than paths. Of the five dead-Templar templates that is the only one
used just **twice**, both in act 3's `02 Hamlet Burned`, where Templars died; the other four serve 9
to 15 corpses each and would have scattered a unique set far too widely.

Editing the template rather than the map means **no new map entity**, so this reaches any save that
has not yet entered that map.

**Gate 0 caught two faults in the first splice**, both worth recording. The inventory array closes at
**4 tabs** while each item closes at **5**, so a reverse search for a 4-tab brace matched *inside* the
5-tab one and spliced the new items into the previous item -- the array then declared 3 items and held
1. The fix is `balanced()` plus the start of that brace's own line, and a round-trip through
`resource_format` so formatting is canonical by construction. This is the array-splice trap that has
cost a release before.

| # | Step | Say | Expect |
|---|---|---|---|
| TS1 | **The row this exists for.** Act 3, `02 Hamlet Burned`, on a save that has **not** been in that map. Find the dead Knight Templars and search them | - | **Two** of them carry a **Helm of the Templars** and a **Spirit Templar Shield** alongside the amulet they always had. Neither item has ever appeared in this game |
| TS2 | **The repair row.** Look at the Helm in your inventory | - | It looks like a **helmet** -- helmet icon, and a helmet on the ground when dropped. In vanilla it would have shown a large shield. If it still looks like a shield, the art repair did not take |
| TS3 | Check where the Helm sorts in the inventory list | - | With **armour**, not with shields. Its grouping moved from `Shield Large` to `Armor` |
| TS4 | **Equip the Helm** | - | It goes on your **head**. The slot was always correct in vanilla; this confirms the art change did not disturb it |
| TS5 | Equip the Shield | - | Off hand, as any shield. It needed no repair at all |
| TS6 | Drop both on the ground and look at them | - | A helmet and a shield, two different models. Both previously used the same `LionShield_PU` |
| TS7 | **Equip the Helm and watch AC.** Note your Armor Class, put it on, note it again | - | **+6** -- double the best plain helmet, and nothing enchanted beats it because `Helmets/Protection` grants +0 AC. As shipped the Helm gave **nothing at all** |
| TS7b | Equip the Shield and watch AC and resistances | - | **AC +8**, **Piercing +15, Slashing +12, Crushing +12**, attack speed **-0.03**. That beats `ShieldLarge` (+7, P15 S10 C10) on AC at **half its encumbrance** and with a lighter speed penalty -- the set's identity is protection at medium weight |
| TS7c | **The set bonus.** Wear **one** piece and note AC. Then wear **both** | - | Wearing both grants **+4 AC on top**, equal to a Rare AC enchantment. One piece alone gives no set bonus. Total for the pair: 6 + 8 + 4 = **+18 AC** |
| TS7d | Take one piece back off | - | The set bonus **goes away** and AC drops by 4 more than the piece itself. If it sticks, the counter is not decrementing and that is a real bug |
| TS8 | Search the **other** dead Templars in that map and in Montserrat | - | **Only the amulet.** Templars 1 to 4 are untouched, so the set stays rare |
| TS15 | **Equip the Shield and check your one-handed skill** | - | **+5 OneHandedMelee**. Below the +8 that enchantments give, so it should feel like a competent shield rather than a weapon upgrade |
| TS16 | **Equip the Helm and check Luck** | - | **+1 Luck**. Watch what moves with it -- `Fortune`, `CriticalChance` and the Cold, Fire and Electrical resistances all read Luck, so a single point touches several numbers. **No other item in the game grants a flat attribute**, so if this feels disproportionate, say so: it is the one number here with no vanilla precedent to anchor it |
| TS17 | Take the Helm off and confirm Luck returns | - | Back to its old value, and the derived numbers that read Luck follow it down. An attribute bonus that sticks after unequipping is a real bug |
| TS14 | **The calibration row.** Compare the set against a `ShieldLarge` plus the best helmet you can find | - | The set should be **clearly better**, or it is not worth two slots and a unique find. If it still feels outclassed, the numbers are the dial and this is the row that says so |
| TS9 | A save that **had already entered** `02 Hamlet Burned` before installing | - | The items are **absent**, by engine design -- the corpses were spawned on first entry. Expected, not a bug, and the reason TS1 specifies a fresh approach to that map |
| TS11 | **The latent-bug row.** Confirm the Helm registers as a helmet | - | It now sets `Wearing a Helmet`, which **three shipped files read**, including `Resurrect player.can`. As shipped it did not, so a Templar helm was not a helmet as far as the game was concerned |
| TS12 | **The blast-radius row.** Make a character with **neither** piece and check AC against a vanilla install | - | **Identical.** The set bonus lives in `(AC) Armor Class`, a core attribute every character uses, so the conditional must return 0 for everyone else. If base AC moved at all, back this out |
| TS13 | Check an **enemy's** behaviour in combat after the AC change | - | Unchanged. Enemies cannot equip items so the counter stays 0, but `(AC) Armor Class` is in every creature's attribute map and this is the row that proves the edit is inert for them |
| TS10 | Judge whether the placement reads | - | A battle-weary helm on a fallen Templar in a burned hamlet. If it feels like loot scattered at random rather than something left on a body, say so -- the alternative was a scripted scene rather than a corpse |

## Enemy-laid traps - caltrops from assassins and thieves

Asked in play: *"do any enemies lay traps? Is that possible?"* No, and yes.

**Traps in the shipped game are static map features** -- a `CRenderablePolygon` in **44 maps**, with a
`CTouchingPolygonTriggerAI` (`Triggered By Players=1`, everything else 0) plus a `CAISecretReveal`
that hides it behind Find Traps at `Skill Adjustment=15` and attaches a `GetCloseThen Disarm Trap`
specifier. Damage is **mojo-scaled**: 25-35 at mojo >= 16, 15-25 at >= 10, else 10-20. Nothing places
one at runtime.

**But 32 monster cans already carry trap machinery**, which was the surprise. The 18 **WarGolems** and
14 **Undead** (`Disedira`, `Festering Undead Walk`, `Second Guardian`) each have a
`CTouchingOvalTriggerAI` as an activity **on themselves** -- `X Radius=125`, `Triggered By Players=1`,
spawning a Fire Circle on entry and doing 1-2 damage every 2 seconds while the player stands in it. A
proximity hazard tied to an enemy is shipped, working behaviour; it just walks around with the golem
instead of being left behind.

(The first survey here reported all 478 cans carrying trap machinery. False positive: `Trap` matches
`Wolf Trapper Perk Checker`, which every can's attribute map lists. Third over-broad pattern of this
kind -- see also the healing one in the 0.33.0 section.)

### Everything needed was already shipping

| piece | where vanilla already uses it |
|---|---|
| spawn an entity at my own feet | `CCreateEntityFromCanAction{New Location=$Trigger}`, **73 uses** |
| the trap's trigger | `CTouchingOvalTriggerAI`, already on 32 enemy cans |
| the damage | `CActionDoDamage` + `CXRPGDamage`, mojo-scaled, as in every map trap |
| fire once per enemy | the `CSeriesAction` one-shot, as the Priest's shield and 0.34.0's draughts |
| clean up afterwards | `CDeleteAction`, how vanilla's spawned pickups remove themselves |

### The two questions that had to be answered first

**Can it hurt other enemies, or the player's companions?** **No.** The map trap and the golem aura use
an identical pattern -- `Triggered By Players=1` with `Anything`, `Player Friends`, `Enemies`,
`Projectiles` and `Companions` all **0** -- so `Character To Damage=$instigator` can only ever resolve
to the player. Copied field for field, and confirmed in the deployed bytes as `(0, 1, 0, 0, 0)`.

**Does it survive its creator, and does it clean up?** Spawned entities are independent of their
creator, and vanilla's spawnable pickup can uses `CDeleteAction` to remove itself after use. This one
is `Trigger Only Once=1` and then deletes itself -- with the delete placed **last**, because an action
after a `CDeleteAction` never runs.

### What was built

`Resources/Common Objects and Scripts/Fixt Caltrops Entity.can` -- cloned from vanilla's spawnable
spirit-pickup can so it carries every field the engine writes, with the template's 32KB mana
specifier replaced by the trigger above. **Radius 55**, `Piercing` damage on vanilla's own three mojo
tiers but at about half a map trap's numbers, because these are improvised and a fight can hold
several:

| player mojo | caltrops | a map trap, for comparison |
|---|---|---|
| >= 16 | 12-18 | 25-35 |
| >= 10 | 8-12 | 15-25 |
| below | 5-9 | 10-20 |

**48 cans lay one**, each exactly once, from their previously empty `Damaged Script Action`: **12
assassins** (`Assasin`, `Bow`, `Zealot`, `Master`, each in three tiers) and **36 thieves** (the
`Thugs/Theif` and `Sewers/Sewer Theif` ladders). Laid on **first being hurt** rather than on engage,
which is better flavour -- a thief scattering caltrops to cover itself -- and keeps the unknowns down,
since no health gate is involved.

**The patch is visible** and deliberately does *not* use `CAISecretReveal`. A dedicated map trap you
must find with Find Traps is fair because it was laid in advance; one dropped mid-fight that you
cannot see would only be a damage tax. Visible is what makes **position** matter, which is the whole
point: the healer made target priority matter, this makes ground matter.

**A balance concern, raised once.** Forty-eight layers means a crowded sewer fight could produce five
or six patches. Each is one-shot, small and self-deleting, so it should self-limit -- but `CT9` is the
row that will say otherwise, and the dials are the radius and the damage rather than the number of
layers.

| # | Step | Say | Expect |
|---|---|---|---|
| CT1 | **The row this exists for.** Fight a thief or assassin, wound it once, then watch the ground | - | A **visible patch appears at its feet**. Walk into it: you take Piercing damage and the patch disappears. Nothing in Lionheart has ever had an enemy place a hazard before |
| CT2 | Wound the same enemy repeatedly | - | **One patch only.** If it scatters caltrops every time it is hit, the `CSeriesAction` one-shot is not holding and this needs rethinking -- the same failure `PO2` watches for |
| CT3 | **The safety row.** Lure *other enemies* across a patch | - | **They are unharmed.** Only `Triggered By Players` is set. If an enemy triggers it, the trigger flags are wrong |
| CT4 | Take a **companion** across a patch | - | **Unharmed.** Companions and player friends are both 0. This matters more than CT3 -- a trap that kills Fernand would be a serious fault |
| CT5 | Walk around a patch rather than through it | - | **Nothing happens.** It is avoidable, and that is the design -- if patches land where you cannot avoid them, say where |
| CT6 | Kill the layer, then walk into its patch | - | The patch **still works**. It is an independent entity, not tied to its creator's life |
| CT7 | Leave a patch untriggered and fight on for a while | - | It stays until walked on. It only removes itself after firing, so an unused patch persists for the fight |
| CT8 | Leave the map with patches still on the ground, then come back | - | Whatever the engine does with the save snapshot. Not a designed behaviour, just worth knowing -- report what you see rather than judging it |
| CT9 | **The balance row.** A crowded fight: the Thieves Congregation, or a sewer room with five thieves | - | Five patches at most, one each. Judge whether the floor becomes unmanageable. The dials are radius 55 and the damage, not the number of layers |
| CT10 | Compare the damage against a real map trap in the Crypt or Alamut | - | The caltrops should hurt **noticeably less** -- about half -- and scale with your mojo the same way |
| CT11 | Try **Find Traps** near a patch | - | **Nothing to find.** These are visible by design and carry no `CAISecretReveal`. If that reads as a missed opportunity rather than a kindness, say so -- the machinery exists and could be added |
| CT12 | Try to **disarm** a patch | - | **Not offered.** Same reason. The map traps' disarm specifier was deliberately not copied |
| CT13 | **The regression row.** Listen to the thieves while fighting them | - | Barks intact on all 36 thief cans. The assassins never had any, which is why 12 of the 48 are silent and that is not a fault |
| CT14 | Watch an assassin's attacks after it lays a patch | - | **Unchanged.** The hurt slot was empty on all 48 and nothing else in any can was touched |

## Potion mimics - the veterans carry one draught each

Asked in play: *"can we give enemies a skill they can only use once to mimic an item?"* Yes, and
vanilla already ships one -- the Priest's shield. Two things had to be settled before building on it.

**Can a one-shot be gated on health?** Yes. There is no health-test *action* in the game --
`CCheckHealthAction`, `CIsHurtAction`, `CVariableHealth`, `CCheckHitPointsAction` are all **zero
files** -- but **`CExpressionHealthPercent`** exists and is used **33 times**, including by the
`Die Hard`, `Adrenaline Rush`, `Grace Under Fire` and `Displacement` perks and by the Jafar duel,
always in one shape: a `CExpressionAction` wrapping
`CIsLessThanOrEqual{CExpressionHealthPercent, CConstant}`. Separately, `(HP) Hit Points` gives the
**maximum** and `CExpressionHitPointsRemaining` the **current** -- vanilla subtracts one from the
other to heal to full in the Gate District, which is how the two were told apart.

**Does one-shot mean once per spawn?** Yes. `CSeriesAction` advances one item per execution and
`When Done=Repeat Last Action` then loops the final item -- that is how the Priest shields itself once
and attacks forever, and how a Mana Tome walks down six declining grants. The index is per
**instance**, not per can: `Next Action Index`, `Executed Action`, `Number Of Times Triggered` and
`Has Triggered At Least Once` are all written into the template as zeroed mutable counters, and if the
index were shared then only the very first Priest in the game would ever shield.

### How it is wired, and one structure that was rejected

The obvious build puts the health test *inside* the series as a `CIfAction` with
`Return failure if the If failes=1`, so a failed test does not advance it. **That value has zero uses
in vanilla** -- all **2,526** are `=0` -- so it was avoided rather than trusted.

Instead the test sits *outside* the series. The series only ever executes when the soldier is already
low, so its first execution is the drink and every execution afterwards lands on an inert
`CSucceedAction`. Identical semantics, and every field value used is one vanilla exercises.

It goes in **`Damaged Script Action`**, which was empty on all twelve cans -- a free hook that fires
when the soldier is hurt. The draught restores **35% of the soldier's own maximum**, which self-scales
across the family rather than needing a number per can, and fires at or below **40%** health. A
`Divine Strength` effect plays so the player can see it happen.

| can | max HP | drinks at | restores |
|---|---|---|---|
| `Soldier3` | 100 | 40 | 35 |
| `Soldier3 Tough` | 123 | 49 | 43 |
| `Soldier3 Super` | 148 | 59 | 52 |
| `Soldier4` / `Soldier4 Mace` | 147 | 59 | 51 |
| `Soldier4 Tough` / `Mace Tough` | 173 | 69 | 61 |
| `Soldier4 Super` / `Mace Super` | 206 | 82 | 72 |
| `Soldier4 Bow` | 115 | 46 | 40 |
| `Soldier4 Bow Tough` | 137 | 55 | 48 |
| `Soldier4 Bow Super` | 168 | 67 | 59 |

**`Soldier1` and `Soldier2` are deliberately excluded** -- twelve cans, byte-identical to what they
were. Only the veteran tiers carry a draught, which is also the in-fiction reason: a conscript does
not have one.

These cans are **shared with act 3 Montaillou and act 7**, so unlike 0.32.0's mana this is not
act-6-only. That is intended here.

**A mistake worth recording.** The first build of this sourced each can from the **vanilla** archive
rather than through `lhbuild.read()`, which prefers `files/`. All twelve were already Fixt overrides
carrying 13 bark references and an attack bank from the bark release, and all of it was destroyed --
**and Gate 0 passed**, because the result was still structurally valid. It was caught only because
regenerating `mod.json`'s file list reported *"added: 0"* when twelve additions were expected. The
files were restored from `HEAD` and the build now asserts that the bark count is unchanged and that
the only textual difference is the hurt slot itself.

| # | Step | Say | Expect |
|---|---|---|---|
| PO1 | **The row this exists for.** Fight a `Soldier4 Super` (act 6 sieges, act 3 Montaillou, act 7). Take it below **40%** health without killing it | - | It **heals once**, about **72 HP**, with a visible `Divine Strength` flash. Then never again, however long the fight runs |
| PO2 | Keep fighting the same soldier after it has drunk | - | **No second draught.** One per soldier, per spawn. If it drinks repeatedly, `CSeriesAction`'s index is not per-instance and this whole mechanism needs rethinking -- report it immediately |
| PO3 | Hit a soldier **once** for light damage, well above 40% | - | **Nothing.** It does not waste the draught on a scratch. This is the half that the health gate buys, and the reason the potion is not simply in series position |
| PO4 | Kill a fresh `Soldier4 Super` in one burst from full health | - | **No heal at all.** It never got below 40% while alive, so the draught is never drunk -- burst damage beats it, which is the intended counterplay |
| PO5 | Fight a **`Soldier1`** or **`Soldier2`** of any variant | - | **No draught.** Only the Soldier3 and Soldier4 tiers carry one |
| PO6 | Fight each of the twelve: `Soldier3` ×3, `Soldier4` ×3, `Soldier4 Bow` ×3, `Soldier4 Mace` ×3 | - | All drink, scaled to their own maximum -- 35 at the bottom of the ladder, 72 at the top |
| PO7 | **The regression row.** Listen to the veterans in a long fight | - | Their **barks still work**. The first build of this destroyed the bark bank on all twelve cans; they were restored, but this is the row that proves it in play rather than in a diff |
| PO8 | Watch a soldier's attacks after it drinks | - | **Unchanged.** The draught is in `Damaged Script Action`; the attack bank in `Shoot Completed` was not touched, and `Skill to select` counts are identical to before |
| PO9 | Judge whether it changes the fight | - | A veteran should feel like it has **one more round in it** than before, not like a different enemy. If a `Soldier4 Super` now feels spongy, the dial is the 35% fraction or the 40% threshold -- say which direction |
| PO10 | Fight a **mixed group**: a Priest plus veteran soldiers | - | The Priest heals them *and* they drink their own draught. That stacking is intended but has never been seen -- if it makes a group unkillable, this is the row that will say so |
| PO11 | Check the drops after killing one | - | **Unchanged.** No drop table was touched; the veterans still drop no spirit energy, which is a separate note in the act 6 section |
| PO12 | Look for the effect being visible | - | A `Divine Strength` flash at the soldier, with sound. If the heal happens invisibly the mechanic is unreadable and the effect needs changing -- it matters that the player can tell a potion was drunk |

## The first enemy healer in the game

Asked in play: *"are there any enemy healers? I've never seen that."* There are none, and the
measurement is exhaustive rather than a spot check. Across all **478** vanilla monster cans, the
complete set of skills any enemy ever selects is ten entries:

| skill | cans | | skill | cans |
|---|---|---|---|---|
| `Fighting/OneHandedMelee` | 104 | | `…/Ice Javelin` | 13 |
| `Magic Thought/Offensive/Lightning Bolt` | 42 | | `…/Ice Missile` | 11 |
| `…/Spike` | 37 | | **`Defensive/ENEMY Magical Shield`** | **3** |
| `…/Fire Orb` | 28 | | **`Defensive/Magical Shield`** | **3** |
| `…/Static Charge` | 26 | | `Magic Divine/Offensive/Celestial Smite` | 2 |

Eight are damage. Two are a defensive buff. Nothing heals, nothing cures, nothing summons a medic.
(An earlier pass of this survey reported all 478 cans referencing healing; that was an over-broad
match on enemy **drop tables** carrying `Potion Mass Healing`. Dropping a healing potion is not
casting one.)

### Why there were none, and it is one line

`Magic Divine/Defensive/Healing` is blocked from enemies two separate ways:

1. A single `CCheckCategoryAction` on `Target Name=$Trigger` checking **`Player,Player Friend`**. The
   skill's area oval actually carries `Trigger Anything=1`, so it catches *everyone* in radius -- that
   category test is the only thing deciding who gets healed.
2. Its magnitude reads `CVariableSkill` on the **caster's own** Healing value, with *output 0 if input
   is below input base*. An enemy has no Healing skill, so even ungated it would heal **zero**.

### Vanilla already ships the recipe

Diffing `Magic Thought/Defensive/Magical Shield` against `ENEMY Magical Shield` -- the only
enemy-variant spell in the game -- gives the exact transformation in five parts: drop the *Player has
cast a spell* bookkeeping modifier, flip the oval's `Trigger if Player` / `Trigger if Enemy` flags,
drop a `CIfAction` gating on category `Player`, reparent to an unlistable parent with `Image=!None`
and a zeroed initial range, and add an **always-false** `Display and Cast Requirement` (`0 == 1`) so
the player can never see or cast it. The English Priest then carries it by a **race preset of 150**,
while its can lists the skill at `0` like every other can in the game.

`Skills/Magic Divine/Defensive/ENEMY Healing` follows that recipe, with **one deliberate departure**:
`ENEMY Magical Shield` left its magnitude expressions pointing at the *player* skill's name, so on a
Priest those read 0 and the preset's only real job is making the skill selectable. All **13**
self-references here are repointed to `ENEMY Healing` instead, so the 150 preset is what the heal
actually scales from -- about **11-18 HP** per trigger, and the oval's `Max Times To Trigger=2`.

### What carries it

The Priest's `Shoot Completed` was already the mechanism this project has been looking for, and it is
vanilla: shield itself **once**, then a `CRandomAction` over three offensive spells which
`When Done=Repeat Last Action` repeats forever. The heal is a **fourth entry in that random bank**, so
roughly one cast in four is a heal.

**All three English Priest tiers carry it**, on vanilla's own ladder for these cans: `ENEMY Magical
Shield` is preset 150 / 200 / 250 across `Priest` / `Tough` / `Super`, so the heal matches it exactly.
With `MinHeal` base 3 step 17 and `MaxHeal` base 6 step 24 over an input range of 1 to 300, that is
about **11-18**, **14-22** and **17-26 HP** per trigger.

The base tier shipped alone in 0.33.0 so one can could prove the mechanism first; the other two were
added at the request of the person playing it, **before `EH5` or `EH1` had been played**. That is a
deliberate trade and it widens the untested surface from one can to three -- if `EH5` fails, three
cans and a skill come back out rather than one.

Three priests are deliberately **not** included. `Priest Near Death` selects no skill at all and is a
scripted one-off rather than a tier. The **Nostradamus Priest trio** is a separate can family in act 5
that casts the plain `Magical Shield` rather than the ENEMY variant and rotates six selections instead
of four, so it needs its own pass. And the **Priestess** line is a different line -- it was given four
offensive spells earlier and never had a shield.

**The heal radius is a flat 200.** Of the 24 Priest generators in the game, **17 sit within 200 of a
soldier or golem generator** (median 135) -- Crossroads to England at 40, Gate District Siege at 57,
Temple District at 84, Hamlet Burned at 119. In the other 7 the Priest can only reach itself.

**The one unverified assumption.** This is the **93rd** `.Skill` file in a game that shipped 92, and
every character can carries a `Skill Values` map enumerating all 92. That map declares **no
`Item Count`** -- it is a keyed map, like `Tree List=CSortList2D` -- so a missing key should simply
default to 0, which is what every can already holds for every skill it does not use. That reasoning is
why `EH5` exists and why it is the row to run first if anything behaves oddly.

| # | Step | Say | Expect |
|---|---|---|---|
| EH5 | **Run this before the rest.** Start a new game and play any ordinary fight -- thugs in the Port District will do | - | **Everything normal.** Adding a 93rd skill to a 92-skill game is the one structural risk here. If enemies behave strangely, spells misfire, or the game will not load, this is the cause and the whole feature comes back out |
| EH1 | **The row the feature exists for.** `Gate District Siege` or `Temple District Siege`, a fight with a **Priest and soldiers together**. Wound a soldier, do not kill it, and watch the Priest | - | The soldier's health **goes back up**. This is the first time anything in Lionheart has healed an enemy, and it is the one thing that cannot be proved statically |
| EH2 | Fight a Priest **alone** and wound it | - | It heals **itself** -- the Priest is `Category=Enemy` like everything else, so it is inside its own oval |
| EH3 | **The safety row.** Cast your own **Healing** on yourself with enemies nearby | - | It heals **you and your friends only**, exactly as before. The vanilla `Healing.Skill` was not touched and is still gated to `Player,Player Friend`. If your heal is now topping up enemies, stop and report immediately |
| EH4 | Open your skill tree and look under Magic Divine / Defensive | - | **No `ENEMY Healing` anywhere**, not castable, not listed, no icon. It is reparented under Fake Wand Spells with `Image=!None` and an always-false display requirement |
| EH6 | Watch a Priest over a long fight and count | - | Roughly **one cast in four** is a heal; the other three are Fire Orb, Spike or Lightning Bolt. If healing feels relentless, the bank weighting is the dial -- say so rather than guessing a number |
| EH7 | **Does it change how you fight?** Take the same Priest-and-soldiers fight twice: once ignoring the Priest, once killing it first | - | Killing the Priest first should be **noticeably better**. That is target priority, and it is the entire point -- the first thing in this game that makes *your* behaviour change rather than the enemy's |
| EH8 | Judge the magnitude: about **11-18 HP** per trigger, up to twice per cast | - | Enough to matter, not enough to make a soldier unkillable. If it out-paces your damage, the race preset of 150 is the dial |
| EH9 | `Crossroads Siege` -- where the nearest soldier generator is **308** away, beyond the radius | - | The Priest heals **only itself**. Expected, not a bug: 7 of the 24 Priest placements are out of reach of anyone else |
| EH10 | Act 3 `02 Hamlet Burned` and the act 7 shrine chambers, which also place Priests | - | Same behaviour. The can is shared, so this is not act-6-only -- unlike the mana change in the same release |
| EH11 | Kill a Priest and check the drops | - | **Unchanged.** `English Priest Drop Action` was not touched; it carries no spirit energy, which is a separate note in the act 6 section |
| EH12 | Fight **`Priest Tough`**, then **`Priest Super`** | - | Both heal, and **harder**: presets 200 and 250 against the base tier's 150, so roughly **14-22** and **17-26 HP** per trigger. If a Super Priest out-heals your damage outright, that is the row to report and the preset is the dial |
| EH13 | Compare the three tiers side by side if you can | - | The heal should scale with the tier the same way their shield already does -- the presets are copied from `ENEMY Magical Shield`'s own 150/200/250 ladder on these exact cans, not chosen freshly |
| EH14 | Fight **`Priest Near Death`** | - | **No healing.** It selects no skill at all in vanilla and is a scripted one-off, so it was left alone |
| EH15 | Fight the **Nostradamus Priests** in act 5 (`English in Caverns of Nostrodomus`) | - | **No healing.** A separate can family that casts the plain `Magical Shield` and rotates six selections rather than four; it needs its own pass rather than the same edit |

## Act 6 - the siege had no mana in it

Reported by a player: *"mag builds suffer from lack of mana during war with England and later on in
the game. Possibly add more mana in cavern of Nostradamus and crypt?"*

**The report is right about the war and wrong about the other two**, and measuring it says why. Mana
reaches the player two ways -- `Spirit N Generator` founts placed in a map, and spirit energy dropped
on death -- and every act in the game is generous in one of them:

| | founts | placed mana | tomes | drop rate |
|---|---|---|---|---|
| act 4 Crypt | 171 | 9,733 | - | **94%** |
| act 5 Nostradamus | 122 | 6,895 | - | **97%** |
| act 7 English Shrine | 46 | 3,419 | **4,909** | 19% |
| act 8 Alamut | 183 | 14,207 | - | 73% |
| **act 6 war with England** | **64** | **4,156** | - | **10%** |

The Crypt and Nostradamus are the two **highest** drop-rate acts in the game. Their thin fount
placement is a deliberate trade -- the mana comes from kills instead -- so adding founts there would
re-solve a solved problem. Act 7 looked like the worst in the game on placement alone until the
**Mana Tomes** were counted: ten of them, only in the shrine, a mechanic that exists nowhere else.
Each is `Trigger Only Once=0` over a `CSeriesAction` of declining grants (125-150, then 75-100, 50-75,
25-50, 20-30) whose sixth item is a balloon with **no mana** (`Node ID=03 Empty`), and `When Done=
Repeat Last Action` repeats *that* -- so a tome is a canteen, not a font, worth 170-905 each and
**4,909 for the act**. That more than doubles act 7 and settles it.

**Act 6 is the only act at the bottom of both axes at once**, and within it the starvation is almost
entirely two maps:

| act 6 map | spawns | founts before | mana before | per spawn |
|---|---|---|---|---|
| **Crossroads Siege** | 427 | 14 | 897 | **2.10** |
| **Crossroads to England map** | 79 | 1 | 95 | **1.20** |
| Gate District Siege | 149 | 19 | 1,077 | 7.23 |
| Temple District Siege | 154 | 30 | 2,087 | 13.55 |

Crossroads Siege carries **40% of the act's enemies on 14 founts.** Gate District and Temple District
are already healthy and were **not touched**; `7.23` -- Gate District's own ratio, an in-act reference
rather than an invented target -- is what the two Crossroads maps were brought to:

| | founts | mana | per spawn |
|---|---|---|---|
| Crossroads Siege | 14 -> **43** | 897 -> **3,061** | 2.10 -> **7.17** |
| Crossroads to England map | 1 -> **8** | 95 -> **551** | 1.20 -> **6.97** |

**Why founts and not drops.** The other axis is where the real oversight looks to be. Of the 50
`Monster Cans/English Enemies` cans, the split is exact:

| | spirit drop |
|---|---|
| 19 **WarGolem** cans | `5Huge Spirit Charge Drop Action` -- **174**, the largest charge in the game |
| 6 **Priest / Priestess** cans | `4Large Spirit Charge Drop Action` -- 95 |
| **24 Soldier** cans (+ `Priest Near Death`) | **none at all** |

So the English were not designed dry -- their golems drop the biggest charge in the game and their
priests the second biggest. The **soldiers specifically were skipped**, and the soldiers are the bulk
of the siege, which is the whole of act 6's 10% drop rate. Vanilla even ships the mechanism to fix it:
`Chance 1 in 2 Small2 Spirit Charge Drop Action.can` and `Chance 1 in 3 XtraSmall1 Spirit Drop
Action.can`.

It was **rejected on scope**, not on merit: of the 52 monster cans act 6 spawns, **not one is exclusive
to act 6.** Every English can is shared with act 3 Montaillou and act 7, so a drop-table edit cannot
be confined to the siege -- it would land in an act deliberately left alone and in the act the tomes
already fix. Map founts are the only lever that is act-6-only. **If a wider pass is ever wanted, the
24 soldier cans are the better repair** and this is the note that says why.

Each new fount is templated from the **verbatim vanilla fount block**, so it carries every field
vanilla writes, and each is placed **inside an enemy generator's own oval** -- walkable by
construction, because the engine spawns enemies across that area. Vanilla itself puts founts as close
as 6 units to a spawn point in these maps; the new ones run 0-134, well inside that. The edit is
provably additive: every original byte of both maps is unchanged.

| # | Where | Steps | Pass |
|---|---|---|---|
| MN1 | **Crossroads Siege**, as a mage, on a save that has **never entered act 6** | Fight the siege normally and do not go out of your way to hunt pickups | You run dry **noticeably less** than before. This is the row the whole change exists for, and it is a feel question -- report whether it still runs out, not whether you saw the orbs |
| MN2 | The same map, same character | Count roughly how often a spirit orb is within reach of a fight | Mana now appears **where the fighting is**, because every new fount sits inside an enemy spawn area. If orbs feel like they are in empty ground instead, say so |
| MN3 | **Crossroads to England map** | Walk it end to end | Eight founts rather than one. This map had the worst ratio in the act at 1.2 mana per spawn |
| MN4 | **Gate District Siege** | Play it | **Unchanged.** 19 founts, 1,077 mana. If this map feels different, something leaked and the change is wrong |
| MN5 | **Temple District Siege** | Play it | **Unchanged.** 30 founts, 2,087 mana. Same test as MN4 |
| MN6 | Any new orb | Walk over it | It is picked up and credits mana like any other. The blocks are copies of vanilla's own fount, so a difference here means the template is wrong |
| MN7 | Watch for an orb inside a wall or on unreachable ground | - | None. Placement is inside generator ovals only, but *walkable is not reachable* -- if one is stranded behind geometry, report the map and roughly where |
| MN8 | Two orbs stacked on the same spot | - | None. All 36 positions are distinct and checked against the existing founts |
| MN9 | A **melee** character through Crossroads Siege | - | No worse than before. Nothing was removed and no enemy changed; the only risk is orbs cluttering a fight visually |
| MN10 | **Act 3 Montaillou** and **act 7 English Shrine** | Play any English fight | **Unchanged.** No can was edited, so no drop behaviour anywhere in the game moved |
| MN11 | **Act 7**, find a Mana Tome and use it repeatedly | - | Declining grants, then an *"empty"* balloon forever. This is vanilla behaviour, measured but **not modified** -- confirm it matches the description above |
| MN12 | A save that **had already entered** Crossroads Siege before installing | - | The new founts are **absent**, by engine design: a map's entity list is baked into the save on first visit. This is expected, not a bug, and is why MN1 specifies a fresh save |

**What was deliberately not done.** Act 3 Montaillou measures 7.6 mana per kill at an 11% drop rate,
worse on drops than the act that was reported -- but that figure counts generator groups only and
excludes individually placed named enemies, so the number is not trusted and nobody has reported it.
It is left alone. Act 6's **health** pickups are also worth a look some day: all four siege maps carry
**zero** `Health N Generate Action` founts, which is its own anomaly and outside what was asked for
here.

## 0.31.0 / 0.31.1 - Butu Khan's heir takes the Ravine Cave

`Mongol Goblin Hat Super` was **placed nowhere in the game**, and its race is the toughest goblin
statline there is -- **250 HP, AC 225, harder than the Khan himself**. The hat line steps 60 -> 80 ->
250 where every other goblin ladder steps about 1.25x, so it was never a third tier: it is a boss
statline filed under hats, which vanilla lent to `Mongol Goblin Khan` for its numbers until 0.30.1
gave that can a race of its own.

And vanilla names a second Khan, exactly once, in a flavour line on an item:

> *"Collected by **Butu Khan**, this book of poetry contains many free verses of Goblin Poetry."*

The `Butu Khan Poetry Book` sits in the **Goblin Warrens**, in Plumjum Khan's own cave, and
`WengChoi.DialogTree` buys it as a rare book without anyone saying whose it was. So a second goblin
dynasty exists in the fiction, and its Khan's book is a curio on the floor of the goblin who outlasted
him.

**After Montserrat, Ravine Cave East belongs to Butu's heir.** Act 1 is untouched.

| | |
|---|---|
| gate | `CWasQuestEverActivatedAction` OR'd over the three Montserrat quests `Brother Montgomerie` hands out -- `Calle Perdida.zax` already uses that class on one of them as a progression gate |
| the flip | entry trigger at the `Start Here` spawn (1364, 1721), once: deactivate `Khan Goblins` and `Goblin Cave Post`, delete them and the three arguers, activate 8 Butu posts and Hrargrub |
| precedent | the deactivate-and-delete swap is at **101 sites**, e.g. `Calle Perdida`'s *"RESET MAP for Invulnerable Cedric"* |
| the tribe | **24 of capacity** plus the heir, recoloured `07 Red` -- of the engine's 17 hue palettes, **16 are used nowhere** in vanilla |
| the heir | `Characters/Monsters/Mongol Goblin King`, which belongs only to the Warrens Khan and the Rumjun Khan. He already looks like a Khan, which is the argument he is making |
| where he stands | the furthest post from the entrance, **(2319, 748)**, about 1360 units in |

**The snapshot rule cuts the wrong way here and must be said out loud.** New map entities only exist
for a save that had **not** entered `Ravine Cave East` when the mod was installed. The players most
likely to walk back in are exactly the ones who were there in act 1, so anyone installing
mid-playthrough after visiting East gets none of this.

| # | Step | Say | Expect |
|---|---|---|---|
| BU1 | **Act 1**, fresh `Ravine Cave East` entered from `Scar Ravine`. Fight through it | - | **Exactly as 0.30.0 and 0.30.1 left it** -- the Khan's goblins, four `Goblin Cave Post` hat posts, the officer alarm, the three-goblin argument. No red goblins, no Hrargrub |
| BU2 | Reach Montserrat and talk to **Brother Montgomerie**, then return to `Ravine Cave East` | - | The cave is **Butu's**. Red goblins at the four post positions, and nothing of the Khan's left alive or spawning |
| BU3 | Count what is there | - | About **24 of capacity** plus the heir, so a shorter fight than act 1's 93 -- the point is that it changed hands, not that it got bigger |
| BU4 | Look at them | - | **Visibly a different tribe.** `07 Red`. If they read as ordinary goblins in the cave's lighting, say so -- `11 Black` and `08 Purple` are the alternatives |
| BU5 | Walk to the far end, **(2319, 748)** | - | **Hrargrub**, on the Goblin King model, and he **talks instead of attacking**. 250 HP / AC 225 if it goes wrong |
| BU6 | Read what he calls himself in the log if you fight him | - | **Hrargrub**, from his own race. His tribe log as *Butu Officer*, *Butu Archer*, *Butu Goblin* |
| BU7 | Re-enter the cave again after the takeover | - | Still Butu's. `Trigger Only Once=1` on both the trigger and the relay |

### What he says depends on what you did about the Khan

| # | Step | Say | Expect |
|---|---|---|---|
| BU8 | Arrive having **killed Plumjum Khan** | *"Plumjum Khan is dead. I killed him."* | `20 you emptied the chair` -- *"You emptied the chair. I am standing in it. I had six winters of reasons and you did it in an afternoon"* |
| BU9 | Arrive as the Khan's **Champion** (`Goblin Rank` 3) | *"I am the Khan's Champion."* | `30 take off his mark`. He offers the choice; **refusing fights him**, and so does choosing the fight reply |
| BU10 | Arrive at **rank 1 or 2** | *"The Khan gave me a rank."* | `40 he gives everyone ranks` -- *"He gives ranks the way he gives speeches, and both cost him nothing. Butu gave his goblins poems."* |
| BU11 | Arrive having completed **`Rid the Dryad's Forest of the Goblins`** | *"I have been killing his goblins for weeks."* | `50 a qualification` -- *"I am not fond of you. I am extremely interested in you."* |
| BU12 | Arrive with **no goblin history at all** | *"Who was Butu?"* | `60 who was butu`, and the line the whole scene is built on: *"He has drawn plans for six winters. Have you seen the plans? They are very good plans."* |
| BU13 | All five routes | - | Each leads to `90 the book`. Five entry reads, two of them quest tests in `Custom Requirement=` and two from Fixt's `Goblin Horde *` cans |

### The book

| # | Step | Say | Expect |
|---|---|---|---|
| BU14 | At `90 the book`, **without** the poetry book | *"I will find it."* | `95 agreed`. He does not stand the cave down yet |
| BU15 | Get the `Butu Khan Poetry Book` from the **Goblin Warrens** and bring it back | *"I have it here."* | `100 the book returned` -- *"He takes it in both hands, and does not open it."* The book leaves your inventory, XP, and the cave stands down |
| BU16 | **If the book is already gone**, tell him so | - | **You cannot buy it back** -- an earlier draft of this row said you could, and that was wrong. The turn-in removes the item, Weng Choi's two merchant inventories hold **no books at all**, and the Goblin Warrens copy is the only one placed in the game. So the errand would have been unwinnable; `BU38`-`BU40` are the two routes that close it |
| BU17 | After the handover, walk the cave | - | The red goblins **do not attack**. `Butu alliance` clears targeting and drops `Enemy` on `Butu Warriors` |
| BU18 | Open the journal after `95 agreed` | - | **`Butu Khan's Poems`** is listed. An earlier draft of this section said there would be no journal entry and that a tracked quest was out of scope -- wrong on both counts, since Fixt has authored fourteen `.Quest.txt` definitions already |

### Two quests, and they fork

The feature was a boss fight with one untracked errand until this was added. Both ends now pay, and
they are mutually exclusive.

| quest | states | |
|---|---|---|
| **`Butu Khan's Poems`** | `BTU4K7ZQ` -> `BTU8M3XV` | the heir's errand. Return the poems and the cave stands down |
| **`The Goblin of Butu's Line`** | `BTU5P9HK` -> `BTU2W6RJ` | Plumjum's contract. Kill the heir and **Goblin Rank advances** |

| # | Step | Say | Expect |
|---|---|---|---|
| BU29 | Accept the heir's errand, then check the journal | *"I will find it."* | **`Butu Khan's Poems`** at its first state -- *"His Khan's book of poems is somewhere in Plumjum Khan's warren, where it is being kept as shiny."* |
| BU30 | Return the book | *"I have it here."* | The quest **completes** -- *"You put Butu Khan's poems back in the hands of his line."* The book leaves your inventory, and the red goblins stand down |
| BU31 | Arrive already **holding** the book, having never taken the errand | *"I have it here."* | It still appears in the journal **and then completes**, rather than completing something that was never listed. Both states fire in order on that path deliberately |
| BU32 | Take the Khan's contract | *"It will be done, Great Khan."* | **`The Goblin of Butu's Line`** opens -- *"The Khan wants him dead and does not want to hear his name."* |
| BU33 | Kill Hrargrub **with the contract taken** | - | The quest completes, and **`Goblin Rank` advances** -- invoked through `Advance Goblin Rank` with `CUseCannedActionAction`, the way the Khan's own tree already invokes it. Check the perk and faction actually changed |
| BU34 | Kill Hrargrub **without** ever taking the contract | - | **No quest completes and no rank is given.** The death hook is guarded on `CWasQuestEverActivatedAction`, so killing him on your own account pays nothing |
| BU35 | After killing him on the contract, go back to the Khan | *"The east rock is yours again. I will not say the name."* | `382 you did not say it` -- *"Then there was never anybody there, and I never sent anybody east, and you have gone up in the world for doing nothing at all. That is how it works, morsel."* |
| BU36 | Try to do **both** | - | You cannot. Returning the poems stands the cave down and shuts the act 8 gate; killing him closes the other. Confirm neither route leaves the other's quest stuck open in the journal |
| BU37 | Check the heir's death hook was not overridden | - | His `Destroyed Script Action` is the one slot that was free on his can, and **no generator sets `CSetDestroyedScriptActionAction` over it** -- the trap that made the Lava Troll Hide dead code from 0.10.0. Gate 0's A0.14 guards it, but a kill confirms it |

### Where the poems went, and why a collector is not a buyer

The errand could become unwinnable, and the ordering made that likely rather than unlikely: Weng
Choi's rare-books job is an act 1 Gate District errand, and Hrargrub does not exist until after
Montserrat. Measured rather than assumed -- the turn-in runs `CActionRemoveInventoryItem` and pays
250, Weng Choi's merchant inventories hold **6 and 18 items and no books**, and the Warrens copy is
the only placement in the game.

Vanilla already draws the distinction the scene needed. The quest is called **`Complete Weng Choi's
Book Collection`** and its own text calls him *"an avid collector of unique tomes"* -- so giving a
dead Khan's poems to a collector is not the same act as selling them by weight, and the heir cares
which.

| # | Step | Say | Expect |
|---|---|---|---|
| BU38 | Turn the book in to **Weng Choi** in act 1, then meet Hrargrub and tell him | *"I gave them to a collector in the city. He keeps rare books, and he will read it."* | `101 the collector` -- *"A human who keeps words he cannot eat... Then Butu is read in a city that never heard of him, which is further than Plumjum has ever carried anything."* The cave stands down and the errand **completes**. Gated on that quest, so the reply only exists if it is true |
| BU39 | On a character who never dealt with Weng Choi, look for that reply | - | **Not offered.** The player cannot claim the collector without having used him |
| BU40 | Tell him you sold them | *"I sold them."* | `102 the price of poems` -- he puts his hand out and **takes 250**, the exact figure vanilla pays for it, with `CTakeMoneyAction`. *"I did not pick the number. A human did, and you took it."* The errand still completes; the insult is the price, not a refusal |
| BU41 | Do BU40 with **less than 250 gold** | - | He deals anyway. The take is wrapped in `CHasMoneyAction`, so a poor player is not softlocked out of the alliance -- confirm no money goes negative |
| BU42 | Across all three routes -- returned, collector, sold | - | **Three ways to close `Butu Khan's Poems` and no dead end.** Returning the book is still the best of them: it is the only one where he holds it |

### The late game remembers

`01 Desert Sprawl`'s `Fixt goblin gate` already decided whether Plumjum Khan meets you in Persia and
whether **Grumdjum joins you as a companion**, on two conditions: you are his Champion, and he is
alive. It now has a third.

| # | Step | Say | Expect |
|---|---|---|---|
| BU19 | Be the Khan's **Champion**, leave him **alive**, **do not** side with Hrargrub, then reach `01 Desert Sprawl` | - | Unchanged from 0.30.0: the **Rumjun Khan appears** and **Grumdjum joins as a companion** |
| BU20 | Same run, but **hand Hrargrub the book** first | - | **Neither appears.** A mid-game choice in an optional cave costs a late-game companion. This is the row the whole feature exists for |
| BU21 | Check the marker is doing it and not something else | - | `Sided with Butu's heir` lives in `01 Desert Sprawl` itself, `Active=0`, flipped from Ravine Cave East by `COtherMapAction`. It is **not** in the Wilderness, because the expiry door closes those maps before act 8 |
| BU22 | **Open question, and it predates this build.** Kill Plumjum Khan in act 1, then reach `01 Desert Sprawl` as his Champion | - | He should **not** appear. But `Goblin Khan is Dead` lives in `Inquisition Chambers2` and `Grumdjum Dead` lives in `Lake`, and **both maps are expired** by `3 Montaillou/02 Hamlet Burned`'s `From Crypt or Nostro Portal` spawn point before act 8. If the Khan turns up in Persia anyway, those markers are being read out of expired maps and Fixt's act 8 gate has never worked |

### The Khan tells you, because otherwise nobody would

Hrargrub sits in a cave the game never sends anyone to: the Sacred Scimitar needs the silver in
**West**, East has its own entrance off `Scar Ravine`, and the halves connect only by a crystal-node
teleport. Plumjum Khan is the right source -- he is the one who loses by it -- and the node hangs off
`1 Conversation Start` and `05 Return Friends of Khan`, the same two entries 0.30.0's
`375 the khan has eaten well` uses, gated on the same three Montserrat quests that flip the cave.

| # | Step | Say | Expect |
|---|---|---|---|
| BU24 | Talk to the Khan in the Goblin Warrens **before** reaching Montserrat | - | **No mention of the east cave.** The reply is gated on the same quests as the takeover, so he never refers to something that has not happened |
| BU25 | Reach Montserrat, then talk to the Khan again | *"Someone is sitting in your east cave, and he is not one of yours."* | `380 the east rock is taken` -- *"Butu's line were nobodies when I was young and they are nobodies with a cave. He has my east rock and my shiny and he tells my goblins that I draw maps."* **He never says Hrargrub's name**, and tells you not to bring it back |
| BU26 | Take the Speech reply | *"He says you have been drawing those maps for six winters."* | `381 do not repeat that` -- *"He does not move at all, which from him is the loudest thing available."* No punishment, which is the joke |
| BU27 | Both of the Khan's entry nodes | - | The reply appears from a first conversation and from `05 Return Friends of Khan` alike |
| BU28 | Kill the Khan, then look for the pointer | - | Gone with him, as it should be. A player who killed Plumjum and never went east simply never hears about Hrargrub -- fair, and worth confirming it fails quietly rather than leaving an orphan reply |

**Pre-existing, found while adding this and not caused by it:** vanilla's own `GoblinKhan.DialogTree`
points at a node `130 the job` that **does not exist** in the tree. One dangling reply, vanilla's,
unrelated to the Khan's war campaign or to this build. Recorded for `reachability.py` rather than
patched blind.

### What expiry actually does, settled from the saves

The question was whether an expired map's entities can still answer `CCheckExistenceAction`, because
Fixt's act 8 gate reads two markers out of maps the door closes. Measured rather than guessed:

* **`Has Expired` is a per-layer flag in the save**, not a deletion -- the layer mapping and its
  `Current Temp File` stay in `CSwappedLayerFilenameMappingTable`. The engine simply refuses to touch
  it: *"Attempting to load expired map... (--Loren)"*, *"Attempting to save to expired map... This
  shouldn't happen"*.
* **Across all 65 saves in this install, exactly one map has ever been expired:**
  `Wilderness Maps/Slave Pit Exterior INTRO MOVIE.zax`, retired at the start of every game. The
  130-map block has never fired in any of them.
* The furthest-progressed save, `mountaillouinn.sav` at 78 layers, is **in Montaillou with the door
  still shut** -- and no save has ever visited `02 Hamlet Burned`, which is where it lives.
* `CCheckExistenceAction` **is** a global lookup, not map-local: vanilla does it across maps **124
  times**, for instance `Church Interior` checking `Torquemada irritated`, which is defined in
  `Inquisition Chambers2`.

So the idiom is sound and the door is narrower in practice than it looked -- but whether a *flagged*
layer still answers a lookup is still untested, which is why the new marker lives in
`01 Desert Sprawl` and `BU22` exists.

### Siding with the heir: what it costs and what it pays

0.31.0 shipped with no consequence in the horde at all -- you could be Plumjum's Champion and his
betrayer at once and he never found out.

**The Khan's two settlements turn on you.** `Make Goblins Hostile Relay` already existed in
**fourteen** goblin maps and is fired over a hundred times in vanilla, including from
`GoblinEntranceGuard`, `GoblinVillager` and `Rakeb`. The `Butu alliance` relay now throws it in the
**Goblin Warrens** and the **Mongol Camp** by `COtherMapAction`, and deliberately leaves the outlying
villages alone, because the horde is large and news travels slowly.

**The standing swaps rather than being stripped.** The goblin bonus was never a title: Fixt's own
goblin factions, modelled on vanilla's `Saladin Aswaran`, apply real modifiers through
`CPlugInBehaviorModifyCharacterWhenSelected` with `Modification is permanent=1`. An earlier build of
this release subtracted them with sixteen negative modifiers in a `Revoke Goblin Standing.can`; that
can is **gone**, because `Advance Goblin Rank` branches on `rank == 0 / 1 / 2` against factions that
set rank to an absolute 1 / 2 / 3, which only works if selecting a faction **replaces** the previous
one's contribution. The engine takes it back by itself.

**And the defection is tiered**, because Hrargrub gains more by taking the Khan's Champion than by
taking a chum -- an untiered version made betrayal a free upgrade for a rank-1 player:

| rank given up | you lose | `Join Butus Line.can` assigns | you gain |
|---|---|---|---|
| none | nothing | **Goblin Traitor - Foe** | OneHandedMelee +10 |
| Chum (1) | Sneak +10, Poison +10, Carry +10 | **Goblin Traitor - Bad Blood** | OneHandedMelee +20, Crushing +15 |
| Blooded (2) | Sneak +18, Poison +20, Carry +10, Barter +8, Disease +10 | **Goblin Traitor - Bad Blood** | OneHandedMelee +20, Crushing +15 |
| Champion (3) | Sneak +30, Poison +35, Carry +30, Barter +14, Disease +10 | **Goblin Traitor - Fallen Champion** | OneHandedMelee +35, Crushing +30, Slashing +20, Carry +20 |

| # | Step | Say | Expect |
|---|---|---|---|
| BU43 | **The row this release most needs.** As a Goblin **Champion**, write down Sneak, Barter, carry weight and poison/disease resistance. Side with Hrargrub. Read them again | - | Sneak, Barter, poison and disease should have **dropped by the Champion faction's amounts**, and melee/crushing/slashing/carry risen by the Fallen Champion's. **If the old numbers are still there on top of the new ones**, factions accumulate rather than replace, the inference this build rests on is wrong, and the revoke can has to come back. Report the actual numbers, not a yes or no |
| BU44 | Same as a **Chum** (rank 1) | - | **Goblin Traitor - Bad Blood**: melee +20, crushing +15. The poison resistance and carry weight go away entirely, so it is a different build rather than a better one |
| BU45 | Same as **Blooded** (rank 2) | - | Also Bad Blood. Ranks 1 and 2 share a tier on purpose |
| BU46 | Same having **never joined the horde** | - | **Goblin Traitor - Foe**: melee +10 and nothing else. He is taking a nobody and pays accordingly |
| BU47 | Check the perk list after any of them | - | A **Goblin Traitor** title perk, and the old goblin title **still there** -- nothing in the engine can remove a perk, and the titles carry no modifiers of their own. *"The Horde has a word for it and the word is not Champion."* |
| BU48 | Go to the **Goblin Warrens** afterwards | - | **They attack**, Khan included, so there is no conversation with him. Confirm the game does not try to open one |
| BU49 | And the **Mongol Camp** | - | Also hostile |
| BU50 | And an **outlying** village -- any `Goblin House Interior`, the vendor hut, `ShamanInterior` | - | **Still neutral**, by design. If that reads as an oversight rather than as distance, say so: each one has its own `Make Goblins Hostile Relay` and adding them is one line each |
| BU51 | Try a `Goblin Horde IS` gate elsewhere afterwards -- the Scar Ravine goblin, the Crossroads patrol | - | The rank is 0 now, so those routes are closed. **This is the leak worth watching**: the Mine Foreman is the one that matters, and the deed is why it is survivable |

### The deed, and three things to do with it

`Inventory/Specific Item Cans/Quest Items/Silver Mine Deed` is one of **twelve unique item cans the
shipped game references from nothing**: *"Legal document proscribing ownership of the Silver Mine."*

Two earlier ideas for it were **mistimed and dropped**: solving Eduardo's silver quest and opening the
mine are both act 1 problems, and the deed does not exist until after Montserrat, so for most players
they would be answers to a question already settled. Shylocke is not time-locked -- he is reachable
from act 1 until the expiry door, he holds Shakespeare's muse as collateral and sues Cortes over a
contract clause, and a mine deed is his actual trade.

| # | Step | Say | Expect |
|---|---|---|---|
| BU52 | Side with the heir by any of the three book routes, then check inventory | - | **Silver Mine Deed.** Handed over in the reply rather than the relay, because `$Instigator` only reliably resolves to the player in a reply's Custom Action |
| BU53 | Take it to **Shylocke** in the Temple District, from `5 Questions` | *"I hold the deed to a silver mine…"* | `700 the deed` -- *"You are selling me a hole in the ground full of creatures, and the law of Spain agrees the hole is yours to sell. Twelve hundred, and I will never visit it."* |
| BU54 | Accept at the opening price | *"Done."* | **1200 gold**, the deed leaves your inventory |
| BU55 | With **Barter 40**, haggle | *"It pays whether you go or not. Eighteen hundred."* | **1800** |
| BU56 | With **Barter 70** | *"…you know what the smiths pay for what comes out of it."* | **2500**, which is vanilla's own ceiling for a dialogue payout |
| BU57 | Sell it, then try to sell it again | - | **Not offered.** The deed is removed on all three price routes, so there is no selling it twice |
| BU58 | Keep it instead and take it to the **Mine Foreman** at Ravine Cave West | *"The mine is mine. I have the paper that says so, and a goblin gave it to me."* | `90 the paper` -- *"He takes it, holds it the wrong way up, and hands it back with enormous care… Nurg saw nothing."* The mine opens by title instead of favour |
| BU59 | Confirm the symmetry that makes the deed the right gift | - | Betraying Plumjum **closes** the `Goblin Horde IS` route past the foreman; the deed **reopens** it. A player who sides with the heir must not be locked out of the Sacred Scimitar as a side effect |
| BU60 | Check the foreman's other routes on a character who never met the heir | - | Horde mark, Barter 40, Speech 40, Schmooze 7, the ungated demand, the fight, the exit. **Nine nodes now, was eight** |
| BU61 | Loot the silver after using the deed | - | Exactly one *Magnetized Silver*. The deed moves the guards, not the ore |
| BU62 | Sell the deed to Shylocke **and** then try the foreman | - | One or the other, not both. That is the intended choice, so confirm the foreman reply is simply absent rather than failing oddly |

### The door nobody had noticed

Worth recording outside this feature, because it constrains everything Fixt adds to the Wilderness.
A spawn point in `3 Montaillou/02 Hamlet Burned` named **`From Crypt or Nostro Portal`** carries
**130 `CExpireMapAction`s** and closes Barcelona, the Sewers, **every Wilderness map**, Montserrat,
Montaillou, the Crypt and Nostradamus. The engine is blunt about what that means:
*"Attempting to load expired map."* It fires on returning to the burned hamlet from the Crypt or the
Nostradamus portal.

| # | Step | Say | Expect |
|---|---|---|---|
| BU23 | Reach the Crypt or Nostradamus, return to the burned hamlet, then try to travel to any Wilderness map | - | **You cannot.** Confirm where the world map stops offering them. Everything in acts 1-4 is one-way after this point, and all 780 goblins live behind it |

## 0.30.1 - what the combat log calls people

Reported from play: **Fernand Desoto is logged as "Sailor" when he takes damage.**

The log line is `<Attacker> hit <Defender> for ...`, and the defender's name comes from the
creature's **race**, not its can. All 753 cans in the game say `Display Name=unnamed` and **not one
sets a real name**; 58 races do, which is why a wolf reads *Black Wolf* rather than *Wolf Black
Super*. `Races/NPCs/Sailor` has an **empty** Display Name, so the engine falls back to the race's own
name and a companion who fights beside you for most of the game is called "Sailor".

That race is shared by five cans -- `DrunkSailorsin Bar`, `Mute Sailor`, `ShipSailorsonShipCanned`
and two more -- so it was **cloned, not edited**: naming it in place would have renamed every sailor
in Barcelona to Fernand Desoto. The clone carries all three stat presets unchanged.

Sweeping the rest of the class found the goblin officers reading **"Goblin Grumjun"** -- Grumdjum's
race name copy-pasted onto all four hat and khan races -- which is reachable in six maps and is now
Fixt's problem in particular, since 0.30.0 gave those officers barks and the post alarm and
`Mongol Goblin Hat Tough` is the Mine Foreman.

| who | was logged as | now |
|---|---|---|
| Fernand Desoto | *Sailor* | **Fernand Desoto** |
| goblin officers, incl. the Mine Foreman | *Goblin Grumjun* | **Mongol Goblin Officer** |
| the Warrens' Goblin King | *Goblin Grumjun* | **Goblin Khan** |
| Fixt's Rumjun Khan in `01 Desert Sprawl` | *Goblin Grumjun* | **Rumjun Khan** (own race) |
| Grumdjum, the companion | *Goblin Grumjun* | **Goblin Grumdjum** |

Race and can edits, so they reach creatures spawned after install. **If a name is still wrong, try a
save that has not entered that map before reporting it** -- whether the engine resolves the display
name at log time or baked it into the entity snapshot is exactly what `DN1` settles.

| # | Step | Say | Expect |
|---|---|---|---|
| DN1 | Recruit Fernand, take a hit for him or let an enemy hit him, and read the log | - | **"Fernand Desoto"**, not "Sailor". If it still says Sailor on a save that already had him, repeat on a fresh character -- that answers whether display names are snapshot or resolved live, and the answer is worth recording either way |
| DN2 | Hover the cursor over Fernand before you ever talk to him on the dock | - | He will read **Fernand Desoto** rather than Sailor, which is a small spoiler and deliberate: it is the same thing vanilla does with Cervantes and Inquisitor Diego, both of whom carry their names on their races from the moment they are placed |
| DN3 | Every other sailor: the drunks in the Port District tavern, the mute sailor, the crew on the ship, Cortez Cave | - | **Still unnamed sailors.** `Races/NPCs/Sailor` was not touched; Fernand got a clone. If any of them says "Fernand Desoto", that is the bug this avoided |
| DN4 | Check Fernand's stats are unchanged -- HP, AC, how hard he hits | - | Identical. The clone carries `Races/NPCs/Sailor`'s three presets verbatim; only the name differs |
| DN5 | Fight a goblin in a hat anywhere -- `Bounty Hunter Camp`, `Waterfall Passage`, `Random Ethereal Ring`, `Random Forest Map 1`, `Ravine Cave East` | - | **"Mongol Goblin Officer"**, not "Goblin Grumjun" |
| DN6 | Attack the **Mine Foreman** at Ravine Cave West instead of parleying | - | He logs as **Mongol Goblin Officer**. His dialogue still calls him Nurg; the log cannot show that without giving him a race of his own, which is noted as a refinement rather than done |
| DN7 | The Warrens' Khan, and Fixt's Rumjun Khan in `01 Desert Sprawl` | - | **"Goblin Khan"** and **"Rumjun Khan"** respectively. Rumjun got his own race cloned from `Goblin Hat Super`, carrying 0.30.0's boss damage profile unchanged, so he should still take -10 from fire and shrug off poison |
| DN8 | Grumdjum as a companion, taking damage | - | **"Goblin Grumdjum"**, with the d. Vanilla's race spelled it *Grumjun* while all twelve of his map entity names and his whole dialogue tree spell it Grumdjum |
| DN9 | Any ordinary goblin, and any goblin shaman | - | Unchanged -- *Mongol Goblin* and *Goblin Shaman*. Only the hat and khan races were touched |

### The rest of the class, fixed in the same pass

Three more wrong names, and fixing them forced three others into view because the races are shared.

| who | was logged as | now |
|---|---|---|
| Leonardo da Vinci | **River Dryad** | Leonardo DaVinci |
| Galileo (Barcelona, and the final encounter) | *River Dryad*, then *Leo* | Galileo, by two cloned races |
| the endgame Leonardo in `08 Final Encounter` | *Leo* | Leonardo DaVinci |
| Sir Roger Templeton | **Knight Templar 5** | Sir Roger Templeton |
| Guard Esteban | *Knight Templar 5* | Guard Esteban |
| Sir Jorge | *Knight Templar 3* | Sir Jorge |
| every dead, burned, siege and bar-patron Templar | *Knight Templar 1* through *5* | Knight Templar |
| `English in Caverns of Nostrodomus/Priest` | **Jerk** | Priest |

Two things worth stating plainly rather than claiming more than is true.

**Nothing in the game ever read "Jerk".** No can points at that race. The earlier note that it was
placed in four maps was wrong -- those cans use `English Enemies/Priest`, whose Display Name is empty
and so falls back to "Priest" correctly. It is fixed because the string is one edit away, not because
anyone was seeing it.

**Guard Esteban nearly got a serious regression.** Vanilla already ships
`Races/NPCs/Knights Templar/Guard Esteban.Race`, used by nothing, which looks like exactly the right
place to point him. It presets **AC 1000 and HP 10000** -- the deliberate invulnerability pattern. Had
he been repointed at it he would have become unkillable, silently breaking 0.1.1's counter-contract,
0.1.4's `Esteban Death Consequences` and the 0.10.3 repair that exists *because* the Templar
initiation died with him. That file is instead overridden with `Knight Templar 5`'s own stats and his
name: the label changes and nothing else does.

| # | Step | Say | Expect |
|---|---|---|---|
| DN10 | Fight or watch **Leonardo da Vinci** take damage -- the Gate District, the workshop, the secret chamber, `01 Hamlet Exterior`, `04 Inn Interior` | - | **"Leonardo DaVinci"**, not "River Dryad" |
| DN11 | **Galileo** in the Temple District, and again in `08 Final Encounter` | - | **"Galileo"** both times. He shared Leonardo's race in Barcelona and the endgame pair race at the end, so he was reading *River Dryad* and then *Leo* |
| DN12 | The endgame **Leonardo** in `08 Final Encounter` | - | **"Leonardo DaVinci"**, not "Leo" |
| DN13 | **Sir Roger Templeton** as a companion, taking a hit | - | **"Sir Roger Templeton"**, not "Knight Templar 5" |
| DN14 | **Guard Esteban** at the Crossroads: hit him once, then let him live | - | Logs as **"Guard Esteban"**. Critically, **he must still be killable** -- if he shrugs off everything, this is the row that caught it, and the fix is to re-check his race presets are 200/200 and not 1000/10000 |
| DN15 | Kill Esteban deliberately, then take the Templar initiation to Javier | - | Exactly as before this patch: `Esteban Death Consequences` fires and Javier's alternative line is reachable. His stats did not change, only his name |
| DN16 | **Sir Jorge** in the Port District | - | **"Sir Jorge"**, not "Knight Templar 3" |
| DN17 | Any anonymous Templar -- the dead ones in `02 Hamlet Burned`, the siege Templars, the two bar patrons, the cathedral guard | - | **"Knight Templar"**, with no tier number. Five races stopped leaking it |
| DN18 | Check Sir Roger, Esteban and Sir Jorge all still fight as they did | - | Each got a clone of the tier race they were using, presets carried verbatim; only the name differs |


## 0.30.0 - the goblins: a voice, a damage profile, an officer who calls for help

Goblins are the **largest enemy population in the game** -- 780 of spawn capacity across 30 maps,
more than the thieves, soldiers, snakebreed and trolls together -- and until now the only major
family with **no barks and no damage resistances at all**. Every goblin change Fixt had made was
about *not* fighting them.

**105 distinct lines**, 92 authored and 13 of vanilla's own. The banks are deliberately much larger
than any shipped family, because the player hears goblins more than every other family combined:

| bank | lines | made of |
|---|---|---|
| rabble | **40** | 18 shared + 16 its own + **6 restored from `GoblinVillager`** |
| shamans | **37** | 18 shared + 16 its own + 3 reused from the `Goblin Shaman` tree |
| archers / officers | **34** | 18 shared + 16 its own |
| hurt (all tiers) | **14** | 10 its own + **4 restored** |

For comparison the shipped families run 11-14, where a repeat turns up after about five barks. At
34-40 it takes about eight. `GoblinVillager.DialogTree` had 11 nodes fired by nothing in the whole
game; the restored lines are referenced at their own vanilla node IDs rather than copied, so vanilla's
dead nodes start firing.

Can and race edits throughout, so **every row needs a save that has not entered the area**.

| # | Step | Say | Expect |
|---|---|---|---|
| GB1 | Fight any `Mongol Goblin` on a fresh map | - | Floating text **over the goblin's head**, not in the combat log. About one attack in four |
| GB2 | Fight them for a long stretch -- several minutes | - | **It should take a long time to hear a repeat.** 40 lines for the rabble. This is the row the first build would have failed |
| GB3 | Listen for the register | - | They talk about **eating you**, which is vanilla's own goblin voice: *"The pot is already hot, morsel."*, *"Your bones go in the broth. The rest of you goes in the bowl."*, *"Me eat brain! Then me am smart!"* |
| GB4 | Fight a goblin **archer** and a plain goblin in the same run | - | Different registers. The archer talks distance -- *"No closer, meat. I like you at this distance."*, *"I do not have to be brave at this range."* |
| GB5 | Fight a `Mongol Goblin Hat` / `Hat Tough` / `Hat Super` | - | Orders, not hunger -- *"Form! Form, you stupid things!"*, *"It is one of them and twelve of you. Explain that to me."*, *"I will tell the Khan who fought. I will also tell him who did not."* |
| GB6 | **Hurt** a goblin without killing it, repeatedly | - | A second register entirely, rarer (about one hit in six): *"They are too mighty!"*, *"We must flee and make haste!"*, *"Run! AIIIIiiiiIIII!"*, *"Where is the one with the hat? Where is he!"* **Three of those are vanilla lines `Bounty Hunter Camp` was the only map ever to fire** |
| GB7 | Fight a `Mongol Goblin Shaman` and watch it **attack** | - | It barks too, which the first build could not manage. Its `Shoot Completed` is a spell *picker*, so the bank went in as a fourth item: *"Flesh is a borrowed thing, and I am calling it back!"*, *"Rakeb taught me this one."* |
| GB8 | Watch the shaman's **spells** across a long fight | - | **Still Spike and Static Charge, still roughly 1:2.** The picker kept all three of its selections and gained the bark as a fourth. If a shaman stops casting, this is the row that failed |
| GB9 | Talk to the **Khan**, **Rakeb**, **Grumdjum**, the Warrens' **Goblin Girl** and **Goblin Guard**, and the **Crossroads Patrol Leader** | - | All six exactly as before. **Named and talkable goblins were deliberately given no barks** -- a named character must not speak the rabble's lines |
| GB10 | Check the combat log during all of the above | - | Barks are **not** in it. `Include In Log=0` |

### The damage profile -- the actual answer to "why does every goblin fight feel the same"

Every other family has one. Animals resist slashing and crushing 38 and take extra cold; English
Enemies are armoured and fold to crushing at **-44**; wererats are immune to fire; undead shrug off
electricity. Across 417 races and nine damage types the goblins' 19 races were **blank in all nine
columns**. They now read as one family with one weakness:

| tier | Slash | Pierce | Crush | Fire | Cold | Elec | Poison | Disease |
|---|---|---|---|---|---|---|---|---|
| rabble and archers | -10 | - | -20 | **-25** | 20 | 15 | 100 | 100 |
| shamans | -10 | - | -20 | **-25** | 20 | **50** | 100 | 100 |
| hat officers | **20** | **20** | 0 | **-25** | 20 | 15 | 100 | 100 |
| Khan, Hat Super, Grumjun, Rakeb | 25 | 25 | 10 | **-10** | 25 | 25 / 50 | 100 | 100 |

| # | Step | Say | Expect |
|---|---|---|---|
| GB11 | Burn a goblin. Any fire source, any tier | - | **Noticeably more damage.** Fire is the family signature. Nothing else in the game is reliably fire-vulnerable -- wererats are immune and the English resist it 73 |
| GB12 | Poison or disease a goblin | - | **Nothing.** Both 100, vanilla's own immune value. They eat carrion and brains. The log should say *"resists all of your damage"* |
| GB13 | Hit the **rabble** with a blunt weapon, then a blade | - | Crushing -20 against slashing -10: the club should beat the sword. Small bodies, no armour |
| GB14 | Now hit a **hat officer** with the same two weapons | - | **It inverts.** Slashing and piercing +20, crushing 0. The officer wears real kit and needs a different answer than the rabble around him |
| GB15 | Hit a **shaman** with Static Charge or Lightning Bolt | - | Electrical 50, about half. They throw lightning themselves, so lightning is the wrong tool. Burn them |
| GB16 | Check the log on a resisted hit | - | `hit ... for <UnresistedDamage> ... (Resisted <n>) INFLICTED <Damage>`. The save logs every hit with its damage type, so one save file settles GB11-GB15 exactly |
| GB17 | **Grumdjum as a companion**, with a fire-casting player | - | He is `Goblin Grumjun`, so fire-vulnerable too -- but at the boss tier's **-10**, not -25. If he still burns down noticeably faster than other companions, say so: the taper exists for this and can go further |
| GB18 | A goblin in the **Djinn dream arena** (`Dream Djinni Map`) | - | Same profile. `DjinnArenaMonster1` shares the `Goblin Archer` races and is a goblin archer by model -- correct spillover, not a leak |

### The officer calls for help

Fixt's own troll idiom, inverted. A generator's `New Name` applies to **every** creature it spawns,
so a post holding two archers and a Hat cannot name the Hat alone without being cloned -- so the
*post* is named and the *officer* is the trigger. `Ravine Cave East` only: its four archer posts at
(1269, 851), (1914, 647), (2319, 748) and (2342, 1719) are now `Goblin Cave Post`.

The Hat appears **only in the generator's top `Max Party Mojo` group, at weight 1 against the
archer's 2**, so about one spawn slot in three is an officer. The bound there is 50, but the engine
picks the group whose bound the party falls *under* and the next one down is 10 -- so that group is
entered at a party mojo of about **11**, not 50. It makes officers uncommon; it does **not** gate the
alarm behind a strong party. **Worst case measured: 12 creatures, once per level.**

| # | Step | Say | Expect |
|---|---|---|---|
| GB19 | A **high-level** party, fresh `Ravine Cave East`. Find a goblin wearing a hat and hit it once | - | The archer posts converge. `COnlyOnceAction`, so it happens once. **Count them and report the number** -- the design budget is 12 and the troll pack alarm had to be rescoped after exactly this measurement |
| GB20 | Hit the same officer again, or a second officer | - | **No second alarm.** `Trigger Only Once` |
| GB21 | Hit the rabble and the archers, never the officer | - | **No alarm at all.** Only the hat raises it. If striking an ordinary goblin brings the cave, report it |
| GB22 | A **low-level** party in the same cave | - | Likely no alarm, because likely no officer -- the Hat is top-tier only. Worth confirming the cave still plays as it always did |
| GB23 | The **Mine Foreman** in Ravine Cave West: attack him instead of parleying | - | He is `Mongol Goblin Hat Tough`, so he carries the alarm -- but `Goblin Cave Post` does not exist in that map and the alarm is guarded on the name existing, so it must be a **no-op**. `Mine Guards` should wake exactly as they did via the dialogue's fight reply, and nothing else |
| GB24 | Fight hats in `Random Ethereal Ring` (12 of them), `Waterfall Passage`, `Bounty Hunter Camp`, `Random Forest Map 1` | - | **No alarm** -- those maps have no `Goblin Cave Post`. Only Ravine Cave East was wired this pass |

### The argument vanilla wrote and never staged

Three consecutive `GoblinVillager` nodes, fired by nothing in the whole game, that are not three
interchangeable barks but one exchange between three goblins who are losing:

> **Drubjub** -- *"They have butchered our brothers with alarming ease. Perhaps discretion would be
> the more prudent course of action?"*
> **Wumjup** -- *"Nonsense, we are Mongol-trained goblins, the scourge of the land!"*
> **Lumgrub** -- *"Yes, Wumjup is right! Muster up your courage and attack! AIIIIiiiiIIII!"*

Line C names its own middle speaker, so **B had to be Wumjup** -- which is also why the rabble's
barks keep mentioning a Wumjup nobody ever met. `Drubjub` and `Lumgrub` are vanilla's too: they are
the goblins talking to each other in `GoblinGuards` and `GoblinLt`. None of the three was an entity
name anywhere in the game.

Staged on vanilla's own `goblin attack banter` relay from `Crossroads`: `CSeriesAction` with
`Next Action Index=0`, which advances **one item per trigger**. So the trigger is a goblin dying, and
the argument escalates as the fight goes worse -- the coward speaks over the first body, the boaster
over the second, the charge over the third. `Ravine Cave East` only, the three standing together at
**(2174, 1197)**, about 965 units in from the map's `Start Here` spawn at (1364, 1721) -- far enough
to have fought on the way. Note the cave's real shape, which an earlier draft of this section got
wrong: **`Ravine Cave East` is not behind the mine.** It has its own entrance off `Scar Ravine` at
(2834, 519), the two halves connect only by the `Crystal Node Ravine Cave Teleport` pair, and the
magnetized silver is in **West only** -- so the Sacred Scimitar never requires entering East at all.
Capacity there
goes 90 to 93.

| # | Step | Say | Expect |
|---|---|---|---|
| GB30 | Fresh `Ravine Cave East`, entered from `Scar Ravine` (not from the mine -- there is no passage between the halves). Fight inward until **one** goblin is dead | - | Over **Drubjub**: *"They have butchered our brothers with alarming ease. Perhaps discretion would be the more prudent course of action?"* |
| GB31 | Kill a **second** goblin | - | Over **Wumjup**, a different goblin: *"Nonsense, we are Mongol-trained goblins, the scourge of the land!"* |
| GB32 | Kill a **third** | - | Over **Lumgrub**, a third goblin: *"Yes, Wumjup is right! Muster up your courage and attack! AIIIIiiiiIIII!"* **This is the payoff -- Lumgrub names Wumjup, and Wumjup is the one who actually said it** |
| GB33 | Keep killing goblins after that | - | **Nothing more.** `When Done=Do Nothing`, so the series stops on the third line and does not loop |
| GB34 | Check that the three balloons appeared over **three different goblins** | - | The whole point. If all three stack over one goblin, `Name of Position` is not resolving by name and the build has failed |
| GB35 | Find the three of them before killing anything -- mid-cave, around (2174, 1197) | - | A plain goblin, a `Mongol Goblin Tough` and another plain goblin standing together. They fight normally; nothing about them is pacified |
| GB36 | Kill **Wumjup first**, then three other goblins | - | The exchange still runs and simply skips his line. `Require Success To Advance=0`, so a dead speaker does not stall the series -- the alternative was it jamming forever on line B |
| GB37 | Fight `Mongol Goblin` / `Tough` / `Super` in any **other** map -- `Lake`, `Plains`, `Woodcutter Forest` | - | **No exchange, and no errors.** The death trigger is guarded on the relay entity existing, and `goblins losing heart` exists in one map of the sixteen that spawn those cans |
| GB38 | Watch for the hide-style failure: does killing a goblin do anything it did not before? | - | Their `Destroyed Script Action` was empty in vanilla and no `Ravine Cave East` generator sets one, so nothing was overridden -- checked, because `CSetDestroyedScriptActionAction` on a generator is what made the Lava Troll Hide dead code from 0.10.0 |
| GB39 | **The row this repair exists for.** Find a goblin fighting **alone** -- `Mongol Goblin` spawns alone in 48 of its 64 groups, so this is the common case rather than a hunt. Hurt it and read the bank out | - | **Nothing refers to a companion**, a line, or anyone standing behind it. The reported line was `<He looks for the goblin who was beside him a moment ago.>`; it is now `<He looks around for help, and takes his time about believing there is none.>` |
| GB40 | A **lone officer** -- `Mongol Goblin Hat`, which is alone in **12 of its 13** groups | - | No *"Hold the line!"* and no *"the line tightens"*. He now points and keeps pointing until something moves, which is the joke when nothing does. These were the most frequently wrong of the seven |
| GB41 | A goblin fighting **in a group**, any type | - | The reworded lines must still read correctly *with* company -- that is the half a deletion would have got for free and a rewrite has to earn. If any of the seven now sounds wrong in a crowd, say which |
| GB42 | Count the barks across a long fight | - | **Still 92 nodes**, 105 distinct lines with the vanilla ones. Nothing was removed: four banks would have been thinned by deleting the seven, and bank size is the whole defence against repetition |

### They answer each other

| # | Step | Say | Expect |
|---|---|---|---|
| GB25 | **Open question.** Attack one goblin at the edge of a group on a fresh map | - | Do the others come? `Respond to calls for reinforcements` is now `1` on all 16 hostile goblin cans; it was `0` on 21 of 23, leaving goblins alone with the Animals and Thugs while the Undead run it on **88 of 92**. Its description: *"will make this character aquire a target when a friend asks for help"* |
| GB26 | The control for GB25 | - | `CCallForReinforcementsAction` -- the explicit "ask for help" action -- is registered in the exe and used **zero** times in all of vanilla. So either being attacked calls implicitly (and the undead have swarmed all along), or the field is inert everywhere and this changes nothing. **Static analysis cannot separate those two; GB25 can.** Harmless either way, and the answer is worth having |
| GB27 | If GB25 swarms: fight in `Lake` (153 capacity) | - | It must stay a *local* response, not a map alarm. It is per-creature by design -- a creature acquiring a target, not a broadcast -- but if a whole map arrives, report it and it comes straight out |

### One repair carried along

| # | Step | Say | Expect |
|---|---|---|---|
| GB28 | Fight a bow thief, a bow soldier and a Snakebreed Venom | - | They should shoot as they always did. **21 archer cans shipped since 0.27.0 with a bark filler selecting `Skills/Fighting/OneHandedMelee` -- a skill not present on their race at all.** Vanilla uses that action in that slot to choose the next attack (`Priest Super` casts its shield, then picks Fire Orb or Spike), so it was never inert. Each is now repointed at its own race's primary. `Soldier4 Bow Super` has Ranged 97 and was told to select melee three attacks in four |
| GB29 | Specifically: did bow units get *better*? | - | If archers were visibly fumbling before and are not now, that is GB28 landing, and it means the defect was live rather than silently ignored. Worth knowing either way |

## 0.30.0 - Ravine Cave: the silver mine can be talked past

The Sacred Scimitar is a **Knights of Saladin initiation** step, and its first task had exactly one
solution: kill the cave. There is one source of magnetized silver in the entire game -- a bone pile in
`Ravine Cave West` -- no merchant sells it, `Ravine Cave West` had **zero dialogue trees**, and
Eduardo closes every alternative in his own voice (mercenary, suppliers, the city guard).

Now a foreman holds the mouth of the cave with the archer post around him, bows up and not firing, and
there are four ways past him. **The three deeper posts stay hostile until a parley succeeds**, so a
player who attacks gets the cave exactly as vanilla built it.

A map change, so it needs a character who has **never entered `Ravine Cave West`**. A Sacred Scimitar
run arrives there naturally, and is also the character most likely to have **no goblin standing**,
which `MF2` depends on.

| # | Step | Say | Expect |
|---|---|---|---|
| MF1 | Enter `Ravine Cave West` from Scar Ravine and walk in about 800 units | - | A `Mongol Goblin Hat Tough` -- **Nurg** -- challenges you instead of attacking, with archers around him. *"Far enough… every bow in the dark comes up at once, and none of them wavers."* **They do not shoot** |
| MF2 | With **no goblin standing**, choose *"I have come for the silver. Stand aside."* | - | `60 refused`. He warns you and nothing attacks -- *"Come for it with coin, or a mark, or a better tongue than that."* You can walk off and come back, so the routes are discoverable without a fight |
| MF3 | With `Goblin Horde IS`, choose *"I wear the Khan's mark."* | - | `20 the khans man`. The bows go down before he speaks -- *"Then it was never ours to keep."* |
| MF4 | With Barter 40+, choose *"I am the buyer you have been waiting on."* | - | `30 the price`. This is the one the fiction asks for -- Eduardo says they are driving the price up, so they are sellers with no buyer. *"Four months we sit on rock nobody comes for"* |
| MF5 | With Speech 40+, take the reasoned route | - | `40 reasoned past` -- *"The Khan hears about dead humans in his mine. He does not hear about rock."* |
| MF6 | With Schmooze 7+, take the charm route | - | `50 charmed` -- *"You talk like a goblin."* |
| MF7 | After any of MF3-MF6, walk deeper toward the silver | - | **The three deeper goblin posts do not attack either.** `Mine passage granted` clears targeting and drops `Enemy` on all four posts. This is the whole point: the parley opens the road |
| MF8 | Reach the bone pile at roughly (1983, 455) and loot it | - | *Magnetized Silver*, **exactly one**. Negotiation moved the guards, never the ore -- the pile is where vanilla put it |
| MF9 | Take it to Eduardo | - | He forges the Sacred Scimitar as normal. Nothing in his chain was touched |
| MF10 | On a fresh character, choose *"Then your people can decide."* | - | Nurg **and** the whole archer post turn on you at once. `CGoToCombatAction` on `$Trigger` and on `Mine Guards` |
| MF11 | On a fresh character, attack Nurg without talking | - | He fights, and so does his post. The deeper posts are hostile as they always were -- the combat route is unchanged |
| MF12 | Choose *"Another time, then."* | - | He lets you leave -- *"Walk out the way you walked in, and we stay bored."* No state change; you can return and parley |
| MF13 | The wasps, on every route | - | **Still hostile, and still 57 of them.** A parley gets you past the goblins; it does not clear the nest, and a pure talker may still have to survive the walk to the pile |
| MF13a | **Open question.** Toggle Sneak on and walk in without talking to anyone | - | Does anything notice? `Sneak` is a real skill with a HUD toggle and tiers at 10/20/25/35, the wasps carry `Sneak Adjustment=0` and every goblin `+15` -- but what that field *means* is unresolved. Its extremes are Wererat Minions at **-300** and Assassins at **-85**, against Skeletons and Zombies at **+25 to +50**, which reads like the creature's own stealth rather than its alertness. Static analysis cannot settle it; one walk with Sneak up will. **Report what happens** |
| MF13b | If MF13a gets you to the pile untouched, try it again with Sneak **off** | - | The control. If sneaking made no difference, the field is about the creature's own stealth and the cave has no stealth route -- which is worth knowing before anyone designs one |
| MF14 | Count the archers at the mouth on a weak and then a strong party | - | It scales -- the post spawns 1 Archer at `Max Party Mojo=3`, up to 2-3 Archer Supers at 25. The threat is meant to read as serious |
| MF15 | Parley successfully, leave the cave, come back | - | The posts should still be stood down. `Mine passage granted` is `Trigger Only Once=1`, so if they are hostile again on re-entry, report it -- that is the entity-snapshot question |

## 0.30.0 - Scar Ravine: the hostage gets an evil outcome, and her father finds out

Four tiers. The hostage scene north of the Crossroads had five ways to save Gloria, **no way to
decline** (both refusals fired `CGoToCombatAction`), and no evil outcome at all -- while her father
never learned anything, because the `daughter attacked` marker was set and read only to *withdraw* one
reply.

**Needs a character who has never entered `Woodcutter Forest`**, because `daughter taken` is a new
entity on that map and entity lists are snapshotted on first visit. A Sacred Scimitar run reaches Scar
Ravine first -- the magnetized silver is in `Ravine Cave West`, through Scar Ravine -- so that is the
natural test character, and it is also the character most likely to have **no goblin standing**, which
`GL7` depends on.

| # | Step | Say | Expect |
|---|---|---|---|
| GL1 | Talk to the goblin, choose *"I was never here, and neither were you."* | - | **He lets you go.** No combat, no state change. The scene is still running and you can come back and save her |
| GL2 | Talk again and choose *"It's no concern of mine what you do with her"* | - | He still attacks, exactly as vanilla. That route was deliberately left alone -- the fix adds a way out, it does not remove one |
| GL3 | With Speech 55, choose *"Let me take this child to the Goblin Khan…"* | - | The reply is tagged **`<Lie>`**, and it resolves as it always did: he backs down, she escapes, the quest completes as a rescue. The label is the fix -- the words and the outcome finally agree |
| GL4 | Regression: ST 8+, Barter 55, and killing him | - | All three still free her. `71 backs down`, `72 the trade`, and the fight are untouched |
| GL5 | **With goblin standing**, choose *"I carry the Khan's favour…"* (Quest icon) | - | `73 the handover`. Grimek steps back, disowns her, and names himself. You take her |
| GL6 | After GL5, watch both of them | - | **She walks off and vanishes; Grimek also leaves and is gone.** He is disposed of exactly as the rescue routes do it -- if he is still standing there, that is the bug this tier fixed |
| GL7 | **With no goblin standing at all**, choose *"The Khan would want to know who fed him this well…"* | - | `74 a way in`. He sponsors you, and you become a **Goblin Chum** -- first standing, earned by the act. `savecheck save` should show `Goblin Rank=1` |
| GL8 | After either delivery, check your character | - | **Slayer of Innocents** title gained, and **-50 karma**. `savecheck save` shows the karma; the title shows in the perk list |
| GL9 | After delivery, go to the woodcutter's house | - | She is **not** there. Her home generator is deleted, as on the attacked path |
| GL10 | Deliver her **without** having taken the quest, then meet Felipe | - | He asks for help as normal, and the accept reply is **absent**. Nothing records a failure, because there was no quest to fail -- `CSetQuestSatusToFailedIfActiveAction` |
| GL11 | Take his quest first, then deliver her, then return | - | The quest is **failed** |
| GL12 | Talk to Felipe after delivering or striking her, choose *"I am the reason she did not come home."* | - | `31 she never came home`. He does not shout and does not attack. **He shuts the cave** |
| GL13 | The same, choosing *"I searched the forest and found nothing."* | - | Tagged `<Lie>`, and it lands on the same node. He is not fooled; the cave still closes |
| GL14 | After GL12, try to get the Darkwood | - | You cannot. The cellar never opens -- `COpenDoorAction` lives in a task only he performs. The **Wielders'** first task is closed, and that is intended: the **Dark Wielders** remain open through Relican, reachable via Brambles or on sight |
| GL15 | Strike Gloria instead of delivering her, then talk to Felipe | - | The same `31` response. From his side the outcomes are identical -- she never came home either way |
| GL16 | Reach the Goblin Khan after delivering, on a **first** meeting | - | A Quest-icon reply about the child. `375 the khan has eaten well` -- Grimek's runner beat you there by three days with his own name in front |
| GL17 | Reach him again later as a goblin friend | - | The same reply is offered from `05 Return Friends of Khan` |
| GL18 | Deliver, then check `python tools/savecheck.py save latest` | - | Karma down 50, `Goblin Rank` set, and the title in the perk list. This is also the cheapest check that `$Instigator` resolved to the player in the reply action |

## 0.29.0 - the Inquisition Chambers CTD

Reported by a player: a crash to desktop on entering the Inquisition Chambers.

> Invalid class type -- Tried to use an unknown class "ClsQuestStatusCompletedAction" for a "Action"
> (CAction). Last file opened = "Resources/Levels/1 Barcelona/Dialog/Temple
> District/GrandInquisitor.DialogTree:Node:Reply:Custom Requirement:Operand2:Operand1"

The report is accurate and the name in it is only disguised by the crash dialog's font -- a capital I
rendering as a lowercase l. The file named `CIsQuestStatusCompletedAction`, which does not exist. The
real class is `CIsQuestCompletedAction`; the three sites already carried its exact field set, a lone
`Quest=`, so only the name was wrong. Most likely a blend of it with `CSetQuestSatusToCompletedAction`,
whose "Satus" typo is vanilla's own -- and `CIsQuestStateCompleatedAction` is also real, also
misspelled, and takes different fields.

**Shipped in 0.13.0 and present in 27 tagged releases, through 0.28.2.** It survived because the three
sites are the Grand Inquisitor's *return* nodes gated on a Wilderness quest, so a player has to get
that far and then come back.

A dialogue tree change, so it needs no fresh save.

| # | Step | Say | Expect |
|---|---|---|---|
| IQ1 | With `Bring the Rogue Inquisitors to Justice` **completed**, enter the Inquisition Chambers | - | **No crash.** This is the whole fix |
| IQ2 | Talk to the Grand Inquisitor on a normal return (`3 Return Dialogue`) | - | He greets you and the conversation opens |
| IQ3 | Ask *"Does the Inquisition have any tasks for me?"* on the irritated return (`2 Irritated Return Dialogue`) | - | The reply appears and resolves. It is gated on that quest being complete, which is the gate that was crashing |
| IQ4 | The same on the favored return (`5 Favored Return`) | - | Likewise |
| IQ5 | Enter the Chambers **without** that quest complete | - | No crash either. The requirement now evaluates instead of failing to load |
| IQ6 | `python tools/validate.py` | - | Passes. A0.15 fails on any class the engine does not register, which is what should have caught this in 0.13.0 |

## 0.29.0 - the lava trolls: barks, the stomp, regeneration, a pack alarm

All four are can / race / item level, so one fresh Troll Pit covers them together with `TH1`-`TH8`.
**Needs a character who has not entered 05 Troll Pit.**

| # | Step | Say | Expect |
|---|---|---|---|
| LT1 | Fight the drones | - | Hover text over their heads, roughly one attack in four, broken and terse -- *"You no belong!"*, *"Hot now, yes?"* -- and sometimes a wordless line like *"<It grunts, and keeps coming.>"* |
| LT2 | Fight the chief | - | A different register, measured and counting: *"I will count you with the others."*, *"Hold him. He is one and we are many."* **No drone should ever speak a chief line, or the reverse** |
| LT3 | Watch the ground when a troll connects | - | The **Troll Stomp** effect plays. The radius-120 area pulse was always there; this is the first time it is visible |
| LT4 | Take a hit from the chief and count the damage lines | - | Fire damage, one or two pulses of 6-16. That is the stomp, not a separate attack |
| LT5 | Wound a troll, then break off and watch it | - | It **closes its own wounds** -- 0.6 HP/sec for a drone, 1.0 for the chief, against your own ~0.37. Visible over several seconds, not instant |
| LT6 | Fight the chief to the end with a **piercing** weapon | - | Hard. Troll races resist piercing at 50 percent, and the simulation puts this near a coin flip |
| LT7 | Fight him again with **cold** | - | Markedly easier: `Cold Damage Resistance=-15` is their one weakness and it already shipped in vanilla |
| LT8 | Hit a lone drone away from the others | - | **The chief comes.** One ally, not the pit. Fires once per drone |
| LT9 | Hit a second drone | - | The chief does not come twice. `COnlyOnceAction` is per troll, and he only has to arrive once |
| LT10 | Make peace with the trolls first, then strike one | - | **No alarm at all.** The call sits behind a `Troll Peace Keeper` check, so an accidental swing does not turn the pit hostile |
| LT11 | Count the trolls that engage after an alarm | - | A handful, never the whole level. The pit holds 80-94 trolls with a 4000 leash -- a group-wide call was built, measured, and deliberately cut back |
| LT12 | Kill the chief | - | The *Lava Troll Hide* still arrives in your pack (`TH1`). None of this touched the drop |

## 0.28.2 - Fernand's combat AI stops freezing

Reported from play: he freezes after a kill and only reacts when attacked. He is the only companion
whose skeleton AI is hand-built in a map relay, and vanilla gave it `Vision Cone=90` and
`Max Distance=300` -- sentry values, where every other companion and 1317 uses across the game have
`360`, and 1019 have `550`. After a kill, re-acquisition only saw a 90-degree arc of his facing;
`Target shooter if hit=1` bypasses acquisition, which is why being hit woke him. Now `360` / `550`.

The relay writes his AI at join time, so this needs a **fresh recruit** -- an existing companion keeps
the old eyes.

| # | Step | Say | Expect |
|---|---|---|---|
| FA1 | Recruit Fernand, take him into the Vodyanoi fight at the north island | - | After killing one, he **moves to the next enemy on his own**, including one behind or beside him. Before this he stood still until something hit him |
| FA2 | Stand him where an enemy is roughly 400-500 units off and out of his facing | - | He acquires it. The old 300 range and 90-degree cone could see neither |
| FA3 | Let an enemy attack him while he is idle | - | He fights back, as he always did -- `Target shooter if hit=1` was never the broken part |
| FA4 | Take his health below 40 percent | - | **He breaks off and retreats.** Deliberate: `Retreat when=40` is kept, unlike Cervantes who never flees. Not a bug |
| FA5 | Walk far enough away mid-fight | - | He disengages and returns to following. `Max dist from home=500` is unchanged |
| FA6 | Compare against Cervantes in the same fight | - | Broadly similar engagement now. He still retreats where Cervantes does not, by choice |

## 0.28.1 - Fernand Desoto can be taken back (attempts six and seven)

See the section below for the five that failed. The cause was never in his dialogue tree: while an NPC
is a companion the engine lays `Player Data/Companion AI Interaction Specifier.can` over the top --
`Use=Shared Global Instance`, opening `Levels/Generic Companion Dialog` node `01 Conversation Start` --
so talking to a follower opens the **generic companion menu** and his own conversation is unreachable.
His standing specifier is seen only once he is released, so it must open the *released*-state node.

Needs a character who has **not yet recruited him** -- the specifier is entity state, snapshotted on
first visit. `FN8` is the exception and is the interesting case for an existing save.

**Signed off 10/01/26: the release and rejoin cycle was exercised by hand and works.** FN11 and FN12 were verified from the save first.

**0.28.0 fixed only half of this and 0.28.1 fixes the rest.** The engine's overlay is a *swap that
remembers*: `FUN_005e7870` looks for an existing `CAIInteractionSpecifier`, parks it in the
`CCompanionManagerAI` as `Original AIInteractionSpecifier`, and replaces it -- and only appends if the
entity has none. Fernand's join node triggered the relay that removes his specifier and re-adds it
0.1s later, while `CSetCompanionAction` also fired at 0.1s. The companion call won that race, found an
empty slot, appended the overlay and parked nothing, so release had nothing to put back and the generic
menu stayed on him permanently. The companion call now waits 0.5s. Cervantes never had a race to lose:
his specifier is standing map data, present before anyone recruits him.

| # | Step | Say | Expect |
|---|---|---|---|
| FN1 | Recruit Fernand, then talk to him | - | The **generic companion menu**: *"What would you like your companion to do?"* with *Release Companion*. That is the engine's, not his, and is expected. **PASSED** 10/01/26, release and rejoin exercised by hand |
| FN2 | Choose *Release Companion* | - | He stops following. **PASSED** 10/01/26, release and rejoin exercised by hand |
| FN3 | Talk to him again | - | **His own conversation opens**: *"Shall we continue, or is my place here for now?"* with *Walk with me again, Fernand.* This reply is the whole release. **PASSED** 10/01/26, release and rejoin exercised by hand |
| FN4 | Choose *"Walk with me again, Fernand."* | - | **He rejoins and follows.** This is the bug, reported five times across seven attempts. **PASSED** 10/01/26, release and rejoin exercised by hand |
| FN5 | Talk to him while he follows again | - | The generic menu once more. His node is hidden while he follows -- correct, not a regression. **PASSED** 10/01/26, release and rejoin exercised by hand |
| FN6 | Cycle release and rejoin three times | - | Works every time. No flag, nothing to desynchronise |
| FN7 | Choose *"Hold this spot a while longer."* | - | The conversation closes and he stays put. Talking again re-offers the rejoin |
| FN8 | On a save that recruited him under 0.25.3-0.28.0 | - | **Not achievable, and the expectation here was wrong.** 0.28.0 assumed giving node 100 the rejoin would repair such a save; 0.28.1's own finding rules it out. That character lost the join race, so the generic overlay was appended with nothing parked and still sits first in the AI array -- he opens the generic menu and no node of ours is reachable. Node 100 keeps the rejoin anyway, which costs nothing. Needs a fresh recruit |
| FN9 | A save that recruited him **before 0.25.7** | - | Still broken: that save has a *balloon* specifier baked in, so he floats a line and opens nothing. Needs a fresh recruit, and cannot be repaired from our side |
| FN10 | `python tools/savecheck.py grep "Fernand Is Waiting" --save latest` | - | Absent. 0.25.4's scripting variable is deleted and nothing depends on it. **PASSED** -- absent in every save checked |
| FN11 | **Save immediately after recruiting him, before releasing.** `python tools/savecheck.py grep "Original AIInteractionSpecifier" --save latest` | - | **The decisive check, and it needs no release at all.** It must be present, and the specifier parked inside it must open `103 fernand waiting`. That is the engine's own restore slot -- Cervantes' holds `3 Return after release as a companion`. **PASSED** 10/01/26 -- parked and opening `103 fernand waiting` |
| FN12 | In the same save, count his active specifiers | - | **Exactly one**, the generic `Generic Companion Dialog` at `X Radius=30`. Two means the join race is back: the engine appended the overlay instead of swapping his out, nothing was parked, and release will have nothing to restore. **PASSED** 10/01/26 -- exactly one, the generic at `X Radius=30` |

## 0.28.0 - the troll chief drops the hide when killed

Reported from play: *"I'm killing the lava troll boss and all trolls, but I'm not getting a hide."*
Correct report. 0.10.0 put the drop on the three `Lava Troll Boss` cans, but the chief is spawned
through a generator whose `After Action` runs `CSetDestroyedScriptActionAction` -- which *changes* the
spawned entity's destroyed action, overwriting the can's slot the moment he appears. The can's drop was
dead code from the day it shipped, so the kill route could never yield a hide while the **peace** route
handed one over in two different nodes.

Both chief generators now carry `CActionGiveStandardInventoryItem`, the same action the Titan bosses use
for their stonehearts and the same one the peaceful trolls already use. It goes **straight into the
killer's pack with a notification**, so nothing can land in the lava.

A map change, so it needs a character who has **not yet entered 05 Troll Pit** -- the entity list is
snapshotted on first visit.

| # | Step | Say | Expect |
|---|---|---|---|
| TH1 | Fresh Troll Pit. Kill the troll chief (the big one, any difficulty) | - | *Lava Troll Hide* arrives **in inventory** with an on-screen notification. Not on the floor |
| TH2 | Check the quest log | - | `Troll Hide for Quinn` can now be completed. Killing him still completes `Destroy the Lava Troll Menace` as before |
| TH3 | Listen as he dies | - | The sewer ambience still switches from monsters to quiet. The vanilla bookkeeping is untouched -- the give was appended, not substituted |
| TH4 | Kill the ordinary trolls, tough and super included | - | **No** hide from any of them. Only the chief carries one, deliberately |
| TH5 | Take the hide to Quinn | - | He takes it, removes it from the pack, and goes to `850 troll hide turned in` |
| TH6 | Peace route instead: ask the chief for a hide (`133 the hide`, or `30 troll trade`) | - | He hands one over as before. Unchanged by this fix |
| TH7 | Peace route, then desecrate the field and kill the angry chief | - | A hide, exactly one. His generator got the same give, so both chiefs behave alike |
| TH8 | Already hold a hide, then kill the chief | - | A second one. Harmless, and the same as vanilla's behaviour for a Titan heart |

## 0.27.0 - Fernand, the fourth attempt (FAILED - superseded by 0.28.0)

Nothing to test. This attempt gave him a dedicated released-state node reached by specifier swaps
fired from canned objects, and the swap never ran -- like the three before it, it edited a reply the
player could not reach. The cause and the working fix are in the 0.28.0 section above, which carries
the test cases; the swap objects are deleted.

## 0.27.0 - hover-text barks, a voice per family and a sub-bank per type

67 cans, 71 lines. Each creature draws from its family's shared lines plus its own type's sub-bank, so
a thief archer and a thief boss say different things and neither says a soldier's line. Roughly one
attack in four. Can edits, so each needs a save that has not entered the area.

| # | Step | Say | Expect |
|---|---|---|---|
| BK1 | Fight thieves | - | Floating text **over the thief's head**, not in the combat log |
| BK2 | Fight a thief **boss** and a thief **archer** in the same run | - | Different registers. The boss gives orders -- *"Hold him! He is worth more breathing!"*; the archer talks range -- *"Keep your distance from him!"* |
| BK3 | Fight the same thief for a long stretch | - | **It varies.** One creature should not repeat one line. This is the fault the first build had |
| BK4 | Act 7, English soldiers: a Super and a Bow | - | Officer *"Not one step back, do you hear me!"* against archer *"Nock and draw!"* -- and no thief line from either |
| BK5 | Fight Snakebreed, including a Venom and a Boss | - | Sibilant throughout; Venom talks poison -- *"Feel it ssspreading?"*; stage directions like *&lt;It rears to its full height&gt;* |
| BK6 | Watch the frequency over a long fight | - | About one bark in four attacks. **If it reads as chatter this is the row that fails** -- the fix is one Item Count |
| BK7 | Check the combat log | - | Barks are **not** in it. `Include In Log=0` |
| BK8 | Fight `Snakebreed Summoner`, and both PROBE archers | - | No bark. All three have an attack slot already in use and were deliberately skipped |

## PROBES - deploy-only, on top of 0.27.0. NOT in any release

Re-applied by hand after 0.27.0 shipped. They live as **uncommitted modifications** to two tracked
cans, so the release version is one command away:

    git checkout -- "files/Resources/Monster Cans/Thugs/Theif3 Bow.can"                     "files/Resources/Monster Cans/Thugs/Theif4 Bow.can"

then reinstall. **Gate 0 fails while they are installed** -- `check_no_probes` rejects any can whose
display name begins `PROBE `, so a release cannot be cut over them by accident. That failure is
expected and is the guard working.

Both wear their names in-game and in the combat log: **PROBE A Strafe** and **PROBE B Step**. Neither
carries a bark -- probe A because the bark would sit *inside* the `CStrafeAttackAI` block it installs,
so a load failure could no longer be blamed on the class rather than the field

Two experiments deployed 2026-09-30, both on bow thieves in the RED FILE bonus level: 31 `Theif3 Bow`
and 22 `Theif4 Bow`, neither touched by the backstab or Sniper work, which were Super-tier only.

**If the game refuses to load the bonus level or the sewers, that is probe A answering**, not a
regression. Say so and both come straight out.

| # | Step | Say | Expect |
|---|---|---|---|
| PA1 | Enter the bonus level | - | It loads. A DataCrash naming a field means `CStrafeAttackAI` is real but takes different fields -- **record the field name**, it is the whole answer |
| PA2 | Fight a **`Theif3 Bow`** (the plain one, not Tough or Super) | - | Watch its feet. Does it **circle** you, or close and shoot like every other archer? |
| PA3 | If it circles, which way, and does it keep facing you | - | Direction and facing decide whether four unused attack AIs are usable |
| PA4 | If it behaves exactly as before | - | `CStrafeAttackAI` is a registered stub. Question closed, and worth knowing |
| PB1 | Fight a **`Theif4 Bow`** | - | After each shot it should **displace about 120 units**. Does it move at all? |
| PB2 | Move around it and watch which way it steps | - | **Circles you as you move** = angle is relative to the instigator, flanking is buildable. **Always the same compass direction** = absolute, flanking is not |
| PB3 | Fight one near a wall or a corner | - | Does it **slide through** the wall? If so it is timed displacement, not navigation -- good for knockback, useless for flanking |
| PB4 | Note whether it still shoots normally between steps | - | A displacement that interrupts shooting is a different cost than one that does not |

## 0.26.0 - the combat plan, parts 1, 3 and 5

Three independent changes. **Judge each separately** -- that is what these rows are for.

### Item 1, Sniper on the thief archers

Needs a save that has not entered the sewers or the bonus level. Super tier only.

| # | Step | Say | Expect |
|---|---|---|---|
| SN1 | Fight a **Super** bow thief, save, run `savecheck events latest --combat` | - | Critical hits from the archer, far more often than from a base or Tough bow thief |
| SN2 | Fight base and Tough bow thieves | - | Unchanged. Only the Super pair carries it |
| SN3 | Fight a `Thug3 Bow` or `Thug4 Bow` anywhere | - | Unchanged. Thugs do not share the new races |
| SN4 | Judge whether the bonus level is now unfair at range | - | **The row that decides whether this stays.** 100 bow thieves stand there |

### Item 3, the Assassin Masters telegraph

Slave Pits, act 1.

| # | Step | Say | Expect |
|---|---|---|---|
| TG1 | Fight an `Assasin Master` | - | Roughly one attack in four spawns a visible effect on him, pauses about a second, then lands an extra hit |
| TG2 | Watch for the pause | - | **The point of the item.** If the warning does not read as a warning, it failed even if the damage lands |
| TG3 | Compare Super against base | - | Same shape, bigger extra hit: 12-22 against 6-12 |
| TG4 | Judge whether it makes the fight more readable or just longer | - | The row that decides whether this stays |

### Item 5, the Bonecaller's wounded wave

Act 4, the Doomed Plateau. Needs a save that has not entered it.

| # | Step | Say | Expect |
|---|---|---|---|
| PH1 | Fight a Bonecaller down past **40%** health | - | It raises a burst of ghouls once, with the summoning effect. 3, 4 or 5 by tier |
| PH2 | Keep fighting below 40% | - | The burst does **not** repeat. It is a threshold crossing, not a state |
| PH3 | Kill one from above 40% in a single burst of damage | - | Crossing below still fires it, or it dies first. Either is acceptable; note which |
| PH4 | Judge whether the Plateau is still winnable | - | The row that decides whether this stays. The only item that adds enemies mid-fight |

## 0.25.7 - Fernand's conversation opens

**Needs a character who has not yet recruited Fernand** -- this is an entity change and the old
interaction is snapshotted into any save that already triggered it.

| # | Step | Say | Expect |
|---|---|---|---|
| FC1 | Recruit Fernand, then walk up to him | - | A **conversation** opens, not a floating line over his head. This is the whole release |
| FC2 | In it, choose *"Wait here, Fernand"* | - | He stops following, and `savecheck grep "Fernand Is Waiting"` reads 1 |
| FC3 | Talk again | - | Only *"Walk with me again"* -- the gating from 0.25.4 finally has a conversation to run in |
| FC4 | Use the stat bar's **Companion Follow / Stop Following** toggle instead, then talk | - | That stops him following without releasing him, and does not touch the variable. The dismiss line shows; choosing it sets the variable and the rejoin appears after |
| FC5 | On a save that already recruited him before 0.25.7 | - | Still the old balloon. Expected, and the reason this row exists |

## 0.25.5 - the Knight of Saladin's replies are gated

Act 8, `02 Shifting Dunes`. `KS1` is the state that never worked.

| # | Step | Say | Expect |
|---|---|---|---|
| KS1 | Meet him, do **not** recruit, then talk again | - | Only *"Let's go."* is offered. **No** "Hold this ground" -- he is not with you to dismiss |
| KS2 | Recruit him, then talk | - | Only *"Hold this ground and wait for me."*. **No** "Let's go." |
| KS3 | Dismiss him, then talk | - | *"Do you need my help again?"* with "Yes, please rejoin me." -- the `666 Rejoin` node |
| KS4 | Rejoin, then talk | - | Back to only the dismiss line |
| KS5 | Recruit him the first time through `30 go` | - | Works as before; that node still has its default reply |
| KS6 | Cycle dismiss and rejoin three times, then talk | - | Still exactly one of the two replies, never both and never neither. The variable must not drift |
| KS7 | `python tools/savecheck.py grep "Saladin Knight Follows" --save latest` | - | 1 while he follows, 0 or absent otherwise |

## 0.25.4 - Fernand's replies are gated

| # | Step | Say | Expect |
|---|---|---|---|
| FG1 | With Fernand **following**, talk to him | - | Only *"Wait here, Fernand"* is offered. **No** rejoin line |
| FG2 | Dismiss him, then talk again | - | Only *"Walk with me again"* is offered. **No** dismiss line. This is the reported bug |
| FG3 | Rejoin, then talk again | - | Back to only the dismiss line. The pair alternates cleanly |
| FG4 | Dismiss him, walk to another district, talk to him there | - | Still only the rejoin line. The state is on the player, not the Port District map |
| FG5 | On a save dismissed **before** 0.25.4 | - | The dismiss line shows once; choosing it is harmless and switches him to the rejoin line thereafter |
| FG6 | `python tools/savecheck.py grep "Fernand Is Waiting" --save latest` | - | Reads 1 while he waits, absent or 0 once he rejoins |

## 0.25.3 - Fernand can be taken back

Port District, after saving Juan. Needs a character who can recruit him (Speech 20 or Barter 20 at the
ask) or a save where he is already following.

| # | Step | Say | Expect |
|---|---|---|---|
| FD1 | Recruit Fernand, then talk to him | - | *"Where you go, I follow."* now offers replies instead of closing. That node is his only interaction once he has joined |
| FD2 | Choose *"Wait here, Fernand. I will come back for you."* | - | He stops following and stays put, and answers that the Armada can spare him a while longer |
| FD3 | Talk to him again and choose *"Walk with me again, Fernand."* | - | **He rejoins.** This is the bug: before, there was no route back at all |
| FD4 | Release him by any means other than that reply, then talk to him | - | The rejoin reply is still there. It is deliberately ungated so he is recoverable from any state |
| FD5 | Rejoin without meeting Speech 20 or Barter 20 | - | Allowed. The recruit check is not re-applied -- he has already been persuaded once |
| FD6 | Take him through a map transition after rejoining | - | He follows normally, as on the first recruitment |

## 0.25.2 - the trees that named themselves

Four conversations that crashed the game outright. Each row is "talk to them and the game survives".

| # | Step | Say | Expect |
|---|---|---|---|
| SR1 | Port District: board the ship and talk to **Captain Isabella** | anything | The conversation opens. No "infinite loop while trying to load" dialog |
| SR2 | Take **Grace** as a companion, then dismiss her with *"Wait here. I will come back for you."* | - | She stays put and a balloon appears over her. That balloon is the line that crashed |
| SR3 | La Calle Perdida: complete a favour for **Brambles** | - | One of three thank-you balloons appears, varying between runs |
| SR4 | Wilderness: take **Grumdjum** as a companion | - | Conversation survives, and walking up to him again opens the companion nodes, not the first-meeting ones |
| SR5 | Dismiss Grumdjum, then approach him again and rejoin | - | Both transitions survive; his interaction rewires each time |
| SR6 | Alamut: dismiss the **Knight of Saladin** companion and rejoin him | - | The rejoin node opens |
| SR7 | Run `python tools/validate.py` | - | Passes. Reintroducing any self-reference must exit 1 |

## 0.25.1 - the startup crash

Any save, or none. `SU1` is the whole release.

| # | Step | Say | Expect |
|---|---|---|---|
| SU1 | Launch the game | - | It reaches the main menu. No "DataCrash Explanation - Fatal Not Found Error" dialog naming `Skills/Fighting/Melee` |
| SU2 | Load any save and check the character screen | - | Normal. Nothing about this touched the player |
| SU3 | Meet Grace O'Malley on the act 7 landing beach and let her fight | - | She survives it -- 190 AC, 165 HP, OneHandedMelee 110, Evasion 55, which is what 0.19.0's review intended |
| SU4 | Run `python tools/validate.py` | - | Passes. Reintroducing `Skills/Fighting/Melee` must make it exit 1 |

## 0.25.0 What They Were Built To Do - the Priestesses cast

Act 7. Needs a save that has **not yet entered** `05 Exalted Chambers`, `09 Secret Chamber` or
`10 Inner Sanctum`. The Priests are the control: they behaved this way already.

| # | Step | Say | Expect |
|---|---|---|---|
| PC1 | Fight a **Priestess** in act 7 | - | She casts **Spike** at you instead of only closing to melee |
| PC2 | Fight a **Priestess Tough** | - | Fire Orb or Spike, varying between casts |
| PC3 | Fight a **Priestess Super** in `05 Exalted Chambers` | - | Fire Orb, Lightning Bolt, Spike or Static Charge, varying |
| PC4 | Watch a Priestess of any tier over several attacks | - | She does **not** cast `ENEMY Magical Shield` -- that is the Priests' opener, and no Priestess race knows it |
| PC5 | Fight a **Priest**, **Priest Tough** or **Priest Super** | - | Unchanged: shield first, then Fire Orb / Spike / Lightning Bolt |
| PC6 | Judge the Exalted Chambers approach as a whole | - | Meaningfully harder: eleven Priestesses and six Supers in that room now cast. **This is the row that decides whether the tier stays** |
| PC7 | The Inner Sanctum (14 of them) and the Secret Chamber (12) | - | The same change, and the same question |
| PC8 | Watch one **Priestess Super** over four or more casts | - | She works through all four spells before repeating any. She should not cast the same one twice running |
| PC9 | Watch a **Priestess Tough** | - | Fire Orb and Spike alternate rather than randomly repeating |
| BL1 | Fight the **Bonecaller** on the Doomed Plateau | - | Roughly one attack in four is a summon: a spellcast animation, then ghouls rising beside him with a summoning effect |
| BL2 | Count what the base Bonecaller raises across a whole fight | - | Four ghouls, then no more. Tough raises five, Super six |
| BL3 | Check what comes up | - | Ghoul Male and Ghoul Female and their Tough/Super variants -- the Plateau's existing `ghoul clone generator`, not a new creature |
| BL4 | Kill the Bonecaller mid-summon | - | No orphaned clone generator is left behind and nothing keeps spawning |
| BL5 | Talk the Bonecaller down instead, as 0.21.0 allows | - | He stops summoning along with everything else. The stand-down is unaffected |
| BL6 | The Old Man of the Mountain and the finale | - | **Unchanged in every respect.** No file for that fight was touched |

## 0.25.0 What They Were Built To Do - the thieves of Barcelona backstab

Act 1. Needs a save that has **not yet entered** the Slave Pits or the sewers -- these are can and race
changes, so they reach only thieves spawned after the install. `BS1` is the row that matters most: it
checks that presetting an engine-owned attribute did not break the creature.

| # | Step | Say | Expect |
|---|---|---|---|
| BS1 | Walk into `Sewers/01 Sewer Main Entrance` and just **look** at a thief before fighting | - | He appears normally, walks at normal speed, is visible and targetable. **If thieves are invisible, creeping, or missing, stop and revert** -- that means `Sneak Enabled` reached the engine's sneak state after all |
| BS2 | Fight a `Sewer Theif4 Sword` head-on, facing him | - | No backstab line in the log. The facing condition needs at least 90 degrees of difference |
| BS3 | Engage one thief, let a **second** close on you from behind, then **save** | - | `python tools/savecheck.py events latest --backstab` prints a line with the **thief** as attacker: *"... sneaks up on ... and hits for ... (25 percent backstab bonus)"*. This is the whole point of the release. The log is a rolling 300 events, so save soon after the fight |
| BS4 | Same in `02 Thieves Congregation`, where 51 thieves spawn | - | Same, and more often -- crowds make flanking happen by itself |
| BS4a | **The RED FILE preorder bonus level**, entered from the Gate District, on a save that has never been in it | - | The densest test in the game: **90** spawns carry the new races (Pale x33, 4 Sword x23, 3 Mace x12, plus Tough). Crowds this size are where the behind-attack geometry should happen on its own. Its 100 bow thieves must **never** produce a backstab line |
| **BS3/BS4a: PASSED 2026-09-29** | Fought surrounded in the RED FILE bonus level, saved, read the log | - | `Thief Swordsman sneaks up on Antonio Gula and hits for 8 (9 Slashing Damage) (25 percent backstab bonus)` -- 1 backstab in 7 landed melee thief attacks. Note the log **wraps**: the bonus text lands on a second row |
| BS5 | Note the bonus percentage in the log across tiers | - | 25 for base, 35 for Tough, 50 for Super |
| BS6 | Fight a `Sewer Theif3 Bow` or `Theif4 Bow` | - | **Never** a backstab line. Archers were deliberately left out |
| BS7 | Judge whether the sewers are harder in an interesting way or simply harder | - | **The row that decides whether the release stays.** Remember AC and HP also rose with the repoint |
| BS8 | Compare a `Thug4 Sword` in the Gate District, or `Thug Boss` in act 8 Alamut | - | Unchanged -- still 95 AC, no backstab. Thugs share nothing with the new thief races |
| BS9 | Kill a thief and check its XP and drops | - | Unchanged. The repoint touched `Race=` only; XP lives on the can |
| BS10 | `1 Barcelona/Slave Pits` at low level | - | Survivable. If a level-2 character is being killed by 25 percent backstabs here, drop the base tier to 0.15 before anything else |

**Note on BS1.** The enemies do **not** visibly sneak, and that is by design rather than a failure. The
engine's sneak setter writes two separate things -- the real sneak-state field at `+0x134`, which drives
movement and rendering, and the attribute the backstab gate reads. The race preset sets only the second,
so a backstabbing thief walks, looks and fights exactly as before. The **only** observable difference is
the damage number and the log line.


## 0.24.0 - the register

Act 3, Montaillou. Needs a **Knight of Saladin** who has not yet spoken to the Bishop of Pamiers in
`05 Church Interior`, and a save that has never entered `05 Church Interior` or `01 Hamlet Exterior`.

| # | Step | Say | Expect |
|---|---|---|---|
| RG1 | As a Knight of Saladin, meet the Montaillou gate guard **before** visiting the church | - | The vanilla welcome: *"you are an ally of the Templars - and thus welcome here"* |
| RG2 | Go to the church and talk to the Bishop of Pamiers | - | A new reply: *"Your grace. I am a sworn knight of the Order of Saladin."* |
| RG3 | Take it | - | He writes you down. The quill does not stop |
| RG4 | Leave, and give the guard the same Saladin answer again | - | The **cold** version. He still lets you pass; he is no longer pleased about it |
| RG5 | Repeat RG2 as a sylvant, a feralkin and a demokin | - | The introduction is offered on all four openings, including the untainted one, which offers no order introduction at all in vanilla |
| RG6 | As a Knight of Saladin, never speak to the Bishop, and use the guard repeatedly | - | The warm welcome every time. The cost is only paid if you introduce yourself |
| RG7 | As a **Templar** or an **Inquisitor**, do RG2 | - | Their own introductions, unchanged, and no register entry |
| RG8 | Carrying no order, talk to the Bishop | - | His vanilla openings, unchanged |
| RG9 | After RG3, check the Bishop's other business still works -- the witch, the mayor, the gem | - | All unchanged. The register is a flag, not a gate |
| TB1 | As a **Knight Templar** with 150+ gold, eat in the Montaillou tavern and let the Cathar toughs start on you | - | The line *"I'm not a priest, nor are they my friends"* is **absent** |
| TB2 | Take the reply that is there instead | - | *"No. I am a knight of the Temple, and I have eaten at the mayor's table this week."* then `61 the knights` |
| TB3 | Pay the hundred and fifty | - | `100 Welcome`, no fight, and **150 gold gone** |
| TB4 | Repeat carrying **less than 150 gold** | - | The paying reply is absent. Only the two answers that start the brawl remain |
| TB5 | Take either of those instead | - | `40 Super Insult` and the brawl, as every other wrong answer in that tree does |
| TB6 | Repeat the whole scene as an **Inquisitor** | - | Unchanged: his own reply, and the disclaimer still closed to him as in vanilla |
| TB7 | Repeat as a **Wielder** | - | Unchanged -- he still talks his way to `100 Welcome` for free at `70 Challenge Answer` |
| TB8 | Repeat carrying **no order** | - | The disclaimer is available exactly as in vanilla, and no Templar reply appears |
| HC1 | Sworn to the **Goblin Horde**, buy from Alvaro at the Crossroads | - | `21 the horde price` and his speech about the three carts, before any shop opens |
| HC2 | Buy something and compare the price with a non-Horde character | - | Visibly worse: 1.5 against 1 |
| HC3 | Repeat at **high karma**, where he offers his special supplies | - | Also gated. The special stock does not dodge the surcharge |
| HC4 | Take *"Keep them"* | - | `10 goodbye`, no shop, no hostility. He is a trader, not a guard |
| HC5 | Repeat carrying **no Horde allegiance**, at both normal and high karma | - | `Vendor 1 Inventory` and `Good Karma Store for Alvaro` exactly as in vanilla |
| HC6 | As a Horde member, buy from **Hub'blub** in the warrens | - | Still 0.75. The Horde's own discount is untouched |

## 0.23.0 - what the Crescent is worth

Act 8, the Knights of Saladin. `SR16`-`SR29` need only a knight of any rank; `SR1`-`SR15` need an
**Exalted** knight: take the Dream Djinni initiation,
take Jafar's Montaillou or Montserrat errand, and find all five green Way Crystals. `SR5`-`SR8` need a
knight who is **not** Exalted, and one of each other order as a control. Needs a save that has never
entered `02 Shifting Dunes`.

| # | Step | Say | Expect |
|---|---|---|---|
| SR1 | As an Exalted **male** knight, meet the Knight of Saladin in the dunes | - | *"Salaam - Exalted... Command me, Brother"* -- not the vanilla "You do much honor to Saladin's name" |
| SR2 | The same as an Exalted **female** knight | - | The same greeting, addressed Sister |
| SR3 | Ask what the order says about this place | - | `24 the standing order`: the oath every Aswaran takes, and that you are the one who is nearest |
| SR4 | Reach the Old Man and read the replies at `40 ruse` | - | **Two** Saladin lines: the vanilla-era *"I am what came back"* and the new standing-order one. Both lead to the fight |
| SR5 | Repeat SR1 as a knight who took the initiation but **not** all five crystals | - | The vanilla Brother/Sister greeting. No Exalted line, no standing order, no second Old Man reply |
| SR6 | Repeat as a **Templar** | - | The vanilla Knight Templar greeting and the tribute reply, unchanged |
| SR7 | Repeat carrying **no order** | - | `1 Conversation Start`, unchanged |
| SR8 | As an Exalted knight, dismiss the companion and pick him up again | - | `666 Rejoin` and `3 Return` behave exactly as before; the rank greeting is a first-meeting only, as vanilla's are |
| SR9 | As an Exalted knight, take `24 the standing order` and then *"Then come the whole way in"* | - | `25 the order rides`, and he agrees to come as far as the Old Man's door |
| SR10 | Walk on into 03 Sand Dragon, then 04 Maw of the Assasin | - | A Knight of Saladin is standing at each arrival and fights with you. He is talkable and gives `3 Return` |
| SR11 | Continue through 05 Acid Wash, 06 Chamber of Torment and 07 Dark Temple | - | The same on each. He is the 220 HP / 215 AC companion race, not a citizen |
| SR12 | Enter 08 Final Encounter | - | **He does not follow.** The finale plays exactly as vanilla, with no extra body in the scripted scene |
| SR13 | Do **not** take the ride reply, then walk in | - | No escort on any of the five maps. The act is unchanged |
| SR14 | Take the ride reply, then walk *backwards* to a map you already crossed | - | No escort there until you leave and re-enter -- the checker is read on arrival. Recorded, not a defect |
| SR15 | Reach the Maw as a Templar or with no order | - | No escort, no ride reply, no Exalted greeting |
| SR16 | As **any** Knight of Saladin (rank does not matter), talk to the desert merchant in `01 Desert Sprawl` | - | A new first reply about riding for the Sultan's house, then `40 the order` |
| SR17 | Buy something, then compare with a non-Saladin character | - | Visibly cheaper: his multiplier drops 2.0 to 1.5 |
| SR18 | Talk to him again, take the Saladin reply's node a second time | - | The reply is gone -- the discount lands once, not once per conversation |
| SR19 | As a Knight of Saladin with Barter 40 and then 95, haggle after taking the discount | - | Both haggle steps still work and stack on top: 1.5, then 1.4, then 1.3 |
| SR20 | Open his shop as anyone at all | - | `Great Healing` x3, `Superior Healing` x2 and `Supreme Healing` x1 on the shelf -- Quinn's tiers, available in act 8 for the first time |
| SR21 | Buy and drink a Supreme Healing bought from him | - | Heals as the herbalist's does. It is the same addition on the same base potion |
| SR22 | As a Knight of Saladin, walk up to Fazeem in `01 Desert Sprawl` **without** having spoken to the merchant | - | A first reply about the men in black who use this road. The Speech 70 route is still absent until the merchant mentions them |
| SR23 | Take it, then answer his challenge truthfully | - | `31 the bargain`, and the bird men turn on the Assassins -- the same outcome the con produces |
| SR24 | Check your gold before and after | - | **No payment.** The con's gold is on the Barter branches only; the honest route pays nothing |
| SR25 | Check XP | - | The same `Talked Fazeem into Fighting Assassins XP` award the con gives |
| SR26 | Afterwards, walk into the Assassins on that map | - | Fazeem and the bird men near him fight them, as they do after the con |
| SR27 | As a Knight of Saladin with Speech 70 who **has** heard the merchant | - | Both routes offered. The Saladin reply sits above the Speech one and does not replace it |
| SR28 | Take the new route's "I think I will kill you instead" or its exit reply | - | `Make All Bird Men Attack`, exactly as every other exit in that tree |
| SR29 | Approach Fazeem carrying no order | - | The vanilla encounter, unchanged |

## 0.22.0 - the Talker and the Thief

Four sections' worth of checks ship in this one release: `DM1`-`DM8` (the Druid Master reads your order),
`DS1`-`DS8` (she can be talked down), `SN1`-`SN9` (Sneak), and `AF1`-`AF6` (triggers that must fire on a
second visit). The act-7 rows all need a save that has **never entered** the act-7 maps -- new map parts
do not appear on a save that has already visited a level.

### 0.21.5 - the field the builder forgot

Repeat-visit triggers. Each of these is a polygon you are meant to enter, leave, and enter again after
something changed elsewhere; before this release they lacked the field that re-arms them.

| # | Step | Say | Expect |
|---|---|---|---|
| AF1 | In `Mountain Pass`, walk through a charm sweep polygon **before** breaking the ogre charm | - | Nothing happens |
| AF2 | Break the charm, then walk back into that same polygon | - | `the charm lifts` fires. This is the case the missing field put at risk |
| AF3 | Repeat AF1/AF2 in `Ogre Cave` and `Ogre Sprawl` | - | Same behaviour on all ten sweeps |
| AF4 | In `4 Undercroft`, cross `guard room poly`, leave the room, cross it again | - | It responds on the later crossing as well as the first |
| AF5 | In `9 Burial Chamber`, secure the relic, then re-enter Jehanne's polygon | - | She reacts to the relic being secured |
| AF6 | Every one-shot trigger from earlier releases -- the gate parley at the Grove, the Montaillou gate strip, the four Misc Crypt hovers, the two cave hovers, the two Crossroads Siege hovers, the Plains rogue strip | - | Unchanged. They still fire exactly once |

### 0.21.3 - act 7's Speech route and the three Sneak cans

Act 7. `DS1`-`DS8` need a character with **Speech 130 or better** who has not yet reached the Druid
Master; `SN1`-`SN9` need one with **Sneak 25**, one with **Sneak 10-19**, and one with **Sneak 20+**.
All of it needs a save that has **never entered** the act-7 maps -- new map parts do not appear on a
save that has already visited a level.

| # | Step | Say | Expect |
|---|---|---|---|
| DS1 | Reach the Druid Master at Speech 130 and take *"And what kind of power do you offer?"* first | - | No Speech reply on the temptation node. The route is on the lore branch only |
| DS2 | Ask *"How are you going to raise the dragon?"*, then sit through `30 ley lines` and `40 ley lines 2` | - | A Speech-icon reply about Richard's blood and the grave nine paces away |
| DS3 | Take it | - | `50 the bloodline`: *"If you are wrong I lose a night of work. If you are right I lose the hill"* |
| DS4 | Press it home | - | She calls the fires out, `51 the fires out` plays as a balloon, **3,000 XP**, and **no fight starts** |
| DS5 | After DS4, walk the chamber | - | Controls work, the camera has let go, the ambush door stays shut, no golems, and she does not attack |
| DS6 | Walk out to the Alamut crossing without touching her | - | `Stop the Druids` completes and the 4,000 XP fires exactly as it does after killing her |
| DS7 | Repeat at Speech 129 or below | - | The Speech reply is absent; the three vanilla replies and the four faction refusals are unchanged |
| DS8 | On `50 the bloodline`, take the other reply instead | - | The normal fight, ambush and all |
| SN1 | At Sneak 25, enter 02 Temple Initiate and open the secret door at the south-west wall | - | A balloon about two lines of wear in the flagstones, **250 XP**, the room revealed, the strongbox usable |
| SN2 | After SN1, walk to the far end of that room | - | A passage that relocates straight to 05 Exalted Chambers, skipping 03 and 04 |
| SN3 | At Sneak 10-19, open the same door | - | Only the draught balloon. No strongbox, no passage |
| SN4 | At Sneak 9 or below, open the same door | - | Nothing at all, exactly as vanilla |
| SN5 | Reach 05 at Sneak 20+ **with sneak mode switched on** and cross the floor in front of her | - | A fifth reply on her opening node naming the men behind the wall |
| SN5a | Cross that same floor at Sneak 20+ **not** sneaking, then step back out, switch sneak on and cross again | - | No reply the first time; the reply is there the second time. The check retries |
| SN6 | Take it | - | The fight starts and her golems appear, but **the ambush door stays shut and no soldiers come out of it**. 500 XP |
| SN7 | Repeat SN5 as a sylvant, a feralkin and a demokin | - | The same reply on each of the three race openings, each node's own refusals still reading correctly |
| SN8 | Reach 05 at Sneak 19 or below, sneaking | - | No fifth reply. The vanilla fight, ambush included -- the toggle alone is not enough |
| SN9 | Come back into 02 from 05 the vanilla way, having never passed a Sneak check | - | The secret opens on arrival as it always did, and no Fixt balloon plays |

### 0.21.2 - the Druid Master hears you

Act 7, the Inner Sanctum's boss. Needs a character who has **not yet reached the Druid Master**, and one of
each order to see all four lines. Her race greetings are vanilla and unchanged.

| # | Step | Say | Expect |
|---|---|---|---|
| DM1 | Reach the Druid Master as an **Inquisitor** and hear her temptation, then look at the replies | - | A refusal no one else gets: *"You have just offered the destruction of the Holy Office to a sworn officer of it."* |
| DM2 | The same as a **Wielder** | - | *"You are offering me the one thing I have ever wanted, and you are offering it with a dragon."* |
| DM3 | The same as a **Templar** | - | *"My Order crossed a sea to keep a relic out of your hands, and you have just told me why."* |
| DM4 | The same as a **Knight of Saladin** | - | *"You are promising to settle a quarrel I am not in."* |
| DM5 | The same carrying **no order** | - | Her three vanilla refusals and the question about the ley lines. None of the four new lines appear |
| DM6 | Pick any of the four | - | The fight starts exactly as it does from her vanilla refusals -- same `Fighting the Druids Last Chamber` relay, same Fight Icon |
| DM7 | Check her **race** greetings still work: arrive as a Sylvant, a Feralkin, a Demokin and a human | - | Four different openings, unchanged from vanilla. The race layer is hers, not ours |
| DM8 | Ask *"How are you going to raise the dragon?"* first, then refuse with a faction line | - | `30 ley lines` then `40 ley lines 2` as before, and the faction refusals are still offered afterwards |

### 0.21.1 - the Daeva

Act 3, Montaillou, and one act-1 decision that feeds it. Needs a character who has **not yet
entered `01 Hamlet Exterior`**. `DV1` needs the **Ring of the Prophet** from `15 Witch SecretCave` and `DV2`
the **Amulet**. `DV7`-`DV13` each need a different outcome at the Barcelona Inquisition Pit -- the wizard lured
to the demon, the crosses broken yourself, the demon killed, or never met -- so they want four characters, or
four saves before that choice.

| # | Step | Say | Expect |
|---|---|---|---|
| DV1 | Carrying only the **Ring of the Prophet**, cross the Prophet Polygon in the hamlet | - | `4 Ring`: *"You bear a powerful relic, mortal. Something of the prophet Zarathustra's if I'm not mistaken."* In vanilla this played the Amulet's line instead |
| DV2 | Carrying only the **Amulet**, same approach | - | `4 Amulet`, unchanged: *"Ah, you have a bauble from that accursed prophet."* |
| DV3 | Carrying **both** relics | - | The Amulet's line. The fork checks the Amulet first, so it wins the tie |
| DV4 | Carrying **neither** | - | The scene does not trigger at all, exactly as before -- the outer check is unchanged |
| DV5 | Fail to kill the Daeva in Montaillou and let it break off | - | `3 Undefeated`: *"this exertion has left me ravenous... that lake town has all of my favorite flavors."* In vanilla it left in silence |
| DV6 | Compare with the Toulouse escape on Titan Village | - | `35 teleport out of toulouse` still plays there. The two lines are a pair and should now read as one chain |
| DV7 | In act 1, get **Faust lured to the demon** so it frees itself, then reach the Daeva in Montaillou with **no relic** | - | The clone loop stops, the true form comes up, and **the Daeva of Pain arrives and fights it**. HP 900 / AC 200, tagged `Player Friend` |
| DV7a | Watch exactly where the Daeva of Pain appears on the Faust route | - | At the **Giants Cave mouth, (280,260)**, behind you and facing the fight -- **not** inside the shapeshifter. He spawned on the true form's own point until this was caught |
| DV7b | Watch the arrival to the end without acting | - | A **cutscene**: camera moves to (421,345), and the two of them trade three barbs -- his, hers naming him **Aeshma**, then his -- before the sequence ends and they fight. He should not be clickable during it |
| DV7c | Try to click him during or after the barbs | - | Nothing. The inherited `GetCloseThenTriggerAndFight` specifier is gone; on this route he is a combatant, not a conversation |
| DV9a | On the **lesser** debt route, walk to where your spirit warns you something is ahead | - | He is **sitting there**, at (1377,1058), waiting and not fighting. The spirit's warning and the informant are the same beat |
| DV9b | Talk to him | - | `1 the warning`, then `2 the name`. Taking the name sets `Fixt knows Nanghaithyas name` |
| DV9c | Refuse him at `3 declined`, then reach the shapeshifter with Speech 95+ | - | **No Speech reply.** The route now needs the name to have actually been given, not merely the demon freed |
| DV9d | On the **Faust** route, check the wall at (1377,1058) | - | Nobody there. The informant seat is gated on the lesser debt **and not** the larger, so the two routes never both fire |
| DV8 | Check the true form is killable on that run | - | It should die and stay dead. It is the bound template: same race and 2750 XP, with the 20-25 HP/sec heal removed |
| DV9 | Instead **break the crosses yourself**, then reach it with **no relic and Speech under 95** | - | The loop still breaks and the bound form comes up, but no ally arrives |
| DV10 | Break the crosses yourself, then reach it with **no relic and Speech 95+** | - | A new reply: *"Nanghaithya. A demon in a Barcelona cell gave me your name, and it owed me the favour."* It opens `2000 using speech`, which was relic-only |
| DV11 | **Kill** the demon in act 1 instead, then fight the Daeva with no relic | - | Nothing changes. The loop is unbreakable and the fight cannot be finished, exactly as vanilla |
| DV12 | Never visit the demon at all, then fight with a relic | - | Unchanged vanilla behaviour: `Prophet Polygon` puts up the ordinary healing true form |
| DV13 | Watch what happens on the wave where the debt fires | - | Expect the last clones to spawn **alongside** the true form. The debt check is first in `Form Relay` but deactivating a relay mid-array may not abort it. Note whether that reads well or badly |

### 0.21.0 - the Doomed Plateau

Act 4. Needs a character who has **not yet entered `7 Doomed Plateau`** -- all of it is level parts.
`DP2`-`DP5` need Speech 80+, Divine 80+, or Wielder standing, and `DP4` needs Speech 110 or Divine 80.
`DP5b`-`DP5f` need **karma below 600**, and `DP5g` a high-karma character. `DP16` is on a different map.

| # | Step | Say | Expect |
|---|---|---|---|
| DP1 | Enter `7 Doomed Plateau` and find the Bonecaller, north-east of the slope | - | A lich in rotted mail that **does not attack on sight**: `1 the bonecaller`, *"you are the first new thing on this plateau in ninety years"* |
| DP2 | Talk to it as a **Wielder**, or with **Divine 80+**, or **Speech 80+** | - | A route into `10 bound`. Each order of approach has its own line; all three reach the same node |
| DP3 | Ask *"What are you?"* first | - | `5 the answer` -- it raises what falls, the knights cut it down, and tomorrow it raises them again |
| DP4 | At `10 bound`, use **Speech 110** or **Divine 80** | - | `20 stands down`. It stops, and is retagged into the other army |
| DP5 | Watch it after it stands down | - | **The horde attacks it and it fights back.** It is retagged `Scripted Custom 2,Undead` and pointed at `Enemy`, which is what all 81 horde generators target and what every horde spawn carries |
| DP5a | Check the journal XP after standing it down | - | **2000 XP**, from the anchor part `Fixt Talked the Bonecaller Down XP`. If the horde then kills the Lich, that kill XP is theirs, not yours -- 2000 is the whole of the peaceful route's award |
| DP5b | On a character with **karma under 600**, reach `10 bound` | - | A third reply: *"Keep your orders. I will open the keep for you, and you will owe me the spear."* -> `21 the bargain`. A high-karma character does not see it |
| DP5c | Take the bargain | - | 2000 XP from `Fixt Sworn to the Bonecaller XP`, and the Lich is retagged `Player Friend,Undead` pointed at `Undead` |
| DP5d | Walk it toward the keep | - | **The Templar garrison attacks it** -- they target `Player,Player Friend` -- and the horde ignores its own commander. It fights the knights |
| DP5e | After the bargain, talk to an Undead Templar | - | *"Are you a Knight? Have you been sent to reinforce us?"* has **no good answer left**: all three recruitment replies are gone, including the `<Lie>`. Only *"No, I came to destroy you"* remains |
| DP5f | On a separate run, release the Lich instead, then talk to a Templar | - | Recruitment still works. `Fixt sworn to the Bonecaller` is only set by the bargain |
| DP5g | On a **high-karma** character, check the release arm is still offered | - | Yes. The release arm is ungated by karma on purpose -- anyone may free it, only the wicked may recruit it |
| DP6 | Refuse it, or say you have nothing to say to the dead | - | It fights. HP 385/462/520 by party level, AC 80 -- easy to hit, huge pool, **immune to cold, poison and disease, and weakest to fire** |
| DP7 | Kill it | - | 1500/2000/2500 XP by tier. This is the first time anything in the game has spawned a `Boss Lich`: three races, a sprite and seventeen animations shipped with no template pointing at them |
| DP8 | Find the Bonewright, mid-slope west | - | `100 the bonewright` as it plants its standard, and the fallen around you start getting up |
| DP9 | Stand and fight near it for a minute without killing it | - | Waves keep arriving, roughly every 22 seconds. They are `Greater Skeleton` tiers from a generator it switches on |
| DP10 | Kill the Bonewright | - | `101 the bonewright falls`, and **the waves stop** -- the relay and its generator are both shut off permanently |
| DP11 | Check the Bonewright's own strength | - | HP 250/400/600, AC 175/215/300. In vanilla it ran on `Ghoul Male Large` at 150/200/275 while its own race sat unused |
| DP12 | Find the Revenant Sergeant, east of mid-slope | - | `110 the sergeant`. It is fighting the Templar knights and **has not looked at you** |
| DP13 | Bring it below **66%** | - | `111 the sergeant rallies` -- its section leaves the knights and closes on you |
| DP14 | Bring it below **33%** | - | `112 the sergeant fixates`. It abandons the battle: `Valid Targets` narrows to `Player` and it comes through its own dead |
| DP15 | Check the Templar garrison still works | - | `UndeadTemplar` unchanged: it still mistakes you for a monster, still recruits a Templar, still says *"Find Jehanne"* |
| DP16 | Check `2 Retreat of Souls` | - | Its three `Second Guardian` spawns are now at the restored strength too. They are weight 1, so they stay rare |

### 0.20.0 - Alamut

Act 8, all six tiers. Needs a character who has **not yet entered act 8** -- most of it is level parts.
`AL15`-`AL29` additionally need one who reached **Goblin Champion** in the Wilderness, and `AL26`
one who killed the goblin Khan for Torquemada in act 1. `AL37`-`AL47` need a character of each order.

| # | Step | Say | Expect |
|---|---|---|---|
| AL1 | Enter `05 Acid Wash` from `04 Maw of the Assassin` and walk west along the channel | - | `1 the channel` arrives **before** any acid: the cut channel and its fall to the west, the stone eaten smooth like a streambed, and the bowmen on the terraces who have no intention of being in it |
| AL2 | Keep going until the first wash fires | - | `2 the first sluice` as it launches -- it lets go up-slope to the east, and the channel is ready again about ten seconds later. The wash is unchanged: 20-40 Acid, `Defend Against=1`, so acid resistance still applies |
| AL3 | Stand clear, wait, then cross the same spot again | - | The wash fires again. `First Trap Trigger` is still `Trigger Only Once=0`, so the hazard cycles exactly as it shipped -- but neither balloon repeats |
| AL4 | Reach the western gate's trigger | - | `3 the second sluice`. The trigger polygon is vanilla's own, byte for byte |
| AL5 | Walk up to the switch beside the spiked gates | - | `4 the sluice control`: an iron switch at waist height, rock worn pale by hands, and the gates standing closed across the passage |
| AL6 | Press it | - | All five of vanilla's own effects -- the `Spike Door near Switch` gates open, the coffin-lid sound plays, both wash triggers deactivate, and **Disarmed trap** prints emphasised -- and then `5 the gates open` as a sixth |
| AL7 | Walk back over both wash triggers | - | Neither fires. Vanilla's two `CDeactivateAction`s are untouched |
| AL8 | Press the switch again | - | Nothing happens. The relay is `Trigger Only Once=1`, as it shipped |
| AL9 | On a fresh character, enter instead from `06 Chamber of Torment` and walk east | - | All four triggers still fire when crossed from that side, but the ordering is only guaranteed on the forward path: approaching from the west, `2 the first sluice` can arrive before `1 the channel`. Worth knowing whether that reads badly |
| AL10 | Check the combat log after AL1-AL6 | - | All five balloon texts are in the log. Every node carries `Include In Log=1` |
| AL11 | As a Wielder who killed Relican, talk to a wizard in La Calle Perdida and reach `60 Membership` | *"Did you have to pass such tests?"* | Four replies, not five. The dead *"Save your flattery and begone"* -- a Fight Icon that started no fight and closed the conversation -- is gone from this node as it already was from `50 Spirit` |
| AL12 | Enter `08 Final Encounter` carrying **Find Galileo and DaVinci** from act 6's blacksmith | - | It completes. DaVinci speaks in the opening cinematic, through `DaVinci Ending / 100 Respond ask about Tank`, so the find is dramatised and not only a journal tick |
| AL13 | Enter it carrying **Pursue the Retreating Druid Forces**, activated at act 6's crossroads | - | It completes when `Cross Regret for Player generator` hands over the `TRUE CROSS` -- the relics the Old Man is using in the ritual are the ones stolen in act 6 |
| AL14 | Reach act 8 with Grace O'Malley recruited in act 7 | - | She follows and has nothing to say, exactly as Sir Roger does. This is parity with vanilla, not a gap |
| AL15 | Reach **Goblin Champion** (`Goblin Rank` 3) with the Horde, leave the goblin Khan **alive**, then enter `01 Desert Sprawl` from England | - | Grumdjum is waiting near where you arrive. `300 companion`: *"Greetings, goblin friend... since my Khan has tasked me to aid with your quest, let us seek the Old Man in Alamut"* |
| AL16 | Ask *"Why do you want to help me?"* | - | `300 kill old man` -- the Great Khan's warriors died trying, and he wants the Old Man's brain as his fee |
| AL17 | Accept from either node | - | He joins as a companion. `300 companion quips 3` plays. Both accept replies now carry `CSetCompanionAction` |
| AL18 | Fight alongside him for a minute | - | `300 companion quips 1/2/3` shuffle roughly every 13 seconds, in rhyming couplets, anchored over him and not over you |
| AL19 | Let him drop below half health, then below a fifth | - | `300 grumdjum hurting` then `300 grumdjum hurting 2`. Each fires once |
| AL20 | Talk to him while he is your companion | - | `300 player speaks to goblin as companion`: *"What can Grumdjum do for you?"* -- not the recruitment node again |
| AL21 | Dismiss him with *"I work alone. Leave."* | - | `300 companion leaves you`, he stays put, and he calls `300 grumdjum asks to rejoin` as you pass |
| AL22 | Talk to him again | - | `300 companion joins you` **with two replies** -- it was recorded reply-less, asking a question nobody could answer. Accepting plays `300 grumdjum rejoins` |
| AL23 | Tell him *"I'd rather kill you where you stand"* | - | He actually fights. This reply had a Fight Icon and no action in vanilla |
| AL24 | Walk a little further in with the Khan alive | - | Rumjun Khan is there too, as a cameo: `500 Start in Persia`, **and it is voiced** -- all three Persia nodes shipped with the VO flag off and the recordings present |
| AL25 | Accept the Khan's offer, then decline on another run | - | `501 Excellent` and `502 Too bad`. He is not a companion either way -- he sows his own destruction, or takes his brethren east |
| AL26 | On a character who **killed the goblin Khan** for Torquemada in act 1, enter act 8 | - | **No goblin at all.** Neither generator activates. The gate reads vanilla's own `Goblin Khan is Dead` checker |
| AL27 | On a **Goblin Chum or Blooded** (rank 1 or 2), Khan alive | - | **Neither goblin appears.** Both are gated on `Goblin Horde Highlevel`, the same can the Khan gates his own top-tier replies on -- the Khan tasks a warrior to his Champion, not to an acquaintance |
| AL28 | As a Goblin Champion who killed Grumdjum at the Lake | - | The Khan appears; Grumdjum does not. The gate reads `Grumdjum Dead`, the marker his own vanilla generator sets |
| AL29 | As a Goblin Champion who never met Grumdjum at all | - | He still comes. Champion standing is the whole gate -- the Khan sent him, and his *"once again"* is the Horde's camp, not the lake |
| AL30 | Meet the Knight of Saladin on `02 Shifting Dunes` and ask *"What is inside Alamut?"* | - | `20 alamut` answers. Five replies pointed at `20 Alamut` with a capital A against a lowercase node |
| AL31 | Recruit him the **first** time you meet him, via *"Let's carry the battle to Alamut, then"* | - | He **follows you**. In vanilla this path set the companion flag without the escort AI, so he stood where he was |
| AL32 | Talk to him while he is following | - | `3 Return`, *"Salaam. May the Prophet give us strength"* -- **not** *"Do you need my help again?"*, which is what vanilla opened for an already-recruited companion |
| AL33 | Tell him *"Hold this ground and wait for me."* | - | He is released and stays. Vanilla had no dismissal for him anywhere in the tree |
| AL34 | Talk to him again | - | `666 Rejoin`. *"Yes, please rejoin me"* restores the escort AI as well as the flag; *"No, wait here"* now does the right thing, because he is waiting |
| AL35 | Fight beside him in `04 Maw of the Assasin` or later | - | He survives contact. Repaired to HP 220 / AC 215 from 150/145, with `OneHandedMelee 200` untouched |
| AL36 | Recruit him on a **return** visit instead, via `3 Return`'s *"Let's go."* | - | Same result as AL31. Both recruit paths now give the escort AI and open `3 Return` afterwards |
| AL37 | Reach `40 ruse` in the final confrontation as a **Knight of Saladin** | - | A sixth reply: *"Twice your knives found Saladin's tent, and twice they found nothing in it. I am what came back."* Leads to `45 combat` like the rest |
| AL38 | The same as a **Templar** | - | *"The Temple has sent you coin for sixty years to keep your knives out of our chapter houses."* |
| AL39 | The same as an **Inquisitor** | - | *"I have put men to the fire for a tenth of the heresy you have spoken since I walked in."* |
| AL40 | The same as a **Wielder** | - | *"Something else lives in me, and it has never once lied to me about what it wants."* |
| AL41 | The same as a **Goblin Champion** | - | *"The Great Khan sent proud warriors after you once and not one of them came home."* This is the Khan's attempt that `300 kill old man` describes |
| AL42 | Reach `40 ruse` with **no order and no goblin rank** | - | Exactly vanilla's five replies. None of the new ones show |
| AL43 | Carry two of those at once, e.g. Templar **and** Goblin Champion | - | Both replies offered. They are alternatives, not ranked |
| AL44 | Check the Speech path is untouched: reach `200 begin non combat solution path` at Speech 100 | - | Still gated on Speech 100, then 130, then 180, with karma branching at 600. Nothing about the talk-down route changed |
| AL45 | Greet the Knight of Saladin on `02 Shifting Dunes` as a **Templar** | - | A fourth reply about the two orders' arrangement, leading to `22 the tribute` |
| AL46 | Greet him as a **Knight of Saladin**, male or female | - | A fourth reply, *"They sent knives into Saladin's own tent. Twice."*, leading to `23 the tent` |
| AL47 | Greet him carrying **no order** | - | His three vanilla replies only. `1 Conversation Start` is unchanged |
| AL48 | Recruit Grumdjum on `01 Desert Sprawl`, walk him to `04 Maw of the Assasin` or later, then dismiss him there | - | He is released **and** his interaction switches to `300 companion joins you`. Before the review pass the switch sat on a relay that only exists on `01 Desert Sprawl` |
| AL49 | Talk to him on that far map after dismissing him | - | `300 companion joins you`, answerable, not *"What can Grumdjum do for you?"* |
| AL50 | Recruit the Knight of Saladin, walk him off `02 Shifting Dunes`, dismiss him there | - | Same: released, and his interaction switches to `666 Rejoin` on whatever map he is standing on |
| AL51 | Recruit Grace in act 7 and dismiss her on `01 Outside Shrine` | - | Unchanged from 0.19.0. Her switch replies are goto-only from the arrival conversation on that map, so they were never at risk |

### 0.19.0 - the English Shrine

Act 7. Needs a character who has **never entered act 7**. `ES21`-`ES28` and `ES37`-`ES58` additionally
need one who has **not yet finished act 1's Port District**, since the England allegiance, Grace's arc
and Surrey's third route are all decided there.

| # | Step | Say | Expect |
|---|---|---|---|
| ES54 | Carrying **Servant of the Queen** from act 1, talk to Surrey O'Connell at `Crossroads to England map` | - | A third reply, about the service the Queen set her hand to. He goes cold: *"Do not say my name where anybody writes things down."* |
| ES55 | Open the Regent's chest after ES54 | - | No shout, no guards. Same outcome as the clover and the Holy Office -- all three set `Surrey looks away` |
| ES56 | Tell him *"You have nothing to fear from me, Surrey."* | - | *"No. No, I have not, and I have not from the last four either, and here I still am weighin' out bolts on the wrong road."* |
| ES57 | Carrying the clover **and** the title | - | Both replies offered. They are different reasons, not ranked alternatives; either works |
| ES58 | Carrying neither, and no Inquisitor rank | - | Only his vanilla replies plus the PE 8 and Speech 70 routes. Unchanged |
| ES1 | **A save that has never entered act 7.** Fight through `02 Temple Initiate` | - | **Druids among the English soldiers.** Vanilla fielded the `Druid` template nowhere at all, in the act whose enemy faction is the Druids |
| ES2 | Compare `02 Temple Initiate` with `09 Secret Chamber` and `10 Inner Sanctum` | - | Druids are occasional at the entrance and common in the deep rooms. The placement is deepest-first on purpose |
| ES3 | Fight through the three Meditation Chambers | - | Druids alongside the golems and priests. These rooms had no soldiers at all in vanilla |
| ES4 | Reach `05 Exalted Chambers`, the Druid Master's chamber | - | **Priestesses**, including `Priestess Super`. All three Priestess templates were fielded nowhere in the entire game, while the Druid Master herself has the race `Priestess Super` |
| ES5 | Fight priestesses at all three tiers | - | They should feel like priests who hit harder and shield less. The shipped ladder had AC **260 / 80 / 150** and no damage resistance at any tier; it is now 260 / 280 / 310 with 50 / 60 / 65% |
| ES5a | Hit a priestess with cold, electrical or fire damage | - | It resists, 50-65% by tier. In vanilla no priestess resisted anything |
| ES5b | Watch whether priestesses ever cast `ENEMY Magical Shield` | - | **They should not.** That is the priests' signature and was deliberately withheld, so the two lines stay distinct |
| ES6 | Check XP gain across the act against your notes, if you have any | - | Roughly **+15% act-wide**, concentrated in `05`, `09` and `10` (+40-54%). A Druid pays 950 where the identically-statted Soldier1 pays 348. **Report if this feels like too much; the weights are one table** |
| ES7 | Fight the Druid Master | - | **A real boss fight now.** She shipped on the rank-and-file `Priestess Super` race at HP 95 / AC 150 / no resistance -- weaker than her own guards, and against an `Assasin Master` on the same map at HP 400 / AC 305. She is now HP 350 / AC 300 / 65% resist, four spells at 130 and Evasion 60 |
| ES7a | Check the XP for killing her | - | **2,500**, up from 1,100. She shipped paying less than the 1,949 her own attendant priestesses pay |
| ES7b | Fight a rank-and-file `Priestess Super` in the same room | - | Distinctly weaker than the Master: HP 135 / AC 310. They no longer share a race |
| ES37 | **In act 1**, accuse Captain Isabella, hear her out, and choose *"You have persuaded me to silence."* (not the `<Lie>` variant) | - | The Morales quest completes at state `JMBN5402` and she says *"I will not forget your kindness."* |
| ES38 | **A save that has never entered act 7.** After ES37, land at `01 Outside Shrine` | - | **Grace is on the beach at 505,639**: *"You have found me! First you spared me in Barcelona and now you have come so far to rescue me."* Her generator shipped inactive, unnamed and with no AI |
| ES39 | Ask her about the druids | - | *"Once they fought the English with us, but now they have formed an alliance with the Queen."* **The shipped text saying what Sir Roger says in tier 3** |
| ES39a | **In act 1**, after ES37, let her finish -- there is a new beat after *"I will not forget your kindness"* | - | *"Two years of being careful in a language that is not mine, and in all that time not one person has asked me why."* **Her continue reply had no destination at all in vanilla** |
| ES39b | Answer *"Then I will hope to see the ship and not the sinking."* | - | She gives you her name -- *"Grace, then. Not Captain, and not Isabella."* -- and **Grace's Regard** appears among your titles |
| ES39c | Decline instead, warmly or coldly | - | *"You have my thanks, which is not nothing from me."* No title |
| ES39d | Take the `<Lie>` route at *"You have persuaded me to silence."* | - | The beat still plays -- she opens up to someone deceiving her -- but **the reply that answers her is not offered** |
| ES40 | With **Grace's Regard**, accept her in act 7 with *"My dear, your companionship is most welcome."* | - | *"Together we cannot fail. My heart and my sword are yours!"* and **she joins as a companion** |
| ES40a | **Without** Grace's Regard, check her act-7 replies | - | The romantic acceptance is **not offered**. She still declares herself -- she is voiced and that line is hers -- but the routes left are the sword without the heart, and refusal |
| ES41 | Accept with *"Your sword is welcome, but I have no use for your heart."* | - | *"I will honor it, and serve you not for love, but for duty."* She joins anyway |
| ES42 | Refuse with *"Sorry, I work alone."* | - | *"Do not worry - we will not cross paths again."* No companion |
| ES43 | Instead reach act 7 having **driven her off or turned her in to the Duke** | - | **She is not on the beach at all.** The shipped `Captain Isabella fled` checker is what act 1 sets in both cases |
| ES44 | Instead reach act 7 having **taken her bribe, or lied, or never accused her** | - | `500`: *"if I can't kill the English, I will settle the score with you"* -- and she attacks |
| ES45 | With her as a companion, talk to her again | - | *"Are you ready to continue our quest?"* |
| ES46 | With Grace as a companion, fight for a minute | - | She shouts *"For Ireland."*, *"We cannot fail."*, *"I need healing!"* **Never played in vanilla** |
| ES47 | Let her drop below about 60% health, then below 25% | - | *"I require aid!"* then *"I will not survive much longer...Help me!"* -- **both are recorded lines that had no trigger** |
| ES48 | With Sir Roger along, fight for a minute | - | *"For England!"*, *"For The Queen!"*, *"For The Templars!"*, *"We shall Prevail!"*, *"On my honor!"* Five authored barks, opened by nothing in vanilla |
| ES48a | With Grace as a companion, let her take a real fight | - | **She should survive it.** Her act-1 template is HP 36 / AC 90, below every enemy in act 7; act 7 spawns her on a companion race at HP 165 / AC 190 |
| ES48b | Kill Captain Isabella in the act-1 Port District | - | Unchanged -- still HP 36. The act-7 template is separate so act 1's balance is untouched |
| ES49 | Take a companion through a map transition and keep fighting | - | Barks still play. They ride on the character's own AI list, not a relay belonging to one map |
| ES50 | Talk to Grace while she is a companion | - | *"Are you ready to continue our quest?"* -- **and you should now hear it**, because the node was renamed back to match its recording |
| ES51 | Tell her *"Wait here. I will come back for you."* | - | *"If that is your desire. I will await your return here."* She stops following |
| ES52 | Come back and talk to her | - | *"Let us continue our quest."* -- the second renamed recording -- and she rejoins |
| ES53 | Check she is not still following after ES51 | - | She should stay put until ES52 |
| ES29 | **A save that has never entered act 7.** Enter `10 Inner Sanctum` from the Antechamber | - | About a second in: *"There is a great deal of wall for a room this size -- and the wall does not ring the same all the way round."* **This map had no tree, no balloon and no label printer at all** |
| ES30 | Cross to the western corner, around 1500,1400, and look at the wall | - | *"Three stones are set into the wall here at shoulder height, worn paler than the rest..."* The hover covers all three switches |
| ES31 | Click the switch at 1482,1379 | - | A panel opens in the **eastern** wall on two strongboxes with the Temple's mark, and you are told so -- the door is 800 units away and vanilla gave no feedback whatsoever |
| ES32 | Open those two chests | - | Good weapons and arrows/bolts, on `Chest Generator Good`. **The best loot in the act outside a boss, behind an unmarked switch in vanilla** |
| ES33 | Click the switch at 1620,1364 | - | Grinding to the **north** and *"a great many boots"* -- an ambush of soldiers, bowmen and druids |
| ES34 | Click the switch at 1508,1471 | - | Grinding to the **south**, hot iron and wet stone -- war golems, a priest, a druid and a priestess |
| ES35 | Read the end of each switch line | - | Each says how many stones are left, so finding one tells you to look for the others |
| ES36 | Check that the doors, ambushes and chests behave as before | - | Unchanged. Only balloons were added to the three relays; every vanilla action on them is intact |
| ES21 | **In act 1**, take Guy Fawkes' side and reach either good ending -- decline the Duke's murder, or carry it out and collect the Queen's gold | - | **Servant of the Queen** appears among your titles. Vanilla stored the allegiance nowhere at all |
| ES22 | Betray him instead: expose him, or tell the Duke you will deal with him | - | **No title.** Both grants sit past every betrayal branch, which matters because the engine has no way to take a perk back |
| ES23 | In act 1, accept the Duke's murder -- *"I'll lure the Duke to the trap."* | - | He answers: *"you will be remembered forever in English history... When the deed is done, return here."* **In vanilla that reply ended the conversation silently** |
| ES24 | Carrying the title, talk to **Sir Roger** in act 7 -- first meeting or any return | - | A new reply about the Queen owing you a service. He tells you **the Queen keeps druids**, and that his Order came to the shrine **without her leave** |
| ES25 | Press him on it | - | *"she will call it hers when it is done, and the men who stopped it will have been brigands."* Both nodes lead into `10 accept`, so it is a way into the alliance |
| ES26 | Without the title, check Sir Roger's replies | - | The new reply is not offered, on any of his six entry nodes, and everything else is as vanilla |
| ES27 | Carrying the title, ask the Templar camp surgeon for healing as a plain human with no order | - | Healed free. A servant of the Queen counts as a knight to him |
| ES28 | Check your titles after act 6 has failed the conspiracy quest | - | **The title survives.** Act 6's bulk quest-fail is `IfActive`, so a completed conspiracy is untouched |
| ES9 | **A save that has never entered act 7.** Accept Sir Roger's offer of help, then look around the entrance of `02 Temple Initiate` | - | A Templar post: a quartermaster, a field surgeon and a guard, around 2820,1300. **Act 7 had no merchant on any of its eleven maps** |
| ES10 | **Refuse** his help instead -- *"I am not interested in help from any Englishman"* -- and look in the same place | - | **Nothing there.** No camp, no shop, no surgeon. That reply cost nothing at all before this |
| ES11 | Reach `04 Antechamber of Lore` after accepting | - | A second post around 5880,1560. It is opened from `02` by a `COtherMapAction`, so it should already be there when you arrive |
| ES12 | Talk to a camp guard | - | *"My sword is yours."* **The one dialogue tree in the act that nothing opened** |
| ES13 | Buy from the quartermaster with **none** of Quinn's three errands done | - | One "Show me what you have" reply. Potions, 40 bolts, 40 arrows, hard leather, a medium shield |
| ES14 | The same having done **one or two** of Quinn's errands | - | The reply mentions a herbalist who owes you, and the stock adds **Great Healing** potions |
| ES15 | The same having done **all three** | - | The reply says you did the herbalist some favours, and the stock adds **Superior** and **Supreme Healing** -- the potions 0.4.0 unlocked, six acts earlier |
| ES16 | Count the "Show me what you have" replies in any of ES13-ES15 | - | **Exactly one, ever.** The first draft would have shown three identical replies to a player who had done all three errands |
| ES17 | As a **Templar**, then as a **Knight of Saladin**, ask the surgeon for help | - | Healed to full, free. He treats both orders as brothers |
| ES18 | As a sworn **Inquisitor** | - | He heals you, and **charges the 200** like anyone else. Deliberate: the Inquisition is Spanish and ecclesiastical, not his brotherhood |
| ES19 | With fewer than 200 gold and no order | - | The paid reply is not offered |
| ES20 | Ask the surgeon how many he has lost, and the quartermaster whose stock it is | - | Two answers about the twenty who held the gate. Neither is a shop |
| ES8 | Everything else about the act's spawns | - | Unchanged. No generator was added or removed and no vanilla spawn entry was dropped; only weighted entries were added to existing groups |

### 0.18.0 - the Barcelona Attack

Act 6. Needs a character who has **never entered act 6**; BA22-BA26 additionally need one who has
never entered the peacetime Gate, Temple or Port districts, since the title is granted by level
parts on their citizen generators. **BA26a-BA26h are 0.18.1** and need a
character who has never entered Scar Ravine, the Port District, the Troll Pit or Montaillou.

| # | Step | Say | Expect |
|---|---|---|---|
| BA1 | **A save that has never entered act 6.** Stand in the fighting on `Gate District Siege` for a minute | - | Both sides shout. Spaniards: *"To Hell with these accursed druids!"*, *"God save Barcelona!"*; English: *"Attack! For England!"*, *"For the Queen!"* **Nineteen lines across three trees, none of which has ever played** |
| BA2 | BA1 on `Temple District Siege` | - | The same, quieter -- that map has one defender generator and three attacker generators still standing |
| BA3 | Watch where the balloons appear | - | Over the soldiers themselves, not over the player. They position on `$Trigger` |
| BA4 | Listen for about a minute on either map | - | Roughly one line per armed soldier every eight seconds, plus a steadier defender line every twenty-four. **If it reads as a wall of text, the count to reduce is the six-per-side cap** |
| BA5 | Listen for the steadier defender lines specifically | - | *"We must remain vigilant."*, *"The gall of these druids!"*, *"Spain is too powerful for the druids!"* One of the six is *"I'll secure this area."*, which can land mid-fight -- known, and noted in the release |
| BA6 | Kill every English soldier near an armed defender | - | The defender keeps talking. There is no end-of-fight event on these maps, so the lines are timed rather than triggered |
| BA7 | **A save that has never entered act 6.** Find the blacksmith during the siege and ask where Galileo and Leonardo are | *"Where are Galileo and Leonardo? Their workshops are open to the street."* | He puts the hammer down and says they were taken west with a guard who had a list. **Find Galileo and DaVinci** enters the journal -- a quest that shipped with a blank name and no states |
| BA8 | BA7, then check the journal | - | One entry, one state. Not an empty or unnamed quest line |
| BA9 | Reach `Crossroads to England map` | - | **Pursue the Retreating Druid Forces and Recover the True Cross** enters the journal about a second after you land |
| BA10 | Leave and re-enter that map | - | No second copy of the entry. `the pursuit has been called` holds it |
| BA11 | Reach `8 Alamut/08 Final Encounter` and find Galileo | - | **Find Galileo and DaVinci** completes |
| BA12 | The same, when the `TRUE CROSS` is handed to you | - | **Pursue the Retreating Druid Forces** completes. **These hooks reach two acts ahead of the release and may move when act 8 is surveyed** |
| BA13 | Ask the blacksmith for supplies as before | - | His vendor path is unchanged, and his three recorded voice-over lines still play |
| BA14 | **A save that has never entered act 6.** Cross from `Gate District Siege` into `Crossroads Siege` | - | About a second after landing: *"The crossroads is not a crossroads any more..."* **This map had no balloon, no conversation and no dialogue tree at all** |
| BA15 | Walk to the middle of the field, around 2500,1000 | - | *"Somebody has driven a standard into the stones at the centre of it..."* Once only |
| BA16 | Reach the road to England at the western end | - | *"The road west, and the ruts in it are fresh..."* |
| BA17 | BA16 **without** having asked the blacksmith (BA7) | - | The plain line, and no XP. The evidence is what the blacksmith's answer turns the ruts into |
| BA18 | BA16 **after** BA7, with *Find Galileo and DaVinci* active | - | The longer line -- the cracked lens and the wax tablet -- and **1500 XP, once** |
| BA19 | Walk back over the western end again | - | No repeat and no second payment |
| BA20 | Fight anywhere on the map for a minute | - | English soldiers shout: *"Press forward, men!"*, *"Attack! For England!"*, *"For the Queen!"* Six of the thirty-four generators are armed |
| BA21 | Compare the volume against `Gate District Siege` (BA4) | - | Similar. This map has no defenders, so only the English are heard |
| BA26a | Attack **Marisol** outside the sewers in the Port District | - | She screams *"Ahhh!"*, will not speak to you again, walks off to her disappear point, *Find the lost boy Tomas in the Sewers* fails -- all vanilla -- **and you are now Slayer of Innocents** |
| BA26b | Attack the **woodcutter's daughter** in Scar Ravine | - | The same, plus the goblin turns on you and *Find the Woodcutter's lost son* fails. Then ask the woodcutter about her: he already reads `daughter attacked` in vanilla |
| BA26c | Attack **Tomas** in the troll pit | - | He screams and flees; the title is granted |
| BA26d | Attack the **shepherd's son** in Montaillou | - | He screams, `Player hurt the son` and `Make Maury mad for hurting son` activate as in vanilla, and the title is granted |
| BA26e | Attack the **Gate District boy** while `Child Leaving` is switched on | - | The title is granted |
| BA26f | Keep hitting the same child, or attack a second one after the first | - | No duplicate grant. Each hook is `COnlyOnce` and the grant checks the perk first |
| BA26g | Let the goblin stand over the daughter, or the trolls over Tomas, and do nothing | - | **No title.** No enemy on those maps can target a neutral, so only the player can trigger a child's hook |
| BA26h | After any of BA26a-e, walk up to a Gate District guard | - | *"There have been reports of a monstrous killer of helpless children..."* -- and on *"I am the killer"* he shouts **"Have at thee, monster!"** and the district turns on you. **This chain has never fired in any playthrough** |
| BA22a | Let your own character be killed by anything, at any point in the game | - | **No title is granted by dying.** The first pass armed the player's own death by mistake; the hook belongs on the citizen, not on whoever the balloon was talking to |
| BA22 | **A save that has never entered the Gate District.** In peacetime Barcelona, kill one unarmed citizen | - | **Slayer of Innocents** appears among your titles. Vanilla never granted this perk anywhere |
| BA23 | BA22, then walk up to any gate guard in the Gate District | - | *"There have been reports of a monstrous killer of helpless children...you loosely fit the description."* Two replies: deny, or admit it and threaten him. **Five authored nodes that had never fired** |
| BA24 | BA23, then talk to the same guard again | - | The `Childkiller Return` variant, not the intro again |
| BA25 | Kill a vendor instead | - | **Merchant Slayer**, as in vanilla. The two vendor cans are deliberately not wired to the new title |
| BA26 | Attack `Barcelona Boy` in the Gate District, or any child anywhere | - | Nothing happens. Children are HP 10000 / AC 1000 in vanilla and stay that way |
| BA27 | **Without** the title, enter `Gate District Siege` and talk to the man calling for Phillipe | - | He asks you to look for a boy in a red cap. **Vanilla gave every player the accusation instead** |
| BA28 | **With** the title, do the same | - | *"Leave me alone! Haven't you done enough?!"* -- the shipped line, now on the shipped condition |
| BA29 | Walk past him without talking | - | The old polygon bark still fires: *"Phillipe! Where are you?!"* |
| BA30 | Find Phillipe around 2694,1251, behind a barrel, **before** speaking to his father | - | He talks, but the reply that sends him home is not offered |
| BA31 | Speak to the father first, then find Phillipe | - | The reply is offered; he runs; **1000 XP, once**, and a closing line about the man who stops saying one word |
| BA32 | Go back to where Phillipe was | - | He is gone, and no second payment |
| BA33 | **A save that has never entered act 6.** On `Gate District Siege`, find the woman around 2551,1520 and talk to her | - | An ordinary Barcelona citizen greeting. **She did not exist; the map's relay was positioning a balloon over her name** |
| BA34 | Murder her, or murder the man searching for Phillipe, while she is alive to see it | - | *"Ayudame! Help me! Guards!"* and about two seconds later **the whole garrison turns on you**, with a +40% AC buff -- the same consequence vanilla gives for attacking a guard |
| BA35 | Murder the man searching for Phillipe **after** killing her | - | No scream and no turn. The witness has to be alive |
| BA36 | Let the English kill defenders all around you without lifting a hand | - | Nothing happens. The scream is armed on civilians only, so the garrison never blames you for the siege |
| BA37 | Attack a defender directly, as in vanilla | - | The garrison turns, as before. Unchanged |
| BA38 | Find the `Generic Gaurd NPC` body at 1618,845 and use it | - | *"Stranger...here...take my gold. Don't let those English have it..."* and **250 gold**, once |
| BA39 | Find the `Soldier1` body at 1678,2914 | - | *"I am sorry Espana...I do not know why we came with swords drawn and bloodlust in our hearts..."* |
| BA40 | On `Temple District Siege`, walk the length of the map using bodies | - | Six of them speak, three Spanish and three English, spread west to east. **Vanilla had 62 bodies and zero talkable ones on this map** |
| BA41 | The dying Spaniard on the Temple District | - | Also pays 250, once |
| BA42 | Re-use any body that has already spoken | - | Nothing. Each specifier is once-only, and no second payment |
| BA43 | **A save that has never entered act 6**, carrying the Clover from the Port District Irish sailor. Talk to Surrey O'Connell | - | A new reply offering the clover. He stops grovelling and tells you to take what you need off the Regent's pile |
| BA44 | BA43, then open the Regent's chest | - | **No shout, no guards, and Surrey stays friendly.** In vanilla only Sneak 100 avoided the alarm |
| BA45 | The same without the clover and without Sneak 100 | - | He shouts *"That's the Regent's loot!"*, the `chest guards generator` wakes and he turns on you -- unchanged |
| BA46 | As a sworn Inquisitor, talk to Surrey | - | *"The Spanish -- no. No, guvna', I never --"* and the same look-away |
| BA47 | Without either, check the reply list | - | Neither new reply is offered. His PE 8 and Speech 70 routes are untouched |
| BA48 | As a Templar, then as an Inquisitor, talk to the blacksmith | - | Both get `30 the orders` -- what the two orders lost in the district |
| BA49 | As a Feralkin or Sylvant, talk to the blacksmith | - | `40 no flinching`. He has no attention left for a tainted face today |
| BA50 | Holding **Slayer of Innocents** (BA22), talk to the blacksmith | - | `50 the reports`. He sells to you and tells you not to come back after the city is standing |
| BA51 | As a plain human with no order and no title | - | None of the three appear, and his vanilla replies are unchanged |
| BA52 | Enter `Church Crypt Interior Siege` and look around | - | Hover lines for the room and for one slab in the wall. **This map had thirteen parts and nothing to do** |
| BA53 | Walk toward the chest at 560,600 without any Traps skill | - | Poison gas, 25-40, once |
| BA54 | The same with Traps/Perception enough to spot it (`Skill Adjustment=10`) | - | The trap is revealed and can be disarmed at Lockpick 40 |
| BA55 | Open the chest behind it | - | Locked at -40. The sacristan's plate |
| BA56 | Use the dead guard on the stair | - | A line about his sword and which way his feet are pointing |
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
| 0.17.0 | PASS (automated) | PASS | - | - | - | - | **published, entirely unplayed (NO1-NO96); repairs go to 0.17.1. NO1 and NO81 are the two rows that prove the release** |

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
