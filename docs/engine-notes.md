# Engine notes - what the game actually does, and what this project keeps getting wrong about it

Facts about the engine that cost a release to learn, and the method rules that came out of the same
mistakes. This exists so the next release does not re-derive them, and so a claim here can be
**checked** rather than trusted: every number below is counted against `data.dat.vanilla.bak`.

Most of these were paid for in public. The right-hand column of the last table names the release
that found each one, and several of those releases exist only because the one before them was
wrong.

---

## Contents

- [How content is reached](#how-content-is-reached)
- [The save, and what reaches it](#the-save-and-what-reaches-it)
- [Shapes that crash](#shapes-that-crash)
- [Characters and their behaviour](#characters-and-their-behaviour)
- [Method rules](#method-rules)
- [What each lesson cost](#what-each-lesson-cost)

---

## How content is reached

**A node's shape tells you how it was meant to be delivered.** Three signatures, and reading them
correctly is the difference between restoring a scene and inventing one:

| the node has | it is | fire it with |
|---|---|---|
| replies | a conversation | `CDisplayDialogTreeAction`, from a map or a specifier |
| no replies at all | a balloon | `CDisplayDialogBalloonAction` |
| blank reply text, no target node, `CSendAIDoneMessage` | a **cutscene** a map was supposed to show | a relay, after whatever beat it belongs to |

So "this node has no replies" is not evidence that anything is unfinished: `1100 Found Mana` has
none either and is fired, as a balloon, from `First Mana Pickup Spirit Call.can`. And
`500 davinci gives a gift to help you get started male` had the cutscene signature, which named its
host before any map was searched.

**"No reply points at this node" is not "unused".** A map or a can can open a node directly, and 325
vanilla balloon firings land on recorded nodes (counted for 0.56.0). Grep the `.zax` files for the `(tree, node)` pair
before calling anything orphaned.

**A tree's own root can name the trigger that was never built.** `DaVinciBarcelona`'s
`Default Canceled Node Action` activates `detect player for davinci gift` -- an entity that exists
in **no map in the game**. A name that only a dialogue tree mentions is cut wiring, and nothing in
the project's gates crosses that boundary.

**Node references resolve under three different rules.** A map or can naming a node matches it
**byte for byte**, and a mismatch is a hard crash on map entry -- `800 general attack ` ships with
a trailing space. A reply's `Go to node ID=` is trimmed and case-folded. Voiceover resolves as
`<TreeName> VOs/<Node ID>.ogg`, trimmed.

**A reply added inside a cutscene inherits that cutscene's duty to end it.** The Montserrat
send-off runs inside `CBeginNonInteractiveSequenceAction` with `Disable Player Controls=1`, and
exactly one reply in Lord Javier's tree fires the relay that ends it. 0.9.0 added a fourth option
that reached a node whose own exit did not, and the result was a soft lock that shipped for a year.
Before adding a reply, ask what opened the node it sits on.

**Experience from a dialogue tree needs a named marker entity in the current map.**
`CGiveExperiencePointsToAllPlayersAction` takes `Get XP Frome=<marker>` plus `Experience Points To
Add=1`; the marker carries the real amount. Of 430 awards in trees, **0** use `$Trigger` with a
literal, and `$Trigger` resolves only inside cans. A save that predates the marker can never be
paid, because a room's entity list is frozen on first visit.

**Item counts are expressible, by repetition.** `CActionCheckForInventoryItem` has no count field in
any of its **653** uses across vanilla's `.can`, `.zax` and `.dialogtree` files; N checks AND'd with N removes really does require N, confirmed in play with
Quinn's wasp stingers.

---

## The save, and what reaches it

**A map's entity list is written into the save the first time the player enters, and restored from
there forever after.** Dialogue is not: it is read fresh at conversation time.

That asymmetry decides where a fix can live:

| the fix is | reaches an existing save | notes |
|---|---|---|
| a new level part | **no** | the player needs a character that has not entered that map |
| an edit to an existing part | **no** | same snapshot |
| a character template (`.can`) | **no** | read when the entity is created |
| anything in a dialogue tree | **yes** | including actions on a reply that name existing entities |

So a repair that must reach a live save has to be expressed as actions on a reply, naming entities
that already exist. Three releases this run used that route: DaVinci re-activated from his own
dialogue, and the Crossroads horse pacified, voiced and de-fanged through Alvaro's shop replies.

**Reading a save.** A `.sav` is brace-grammar text, but every visited map sits in a
`Current Temp File=TempFile` block as `Length=N bytes`, a `#### BEGIN TEMPORARY FILE ####` marker,
three little-endian uint32s and then a **zlib stream**. Decompressed, each blob is `.zax`-shaped. A
plain search of the file finds none of it: searching a quicksave for "Fernand" and "sailor" returned
zero while both sat in the Port District blob.

---

## Shapes that crash

Four ways to produce a file that loads in every tool here and kills the engine. All four are now
checked by `tools/validate.py`.

| shape | what happens | checked by |
|---|---|---|
| a class value led by whitespace (`Then=<tabs>CClass`) | map refuses to load | `WS_CLASS` in `check_resource` |
| a map or can naming a node that does not match byte for byte | hard crash on map entry | `check_map_node_refs` |
| an `Array` whose `Item Count` disagrees with its contents | silent truncation | `check_array_counts` |
| **a field with an empty value followed by a `{` block** | *"Found unexpected '{' while parsing class ..."* on load | **A0.17**, `ORPHAN_BLOCK` |

The last one shipped in 0.60.5 and crashed the Crossroads. It came from blanking a class name and
leaving the block that class owned: `Attack AI=` and then a brace. A vanilla empty field, as in
`Barcelona Boy.can`, is `Attack AI=` followed straight by the next field.

**Why it got through, which is the part worth keeping.** `resource_format` attaches an orphan block
to the preceding key as an unnamed object and **round-trips the file byte for byte**, so it passed
"canonical engine formatting", `validate.py` was green, the delta build verified every file
reconstructs, and the release zip was checked four ways. A round-trip proves the parser agrees with
itself. It proves nothing about the engine.

---

## Characters and their behaviour

**`CSkeletonAI` is a bundle, not a behaviour.** It holds the patrol, the targeting, the pursuit and
the attack in one activity, and **`Valid Targets` lives inside it**, nested in the
`Target Type=CEntityBehaviorStateSetClosestTarget` block beside `Max Distance=550` and
`Vision Cone=360`. Swapping the bundle therefore moves four things when you mean to move one: in
0.60.5 a fresh copy handed a pacified horse its targeting back, and it spent 0.60.6 following people
around with no attack to finish with.

Edit the fields instead:

| to | set | vanilla uses |
|---|---|---|
| stop it fighting, keep it moving | `Attack AI=` empty | 47, e.g. `Barcelona Boy.can` |
| stop it seeing anyone | `Valid Targets=` empty | 972 |
| stop it being a target for companions | `CRemoveCategoryAction{Categories To Remove=Enemy}` | shipped in two maps |
| stop it behaving at all | `CRemoveAIAction{AI=CSkeletonAI}` | 35 |

**An animal with no interaction specifier is just a target**, because the default click on a
creature is an attack. Beatrice's chickens are the shipped answer: a `GetCloseThenTrigger` specifier
over a `CRandomAction` of balloons. Having a specifier is what takes the click away from the swing.

**Check a creature's can before placing it.** `Monster Cans/Animals/Horse.can` is built on
`Races/Enemies/Animals/Wolf Gray` with `Valid Targets=Player,Player Friend`, `Category=Animal,Enemy`
and `Attack AI=CNormalAttackAI`, and the horse model ships `Idle`, `Walk`, `Death` and nothing else.
Placed as it stands it charges the player and then asks for an attack animation that does not exist,
which drops the engine back to another model. An unused creature is usually unused for a reason
visible in those four fields.

**The name the combat log prints is `User Assigned Name` on the can.** `Display Name` is `unnamed`
on every character in the game. Jafar's can says `Amir`, Joan's says `Jehanne d'Arc`, Cortez's says
`Cortes`. Fernand's said `Sailor` for nine releases after he was given a race, a tree and an
introduction, because none of those is the field the engine reads. There is no shipped way to rename
an NPC in play: all six vanilla uses of `CSetCharacterDisplayNameAction` target `$instigator`.

**Deactivated is not deleted.** `CDeactivateAction` parks a spawned character; it can be activated
again, faded back to opacity 1 and handed a fresh specifier with `CAddAIAction`. Vanilla does
exactly this to the Mayor in `01 Hamlet Exterior.zax`. Before writing a later scene for a character,
check whether something tears them down first -- DaVinci's chamber copy is removed for good by the
Goodbye reply of the conversation that hands out his quest.

**`$Instigator` means different things in different places.** In a generator's `After Action` it is
the entity just spawned. In a dialogue reply it is the **player**. In a relay fired from a reply it
resolves to nothing at all, and so does `$trigger` -- use a literal entity name there, as about
ninety vanilla `CDisplayDialogTreeAction`s do.

---

## Method rules

**No vanilla precedent means the form is wrong.** Checked three times this run, each time after
shipping the unprecedented version: `$Trigger` plus a literal for experience (0 of 430 tree awards),
a reply firing `CDisplayDialogTreeAction` directly (0 uses; relays have 661), and an attack removed
by deleting a class name (the engine wanted the block gone too). Count the shipped uses of the exact
shape before building on it, and prefer a 35-use action to a 1-use flag from a test map.

**Measure against the right baseline.** For a file this mod already ships, the comparison is `HEAD`,
not vanilla: `Crossroads Vendor.dialogtree` differs from vanilla by Fixt's own earlier work, and
asserting against vanilla fails for the wrong reason.

**Count what the format counts.** A `.DialogTree` is flat, so an action's `Node ID=` starts at
column 0 exactly like a node header: count the dashed separators instead. `AIs to Add=Array` matches
inside `Canned AIs to Add=Array`: anchor on the line start. `After Action=` appears on every
balloon: match the one whose value is a class. A block cut with `balanced()` ends **on** its closing
brace and carries no line ending: splice an explicit CRLF after it.

**Read a restored line beside four of the character's shipped ones.** Nothing in the gates reads for
voice, so a paragraph in the wrong register passes everything. Vanilla's DaVinci is short, warm and
exclamatory -- *"There! It is complete."*, *"Bravisimo!"*, *"Grazie!"* -- and three sentences is a
long speech for him; three reactions written for him ran to eight and had to be cut by half in
0.57.10.

**Fix both halves when the save matters.** The generator or template for every future spawn, and a
dialogue route for the character who already has the broken version.

**Play finds what static checks cannot.** This run shipped six defects that every gate passed, three
of them ours: a soft lock from 0.9.0, a horse built on a wolf, and a crash. Each was reported in one
sentence by someone playing, and each took under an hour to find once reported.

---

## What each lesson cost

| lesson | found by | release |
|---|---|---|
| Experience needs a named marker in the map | the award paid nobody | 0.57.4 -> 0.57.5 |
| A proximity conversation can hold a destructive reply | one dismissive click lost the quest item | 0.57.6 |
| The quest ends where the machine is, not where the man is | "it feels like a pretty simple quest" | 0.57.7 |
| Deactivated is not deleted | "he leaves and I don't think he ever returns" | 0.57.9 |
| Nothing reads for voice | "aren't right tonally for leonardo and it's too long" | 0.57.10 |
| A tree's root can name a trigger nobody built | the gift fired over its own goodbye | 0.58.1 |
| A reply-less node is a balloon | the undead warning had no replies and three recordings | 0.59.0 |
| `.dialogtree` can be lowercase | a `*.DialogTree` search said the tree did not exist | 0.60.0 |
| A new reply inherits the cutscene's exit | issue #7, a soft lock from 0.9.0 | 0.60.1 |
| An unused creature is unused for a reason | "it seems to be hostile ... granny model" | 0.60.2 |
| `User Assigned Name` is what the log prints | "still called sailor in the log" | 0.60.3 |
| A creature needs a specifier or the click is a swing | "the default interaction is to fight it" | 0.60.4 |
| Blank the field, do not remove the activity | "I'd prefer the wandering without the fighting" | 0.60.5 |
| An orphan block crashes the engine and passes every gate | a screenshot of the crash | 0.60.6 |
| `CSkeletonAI` is a bundle, and `Valid Targets` is inside it | "it sees and follows me around the map" | 0.60.7 |
