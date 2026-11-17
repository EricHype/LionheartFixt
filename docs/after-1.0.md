# After 1.0

Options held back until 1.0 ships. Each one is designed far enough to build, and none is promised, except the first:
widescreen is the first thing after 1.0.

## Widescreen, and text you can read at it (first after 1.0)

Asked for after studying KoriTama's 2014 *Lionheart Widescreen Patch*: *"if we wanted to build a better version of this
and make it compatible with fixt what would we do?"*, then *"this will be the first thing we do after 1.0 I want a
complete action plan for it. Can we do anything about the text size at larger resolutions?"*

### Ground rules

- **Fixt stays data-only** (`design.md`: "No exe patching"). Widescreen is a separate, opt-in LionheartModTools
  component with its own release. Fixt's README links to it. Both must work alone and together.
- **Never ask the player to extract or delete `data.dat`.** Every data change ships as a `modmanager` mod, built into
  `data.dat` like Fixt and the playtest kit.
- **The engine work is ours.** It is written from our own analysis, and KoriTama is credited for the findings. None of
  his code or generated art is copied.
- **GOG and Steam both** (Steam app 595060). The 2026-11-17 analysis covered only the GOG exe, so nothing may depend on
  a GOG-only fact:
  - **Exe build.** Identify it by hash. Locate every patch site by a byte pattern with expected bytes, not by a fixed
    VA, and keep one table per build.
  - **DRM.** If the Steam exe is wrapped (SteamStub or similar), the code is only unpacked once the game starts, so the
    patch must be applied after that, not when our DLL first loads.
  - **The `ddraw.dll` wrapper.** GOG ships its own D3D9 wrapper (`ddraw.dll`, set up by `dxcfg.exe`), which already
    scales the picture to the desktop. Steam may ship nothing, or players may have added dgVoodoo or cnc-ddraw.
    Presentation and scaling must work in all four cases.
  - **QA on both builds.** Every Phase 5 row runs on GOG and on Steam.

### What KoriTama's patch does (analysed 2026-11-17, Ghidra on `LionheartWidescreenPatch.exe` and the GOG `Lionheart.exe`)

**The patcher** is a wxWidgets 2.9.2 GUI. You pick a 16-bit mode from a list and tick or untick "Fullscreen mode". It
writes `Screen Width`/`Screen Height` to `Lionheart.CFG`, backs files up to `Backup\`, then patches two things.

- **Data, loose:**
  - `HUD Text Window Top/Bottom.frm16` are re-encoded onto a W×H canvas, centred, with the anchor point moved.
  - `Hud Background.frm16` and `Hud Background Without Lion.frm16` are stretched sideways; the routine handles 17
    frame types.
  - `Hud Background.txt` is updated.
  - It refuses to run while `data.dat` exists, which is the incompatibility with Fixt.
- **`Lionheart.exe`, on disk, with no check of which build it is:**
  - a 73-row value table: (VA, value type) with the value computed from W and H, such as W, H, -W, -H, W-1, W-400,
    400-W, H-164, H-198 and H-241;
  - about 67 hand-written writes, mostly short jumps chained through the int3 padding between functions.

**What the exe patches change:**

| Area | Site | Change |
|---|---|---|
| Display modes | EnumDisplayModes filter 0x619a40, float at 0x6de90c | aspect upper bound 1.4333 → 2.0 (lower bound 1.2333 unchanged) |
| Fullscreen | byte 0x718780, read by mode set 0x619f20 and present 0x61b500 | set from the checkbox |
| Camera | FUN_0061bdb0 (attract camera), detour 0x61bdd3-0x61fa73 | target clamped into [W/2, mapW-W/2] × [H/2, mapH-H/2] so an attract near a map edge can arrive |
| Edge scroll | FUN_0061ba10 | 799/599 → W-1/H-1 |
| Play area | 0x638ad0, 0x58d430 | side and top panels no longer shrink the visible rect; the 164 px bottom cut stays |
| World view | 0x5afb80, 0x5ab0e0, 0x5aad90, 0x5aaed0 | view and draw rects use W, H instead of 800, 600 |
| Map layers | 0x5a7b60 (CLayerSaveData Width) | layer width at least W |
| Windows | `Window::MoveTo` 0x40cd20 callers | Help 0x58d260, Map 0x4ba290, Inventory 0x50bfc0 and Merchant 0x5c68b0 move to (0, H-600). Character sheet 0x513960 moves flush right. Front-end pages 0x4fc230 are centred, the main menu root 0x5c12a0 becomes W×H, Options 0x48eed0 is centred. The main HUD 0x637240 moves to (0, H-198), the slider 0x646270 to H-241. The right panel 0x63a720 grows to W-400 wide and reaches H. The conversation window 0x52ae00 and popups 0x5318a0 grow to W-400 wide |
| Transitions | 0x5b25d0, 0x5b39f0 | the present call is NOPed in the fade loops and in "Start New Game" |

**Its bugs and gaps:**

1. **World Map window sized H×W.** `SetSize` at 0x654652/57 has its arguments swapped.
2. **Broken "no position" sentinel.** In the message encode/decode pair 0x5ab590/0x5ab8a0 the patched sentinel mixes -W
   and -H, so "no position" decodes as a real position whenever W ≠ H. The 0x5ab700/0x5ab9c0 pair is consistent. Its
   purpose (positional sound or effect events) is inferred.
3. **Camera clamp on small maps.** The max is applied before the min, so a map narrower or shorter than the screen
   pushes the camera's top-left negative. **This is the leading theory for the reports of broken cutscenes at high
   resolutions** (untested in play).
   - 60 of the game's 125 camera attractors start the next step of their scene from `Camera Arrived Action`.
   - Arrival means the camera got within 10 px of centring on the target, which it cannot do near a map edge.
   - Attractors that close to an edge: 1 at 800×600, 17 at 1280×720 (4 of them chained), and 47 at 1920×1080 (20 of
     them chained).
   - KoriTama's clamp rescues them on maps bigger than the screen, but not on the 11 cutscene maps smaller than
     1920×1080: House of Ilk, Shylocke Shop, Church Interior ruined, 03 Sand Dragon and 7 more.
   - There an unarrivable target leaves the scene waiting forever, under a cutscene that has disabled the controls.
   - The fix: centre on any axis where the map is smaller than the screen, and count arrival once the camera is as close
     as the view clamp allows. The first QA rows are Shylocke's scene, the Sand Dragon, the ruined church and Machiavelli's
     house at 1920×1080.
4. **Main HUD window stays 800 wide** (`SetSize(800,198)` at 0x63727e), while its art is widened. Unless something
   resizes it later (not traced), the extra art is clipped or dead.
5. **Not identity at 800×600.** The combat log width becomes W-461 (354 → 339) and the panel children W-400 (390 → 400),
   so patching at 800×600 changes the game.
6. **Missed 800/600 sites:**
   - an 800×50 bar 0x4a9350;
   - the loading screen rect 0x4be3c5;
   - the merchant text width 0x5c78b9;
   - the default Screen Width 0x5841fc (its height twin is patched).
7. **Breaks below 800×600** (negative W-400/H-600), and an offset at 0x587d73 changes sign at W = 1214. Exactly 2:1 and
   wider screens are still rejected.
8. **Fragile code.** Two jumps (`0x61c2a3`, `0x61c320`) land mid-instruction and work only because the next instructions
   reset flags and registers. Edge scroll needs the cursor on the exact last pixel. Wide resolutions can push some modes
   off the 100-entry mode list.
9. **Layout is spread, not centred.** Windows sit at the left and right edges with dead space between them, while the
   HUD art is centred.

The analysis scripts, and `ws_rem.txt` (every 800/600 immediate in the game), were made in the 2026-11-17 session's
scratchpad. Phase 1 recreates them in LionheartModTools so nothing depends on that folder.

### Text size

Fonts are data. Each `Resources/Fonts/*.FONT.TXT` names a TrueType file (`True Types/lionheart dialog.ttf`) and a `Point
Size` (dialogue 12, bubbles 10). The engine draws from a glyph sheet cached as `Cache/Resources/Fonts/*.frm16`. At
1920×1080 a 12-point font is the same number of pixels as at 800×600, so it reads at about 40% of its old size. There
are two ways to fix that, and the plan offers both:

- **A. Scale the whole frame (default).** The game renders at a logical resolution (for example 1280×720 or 1600×900),
  and the proxy DLL stretches the finished frame to the monitor's native size when it presents it. Text, HUD and art all
  grow together, nothing in the layout changes, and the HUD stays readable. The cost is some softness at non-integer
  scales; offer nearest-neighbour or bilinear filtering, and integer scaling when it fits (1280×720 → 2560×1440 is
  exactly ×2).
- **B. Bigger fonts at native resolution (option).** A `modmanager` mod raises each font's `Point Size` by a factor and
  regenerates the glyph caches. It is data, so it could even ship with Fixt as an option. Its risks need checking first:
  - **The cache:** prove whether the engine rebuilds a glyph sheet from the TTF when it is missing or stale. If it does
    not, we render the sheets ourselves into `.frm16` (ModTools already writes `.frm16`).
  - **Line height and wrapping:** these come from the font, but several windows are fixed sizes (dialogue 800×436,
    balloon wrap 200-600). Larger text may clip, so A's layout work and B have to be tested together.
  - **Fixt text that was fitted to the old size:** every line Fixt fitted to a balloon or window is affected, including
    the 0.99.29 Faust camera move, which was sized for a 600 px screen.

A and B can combine: scale 1600×900 to 4K and raise fonts 1.25×.

### Phase 1 - inventory (analysis, no code shipped)

1. **The tooling is in `LionheartModTools/tools/widescreen/`** (done 2026-11-17, 9e23c20):
   - the PE/capstone extractor for KoriTama's writes (for reference);
   - `ws_rem.py`, which lists every 800/600 immediate in `Lionheart.exe`.

   Run it on the Steam exe too.
2. **Sort every immediate** into: screen-dependent and patched by KoriTama; screen-dependent and missed; or not screen
   related (music volume, library code). Record the owner function and what it lays out.
3. **Trace what KoriTama did not:**
   - who consumes the 0x638ad0 play rect;
   - whether anything resizes the main HUD window after 0x63727e;
   - what the 0x5ab590 messages carry;
   - why the fade loops' present was NOPed. Reproduce the bug on an unpatched exe at a forced wide mode.
4. **Write it up** as `engine-notes.md`, "What assumes 800×600", in the notes' usual form: address, owner, effect.
5. **Exit:** every screen-dependent site has an owner and a decided treatment.

### Phase 2 - the runtime engine patch

1. **Prototype the delivery first.** The patch runs in memory from a proxy DLL, decided 2026-11-17. It is not a
   `ddraw.dll`, because that slot belongs to GOG's wrapper, dgVoodoo or cnc-ddraw. The game also imports
   `MSACM32.dll` and `WINMM.dll`.
   - Proxy `msacm32.dll`, with `winmm.dll` as the fallback. It forwards every export to the system DLL.
   - It applies the table once the code is unpacked: on the first `DirectDrawCreate`, or when the expected bytes appear.
   - It does nothing, and logs why, on an unknown build.

   Prove four things on both GOG and Steam:
   - it loads on Windows 10 and 11, and under Wine or Proton with a DLL override;
   - it coexists with GOG's wrapper, dgVoodoo, cnc-ddraw and DxWnd;
   - Galaxy, the Steam overlay and Steam DRM don't block it;
   - antivirus doesn't quarantine it. Publish the source and hashes, and sign it if we can.

   If any of those fails, fall back to an on-disk patcher with the same table, an exact-build check, backup and unpatch.
   On-disk patching cannot work at all on an exe with encrypted code, so check that first on the Steam build.
2. **Get a Steam copy** and repeat the 2026-11-17 analysis on it:
   - hash it, and look for DRM;
   - list its DLLs and its folder (does it ship a wrapper?);
   - diff its code against GOG's at the patch sites.

   Locating sites by byte pattern is required only if the builds differ.
3. **Patch table as data** (`widescreen-sites.json`). Each entry has the VA, the expected original bytes, the
   replacement and its formula in W, H and the HUD height. The loader refuses to apply anything if one expected-bytes
   check fails, which makes it safe against other builds and other patches. A gate checks every detour lands on an
   instruction boundary.
4. **Configuration** in `Lionheart.CFG`: the existing `Screen Width/Height`, plus new keys `Render Width/Height` (the
   logical resolution), `Scale Filter`, `Integer Scale`, `Layout=Centred|Spread`, `Fullscreen` and `Windowed Borderless`.
5. **Presenting the frame (text option A).** On GOG, test whether its wrapper (`dxcfg.ini`: `scaling=fit`) already
   stretches a 1280×720 render to the desktop. If it does, our DLL needs no scaling code there. Where no wrapper scales
   (likely a bare Steam install), there are two choices:
   - hook the present at 0x61b500 (a GOG address, to be located on Steam) so the back buffer is stretched to the window
     or display size;
   - bundle a licence-compatible wrapper such as cnc-ddraw (MIT; first confirm Lionheart's renderer is plain
     DirectDraw, which the `pixomatic.dll` software renderer suggests).

   Borderless windowed then comes from the same hook or the wrapper.
6. **Display modes:** ignore the driver's mode list for the logical size. Render to an off-screen surface of the chosen
   size and present at native size, so any aspect works.

### Phase 3 - layout (the better version)

1. **Centred is the default.** The 800×600 HUD group stays one block, centred at the bottom: HUD, text windows, panels,
   inventory and character sheet. Full-screen windows (Help, Map, Merchant, menus) are centred as 800×600 frames. The
   world view fills the whole screen. Nothing grows sideways.
2. **Spread is an option.** Panels go to the screen edges like KoriTama's, but with the art and click areas matching.
3. **Fix every bug in his list:**
   - the World Map size swap;
   - the sentinel, using one consistent marker;
   - the camera clamp, which centres when the map is smaller than the screen;
   - the HUD window width;
   - identity at 800×600, as a hard test: patched at 800×600, the game must behave exactly as vanilla;
   - the missed sites;
   - edge scroll at or beyond the last pixel;
   - the mode filter.
4. **Minimum and maximum size:** refuse below 800×600, and test the layout up to 3840×2160 and 32:9.

### Phase 4 - art and fonts as a mod package

1. **`widescreen-ui` modmanager mod.** A build step generates, for the configured logical resolution:
   - the HUD Text Window Top/Bottom and both HUD backgrounds;
   - `Hud Background.txt`;
   - frames or backdrops for 800×600 full-screen art: the main menu painted backgrounds, `Menu Background`, the loading
     screen and full-screen windows (a dark frame or a blurred extension, judged in play).

   It starts from whatever the current `data.dat` holds, never from vanilla, so Fixt's stamped title version and any
   other mod's art survive. Rebuild after installing Fixt; modmanager's load order puts it last.
2. **`larger-text` option (text option B):** a font scale factor, plus glyph caches regenerated or proven to rebuild
   themselves.
3. Both stay out of Fixt's own `files/`, so Fixt remains independent of resolution.

### Phase 5 - Fixt at wide resolutions

1. **List every Fixt change that depends on the screen:**
   - camera moves (`build_faust_cam.py` and every attract or camera marker Fixt placed);
   - balloon offsets and long balloons;
   - `CPrintBigOverlayMessageAction` lines;
   - the Quick Status work;
   - stamped menu art.
2. **QA section `WS`** at 800×600 (identity), 1280×720, 1600×900, 1920×1080, 2560×1440 scaled from 1280×720, and one
   32:9 mode. Rows:
   - every scripted camera scene Fixt touched, and the Daeva of Pain's speech readable;
   - the world map, the merchant, the conversation window, the inventory and character sheet;
   - HUD seams and click areas;
   - edge scroll;
   - camera at map edges on the three smallest maps;
   - fade-to-black transitions, including the Goblin Girl's pie fade (0.99.32);
   - main menu, loading screen and save/load;
   - text: one long conversation and one long balloon at both text options.
3. Fix what Fixt itself got wrong there in normal Fixt releases (data only). Engine issues go back to Phases 2-3.

### Phase 6 - release

- A ModTools release, `lionheart-widescreen`: the proxy DLL, the `widescreen-ui` mod, the `larger-text` mod, install and
  uninstall steps, the tested resolution list and KoriTama's credit.
- **Uninstall is part of the release check:** delete the DLL, disable the mods, rebuild, and confirm the game is byte-for-
  byte the same as vanilla plus Fixt.
- **Fixt's README:** "Widescreen: optional, separate, tested with Fixt X.Y at these resolutions."

### Open decisions

1. ~~Proxy DLL or on-disk patcher.~~ **Decided 2026-11-17:** an in-memory patch from an `msacm32.dll` proxy (fallback
   `winmm.dll`), never `ddraw.dll`, supporting GOG and Steam. The on-disk patcher is kept only as the fallback if the
   Phase 2 prototype fails.
2. **The default render resolution** for 1080p and 1440p players (proposed: 1280×720 at 1440p, which is integer ×2, and
   1600×900 or native at 1080p with larger text).
3. **The art treatment** behind 800×600 full-screen windows: a plain dark frame or a blurred extension.

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
