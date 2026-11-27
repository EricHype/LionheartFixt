# Replies that disagree with their twins

Status: **15 repaired, built, not yet released or played.** Survey: `tools/sibling_replies.py`.
Repairs: `tools/build_sibling_repairs.py`. Measured on `main` after the link-rot commit (9959c81).

## What was repaired

Fifteen of the sixteen below, as 17 reply edits in 13 trees (S12 is three replies). Each odd copy
now does what its own twins in the same tree do, so nothing is new behaviour:

- **Copied the twin's action** (S1, S2, S5-S9, S11-S14): the twin's `Custom Action`, byte for byte.
- **Sent it where its twins go** (S3, S4, S16).
- **Lord Javier (S15)** is the one that also removes something, and it was worse than it looked.
  The first-meeting donation took 1000 gold itself and then went to `210 give gold`, which takes
  another 1000. **It charged twice**, and skipped `520 before I accept`, the warning that no other
  faction will have you. It now routes through the warning like the return copies, and pays once,
  at `210`.
- **Not repaired: S10 (Jafar).** Read again, it is not a defect. The one exit from `400 NIS
  Montserrat Directions` activates the same *Travel to Montserrat* state, so the odd copy only
  skips activating it one line early.

Checked: every edit is an added action block or a changed target, except Javier's removed double
payment; CRLF throughout; re-running the sweep resolves all 15 outlier groups and creates none;
`validate.py`, `check_node_variants.py` and `test_triggers.py` pass. `reachability.py` fails only on
`Warning Troll`, as it already does on `main`. `GuardTomas`, `Demon` and `Bounty Hunter` are new to
`files/`; GuardTomas's race-variant report is identical to vanilla's.

There is no gate for this. The sweep reads the whole archive, and tier C is too noisy to hold a
release to. Re-run it after any release that edits a tree.

A tree often carries one reply in several nodes. When the copies share text and gate, they should
do the same thing. Two defects found during the link-rot work had this shape, and no gate could
see either: the organ's *"Goodbye."* that loops back to its greeting, and the Conspirator's
return-visit ale that gives no ale. The sweep groups each tree's choosable replies by (text, gate)
and reports the groups whose copies disagree.

## What it found

| | Groups |
|---|---|
| Copies disagree, anywhere | 308 in 103 trees |
| ... **outliers**: 3+ copies, exactly one differs | 105 |
| ... tier A, the odd copy *lacks* its twins' action or ends where they continue | 24 |
| ... tier B, the odd copy goes somewhere else | 16 |
| ... tier C, the odd copy does more, or is a race/standing variant | 65, unread |

**Both known defects are found.** The Conspirator turns up three times. Tier A and B were read
in full, each odd copy beside its twin: 16 are real, 4 probable, 20 deliberate.

## Real (16)

| # | Tree | Reply | The odd copy | Twins | Origin |
|---|---|---|---|---|---|
| S1 | Shakespeare | *"I convinced Shylocke to extend your debt."* | at `5 Return Dialogue 2`: never completes the quest or pays its XP | 1 | vanilla |
| S2 | Toulouse Rhea | *"Your philosophy sickens me."* | no Good Karma, though its own note says *"give karma bonus"* | 3 | vanilla |
| S3 | Demon | *"You are a foul demon and worthy of a swift death..."* | ends the conversation; its note says `50 Insult`, where its twins go | 4 | vanilla |
| S4 | Bounty Hunter | *"How many goblins have you killed so far?"* | at `50 Linripper`: ends without the answer | 2 | vanilla |
| S5 | Blacksmith | *"I've been told you can forge a Lion Shield."* | at `07 what more`: never starts *Forge a Lion Shield* | 14 | vanilla |
| S6 | Guard Tomas | *"I have killed some goblins just around the bend..."* | from `15 Other Questions`: none of the reward its twins give | 6 | vanilla |
| S7 | Guard Tomas | *"Someone has been murdered..."* | from `15 Other Questions`: no karma 25 | 6 | vanilla |
| S8 | Guard Tomas | *"There are goblins spying along the western wall..."* | from `15 Other Questions`: no reward | 5 | vanilla |
| S9 | Mayor | *"Is Montaillou in danger?"* | at `900 Toulouse`: never sets `Spoke to mayor about Toulouse` | 2 | vanilla |
| S10 | Jafar | *"I will go to Montserrat, just tell me where to go."* | at `400 crown of thorns`: never activates *Travel to Montserrat* | 2 | vanilla |
| S11 | Weird Woman | *"You have the look of a witch..."* | at `35 Shell Game 2`: never advances *Find the Witch for the Inquisitor* | 2 | vanilla |
| S12 | Conspirator | *"I'm not interested in drinking with you."*, and both drink replies | at `3 return no drink`: no `took drink`, no `rude response`, no ale | 2 | vanilla |
| S13 | Fish Monger | *"I have a vodyanoi skull to sell you."* | at `10 name`: ends without the relay that opens his shop | 7 | vanilla |
| S14 | Spirit Council | *"I will see what I can do."* | at `23 The Wish Ending`: never sets `CRY2CURS` | 4 | **Fixt, 0.16.0** |
| S15 | Lord Javier | *"I would like to donate the thousand gold."* | at the first meeting: pays at once, skipping `520 before I accept`, the warning that no other faction will take you | 2 | vanilla |
| S16 | Viola Organista | *"Goodbye."* | at `5 organ already tuned`: back to the first-tuning greeting | 3 | vanilla |

S10 sits in the cathedral's scene family. Before changing it, check how that scene is driven, as the
link-rot work did for the NIS rows.

## Probable, read before repairing (4)

- **Brother Michel**: the demokin copy of the heritage question has no Good Karma; the Sylvant and Feralkin copies do.
- **False Crypt Protector**: leaving on return skips `Protector get rid of him`. Find out what that relay does first.
- **Goblin Henchman** (a Fixt tree): one copy of *"I'll just be on my way."* omits `CActionResetPointClickAI`.
- **Relican**: *"I'm going to leave now."* at the ultimatum does not advance *Hunt down Relican*. The ultimatum may handle the quest itself.

## Read and dismissed (20)

The odd copy is in a different situation from its twins, and the difference is the design: a
return visit (Sanchez: *"you promised you would reform before"*), a released companion (the Lost
Knight), a branch with its own outcome (the Grand Inquisitor's renounce sends you to jail rather
than to a fight), a state machine (the organ's keys), or a skipped thank-you line (Shylocke's
`1100`, three goodbyes). Galileo differs only in a blank `Fail Action` versus an explicit success.

## Limits

- Tier C (65) and the 203 non-outlier splits are unread. Two-copy splits are where the Conspirator's
  ale was, so they hold real rows too, at a lower rate.
- Copies differing in gate are never compared. That is deliberate (a different gate legitimately
  explains a different target), and it means a defect in the gate itself goes unseen.
- Text is matched exactly, after folding case and whitespace. A reworded copy is not a twin.

## QA

Each row fails while the bug is there. Dialogue-only, so any save works.

| # | Do | Passes when |
|---|---|---|
| TW1 | Shakespeare, on the second return line, with Shylocke persuaded: *"I convinced Shylocke to extend your debt."* | the quest completes and XP is paid the first time you say it |
| TW2 | Rhea at Toulouse, from *"Might makes right"*: *"Your philosophy sickens me."* | karma rises, as it does from her morality line |
| TW3 | The Demon, after *"a hell of a deal"*: *"You are a foul demon..."* | he answers the insult; the conversation does not just close |
| TW4 | The Bounty Hunter, after asking about Linripper: *"How many goblins have you killed so far?"* | he gives the count |
| TW5 | The Blacksmith, from *"what more"*: *"I've been told you can forge a Lion Shield."* | *Forge a Lion Shield* appears in the journal |
| TW6 | Guard Tomas, from *Other Questions*: report the goblins killed, the murder, and the spies | karma rises for each, as from his opening menu |
| TW7 | The Mayor of Montaillou, first time on Toulouse, ask only *"Is Montaillou in danger?"*; then talk to Esclarmonde | she offers the reply that marks Titan Village on the world map (it checks `Spoke to mayor about Toulouse`) |
| TW8 | The Weird Woman, after the shell game: *"You have the look of a witch..."* | *Find the Witch for the Inquisitor* advances |
| TW9 | The Conspirator, on return: take the ale; on another save take the bile; on a third refuse rudely | the ale or bile is given, and he remembers the drink or the insult |
| TW10 | The Fish Monger, holding the vodyanoi skull, from his name line: *"I have a vodyanoi skull to sell you."* | his shop opens |
| TW11 | The Spirit Council, at the wish's ending: *"I will see what I can do."* | the doomed knights' quest advances |
| TW12 | Lord Javier, first meeting, 1000 gold or more: donate | his faction warning plays first; accepting takes **1000** gold, not 2000; *"I need more time"* takes nothing |
| TW13 | The Viola Organista, tuned, on return: *"Goodbye."* | the organ hums and the conversation ends |
