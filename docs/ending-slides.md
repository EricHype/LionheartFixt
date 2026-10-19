# The ending slides

Closing paragraphs on the last screen of the game, after Lord Javier's final line and before the
credits. One fires per faction you have standing with; a character who served two hears both, in the
order below.

**Spoken by nobody.** An unnamed, portraitless text box, through the same invisible speaker the
epilogue already uses. Thirteen vanilla trees ship with no name and no portrait, so this is a shipped
form. A voice for these can be anyone's, with no performance to match.

**Length and register are pitched at the Fallout: New Vegas ending slides** -- 95 to 130 words, four
to six sentences, plain past tense, written to be read aloud at a measured pace. Each one states the
outcome, then the mechanism, then a concrete particular, then the long view.

**Each slide covers three things: status, your impact, near future.** The beats take their values
from different places, which is what makes the futures differ:

| beat | reads | why |
|---|---|---|
| **status** -- where the faction stands | the fate levers | the player can actually change this |
| **impact** -- what you did to them | rank, titles, quest history | standing, not institutional fate |
| **near future** -- what became of them | the fate levers | follows from the status |

**A date correction from the last draft.** Every slide previously opened with the faction coming out
of *the Cataclysm*. The Cataclysm is 1192; the game ends at the siege of Barcelona and Alamut, four
centuries later. They now come out of **the siege**, and look back on Alamut.

**Why the future is not fixed.** 0.47.0 wired the four *Enemy of the ...* titles onto 33 member cans
covering 568 spawn points, and the game already shipped levers that change a faction's actual fate
rather than your standing with it. All of them are **perks, rank attributes or quest history, which
live on the character**, so they test from any map and work on a save made before Fixt was installed.
Map flags cannot be used: an existence check is local to its map, which is why vanilla's own
`Player talked way into Ahriman death` needs a checker entity in the endgame map and a
`COtherMapAction` fired from `08 Final Encounter`. A flag for something done in the Wilderness would
never reach a save already past it.

| lever | kind | what it changes |
|---|---|---|
| `Player talked way into Ahriman death` | endgame flag (vanilla) | the Templars are never sworn to Ahriman |
| `Exposer of Calle Perdida` -- *Hero of the Inquisition* | perk | you gave the hidden city to the Inquisition |
| `Ruler of Calle Perdida` -- *Dark Lord of Calle Perdida* | perk | you turned Relican's ring on it yourself |
| `Goblin Traitor` | perk (Fixt) | you handed the Khan's east rock to Butu's heir |
| `Goblin Chum` / `Blooded` / `Champion` | perks (Fixt) | how far you rose in the Horde |
| the four `FACTION ... Killer` titles | perks (0.47.0) | you killed that faction's own |
| `Slay Goblins for the Savage Heart` | quest history | you took Raylark's contract |
| `Slay the Bounty Hunter for the Khan` | quest history | you killed Raylark for the Khan |

**Firing order matters.** Within a faction the fate levers are tested **before** the rank tiers, so a
betrayer never gets the ordinary paragraph. The order written below is the order tested.

**Reviewing:** rewrite any prose freely, this file is the input for the build. Leave the `node id`
lines alone, since the relay picks slides by those ids and a mismatch crashes the ending.

---

## The Knights Templar

Six, because the fealty is conditional and because a Templar can have Templar blood on them.

### when: Templar Rank > 0, Enemy of the Knights Templar, and Javier swore the order

    node id: 900 order templar knelt killer

The Knights Templar came out of the siege with their chapter houses standing and their numbers
halved, and within the year Lord Javier swore the order to the power he had called his benefactor.
You had worn their cross and you had killed men wearing it, and the order never found a way to put
both facts on the same page. The commanderies took their new instructions quietly. Those who objected
were reassigned to postings they did not come back from, and inside a generation the white cross was
a thing worn in the desert's service. Your name stayed in the rolls eleven years, and was then struck
out by a hand nobody signed for.

### when: Templar Rank > 0, Enemy of the Knights Templar, and you talked Ahriman into dying

    node id: 900 order templar unknelt killer

The Knights Templar came out of the siege with their chapter houses standing and their numbers
halved, and no benefactor ever came to collect on them. You had killed men who wore the same cross
you did, and then you spared the whole order by talking its creditor into its own death, which is not
a thing the rolls have a line for. They rebuilt slowly, under their own banners and out of their own
treasury. The brothers who had buried the men you killed argued with the brothers who had read the
Alamut dispatches, and they argued for as long as any of them lived, and the order never settled it.

### when: Templar Rank > 2, and Javier swore the order to Ahriman

    node id: 900 order templar high knelt

The Knights Templar came out of the siege with their chapter houses standing and their numbers
halved, and within the year Lord Javier swore the order to the power he had called his benefactor.
You had stood close enough to Javier to be counted among his own, and when he knelt there was no
record of you being anywhere else. The commanderies took their new instructions quietly. Those who
objected were reassigned to postings they did not come back from, and inside a generation the white
cross was a thing worn in the desert's service. The men who carried it there had trained under you.

### when: Templar Rank > 1, and Javier swore the order to Ahriman

    node id: 900 order templar mid knelt

The Knights Templar came out of the siege with their chapter houses standing and their numbers
halved, and within the year Lord Javier swore the order to the power he had called his benefactor.
You had carried their banner the length of the war, from the Port District chapter to the relic
vaults at Montserrat, and knights who had trained beside you rose behind you. The commanderies took
their new instructions quietly, and those who objected were reassigned to postings they did not come
back from. Inside a generation the white cross was a thing worn in the desert's service, carried by
men who had learned how to carry it from watching you.

### when: Templar Rank > 0, and Javier swore the order to Ahriman

    node id: 900 order templar knelt

The Knights Templar came out of the siege with their chapter houses standing and their numbers
halved, and within the year Lord Javier swore the order to the power he had called his benefactor.
You had taken their oath and fought under it, and that was the whole of what the rolls had to say
about you. The commanderies took their new instructions quietly. Those who objected were reassigned
to postings they did not come back from, and inside a generation the white cross was a thing worn in
the desert's service. Nobody ever wrote to ask what you thought of it.

### when: Templar Rank > 0, and you talked Ahriman into dying, so Javier never swore

    node id: 900 order templar unknelt

The Knights Templar came out of the siege with their chapter houses standing and their numbers
halved, and no benefactor ever came for them. You had taken their oath, and you had talked the thing
that meant to collect on it into its own death before it ever reached a chapter house. The order
rebuilt slowly, under its own banners and out of its own treasury, and for a generation it was poorer
than it had been in two hundred years. No record was ever written of what you spared them, because
the only men who could have written it were standing at Alamut and did not understand what they had
heard.

---

## The Inquisition

### when: Exposer of Calle Perdida (with or without rank)

    node id: 900 order inquisition exposer

The Inquisition came out of the siege with the most intact command structure left in Barcelona, and
the city handed it the rebuilding. Part of that standing was your doing. You walked into the Temple
District and told them where La Calle Perdida was, and your directions were good, because you had
been inside it as a friend. The Holy Office took the quarter apart over nine days and spent thirty
years cataloguing what it found there. The men who did the work were promoted on the strength of your
word, the pyres were lit in the plaza where the markets had been, and the cities paid for the wood.

### when: Inquisition Rank > 0 and Enemy of the Inquisition

    node id: 900 order inquisition killer

The Inquisition came out of the siege with the most intact command structure left in Barcelona, and
the city handed it the rebuilding. You had worn its mark and you had killed its own, and the Holy
Office is an organisation that keeps careful records of a name entered twice. Its fires burned on
through the peace exactly as they had burned through the war, because a frightened city asks its
inquisitors for more work rather than less, and the cities paid for the wood without being asked
twice. Nothing was ever formally charged against you. But there were four towns between Barcelona and
the coast that you never entered again, and you knew all four names.

### when: Inquisition Rank > 2

    node id: 900 order inquisition high

The Inquisition came out of the siege with the most intact command structure left in Barcelona, and
the city handed it the rebuilding. You had risen high in the Holy Office, high enough that the work
reached you as paper rather than as duty, and high enough to sign what other men then carried out.
Its fires burned on through the peace exactly as they had burned through the war, because a
frightened city asks its inquisitors for more work rather than less. The cities paid for the wood.
Your signature was on enough of it that the archive eventually gave you a box of your own.

### when: Inquisition Rank > 0

    node id: 900 order inquisition

The Inquisition came out of the siege with the most intact command structure left in Barcelona, and
the city handed it the rebuilding. You had worn its mark and done its work, and for a few years
afterward the mark was worth a good deal more than the work had been. It opened doors in the new
Barcelona, and then it went on opening doors you had stopped wanting to walk through. Its fires
burned on through the peace exactly as they had burned through the war, and the cities paid for the
wood. You stopped wearing the mark somewhere in the third year, and nobody ever came to ask you why.

---

## The Order of Saladin

### when: Saladin Rank > 0 and Knight of Saladin Slayer

    node id: 900 order saladin killer

The Knights of Saladin kept the pact of east and west after the west had stopped keeping it, and
after Alamut they kept it alone. You had eaten at their table in the Gate District and you had killed
one of their knights, and the order wrote down both of those without comment, which is their way of
closing a matter. They held the eastern shrines for two generations against raids the west never
heard about, and were called weak for it by men who had never fought them. Guests at their table were
told your name, and told it carefully, as part of a longer lesson about hospitality.

### when: Saladin Rank > 2

    node id: 900 order saladin high

The Knights of Saladin kept the pact of east and west after the west had stopped keeping it, and
after Alamut they kept it alone. You had been named a Favored One, the first westerner in living
memory given the title, and the men who argued against it were outnumbered rather than persuaded.
They held the eastern shrines for two generations against raids the west never heard about, and were
called weak for it by men who had never fought them. Your name stayed in the recitation at Alamut
long after anybody there could have said what you looked like.

### when: Saladin Rank > 0

    node id: 900 order saladin

The Knights of Saladin kept the pact of east and west after the west had stopped keeping it, and
after Alamut they kept it alone. You had been their guest, and you had fought beside them in a season
when their own numbers were thin enough that it mattered. They held the eastern shrines for two
generations against raids the west never heard about, and were called weak for it by men who had
never fought them. The order kept a short list of westerners who had been worth the hospitality. You
were on it, and in sixty years the list did not get any longer.

---

## The Wielders

Three fates, not one. The city survives, is raided, or is destroyed by your own hand.

### when: Ruler of Calle Perdida (you turned Relican's ring on the city)

    node id: 900 order wielder ring

La Calle Perdida was never found, because by the end of that year there was nothing left of it to
find. You put on Relican's ring and turned it on the hidden city yourself, and the few who walked out
gave you the only title that fit, which was Dark Lord of a place that no longer existed. What the
Church had spent three hundred years failing to drown, you buried in an afternoon. The Tome of
Geomancy went down with it, the Five Ways crystals were never gathered again, and nobody taught any
of it in the open, then or afterward.

### when: Exposer of Calle Perdida (with or without Wielder rank)

    node id: 900 order wielder exposed

La Calle Perdida was found, and it was found because you told the Inquisition where to look. You had
been inside as a friend first, which is the only reason your directions were good enough to act on.
The Holy Office took the quarter apart over nine days, and what the Wielders had kept hidden for a
century was catalogued, carted out and burned in the open. Cedric's library went in the third load. A
handful got away through the sewers and taught what they could remember to people who did not
understand what they were being given, and inside two generations it was gone.

### when: Wielder Rank > 0 and Enemy of the Wielders

    node id: 900 order wielder killer

La Calle Perdida was never found, not by the Inquisition and not by the knights. You had walked its
streets as a friend and left Wielder dead behind you, and in a city that small both of those were
known before you reached the gate. The magic the Church had tried to drown went on under the streets
without you, and was taught in the open again long after everyone who had hidden it was dead. The
door you had been given was not opened a second time. They never hunted you for it, which was its own
kind of answer.

### when: Wielder Rank > 2

    node id: 900 order wielder high

La Calle Perdida was never found, not by the Inquisition and not by the knights, and after the siege
it took in more of Barcelona's unwanted than it had room for. You had risen high among the Wielders,
a scion of Richard's line who chose the sorcerers over the cross, and that choice was argued over in
both houses for a century. The magic the Church had tried to drown went on breathing under the
streets, and was taught in the open again long after everyone who had hidden it was dead. When it
was, the first teachers cited you, and got the details wrong.

### when: Wielder Rank > 0

    node id: 900 order wielder

La Calle Perdida was never found, not by the Inquisition and not by the knights, and after the siege
it took in more of Barcelona's unwanted than it had room for. You had walked the hidden city as a
friend, and the Wielders put your name somewhere the Inquisition's archive was never going to reach
it. The magic the Church had tried to drown went on breathing under the streets, and was taught in
the open again long after everyone who had hidden it was dead. You were welcome there for the rest of
your life. You went back twice.

---

## The Goblin Horde

### when: Goblin Traitor

    node id: 900 order horde traitor

The goblin tribes came down out of the mountains, counted themselves, and discovered that they had
two claimants and one rock. You handed the Khan's east rock to Butu's heir, and you were paid for it,
and the Horde has a word for that and the word is not Champion. What might have been a war against
the border towns was a war inside Khara'Khorum instead. It ran three generations and ended with
fewer goblins than it started with. They remembered you accurately, which was the worst of it: of all
the names that came out of that war, yours was the one they taught to children.

### when: Goblin Champion

    node id: 900 order horde high

The goblin tribes came down out of the mountains, counted themselves, and found that they were many,
and that nothing in the west was counting at all. You had been their Champion, and when the banner
went up your name was stitched beside the Khan's on it, in a script you could not read. A Khan's
banner rose again inside three generations. The border towns burned first, then the valley forts, and
the chronicles of the west recorded the whole thing as a surprise. In Khara'Khorum it had been
expected for ninety years, and they were still telling the story with your name in it.

### when: Goblin Blooded

    node id: 900 order horde mid

The goblin tribes came down out of the mountains, counted themselves, and found that they were many,
and that nothing in the west was counting at all. You had been blooded among them, which is further
than almost any outsider gets, and the tribes argued for years afterward about what exactly that had
made you. A Khan's banner rose again inside three generations. The border towns burned first, and the
chronicles of the west recorded it as a surprise. Your name came up in their arguments about the
succession, and was voted down, and came up again.

### when: Goblin Chum

    node id: 900 order horde

The goblin tribes came down out of the mountains, counted themselves, and found that they were many,
and that nothing in the west was counting at all. You had been a chum of the Horde, which in their
mouths means useful rather than trusted, and they kept the word for as long as any of them remembered
you. A Khan's banner rose again inside three generations. The border towns burned first, and the
chronicles of the west recorded it as a surprise. Two trade paths through the mountains stayed open
that entire time, and nobody ever wrote down why.

---

## The Savage Heart

The mercenary company Raylark hunts for. Joining is quest history rather than a rank, so it is
testable from the ending and survives on an old save.

### when: you took Raylark's contract, then killed him for the Khan

    node id: 900 order savage heart betrayed

The Savage Heart came out of the war the way mercenary companies do, which is richer and with a
shorter roster, and one of the names on the short side was Raylark's. You took his contract, and then
you took the Khan's, and you carried the Everlasting into Khara'Khorum to prove you had earned it.
The company does not avenge its dead, it prices them, and the price it set on you was entered in the
books at Marseilles and never once collected. In the years after Alamut the Savage Heart turned away
more work than it could staff. None of it was ever yours, and that was the whole of its revenge.

### when: you took Raylark's contract

    node id: 900 order savage heart

The Savage Heart came out of the war the way mercenary companies do, which is richer and with a
shorter roster. You took Raylark's contract and killed goblins for the bounty, counted by the ear,
and the company's books still carry the entry under your name. In the years after Alamut half of
Europe wanted men who would do that sort of work and not ask after the paperwork, and the Savage
Heart raised its rate twice in five years. Raylark kept his camp west of Khara'Khorum until he was
too old to hold it. The Horde had learned to count western killers by name, and yours was one of the
names.

---

## No allegiance

### when: no rank, and none of the fate levers

    node id: 900 order none

Every order came out of the siege smaller than it had gone in, and every one of them claimed the
ending as its own. You had taken no oath and worn no mark, and there was no faction anywhere that
could produce a document with your name on it. The Templars wrote that a knight had finished it. The
Inquisition wrote that a faithful servant had. The Wielders wrote that one of their own had, and the
Horde told it as a story about a westerner who had owed them a favour. All four accounts survive in
the archives, and not one of them is true.

---

## England

Not one of the five orders, but a faction Fixt gave the player real dealings with, and it already has
its own title perks.

### when: Servant of the Queen

    node id: 900 order england

England spent that year waiting on Barcelona, and in the end the Armada never had to sail into a city
that was already burning. You had carried the Crown's business through the Port District while the
fleet was still in harbour, inside a conspiracy that would have hanged you in any week of it. Guy
Fawkes' promise was kept the way such promises are kept: a pension paid out of an account with
another man's name on it, a quiet word in two ports, and no record anywhere of the reason for either.
He was hanged for something else, years later, and said nothing about you.

### when: Grace's Regard

    node id: 900 order omalley

Grace O'Malley kept her ships, her harbour and her true name, and the Crown learned none of the three
from you. You had been given more than her silence to hold, at a point where selling it would have
cost you nothing and paid well. She was still taking prizes off the Irish coast twenty years after
Barcelona, under the name she had chosen rather than the one she was born to. Her crews told the
Barcelona story the entire time, with you in it, and told it badly, and she never once corrected them.

---

Recording one later: save it as `<node id>.ogg` beside the tree and it plays. Every node ships
flagged for voiceover already, so nothing in the mod has to change.
