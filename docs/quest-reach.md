# Quests that cannot end, and gates nothing opens

Status: **3 repaired, built, not yet released or played.** Survey: `tools/quest_reach.py`.
Repairs: `tools/build_quest_repairs.py`. Measured on `main` after the sibling repairs (5d4f020).

Four of the sixteen defects in [`sibling-replies.md`](sibling-replies.md) were quests, and nothing
checked quest wiring: that every `Quest=` names a quest file and every `State=` one of its states,
that a quest a player can start can also end, and that a gate waiting on a state can ever open. This
sweep reads every quest action and check in the game against the quest files, counting only what a
player can reach.

## What it found

| | Fixt | Vanilla |
|---|---|---|
| Quests | 163 | 150 |
| Quest actions and checks read | 3,752 | 2,857 |
| `Quest=` or `State=` naming nothing | 0 | 0 |
| **no-end**: a player can start it, nothing a player can reach ends it | 1 | 0 |
| **no-win**: a player can start it, it can only ever fail | 3 | 2 |
| **dead-gate**: a reply waits on a state nothing reachable sets | 4 issues (11 replies) | 4 issues |
| ... the same, in requirement cans no reachable reply uses | 6 | 7 |

**Three ways the first runs were wrong**, kept because each would mislead a rerun:

- **Maps are tab-indented.** The first pass found an action's block from one character past its line,
  which in an indented map lands before the brace and returns the *parent* block, pinning some other
  action's `Quest=` on this one. That invented three dangling references and 61 of 81 dead gates.
- **Items carry quest actions.** Picking up the Felgnash Sword or the Magnetized Silver sets their
  quest states from the `.InventoryItem`. Scanning a list of extensions missed them; the sweep now
  reads every text resource that names a quest.
- **A requirement can matters only through the replies that name it.** Six dead gates sit in cans no
  reachable reply uses. They are counted, not reported.

## Repaired (3)

| # | Quest | The defect | The repair | Origin |
|---|---|---|---|---|
| Q1 | *Initiation Quest for the Wielders* | Two requirement cans check `J5WOL4C2` on this quest, which has a state of that ID that nothing sets. Cedric and the Inquisition Pit set it on *Bind Spirit to Rod*, where Galileo's own opening lines check it. So Galileo's three mid-conversation *"Cedric told me to seek you out..."* never appeared, and the Prisoner Wielder's *"I'm looking for Galileo."* (four copies) never appeared in any game. | Both cans name *Bind Spirit to Rod*. Seven replies come back. | vanilla |
| Q2 | *Travel to Montserrat* (Knights of Saladin) | In vanilla every line that starts it was unreachable. Fixt's Jafar work made three reachable, and nothing completes it, so the Temple District siege later **fails** it. | Completes in the four replies where every other faction's Montserrat quest completes: Brother Montgomerie's two, and Sahar's two. | **Fixt** |
| Q3 | *Obtain Darkwood from the Wilderness* | Darkwood Cave starts it and nothing ends it, so the siege failed it. | The Darkwood pickup, which already advances both factions' rod quests, completes it. | vanilla |

Q2 and Q3 add a completion guarded by `CWasQuestEverActivatedAction`, so a player who never had the
quest gets no journal entry for it.

## Read and left alone

- ***Fixt The Spellbound Soldiers*** (no-end) is a journal hint from 0.99.2, kept as a sub-quest "so
  its state is never touched". It is meant to stay open.
- ***Purify the Shadow Dryad*** (no-win) is wired exactly as in vanilla, and the README already
  records leaving it: she cannot be killed, and the quest is unfinished, not cut.

## Unfinished content, not repairs (4)

These gates wait on quests or states that nothing anywhere starts, not even unreachable dialogue.
Repairing them means deciding where a quest should begin, which is restoration work (goal 2):

- ***Help the Thieves Destroy the Beggars Guild*** is completed four times and failed twice in
  Juanita's tree, and never started anywhere, so its journal never appears. The Beggar Captain's
  *"Juanita will be glad to hear I've killed you!"* (two copies, noted *"only show this reply if
  player has seen Juanita"*) waits on its second state.
- ***Enter Inquisitor's House and Learn about Relics*** is never started. Lord Relican's *"Let us
  talk about the events that transpired in the Church."*, which completes it with XP, never appears.
- ***Brink back any rare books to Weng Choi***'s second state is never set. The firepowder reply that
  waits on it has a working twin, so nothing a player can buy is lost.
- In the cans nothing uses: *Recover Red Iron for Eduardo* and *Shake Down Shakespeare* are never
  started either.

## Checked

Every edit is a changed `Quest=` line or an added guarded completion, with each array's `Item Count`
raised by one; CRLF throughout; the can and item edits round-trip through `resource_format`.
`validate.py`, `reachability.py`, `check_node_variants.py` and `test_triggers.py` pass, and the
sibling sweep's count is unchanged at 90.

There is no gate. The sweep takes about fifteen seconds, and could be one: it would have caught Q2,
a regression Fixt introduced.

## QA

Each row fails while the bug is there.

| # | Do | Passes when |
|---|---|---|
| QR1 | As a Wielder initiate sent to Galileo by Cedric, talk to the Prisoner Wielder in the Inquisition | *"I'm looking for Galileo."* is offered |
| QR2 | Talk to Galileo, let him explain how a spirit is got, and carry on the conversation | *"Cedric told me to seek you out to obtain a spirit for my wand."* is still offered mid-conversation |
| QR3 | As a Knight of Saladin, accept *Travel to Montserrat* from Jafar, then reach Brother Montgomerie (or take Sahar's ring) | the quest shows **completed**, and the Temple District siege does not fail it |
| QR4 | As any other faction, do the same | no *Travel to Montserrat* entry appears |
| QR5 | Enter Darkwood Cave, then pick up the Darkwood | *Obtain Darkwood from the Wilderness* completes, and the rod quest still advances |
