# Companions level with you, and say so

For review. Nothing is built.

Thirteen balloon lines, one per companion, fired by the engine's own level-up trigger. Each is one
sentence, because it is a balloon over their head and not a conversation.

---

## Corrected after building it

Two names came off the roster, and the gate was rebuilt, because presence in a map is not consent.

**`CCheckExistenceAction` tests whether an entity of that name is in the current map.** The engine has
no companionship test: `CSetCompanionAction` and `CReleaseCompanionAction` exist and nothing reads
them. Vanilla's own `Is Darsh a Companion` works only because Darsh cannot be in those maps unless he
is following you. Most of this roster can, so 0.72.0 as published grants stats and a line to people
who never joined -- including **Joan of Arc, who is hostile in the Crypt until talked down**, which
made a boss fight harder for no reason.

The gate now reads a per-companion scripting variable written where recruitment actually happens, at
46 sites across 14 trees and 5 maps: **0** never happened, **1** travelled with you, **2** died
without travelling with you, **3** travelled with you and died. The growth branch fires on 1, and
existence is kept only to give the balloon an anchor. The same record is what the ending slides in
[`companion-endings.md`](companion-endings.md) read at the finale.

**Don Quixote is not recruitable.** `Companion=` never names him anywhere in the game. He is the shade
Cervantes' quill conjured, built from `Races/NPCs/Cervantes` and `Characters/NPC/Barcelona/Cervantes`
-- the same race and model as the man.

**Gentle Ben is not a companion either.** A `Cathar Bearform` standing in the Montaillou hamlet with
no dialogue tree. **Fang is**, and stays: the `Cub Companion` can, recruited at the Crossroads by
`hunter scene poly 1`, talking through `Bear Companion.DialogTree`.

All three errors had one cause: the roster was built from a `New Name=` scan, which finds every NPC
the maps name rather than every NPC you can recruit. The authoritative source is `CSetCompanionAction`.

---

## How it fires

`CXRPGAITriggerWhenLevelUp`, attached to the player: *"Action is triggered when the layer part the
AI is attached to levels up."* On each level-up it checks each companion by scripting name, and for
whoever is actually with you it grants the modifier and shows the line. **It has zero uses in the
shipped game**, so the field layout comes from the exe's registration table rather than from a
sibling to clone, and the fallback if it does not fire is `CRepeatTimerTriggerAI`, which runs the
Gate District beggars and the Inquisition pit's whining prisoner.

A companion only gets a grant for levels gained **while they are with you**, which is why a late
joiner does not catch up to an early one.

---

## The roster, and what the grant does to them

Beatrice is excluded. `Inquisitor Darsh` and `Captain Isabella` recruit themselves from their own
trees but no generator in the game carries their name as a `New Name=`, so their scripting name is
still unresolved and they are not in the table yet.

End states assume an act 1 recruit sees about twenty levels, since the game floors the player at 8
in the Grove and 28 in Alamut.

| companion | scripting name | HP now | AC now | skill now | joins |
|---|---|---|---|---|---|
| Fang | `Fang` | 27 | 50 | melee 45 | Crossroads |
| Bishop Diego | `Bishop Diego` | 35 | 45 | smite 30 | Wilderness |
| Goblin Girl | `Goblin Girl` | 36 | 125 | melee 15 | Goblin Warrens |
| **Fernand Desoto** | `Distressed Sailor` | **36** | 90 | melee 35 | Port District |
| Inquisitor Darsh | `Darsh` | 42 | 70 | smite 30 | the goblin camp |
| Lost Knight | `Lost Knight` | 49 | 80 | melee 50 | thieves' vault |
| Cervantes | `Cervantes` | 60 | 50 | melee 50 | act 1 |
| ~~Don Quixote~~ | -- | 60 | 50 | melee 50 | **not recruitable, removed** |
| Cortes | `Cortes` | 60 | 85 | melee 75 | act 1 |
| War Golem | `Golem` | 67 | 100 | melee 100 | Giants Cave |
| Grace O'Malley | `Grace` | 165 | 190 | melee 110 | English Shrine |
| ~~Gentle Ben~~ | -- | 175 | 180 | melee 62 | **not a companion, removed** |
| Joan of Arc | `Joan of Arc` | 200 | 225 | melee 90 | the Crypt |
| Sir Roger Templeton | `Sir Roger Templeton` | 200 | 200 | melee 90 | English Shrine |
| Knight of Saladin | `Knight of Saladin` | 220 | 215 | melee 200 | Alamut |
| Goblin Grumdjum | `Goblin Grumdjum` | 225 | 200 | melee 35 | Wilderness |

**Option A, uniform: +9 HP, +8 AC, +3 skill per level.** Fernand ends near 216 HP, Cervantes near
240, which is where a late-game ally sits. But Grumdjum joins in the Wilderness and would end near
**390 HP**, and the Knight of Saladin's melee 200 would reach 260.

**Option B, two tiers.** The ones who join weak grow at Option A's rate; the ones who already arrive
at 165 HP or better grow at **+5 HP, +3 AC, +1 skill**. That puts Grumdjum near 315 instead of 390
and leaves Joan and Sir Roger recognisably themselves, while still meaning nobody stops growing.

Option B is the recommendation. Option A is simpler and is one number away if you would rather have
it.

---

## The lines

Animals and the golem get a stage direction rather than speech, the way the wounded assassin's
opening does.

| who | the line |
|---|---|
| Cervantes | I am writing all of this down. Including the parts where I improve. |
| ~~Don Quixote~~ | *unused -- he cannot be recruited* |
| Cortes | Bueno. I am worth more than I was this morning. |
| Joan of Arc | I learn in the fighting. God is a thorough teacher. |
| Sir Roger Templeton | I have not been drilled this hard since my vigil. |
| Goblin Grumdjum | The poets will need a longer verse for me now. |
| Bishop Diego | The Lord sharpens what He intends to use, my child. |
| Inquisitor Darsh | Even an old inquisitor can be taught, young one. |
| Goblin Girl | Ooh! I can do a new thing. Want to see it on something? |
| Knight of Saladin | Salaam. I am less clumsy than the man you met. |
| Fernand Desoto | A sailor learns or a sailor drowns. I have been learning. |
| Grace O'Malley | My blade is sharper for following yours. |
| Lost Knight | Good. The next ones will be easier. |
| War Golem | &lt;The golem's plates reseat themselves, and it holds its weapon differently.&gt; |
| Fang | &lt;Fang's ears go flat, and he circles wider than he used to.&gt; |
| ~~Gentle Ben~~ | *unused -- he is not a companion* |

### Why these and not "I have learned some new skills"

Each one is in the register the tree already uses, checked against their own shipped text rather than
written from the character's reputation:

| who | what the tree sounds like |
|---|---|
| Grumdjum | *"tales of bloodshed that goblin poets will sing of for years to come"*, and he threatens to make *"an epic poem about your long torture"*. He is sardonic and literary, not a broken-speech goblin, which is what I had assumed before reading him |
| Goblin Girl | *"You're cute for a... whatever it is you are."* Bubbly, and alarming about food |
| Sir Roger | *"My Lord, as I've said, my sword is yours"*. He addresses you by rank and gender, so the line avoids the address rather than needing two variants |
| Knight of Saladin | opens every greeting *"Salaam."* |
| Bishop Diego | *"Go with the holy spirit, my child."* |
| Joan of Arc | *"It is the will of a higher power that this place remains unspoiled."* Certainty, no ornament |
| Cortes | *"Good to see you again. What can I do for you?"* Plain and transactional |
| Cervantes | he is the one who keeps seeing *"La bestia!"*, and Don Quixote is the one who calls him a madman. The comic pair stays a comic pair |
| Fernand Desoto | his vanilla lines are a man shouting for help for his brother. Plain, no flourish |
| Inquisitor Darsh | *"You disappoint me, young one."* An imperious senior inquisitor who calls you young one and offers to conceal you with magic |
| Grace O'Malley | *"My heart and my sword are yours!"*, *"My love, know that my blade and..."*, and a `&lt;Spits in disgust&gt;` at the druids. Ardent, martial, and she can join for love or for duty, so the line has to read for both |

### Two names resolved while checking the voices

**`Darsh`, not `Inquisitor Darsh`.** He is spawned by `Darsh Generator` in `Lake.zax` and
`Mongol Camp.zax` from a can spelled `Inquisitor Darsch`, under the scripting name `Darsh`. And
vanilla already does the exact check this release needs: seven maps carry a part commented
**`Is Darsh a Companion`** over a `CCheckExistenceAction{Name To Check For=Darsh}`. So the
"is this companion actually with you" test is not a new idea, it is the shipped one.

**Captain Isabella is not a companion.** Her tree hosts *Grace's* England scenes -- `502 arrive in
england grace friendly`, `502 grace joined romantic`, `502 grace companion near death` and the rest
of the 5xx block -- which is why her tree carries four `CSetCompanionAction`s and why Grace has no
tree of her own. Grace's scripting name is `Grace`, from `01 Outside Shrine.zax`.
