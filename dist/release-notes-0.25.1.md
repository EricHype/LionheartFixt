# Lionheart Fixt 0.25.1 - the startup crash

**Install this over any earlier release. 0.19.0 through 0.25.0 could not reach the main menu.**

Seven published releases. The game said so precisely, in its own diagnostic dialog, before the title
screen:

> The item we are looking for is `Skills/Fighting/Melee` [...] It was referenced by
> `Resources/Races/NPCs/Grace OMalley.Race:Skill Preset:Skill`

There is no `Skills/Fighting/Melee` in Lionheart and there never was. The real skill is
`Skills/Fighting/OneHandedMelee` -- which the crash dialog itself lists as item 9 of the skills it *did*
find, one line below the name it was looking for.

Grace O'Malley's race was authored in 0.19.0, during a review that found she could not have survived the
fight the act drops her into. The melee preset that fixed that named a skill that does not exist.

The engine resolves a race's skill presets **at load**, so this was not a latent defect waiting for the
right save. It was every launch, for everyone.

## The fix

One value in one file: `Melee` becomes `OneHandedMelee`, keeping the preset of 110. Grace is what the
0.19.0 review intended -- 190 AC, 165 hit points, OneHandedMelee 110, Evasion 55.

## Why seven releases went out with it

`tools/validate.py` resolves resource references and has done since early on; it is what caught the wrong
requirement paths during 0.22.0. It had two gaps, and they lined up exactly:

| gap | effect |
|---|---|
| it scanned only `.dialogtree`, `.zax` and `.can` | `.race` files were **never** examined |
| it had no reference kind for `Skill=`, `Race=` or `Derived Character Attribute=` | even a scanned race would not have had these checked |

Either gap alone would have caught this. Both together meant the one reference kind the engine kills the
process over was the one nothing looked at.

Both are closed. `.race` joins the scanned suffixes, and three kinds are added: `Skill=` and
`Skill to select=` resolving to `.Skill`, `Derived Character Attribute=` to `.DerivedCharacterAttribute`,
and `Race=` to `.Race` or `.race`, since the shipped archive is inconsistent about that extension's case.

The check was then proved rather than assumed: reintroducing the exact bug makes the gate exit 1 with
*"Grace OMalley.Race: reference does not resolve to any file: 'Skills/Fighting/Melee'"*, and restoring
the fix makes it pass.

A sweep of all 279 Fixt resource files, across **376** references of these kinds, found **exactly one**
unresolved -- the one above. That sweep also covers the 36 derived-attribute references 0.25.0 added the
day before with its twelve thief races; they resolve, but until now nothing had proved it.

## The honest part

This is the failure mode the project's own standing trade makes likely: finish development, then
playtest. Nothing had been launched since 0.19.0, and **a crash before the main menu is invisible to
every gate that reads files rather than running them.** Six releases of work were published on top of a
build that could not start.

Nothing in 0.19.0 through 0.25.0 is withdrawn or changed by this -- all of it was correct, and none of it
had ever run.

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt.

Download, unzip, run `Mod Manager.bat`. No save requirements: this one is a one-value repair and applies
to any character, including none. If you have any earlier release installed, replace it.

https://github.com/EricHype/LionheartFixt/releases/tag/v0.25.1
