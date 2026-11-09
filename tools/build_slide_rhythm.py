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
from slide_rhythm_companions import BATCH_1, BATCH_2, BATCH_3

SLIDES = "Resources/Levels/8 Alamut/Dialog/Fixt Ending Slides.DialogTree"
DOCS = [Path(__file__).resolve().parent.parent / "docs" / n for n in ("ending-slides.md", "companion-endings.md")]

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
        OPENING + KNELT + "You had carried their banner the length of the war, from the Cathedral in the Temple District to "
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
        PACT + "You had been a guest in their tents in the Gate District and you had killed one of their knights. The "
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

NEVER = "La Calle Perdida was never found, not by the Inquisition and not by the knights. "
UNWANTED = "After the siege it took in more of Barcelona's unwanted than it had room for. "
DROWN = "The magic the Church had tried to drown went on "
OPEN = "It was taught in the open again long after everyone who had hidden it was dead. "

WIELDER = {
    "900 order wielder ring": (
        "La Calle Perdida was never found, because by the end of that year there was nothing left of it to find. "
        "You put on Relican's ring and turned it on the hidden city yourself. The few who walked out gave you the "
        "only title that fit: Dark Lord of a place that no longer existed. What the Church had spent three hundred "
        "years failing to drown, you buried in an afternoon. Whatever books it still held went down with it. The Five Ways "
        "crystals were never gathered again. Nobody taught any of it in the open, then or afterward."),
    "900 order wielder exposed": (
        "La Calle Perdida was found, and it was found because you told the Inquisition where to look. You had been "
        "inside as a friend first, which is the only reason your directions were good enough. The Holy Office took "
        "the quarter apart in nine days. What the Wielders had kept hidden for a century was catalogued, carted out "
        "and burned in the open. Cedric's own house went in the third load. A handful got away through the sewers. "
        "They taught what they could remember to people who did not understand what they were being given, and "
        "inside two generations it was gone."),
    "900 order wielder killer": (
        NEVER + "You had walked its streets as a friend and left Wielder dead behind you. In a city that small, both "
        "were known before you reached the gate. " + DROWN + "under the streets without you. " + OPEN + "The door you "
        "had been given was not opened a second time. They never hunted you for it, which was its own kind of answer."),
    "900 order wielder high": (
        NEVER + UNWANTED + "You had risen high among the Wielders, a scion of Richard's line who chose the sorcerers "
        "over the cross. That choice was argued over in both houses for a century. " + DROWN + "breathing under the "
        "streets. " + OPEN + "When it was, the first teachers cited you, and got the details wrong."),
    "900 order wielder": (
        NEVER + UNWANTED + "You had walked the hidden city as a friend, and the Wielders put your name somewhere the "
        "Inquisition's archive was never going to reach it. " + DROWN + "breathing under the streets. " + OPEN +
        "You were welcome there for the rest of your life. You went back twice."),
}

COUNTED = "The goblin tribes came down out of the mountains, counted themselves, and found that they were many. Nothing in the west was counting at all. "
BANNER = "A Khan's banner rose again inside three generations. "
BURNED = "The border towns burned first, and the chronicles of the west recorded it as a surprise. "
ROSTER = "The Savage Heart came out of the war the way mercenary companies do, which is richer and with a shorter roster. "

HORDE = {
    "900 order horde traitor": (
        "The goblin tribes came down out of the mountains, counted themselves, and discovered that they had two "
        "claimants and one rock. You handed the Khan's east rock to Butu's heir, and you were paid for it. The Horde "
        "has a word for that, and the word is not Champion. What might have been a war against the border towns was "
        "a war inside Khara'Khorum instead. It ran three generations and ended with fewer goblins than it started "
        "with. They remembered you accurately, which was the worst of it. Of all the names that came out of that "
        "war, yours was the one they taught to children."),
    "900 order horde high": (
        COUNTED + "You had been their Champion, and when the banner went up your name was stitched beside the Khan's "
        "on it, in a script you could not read. " + BANNER + "The border towns burned first, then the valley forts. "
        "The chronicles of the west recorded the whole thing as a surprise. In Khara'Khorum it had been expected for "
        "ninety years, and they were still telling the story with your name in it."),
    "900 order horde mid": (
        COUNTED + "You had been blooded among them, which is further than almost any outsider gets. The tribes argued "
        "for years afterward about what exactly that had made you. " + BANNER + BURNED + "Your name came up in their "
        "arguments about the succession, and was voted down, and came up again."),
    "900 order horde": (
        COUNTED + "You had been a chum of the Horde, which in their mouths means useful rather than trusted. They kept "
        "the word for as long as any of them remembered you. " + BANNER + BURNED + "Two trade paths through the "
        "mountains stayed open that entire time, and nobody ever wrote down why."),
    "900 order savage heart betrayed": (
        ROSTER + "One of the names on the short side was Raylark's. You took his contract, and then you took the "
        "Khan's, and you carried the Everlasting into Khara'Khorum to prove you had earned it. The company does not "
        "avenge its dead. It prices them. The price it set on you was entered in the company's books and never "
        "once collected. In the years after Alamut the Savage Heart turned away more work than it could staff. None "
        "of it was ever yours, and that was the whole of its revenge."),
    "900 order savage heart": (
        ROSTER + "You took Raylark's contract and signed on to hunt goblins for the bounty, counted by the scalp. The company's "
        "books still carry the entry under your name. In the years after Alamut half of Europe wanted men who would "
        "do that sort of work and not ask after the paperwork. The Savage Heart raised its rate twice in five years. "
        "Raylark kept his camp west of Khara'Khorum until he was too old to hold it. The Horde had learned to count "
        "western killers by name, and yours was one of the names."),
}

REMAINDER = {
    "900 order none": (
        "Every order came out of the siege smaller than it had gone in, and every one of them claimed the ending as "
        "its own. You had taken no oath and worn no mark. No faction anywhere could produce a document with your name "
        "on it. The Templars wrote that a knight had finished it. The Inquisition wrote that a faithful servant had. "
        "The Wielders wrote that one of their own had. The Horde told it as a story about a westerner who had owed "
        "them a favour. All four accounts survive in the archives, and not one of them is true."),
    "900 order england": (
        "England spent that year waiting on Barcelona. In the end the Armada never had to sail into a city that was "
        "already burning. You had carried the Crown's business through the Port District while the fleet was still in "
        "harbour. Any week of it would have hanged you. Guy Fawkes' promise was kept the way such promises are kept. "
        "There was a pension paid out of an account with another man's name on it, and a quiet word in two ports. "
        "There was no record anywhere of the reason for either. He was hanged for something else, years "
        "later, and said nothing about you."),
    "900 order omalley": (
        "Grace O'Malley kept her life and her true name. The Crown learned neither from "
        "you. You had been given more than her silence to hold, at a point where selling it would have cost you "
        "nothing and paid well. She was still taking prizes off the English coast twenty years after Barcelona, under "
        "the name she had chosen. Her crews told the Barcelona story the entire time, with you in it. They told it "
        "badly, and she never once corrected them."),
}

BATCHES = [TEMPLAR, SALADIN, WIELDER, HORDE, REMAINDER, BATCH_1, BATCH_2, BATCH_3]


def apply_tree(batch):
    z = lhbuild.read(SLIDES)
    for nid, text in batch.items():
        z, n = re.subn(r"(Node ID=" + re.escape(nid) + r"\r\nText=)[^\r\n]*", lambda m: m.group(1) + text, z)
        assert n == 1, nid
    assert z.count("\r\n") == z.count("\n")
    (FX / SLIDES).write_bytes(z.encode("latin-1"))


def apply_doc(batch):
    for nid, text in batch.items():
        hits = 0
        for doc in DOCS:
            raw = doc.read_bytes().decode("utf8")
            nl = "\r\n" if "\r\n" in raw else "\n"
            t, n = re.subn(r"(    node id: " + re.escape(nid) + r"\n\n)(?:[^\n]+\n)+",
                           lambda m: m.group(1) + textwrap.fill(text, 100, break_long_words=False, break_on_hyphens=False) + "\n",
                           raw.replace(nl, "\n"))
            hits += n
            doc.write_bytes(t.replace("\n", nl).encode("utf8"))
        assert hits == 1, nid


def main():
    for batch in BATCHES:
        apply_tree(batch)
        apply_doc(batch)


if __name__ == "__main__":
    main()
