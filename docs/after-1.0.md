# After 1.0

Options held back until 1.0 ships. Each one is designed far enough to build, and none is promised.

## Telling friend from foe, and seeing the party's health

From play after 0.99.30: *"with the quick status on i can't tell which life bars are friendly and which are enemy in a
crowded melee"*, then *"are there any changes you can think of we could make there so i could see my party's health at
a glance"*.

**What the engine allows** (`engine-notes.md`, "Quick Status bars cannot show allegiance"):

- The Quick Status bar is coloured by health alone, red through yellow to green. Its frame and size are immediates in the
  exe, and it never reads the friend or enemy flags it is sent.
- Only the hover name shows allegiance: red for an enemy, green for a player or friend, khaki for anyone else.
- The HUD's layout, its orbs and its four multiplayer slots are code, and the slots are for human players. No data file
  can add a party panel.
- Companions already carry `Companion,Player Friend`, as the reporter's save shows. Category is not the gap.

So the cue has to go on the companions themselves. The hook for it already exists: every companion's health watch in
`Fixt Companion Health Install` (`CAIHealthPercentThresholdTrigger`) fires as health crosses 75, 40 and 15 percent. Today
it only renames them `(Injured)`, `(Badly Injured)` and `(Near Death)`, and the new name shows on hover alone.

### 1. A marker that tracks health (recommended)

Each companion gets a sparse stream of motes rising from the head, and its colour follows their health:

| Health | Marker |
|---|---|
| 75% and up | `Particles/SylvantWhite` |
| below 75% | `Particles/SylvantYellow` |
| below 40% | `Particles/SylvantRed` |

- This answers both questions. Only your side has motes, so one glance in a crowd shows who is yours and who needs a
  potion.
- The emitter is vanilla's own: a `CGenericParticleSystemAI` launched from `Bip01 Head`
  (`CGrannyBoneParticleStartPositionType`), added with `CAddAIAction`. The game uses it for imbued Sylvant player heads
  (`Player Data/Canned Actions For Imbued Head Types`), and it follows a moving character.
- On each crossing the watch swaps the colour: `CRemoveAIAction` of `CGenericParticleSystemAI`, then add the new
  emitter. It needs triggers on `When Health Percent Crosses Above` too, so the colour comes back as they heal.
- The emitter goes on in `Fixt Companion Joined` and comes off on dismissal and in `Fixt Companion Died`.
- **Check first:**
  - no companion can carries a particle AI of its own, since the swap would remove it;
  - a Sylvant player's own head motes use the same models, so the companion stream needs a different burst rate or
    height to read apart.
- **Risk: clutter.** Keep the burst frequency low and the age short, and judge it in play before shipping.

### 2. A line over their head when it gets bad

At 40% and 15%, a short balloon over the companion (`<Fang staggers, badly hurt.>`) and the same line in the combat log
(`Include In Log=1`). It fires once per crossing, so it does not spam, and in a melee it appears over the right person.
Write each line in the companion's own voice, read beside their real lines in their tree.

### 3. A centre-screen alert at near death

`CPrintBigOverlayMessageAction`, which vanilla uses for "party not ready", with *"Fang is near death!"* at 15% only.
It is the loudest of the three, and it is worth having only if 1 and 2 prove too quiet.

### 4. An optional exe patch for the bar itself

This is the only way to change the bars. It would be a separate opt-in download, outside the data mod, and it needs the
"no exe patching" rule in `design.md` relaxed. The smallest change is a branch on the record's `+0x1e` (IsPlayerOrFriend)
inside the bar renderer at `0x5169c0`, giving friends a different frame colour from the dark blue (16,70,112) drawn near
`0x516bd0`.

### Reaching an existing save

The health watch is saved inline on each companion when it is first armed, so editing `Fixt Companion Health Install`
will not change a watch already running (the same trap as `Fixt Companion Growth Install`). Version it: a new flag per
companion (`Fixt Companion Health Watch v2 <name>`), and on the next run of the install, remove the old
`CAIHealthPercentThresholdTrigger` and add the new one. Then nobody has to dismiss and re-invite anyone. Today the install
runs on every join, so a save also needs a second caller that already runs during play.
