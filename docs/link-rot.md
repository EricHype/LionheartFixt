# Phase 1, finished

Status: **built, not yet released or played.** `tools/build_link_rot.py`; the gate is `link-rot`
in `tools/validate.py`.

[`design.md`](design.md) Phase 1 found 84 replies that point at a node that does not exist.
Choosing one advances to nothing and the conversation stops responding. 13 went with earlier
work. Of the 71 left, **48 are repaired** and **23 are left alone because nobody can choose
them**. No reply a player can reach now goes to a node that does not exist.

## The count

A target is dead when no node in the same tree matches it case-folded and trimmed, which is the
engine's rule (it reproduces vanilla's 84 exactly).

| | Before | After |
|---|---|---|
| Dead replies in the game as Fixt leaves it | 71 | 23 |
| ... a player can choose | 47 | **0** |

**A balloon does not offer replies.** The first triage counted 52 choosable. Five of those sit on
nodes that are only ever shown through `CDisplayDialogBalloonAction`, and a balloon never presents
its replies: the pirate ghosts' greeting, Cervantes' beast scene, and the cathedral NIS lines of
Raphael and Lord Javier. `Church Interior.zax` and `Barcelona Coast.zax` fire every line of those
scenes themselves through `Next Action` and `After Action` chains, and never name the missing
nodes, so those reply targets are vestigial. (The coast map names `202 encounter beast` with a
**trailing tab**: that node ID must stay byte-exact.)

## What each reply now does

Decided by reading the tree, never by matching the node's number. No missing target had a
recording, so nothing was restored from voiceover. Only `Go to node ID=` lines changed: no reply
text, no requirement, no node ID.

**Retargeted, 13 replies.** The tree already sends the same reply there, or plainly meant to.

| Tree | Replies | Was | Now | Why |
|---|---|---|---|---|
| `Fish Monger` | 2 | `5 Goodbye.`, `I'll be leaving now.` | `5 goodbye` | a stray period; reply text pasted into the target |
| `fabrisse` | 2 | `10 goodbye` | `10 goobye` | the node's own typo; retargeted, not renamed, because a map naming a node must match it byte for byte |
| `shakespeare` | 1 | `Shakespeare in love 3a` | `2000 Shakespeare in love 3a` | *"I would love to hear your poetry"* leads into the sonnet |
| `MarcoPoloSpirit` | 1 | `06 Goodbye forever` | `06 Goodbye forever leaving` | `60 Leaving` and `200 boots` send the identical decline there |
| `Conspirator` | 3 | `10 no thanks` | `5 goodbye` | *"I'll just be going."* in the same nodes goes there |
| `cortes` | 1 | `5 goodbye` | `10 goodbye` | his plain exit, *"Until the next time."* |
| `Viola Organista` | 1 | `40 play the organ` | `40 play the organ 1` | the melody starts there, and every wrong key returns there |
| `Viola Organista` | 1 | `5 organista` | `60 name` | `5 organ tuned` sends the identical question there |
| `Barcelona Vendor Sympathetic` | 1 | `86 Speech solution` | `86 Speech skill` | the same line elsewhere in his tree goes there, and the node's note says `speech skill` |

**Ended, 35 replies.** An empty target ends the conversation, vanilla's own shape in 2,263 replies.
These trees have no plain goodbye, and the obvious candidate was wrong in every one:

| Tree | Replies | Was | The candidate, and why not |
|---|---|---|---|
| `Inquisitor Port` | 12 | `5 goodbye` | no node 5 at all |
| `ToulouseIapetus` | 16 | `100 Goodbye` | `100 Quest Goodbye` is the line that hands out his quest |
| `Surrey Vendor` | 2 | `10 goodbye` | `10 Fight baloon`: *"You'll see what an Irishman kin do!"* |
| `RogueInquisitor` | 5 | `10 combat` | `10 Goodbye` says *"You won't be leaving here alive!"* |

## Where reading overturned the plan

The first draft of this plan was wrong six times, each caught by reading before writing:

- **The Rogue Inquisitor** was going to be retargeted to `10 Goodbye`. But his *"moving along"*
  reply already carries the outcome in a `CIfAction`: a friend is let go, anyone else is attacked.
  Retargeting would have told a friend he was about to die. His own `3 Return Dialogue` copy of
  that reply already has a blank target.
- **Marco Polo** looked like a trap: the only candidate removes his interaction specifier for good.
  It is also where both of his other declines go, so it is the farewell, not a trap.
- **The sympathetic vendor** looked ungated, and the plan proposed copying the Speech 25 gate from
  his other two copies. It is gated, on **Barter 35**, through a `Custom Requirement` that a
  `Requirement=`-only read missed. The builder's assertion stopped it, and the gate stays as shipped.
- **The Conspirator and Cortes** each have a plain goodbye of their own, which beats a blank.
- **The organ's** two rows turned out to be answered by the tree's own siblings.
- **The pirate ghosts, Cervantes and the cathedral NIS** were balloons all along (above).

## Left alone (23)

On nodes nothing reaches, in trees nothing opens, or on nodes only shown as balloons. They are
`INERT` in the builder, and the gate allows exactly these and no more:

- `Bar Patrons` (3), `ShipSailorsonShipCanned` (2)
- `cortes` `5 cortes agrees to deliberation return` / `800 Return Dialogue` (4)
- `GrandInquisitor` `400 NIS Dialogue 4b` (3), `InquisitorRaphael` (3), `LordJavier` (1), `Shylocke` (1)
- `Shapeshifting Daeva` and `Trueform` (2), `Cervantes` (1), `Pirate Ghosts` (1)
- `EvilEndingAllDie`, `GoodEndingAllSurvive` (2): trees nothing opens

A release that makes any of these reachable fails `link-rot` until it deals with the dead reply.

## The gate

`lhcheck` forgives vanilla's own dead targets. That is right for a mod that copies a tree to change
one line, and it is also how 71 of the 84 outlived Phase 1 for 99 releases. Fixt's `validate.py`
now adds `link-rot`, which forgives only the `INERT` list: any shipped tree with a dead reply
beyond it fails. Proved both ways: it passes on this build, and putting back the pre-fix
`ToulouseIapetus` fails it with *"16 replies go to '100 goodbye'"*.

## Found on the way, not touched

- **The organ's `Goodbye.`** at `5 organ already tuned` goes to `5 organ tuned`, the first-tuning
  greeting, instead of `5 goodbye`. A misroute rather than a dead link.
- **The Conspirator's return** at `3 return no drink`: accepting the ale there gives no ale and sets
  no `took drink`, unlike the same reply at `1 Conversation Start`.
- **`reachability.py` fails on `main` already:** `Warning Troll` `91 that is ours` is unreachable as
  shipped in 0.99.44.

## QA

Each row fails while the bug is there. Dialogue-only, so any save works.

| # | Do | Passes when |
|---|---|---|
| LR1 | Fish Monger, Port District: ask about fish, then *"Goodbye."*; and *"Goodbye."* from other questions | both say *"Farewell. Come again if I ever get some fish."* and end |
| LR2 | Fabrisse, Montaillou: *"I should go now."* at the start and on return | *"Au revoir!"* and the conversation ends |
| LR3 | Shakespeare, the love thread to 5: *"A poem? For me?"* | the sonnet begins (*"My mistress' eyes..."*) |
| LR4 | Marco Polo, after Jameson: *"Sorry, I don't have the time."* | *"Then live your life to the fullest..."* plays and he leaves, and the bridge still reaches the enchanter |
| LR5 | The Conspirator: *"Not right now, thanks."*, and *"No thank you, I don't drink."* on return | *"Until our paths cross again. Adios."*, no quest failure |
| LR6 | Cortes, the arm unfinished: *"Not yet..."* | *"Until the next time."* |
| LR7 | The Viola Organista, tuned: *"Examine the keys."*; *"What is your name?"* on return | the seven-key menu, and the melody works from it; his name |
| LR8 | Raymundo, as a tainted character with Barter 35: *"This town is full of merchants..."* at the bigotry line | *"I suppose you are right..."*, and the shop opens. Without Barter 35 the reply is not offered |
| LR9 | Inquisitor at the Port: *"I'm leaving."* from several nodes | the conversation ends |
| LR10 | Iapetus at Toulouse: any goodbye | the conversation ends, and no quest is given |
| LR11 | The Surrey vendor, siege: *"Nevermind. Goodbye."* | the conversation ends with no fight |
| LR12 | The Rogue Inquisitor: *"moving along"* as a friend, then as a stranger | a friend is let go; a stranger is attacked; neither hangs |
