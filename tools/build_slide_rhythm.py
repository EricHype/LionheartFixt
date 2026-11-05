"""End slides rewritten to the game's rhythm, one group at a time.

Vanilla dialogue averages 10.2 words a sentence and 3% run past 25. The slides, pitched at New Vegas in
0.71.0, averaged 21.4 and 36%. Every particular stays. One long sentence stays where the length is doing
something. A rerun is a no-op, and `docs/ending-slides.md` is rewritten from the same text.

    python tools/build_slide_rhythm.py
"""
import re
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhbuild
from lhbuild import FX

SLIDES = "Resources/Levels/8 Alamut/Dialog/Fixt Ending Slides.DialogTree"
DOC = Path(__file__).resolve().parent.parent / "docs" / "ending-slides.md"

OPENING = "The Knights Templar came out of the siege with their chapter houses standing and their numbers halved. "
KNELT = "Within the year Lord Javier swore the order to the power he had called his benefactor. "
QUIET = ("The commanderies took their new instructions quietly. Those who objected were reassigned to postings "
         "they did not come back from. ")
DESERT = "Inside a generation the white cross was a thing worn in the desert's service"

TEMPLAR = {
    "900 order templar knelt killer": (
        OPENING + KNELT + "You had worn their cross and you had killed men wearing it. The order never found a "
        "way to put both facts on the same page. " + QUIET + DESERT + ". Your name stayed in the rolls eleven "
        "years. Then it was struck out by a hand nobody signed for."),
    "900 order templar unknelt killer": (
        OPENING + "No benefactor ever came to collect on them. You had killed men who wore the same cross you "
        "did. Then you spared the whole order by talking its creditor into its own death. The rolls have no line "
        "for that. They rebuilt slowly, under their own banners and out of their own treasury. The brothers who "
        "had buried the men you killed argued with the brothers who had read the Alamut dispatches. They argued "
        "for as long as any of them lived, and the order never settled it."),
    "900 order templar high knelt": (
        OPENING + KNELT + "You had stood close enough to Javier to be counted among his own. When he knelt, there "
        "was no record of you being anywhere else. " + QUIET + DESERT + ". The men who carried it there had "
        "trained under you."),
    "900 order templar mid knelt": (
        OPENING + KNELT + "You had carried their banner the length of the war, from the Port District chapter to "
        "the relic vaults at Montserrat. Knights who had trained beside you rose behind you. " + QUIET + DESERT +
        ", carried by men who had learned how to carry it from watching you."),
    "900 order templar knelt": (
        OPENING + KNELT + "You had taken their oath and fought under it. That was all the rolls had to say about "
        "you. " + QUIET + DESERT + ". Nobody ever wrote to ask what you thought of it."),
    "900 order templar unknelt": (
        OPENING + "No benefactor ever came for them. You had taken their oath. Then you talked the thing that "
        "meant to collect on it into its own death, before it ever reached a chapter house. The order rebuilt "
        "slowly, under its own banners and out of its own treasury. For a generation it was poorer than it had "
        "been in two hundred years. No record was ever written of what you spared them. The only men who could "
        "have written it were standing at Alamut, and they did not understand what they had heard."),
}

PACT = "The Knights of Saladin kept the pact of east and west after the west had stopped keeping it. After Alamut they kept it alone. "
SHRINES = ("They held the eastern shrines for two generations against raids the west never heard about. They were "
           "called weak for it by men who had never fought them. ")

SALADIN = {
    "900 order saladin killer": (
        PACT + "You had eaten at their table in the Gate District and you had killed one of their knights. The "
        "order wrote down both without comment, which is their way of closing a matter. " + SHRINES +
        "Guests at their table were told your name, and told it carefully, as part of a longer lesson about "
        "hospitality."),
    "900 order saladin high": (
        PACT + "You had been named a Favored One, the first westerner in living memory given the title. The men "
        "who argued against it were outnumbered, not persuaded. " + SHRINES + "Your name stayed in the recitation "
        "at Alamut long after anybody there could have said what you looked like."),
    "900 order saladin": (
        PACT + "You had been their guest, and you had fought beside them in a season when their own numbers were "
        "thin enough that it mattered. " + SHRINES + "The order kept a short list of westerners who had been worth "
        "the hospitality. You were on it. In sixty years the list did not get any longer."),
}

BATCHES = [TEMPLAR, SALADIN]


def apply_tree(batch):
    z = lhbuild.read(SLIDES)
    for nid, text in batch.items():
        z, n = re.subn(r"(Node ID=" + re.escape(nid) + r"\r\nText=)[^\r\n]*", lambda m: m.group(1) + text, z)
        assert n == 1, nid
    assert z.count("\r\n") == z.count("\n")
    (FX / SLIDES).write_bytes(z.encode("latin-1"))


def apply_doc(batch):
    raw = DOC.read_bytes().decode("utf8")
    nl = "\r\n" if "\r\n" in raw else "\n"
    t = raw.replace(nl, "\n")
    for nid, text in batch.items():
        t, n = re.subn(r"(    node id: " + re.escape(nid) + r"\n\n)(?:[^\n]+\n)+",
                       lambda m: m.group(1) + textwrap.fill(text, 100, break_long_words=False, break_on_hyphens=False) + "\n",
                       t)
        assert n == 1, nid
    DOC.write_bytes(t.replace("\n", nl).encode("utf8"))


def main():
    for batch in BATCHES:
        apply_tree(batch)
        apply_doc(batch)


if __name__ == "__main__":
    main()
