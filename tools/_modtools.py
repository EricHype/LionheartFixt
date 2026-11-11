"""Where LionheartModTools is, for the Fixt tools that now forward to it.

validate.py, check_series_flow.py, auto_open_risk.py, savecheck.py and test_savecheck.py used to
hold their checks here. The engine-rule halves moved to LionheartModTools so any Lionheart mod can
run them; what stayed in Fixt is the part that is about Fixt's own conventions, and it lives in this
module so validate.py and check_series_flow.py cannot drift apart.

The mod tools are found from `--tools DIR`, else $LIONHEART_TOOLS, else ../LionheartModTools.
"""
import ast
import importlib.util
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FILES = REPO / "files"
DEFAULT_VANILLA = os.path.join(
    "C:" + os.sep, "Program Files (x86)", "GOG Galaxy", "Games",
    "Lionheart - Legacy of the Crusader", "data.dat.vanilla.bak")


def vanilla():
    return os.environ.get("LIONHEART_VANILLA", DEFAULT_VANILLA)


def tools_dir(argv=None):
    """The mod tools folder. A `--tools DIR` in `argv` is honoured and removed from it."""
    t = os.environ.get("LIONHEART_TOOLS", str(REPO.parent / "LionheartModTools"))
    if argv is not None:
        for i, a in enumerate(argv):
            if a == "--tools" and i + 1 < len(argv):
                t = argv[i + 1]
                del argv[i:i + 2]
                break
            if a.startswith("--tools="):
                t = a.split("=", 1)[1]
                del argv[i]
                break
    return Path(t)


def load(name, argv=None, module=None):
    """Import <tools>/<name>.py. `module` names it privately, for a tool whose Fixt shim has the
    same file name -- `import savecheck` from tools/ must still find the shim."""
    d = tools_dir(argv)
    path = d / (name + ".py")
    if not path.exists():
        sys.exit("%s not found in %r -- pass --tools or set LIONHEART_TOOLS" % (path.name, str(d)))
    if str(d) not in sys.path:
        sys.path.append(str(d))
    mod_name = module or name
    if mod_name in sys.modules:
        return sys.modules[mod_name]
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


def public(mod):
    """A module's names, for a shim to re-export so `import savecheck` keeps working."""
    return {k: v for k, v in vars(mod).items() if not k.startswith("__")}


def spawn_name_skip():
    """build_spawn_names.SKIP, read without importing it (its import opens the archive via lhbuild)."""
    src = (Path(__file__).resolve().parent / "build_spawn_names.py").read_text(encoding="utf-8")
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "SKIP" for t in node.targets):
            return set(ast.literal_eval(node.value))
    sys.exit("tools/build_spawn_names.py has no SKIP set")


def fixt_config():
    """The choices Fixt makes that another mod would not.

    chained_relay_prefix: every relay Fixt adds is named "Fixt ...", and vanilla steps some series
    from outside while they also fire themselves, so the dead-step rule covers only Fixt's relays.

    nameless_spawn_skip / excuse_vanilla: build_spawn_names.py repairs every vanilla generator whose
    spawns a script cannot address, except in the maps it deliberately skips -- so a vanilla-inherited
    miss is NOT excused here, the way it is by default for other mods.
    """
    return {
        "chained_relay_prefix": "Fixt",
        "nameless_spawn_skip": spawn_name_skip(),
        "nameless_spawn_excuse_vanilla": False,
    }
