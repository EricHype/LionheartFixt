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

The Goblin Girl, Fang, the Golem, Sir Roger and the Knight of Saladin have no quest footprint, so for
them "didn't travel" means you walked past them, and they get no slide rather than one about
nothing. Grace is the exception in the other direction: her Barcelona choice already has a slide, and
what it lacked was the case where she dies with you.

**Reviewing:** rewrite any prose freely, this file is the input for the build. Leave the `node id`
lines alone.

---

## Cervantes

### when: travelled with you, survived

    node id: 900 friend cervantes

Miguel de Cervantes went home with DaVinci's quill and without the beast. He could explain neither.
Years later he finished his long book about a madman who believed himself a knight. It sold badly
and was copied everywhere. Near the end he sent the madman to Barcelona to be beaten. He never wrote
down what the quill was. He died in Madrid, in debt, and his grave was lost for four hundred years.

### when: died in your service

    node id: 900 friend cervantes dead

Cervantes was buried where he fell, with the quill still on him. Whoever went through his pockets
could not read. A bookseller in Valladolid later claimed to own a manuscript about a madman who
believed himself a knight. He could never produce it. The book was never finished. A Templar
inventory of his effects lists four notebooks, a sword and one quill. It values the quill at
nothing. Nobody else ever saw the beast.

### when: he died and never travelled with you

    node id: 900 friend cervantes dead alone

Cervantes died in Barcelona with the quill still on him. His novel was never finished and the beast
was never slain. The quill went into an evidence chest in the Chambers of the Inquisition. A clerk
entered it as a quill, and it is presumably there yet. Nobody in Spain has heard of him. Don Quixote
de la Mancha exists in no library anywhere. The gap has no shape, so nobody has ever noticed it.

### when: you heard him out and left him to it

    node id: 900 friend cervantes alone

You listened to him about the beast and left him to it, as everybody else had. He hunted it alone.
The Knights Templar arrested him for attacking city property. They released him once they decided he
was harmless. He published anyway. The book is about a madman who believed himself a knight. Its
author had once offered you the post of squire. No reader has ever needed to know that to laugh at
it.

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
Barcelona that year. He asked whether there had been quests he would not now get to. He was told
that there had been, and took it a great deal better than the man who made him would have. A single
feather came down where he had been standing, went along the floor, and out under the door.
Cervantes did not write about it and did not pick the quill up again for eleven years. The book,
when it finally came, is about a man whom nobody had conjured.

### when: you killed him

    node id: 900 shade killed

You killed Don Quixote in front of the man who had made him. Cervantes watched it without saying
anything, and then talked about it for thirty years. There was no body, and they buried something
anyway. The plot was never charged for, because the parish never established what was in it. He had
asked only that you address him correctly. You had, every time, which he mentioned to Cervantes more
than once. He said he was a slayer of dragons. By the end that was nearly true. Nobody in the Port
District ever asked what was in the coffin.

### when: you met him and left it alone

    node id: 900 shade persists

Don Quixote was still at it twenty years later, by which time he had outlasted most of the people
who had found him funny. He kept to the Port District and challenged whatever he was given to
challenge. He was fed by a tavern that had decided he was good for custom and billed the city for
his stool twice. Nobody ever told him what he was. Cervantes never did either, which may have been
cowardice and may have been the kindest thing either of them managed. He is in the book. He does not
know.

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

Cortes came out of the cave with a mechanical arm and a share of a treasure. He paid Shylocke in
full in front of witnesses. He burned the note himself. The arm wanted a smith twice a year. He paid
that too, and never asked DaVinci for a discount. His next expedition stayed in preparation for the
rest of his life. He talked about the cave instead, and the river before it.

### when: died in your service

    node id: 900 friend cortes dead

Cortes died with DaVinci's arm still on him, and the arm was what came home. A Templar sergeant
carried it back to Barcelona because it was obviously worth something. DaVinci took it apart on his
bench and did not rebuild it. He kept the hand in a drawer and showed it to visitors for years. He
told the story wrong every time. The debt was never paid. Only you now knew where the cave was.

### when: you judged the dispute for Cortes, and parted there

    node id: 900 friend cortes vindicated

You heard both men out and found for the conquistador. Shylocke did not get the ship. Cortes never
sailed again regardless. He had no crew, one arm and no credit anywhere in Barcelona. He kept the
ship tied up in sight of the tavern, and paid harbour fees for nine years. He told the story of the
hearing to everybody. In his telling you were a judge, not a stranger.

### when: you judged the dispute for Shylocke

    node id: 900 friend cortes shylocke

You found for the moneylender. He took the ship inside a fortnight and sold it inside a month.
Cortes said, "And here I thought you would vindicate me." After that he had nothing to say to you.
He drank in La Serpienta Vieja, on credit a landlord extended out of pity. He never reached the
cave, and the treasure is still in it. Shylocke returned the favour with a cheaper loan.

### when: you would not judge it

    node id: 900 friend cortes no verdict

You declined to settle it. Shylocke said he would take the matter to the magistrates, and he did.
They had no patience for either man and split the difference badly. Cortes kept half a ship and a
debt he could not service. "I suppose I should not have rested my hopes on a stranger," he had said.
Shylocke billed him for the magistrates' time as well, and collected.

---

## Joan of Arc

### when: travelled with you, survived

    node id: 900 friend joan

Jehanne d'Arc left the Crypt of the Bleeding Lance after two hundred years and went back to France.
She was still a corpse, and she did not hide it. Soldiers followed her anyway, for a while. She had
been burned by a court at Rouen, so she kept clear of courts. The Council stayed silent. She asked
after you once, as the crusader. Nobody in France could say who that was.

### when: died in your service

    node id: 900 friend joan dead

Jehanne d'Arc died in your service, after two hundred years of holding one gallery. This time no
wish kept her standing. The Templars never recorded who carried the Bleeding Lance after her. People
remembered her as the maid, the commander, the witch or the saint, whatever the year required. A
chapel outside Orleans carried her name within a century. The men who built it could not have named
the relic she had guarded.

### when: you broke the curse and released her

    node id: 900 friend joan released

Jehanne d'Arc stopped. Two hundred years of holding one gallery ended in a wish you worded to an
efreet. She thanked you and passed the guarding of the relic into your keeping. Then she went to the
place beyond. The souls of her knights were freed by the same wish. The Spirit Council never
explained itself to anybody. What was left in that crypt afterwards was ordinary stone, for the
first time in two centuries.

### when: she raised the gate and you left her holding it

    node id: 900 friend joan passed

You learned of the curse on Jehanne d'Arc, and you left it. She went on standing where she had stood
for two hundred years. The Council never spoke to her again, and she went on listening for it. Her
knights stayed in that crypt with her. She was still there when the crypt was sealed. Nobody came
back to lift it.

### when: you killed her for the Lance

    node id: 900 friend joan killed

You killed Jehanne d'Arc in her own crypt, with her Council not answering. She had helped crown a
King of France and had won at Orleans. She had held that gallery for two hundred years. The Bleeding
Lance lay sealed in a tomb below her, and you went down for it. Her Council had called her their
Pious Child. Nobody was left to call her anything. The gallery was quiet afterwards.

---

## Sir Roger Templeton

### when: travelled with you, survived

    node id: 900 friend roger

Sir Roger Templeton went back to an England whose Queen still kept druids. His order had gone to the
Shrine without her leave, and it was told off for that. He went on calling you Lionheart long after
you had left. The Shrine was sealed by men he had argued into doing it. He is in the order's rolls
as having died in Spain. He found that funny and never corrected it.

### when: died in your service

    node id: 900 friend roger dead

Sir Roger Templeton died in the field, with his sword still yours. The men who sealed the Shrine
afterwards had never met him. They sealed it on general principle. His order had gone there without
the Queen's leave, so the Queen sent no word. His sword went to a nephew who sold it. The entry
beside his name in the order's rolls reads "abroad". That was the whole of what the order knew.

### when: you met him at the Shrine and left him there

    node id: 900 friend roger alone

Sir Roger Templeton told you it was an honor to meet you and offered you his sword. You went into
the Shrine without him. He went home with the men he had brought. The order wrote the business up as
a success, though the Cross was gone. He was given a garrison in Kent. It was the duty that goes to
men owed something and trusted with nothing. He told nobody you had refused him.

---

## Goblin Grumdjum

### when: travelled with you, survived

    node id: 900 friend grumdjum

Grumdjum got his verse. He delivered it at length, in a hall full of goblins who had never seen
Alamut. It was accurate about the fighting and ruinous about everything else. The meter was a bit
off. You are in it as the dark knight. He outlived three Khans by being the only goblin anyone
wanted to hear. Goblin children still recite the Alamut stanza, badly. In it he eats the Old Man's
brain.

### when: died in your service

    node id: 900 friend grumdjum dead

Grumdjum went to the stewpot beyond before his verse was finished. The lines he had already made
were remembered correctly for about ten years. Then they merged with four other poems about four
other goblins. The composite hero is braver than Grumdjum and much less funny. Nobody who recites it
knows you are in it. The hall he would have used was still standing eighty years later. It was never
used for poetry again.

### when: you killed him

    node id: 900 friend grumdjum killed

Grumdjum died in the Wilderness at your hands, with his new poem unfinished. His own guards had
called hearing it a misfortune. Goblins who knew pieces of it argued about the pieces for a season,
and then stopped. He had been the clever one, by the Khan's own account. Bloodspiller the Pensive
and Bonecrusher the Pedantic lost their last reader. Nobody finished the poem, and no goblin asked
anybody to.

---

## Bishop Diego

### when: travelled with you, survived

    node id: 900 friend diego

Bishop Diego's eyes went entirely inside two years, and he kept working. He was given a reader and a
boy to lead him, and he outlasted both posts. He heard confession in a stone room on the plains. He
got more out of voices than he had ever got out of faces. The Inquisition left him there, because
moving him needed a decision. He called everyone "my child" to the last, at about ninety.

### when: died in your service

    node id: 900 friend diego dead

Bishop Diego died on the plains, with his eyes most of the way gone. He had gone out with you
knowing how little he could see. His post stood unfilled for six years. Shepherds buried him under a
cairn and kept adding to it. Nobody local could say what the old man had been doing there. They knew
only that he had called them "my child", and had meant it.

### when: you killed him for the Dark Inquisitors

    node id: 900 friend diego sold

You took the Dark Inquisitors' commission and killed Bishop Diego near the south road of the plains.
His eyes were not so good, so it cannot have been hard. They paid you in a few items, then let you
buy from their cache. They spoke of you afterwards in the admiring way of people who have found
somebody worse than themselves. Nobody came to fill his post. He had called you "my child".

### when: you dealt with the cult for him, and parted there

    node id: 900 friend diego defended

You dealt with the Dark Inquisitors on his behalf and went on your way. Bishop Diego kept his post
and his failing eyes for another decade. He had told you faith would guide you, and afterwards he
gave it the credit. He blessed you whenever you came back. He no longer knew what you looked like.
The Inquisition left him there, since moving him needed somebody to decide something.

---

## Inquisitor Darsh

### when: travelled with you, survived

    node id: 900 friend darsh

Inquisitor Darsh reported to the Grand Inquisitor and wrote his rescue up as a tactical withdrawal.
He was promoted on it. The goblins had held him for days and taken an ear. His report mentioned a
young one who was present. He ran the Wilderness chapter for eleven years. He concealed more
heretics than he burned, and never said why. He was buried in the chapter house with full honours,
the withdrawal cited by name.

### when: died in your service

    node id: 900 friend darsh dead

Inquisitor Darsh died on the way home to Barcelona. He had been a prisoner for days, and he was an
ear short when you found him. He had wanted every goblin in the village dead, and he did not live to
see it. The Inquisition recorded a tragic ending to a loyal Inquisitor. Nobody senior asked how he
had got out. The part you did went unrecorded, in an archive that recorded everything.

### when: you never got him out of the camp

    node id: 900 friend darsh eaten

Inquisitor Darsh never left the goblin village. The goblins had sent Barcelona his severed ear with
a ransom note, and the Inquisition did not bargain. Then the goblins did what goblins do. The camp
argued for a fortnight over the red spice and the grey. The grey won by a narrow margin. The
Inquisition recorded a tragic ending to a loyal Inquisitor. The Khan's daughter was not consulted,
and she remembers it differently.

---

## The Goblin Girl

### when: travelled with you, survived

    node id: 900 friend goblin girl

The Khan's daughter never left the Warrens. She followed you to the way out and would not go past
it. Her momma called you a no-account loser and kept saying so. She grew into something the Horde
had no word for, and it turned out to suit her. She kept a running count of everything she had eaten
and recited it to strangers. She watched that cave mouth longer than she admitted. Momma noticed.

### when: died in your service

    node id: 900 friend goblin girl dead

The Khan's daughter died in the Warrens, behind you, in company her momma had warned her about. The
Khan wanted a name, and a goblin who had been there gave him yours. He did nothing about it, for
reasons political rather than paternal. Her momma took no satisfaction in being right. The first
thing she ever asked you was what you were. Nobody could tell her.

---

## The Knight of Saladin

### when: travelled with you, survived

    node id: 900 friend saladin knight

The Knight of Saladin reported to his order, at length and accurately. He was not entirely believed
about the Old Man. He spent the rest of his service training men for fortresses like Alamut. There
would be another, he reasoned. He opened every greeting with Salaam, and his students copied it
without understanding why. Your name went into his report, spelled three different ways in the same
paragraph.

### when: died in your service

    node id: 900 friend saladin knight dead

The Knight of Saladin died at Alamut. He had offered you his service in the first minute of knowing
you, and he kept the offer. His report was never written. What lay inside the fortress stayed a
rumour in the east for two generations. Then people stopped discussing it at all. The men he would
have trained were trained by somebody else, less well. His order learned where he fell, and very
little else.

---

## Fernand Desoto

### when: travelled with you, survived

    node id: 900 friend fernand

Fernand Desoto went back to the water. He had agreed to follow you for a short time, to repay a
debt. He and Juan worked the Barcelona coast for thirty more years and never went north past the
island. He told every crew how Juan was saved. In his version he did rather more and you did rather
less. Juan corrected him every time. He named a small boat after you, and it leaked.

### when: died in your service

    node id: 900 friend fernand dead

Fernand Desoto died ashore, following you to repay a debt. Juan heard three weeks later, from a man
who had the details wrong. He worked the coast alone after that. He told the rescue story once a
year, accurately. Fernand had told him twice not to fish off the island alone. No boat was named
after you. Juan could not afford one, and he kept his brother's name on the licence.

### when: Juan was not saved, and Fernand outlived him

    node id: 900 friend fernand brother lost

Fernand Desoto went back to the water alone. He had thanked you for trying, and he had asked how he
could ever face his father again. He worked the coast for thirty more years and never went north
past the island. He told the story once, to a man who asked him twice. That man did not ask a third
time. He named a boat after you, and kept it afloat long past its worth.

### when: you both died, the brother first

    node id: 900 friend fernand dead both

Fernand Desoto died ashore, and Juan was already dead. He had been the eldest of the Desoto family.
He had asked how he could ever face his father again, and in the end he never had to. Their father
asked after them at the docks for two years. Then he stopped. The island stayed where it was.
Nothing on that coast was named for either son, or for you.

## Grace O'Malley

She is the one companion who already has a slide, and it is wrong in one case.

`900 order omalley` fires on the `Graces Regard` perk, which is granted in **Barcelona** and then
checked as a `CHasPerkExpression` on her recruitment reply in England. It records what you did about
her secret, not whether she lived. So it says *"she was still taking prizes off the English coast
twenty years after Barcelona"* even when she joined you and died in Alamut, which is 0.71.0's own
work contradicted by this roster.

**The fix is a gate, not a rewrite.** `900 order omalley` keeps firing on the perk, with
`Fixt Companion Grace != 3` added, and the slide below takes the case it was never written for.

### when: she sailed with you and died doing it

    node id: 900 friend grace dead

Grace O'Malley died on land, with Ireland already under the sea. She had spent two years being
Captain Isabella to bring Spain against England. You had spared her in Barcelona, and she drifted
ashore in England when the Armada went down. A cousin took what was left of her ships and renamed
them. No Irish survivor was told where she had gone. Her crews stopped telling the story, for want
of an ending.

---

## Fang

### when: travelled with you, survived

    node id: 900 friend fang

Fang grew. At the Crossroads he had been a runt, barely worth an arrow by the hunter's own count. In
later years strangers crossed the road for him. He outlived most of the party. Hunters stopped
working the woods around the Crossroads for a decade, and gave reasons that got taller every year. A
Templar's report called him the beast, trained, in the company of the Scion. It was the only pelt
anyone got.

### when: died in your service

    node id: 900 friend fang dead

Fang died a cub, in a fight he had no business being in. Nobody asked him. The hunters were back
around the Crossroads inside two years. Nobody wrote him down. A hunter had once told him to his
face what his pelt would fetch. You had got in the way of that. He got more time than the man meant
to give him, and a death he would not have chosen.

---

## The War Golem

### when: travelled with you, survived

    node id: 900 friend golem

The golem stopped. It had been built in England to break a line. Its last campaign was spent walking
behind you. You said follow or stay, and it answered in the same few noises. It stopped in a cave in
the giants' country, upright, facing the way you had gone. Two centuries later a shepherd found it
and took the arm for scrap. His family kept a shoulder plate as a doorstep for sixty years.

### when: died in your service

    node id: 900 friend golem dead

The golem was broken in your service. It had been built in England to break a line, and it went down
in yours. What was left was an empty suit of armor, badly damaged, buzzing a little. The English
sent others like it up the streets of Barcelona. Nobody could have told this one from them. There
was nobody to ask, and nothing left in it that could have answered.

---

## The Lost Knight

### when: travelled with you, survived

    node id: 900 friend lost knight

The Lost Knight got out of the sewers, and you were the only reason he did. He told Auric his
brothers had sent help, and Auric let it stand. He served twenty more years and never spoke of the
thieves without calling them accursed. He never told a junior how he came to be lying in their vault
with his head open.

### when: died in your service

    node id: 900 friend lost knight dead

The Lost Knight died under Barcelona after all. He had been sure his brothers were coming. Auric had
sent nobody but you. The order wrote him down as missing, and the thieves kept the vault another
eleven years. He had told you he expected a more seasoned knight. Auric prayed for him every year,
from a list, among nineteen other names.

### when: you killed him

    node id: 900 friend lost knight killed

You killed a Templar in a thieves' vault, then told Sir Auric he had met an unfortunate end in the
sewers. It was true, as far as it went. Auric wrote it up as a patrol lost underground and stopped
sending patrols. The thieves kept the vault another eleven years. The knight had been certain his
brothers were coming. Auric prayed for him every year, from a list, among nineteen other names.

### when: you walked him out and he went back to work

    node id: 900 friend lost knight returned

The Lost Knight went back to his duties. That was his phrase for it, and all the thanks you got. He
told the order his brothers had come for him, because that was what he had been sure of underground.
Auric had sent one stranger, and did not correct him. He served twenty more years and never said how
he came to be lying in a vault with his head open.

---

## Open

**Grace O'Malley already had one, and it was not enough.** `900 order omalley` fires on a perk
granted in Barcelona and asserts she outlived the campaign, so it is false whenever she dies as your
companion. She now has a death slide and the old one needs `Fixt Companion Grace != 3` on its gate.

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
| **Grace O'Malley** | 1 + 1 shipped | `900 order omalley` already covers her Barcelona choice; the new one is **died with you**, which that slide contradicts |
| **The Lost Knight** | 4 | survived, died with you, **you killed him and reported it to Auric**, you walked him out and he returned to duty |
| **Sir Roger Templeton** | 3 | survived, died with you, you left him at the Shrine |
| the Knight of Saladin, the Goblin Girl, Fang, the War Golem | 2 each | survived, died with you |

**Nothing is outstanding in the prose.** Every companion with a non-companion state worth stating
now has one, and the six without a quest footprint get none on purpose. The Goblin
Girl, Fang, the Golem and the Knight of Saladin get none, because walking past them says nothing
about either of you.

**Variables still to add**, on top of the four-state record already built:

| | |
|---|---|
| the arbitration verdict | three Cortes slides depend on it, and the verdicts set only a Port District checker |
| whether *you* killed Cervantes for the shade | the Bestia quest records only that he died, not who did it |
| which of the shade's three fates happened | `500 convince don quixote` and the kill are both reachable and neither is recorded |
| Juan | `VMS91BAX` and `JUA1LIVE` already record it, so **no new variable** -- this one is free |
| Grace's gate | no new variable either: `900 order omalley` takes `Fixt Companion Grace != 3`, which the gate fix already built |

**Voiceover.** As with the faction slides, every node ships flagged for voiceover and a recording can
be dropped in later as `<node id>.ogg` beside the tree.
