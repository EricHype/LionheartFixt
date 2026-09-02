# Lionheart Fixt - the mod, and its releases

Status: **0.5.1 built, not yet signed off**; 0.6.0 is scoped and not started. 0.5.0 was built and never published; its artifact crashes on entering the vault and is superseded. 0.1.0 through 0.4.1 are published; the sections
below are in reverse release order, newest first.

The diagnosis lives in [`design.md`](design.md); the
map-by-map work lives in [`plan.md`](plan.md). This document
is the other half: what actually gets packaged, under what name, in what order, and what
"done" means for each release.

## The name, and what it commits us to

**Lionheart Fixt**, after Fallout Fixt - a single, cumulative, community-maintained mod
that repairs the shipped game, restores what was cut, and adds new content, in that order
of confidence. Taking the name means taking the discipline that came with it:

- **One mod, one install.** Not a suite of optional patches the player has to reason
  about. The whole thing installs and enables as one id.
- **Fix, then restore, then extend** - each release visible in all three registers, so a
  version is never "just the new stuff".
- **Vanilla-compatible saves are not promised.** Fixt never promised them either. New
  factions and new dialogue nodes will not retrofit onto a mid-game save cleanly.
- **The original writers' voice is the house style.** Goblins speak in rhyming couplets.
  Anything new that does not is wrong.

## Packaging

| Decision | Value | Why |
|---|---|---|
| Mod id | `lionheart-fixt` | One id, cumulative, matching the Fixt model |
| Display name | `Lionheart Fixt` | |
| First version | `0.1.0` | |
| Format | `mod_format_version: 1` | The shape `modmanager.py` already installs |
| `requires` | none | Fixt must stand alone |

**Versioning.** `0.MINOR.PATCH` until the whole-game reactivity pass is in. Each MINOR is
one themed release that ships alone and is playable alone; PATCH is repair to a shipped
MINOR. 1.0.0 is when every act, not just the front half, has been through a reactivity
pass.

**Conflicts with the existing mods in this repo.** The scratch mods are not part of Fixt
and will collide with it on shared files. Recorded now so it is not discovered during a
build:

| Mod | Shared file | Note |
|---|---|---|
| `marco-the-pickpocket` | `Levels/1 Barcelona/Gate District.zax` | Fixt 0.1.0 touches Hrubjub's dialogue but *not* the Gate District map - no collision expected, but this is the one to watch if placement becomes necessary |
| `test-pocket`, `outpost-expedition` | `Herbalist Dialogue.DialogTree`, `Test Pocket.zax` | No overlap with 0.1.0 |

Last-enabled wins on conflict, so Fixt should load **last** in `enabled.json` during
development.

## Release map

| Version | Theme | Why this order |
|---|---|---|
| **0.1.0** | **The Horde** - the goblin thread becomes a faction you can join, and the camp starts reading your build | The most complete unfinished thread in the game. Almost no new machinery, one new quest, and it is the only evil path with writing already in place |
| **0.1.1** | **The Crossroads patrol** (built) - disarm the spawn-hostility, add the counter-contract on Esteban, and let the Templar exclusivity bite | Finishes the goblin theme while its machinery is fresh. Kept out of 0.2.0 deliberately: it is new writing, and 0.2.0's value is that it has none |
| **0.1.2** | **Standing** (built) - the camp reacts to your rank, and standing accumulates across every service rather than being granted once | Completes the faction as a thing with texture, not just a gate |
| **0.1.4** | **What playtesting found** (built) - Esteban's death is recognised, the rank titles stop naming a deed you may not have done, and the Goblin Girl's dead replies are repaired | The first release made entirely of play reports. Cut as its own version because the fixes change behaviour players had already seen |
| 0.2.0 | Link repair, whole game | 84 true dead ends. Ships standalone, needs no new writing. Deliberately *not* first: 0.1.0 needs to demonstrate the thing Fixt is for |
| 0.3.0 | **The Knights of Saladin** (built) - the order awards the rank, not just the title | The second minor faction. Ordered ahead of Quinn deliberately: the core repair is one faction assignment with four acts of payoff, which is far cheaper than a three-quest chain |
| 0.4.0 | **Quinn's reagents** (built) - three quests, three healing potion tiers | The project's first new content. Most of the assets already existed |
| 0.5.0 | Cut content into its right home | Titan quest, Guard Pablo, Isabella, the helpful wererat |
| 0.6.0 | **The Port District** - Fernand Desoto becomes the game's fourth companion, because his brother can finally be saved | The companion is written and wired on both sides and reachable by nothing. It exercises the companion machinery on the cheapest case before Grace or the Crypt need it |
| 0.7.0+ | The back half - the Crypt's war, the two new areas, the England companion | The largest work, and it wants the faction and reactivity templates settled first |

## The Crossroads patrol, and why it is hostile

Found while testing 0.1.0-rc1: talking to Guard Esteban about the local dangers makes the
Crossroads goblins attack, with no quest accepted. This is vanilla, and the mechanism is
now fully traced.

`30 Dangers` -> `500 goblins` -> `500 goblin continued` fires `Relay Name=goblin encounter`
unconditionally, unless `Corner Goblins Dead` is already set. There is no quest gate
anywhere on that path.

**The relay itself is innocent.** `goblin encounter` is a `CRelayAI` whose six actions
force-generate the Corner Goblins, activate the Scout Generator, set a patrol route to
`Goblin patrols here`, and fade in the Patrol Leader and Scout. It contains **no combat
action at all**, and it is `Trigger Only Once=1`.

**The hostility is in the template, and the fix is in the generator.** The spawned entity
is `Monster Cans/Mongol Gate District`, which carries `Valid Targets=Player,Player Friend`
and `Category=Enemy,Goblin` -- it aggroes on sight, with no script needed.

The decisive detail is that **Goblin Warrens spawns the same kind of goblin from equally
hostile templates and its villagers are peaceful**. `Mongol Archer Village` and
`Mongol SwordsmanVillage` also ship as `Valid Targets=Player,Player Friend` /
`Category=Enemy,Goblin`. What makes them neutral is two actions in the generator's
`After Action`, run at spawn:

```
Action=CSetTargetTypeAction
{
    Entity Name=$Instigator
    Name To Target=
    Valid Targets=            <- clears targeting
}
Action=COldBad_S_e_t__C_a_t_e_g_o_r_y_Action
{
    Target Name=$Instigator
    New Category=Goblin       <- drops "Enemy"
}
```

`Corner Goblin Generator` at the Crossroads has no `After Action` at all. That single
omission is the whole difference between a patrol you can walk past and one that charges.

**So the fix is small and fully precedented**: add that two-action `After Action` to
`Corner Goblin Generator`, and let the existing `goblin confrontation` relay -- which
already does `CSetTargetTypeAction` + `CGoToCombatAction` on the Patrol Leader -- turn them
hostile when the scene calls for it. Do not edit the shared template; it is used elsewhere.

**It should not ship alone.** A neutral patrol with nothing to say is worse content than a
hostile one: it removes an encounter and replaces it with nothing. This lands with the
counter-contract, which is the thing that gives a peaceful patrol a purpose. It is
also why the counter-contract could never have worked as scoped -- a patrol that is
already charging cannot offer you a job.

**Both shipped in 0.1.1.** This was briefly recorded as 0.2.0, which was wrong twice over:
0.2.0 is defined as link repair that needs no new writing, and `plan.md` had originally
scoped the counter-contract inside the goblin faction ladder -- 0.1.0's own theme. It also
no longer has to be rung 2 of that ladder, since rank 2 now comes from the shaman's eyes
quest, so it is optional content that can be sequenced on its merits rather than forced
into a release it does not fit.

## 0.6.0 - the Port District

**The Fernand quest is built and unplayed. The rest of the section is still scope.**
Every figure is measured against `data.dat.vanilla.bak` and is reproducible from the
scripts described under "how this was found".

The Sewers work closed with the thieves and the beggars roughly level. The Port District
is the next-largest cluster of Barcelona content, and it holds **the game's fourth
companion** - written, wired on both the dialogue and the map side, and reachable by
nothing.

### How this was found

Reachability, per tree: walk `Go to node ID` outward from every entry point and report
what is never visited. Entry points are the first node in the file, plus any node named
by a `Dialog Tree File=` / `Node ID=` pair anywhere in the shipped game. Both of those
fields sit in the same brace block **in either order**, so the block has to be delimited
properly rather than scanned forwards a fixed distance - a forward-only scan misses
entries and reports live balloons as orphans.

Across the district's **31 trees that is 111 unreachable nodes**, and most of them are
balloons and combat barks that a map fires directly. Sorting by "carries replies" cuts it
to **38**, which is where authored branches live. Two of those branches are cut content.
The rest are barks, superseded drafts, or one-line flavour.

Reproduce with:

```
python tools/reachability.py --survey "Port District"
```

That is `tools/reachability.py`, promoted out of scratch while this was being written -
which immediately corrected two figures in an earlier draft of this section. The
district has 31 trees, not 30: `Character Templates/Port District/Maria.DialogTree` sits
outside the `Dialog/` folder and a folder glob misses it.

### Fernand Desoto is a finished companion

`Distressed Sailor.DialogTree` - header `Name=Fernand Desoto` - is 31 nodes, **17 of them
unreachable**, and the unreachable half is the entire success branch.

Node `80 companion` runs a real
`CSetCompanionAction{Player=$Instigator, Companion=Distressed Sailor}`. That is the same
call that makes Cervantes, Cortes and Fang follow you, and those three are the only
companions in the shipped game. The map side is finished too: `Port District.zax` carries
a 14KB relay named `fernand joins you` that strips his `CSkeletonAI` and adds a
follow-capable one, swaps his `CAIInteractionSpecifier`, and gives him companion banter
through `100 companion banter` - *"Where you go, I follow."*

Nothing fires any of it. `1 return after saving juan`, the node the whole branch hangs
off, is **defined once and referenced nowhere in the game**. It offers six replies:

| Reply | Gate | Goes to | Pays |
|---|---|---|---|
| "I would like you to accompany me for a time." | none | `40 companion` | the companion |
| "don't you think his life is worth more than I was paid?" | Barter 20 | `40 hard barter` | chain mail, an Extra Healing potion, 100 gold |
| "I have great need of gold." | Barter 20 | `40 barter` | 100 gold |
| "Tell me about yourself." | none | `50 who are you` | - |
| two exits | none | - | - |

`40 companion` then gates the recruitment on **Speech 20 or Barter 20**, with a written
refusal (`70 rejection`) for anyone who has neither. Both routes reach `80 companion`.

### Why it is unreachable: Juan cannot be saved

The only Juan on the map is a `Fixed Dead Body Generator` at (5293,221) - a
`CSimpleGeneratorForCannedEntitiesAI` over `ShipSailorsonShipCanned`, `New Name=Juan`,
dropping leather armour and a club. The `sailor rescues brother` proximity trigger at
(5275,242) **unconditionally** plays `Sailor Juan / 100 dead` (*"you notice that it has
been very recently killed"*) and sets the quest to `VMS91BAX`.

`help distressed sailor.Quest.txt` ships with exactly two states and **neither is a
success state**:

- `S1NPX04I` - "Search the coast for Fernand's missing brother and see if it is possible
  to save him."
- `VMS91BAX` - "Return to Fernand and tell him that unfortunately, his brother perished."

You get 150 XP for reporting a death, and that is the whole quest as shipped.

But the rescue was written:

- `Sailor Juan.DialogTree` - *"Mi hermano! You saved me!"*, `1 Juan lives thanks you`, and
  male and female thanks nodes. **Three of its five nodes are unreachable.**
- Fernand's `20 still breathing`, `20 not breathing`, `30 saved juan`.
- Map position markers named for Juan - `juan heads to ship` (4639,1354),
  `juan travels back` (4345,1483), `juan travels back further` (4176,1703) - tracing a
  route from the island back to the ship. **These are not unused**, and an earlier draft
  of this section wrongly said nothing sends anyone to them: `sailor leaves` walks
  *Fernand* down all three, plus `sailor runs to help` and `distressed sailor goes here`,
  when the quest ends badly. Each of the five is referenced exactly once, by that one
  relay. That they carry Juan's name while moving his brother suggests the route was laid
  out for Juan and reused - but that is inference, not evidence, and it is weaker support
  for "the rescue was written" than the dialogue and the unused requirement are.
- The fight is there too: three `Vodyanoi agile Generator`s at (4967,231), (4987,549) and
  (5232,226), straight across the approach to the body.

### The intended mechanic is identifiable

When you take the job, node `30 take the job` hands you a healing potion: *"Take this
potion of healing, you might need it against those creatures."*

And `Dialog/Port District/Requirements/Player has a potion of healing.can` exists, checks
`CActionCheckForInventoryItem` against `Inventory Items/Potion`, and is **referenced by
nothing in the game**. It is one of four unused requirement files in the district.

Reach Juan with the potion still on you and he lives. That is the design, and it wants
wiring rather than authoring.

### The build

1. **A success state.** Add one to `help distressed sailor.Quest.txt` - "Return to
   Fernand and tell him his brother lives." Note this would be **the first shipped
   `.Quest.txt` Fixt edits**; all eight quest files it currently ships are new ones. The
   shape is an `Item Count=N` array of `State=` entries, which is the same edit made
   routinely inside `.zax`, so the risk is low - but it is a new file class and gets its
   own validator check and a first-entry playtest before anything else is judged.

2. **The rescue.** `sailor rescues brother` becomes a `CIfAction` on the unused
   requirement. Potion in hand: spawn Juan alive, play `Sailor Juan / 1 Save Juan`, set
   the new state. No potion: exactly what happens today, unchanged.

3. **A living Juan.** A `CGeneratorAI` beside the corpse generator, which stays for the
   no-potion path. The walk home copies `sailor leaves`, which already does
   `CAssignTemporaryTaskAction` over a chain of five `CGoToAI` for Fernand; Juan shares
   three of its destinations rather than claiming them, and his `CGoToAI` legs are
   lifted out of that relay byte-for-byte with only `Destination=` changed.

4. **Fernand's return branch.** His generator's interaction is a two-armed `CIfAction`:
   quest ever activated -> `1 Return 2`, else -> `1 Return`. `CIfAction` has one `Then`
   and one `Else`, so a third arm nests: put the brother-alive test outermost with
   `1 return after saving juan` as its `Then`, and the existing `CIfAction` as its `Else`.

5. **Rewards.** Nothing new is needed. Both Barter routes self-limit through the
   `fernand gave barter` checker, already placed at (4592,1759) and `Active=0`. Success
   XP is the one decision: the death report pays 150 through the `saved juan but died`
   entity, and a rescue should pay more - a **second** XP entity, so the failure path
   keeps its shipped value.

### What got built

The footprint on `Port District.zax` is **four parts added, two changed, none
removed**, out of 1317, plus one line changed and one node added in a shipped dialogue
tree:

| Part | |
|---|---|
| `juan goes home` | new, walks him back down three of `sailor leaves`' markers |
| `juan bleeds out` | new, the 45-second clock and the shipped failure path |
| `told fernand juan lives` | new checker, so the payout happens once |
| `saved juan and he lived` | new XP entity, 300 |
| `sailor rescues brother` | changed: the potion branch |
| `Distressed Sailor generator` | changed: a third arm to the reward node |

The no-potion path is the shipped balloon and the shipped quest-If, **character for
character** -- the verifier re-extracts both from the archive and compares. Juan's three
`CGoToAI` legs are lifted out of `sailor leaves` byte-for-byte with only `Destination=`
changed; each is ~75 lines of movement boilerplate, and retyping them is how a default
gets altered by accident. Fernand's shipped two-armed `CIfAction` survives untouched as
the `Else` of the new one.

Both gates pass. The quest-state check needed fixing first: it scanned only the mod tree
for activations, so the two states this quest inherits -- activated by vanilla maps we do
not ship -- would have been reported as dead. It now reads the vanilla archive too, with
our files shadowing their archive counterparts rather than being unioned with them.

### Decisions taken while building

- **The potion is consumed, and the rescue is a click on the body.** Both of these
  reverse what the first build did, and both came out of playing it. The first build
  fired on the proximity trigger, so the rescue happened *to* the player rather than
  being something they did; and it did not take the potion, on the grounds that vanilla
  only ever removes specific quest items. That second claim was simply wrong. DaVinci's
  Magic Machine asks for "a magical potion - any potion will do", tests
  `Inventory Items/Potion` and then removes `Inventory Items/Potion` -- the same generic
  path Fernand hands out. One survey of `CActionRemoveInventoryItem` had shown only
  `Specific Item Cans/...` uses and that was taken as the whole picture; four generic ones
  were in the same result set, further down. The known limitation stands, but is now a
  cost paid deliberately rather than a reason not to act: the remove carries no
  `Additions`, so it takes *a* potion and may take a better one than the healing potion
  Fernand gave you. Vanilla's own Magic Machine has exactly this flaw.
- **300 XP**, against the district's own scale: Helped Bartolome 250, Saved Tomas 200,
  the death report 150, the murder-mystery payouts 500. The failure path keeps its
  shipped 150 through its own entity; this adds a second rather than editing that one.
- **Juan is revived in place, not replaced.** The first build deleted the corpse and
  spawned a fresh Juan from a generator, which is precisely a teleport, and looked like
  one. The engine never needed that. `Genderate Dead Body` -- the shared canned script
  behind every corpse in the game -- *transforms an entity in place* in nine steps, and
  each one has an inverse: drop the `Corpse` category, make him collidable, re-add the
  `CAISetOpacityBasedOnVisibility` it stripped, and wake the CSkeletonAI it parked in a
  `CWaitAI`. Then `GetUp` plays on the body already lying there.
  - **Order is load-bearing.** `Raise Enemy Action.can`, the necromancy spell and the only
    shipped thing that raises one of these corpses, sends the `Raise Enemy` message
    *before* playing `getup`. That is not cosmetic: the corpse script's `CWaitAI` has
    `Completion Message to wait for=Raise Enemy`, and `CPlayAnimationAction`'s
    `AI To Interrupt=CSkeletonAI` has nothing to interrupt until the message restores it.
  - **The animation exists for this model**, which had to be checked rather than assumed:
    `Boatswain/Shared Animations/{01,02}/GetUp.ANIMATION.GR2` is on disk, and the
    pre-rendered sprite the game actually draws,
    `Cache/Models/Characters/NPC/Barcelona/Sailors/BoatswainMace.mdl16`, lists
    `Shared Animations/02/GetUpB` among its baked sequences. A source animation with no
    baked frames would have played as nothing.
  - **Double-clicking cannot cost two potions.** The whole interaction is wrapped in
    `CCheckCategoryAction` for `Corpse`, and the revive drops that category as its second
    action, so a second click during the get-up finds nothing to do. This is structural
    rather than a `Trigger Only Once` flag, which would have burned the one chance for a
    player who arrived without a potion.
- **A player who never took the quest can still save Juan.** The trigger is `Active=1`
  from map load, so anyone who wanders to the island with a potion sets `JUA1LIVE`, which
  starts the quest already at "go tell Fernand". Vanilla anticipates the no-quest case on
  the death path the same way, through `discoverd brother dead`. Fernand's greeting then
  says "thank you *again*", which is slightly off for someone he has never met.

- **Juan is dying, not dead, and he can run out of time.** Play turned up a line
  that the restoration itself had made false: the shipped bark on approach reads
  *"<Arriving at the body, you notice that it has been very recently killed.>"*, which is
  correct for a corpse and absurd for a man who sits up when you pour a potion into him.
  Rewording it is one line, but it cannot ship alone, and the reason is worth writing
  down. `VMS91BAX` -- the state vanilla sets the instant you walk up -- is what gates
  Fernand's reply *"No, I was not. I'm very sorry, but your brother has perished."* So in
  the first build you could walk up, immediately report him dead, walk back, and revive
  him. A bark that says he is *dying* makes that contradiction impossible to ignore, so
  the state had to move to a moment when it is true, and nothing in the vanilla design
  provides such a moment. The timer creates it.
  - The approach trigger now sets **no quest state at all**. It starts a 45-second relay.
  - The **shipped quest-state If moves across whole** -- both arms, character for
    character, including the `discoverd brother dead` branch for a player who never took
    the job. The failure path is not rewritten, only rescheduled.
  - **The delay is not cancellable, by design.** `CDelayAction` fires no matter what, so
    rather than adding a second mechanism to call it off, the delayed block re-checks the
    same `Corpse` category the rescue does. Healed Juan has no such category and the whole
    block does nothing. One guard, read in two places, instead of two mechanisms that can
    drift apart.
  - It lives on a **relay** rather than inside the trigger because the trigger deletes
    itself on the frame it fires. Vanilla gets away with ordering actions after that
    `CDeleteAction` because deletion is deferred to end of frame; ninety seconds is not.
  - **45 seconds**, down from 90 after the first playtest, where the clock did not
    fire at all -- for the ordering reason below, not because 90 was too long. Verified
    in play at 45. A `Vodyanoi agile Generator` sits 61 units from the body --
    Agile, Super and Tough -- so the player usually arrives into the fight Fernand
    describes. That is what makes the timer a decision (pour the potion mid-fight, or
    clear the creatures first and gamble) rather than a formality. Too short and it stops
    being a decision and becomes a reload.
  - **A relay must be fired before its trigger deletes itself. Confirmed in play.**
    The first build ordered `CTriggerRelayAction` *after* the `CDeleteAction` that removes
    the trigger, and the clock silently never ran. Moving the relay call one slot earlier
    fixed it, and Juan now dies on schedule.

    This is worth stating as a general engine rule, because everything else about the
    relay was already correct and none of it was the problem: `Relay Name` is the only
    field the game ever uses (4021 times), `Forget Trigger=0` is what all 4089 shipped
    `CDelayAction`s use, a 130-second delay inside a `CRelayAI` is shipped, and
    runtime-added categories *are* visible to `CCheckCategoryAction` -- vanilla both adds
    and checks `Player Friend` and `Scripted Custom 1`. Chasing any of those would have
    been wasted effort.

    What found it was asking a narrower question: *what does this build do that no shipped
    map does?* Of the two vanilla enter-actions containing both a `CDeleteAction` and a
    `CTriggerRelayAction`, neither orders the delete first. That was the only deviation,
    and it was the bug. The trap is that vanilla **does** put a `CIfAction` and a
    `CDeactivateAction` after its self-delete and those demonstrably run -- deletion is
    deferred to end of frame -- which makes "actions after a self-delete are fine" look
    like a safe general rule. It is not: those actions need nothing *from* the trigger,
    whereas dispatching a relay evidently goes through it. The failure is silent, with no
    error and no partial effect.
  - **A regression the timer introduced, still open.** Vanilla set `VMS91BAX` the instant
    you walked up, so the death report to Fernand was always available. It is now set only
    when the clock runs out. A player who looks at Juan and walks off the map probably
    loses the pending delay along with the layer, which would leave the quest stuck at
    "I have not found him yet" and the shipped 150 XP report unreachable. The short clock
    makes it much more likely the question resolves while the player is still standing
    there, but that is mitigation, not a fix. If play confirms it, the answer is probably
    a second always-on trigger that resolves the state on re-entry.
  - This is the first **timed failure in the game**. Nothing in vanilla fails a quest on a
    clock -- no shipped quest state mentions running out of time -- so it is a new kind of
    pressure for Lionheart, and the main thing to be suspicious of in play. The primitive
    is not new, though: `CDelayAction` at this scale is shipped (vanilla runs one at 130s),
    and the map already uses `CLimitedTimeAI`.
  - It stays **losable, never unwinnable**: failing just routes to the vanilla death
    report, which still pays its shipped 150 XP and 100 gold.

### What to play

No QA cases yet, deliberately -- 0.5.0's lesson was that they should be written against
what play shows rather than what the build intends. Needs **a save that has never entered
the Port District**. Four routes:

1. Take the job, keep the potion, reach the body. You should get the shipped "he's dead"
   balloon on approach, exactly as in vanilla, and then the cursor should turn to the
   Interact hand over Juan. Click him: the potion goes, he plays a get-up animation,
   thanks you, and walks off toward the ship.
2. Take the job, arrive without a potion. Clicking him prints that he is beyond your
   help, and leaves the body clickable -- but the clock is running, so coming back with
   one is only possible inside 45 seconds.
3. Take the job and stand there. After 45 seconds he dies -- **confirmed in play**.
   Still to check: that the body stops being clickable, that only then does the log say to
   tell Fernand he perished, and that reporting it pays the unchanged vanilla 150 XP and
   100 gold.
4. **Whether the clock survives leaving the map is not known and needs watching.** The
   engine swaps a level out when you leave, so a pending delay may pause, may resume, or
   may be lost. All three are survivable -- worst case he stays savable indefinitely --
   but which one happens decides whether "go buy a potion" is a real option.
5. Report back to Fernand after 1. The reward node should open, pay 300 once, close the
   quest, and offer the companion at Speech 20 or Barter 20.
6. Recruit him, and take him somewhere. This is the first time the companion machinery
   has ever run for this character.

### Open decisions

- **The potion check is loose.** `Player has a potion of healing.can` tests for
  `Inventory Items/Potion` generically; Healing and Extra Healing are distinguished by
  their `Additions`, not the item. As written, any potion passes, so a player carrying
  one for any reason gets the good ending without spending Fernand's. Recommend accepting
  the vanilla file's own looseness rather than tightening it: it only ever helps someone
  who came prepared, and using the shipped file unmodified is the stronger claim about
  what was intended.
- **Fernand is fragile.** `Distressed Sailor.can` points at `Races/NPCs/Sailor` - a real
  race, so not the dangling-self-reference bug - at **36 HP and AC 90**, against the
  Wererat Boss's 150. Recommend leaving him: the writing is explicit that he is a sailor
  of modest means breaking a vow of duty, and a companion you have to keep alive is the
  more interesting object than a repointed one. Revisit only if play says he dies before
  he can say anything.
- **Where he can follow.** He has one banter node and no hurt or combat barks, unlike
  Cortes, who has ten. Nothing needs stripping, but he will be silent in a way the other
  companions are not, and that is worth seeing in play before deciding whether to write
  any.

### The rest of the district

| Item | Verdict |
|---|---|
| Port guards' murder reaction - `200 Duke is Dead`, `300 assassination`, `500 tragedy` | Written, never plays. Cheap, and it makes the Duke's death visible in the streets. **In scope.** |
| Fish Monger `60 sold skull normal price` | Orphaned branch of the Vodyanoi Skull sale, which the sailor quest now sends players past. **In scope, small.** |
| Brendan Michael Sullivan, the Irish sailor | `200 irish`, `200 name`, `200 drink`, `200 insult` - dead in **both** `Bar Patrons` (5 replies) and `ShipSailorsonShipCanned` (4 replies). Two copies of the same tavern character, both orphaned. **Probably in scope**; needs a read to decide which copy is the live one. |
| `Gather the drunken sailors from the tavern` | Zero states, referenced only by the fall-of-Barcelona failure sweep, and `DrunkSailorsInBar.DialogTree` is seven ambient barks with no quest content. Nothing to restore - it would be new writing. **Out.** |
| Cortes `165 help with arm` -> `170 accept cortes arm quest`, and the unused `Cortes Help Him Rebuild Arm.can` | **Not touched.** This looks like a superseded draft, not cut content: the reachable `164 cortes needs to repair the arm` does the same job, and the two activate *different* states of the same quest (`165` jumps to `WEDKYW9X`, skipping `EPVSO4Y0`). This is exactly the shape misread twice during 0.5 - it gets a proper read against the quest's six states before anyone calls it either way. |
| Bartolome's `80 thank you`, handing out Boots Arid dJinn | Orphaned, but `100 saved brother` is reachable, gives the same boots and completes the quest. A draft, not a loss. **Out.** |

### Explicitly not in it

**Grace O'Malley.** Isabella's tree carries eleven unreachable `500`/`502`/`503` nodes for
the England act - `502 grace joined romantic`, `502 grace companion near death`,
`503 druids` - with matching `.ogg` files sitting in her Port District VO folder. They are
unreachable for a blunter reason than Fernand's: `Captain Isabella.DialogTree` is opened
by exactly one map, `Port District.zax`, and she is never placed in Act 7 at all.
Restoring her means placing a character in the English Shrine and deciding what her
presence does to that act's ending. That is a release of its own, and it belongs after the
companion machinery has been exercised once on Fernand.

### Gates before this ships

- `tools/validate.py` extended with a `.Quest.txt` check: state IDs unique, `Item Count`
  matching the array, every ID referenced by a `CActivateQuestStateAction` or
  `CIsQuestStateTheCurrentStateAction` somewhere.
- `tools/reachability.py` in gate mode (**built**, and now part of Gate 0 as A0.13): no
  node this mod adds may be unreachable. Nodes already orphaned in the shipped tree are
  tolerated, since a Fixt tree is usually a shipped tree with nodes spliced into it - it
  currently tolerates 69 and passes. Negative-tested against both halves of the rule: a
  new node nothing links to, and a broken link orphaning a node that used to be reachable.
  This release exists because that check did not exist, and it should not have to be
  rediscovered.
- **A save that has never entered the Port District.** New entities on an edited map do
  not appear on a save that has already visited it, and this release adds several.
- The vodyanoi fight, the potion route, the no-potion route, and the recruitment played
  separately. Nine defects in 0.5 passed parse, byte-identical round-trip, every validator
  check and verified deployment, and were visible only in the running game.

## 0.5.1 - the two crashes 0.5.0 would have shipped

0.5.0 was packaged and never tagged. Play found two fatal errors within minutes of each
other, both on entering the vault, both the same underlying mistake: art referenced
without being checked against the archive.

- **`Model=Environments/Misc/Chest/Chest A` does not exist.** An invented path. The game
  dies on map entry with a "Fatal Not Found Error" naming the model and the map.
- **`Cur Sequence=Idle` on a chest.** Chest models have `Closed`, `Open` and `Opening`,
  and no `Idle`. Same dialog, same fatality, one field over -- found immediately after
  fixing the first, because fixing the model did not prompt me to check the animation on
  it.

Both are now gates. `tools/validate.py` asserts every `Model=` exists, and that every
`(Model, Cur Sequence)` pair a Fixt file introduces is one the shipped game uses for that
model -- 200 vanilla maps are a better authority on which animation belongs to which
model than anything inferred, and it means the check reports the correct value rather
than just refusing. Both were written before their fix and confirmed against the real
crash. Neither existed before, which is exactly why 0.5.0 was packaged with two of them
after passing every other check, round-tripping byte-exact and deploying byte-identical.

A sweep of every entity this mod adds across all four edited maps found no other
instance of either fault.

### The guard attacked after the Speech check passed

Also found in play. The quiet routes ran `CDeactivateAction` on `Secret Quest Guard`,
which is the **generator**, not the man. The spawned guard carries three AIs of his own
and one is a `CTouchingOvalTriggerAI` holding `CGoToCombatAction` -- a proximity trigger
that fires when you walk into his oval regardless of anything said. Deactivating the
generator only stops it spawning a replacement.

He also spawned as `New Name=Sewer Thief`, shared with every thief in the den and with
the mass-hostility relay's target list, so he could not be addressed individually. He is
now `Vault Guard` on that generator alone; the other eight `Sewer Thief` spawners are
untouched. The four quiet routes strip the proximity trigger and clear his targeting --
`CRemoveAIAction` and `CSetTargetTypeAction`, both idioms vanilla already uses in that
map and in the jail relay -- and the fight route names him explicitly rather than
relying on `$Trigger` scoping.

One consequence: because he is no longer called `Sewer Thief`, the mass-hostility relay
does not include him. On the fight route he is made hostile directly, so that path is
unaffected, but if the den is roused some other way while he lives he will not join in.

## 0.5.0 - the thieves' guild

**Not signed off.** Of the three things in this release only one has been played: the
final job, end to end, by a tester on the day it was built. The caught-in-the-act
branch and the vault job are built, verified and unplayed. `docs/qa.md` SR1-SR42
covers the first two; the vault has no cases yet, deliberately, because they should be
written against what play shows rather than what the build intends.

### Why the thieves needed it

Counted properly, Enrique offers five jobs and Juanita four. He pays out around 600
gold across his line; she has seven `CTakeMoneyAction` and not one give. The single
biggest quest in the Sewers -- the wererat cure, five states across three maps -- is on
his side. Her jobs pay more XP each (500 against 200), but there is one fewer of them
and they cost money to take.

Her fifth job was written and never reachable. `130 Final Job` is the only thing that
activates `Thieve in Temple District`; nothing reaches node 130; that quest's second
state is activated by nothing; and the requirement `.can` written to gate its turn-in
is used nowhere. The frame shipped whole with nowhere to happen.

### The first new map

There was no house to rob, so this adds one. That is possible because no file registers
the 200 shipped maps, a room's walls and floor are a single prefab entity rather than
baked terrain, and -- per the tools repo's own `test-pocket`, built from scratch and
shipping no caches at all -- the engine generates the waypoint graph and automap when
they are absent.

The entrance took three attempts and the two failures are worth keeping. An unnamed
door with a `CDoorAI` and an empty `After Opened` looked like an unused entrance; it is
the only door in Barcelona that draws behind its own building, sitting at 48% across
and 49% down the House Of Ilk's sprite, and the ground behind its fence is unreachable.
Both are why it shipped dead. The second attempt then treated walkable ground as
reachable ground -- the `.way` positions decode reliably, but connectivity lives in the
edge lists, which do not.

### Getting caught

Skill decides the cost, not whether the job is possible. Vanilla's own equivalent
robbery has no gate at all: the entity named `hidden poly reveaked if perception check
passed` is `Active=1` with zero activations anywhere. Here, Perception 5 or Find Traps
35 gets you out quietly. Without either, a guard is waiting outside. Surrender copies
`Eduardo Sends you to jail` and lands you in `Inquisition Chambers2 @ Jail Start`, where
Sanchez already handles the fine, the Speech routes and release -- and nothing in that
flow strips inventory, so the quest survives a sentence. Fight instead and Juanita
takes you anyway, with a word about drawing the watch onto the guild.

She reacts only to *this* arrest. Vanilla's `been in jail before` is set and read only
inside `Inquisition Chambers2`, purely to pick Sanchez's greeting, and six shipped
routes reach that cell; keying off it would have made her hostile over a Templar
scuffle. Two new markers carry it instead.

### The vault

`09 Secret Quest` is a 324KB map -- spike-trap doors, thief archers, guard dogs, ~950
XP of markers -- that no quest points at, behind a door that is unlocked. Its guard is
fully built and `Active=0`, so today you are shouted at twice by warning balloons
belonging to someone who is not there, and you walk in.

Taking Skulker's job switches him on. Five ways past: the `Thief Friend` perk, Speech
40, a hundred gold at Barter 35, Sneak 35, or steel. Fighting fires vanilla's own
`Thief enemy trigger` -- `CGoToCombatAction` over Sewer Thief, Juanita and the dogs,
plus `Make unspawned thieves mad at player` -- and the den comes for you. Quiet costs
nothing.

Skulker rather than Juanita for a reason: after the seduction she is stripped of her
interaction specifier and walks out through `secret door2`. She is not deleted, but she
can never be spoken to again, so her arc has a hard terminus.

### Repairs found on the way

- **Juanita's fee was avoidable.** Refuse her 70 gold, walk away, come back, and the
  reply "I've decided to pay you for another lead" handed it over free -- no
  `CHasMoneyAction`, no `CTakeMoneyAction`. Node `81 decided to pay` charges 100 and was
  unreachable, and `Juanita requires player to have less than 100 gold` ships used
  nowhere. Both are now wired.
- **The night with Juanita explains itself.** `Juanita Seduction` ships with real text
  in all nine nodes but no replies in any of them, so it opens and closes on its own and
  does not register. The low-charisma path takes up to 500 gold and tells you only
  through that box.

### Gates

`tools/validate.py` passes at 97 files. Every map edited round-trips byte-identically
through `resource_format`, and the deployed `data.dat` was byte-compared against source
after every change. Check A0.7b caught a hard crash before it shipped -- an empty
`Node ID=` in the guard confrontation poly.

None of that is a substitute for playing it, which is the whole point of the note at the
top of this section.

## 0.4.1 - repair

**No new content.** Every line of this release fixes something already shipped, and two of
the three items were only found because 0.5's work made a player walk paths that had never
been walked.

### The blank line

A reply in a `.DialogTree` must be preceded by an empty line. Vanilla holds this without a
single exception -- 10915 replies, zero violations -- and the parser needs it: without the
separator a reply is swallowed into the one before it, so it never becomes its own choice and
its `Custom Action` never runs. The failure is silent and looks nothing like its cause. A
conversation plays through normally and a quest simply does not advance.

Fixt has been shipping that defect since 0.2.0, in **47 places across six conversations**,
because every helper used to reorder or append replies rebuilt the node by joining on a single
newline:

| Conversation | Sites | Shipped in |
|---|---|---|
| Herbalist (Quinn) | 21 | 0.4.0 |
| GoblinKhan | 5 | 0.2.0 |
| Jafar (Amir) | 2 | 0.3.0 |
| saladinknightcan | 1 | 0.3.0 |
| Guard Esteban | 1 | 0.2.0 |
| Blacksmith (Eduardo) | 1 | 0.5 work |
| Warning Troll | 16 | 0.5 work |

Jafar's `3 Return Dialogue` being on that list matters: it is the node the Sacred Scimitar
hand-in was moved to after being reported unreachable **twice** in 0.3.0. The move was correct
both times. It was very likely landing in a malformed node all along, which means that
diagnosis was wrong.

### Two of Quinn's three errands could never be started

The replies offering the wasp stingers and the troll hide carried a `Custom Requirement` --
the gate deciding whether to *show* them -- and no `Custom Action` at all. Quinn asks, the
player agrees, and the quest never activates, so both turn-ins stay invisible and both errands
are uncompletable. That is two thirds of 0.4.0.

`QN8HD4LM` also gates the Warning Troll's peaceful trade reply, so the non-violent route to a
lava troll hide was dead as well.

### Esteban's contract never closed its journal

`Kill Guard Esteban for the Goblin Patrol` defines a second state -- "Esteban is dead. Return
to the goblin patrol leader and collect what you were promised" -- that nothing ever set, so a
player carrying his corpse still read "kill him". The hand-in always worked, being gated on
his death rather than the state; only the log was wrong. Now hooked into the death script and
guarded on the contract actually having been taken, so it cannot retroactively hand a goblin
contract to somebody who killed him for the Templars.

### Two new gates, because none of the above was catchable

`tools/validate.py` now fails on a reply that is not preceded by a blank line, naming the
node, and on any state of a Fixt-authored quest that is never activated. Both were verified by
deliberately breaking them. The second immediately caught the Esteban state -- and then caught
its own first implementation being wrong, because the regex assumed no indentation, which
holds for DialogTrees and not for tab-indented `.can` files.

### What is NOT in this release

The Sewers faction work -- troll peace, the Tomas ransom, three allied errands, the
desecration scene -- is on `main` but is **0.5.0**, unfinished and lightly played. None of it
is reachable on an existing save, so it is inert for anyone installing 0.4.1 over 0.4.0.

## 0.4.0 - "Quinn's Reagents"

**The first release that is mostly new content**, and it should be read as a deliberate
crossing rather than more restoration. The project's order is fix, then restore, then
extend, and this is extend.

What makes it cheap is that almost none of it needed authoring. Two of the three reagents
already exist as items with finished art, and one of them -- `Lava Troll Hide` -- was
referenced by **nothing at all** in the shipped game: a quest item for a quest nobody wrote.
The three healing tiers were already built in a separate mod, shipping into a test map where
no player could reach them.

### The chain

| Errand | Reagent | Unlocks |
|---|---|---|
| 1 | three wolf pelts | Great Healing |
| 2 | five wasp stingers | Superior Healing |
| 3 | one lava troll hide | Supreme Healing |

Strictly ordered, and **paced by where each reagent lives** rather than by a level check --
which is the whole reason the order matters. Supreme Healing is roughly four times Extra
Healing and would wreck act 1 if it arrived there.

### Three ways to the hide, so nobody is locked into hostility

Vanilla wrote a diplomatic opening to the lava trolls and closed it. Every branch of
`Warning Troll.DialogTree` ends in combat or walking away, and killing one turns the whole
pit. But the troll states his grievance unprompted, and it is **pragmatic, not moral**: the
wererats are killing his people, and he does not care how that stops.

Because the Beggars *are* the wererats, both endings are already tracked vanilla quests:

| Route | Read |
|---|---|
| Cure them | `Discover a cure for wererat lycanthropy` |
| Exterminate them | `Kill The Beggar Master`, or `Help the Thieves Destroy the Beggars Guild` |
| Kill a Lava Troll Boss | it drops the hide |

Good path, evil path, or no diplomacy at all. The route deliberately does not reward mercy
specifically -- vanilla's own cure quest requires killing the Prime Wererat for a patch of
fur, so framing it that way would be dishonest.

### The Wolf Trapper perk locked you out of the errand

The migrated wolf-pelt mod consumed the plain `Wolf Pelt`. Every wolf can branches on
`Wolf Trapper Perk Checker`: without the perk you get one plain pelt through a canned list,
with it you get two `Wolf Pelt Perk Quality`. So taking the perk handed you pelts your own
quest would not accept. Either now counts, at each of the three units.

*(My first diagnosis of this was wrong -- I said the quest was uncompletable by anyone,
having missed the canned-list indirection. The user had completed it in play. Corrected in
`321a9cb`.)*

### Also in it

Gate 0's validator moved into the repo at [`tools/validate.py`](../tools/validate.py). It
had been described as scripted since 0.1.0 while only ever existing in a session scratchpad.

## 0.3.0 - "The Knights of Saladin"

### The order awards the title and never the rank

The Dream Djinni trials are reachable and completable, and they award `Dervish of the
Crescent` -- whose own text reads *"You have become a **Favored One of the Knights of
Saladin**"* -- or `Scholar of the Crescent`, chosen by whether you beat Kabool in combat or
in a contest of wits. Both are perks, and perks confer only skills.

`Dream Djinni Map.zax` performs **0 faction assignments and 0 Saladin Rank writes.**
Meanwhile `Saladin IS` tests `Uber Perks/Saladin Rank > 0`, and the only things that
increment that counter are the three `.Faction` records -- assigned nowhere in the shipped
game except `Levels/Test Maps/James/James.zax`, a test map.

So the title and the rank were never connected, and **20 replies across four acts can never
appear:**

| Where | Replies |
|---|---|
| Quinn the Herbalist, Gate District | 6 |
| Sir Roger, English Shrine | 7 |
| Brother Michel, Montaillou | 3 |
| Joan of Arc, the Crypt | 3 |
| Temple Entrance Guard, Gate District | 1 |

Plus node-level greetings: both Barcelona knights have *"Welcome, brother into the Order of
Saladin"* nodes, and the Alamut companion has male and female Saladin variants.

**The repair is one `CAssignFactionToCharacterAction` for `Factions/Saladin Aswaran`, beside
each of the two perk grants that already fire.** Aswaran is the entry rank, which matches
"Favored One" and leaves Blessed and Exalted as headroom.

Safe against double-assignment two ways. Each grant is already wrapped in a *"does the
player not already have this perk"* guard, so it fires once; and faction tiers replace
rather than stack -- the lesson 0.1.4 learned the hard way with the goblins -- so a player
who somehow earned both trials still lands on Aswaran at rank 1, which is all `Saladin IS`
needs.

Note the stacking that becomes visible for the first time: the faction record adds +10
One-Handed, +10 Two-Handed, +1 Endurance and +20 carry weight on top of Dervish's +5s. That
is vanilla's arithmetic, but nobody has ever had it applied.

Six of the twenty replies are on **Quinn**, which is a useful accident -- he is metres from
the Dream Djinni, so the cheapest test of this fix is also the character the next release is
built around.

### What else shipped in it

**The Sacred Scimitar questline, restored.** Fully authored, unstartable, broken at all
three ends -- the starter was a proximity trigger with both `Active=0` and `X Radius=0`,
Amir's second-task node was a fork that had lost an arm, and the hand-in reply pointed at a
node that does not exist while carrying the quest's completion action. Routed through Amir
rather than by re-enabling the dead trigger, which is ungated and would hand the quest to
anyone who walked into the smithy.

**Farshad's conversation.** Sixteen nodes, including two "Welcome into the Order of Saladin"
greetings, hidden because his talk interaction opened a *balloon* of `10 Goodbye` and
`saladinknightcan` was never opened as a tree anywhere. Third instance of that bug shape
this project has found.

**The scimitar remembers how you earned it**, and the Dream Djinni sets it alight rather
than handing you a duplicate. See the release notes.

### Four vanilla defects the restoration exposed

All four found by playing, none catchable by Gate 0, and all invisible before because the
questline could not be started:

| Defect | |
|---|---|
| The quest could move backwards | `I8FFAL7P`, the state Amir's gate needs, is set in exactly one place; the other reply at node 64 sent the quest back to "Do as Blacksmith requests" with nothing to advance it again |
| The hand-in was unreachable | Its reply sits on `15 questions`, entered from seventeen topic nodes and never from the greeting the map opens |
| A duplicate reward | The combat trial hands out the same Sacred Scimitar -- almost certainly the cut quest's payoff, relocated |
| A near miss | Enchanting the blade would have broken Farshad's lesson gate, which tested only for the item |

**The lesson of the release:** restoring content runs code that has never executed. Static
verification proves every reference resolves and tells you nothing about any of this.

## 0.2.1 - the bandit you killed before he asked

A patch. One relay in `Crossroads.zax`, `After Verify thief display dialog tree`, opened
`113 Thief success` -- *"Good work! Here is your justly deserved reward"* -- when the only
path that can reach it is the one where Esteban never gave you the job. `114 pre assigned
thief success` was written for it and reached by nothing.

The path is provably exclusive: `140 verify too` has two inbounds and both sit behind
`Esteban will not reassign thief quest`, which succeeds only when `Find the Crossroads
Bandit` was never activated.

Corroborating, and the reason this was findable at all: the shipped gate `Esteban requires
bandit dealth with before assinging quest` -- the bandit quest *completed* -- is read by
nothing anywhere in the game. Built for this state and never wired, the same shape as the
`Goblin Horde Midlevel` gate that 0.2.0 finally gave a reader.

### Pointing the relay at 114 exposed that 114 was unfinished

Consistent with it being the arm that got dropped. Both gaps closed with lines and targets
already present in the tree:

- Its wasps reply had an empty target. Both nodes complete `Slay the Giant Wasps` inline
  and pay 100 gold, but 113 continues to `103 wasps killed` and 114 did not, so handing in
  the wasps on this path ended the conversation with no acknowledgement. `103 wasps killed`
  completes nothing and pays nothing itself -- checked before retargeting, because
  double-payment is exactly how this class of fix goes wrong.
- It had no goodbye, and its default reply advanced to `35 dangers 2` rather than closing.
  It now carries 113's *"I should be on my way."* as the default.

`113` is untouched and still reached from six places, which is the regression to watch.

**This is a voice fix.** The 150 gold, the experience and the quest completion all worked
before.

## 0.2.0 - "What Was Written"

Almost everything here was written by Black Isle and never reached the game. Not cut lines
in a leftover file -- finished nodes, in the files the engine loads, that nothing in the
game can ever open. The release is named for that.

It is also the first release scoped deliberately rather than by opportunity. The survey
found 84 repairable dead ends across five acts; shipping them all would have been more
surface than one person can play-test, so 0.2.0 stays inside the goblin thread that 0.1.x
already established.

### The Goblin Girl's follow was written and never wired

Vanilla ships `90 Follow`, `190 Follow 2` and `195 Follow 2 no snails` -- three terminal
nodes in which she announces she is coming along, each with no replies and no action. Their
neighbours carry `Action work in progress=girls walks away` and `girl storms off`, the
original designers' inline to-do key, so the whole gesture was cut rather than forgotten.

The engine has exactly one follow mechanism, `CSetCompanionAction`. There is no generic
follow AI: `CApproachTargetAI` and `CPursueAI` have zero uses in shipped content and
`CGaurdNearMovingPosAI` has no target field. Companions cross map transitions, gated on
"You must gather your party", and vanilla bounds them with a remover entity on each map
where they are unwanted -- `Remover of Barcelona Companions` appears on eight. The Warrens
is cheap to bound because both its exits relocate to the same map, so the release happens
at the exits themselves, behind a farewell node.

**Confirmed in play.**

### The Khan's war campaign, and the fight for walking out of it

`350 next task` -> `360 attack barcelona` -> `365 barcelona walls`, all vanilla, all
orphaned, all reply-less. `365` names Guard Esteban as step one of an invasion -- which is
the motive the Esteban contract has never had, one release after 0.1.4 made that kill pay
out. `400 Where are you going?` was a fourth orphan and is what refusing the campaign now
reaches.

Gated on Champion, the rank the Khan himself grants. One new node, `370`, for the case Fixt
created: a player who killed Esteban before ever hearing why.

**The horde never does attack Barcelona.** Act 6 has essentially no goblins in it. The
briefing restores the plan the Khan states and leaves it stated; wiring the second half of
the order is buildable -- the Gate District holds nine `Gate Guard` entities and a
`Barcelona Portcullis` -- but it would resolve to nothing, and a tracked objective that
visibly fails to pay is worse than a stated plan that never happens.

### Grumdjum's post-dryad conversation opened a bark

One field. Handing in the dryad kill despawns him and spawns a second copy at her body,
whose talk interaction opened `160 After Dryad death bubble` -- one line, no replies -- instead
of `8 Return Dialogue Dryad Dead`. The tree proves the intent: node 8's own exit reply goes
to 160, so the designers wrote the bubble as the sign-off and the wiring sat one level too
shallow.

Node 8 is the sole gateway to `100 Goblin City`, where he says to seek the goblin city
*through the waterfall to the east* -- the only in-world direction to the Warrens that
exists -- and to `200 new poem`.

### Standing counts with the goblin jailor

The Darsh escort scene is fully wired in vanilla and needed no repair; it offers one
non-violent way past the jailor, Speech 25. `Goblin Horde Midlevel` had been built in 0.1.2
and read by nothing, so Blooded and Champion now pull rank instead. Adds a route, removes
none.

### Five dead replies

One dangling target in Inquisitor Darsh's tree, cleared rather than retargeted because all
four replies on that node fire a relay and the relay is the outcome. Four blank options
that did nothing when clicked -- deleted where the node had other replies, marked as the
default close where they were its only exit.

### What the survey got wrong

The scan that found this release -- a node nothing reaches, counting both the tree's own
`Go to node ID` and every `.zax` that opens it -- runs at about a one-in-three hit rate.
Three leads were investigated and cleared, and are recorded in `qa.md` so they are not
re-opened: the goblin jailor (vanilla wires it end to end), the captive child on Scar
Ravine (a duplicate node ID in a sibling file), and the Woodcutter's A-1 through G greeting
matrix (superseded by two consolidated nodes, not cut).

### Explicitly out of 0.2.0

**Grumdjum's companion arc** -- ten nodes covering join, dismissal, rejoin, injury barks and
combat quips, all in rhyming couplets. His join line is about Alamut, the Khan's `500 Start
in Persia` is a matching cut goblin companion for the same act, and neither has a companion
generator on any map. One cut Act 8 feature, and it should return with Act 8.

## 0.1.4 - "What Playtesting Found"

*Written up as 0.1.3 and never published; more fixes landed before it went out, so it
ships as 0.1.4 rather than leaving a version that exists only in this repository.*

Everything here came from a play session rather than from reading the archive, which makes
it the first release whose contents could not have been planned.

### Rakeb's unreachable greetings

**Rakeb had 33 nodes and the map opened two of them.** Three finished return-greetings were
unreachable, because `3 Return Dialogue` was shown unconditionally and swallowed every
situation they were written for:

| Node | What he says | When it now shows |
|---|---|---|
| `115` | *"You return, but we do not see the eyes. Find the woodsman and return with them."* | you took the eyes job and have not delivered |
| `63` | *"I knew you would return. I have a job for you."* | the devil fish are dead, the second task untaken |
| `136` | *"We hope the items have served you well..."* | all his business concluded |

He now has a selector on the same pattern as the Goblin Girl's -- most specific first, each
rung a strict narrowing of the one below, with `3 Return Dialogue` as the fallback. His
first-meeting node is untouched.

**Confirmed in play**: returning with the eyes job outstanding produces node 115 rather than
the generic greeting. That also settles a question the selector depended on --
`CIsQuestStateTheCurrentStateAction` does evaluate correctly from a map interaction, not
only from a dialogue requirement.

Two orphans are deliberately left alone. `200 dead woodcutter` has no text and no replies:
an empty placeholder, with nothing to restore. `300 shaman` and `300 shaman 2` are
Khan's-court guard lines sitting in the wrong file -- no map anywhere opens Rakeb's tree at
them, and inventing a reason for a shaman to shout *"Bow before the Great Plumdjum Khan, you
worm!"* would be writing new content rather than restoring it.

An audit of the rest of his tree found nothing else wrong. Two things that looked broken are
not: `43 Crazy`'s *"You'll die for that remark!"* has no target because it carries
`CGoToCombatAction`, and the two identical *"I have killed the Devil fish"* replies on node 3
are mutually exclusive -- one requires the Darsh rescue quest to be current, the other
requires it not to be.

### Two rewards were repeatable

**Two rewards could be collected over and over.** The Goblin Girl handed out a liver pie
every time you asked, and Rakeb would re-issue the devil fish quest as often as you cared to
say *"speak to me as clan"*. Same defect in two shapes: a one-time transaction offered from
a node the player returns to freely, with nothing asking whether it had already happened.

Her node 200 is the greeting for as long as the woodcutter is dead, and its *"Here, I
brought you his liver"* reply led to the pie unconditionally -- it did not even check you
were carrying a liver. It is now gated on a flag set when the pie is handed over, so the
reply disappears once the exchange is done.

Rakeb's offer already carried a guard -- `NOT exists("killed all fish")` -- so vanilla did
think about it, but that only rules out re-taking the quest *after* the fish are dead. It
says nothing about taking the quest, walking away and coming back. Vanilla's test is kept
and ANDed with whether the quest was ever activated.

### The faction tiers replaced each other

**Faction tiers replace each other, and that broke the ranks.** The in-game log settles
what no amount of reading the archive had: taking Goblin Blooded prints *"-10 modifier to
Sneak, -10 to Poison Resistance, -10 to Carry Weight"* -- Goblin Chum's whole package being
withdrawn -- and then applies Blooded's. A character holds one faction, not a stack.

Two bugs fell out of that. Every tier granted `+1 Goblin Rank`, so promotion removed the
old `+1` and added a new one and **the rank never exceeded 1** -- which is precisely why the
Crossroads contract kept refusing players who had earned it. The gates were correct; the
number they read was not. Each tier now grants its own number: 1, 2, 3.

And because the previous package is withdrawn, each tier has to be a strict superset of the
one below or promotion is a demotion. Champion granted Barter +6 against Blooded's +8 and
dropped Blooded's disease resistance entirely. The tiers now escalate the way vanilla's
Templar line does -- melee 4, then 8, then 12, each keeping everything beneath it:

| | Chum | Blooded | Champion |
|---|---|---|---|
| Sneak | +10 | +18 | +30 |
| Barter | -- | +8 | +14 |
| Poison Resistance | +10 | +20 | +35 |
| Disease Resistance | -- | +10 | +10 |
| Carry Weight | +10 | +10 | +30 |
| Agility | -- | -- | +1 |
| **Goblin Rank** | **1** | **2** | **3** |

Each tier grants the **running total** of everything below it, so replacement produces the
same character a stack would have. Moving the bonuses onto the perks would stack genuinely
-- perks accumulate and cannot be removed -- but **no shipped title perk grants a bonus**,
all 13 of vanilla's are pure text, and the behaviour that would carry them is named
`...WhenSelected` on a perk the player can never select. Faction bonuses are confirmed
working in play; that path is not, so the arithmetic route wins on evidence.

**Confirmed in play.** Standing climbs 1, 2, 3 across three services, and the disease
resistance survives promotion to Champion -- so both halves landed: the escalating grant
that makes the rank equal the tier, and the cumulative totals that stop a promotion taking
something away. This was the longest-lived defect in the project: it made the Crossroads
contract refuse players who had earned it, and I spent three sessions checking gate
thresholds, branch mappings, name resolution and save snapshots before a screenshot of the
in-game log showed the tiers withdrawing each other.

**Vanilla has the identical defect.** Templar Squire, Warden and Paladin all grant `+1
Templar Rank`, so vanilla's own `Rank > 2` gates can never fire. Fixt inherited this by
copying the shipped pattern faithfully -- which is the lesson worth keeping: a pattern
being vanilla's does not make it a working one.

One thing that cannot be fixed the same way: the titles stay in your perk list as you rise,
so a Champion still shows Goblin Chum and Goblin Blooded. There is no remove-perk action in
the engine -- `CGiveCharacterPerkAction` exists and nothing withdraws one -- so the three
read as a record of what you earned rather than a single current rank.

### Esteban's death went unnoticed

The contract paid nothing, the quest never completed, and the Templar initiation never
failed. All three consequences hung on a destroyed script installed by appending an action
to Esteban's generator -- and a generator's `After Action` runs when it *spawns* the
entity. On a character who had already visited the Crossroads it had therefore never run,
and vanilla gives Esteban no destroyed script at all, so there was nothing underneath it.

Two fixes failed before the cause was found, and both were reasoning errors worth keeping:

1. The first put the check on Esteban's interaction in `Crossroads.zax`. Map entity data is
   snapshotted into a save the first time a level is entered, so a map edit can never reach
   an existing character -- a rule already documented in this project and ignored while
   writing the fix.
2. The second moved it into the dialogue, where it *is* re-read at conversation time, but
   asked `CCheckExistenceAction`. **A killed NPC leaves a corpse, and a corpse exists.**
   The test stayed true after death, so the negation never fired -- on a new game either.
   This is also the likeliest reason the destroyed script never fired: killing is not
   destroying.

`CIsAliveAction` is the question that was actually meant, with 349 uses in the shipped
game and the same two fields. The patrol leader now asks it, and dispatches
`Esteban Death Consequences.can`: set `Esteban Dead`, and fail *Investigate the goblin
menace*, *Slay the Giant Wasps* and the Templar initiation's *Seek out Guard Esteban*.
Every part is idempotent -- the flag does not accumulate, the quest actions are
`...IfActive` -- so it is safe alongside the destroyed script, which stays for the
fresh-spawn path.

### The rank titles named the wrong deed

Accumulating standing broke the titles without anyone noticing. Each perk described the one
route that used to grant it, so killing the river dryad awarded a title saying you had
butchered a woodcutter for his eyes. The general shape is worth stating, because it will
recur: **a description that names an event, attached to a state reachable by several
routes, will eventually describe something the player did not do.** All three now describe
the standing. Rank 3's was vanilla's own text and is overridden.

### Six blank replies in the Goblin Girl's tree

An empty reply with no target, no action and no default flag renders as a clickable blank
that does nothing. Only 0.5% of vanilla's 10,915 replies have that shape, so it is a defect
rather than a convention -- the real close idiom is an empty reply *with*
`Is Default Reply=1`, which node 250 in the same tree uses correctly.

Two of the six had working replies beside them and were deleted. The other four were the
only exit from their node, so deleting them would have left the conversation with no way
out; they are now proper closes. This is exactly the class of repair Fixt exists for, and
all six were vanilla's.

### The Goblin Girl did not remember you

Her greeting keys on `Met the Goblin Girl`, written the first time you speak to her, and on
a fresh character it was not taking effect -- so every visit was her first. The write used
the minority option on all three fields vanilla varies for scripting variables:
`permanent=1` where 47 of 50 use 0, `Player#1-9#` where 34 use `$Instigator`,
`accumulation=0` where 31 use 1. Each is individually legal, which is why nothing caught it.
It now matches the dominant pattern.

What settled it was shipping a diagnostic rather than theorising: a reply on her
first-meeting node, visible only when the flag was set, so its presence on a second visit
would separate a failed write from a failed read. That is the habit worth keeping from this
release -- three earlier bugs cost multiple cycles each to inference that a single
measurement would have ended.

## 0.1.0 - "The Horde"

**The thesis.** Lionheart's most developed evil content is the pro-goblin thread, and it
feeds nothing. There is no faction, no rank, no standing, and no side of the war to be on -
and the settlement answers to exactly one skill. 0.1.0 makes the goblins a faction you can
join, gives joining a price, makes the camp notice which side you picked, and gives it more
than Speech to notice you *with*.

**What is already there.** Measured against `data.dat.vanilla.bak`:

- **16 dialogue trees, 282 nodes, 460 replies, 67 of them gated (14.6%).**
- **15 quests** across Barcelona and the Wilderness, near-symmetrically paired - every
  goblin leader already has a serve-them quest and a kill-them quest.
- **Both capstone perks are written and awarded** - `Goblin Champion` and `Goblin Slayer`.
- **Full voice acting for Grumdjum** - 40 `.ogg` files including companion quips, rejoin
  lines and hurt lines.
- **A camp-wide allegiance switch already exists.** `Make Goblins Hostile Relay` is used
  **250+ times across 17 maps** and from 5 dialogue trees and character templates. The
  goblins can already collectively turn on you. What is missing is the other direction.

**What the 67 gates actually read.** This is the problem in one table:

| Gate | Uses |
|---|---|
| Speech (7 thresholds, 15 to 55) | 19 |
| Quest state and relay flags | 38 |
| Faction (`Inquisitor IS`, `Templar IS`, `NOT Templar or Inquisitor`) | 6 |
| Barter (20, 35) | 2 |
| `IN >= 4` | 1 |
| `ST 8+` | 1 |

A whole settlement, and 19 of its 23 skill checks are the same skill. The six faction
checks are `GoblinKhan` asking who you serve - the right question, asked by exactly one
character, with no goblin answer available.

### The four strands

Each strand ships something visible on its own, and they are built in this order.

#### Strand 1 - Fix

The goblin thread's own dead ends. Four true dangling targets (case-only mismatches
excluded - see *Corrections*):

| File | Node | Broken target |
|---|---|---|
| `Resources/Levels/1 Barcelona/Dialog/Gate District/Goblin Sapper.DialogTree` | `20 ate a poet` | `5 goobye` (typo for `5 goodbye`) |
| same | `30 goblin name` | `5 goobye` |
| `Resources/Levels/Wilderness/Dialog/GoblinVillager.DialogTree` | - | `100 avoid dinner` |
| `Resources/Levels/Wilderness/Dialog/Guard Esteban.DialogTree` | - | `5 Goodbye` |

Esteban is in because strand 3 turns him into a target; a contract on a man whose farewell
dead-ends is a poor advertisement.

#### Strand 2 - Restore

`GoblinGirl` (19 nodes, 28 replies) and `GoblinGuards` (4 nodes, 3 replies) ship in the
archive with **zero map references** - written, finished, never placed. They go into
`Goblin Warrens`.

- `Resources/Levels/Wilderness/Dialog/GoblinGirl.DialogTree` - fix `250 Rejection` and
  `290 follow 3`, and the two `no way out` nodes `220 Liver` / `225 Liver pie`, as part of
  placing her rather than afterwards.
- `Resources/Levels/Wilderness/Dialog/GoblinGuards.DialogTree`.
- New character templates under
  `Resources/Levels/Wilderness/Character Templates/`, following
  `Goblin Grumdjum.can` and `Goblin Lieutenant.can`.
- Placement in `Levels/Wilderness Maps/Goblin Warrens.zax`. The
  `marco-the-pickpocket` mod is the proven recipe for placing a new NPC.

Her node IDs already describe the design - `1 First time PC enters village`,
`2 PC Enters the village again, before completing any quest`, `5 Give me some sugar` ->
*"you'll have to prove yourself"*. That last one wants a rank gate, which strand 3
provides, so she is built before it and wired after.

#### Strand 3 - Enhance: the Horde as a faction

**3a. The faction records.** Three files on the `Saladin Aswaran` pattern, each granting
concrete benefits and incrementing its own rank counter:

- `Resources/Factions/Goblin Chum.Faction` - the vendor's own word for a friend
- `Resources/Factions/Goblin Blooded.Faction`
- `Resources/Factions/Goblin Champion.Faction` - the perk of that name already exists and
  is already awarded; the faction record is the rank behind it
- `Resources/Derived Character Attributes/Uber Perks/Goblin Rank.DerivedCharacterAttribute`

Benefits should be goblin-flavoured rather than a copy of Saladin's melee package: Sneak,
poison resistance, carry weight. Each record grants `+1` to `Goblin Rank` with
`Allow Accumulation=1`, and each tier's benefits are written as **increments on top of the
last, not as tier totals** - see *Ranks accumulate* below.

**3b. The gates.** `Resources/Dialog/Requirements/Monster Races/Goblin IS.can` already
exists and tests the player's *race*. Do not reuse it. New files under
`Resources/Dialog/Requirements/Factions/`:

- `Goblin Horde IS.can`, `Goblin Horde Rank 2+.can`, `Goblin Horde Rank 3.can`
- `NOT Goblin Horde.can`

**3c. The way in.** Hrubjub, the goblin scaling the Barcelona wall, is the entrance and
almost nobody finds it - the whole path hangs off one reply behind a question about a
corpse. Two changes to `Goblin Sapper.DialogTree`:

- a second entry on `1 Start Conversation` or `60 used speech`, so the option survives a
  player who did not ask about the body;
- an onward pointer on `100 completed quest` naming the Warrens and the Khan. He is a spy
  with every reason to tell a useful human where to report, and without it rung one of the
  ladder leads nowhere.

Completing `Spy for Hrubjub the Goblin` assigns rank 1.

**3d. The price.** The Crossroads goblin patrol gets to make the opposite offer to
Esteban's. `Goblin Patrol Leader` already has a node that reacts to having taken Esteban's
contract (`500 goblin confrontation`); it gets a rank-gated variant offering the
counter-contract instead of a fight. New quest, one gated node variant, and rank 2.

This is the strand's centre of gravity, because it is the first goblin choice with a
visible cost: `LordJavier` checks completion of Esteban's tasks three times, so killing
him closes a Knights Templar rung. Esteban is already written as someone you can fall out
with - `Crossroads.zax` holds `piss off esteban`, `Esteban Sends you to jail` and
`Esteban mad cam` - so this does not fight his characterisation.

**3e. The exclusivity.** Torquemada's `Slay the Goblin Khan` and the Khan's own contracts
currently do not notice each other - checking every `CSetQuestSatusToFailed*` against the
goblin quests finds **zero links**, in a game that uses the action 239 times elsewhere.
Wiring the mutual failure is the smallest change here and the one that turns a checklist
into a choice.

**3f. The reactivity pass.** Rank-gated variants across the trees that already exist. The
skill and attribute dimension is strand 4; this is standing only.

| Tree | What it gains from rank |
|---|---|
| `GoblinEntranceGuard` (10/19) | Recognition at the gate. The first place standing should be legible |
| `GoblinVillager` (55/31) | The camp's ambient voice, gated on rank rather than Speech alone |
| `GoblinKhan` (41/77) | Already asks `Templar IS` / `Inquisitor IS`. Add the goblin answer |
| `Rakeb` (30/63) | Whether the shaman treats you as a client or a rival |
| `GoblinVendorHub` (3/4) | Chum prices for a chum |
| `GoblinGirl` | `5 Give me some sugar` -> the "prove yourself" gate she was written for |

**3g. Karma.** Harvesting a man's eyes and liver for a goblin shaman currently moves
nothing, while killing the Barmaid does. One modifier per choice, and karma is a live
system that feeds the ending selector directly.

#### Strand 4 - Check

The camp answers to one skill. Nineteen of its twenty-three skill and attribute gates are
Speech; the other four are two Barter, one `IN >= 4` and one `ST 8+`. Strand 4 is the
build-reads-the-world half of the release, and it is deliberately a peer of the faction
work rather than a garnish on it.

**Most of it costs no new `.can` files.** The gates already exist in the archive and are
referenced by nothing at all:

| Ready-made gate files | Count | Uses in the shipped game |
|---|---|---|
| `Lockpick moreequal 10` .. `95` | 18 | **0** |
| `Schmooze 4..10 greater or equal` | 7 | **0** |
| `Outwit 5..10 greater or equal` | 6 | **0** |
| `AG 1-3`, `4-6`, `7+`, `8+`, `10+` | 5 | **0** |
| `EN` (same five) | 5 | **0** |
| `LK` (same five) | 5 | **0** |
| `Sneak moreequal 10..35` | 5 | 3 |

**46 finished requirement files that nothing in Lionheart reads.** Agility, Endurance and
Luck have never gated a line of dialogue in the shipped game. 0.1.0 can be the release
where they get their first.

**`Outwit` and `Schmooze` are the developers' own names for this idea.** Both are
pass-through derived attributes - `Outwit` is `(IN) Intelligence` unmodified, the file
behind the `Schmooze` gates is `(CH) Charisma` unmodified - built so a writer could say
"outwit him" instead of "IN 7+". They wrote the gate files and then never used one.

And the fossil is in the goblin thread itself:
`Grumdjun Dryad talked to NOT killed Player high Outwit.can` **does not test Outwit.** It
tests `Speech >= 20`. Somebody meant to gate Grumdjum's dryad branch on intelligence,
named the file for it, and shipped Speech. Strand 4 finishes that thought.

**Where the checks go.** Each of these is an existing scene that currently reads nothing
or reads only Speech:

| Where | Check | What it does |
|---|---|---|
| `Crazy Goblin Trapped Conquistador` (18/25, **0 gates**) | `ST 8+`, Lockpick, `Outwit` | He is pinned. Force it, pick it, or work out the mechanism - three ways into a scene that presently has one |
| `Goblin guarding Woodcutter daughter` (14/11, 1 gate) | `Schmooze` / `CH`, `PE` | Talk the guard off her, or notice she is not the only one being held |
| `GoblinVendorHub` / Hub'blub (3/4, **0 gates**) | Barter | A merchant with no Barter check, in a game with 51 Barter gate files. Built as a second `CMerchantAI` entity at a lower `Price Multiplier`, the way `Lope Inventory low`/`high` already works |
| `Rakeb` (30/63) | `Tribal` | The camp's real shaman, and the Tribal tree gates exactly one conversation in the whole game |
| `Goblin Sapper` / Hrubjub | `PE` | Spot what he is actually doing at the wall before asking about the corpse - a second, observation-based way into the entire Horde path |
| `GoblinKhan`, poetry | `Outwit` / `Schmooze` | `XP for flattering Khan` and `Khan told poetry to once` already exist. Rhyming at a goblin king is a Charisma check that writes itself |
| `GoblinGrumdjum`, dryad branch | `Outwit` | Replace the mis-named Speech gate with the check its filename promises |
| `GoblinEntranceGuard` (Speech 40/55) | `Sneak`, `AG` | A second way past the gate for a build that does not talk |
| Slave Pit hut - `trap poly on trapped chest1`, `fire pain radius` | Find Traps, `PE` | Placed trap content with no detection check in front of it |
| `Khan Chest` (`Lock Pick Adjustment=40`) | `LK` | Luck's first use in the game: whether the one goblin who might have seen you happened to look |

**Why `Outwit` and `Schmooze` rather than `IN 7+` and `CH 7+` wherever both would work.**
They live under `Perk and Trait Support`, which is what that folder is for: a derived
attribute a perk can add to. Nothing in the shipped game writes to either, so today
`Outwit 7+` and `IN 7+` are the same test - but gating on the derived one means a perk can
later grant the *reading* without touching the stat. That is the "if you are intelligent
enough, **or** have the observant perk, you notice Y" shape, and it costs nothing extra now
to leave the socket open. Use the raw attribute only where no perk should ever substitute -
`ST 8+` to lift the beam off the conquistador is strength, not cleverness about strength.

**The rule for every one of them:** a check adds a route, it never removes one. The Speech
path stays exactly as shipped. This is the correction the design already carries - "not
combat" is as boring as "only combat", and "only Speech" is the same failure in a third
costume.

### Explicitly out of 0.1.0

- **A new goblin area.** The back half needs one more than the Wilderness does.
- **The unfinished evil quests** (`FIND THE RELICS FOR THE DARK WIELDERS` and the rest) -
  Dark Wielder content, not Horde content.
- **`Goblin Champion` requires slaying Raylark and Fenclaw, but only Raylark is in the
  quest text.** Real, and a 0.1.x patch, not a 0.1.0 blocker.
- **Rebalancing goblin combat.** Subtracting enemies changes pacing in ways only play
  reveals.

### Verification

Per the standing rule, nothing is announced as testable until the deployed bytes are read
back. For each strand:

1. **Static** - re-run the dangling-target scan over the shipped mod and assert the four
   true breaks are gone and no new ones appeared.
2. **Faction** - assert each new `.Faction` parses on the `Saladin Aswaran` shape and that
   `Goblin Rank` increments once per record.
3. **Deploy** - `modmanager.py install <path-to-this-repo> <game-dir>` then
   `modmanager.py build <game-dir>`, then byte-compare the loose `data\` mirror and the
   `data.dat` entries against the mod source.
4. **In-game, in one pass** - Hrubjub via the new entry, spy quest, rank 1; Crossroads
   patrol offers the contract; Esteban dies; Templar rung visibly closes; the Warrens
   greet a ranked player differently; Goblin Girl is present and her rejection branch
   resolves.
5. **Strand 4 needs two characters, not one.** The checks are invisible to a build that
   passes everything. Run the pass a second time on a low-`IN`, low-`CH`, high-`ST`
   character and confirm the Speech routes still work untouched and the new ones are
   correctly absent. A check that silently replaced a shipped route is the failure mode to
   look for.

## Corrections to `plan.md` found while scoping this

Three claims in the plan document are wrong and are fixed there:

- **The Goblin Shaman is not a mute character.**
  `Resources/Levels/Wilderness/Dialog/Goblin Shaman.DialogTree` ("Goblin Shaman Yumjum",
  3 nodes, 0 replies) is a **taunt bank** attached to generic shaman monsters across 16
  maps via `CDisplayDialogBalloonAction`, not a conversation that was left unfinished.
  Giving it replies would give every generic shaman in the game a conversation. The camp's
  real shaman is **Rakeb** - 30 nodes, 63 replies, 7 gates, placed in `Goblin Warrens`,
  with his own kill-quest and bounty. The Tribal-magic opportunity belongs to him.
- **Robbing the Khan's chest is already noticed.** `Khan Chest` in `Goblin Warrens.zax`
  fires `Make Goblins Hostile Relay`, triggers `Stealing from Khan relay` and cancels
  sneaking; Rakeb's chest does the same. `Lock Pick Adjustment=40` and `30` respectively.
  The gap is not that theft goes unremarked - it is that the consequence is *binary*.
  There is no graded standing to lose, no Khan who hears you were in his tent, only the
  whole camp going hostile at once. That is exactly what a rank fixes.
- **244 "broken" links are case-only mismatches and the engine tolerates them.**
  `GoblinKhan` sends players to `130 the job` when the node is `130 The job`, and Rakeb
  does it six times to `90 goodbye`. These are traversed constantly in normal play. The
  84-count in the plan already excludes them; recording the evidence so nobody re-counts
  them as work.

## Answered - how factions and merchants actually work

The three questions that were blocking strands 3 and 4 are resolved against
`data.dat.vanilla.bak`.

### Faction assignment works from a dialogue reply

`CAssignFactionToCharacterAction` has **29 uses: 20 in maps, 9 in four dialogue trees**.
Joining from a conversation is the shipped pattern, not the exception. `CedricAlsen`,
`Lord Relican`, `InquisitorRaphael` and `LordJavier` all recruit the player mid-sentence.
The exact shape, from Cedric:

```
Reply Text=Yes, I will join the Wielders.
Go to node ID=110 fashion
Custom Action=CMultipleActionsAction
  Action=CAssignFactionToCharacterAction
    Faction To Assign=Factions/Wielder Conjurer
    Character To assign=$Instigator
  Action=CActionRemoveInventoryItem ...
  Action=CGiveExperiencePointsToAllPlayersAction ...
```

Note the field names: `Faction To Assign` and `Character To assign` - the second has a
lower-case `a`, and the engine will not forgive a corrected spelling. Strand 3c is
unblocked and copies this verbatim.

### Ranks accumulate, and tier benefits stack

All twelve shipped records grant `+1` to their own rank counter with
`Allow Accumulation=1` and `Modification is permanent=1`, and the `Highlevel` gates test
`Rank > 2`. So rank climbs 1 -> 2 -> 3 across three assignments and **the tiers' benefits
add up** - a rank-3 Templar is carrying Squire's `+4` melee, Warden's `+8` and Paladin's
`+12` at once, for `+24`. The three goblin records must therefore be written as
**increments, not tier totals**.

### A faction cannot be lost - so the price has to be a quest, not a demotion

- Zero assignments to the null faction anywhere in the game.
- Zero negative writes to any rank attribute.
- `CAssignFactionToCharacterAction` is the **only** faction-related action class in the
  entire archive. There is no leave, clear, expel or demote action.

`Resources/Factions/!None.Faction` does exist, but it is an empty record - no plug-in
behaviors, blank display name. Assigning it would clear the *title* and nothing else: the
benefits are stamped `Modification is permanent=1`, and rank is a permanently modified
derived attribute rather than a property of the faction you currently hold, so neither
comes back off.

A negative record *is* expressible - `CCharacterModifierDerivedAttribute` takes any
`Constant Value`, including `-1` - but nothing ships one, so it is unproven.

**This settles strand 3e.** The Horde cannot be quit and the Templars cannot demote you,
so the price of joining has to be paid in **closed content**: Esteban dead, his tasks
unavailable, `LordJavier`'s three checks failing, and the mutual quest-failure wiring. That
was the plan already; it is now the plan because it is the only mechanism that exists.

### Merchants are map entities, and swapping them is a shipped pattern

`Hubglubs Store` is not a resource file. It is a `CEntityBase` inside
`Levels/Wilderness Maps/Goblin Vendor Interior.zax` carrying a `CMerchantAI` activity -
`Display Name=Goblin Vendor`, `Price Multiplier=1`, `Time Between Restock=900`, and a
13-entry stock array. There are **59 such entities** across the game and
`Price Multiplier` is hand-tuned from `0.75` to `2.0`.

Better still, the swap pattern already ships: `Lope Inventory low` / `Lope Inventory high`,
and `Vendor 2 Inventory low` / `high` / `especial`. `CDisplayMerchantWindowAction` names
its merchant entity, so a gated reply can open a *different* store.

**Strand 4's Barter work is therefore concrete**: add a second `CMerchantAI` entity to
`Goblin Vendor Interior.zax` at a lower `Price Multiplier` with friendlier stock, and point
a Barter- or rank-gated reply in `GoblinVendorHub` at it. Chum prices for a chum, built the
way the developers built Lope. `Inventory for Shaman` in `Goblin Warrens.zax` is the same
opportunity for Rakeb.

## Open questions still blocking parts of 0.1.0

- **Can a perk write to `Outwit` or `Charm`?** The folder name says yes and nothing in the
  shipped game does it, so it is untested. If it works, the perk-substitutes-for-stat
  pattern is available to every later release; if it does not, strand 4's gates still work
  as plain `IN`/`CH` checks and nothing is lost.
- **Does `Lock Pick Adjustment` on a chest have any dialogue-visible outcome?** Strand 4
  wants an NPC to react to a picked lock. Whether a `.can` can ask "was this opened by
  force, by key, or by skill" is unknown, and the `LK` check on `Khan Chest` depends on it.
