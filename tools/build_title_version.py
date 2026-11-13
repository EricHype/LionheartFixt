"""Stamp the mod version in the lower right of the title screen. Requested after 0.99.16.

The title screen rotates through seven paintings, `Cache/Resources/Main Menu/Painted Backgrounds/Background 01-07.seq16`
(02 and 07 are byte-identical), each a single 800x600 RLE-16 frame inside a wrapper that carries only the frame's own
header size and a per-painting "Menu Position" for the buttons. `Cache/Interface/Menu Background.frm16`, which the exe
names beside `Startup.wav`, is stamped too. Nothing in the game draws a version there: `CMainMenuDisplayOptions` names a
`Version Font`, but the text it would print is compiled into the exe, and Fixt ships data only.

The letters are a small pixel font drawn here, in white (the game's own `Courier Green` version colour, 20,150,20, was
tried first and changed at the user's request), with a one-pixel dark shadow so it reads over the two paintings whose corners have bright spots. The game's
Courier strip could not be cut up reliably: its glyphs come from a TTF at load time and no table of them ships.

Run in every cut, after the version bump: `stamped()` is a Gate 0 check that the stamp on every image is the version in
mod.json, so the title screen cannot ship a stale number. Rerunning with an unchanged version is a no-op.

    python tools/build_title_version.py
"""
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from build_shrine_repairs import register

sys.path.insert(0, str(lhbuild.MODTOOLS))
import mdl16_format as m

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ["Cache/Resources/Main Menu/Painted Backgrounds/Background %02d.seq16" % k for k in range(1, 8)] + \
         ["Cache/Interface/Menu Background.frm16"]
INK = (255, 255, 255, 255)
SHADOW = (0, 0, 0, 255)
RIGHT, BOTTOM = 10, 6       # margins from the lower-right corner
GLYPH_H = 10
GLYPHS = {
    "F": ["######", "#.....", "#.....", "#.....", "#####.", "#.....", "#.....", "#.....", "#.....", "#....."],
    "i": ["..#...", "......", "......", ".##...", "..#...", "..#...", "..#...", "..#...", "..#...", ".###.."],
    "x": ["......", "......", "......", "......", "#...#.", ".#.#..", "..#...", "..#...", ".#.#..", "#...#."],
    "t": ["......", "..#...", "..#...", "#####.", "..#...", "..#...", "..#...", "..#...", "..#..#", "...##."],
    "0": [".###..", "#...#.", "#...#.", "#..##.", "#.#.#.", "##..#.", "#...#.", "#...#.", "#...#.", ".###.."],
    "1": ["..#...", ".##...", "#.#...", "..#...", "..#...", "..#...", "..#...", "..#...", "..#...", "#####."],
    "2": [".###..", "#...#.", "....#.", "....#.", "...#..", "..#...", ".#....", "#.....", "#.....", "#####."],
    "3": [".###..", "#...#.", "....#.", "....#.", "..##..", "....#.", "....#.", "....#.", "#...#.", ".###.."],
    "4": ["...#..", "..##..", ".#.#..", "#..#..", "#..#..", "#####.", "...#..", "...#..", "...#..", "...#.."],
    "5": ["#####.", "#.....", "#.....", "####..", "....#.", "....#.", "....#.", "....#.", "#...#.", ".###.."],
    "6": ["..##..", ".#....", "#.....", "#.....", "####..", "#...#.", "#...#.", "#...#.", "#...#.", ".###.."],
    "7": ["#####.", "....#.", "....#.", "...#..", "...#..", "..#...", "..#...", ".#....", ".#....", ".#...."],
    "8": [".###..", "#...#.", "#...#.", "#...#.", ".###..", "#...#.", "#...#.", "#...#.", "#...#.", ".###.."],
    "9": [".###..", "#...#.", "#...#.", "#...#.", "#...#.", ".####.", "....#.", "....#.", "...#..", ".##..."],
    ".": ["...", "...", "...", "...", "...", "...", "...", "...", "##.", "##."],
    " ": ["....", "....", "....", "....", "....", "....", "....", "....", "....", "...."],
}


def version():
    return json.loads((ROOT / "mod.json").read_text(encoding="utf8"))["version"]


def label(v):
    return "Fixt " + v


def text_mask(text):
    """[(x, y)] of ink pixels for `text`, origin at its top-left."""
    pts, x = [], 0
    for ch in text:
        g = GLYPHS[ch]
        for y, row in enumerate(g):
            for dx, c in enumerate(row):
                if c == "#":
                    pts.append((x + dx, y))
        x += len(g[0])
    return pts, x


def placed(text, width, height):
    pts, w = text_mask(text)
    ox, oy = width - RIGHT - w, height - BOTTOM - GLYPH_H
    return [(ox + x, oy + y) for x, y in pts]


def stamp(rows, text):
    h, w = len(rows), len(rows[0])
    ink = placed(text, w, h)
    for x, y in ink:                                   # the shadow first, one pixel down and right
        if 0 <= x + 1 < w and 0 <= y + 1 < h:
            rows[y + 1][x + 1] = SHADOW
    for x, y in ink:
        rows[y][x] = INK
    return rows


def source(rel):
    """Always the vanilla image: the stamp is applied to a clean painting, never on top of an older stamp."""
    with zipfile.ZipFile(lhbuild.VANILLA) as zf:
        return zf.read(rel)


def build_one(rel, text):
    d = source(rel)
    h = m.find_header(d)
    img = m.decode_icon(d, h)
    body = m.encode_icon_rle16(h.width, h.height, stamp(img["rows"], text), h.hotspot_x, h.hotspot_y)
    # the frame runs to the end of every one of these files, and the wrapper's only size field is in the frame header
    out = d[:h.offset] + body
    check = m.decode_icon(out, m.find_header(out))
    assert check["width"] == h.width and check["height"] == h.height
    return out


def stamped(text=None):
    """Gate 0: every image carries `text` (default: mod.json's version) where the stamp goes. Returns failures."""
    text = text or label(version())
    fails = []
    for rel in IMAGES:
        p = lhbuild.FX / rel
        if not p.exists():
            fails.append(rel + ": not stamped")
            continue
        d = p.read_bytes()
        rows = m.decode_icon(d, m.find_header(d))["rows"]
        h, w = len(rows), len(rows[0])
        # the images are RGB565, so the ink comes back rounded: within 8 a channel is the stamp
        if any(max(abs(a - b) for a, b in zip(rows[y][x][:3], INK[:3])) > 8 for x, y in placed(text, w, h)):
            fails.append(rel + ": does not carry '" + text + "'")
    return fails


def main():
    text = label(version())
    if not stamped(text):
        print("title screen already reads", repr(text))
        return
    for rel in IMAGES:
        out = build_one(rel, text)
        p = lhbuild.FX / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(out)
        register([rel])
    bad = stamped(text)
    assert not bad, bad
    print("stamped", repr(text), "on", len(IMAGES), "images")


if __name__ == "__main__":
    main()
