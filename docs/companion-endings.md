# Companion ending slides

For review. Nothing is built.

Twenty-eight slides, two per companion, in the register of the 27 faction slides already shipping in
[`ending-slides.md`](ending-slides.md): 95 to 130 words, four to six sentences, plain past tense,
outcome then mechanism then a concrete particular then the long view.

---

## The gap

The ending slides cover **factions and one person**. Six Templar variants, four Inquisition, three
Saladin, five Wielder, four Horde, two Savage Heart, one for no allegiance, one for England, and
`900 order omalley` for Grace O'Malley, who is there because her fate turns on a choice you make.

Nobody you recruited gets an ending. Vanilla closes the loop on **DaVinci** and **Galileo** (233 and
225 references in `08 Final Encounter.zax`) and on no one else. As of 0.72.0 the mod gives you
companions who grow with you for twenty levels and then vanish at the credits, which is a sharper
hole than it was before.

It is also restoration rather than invention. The designers wrote companion partings and nobody can
reach them: `don quixote / 206 cervantes dies`, `cervantes / 400 companion leave cervantes` and its
alternate, `400 cervantes nearly dead as companion`, `cortes / 800 cortes companion returned`,
`800 cortes leaves alternate`, `800 cortes companion return`, `230 wait to leave`. All recorded, all
silent.

---

## The mechanism, and a defect it has to fix on the way

`ending-slides.md` states the rule that decides the design: **map flags cannot be used**, because an
existence check is local to its map. Every lever the 27 existing slides read is a perk, a rank or
quest history, living on the character, so it tests from any map and works on an older save.

So each companion needs a character-resident record, and finding that out exposed something wrong in
what 0.72.0 shipped this morning.

**`CCheckExistenceAction` tests presence in the current map, not companionship.** There is no
companionship test in the engine at all: `CSetCompanionAction` and `CReleaseCompanionAction` exist and
nothing reads them, and the only Companion or Party classes in the exe are
`CCompanionFollowMessage`, `CCompanionManagerAI`, `CPartyMojo` and `CPartySize`. Vanilla's own
`Is Darsh a Companion` works only because Darsh cannot be in those maps unless he is following you.

Most of the growth roster can:

| who | stands in | consequence today |
|---|---|---|
| **Joan of Arc** | the Crypt, **hostile until talked down** | levelling in her map grants her +5 HP and +3 AC and balloons a line. It makes a boss fight harder for no reason |
| Cervantes, Don Quixote, Cortes | the Port District tavern | they grow and speak before you ever recruit them |
| Grumdjum, Bishop Diego | the Wilderness | same |
| Goblin Girl | the Goblin Warrens | same |
| Darsh | the goblin camp, before the rescue | same |
| Fernand Desoto | the Port District | same |
| Grace, Sir Roger | the English Shrine | same |
| Knight of Saladin, Lost Knight, Fang, War Golem | Alamut, the vault, the Crossroads, the Giants Cave | same |
| **Gentle Ben** | the Montaillou hamlet | **he is not a companion at all.** A `Cathar Bearform` with no dialogue tree and nothing setting him as one. He went on the roster from a name scan and must come off it |

**One piece of infrastructure fixes both.** A scripting variable per companion, set on the recruitment
reply, exactly as `Fixt Companion Growth Watch` is set:

* the growth branch gates on the variable **and** existence, so presence stops meaning consent and
  the balloon still has an anchor
* the ending slide reads the variable at the finale, from a different map, on a save made before any
  of this existed

**Death** uses 0.47.0's proven pattern: the companion can's own empty `Destroyed Script Action`, the
hook that carries the four faction-killer titles across 33 cans and 568 spawn points.

That is the 34-reply surgery I avoided on 20 October by installing the watcher from the companion
overlay's tree. It is now justified twice over, and it is the only part of this that is engineering
rather than writing.

**Reviewing:** rewrite any prose freely, this file is the input for the build. Leave the `node id`
lines alone.

---

## Cervantes

### when: travelled with you, survived

    node id: 900 friend cervantes

Miguel de Cervantes went back to Spain with four notebooks and no money, which was how he had
arrived. He had kept notes on every road you walked and on the beast nobody but him ever saw, and
the notes outlasted the beast. Years later he published a long book about a madman who believed
himself a knight, sold it badly, and was copied everywhere. He never once set a scene in Barcelona.
The thing in the dark that he could never make you turn and look at appears in chapter eight, and it
is a windmill.

### when: died in your service

    node id: 900 friend cervantes dead

Cervantes was buried where he fell with the notebooks still on him, and whoever went through his
pockets could not read. He had been writing the whole way without telling you what it was for. A
bookseller in Valladolid later claimed to have owned a manuscript about a madman who believed himself
a knight, could never produce it, and was not believed. *Don Quixote de la Mancha* was never written.
The joke he had been building for a year, about the beast and the windmill, died with the only man
who knew the punchline. The notebooks went into a fire that winter, by a soldier who wanted the
heat and could not have told you whose they were.

---

## Don Quixote

### when: travelled with you, survived

    node id: 900 friend quixote

Don Quixote went on calling himself a Spanish knight and a slayer of dragons, and after Alamut nobody
in the party was inclined to correct him. He had charged things that were not there and twice charged
things that were, and the second kind did him less harm than the first. He died old, in a bed, of
nothing in particular. Cervantes was at the funeral and had the better part of a book about him
written inside the year, in which he is defeated by farm machinery and is entirely right about
everything else.

### when: died in your service

    node id: 900 friend quixote dead

Don Quixote died charging something, which is the only ending he would have accepted and close to the
one he had described in advance. The thing he charged was real, which he never got the satisfaction
of knowing. Cervantes wrote him down anyway and gave him a windmill instead and let him lose to it.
He had asked nothing of you but that you address him correctly, and you had, which he mentioned to
Cervantes more than once and at length. Readers took the joke for four hundred years and missed what
the author knew: the man had been right once, at the end, in a desert, and it had cost him
everything.

---

## Cortes

### when: travelled with you, survived

    node id: 900 friend cortes

Cortes came out of the desert with a mechanical arm, a share of a treasure, and the first clear
accounts of his life. He paid Shylocke in full in front of witnesses and asked for the note back so
he could burn it himself. The arm wanted a smith twice a year and he paid that too, out of the share,
and never once asked DaVinci for a discount. He talked about the cave for the rest of his life, and
about the river before it, and about the arm, and never mentioned the debt to anybody who had not
already heard about it from Shylocke.

### when: died in your service

    node id: 900 friend cortes dead

Cortes died with DaVinci's arm still on him, and it was the arm that came home. A Templar sergeant
carried it back to Barcelona because it was obviously worth something, and DaVinci took it apart on
the bench where he had built it and did not rebuild it. He kept the hand in a drawer and showed it to
visitors for years, and told the story of it wrong every time. The debt was never paid and never pursued,
Shylocke being a man who kept accounts and also kept score. The treasure stayed where it was. Nobody
else in Barcelona knew where the cave was, because Cortes had told only you.

---

## Joan of Arc

### when: travelled with you, survived

    node id: 900 friend joan

Jehanne d'Arc left the Crypt of the Bleeding Lance for the first time in nine years and did not look
back at it. She had been set there to guard a relic and had guarded it well past the point where
anyone was coming to relieve her. In France she was given soldiers, briefly, and then given to a
court, and the court was told what she had been doing in a crypt in Spain and did not believe that
either. She was certain the entire time. She asked after you once, by rank, and was told that nobody
of that name had ever been knighted.

### when: died in your service

    node id: 900 friend joan dead

Jehanne d'Arc died away from the Crypt she had held for nine years, which she would have counted as
the worse of the two losses. The Bleeding Lance went to whoever reached the chamber next and the
Templars did not record who. Her certainty was the thing people remembered and the thing they got
wrong: it had never been about France, she had said so plainly, and France was written into it
anyway. A chapel outside Orleans carried her name within a century, built by men who could not have
named the relic she died for.

---

## Sir Roger Templeton

### when: travelled with you, survived

    node id: 900 friend roger

Sir Roger Templeton went back to an England that had changed sides while he was out of it, and spent
his remaining service explaining to Templars younger than himself that the druids had once fought
beside them. He was believed by about half. He kept the habit of addressing people by rank, including
you, including long after it had stopped being accurate. The Shrine was sealed, properly this time,
by men he had personally argued into doing it. He is in the order's rolls as having died in Spain,
which he found funny and never corrected.

### when: died in your service

    node id: 900 friend roger dead

Sir Roger Templeton died in the field, and the order's rolls got it right by accident, having
already recorded him dead in Spain once. The men who sealed the Shrine afterwards had never heard his
argument about the druids and sealed it on general principle instead. England stopped being a place
that remembered the alliance inside a generation, there being nobody left who had been told to argue
about it. His sword went to a nephew who sold it. The entry beside his name reads *abroad*, which is
the whole of what the order knew.

---

## Goblin Grumdjum

### when: travelled with you, survived

    node id: 900 friend grumdjum

Grumdjum got his verse. He had been threatening you with poetry for a year and he delivered, at
length, in a hall full of goblins who had never been further east than the pass. The poem is accurate
about the fighting and ruinous about everything else, and you are in it under a name he invented and
would not explain. He outlived three Khans by the simple method of being the only goblin anyone
wanted to hear from. Goblin children still recite the Alamut stanza, badly, and the stanza is wrong about Alamut. He
dictated the last third of it, being by then far too grand to write.

### when: died in your service

    node id: 900 friend grumdjum dead

Grumdjum died before he could finish it, which he would have called the single worst outcome
available. The verses he had already made were remembered correctly for about ten years and then
merged with four other poems about four other goblins. The composite hero is braver than Grumdjum and
much less funny. Nobody who recites it knows that the best line in it, about a brave crusader who
threatened to vanquish a knave, was written about you by a goblin who had decided he liked you and never once said so out loud.
The hall he would have recited it in was still standing eighty years later and was never used for
poetry again.

---

## Bishop Diego

### when: travelled with you, survived

    node id: 900 friend diego

Bishop Diego's eyes went entirely inside two years and he kept working. He was given a reader and a
boy to lead him and he outlasted both posts, hearing confession in a stone room in the Wilderness and
getting more out of voices than he had ever got out of faces. He blessed you by name at the end of
every conversation, including the ones in which you had told him nothing. The Inquisition left him
there because he was useful and because moving him would have required somebody to make a decision.
He called you *my child* to the last, being about ninety.

### when: died in your service

    node id: 900 friend diego dead

Bishop Diego died in the Wilderness with his eyes most of the way gone, and his post stood unfilled
for six years afterwards, the Inquisition having no record of anyone ever being assigned to it. He had
gone out with you knowing exactly how little he could see. The stone room became a shepherds' shelter
and then a ruin. Nobody local could say what the old blind man had been doing there, only that he had been there a long time, and had called everyone *my child*, and had meant it. He
had asked to be buried where he fell and was, under a cairn the shepherds kept adding to.

---

## Inquisitor Darsh

### when: travelled with you, survived

    node id: 900 friend darsh

Inquisitor Darsh wrote his own rescue up as a tactical withdrawal and was promoted on it. He had been
in a goblin camp long enough to be written off and came out with his magic and most of his dignity
intact, and he never once used the word rescue in your hearing. His report mentions a young one who
was present. He ran the Wilderness chapter for eleven years, concealed considerably more heretics than he burned, for reasons he took to the grave, and would
have been appalled to hear it put that way. He was buried in the chapter house with full honours,
the withdrawal cited by name.

### when: died in your service

    node id: 900 friend darsh dead

Inquisitor Darsh died out of the camp, and that was the most that could be said for it. The
Inquisition recorded him lost in the Wilderness, which was accurate, complete, and about a tenth of
the story. Nobody senior enough to be curious ever asked how he had got out of the goblin camp in the
first place, so the part you did goes unrecorded in an archive that records everything. The last thing
he said to you he had been saying to everyone for forty years, in exactly that tone: *you disappoint
me, young one.*

---

## The Goblin Girl

### when: travelled with you, survived

    node id: 900 friend goblin girl

The Khan's daughter left the Warrens with you and did not come back, which cost her father a daughter
and a bargaining chip and a quantity of face. Her mother was proved right about you at a volume
audible from the pass. She grew into something the Horde had no word for, being neither Khan's blood
in the Warrens nor anything at all anywhere else, and it turned out to suit her. She kept a running
count of everything she had eaten on the road and recited it to strangers. Nobody who met her later
believed she had been a Khan's daughter, and she never minded.

### when: died in your service

    node id: 900 friend goblin girl dead

The Khan's daughter died away from the Warrens, in company her mother had warned her about, and the
Horde took it the way a Horde takes such things. The Khan wanted a name. He was given yours,
eventually, by a goblin who had been there, and he did nothing about it for reasons that were
political rather than paternal. Her mother was right twice and took no satisfaction in it either
time. She had asked you once whether there were more of you and whether they were all so cute, and
had been told, and had not believed it.

---

## The Knight of Saladin

### when: travelled with you, survived

    node id: 900 friend saladin knight

The Knight of Saladin rode east from Alamut and reported, at length and accurately, and was not
entirely believed about the Old Man. The order had expected to lose him and had already said the
prayers. He spent the rest of his service training men for a fortress that was no longer there, on
the grounds that the next one would be similar. He greeted everybody with *Salaam*, including men he
was about to fight, and his students copied it without understanding why. Your name is in his report,
spelled three different ways in the same paragraph.

### when: died in your service

    node id: 900 friend saladin knight dead

The Knight of Saladin died inside the fortress he had ridden a thousand miles to enter, and the order
said the prayers it had already said once. His report was never written, so what was in Alamut stayed
a rumour in the east for two generations and then stopped being discussed at all. The men he would
have trained were trained by somebody else, less well. He had told you his sword was yours in the
first minute of knowing you, in the formula his order kept for strangers, and had meant it in a way
the formula does not require.

---

## Fernand Desoto

### when: travelled with you, survived

    node id: 900 friend fernand

Fernand Desoto went back to the water, which surprised everyone who had watched him begging for help
on the dock and nobody who had sailed with him. He and Juan worked the Barcelona coast for another
thirty years and never once went north past the island. He told the story of his brother's rescue to
every crew he ever shipped with, in a version where he did rather more and you did rather less, and
Juan corrected him in front of them every time. He named a boat after you. It was a small boat and it
leaked.

### when: died in your service

    node id: 900 friend fernand dead

Fernand Desoto died inland, which for a sailor is its own joke and one he would have made first. Juan
heard about it in a port three weeks later, from a man who had all the details wrong. He worked the
coast alone after that and stopped going near the island altogether, and told the rescue story exactly
once a year, accurately, which is how everyone who heard it knew he had not made it up. There is no boat named after you. Juan considered it and could not afford a boat, and kept his
brother's name on the licence for the rest of his working life.

---

## Fang

### when: travelled with you, survived

    node id: 900 friend fang

The cub grew. He had come to you small enough to carry and ended the campaign big enough that
strangers crossed the road, and he never learned to be quiet about either. He outlived most of the
party, bears being durable and the Crossroads being a great deal safer than Alamut. Hunters in that
country stopped working the eastern woods for a decade and gave reasons that got taller every year. He
is in Grumdjum's poem, which calls him a demon, and in a Templar's report, which calls him *the
beast, trained, in the company of the Scion*.

### when: died in your service

    node id: 900 friend fang dead

The cub died grown, in a fight he had no business being in and was not asked about. The hunters were
back in the eastern woods inside two years. Nobody wrote him down except Grumdjum, who put him in the
poem as a demon and gave him a stanza he had not earned and would have been pleased by. You had taken
him off a man who was going to sell him. On the balance of it he got years he would not otherwise have
had, and a death he would not have chosen, in that order.

---

## The War Golem

### when: travelled with you, survived

    node id: 900 friend golem

The golem stopped. It had been made in England to break a line and spent its last campaign walking
behind you instead, obeying instructions it gave no sign of understanding. When it finally stopped it
was in a cave in the giants' country, upright, facing the way you had gone. The English makers' marks
on the shoulder plate were still legible two centuries later, when a shepherd found it and took the
arm for scrap. Nobody who saw it move ever agreed on whether it had been alive. It never once indicated a
preference. The shepherd's family used the shoulder plate as a doorstep for sixty years.

### when: died in your service

    node id: 900 friend golem dead

The golem was broken rather than stopped, which may or may not be a distinction. It came apart inside
one piece of work, the way the English had built it to, and what was left would not have been worth a
shepherd's trouble. Its makers were dead, its line was broken, and there was no second one anywhere.
Whatever it had been doing when it chose to follow you, it was the last of its kind to do it, and there was nobody to ask and nothing left in it that
could have answered. The English never built a second, the war having moved on to men.

---

## The Lost Knight

### when: travelled with you, survived

    node id: 900 friend lost knight

The Lost Knight got out of the sewers, which he had been certain of the whole time and had been wrong
about until you arrived. He reported to Auric that his brothers had sent help, which was not what had
happened, and Auric let it stand. He never afterwards referred to the thieves as anything but
accursed, and never explained to anyone junior how he had come to be lying in their vault with his
head open. He was a good knight for twenty more years, on the strength of a rescue he had confidently
predicted and could not possibly have survived without.

### when: died in your service

    node id: 900 friend lost knight dead

The Lost Knight died under Barcelona after all, which was the ending the thieves had arranged for him
before you ever got there. He had been entirely sure his brothers were coming. Auric never learned
whether they had, having sent nobody, and the order recorded him missing, missing being the entry
that required no further action. The thieves kept the vault another eleven years. The last thing he said was that he had expected a more seasoned knight, and he said it as a
compliment he had not yet finished building. Auric prayed for him annually, from a list, among
nineteen other names.

---

## Open

**Grace O'Malley already has one.** `900 order omalley`, gated on her `Grace's Regard` perk. She is
not in this file and does not need a second slide.

**Gentle Ben is not a companion** and gets no slide. He also has to come off the growth roster, which
is a repair rather than a decision.

**Dismissed is not a fate.** Leaving somebody behind is reversible in this game, so there is no third
variant for it. A companion who travelled with you at all gets the surviving slide; death overrides
it. If you would rather dismissal counted as its own ending, that is a third variant each and a
second scripting variable, and I would want to hear the argument before writing fourteen more.

**Firing order.** The faction slides test fate levers before rank tiers. These want to fire after all
of the faction slides, in the order above, which is roughly the order you can meet them.

**Voiceover.** As with the faction slides, every node ships flagged for voiceover and a recording can
be dropped in later as `<node id>.ogg` beside the tree.
