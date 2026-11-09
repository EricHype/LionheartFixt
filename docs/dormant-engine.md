# Dormant engine features

The engine registers 297 action and AI classes, and vanilla's data never uses 105 of them. Some of these work.
Some are empty placeholders, and naming one in data can crash the game. This page records which is which, how to
use the working ones from data, and how to check a class nobody has read yet. Everything here was read in Ghidra
from `Lionheart.exe`. Unless a row says otherwise, **none of it has been seen working in play**, because vanilla
never runs it.

Read this before building enemy behaviour. [`engine-notes.md`](engine-notes.md) still holds the general facts; this
page is the reference for classes the shipped game leaves unused.

## Contents

- [Read this first: classes that crash](#read-this-first-classes-that-crash)
- [Verified](#verified)
  - [CCallForReinforcementsAction: a working call for help](#ccallforreinforcementsaction-a-working-call-for-help)
  - [The CSkeletonAI retreat: cut, does nothing](#the-cskeletonai-retreat-cut-does-nothing)
  - [CStandStillAttackAI: a turret while in range](#cstandstillattackai-a-turret-while-in-range)
  - [Standing ground: CNormalAttackAI with Minimum Attack Distance 0](#standing-ground-cnormalattackai-with-minimum-attack-distance-0)
  - [CChargeAttackAI and CStrafeAttackAI: placeholders, never use](#cchargeattackai-and-cstrafeattackai-placeholders-never-use)
  - [CIsEnemyNearbyAction: enemies near the player only](#cisenemynearbyaction-enemies-near-the-player-only)
  - [CDamageExpandingRadiusAI: a damage ring that hits everyone](#cdamageexpandingradiusai-a-damage-ring-that-hits-everyone)
  - [CSkeletonTransition: a live hook on state changes](#cskeletontransition-a-live-hook-on-state-changes)
- [How to verify a class nobody has read](#how-to-verify-a-class-nobody-has-read)
- [The 105 unused classes](#the-105-unused-classes)

---

## Read this first: classes that crash

Every class is registered through `FUN_00415b60(desc, name, version, parent, size, abstract, creator, arrayCreator, props)`.
The abstract flag is stored at `desc+0x48`. Creating an object by name goes through `FUN_00415fc0`, which builds it
only if that flag is 0. **For an abstract class it shows the "DataCrash" message box and exits the process**
(`FUN_00691f1b(-1)`). So writing `Attack AI=CChargeAttackAI` in a can is a crash to desktop when that can loads.

Signs of an abstract placeholder, all visible in its registration:

- abstract flag 1,
- a creator of `FUN_00628c10`, which is `return 0;`,
- a props function of `FUN_004665d0`, the shared empty function (no fields),
- the same size as its parent.

`CAttackAI`, `CChargeAttackAI` and `CStrafeAttackAI` all look like this. Check any class from the list below for
these signs before naming it in data.

Two more registry facts:

- **Aliases.** `FUN_004157d0(name)` adds a second name to a class (`desc+0x50` list, `+0x54` count). The lookup
  `FUN_00415e60` checks aliases too, so an alias loads as the real class. This is how renamed classes keep loading.
- **A missing leading C is added.** The lookup retries with a `C` in front.

---

## Verified

### CCallForReinforcementsAction: a working call for help

**Works** (code). This lifts the limit in the old notes that "nothing can address nearby enemies": a creature can call
idle allies within a radius into its fight. 0.53.0's finding that the engine has no call for help was wrong.

| Field | Offset | Type | Default |
|---|---|---|---|
| `Requester Name` | +0x08 | entity name | `$Trigger` |
| `Max Distance` | +0x0C | float | 500 (range 0 to 1e8, step 10) |

- Registration `0x006220b0`, size 0x10, vtable `0x006df250`, execute at slot +0x84 = `0x00622290`.
- **What it does:** it takes the requester's current target (entity vtable +300) and calls `FUN_00610dc0(requester, target, Max Distance)`.
  That does an oval search around the requester (Y/X 0.712766, flag 0x800000, the requester's team from `entity+0x1C & 0xFFFF`)
  and delivers a reinforcement request to each entity found (entity vtable +0x11C).
- **Who answers:** `CSkeletonAI`'s message handler (`0x00472240`, line 33) acts on the request only if all of these hold:
  1. the message type is the request (`DAT_00809e78`);
  2. `Respond to calls for reinforcements` (CSkeletonAI +0x30) is 1;
  3. the creature is in **Patrol** state (not already fighting);
  4. the caller's target is one of its valid targets (the category mask at +0x58);
  5. it is not already chasing that target.
  Then it takes the target (vtable +0xD0).
- `Respond to calls for reinforcements=1` is already set on **698** vanilla placements. Nothing in vanilla ever sends the call.
- **A correction to `releases.md`.** 0.29.0, 0.30.0 and 0.53.0 called this action a dead end ("a radio nobody transmits
  on"), and 0.30.0 left open whether the listening field did anything. It does: the action works when something fires it,
  and the field is the listener's switch. 0.30.0 already set it to 1 on all 16 hostile goblin cans, so goblins would answer.

```
Action=CCallForReinforcementsAction
{
	Requester Name=$Trigger
	Max Distance=500
}
```

**Caveats.** Answering creatures must be idle, so it pulls in a group that has not noticed you, which is the point.
The team filter uses the entity team field, and every can in the game is `Team Number=Nutral`, so in practice the
filter that matters is each listener's own `Valid Targets`. A Templar (targets `Enemy`) ignores an English soldier's call
to attack the player. Fire it from a can's damage slot or a `CSkeletonTransition` (below) on the switch to Attack.

### The CSkeletonAI retreat: cut, does nothing

**Inert** (code). `CSkeletonAI` registers these fields:

| Field | Offset | Type | Default |
|---|---|---|---|
| `Retreat when` | +0xA4 | float, "% Health or less" | 40 in the editor (0 to 100) |
| `Retreat Start Action` | +0xA8 | action | |
| `Has Started Retreat` | +0xAC | debug flag | |

- The `State` field (+0xC0) is 0 Patrol, 1 Pursue, 2 Attack, **3 Retreat**, 4 Investigate. The strings are stored in reverse beside "Any" and "Unknown".
- The state setter `0x00473b00` fires `Retreat Start Action` on entering state 3.
- **But all 31 of its callers pass 0, 1, 2, 4 or 5, never 3**, and the tick `0x004726d0` has no case for 3.
- So setting `Retreat when` on a can does nothing. Every shipped can sets 0.
- A real retreat has to be built. 0.99.11 does it with a `CGoToAI` temporary task: see `tools/build_soldier_retreat.py`.

All other states are entered and run. Retreat is the only dead state in CSkeletonAI.

### CStandStillAttackAI: a turret while in range

**Works** (code). Its parent is `CAttackAI`, not `CNormalAttackAI`. Size 0x3C, registration `0x004743d0`, vtable `0x006be090`.
It overrides only begin (+0x78, `0x00474530`) and tick (+0x7C, `0x00474570`).

| Field | Offset | Notes |
|---|---|---|
| `Shoot Behavior` | +0x10 | the same embedded block `CNormalAttackAI` uses; copy it from a vanilla block |
| `Turn Behavior` | +0x30 | the same; copy it |

- **The tick only ticks those two behaviours:** it turns toward the target and fires the current weapon or skill.
  Nothing moves the creature.
- **It still moves out of range.** CSkeletonAI keeps checking range every tick. When the target passes the skeleton's
  attack range (+0x90, registered as "Attack/Max Dist", so the key in a can is `Max Dist`; default 200 px), it switches
  to Pursue, and the Pursue AI walks the creature after the target.
- **A shot can be cut off.** Only `CNormalAttackAI` is protected from losing the attack state mid-shot (its +0x51/+0x52 flags).
- **For a true turret,** also neutralise `Pursue AI`. The pursue state null-checks it, so with none it waits for the
  target to come back. That data can blank the field is not yet confirmed.

```
Attack AI=CStandStillAttackAI
{
	Shoot Behavior=<copied from the creature's vanilla CNormalAttackAI block>
	Turn Behavior=<copied from the creature's vanilla CNormalAttackAI block>
}
```

Prefer the next entry unless you need what this class drops.

### Standing ground: CNormalAttackAI with Minimum Attack Distance 0

**Works** (code). `CNormalAttackAI` (registration `0x00456930`, size 0x68, vtable `0x006bc1b0`, tick `0x00457570`) is the
attack AI every vanilla creature uses. Its movement code is skipped when `Move Behavior` is empty **or**
`Minimum Attack Distance` is 0, which the engine labels "Do not move while attacking" (tick lines 139 to 140). Write it
the way 202 vanilla cans do, as the label itself: `Minimum Attack Distance=Do not move while attacking`, not `0`. The
creature then stands, turns and fires, and keeps the mid-shot protection that `CStandStillAttackAI` lacks.

| Field | Offset | Default | Meaning |
|---|---|---|---|
| `Shoot Behavior` | +0x10 | | firing |
| `Turn Behavior` | +0x30 | | facing |
| `Move Behavior` | +0x3C | | movement; empty means never move |
| `Minimum Attack Distance` | +0x40 | 100 | distance it closes to; **0 = do not move while attacking** |
| `Move Buffer Zone` | +0x44 | 50 | hysteresis on re-approach |
| `Use Primary Shoot Behavior` | +0x58 | 1 | |
| `Shoot Completed` | +0x64 | empty | actions after each shot; the attack bank (see engine-notes) |

- **Every vanilla bow can sets `Minimum Attack Distance=350`** (thief, English, goblin archers alike). That is the
  backing-off the thief archers show; a melee thief has 100. The `Max Attack Range=500` (35 for the mace) seen in the
  same cans is **not** an attack AI field: it belongs to the weapon, the `CPlugInBehaviorAttack` on the can's
  `CAIInventory` default item. `CNormalAttackAI` has no such field. (Corrected by the can editor's build, 2026-11-09.)
- **`CStandGroundAttackAI` is not a class.** It is an alias for `CNormalAttackAI`, added at `0x00456fc0`, almost
  certainly the class's old name, so it loads as a plain `CNormalAttackAI` with no behaviour of its own.
- **Melee creatures set to 0 are useless** against a target that keeps its distance. Use it on archers and casters.

### CChargeAttackAI and CStrafeAttackAI: placeholders, never use

**Stubs, and naming either crashes the game** (code). Both are registered exactly like the abstract `CAttackAI`:
size 0x10, abstract flag 1, creator `FUN_00628c10` (`return 0;`), empty props, no vtable, no subclasses.

- `CChargeAttackAI`: registration `0x0044a270`.
- `CStrafeAttackAI`: registration `0x004745d0`. The strings "Strafe Left" and "Strafe Right" have no references.

Neither behaviour exists in code. A charge or a strafe would have to be built from other parts.

### CIsEnemyNearbyAction: enemies near the player only

**Works, with no fields** (code). Size 8, registration `0x00435c50`, vtable `0x006b8d40`, test at slot +0x74
(`0x00435db0`; the slot matches `CIsAliveAction`'s).

- **It ignores its trigger, `$Trigger` and everything else**, and always measures from the **player character**.
- **The area is a fixed square:** ±320 units in X and Y, so 640 by 640. It is not an oval and has no radius field.
- **It returns true** if any entity in that square has the **Enemy** category bit and the alive flag (0x100000).
  That is the creature's own `Category`, not its targets or team. A pacified creature that lost Enemy does not count,
  and corpses do not count.

```
If=CIsEnemyNearbyAction
{
}
```

Use it for "is the player in a fight", for example to hold a scene or a bark until the area is clear. It cannot
tell you what is near an NPC.

### CDamageExpandingRadiusAI: a damage ring that hits everyone

**Works; one field is inert, and it never stops** (code). Parent `CLayerPartAI`, size 0x34, registration `0x0044b9b0`,
vtable `0x006bab38`, tick +0x7C = `0x0044bec0`.

| Field | Offset | Default | Notes |
|---|---|---|---|
| `Damage` | +0x14 | 100 | per second; each tick deals `Damage * dt` |
| `Damage Type` | +0x30 | Unavoidable | passed to TakeDamage |
| `Damage Creator` | +0x10 | 0 | **inert**: both branches make the same call |
| `Use Animation For Radius` | +0x11 | **1** | if set, the radius comes from the owner's animation frame and the four fields below are ignored |
| `Start Radius` | +0x18 | 10 | px |
| `End Radius` | +0x1C | 100 | px |
| `YX Ratio` | +0x20 | 0.712766 | |
| `Start To End Time` | +0x24 | 2 | seconds |

- **Each tick it damages everything carrying the damageable-creature mask (0x840000)** inside the growing oval.
  There is no team filter and no line of sight. The player, allies and enemies all take it; only the owner's creator is spared.
- **The owner must be an animated entity with a current animation,** or it does nothing silently.
- **The owner itself is not excluded,** so put it on a non-creature effect entity, never on a creature.
- **It never ends.** After the time it holds at End Radius and keeps dealing damage until you delete the owner or
  remove the AI. Use a `CDelayAction` then `CDeleteAction`.

```
Action=CAddAIAction
{
	Target Name=<an effect entity with a model and animation>
	AI=CDamageExpandingRadiusAI
	{
		Marked For Deletion=0
		Publisher=
		Damage=100
		Damage Type=Damage
		Damage Creator=0
		Use Animation For Radius=0
		Start Radius=10
		End Radius=100
		YX Ratio=0.712766
		Start To End Time=2
	}
	Delay Between Adds=0
}
```

### CSkeletonTransition: a live hook on state changes

**Used by vanilla** 509 times in 337 files, so this is proven, not dormant. It is listed here because it is the natural
way to fire the classes above. A `CSkeletonAI` can carry `Transition=Array` of `CSkeletonTransition` items. Each has:

- `Trigger`: the values seen are `Once Per New Target`, `Target Acquired`, `Target Lost`, `First Time` and `Every Time`;
- `From State` and `To State`: Patrol, Pursue, Attack, Investigate, or Any;
- an `Action`.

Vanilla uses it to play a creature's alert sound on its first switch to Attack:

```
Transition=Array
{
	Array Count=1
	Array Item=CSkeletonTransition
	{
		Trigger=Once Per New Target
		From State=Any
		To State=Attack
		Action=CPlaySoundAction { ... }
		IsDone=0
	}
}
```

Put a `CCallForReinforcementsAction` in that `Action`, and a creature calls nearby idle allies the moment it spots you.

---

## How to verify a class nobody has read

The method that worked for every class above:

1. **Find the registration.** Get the class name string (`get-strings`), then `find-cross-references` on it. The referencing
   code calls `FUN_00415b60`. Read the size, the abstract flag, the creator and the props function. **If it is abstract, stop: it crashes.**
2. **Read the fields.** In the props function, each field is a call:
   - `FUN_0041b340(name, offset, ...)`: a sub-object, such as an action or AI;
   - `FUN_004178b0(name, offset, ...)`: an entity name;
   - `FUN_00600210(name, offset, 1, ...)`: a bool;
   - `FUN_00601650` / `FUN_006016e0(name, offset, 4, offset, 1, default, ..., max, step)`: a float.
   Defaults are IEEE hex: `0x43fa0000` = 500, `0x42200000` = 40, `0x42c80000` = 100, `0x3f800000` = 1.
3. **Read the vtable.** It is the pointer the creator stores. Compare its slots with a known sibling:
   - for AIs, begin is +0x78, tick is +0x7C and the message handler is +0x94;
   - for actions, the condition test is +0x74 and the per-target execute is +0x84.
   `FUN_005dca20` is the shared empty function, so a slot pointing there does nothing.
4. **Decompile the class's own slots** and say what they do in play. A class can be registered, constructed and still
   inert, like the retreat, so follow the code until it touches the world.
5. **Then test it in play**, because none of this has ever run in shipped data.

---

## The 105 unused classes

Vanilla data never names these. Only the classes marked **verified** have been read; the rest are sorted by what
their names and context suggest, so check each one with the method above before using it.

**Verified** (above): CCallForReinforcementsAction (works), CStandStillAttackAI (works), CStandGroundAttackAI (alias of
CNormalAttackAI), CIsEnemyNearbyAction (works, player only), CDamageExpandingRadiusAI (works), CChargeAttackAI (crashes),
CStrafeAttackAI (crashes). The CSkeletonAI Retreat state is inert.

**Behaviour candidates, unverified.** These are the next ones worth reading:
CApproachTargetAI, CTenaciousInvestigateAI, CInvestigateAreaAI, CStandGuardPatrolAI, CSetPursueAIAction,
CSetAttackAIAction (known to return 0 when given nothing), CBroadcastMessageToAreaAction, CProximitySwitchAI,
CMultipleAIsAI, CWhileAI, CPlaySequenceLoopedAI, CPointOfIntrestAI, CCreateExplosionAction, CAddEffectAction,
CRemoveVelocityAction, CPassThroughTriggerAI, CSimpleCollideTriggerAI, CTouchingPolyongTriggerAI.

**Scripting and world actions, unverified:** CActivateRelayAction, CAddAIFromCanAction,
CAddCharacterAttributeModifierToCharacterAction, CCopyColorAction, CCreateLayerPartAction, CDialogTreeNodeAction,
CDischargeWeaponThisFrameAction, CDoOnceAction, CEndGameAction, CEntityBehaviorExecuteAction, CExpireMapsInFolderAction,
CFlipSwitchAction, CFlushMapAction, CForceMerchantToRestockAction, CGiveExperiencePointsToCharacterAction,
CIsQuestStateCompleatedAction, CPlaySoundBySurfaceTypeAction, CPlayVOAction, CPlayerDiedAction, CPositionedAction,
CQuestAction, CQuestStateAction, CRepeatAction, CRestockMerchantIfNecessaryAction,
CSendMessageIncludeTriggerAndInstigatorAndAIBaseAction, CSetCategoryAction, CSetCompassTargetAction,
CSetDamagedActionAction, CSetDestroyedActionAction, CSetInteractionSpecifierTypeAction, CSetModelAction, CSetMusicAction,
CSetTriesToCollideAction, CSwitchMusicTrackAction, CUseCannedAction, CWhileAction, CXDoorAction, CXOrAction.
Several look like older names for classes vanilla does use (vanilla writes `CUseCannedActionAction` and
`COldBad_S_e_t__C_a_t_e_g_o_r_y_Action`), so check for an alias first.

**Probably abstract base classes, do not name in data:** CAttackAI (verified abstract), CPursueAI, CInvestigateAI,
CPatrolBaseAI, CSkeletonBaseAI, CGeneratorBaseAI, CLayerPartAI, CTriggerAI, CTouchingTriggerAI,
CDischargeWeaponThisFrameBaseAction, CTemporaryTaskAI, CProxyAI, CSimpleProxyAI.

**Multiplayer and scoring, irrelevant to a single-player mod:** CGiveMeSomePointsAction, CGiveMyTeamAPointAction,
CGiveTeamAPointAction, CIsGameTypeAction, CIsMultiplayerGameAction, CIsOnSameTeamAction, CIsOnTeamAction,
CGameTypeSpecificAction.

**Engine internals, rendering and physics:** CClientRenderAI, ClientRenderAI, CCameraTrakerAI, CDrawDialogBaloonAI,
CDrawTimeoutOvalAI, CDrawTimeoutRectAI, CFlyweightLayerPartAI, CLightBeamAI, CParticleAI, CParticleSystemAI,
CPlayerControlAI, CShotAI, CGravityAI, CTurnToBounceDirAI, CWalkingUpperBodyAI, CFakeRenderHeightAction,
COffsetYSortAction, CSameAsParentAI, CPassThroughShooterAI, CShootOverAI, CXRPGSkeletonAI.

The list was made by matching every `C...Action` and `C...AI` string in the executable against every class named in
vanilla's `.zax`, `.can`, `.DialogTree`, `.Quest.txt`, item, skill, race and perk files. A string that is not a
registered class (a stray name, an error message) may appear in it.
