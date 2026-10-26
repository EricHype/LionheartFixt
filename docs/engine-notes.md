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
- [Skills, spells and the skill window](#skills-spells-and-the-skill-window)
- [Wands](#wands)
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

**A conversation must silence the speaker's balloon loop first.** The engine plays one voice line at
a time, so a repeating `CDisplayDialogBalloonAction` keyed to an NPC cuts off any conversation that NPC
is given. Vanilla's answer is a `CDeactivateAction` on the balloon host, fired immediately before the
`CDisplayDialogTreeAction`, and it uses it at **both** of its own DaVinci conversations in the Gate
District. 0.58.1's gift scene was the third and the only one that did not, so his idle commentary talked
over 25 seconds of recorded line. Counted across every shipped map, **65** balloon hosts can fire more
than once and all 65 are vanilla's -- this project has added none, which is why the gift was the only
case. The deactivation is permanent in vanilla too: nothing ever re-activates `davinci banter relay`.

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

**An inactive generator is a template, and the clone is what spawns.** `Grand Inquisitor generator`
in `Inquisition Chambers2.zax` is `Active=0` and no `CActivateAction` anywhere in the game names it,
which reads as dead content and is not. A relay called `RESET MAP for Invulnerable Grand Inquisitor`
clones the part onto its own position, the clone generates the character, and the clone is then
deleted. Every arrival point in the map fires that relay, `Jail Start` included, so the character is
rebuilt fresh on each entry and is always non-hostile and always present. **134** `CCloneAction`s in
the shipped game clone a part onto itself this way, across the 9 maps that carry a `RESET MAP` relay
-- `Church Interior`, both Inquisition maps, `Calle Perdida`, `Knights Templar`,
`DaVinci Workshop interior`, `Blacksmith map`, `Crossroads` and `06 Witch Interior`. Lord Javier
reaches the Cathedral the same way.

So **`Active=0` with no activator is not evidence that a generator never fires**: look for
`Source Name=` and `New Location=` before concluding anything about who is in a room.
`tools/deadparts.py` already counts a clone as naming a part, which is why it has never reported
these. This one was caught one query short of being written up as "the Grand Inquisitor cannot be
met in his own chambers".

**`$Instigator` means different things in different places.** In a generator's `After Action` it is
the entity just spawned. In a dialogue reply it is the **player**. In a relay fired from a reply it
resolves to nothing at all, and so does `$trigger` -- use a literal entity name there, as about
ninety vanilla `CDisplayDialogTreeAction`s do.

---

## Skills, spells and the skill window

**A branch needs a real `Maximum Value` or its spells are not drawn at all.** Of 92 vanilla skills, `Maximum Value` is 300 eighty times, 5700 eleven times and 100 once, and `Amount To Increase Value By With Each Upgrade` is 1 eighty-six times; **neither field is ever 0**. A branch built with a maximum of 0, to make it unspendable, renders itself and nothing under it. All 21 vanilla branches are `Normal` at `-300/300` with upgrade 1. A negative spell value is no obstacle: a branch reading 1 still draws its spells at -23, -48 and -88.

**`Value Differential` is the row a spell is drawn in, not only a gate.** Every spell in a vanilla
branch carries `Sort Priority=0` and a differential from one ladder -- **0, 24, 49, 74, 89, 109** --
and within a branch those values are always distinct. Protective is Aid 0, Physical Aura 24, Holy Fire
49, Mana Shield 89; Fortitude is Healing 0, Purify Body 24, Resist Elements 49, Divine Assistance 74,
Greater Resistance 109. Give two spells in one branch the same differential and they take the same
slot; give them a value off the ladder and the window draws nothing at all. `Sort Priority` does no
work.

**The skill tree is entirely data-driven, and `Skills/!None` is its root.** `!None` is its own parent;
the five categories carry `Parent Skill=Skills/!None` with `Sort Priority` 1, 2, 10, 11, 12; and no
resource anywhere enumerates them, so a new category is just a skill parented to `!None`. Nothing
reads `!None`'s own value: its ~800 references are `Selected Skill`, `Skill To Select When Shoot
Sequence Ends` and six `Parent Skill`, so its `Sum of childrens values` is consumed by nothing.

**The tree is strictly category, branch, spell.** Every root child is a non-spell `Normal` point skill
carrying four or five spells, and **no root anywhere has a castable spell as a direct child**. A path
like `Skills/Magic Divine/Defensive/Healing` is decorative: that spell's parent is
`Skills/Magic Divine/Fortitude`. Only `Parent Skill` builds the tree.

**The window shows the stored value; a cast evaluates the derived one.** A character whose save held
450 for a spell at `Value Differential=300` under a branch reading 1 saw 450 on the screen and was
refused with `Skill has 0 value`, because the cast used `parent - differential`.

**A branch's `Maximum Value` bounds the stored value, not the total.** Every branch bonus in the game
is `Allow Accumulation=1` and adds on top: `Divine Protective` +15, `Torquemada Divine Boon` +7,
`Domination` +15, `Tribal Protective` +15, The Mage +4, and the `of the Mage` armour line +1 a piece.
A branch capped at 300 can reach about 334, so `parent - 300` is not a safe way to hold a derived skill
at or below zero. A parent pinned with `Minimum Value` and `Maximum Value` both 0 is, because nothing
can modify what nothing references.

**`Initial Value=` empty is not zero**, and eleven vanilla skills have it: the six category roots and
the five `Fake Wand Spells`. Whatever it produced was frozen into the eight
`Preexisting Characters/*.Character.txt` files as **450**, eleven entries each, and a character made
from one carries it forever. No change to a `.Skill` can reach a value a character file already bakes.

**`CInventoryAdditionsNamedExpressionExpression` reads nothing when no addition is bound.** It broke
three separate things in one release: a `skilllevel` pin cached garbage through `CCacheFirstResult`,
fifteen spell effect numbers came back zero so a healing wand healed nothing, and a wand's
`Maximum Charges` read zero so the wand was spent before its first cast. Put a spell's numbers in its
own `Expressions` array and read them with `CSkillsNamedExpressionExpression`: the split across 92
vanilla skills is **52 files using the skill's own against 3 using the addition's**, and all three are
wand spells that never ran.

---

## Wands

Every wand in the game is `Inventory Items/Wand` plus an addition carrying
`CPlugInBehaviorWand`. A night of testing established the following, and the table at the end is
what was actually tried, in order, so none of it needs repeating.

**Vanilla never drops a wand.** `All Wands.can` has zero referrers, so no chest, monster or
merchant ever rolls one, and wands appear only in two test maps. Fixt reaches them by wiring
`All Wands` into `All Misc Items except Potions`.

**A wand plugin is initialised only for an addition drawn through the item's addition group.** An
addition named directly in a can is attached but left uninitialised, so `CPlugInBehaviorWand`
believes it has no charges and disables its spell: in group it cast 3 times out of 3, out of group
0 out of 2. Group membership is also what lets the generator stack a second addition onto the item,
so a wand cannot have both a working plugin and a guaranteed single spell. The way out is to drop
the plugin: a pin makes the spell castable, a separate charge item limits it, and a `CIfAction` in
the payload refuses an empty one.

**A wand only works if the item generator made it.** `CActionGiveStandardInventoryItem` gives the item and its addition, but the wand comes out with no usable charges and the first cast fails `Skill Is Disabled`. Of its 374 vanilla uses the 60 that pass an `Addition to add` are potions, arrows, cloaks and flat damage bonuses, none with a stateful plugin. Wands reach a player through `CGenerateInventoryItemAction` (2035 uses), which runs a `Wand <name>.can` generator and drops the item on the ground; through that route the same wand casts normally. All 15 vanilla wands also carry `Charges Remaining Is Valid=0` and `Charges Remaining=0`, leaving the plugin to work the count out itself.

**A wand's charge count does not persist, so it cannot count down.** `Charges Remaining` is read
back from the addition definition rather than kept on the item: pre-load it with
`Charges Remaining Is Valid=1` and the wand casts for ever, leave it at vanilla's 0 and the spell is
disabled before the first cast. Nothing in between is reachable. All 15 vanilla wands carry 0, and
`All Wands.can` has no referrers, so no shipped chest, monster or merchant ever rolls one.

**A stacked item keeps no per-item plugin state.** Adding
`CInventoryItemPlugInBehaviorMergeMultipleInstances` to a wand turns it into a stack, and the wand
plugin then reports no charges however the count is set, because stacked items are fungible.
`MultipleInstances/Current Count` itself is live and persistent, which is how arrows and potions
work, and `Infinite.InventoryAddition` shows an addition can set it; it just cannot share an item
with a wand.

**Only the first wand addition on an item works, and nothing in vanilla stops a second.** The generator stacks additions from a group while the budget lasts, so a wand can arrive as `Wand of Lockpicking, Revelation and Lesser Healing, Spikes`, or with the same addition twice, and casting any spell but the first fails. `Additions Cannot Be Combined With` is the field for it, used by 22 of 286 additions and always pairwise, and it is `Item Count=0` on all 15 vanilla wands.

**An item in no addition group cannot be given an addition.** All 109 of vanilla's specific item
cans carry `Inventory Addition Group=Inventory/!None`, which is what makes a named weapon carry
exactly the properties its author gave it, and it is the only reliable way to stop the generator
adding magic. `Additions Cannot Be Combined With` is honoured somewhere, the engine logging
*"but could not because it is not allowed to be combined with"*, but not for a can's guaranteed
addition, and all 22 vanilla uses of it are armour, amulets and bracers. A complete item also has
no `Expressions` array, so a `%i[]` token in its description resolves to nothing and the numbers
have to be written out.

**`Origonal Item` is stamped by the engine, not read from the file.** An item created from
`Specific Item Cans/Misc Items/Wand of Revelation` carries that path in the save whatever its file
says, so `CActionRemoveInventoryItem` has to name the path an item was actually created from.

**`Display and Cast Requirements` cannot ask about a character.** All 6 vanilla users hold a
constant comparison, `CIsEqualTo{0, 1}`. An inventory check placed there evaluates false, because
nothing binds `$Instigator` in the skill window, and the spell stops casting altogether. Conditions
that need a character belong in the spell's payload, where `CIfAction{If=CActionCheckForInventoryItem}`
is vanilla's own shape.

**A spell cast is neither a strike nor a launch.** `CPlugInBehaviorUseAmmo` on a wand never fires,
whichever of its four thresholds is set, so an item plugin cannot meter a spell. What can is the
spell's own payload: `CActionRemoveInventoryItem` inside a `CPlugInBehaviorLaunchAction` runs on
every cast and takes **one unit off a stack**, which is how a charge item gets spent.

**What was tried, and what each attempt proved.**

| attempt | result |
|---|---|
| `CActionGiveStandardInventoryItem`, charges read through the addition's named expression | no charges |
| the same, with `Maximum Charges=CConstant 15` | no charges, so the route is the problem, not the expression |
| `CInventoryItemGeneratorMiscellaneousMagic`, `Charges Remaining Is Valid=1` | **17 casts, never depleted** |
| the same with `Is Valid=0`, vanilla's value | disabled before the first cast |
| two different additions on one item | only the first spell casts |
| the same addition twice | neither casts |
| `Additions Cannot Be Combined With` across all 18 | did not bind; the generator stacked anyway |
| item level tuned so the budget cannot afford a second addition | undercut anyway |
| the 18 additions taken out of `Wand Additions` | **stacking solved**, one wand spell per wand |
| the whole wand rebuilt as a complete `.InventoryItem` | no charges, and `Origonal Item` is overwritten |
| `MergeMultipleInstances` plus `UseAmmo` on the Weapon slot | the count moved, 20 to 19, but a stack cannot hold a wand plugin |
| `UseAmmo` on the wand, charges in a separate stack | the spell casts and the effect lands, but the count never moves |
| `CActionRemoveInventoryItem` inside the spell's payload | **the route that can meter a cast** |
| the same, gated by `Display and Cast Requirements` on an inventory check | the spell stopped casting at all; that field cannot see a character |
| the charge check moved into the payload as a `CIfAction` | **the working system: a charge spent per cast, an empty wand does nothing** |

A wand's limit therefore lives outside the wand: a stackable charge item, removed by the
spell's own payload, with `Display and Cast Requirements` refusing the cast when none is held.

The working configuration is therefore: addition in the `Wand Additions` group, generated by a
`Wand <name>.can`, `Charges Remaining Is Valid=1` with a pre-loaded count. It casts reliably and
**without limit**, because nothing decrements.
---

## Method rules

**Reverting a whole configuration hides which part mattered.** Chasing a build that had worked, this
release restored every difference at once and put a solved defect back, then spent another round
rediscovering it. Revert the change that is implicated, not the ones that merely changed alongside it.

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
