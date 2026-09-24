**Read this first.** Nothing in this release has been played, and neither has 0.14.0, 0.13.0 or
0.12.0 before it. Everything passes the automated gate and `docs/releases.md` records what each
piece was read against. If you would rather wait for a build somebody has walked, wait for
0.15.1.

## Toulouse

The sacked town the titans are camped in, at the north-east corner of act 3. 0.14.0 opened its
biggest piece of cut content -- the ending where the titans are talked into hearing their fugitive
out and the fugitive is talked into walking home. What was left turned out to be repair rather
than restoration, and then the act had room for enrichment.

**Two flags the act reads and never sets.** The prisoners' guard offers a Speech bluff -- *"It's
okay, Iapetus said I could speak with the prisoners"* -- gated on having spoken to Iapetus, and
nothing in the game recorded that you had. Thierry, who speaks for the penned villagers, will
answer the question *"The titans said this town was harboring one of their kind, is that true?"*
-- gated on a flag Lethos activates under a name **one word different** from the flag that
exists, so the question was never offered and three nodes about the farmer who sheltered the
fugitive were unreachable. Both are wired.

**The guard's own bribe.** `40 Mercury SUCCESS` was the act's last unreachable player reply:
Poimaino taking the flask himself instead of having it routed through Mathuo. The reply that
should have reached it carried its own specification in a designer note -- *"Speech greater
than/equal to 50, must have the mercury"* -- and shipped checking for **wine**, pointing at the
failure. It is now gated as its note says and split on Speech the way the bluff above it is.

**And the warning he was written to give.** Crossing the line at the pen turned both titans on
you in silence; *"Stop, you are entering the human pen. If you insist on proceeding I'll have the
pleasure of squashing you"* was fired by nothing.

**Menoetius' own name.** His generator named him `Rhea`. Nothing on the map was called Menoetius,
so the relay that empties Toulouse when the tribe leaves and the alarm that turns the tribe on an
attacker both missed him entirely, while their two `Rhea` entries hit whichever of the two
identically-named titans the engine found first.

**The news that never reached Montaillou.** All three endings fire a cross-map activation at the
Hamlet for a part called `titans are gone`. No part of that name existed there, so the village
the titans were arguing about marching on never learned they had gone. Now the mayor, whose
position rests on a lie about a deal with them, asks *"Gone where, exactly -- home, or down the
valley towards us?"*; Maury takes his flock up to the high pasture with his son, the first thing
he has decided for himself since the spring; and a Templar knight's hand comes off his sword for
the first time in the conversation.

## Then Toulouse learns to read you

Seven hundred and thirty-nine player replies in the act and not one of them asked about a perk,
a spirit, a karma score or the player's sex. Now the Daeva that feeds on souls is discussed with
somebody carrying one; Rhea's history of humans learning to bind spirits gets answered by the
binding, with a different reply for each of the three; the eater of memories meets a necromancer
and steps back from him; Utnapishtim, who drowned the world to be rid of magic, is called the
first Inquisitor by an Inquisitor; the elders' gems can be haggled at Barter 40; Mathuo's
*"...unready..."* is caught at Perception 7; and Tereo, who by his own custom must earn his name,
finally meets a player who has earned one -- a Goblin Champion, or a killer of children.

## And the people nobody could talk to

**Ephebos**, the tribe's child, had one line and no replies. He now repeats Rhea's chain of being
and gets it wrong, intends to be Atlas, and has stopped announcing it because Tereo told him
nobody earns a name by announcing it. Give him the flask of quicksilver and he takes it, and pays
in the only currency a child who is ignored all day has.

**The pen.** The man explains what the night visits are for. The woman describes the thing that
came to the fence wearing her dead neighbour's shape and voice. And the child, whose description
was written and placed nowhere at all, is now in the pen, and has counted the one thing that
matters: *"nobody watches us at all. I have counted it four times."*

**The ogres**, on fifteen days of mutton, sell for a skin of wine what fifteen days of mutton
bought nobody: a deer that walked on two legs when it thought they had gone. They told the
guard-titan. He said ogres cannot count.

## Also

Guard Pablo, who never spawned in the shipped game, stands inside the Temple District gate in
Barcelona with a conversation built from his own written lines, including the only explanation in
the game of how the Church says a tainted citizen is recognised on sight. And a review pass found
three canned-expression paths written by this project that resolve to nothing -- ten gates in La
Calle Perdida, Lord Javier's initiate gate, and Farshad's two "Welcome into the Order of Saladin"
greetings, which have been falling through to the stranger's opening since 0.3.0.

## Installing

Download, unzip, run `Mod Manager.bat`. It installs over any earlier release. The child in the
pen, the spoor in the cul-de-sac, Menoetius' name, Guard Pablo and the Montaillou flag are level
parts: **they need a character who has not yet entered those maps.** Everything else is dialogue
and works on any save.
