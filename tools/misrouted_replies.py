"""Replies that read like the question an unreachable node answers, and go somewhere else.

`vo_reach.py` asks whether anything enters a recorded node. It cannot see the case where something
*should*: 0.94.0's DaVinci reply, "I could try to speak with the Inquisition about the gem", went to
a generic goodbye while `320 speak to inquisition`, recorded and answering exactly that, sat beside
it. So this ranks each tree's replies by word overlap with each unreachable node's id and text.

**A survey, and a noisy one.** Shared words are not a match: of the first run's 21 hits, one was the
real defect. Read both ends before believing a row.

    python tools/vo_reach.py > vo.txt
    python tools/misrouted_replies.py vo.txt
"""
import os
import re
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VANILLA = os.environ.get("LIONHEART_VANILLA", os.path.join(
    "C:" + os.sep, "Program Files (x86)", "GOG Galaxy", "Games",
    "Lionheart - Legacy of the Crusader", "data.dat.vanilla.bak"))
STOP = set("""the a an i you your to of and in is it that this for me my be will with on at as are
was have do not but if so we they he she his her what who how why can could would should there here
about from now then them him our us am did has had or by very all some any just more no yes well oh
ah""".split())

zf = zipfile.ZipFile(VANILLA)
shipped = {Path(n).stem.lower(): n for n in zf.namelist() if n.lower().endswith(".dialogtree")}
ours = {p.stem.lower(): p for p in (REPO / "files").rglob("*") if p.suffix.lower() == ".dialogtree"}


def words(s):
    return {w for w in re.findall(r"[a-z']+", s.lower()) if w not in STOP and len(w) > 2}


def parse(text):
    nodes = {}
    for part in re.split(r"^-{5,}\s*$", text, flags=re.M):
        m = re.search(r"^\s*Node ID=(.*)$", part, re.M)
        if m:
            said = re.search(r"^Text=(.*)$", part, re.M)
            replies = re.findall(r"^Reply Text=(.*)\r?\n\s*Go to node ID=(.*)$", part, re.M)
            nodes[m.group(1).strip().lower()] = (m.group(1).strip(), said.group(1).strip() if said else "", replies)
    return nodes


rows = re.findall(r"^\s+(\d+) KB\s+(\d+)r\s+(.+?) / (.+)$", open(sys.argv[1], encoding="utf8").read(), re.M)
for kb, _, tree, node in rows:
    tree = tree.strip().lower()
    key = node.strip().lower()
    raw = ours[tree].read_bytes() if tree in ours else zf.read(shipped[tree])
    nodes = parse(raw.decode("latin-1"))
    if key not in nodes:
        continue
    want = words(nodes[key][0]) | words(nodes[key][1])
    hits = []
    for nid, (_, _, replies) in nodes.items():
        for text, target in replies:
            w = words(text)
            overlap = w & want
            if nid != key and text.strip() and target.strip().lower() != key and len(w) >= 2 \
                    and len(overlap) >= 2 and len(overlap) / len(w) >= 0.4:
                hits.append((round(len(overlap) / len(w), 2), text.strip()[:80], target.strip()[:32]))
    if hits:
        print(f"\n{kb} KB  {tree} / {node.strip()}  :: {nodes[key][1][:100]}")
        for hit in sorted(hits, reverse=True)[:3]:
            print("   ", hit)
