"""Non-voiceover audio that nothing in the game names.

**Search bytes, not fields.** The first pass indexed text field values and reported 457 files and
15.5 MB. Almost all of that was false: spell and creature sounds are referenced from inside the
binary `.mdl16` model caches, which no field search can see. This indexes every run of path-shaped
characters in every entry, binaries and the exe included, so a stem counts only if it appears as a
whole path component and `lightning_bolt` is not credited by `lightning_bolt_2`.

**What the result does and does not mean.** Footsteps and numbered weapon hits still come back as
orphans, and they are probably names the engine builds at runtime: surface folders each holding the
same four `Zax Footstep...` files are not four unused sets. Music and ambient tracks are the
trustworthy part, because maps and trees name those in full. Treat the rest as leads.

    python tools/orphan_audio.py
    python tools/orphan_audio.py --copy "<folder>"     # write the orphans out for listening
"""
import argparse
import collections
import glob
import os
import re
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GAME = os.path.join("C:" + os.sep, "Program Files (x86)", "GOG Galaxy", "Games",
                    "Lionheart - Legacy of the Crusader")

ap = argparse.ArgumentParser()
ap.add_argument("--vanilla", default=os.environ.get(
    "LIONHEART_VANILLA", os.path.join(GAME, "data.dat.vanilla.bak")))
ap.add_argument("--copy", help="write every orphan here, keeping its folder")
args = ap.parse_args()

zf = zipfile.ZipFile(args.vanilla)
audio = [n for n in zf.namelist()
         if n.lower().endswith((".ogg", ".wav", ".mp3")) and " vos/" not in n.lower()]
stems = collections.defaultdict(list)
for n in audio:
    stems[Path(n).stem.lower()].append(n)

RUN = re.compile(rb"[a-z0-9_ ()'&,!#+\-]{2,}")
SKIP = (".ogg", ".png", ".bmp", ".tga", ".dds", ".gr2")
seen = set()


def scan(data):
    seen.update(r.strip() for r in RUN.findall(data.lower()))


for n in zf.namelist():
    if not n.lower().endswith(SKIP):
        scan(zf.read(n))
for p in (REPO / "files").rglob("*"):
    if p.is_file() and p.suffix.lower() not in SKIP:
        scan(p.read_bytes())
for exe in glob.glob(os.path.join(os.path.dirname(args.vanilla), "*.exe")):
    scan(open(exe, "rb").read())

orphans = [n for s, ns in stems.items() if s.encode() not in seen for n in ns]
size = sum(zf.getinfo(n).file_size for n in orphans)
print(f"{len(audio)} non-voiceover audio files, {len(orphans)} named by nothing, {size/1e6:.2f} MB")
for folder, count in collections.Counter(str(Path(n).parent) for n in orphans).most_common():
    print(f"{count:4}  {folder}")

if args.copy:
    for n in orphans:
        dest = Path(args.copy) / n
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(zf.read(n))
    print("wrote", len(orphans), "to", args.copy)
