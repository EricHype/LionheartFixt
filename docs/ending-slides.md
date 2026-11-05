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

**Being rewritten to the game's own rhythm, a group at a time.** Vanilla dialogue averages 10.2 words
a sentence, with 3% past 25. These slides averaged 21.4, with 36%. The Inquisition and Dark Inquisitor
slides are done, at about 10 words a sentence and 60 to 100 words a slide. Keep the particulars and
allow one long sentence where it earns its place, because in several slides the length is the joke.

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
halved. Within the year Lord Javier swore the order to the power he had called his benefactor. You
had worn their cross and you had killed men wearing it. The order never found a way to put both
facts on the same page. The commanderies took their new instructions quietly. Those who objected
were reassigned to postings they did not come back from. Inside a generation the white cross was a
thing worn in the desert's service. Your name stayed in the rolls eleven years. Then it was struck
out by a hand nobody signed for.

### when: Templar Rank > 0, Enemy of the Knights Templar, and you talked Ahriman into dying

    node id: 900 order templar unknelt killer

The Knights Templar came out of the siege with their chapter houses standing and their numbers
halved. No benefactor ever came to collect on them. You had killed men who wore the same cross you
did. Then you spared the whole order by talking its creditor into its own death. The rolls have no
line for that. They rebuilt slowly, under their own banners and out of their own treasury. The
brothers who had buried the men you killed argued with the brothers who had read the Alamut
dispatches. They argued for as long as any of them lived, and the order never settled it.

### when: Templar Rank > 2, and Javier swore the order to Ahriman

    node id: 900 order templar high knelt

The Knights Templar came out of the siege with their chapter houses standing and their numbers
halved. Within the year Lord Javier swore the order to the power he had called his benefactor. You
had stood close enough to Javier to be counted among his own. When he knelt, there was no record of
you being anywhere else. The commanderies took their new instructions quietly. Those who objected
were reassigned to postings they did not come back from. Inside a generation the white cross was a
thing worn in the desert's service. The men who carried it there had trained under you.

### when: Templar Rank > 1, and Javier swore the order to Ahriman

    node id: 900 order templar mid knelt

The Knights Templar came out of the siege with their chapter houses standing and their numbers
halved. Within the year Lord Javier swore the order to the power he had called his benefactor. You
had carried their banner the length of the war, from the Port District chapter to the relic vaults
at Montserrat. Knights who had trained beside you rose behind you. The commanderies took their new
instructions quietly. Those who objected were reassigned to postings they did not come back from.
Inside a generation the white cross was a thing worn in the desert's service, carried by men who had
learned how to carry it from watching you.

### when: Templar Rank > 0, and Javier swore the order to Ahriman

    node id: 900 order templar knelt

The Knights Templar came out of the siege with their chapter houses standing and their numbers
halved. Within the year Lord Javier swore the order to the power he had called his benefactor. You
had taken their oath and fought under it. That was all the rolls had to say about you. The
commanderies took their new instructions quietly. Those who objected were reassigned to postings
they did not come back from. Inside a generation the white cross was a thing worn in the desert's
service. Nobody ever wrote to ask what you thought of it.

### when: Templar Rank > 0, and you talked Ahriman into dying, so Javier never swore

    node id: 900 order templar unknelt

The Knights Templar came out of the siege with their chapter houses standing and their numbers
halved. No benefactor ever came for them. You had taken their oath. Then you talked the thing that
meant to collect on it into its own death, before it ever reached a chapter house. The order rebuilt
slowly, under its own banners and out of its own treasury. For a generation it was poorer than it
had been in two hundred years. No record was ever written of what you spared them. The only men who
could have written it were standing at Alamut, and they did not understand what they had heard.

---

## The shield of the order

Shown after the Templar slide, to a Templar who freed the Doomed Knights. Jehanne's own slides cover
what freeing them did for her. This one covers what it did for you.

### when: Templar, knights freed, and Sir Roger gave you the Aegis

    node id: 900 order templar aegis

You forged the Lion Shield as an initiate, and you carried it out of the Crypt with an old cross on
it. Two hundred years of damned knights had gone free to put it there. Sir Roger saw what it was and
took it from you, because a relic is a thing the order lays on tombs. He gave you the Aegis, and you
carried that to the end. The order keeps both now. It tells the story of the second. Nobody there
can tell you who the first one was for.

### when: Templar, and knights freed

    node id: 900 order templar relic

You forged the Lion Shield as an initiate. You carried it out of the Crypt changed, with an old
cross on it and the lion gone faint beneath. Two hundred years of damned knights had gone free to
put it there. No chapter roll records why. When you were gone it went back to the order. They hung
it in a hall, and nobody there could say whose it had been.

---

## The Inquisition

### when: Dark Inquisitor, a member who killed Torquemada

    node id: 900 order inquisition dark

The Inquisition entered the siege without a head. It came out with several. Torquemada died in his
own chambers, and the Holy Office recorded it as a fever. The truth was worse: the hand that killed
him still wore the mark. The cult on the plains had wanted this for years. You did it in an
afternoon. His successors agreed on nothing, and the fires burned low. Within ten years, some cities
stopped paying for the wood. No one ever named you. But the archive keeps a box with nothing written
on it, and its keepers lower their voices.

### when: Breaker of the Hammer, anyone else who killed him

    node id: 900 order inquisition broken

The Inquisition entered the siege without a head. Barcelona would not rebuild under men who could
not say who led them. Torquemada died in his own chambers, at the hand of someone who owed the Holy
Office nothing. You walked out past what was left of his guards. His successors fought over his
chair for years. The fires did not go out, but they burned low. Within ten years, some cities
stopped paying for the wood. No one in those cities knew your name. The Holy Office did. It kept the
page open.

### when: Exposer of Calle Perdida (with or without rank)

    node id: 900 order inquisition exposer

The Inquisition came out of the siege with its command intact, and the city handed it the
rebuilding. Part of that standing was your doing. You told them where La Calle Perdida was, and your
directions were good, because you had been inside it as a friend. The Holy Office took the quarter
apart in nine days. It spent thirty years cataloguing what it found. The men who did the work were
promoted on your word. The pyres were lit in the plaza where the markets had been, and the cities
paid for the wood.

### when: Inquisition Rank > 0 and Enemy of the Inquisition

    node id: 900 order inquisition killer

The Inquisition came out of the siege with its command intact, and the city handed it the
rebuilding. You had worn its mark and you had killed its own. The Holy Office keeps careful records
of a name entered twice. Its fires burned on through the peace as they had through the war, because
a frightened city asks its inquisitors for more work, not less. The cities paid for the wood.
Nothing was ever charged against you. But there were four towns between Barcelona and the coast that
you never entered again, and you knew all four names.

### when: Inquisition Rank > 2

    node id: 900 order inquisition high

The Inquisition came out of the siege with its command intact, and the city handed it the
rebuilding. You had risen high in the Holy Office, high enough that the work reached you as paper.
You signed what other men carried out. Its fires burned on through the peace as they had through the
war, because a frightened city asks its inquisitors for more work, not less. The cities paid for the
wood. Your signature was on enough of it that the archive gave you a box of your own.

### when: Inquisition Rank > 0

    node id: 900 order inquisition

The Inquisition came out of the siege with its command intact, and the city handed it the
rebuilding. You had worn its mark and done its work. For a few years the mark was worth more than
the work had been. It opened doors in the new Barcelona. Then it went on opening doors you no longer
wanted to walk through. Its fires burned on through the peace as they had through the war, and the
cities paid for the wood. You stopped wearing the mark in the third year. Nobody ever asked you why.

---

## The Dark Inquisitors

Shown after the Inquisition slide, to anyone who dealt with the cult, whatever their faction.
A character who did not sees nothing here. Destroyed outranks served.

### when: cult destroyed, and Torquemada dead

    node id: 900 order cult ended dead

You ended the Dark Inquisitors on the plains, and you ended Torquemada in his own chambers. The Holy
Office lost its heretics and its head to the same hand. It could not praise you for the first
without naming you for the second. So it did neither. Both entries were struck from the record. In
the archive, the two pages sit side by side with nothing written on them.

### when: cult destroyed, and reported to Torquemada

    node id: 900 order cult told

The Dark Inquisitors did not survive you. You found them on the northern plains, you ended them, and
you told Torquemada to his face. He paid you and he kept his word. It was never written down. The
Holy Office holds no record of the cult, or the habits, or the men who wore them. Within a
generation you were the last who knew. He had called it rot from inside the house. The house stayed
standing, and nobody ever looked for the rest.

### when: cult destroyed

    node id: 900 order cult ended

The Dark Inquisitors did not survive you. You found them on the northern plains and you ended what
they were doing there. Their habits were burned where they lay. The shepherds brought their flocks
back within the year. Nobody in Barcelona asked what had happened, because nobody in Barcelona
wanted the answer. The Holy Office went on saying that such men had never been its own. You knew
better. You had seen the habits.

### when: killed Diego for them, and Torquemada dead

    node id: 900 order cult inherited

The Dark Inquisitors paid you for Bishop Diego. Nobody paid you for Torquemada, though it was the
job they wanted most. The Holy Office was still fighting over his chair when they came down from the
plains, in good habits, with good letters. There was no honest bishop left to read them. Within a
generation the chair was theirs, and few could have said when it changed. The fires had burned low.
They burned again, and no city was asked to pay for the wood.

### when: killed Diego for them

    node id: 900 order cult served

The Dark Inquisitors paid what they promised. Bishop Diego was dead on the south road, and nobody
was left to write letters about them. They grew. Their habits spread from the northern plains to the
hill towns, and then to parishes that had never heard the name. Within ten years it was hard to say
where the cult stopped and the Holy Office began. Some of them knew your name. They said it the way
the faithful say a saint's.

---

## The Order of Saladin

### when: Saladin Rank > 0 and Knight of Saladin Slayer

    node id: 900 order saladin killer

The Knights of Saladin kept the pact of east and west after the west had stopped keeping it. After
Alamut they kept it alone. You had eaten at their table in the Gate District and you had killed one
of their knights. The order wrote down both without comment, which is their way of closing a matter.
They held the eastern shrines for two generations against raids the west never heard about. They
were called weak for it by men who had never fought them. Guests at their table were told your name,
and told it carefully, as part of a longer lesson about hospitality.

### when: Saladin Rank > 2

    node id: 900 order saladin high

The Knights of Saladin kept the pact of east and west after the west had stopped keeping it. After
Alamut they kept it alone. You had been named a Favored One, the first westerner in living memory
given the title. The men who argued against it were outnumbered, not persuaded. They held the
eastern shrines for two generations against raids the west never heard about. They were called weak
for it by men who had never fought them. Your name stayed in the recitation at Alamut long after
anybody there could have said what you looked like.

### when: Saladin Rank > 0

    node id: 900 order saladin

The Knights of Saladin kept the pact of east and west after the west had stopped keeping it. After
Alamut they kept it alone. You had been their guest, and you had fought beside them in a season when
their own numbers were thin enough that it mattered. They held the eastern shrines for two
generations against raids the west never heard about. They were called weak for it by men who had
never fought them. The order kept a short list of westerners who had been worth the hospitality. You
were on it. In sixty years the list did not get any longer.

---

## The two forks of the Order of Saladin

Shown after the Saladin slide. Amir's second task is the Shard or the Scimitar, and Kabool's trial is
intellect or strength. A member with neither perk sees nothing here.

### when: Shard, intellect

    node id: 900 order saladin shard scholar

You brought the Shard of Dreams out of the slavers' lair and put it in Amir's hands. Then Kabool
offered you the blade or your wits, and you chose your wits. He named you Scholar of the Crescent, a
great honor among the people of the east. The order has told that story for sixty years. It has
never once told it as a fight.

### when: Shard, strength

    node id: 900 order saladin shard dervish

You brought the Shard of Dreams out of the slavers' lair and put it in Amir's hands. Then Kabool
offered you the blade or your wits, and you took the blade. You walked out of the Trial of Dreams
with a Sacred Scimitar, forged in the image of Saladin's own. The order still teaches its novices
how you fought. Few of them ever manage it.

### when: Scimitar, intellect

    node id: 900 order saladin scimitar scholar

Amir offered you a choice of tasks, and you took the sword. Eduardo forged it, you carried it back,
and Amir handed it to you again. Then Kabool offered you the blade or your wits, and you chose your
wits, with the blade at your side the whole time. He named you Scholar of the Crescent. The order
found that very funny. Later it found it wise.

### when: Scimitar, strength

    node id: 900 order saladin scimitar dervish

Amir offered you a choice of tasks, and you took the sword. Eduardo forged it, you carried it back,
and Amir handed it to you again. You took it into the Trial of Dreams and you won. Kabool said a
second blade would be no gift, and he closed his hand around yours. When he opened it the steel was
burning. It did not stop. The order still asks what became of it.

### when: Scimitar, intellect, and the Shard brought back unasked

    node id: 900 order saladin scimitar scholar unasked

Amir offered you a choice of tasks, and you took the sword. Eduardo forged it, you carried it back,
and Amir handed it to you again. Then Kabool offered you the blade or your wits, and you chose your
wits, with the blade at your side the whole time. He named you Scholar of the Crescent. The order
found that very funny. Later it found it wise. You brought him the Shard anyway, and he paid you for
it, because the order does not take a sacred thing as a gift.

### when: Scimitar, strength, and the Shard brought back unasked

    node id: 900 order saladin scimitar dervish unasked

Amir offered you a choice of tasks, and you took the sword. Eduardo forged it, you carried it back,
and Amir handed it to you again. You took it into the Trial of Dreams and you won. Kabool said a
second blade would be no gift, and he closed his hand around yours. When he opened it the steel was
burning. It did not stop. The order still asks what became of it. You brought him the Shard anyway,
and he paid you for it, because the order does not take a sacred thing as a gift.

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
