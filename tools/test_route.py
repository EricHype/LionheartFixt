"""The 1.0 test route: every QA case that still needs a human, in the order a new game reaches it.

Reads docs/test-route/rows.json (from tools/qa_rows.py) and the seven classified-N.json files, which judged each case
against the release history: kept, superseded by a later release, a duplicate, automated, a probe, or not a test.
Writes docs/test-route/route.json and docs/test-route/route-1.0.md.

    python tools/test_route.py
"""
import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "docs" / "test-route"
ORDER = ["1 Barcelona", "Sewers", "Wilderness", "2 Montserrat", "3 Montaillou", "4 Crypt", "5 Nostradamus",
         "6 Barcelona Attack", "7 English Shrine", "8 Alamut", "Ending", "Anywhere"]
OLD_SAVE = re.compile(r"(?i)old save|older save|existing save|save (that|which|from) (pre|before)|before (this release|install)|"
                      r"pre-0\.|on an older|a 0\.\d+\.\d+ save|needs a save from|cannot (pass|be run) on a new game|not on a new game")


LOG_NAME = ("Expected names here came from race names, but 0.60.3 found the log prints the can's User Assigned Name "
            "(a hat goblin logs Goblin Striker). A different name is not a failure on its own; check it against the can.")


def notes(r):
    """Corrections the 1.0 sweep found in a case's own expected result."""
    if r["section"].startswith("0.30.1") and r["id"].startswith("DN") and int(re.sub(r"\D", "", r["id"]) or 0) >= 5:
        r["note"] = (r.get("note", "") + " " + LOG_NAME).strip()


def version(section):
    m = re.match(r"(\d+)\.(\d+)\.(\d+)", section)
    return tuple(int(x) for x in m.groups()) if m else None


def load():
    rows = {r["line"]: r for r in json.loads((D / "rows.json").read_text(encoding="utf8"))}
    out = []
    for n in range(1, 8):
        for c in json.loads((D / f"classified-{n}.json").read_text(encoding="utf8")):
            r = dict(rows[c["line"]])
            r.update({k: v for k, v in c.items() if k != "line"})
            out.append(r)
    assert len(out) == len(rows), (len(out), len(rows))
    return out


def text(r):
    """The case's own words, whatever its table called the columns."""
    skip = {"id", "section", "line", "act", "map", "status", "by", "check", "savecheck", "note", "group"}
    return " | ".join(f"{k}: {v}" for k, v in r.items() if k not in skip and v and v != '"')


def main():
    rows = load()
    status = collections.Counter(r["status"] for r in rows)
    keep = [r for r in rows if r["status"] == "keep"]
    for r in keep:
        notes(r)
        v = version(r["section"])
        r["new"] = bool(v and v >= (0, 99, 0))
        r["old_save"] = bool(OLD_SAVE.search(r.get("note", "") + " " + text(r)))
    play = [r for r in keep if not r["old_save"]]
    old = [r for r in keep if r["old_save"]]
    by_act = collections.OrderedDict((a, []) for a in ORDER)
    for r in play:
        by_act.setdefault(r["act"] if r["act"] in by_act else "Anywhere", []).append(r)
    for a in by_act:
        by_act[a].sort(key=lambda r: (r.get("map") or "~", r["line"]))
    json.dump({"status": status, "acts": by_act, "old_save": old}, open(D / "route.json", "w", encoding="utf8"), indent=1, ensure_ascii=False)

    check = collections.Counter(r.get("check", "") for r in play)
    lines = ["# The 1.0 test route", "",
             f"Built by `tools/test_route.py` from all {len(rows)} cases in `docs/qa.md`. {status['keep']} still need checking;",
             f"{status['superseded']} were replaced by later releases, {status['duplicate']} are duplicates, {status['automated']} are automated,",
             f"{status['probe']} were deploy-only probes and {status['not-a-test']} are not tests.", "",
             f"Of the {len(play)} that a new game can reach, {check['eye']} need your eyes, {check['both']} need your eyes plus a save, and",
             f"{check['save']} are read from a save alone. **NEW** marks 0.99.x work, which has never been played. {len(old)} cases can only",
             "pass on a save from before their release, so they are listed at the end and are not part of a new-game run.", ""]
    for a, rs in by_act.items():
        if not rs:
            continue
        lines += [f"## {a} ({len(rs)})", ""]
        last = None
        for r in rs:
            m = r.get("map") or "anywhere in the act"
            if m != last:
                lines += ["", f"**{m}**", ""]
                last = m
            tag = " **NEW**" if r["new"] else ""
            how = {"save": " [save]", "both": " [eyes + save]"}.get(r.get("check"), "")
            lines.append(f"- [ ] `{r['id']}` (qa.md:{r['line']}){tag}{how} {text(r)}" + (f" -- *{r['note']}*" if r.get("note") else ""))
        lines.append("")
    lines += ["## Old saves only, not part of the new-game run", ""] + [f"- `{r['id']}` (qa.md:{r['line']}) {text(r)}" for r in old]
    (D / "route-1.0.md").write_text("\n".join(lines) + "\n", encoding="utf8")
    print(dict(status))
    print("new-game run:", len(play), dict(check), "| old-save only:", len(old), "| NEW:", sum(r["new"] for r in play))
    print({a: len(rs) for a, rs in by_act.items()})


if __name__ == "__main__":
    main()
