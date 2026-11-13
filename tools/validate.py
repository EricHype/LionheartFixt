"""Gate 0: static validation for every file in the Lionheart Fixt mod tree.

The engine-rule checks live in LionheartModTools now, as `lhcheck.py`, so any Lionheart mod can
run them; that repo's docs/checks.md says what each one catches and the defect it came from. This
script runs them over `files/`, adds the checks that are about Fixt's own conventions, and prints
exactly what it always has.

Fixt's own:

  probes            a `PROBE ` display name marks a deploy-only experiment (check_no_probes, below)
  series-flow       the dead-step rule covers relays whose names start with "Fixt"
  nameless-spawns   leaves alone the maps tools/build_spawn_names.py deliberately skips, and does
                    not excuse a vanilla-inherited miss, because build_spawn_names repairs those
                    (both in tools/_modtools.py, shared with check_series_flow.py)

Usage:
    python tools/validate.py [--tools <LionheartModTools>] [--vanilla <data.dat.vanilla.bak>]
                             [--skip ID] [--only ID]

Both paths default to their usual locations; override them if your checkout differs.
`python <tools>/lhcheck.py --list` names the check ids. Exits non-zero on any problem, so it can
gate a build.
"""
import argparse
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _modtools  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--tools", default=str(_modtools.tools_dir()))
ap.add_argument("--vanilla", default=_modtools.vanilla())
ap.add_argument("--skip", action="append", metavar="ID")
ap.add_argument("--only", action="append", metavar="ID")
args = ap.parse_args()

sys.path.insert(0, args.tools)
try:
    import resource_format  # noqa: F401
except ImportError:
    sys.exit("cannot import resource_format from %r -- pass --tools" % args.tools)
try:
    import lhcheck
except ImportError:
    sys.exit("cannot import lhcheck from %r -- those mod tools predate it; pass --tools" % args.tools)

F = _modtools.FILES
if not Path(args.vanilla).exists():
    sys.exit("vanilla archive not found: %r -- pass --vanilla" % args.vanilla)


def check_no_probes(ctx):
    """Deploy-only experiments must never reach a release.

    The combat-AI probes are installed by hand on top of a release, live only in the working tree, and
    are untracked -- which means a `dist` build would happily package them, because the manifest globs
    `files/**`. A display name beginning `PROBE ` marks one, so this fails the gate while any is
    present and the release simply cannot be cut over them.
    """
    fails = []
    for f in ctx.files:
        if f.suffix.lower() not in (".can", ".dialogtree", ".zax"):
            continue
        text = f.read_bytes().decode("latin-1")
        for pat in (r"Display Name=(PROBE [^\r\n]*)", r"Text to print=(PROBE [^\r\n]*)"):
            for m in re.finditer(pat, text):
                fails.append(f.name + ": carries the deploy-only probe " + repr(m.group(1))
                             + " -- revert it and reinstall before cutting a release")
    return fails


def check_title_version(ctx):
    """The title screen's stamp must be mod.json's version, so a cut cannot ship a stale number.
    Rerun tools/build_title_version.py after the version bump to fix it."""
    import build_title_version
    return [f + " -- rerun tools/build_title_version.py" for f in build_title_version.stamped()]


ctx = lhcheck.Context(F, args.vanilla, config=_modtools.fixt_config())
try:
    findings, stats = lhcheck.run(ctx, only=lhcheck.split_ids(args.only), skip=lhcheck.split_ids(args.skip),
                                  extra=[("probes", check_no_probes, "self-reference"),
                                         ("title-version", check_title_version, "probes")])
except ValueError as e:
    sys.exit(str(e))
sys.exit(lhcheck.report(findings, stats, ctx.notes))
