"""Calmed snakebreed can be force-attacked, and attacking one turns them all. Issue #15: "When siding with the Snakebreed
they become untargetable, but they should still be able to be attacked by pressing K (force attack)". Decided
2026-11-18: "and if you force attack they should all turn hostile".

0.11.0's pacifier, on 47 generator spawns across `01 Grove Exterior` (21), `02 Druid Council Level1` (16) and `Level2`
(10), blanks a snakebreed's targets, drops `Enemy` and gives it a `GetCloseThenTrigger` click showing `52 sentry
passive`. That type has `Fight When Attack Is Forced=0`, so with `Enemy` gone neither a click nor K could attack it.

Each site now:

  * clicks as `GetCloseThenTalk` (`Fight When Attack Is Forced=1`, force-attack cursor Fight), with the same balloon,
    so K works and nothing else about the click changes but the cursor;
  * carries a damaged script, in the shape the Hujark already use: if the damage came from the player or a friend,
    fire `Fixt calmed snakebreed turn`.

`Fixt calmed snakebreed turn`, one per map and Trigger Only Once, turns every snakebreed of that map back by name:
targets `Player,Player Friend`, `Enemy` restored, the stock `GetCloseThenTriggerAndFight` click (radius 50, as the
`Snakebreed` can has it) swapped back in, and `CGoToCombatAction` on all of them. It deliberately does not fire
`truce broken`, which also docks karma for breaking Sahar's word: attacking a garrison you gave no word to costs no
karma (`KM5`). Where a word was given, `sahar word given` re-arms the same damaged slot by name with `truce broken`,
so that route keeps its penalty. Nor does it fire the Grove's `sentry draws`, which spawns the three gate packs; that
stays the parley's.

Also: `truce broken` (`Level2`) and one block in `4 Undercroft` were hand-written as `Categories To Add=`, a spelling
vanilla never uses (it writes `Categories to add=` 526 times). They are corrected to vanilla's, whatever the parser's
case rules turn out to be.

A map edit, so it reaches Montserrat maps not yet entered. A rerun is a no-op.

    python tools/build_snakebreed_truce.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import B, CR
from build_shrine_repairs import register

D = "Levels/2 Montserrat/"
MAPS = {
    "01 Grove Exterior": "Snakebreed, Snakebreed Viper, Snakebreed Crusher, Snakebreed Summoner",
    "02 Druid Council Level1": "Snakebreed, Hall Snakebreed",
    "02 Druid Council Level2": "Snakebreed, Snakebreed Viper, Snakebreed Crusher, Snakebreed Summoner",
}
SPELLING = ["02 Druid Council Level2", "4 Undercroft"]
TURN = "Fixt calmed snakebreed turn"
PASSIVE = "Node ID=52 sentry passive" + CR
OLD_TYPE = "Interaction Type=Interaction Specifiers/GetCloseThenTrigger" + CR
NEW_TYPE = "Interaction Type=Interaction Specifiers/GetCloseThenTalk" + CR
FIGHT = lhbuild.specifier("GetCloseThenTriggerAndFight", "", radius="50")
DAMAGED = B("CSetDamagedScriptActionAction", [
    ("New Damaged Action", ("CIfAction", [
        ("If", ("CCheckCategoryAction", [("Target Name", "$Instigator"), ("Category to check for", "Player,Player Friend")])),
        ("Then", lhbuild.relay(TURN)), ("Else", ""), ("Return failure if the If failes", "0")])),
    ("Target Name", "$Instigator")]).rstrip(CR)


def turn_action(names):
    return lhbuild.multi([
        ("CSetTargetTypeAction", [("Entity Name", names), ("Name To Target", ""), ("Valid Targets", "Player,Player Friend")]),
        ("CAddCategoryAction", [("Target Name", names), ("Categories to add", "Enemy")]),
    ] + lhbuild.swap_specifier(names, FIGHT) + [
        ("CGoToCombatAction", [("Enemy Name", names)]),
    ])


def add_relay(z, names):
    if "\t\t\tName=" + TURN + CR in z:
        return z, 0
    # park it beside the map's own `routed` relay
    i = z.index("\t\t\tName=routed" + CR)
    s = z.rindex("Level Part=", 0, i)
    part = z[s:lhbuild.balanced(z, s)]
    x = re.search(r"\n\t\t\tPosition X=(-?\d+)", part).group(1)
    y = re.search(r"\n\t\t\tPosition Y=(-?\d+)", part).group(1)
    return lhbuild.add_parts(z, [lhbuild.relay_part(TURN, turn_action(names), x, str(int(y) + 40))]), 1


def sites(z):
    n, k = 0, 0
    while True:
        p = z.find(PASSIVE, k)
        if p < 0:
            break
        k = p + 1
        then = z.rindex("Then=CMultipleActionsAction", 0, p)
        e = lhbuild.balanced(z, then)
        assert then < p < e, "the balloon is not inside the pacifier's Then"
        blk = z[then:e]
        if "Relay Name=" + TURN + CR in blk:
            continue
        assert blk.count(OLD_TYPE) == 1 and blk.count(PASSIVE) == 1, "unexpected pacifier at %d" % then
        c = blk.index("Item Count=")
        ce = blk.index(CR, c)
        cnt = int(blk[c + len("Item Count="):ce])
        assert cnt == 4, cnt
        blk = blk[:c] + "Item Count=" + str(cnt + 1) + CR + "Action=" + DAMAGED + blk[ce:]
        blk = blk.replace(OLD_TYPE, NEW_TYPE, 1)
        z = z[:then] + blk + z[e:]
        k = then + len(blk)
        n += 1
    return z, n


def main():
    touched = []
    for mp in sorted(set(MAPS) | set(SPELLING)):
        rel = D + mp + ".zax"
        z0 = lhbuild.read(rel)
        z, a, b = z0, 0, 0
        if mp in MAPS:
            z, a = sites(z)
            z, b = add_relay(z, MAPS[mp])
        fixed = z.count("Categories To Add=")
        z = z.replace("Categories To Add=", "Categories to add=")
        if z != z0:
            lhbuild.write_map(rel, z)
            touched.append(rel)
        print("  %s: %d sites, %d relay, %d spelling" % (mp, a, b, fixed))
    if touched:
        register(touched)


if __name__ == "__main__":
    main()
