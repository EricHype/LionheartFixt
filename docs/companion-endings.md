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

**That half is built.** Commit `e7e228b` carries one scripting variable per companion, written where
recruitment actually happens: **14 variables, 14 canned guarded writes, 46 call sites** across 14
trees and 5 maps. Every write is guarded on `== 0`, so a dismiss-and-rejoin cycle cannot double it.

| value | means | written by |
|---|---|---|
| **0** | never happened | nothing |
| **1** | travelled with you | recruitment, `+1` |
| **2** | died without ever travelling with you | death, `+2` -- **not built yet** |
| **3** | travelled with you and died in your service | both |

The growth branch now fires on **1**, and existence survives only to give the balloon an anchor. The
slides below read the same variable at the finale, from a different map, on a save made before any of
it existed. Don Quixote and Gentle Ben came off the roster in that commit.

**Death, the `+2`, is what is still missing**, and it is 0.47.0's pattern: the companion can's own
`Destroyed Script Action`, the hook that carries the four faction-killer titles across 33 cans and
568 spawn points. It is not uniformly available, and I checked before relying on it:

| can | slot | so |
|---|---|---|
| `Joan of Arc.can`, `Cub Companion.can` | **empty, unoverridden** | the hook goes straight in. Joan killed in the Crypt is cleanly detectable, which is the whole of the state you asked about |
| `Cervantes.can` | **already holds a `CIfAction`** | the hook has to extend what is there rather than fill an empty field |
| Grumdjum, Bishop Diego | **overridden at runtime** | `01 Desert Sprawl.zax`, `Lake.zax` and `Plains.zax` all call `CSetDestroyedScriptActionAction` on them, pointing at existing `Grumdjum Dead` and `Diego Dead` checkers. A can-level hook would be silently replaced the moment the player enters those maps, which is exactly how the Lava Troll Hide was dead code from 0.10.0. Their write goes inside the existing override payload |

Those two already track the death locally. It just cannot be read from the finale, which is the whole
reason this needs character-resident state.

### Where a "didn't travel with you" slide gets its gate

Quest history, which `ending-slides.md` already permits and which reads from any map on an old save.
Eight of the fourteen have a footprint of their own:

| companion | the lever |
|---|---|
| **Joan of Arc** | `Release the Doomed Knights from their Torment` -- `CRY1KNGT`, `CRY2CURS`, `CRY3LAMP`. The knights were cursed into undeath by a Saracen's wish and the lamp of Jah'roosh grants one, so you can free them without her ever joining |
| **Bishop Diego** | `Bring the Dark Inquisitors to Justice` against **`Slay Bishop Diego for the Dark Inquisitors`** -- `AS4T5BB5` is *"now that Bishop Diego is dead"*. You can be hired to kill him |
| **Darsh** | `SZLH5UEU` tell Raphael that Darsh died, against `TTX37U4V` escorted home |
| **The Lost Knight** | `OZUYGYAV` *"met an unfortunate end in the sewers"* against `50CZ48GZ` found and escorted back |
| **Fernand Desoto** | `VMS91BAX` *"his brother perished"* against `JUA1LIVE` *"his brother lives"*. His ending turns on Juan, which is right |
| **Grumdjum** | `Slay the River Dryad for the Goblin Grumdjum`, `2QEGR0S8` collect the reward |
| **Cervantes** | the five Bestia states, including `5PV5XAHX` imprisoned for what he did to a wall and `QYCL1DO7` died |
| **Cortes** | `Give Cortes a Hand` and `Recover the Hidden Treasure with Cortes` -- **plus the arbitration, which needs one new variable**: the three verdicts set only a Port District checker, and a checker cannot be read at the finale |

The Goblin Girl, Fang, the Golem, Grace, Sir Roger and the Knight of Saladin have no quest footprint,
so for them "didn't travel" means you walked past them, and they get no slide rather than one about
nothing.

**Reviewing:** rewrite any prose freely, this file is the input for the build. Leave the `node id`
lines alone.

---

## Cervantes

### when: travelled with you, survived

    node id: 900 friend cervantes

Miguel de Cervantes went home with his quill and without the beast, and could not have explained
either to anybody who asked. He had kept notes on every road you walked, and the notes outlasted
the hunt by four hundred years. Years later he published a long book about a madman who believed
himself a knight, sold it badly, and was copied everywhere. He never once set a scene in Barcelona
and never wrote down what the quill was. He died in Madrid, in debt, and is buried somewhere
nobody has since managed to find.

### when: died in your service

    node id: 900 friend cervantes dead

Cervantes was buried where he fell with the quill still on him, and whoever went through his
pockets could not read. A bookseller in Valladolid later claimed to have owned a manuscript about
a madman who believed himself a knight, could never produce it, and was not believed. The book was
never written. A Templar inventory of his effects lists four notebooks, a sword he could not have
lifted, and one quill, and values the quill at nothing at all. The beast was still out there, and
nobody else had ever seen it either. His brother collected nothing, there being nothing to
collect.

### when: he died and never travelled with you

    node id: 900 friend cervantes dead alone

Cervantes died in Barcelona with the quill still on him, and no book was written and no beast was
hunted. The quill went into an evidence chest in the Chambers of the Inquisition, entered by a
clerk as a quill, and is presumably there yet. Nobody in Spain has heard of him. Don Quixote de la
Mancha exists in no library anywhere, and the gap it leaves is not shaped like anything, so nobody
has ever noticed that it is missing, and nobody ever will. The beast was never found either, by
him or by anybody who came after him.

### when: you heard him out and left him to it

    node id: 900 friend cervantes alone

You listened to him about the beast and left him to it, which is what the whole Port District had
been doing for a year. He hunted it alone, was arrested for what he did to a wall while hunting it,
and was released once the Templars decided he was harmless rather than heretical. He published
anyway. The book is about a madman who believed himself a knight, and the man who wrote it had been
followed down the street by one, and no reader has ever needed to know that to laugh at it.

---

## Don Quixote has no ending, and cannot have one

He is not a person and he cannot be a companion. `Companion=` never names him anywhere in the game,
and his can is built from `Races/NPCs/Cervantes` and `Characters/NPC/Barcelona/Cervantes` -- the
author's own race and the author's own model, because he is the shade the quill conjured. His tree
argues the other way (*"I am real! Cervantes is the shade!"*), DaVinci settles it, and
`500 convince don quixote` lets you talk him out of existing: *"You're right, I sense that I was not
real, but I hoped I was wrong. There were so many quests I wanted..."*, and then `500 feather`.

He belongs in Cervantes' slides, which is where he now is. **An earlier draft of this file gave him
two of his own**, written from the historical Cervantes rather than from the game's, in which he dies
old in a bed and the author writes a book about him. Both were wrong on the fiction and one of them
was wrong about who exists.

If you want the kill recorded -- you took the shade's word against the author's and killed Cervantes
for him, which `206 cervantes dies` makes reachable -- that needs its own variable, because the
Bestia quest records only that Cervantes died and not who did it. It is the strongest ending in the
file and it is one write site away.

---

## The shade, which is where Don Quixote's fate goes

Fires immediately after whichever Cervantes slide applies, and only if you met him, which is what
the Bestia quest's `1V7S39O7` records: the state in which DaVinci has told you what the quill did.
A slide is one node and text is not composed at runtime, so the shade cannot be a sentence inside
Cervantes' paragraph. It is the next paragraph instead, which is how the faction set already handles
a character who served two orders.

### when: you convinced him he was not real

    node id: 900 shade feather

You told Don Quixote what he was and he believed you, which is the only argument anybody won in
Barcelona that year. He asked whether there had been quests he would not now get to, was told that
there had been, and took it a great deal better than the man who made him would have. A single
feather came down where he had been standing, went along the floor, and out under the door.
Cervantes did not write about it and did not pick the quill up again for eleven years. The book,
when it finally came, is about a man whom nobody had conjured.

### when: you killed him

    node id: 900 shade killed

You killed Don Quixote in front of the man who had made him, and Cervantes watched it without
saying anything and then talked about it for thirty years. There was no body, and they buried
something anyway, in a plot the parish never charged for because the parish never established what
was in it. He had asked only that you address him correctly, and you had, every time, which he
mentioned to Cervantes more than once. He said he was a slayer of dragons. By the end that was
nearly true. Nobody in the Port District ever asked what was in the coffin.

### when: you met him and left it alone

    node id: 900 shade persists

Don Quixote was still at it twenty years later, by which time he had outlasted most of the people
who had found him funny. He kept to the Port District, challenged whatever he was given to
challenge, and was fed by a tavern that had decided he was good for custom and billed the city for
his stool twice. Nobody ever told him what he was, and Cervantes never did either, which may have
been cowardice and may have been the kindest thing either of them managed. He is in the book. He
does not know.

**Two beats of that scene do not currently play.** `Barcelona Coast.zax` opens
`500 convince don quixote`, so you can talk him out of existing, and `500 feather` -- the node that
shows it, *"&lt;As the spirit of Don Quixote fades, a single feather floats for a moment, then blows
away.&gt;"* -- is **unreachable**, so the scene ends on nothing at all. `206 cervantes dies`, **39 KB
recorded**, is the shade thanking you for killing the author, and that is unreachable too. One
`After Action` each, and both belong in the same release as these slides.

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

### when: you judged the dispute for Cortes, and parted there

    node id: 900 friend cortes vindicated

You heard both men out and found for the conquistador, and Shylocke did not get the ship. Cortes
never sailed again regardless, having no crew and one arm and no credit anywhere in Barcelona, but he
kept the ship tied up where he could see it from the tavern and paid harbour fees on it for nine
years. He told the story of the hearing to everybody, and in his telling you are a judge rather than
a stranger who happened to be standing there. Shylocke's version is shorter and he tells it less. Cortes is in the harbour ledgers for nine
years running and in no other record of the city at all.

### when: you judged the dispute for Shylocke

    node id: 900 friend cortes shylocke

You found for the moneylender, and he took the ship inside a fortnight and sold it inside a month.
Cortes said one thing about it at the time -- *"here I thought you would vindicate me"* -- and
nothing afterwards, to you or about you. He drank in La Serpienta Vieja on credit extended out of
pity by a landlord who had heard the story, and he never went back into the desert, and the treasure
is still in the cave. Shylocke, who had been entirely within his rights, did not thank you either. The landlord's
charity outlasted the moneylender's profit on the ship by about six years.

### when: you would not judge it

    node id: 900 friend cortes no verdict

You declined to settle it and the two of them went on arguing, which suited Shylocke, time being the
only thing in the dispute that was working for him. The case was heard eventually by a Templar
magistrate who had no patience for either man and split the difference badly. Cortes kept half a
ship and a debt he could not service. *"I suppose I should not have rested my hopes on a stranger,"*
he had said, and he turned out to be right about that in a way he had not intended. Shylocke
billed him for the magistrate's time as well, and collected.

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

### when: you broke the curse and released her

    node id: 900 friend joan released

Jehanne d'Arc stopped. Two hundred years of holding one gallery ended in a sentence somebody else
worded carefully to an efreet, and she had time to say *Dieu est avec vous* before the rest of it
caught up with her. Her knights went in the same minute, all down the corridor, in no particular
order and without being told to. The Lance stayed where it was. The Spirit Council never explained
itself to anybody, and what was left in that crypt afterwards was ordinary stone, which is the
first thing it had been in two centuries.

### when: she raised the gate and you left her holding it

    node id: 900 friend joan passed

Jehanne raised the gate and let you by, which she had done for nobody in two hundred years, and
then went back to standing exactly where she had been standing. You took the Lance out of the tomb
below her and she did not stop you, having been told by somebody she believed that the Council
wished it so. The Council never spoke to her again and she went on listening for it. She was still
there when the crypt was sealed, nobody ever lifted the curse, and she would not have asked
anybody twice.

### when: you killed her for the Lance

    node id: 900 friend joan killed

You killed Jehanne d'Arc where she stood, with the Council she had trusted for two centuries not
answering, and took the Bleeding Lance off a knight who had been set to guard it and never once
relieved. Her knights fought on until there was nothing left to fight for. The curse was never
lifted, there being nobody left for it to be on. She had told you she was the maiden and the
commander of the army of France, and she had been telling the truth the entire time. The gallery
was quiet afterwards for the first time in two hundred years.

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

### when: you killed him

    node id: 900 friend grumdjum killed

Grumdjum died in the Wilderness at your hands, mid-sentence, which was the one ending he had never
thought to compose. He had been working on the verse for years and reciting it to whoever stopped
walking, and it went with him. Goblins who had heard pieces of it argued about the pieces for a
season and then stopped. The dryad he wanted dead outlived him by a century. He had promised to
make an epic of your long torture, and he had been joking, and he was the only goblin in the Horde
who would have bothered to joke with you.

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

### when: you killed him for the Dark Inquisitors

    node id: 900 friend diego sold

You took the Dark Inquisitors' coin and killed a blind bishop on the south road of the plains,
which took a good deal less doing than they had led you to expect. They paid, and spoke about you
afterwards in the admiring way of people who have found somebody worse than themselves. The stone
room stood empty for six years and then became a shepherds' shelter. He had called you *my child*
at the end of every conversation the two of you ever had, including the last one, which he did not
know was the last one.

### when: you dealt with the cult for him, and parted there

    node id: 900 friend diego defended

You dealt with the Dark Inquisitors on his behalf and went on your way, and Bishop Diego kept his
post and his failing eyes for another decade. He never learned how close the cult had come to
buying his death, because the only man who could have told him was the man who had turned the
offer down. He blessed you by name whenever you came back, having long since no idea what you
looked like. The Inquisition left him there because he was useful and because moving him would
have needed somebody to decide something.

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

### when: you never got him out of the camp

    node id: 900 friend darsh eaten

Darsh was never taken out of the goblin camp, and the goblins did what goblins do. The Warrens
argued for a fortnight afterwards about whether he had been better with the red spice or the grey,
settled on the grey by a narrow margin, and still cite the argument as the time there was
something in the Warrens worth arguing about. The Inquisition recorded him lost in the Wilderness.
Raphael asked after him twice in eleven years and was told nothing, there being nothing anybody
wished to put in writing. The Khan's daughter was not consulted and remembers the whole business
differently.

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

### when: Juan was not saved, and Fernand outlived him

    node id: 900 friend fernand brother lost

Fernand Desoto went back to the water alone, which the dock had expected of him and he had not. He
worked the Barcelona coast for another thirty years, never once went north past the island, never
told a crew why, and was understood by every crew he shipped with. He told the rescue story once,
to a man who asked him twice, and told it accurately, which is how that man knew not to ask a
third time. There is a boat named after you. He bought it cheap and kept it afloat long past its
worth.

### when: you both died, the brother first

    node id: 900 friend fernand dead both

Fernand Desoto died inland, which for a sailor is its own joke and the one he would have made
first, and there was nobody left who would have got it. The brothers are in no parish register in
Barcelona, having been born somewhere that kept none either. A landlord in the Port District held
their account open for two years out of a habit he could not account for, and then closed it. The
island is still there. Nothing on that coast is named for either of them, or for you. The boat he
had meant to buy went to somebody else and sank inside the year.

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

**Gentle Ben and Don Quixote are not companions** and get no slides. Both came off the growth roster
in `e7e228b`; neither was a decision, both were my error.

**Dismissed is still not a fate.** Leaving somebody behind is reversible, so it gets no variant. A
companion who travelled with you at all gets the surviving slide, and death overrides it.

**Firing order.** The faction slides test fate levers before rank tiers. These want to fire after all
of the faction slides, in the order above, which is roughly the order you can meet them.

### Where the draft stands

**43 slides**, against the 27 the factions ship with. 95 to 114 words, mean 102, inside the range the
shipped set holds to.

| who | slides | states |
|---|---|---|
| **Cervantes** | 4 | survived, died with you, died without you, you heard him out and left him to it |
| **the shade** | 3 | you unmade him, you killed him, you left him to it. Fires after whichever Cervantes slide applied |
| **Cortes** | 5 | survived, died with you, and all three verdicts in the Shylocke dispute |
| **Joan of Arc** | 5 | survived, died with you, **released from the curse**, she raised the gate and you left her to it, you killed her for the Lance |
| **Bishop Diego** | 4 | survived, died with you, **sold to the Dark Inquisitors**, you dealt with the cult for him |
| **Fernand Desoto** | 4 | survived with Juan, survived without Juan, died with you, you both died with Juan first |
| **Darsh** | 3 | survived, died with you, **never got out of the camp** |
| **Grumdjum** | 3 | survived, died with you, **you killed him** |
| Sir Roger, the Knight of Saladin, the Lost Knight, the Goblin Girl, Fang, the War Golem | 2 each | survived, died with you |

**Still to write:** the didn't-travel slide for Sir Roger and the Lost Knight, whose quest levers
exist (`OZUYGYAV` against `50CZ48GZ` for the knight) and which I have not reached yet. The Goblin
Girl, Fang, the Golem, the Knight of Saladin and Grace get none, because walking past them says
nothing about either of you.

**Variables still to add**, on top of the four-state record already built:

| | |
|---|---|
| the arbitration verdict | three Cortes slides depend on it, and the verdicts set only a Port District checker |
| whether *you* killed Cervantes for the shade | the Bestia quest records only that he died, not who did it |
| which of the shade's three fates happened | `500 convince don quixote` and the kill are both reachable and neither is recorded |
| Juan | `VMS91BAX` and `JUA1LIVE` already record it, so **no new variable** -- this one is free |

**Voiceover.** As with the faction slides, every node ships flagged for voiceover and a recording can
be dropped in later as `<node id>.ogg` beside the tree.
