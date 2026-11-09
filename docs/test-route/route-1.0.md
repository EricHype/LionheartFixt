# The 1.0 test route

Built by `tools/test_route.py` from all 2791 cases in `docs/qa.md`. 2440 still need checking;
183 were replaced by later releases, 79 are duplicates, 43 are automated,
8 were deploy-only probes and 38 are not tests.

Of the 2386 that a new game can reach, 1808 need your eyes, 443 need your eyes plus a save, and
135 are read from a save alone. **NEW** marks 0.99.x work, which has never been played. 54 cases can only
pass on a save from before their release, so they are listed at the end and are not part of a new-game run.

## 1 Barcelona (449)


**Amir**

- [ ] `AM1` (qa.md:2851) step: Talk to Amir, take *"Where are you from?"*, then *"What is this important matter?"* | say: - | expect: His account of the theft from the mosque, and a new option: **"Do you know who is responsible?"**
- [ ] `AM2` (qa.md:2852) step: Take it | say: - | expect: **With voiceover.** *"Unfortunately, we do not know. Our enemy must wield powerful sorcery to overcome the wards we placed around the mosque. We fear that even the Cathedral of Barcelona may be vulnerable to whoever or whatever is targeting the relics."*
- [ ] `AM3` (qa.md:2853) step: **The row that matters.** Click through his answer | say: - | expect: You land back on *"Now, what else would you like to speak about?"* and can carry on. His answer already carried its own way out
- [ ] `AM4` (qa.md:2854) step: Take *"Goodbye"* from his answer instead | say: - | expect: The conversation closes normally
- [ ] `AM5` (qa.md:2855) step: Return to the subject later through the hub | say: - | expect: The option is still there. The route to that node is repeatable, so this is not a one-time question
- [ ] `AM6` (qa.md:2856) step: **Regression.** Take the two replies that were always on that node | say: - | expect: *"I have other questions"* still reaches his hub, *"Goodbye"* still closes

**Barcelona Cathedral crypt**

- [ ] `LE14` (qa.md:6411) where: Same | steps: Go back upstairs, then fight the spirits in the crypt if you have not | pass: Upstairs is the cathedral's own ambience again, so the chant has not followed you. Note what plays in the fight: it should be whatever played before, because Medium and Full were left alone

**Barcelona gate (Guard Tomas)**

- [ ] `DL5` (qa.md:6366) where: New game, wait for Guard Tomas to open the gate, then walk through | steps: Listen | pass: *"Come, let's explore this grand city!"* over DaVinci as he follows you in, once only, then *"Now what did I need from the market again?"* when he arrives. **Judgement:** does it overlap his portcullis line or the market line? Rushing the gate may clip the portcullis line -- *Needs a new game; judgement on overlap.*

**Barcelona quest givers; Templar and Inquisition initiations**

- [ ] `N4` (qa.md:6007) pass: Spot-check Barcelona quest givers, the Templar/Inquisition initiations

**Blacksmith map**

- [ ] `MF9` (qa.md:5074) [eyes + save] step: Take it to Eduardo | say: - | expect: He forges the Sacred Scimitar as normal. Nothing in his chain was touched

**Cathedral**

- [ ] `SA1` (qa.md:2003) step: **The reported row.** As an Inquisition character who completed the Saladin initiation, ask Amir what troubles the order and accept "Of course, I will accompany you" | say: - | expect: The **Saladin** summit plays: Javier welcomes Amir, Amir answers, and it runs to "Leave for Montserrat". Before this it stalled on Javier's welcome
- [ ] `SA2` (qa.md:2004) step: The same as a Templar | say: - | expect: The Saladin summit, not the Templar one
- [ ] `SA3` (qa.md:2005) step: The same as a Wielder | say: - | expect: The Saladin summit, not the Wielder one
- [ ] `SA4` (qa.md:2006) step: **Regression.** Reach the summit by the Inquisition route, with the Inquisitors | say: - | expect: The Inquisition summit, unchanged. Its forcing object is set by `Inquisition Foyer1` and is still tested before the faction fallbacks
- [ ] `SA5` (qa.md:2007) step: **Regression.** Reach it by the Templar route, through Lord Javier | say: - | expect: The Templar summit, unchanged
- [ ] `SA6` (qa.md:2008) step: **Regression.** Reach it as a Wielder or Dark Wielder from Calle Perdida | say: - | expect: Unchanged
- [ ] `SA7` (qa.md:2009) step: **Regression.** Complete the Saladin summit, then return to the Cathedral later | say: - | expect: Nothing re-fires. `End Saladin NIS Relay` switches the forcing object off, which the three shipped routes do not do for theirs

**Cathedral (Church Interior)**

- [ ] `CS1` (qa.md:2753) step: **The row that matters.** Join one order, go through the Cathedral summit, then join a second order and take its chapter-2 briefing | say: - | expect: The briefing plays and the conversation ends normally. **No second trip to the Cathedral**, no empty room, no lost controls
- [ ] `CS2` (qa.md:2754) step: **Regression, and the one that must not break.** On a fresh character, join one order and take its chapter-2 briefing | say: - | expect: The summit runs exactly as before: the cast is present, Javier speaks, you are sent to Montserrat
- [ ] `CS3` (qa.md:2755) step: Load the save attached to issue #10 and talk to the Wielder guildmaster | say: - | expect: No warp to the Cathedral. That save already ran its summit, and the guard detects it from the Montserrat quest in the log rather than from the marker, which it cannot have -- *Needs the issue #10 save, not a new game.*
- [ ] `CS5` (qa.md:2757) step: Same for the **Inquisition** (Raphael) and the **Dark Wielders** (Relican) | say: - | expect: Each order's own scene
- [ ] `CS6` (qa.md:2758) step: **Saladin.** Reach the summit as a Knight of Saladin | say: - | expect: Jafar's Saladin summit, now reached because you hold Saladin rank rather than because every other test failed -- *0.80.1 changed how the Saladin arm is chosen; SA1-SA3 (lines 2003-2005) cover cross-faction cases.*
- [ ] `CS7` (qa.md:2759) [save] step: Check your quest log after the summit | say: - | expect: The Montserrat quest belongs to **your** order. A Wielder should not be carrying `Knights Saladin Initiation/Travel to Montserrat`

**Cathedral (Lord Javier)**

- [ ] `X12` (qa.md:1183) steps: **Character B**, never took the contract | pass: The whole Templar initiation still works exactly as vanilla
- [ ] `TD16` (qa.md:1224) [eyes + save] where: Lord Javier | steps: Ask to become an initiate with **no** sponsorship and no second chance | pass: **`190 need sponsor`** -- *"you'll need a sponsor. Perhaps Sir Auric will do it"* -- and the reply sets the *Seek out Sir Auric* quest
- [ ] `TD17` (qa.md:1225) steps: Same **with** Auric's sponsorship | pass: The old route to `100 auric initiate` still fires, and the no-sponsor reply is absent
- [ ] `TD18` (qa.md:1226) steps: On his Montserrat directions, ask about the Sacred Lance | pass: The lore node plays and its reply still leads to *Leave for Montserrat*
- [ ] `MS34` (qa.md:1309) [eyes + save] where: Javier, after Esteban has died with the Esteban step given and not done | steps: Any greeting | pass: *"Sir Esteban is dead."* -> the weighs-heavy line -> the Auric step given; the reply gone once Seek out Sir Auric exists
- [ ] `MS35` (qa.md:1310) where: Cathedral, fresh map | steps: Attack Javier, wake in the cell, walk back in | pass: About a second after entering, *"If you blaspheme this cathedral again..."* over Javier once; an extra guard beside him on this and every later visit

**DaVinci's secret chamber; Relican**

- [ ] `SB2` (qa.md:2155) [eyes + save] step: **Regression.** The normal order: take the errand, then loot the chamber | say: - | expect: Exactly as 0.39.0 left it. The journal advances on pickup and the same bind reply is offered

**DaVinci's workshop (organ)**

- [ ] `WC22` (qa.md:2527) [eyes + save] step: **The organ gives once, ever.** Play `F A C E`, take the wand, spend every charge, then play it again | say: Read the replies on the drawer node | expect: There is no **Take the wand.** reply the second time, only **Leave the drawer alone.**, whatever you are carrying. The marker is the perk **Leonardo's Gift**, which should appear on the character sheet with no effect. The other four sequences are gone and vanilla's `C, E, C, C, A` still reaches the secret chamber

**Dream Djinni Map**

- [ ] `S1` (qa.md:1028) [eyes + save] where: Dream Djinni, Barcelona | steps: Win the trials by **combat** | pass: `Dervish of the Crescent` awarded **and** the character sheet shows the Aswaran modifiers: +10 One-Handed, +10 Two-Handed, +1 EN, +20 carry
- [ ] `S2` (qa.md:1029) [eyes + save] steps: Win by **wits** instead | pass: `Scholar of the Crescent` awarded, same Aswaran modifiers
- [ ] `S3` (qa.md:1030) [save] steps: Re-trigger the trial reward if possible | pass: Rank does **not** climb past 1. Faction tiers replace rather than stack, and only Aswaran is ever assigned -- *0.23.0 added Blessed and Exalted rungs, so rank 2+ from Jafar or crystals is not a failure.*
- [ ] `S24` (qa.md:1064) [eyes + save] where: Dream Djinni, **carrying a scimitar you forged** | steps: Win the combat trial | pass: He does **not** hand you a second one. He enchants the one you have -- it gains **Flame**, fire damage
- [ ] `S25` (qa.md:1065) steps: Took the **Shard** arm instead, so no forged blade | pass: Vanilla: he hands you a Sacred Scimitar as always
- [ ] `AQ2` (qa.md:1740) step: Fight the zombies in the Dream Djinni Map | say: - | expect: Same, and for the same reason: they count as ranged because they **throw chunks**, `Minimum Attack Distance=350`
- [ ] `GB18` (qa.md:4967) step: A goblin in the **Djinn dream arena** (`Dream Djinni Map`) | say: - | expect: Same profile. `DjinnArenaMonster1` shares the `Goblin Archer` races and is a goblin archer by model -- correct spillover, not a leak

**Eduardo's shop**

- [ ] `LE7` (qa.md:6404) where: **Fresh save.** Attack Eduardo | steps: Get jailed, escape, walk back into the shop | pass: About two seconds in: *"Perhaps now you will think twice about attacking me..."*, voiced, over **his** head. Judge the delay. If he is not standing yet there is no line, and `Delay=2` needs raising -- *Fresh save.*
- [ ] `LE8` (qa.md:6405) where: Same | steps: Leave and come back | pass: Silence. It plays once
- [ ] `LE9` (qa.md:6406) where: **The regression.** Fresh save, never attack him | steps: Enter the shop, buy something, leave, return | pass: No line, customers as normal, greeting unchanged. The spawn point is shared with both of his setup relays

**Ether plane under La Calle Perdida**

- [ ] `MB1` (qa.md:2403) [eyes + save] step: New game. Reach the ether plane under La Calle Perdida and let Marco put his spirit in his boots | say: - | expect: You get Marco Polo's Boots, exactly as in vanilla. Nothing in this release changes how you get them

**Foyer**

- [ ] `HH49` (qa.md:6149) [eyes + save] where: Ran from Torquemada, in the Foyer | steps: - | pass: Raphael is **absent**, not an invincible enemy
- [ ] `HH50` (qa.md:6150) [eyes + save] where: Kill Torquemada, reach Raphael as an Inquisitor | steps: Take the deal | pass: No gold taken. A short fade, he is gone, and the guards are calm
- [ ] `HH51` (qa.md:6151) [save] where: Same, as an outsider with gold | steps: Hand over your purse | pass: **Your gold is exactly 0.** Try an odd amount, this is the only proof of the ladder
- [ ] `HH53` (qa.md:6153) where: Refuse him | steps: - | pass: *"To the hellfire with you, heathen!"* He fights, guards join, and you are not jailed
- [ ] `HH54` (qa.md:6154) [eyes + save] where: Run from that fight and return | steps: - | pass: Still hostile, and no deal is offered
- [ ] `HH55` (qa.md:6155) [save] where: Kill him | steps: Check perks | pass: **Sede Vacante**. He stays dead, and the Inquisition stays hostile

**Foyer, Temple, Gate and Port Districts, Forest Exterior**

- [ ] `HH46` (qa.md:6146) [eyes + save] where: Start the fight with Torquemada and run, new game | steps: Walk through the Foyer, the Temple, Gate and Port Districts, and the Forest Exterior | pass: Named Inquisitors and guards attack on sight. **You are never arrested.** This is the row that proves the release -- *Needs those maps unvisited at fight time, so in practice a new game.*

**Gate District**

- [ ] `EL4` (qa.md:2387) step: New character. Finish the RED FILE guy's quest in the Gate District and open his stock | say: - | expect: **Four** things, not two: Hellfire, Hoarfrost, the Tempest and the Sword of Undead Ice
- [ ] `GB4` (qa.md:2513) step: **Regression.** After the gift, keep walking with him into the city | say: - | expect: He still comments on the portcullis and on the market as he goes. Those two are played straight from his walk, not through the relay, so the fix must not have touched them -- *0.97.1 adds a portcullis bark; DL5 (qa.md 6366) judges overlap.*
- [ ] `GB5` (qa.md:2514) step: **Regression.** Walk up and talk to him | say: - | expect: His return dialogue opens as before, and the faction quest and the opening autosave both still happen
- [ ] `GF10` (qa.md:3087) step: **The row the report is about.** Listen | say: - | expect: *You hear it.* 25 seconds of DaVinci in the male recording, 22 in the female. Silence here means the speaker still is not resolving **PASSED** -- *"it worked"*, 2026-10-13
- [ ] `GF11` (qa.md:3088) step: Watch him while it plays | say: - | expect: He is **still beside you**, on the walk. The scene sits short of the courtyard trigger that releases him, so he should not be strolling or bantering yet **PASSED**
- [ ] `GF15` (qa.md:3092) [eyes + save] step: Dawdle: finish the talk, wander back toward the city gate, then go north later | say: - | expect: The scene still fires when you eventually cross that stretch. The detector stays armed; it is `Trigger Only Once=1`, not time-limited
- [ ] `GF2` (qa.md:3103) step: Same on a **female** character | say: - | expect: *"Signora!"*, and the wording differs through the whole line. The check tests for Male and falls to female, so a wrong gender shows up as a female character hearing *"Signore"*
- [ ] `GF3` (qa.md:3104) [eyes + save] step: Close the scene and open the bag | say: - | expect: The inventory icon flashes, and there is **one more Potion of Healing** than the kit gave you. Two in total
- [ ] `GF4` (qa.md:3105) [save] step: **Regression.** Check the rest of the starting kit | say: - | expect: Unchanged: the weapon or bow the kit rolls for your build, infinite arrows and bolts, and the kit's own single healing potion. The gift relay was added beside that one, not into it
- [ ] `GF5` (qa.md:3106) [save] step: **The one that catches a repeat.** Finish the scene, keep playing, come back and talk to him | say: - | expect: No second gift and no second potion. The relay is `Trigger Only Once=1` and deactivates itself, and nothing in the tree points at the node that fires it
- [ ] `LD3` (qa.md:3874) where: **The approach.** With the task active, talk to DaVinci | steps: - | pass: A `Quest Icon` reply about carrying another man's words -> `800 Fixt Relican Offer`. It must appear from **all five** of his entry nodes: first meeting, the two other first-meeting variants, `3 Return Dialogue`, and `3 Return Dialogue Workshop`
- [ ] `LD4` (qa.md:3875) where: **The row that matters. Refuse him** -- take the ungated *"Relican is offering you power"* reply -> `802` -- then check everything he still does: his shop talk, the Wielder referral to Quinn, and `Build DaVinci's Repeating Crossbow` if you have it | steps: - | pass: **Nothing is withdrawn.** He argues you off the path and takes nothing away. If his crossbow quest breaks or the Quinn referral vanishes, the refusal has teeth it was explicitly not meant to have
- [ ] `LD5` (qa.md:3876) [eyes + save] where: After LD4, talk to him again | steps: - | pass: He does **not** re-offer the conversion; the quest has moved to the refused state. He is cold but functional
- [ ] `LD6` (qa.md:3877) [eyes + save] where: **The ideological route.** At Speech 50 or above, take the reply about the man left in the ether pocket | steps: - | pass: He concedes -> `801 Fixt DaVinci Joins`, journal advances to "return to Relican"
- [ ] `LD7` (qa.md:3878) where: Try LD6 **below** Speech 50 | steps: - | pass: That reply is absent. Only the ungated attempt and the back-out remain
- [ ] `LD8` (qa.md:3879) where: **The arcane route.** With General Thought **or** General Tribal at 80+, take the mastery reply | steps: - | pass: Present and it works. Check **both** disciplines independently -- the gate is a `COR` of vanilla's two 80-threshold cans, so either alone must suffice
- [ ] `LD9` (qa.md:3880) where: **Where 0.39.0 interlocks.** Carrying the **Ring of the Trapped Spirit** from the Enchanter's pact, talk to DaVinci | steps: - | pass: A third route appears -- *"I have been down the well... He wears my bargain now"* -- and succeeds. Without the ring it must be absent
- [ ] `LD10` (qa.md:3881) where: Take the back-out reply (*"Nothing. Forget that I raised it"*) | steps: - | pass: Conversation ends and the quest stays open: the approach reply is offered again next time. **This must be retryable**
- [ ] `DN10` (qa.md:4896) [save] step: Fight or watch **Leonardo da Vinci** take damage -- the Gate District, the workshop, the secret chamber, `01 Hamlet Exterior`, `04 Inn Interior` | say: - | expect: **"Leonardo DaVinci"**, not "River Dryad" -- *0.60.3 found the log prints the can's User Assigned Name, not the race name this release edited. Expected names here came from race names, but 0.60.3 found the log prints the can's User Assigned Name (a hat goblin logs Goblin Striker). A different name is not a failure on its own; check it against the can.*
- [ ] `BS8` (qa.md:5462) step: Compare a `Thug4 Sword` in the Gate District, or `Thug Boss` in act 8 Alamut | say: - | expect: Unchanged -- still 95 AC, no backstab. Thugs share nothing with the new thief races
- [ ] `BA26e` (qa.md:5844) [eyes + save] step: Attack the **Gate District boy** while `Child Leaving` is switched on | say: - | expect: The title is granted
- [ ] `BA26h` (qa.md:5847) step: After any of BA26a-e, walk up to a Gate District guard | say: - | expect: *"There have been reports of a monstrous killer of helpless children..."* -- and on *"I am the killer"* he shouts **"Have at thee, monster!"** and the district turns on you. **This chain has never fired in any playthrough**
- [ ] `BA23` (qa.md:5850) step: BA22, then walk up to any gate guard in the Gate District | say: - | expect: *"There have been reports of a monstrous killer of helpless children...you loosely fit the description."* Two replies: deny, or admit it and threaten him. **Five authored nodes that had never fired**
- [ ] `BA24` (qa.md:5851) step: BA23, then talk to the same guard again | say: - | expect: The `Childkiller Return` variant, not the intro again

**Gate District (Amir)**

- [ ] `BL3` (qa.md:489) where: Amir, with the Sacred Scimitar | steps: Open the conversation | pass: The hand-in reply is reachable from the greeting
- [ ] `S10` (qa.md:1050) where: Amir, Gate District, at `202 make a scimitar` | steps: Reach the second task **without** having taken the Shard | pass: **Two** replies now: the Shard as before, and *"Eduardo the smith speaks of a sacred blade..."*
- [ ] `S11` (qa.md:1051) [eyes + save] steps: Take the scimitar arm | pass: The `Forge a Sacred Scimitar` quest starts -- **from Amir**, not from the dead trigger in the smithy
- [ ] `S12` (qa.md:1052) steps: Take the Shard arm instead, then return | pass: The scimitar reply is **gone**. One arm or the other, never both
- [ ] `S14` (qa.md:1054) steps: Continue | pass: Both arms converge on `120 donate gem` and the trials

**Gate District (Amir) / Cathedral summit**

- [ ] `MS22` (qa.md:1297) [eyes + save] where: Amir, as a Favored One | steps: *"What troubles the Order, Amir?"* -> *"Of course, I will accompany you"* | pass: The cathedral summit plays for Saladin: Javier's opening, Amir's two lines, the exchange, the directions, *"May the Prophet guide you"*, fade, and back to the Gate District with Montserrat on the map. Amir never hostile. **PASSED**, on a save that had not entered the cathedral

**Gate District (Bludjund)**

- [ ] `C19` (qa.md:250) where: Bludjund (Barcelona wall), `10 brain` | steps: ST 8+ | pass: The wrist reply is visible; reaches `30 used speech` and he backs off
- [ ] `C20` (qa.md:251) where: Bludjund, `50 secret mission` | steps: IN 7+ | pass: The "what else are you not telling me" reply is visible; reaches `55 not telling`, which returns cleanly
- [ ] `C21` (qa.md:252) where: Bludjund, after the spy quest (`1 start likes you`) | steps: CH 7+ | pass: The full couplet reply is visible; reaches `1 he likes poem`. The vanilla `IN 4` reply is still there too

**Gate District (Eduardo)**

- [ ] `O6` (qa.md:420) where: Gate District, Eduardo | steps: Open the conversation, any greeting | pass: The reply *"Their chief sends you terms"* is on **every** opening, not buried in a topic
- [ ] `O7` (qa.md:421) steps: As a Demokin / Sylvant / Feralkin / wizard / after insulting him | pass: Still present -- all eight openings carry it
- [ ] `O8` (qa.md:422) steps: Give the terms | pass: He sets down the tongs. *"Fourteen years I have sent boys down there in the dark"*
- [ ] `O10` (qa.md:424) steps: **Barter 35+** | pass: The second acceptance reply is present; absent below it
- [ ] `O15` (qa.md:429) where: Any | steps: Never talk to the trolls at all | pass: All four vanilla routes unchanged. Eduardo's node count is vanilla + 3
- [ ] `BL1` (qa.md:487) [eyes + save] where: Eduardo, ore terms | steps: Agree on the **plain** path | pass: Quest reaches state 2. Chief's return reply appears
- [ ] `BL2` (qa.md:488) [eyes + save] steps: Agree on the **Barter 35** path | pass: Same -- this is the reported failure
- [ ] `AU7` (qa.md:513) where: Eduardo, node 792 | steps: Never took Marisol's quest | pass: He does **not** name Tomas
- [ ] `AU8` (qa.md:514) steps: Tomas rescued | pass: A gated player reply offers him, and node 793 is Eduardo realising who he had been sending down there
- [ ] `S15` (qa.md:1055) [eyes + save] where: Eduardo, **retrieved his father's sword** | steps: Take the scimitar | pass: The **Sacred** Scimitar: +5 critical, +10 piercing resistance. Karma or 150 gold as vanilla, depending on whether you took payment
- [ ] `S16` (qa.md:1056) [eyes + save] where: Eduardo, **talked or bartered past the test** | steps: Take the scimitar | pass: The **Crescent** Scimitar -- same art, no bonuses. The quest still completes and Amir still accepts it

**Gate District (Eduardo, Amir)**

- [ ] `S13` (qa.md:1053) [eyes + save] where: Eduardo, then Amir | steps: Forge the blade, return to Amir | pass: *"I have forged the Sacred Scimitar"* now reaches `210 have scimitar` instead of dead-ending. He hands it **back** -- the Shard is surrendered, the scimitar is kept

**Gate District (Farshad)**

- [ ] `S17` (qa.md:1057) where: Farshad, Gate District | steps: Talk to him at all | pass: **A conversation opens.** Before this he gave a one-line balloon and nothing else
- [ ] `S18` (qa.md:1058) steps: As a male Saladin | pass: *"Word of your deeds have come before you, brother. Welcome into the Order of Saladin."*
- [ ] `S19` (qa.md:1059) steps: As a female Saladin | pass: The sister variant of that greeting
- [ ] `S20` (qa.md:1060) steps: Not a Saladin | pass: `1 Conversation Start`, the ordinary entry -- unchanged
- [ ] `S21` (qa.md:1061) [eyes + save] steps: Carrying either scimitar, ask about the duel | pass: He offers a lesson; accept for **+5 One-Handed Melee** after a fade
- [ ] `S22` (qa.md:1062) [eyes + save] steps: Ask again | pass: The offer is **gone**. Once only
- [ ] `S23` (qa.md:1063) steps: Carrying no scimitar, scimitar quest never done | pass: The offer never appears
- [ ] `S26` (qa.md:1066) where: Farshad, **after** the Djinni enchanted your blade | steps: Ask about the duel | pass: The lesson is **still offered**. The gate accepts the quest being completed as well as the item being carried, because re-granting the blade with an addition may not satisfy an item check

**Gate District (Hrubjub)**

- [ ] `L1.4` (qa.md:99) how: talk to Hrubjub; the `PE 7+` reply is visible on a PE 7+ character
- [ ] `F1` (qa.md:154) where: Hrubjub, node `20 ate a poet` | steps: Ask what he is, compliment his poetry, then *"I've heard enough. Goodbye."* | pass: Reaches `5 goodbye` ("you must earn your reprieve"), not a dead stop
- [ ] `H1` (qa.md:163) where: Hrubjub, first conversation | steps: PE 7+ character approaches | pass: Reply *"You are no scavenger..."* is **visible**
- [ ] `H2` (qa.md:164) steps: Choose it | pass: Node `15 spotted the sap` plays; three replies offered
- [ ] `H3` (qa.md:165) [eyes + save] steps: Choose *"I am no friend to these city guards"* | pass: Reaches `100 bad karma`; karma drops 25
- [ ] `H4` (qa.md:166) steps: Instead choose *"I will be reporting every stone of it"* | pass: Reaches `40 combat threat`
- [ ] `H5` (qa.md:167) steps: Instead choose *"I will keep my observations to myself"* | pass: Reaches `5 goodbye`
- [ ] `H6` (qa.md:168) [eyes + save] where: Hrubjub, after Speech 20 talk-down (`60 used speech`) | steps: Choose *"You and I may have more in common..."* | pass: Reaches `100 bad karma`; karma drops 25
- [ ] `H7` (qa.md:169) where: Hrubjub, vanilla route | steps: Ask *"Did you kill this town guard?"* then admire his handiwork | pass: Still works exactly as vanilla
- [ ] `H8` (qa.md:170) [save] where: Spy quest | steps: Accept, scout the gate, return and report | pass: Quest completes
- [ ] `H9` (qa.md:171) steps: On completion, read his line | pass: Names the warrens beyond the western wood and tells you to use his name
- [ ] `H10` (qa.md:172) [save] steps: Check character sheet after completion | pass: Sneak +10, carry weight +10, Poison resistance +10

**Gate District (Quinn)**

- [ ] `BL4` (qa.md:490) where: Quinn | steps: Each of the three reagent turn-ins | pass: All 21 repaired sites are in this tree; every turn-in reply must be selectable
- [ ] `Q1` (qa.md:989) where: Quinn | steps: Ask what you can help with | pass: He asks for **three wolf pelts**
- [ ] `Q4` (qa.md:993) where: Quinn, after Q2/Q3 | steps: Ask again | pass: He asks for **five wasp stingers**. The pelt errand is gone
- [ ] `Q5` (qa.md:994) [eyes + save] steps: Try to turn in with four | pass: He counts, pushes them back, and says to bring all five. **No stingers are taken** -- 0.8.2; before it, four were consumed and the success speech played
- [ ] `Q8` (qa.md:997) steps: Ask again | pass: He asks for a **lava troll hide**, and mentions the trolls are not animals
- [ ] `Q13` (qa.md:1002) steps: Buy and drink each | pass: Great heals more than Extra Healing; Superior more than Great; Supreme most
- [ ] `S4` (qa.md:1031) where: **Quinn the Herbalist**, Gate District | steps: Talk to him as a Saladin | pass: **6 replies** appear that were previously unreachable -- more than any other NPC in the game
- [ ] `MS25` (qa.md:1300) where: Quinn, fresh shop | steps: Complete an errand, then *"Can I see what you have for sale?"* | pass: One shop window with the earned tiers in it (Great Healing after pelts; Superior after stingers; Supreme after the hide); no reserve reply anywhere. On a save that entered the shop before 0.10.0: the plain shop, and *"What have you set aside for me?"* on the greeting
- [ ] `MS26` (qa.md:1301) where: Quinn, any greeting | steps: *"Is there anything around here I could help you with?"* | pass: `805 errands`: the next open errand offered; the reply gone once the troll errand has been given

**Gate District (Temple Entrance Guard)**

- [ ] `S5` (qa.md:1032) where: Temple Entrance Guard, Gate District | steps: Talk as a Saladin | pass: 1 new reply

**Gate District (Weng Choi)**

- [ ] `MB2` (qa.md:2404) step: Carry them to Weng Choi in the Gate District and talk to him | say: - | expect: A new reply, *"You keep looking at my boots."* It appears whether or not you are a special customer, because both of his return hubs carry it
- [ ] `MB3` (qa.md:2405) [eyes + save] step: Decline with *"They are dead men's errands."* and talk to him again | say: - | expect: The offer is still there. Declining does not activate the quest, so it is not spent
- [ ] `MB4` (qa.md:2406) [save] step: Accept | say: - | expect: A journal entry naming an ogre tusk and a snakebreed venom sac
- [ ] `MB7` (qa.md:2409) [eyes + save] step: **The row the edge case is about.** Put the boots in a chest or sell them, then take both parts to Weng Choi | say: - | expect: He **refuses, aloud**, and **keeps nothing**. Both parts are still in your pack afterwards. If he takes them, the quest can be stranded unfinishable
- [ ] `MB8` (qa.md:2410) [save] step: Recover the boots, return with all three | say: - | expect: He takes the tusk and the sac, the quest completes, **500 XP**, and **Walk a Mile in His Shoes** appears on the character sheet
- [ ] `MB13` (qa.md:2415) step: **Regression.** Talk to Weng Choi about books, the Wind Scroll and his special stock | say: - | expect: Unchanged. Four replies were added to his two hubs and nothing else was touched
- [ ] `MB14` (qa.md:2416) step: After finishing, talk to him again | say: - | expect: No offer, no delivery reply, no refusal. All three are gated on the quest's state or on not having activated it

**Gate District / Inquisition Foyer / La Calle Perdida / Cathedral (patron)**

- [ ] `MS16` (qa.md:1291) [eyes + save] where: Whoever sent you: Amir, Raphael, Cedric, or Javier (cathedral) | steps: Report Montserrat carrying the journal | pass: *"Sir Tomas de Vilanova led the Templars..."* -> the patron's own node, book taken, +500 XP, *Sir Tomas's Journal* closes, back to the report node for the vanilla reply

**Gate District courtyard**

- [ ] `GB1` (qa.md:2510) step: **The row the report is about.** New game. Finish the opening talk, then dawdle -- let him finish the whole stroll and park in the courtyard, turning in place and commenting on things. Now walk north into the gift spot | say: - | expect: The gift scene opens and runs to the end, 25 seconds of it, with **no hovertext line cutting in**. His commentary stops the moment the scene opens and does not come back
- [ ] `GB2` (qa.md:2511) step: Now the other way: new character, walk north with him instead of lagging | say: - | expect: The gift still fires partway up the walk, and his arrival line at that same spot does not land on top of it. That waypoint is where the trigger sits, so this is the near-certain collision, not the unlucky one
- [ ] `GB3` (qa.md:2512) step: **Regression.** On that walk, before the gift fires, listen | say: - | expect: He still banters during the stroll. Nothing is silenced until the gift scene opens

**Gate District, DaVinci's secret chamber**

- [ ] `TR35` (qa.md:3118) step: Seat the ring and watch the screen, not the text | say: - | expect: He teleports in **about half a second** after it seats, while the paragraph about the ring is still up, and the balloon *"Ah! Do not move it, let me *see*!"* lands a second later **PASSED**
- [ ] `TR36` (qa.md:3119) step: Talk to him there | say: - | expect: Three sentences, not eight: *"I felt that through the floor and I knew! <He pats the hull twice.> The turret will turn now..."* **PASSED**
- [ ] `TR37` (qa.md:3120) step: **The judgement row.** Read it next to any vanilla DaVinci line, say his *"There! It is complete."* or *"Bravisimo!"* | say: - | expect: It should sound like the same man. If it still reads like a narrator rather than Leonardo, say so and it gets cut again. **PASSED** -- *"it works"*, 2026-10-13
- [ ] `TR32` (qa.md:3134) [eyes + save] step: **The one that catches a half-restored NPC.** Walk up to him and check he is solid and clickable | say: - | expect: Fully opaque, not a ghost, and the conversation opens. He was faded to zero opacity on his way out, so a silhouette you cannot talk to means the fade or the specifier swap did not land **PASSED** -- he is solid and the conversation opens
- [ ] `TR33` (qa.md:3135) [eyes + save] step: Talk to him again, then leave the chamber and come back | say: - | expect: He is still there and still says it. He does not teleport out again -- the leave relay is spent
- [ ] `TR22` (qa.md:3161) [eyes + save] step: Or ignore him and fit it at the **tank** | say: - | expect: `(look at where the ring would go)`, then `(fit the rotary gear into the turret ring)`, same completion and the same reward
- [ ] `TR24` (qa.md:3163) step: Carry the gear a long time, doing other quests, then try either ending | say: - | expect: Both still offered. The gate now asks only whether you hold the gear, where before it also required the quest's current state to be the one the engine set
- [ ] `TR13` (qa.md:3172) [eyes + save] step: **The report.** Walk into the secret chamber carrying the gear and let the tank's box open by itself, then click through it the way you would dismiss it | say: - | expect: **You still have the gear.** The only options are *(look at where the ring would go)* and *(leave it as it stands)*, and neither costs anything
- [ ] `TR14` (qa.md:3173) step: Choose *(look at where the ring would go)* | say: - | expect: `3 Fixt the empty shaft`: the ring's seat, keyed, oiled and empty. **Then** the fitting is offered
- [ ] `TR15` (qa.md:3174) [eyes + save] step: From there, choose *(fit the rotary gear into the turret ring)* | say: - | expect: The ring seats, the quest completes, the experience is awarded where the marker exists
- [ ] `TR16` (qa.md:3175) [eyes + save] step: From there, choose *(not yet)* | say: - | expect: Nothing happens and you keep the gear. This is the row that proves the second step is a real decision
- [ ] `TR17` (qa.md:3176) [eyes + save] step: With the gear, hand it to DaVinci instead | say: - | expect: His hand-over scene plays as before. **The tank must not have eaten the gear first**, which is what made this look like two bugs
- [ ] `TR9` (qa.md:3185) [save] step: On a character whose **first** visit to the chamber or workshop is after installing, hand in or fit a rotary gear | say: - | expect: The experience arrives. 0.57.4 paid zero here, which is worse than the bug it tried to fix
- [ ] `TR10` (qa.md:3186) [save] step: Check your purse | say: - | expect: **No coin.** This quest pays experience or nothing, by design
- [ ] `TR3` (qa.md:3200) step: `TR2`: read what it says as it goes in | say: - | expect: The ring seats, the turret swings a hand's breadth and stops, *"because nothing inside it is alive yet"*. The tank still needs the spirit, which is the other half of DaVinci's problem and a live quest
- [ ] `TR4` (qa.md:3201) step: Examine the tank **without** the gear | say: - | expect: **Exactly as before:** the description, and no choices at all. Both replies are gated on carrying the gear, the exit included, so nothing changes for a player who has not got it
- [ ] `TR6` (qa.md:3203) step: Hand it to DaVinci, then examine the tank | say: - | expect: No fitting option. The mirror of `TR5`
- [ ] `TR7` (qa.md:3204) step: Examine the **catapult** and the **sweeper** | say: - | expect: Unchanged. They share this tree and must not have grown replies
- [ ] `MC1` (qa.md:3766) where: **The setup.** Reach DaVinci's hidden chamber and talk to him | steps: - | pass: Unchanged from vanilla, plus a new reply asking whether the gears are finished -> `901`. He sends you to his engine, **not** to a blacksmith
- [ ] `MC2` (qa.md:3767) where: Examine the machines in the chamber | steps: - | pass: `1 Catapult`, `1 Sweeper`, `1 Siege Tank` all still work and still say the machines are incomplete. Untouched vanilla
- [ ] `MC3` (qa.md:3768) [save] where: Check the quest log after MC1 | steps: - | pass: `Create Mechanical Gears for DaVinci's Siege Tank` appears and names the steam engine. In vanilla this quest had **no states at all** and could never appear
- [ ] `MC15` (qa.md:3780) where: **The spirit half must be untouched.** Ask him why the engine needs a spirit, and run `Obtain the Spirit Gem for DaVinci` | steps: - | pass: Unchanged. The two halves of the machine are independent and neither blocks the other
- [ ] `EB8` (qa.md:3914) [eyes + save] where: **The shell is now the drop.** Open DaVinci's secret chamber | steps: - | pass: You get the **empty** Sceptre of Bone -- *"Fashioned darkwood that is but an empty shell without a spirit to power it"* -- not the finished one

**Gate District, DaVinci's workshop**

- [ ] `TR26` (qa.md:3146) step: Read what he calls the missing half | say: - | expect: **a spirit**, not a soul. Lowercase, matching his own lines about the spirit gem
- [ ] `TR27` (qa.md:3147) step: Before finishing the quest, check the same greeting | say: - | expect: **No such reply.** It is gated on the quest being complete
- [ ] `TR28` (qa.md:3148) step: Ask him again later | say: - | expect: He says it again. It is a reflection on his machine, not a one-time cutscene, and nothing is paid twice
- [ ] `TR29` (qa.md:3149) step: **Regression.** Find his vanilla line about a dark nature growing in you | say: - | expect: *"There is a sinister taint in your **soul** that you must restrain"* -- unchanged. Only my own line was reworded
- [ ] `TR19` (qa.md:3158) step: **The report.** Buy the gear, then offer it to DaVinci **in the workshop** | say: - | expect: *"No. Not to me, to it."* He **does not take it**, the quest does **not** complete, and he tells you the instrument knows the way down
- [ ] `TR20` (qa.md:3159) [save] step: Check your pack and quest log after `TR19` | say: - | expect: **You still have the gear** and the quest is still open. This is the row that proves he declines rather than silently accepting
- [ ] `TR23` (qa.md:3162) step: Make sure the instrument still works more than once | say: - | expect: It does, and it is ungated: the chamber must stay reachable, or declining in the workshop would strand the quest
- [ ] `TR5` (qa.md:3202) step: Fit it to the tank, then talk to DaVinci | say: - | expect: He has **no** hand-in reply left. Both routes gate on holding the gear, so the quest cannot be paid twice
- [ ] `CG1` (qa.md:3220) step: **The report.** Take the apology route from the engine, **without ever having built the repeating crossbow**, then settle it with DaVinci in the workshop | say: - | expect: He thanks you for the ring and says the engine has had a hand in every machine in the room. **No mention of crossbow gears**
- [ ] `CG2` (qa.md:3221) step: The same, **having finished** `Build DaVinci's Repeating Crossbow` | say: - | expect: The original, richer line: *"it is the engine's ring, the crossbow gears were the engine's too"*. That line is unchanged and should read exactly as it did
- [ ] `CG4` (qa.md:3223) step: Either case: check the apology appears **once** | say: - | expect: One reply, not two. The pair has mutually exclusive gates and identical player text, so a doubled reply means one gate is not resolving
- [ ] `CG5` (qa.md:3224) step: **Mid-quest**: start the crossbow quest but do not finish it, then settle the debt | say: - | expect: The **neutral** line. Completed-rather-than-started is deliberate: the neutral version is never wrong, and this is the row that confirms the safe direction was taken
- [ ] `MC13` (qa.md:3778) where: Take routes 1 or 2 instead, then talk to DaVinci in the workshop | steps: - | pass: **No** crediting reply appears, and the machine never reproaches you. The obligation only exists if you made it
- [ ] `MC16` (qa.md:3781) where: Judge the **writing**, which no check can settle | steps: - | pass: Does the engine read as aggrieved rather than merely rude? Does DaVinci's embarrassment land? And is the promise worth keeping when nothing mechanical rewards it? That last one is the whole point of the release

**Gate District, DaVinci's workshop (steam engine)**

- [ ] `CG3` (qa.md:3222) step: Either case: talk to the engine afterwards | say: - | expect: It stops reproaching you. **Both endings set the same marker**, so a player who got the neutral line is not left owing it forever
- [ ] `GP1` (qa.md:3237) step: Ask the engine for the turret ring carrying **one** potion | say: - | expect: **The flask route is not offered.** It wants three now, and the reply is absent, not greyed
- [ ] `GP2` (qa.md:3238) [eyes + save] step: **The new one.** Carry **three** potions and take that route | say: - | expect: *"Three flasks, then. One for the heat, one for the cut, one for the ring itself."* **Three** potions leave your pack, and you cannot choose which three: every potion in the game is the same item wearing an addition, so the engine picks
- [ ] `GP3` (qa.md:3239) step: With **Endurance 6 or more**, take the blood route | say: - | expect: `703 Fixt the tithe`, then *"(hold out your arm)"*, and you take **50 unavoidable damage**. Armour and resistance do nothing. **This can kill you**, deliberately, and no health floor was added
- [ ] `GP4` (qa.md:3240) step: With **Endurance 5 or less** | say: - | expect: The blood route is absent. A frail character pays in flasks, haggles, or thinks of the apology
- [ ] `GP5` (qa.md:3241) step: With **Barter 50+** | say: - | expect: The haggle route works as before. It used to open at 35, which was vanilla's price for the *small* crossbow gears
- [ ] `GP6` (qa.md:3242) step: With **Barter 35 to 49** | say: - | expect: **No haggle.** This is the row that proves the raise landed
- [ ] `GP7` (qa.md:3243) step: With **Outwit 7+** | say: - | expect: The promise route is offered, free, and still sets the debt the engine reproaches you for
- [ ] `GP8` (qa.md:3244) step: With **Outwit 6 or less** | say: - | expect: **The promise is gone.** It was ungated before, so a dull character used to get the ring for nothing. Check the other routes are still there, because this is the gate that could strand someone if its can failed to resolve
- [ ] `GP9` (qa.md:3245) [eyes + save] step: **Any** of the four routes | say: - | expect: `705 Fixt the gear is cut` plays, the room **shakes**, and the rotary gear lands in your inventory with the quest state advanced
- [ ] `GP10` (qa.md:3246) [eyes + save] step: Buy the **crossbow** gears from the engine, before or after | say: - | expect: Unchanged, still one potion. Only the turret ring was repriced
- [ ] `GC9` (qa.md:3270) step: `GC8`: listen | say: - | expect: **No angry steam sound.** Only the shake was borrowed; the sound belongs to the tantrum, not to work
- [ ] `MC7` (qa.md:3772) where: **Route 3, promise.** Offer to tell DaVinci who built it | steps: - | pass: `702` -- it names its terms: say it to him, **in that room**, out loud. The gear is free -- *Route now needs Outwit 7+ (GP7, 3243).*
- [ ] `MC12` (qa.md:3777) where: **The other row that proves it. Never go back.** Take route 3, finish the quest, and simply never credit the engine. Talk to it a few times | steps: - | pass: `706` every time -- *"One sentence, where I can hear it. Until then I have nothing to say to you that is not this."* There is **no reply anywhere that betrays the promise on purpose**; it breaks by neglect

**Gate District, Eduardo's forge**

- [ ] `SV1` (qa.md:3364) step: Reach Eduardo holding both commissions | say: - | expect: **Both** *"I've been told you can forge a Lion Shield"* and *"...a Sacred Scimitar"* are offered. If only one is, the character is not in both orders and nothing below applies
- [ ] `SV2` (qa.md:3365) [save] step: Bring him the one Magnetized Silver and take **either** item | say: - | expect: It arrives as it always did. `qa.md` has no row for this because vanilla's delivery nodes are reused untouched
- [ ] `SV4` (qa.md:3367) step: Take it | say: - | expect: He explains the filings and the skin off the pour, and names **a thousand gold** -- the silver is free because you went into the mine for it, the weeks are not
- [ ] `SV5` (qa.md:3368) step: With Barter **below** 50 | say: - | expect: Only the flat price is offered. The argument reply is absent
- [ ] `SV6` (qa.md:3369) [eyes + save] step: With Barter **50+** and at least 600 gold | say: - | expect: *"A thousand for sweepings? Six hundred, Eduardo, and you keep a customer."* Pay it and **600** leaves your purse, not 1000
- [ ] `SV7` (qa.md:3370) step: With less gold than the price | say: - | expect: That price's reply is **absent** rather than offered and failing. Both are gated on `CHasMoneyAction`
- [ ] `SV8` (qa.md:3371) [eyes + save] step: Pay, either way | say: - | expect: The second item arrives through vanilla's own delivery node, and its quest advances. **Check your purse** -- the gold must actually be gone
- [ ] `SV9` (qa.md:3372) step: Talk to him once more | say: - | expect: Neither new reply is offered any longer. Both are gated on the item still being owed
- [ ] `BP11` (qa.md:3406) step: Reach Eduardo at the Gate District forge and ask whether his man has been down | say: - | expect: `794 the rock does not answer` -- Mateo knocked three days running. The reply is offered in **all nine** of his greeting variants
- [ ] `BP12` (qa.md:3407) [eyes + save] step: `BP11`, then **admit it**; on a separate run, **lie** | say: - | expect: `795 the smith told` and `796 the smith not told`. Either closes the quest, and the lie is the worse scene. Saying nothing leaves it open
- [ ] `AG12` (qa.md:3812) where: **The Blacksmith, which must NOT have changed.** In the Gate District, commission a Lion Shield or Sacred Scimitar, collect it, and take *"Yes, I need the shield and something else"* | steps: - | pass: You reach `07 what more` with its full menu **including the Red Ore hand-in**. Node `80 Do You Have The Item I Need?` is a superseded draft and was deliberately left unreachable -- if it appears, something was wired that should not have been

**Gate District, Weng Choi's shop**

- [ ] `FJ1` (qa.md:3532) [eyes + save] where: The Gate District, Weng Choi's shop | steps: Become a valued customer and collect his rare books, returning as many times as it takes | pass: You are given a different book each time, cycling through his stock
- [ ] `FJ3` (qa.md:3534) [eyes + save] where: Look at the Journal in your inventory | steps: - | pass: It is called **`Feralkin Journal`** -- with **no trailing full stop**. It was the only one of the twelve books whose name ended in one. Its description mentions the life and trials of a Feralkin at the hands of the Inquisition
- [ ] `FJ4` (qa.md:3535) where: Pick it up and put it down | steps: - | pass: It plays the scroll/book pickup and putdown sounds. Those were always in the item; nothing here changed them
- [ ] `FJ5` (qa.md:3536) where: **He buys it too.** Sell the Journal back to Weng Choi | steps: - | pass: His *"What is this you have sold me? A rare book?"* response fires, exactly as it does for the other ten
- [ ] `FJ8` (qa.md:3539) [save] where: **The regression.** Collect Weng Choi's books again on a fresh character | steps: - | pass: **All ten of the originals still appear** -- Eloquent Works, Art of Barter, the five History books, Centuries, Tome of Geomancy, Book of Death, Poetry Book. This release inserted into the middle of the series that gives them out

**Gate District, secret chamber and workshop**

- [ ] `TR38` (qa.md:3121) step: Finish at the tank, talk to him there, then go up and talk to the workshop DaVinci | say: - | expect: **The two do not repeat each other.** The chamber line is about feeling it through the floor; the workshop line reaches for the spirit's temper instead
- [ ] `MC9` (qa.md:3774) [eyes + save] where: **The row that proves the design.** Take route 3, hand the gear to DaVinci in the chamber, then leave and come back to the workshop | steps: - | pass: The quest is **complete** and paid, but the engine is **still owed**. A new reply to DaVinci in the workshop offers to say it. The debt survived the quest ending -- *Since 0.57.7 finish at the tank; the chamber hand-in only works if he is still there.*

**Gate, Port and Temple Districts; Shylocke's shop**

- [ ] `AQ4` (qa.md:1742) step: **Negative, the sweep that was reverted.** Commit a crime in the Gate, Port or Temple District; talk to Cedric; enter Shylocke's shop | say: - | expect: The guards react as before and every conversation opens as before. The first sweep caught the **Guard Reserves**, which are the crime system, plus `Cedric Talks to Player`, `check if player attack overrided` and `Start Here`, which are dialogue triggers. None of them is touched

**Herbalist's shop**

- [ ] `SD12` (qa.md:1692) step: **Negative, and the one that matters most.** Open the **herbalist's** shop at every stock tier and look for any scroll | say: - | expect: **There is none.** The herbalist sells potions, including Fixt's Great, Superior and Supreme Healing. If a scroll appears there, the picker edit leaked into the potion pool and the whole "magic vendors only" split is gone

**Inquisition Chambers**

- [ ] `TQ1` (qa.md:2593) step: **The row that matters.** Get past the tithe inquisitor and step into the Grand Inquisitor's chamber for the first time | say: - | expect: The apparition forms out of the fog, **Torquemada speaks first** -- *"It is a great honor to speak with you again, Asha."* -- then the Old Man gives his order about the Cathars, then he dissolves
- [ ] `TQ2` (qa.md:2594) step: **The row that stops TQ1 going too far.** Watch it to the end without fast-forwarding | say: - | expect: Controls come back, and the secret door behind him can now be found. A series that stalls on a balloon leaves the player locked in the cutscene with no controls, which is the only way this change can hurt
- [ ] `TQ3` (qa.md:2595) step: Fast-forward it instead | say: - | expect: Same ending: controls back, secret findable
- [ ] `TQ4` (qa.md:2596) step: On a magic-using character, let Torquemada try to purify you with fire | say: - | expect: He now says *"You resist? The flames do not harm you..."* **before** *"I do not know whether divine providence or fiendish charms guard your body"*
- [ ] `TQ5` (qa.md:2597) step: **Regression.** Take each of the three replies on *"do you wield your magic for good or for dark purposes?"* | say: - | expect: Good goes to `204 saved`, own needs to `220 no reasoning`, dark purposes starts the fight. Unchanged -- *0.95.0 changed what a fight with him does before Montserrat (HH1, line 6100).*
- [ ] `IQ1` (qa.md:5141) step: With `Bring the Rogue Inquisitors to Justice` **completed**, enter the Inquisition Chambers | say: - | expect: **No crash.** This is the whole fix
- [ ] `IQ2` (qa.md:5142) step: Talk to the Grand Inquisitor on a normal return (`3 Return Dialogue`) | say: - | expect: He greets you and the conversation opens
- [ ] `IQ3` (qa.md:5143) step: Ask *"Does the Inquisition have any tasks for me?"* on the irritated return (`2 Irritated Return Dialogue`) | say: - | expect: The reply appears and resolves. It is gated on that quest being complete, which is the gate that was crashing
- [ ] `IQ4` (qa.md:5144) step: The same on the favored return (`5 Favored Return`) | say: - | expect: Likewise
- [ ] `IQ5` (qa.md:5145) step: Enter the Chambers **without** that quest complete | say: - | expect: No crash either. The requirement now evaluates instead of failing to load

**Inquisition Chambers (Raphael)**

- [ ] `IQ1` (qa.md:2865) step: After the summit, return to Raphael in the Chambers of the Inquisition | say: - | expect: A new option on his return hub: **"What would you have me do about Montserrat?"**
- [ ] `IQ2` (qa.md:2866) step: Take it | say: - | expect: **With voiceover.** *"To the north is the Abbey of Montserrat... I wish you to head north to the abbey and determine what has happened."*
- [ ] `IQ4` (qa.md:2868) [save] step: Check **Aid Sir Auric** in the log | say: - | expect: Failed. The Inquisition order replaces the Templar initiation, and `321` is what fails it
- [ ] `IQ7` (qa.md:2871) step: **Regression, non-Inquisitor.** Talk to Raphael as a Templar or unaffiliated character | say: - | expect: No new option. It is gated `Inquisitor IS`, the same requirement its neighbour uses
- [ ] `IQ8` (qa.md:2872) step: Ask twice in the same window, if you can | say: - | expect: Harmless. Re-activating a state that is already current is a no-op, and a failed quest cannot fail twice

**Inquisition Chambers (Torquemada)**

- [ ] `TD1` (qa.md:1208) [eyes + save] where: Torquemada, Inquisition Chambers | steps: Join the Inquisition, take the Khan task, kill him, report | pass: You reach **`407 killed khan`** -- *"I have known, child... Are you ready for another task?"* -- and are paid 150 gold
- [ ] `TD2` (qa.md:1209) [eyes + save] steps: Same, as a **non**-Inquisitor | pass: You still reach `408` -> `409`, *"I feel there is now hope for your soul"*, and are paid 150 gold. **Unchanged from vanilla**
- [ ] `TD3` (qa.md:1210) steps: Report as an Inquisitor and read the reply list | pass: Exactly **one** Khan report reply is offered, not two

**Inquisition Chambers (jailor)**

- [ ] `MS30` (qa.md:1305) [eyes + save] where: Inquisition Chambers jailor, as an Inquisitor | steps: *"I am eagerly awaiting training on the Rites of Confession"*, take the keys, talk to any cell prisoner, return | pass: *"I have spoken with the possessed..."* offered; the lesson pays 250/100/25/5 XP by Speech, the belt at the top; not offered again
- [ ] `MS31` (qa.md:1306) where: Same jailor, as a Templar or with Speech 30, not an Inquisitor | steps: *"I'm here on important business from the Knights Templar"* | pass: Keys given; the reply is gone on the next greeting, and *"How do you get inside these cells?"* is not offered

**Inquisition Chambers2 (Sanchez)**

- [ ] `SR32` (qa.md:879) steps: Get out via any of Sanchez's routes -- pay the fine, `Speech 35`, `Speech 50`, or Templar | pass: All work as they always did. Nothing here is new

**Inquisition Chambers2 (cell)**

- [ ] `SR31` (qa.md:878) [save] where: The cell | steps: Check your inventory | pass: **You still have what you stole.** If it is gone, stop -- the quest can no longer be completed

**Inquisition Pit3**

- [ ] `CV13` (qa.md:3328) step: Find Cervantes as a **prisoner** in `Inquisition Pit3` and hurt him | say: - | expect: **No bark.** That map replaces his damaged slot by name, which is expected and deliberately left alone

**Inquisition Pit3 (Galileo)**

- [ ] `CP15` (qa.md:1353) where: Fresh Inquisition Pit3 (Galileo's cell) | steps: Attack Galileo, the random map, walk back in | pass: *"Beware braggart, I have less tolerance now for your idiocy"* (voiced) once over him; not on a first entry

**Inquisition Pit3; Slave Pits; Lava Troll**

- [ ] `AQ3` (qa.md:1741) step: **Negative, and the point of the row.** Fight the Terrors in Inquisition Pit3, the Lava Troll, or the Slave Pits melee | say: - | expect: A little more room before they commit, and **no more than that**. Confirmed in play: *"it doesn't feel vastly different, that's probably ok"*. If it reads as a difficulty drop, that is the risk this release carries and the reason to revert it

**Inquisition foyer**

- [ ] `RJ2` (qa.md:2599) step: **The row that stops RJ1 firing twice.** Leave the foyer and come back | say: - | expect: Nothing on approach. Clicking him opens the ordinary return conversation
- [ ] `RJ3` (qa.md:2600) step: **Regression.** A character who never attacked anyone walks past him | say: - | expect: No balloon, ever, on any visit

**Jafar**

- [ ] `SH3` (qa.md:3376) [eyes + save] step: Give it to him | say: - | expect: `216 the shard unasked`. He presses coins on you and will not take it as a gift. **Karma and 250 coin**, and the Shard leaves your pack
- [ ] `SH4` (qa.md:3377) [save] step: Check the quest log afterwards | say: - | expect: **No new quest, completed or otherwise.** The task stays untaken; only the relic changed hands
- [ ] `SH5` (qa.md:3378) step: Check what he says next | say: - | expect: He does **not** send you to the Dream Djinn trials. That is `215 shard`, the task version, and this route must not reach it
- [ ] `SH6` (qa.md:3379) step: Take the **shard** task at the fork instead, carrying the Shard already | say: - | expect: The existing *"I already have the Shard of Dreams"* reply resolves it, with its own full reward. 0.3.0 built that and this release must not have disturbed it
- [ ] `SH7` (qa.md:3380) step: **The trap case.** Carry the Shard but do not reach Jafar's fork yet | say: - | expect: The new reply is **absent**. It also requires that the scimitar task was actually taken -- otherwise you could hand the relic over and then be sent to find it
- [ ] `SH8` (qa.md:3381) step: Do the shard task normally, start to finish | say: - | expect: Unchanged, including the Dream Djinn hand-off

**Jafar; Slave Pits**

- [ ] `SH1` (qa.md:3374) [save] step: Take Jafar's **scimitar** task at the fork, then recover the Shard of Dreams from the slavers | say: - | expect: No quest appears for it. That is correct and is the design -- you took the other task

**Knights Templar armory (Sir Auric)**

- [ ] `TD14` (qa.md:1222) where: Sir Auric | steps: Complete his first task as a **tainted** character | pass: You get **`100 join tainted`** -- *"I didn't think someone like you could have completed the task"* -- and the sponsorship is granted
- [ ] `TD15` (qa.md:1223) steps: Same as a **human** | pass: You get `100 join`, the vanilla wording. Only one of the two is ever offered
- [ ] `MS33` (qa.md:1308) [eyes + save] where: Knights Templar armory, fresh map | steps: Attack Auric, wake in the cell, walk back to the armory | pass: About a second after entering, *"Save your belligerence..."* (voiced) over Auric, logged; not again on the next entry; he talks normally after

**La Calle Perdida**

- [ ] `CP2` (qa.md:1340) where: La Calle Perdida, fresh, a Wielder who killed Relican | steps: Talk to any generic wizard | pass: *"Welcome, fellow Wielder. We have heard much of your victory over Relican"*; `60 Membership` has no fight reply
- [ ] `CP3` (qa.md:1341) where: La Calle Perdida, fresh, a Wielder who has not, and a non-Wielder | steps: Talk to a wizard | pass: The greetings as before
- [ ] `CP4` (qa.md:1342) where: La Calle Perdida, fresh | steps: Attack Cedric, the random map, walk back in | pass: *"You have strained what little welcome you had..."* (voiced) once over him; not on a first entry
- [ ] `CP5` (qa.md:1343) where: After Relican's takeover | steps: Attack Relican, the random map, walk back in | pass: *"I trust you have come to your senses?"* once over him
- [ ] `CP6` (qa.md:1344) where: Dark Wielder, Relican's `30 power` | steps: *"Power is what you took from the Wielders..."* -> *"With the ones you drove out of here..."* | pass: `80 war`; Relican, the Undead Guard and Brambles the Man attack; Relican takes damage and spells; no random-map relocate
- [ ] `CP7` (qa.md:1345) [eyes + save] where: CP6, kill Relican | steps: - | pass: *"<He goes down the way he stood...>"*; XP; the four Dark Wielder quests failed in the journal; a generic wizard then greets you as the one who killed Relican
- [ ] `CP8` (qa.md:1346) [eyes + save] where: Wielder, Cedric's secondary greeting | steps: *"Is there anything else the Wielders need?"* | pass: `140`; accept -> the crystal quest in the journal; the reply gone after; a non-Wielder never sees it
- [ ] `CP10` (qa.md:1348) [eyes + save] where: CP9, Cedric | steps: *"I went to the crystal by the lake. It raises the dead."* | pass: `141`; quest complete; 400 XP; Cedric's Ward in inventory (no slot, sellable)
- [ ] `CP12` (qa.md:1350) where: Inquisitor, turn the Calle over | steps: Watch the wipeout | pass: Wielders that appear during it die on generation as the shipped relay intends
- [ ] `CP13` (qa.md:1351) where: Brambles, pour the potion, the man | steps: - | pass: After his thanks, one of three random barks over him 1.5 s later
- [ ] `AT3` (qa.md:2900) step: Attack Cedric Alsen in La Calle Perdida | say: - | expect: *"Wielders, to me! La Calle Perdida is under attack! The intruder must not leave here alive!"*
- [ ] `PK9` (qa.md:3640) [save] where: Kill a Wielder in La Calle Perdida | steps: Check the sheet | pass: **Enemy of the Wielders** is listed
- [ ] `PK10` (qa.md:3641) where: After `PK9`, talk to a Wielder wizard there -- **especially if you are a Wielder**, so you get *"Welcome, fellow Wielder"* | steps: - | pass: The candles-down-a-long-hall reply is offered, and the room turning cold is in the line
- [ ] `LD14` (qa.md:3885) where: **No interference.** Run the Quinn task and `40 dark wielder task 3` with the DaVinci quest active, and again after completing it | steps: - | pass: Unchanged. The DaVinci task sits on the hub, not in the numbered chain
- [ ] `LD15` (qa.md:3886) where: **The ignore case.** Play the whole Dark Wielder initiation and never speak to DaVinci about Relican | steps: - | pass: Identical to 0.39.0. The task is optional and nothing waits on it
- [ ] `EB18` (qa.md:3924) [save] where: **The title.** Finish the dark path and answer **Yes** to Relican's Summoning Ring | steps: - | pass: You gain **`Ruler of Calle Perdida`** / "Dark Lord of Calle Perdida". Karma still drops 800 and the three good quests still fail, exactly as before -- the only change is that the ending now names you
- [ ] `SR3` (qa.md:5405) step: La Calle Perdida: complete a favour for **Brambles** | say: - | expect: One of three thank-you balloons appears, varying between runs
- [ ] `AL11` (qa.md:5690) step: As a Wielder who killed Relican, talk to a wizard in La Calle Perdida and reach `60 Membership` | say: *"Did you have to pass such tests?"* | expect: Four replies, not five. The dead *"Save your flattery and begone"* -- a Fight Icon that started no fight and closed the conversation -- is gone from this node as it already was from `50 Spirit` -- *Needs a Wielder who killed Relican.*
- [ ] `CP16` (qa.md:5922) step: Fresh Calle Perdida, as a player who has defeated Relican | say: Walk the Cedric-gated content | expect: Ten canned gates in the Calle pointed at a nonexistent expression until this release and were taking the Else; confirm the defeated-Relican branches now open

**La Calle Perdida well, Trapped Ether Plane**

- [ ] `EB1` (qa.md:3907) where: **The well.** La Calle Perdida, find and enter the well | steps: - | pass: You reach the Trapped Ether Plane. Re-enter it a second time to confirm the door is not once-only

**La Calle Perdida, Lord Relican**

- [ ] `LD1` (qa.md:3872) [eyes + save] where: **The offer.** On Relican's path, talk to Lord Relican at his hub | steps: - | pass: A `Quest Icon` reply asks about Leonardo in the Gate District -> `90 Fixt DaVinci task`. He says he will not have him killed, *"a corpse invents nothing"*. The journal gains `Convince DaVinci to Join the Dark Wielders`
- [ ] `LD2` (qa.md:3873) where: Decline the task (*"Leave the tinker to his toys"*) | steps: - | pass: Conversation ends, no quest activated, and the reply is still offered next time
- [ ] `LD11` (qa.md:3882) [eyes + save] where: **Report success.** After LD6/LD8/LD9, return to Relican | steps: - | pass: A reply reports Leonardo will not stand against him -> `91 Fixt DaVinci joined`. Quest **completes** and you gain **650 XP**
- [ ] `LD12` (qa.md:3883) [eyes + save] where: **Report the refusal.** After LD4, return to Relican | steps: - | pass: A reply reports Leonardo refused -> `92 Fixt DaVinci refused`. Quest **completes** -- it must not sit open or show as failed -- and pays **no** XP
- [ ] `LD13` (qa.md:3884) [save] where: Check the journal after both LD11 and LD12 | steps: - | pass: No dangling entry in either case. Both paths close the quest
- [ ] `EB7` (qa.md:3913) [eyes + save] where: **The fallback, and the row that matters most.** On Relican's path, take the Sceptre shell from DaVinci's secret chamber, then **kill the Enchanter** (or never enter the plane), then talk to Relican | steps: - | pass: A reply offers *"I have the Sceptre, but it is a dead thing"* -> **`47 Fixt Relican Binds Shell`**. He binds it, you receive `Rod Bone WITH Spirit`, the quest completes and you continue to `40 dark wielder task 2`. **If this reply does not appear, the Dark Wielder initiation is unfinishable and the release must be pulled**

**Port District**

- [ ] `AT6` (qa.md:2903) step: Attack Shakespeare in the Port District | say: - | expect: *"Time to make an honorable retreat rather than face a dishonorable foe!"* He cannot actually retreat; nothing in this engine can
- [ ] `FN16` (qa.md:3017) step: **Regression.** Look at the other sailors: the mute one, the crew on the ship, and Juan's body | say: - | expect: All still "Sailor". Only his own template changed, and the shared ship-sailor template was deliberately left alone
- [ ] `PK7` (qa.md:3638) [save] where: Kill a Knight Templar (the Port District has them) | steps: Check the sheet | pass: **Enemy of the Knights Templar** is listed
- [ ] `PK8` (qa.md:3639) where: After `PK7`, talk to a Templar -- **and if you are a Templar yourself, use that path** | steps: - | pass: The reaction is reachable from the ordinary greeting *and* from *"Well met, brother"* / *"Well met, sister"*. The *"I will not call you brother again"* line should land hardest there
- [ ] `EH5` (qa.md:4469) step: **Run this before the rest.** Start a new game and play any ordinary fight -- thugs in the Port District will do. Also skim your character sheet's skill list, and fold in `EH3` while you are there | say: - | expect: **You are looking for nothing to happen.** Port thugs are not the Priest family, so no new behaviour should appear; this only confirms that adding a 93rd `.Skill` to a 92-skill game broke nothing. **Checked 2026-10-10 and the risk is narrower than this row used to claim:** `Skill Values` is keyed by **full path name** with **no `Item Count`** (184 entries of `Skills/<path>=v,min,max`), so there is no positional index and **adding a skill cannot shift anything**. The only live question is whether a name-lookup miss returns 0 or errors. Fail looks like an enemy standing inert or using a visibly wrong attack, a blank or duplicated entry in the skill list, or a crash on entering combat or opening the skill tree -- **not** odd numbers. If it fails, the fallback needs no new skill at all: `CGiveHealthToCharacterAction` fired from a can makes an enemy heal itself. **PASSED 2026-10-10** -- Port District thugs fought normally on a fresh game. The 93rd `.Skill` breaks nothing, so **0.33.0 and 0.34.0 are no longer at risk of wholesale removal** and the name-keyed `Skill Values` reading is confirmed in play. Note this clears the *structural* gate only: the healing feature itself is still unproven, and `EH1` (act 6, a Priest and soldiers together) remains the row it exists for
- [ ] `DN4` (qa.md:4857) step: Check Fernand's stats are unchanged -- HP, AC, how hard he hits | say: - | expect: Identical. The clone carries `Races/NPCs/Sailor`'s three presets verbatim; only the name differs
- [ ] `DN16` (qa.md:4902) [save] step: **Sir Jorge** in the Port District | say: - | expect: **"Sir Jorge"**, not "Knight Templar 3" -- *0.60.3 found the log prints the can's User Assigned Name, not the race name this release edited. Expected names here came from race names, but 0.60.3 found the log prints the can's User Assigned Name (a hat goblin logs Goblin Striker). A different name is not a failure on its own; check it against the can.*
- [ ] `FA1` (qa.md:5181) step: Recruit Fernand, take him into the Vodyanoi fight at the north island | say: - | expect: After killing one, he **moves to the next enemy on his own**, including one behind or beside him. Before this he stood still until something hit him
- [ ] `FA2` (qa.md:5182) step: Stand him where an enemy is roughly 400-500 units off and out of his facing | say: - | expect: He acquires it. The old 300 range and 90-degree cone could see neither
- [ ] `FA3` (qa.md:5183) step: Let an enemy attack him while he is idle | say: - | expect: He fights back, as he always did -- `Target shooter if hit=1` was never the broken part
- [ ] `FA4` (qa.md:5184) step: Take his health below 40 percent | say: - | expect: **He breaks off and retreats.** Deliberate: `Retreat when=40` is kept, unlike Cervantes who never flees. Not a bug
- [ ] `FA5` (qa.md:5185) step: Walk far enough away mid-fight | say: - | expect: He disengages and returns to following. `Max dist from home=500` is unchanged
- [ ] `FA6` (qa.md:5186) step: Compare against Cervantes in the same fight | say: - | expect: Broadly similar engagement now. He still retreats where Cervantes does not, by choice
- [ ] `FN1` (qa.md:5212) step: Recruit Fernand, then talk to him | say: - | expect: The **generic companion menu**: *"What would you like your companion to do?"* with *Release Companion*. That is the engine's, not his, and is expected. **PASSED** 10/01/26, release and rejoin exercised by hand
- [ ] `FN2` (qa.md:5213) step: Choose *Release Companion* | say: - | expect: He stops following. **PASSED** 10/01/26, release and rejoin exercised by hand
- [ ] `FN3` (qa.md:5214) step: Talk to him again | say: - | expect: **His own conversation opens**: *"Shall we continue, or is my place here for now?"* with *Walk with me again, Fernand.* This reply is the whole release. **PASSED** 10/01/26, release and rejoin exercised by hand
- [ ] `FN4` (qa.md:5215) step: Choose *"Walk with me again, Fernand."* | say: - | expect: **He rejoins and follows.** This is the bug, reported five times across seven attempts. **PASSED** 10/01/26, release and rejoin exercised by hand
- [ ] `FN5` (qa.md:5216) step: Talk to him while he follows again | say: - | expect: The generic menu once more. His node is hidden while he follows -- correct, not a regression. **PASSED** 10/01/26, release and rejoin exercised by hand
- [ ] `FN6` (qa.md:5217) step: Cycle release and rejoin three times | say: - | expect: Works every time. No flag, nothing to desynchronise
- [ ] `FN7` (qa.md:5218) step: Choose *"Hold this spot a while longer."* | say: - | expect: The conversation closes and he stays put. Talking again re-offers the rejoin
- [ ] `FD6` (qa.md:5395) step: Take him through a map transition after rejoining | say: - | expect: He follows normally, as on the first recruitment -- *Rejoin is now Release Companion then node 103's 'Walk with me again'; no FN row covers a map transition.*
- [ ] `ES37` (qa.md:5756) [eyes + save] step: **In act 1**, accuse Captain Isabella, hear her out, and choose *"You have persuaded me to silence."* (not the `<Lie>` variant) | say: - | expect: The Morales quest completes at state `JMBN5402` and she says *"I will not forget your kindness."*
- [ ] `ES39a` (qa.md:5759) step: **In act 1**, after ES37, let her finish -- there is a new beat after *"I will not forget your kindness"* | say: - | expect: *"Two years of being careful in a language that is not mine, and in all that time not one person has asked me why."* **Her continue reply had no destination at all in vanilla**
- [ ] `ES39b` (qa.md:5760) [eyes + save] step: Answer *"Then I will hope to see the ship and not the sinking."* | say: - | expect: She gives you her name -- *"Grace, then. Not Captain, and not Isabella."* -- and **Grace's Regard** appears among your titles
- [ ] `ES39c` (qa.md:5761) [eyes + save] step: Decline instead, warmly or coldly | say: - | expect: *"You have my thanks, which is not nothing from me."* No title
- [ ] `ES39d` (qa.md:5762) step: Take the `<Lie>` route at *"You have persuaded me to silence."* | say: - | expect: The beat still plays -- she opens up to someone deceiving her -- but **the reply that answers her is not offered**
- [ ] `ES48b` (qa.md:5774) step: Kill Captain Isabella in the act-1 Port District | say: - | expect: Unchanged -- still HP 36. The act-7 template is separate so act 1's balance is untouched
- [ ] `ES21` (qa.md:5788) [eyes + save] step: **In act 1**, take Guy Fawkes' side and reach either good ending -- decline the Duke's murder, or carry it out and collect the Queen's gold | say: - | expect: **Servant of the Queen** appears among your titles. Vanilla stored the allegiance nowhere at all
- [ ] `ES22` (qa.md:5789) [eyes + save] step: Betray him instead: expose him, or tell the Duke you will deal with him | say: - | expect: **No title.** Both grants sit past every betrayal branch, which matters because the engine has no way to take a perk back
- [ ] `ES23` (qa.md:5790) step: In act 1, accept the Duke's murder -- *"I'll lure the Duke to the trap."* | say: - | expect: He answers: *"you will be remembered forever in English history... When the deed is done, return here."* **In vanilla that reply ended the conversation silently**
- [ ] `BA26a` (qa.md:5840) [eyes + save] step: Attack **Marisol** outside the sewers in the Port District | say: - | expect: She screams *"Ahhh!"*, will not speak to you again, walks off to her disappear point, *Find the lost boy Tomas in the Sewers* fails -- all vanilla -- **and you are now Slayer of Innocents**

**Port District (Fernand)**

- [ ] `CP14` (qa.md:1352) where: Fresh Port District, recruit Fernand, fight beside him | steps: - | pass: He closes to arm's length before swinging; no hits from across the room

**Port District (Fernand, Juan)**

- [ ] `MS19` (qa.md:1294) [eyes + save] where: Port District, Fernand and Juan | steps: Take Fernand's job; go to Juan | pass: Fernand hands over *Fernand's Draught* (not a plain potion); Juan shows the interaction cursor, and Absorb Spirit cannot target him from any range; the draught saves him: he stands, walks to Fernand, and six balloons play -- three vanilla, three of Fernand chiding him -- before he walks to the ship. Leave him instead: *fading* at 20 seconds, the too-late line and the failed state at 45. The Mute Sailor's reward is a plain potion again. **PASSED** on a fresh Port District

**Port District (Shakespeare's house)**

- [ ] `SW8` (qa.md:3061) step: **Regression.** Visit his house in the Port District | say: - | expect: Everything there is as it was: the muse thanks, the debt conversations, the arbitration. One action was added to his whole tree and no line was changed

**Port District (ship)**

- [ ] `SR1` (qa.md:5403) step: Port District: board the ship and talk to **Captain Isabella** | say: anything | expect: The conversation opens. No "infinite loop while trying to load" dialog. **PASSED**, on several separate conversations rather than one -- *Already marked PASSED.*

**Port District tavern**

- [ ] `NR1` (qa.md:3731) [save] where: **Baseline.** In the Port District tavern before Montserrat, spare the drunkard a gold and learn Drunken Boxing | steps: - | pass: Unchanged vanilla. He teaches the style; your Unarmed goes up 3
- [ ] `NR2` (qa.md:3732) where: Speak to him again, still before Montserrat | steps: - | pass: *"Good to see you again, friend. Grab an ale and enjoy yourself"* and **nothing else**. In vanilla this node had no replies at all and before Montserrat it still must not
- [ ] `NR15` (qa.md:3745) where: Check the drunkard still works for a character who **never** gave him gold | steps: - | pass: He stays in his gibberish state. The whole chain hangs off the kindness in NR1

**Port District tavern (Brendan)**

- [ ] `AB5` (qa.md:1262) [eyes + save] where: Port District tavern, Brendan (Luck <= 3) | steps: Take his drink | pass: After *"Take a healthy tug from the Serpent's Bile..."* he notices your luck (`200 low luck`, or the `lass` twin for a woman), and you receive **Sullivan's Clover**; then *"Grand. Now, what can I do fer ye?"*. The clover equips at the neck and shows +1 Luck
- [ ] `AB6` (qa.md:1263) [eyes + save] where: Port District tavern, Brendan (Luck >= 4) | steps: Take his drink | pass: Straight to *"Grand. Now, what can I do fer ye?"*; no clover
- [ ] `AB7` (qa.md:1264) [eyes + save] where: Brendan, negative | steps: Talk to him again after the clover | pass: The drink is not offered again (vanilla `took irish drink`), so no second clover. **This was false from 0.9.1 until 0.83.3** -- six of the seven replies reaching `200 drink` carried the gate and the one on `200 irish` did not, so *"That accent is odd"* re-opened it every conversation. 0.9.1 is recorded as entirely unplayed, so the row was never run rather than wrongly passed. **Take the drink, then try all four ways back to it**
- [ ] `ID1` (qa.md:1884) step: **The reported row.** Port District tavern, Brendan. Take the drink, then re-open the conversation and take *"That accent is odd - where are you from?"* | say: *"I'll take that drink now, if you're still buying."* | expect: **The reply is not there.** That was the tap: six of the seven replies reaching `200 drink` checked the `took irish drink` flag and this one did not
- [ ] `ID2` (qa.md:1885) step: From the same greeting, work through **every** way back to the drink: *"Who are you?"* (`200 name`), *"Why did you say you will fight the English?"* (`200 english`), the singer's return nodes, and `1500 other questions for irish` | say: - | expect: None of them offers it either. Seven paths, seven gates
- [ ] `ID3` (qa.md:1886) step: **Before** taking the drink, check the same seven paths | say: - | expect: Each one **does** offer it. The gate is "not yet taken", so a first-time player loses nothing
- [ ] `ID4` (qa.md:1887) [eyes + save] step: **Luck 3 or less.** Take the drink, get Sullivan's Clover, then try to reach it again by any route | say: - | expect: **One clover only.** `200 low luck` and its `lass` twin are reached from `200 drink` and nothing else, so this loop closed with the drink -- it was farmable the same way
- [ ] `ID5` (qa.md:1888) step: Regression: the drinking song and the insult route | say: *"You're Irish? I don't drink with Irish."* | expect: Unchanged. Only one reply gained a requirement; the song relay, the insult node and the goodbye are untouched

**Port District, Gate District**

- [ ] `NR12` (qa.md:3742) where: **The timing gate.** On a fresh character, try to reach any of the above **before** Montserrat | steps: - | pass: The drunkard's ask is absent, Quinn's reply is absent, the witch's reply is absent. Nothing in the chain is reachable early

**Port District; Slave Pits**

- [ ] `AQ1` (qa.md:1739) step: Fight the Thug archers in the Port District, or the Bow thugs in the Slave Pits | say: - | expect: They open fire **before** you are on them. Their radius went 550 to 850 against a standoff of 350, so they no longer acquire you and then walk 200 units closer before shooting

**Quinn**

- [ ] `WS6` (qa.md:1923) [eyes + save] step: Hand Quinn five stingers | say: *"I have five wasp stingers for you."* | expect: He accepts and the quest advances. Four is refused -- the tree checks the item five times and removes it five times
- [ ] `WS7` (qa.md:1924) [eyes + save] step: **The sibling, for comparison.** Bring Quinn three wolf pelts | say: *"I brought you three wolf pelts, as you asked."* | expect: Accepted. All ten wolf cans drop a pelt, so three pelts is three kills; this row exists to keep the two quests' difficulty in view of each other

**Quinn and Weng Choi shops**

- [ ] `WC20` (qa.md:2528) step: **Charges can be bought.** Visit Quinn and Weng Choi, trade, leave, wait for a restock, return | say: Look for **Wand Charge** in their stock | expect: It turns up about one restock in thirty-one. Four shop slots carry it: Quinn's non-Inquisitor and Wielder stores, Weng Choi's ordinary and special inventories -- *Price is now 50 each (0.83.4).*

**Quinn; the Montaillou witch**

- [ ] `NR14` (qa.md:3744) where: **Nothing shipped disturbed.** Run Quinn's own `Troll Hide` and `Wasp Stingers` fetches and his shop tiers; run the witch's Nostradamus, caverns and Cathar branches | steps: - | pass: All unchanged. Three heavily-used trees were edited and none of their existing content may shift

**RED FILE bonus level**

- [ ] `BS4a` (qa.md:5457) [eyes + save] step: **The RED FILE preorder bonus level**, entered from the Gate District, on a save that has never been in it | say: - | expect: The densest test in the game: **90** spawns carry the new races (Pale x33, 4 Sword x23, 3 Mace x12, plus Tough). Crowds this size are where the behind-attack geometry should happen on its own. Its 100 bow thieves must **never** produce a backstab line

**Relican (Enchanter route)**

- [ ] `SB5` (qa.md:2158) [eyes + save] step: **Regression.** The Enchanter route: ally him, take the ring, then offer him the shell | say: - | expect: `75 Fixt Sceptre`. The shell is removed, the spirited sceptre arrives, and the journal advances to deliver it to Relican

**Slave Pits**

- [ ] `TG1` (qa.md:5329) step: Fight an `Assasin Master` | say: - | expect: Roughly one attack in four spawns a visible effect on him, pauses about a second, then lands an extra hit
- [ ] `TG2` (qa.md:5330) step: Watch for the pause | say: - | expect: **The point of the item.** If the warning does not read as a warning, it failed even if the damage lands
- [ ] `TG3` (qa.md:5331) step: Compare Super against base | say: - | expect: Same shape, bigger extra hit: 12-22 against 6-12
- [ ] `TG4` (qa.md:5332) step: Judge whether it makes the fight more readable or just longer | say: - | expect: The row that decides whether this stays
- [ ] `BS10` (qa.md:5464) step: `1 Barcelona/Slave Pits` at low level | say: - | expect: Survivable. If a level-2 character is being killed by 25 percent backstabs here, drop the base tier to 0.15 before anything else
- [ ] `SP4` (qa.md:6379) where: **The regression.** Slave Pits, wound the slavers | steps: - | pass: No caltrops from any `Thug`. They are not guild thieves, and 0.97.0 briefly gave them the drop

**Slave Pits / Javier**

- [ ] `HH59` (qa.md:6159) where: Finish the slavers, by force and by talk, and be knighted by Javier | steps: - | pass: The Templar theme starts under *"I am proud to bestow upon you the title of Knight"* on every route, and the game's music returns normally afterwards -- *Music: listen only.*

**Slave Pits exterior yard**

- [ ] `SP5` (qa.md:6381) [eyes + save] where: Leave the pits, come back through the exterior | steps: Walk to the yard | pass: Five captives and the buyer stand there, idle, and none of them fights
- [ ] `SP6` (qa.md:6382) where: Same, goblins | steps: Look at them | pass: They animate as goblins, not frozen or in a T-pose
- [ ] `SP7` (qa.md:6383) [save] where: Don Alfonso | steps: **Free** | pass: His thanks, 300 gold, +50 karma, he disappears. **Karma must not also fall by 100**: this row proves the `Gone` guard
- [ ] `SP8` (qa.md:6384) [save] where: Reload, Don Alfonso | steps: **Sell** | pass: His line, 750 gold, -75 karma, he disappears
- [ ] `SP9` (qa.md:6385) [save] where: Reload, Don Alfonso | steps: **Kill** | pass: He dies at once and karma falls by 100, once
- [ ] `SP10` (qa.md:6386) [eyes + save] where: Reload, a Sylvant | steps: Attack with a weapon rather than the reply | pass: If the game lets you, the kill costs 125 karma. Note if it will not let you target them
- [ ] `SP11` (qa.md:6387) [eyes + save] where: After any choice | steps: Leave and come back twice | pass: Nobody who was freed, sold or killed returns, and nobody is doubled. This row proves `Placed`

**Temple District**

- [ ] `SR18` (qa.md:826) where: Temple District | steps: Enter the district at all | pass: Loads normally. Two entities were added to a map with 1028
- [ ] `SR19` (qa.md:827) steps: Machiavelli's door, and the **unnamed door at (1034,499)** the first attempt used | pass: Machiavelli's still opens into the House of Ilk map. The other is inert and unnamed again, exactly as vanilla ships it
- [ ] `SR20` (qa.md:828) steps: The Cathedral, Shylocke, the Inquisition doors, the sewer entrance | pass: All still work
- [ ] `SR21` (qa.md:829) steps: The **other** Temple District robbery -- Juanita's node 124 job with her key | pass: Unaffected. It is a different house and a different quest
- [ ] `SR23` (qa.md:831) where: Temple District, the yard gate | steps: Walk up to the iron gate at (3365, 2504) | pass: It is passable. The swapped `FenceDoor2` sprite is 3x wider than the piece it replaced, so also check it sits in the fence run rather than overhanging it
- [ ] `SR24` (qa.md:832) steps: Walk from the gate to the house doorway | pass: A continuous walkable route, without going round the outside. The waypoints show a band at y 2483-2540 and nothing between 2363 and 2483, which should be the house itself
- [ ] `SR25` (qa.md:833) [eyes + save] steps: Rob the house cleanly, then walk the district | pass: **No** guards appear anywhere. There are **27** entities named `Temple Guard Reserves` and name-targeted actions broadcast, so a mistake here spawns guards across the whole district, not just at the yard. The new post is uniquely named to avoid that
- [ ] `AT1` (qa.md:2898) step: **The row that matters most.** Walk into the Temple District at all | say: - | expect: **No crash.** Torquemada's node id ends in a space and a can naming a node is matched byte-exactly; getting it wrong is a load-time crash, not a missed line **PASSED** -- *"temple district loads"*, 2026-10-16, on 0.64.0 verified deployed (`'1000 attack torquemada '` read back from data.dat with its trailing space) -- *Passed on 0.64.0; any visit re-checks it.*
- [ ] `CV9` (qa.md:3324) step: **The regression row that matters most.** Attack Cervantes yourself in the Temple District | say: - | expect: The district still reacts exactly as before -- his damaged slot relays `Damage a guard in the Temple district`. His bark bank was **wrapped beside** that action, never over it. If the guards stop caring, the wrap is wrong and this is a real bug
- [ ] `PK5` (qa.md:3636) [save] where: **Proves half two.** Kill any ordinary Inquisition member -- a generic inquisitor in the Temple District will do | steps: Check the sheet | pass: **Enemy of the Inquisition** is listed
- [ ] `PK6` (qa.md:3637) where: After `PK5`, talk to any other inquisitor | steps: - | pass: From *"Greetings, child"*, a new reply leads to the ledger-and-arithmetic line
- [ ] `MA6` (qa.md:3673) where: **The composition.** Accept at level 5+, then leave the house to trigger the ambush | steps: Look at the four attackers | pass: Four snake-women, not four identical ones: **one visibly larger** leader near the door, two of the same smaller build, and one that **attacks from range** rather than closing
- [ ] `MA7` (qa.md:3674) [eyes + save] where: During the ambush, read the name under any attacker | steps: - | pass: It is **no longer "Demokin"**. That label was the player race leaking through
- [ ] `MA9` (qa.md:3676) where: **The judgement row.** Play the ambush properly at level 5 and try to keep Machiavelli alive | steps: - | pass: He survives if you play well. He has **AC 40 / HP 35**, so he is meant to be genuinely at risk -- but if he dies even when you fight well, level 5 is too low and the gate needs raising
- [ ] `MA10` (qa.md:3677) where: Watch the ranged one specifically | steps: - | pass: It spits at range for piercing and poison damage. Judge whether it can reach Machiavelli past you from the far corner -- that is the one new threat vector this release adds
- [ ] `MA12` (qa.md:3679) where: Save Machiavelli, then talk to him | steps: - | pass: His thank-you plays, he asks you to let him go, and the Barcelona reward is paid as shipped
- [ ] `MA14` (qa.md:3681) where: **The control.** Deliberately let him die, or refuse the task entirely and continue the game | steps: - | pass: The failure and refusal paths behave exactly as they always have. Only the enemies and the gate changed
- [ ] `BU53` (qa.md:4797) step: Take it to **Shylocke** in the Temple District, from `5 Questions` | say: *"I hold the deed to a silver mine…"* | expect: `700 the deed` -- *"You are selling me a hole in the ground full of creatures, and the law of Spain agrees the hole is yours to sell. Twelve hundred, and I will never visit it."*
- [ ] `BU54` (qa.md:4798) [eyes + save] step: Accept at the opening price | say: *"Done."* | expect: **1200 gold**, the deed leaves your inventory
- [ ] `BU55` (qa.md:4799) [eyes + save] step: With **Barter 40**, haggle | say: *"It pays whether you go or not. Eighteen hundred."* | expect: **1800**
- [ ] `BU56` (qa.md:4800) [eyes + save] step: With **Barter 70** | say: *"…you know what the smiths pay for what comes out of it."* | expect: **2500**, which is vanilla's own ceiling for a dialogue payout
- [ ] `BU57` (qa.md:4801) step: Sell it, then try to sell it again | say: - | expect: **Not offered.** The deed is removed on all three price routes, so there is no selling it twice
- [ ] `TD1` (qa.md:5915) step: **A save that has never entered the Temple District.** Enter it from the Gate District | say: - | expect: A named guard stands a few steps inside the gate; talking to him gives *"Greetings stranger. I hope your day in the Temple District is a pleasant one."* Leave the map and come back: *"Hello again citizen."*
- [ ] `TD2` (qa.md:5916) step: TD1, ask who is allowed inside | say: *"Who is allowed inside these walls?"* | expect: The restriction speech, then *"What do you mean by tainted citizens?"* gives the pointed-teeth-and-cat-eyes explanation
- [ ] `TD3` (qa.md:5917) step: TD1 as a Feralkin, Sylvant or Demokin | say: *"You are looking at a tainted citizen standing on holy ground."* | expect: `30 tainted`: he does not challenge or attack; he asks that an Inquisitor not hear of it. A human never sees the reply
- [ ] `TD4` (qa.md:5918) step: TD1, then cast a spell or strike a guard in the district | say: - | expect: Pablo reacts exactly as the other Temple Guards do (spellcast detected, the damaged-guard relay); he must not be the only guard who ignores it
- [ ] `TD5` (qa.md:5919) step: TD1, walk past him repeatedly and leave the district and return | say: - | expect: He never blocks passage, never demands a donation, and the outer gate guard's scene is unchanged
- [ ] `TD6` (qa.md:5924) step: Temple District, Lord Javier, before beginning the initiate quest | say: His initiate replies | expect: The gate that reads "initiate quest NOT begun" now resolves; check the pre-quest and post-quest branches differ

**Temple District (Cervantes)**

- [ ] `TD19` (qa.md:1227) where: Cervantes, Temple District | steps: Talk to him, walk away, talk again | pass: The **second** conversation opens `3 Return Dialogue` -- *"It was just here! Perhaps you saw it this time?"* -- with its four replies

**Temple District (Lord Javier)**

- [ ] `LJ2` (qa.md:3040) step: Same run, watch the gear icon | say: - | expect: It clears. If it is still spinning after the fade, the relay did not fire
- [ ] `LJ3` (qa.md:3041) step: **Regression, the main path.** Take *"I am ready to depart for Montserrat."* straight away | say: - | expect: Unchanged, exactly as it always worked
- [ ] `LJ4` (qa.md:3042) step: **Regression, the vanilla detours.** Ask about the Crown of Thorns and about the relics, then depart | say: - | expect: Both still loop back to the directions node and the scene still ends
- [ ] `LJ5` (qa.md:3043) step: Check the Lance text itself | say: - | expect: Unchanged. Only where the reply goes changed, and no line in the tree was rewritten
- [ ] `LJ6` (qa.md:3044) step: Afterwards, talk to Javier again in the Temple District | say: - | expect: Normal return dialogue. The quest is live and nothing about the knighting or the faction paths moved

**Temple District (Raphael)**

- [ ] `AT5` (qa.md:2902) step: Attack Raphael in the Temple District | say: - | expect: *"To the hellfire with you, heathen!"*

**Temple District (any inquisitor)**

- [ ] `FJ6` (qa.md:3537) where: **The reaction.** Carry the Journal and talk to any ordinary inquisitor | steps: Read the replies | pass: A new reply offers to tell him you are carrying an account of what his order did to a feralkin. Taking it gets his answer about the wretch having written it *alive*
- [ ] `FJ7` (qa.md:3538) [save] where: After `FJ6`, check your inventory | steps: - | pass: **You still have the book.** He demands it and nothing takes it -- that is deliberate. If the Journal is gone, something is wrong
- [ ] `FJ9` (qa.md:3540) where: Without the Journal, talk to an inquisitor | steps: - | pass: The new reply is **absent**. It is gated on actually carrying the book. The 0.47.0 *"Enemy of the Inquisition"* reply, if you have earned that title, is unaffected and still works
- [ ] `FJ10` (qa.md:3541) where: Judge the **scene**, which no check settles | steps: Do `FJ6` as a feralkin character, if you can | pass: Does his answer land? He is being shown an account of his own order's cruelty and refuses the accusation rather than denying the facts. If it reads as toothless, the node is worth rewriting

**Temple District (walled yard)**

- [ ] `SR1` (qa.md:796) where: Temple District, the walled yard | steps: Walk through the iron gate at the far end of the district and into the arched doorway of the house inside | pass: You load into a room. **A crash, a hang or a black screen here is the whole test failing**
- [ ] `SR6` (qa.md:801) steps: Walk into the doorway again | pass: You go back in. It is not a one-shot
- [ ] `SR27` (qa.md:873) steps: Take it with **PE 4 or lower and Find Traps under 35** | pass: Step outside and a guard is there: *"You came out of a house that is not yours, carrying something that is not yours, and you did not even have the sense to do it quietly."*
- [ ] `SR28` (qa.md:875) steps: Same, but check the timing | pass: He appears at the doorway you came out of, not somewhere across the yard, and the conversation opens by itself
- [ ] `SR29` (qa.md:876) where: The guard | steps: *"You will not take me anywhere."* | pass: He turns hostile and fights. Killing him leaves you free, and you keep the cache

**Temple District / 08 Final Encounter**

- [ ] `DN11` (qa.md:4897) [save] step: **Galileo** in the Temple District, and again in `08 Final Encounter` | say: - | expect: **"Galileo"** both times. He shared Leonardo's race in Barcelona and the endgame pair race at the end, so he was reading *River Dryad* and then *Leo* -- *0.60.3 found the log prints the can's User Assigned Name, not the race name this release edited. Expected names here came from race names, but 0.60.3 found the log prints the can's User Assigned Name (a hat goblin logs Goblin Striker). A different name is not a failure on its own; check it against the can.*

**Temple District yard / Inquisition Chambers2**

- [ ] `SR30` (qa.md:877) steps: *"I will come quietly."* | pass: Screen fades, controls lock, and you wake in the Inquisition prison with Sanchez talking at you

**Temple District, Machiavelli's house**

- [ ] `MA1` (qa.md:3668) where: Temple District, Machiavelli's door. Talk to him on a **new game**, below level 5 | steps: Pick any of mercenary / soldier / general, reach his task offer | pass: He describes his dangerous opponents as shipped. The conversation works exactly as before
- [ ] `MA2` (qa.md:3669) where: **Half one of the gate.** Same conversation, still **under level 5** | steps: Read every reply on the task offer | pass: *"I'm interested. You can count on me for support."* is **absent**, and a new reply *"I could not protect you as I am. Not yet."* is present. Choosing it gives his refusal line about buying company in the grave. **Not a pass on its own -- see MA3**
- [ ] `MA3` (qa.md:3670) where: **Half two, and the one that matters.** Reach **level 5**, return and talk to him again | steps: Use his return greeting, then ask about work | pass: *"I'm interested..."* is now **present** with its quest icon, and the *"I could not protect you"* reply is **gone**. If the offer is still missing at level 5, the level check is not resolving and the release must be pulled
- [ ] `MA4` (qa.md:3671) [save] where: After `MA3`, accept the task | steps: - | pass: The quest `Task for Machiavelli` activates in your log exactly as it always did
- [ ] `MA5` (qa.md:3672) where: **The lockout check.** Before reaching 5, exhaust his conversation -- refuse, leave, come back, refuse again | steps: - | pass: He never runs out of replies, the goodbye option is always there, and returning later still leads back to the offer. The quest must never become permanently unavailable

**Temple District, Shylocke**

- [ ] `LU12` (qa.md:3846) where: **Shylocke**, Temple District. Reach his *favors you* return greeting | steps: - | pass: Audible -- 91 KB. Unrelated to Lucius; same filename-drift cause

**Temple District; Montaillou**

- [ ] `HH52` (qa.md:6152) [eyes + save] where: After either deal | steps: Temple District, then Montaillou | pass: Neutral everywhere

**Temple Ilk Store Room**

- [ ] `SR2` (qa.md:797) where: Inside | steps: Look around | pass: A furnished Barcelona interior, walls and floor drawn normally, no missing geometry or holes
- [ ] `SR3` (qa.md:798) steps: Walk to each corner, and around the table and shelves | pass: Pathing works and the character routes around furniture. Getting stuck, walking through a prop, or refusing to move is a **navmesh mismatch** -- report it
- [ ] `SR4` (qa.md:799) steps: Open the map / minimap | pass: The automap draws. A blank or garbage automap is a `.frm16` problem, not a quest problem
- [ ] `SR12` (qa.md:812) [eyes + save] where: The store room | steps: Look at the floor **just south of the bookshelf** | pass: A glint at (568,509). Click it: **250 coin**, **50 XP**, and the journal advances to *"Tell Juanita about Temple District success"*
- [ ] `SR12b` (qa.md:813) steps: Check it does not fight the exit | pass: It sits 138 units clear of the exit area. It previously sat at (486,681), inside that area, so clicking it competed with leaving the room -- found in play
- [ ] `SR13` (qa.md:814) steps: Do SR12 on **any** build, however low PE and Find Traps | pass: It is there and it is clickable. Finding the cache is not skill-gated at all; skill only decides whether the guard is waiting outside (SR26/SR27)
- [ ] `SR13b` (qa.md:815) [eyes + save] steps: Enter the room with **no quest at all**, any skill | pass: **There is no secret in the room.** The cache is `Active=0` until the spawn point sees the quest state. A passer-by finds the bookshelf potion and has no reason to think anything of the place
- [ ] `SR14` (qa.md:816) steps: The bookshelf, on any character | pass: Gives a random potion, exactly as it does in `Port House Near Warehouse`. It is byte-identical to vanilla and carries no quest wiring
- [ ] `SR26` (qa.md:872) where: The store room | steps: Take the cache with **PE 5+ or Find Traps 35+** | pass: You leave unchallenged. No guard, no dialogue. This is a separate, scripted check from the one that reveals the cache -- finding it is the engine's job, being *seen* is this one
- [ ] `SR27b` (qa.md:874) steps: Rob the house **before** Juanita ever mentions it, then take the job and go back | pass: The cache is there when you return. It was never present to be consumed early -- this was a genuine soft-lock until the cache was gated on the quest

**Temple Ilk Store Room / Temple District yard**

- [ ] `SR5` (qa.md:800) steps: Leave by the exit at the edge of the room | pass: You land back inside the yard, on walkable ground, near the doorway you came in by -- not outside the fence

**Thieves Congregation / sewers**

- [ ] `CT9` (qa.md:4304) step: **The balance row.** A crowded fight: the Thieves Congregation, or a sewer room with five thieves | say: - | expect: Five patches at most, one each. Judge whether the floor becomes unmanageable. The dials are radius 55 and the damage, not the number of layers

**Torquemada's chambers**

- [ ] `HH1` (qa.md:6101) where: His chambers, **before** Montserrat. Admit to the taint and reply *"You are the one who will burn"* | steps: Listen | pass: The full 14 seconds, **voiced**, then jail. **You must not see "Perhaps some time in a cell"**
- [ ] `HH2` (qa.md:6102) where: Same | steps: Hit him instead of talking | pass: As before: the cell line, then jail. This is the regression on vanilla's behaviour
- [ ] `HH3` (qa.md:6103) where: Same | steps: Cast a spell near him as a magic user | pass: *"Magic use has been detected!"* and jail, unchanged
- [ ] `HH4` (qa.md:6104) where: **Before** Montserrat | steps: Look at his replies | pass: *"I have come to end you"* is **absent** at every greeting
- [ ] `HH5` (qa.md:6105) where: **After** Montserrat, any faction | steps: Talk to him at each greeting you can reach | pass: The reply is present, with a fight icon
- [ ] `HH6` (qa.md:6106) [eyes + save] where: Same | steps: Take it | pass: The speech, then a fight. **He attacks you**, two guards arrive, and *"Arrogant fool! Guards! Restrain this heretic!"* plays. You must **never** be jailed. This is the row that proves the release
- [ ] `HH7` (qa.md:6107) where: Same | steps: Hit him instead | pass: The same fight with no speech
- [ ] `HH8` (qa.md:6108) where: Same, as a mage | steps: Damage him with a spell | pass: It lands. In vanilla `Spell Immunity` would have blocked it
- [ ] `HH9` (qa.md:6109) where: Hurt the pit guards first, then start the fight | steps: Let the guards reach you | pass: Still no jail. The chase poly fires on enemies and the fight has to disarm it
- [ ] `HH10` (qa.md:6110) [eyes + save] where: Leave mid-fight and return | steps: - | pass: **Reversed in 0.96.0.** He and his guards are still hostile, and so is everyone in `HH46`. There must be no duplicate guards -- *Pass text already reflects the 0.96.0 reversal.*
- [ ] `HH11` (qa.md:6111) [save] where: **Kill him as an Inquisitor** | steps: Check perks and journal | pass: **Dark Inquisitor** and **Enemy of the Inquisition**. `Create a Rod` and `Slay the Goblin Khan` fail if open
- [ ] `HH12` (qa.md:6112) [save] where: **Kill him as anyone else** | steps: Check perks | pass: **Breaker of the Hammer** and **Enemy of the Inquisition**, and not Dark Inquisitor
- [ ] `HH13` (qa.md:6113) [eyes + save] where: Leave and come back | steps: - | pass: He stays dead, and the Old Man cutscene does not play over the empty room
- [ ] `HH16` (qa.md:6116) where: **Judgement.** Fight him at the level you reach him | steps: Is 260 HP / AC 225 right? Does he feel like the head of the Inquisition, or a tall guard? | pass: The stats are a starting number, and he carries no unique reward. Say what it wants -- *Judgement row.*

**Trapped Ether Plane**

- [ ] `EB2` (qa.md:3908) [eyes + save] where: **Kill him.** Fight the Enchanter to death as in vanilla | steps: - | pass: He drops `Kublai Khans Sword` and gold, exactly as before. **Nothing in this release may change this route**
- [ ] `EB3` (qa.md:3909) where: **Talk him to death.** The `63/65 Self Destruct` route | steps: - | pass: Unchanged from vanilla; he destroys himself and the crystal powers
- [ ] `EB4` (qa.md:3910) [eyes + save] where: **Spare him.** Take `50 Escape` -> `55` -> `57` -> `59 Winner` without insulting him | steps: - | pass: He spares you, then **`61 Fixt Bound Token`** fires and you receive the **Amulet of the Trapped Spirit**
- [ ] `EB5` (qa.md:3911) where: After EB4, leave the plane by powering the crystal from the spirits | steps: - | pass: You get out **with the Enchanter still alive**. This is the shipped route; confirm 0.39.0 did not break it
- [ ] `EB6` (qa.md:3912) where: After EB4, re-enter the plane and talk to him | steps: - | pass: He is non-hostile and opens at `05 Return Dialogue 1`
- [ ] `EB10` (qa.md:3916) [eyes + save] where: **The pact.** On Relican's path, with the Enchanter spared, talk to him | steps: - | pass: A `Quest Icon` reply offers the hidden city of wielders -> `70 Fixt Pact 1` -> `71 Fixt Pact 2`. You receive the **Ring of the Trapped Spirit**
- [ ] `EB11` (qa.md:3917) where: Try EB10 **without** having joined Relican | steps: - | pass: The pact reply is **absent**. It is gated on the Dark Wielder initiation having been activated
- [ ] `EB13` (qa.md:3919) where: Try EB12 **without** the shell in inventory | steps: - | pass: The reply is absent. It is gated on holding the shell *and* being at the bind step
- [ ] `EB17` (qa.md:3923) [eyes + save] where: **The bluff route completes the pair.** Resolve him by the `40 Barter` -> `43` -> `45 Barter 3` bluff instead of `59 Winner`, then take the pact | steps: - | pass: You receive **both** items, not just the ring. `Trigger Only Once=1` must yield **exactly one** amulet -- if two arrive, the guard failed

**Trapped Ether Plane (Enchanter)**

- [ ] `CP1` (qa.md:1339) where: Trapped Ether Plane, the Enchanter, `50 Escape` | steps: *"The crystal you fashioned. It only needs enough energy..."* -> the continue replies at 55 and 57 | pass: `59 Winner`; he stands down and *"I am still watching you"* on a click; the undead stay hostile; the lie route and `53 Whoops` unchanged

**Weng Choi or the Herbalist**

- [ ] `WV1` (qa.md:1871) step: Buy a Wand Charge from Weng Choi or the Herbalist | say: - | expect: **50 gold each**, not 10. At 10 a charge undercut every comparable potion; a Wand of Revelation cast did an 80-gold potion's job for 10

**Weng Choi's shop**

- [ ] `WV5` (qa.md:1875) step: **The open question.** Enter Weng Choi's shop, leave, wait past his 900-second restock, and return -- repeatedly. Watch the Wand Charge **and the arrow** stacks on his shelf | say: - | expect: **If his stacks grow each restock, the reported pile of 20 was merchant-side merging, not our stack size** -- and arrows would grow too, since they stack the same way at `Current Count=50`. If neither grows, the 20 came from somewhere else and this row is how we find out -- *Open question; observation only*

**Weng Choi; also Weird woman (Hamlet Burned), Witch Interior, Rogue Inquisitor (Plains)**

- [ ] `SD13` (qa.md:1693) step: Open **Weng Choi's** shop, the **Weird woman** in Hamlet Burned or the Witch Interior, or the **Rogue Inquisitor** on the Plains, and restock a few times | say: - | expect: Healing scrolls turn up. They stock the scroll pool, where Healing is now 22.1% of rolls. Before this the pool's most frequent entry was a Very Rare ward, so scrolls effectively never appeared

**Wilderness wolves, then Gate District (Quinn)**

- [ ] `Q3` (qa.md:991) [eyes + save] steps: Same **with** the Trapper perk | pass: The quality pelts are accepted too. **This is the case that was broken**: a Trapper gets `Wolf Pelt Perk Quality` and the turn-in only took the plain pelt, so the perk locked you out of the errand
- [ ] `Q3b` (qa.md:992) steps: Mix them -- some plain, some quality | pass: Any three count, in any combination

**a magic vendor (Weng Choi)**

- [ ] `SD3` (qa.md:1683) step: Check its price and its drop grade in a shop | say: - | expect: **50 gold**, and it now appears in scroll loot at all. It was graded `1 Common` and absent from every generator, so that grade had never been exercised

**anywhere in the act**

- [ ] `AT8` (qa.md:2905) step: **Regression.** Talk to all five normally, before attacking anything | say: - | expect: Their conversations are unchanged. Only the combat slot was touched
- [ ] `PK11` (qa.md:3642) [save] where: Kill a Knight of Saladin, or **Jafar** | steps: Check the sheet | pass: The Saladin title is listed. **This one was dead in vanilla too** -- its shipped grant sits on an inactive part that nothing activates
- [ ] `PK12` (qa.md:3643) where: After `PK11`, talk to a Knight of Saladin, ideally one who greets you with *"Word of your deeds have come before you, brother"* | steps: - | pass: The *"do not call me brother where the others can hear you"* reply is offered
- [ ] `PK15` (qa.md:3646) [eyes + save] where: **The control.** Play Barcelona normally, killing none of these factions | steps: - | pass: No faction title appears, none of the new replies is offered, and every one of these NPCs behaves exactly as before
- [ ] `LD16` (qa.md:3887) where: Judge the **writing**, which no check can verify | steps: - | pass: Does Relican's refusal to have him killed read as his own judgement rather than an engine limit? Does DaVinci's warning land as concern rather than a lecture? This is the only row that can fail on craft
- [ ] `WD8d` (qa.md:4023) [eyes + save] step: **The row that proves the gate is real.** Find any magic equipment in act 1 and check its rarity in the item description | say: - | expect: Never above Uncommon. If a Very Rare or Unique turns up early, the mojo list is not being consulted and the gating has failed
- [ ] `WD10` (qa.md:4026) step: Fight in act 1 and 2 and watch drops | say: - | expect: Changed only as much as those acts draw from `1 MASTER ALL Items in the game`. Most early maps use their own tables, so the shift should be smaller there
- [ ] `FN10` (qa.md:5221) [save] step: `python tools/savecheck.py grep "Fernand Is Waiting" --save latest` | say: - | expect: Absent. 0.25.4's scripting variable is deleted and nothing depends on it. **PASSED** -- absent in every save checked
- [ ] `FN11` (qa.md:5222) [save] step: **Save immediately after recruiting him, before releasing.** `python tools/savecheck.py grep "Original AIInteractionSpecifier" --save latest` | say: - | expect: **The decisive check, and it needs no release at all.** It must be present, and the specifier parked inside it must open `103 fernand waiting`. That is the engine's own restore slot -- Cervantes' holds `3 Return after release as a companion`. **PASSED** 10/01/26 -- parked and opening `103 fernand waiting`
- [ ] `FN12` (qa.md:5223) [save] step: In the same save, count his active specifiers | say: - | expect: **Exactly one**, the generic `Generic Companion Dialog` at `X Radius=30`. Two means the join race is back: the engine appended the overlay instead of swapping his out, nothing was parked, and release will have nothing to restore. **PASSED** 10/01/26 -- exactly one, the generic at `X Radius=30`
- [ ] `TH5` (qa.md:5247) [save] step: Take the hide to Quinn | say: - | expect: He takes it, removes it from the pack, and goes to `850 troll hide turned in`
- [ ] `BK1` (qa.md:5267) step: Fight thieves | say: - | expect: Floating text **over the thief's head**, not in the combat log
- [ ] `BK2` (qa.md:5268) step: Fight a thief **boss** and a thief **archer** in the same run | say: - | expect: Different registers. The boss gives orders -- *"Hold him! He is worth more breathing!"*; the archer talks range -- *"Keep your distance from him!"*
- [ ] `BK3` (qa.md:5269) step: Fight the same thief for a long stretch | say: - | expect: **It varies.** One creature should not repeat one line. This is the fault the first build had
- [ ] `BA22` (qa.md:5849) [eyes + save] step: **A save that has never entered the Gate District.** In peacetime Barcelona, kill one unarmed citizen | say: - | expect: **Slayer of Innocents** appears among your titles. Vanilla never granted this perk anywhere
- [ ] `BA25` (qa.md:5852) [eyes + save] step: Kill a vendor instead | say: - | expect: **Merchant Slayer**, as in vanilla. The two vendor cans are deliberately not wired to the new title
- [ ] `HH48` (qa.md:6148) [eyes + save] where: **The regression.** Never fight him | steps: Play Barcelona normally | pass: Nobody is hostile, jail still works, and every district's arrival still does what it did. The relay is on all 74 spawn points

## Sewers (171)


**01 Sewer Main Entrance**

- [ ] `AM6` (qa.md:3512) [eyes + save] where: The Sewers, `01 Sewer Main Entrance` | steps: Trigger the generator that used to give magic arrows | pass: It now gives **either** magic arrows or magic bolts. It is the one place that always gave enchanted ammunition and should still do so
- [ ] `BS1` (qa.md:5453) step: Walk into `Sewers/01 Sewer Main Entrance` and just **look** at a thief before fighting | say: - | expect: He appears normally, walks at normal speed, is visible and targetable. **If thieves are invisible, creeping, or missing, stop and revert** -- that means `Sneak Enabled` reached the engine's sneak state after all -- *Most important row: stop and revert if thieves are invisible or creeping.*
- [ ] `BS2` (qa.md:5454) [eyes + save] step: Fight a `Sewer Theif4 Sword` head-on, facing him | say: - | expect: No backstab line in the log. The facing condition needs at least 90 degrees of difference
- [ ] `BS3` (qa.md:5455) [save] step: Engage one thief, let a **second** close on you from behind, then **save** | say: - | expect: `python tools/savecheck.py events latest --backstab` prints a line with the **thief** as attacker: *"... sneaks up on ... and hits for ... (25 percent backstab bonus)"*. This is the whole point of the release. The log is a rolling 300 events, so save soon after the fight

**02 Thieves Congregation**

- [ ] `BS4` (qa.md:5456) [save] step: Same in `02 Thieves Congregation`, where 51 thieves spawn | say: - | expect: Same, and more often -- crowds make flanking happen by itself

**04 Hall of Beggars**

- [ ] `BP15` (qa.md:3410) step: Tell Enrique in the Hall of Beggars | say: - | expect: `713 the contract nobody paid` -- *"I am not going to ask you which."* He accuses you of nothing, and nothing is recorded from him

**05 Troll Pit**

- [ ] `BP1` (qa.md:3396) step: Make peace with the trolls by any route, then strike one | say: - | expect: **The chief comes and speaks.** Nothing happening is the exact failure this release exists to fix
- [ ] `BP2` (qa.md:3397) step: `BP1` having also stood the rite over the old chief (`The Chief Before` complete) | say: - | expect: `160 the peace broken rite` -- *"I told you a chief must be counted by one who was not there."* The deepest of the three, and it should beat the other two
- [ ] `BP3` (qa.md:3398) step: `BP1` having carried the ore terms and taken the first ore, **without** the rite | say: - | expect: `161 the peace broken ore` -- *"The same man each time. So we know the face."*
- [ ] `BP4` (qa.md:3399) step: `BP1` with neither -- only the case argued to Enrique | say: - | expect: `162 the peace broken word` -- *"Tell the men who sent you that we counted every time... There are none."*
- [ ] `BP5` (qa.md:3400) step: In any of `BP2`-`BP4`, look for a way to talk it back | say: - | expect: There is none. One reply, `<There is nothing you can say to this.>`, and **no Speech check anywhere in the scene**
- [ ] `BP6` (qa.md:3401) step: Watch the pit for the few seconds after he finishes | say: - | expect: The trolls near you come. The far side of the pit does not, until you go to it
- [ ] `BP7` (qa.md:3402) step: Count what engages at once | say: - | expect: A handful, exactly as `LT11` still requires. **If the whole pit converges the restore has been pushed instead of restored** -- that would mean a `CGoToCombatAction` is in the relay, and none should be
- [ ] `BP8` (qa.md:3403) step: Strike a second and a third troll | say: - | expect: No second speech. The relay is `Trigger Only Once=1`
- [ ] `BP9` (qa.md:3404) step: Let the fight run well past half a minute | say: - | expect: **Nobody goes idle again.** The `Troll Peace Keeper` is stopped before anything else happens; a troll that stops fighting after about twenty-four seconds means its two-second tick is still running
- [ ] `BP10` (qa.md:3405) [save] step: Open the quest log | say: - | expect: *The Peace You Brokered* is there, and it says nobody above was paying for this one
- [ ] `BP14` (qa.md:3409) step: Break the peace, survive, then walk onto the old chief's body field | say: - | expect: **Known overlap:** the desecration scene plays as well, because that relay is not gated on the peace. Recorded rather than patched blind -- report what it looks like
- [ ] `LT1` (qa.md:5155) step: Fight the drones | say: - | expect: Hover text over their heads, roughly one attack in four, broken and terse -- *"You no belong!"*, *"Hot now, yes?"* -- and sometimes a wordless line like *"<It grunts, and keeps coming.>"* -- *0.52.0 halved the swing bark rate to about 1 in 8.*
- [ ] `LT2` (qa.md:5156) step: Fight the chief | say: - | expect: A different register, measured and counting: *"I will count you with the others."*, *"Hold him. He is one and we are many."* **No drone should ever speak a chief line, or the reverse**
- [ ] `LT3` (qa.md:5157) step: Watch the ground when a troll connects | say: - | expect: The **Troll Stomp** effect plays. The radius-120 area pulse was always there; this is the first time it is visible
- [ ] `LT4` (qa.md:5158) step: Take a hit from the chief and count the damage lines | say: - | expect: Fire damage, one or two pulses of 6-16. That is the stomp, not a separate attack
- [ ] `LT5` (qa.md:5159) step: Wound a troll, then break off and watch it | say: - | expect: It **closes its own wounds** -- 0.6 HP/sec for a drone, 1.0 for the chief, against your own ~0.37. Visible over several seconds, not instant
- [ ] `LT6` (qa.md:5160) step: Fight the chief to the end with a **piercing** weapon | say: - | expect: Hard. Troll races resist piercing at 50 percent, and the simulation puts this near a coin flip
- [ ] `LT7` (qa.md:5161) step: Fight him again with **cold** | say: - | expect: Markedly easier: `Cold Damage Resistance=-15` is their one weakness and it already shipped in vanilla
- [ ] `LT8` (qa.md:5162) step: Hit a lone drone away from the others | say: - | expect: **The chief comes.** One ally, not the pit. Fires once per drone
- [ ] `LT9` (qa.md:5163) step: Hit a second drone | say: - | expect: The chief does not come twice. `COnlyOnceAction` is per troll, and he only has to arrive once
- [ ] `LT11` (qa.md:5165) step: Count the trolls that engage after an alarm | say: - | expect: A handful, never the whole level. The pit holds 80-94 trolls with a 4000 leash -- a group-wide call was built, measured, and deliberately cut back. **0.53.0 holds to this**: breaking the peace restores hostility rather than pushing a charge, so engagement is still bounded by the 550 acquisition range and not by the 4000 leash
- [ ] `LT12` (qa.md:5166) [save] step: Kill the chief | say: - | expect: The *Lava Troll Hide* still arrives in your pack (`TH1`). None of this touched the drop
- [ ] `TH1` (qa.md:5243) [eyes + save] step: Fresh Troll Pit. Kill the troll chief (the big one, any difficulty) | say: - | expect: *Lava Troll Hide* arrives **in inventory** with an on-screen notification. Not on the floor
- [ ] `TH2` (qa.md:5244) [save] step: Check the quest log | say: - | expect: `Troll Hide for Quinn` can now be completed. Killing him still completes `Destroy the Lava Troll Menace` as before
- [ ] `TH3` (qa.md:5245) step: Listen as he dies | say: - | expect: The sewer ambience still switches from monsters to quiet. The vanilla bookkeeping is untouched -- the give was appended, not substituted
- [ ] `TH4` (qa.md:5246) [save] step: Kill the ordinary trolls, tough and super included | say: - | expect: **No** hide from any of them. Only the chief carries one, deliberately
- [ ] `TH6` (qa.md:5248) [save] step: Peace route instead: ask the chief for a hide (`133 the hide`, or `30 troll trade`) | say: - | expect: He hands one over as before. Unchanged by this fix
- [ ] `TH7` (qa.md:5249) [save] step: Peace route, then desecrate the field and kill the angry chief | say: - | expect: A hide, exactly one. His generator got the same give, so both chiefs behave alike
- [ ] `TH8` (qa.md:5250) [save] step: Already hold a hide, then kill the chief | say: - | expect: A second one. Harmless, and the same as vanilla's behaviour for a Titan heart
- [ ] `BA26c` (qa.md:5842) [eyes + save] step: Attack **Tomas** in the troll pit | say: - | expect: He screams and flees; the title is granted

**Hall of Beggars**

- [ ] `W1` (qa.md:970) where: Sewers, Hall of Beggars, near Enrique Garcia | steps: Enter the map on a fresh character | pass: A wererat stands apart from the swarm and **does not attack**
- [ ] `W2` (qa.md:971) steps: Talk to him | pass: *"Since you are a friend of beasts, I'll give you some advice. Never trust a thief and beware of the lava trolls."*
- [ ] `W3` (qa.md:972) steps: Ask where the thieves are | pass: The eastern corridors, and a warning about traps
- [ ] `W4` (qa.md:973) steps: Ask where the lava trolls are | pass: The lower levels, and advice to avoid them
- [ ] `W5` (qa.md:974) steps: Leave and return | pass: He is still there and still talks
- [ ] `W6` (qa.md:975) steps: Attack him | pass: He fights back like any wererat. Nothing else in the map changes

**Hall of Beggars (Enrique)**

- [ ] `SF3` (qa.md:689) where: Hall of Beggars, Enrique | steps: Open the conversation, either greeting | pass: The reply is on **both** openings, not buried in a topic
- [ ] `SF4` (qa.md:690) steps: Deliver it | pass: Node 701 -- he gets faster and less comfortable
- [ ] `SF5` (qa.md:691) steps: **Speech 50+** | pass: *"You are paying to create the problem you are paying to solve"*
- [ ] `SF6` (qa.md:692) steps: **Barter 45+** | pass: The ledger argument. Both absent below the thresholds
- [ ] `SF7` (qa.md:693) steps: With **The Red Ore Trade** complete | pass: A third door, no skill needed -- the trade is worth more than the trolls are dead. **PASSED**, once the gate was made `completed OR current(final)`
- [ ] `SF8` (qa.md:694) steps: Without it | pass: That third reply is absent
- [ ] `SF9` (qa.md:695) [eyes + save] steps: Any of the three | pass: Contract withdrawn. `Destroy the Lava Trolls` shows **failed** if it was active, untouched if not
- [ ] `SF10` (qa.md:696) steps: Say nothing (node 703) | pass: He keeps the offer open. Nothing is lost
- [ ] `SF12` (qa.md:698) where: Hall of Beggars | steps: On `141 Lava Trolls 2`, decline | pass: **New in Fixt**: *"No. I will not hunt them for you."* Node 704 keeps a way back to the contract
- [ ] `SF13` (qa.md:699) [eyes + save] steps: Take the contract, kill the trolls anyway | pass: Vanilla's route is entirely unchanged
- [ ] `VR9` (qa.md:729) where: Enrique, node 701 | gate: `Templar IS` | pass: *"I am being lectured about mercy toward monsters. By a Templar."* And: you are the first one who asked them first
- [ ] `VR10` (qa.md:730) gate: `Inquisitor IS` | pass: He checks the chair for a trap. *"I am extremely listening."*
- [ ] `VR11` (qa.md:731) gate: `CH lessthan 6` | pass: The blunt version lands *better* -- he was braced for cleverness and got a fact
- [ ] `VR12` (qa.md:732) gate: Any of VR9-VR11 | pass: Returns to node 701. Speech / Barter / ore-trade routes all still reachable
- [ ] `MS24` (qa.md:1299) [eyes + save] where: Enrique, after the contract is withdrawn | steps: Either greeting | pass: *"You said there was one thing more you needed, before the trolls came between us."* -> his confession -> the cure quest, exactly as the kill route gives it. Absent once the cure quest has ever been given

**Sewer Main Entrance / Thieves' Congregation (stash chest)**

- [ ] `MS27` (qa.md:1302) [eyes + save] where: Thieves' stash chest (Main Entrance top-left, or Congregation SA1), Sneak below 25/30 | steps: Open it | pass: Loot drops, then *"Oi! Hands off the guild's take!"* over a thief, then the guild turns; the line is in the log
- [ ] `MS28` (qa.md:1303) [eyes + save] where: Same chest, Sneak at or above the threshold | steps: Open it | pass: Loot drops and *"<Nobody is looking your way...>"* over the chest; nobody turns
- [ ] `MS29` (qa.md:1304) [eyes + save] where: Same chest, Sneak below the threshold, every `Sewer Thief` on the map dead | steps: Open it | pass: Loot drops, no bark, nobody turns (Juanita and the dogs stay as they were)

**Sewers (Warning Troll)**

- [ ] `Q10` (qa.md:999) [eyes + save] steps: **Or**: settle the wererats first (cure them, or destroy the Beggars either way), then talk to the Warning Troll | pass: A new reply appears and he **gives** you a hide. The pit does not turn hostile
- [ ] `Q11` (qa.md:1000) steps: Same, wererats unresolved | pass: That reply is absent. Killing remains the only route

**Sewers entrance (Warning Troll)**

- [ ] `B12` (qa.md:377) where: Sewers entrance, **on** the Tomas quest | steps: Talk to the Warning Troll | pass: *"There is a child of my kind shut in your rock. Who do I speak to about it?"* on **both** `01 Greeting` and `20 no trust` -- *Reply text has since been reworded (now asks about a boy); match by node.*
- [ ] `B13` (qa.md:378) steps: Not on the quest, or debt already settled | pass: Both are absent
- [ ] `B14` (qa.md:379) [eyes + save] steps: Take the parley | pass: He points you deep, past the water. Peace comes on. `make troll mad` is switched off, so he does not re-aggro as you walk away
- [ ] `B15` (qa.md:380) steps: Walk to the chief and negotiate | pass: B1-B11 all reachable now
- [ ] `B16` (qa.md:381) steps: Open with *"I come in peace, Eduardo said..."* | pass: `20 no trust` is no longer a fight-or-leave dead end -- parley and the wererat route are both there

**Sewers stash; an ogre map with the charm**

- [ ] `XS13` (qa.md:6301) where: Sewers stash at low Sneak; break an ogre charm with ogres in view | steps: - | pass: *"Oi! Hands off..."* appears over the stash. The charm line comes from one ogre, which may be off screen, so note whether it reads as silent -- *Two unrelated balloons, in different acts.*

**Skulker**

- [ ] `VJ2` (qa.md:1722) [eyes + save] step: The same with **Strength 8 or more** | say: then *"Nobody in the sewers would miss a skulker. Pay more, or join the muck."* | expect: Node `65`: *"&lt;He does not reach for his knife, and takes a moment to decide that.&gt;"* and **50 more**, for 450. He pays the 400 first, so watch the counter move twice
- [ ] `VJ3` (qa.md:1723) step: **Negative.** VJ2, then leave and talk to him again | say: - | expect: The hand-over reply is **gone** and so is the threat. If either is still offered, the quest can be farmed and the release must be held
- [ ] `VJ5` (qa.md:1725) [eyes + save] step: The same with **Barter 40 or more** | say: then *"The door man saw nobody. That is worth more than this."* | expect: Node `64`: *"&lt;He counts it out twice, and does not look happy about the second time.&gt;"* and **200 more**, for 700
- [ ] `VJ6` (qa.md:1726) [save] step: **Negative, and the row the whole feature turns on.** Walk VJ1 and VJ4 on the same character in two saves and compare the totals | say: - | expect: **400 against 500.** If both pay 400 the manner flag is never written; if both pay 500 it is written on the hostile route too. Either way every other row above still passes, which is why this comparison is the test -- *The row the feature turns on*
- [ ] `VJ7` (qa.md:1727) step: **Negative.** Kill the door man, then hand the box over on a character with **Barter 40+** | say: - | expect: No haggle reply. The premium is for discretion; with a body on the floor he is not in a haggling mood, and the Barter push lives only on node `63`

**Skulker / thieves' vault**

- [ ] `VJ1` (qa.md:1721) [eyes + save] step: Take the job, kill the door man, take the box, hand it over with **Strength under 8** | say: *"I have your strongbox."* | expect: Node `62`, **400 gold**, 600 xp, and then **no further reply but the exit**. The threat must not be offered
- [ ] `VJ4` (qa.md:1724) [eyes + save] step: Talk the door man aside (Thief Friend or Speech 40), bribe him the hundred, **or** slip past on Sneak 35. Take the box, hand it over with **Barter under 40** | say: *"I have your strongbox."* | expect: Node `63`: *"&lt;He weighs the box, then adds a second handful.&gt; Door man saw nobody."* and **500 gold**. All three quiet routes must read the same

**Thieves' Congregation (Juanita)**

- [ ] `SR7` (qa.md:807) [eyes + save] where: Juanita, after handing over the Port District dues | steps: Take the reward | pass: She still gives the **Bracers of Stealthy Cunning** and the **Thief Friend** perk, and prints "You have become a friend of the thieves." The rewards come *before* the new job and cannot be missed
- [ ] `SR8` (qa.md:808) steps: Continue | pass: She offers the final job: *"Now, for the final task. In the Temple District there is a prime location"*
- [ ] `SR9` (qa.md:809) steps: Choose *"Another time. I have business elsewhere."* | pass: Goes straight to the seduction, exactly as it did before this change. **This is the regression case** -- declining must lose nothing
- [ ] `SR10` (qa.md:810) steps: Choose *"Consider it done. Where am I going?"* | pass: She names a walled yard with an iron gate at the far end of the district, says the gate stands open, mentions a guard, and warns that what she wants will not be sitting out on a table
- [ ] `SR16` (qa.md:819) [eyes + save] return after sr12: Take it | a new reply: *"the house by the flags is lighter than it was. this was in it."*: Quest completes, **500 XP** (the same as her other jobs), and the conversation moves to the seduction
- [ ] `SR17` (qa.md:820) [eyes + save] return after sr12: Talk to her again | a new reply: *"the house by the flags is lighter than it was. this was in it."*: The turn-in reply is gone. No double completion, no double XP
- [ ] `SR33` (qa.md:880) where: Juanita, after being jailed | steps: Hand in the job | pass: She is disgusted -- *"you sat in Sanchez's prison with my name in your mouth and my errand in your pocket"* -- and demands **300**
- [ ] `SR34` (qa.md:881) [save] steps: Pay the 300 | pass: You stay a member. The debt does not come up again
- [ ] `SR35` (qa.md:882) [eyes + save] steps: Say you do not have it, leave, come back | pass: The debt is still there as a reply on her hub. It does not quietly vanish
- [ ] `SR36` (qa.md:883) steps: With the debt unpaid or paid, try for the seduction | pass: **She refuses either way.** Being jailed on her errand ends that possibility permanently -- the fee buys membership, not forgiveness
- [ ] `SR37` (qa.md:884) where: Juanita, after fighting the guard off | steps: Hand in the job | pass: She takes you to bed as normal, but first: *"a dead guard at a rich man's gate is a thing people ask questions about. Next time you go quiet or you do not go."*
- [ ] `SR38` (qa.md:885) where: Juanita, clean job | steps: Hand in the job | pass: Neither speech appears. Straight to the seduction, exactly as before this branch existed
- [ ] `SR39` (qa.md:914) where: Anywhere | steps: Get jailed for something **unrelated** -- provoke Eduardo, the Church, Inquisition Foyer1, the Knights Templar or the Crossroads -- then go and see Juanita | pass: **She does not care at all.** No disgust, no fee, seduction still available
- [ ] `SR40` (qa.md:915) [eyes + save] where: Juanita, after the seduction | steps: Sleep with her on **CH 9 or better** | pass: An on-screen line: *"You wake refreshed, and alone. Juanita has gone about her business."* Without it she simply vanishes and nothing explains it -- found in play
- [ ] `SR41` (qa.md:916) [eyes + save] steps: Sleep with her on **CH under 9** | pass: *"You wake refreshed, and alone. Your purse feels lighter than it did."* **She robs you**, scaled to what you carry -- up to 500 gold
- [ ] `SR42` (qa.md:917) [save] steps: Count your gold before and after SR41 | pass: The loss matches one of vanilla's brackets: 500 / 400 / 300 / 200 / 100 / 50 / 25, or nothing under 25

**Thieves' Congregation (Juanita) / Port District**

- [ ] `SR22` (qa.md:830) where: Juanita | steps: The henchman shakedown: refuse to pay the 150, meet the thug in the Port District, pay him, return | pass: Node 230 still opens and still leads to the seduction

**Troll Pit**

- [ ] `B1` (qa.md:348) where: Troll Pit, **on** the Tomas quest | steps: Talk to the alpha | pass: A new reply: *"There is a child of my kind shut in your rock"* -- *Reply text has since been reworded ("I am looking for a human child"); match by node.*
- [ ] `B2` (qa.md:349) steps: Not on the quest | pass: That reply is **absent**
- [ ] `B3` (qa.md:350) steps: Ask his price | pass: Two hundred gold -- *"Not for the boy. For the times before, when we did not catch him"*
- [ ] `B4` (qa.md:351) [eyes + save] steps: Pay it (needs 200) | pass: 200 taken, the pit stands down, XP
- [ ] `B5` (qa.md:352) [eyes + save] steps: **Barter 40+**, with 100 gold | pass: 100 taken instead. The reply is absent below Barter 40 or under 100 gold
- [ ] `B6` (qa.md:353) steps: **Speech 45+** | pass: He concedes for nothing -- *"A child. Yes. Sent by men who are not"*
- [ ] `B7` (qa.md:354) steps: Refuse and threaten him | pass: Combat, and the peace switches **off**
- [ ] `B8` (qa.md:355) where: After settling any way | steps: Walk the pit and find Tomas | pass: No fighting needed. He leaves under his own power, as vanilla
- [ ] `B9` (qa.md:356) steps: Tell Tomas you did **not** kill the trolls | pass: *"That's too bad. I was looking forward to getting revenge."* Vanilla's own line, and the sting the peaceful route earns
- [ ] `B10` (qa.md:357) steps: Talk to the alpha again | pass: The offer is gone -- it is gated on the debt being unsettled
- [ ] `B11` (qa.md:358) [save] steps: Check gold after B4/B5 | pass: Taken exactly once. Reloading and re-settling must not charge twice
- [ ] `O1` (qa.md:415) where: Troll Pit, peace **not** made | steps: Talk to the chief | pass: The ore reply is **absent** -- it is gated on the peace being live
- [ ] `O3` (qa.md:417) steps: Hear him out | pass: Node 100, then his four terms: dig and stack, one man in daylight, paid in **iron not coin**, the same face each time
- [ ] `O4` (qa.md:418) [save] steps: Accept | pass: Quest **The Red Ore Trade** appears at state 1
- [ ] `O5` (qa.md:419) [eyes + save] steps: Talk to the chief again | pass: The offer is **gone**. If it reappears the marker gate failed and the quest can be walked backwards
- [ ] `O12` (qa.md:426) [save] steps: Take it | pass: **Red Ore** in inventory, quest state 3, **1509 XP** -- *The ore now comes from the pit chest (TP1, line 1326).*
- [ ] `O13` (qa.md:427) [save] steps: Talk to him again | pass: Nothing repeats. No second ore, no second grant
- [ ] `O14` (qa.md:428) [save] steps: Check Davinci's quest | pass: The ore behaves exactly as looted ore does -- this adds an item, it does not touch `3KL9W1JQ`
- [ ] `CB2` (qa.md:585) steps: Peace **not** made | pass: That reply is absent
- [ ] `CB3` (qa.md:586) [eyes + save] steps: Hear him out | pass: Node 111: a chief is counted by one who was not there. Quest **The Chief Before** at state 1
- [ ] `CB4` (qa.md:587) [eyes + save] steps: Talk to him again | pass: The offer is gone -- marker-gated, cannot run backwards
- [ ] `T1` (qa.md:948) where: Troll Pit, wererats **not** settled | steps: Walk in | pass: Vanilla: the Warning Troll confronts you, the pit is hostile
- [ ] `T2` (qa.md:949) steps: Take a Fight-icon reply | pass: Combat, exactly as vanilla
- [ ] `T3` (qa.md:950) [eyes + save] where: Troll Pit, wererats **settled** | steps: Talk to the Warning Troll, take the trade | pass: He gives the hide **and the pit stands down**
- [ ] `T4` (qa.md:951) steps: Walk the **whole** pit, southern path included | pass: Trolls spawning ahead of you settle within a second or two. None of them attacks
- [ ] `T5` (qa.md:952) steps: Click an ordinary troll | pass: It **grumbles** -- one of three lines. It does not attack, and it is not inert
- [ ] `T6` (qa.md:953) steps: Click the **alpha** (taller, different model) | pass: A conversation, not a grumble
- [ ] `T8` (qa.md:955) [eyes + save] steps: After breaking it, walk on | pass: Newly spawned trolls stay hostile -- the keeper is off
- [ ] `T9` (qa.md:956) steps: Look for the dead boss corpse | pass: Still lying there, untouched by any of this
- [ ] `TP1` (qa.md:1326) [eyes + save] where: Troll Pit, at peace, the Red Ore Trade carried to the chief | steps: *"I will see he keeps to it. <Go and take it.>"* | pass: The chest across the pit opens with the ore sound; one Red Ore on it; the trolls do not move
- [ ] `TP2` (qa.md:1327) [eyes + save] where: Troll Pit, at peace, chief alive, ore not yet paid | steps: Open the ore chest | pass: *"That is ours"* over the chief, then the desecration scene and the trolls turn
- [ ] `TP3` (qa.md:1328) [eyes + save] where: Troll Pit, fought in, no peace | steps: Open the ore chest | pass: Plain: animation, one ore, no reaction

**Troll Pit (Warning Troll)**

- [ ] `AU1` (qa.md:507) where: Warning Troll, `20 no trust` | steps: Character who has done **nothing** about the wererats | pass: The *"wererats are finished"* reply is **absent**. Before this it was ungated -- see below
- [ ] `AU2` (qa.md:508) steps: On Quinn's hide quest, wererats resolved, no hide held | pass: It appears, exactly as on `01 Greeting`

**Troll Pit (chief)**

- [ ] `AU3` (qa.md:509) where: Troll chief, ore offer | steps: Never took Eduardo's or DaVinci's Red Ore quest | pass: *"Is there anything your people need from the city?"* -- the player claims nothing. The **chief** names the ore and names Eduardo
- [ ] `AU4` (qa.md:510) steps: Then hear the terms | pass: *"The smith sends one man"* now has an antecedent
- [ ] `AU5` (qa.md:511) steps: Rite offer | pass: *"There is a dead troll out on the rock bigger than any I have seen standing. Who was he?"* -- an observation. Node 110's *"You have seen it. Good"* now answers something
- [ ] `AU6` (qa.md:512) steps: Speak-for-us offer, **never having met Enrique** | pass: The player asks who sent the bodies; the chief answers *"Enrique Garcia. The one who keeps the beggars."* That is also how the player learns where to go
- [ ] `TR1` (qa.md:553) where: Troll chief, first conversation | steps: Peace just made, nothing done | pass: **Exactly one** errand offered -- the ore trade. Plus the Tomas reply if you are on that quest, the flavor replies, and the goodbye
- [ ] `TR2` (qa.md:554) steps: Take the ore trade, return before finishing | pass: No new offers. The ore offer itself is gone
- [ ] `TR3` (qa.md:555) steps: Finish the ore trade | pass: The rite appears. Speak-for-us does **not**
- [ ] `TR4` (qa.md:556) steps: Finish the rite | pass: Speak-for-us appears
- [ ] `TR5` (qa.md:557) steps: Finish all three | pass: No offers left. Only flavor and the goodbye
- [ ] `TR6` (qa.md:558) steps: Reach peace via the **wererat** route, never taking the Tomas quest | pass: The ore trade is still offered -- tier 1 keys on peace, not on Tomas
- [ ] `CB9` (qa.md:592) [eyes + save] where: Back at the chief | steps: Tell him | pass: Node 112 -- the trolls move east *en masse*. **1509 XP**, quest state 3
- [ ] `CB10` (qa.md:593) [eyes + save] steps: Talk again | pass: Nothing repeats
- [ ] `CB11` (qa.md:604) where: Troll chief | steps: Turn in the rite | pass: The screen fades down and comes back by itself
- [ ] `SF2` (qa.md:688) [eyes + save] steps: Hear him out | pass: He gives you the exact words. Quest **Speak for the Trolls** at state 1
- [ ] `SF11` (qa.md:697) [eyes + save] steps: Back at the chief | pass: Node 132 -- he sits down. **1509 XP**, quest state 3
- [ ] `VR6` (qa.md:726) where: Troll chief, node 95 | gate: `ST 8+` | pass: He looks away first, and makes it a courtesy. *"Big is common down here"*
- [ ] `VR7` (qa.md:727) gate: Feralkin or Sylvant | pass: He sees it. They have a word for you up there and it is the same word the trolls get
- [ ] `VR8` (qa.md:728) gate: Human / Demokin, ST 7 or less | pass: Both absent
- [ ] `MS23` (qa.md:1298) [eyes + save] where: Troll chief, after *Speak for the Trolls* completes, Quinn's hide errand open, no hide held | steps: Talk to him | pass: *"The herbalist in the city needs the hide of a lava troll..."* -> he gives one from his dead. Absent with a hide in hand or the errand turned in

**Troll Pit (corpse field)**

- [ ] `CB5` (qa.md:588) where: Troll Pit, far east end | steps: Walk to (4736, 3014) | pass: The old chief's body. **It can be clicked and it talks** -- *0.99.1 corrected the corpse positions, so the coordinates may have moved.*
- [ ] `CB6` (qa.md:589) steps: Read node 120 | pass: It names what is lying around him, and does not arrange them
- [ ] `CB7` (qa.md:590) steps: **Not** on the quest | pass: Node 120 still opens; the rite reply is absent, the look-and-leave reply is not
- [ ] `CB8` (qa.md:591) [eyes + save] steps: Stand the rite | pass: Node 121. Quest to state 2
- [ ] `CB12` (qa.md:605) [eyes + save] where: The field | steps: Walk back in | pass: **The five troll bodies are gone.** The eight raiders are still lying there
- [ ] `CB13` (qa.md:606) steps: Read what fires now | pass: Node 125, not 120 -- it describes the drag marks and what was left. Node 120 must **not** fire, it describes a body that no longer exists
- [ ] `CB14` (qa.md:607) steps: Before the rite | pass: Node 120 still fires normally
- [ ] `CB15` (qa.md:625) where: The field | steps: Cast **Absorb Spirit** on the old chief | pass: You are healed and the body is consumed -- vanilla behaviour, unchanged
- [ ] `CB16` (qa.md:626) [eyes + save] steps: Immediately after | pass: **The chief speaks** -- node 127 -- and then peace ends and Lava Troll, Troll Chief and the gatekeeper all turn hostile
- [ ] `CB16b` (qa.md:627) steps: **Without ever being given the errand** | pass: Same reaction -- he still arrives, they still turn. But the line is node **128**, not 127
- [ ] `CB16c` (qa.md:628) steps: With the errand given | pass: Node **127** -- the only case where "I asked you because you owed him nothing" is a sentence he can say
- [ ] `CB16d` (qa.md:629) steps: Having fought your way east through a hostile pit | pass: Node 128 still reads correctly. It says nothing about alliance or permission
- [ ] `CB17` (qa.md:630) [save] steps: Check the journal | pass: **The Chief Before** is failed. No-op if it was never taken
- [ ] `CB18` (qa.md:631) steps: Walk back into the field | pass: Node **126**, not 120 -- a shape in the dust, and the eight raiders left. Node 120 must not fire
- [ ] `CB19` (qa.md:632) steps: Do it having never taken the rite | pass: Same reaction. Peace still ends; the errand is simply never offered
- [ ] `VR1` (qa.md:721) where: The corpse field, node 120 | gate: `PE 7+` | pass: The four trolls are in a line, all facing his way -- they were still coming when it ended. A bow with no arrow nocked. The dogs are the only ones who ran
- [ ] `VR2` (qa.md:722) gate: `IN 6+` | pass: Wererats *and* thieves in one party -- two ends of a war that has run for years. Somebody bought both halves for the same night and told neither
- [ ] `VR3` (qa.md:723) gate: `IN below 4` | pass: *"Thirteen. That is a lot."* Short and flat, not comic
- [ ] `VR4` (qa.md:724) gate: PE 6 or less / IN 4-5 | pass: VR1 and VR2 absent. The plain description is all you get
- [ ] `VR5` (qa.md:725) gate: After any of VR1-VR3 | pass: Returns to node 120. The rite is still available

**thieves' vault**

- [ ] `VJ8` (qa.md:1728) [eyes + save] step: Rob the vault **without ever taking the job**, then ask Skulker about the door | say: - | expect: Unchanged and impossible as before: the strongbox part is `Active=0` until he sets the quest, so there is nothing to take. This row exists because it was asked and answered, not because anything changed
- [ ] `VJ9` (qa.md:1729) [save] step: Click the strongbox in the vault room | say: - | expect: The log says **You have the thieves' strongbox. It is too big for your pack, so you carry it under one arm.** emphasized, and the journal updates. The box is a map entity with no item file at all, so before this the only feedback was the chest vanishing with a trap-disarm sound. The line prints **before** `Taken Hidden Treasure`, which deletes the interaction's own host

**anywhere in the act**

- [ ] `BS5` (qa.md:5459) [save] step: Note the bonus percentage in the log across tiers | say: - | expect: 25 for base, 35 for Tough, 50 for Super
- [ ] `BS6` (qa.md:5460) [save] step: Fight a `Sewer Theif3 Bow` or `Theif4 Bow` | say: - | expect: **Never** a backstab line. Archers were deliberately left out
- [ ] `BS7` (qa.md:5461) step: Judge whether the sewers are harder in an interesting way or simply harder | say: - | expect: **The row that decides whether the release stays.** Remember AC and HP also rose with the repoint -- *Judgement row: decides whether the release stays.*
- [ ] `BS9` (qa.md:5463) [eyes + save] step: Kill a thief and check its XP and drops | say: - | expect: Unchanged. The repoint touched `Race=` only; XP lives on the can

## Wilderness (394)


**Abandoned Cave**

- [ ] `TK12` (qa.md:1948) [eyes + save] step: Abandoned Cave, after Bernat packs up and leaves | say: - | expect: **His campfire is out.** The bales and crate go with it. Before this it burned on in an empty camp
- [ ] `RN20` (qa.md:5985) step: Fresh Abandoned Cave, walk west to the camp | say: Talk to Bernat | expect: *"Hold -- hold! Guilhem, down."*; who/news/shop all answer; Guilhem and Peire have their own barks; no wolves spawn on top of the camp; a second visit opens `3 return dialogue`
- [ ] `RN21` (qa.md:5986) [eyes + save] step: RN20 carrying a healing potion | say: *"Your man by the fire is hurt..."* | expect: The potion is taken, Peire's bark changes to *"The arm holds. My thanks."*, XP once; the reply gone afterwards
- [ ] `RN22` (qa.md:5987) step: RN20 before beating Aka Manah | say: - | expect: The "road south is open" reply is absent
- [ ] `RN23` (qa.md:5988) [eyes + save] step: RN20 after the charm breaks | say: *"The road south is open."* | expect: 400 gold, the Tome of Geomancy, 600 XP; Bernat, Guilhem and Peire and the camp props are gone; the cold-camp hover plays where they were
- [ ] `RN24` (qa.md:5989) step: Fresh Abandoned Cave, the camp | say: Walk to the bodies north-west of the fire; ask Bernat *"There are bodies in here."* | expect: The hover once; his answer on every greeting; the fire is lit and his opening line matches it

**Barcelona Coast**

- [ ] `CE12` (qa.md:2581) step: Kill Cervantes for Don Quixote instead | say: - | expect: The shade thanks you: *"Thank you for helping me destroy that madman!"* 39 KB of recorded audio that has never played
- [ ] `CV11` (qa.md:3326) step: **`Barcelona Coast`, not yet visited on that save**: walk up to Cervantes several times | say: - | expect: He now cycles **three** lines -- his greeting, *"We must not waste any time. La bestia is lurking nearby."*, and *"Have caution, squire, la bestia is everywhere."* Two of the three are what vanilla cycled

**Bounty Hunter Camp**

- [ ] `AU1` (qa.md:2452) [eyes + save] step: Reach the Bounty Hunter Camp in the Wilderness and walk into the trigger | say: - | expect: Three amulets at once: Icy Fury, Acid Touch and Lava Burn

**Crossroads**

- [ ] `F5` (qa.md:223) [eyes + save] where: Crossroads | do: Kill Esteban, return to the patrol leader | expect: He pays, the quest completes, his own quests fail. A corpse still *exists*, so the check had to ask whether he was *alive*
- [ ] `E1` (qa.md:325) where: Crossroads | steps: Kill El Bandito Rie **before** taking any Esteban quest, then talk to him and ask about thieves | pass: The reply *"I've already taken care of those thieves"* is offered
- [ ] `E2` (qa.md:326) steps: Take it | pass: He verifies, screen fades, and he returns with *"**Really? Most excellent.** Here is your reward"* -- **not** *"Good work!"*
- [ ] `E3` (qa.md:327) [save] steps: Check money and log | pass: 150 gold and the XP from the verify step, `Find the Crossroads Bandit` completed. Unchanged from before this fix -- the payout was never the broken part
- [ ] `E4` (qa.md:328) [eyes + save] steps: If the wasps are also dead, take *"I have also slain the wasps"* | pass: Wasp quest completes, 100 gold, **and he now answers** with `103 wasps killed` -- *"Muy excelente!"* Before, the conversation ended silently
- [ ] `E5` (qa.md:329) steps: Take *"I should be on my way"*, or press Escape | pass: `10 Goodbye`. This reply did not exist on the node before; its default used to push you on to `35 dangers 2`
- [ ] `E6` (qa.md:330) where: Crossroads, the **assigned** route | steps: Take the thief quest from Esteban normally, then complete it | pass: Still reaches `113 Thief success` and *"Good work!"* -- 113 is reached from six other places and must be untouched
- [ ] `X1` (qa.md:1161) where: Crossroads | steps: Ask Esteban about the dangers -- but **do not accept his goblin quest** -- then walk to the patrol | pass: The goblins **do not attack**. They patrol and can be approached
- [ ] `X1b` (qa.md:1162) steps: Talk to the Patrol Leader | pass: A conversation opens. **In vanilla and in the first 0.1.1 build the only interaction was an attack**; his `GetCloseThenTriggerAndFight` specifier was shadowing the conversation
- [ ] `X1c` (qa.md:1163) steps: Now accept Esteban's goblin quest | pass: The patrol turns hostile -- vanilla's `goblin confrontation` relay. **This is the choice, not a bug**: you agreed to clear them out
- [ ] `X1d` (qa.md:1164) steps: Mouse over any goblin in the patrol before anything turns hostile | pass: A **speech** cursor, not a sword. Clicking gets a line of banter
- [ ] `X2` (qa.md:1165) steps: Attack one anyway | pass: The full vanilla fight starts -- Patrol Leader, Scout **and** the corner goblins all turn. If any stands inert, `goblins attack` did not re-arm it
- [ ] `X3` (qa.md:1166) where: Goblin Patrol Leader | steps: Talk to him with **no** Horde rank | pass: The purge line, a `Speech 40` route, a fight and a walk-away. **No contract offered**
- [ ] `X4` (qa.md:1167) steps: Talk carrying **rank 1 only**, before ever meeting the Khan | pass: He recognises you but offers **no contract** -- he sends you to the Khan first
- [ ] `X4b` (qa.md:1168) steps: Meet the Khan, come back still at rank 1 | pass: *"You are still only a chum."* He tells you to do the shaman's work. Still no contract
- [ ] `X4c` (qa.md:1169) steps: Come back at **rank 2** (after Rakeb's eyes quest) | pass: Now the contract is offered. With IN 7+ you can also work out why he needs a *human* hand
- [ ] `X5` (qa.md:1170) steps: With IN 7+ | pass: The "you need a human hand" reply is visible and leads to the same offer
- [ ] `X6` (qa.md:1171) [eyes + save] steps: Accept the contract | pass: Quest appears; karma drops 50. **Esteban is unaffected** -- he was not there and cannot know
- [ ] `X7` (qa.md:1172) where: Guard Esteban | steps: Talk to him after accepting | pass: He behaves **exactly as before**. Still offers his quests, still takes turn-ins
- [ ] `X8` (qa.md:1173) steps: **With the contract accepted**, attack him | pass: A real fight starts. **You are not sent to prison.** In vanilla any player damage triggers `Esteban Sends you to jail`. He is 200 HP / 200 AC / melee 90 and **spell-immune** -- roughly Goblin Khan tier, weapons only
- [ ] `X8a` (qa.md:1174) steps: As a caster, cast near him after accepting | pass: Also no jail -- the 400-radius spellcast ward is removed too
- [ ] `X8c` (qa.md:1175) [eyes + save] steps: Kill him | pass: His two quests fail, the Templar step fails and rewinds to `F5BCFW6V`, karma drops 75, `Esteban Dead` is set
- [ ] `X8d` (qa.md:1176) steps: **Without** the contract, attack him | pass: **Still jailed.** The wards are lifted only by taking the contract; vanilla behaviour is untouched for everyone else
- [ ] `X8e` (qa.md:1177) steps: Accept the contract, **leave the Crossroads and come back**, then attack | pass: Still no jail. Every map entry re-clones a warded Esteban from the generator, so the fix has to survive that -- it disables the reset itself
- [ ] `X8b` (qa.md:1178) steps: If you find another way to kill him without the contract | pass: Same consequences. Killing a Templar man-at-arms costs the same whoever asked
- [ ] `X9` (qa.md:1179) [eyes + save] where: Goblin Patrol Leader | steps: Return after killing Esteban | pass: He pays 450 gold, completes the quest, karma drops another 75
- [ ] `X10` (qa.md:1180) [eyes + save] steps: Talk again after payment | pass: The `50 after` line, and **no second payment**
- [ ] `WR2` (qa.md:1856) step: **Regression, the whole point of the release.** Recover the muse and **do not** cross him | say: - | expect: Unchanged from 0.60.0: arrival on the first approach, the Richard II pitch and the stay-or-go choice on the second, *"return later"* on every one after
- [ ] `WR3` (qa.md:1857) step: Having crossed him, take the hostile line and then try to talk again | say: - | expect: The same line again. It is reply-less, so the conversation ends on it each time
- [ ] `WR4` (qa.md:1858) step: **Negative.** Having crossed him, check that no reply appears offering *"But I have recovered your muse Sytheria"* | say: - | expect: **It must not.** That reply belongs to `4 Shakespeare Hates you` and leads to `200 saved muse`, which would flip him to grateful, re-complete the quest and pay experience from a `Muse Quest XP` marker that exists in Shakespeares Home and **not** in the Crossroads. `800` was chosen over `4` for exactly this
- [ ] `WR5` (qa.md:1859) [eyes + save] step: Cross him by **each** of the two routes, on separate characters | say: - | expect: Both suppress the arrival. Four separate moments raise the old `shakespeare hates you` checker across two maps and two replies, and all four now also set the variable, because no single one of them is on every route
- [ ] `WR6` (qa.md:1860) step: Having crossed him, choose *"This place is too dangerous for you. Return to Barcelona."* | say: - | expect: **Not offered** -- that reply lives on `1000 in wilderness 2`, which a hostile player never reaches. He stays on the road, refusing you, which is the intended end state
- [ ] `HR36` (qa.md:2976) [eyes + save] step: **The report.** Stand near the horse, then walk away across the camp | say: - | expect: It stays where it is. It does not trail you, and it does not trail your companion either
- [ ] `HR37` (qa.md:2977) step: Watch it for a while | say: - | expect: It still shifts about its own small area. The patrol was never the problem and is untouched
- [ ] `HR38` (qa.md:2978) step: **Regression.** Click it, ten times; then hit it | say: - | expect: Whinnies, the tenth line, and Alvaro still objects. None of that moved
- [ ] `HR39` (qa.md:2979) step: **The save-reaching half.** On a character whose horse already follows, trade with Alvaro | say: - | expect: It settles and stops following from that moment -- *Needs a save whose horse already follows; n/a on a new game.*
- [ ] `HR33` (qa.md:2985) step: **The report.** Enter the Crossroads | say: - | expect: It loads. 0.60.5 died here with a DataCrash about an unexpected `{` while parsing `CSkeletonAI`  **PASSED** -- *"works"*, 2026-10-15 -- *Passed on 0.60.6; any visit re-checks it.*
- [ ] `HR28` (qa.md:2993) step: **The report.** Provoke it however you can: hit it, let a wolf at it, fight beside it | say: - | expect: It never swings, and the wrong model never appears
- [ ] `HR32` (qa.md:2997) step: **The save-reaching half.** On a character whose horse was already standing there, trade with Alvaro, then provoke it | say: - | expect: Same: it wanders, it will not swing. The shop replies swap its behaviour for the de-fanged copy -- *Needs a pre-install save; n/a on a new game.*
- [ ] `HR23` (qa.md:3004) step: Click it a few more times | say: - | expect: The line varies. Four of them, picked at random, the way the Montaillou chickens work
- [ ] `HR24` (qa.md:3005) step: **The save-reaching half.** On a character whose horse was already standing there, trade with Alvaro, then click the horse | say: - | expect: Same: it whinnies. The shop reply hands it the interaction with `CAddAIAction`, beside the pacifier from 0.60.2 -- *Needs a pre-install save; n/a on a new game.*
- [ ] `HR27` (qa.md:3008) step: Walk away, come back, keep clicking | say: - | expect: The count carries on where it left off rather than restarting. `CSeriesAction` keeps its index per instance, and the instance is in your save
- [ ] `HR17` (qa.md:3026) step: **New character.** Reach the Crossroads and walk up to the merchant's camp | say: - | expect: The horse stands by the cart. It does **not** approach you, does not attack, and your companion ignores it **PASSED** -- *"the horse is calm now"*, 2026-10-14 -- *Passed on 0.60.2.*
- [ ] `HR18` (qa.md:3027) step: **The save-reaching half.** On a character that already met the hostile horse, trade with Alvaro once | say: - | expect: It settles from that moment: no more charging, and the companion loses interest. The pacifier rides on his shop replies because dialogue is read fresh and map entities are not **PASSED in effect.** The report did not say which half delivered it, fresh spawn or shop repair, so this row is still worth walking deliberately on a save that had the hostile horse -- *Needs a save that met the hostile horse; n/a on a new game.*
- [ ] `SW1` (qa.md:3054) step: Recover Shakespeare's muse from Shylocke, then travel to the Crossroads from Barcelona | say: - | expect: He is standing on the road a few steps in, west of where you arrive
- [ ] `SW2` (qa.md:3055) step: Talk to him | say: - | expect: *"And enter the hero, stage right!"* -- he is visiting your battle sites to research a play. **With voiceover**
- [ ] `SW3` (qa.md:3056) step: Talk again | say: - | expect: The pitch: **Richard II**, named for you, *"a tale whose ending *you* will complete"*, and two replies
- [ ] `SW4` (qa.md:3057) step: Take *"I'm pleased and flattered"* | say: - | expect: *"Oh joyous moment... You must return later and I will reveal to you the opening scene of your play!"*
- [ ] `SW5` (qa.md:3058) step: Talk to him after that | say: - | expect: *"The fruit of the tree is too young and not yet ripe for the picking."* Every time, for good -- the game contains no opening-scene node, so this is the honest end of the thread
- [ ] `SW7` (qa.md:3060) [eyes + save] step: After sending him home, leave the Crossroads and come back | say: - | expect: Still gone. The generator is switched off too, so he does not respawn
- [ ] `HR1` (qa.md:3701) where: **The row that matters.** Travel to the Crossroads in the Wilderness and look near Alvaro the merchant | steps: - | pass: A **horse** is standing there, rendered, on the ground, close to him. If it is absent, floating, or sunk into the terrain, the placement is wrong and nothing else in this section can be tested
- [ ] `HR4` (qa.md:3704) where: **The consequence.** Attack the horse once | steps: - | pass: Alvaro shouts *"Away from her! She has pulled my cart these nine years and you raise a hand to her?"* in a balloon over his head, **and then turns hostile and attacks you** -- *Attack from the attack cursor; a plain click now whinnies (0.60.4).*
- [ ] `HR5` (qa.md:3705) [eyes + save] where: After HR4, try to trade with him | steps: - | pass: You cannot. He is hostile. This is a real cost for a petty act, which is the point
- [ ] `HR6` (qa.md:3706) where: Reload and instead **rob** Alvaro (pickpocket/steal), without touching the horse | steps: - | pass: The **shipped** reaction still happens: he cries *"Thief! THIEF!"*, walks to the guard captain, and goes hostile. The new relay must not have replaced or broken that one
- [ ] `HR7` (qa.md:3707) where: Reload and attack **Alvaro** directly, leaving the horse alone | steps: - | pass: His own vanilla damaged script still fires `Merchant1 requests help`. Unchanged
- [ ] `HR8` (qa.md:3708) where: Reload and kill the horse outright | steps: - | pass: It dies, plays its death animation, and you should **hear the horse death sound** -- a 27 KB recording that has never played in this game
- [ ] `HR10` (qa.md:3710) [eyes + save] where: Leave the Crossroads and return | steps: - | pass: The horse is still there, and if you had already angered Alvaro he is still hostile. The relay is `Trigger Only Once=1`, so the shout must not repeat endlessly
- [ ] `HR12` (qa.md:3712) where: Judge the **fiction**, which no check can settle | steps: - | pass: Does a cart horse with no cart read as odd? No map in the game places a cart model, so the cart exists only in his line. If the absence is glaring, that is worth knowing -- the alternative is placing an unverified model
- [ ] `DN14` (qa.md:4900) [eyes + save] step: **Guard Esteban** at the Crossroads: hit him once, then let him live | say: - | expect: Logs as **"Guard Esteban"**. Critically, **he must still be killable** -- if he shrugs off everything, this is the row that caught it, and the fix is to re-check his race presets are 200/200 and not 1000/10000 -- *0.60.3 found the log prints the can's User Assigned Name, not the race name this release edited. Expected names here came from race names, but 0.60.3 found the log prints the can's User Assigned Name (a hat goblin logs Goblin Striker). A different name is not a failure on its own; check it against the can.*
- [ ] `DN15` (qa.md:4901) [eyes + save] step: Kill Esteban deliberately, then take the Templar initiation to Javier | say: - | expect: Exactly as before this patch: `Esteban Death Consequences` fires and Javier's alternative line is reachable. His stats did not change, only his name -- *Expected names here came from race names, but 0.60.3 found the log prints the can's User Assigned Name (a hat goblin logs Goblin Striker). A different name is not a failure on its own; check it against the can.*
- [ ] `HC1` (qa.md:5497) step: Sworn to the **Goblin Horde**, buy from Alvaro at the Crossroads | say: - | expect: `21 the horde price` and his speech about the three carts, before any shop opens
- [ ] `HC2` (qa.md:5498) step: Buy something and compare the price with a non-Horde character | say: - | expect: Visibly worse: 1.5 against 1
- [ ] `HC3` (qa.md:5499) step: Repeat at **high karma**, where he offers his special supplies | say: - | expect: Also gated. The special stock does not dodge the surcharge
- [ ] `HC4` (qa.md:5500) step: Take *"Keep them"* | say: - | expect: `10 goodbye`, no shop, no hostility. He is a trader, not a guard
- [ ] `HC5` (qa.md:5501) step: Repeat carrying **no Horde allegiance**, at both normal and high karma | say: - | expect: `Vendor 1 Inventory` and `Good Karma Store for Alvaro` exactly as in vanilla

**Crossroads (Alvaro)**

- [ ] `TS1` (qa.md:2932) step: Talk to Alvaro and take *"Can you spare some coin for a poor traveller?"* | say: - | expect: *"You have some nerve begging from me, you tainted lout! Be off with you!"*
- [ ] `TS3` (qa.md:2934) step: **The row that matters.** If the beg option is still offered, take it again and reopen the shop | say: - | expect: Prices **unchanged from TS2**. The surcharge is once per character, and the vanilla gate that would have stopped a second beg is the checker that was missing
- [ ] `TS4` (qa.md:2935) step: On a **high-karma** non-human, do TS2 against his special stock | say: - | expect: The 15% lands there too. Vanilla's relay named only the ordinary store
- [ ] `TS5` (qa.md:2936) step: On a **Horde-sworn** non-human, do TS2 | say: - | expect: The 15% lands on the Horde store as well, so his 1.5 becomes 1.65
- [ ] `TS6` (qa.md:2937) step: **New save only.** Beg once, leave the conversation, talk to him again | say: - | expect: *"What *you* want now?"* and **no beg option**. That greeting has never been reachable at the Crossroads
- [ ] `TS7` (qa.md:2938) step: **Regression, human character.** Beg | say: - | expect: *"What do you think I am running here, a charity?"* and **no price change**. The surcharge is the non-human branch only
- [ ] `TS8` (qa.md:2939) step: **Regression.** Shop as a non-human who has **not** begged | say: - | expect: Normal prices. Nothing applies until you ask him for money
- [ ] `HR21` (qa.md:3030) step: **Regression.** Buy and sell with Alvaro, including as a Goblin Horde character | say: - | expect: The shop works exactly as before, on all three of his shop replies. The pacifier was added in front of the merchant window, not in place of it

**Crossroads (Guard Esteban)**

- [ ] `F4` (qa.md:157) where: Guard Esteban, Crossroads, node `50 Monsters` | steps: Ask about monsters, then "Goodbye." | pass: Reaches `10 Goodbye` ("Be safe traveler.")

**Crossroads (cross him in Shakespeares Home)**

- [ ] `WR1` (qa.md:1855) [eyes + save] step: **The reported row.** Recover the muse, then cross him -- extort Shylocke (`270 threat`) or tell him *"Sounds like you deserve your fate"* (`400 shylocke continued`). Then go to the Crossroads | say: - | expect: He is standing on the road as before, and the **first and every** approach gives *"Thou art a villain to impugn me thus. So I bid you farewell, and pray you pester a soul more deserving of your slander!"* -- `800 shakespeare hates you`, which is recorded. No arrival scene, no play named after you

**Darkwood Cave**

- [ ] `UE1` (qa.md:3071) step: Enter Darkwood Cave from the Woodcutter Forest and walk west | say: - | expect: A few steps in, the screen takes over: your spirit appears beside you with its own summoning effect, says its line, and vanishes again
- [ ] `UE2` (qa.md:3072) step: Listen | say: - | expect: *With voiceover.* Beast and Elemental: *"I sense abominations... unliving creatures animated by dark spirits."* Demonic has its own: *"Die by their hands and you'll join them in unlife. Do *try* and avoid dying, mmm?"*
- [ ] `UE3` (qa.md:3073) step: **The row that proves the spirit branch.** Play a character of each spirit | say: - | expect: Each gets **their own** recording and their own summoning effect, Beast / Demonic / Elemental. The same three-way test the wererat cave scene uses
- [ ] `UE4` (qa.md:3074) step: Note where it fires | say: - | expect: **Before** the first undead, not on top of them, and not as the map loads. It sits 350 units past the arrival pad and 339 short of the nearest skeleton generator
- [ ] `UE5` (qa.md:3075) [eyes + save] step: **Once only.** Leave the cave and come back; find undead elsewhere | say: - | expect: It does not play again, anywhere. It is guarded by a scripting variable that is set the first time, exactly as the first-mana-pickup scene is
- [ ] `UE6` (qa.md:3076) step: Watch the end of it | say: - | expect: Controls come back, the spirit plays its Disappear and is gone. Anything left standing in the cave means the cleanup did not run
- [ ] `UE8` (qa.md:3078) step: **Regression.** Finish the darkwood errand | say: - | expect: Unchanged. Nothing else in the cave was touched: every other level part is byte-identical to vanilla

**Goblin House Interior / ShamanInterior**

- [ ] `BU50` (qa.md:4780) step: And an **outlying** village -- any `Goblin House Interior`, the vendor hut, `ShamanInterior` | say: - | expect: **Still neutral**, by design. If that reads as an oversight rather than as distance, say so: each one has its own `Make Goblins Hostile Relay` and adding them is one line each

**Goblin Vendor Interior**

- [ ] `V1` (qa.md:1189) where: Goblin Vendor Interior | steps: Character B | pass: Only the vanilla *"I would like to see what you have for sale"* is offered; store opens normally
- [ ] `V2` (qa.md:1190) steps: Character A with Horde rank | pass: Chum-price reply visible; `25 chum vendor` plays; store opens
- [ ] `V3` (qa.md:1191) steps: Character A with Barter 60+, no rank | pass: Barter reply visible; same store opens
- [ ] `V4` (qa.md:1192) steps: Compare a specific item's price between V1 and V2 | pass: **Noticeably cheaper** in the chum store

**Goblin Warrens**

- [ ] `G7b` (qa.md:185) [save] where: Any two further services, in any order | steps: e.g. the vodyanoi, then the Everlasting | pass: Rank climbs 1 -> 2 -> 3 regardless of order, and **never past 3**
- [ ] `G7c` (qa.md:186) [save] where: A fourth and fifth service after reaching rank 3 | steps: Anything else pro-goblin | pass: Nothing happens. No rank, no duplicate title perk
- [ ] `F4` (qa.md:222) [eyes + save] do: Ask the girl for a pie twice; ask Rakeb for the fish job twice | expect: Neither is given twice. Both were farmable
- [ ] `R1` (qa.md:264) [eyes + save] where: Goblin Warrens, near the Khan's court | steps: Enter the map on a fresh save | pass: **Goblin Girl is present and talkable**
- [ ] `R2` (qa.md:265) steps: Talk to her the first time | pass: Node `1 First time PC enters village` plays
- [ ] `R3` (qa.md:266) steps: Talk again | pass: Node `2 PC Enters the village again...` plays
- [ ] `R4` (qa.md:267) steps: *"give me some sugar"* -> insult her complexion | pass: `7 sugar part 2` -> `90 Follow`
- [ ] `R5` (qa.md:268) steps: Rebuff her instead | pass: `80 Rebuffed`, conversation ends cleanly
- [ ] `R6` (qa.md:269) steps: After killing the woodsman, choose *"why don't you find a nice goblin man"* | pass: Node `250 Rejection` plays and **ends cleanly** (this node did not exist in vanilla)
- [ ] `R10` (qa.md:273) steps: Talk again | pass: `120 Player returns again after killing dryad...`
- [ ] `P1` (qa.md:280) [eyes + save] where: Goblin Girl, after bringing the woodsman's liver | steps: Take the plain reply | pass: Node `290 follow 3` plays; **pie appears in inventory**
- [ ] `P2` (qa.md:281) [eyes + save] steps: Check the inventory entry | pass: Named "Liver Pie", correct pie icon, description unchanged from vanilla
- [ ] `P3` (qa.md:282) steps: PE 7+ character | pass: *"a sharp green smell"* reply visible; reaches `227 momma's seasoning`
- [ ] `P4` (qa.md:283) steps: IN 7+ character | pass: The "measuring me for a pot" reply visible; reaches `227`
- [ ] `P5` (qa.md:284) [eyes + save] steps: From `227`, accept | pass: Still receive the pie, then `290 follow 3`
- [ ] `F1` (qa.md:297) where: Goblin Warrens, at any follow node (`90`, `190`, `195`, `290`) | steps: Take the accepting reply | pass: She falls in behind you and keeps up across the cave
- [ ] `F2` (qa.md:298) steps: Take the declining reply instead | pass: Conversation ends, she stays put, nothing else changes
- [ ] `F3` (qa.md:299) steps: Open the conversation and press Escape | pass: Same as F2 -- decline is the default reply, so cancelling is never the committing path
- [ ] `F4` (qa.md:300) where: Warrens main exit, **while she follows** | steps: Click the exit | pass: Node `295 goblin girl stays behind` opens instead of the map change
- [ ] `F5` (qa.md:301) steps: Take *"Not yet. There is more down here."* | pass: **You do not leave the map.** She is still following
- [ ] `F7` (qa.md:303) where: Waterfall passage exit, while she follows | steps: Same as F4-F6 | pass: Node `296 goblin girl stays behind waterfall`; different line, same behaviour
- [ ] `F8` (qa.md:304) where: Either exit, **not** following | steps: Click the exit | pass: Straight map change, no dialogue -- vanilla behaviour is untouched
- [ ] `F10` (qa.md:306) where: Warrens, kill her while she follows | steps: Then click an exit | pass: Straight map change, **no farewell from a corpse**. Her death script clears the marker, and the exit also checks `CIsAliveAction`
- [ ] `F11` (qa.md:307) where: Warrens, leave and return while she followed | steps: Talk to her | pass: She is where you left her and still greets by quest state
- [ ] `PK2` (qa.md:3633) where: After `PK1`, talk to any goblin villager | steps: - | pass: A new reply is offered: *"You know what I am. Say it."* Taking it gets the *"you are weather"* speech, and notably **the villager does not offer to eat you**, which every one of its other 17 greetings does
- [ ] `BU32` (qa.md:4658) [eyes + save] step: Take the Khan's contract | say: *"It will be done, Great Khan."* | expect: **`The Goblin of Butu's Line`** opens -- *"The Khan wants him dead and does not want to hear his name."*
- [ ] `BU35` (qa.md:4661) step: After killing him on the contract, go back to the Khan | say: *"The east rock is yours again. I will not say the name."* | expect: `382 you did not say it` -- *"Then there was never anybody there, and I never sent anybody east, and you have gone up in the world for doing nothing at all. That is how it works, morsel."*
- [ ] `BU24` (qa.md:4709) step: Talk to the Khan in the Goblin Warrens **before** reaching Montserrat | say: - | expect: **No mention of the east cave.** The reply is gated on the same quests as the takeover, so he never refers to something that has not happened
- [ ] `BU25` (qa.md:4710) step: Reach Montserrat, then talk to the Khan again | say: *"Someone is sitting in your east cave, and he is not one of yours."* | expect: `380 the east rock is taken` -- *"Butu's line were nobodies when I was young and they are nobodies with a cave. He has my east rock and my shiny and he tells my goblins that I draw maps."* **He never says Hrargrub's name**, and tells you not to bring it back
- [ ] `BU26` (qa.md:4711) step: Take the Speech reply | say: *"He says you have been drawing those maps for six winters."* | expect: `381 do not repeat that` -- *"He does not move at all, which from him is the loudest thing available."* No punishment, which is the joke
- [ ] `BU27` (qa.md:4712) step: Both of the Khan's entry nodes | say: - | expect: The reply appears from a first conversation and from `05 Return Friends of Khan` alike
- [ ] `BU28` (qa.md:4713) step: Kill the Khan, then look for the pointer | say: - | expect: Gone with him, as it should be. A player who killed Plumjum and never went east simply never hears about Hrargrub -- fair, and worth confirming it fails quietly rather than leaving an orphan reply
- [ ] `BU48` (qa.md:4778) step: Go to the **Goblin Warrens** afterwards | say: - | expect: **They attack**, Khan included, so there is no conversation with him. Confirm the game does not try to open one
- [ ] `GL16` (qa.md:5114) step: Reach the Goblin Khan after delivering, on a **first** meeting | say: - | expect: A Quest-icon reply about the child. `375 the khan has eaten well` -- Grimek's runner beat you there by three days with his own name in front
- [ ] `GL17` (qa.md:5115) step: Reach him again later as a goblin friend | say: - | expect: The same reply is offered from `05 Return Friends of Khan`
- [ ] `HC6` (qa.md:5502) step: As a Horde member, buy from **Hub'blub** in the warrens | say: - | expect: Still 0.75. The Horde's own discount is untouched
- [ ] `N1` (qa.md:6004) pass: Every vanilla solution still reachable -- *Summary row: met by playing the goblin-thread scenes with a second, different character.*
- [ ] `N3` (qa.md:6006) pass: Confirmed -- *Summary row: met by a low-stat character finishing the goblin scenes.*
- [ ] `N6` (qa.md:6009) [eyes + save] pass: Quest completes and the shipped `Goblin Champion` perk is still granted. The rank guard fails silently; it must not swallow the perk
- [ ] `S1` (qa.md:6446) [save] pass: Rank and bonuses survive
- [ ] `S4` (qa.md:6449) [eyes + save] pass: Girl and Guards persist
- [ ] `S5` (qa.md:6450) pass: No script errors; camp hostility behaves normally

**Goblin Warrens (Goblin Girl)**

- [ ] `T9` (qa.md:205) where: Goblin Girl, **first meeting**, with the River Dryad already dead | steps: Talk to her | pass: *"You're cute for a... whatever it is you are."* **Not** the snails line. Reported from play: she used to greet a stranger as an old friend
- [ ] `T10` (qa.md:206) steps: Same, with the **woodcutter** already dead | pass: Still the first-meeting line. World state must never beat first contact
- [ ] `T11` (qa.md:207) steps: Talk again after that first meeting | pass: *Now* the state greetings apply -- snails if the dryad is dead, the woodsman line if he is
- [ ] `F8` (qa.md:226) do: Click every reply on her first-meeting node | expect: No blank option that does nothing. Six such replies were repaired

**Goblin Warrens (Khan)**

- [ ] `G7d` (qa.md:187) [save] where: The Khan's *"I'm glad we see eye-to-eye"* reply | steps: Take it at rank 2 | pass: Exactly **one** rank. That reply both completes the bounty quest and grants rank, and briefly advanced twice
- [ ] `G8` (qa.md:188) [save] where: Goblin Khan | steps: Hand over the Everlasting (any of the three price routes) at rank 2 | pass: **Rank 3, `Goblin Champion`**, granted alongside the shipped `Goblin Champion` perk
- [ ] `G9` (qa.md:189) [save] steps: Try the other two Everlasting routes afterwards | pass: Rank does **not** increment again -- the rank==2 guard makes it idempotent
- [ ] `T6` (qa.md:202) where: The Khan, entering his cave | steps: At **rank 3** | pass: A different greeting: *"Not 'morsel'. Not today."* <span>If he still opens with the morsel line, the map-side rank gate failed</span>
- [ ] `T7` (qa.md:203) steps: At rank 3, when he demands entertainment | pass: You can refuse: *"Ask the room whether the Khan's champion dances."*
- [ ] `T8` (qa.md:204) steps: At **rank 0-2** | pass: Every vanilla greeting and the entertainment demand are unchanged
- [ ] `T12` (qa.md:208) where: The Khan, **first meeting at rank 3** earned without the Everlasting (spy + dryad + eyes) | steps: Enter his cave | pass: The **vanilla** greeting. He must not claim the Everlasting hangs on his wall
- [ ] `T13` (qa.md:209) steps: Then deliver the Everlasting and return | pass: *Now* the Champion greeting
- [ ] `C8` (qa.md:239) [eyes + save] where: Goblin Khan | steps: CH 7+, at `11 Earn Goodbye` | pass: Charm reply visible; reaches `16 flattered khan`; XP awarded
- [ ] `C9` (qa.md:240) steps: Character B with Speech 25 | pass: Vanilla flattery reply still works
- [ ] `C17` (qa.md:248) steps: After C16, talk to the Goblin Khan | pass: The "I could tell you a Goblin poem" option is available -- the Schmooze route sets the same flag the vanilla routes do
- [ ] `K1` (qa.md:1109) where: Goblin Khan, as **Champion** | steps: Talk to him | pass: New reply *"I would serve the Horde again. What does the war need?"* is offered
- [ ] `K2` (qa.md:1110) steps: Take it | pass: `350 next task` -- *"I have need of a strategist"*
- [ ] `K3` (qa.md:1111) steps: Continue twice | pass: `360 attack barcelona`, then `365 barcelona walls`, which names Esteban and the gate guards
- [ ] `K4` (qa.md:1112) steps: Accept | pass: Conversation ends peacefully. Nothing else changes -- the briefing grants no quest and no reward
- [ ] `K5` (qa.md:1113) steps: At `350` or `360`, take the **Exit Icon** reply, or press Escape | pass: Conversation ends, camp stays calm. **The default reply is never the fight**
- [ ] `K6` (qa.md:1114) steps: Take a **Fight Icon** reply at any of the three | pass: `400 Where are you going?` -- *"I did not say you could leave!"* -- and the Khan turns hostile
- [ ] `K7` (qa.md:1115) steps: **Below Champion** (Chum or Blooded) | pass: The entry reply is **absent**; his conversation is unchanged from 0.1.4
- [ ] `K8` (qa.md:1116) where: Khan, **after already killing Esteban** | steps: Reach `365` | pass: A fourth reply appears: *"Esteban is already dead. I cut him down before you asked."* -> `370`, the Khan's reaction
- [ ] `K9` (qa.md:1117) steps: Same, with Esteban **alive** | pass: That reply is **absent**
- [ ] `K10` (qa.md:1118) where: Khan, **after killing Esteban**, on the greeting itself | steps: Talk to him | pass: A **second** Champion reply is offered: *"the gatekeeper Esteban is dead. I want you to hear it from me."* -> straight to `370`, without re-walking the briefing
- [ ] `K11` (qa.md:1119) steps: With Esteban **alive** | pass: That reply is absent; only the briefing entry shows
- [ ] `K12` (qa.md:1120) steps: After reporting, talk again | pass: The briefing entry is still there and still works. Re-hearing his plan is intended; nothing is granted, so there is nothing to farm

**Goblin Warrens (Rakeb)**

- [ ] `G6` (qa.md:183) [eyes + save] where: Rakeb | steps: Bring the woodcutter's eyes and liver; hand them over (either the Barter 35 route or the plain one) | pass: **Rank 2, `Goblin Blooded`**: Sneak and Barter each +8, Poison and Disease resistance each +10 -- *Since 0.1.4 tiers are running totals, so read the delta from rank 1.*
- [ ] `G7` (qa.md:184) [save] steps: Do the eyes quest as your **first** goblin service ever | pass: You become **`Goblin Chum`**, not Blooded -- the cascade grants the next rank you lack, so no service is wasted
- [ ] `T4` (qa.md:200) where: Rakeb | steps: At **rank 2** | pass: *"Clan. Yes. The bones have been saying so for a while."* No tourist's price
- [ ] `T5` (qa.md:201) steps: At **rank 3** | pass: He is not sure the clan should be glad -- *"a door left open, and doors are how weather gets in"*
- [ ] `F3` (qa.md:221) where: Goblin Warrens | do: Rakeb, at three points in his errands | expect: Eyes job taken, not delivered -> *"we do not see the eyes"*. Fish killed, second job untaken -> *"I have a job for you"*. All done -> *"the items have served you well"*. All three were unreachable. *"we do not see the eyes"* **confirmed in play**; the other two rungs are not. Needs a character new to the map
- [ ] `C6` (qa.md:237) where: Rakeb (Goblin Warrens) | steps: Tribal 80+, at node `30 Explanation` | pass: Reply about frogs/mirrors/entrails visible; reaches `35 fellow practitioner`
- [ ] `C7` (qa.md:238) steps: Character B | pass: That reply absent; *"I don't speak Goblin"* still there

**Goblin Warrens (entrance guard)**

- [ ] `G1` (qa.md:178) where: Goblin camp entrance guard | steps: Arrive **after** H8, before any Speech option | pass: Reply *"Hrubjub of the Horde sent me..."* is visible
- [ ] `G2` (qa.md:179) steps: Choose it | pass: Reaches `30 khan`; the camp does not turn hostile
- [ ] `G3` (qa.md:180) steps: Character B, no Horde rank | pass: That reply is **absent**
- [ ] `G4` (qa.md:181) steps: Character A with CH 7+ | pass: The `Schmooze` gate reply is visible and also reaches `30 khan`
- [ ] `G5` (qa.md:182) steps: Vanilla Speech 40 route | pass: Still present and still works

**Goblin Warrens (southern approach)**

- [ ] `R7` (qa.md:270) [eyes + save] where: Goblin Warrens, southern approach | steps: Enter the map | pass: **Two guards present**, conversation auto-advances through all four nodes to *"Shhh, did you hear something?"*
- [ ] `R8` (qa.md:271) steps: Attack the camp / trip the hostility relay | pass: Both new NPCs turn hostile with everyone else

**Goblin Warrens (villager)**

- [ ] `T1` (qa.md:197) where: A goblin villager in the Warrens | steps: Talk to one at **rank 0** | pass: The vanilla threat, and only the Speech way out
- [ ] `T2` (qa.md:198) steps: At **any rank** | pass: *"Word travels, and your name has been in three mouths this week."* The spear comes down
- [ ] `T3` (qa.md:199) steps: At **rank 3** | pass: The goblin kneels. *"Forgive it, Champion."*

**Goblin Warrens / 01 Desert Sprawl**

- [ ] `DN7` (qa.md:4860) [save] step: The Warrens' Khan, and Fixt's Rumjun Khan in `01 Desert Sprawl` | say: - | expect: **"Goblin Khan"** and **"Rumjun Khan"** respectively. Rumjun got his own race cloned from `Goblin Hat Super`, carrying 0.30.0's boss damage profile unchanged, so he should still take -10 from fire and shrug off poison -- *0.60.3 found the log prints the can's User Assigned Name, not the race name this release edited. Expected names here came from race names, but 0.60.3 found the log prints the can's User Assigned Name (a hat goblin logs Goblin Striker). A different name is not a failure on its own; check it against the can.*

**Goblin Warrens / Crossroads**

- [ ] `BL5` (qa.md:491) where: Goblin Khan / Esteban | steps: Re-walk 0.2.0's branches | pass: 6 repaired sites

**Goblin Warrens / Mongol Camp**

- [ ] `F6` (qa.md:302) steps: Take *"Wait here for me."* | pass: She stays; you arrive at the Mongol Camp **alone**

**Goblin Warrens or Mongol Camp**

- [ ] `PK1` (qa.md:3632) [save] where: **Proves half one.** Kill goblins in the Goblin Warrens or the Mongol Camp until the Raylark bounty or the Savage Heart quest ticks over (twelve) | steps: Check the character sheet | pass: The title **Goblin Slayer** is now listed. It should arrive at the same moment the bounty or quest advances, because it hangs off that same branch

**Goblin Warrens; Torquemada's chambers**

- [ ] `N5` (qa.md:6008) [eyes + save] pass: Take the contract, kill the Khan, collect from Torquemada -- unchanged from vanilla

**Goblin Warrens; Woodcutter Forest**

- [ ] `N8` (qa.md:6011) pass: No script errors; the camp-hostility relay behaves normally

**Lake**

- [ ] `SR4` (qa.md:5406) step: Wilderness: take **Grumdjum** as a companion | say: - | expect: Conversation survives, and walking up to him again opens the companion nodes, not the first-meeting ones
- [ ] `SR5` (qa.md:5407) step: Dismiss Grumdjum, then approach him again and rejoin | say: - | expect: Both transitions survive; his interaction rewires each time

**Lake (Grumdjum)**

- [ ] `C10` (qa.md:241) where: Grumdjum, dryad branch | steps: IN 7+, **Speech below 20** | pass: The dryad reply is now visible (it was Speech-only before)
- [ ] `C11` (qa.md:242) steps: Speech 20+, IN below 7 | pass: Still visible -- the Speech route was not removed
- [ ] `C12` (qa.md:243) where: Grumdjum (Lake), `10 Smart Goblins` | steps: IN 7+ | pass: The Bonecrusher reply is visible; reaches `11 fellow pedant`, which returns cleanly to `20 The Offer`
- [ ] `C13` (qa.md:244) where: Grumdjum, `81 Magic Node` | steps: Thought 80+ | pass: The reservoirs reply is visible; reaches `82 the residue theory`
- [ ] `C14` (qa.md:245) where: Grumdjum, `91 Dryad Magic` | steps: IN 7+ | pass: The "you are afraid I will listen to her" reply is visible; reaches `92 why silence her`
- [ ] `C15` (qa.md:246) steps: From `92`, choose *"I will hear her out first"* | pass: Conversation ends without accepting the kill contract; the dryad can still be talked to
- [ ] `C16` (qa.md:247) where: Grumdjum, `110 Goblin Poetry` | steps: CH 7+ | pass: The craft-praise reply is visible; reaches `120 More pun-ishment`
- [ ] `C18` (qa.md:249) where: Grumdjum | steps: **Character B** | pass: All four new replies absent; every vanilla route through his tree still works
- [ ] `G1` (qa.md:1083) where: Lake, after handing in the dryad kill | steps: Find Grumdjum at the dryad's crystal and talk to him | pass: *"It is always a pleasure to see you, my dryad slayer..."* and **three replies**. Before this fix he said one line about her brain and the conversation ended
- [ ] `G2` (qa.md:1084) steps: Ask *"What is New Khara'Khorum?"* | pass: `100 Goblin City` -- he says to seek it **through the waterfall to the east**. That is a real direction: the Warrens' second exit is `From Waterfall Passage`
- [ ] `G3` (qa.md:1085) steps: Ask about poetry (needs `Player has heard Grumjun poetry` > 0, so hear a poem from him first) | pass: `200 new poem`, then any of three reactions -> `200 new poem response`
- [ ] `G4` (qa.md:1086) steps: Take the third reply, or press Escape | pass: `160 After Dryad death bubble` -- the brain line, now working as the sign-off it reads as
- [ ] `G5` (qa.md:1087) steps: Re-open the conversation | pass: Repeats cleanly; no farming, since nothing here grants anything
- [ ] `G6` (qa.md:1088) [eyes + save] where: Lake, **before** handing in the dryad kill | steps: Talk to Grumdjum | pass: Unchanged from vanilla -- the rotating `3` / `5` / `6` / `7` greetings, and the hand-in reply still pays the Ring of Fiery Death and advances rank

**Lake (Trapped Conquistador)**

- [ ] `C1` (qa.md:232) where: Trapped Conquistador (Lake) | steps: Character A, CH 7+ | pass: Herald reply visible; leads to `35 herald` then `40 Return Barcelona`
- [ ] `C2` (qa.md:233) steps: Character A, IN 7+, on any of the three argument nodes | pass: Deduction reply visible; goes straight to `40 Return Barcelona`
- [ ] `C3` (qa.md:234) steps: Character B, ST 8+ | pass: *"I am your next challenger..."* visible; goes to `40 Return Barcelona`
- [ ] `C4` (qa.md:235) steps: **Character B** | pass: The vanilla "Where is your home?" route still works, and CH/IN replies are absent
- [ ] `C5` (qa.md:236) [eyes + save] steps: From `40 Return Barcelona`, recruit him | pass: He joins as a companion, XP awarded

**Lake (red crystal node)**

- [ ] `CP9` (qa.md:1347) [eyes + save] where: Fresh Lake map, quest active | steps: Click the node three times, kill the waves | pass: The journal advances to *"The crystal draws the dead..."* when the third wave strips the click

**Lake / Plains / Woodcutter Forest**

- [ ] `GB37` (qa.md:5027) step: Fight `Mongol Goblin` / `Tough` / `Super` in any **other** map -- `Lake`, `Plains`, `Woodcutter Forest` | say: - | expect: **No exchange, and no errors.** The death trigger is guarded on the relay entity existing, and `goblins losing heart` exists in one map of the sixteen that spawn those cans

**Lake, Plains, Woodcutter Forest or Barcelona Coast**

- [ ] `GL1` (qa.md:6184) **NEW** [eyes + save] where: Lake, Plains, Woodcutter Forest or Barcelona Coast, first visit | steps: Find a band with a hat goblin named Goblin War Leader, kill him | pass: The log says the goblins around him lose heart, and his band attacks visibly slower. Other bands are unchanged | new: True
- [ ] `GL2` (qa.md:6185) **NEW** [eyes + save] where: The same, as the Khan's Champion | steps: Walk in | pass: The bands and their war leaders keep their distance | new: True
- [ ] `CO2` (qa.md:6214) **NEW** [eyes + save] where: Lake, Plains, Woodcutter Forest or Barcelona Coast, first visit, Khan killed | steps: Fight a band | pass: The log says they fight with less heart, and they attack visibly slower | new: True
- [ ] `CO3` (qa.md:6215) **NEW** [eyes + save] where: The same, as Goblin Champion | steps: Walk in | pass: The log says they keep their distance, and the bands do not attack. Quest goblins (Grumdjum, the guard at the girl) are unchanged | new: True

**Mongol Camp**

- [ ] `F9` (qa.md:305) [eyes + save] where: Mongol Camp, after F6 | steps: Walk around | pass: **She is not with you.** This is the whole point; if she is here, the release lost its race with the relocate and Mongol Camp needs vanilla's remover entity
- [ ] `J3` (qa.md:1149) steps: Take either other reply, or press Escape | pass: Camp turns hostile. This is vanilla's design, not a bug -- the bluff has no check behind it and the default reply is the bluff
- [ ] `J4` (qa.md:1150) steps: **Goblin Blooded or Champion**, any Speech | pass: New reply *"I am of the Horde, and this morsel is spoken for"* is offered **above** the Speech option, and reaches the same release
- [ ] `J5` (qa.md:1151) steps: Goblin Chum (rank 1) only | pass: The rank reply is **absent** -- the gate is `Goblin Rank > 1`, not merely "in the Horde"
- [ ] `J6` (qa.md:1152) steps: Kill the jailor first, then escort Darsh out | pass: No challenge at all; the trigger checks `CIsAliveAction` before firing
- [ ] `BU49` (qa.md:4779) step: And the **Mongol Camp** | say: - | expect: Also hostile

**Mongol Camp (Goblin Khan)**

- [ ] `PK4` (qa.md:3635) where: **The contradiction.** Hold `Goblin Slayer` **and** goblin rank (be in the horde), then speak to the **Goblin Khan** | steps: - | pass: A reply appears admitting you wear his mark and have killed his people. His answer should be approval, not condemnation. **With no goblin rank this reply must not appear at all**

**Mongol Camp (jail exit)**

- [ ] `J1` (qa.md:1147) where: Mongol Camp, escorting Darsh | steps: Walk Darsh toward the exit | pass: The **Goblin Jailor** stops you: *"And just where do you think you are taking that prisoner?"*
- [ ] `J2` (qa.md:1148) steps: Speech 25+, take *"The Khan has requested to eat this morsel"* | pass: `400 jailor okays release`; **camp stays calm** and you leave with Darsh

**Mongol Camp gate**

- [ ] `AB1` (qa.md:1258) where: Mongol Camp gate | steps: Enter the camp for the first time; take any of the four peaceful routes past the guard (Grumdjum's friend, Horde messenger, Schmooze, Speech) | pass: The challenge plays once as before. Leave the camp and come back through the gate: **`3 Return Dialogue`** -- *"Greetings goblin friend. What do you want?"* -- with the audience ask (Speech 40), the Darsh ask only while the Darsh quest is current, and *"Nothing today. I will be on my way."*
- [ ] `AB2` (qa.md:1259) where: Mongol Camp gate | steps: On the return greeting, pick *"I have come to rid this forest of your existence, monster."* | pass: The camp turns hostile, exactly as the same line does on the first meeting
- [ ] `AB3` (qa.md:1260) where: Mongol Camp gate, negative | steps: Enter, get challenged, and leave without being welcomed or fighting (e.g. *"I come in peace"* goes hostile, so this needs the Darsh route or a quick exit); come back | pass: Silence at the gate, as vanilla. No second challenge
- [ ] `AB4` (qa.md:1261) where: Mongol Camp gate, negative | steps: Make the camp hostile by any route, then cross the gate again | pass: Nothing fires

**Mountain Pass**

- [ ] `TG1` (qa.md:2807) step: Kill a good number of **basic** Rock Titans | say: - | expect: A **sphere** about one in four, worth **100** now rather than 200. **No crystal**
- [ ] `TG2` (qa.md:2808) step: Kill **Tough** ones | say: - | expect: A sphere about one in three. Still no crystal
- [ ] `TG3` (qa.md:2809) step: **The row that matters.** Kill **Super** ones | say: - | expect: A sphere about one in two, **and** a crystal about one in four -- so roughly one Super in eight leaves **both**, which no other titan can
- [ ] `TG5` (qa.md:2811) step: Add up a dozen kills per tier | say: - | expect: Rising roughly 25, 33 and 100 gold expected per kill against 100, 130 and 160 HP
- [ ] `TG6` (qa.md:2812) [eyes + save] step: **Regression.** Check XP and the ordinary loot | say: - | expect: 1509 XP and the same gold and spirit charge on all three, untouched
- [ ] `TC3` (qa.md:2824) step: Look at it on the ground before picking it up | say: - | expect: Its own model, `TitanCrystal_PU`, used by this item alone and never displayed in the game before
- [ ] `RT2` (qa.md:2838) step: **The row that matters.** Look at it on the ground before picking it up | say: - | expect: Its own model, not the generic gem the stone hearts use. `TitanSphere_PU` has never been displayed in the game before
- [ ] `AF1` (qa.md:5558) step: In `Mountain Pass`, walk through a charm sweep polygon **before** breaking the ogre charm | say: - | expect: Nothing happens
- [ ] `AF2` (qa.md:5559) step: Break the charm, then walk back into that same polygon | say: - | expect: `the charm lifts` fires. This is the case the missing field put at risk
- [ ] `RN19` (qa.md:5984) step: Fresh Pass, walk the road south to north | say: - | expect: The dead ground, the titans' quarry and the cairn, once each; after the charm breaks the cairn reads its quiet version

**Ogre Cave**

- [ ] `RN18` (qa.md:5983) step: RN17 by the Speech route instead (`160 tricked aka manah`) | say: - | expect: The same stand-down; the XP and Alamut hook as before

**Ogre Cave, Ogre Sprawl**

- [ ] `AF3` (qa.md:5560) step: Repeat AF1/AF2 in `Ogre Cave` and `Ogre Sprawl` | say: - | expect: Same behaviour on all ten sweeps

**Ogre Cave, Ogre Sprawl, Mountain Pass**

- [ ] `RN17` (qa.md:5982) step: Fresh ogre maps, kill Aka Manah | say: Walk back out through the Cave, the Sprawl and the Pass | expect: Every ogre stands down, once, with *"<The ogre stops mid-swing...>"*; rock titans and wolves still attack; ogres spawning near you afterwards are passive -- *Since 0.98.0 the charm line comes from one ogre only (XS13).*

**Ogre Conjurer Cave**

- [ ] `RN25` (qa.md:5990) step: Ogre Conjurer Cave, fresh | say: *"What do you want with me?"* -> *"So, I have you to thank for all the Ogres in this cave?"* | expect: `30` then `50 Ogre Spells`; *"Who is your master?"* reaches `170 Master`, not the Nueva Barcelona node
- [ ] `RN26` (qa.md:5991) step: As a tainted character | say: *"You have felt what I carry..."* -> *"Then let me walk out..."* | expect: `80`, then `70`; he does not attack, you can leave the cave; a second visit opens `130`; the ogres are still hostile and Bernat is still stuck
- [ ] `RN27` (qa.md:5992) step: Speech 40+ | say: *"Your master has made terms with the Titans of Toulouse."* | expect: `90`; *"Fair enough, and farewell"* makes him leave as the Speech route does -- XP, and the ogres stand down
- [ ] `RN28` (qa.md:5993) step: Speech under 40 | say: The same reply | expect: `120`, and he attacks
- [ ] `RN29` (qa.md:5994) step: Flee the fight and come back without either outcome | say: - | expect: The first greeting again, not *"Was my warning not sufficient?"*

**Ogre maps**

- [ ] `MB5` (qa.md:2407) [eyes + save] step: Kill ogres in the Wilderness | say: - | expect: An **Ogre Tusk**, about one kill in three. Check the icon is a broken ivory tusk with a dark root and **not** the jewelled Alamut medallion
- [ ] `MB15` (qa.md:2417) step: **Regression.** An ogre or a snakebreed killed by something other than you | say: - | expect: No part. The drop sits inside the existing `CWasDamagedByPlayerAction` check

**Plains**

- [ ] `RN1` (qa.md:5966) step: Fresh Plains, any spirit-bearing race, walk to the rogue camp from the south-east | say: - | expect: The spirit manifests ahead of you and says *"Beware, the dark inquisitors wield the power to cancel magic by touch..."* (voiced), fades; once; a Pureblood sees nothing
- [ ] `RN2` (qa.md:5967) step: Fresh Plains, fight the rogue camp | say: Kill them | expect: As the last one or two fall: the summoning flare on the pentagram, *"<The men stop. The circle does not...>"*, a Terror rises and attacks; once
- [ ] `RN3` (qa.md:5968) step: Fresh Plains, kill Diego, tell the rogues | say: `30 join`, close the store | expect: The flare, *"<The circle flares and holds what it called...>"*, a Terror that stands in the circle and does not attack
- [ ] `RN4` (qa.md:5969) step: RN3, then attack a rogue | say: - | expect: The Terror joins the fight; no second rising when the rogues die
- [ ] `RN5` (qa.md:5970) step: Plains, no loan, trip the goons | say: *"Who sends you?"*; then Barter 40 / Outwit 7 / guild / Church / ST 10 threat / Speech 30 lie | expect: Shylocke's name; 100 taken; let pass; stand down; stand down; the intimidation menu then *"K-keep your gold"*; *"A pauper"* -- each once, the leader silent after
- [ ] `RN6` (qa.md:5971) [eyes + save] step: Plains, in debt, trip the goons | say: Barter 40 *"Shylocke's rate is six hundred"* | expect: 600 taken; in Barcelona Shylocke offers no repayment and will lend again
- [ ] `RN7` (qa.md:5972) step: Plains, in debt, a Templar or Inquisitor | say: *"You'd put hands on a sworn brother..."* | expect: *"...his ledger doesn't close for a cross"*; they let you pass; Shylocke still expects payment
- [ ] `RN8` (qa.md:5973) step: Plains, in debt, scare them off (any of the four) | say: Then Shylocke | expect: No repayment offer; a new loan possible
- [ ] `RN9` (qa.md:5974) step: Plains, the goons, a character with Salesman / Eloquence / Educated / Thief / Master Thief / Brutish Hulk / Dark Majesty / Blademaster / Summoning | say: The perk line | expect: The haggle without Barter 40; let pass; the 600; the purse back (Thief +0, Master Thief +50); the four intimidations into the stammer; each once
- [ ] `RN10` (qa.md:5975) step: Fresh Plains, walk to Mauldo's stall, then to the camp's east stake | say: - | expect: *"<A stake cut into a rough cross...>"* once at each; at the camp a PE 7+ character reads the re-set ring instead
- [ ] `RN11` (qa.md:5976) step: Fresh Plains, a Wielder of Cedric's (no Necromancer), walk into the camp | say: - | expect: *"...You are off the hidden street in Barcelona"*; the warning reply -> `21`; study/fight/leave as before
- [ ] `RN12` (qa.md:5977) step: Fresh Plains, a Dark Wielder (Necromancer) | say: *"I know what the circle is for..."* | expect: `22 dark tribute`; accepting arms the Diego quest as before; *"Keep your circle. I have my own."* lets you walk
- [ ] `RN13` (qa.md:5978) step: Fresh Plains, a non-Wielder, and a Wielder with Diego in tow | say: - | expect: The vanilla greeting and `50 Player Has Diego` respectively
- [ ] `RN14` (qa.md:5979) step: Plains, a sworn Inquisitor, talk to Diego | say: *"I am of the Order myself, Inquisitor."* | expect: `21 brother`; "Tell me." reaches his own quest offer unchanged; a non-Inquisitor never sees the reply
- [ ] `RN16` (qa.md:5981) step: Plains, after either rising, talk to Mauldo again | say: - | expect: *"Something answered on the north road..."*; before the rising, the plain return greeting; the low-karma greeting and his shop unchanged

**Plains (Mauldo)**

- [ ] `GS8` (qa.md:2356) step: **Regression.** `Axe of the Feral Curse`, bought from Mauldo in the Plains | say: - | expect: Unchanged: 66 flat against animals, +20 Sneak, +20 Evasion, -1 Charisma, 1,722 gold, still in his stock. Nothing in this release touched it

**Plains / Barcelona Coast / Lake (red crystal node)**

- [ ] `CP11` (qa.md:1349) where: Fresh Plains / Coast / Lake / Grove, walk near the red node | steps: - | pass: *"<A crystal the colour of old blood...>"*; the PE 7+ and Wielder variants; after the third wave the spent line

**Plains or Inquisition Chambers**

- [ ] `PK16` (qa.md:3647) [eyes + save] where: **The judgement row.** Kill a **rogue** inquisitor (the Inquisition Chambers and Plains have them) | steps: Check the sheet | pass: Enemy of the Inquisition should **not** be granted. A rogue has left the order. Decide whether that reads correctly -- the Grand Inquisitor hunts them himself

**Plains, then Torquemada in Barcelona**

- [ ] `RN15` (qa.md:5980) [eyes + save] step: RN14, kill the rogues, return to Torquemada | say: *"There was a cult on the northern plains wearing our habit"* | expect: `413`; 800 XP and 250 gold; the reply gone afterwards; never offered to a non-Inquisitor or before the quest completes

**Random Ethereal Ring / Waterfall Passage / Bounty Hunter Camp**

- [ ] `GB24` (qa.md:4989) step: Fight hats in `Random Ethereal Ring` (12 of them), `Waterfall Passage`, `Bounty Hunter Camp`, `Random Forest Map 1` | say: - | expect: **No alarm** -- those maps have no `Goblin Cave Post`. Only Ravine Cave East was wired this pass

**Ravine Cave East**

- [ ] `BU1` (qa.md:4614) [eyes + save] step: **Act 1**, fresh `Ravine Cave East` entered from `Scar Ravine`. Fight through it | say: - | expect: **Exactly as 0.30.0 and 0.30.1 left it** -- the Khan's goblins, four `Goblin Cave Post` hat posts, the officer alarm, the three-goblin argument. No red goblins, no Hrargrub
- [ ] `BU2` (qa.md:4615) [eyes + save] step: Reach Montserrat and talk to **Brother Montgomerie**, then return to `Ravine Cave East` | say: - | expect: The cave is **Butu's**. Red goblins at the four post positions, and nothing of the Khan's left alive or spawning
- [ ] `BU3` (qa.md:4616) step: Count what is there | say: - | expect: About **24 of capacity** plus the heir, so a shorter fight than act 1's 93 -- the point is that it changed hands, not that it got bigger
- [ ] `BU4` (qa.md:4617) step: Look at them | say: - | expect: **Visibly a different tribe.** `07 Red`. If they read as ordinary goblins in the cave's lighting, say so -- `11 Black` and `08 Purple` are the alternatives
- [ ] `BU5` (qa.md:4618) step: Walk to the far end, **(2319, 748)** | say: - | expect: **Hrargrub**, on the Goblin King model, and he **talks instead of attacking**. 250 HP / AC 225 if it goes wrong
- [ ] `BU6` (qa.md:4619) [eyes + save] step: Read what he calls himself in the log if you fight him | say: - | expect: **Hrargrub**, from his own race. His tribe log as *Butu Officer*, *Butu Archer*, *Butu Goblin*
- [ ] `BU7` (qa.md:4620) [eyes + save] step: Re-enter the cave again after the takeover | say: - | expect: Still Butu's. `Trigger Only Once=1` on both the trigger and the relay
- [ ] `BU8` (qa.md:4626) step: Arrive having **killed Plumjum Khan** | say: *"Plumjum Khan is dead. I killed him."* | expect: `20 you emptied the chair` -- *"You emptied the chair. I am standing in it. I had six winters of reasons and you did it in an afternoon"*
- [ ] `BU9` (qa.md:4627) step: Arrive as the Khan's **Champion** (`Goblin Rank` 3) | say: *"I am the Khan's Champion."* | expect: `30 take off his mark`. He offers the choice; **refusing fights him**, and so does choosing the fight reply
- [ ] `BU10` (qa.md:4628) step: Arrive at **rank 1 or 2** | say: *"The Khan gave me a rank."* | expect: `40 he gives everyone ranks` -- *"He gives ranks the way he gives speeches, and both cost him nothing. Butu gave his goblins poems."*
- [ ] `BU11` (qa.md:4629) step: Arrive having completed **`Rid the Dryad's Forest of the Goblins`** | say: *"I have been killing his goblins for weeks."* | expect: `50 a qualification` -- *"I am not fond of you. I am extremely interested in you."*
- [ ] `BU12` (qa.md:4630) step: Arrive with **no goblin history at all** | say: *"Who was Butu?"* | expect: `60 who was butu`, and the line the whole scene is built on: *"He has drawn plans for six winters. Have you seen the plans? They are very good plans."*
- [ ] `BU13` (qa.md:4631) step: All five routes | say: - | expect: Each leads to `90 the book`. Five entry reads, two of them quest tests in `Custom Requirement=` and two from Fixt's `Goblin Horde *` cans
- [ ] `BU14` (qa.md:4637) step: At `90 the book`, **without** the poetry book | say: *"I will find it."* | expect: `95 agreed`. He does not stand the cave down yet
- [ ] `BU15` (qa.md:4638) [eyes + save] step: Get the `Butu Khan Poetry Book` from the **Goblin Warrens** and bring it back | say: *"I have it here."* | expect: `100 the book returned` -- *"He takes it in both hands, and does not open it."* The book leaves your inventory, XP, and the cave stands down
- [ ] `BU16` (qa.md:4639) step: **If the book is already gone**, tell him so | say: - | expect: **You cannot buy it back** -- an earlier draft of this row said you could, and that was wrong. The turn-in removes the item, Weng Choi's two merchant inventories hold **no books at all**, and the Goblin Warrens copy is the only one placed in the game. So the errand would have been unwinnable; `BU38`-`BU40` are the two routes that close it
- [ ] `BU17` (qa.md:4640) [eyes + save] step: After the handover, walk the cave | say: - | expect: The red goblins **do not attack**. `Butu alliance` clears targeting and drops `Enemy` on `Butu Warriors`
- [ ] `BU18` (qa.md:4641) [eyes + save] step: Open the journal after `95 agreed` | say: - | expect: **`Butu Khan's Poems`** is listed. An earlier draft of this section said there would be no journal entry and that a tracked quest was out of scope -- wrong on both counts, since Fixt has authored fourteen `.Quest.txt` definitions already
- [ ] `BU29` (qa.md:4655) [eyes + save] step: Accept the heir's errand, then check the journal | say: *"I will find it."* | expect: **`Butu Khan's Poems`** at its first state -- *"His Khan's book of poems is somewhere in Plumjum Khan's warren, where it is being kept as shiny."*
- [ ] `BU30` (qa.md:4656) [eyes + save] step: Return the book | say: *"I have it here."* | expect: The quest **completes** -- *"You put Butu Khan's poems back in the hands of his line."* The book leaves your inventory, and the red goblins stand down
- [ ] `BU31` (qa.md:4657) [eyes + save] step: Arrive already **holding** the book, having never taken the errand | say: *"I have it here."* | expect: It still appears in the journal **and then completes**, rather than completing something that was never listed. Both states fire in order on that path deliberately
- [ ] `BU33` (qa.md:4659) [eyes + save] step: Kill Hrargrub **with the contract taken** | say: - | expect: The quest completes, and **`Goblin Rank` advances** -- invoked through `Advance Goblin Rank` with `CUseCannedActionAction`, the way the Khan's own tree already invokes it. Check the perk and faction actually changed
- [ ] `BU34` (qa.md:4660) [save] step: Kill Hrargrub **without** ever taking the contract | say: - | expect: **No quest completes and no rank is given.** The death hook is guarded on `CWasQuestEverActivatedAction`, so killing him on your own account pays nothing
- [ ] `BU36` (qa.md:4662) [eyes + save] step: Try to do **both** | say: - | expect: You cannot. Returning the poems stands the cave down and shuts the act 8 gate; killing him closes the other. Confirm neither route leaves the other's quest stuck open in the journal
- [ ] `BU38` (qa.md:4680) [eyes + save] step: Turn the book in to **Weng Choi** in act 1, then meet Hrargrub and tell him | say: *"I gave them to a collector in the city. He keeps rare books, and he will read it."* | expect: `101 the collector` -- *"A human who keeps words he cannot eat... Then Butu is read in a city that never heard of him, which is further than Plumjum has ever carried anything."* The cave stands down and the errand **completes**. Gated on that quest, so the reply only exists if it is true
- [ ] `BU39` (qa.md:4681) step: On a character who never dealt with Weng Choi, look for that reply | say: - | expect: **Not offered.** The player cannot claim the collector without having used him
- [ ] `BU40` (qa.md:4682) [eyes + save] step: Tell him you sold them | say: *"I sold them."* | expect: `102 the price of poems` -- he puts his hand out and **takes 250**, the exact figure vanilla pays for it, with `CTakeMoneyAction`. *"I did not pick the number. A human did, and you took it."* The errand still completes; the insult is the price, not a refusal
- [ ] `BU41` (qa.md:4683) [eyes + save] step: Do BU40 with **less than 250 gold** | say: - | expect: He deals anyway. The take is wrapped in `CHasMoneyAction`, so a poor player is not softlocked out of the alliance -- confirm no money goes negative
- [ ] `BU42` (qa.md:4684) [eyes + save] step: Across all three routes -- returned, collector, sold | say: - | expect: **Three ways to close `Butu Khan's Poems` and no dead end.** Returning the book is still the best of them: it is the only one where he holds it
- [ ] `BU43` (qa.md:4773) [eyes + save] step: **The row this release most needs.** As a Goblin **Champion**, write down Sneak, Barter, carry weight and poison/disease resistance. Side with Hrargrub. Read them again | say: - | expect: Sneak, Barter, poison and disease should have **dropped by the Champion faction's amounts**, and melee/crushing/slashing/carry risen by the Fallen Champion's. **If the old numbers are still there on top of the new ones**, factions accumulate rather than replace, the inference this build rests on is wrong, and the revoke can has to come back. Report the actual numbers, not a yes or no
- [ ] `BU44` (qa.md:4774) [eyes + save] step: Same as a **Chum** (rank 1) | say: - | expect: **Goblin Traitor - Bad Blood**: melee +20, crushing +15. The poison resistance and carry weight go away entirely, so it is a different build rather than a better one
- [ ] `BU45` (qa.md:4775) [eyes + save] step: Same as **Blooded** (rank 2) | say: - | expect: Also Bad Blood. Ranks 1 and 2 share a tier on purpose
- [ ] `BU46` (qa.md:4776) [eyes + save] step: Same having **never joined the horde** | say: - | expect: **Goblin Traitor - Foe**: melee +10 and nothing else. He is taking a nobody and pays accordingly
- [ ] `BU47` (qa.md:4777) [save] step: Check the perk list after any of them | say: - | expect: A **Goblin Traitor** title perk, and the old goblin title **still there** -- nothing in the engine can remove a perk, and the titles carry no modifiers of their own. *"The Horde has a word for it and the word is not Champion."*
- [ ] `BU52` (qa.md:4796) [save] step: Side with the heir by any of the three book routes, then check inventory | say: - | expect: **Silver Mine Deed.** Handed over in the reply rather than the relay, because `$Instigator` only reliably resolves to the player in a reply's Custom Action
- [ ] `GB19` (qa.md:4984) step: A **high-level** party, fresh `Ravine Cave East`. Find a goblin wearing a hat and hit it once | say: - | expect: The archer posts converge. `COnlyOnceAction`, so it happens once. **Count them and report the number** -- the design budget is 12 and the troll pack alarm had to be rescoped after exactly this measurement
- [ ] `GB20` (qa.md:4985) step: Hit the same officer again, or a second officer | say: - | expect: **No second alarm.** `Trigger Only Once`
- [ ] `GB21` (qa.md:4986) step: Hit the rabble and the archers, never the officer | say: - | expect: **No alarm at all.** Only the hat raises it. If striking an ordinary goblin brings the cave, report it
- [ ] `GB22` (qa.md:4987) step: A **low-level** party in the same cave | say: - | expect: Likely no alarm, because likely no officer -- the Hat is top-tier only. Worth confirming the cave still plays as it always did
- [ ] `GB30` (qa.md:5020) step: Fresh `Ravine Cave East`, entered from `Scar Ravine` (not from the mine -- there is no passage between the halves). Fight inward until **one** goblin is dead | say: - | expect: Over **Drubjub**: *"They have butchered our brothers with alarming ease. Perhaps discretion would be the more prudent course of action?"*
- [ ] `GB31` (qa.md:5021) step: Kill a **second** goblin | say: - | expect: Over **Wumjup**, a different goblin: *"Nonsense, we are Mongol-trained goblins, the scourge of the land!"*
- [ ] `GB32` (qa.md:5022) step: Kill a **third** | say: - | expect: Over **Lumgrub**, a third goblin: *"Yes, Wumjup is right! Muster up your courage and attack! AIIIIiiiiIIII!"* **This is the payoff -- Lumgrub names Wumjup, and Wumjup is the one who actually said it**
- [ ] `GB33` (qa.md:5023) step: Keep killing goblins after that | say: - | expect: **Nothing more.** `When Done=Do Nothing`, so the series stops on the third line and does not loop
- [ ] `GB34` (qa.md:5024) step: Check that the three balloons appeared over **three different goblins** | say: - | expect: The whole point. If all three stack over one goblin, `Name of Position` is not resolving by name and the build has failed
- [ ] `GB35` (qa.md:5025) step: Find the three of them before killing anything -- mid-cave, around (2174, 1197) | say: - | expect: A plain goblin, a `Mongol Goblin Tough` and another plain goblin standing together. They fight normally; nothing about them is pacified
- [ ] `GB36` (qa.md:5026) step: Kill **Wumjup first**, then three other goblins | say: - | expect: The exchange still runs and simply skips his line. `Require Success To Advance=0`, so a dead speaker does not stall the series -- the alternative was it jamming forever on line B

**Ravine Cave West**

- [ ] `WS2` (qa.md:1919) [save] step: The same character in **Ravine Cave West** | say: - | expect: **Unchanged** at about a third. The caves were already correct and must not have moved
- [ ] `BU58` (qa.md:4802) step: Keep it instead and take it to the **Mine Foreman** at Ravine Cave West | say: *"The mine is mine. I have the paper that says so, and a goblin gave it to me."* | expect: `90 the paper` -- *"He takes it, holds it the wrong way up, and hands it back with enormous care… Nurg saw nothing."* The mine opens by title instead of favour
- [ ] `BU59` (qa.md:4803) step: Confirm the symmetry that makes the deed the right gift | say: - | expect: Betraying Plumjum **closes** the `Goblin Horde IS` route past the foreman; the deed **reopens** it. A player who sides with the heir must not be locked out of the Sacred Scimitar as a side effect
- [ ] `BU60` (qa.md:4804) step: Check the foreman's other routes on a character who never met the heir | say: - | expect: Horde mark, Barter 40, Speech 40, Schmooze 7, the ungated demand, the fight, the exit. **Nine nodes now, was eight**
- [ ] `BU61` (qa.md:4805) [save] step: Loot the silver after using the deed | say: - | expect: Exactly one *Magnetized Silver*. The deed moves the guards, not the ore
- [ ] `BU62` (qa.md:4806) step: Sell the deed to Shylocke **and** then try the foreman | say: - | expect: One or the other, not both. That is the intended choice, so confirm the foreman reply is simply absent rather than failing oddly
- [ ] `DN6` (qa.md:4859) [save] step: Attack the **Mine Foreman** at Ravine Cave West instead of parleying | say: - | expect: He logs as **Mongol Goblin Officer**. His dialogue still calls him Nurg; the log cannot show that without giving him a race of his own, which is noted as a refinement rather than done -- *0.60.3 found the log prints the can's User Assigned Name, not the race name this release edited. Expected names here came from race names, but 0.60.3 found the log prints the can's User Assigned Name (a hat goblin logs Goblin Striker). A different name is not a failure on its own; check it against the can.*
- [ ] `GB23` (qa.md:4988) step: The **Mine Foreman** in Ravine Cave West: attack him instead of parleying | say: - | expect: He is `Mongol Goblin Hat Tough`, so he carries the alarm -- but `Goblin Cave Post` does not exist in that map and the alarm is guarded on the name existing, so it must be a **no-op**. `Mine Guards` should wake exactly as they did via the dialogue's fight reply, and nothing else
- [ ] `MF1` (qa.md:5066) step: Enter `Ravine Cave West` from Scar Ravine and walk in about 800 units | say: - | expect: A `Mongol Goblin Hat Tough` -- **Nurg** -- challenges you instead of attacking, with archers around him. *"Far enough… every bow in the dark comes up at once, and none of them wavers."* **They do not shoot**
- [ ] `MF2` (qa.md:5067) step: With **no goblin standing**, choose *"I have come for the silver. Stand aside."* | say: - | expect: `60 refused`. He warns you and nothing attacks -- *"Come for it with coin, or a mark, or a better tongue than that."* You can walk off and come back, so the routes are discoverable without a fight
- [ ] `MF3` (qa.md:5068) step: With `Goblin Horde IS`, choose *"I wear the Khan's mark."* | say: - | expect: `20 the khans man`. The bows go down before he speaks -- *"Then it was never ours to keep."*
- [ ] `MF4` (qa.md:5069) step: With Barter 40+, choose *"I am the buyer you have been waiting on."* | say: - | expect: `30 the price`. This is the one the fiction asks for -- Eduardo says they are driving the price up, so they are sellers with no buyer. *"Four months we sit on rock nobody comes for"*
- [ ] `MF5` (qa.md:5070) step: With Speech 40+, take the reasoned route | say: - | expect: `40 reasoned past` -- *"The Khan hears about dead humans in his mine. He does not hear about rock."*
- [ ] `MF6` (qa.md:5071) step: With Schmooze 7+, take the charm route | say: - | expect: `50 charmed` -- *"You talk like a goblin."*
- [ ] `MF7` (qa.md:5072) [eyes + save] step: After any of MF3-MF6, walk deeper toward the silver | say: - | expect: **The three deeper goblin posts do not attack either.** `Mine passage granted` clears targeting and drops `Enemy` on all four posts. This is the whole point: the parley opens the road
- [ ] `MF8` (qa.md:5073) [save] step: Reach the bone pile at roughly (1983, 455) and loot it | say: - | expect: *Magnetized Silver*, **exactly one**. Negotiation moved the guards, never the ore -- the pile is where vanilla put it
- [ ] `MF10` (qa.md:5075) step: On a fresh character, choose *"Then your people can decide."* | say: - | expect: Nurg **and** the whole archer post turn on you at once. `CGoToCombatAction` on `$Trigger` and on `Mine Guards`
- [ ] `MF11` (qa.md:5076) step: On a fresh character, attack Nurg without talking | say: - | expect: He fights, and so does his post. The deeper posts are hostile as they always were -- the combat route is unchanged
- [ ] `MF12` (qa.md:5077) step: Choose *"Another time, then."* | say: - | expect: He lets you leave -- *"Walk out the way you walked in, and we stay bored."* No state change; you can return and parley
- [ ] `MF13` (qa.md:5078) step: The wasps, on every route | say: - | expect: **Still hostile, and still 57 of them.** A parley gets you past the goblins; it does not clear the nest, and a pure talker may still have to survive the walk to the pile
- [ ] `MF13a` (qa.md:5079) step: **Open question.** Toggle Sneak on and walk in without talking to anyone | say: - | expect: Does anything notice? `Sneak` is a real skill with a HUD toggle and tiers at 10/20/25/35, the wasps carry `Sneak Adjustment=0` and every goblin `+15` -- but what that field *means* is unresolved. Its extremes are Wererat Minions at **-300** and Assassins at **-85**, against Skeletons and Zombies at **+25 to +50**, which reads like the creature's own stealth rather than its alertness. Static analysis cannot settle it; one walk with Sneak up will. **Report what happens**
- [ ] `MF13b` (qa.md:5080) step: If MF13a gets you to the pile untouched, try it again with Sneak **off** | say: - | expect: The control. If sneaking made no difference, the field is about the creature's own stealth and the cave has no stealth route -- which is worth knowing before anyone designs one
- [ ] `MF14` (qa.md:5081) step: Count the archers at the mouth on a weak and then a strong party | say: - | expect: It scales -- the post spawns 1 Archer at `Max Party Mojo=3`, up to 2-3 Archer Supers at 25. The threat is meant to read as serious
- [ ] `MF15` (qa.md:5082) [eyes + save] step: Parley successfully, leave the cave, come back | say: - | expect: The posts should still be stood down. `Mine passage granted` is `Trigger Only Once=1`, so if they are hostile again on re-entry, report it -- that is the entity-snapshot question

**Ravine Cave West / Scar Ravine**

- [ ] `Q6` (qa.md:995) [eyes + save] where: Ravine Cave West / Scar Ravine | steps: Kill **Cursed or Tainted** wasps | pass: Stingers drop. Plain wasps give none -- 6 of the 9 cans carry it

**Raylark**

- [ ] `PK3` (qa.md:3634) where: After `PK1`, return to **Raylark** | steps: - | pass: A new reply about the vale being quieter. He approves, and complains that every goblin you take is a bounty he never collects

**River**

- [ ] `WS3` (qa.md:1920) [save] step: **River**, a map never entered, at mojo 5 or below | say: - | expect: Wasps there can now drop at all. That band was **0%** -- a pack that could never produce a stinger

**Scar Ravine**

- [ ] `C24` (qa.md:255) steps: Any character | pass: *"What would you take for her?"* is visible and reaches `40 goblin offers trade` -- **unreachable in vanilla**
- [ ] `C26` (qa.md:257) steps: From `40`, **Character B** | pass: Only the fight and the walk-away replies; both still behave as vanilla
- [ ] `C27` (qa.md:258) steps: **Character B**, whole scene | pass: The Speech 55 route and every combat route work exactly as vanilla
- [ ] `MS20` (qa.md:1295) where: Scar Ravine, the goblin holding the girl | steps: ST 8+: *Try.* / Barter 55: the salt-pork offer | pass: The goblin backs down (`71`) or takes the trade (`72`) in his own words; neither mentions the Khan. The Horde and Speech routes still get *"Y-you know the Khan?"*
- [ ] `WS1` (qa.md:1918) [save] step: **The reported row.** A character at mojo 5 or below, on a Scar Ravine that has never been entered. Clear the main area, counting wasps killed and stingers taken | say: - | expect: Roughly **one stinger per three wasps**. Five stingers should cost about fifteen kills, where before the fix the band was 9% and cost about fifty-five
- [ ] `WS4` (qa.md:1921) step: **Regression.** A character above mojo 5 in Scar Ravine | say: - | expect: Unchanged. Only the `Max Party Mojo=5` band was touched; the 10, 50 and 65 bands keep their exact weights
- [ ] `GL1` (qa.md:5099) step: Talk to the goblin, choose *"I was never here, and neither were you."* | say: - | expect: **He lets you go.** No combat, no state change. The scene is still running and you can come back and save her
- [ ] `GL2` (qa.md:5100) step: Talk again and choose *"It's no concern of mine what you do with her"* | say: - | expect: He still attacks, exactly as vanilla. That route was deliberately left alone -- the fix adds a way out, it does not remove one
- [ ] `GL3` (qa.md:5101) step: With Speech 55, choose *"Let me take this child to the Goblin Khan…"* | say: - | expect: The reply is tagged **`<Lie>`**, and it resolves as it always did: he backs down, she escapes, the quest completes as a rescue. The label is the fix -- the words and the outcome finally agree
- [ ] `GL4` (qa.md:5102) step: Regression: ST 8+, Barter 55, and killing him | say: - | expect: All three still free her. `71 backs down`, `72 the trade`, and the fight are untouched
- [ ] `GL5` (qa.md:5103) step: **With goblin standing**, choose *"I carry the Khan's favour…"* (Quest icon) | say: - | expect: `73 the handover`. Grimek steps back, disowns her, and names himself. You take her
- [ ] `GL6` (qa.md:5104) step: After GL5, watch both of them | say: - | expect: **She walks off and vanishes; Grimek also leaves and is gone.** He is disposed of exactly as the rescue routes do it -- if he is still standing there, that is the bug this tier fixed
- [ ] `GL7` (qa.md:5105) [eyes + save] step: **With no goblin standing at all**, choose *"The Khan would want to know who fed him this well…"* | say: - | expect: `74 a way in`. He sponsors you, and you become a **Goblin Chum** -- first standing, earned by the act. `savecheck save` should show `Goblin Rank=1`
- [ ] `GL8` (qa.md:5106) [save] step: After either delivery, check your character | say: - | expect: **Slayer of Innocents** title gained, and **-50 karma**. `savecheck save` shows the karma; the title shows in the perk list
- [ ] `GL18` (qa.md:5116) [save] step: Deliver, then check `python tools/savecheck.py save latest` | say: - | expect: Karma down 50, `Goblin Rank` set, and the title in the perk list. This is also the cheapest check that `$Instigator` resolved to the player in the reply action
- [ ] `BA26b` (qa.md:5841) [eyes + save] step: Attack the **woodcutter's daughter** in Scar Ravine | say: - | expect: The same, plus the goblin turns on you and *Find the Woodcutter's lost son* fails. Then ask the woodcutter about her: he already reads `daughter attacked` in vanilla

**Scar Ravine / Crossroads**

- [ ] `BU51` (qa.md:4781) [eyes + save] step: Try a `Goblin Horde IS` gate elsewhere afterwards -- the Scar Ravine goblin, the Crossroads patrol | say: - | expect: The rank is 0 now, so those routes are closed. **This is the leak worth watching**: the Mine Foreman is the one that matters, and the deed is why it is survivable

**Scar Ravine, 05 Troll Pit**

- [ ] `BA26g` (qa.md:5846) [save] step: Let the goblin stand over the daughter, or the trolls over Tomas, and do nothing | say: - | expect: **No title.** No enemy on those maps can target a neutral, so only the player can trigger a child's hook

**Woodcutter Forest**

- [ ] `GL9` (qa.md:5107) step: After delivery, go to the woodcutter's house | say: - | expect: She is **not** there. Her home generator is deleted, as on the attacked path
- [ ] `GL10` (qa.md:5108) step: Deliver her **without** having taken the quest, then meet Felipe | say: - | expect: He asks for help as normal, and the accept reply is **absent**. Nothing records a failure, because there was no quest to fail -- `CSetQuestSatusToFailedIfActiveAction`
- [ ] `GL11` (qa.md:5109) [save] step: Take his quest first, then deliver her, then return | say: - | expect: The quest is **failed**
- [ ] `GL12` (qa.md:5110) step: Talk to Felipe after delivering or striking her, choose *"I am the reason she did not come home."* | say: - | expect: `31 she never came home`. He does not shout and does not attack. **He shuts the cave**
- [ ] `GL13` (qa.md:5111) step: The same, choosing *"I searched the forest and found nothing."* | say: - | expect: Tagged `<Lie>`, and it lands on the same node. He is not fooled; the cave still closes
- [ ] `GL14` (qa.md:5112) step: After GL12, try to get the Darkwood | say: - | expect: You cannot. The cellar never opens -- `COpenDoorAction` lives in a task only he performs. The **Wielders'** first task is closed, and that is intended: the **Dark Wielders** remain open through Relican, reachable via Brambles or on sight
- [ ] `GL15` (qa.md:5113) step: Strike Gloria instead of delivering her, then talk to Felipe | say: - | expect: The same `31` response. From his side the outcomes are identical -- she never came home either way
- [ ] `N7` (qa.md:6010) [eyes + save] pass: Quest completes and the reward is paid as vanilla. No rank, no error

**goblin maps**

- [ ] `BV8` (qa.md:3485) where: **0.52.1.** Fight a goblin one-on-one -- `Mongol Goblin`, an Archer or a Shaman | steps: Trade blows until you see both a swing bark and a wounded bark close together | pass: **Both are readable.** The wounded line sits clearly higher above the goblin's head than the attack line. Before 0.52.1 they drew at the identical point and overlapped
- [ ] `BV9` (qa.md:3486) where: **0.52.1, the judgement row.** Same fight | steps: - | pass: Is stacked-but-readable good enough? Both barks still *fire* -- 0.52.1 separated them, it did not make one yield. If two lines at once still reads as too much, the next step is a per-creature suppression flag, which is blocked on an engine question about whether a delayed action survives its owner's death
- [ ] `BV10` (qa.md:3487) where: **0.52.1, the one that would mean I got it backwards.** Any goblin that gets wounded | steps: - | pass: The wounded balloon is **above** the goblin, not inside or below it. The offset axis was inferred from shipped values (goblins -60, taller families -70) rather than read out of the engine. If it renders low or inside the model, the sign is wrong and it is a one-character fix

**wherever Mongol Goblin Shamans spawn**

- [ ] `BV5` (qa.md:3482) where: **Mongol Goblin Shaman**, any variant | steps: Fight one and watch which spells it casts | pass: It still casts **both Spike and Static Charge**, with Static Charge roughly twice as common. Its pads encode that mix; if it has started casting almost nothing but Spike, the pad cycling was wrong

**anywhere in the act**

- [ ] `GS5` (qa.md:2353) step: A weapon of **Goblin Slaying** in the Wilderness | say: - | expect: Large, about 22 on a 6,000 gold weapon, and goblins are 20% of what the Wilderness spawns
- [ ] `DN5` (qa.md:4858) [save] step: Fight a goblin in a hat anywhere -- `Bounty Hunter Camp`, `Waterfall Passage`, `Random Ethereal Ring`, `Random Forest Map 1`, `Ravine Cave East` | say: - | expect: **"Mongol Goblin Officer"**, not "Goblin Grumjun" -- *0.60.3 found the log prints the can's User Assigned Name, not the race name this release edited. Expected names here came from race names, but 0.60.3 found the log prints the can's User Assigned Name (a hat goblin logs Goblin Striker). A different name is not a failure on its own; check it against the can.*
- [ ] `DN9` (qa.md:4862) [save] step: Any ordinary goblin, and any goblin shaman | say: - | expect: Unchanged -- *Mongol Goblin* and *Goblin Shaman*. Only the hat and khan races were touched -- *Expected names here came from race names, but 0.60.3 found the log prints the can's User Assigned Name (a hat goblin logs Goblin Striker). A different name is not a failure on its own; check it against the can.*
- [ ] `GB2` (qa.md:4934) step: Fight them for a long stretch -- several minutes | say: - | expect: **It should take a long time to hear a repeat.** 40 lines for the rabble. This is the row the first build would have failed
- [ ] `GB3` (qa.md:4935) step: Listen for the register | say: - | expect: They talk about **eating you**, which is vanilla's own goblin voice: *"The pot is already hot, morsel."*, *"Your bones go in the broth. The rest of you goes in the bowl."*, *"Me eat brain! Then me am smart!"*
- [ ] `GB4` (qa.md:4936) step: Fight a goblin **archer** and a plain goblin in the same run | say: - | expect: Different registers. The archer talks distance -- *"No closer, meat. I like you at this distance."*, *"I do not have to be brave at this range."*
- [ ] `GB5` (qa.md:4937) step: Fight a `Mongol Goblin Hat` / `Hat Tough` / `Hat Super` | say: - | expect: Orders, not hunger -- *"Form! Form, you stupid things!"*, *"It is one of them and twelve of you. Explain that to me."*, *"I will tell the Khan who fought. I will also tell him who did not."*
- [ ] `GB6` (qa.md:4938) step: **Hurt** a goblin without killing it, repeatedly | say: - | expect: A second register entirely, rarer (about one hit in six): *"They are too mighty!"*, *"We must flee and make haste!"*, *"Run! AIIIIiiiiIIII!"*, *"Where is the one with the hat? Where is he!"* **Three of those are vanilla lines `Bounty Hunter Camp` was the only map ever to fire**
- [ ] `GB7` (qa.md:4939) step: Fight a `Mongol Goblin Shaman` and watch it **attack** | say: - | expect: It barks too, which the first build could not manage. Its `Shoot Completed` is a spell *picker*, so the bank went in as a fourth item: *"Flesh is a borrowed thing, and I am calling it back!"*, *"Rakeb taught me this one."*
- [ ] `GB8` (qa.md:4940) step: Watch the shaman's **spells** across a long fight | say: - | expect: **Still Spike and Static Charge, still roughly 1:2.** The picker kept all three of its selections and gained the bark as a fourth. If a shaman stops casting, this is the row that failed
- [ ] `GB9` (qa.md:4941) step: Talk to the **Khan**, **Rakeb**, **Grumdjum**, the Warrens' **Goblin Girl** and **Goblin Guard**, and the **Crossroads Patrol Leader** | say: - | expect: All six exactly as before. **Named and talkable goblins were deliberately given no barks** -- a named character must not speak the rabble's lines
- [ ] `GB10` (qa.md:4942) [save] step: Check the combat log during all of the above | say: - | expect: Barks are **not** in it. `Include In Log=0`
- [ ] `GB11` (qa.md:4960) [eyes + save] step: Burn a goblin. Any fire source, any tier | say: - | expect: **Noticeably more damage.** Fire is the family signature. Nothing else in the game is reliably fire-vulnerable -- wererats are immune and the English resist it 73
- [ ] `GB12` (qa.md:4961) [eyes + save] step: Poison or disease a goblin | say: - | expect: **Nothing.** Both 100, vanilla's own immune value. They eat carrion and brains. The log should say *"resists all of your damage"*
- [ ] `GB13` (qa.md:4962) [eyes + save] step: Hit the **rabble** with a blunt weapon, then a blade | say: - | expect: Crushing -20 against slashing -10: the club should beat the sword. Small bodies, no armour
- [ ] `GB14` (qa.md:4963) [eyes + save] step: Now hit a **hat officer** with the same two weapons | say: - | expect: **It inverts.** Slashing and piercing +20, crushing 0. The officer wears real kit and needs a different answer than the rabble around him
- [ ] `GB15` (qa.md:4964) [eyes + save] step: Hit a **shaman** with Static Charge or Lightning Bolt | say: - | expect: Electrical 50, about half. They throw lightning themselves, so lightning is the wrong tool. Burn them
- [ ] `GB16` (qa.md:4965) [save] step: Check the log on a resisted hit | say: - | expect: `hit ... for <UnresistedDamage> ... (Resisted <n>) INFLICTED <Damage>`. The save logs every hit with its damage type, so one save file settles GB11-GB15 exactly
- [ ] `GB38` (qa.md:5028) step: Watch for the hide-style failure: does killing a goblin do anything it did not before? | say: - | expect: Their `Destroyed Script Action` was empty in vanilla and no `Ravine Cave East` generator sets one, so nothing was overridden -- checked, because `CSetDestroyedScriptActionAction` on a generator is what made the Lava Troll Hide dead code from 0.10.0
- [ ] `GB39` (qa.md:5029) step: **The row this repair exists for.** Find a goblin fighting **alone** -- `Mongol Goblin` spawns alone in 48 of its 64 groups, so this is the common case rather than a hunt. Hurt it and read the bank out | say: - | expect: **Nothing refers to a companion**, a line, or anyone standing behind it. The reported line was `<He looks for the goblin who was beside him a moment ago.>`; it is now `<He looks around for help, and takes his time about believing there is none.>`
- [ ] `GB40` (qa.md:5030) step: A **lone officer** -- `Mongol Goblin Hat`, which is alone in **12 of its 13** groups | say: - | expect: No *"Hold the line!"* and no *"the line tightens"*. He now points and keeps pointing until something moves, which is the joke when nothing does. These were the most frequently wrong of the seven
- [ ] `GB41` (qa.md:5031) step: A goblin fighting **in a group**, any type | say: - | expect: The reworded lines must still read correctly *with* company -- that is the half a deletion would have got for free and a rewrite has to earn. If any of the seven now sounds wrong in a crowd, say which
- [ ] `GB42` (qa.md:5032) step: Count the barks across a long fight | say: - | expect: **Still 92 nodes**, 105 distinct lines with the vanilla ones. Nothing was removed: four banks would have been thinned by deleting the seven, and bank size is the whole defence against repetition

## 2 Montserrat (161)


**01 Grove Exterior**

- [ ] `KM5` (qa.md:2079) [eyes + save] step: **Regression.** Attack a calmed snakebreed during the sentry's parley | say: - | expect: The fight comes back, and **no** Karma change. You gave no word, and the same relay fires if you simply refuse him
- [ ] `KM6` (qa.md:2080) [eyes + save] step: **Regression.** Refuse the sentry outright, or close his conversation | say: - | expect: Hostile, no Karma change
- [ ] `TR1` (qa.md:2090) step: **The reported row.** Let the sentry hail you, then force-attack a calmed snakebreed while the conversation is open | say: - | expect: The whole garrison comes back at you and the three gate packs spawn, exactly as if you had attacked the sentry. Before this it took the hit, did not fight back, and nothing noticed
- [ ] `TR2` (qa.md:2091) step: Let him hail you with an assassin still alive nearby, and just talk | say: - | expect: Nothing attacks you. The parley pacifier now covers `Assassin`, which the accept block always did and it did not
- [ ] `GR1` (qa.md:2121) step: **The reported row.** Fight to the gates, then let the sentry hail you and hold the conversation open | say: - | expect: Nothing attacks you while you talk. Before this, any Viper, Crusher or Summoner still alive kept swinging, because the pacifier named six creatures that do not exist and one that does
- [ ] `GR2` (qa.md:2122) [eyes + save] step: Accept the invitation and watch the gate yard as you are taken | say: - | expect: The whole garrison is standing down, not just the plain snakebreed
- [ ] `GR4` (qa.md:2124) step: **Regression.** Refuse the sentry, or attack him | say: - | expect: The whole garrison comes back at you, including the Vipers and Crushers, and the three gate packs spawn. `sentry draws` had the same half-matching list
- [ ] `SN2` (qa.md:2636) step: Take it through | say: - | expect: He demands your steel exactly as before, and you are delivered. Nothing about the route changed
- [ ] `SN3` (qa.md:2637) step: Start again and name the trap | say: *"This is a trap, but I suppose I have no choice."* | expect: He answers *"I was told to bring you up alive..."* and does **not** reassure you. Then you can go on, or still draw
- [ ] `SN4` (qa.md:2638) step: **Regression.** Run the Outwit 6 bluff, and the Demokin or Sylvant line | say: - | expect: Both unchanged, both still deliver you armed or unsearched as before
- [ ] `SN5` (qa.md:2639) step: **Regression.** Pick the fight instead, at every step including the new node | say: - | expect: `sentry draws` fires every time. There is still no node you can get stuck in
- [ ] `CV12` (qa.md:3327) step: **`01 Grove Exterior`, not yet visited**: with Cortes as a companion, let his remark fire twice | say: - | expect: *"I yearn to find the treasure. Let us return to our quest."* first, then *"Keep that madman Cervantes away from me."* -- **and control returns both times.** The remark plays inside a non-interactive sequence and each entry carries its own end; one that did not would freeze you exactly like the Cathar hang

**01 Grove Exterior (first of his exit points)**

- [ ] `CF1` (qa.md:3290) step: Take **Cortes** as a companion with a **female** character, then reach the point where he has to leave: the Montserrat grove, Montaillou's hamlet, the Titan village, the Crypt entrance, the Heart entrance, the Mountain Pass or the Plains | say: - | expect: **He says goodbye**, in the line recorded for a woman. In the shipped game he leaves without a word
- [ ] `CF2` (qa.md:3291) step: **The regression row.** The same with a **male** character | say: - | expect: **Unchanged**, exactly the farewell that always played. The branch tests for *female* and falls through to the male line, so a male character cannot be affected
- [ ] `CF3` (qa.md:3292) step: Either gender: check he actually goes | say: - | expect: He is still released from the party and still walks off. `CReleaseCompanionAction` and the sequence around it were not touched; only the line he speaks is now chosen

**01 Grove Exterior or 02 Druid Council Level1**

- [ ] `SB1` (qa.md:6165) **NEW** [eyes + save] where: Grove Exterior or Druid Council Level 1, a save that has not entered it | steps: Fight a Snakebreed Summoner | pass: It casts, says a summoning line, and snakebreed appear beside it. They vanish on their own about a minute later | new: True
- [ ] `SB2` (qa.md:6166) **NEW** [eyes + save] where: The same | steps: Kill the Summoner while its brood lives | pass: The log says the brood unravels, and every summoned snakebreed on the map is gone. Ordinary snakebreed are not | new: True
- [ ] `SB3` (qa.md:6167) **NEW** [eyes + save] where: The same, peaceful route | steps: Take Sahar's ring or the parley while a brood is out | pass: The summoned snakebreed stand down with the rest | new: True

**02 Druid Council Level1**

- [ ] `RT7` (qa.md:2063) step: **The great door.** Escape the cell up the stair so Level 1 is first entered from below, then try the great door switch | say: - | expect: It works and the exit polygon is there. Before this you were forced out through the sanctum
- [ ] `WA1` (qa.md:2640) step: Enter Level 1 by **fighting**, clear the hall and the pack beyond it, then talk to the wounded assassin | say: - | expect: *"You are late. They have gone on without me."* His original line, unchanged, because now it is true
- [ ] `WA2` (qa.md:2641) step: **The row that matters.** Get delivered to the pen, escape by the drain, then find him with his own side still alive nearby | say: - | expect: *"They can see me from there. I am not worth the walk."* If he says *"gone on without me"* while they are standing there, the gate did not take
- [ ] `WA3` (qa.md:2642) step: From either opening, ask him everything | say: - | expect: The same eight replies, the same answers, the same Speech 40 and Demokin branches. The two openings differ only in their first line
- [ ] `WA4` (qa.md:2643) step: Talk to him, walk away, come back | say: - | expect: *"Still here? Finish it, or go."* -- the return node, from either opening
- [ ] `WA5` (qa.md:2644) step: **The thing that used to be invisible.** Click him on a save where the hall ambush is alive and unsprung | say: - | expect: He is reachable and says something. He used to do nothing at all, with no way to tell him from scenery

**02 Druid Council Level1; 01 Grove Exterior**

- [ ] `MS1` (qa.md:6191) **NEW** [eyes + save] where: Montserrat peaceful route, a save that has not entered Druid Council Level 1 | steps: Take Sahar's ring, then walk back through Level 1 and the Grove | pass: No snakebreed or assassin attacks you, including the group in the hall and its runner; the wounded assassin still talks | new: True

**02 Druid Council Level2**

- [ ] `PQ1` (qa.md:1958) step: **The reported row.** Take her ring, then walk east | say: - | expect: The wooden posts are open. Before this only killing her opened them, because the only thing that opens them is Brother Montgomerie's tree and he never appears on this route
- [ ] `PQ2` (qa.md:1959) step: **She says no.** Ask her to send you north | say: - | expect: A refusal, not the ring. *"No. I have no wagons left, no sisters to spare..."*
- [ ] `PQ3` (qa.md:1960) step: **A talker.** Speech 50 or better | say: - | expect: *"You need a courier more than you need a corpse"*, then she asks why you would arrive. `IN 7+` or `CH 7+` answer it best
- [ ] `PQ4` (qa.md:1961) step: **Her own orders.** Outwit 9 | say: - | expect: She makes you name who gave them. `Outwit 10` names him
- [ ] `PQ5` (qa.md:1962) step: **The payoff.** Reach `56 she is satisfied` by either route | say: - | expect: She names the pass above Montaillou, and an old man east of here. New information; the route never gave you any
- [ ] `PQ7` (qa.md:1964) step: **Lose it on purpose**, once from each of the five nodes | say: - | expect: She ends the parley and the fight starts. **One strike** -- there is no second attempt
- [ ] `PQ8` (qa.md:1965) step: **The keypress.** Press Escape at her refusal | say: - | expect: The conversation closes and **nothing attacks you**. She can be hailed again. 0.79.9 shipped the opposite of this
- [ ] `PQ9` (qa.md:1966) step: **No levers at all.** Speech under 50, Outwit under 9, Barter under 50, never met Pau | say: - | expect: Two unmarked replies, the explicit fight, and the way out. Say if this reads as a dead end rather than a choice -- *Say if it reads as a dead end*
- [ ] `PQ10` (qa.md:1967) step: **The tell.** Look at the icons on her replies | say: - | expect: The safe and the fatal reply look identical. If one is marked and the other is not at any node, that is the bug this release fixed coming back
- [ ] `PQ11` (qa.md:1968) step: **Regression.** Her opening line | say: - | expect: Ends *"...while you were lying in my cellar."* She should never sound like she is helping you decide
- [ ] `PQ12` (qa.md:1969) step: **The pop.** Walk into the sanctum from the Grove, and again from the prison stair | say: - | expect: She is already standing on the step. Before this she was created by a trigger 230 units away and appeared in front of you
- [ ] `PQ13` (qa.md:1970) step: **She holds her ground.** Watch her before speaking, and again after | say: - | expect: She stays on the reliquary step and turns to watch. She used to wander up to 110 units, which also contradicted her own lines
- [ ] `RD1` (qa.md:1976) step: **The row that proves the release.** Meet Sahar | say: - | expect: She is red. SB1 in 0.80.0 and SB1b in 0.80.2 both failed this; the texture is now repainted rather than remapped -- *The row that proves the release*
- [ ] `RD3` (qa.md:1978) step: **Regression.** Watch her idle, walk, attack, cast and die | say: - | expect: All play normally. Her descriptor still points its eight animation paths at `Snakewoman tough/`, and only the texture bytes changed
- [ ] `RD4` (qa.md:1979) step: **Regression.** Her shading in motion | say: - | expect: Folds, scale edges and shadows look as they always did. Only hue and saturation moved; lightness was untouched, worst drift 0.0000 over 1,771 samples
- [ ] `RD5` (qa.md:1980) step: Watch for a missing or black texture on her at any camera distance | say: - | expect: None. If one appears, the MIP chain is the suspect: the shipped texture has one level and so does the replacement
- [ ] `GH1` (qa.md:1988) [eyes + save] step: **The reported row.** Accept Sahar's ring | say: - | expect: The garrison stops being hostile and **stays where it is**. Before this it was deleted on the spot the instant you agreed
- [ ] `GH2` (qa.md:1989) step: Walk among them afterwards | say: - | expect: They ignore you. They are still armed, still in the abbey, and still holding it
- [ ] `GH3` (qa.md:1990) [eyes + save] step: **Regression.** Attack one of them after the stand-down | say: - | expect: `truce broken` still fires: they turn on you, 100 Karma, once only
- [ ] `ST2` (qa.md:1993) step: **Regression.** Fight her | say: - | expect: Unchanged. The canned AI only handles the talk message; her patrol, pursue and attack AI are untouched
- [ ] `RL1` (qa.md:2018) step: **The rally.** Fight Sahar and her garrison | say: - | expect: They hit harder than the same snakebreed elsewhere: +15 AC and +25 to each offensive damage percent
- [ ] `RL2` (qa.md:2019) step: Break the truce after taking the ring, and fight | say: - | expect: The same rally applies -- it hangs off `truce broken` as well as `sahar fights`
- [ ] `RL3` (qa.md:2020) step: **Kill Sahar with her garrison still standing, and keep fighting** | say: - | expect: They get **measurably weaker**. If they do not, `CRemoveCharacterModifierFromCharacterAction` did not fire -- it has one shipped use in the whole game, in a test map -- and the rally must be cut. **Say so before anything else** -- *Say so before anything else if they do not weaken*
- [ ] `SC3b` (qa.md:2025) step: **The 0.79.9 repair.** Open her conversation, close it with Escape, walk up and click her | say: - | expect: It reopens. 0.79.9 claimed this and shipped it into her *death* script, so it has never worked
- [ ] `SC4` (qa.md:2043) [eyes + save] step: **The ring.** Take the ring, leave, then come back and click her | say: - | expect: `60 the ring is on your hand` -- *"Still here. The ring says what you are and the road says where."* Choosing `<Draw.>` there should cost **100 Karma**, because it fires `truce broken`
- [ ] `SC7` (qa.md:2046) step: The escort route, for the camera | say: - | expect: Arriving before Sahar, the view is framed on the scene rather than leaving her a small shape 462 units away. **If the camera sticks after the conversation, say so** -- it is activate-only, like 108 of the game's 115 camera attractors, and a release is one line
- [ ] `SC8` (qa.md:2047) [eyes + save] step: **Regression.** Refuse her outright with `<Draw.>` from her opening node | say: - | expect: The fight starts as before, via `sahar fights`, with no Karma penalty -- that is refusing a parley, not breaking a truce
- [ ] `RT3` (qa.md:2059) [eyes + save] step: **The one thing here that was measured and not proven.** Watch the sanctum's own survivors in particular | say: - | expect: They should reach `rout exit L2` and vanish. Its marker is the only one of the three with no spawn point near it, so **if they jam, say so** and the marker moves -- *Death route only now; on the ring route they hold the abbey*
- [ ] `RT10` (qa.md:2066) [eyes + save] step: **Montgomerie, which this release did not change.** Kill Sahar and wait | say: - | expect: He comes out, says he will not last, names Brother Michel, unlocks the Plains on the world map and dies. **If he does not appear, say so** -- the files say the only reachable branch reveals him, and if that is wrong it is unfound
- [ ] `KM1` (qa.md:2075) [eyes + save] step: Note your Karma, take Sahar's ring, then attack her | say: - | expect: Karma drops by exactly **100**, once. She and anything still standing turn on you
- [ ] `KM2` (qa.md:2076) [save] step: Keep hitting her after that | say: - | expect: **No further Karma loss.** The relay is `Trigger Only Once=1`; if it drops again the penalty is farmable
- [ ] `KM7` (qa.md:2081) [eyes + save] step: **Regression.** Kill Sahar the ordinary way, without taking the ring | say: - | expect: No truce to break, so no Karma penalty from this release
- [ ] `TR7` (qa.md:2096) [save] step: After breaking the truce, check whether you still have the ring | say: - | expect: You do. Confiscating it would close Machiavelli's two replies and the Crypt assassin's scene, which is deliberately not what this release does
- [ ] `BM7` (qa.md:2561) [eyes + save] step: **Adjudication, not a bug.** Peaceful route, no kills in the sanctum | say: - | expect: Brother Montgomerie does **not** appear, and nothing waits on him. This is deliberate
- [ ] `RL3` (qa.md:2713) [eyes + save] step: **Sahar herself** | say: - | expect: **Stays where she is, alive.** She is not in the roster, deliberately: removing her would flip `Snakebreed dead relay` and summon Brother Montgomerie as a side effect of accepting a ring
- [ ] `RL5` (qa.md:2715) [eyes + save] step: **Regression.** Check the ring, the Montaillou quest state and her balloon | say: - | expect: All unchanged
- [ ] `SL3` (qa.md:2725) step: Reach Sahar having **fought** your way in | say: - | expect: Her opening ends *"I had wagons for this once, and sisters I could spare. You have spent both on your way in."*
- [ ] `SL4` (qa.md:2726) step: On that same character, look for a peaceful reply | say: - | expect: There is still none, and that is deliberate. SL3 is the line that tells you why
- [ ] `SL5` (qa.md:2727) step: **Regression.** Ask her about the master, the Crown and the monks | say: - | expect: All three answers unchanged
- [ ] `SL6` (qa.md:2728) step: **Regression.** Fight her | say: - | expect: Unchanged, and her death still routs the garrison
- [ ] `MP3` (qa.md:2738) [eyes + save] step: **Regression.** Reach Sahar and fight her instead | say: `<Draw.>` | expect: Unchanged: she fights, and on her death the garrison routs exactly as before
- [ ] `MP4` (qa.md:2739) [eyes + save] step: **Regression.** Check you still receive the ring | say: - | expect: `Sahar Ring` in inventory, once, and act 5's assassins still read it as safe conduct
- [ ] `MP5` (qa.md:2740) [save] step: Check the Montaillou quest after taking the ring | say: - | expect: Still advances, as before
- [ ] `MP6` (qa.md:2741) step: **Machiavelli.** Reach Sahar with Outwit 7 but without ever taking Machiavelli's task | say: - | expect: The *"I carry Machiavelli's word"* reply **does not appear**
- [ ] `MP7` (qa.md:2742) step: Same, but after taking Machiavelli's task in the Temple District | say: - | expect: The reply appears, on both her opening node and her delivered-prisoner node
- [ ] `MP9` (qa.md:2744) step: Same, as a **delivered** prisoner | say: - | expect: *"Then send me north"* is offered on that node too, so the Outwit line costs nothing -- *'Then send me north' now leads to her refusal (0.82.0).*

**4 Animal Cave**

- [ ] `QS1` (qa.md:1900) [save] step: Kill the Wasp Queen on a fresh `4 Animal Cave`, with your own damage on her | say: - | expect: **Two** Wasp Stingers, as one stack of 2 -- the item merges. One is the defect this release fixes; zero means you never damaged her, since the drop is gated on `CWasDamagedByPlayerAction`

**4 Animal Cave (Grove wasp nest)**

- [ ] `PM24` (qa.md:1338) [eyes + save] where: Grove, the second cave (wasp nest), fresh | steps: Enter; the hover at the mouth; go to the deep west chamber | pass: The cave loads; *"The floor of the cave is paper..."* a second after arriving; a cursed wasp twice the size, named Wasp Queen, 200 HP; two stingers on death. **Signed off as passing in 0.11.0 while she dropped one** -- her can said `Number of items to generate=1` from the day she was built. The row named the right number; nobody counted them. **Count the stingers.** Fixed in 0.83.2

**4 Undercroft**

- [ ] `PM13` (qa.md:1324) where: Any of PM7-PM11, then walk back down | steps: - | pass: The pen state persists; no second setup; no timer restart
- [ ] `SC2` (qa.md:2041) step: **The warden.** Talk to him in the cell, close the conversation, and watch him | say: - | expect: He stands still on his stool. No skating, and no drifting west into Brother Pau's cell door. Click him again and he talks
- [ ] `RT6` (qa.md:2062) step: **The burned scene.** Fight in the front door, go down the prison stair before ever being captured, look around, leave, then surrender to the sentry | say: - | expect: The cell block is empty on the early visit, and the **real scene still plays** when you are delivered: locked door, jailer, Brother Pau, the 45/75/100 beats. Before this the early visit spent the one-shot and the delivery woke you in an unlocked, empty cell
- [ ] `RT8` (qa.md:2064) step: **Regression.** Attack the warden and let him fight | say: - | expect: He is hostile, auto-targetable, and swings. His `Valid Targets` and `Enemy` category are now restored explicitly
- [ ] `RT9` (qa.md:2065) [eyes + save] step: **Regression, 0.79.7.** Kill Brother Pau | say: - | expect: Karma drops by exactly 200. The array that holds that penalty had its count declared in the wrong place
- [ ] `KM4` (qa.md:2078) [eyes + save] step: **Regression.** Talk to Pau and leave him alive | say: - | expect: No Karma change, and his drain line still works
- [ ] `WD1` (qa.md:2105) step: **The reported row.** Take the drain out of the cell, come up by the stairs, walk back to the warden and click him | say: - | expect: He draws on you. The stair assassin draws, the reinforcements spawn and the floors above are alerted. Before this he said *"Still here. Good. Sit."* to your face
- [ ] `WD2` (qa.md:2106) step: Pick the lock, pass the Sneak roll, then come back and click him | say: - | expect: The same. `Fixt slipped out` is the other quiet escape and is guarded identically
- [ ] `WD3` (qa.md:2107) step: **Regression, and the row that matters.** Click him while you are still in the cell | say: - | expect: `3 still here`, unchanged, with all five replies including Speech 40 and Charisma 7. **If he draws on a prisoner who is still behind bars, the guard is inverted** -- *If he draws on a prisoner still behind bars, the guard is inverted*
- [ ] `WD5` (qa.md:2109) step: **Regression.** Force the pins, or get caught picking the lock | say: - | expect: Hostile as before, by the same relay. Nothing should fire twice or spawn reinforcements twice
- [ ] `WD6` (qa.md:2110) step: Escape by the drain and go straight up the stairs without approaching him | say: - | expect: The abbey is still calm. The guard fires on the click, not on the escape
- [ ] `PN1` (qa.md:2137) step: **The row the release is for.** Get delivered to the pen on a character who has never been in it, and look at the warden | say: - | expect: He is sitting on his stool across the room, in the open. Before this he stood inside the wall beside the cell door
- [ ] `PN2` (qa.md:2138) step: Click him from inside the cell | say: - | expect: His conversation opens, `1 bars` or `3 still here`. His reach is now 320 against the 298 from the stool to the bars. **If nothing happens, say so** -- the fallback is a click-poly at the bars, which is what `cell pins` and `cell drain` already are
- [ ] `PN3` (qa.md:2139) step: **Regression.** Wait in the cell without touching anything | say: - | expect: 45s a glance and a bark, 75s he opens the conversation himself, 100s he escorts you up. All three anchor on him by name, so none depends on where he stands
- [ ] `PN4` (qa.md:2140) step: **The second row the release is for.** Ask Brother Pau about the drain and take either closing reply | say: - | expect: A **Secret Icon appears over the grate** in your cell. Before this you were told it existed and shown nothing
- [ ] `PN5` (qa.md:2141) step: Then click the grate | say: - | expect: You go down the drain and come up at `Drain Out`, abbey calm. Unchanged, this is only about finding it
- [ ] `PN6` (qa.md:2142) [eyes + save] step: **Regression.** Find the drain with Perception 7 instead, without asking Pau | say: - | expect: The icon appears, the secret-found sound plays and you get the **25 experience points**. Being told by Pau should pay nothing
- [ ] `PN7` (qa.md:2143) step: **Regression.** The other four ways out of the pen | say: - | expect: Speech 40 or Charisma 7 through the warden, Strength 8 on the pins, Lock Pick 40 then Sneak 30, and doing nothing. Only the two loud ones turn the abbey hostile
- [ ] `HW2` (qa.md:2620) step: **What t=75 is protecting.** In that first minute, go to the east bars and talk to Brother Pau | say: - | expect: You have time for his whole tree, the drain included, before the warden arrives
- [ ] `HW3` (qa.md:2621) step: On a Speech 40 or Charisma 7 character, take his offer | say: - | expect: He walks you up. You arrive in Druid Council Level 2 and the abbey is calm. This route was unreachable until now
- [ ] `HW6` (qa.md:2624) step: Escape by the drain, the pins or the lock before 75 seconds | say: - | expect: He never walks over, and no conversation opens behind you
- [ ] `UC7` (qa.md:2659) step: Wake in the pen and walk to the east bars | say: - | expect: Pau speaks **without being clicked**, and he is visibly behind bars in a compartment of his own with its own door -- not standing in the open beside the cells
- [ ] `UC8` (qa.md:2660) step: After that conversation ends, click Pau again | say: - | expect: *"Still here. Good..."* -- **not** the opening line a second time. If he repeats it, the series swap did not take
- [ ] `UC9` (qa.md:2661) step: Try to reach Pau by clicking him from the far side of your cell | say: - | expect: You walk to the bars and talk, or you stop at the bars. Either is fine; being teleported or stuck on the geometry is not
- [ ] `UC10` (qa.md:2662) step: Walk south through the cellar after escaping by the drain | say: - | expect: A dressed larder: crates, barrels, litter. Nothing floating, nothing inside a wall, nothing overlapping
- [ ] `UC11` (qa.md:2663) step: Open the chest down there | say: - | expect: It opens, pays loot scaled to your level, and does not re-open for a second payout
- [ ] `UC12` (qa.md:2664) step: **Crash check.** Simply enter the Undercroft | say: - | expect: It loads. Pau's door was a `Door2` carrying `Cur Sequence=Idle`, an animation that model does not have -- *Covered by simply playing the route.*
- [ ] `LE3` (qa.md:2674) step: **Regression.** Walk the delivered route through to Sahar without escaping at all | say: - | expect: Unchanged from 0.71.6
- [ ] `AF4` (qa.md:5561) step: In `4 Undercroft`, cross `guard room poly`, leave the room, cross it again | say: - | expect: It responds on the later crossing as well as the first

**4 Undercroft (cell)**

- [ ] `PM7` (qa.md:1317) where: In the cell | steps: Click the door | pass: Locked; with Lockpick 35 it opens; the guard room, the stair, Level 1's south-west room
- [ ] `PM8` (qa.md:1318) where: In the cell, ST 8 | steps: Click the floor by the door's pins | pass: *"The lower pin shears..."*, the door opens, the handler attacks; with ST below 8, *"Old iron, old stone"*
- [ ] `PM10` (qa.md:1320) where: In the cell | steps: Talk to Brother Pau through the bars, ask how to get out | pass: The drain; click the straw -> *"a square of darkness"* and you are in his cell; his door opens on a click
- [ ] `PM10b` (qa.md:1321) where: In the cell, PE 7, without talking to him | steps: Click the straw | pass: The same, unaided; below PE 7 and untold, *"Straw, old and flat"*

**4 Undercroft then 02 Druid Council Level2**

- [ ] `PQ6` (qa.md:1963) [eyes + save] step: **The monk.** Speak to Brother Pau in the cells, then reach her | say: - | expect: A fifth opening, gated on having met him rather than on a stat

**4 Undercroft to 02 Druid Council Level1**

- [ ] `UC1` (qa.md:2653) [eyes + save] step: **The row that matters.** Pick the cell lock, cross the warden's room and pass the Sneak 30 check -- the balloon says you slip past -- then go up the stairs into Level 1 | say: - | expect: **The abbey is calm.** Nothing aggros. If Level 1 turns on you, this release did not take: that is exactly the 0.71.7 bug
- [ ] `UC2` (qa.md:2654) [eyes + save] step: Same run, but fail the Sneak check and let the warden catch you | say: - | expect: Level 1 **is** hostile. The loud half still works, which is what 0.71.7 was for
- [ ] `UC3` (qa.md:2655) [eyes + save] step: Break the pins with Strength 8+ instead | say: - | expect: Hostile above. Unchanged
- [ ] `LE4` (qa.md:2675) step: **The one to watch.** Play the loud route all the way out | say: - | expect: Harder than before, deliberately. None of this had ever run, so if anything is now unwinnable rather than merely hunted, that is worth reporting

**Animal Den**

- [ ] `PM14` (qa.md:1325) where: The Animal Den | steps: Enter | pass: Vanilla: three bears, no door

**Druid Council Level 2**

- [ ] `MS11` (qa.md:1286) where: Level 2, west chest (1143,365) | steps: Open it | pass: Two assassins fade in a second later; at Lockpick/Disarm 35+ the needle line and no assassins
- [ ] `MS14` (qa.md:1289) [eyes + save] where: After Sahar | steps: Kill everything near Montgomerie | pass: He speaks (vanilla gate). Templar: *"I am of the Temple, brother"*; journal: `21 the captain`
- [ ] `MS15` (qa.md:1290) where: Level 2 hovers | steps: Altar (3900,2200), the dead at (3975,2365), the Inquisitor at (2685,1020) | pass: The reliquary line; the missing-monks line; Inquisitor IS sees the sealed order

**Druid Council Level 2 (Montgomerie)**

- [ ] `MS1` (qa.md:1276) where: Montgomerie | steps: Reach `45 prophecy 2` | pass: *"How long ago did they come?"* plays the voiced `60 not long`, then Michel

**Druid Council Level 2 (sanctum)**

- [ ] `MS13` (qa.md:1288) where: Sahar at 60% and 25% | steps: Fight her | pass: *"To me!"* and two assassins at the threshold (three if MS9's runner got through); at 25% the heal effect and *"The Master is not done with me"*
- [ ] `PM15` (qa.md:1329) where: Delivered, arrive at Sahar (escort or walk) | steps: - | pass: *"You walked in. Good. It saves rope"*; the offer reply present; a fighter who walked in gets *"You are late"* as before

**Druid Council Level1**

- [ ] `MS6` (qa.md:1281) where: Level 1, y=1700 | steps: Cross the hall southward | pass: `<Behind you...>` and three assassins fade in north of you. With Sneak 40+: nothing
- [ ] `MS7` (qa.md:1282) [eyes + save] where: Level 1 (2000,1900) | steps: Click the man in black among the dead | pass: Laughs; who (Speech 40 / *"Ask the snakes"*), where, why; Demokin and Saladin lines if applicable; Finish him -> pain sound, corpse, polygon gone, +100 XP; questions +150 XP once
- [ ] `MS8` (qa.md:1283) where: Level 1, before the inner door (y~2800) | steps: Cross it | pass: Poison and the needle line; at Find Traps 35+ the tripwire line and no damage
- [ ] `MS9` (qa.md:1284) where: Level 1 (2450,2450) | steps: Approach | pass: One assassin breaks and runs for the inner door and vanishes there
- [ ] `MS10` (qa.md:1285) where: Level 1 hovers | steps: Barricade at the entrance, jailor body (2312,2450), a candle stand (2479,1263), the druid gate | pass: Balloons; jailor and candles have PE 7+ lines; the gate reads four ways (Wielder / Sylvant / IN 6 or Educated / plain)
- [ ] `MS32` (qa.md:1307) [eyes + save] where: Montserrat Level 1 needle trap, Find Traps below 35, fresh map | steps: Walk the strip before the inner door | pass: Poison, the generic trap message, and *"<Something gives under your foot...>"* over the character
- [ ] `PM19` (qa.md:1333) where: Delivered, quiet escape (lock + Sneak, or drain), walk Level 1 | steps: - | pass: Packs passive with the Keep-walking click
- [ ] `PM20` (qa.md:1334) where: Delivered, loud escape (pins, or caught) | steps: Walk Level 1 | pass: Packs that spawn after are hostile

**Druid Council Level1 / 4 Undercroft**

- [ ] `PM12` (qa.md:1323) where: Level 1, never delivered | steps: Walk down the stair in the south-west room | pass: The undercroft: two cells, doors closed and unlocked, no handler, no monk; the stair hover reads

**Druid Council Level1 to Level2**

- [ ] `SC1` (qa.md:2040) step: **The reported row.** Come up the prison stair into Level 1, cross to Level 2 and head east toward the sanctum | say: - | expect: She stops you. Before this the tripwire covered 271 units of a 1,974-unit gap, so this approach missed it and she was never spawned -- an empty chamber

**Gate District, Quinn (after Montserrat)**

- [ ] `NR6` (qa.md:3736) where: **Quinn.** Take the ask to Quinn in the Gate District | steps: - | pass: He knows the affliction, explains nightshade does not grow south of the mountains, and points you at a woman in Montaillou -- asking you not to say he sent you. Try this from several of his greetings; the reply is on **7** of his hubs -- *0.93.4 put the reply on more of his hubs, so 7 is now a floor.*
- [ ] `NR7` (qa.md:3737) [eyes + save] where: Check the journal after NR6 | steps: - | pass: It names Montaillou and the unlicensed woman, not a vague "find an ingredient"

**Grove Exterior**

- [ ] `MS3` (qa.md:1278) where: Grove | steps: Walk the ruins | pass: Packs are mixed: snakebreed, a human assassin in most packs of three, a Summoner in packs of four. One assassin near (2650,1150) calls *"The Scion! To me!"* on his first wound and two packs arrive
- [ ] `MS4` (qa.md:1279) where: Grove, negative | steps: Kill the sentry in one blow | pass: No call, no reinforcements
- [ ] `MS5` (qa.md:1280) where: Grove hovers | steps: Click the campfire (near 4400,3400), the dead snakebreed at the gate | pass: Balloons; the campfire's second line at PE 7+

**Grove Exterior (gate)**

- [ ] `MS2` (qa.md:1277) [eyes + save] where: Grove gate fight (2730,705) | steps: Click the knight | pass: `<...shield still on his arm...>`; Read -> three entries -> Take. Second click: `2 taken`, Read it again offered, Take not
- [ ] `PM1` (qa.md:1311) where: Grove, fresh Montserrat, walk to the gate | steps: Enter the gate area | pass: The sentry appears passive and *"Far enough..."* opens on him; no pack attacks during the talk
- [ ] `PM2` (qa.md:1312) where: PM1, *"I am not. <Draw.>"* or Escape | steps: - | pass: He draws, *"The Scion! To me!"*, both reinforcement packs come (Tier 4 unchanged)
- [ ] `PM3` (qa.md:1313) [save] where: PM1, *"Take me to your captain"* -> *"Take it"*, carrying a named weapon and a rolled magic one | steps: - | pass: Every weapon and all ammunition gone from the inventory; fade; wake in the den at the back
- [ ] `PM4` (qa.md:1314) [eyes + save] where: After PM3, get out and return to the gate | steps: Look at the ground by the sentry | pass: The named weapon itself, a plain base for each rolled one, and two good weapons; the garrison passive, *"Keep walking, Scion"* on a click
- [ ] `PM5` (qa.md:1315) where: PM1 with Outwit 6 | steps: The armed reply | pass: Delivered with everything kept
- [ ] `PM6` (qa.md:1316) where: PM1 as Demokin or Sylvant | steps: *"Look at me..."* | pass: Delivered unsearched

**Grove Exterior, Druid Council, Clan of the Hand/Skull, Cave 2**

- [ ] `SM1` (qa.md:3348) step: Fight a **Snakebreed Summoner** in act 2 (Grove Exterior, the Druid Council, Clan of the Hand or Skull, Cave 2) and let it summon | say: - | expect: A taunt appears as it casts -- *"Come, my brood. Come."*, *"We are many. You are one."*, *"The nessst wakessss."*, or *"<It calls, and the dark answers>"*

**Inquisition Chambers (Raphael)**

- [ ] `IQ6` (qa.md:2870) [eyes + save] step: **Regression.** Take the report option and finish the thread | say: - | expect: Unchanged. `330 return from montserrat` already completes the quest this release can finally start

**Montserrat / Montaillou**

- [ ] `WD8b` (qa.md:4021) step: **Mid game, mojo 7-16.** Montserrat, Montaillou | say: - | expect: All six slots now, up to **Rare** -- 22 live enchantments. Still nothing Very Rare or Unique -- *Enchantment counts moved with later cloak additions; the slot and rarity ceiling are what to check.*

**Montserrat grove; 04 Maw of the Assasin (act 8)**

- [ ] `SP4a` (qa.md:6380) where: Montserrat grove, then an Assassin Master in the Assassins' caves | steps: Wound one | pass: One patch, once each, as `SP1`. A spellcaster that never closes to melee should still drop one when hurt -- *Two halves in two acts.*

**Montserrat, then Raphael**

- [ ] `IQ5` (qa.md:2869) step: Go to Montserrat, speak to Brother Montgomerie, then come back to Raphael | say: - | expect: The new option is **gone** (Montgomerie advances Javier's quest past the state the option is gated on) and the existing report option is there instead -- *Fight route only: Montgomerie never appears on the peaceful route.*

**Patron, after Montserrat**

- [ ] `BM3` (qa.md:2557) step: **The row that stops BM1 going too far.** Fight through Montserrat, meet Montgomerie, then report | say: - | expect: The original lines, naming him, exactly as before
- [ ] `BM4` (qa.md:2558) step: On the peaceful route, hand your patron Sir Tomas' journal and continue | say: - | expect: You come back to the **assassin** version, not the Montgomerie one. This was the leak the first two passes missed

**Port District tavern (Barcelona), after the Undercroft**

- [ ] `RT5` (qa.md:2061) [eyes + save] step: **Then check Barcelona.** After doing RT4, go to the Tavern in the Port District | say: - | expect: **One** Cortes, not two. Closing the jailer's conversation used to fire the Barcelona Cortes cloner

**Port District tavern, Barcelona (after Montserrat)**

- [ ] `NR4` (qa.md:3734) [eyes + save] where: **The ask.** After Montserrat, return to the drunkard | steps: - | pass: He admits he has been drinking since the news from the abbey and asks you to see Quinn. The journal gains `Gather Nightshade Root for Quinn`, which in vanilla had no states and could never appear
- [ ] `NR5` (qa.md:3735) where: Decline him (*"Drink less."*) | steps: - | pass: Conversation ends, no quest, and the ask is still offered next time

**anywhere in the act**

- [ ] `RD2` (qa.md:1977) step: **Regression.** Any other snakebreed -- boss, summoner, viper, the garrison | say: - | expect: Still green. Only her forked mesh was repainted; the six cans on the donor model are untouched
- [ ] `RL4` (qa.md:2021) step: **Regression.** Snakebreed anywhere outside her sanctum | say: - | expect: Unchanged. The rally names only the four `sahar fights` enumerates, in her map
- [ ] `MA6` (qa.md:2031) [save] step: Check the journal after killing her | say: - | expect: **No new entry.** The outcome is carried by player-scoped scripting variables, not a quest, specifically so a murder does not get a journal line
- [ ] `GR6` (qa.md:2126) step: **Regression.** The wounded assassin, and Brother Montgomerie | say: - | expect: Unchanged. Neither is in any of these lists and neither was touched
- [ ] `GR7` (qa.md:2127) step: Check that nothing in the abbey is pacified that should not be | say: - | expect: The lists gained no new targets. Only the names that matched nothing were corrected, so the undead, the vodyanoi and the wolves in the Grove are exactly as before
- [ ] `MB6` (qa.md:2408) [eyes + save] step: Kill the venom-spitting snakebreed in Montserrat | say: - | expect: A **Snakebreed Venom Sac**, about one in three. Green, veined. The plain and boss snakebreed drop nothing, deliberately
- [ ] `BM2` (qa.md:2556) [save] step: Check the quest log on that route | say: - | expect: *"You have been asked to cross the Pyrenees Mountains"*. No Montgomerie
- [ ] `SM3` (qa.md:3350) step: Watch a summoner that is **not** summoning | say: - | expect: No summoner taunt. These four lines fire only on the summon, unlike the shared and drone banks
- [ ] `SM4` (qa.md:3351) step: Fight ordinary Snakebreed, Venom and Boss variants | say: - | expect: Their barks are exactly as before. Only the three summoner cans changed
- [ ] `BK5` (qa.md:5271) step: Fight Snakebreed, including a Venom and a Boss | say: - | expect: Sibilant throughout; Venom talks poison -- *"Feel it ssspreading?"*; stage directions like *&lt;It rears to its full height&gt;*
- [ ] `BK8` (qa.md:5274) step: Fight `Snakebreed Summoner`, and both PROBE archers | say: - | expect: No bark. All three have an attack slot already in use and were deliberately skipped

## 3 Montaillou (226)


**01 Hamlet Exterior**

- [ ] `TK13` (qa.md:1949) step: Montaillou, Hamlet Exterior, the Pain and Nanghaithya exchange | say: Try to walk away while it plays | expect: **You cannot.** The scene holds the controls for its thirteen seconds and the demons are held with you
- [ ] `RG1` (qa.md:5480) step: As a Knight of Saladin, meet the Montaillou gate guard **before** visiting the church | say: - | expect: The vanilla welcome: *"you are an ally of the Templars - and thus welcome here"*
- [ ] `RG4` (qa.md:5483) step: Leave, and give the guard the same Saladin answer again | say: - | expect: The **cold** version. He still lets you pass; he is no longer pleased about it
- [ ] `RG6` (qa.md:5485) step: As a Knight of Saladin, never speak to the Bishop, and use the guard repeatedly | say: - | expect: The warm welcome every time. The cost is only paid if you introduce yourself
- [ ] `DV1` (qa.md:5619) step: Carrying only the **Ring of the Prophet**, cross the Prophet Polygon in the hamlet | say: - | expect: `4 Ring`: *"You bear a powerful relic, mortal. Something of the prophet Zarathustra's if I'm not mistaken."* In vanilla this played the Amulet's line instead
- [ ] `DV2` (qa.md:5620) step: Carrying only the **Amulet**, same approach | say: - | expect: `4 Amulet`, unchanged: *"Ah, you have a bauble from that accursed prophet."*
- [ ] `DV3` (qa.md:5621) step: Carrying **both** relics | say: - | expect: The Amulet's line. The fork checks the Amulet first, so it wins the tie
- [ ] `DV4` (qa.md:5622) step: Carrying **neither** | say: - | expect: The scene does not trigger at all, exactly as before -- the outer check is unchanged
- [ ] `DV5` (qa.md:5623) step: Fail to kill the Daeva in Montaillou and let it break off | say: - | expect: `3 Undefeated`: *"this exertion has left me ravenous... that lake town has all of my favorite flavors."* In vanilla it left in silence
- [ ] `DV7` (qa.md:5625) [eyes + save] step: In act 1, get **Faust lured to the demon** so it frees itself, then reach the Daeva in Montaillou with **no relic** | say: - | expect: The clone loop stops, the true form comes up, and **the Daeva of Pain arrives and fights it**. HP 900 / AC 200, tagged `Player Friend` -- *Needs the act 1 Inquisition Pit choice: wizard lured to the demon.*
- [ ] `DV7a` (qa.md:5626) [eyes + save] step: Watch exactly where the Daeva of Pain appears on the Faust route | say: - | expect: At the **Giants Cave mouth, (280,260)**, behind you and facing the fight -- **not** inside the shapeshifter. He spawned on the true form's own point until this was caught
- [ ] `DV7b` (qa.md:5627) step: Watch the arrival to the end without acting | say: - | expect: A **cutscene**: camera moves to (421,345), and the two of them trade three barbs -- his, hers naming him **Aeshma**, then his -- before the sequence ends and they fight. He should not be clickable during it -- *She now names him Boruta, not Aeshma (0.99.1).*
- [ ] `DV7c` (qa.md:5628) step: Try to click him during or after the barbs | say: - | expect: Nothing. The inherited `GetCloseThenTriggerAndFight` specifier is gone; on this route he is a combatant, not a conversation
- [ ] `DV9a` (qa.md:5629) [eyes + save] step: On the **lesser** debt route, walk to where your spirit warns you something is ahead | say: - | expect: He is **sitting there**, at (1377,1058), waiting and not fighting. The spirit's warning and the informant are the same beat
- [ ] `DV9b` (qa.md:5630) [eyes + save] step: Talk to him | say: - | expect: `1 the warning`, then `2 the name`. Taking the name sets `Fixt knows Nanghaithyas name`
- [ ] `DV9c` (qa.md:5631) step: Refuse him at `3 declined`, then reach the shapeshifter with Speech 95+ | say: - | expect: **No Speech reply.** The route now needs the name to have actually been given, not merely the demon freed
- [ ] `DV9d` (qa.md:5632) [eyes + save] step: On the **Faust** route, check the wall at (1377,1058) | say: - | expect: Nobody there. The informant seat is gated on the lesser debt **and not** the larger, so the two routes never both fire
- [ ] `DV8` (qa.md:5633) step: Check the true form is killable on that run | say: - | expect: It should die and stay dead. It is the bound template: same race and 2750 XP, with the 20-25 HP/sec heal removed
- [ ] `DV9` (qa.md:5634) step: Instead **break the crosses yourself**, then reach it with **no relic and Speech under 95** | say: - | expect: The loop still breaks and the bound form comes up, but no ally arrives
- [ ] `DV10` (qa.md:5635) step: Break the crosses yourself, then reach it with **no relic and Speech 95+** | say: - | expect: A new reply: *"Nanghaithya. A demon in a Barcelona cell gave me your name, and it owed me the favour."* It opens `2000 using speech`, which was relic-only
- [ ] `DV11` (qa.md:5636) step: **Kill** the demon in act 1 instead, then fight the Daeva with no relic | say: - | expect: Nothing changes. The loop is unbreakable and the fight cannot be finished, exactly as vanilla
- [ ] `DV12` (qa.md:5637) step: Never visit the demon at all, then fight with a relic | say: - | expect: Unchanged vanilla behaviour: `Prophet Polygon` puts up the ordinary healing true form
- [ ] `DV13` (qa.md:5638) step: Watch what happens on the wave where the debt fires | say: - | expect: Expect the last clones to spawn **alongside** the true form. The debt check is first in `Form Relay` but deactivating a relay mid-array may not abort it. Note whether that reads well or badly -- *Judgement row.*
- [ ] `BA26d` (qa.md:5843) [eyes + save] step: Attack the **shepherd's son** in Montaillou | say: - | expect: He screams, `Player hurt the son` and `Make Maury mad for hurting son` activate as in vanilla, and the title is granted
- [ ] `MO1` (qa.md:5936) step: Fresh Montaillou, walk in from the east | say: - | expect: A knight stops you: *"You there! What business do you have in Montaillou?"*; once only
- [ ] `MO2` (qa.md:5937) step: MO1 as an Inquisitor / male Templar / female Templar / Knight of Saladin | say: The matching claim | expect: *"Forgive me Inquisitor"* / *"Forgive me brother"* / *"Forgive me sister"* / *"A Knight of Saladin? ... then you are an ally of the Templars"*; each claim is offered only to that faction
- [ ] `MO3` (qa.md:5938) step: MO1 as anyone | say: *"I'm on an urgent mission to protect the relics of this region."* | expect: The relic answer, no dead link
- [ ] `MO4` (qa.md:5939) step: MO1 | say: *"My business is my own."* -> *"Why is this town under investigation?"* | expect: The heresy answer, then the goodbye; the reply never loops back on itself
- [ ] `MO5` (qa.md:5940) step: After MO1, click either knight | say: - | expect: *"What can I help you with, stranger?"*, not *"Halt, and state your business"*
- [ ] `MO8` (qa.md:5943) step: Montaillou, Andre, Lethos quest accepted, Speech 50+ / Outwit 8+ | say: *"Go back to them and say it to their faces"* / *"Walk in under a truce"* | expect: The success nodes, with no [REMOVED FROM GAME] in the text; below the skill, the written refusals, which still offer the fight
- [ ] `MO9` (qa.md:5944) [eyes + save] step: MO8 success | say: - | expect: Andre leaves Montaillou; the mneme quest reads *"allow Lucius to live"*; *Kill the Titans of Toulouse* completes; pacifist XP
- [ ] `MO11` (qa.md:5946) step: Montaillou, Andre, first meeting | say: *"I want to talk to you."* | expect: `20 Introductory`, with the gatekeeper, the gullible line and his story
- [ ] `MO12` (qa.md:5947) step: Andre, a return visit, having seen the corpse | say: *"There is a gruesome corpse..."* | expect: `02 corpse` -- the same answer, but the hearts, the accusations and Michel are still offered
- [ ] `MO13` (qa.md:5948) step: MO12 having heard both the mayor's story and Esclarmonde's | say: *"I spoke to a woman from Toulouse... and the mayor..."* | expect: `800 Both lies`: he admits the lie and asks you to keep his secret
- [ ] `MO21` (qa.md:5956) step: Maury the shepherd, his questions hub | say: *"Is there anyone here I should be careful of?"* | expect: The warning about Guillaume Belibaste
- [ ] `MO23` (qa.md:5958) step: Montaillou square, the Relaxed Thug, as a friend of Juanita's guild / a Master Thief / a Thief | say: The matching reply | expect: `80 guild`; he stands down, keeps his coins-speech, warns you off his patch; afterwards he greets you as a friend. Only one of the three replies is ever offered
- [ ] `MO24` (qa.md:5959) step: Arrive at Montaillou as a member of the Goblin Horde | say: *"I ride with the Horde of the Khan..."* | expect: `100 horde`; the knight does not draw but says you will be watched; the reply is absent to anyone not of the Horde
- [ ] `MO30` (qa.md:5965) step: Maury at PE 7+, asking about the Inquisition | say: *"You look at the church door every time you say the Bishop's name."* | expect: `131 careful`, his voice dropped, then back to his questions hub

**02 Hamlet Burned**

- [ ] `TS1` (qa.md:4200) [eyes + save] step: **The row this exists for.** Act 3, `02 Hamlet Burned`, on a save that has **not** been in that map. Find the dead Knight Templars and search them | say: - | expect: **Two** of them carry a **Helm of the Templars** and a **Spirit Templar Shield** alongside the amulet they always had. Neither item has ever appeared in this game
- [ ] `TS10` (qa.md:4219) step: Judge whether the placement reads | say: - | expect: A battle-weary helm on a fallen Templar in a burned hamlet. If it feels like loot scattered at random rather than something left on a body, say so -- the alternative was a scripted scene rather than a corpse
- [ ] `HR1` (qa.md:6173) **NEW** where: Hamlet Burned, first visit | steps: Walk toward the middle of the village | pass: A Druid War-Priest speaks to you before the fight. "Then I will cut them loose myself" starts it | new: True
- [ ] `HR2` (qa.md:6174) **NEW** [eyes + save] where: The same | steps: Kill the War-Priest | pass: The log says his hold breaks. Every English soldier on the map stands down, says a dazed line about France, and can be talked to. Hit one: only his band turns | new: True
- [ ] `HR3` (qa.md:6175) **NEW** [eyes + save] where: The same, Speech 75 | steps: Take the parley reply | pass: He vanishes in a flash and the soldiers stand down as in HR2. He does not come back | new: True
- [ ] `HR4` (qa.md:6176) **NEW** [eyes + save] where: The same, Tribal 75 and at least 20 mana | steps: Take the wrest reply, walk away, wait, come back | pass: Your mana is gone, the band around him stands down. Coming back after 20 seconds, he speaks again ("Back again"), and each cast frees one more band, four in all | new: True
- [ ] `HR5` (qa.md:6177) **NEW** [eyes + save] where: The same, a Cathar friend of the Weird Woman | steps: Ask her to call the bears off | pass: The bears stop hunting you, including those later fights bring. Without the promise the reply is absent | new: True
- [ ] `HR6` (qa.md:6178) **NEW** [eyes + save] where: The same | steps: Reach the fight4 or fight6 squad, kill its priest | pass: That squad's soldiers stand down. A squad whose priest has not spawned yet does not stand down early | new: True

**02 Hamlet Burned / Montserrat**

- [ ] `TS8` (qa.md:4210) step: Search the **other** dead Templars in that map and in Montserrat | say: - | expect: **Only the amulet.** Templars 1 to 4 are untouched, so the set stays rare

**02 Hamlet Burned / act 7 shrine chambers**

- [ ] `EH10` (qa.md:4478) step: Act 3 `02 Hamlet Burned` and the act 7 shrine chambers, which also place Priests | say: - | expect: Same behaviour. The can is shared, so this is not act-6-only -- unlike the mana change in the same release

**02 Hamlet Burned / sieges**

- [ ] `DN17` (qa.md:4903) [save] step: Any anonymous Templar -- the dead ones in `02 Hamlet Burned`, the siege Templars, the two bar patrons, the cathedral guard | say: - | expect: **"Knight Templar"**, with no tier number. Five races stopped leaking it -- *0.60.3 found the log prints the can's User Assigned Name, not the race name this release edited. Expected names here came from race names, but 0.60.3 found the log prints the can's User Assigned Name (a hat goblin logs Goblin Striker). A different name is not a failure on its own; check it against the can.*

**04 Inn Interior**

- [ ] `TB1` (qa.md:5489) step: As a **Knight Templar** with 150+ gold, eat in the Montaillou tavern and let the Cathar toughs start on you | say: - | expect: The line *"I'm not a priest, nor are they my friends"* is **absent**
- [ ] `TB2` (qa.md:5490) step: Take the reply that is there instead | say: - | expect: *"No. I am a knight of the Temple, and I have eaten at the mayor's table this week."* then `61 the knights`
- [ ] `TB3` (qa.md:5491) [eyes + save] step: Pay the hundred and fifty | say: - | expect: `100 Welcome`, no fight, and **150 gold gone**
- [ ] `TB4` (qa.md:5492) step: Repeat carrying **less than 150 gold** | say: - | expect: The paying reply is absent. Only the two answers that start the brawl remain
- [ ] `TB5` (qa.md:5493) step: Take either of those instead | say: - | expect: `40 Super Insult` and the brawl, as every other wrong answer in that tree does
- [ ] `TB6` (qa.md:5494) step: Repeat the whole scene as an **Inquisitor** | say: - | expect: Unchanged: his own reply, and the disclaimer still closed to him as in vanilla
- [ ] `TB7` (qa.md:5495) step: Repeat as a **Wielder** | say: - | expect: Unchanged -- he still talks his way to `100 Welcome` for free at `70 Challenge Answer`
- [ ] `TB8` (qa.md:5496) step: Repeat carrying **no order** | say: - | expect: The disclaimer is available exactly as in vanilla, and no Templar reply appears
- [ ] `MO26` (qa.md:5961) step: The Cathar toughs' challenge, as an Inquisitor / as a Wielder | say: *"I am the Inquisition, and I am standing in your tavern"* / *"the Church burns my kind first"* | expect: Their own hostile node / their own welcome; neither reply shows to anyone else
- [ ] `MO27` (qa.md:5962) step: The inn's Inquisition agent, as an Inquisitor | say: *"Who are you reporting to, brother?"* | expect: `36 brother`: he explains the meat test and tells you to stop drawing eyes

**05 Church Interior**

- [ ] `RG2` (qa.md:5481) step: Go to the church and talk to the Bishop of Pamiers | say: - | expect: A new reply: *"Your grace. I am a sworn knight of the Order of Saladin."*
- [ ] `RG3` (qa.md:5482) step: Take it | say: - | expect: He writes you down. The quill does not stop
- [ ] `RG5` (qa.md:5484) step: Repeat RG2 as a sylvant, a feralkin and a demokin | say: - | expect: The introduction is offered on all four openings, including the untainted one, which offers no order introduction at all in vanilla -- *Needs sylvant, feralkin and demokin characters.*
- [ ] `RG7` (qa.md:5486) step: As a **Templar** or an **Inquisitor**, do RG2 | say: - | expect: Their own introductions, unchanged, and no register entry
- [ ] `RG8` (qa.md:5487) step: Carrying no order, talk to the Bishop | say: - | expect: His vanilla openings, unchanged
- [ ] `RG9` (qa.md:5488) step: After RG3, check the Bishop's other business still works -- the witch, the mayor, the gem | say: - | expect: All unchanged. The register is a flag, not a gate
- [ ] `MO32` (qa.md:5914) step: Montaillou, accept the Inquisitor's mayor task, speak to the mayor, return to the Bishop | say: *"I have spoken to the Mayor - he is a heretic and an adulterer."* | expect: Whether this reply appears answers whether an empty canned requirement fails open or closed -- it is still gated on one, deliberately, as the control case. Report which -- *Diagnostic: tells whether an empty canned requirement fails open or closed.*
- [ ] `MO18` (qa.md:5953) step: Montaillou church, take the witch task or report the mayor | say: *"Is there anything else in this district that troubles the Inquisition?"* -> *"What is it, your grace?"* | expect: The offer, then the barred cave with the aura of magic; both replies return to his hub
- [ ] `MO19` (qa.md:5954) step: Montaillou church as a Sylvant / Feralkin / Demokin, no faction | say: *"My blood is what it is. Is there nothing a tainted soul can do for the Church?"* | expect: *"Well then tainted one, have you come to cleanse yourself of sin?"* and the offer of service
- [ ] `MO25` (qa.md:5960) step: Montaillou church as a Necromancer, ask about the heresy | say: *"You have missed one, your grace..."* | expect: `61 the ninety-ninth`; leaving ends it, *"Find them now, then"* starts the fight; the reply is absent without the title

**06 Witch Interior**

- [ ] `MO14` (qa.md:5949) step: Witch hut, after she restores Beatrice | say: Talk to her again | expect: *"No chickens this time? Perhaps a weasel or stoat who is really the King of Persia..."*; the not-promised variant if you never promised
- [ ] `MO15` (qa.md:5950) step: Witch hut as a sworn Inquisitor, having promised | say: - | expect: *"Greetings your holiness..."* rather than the plain return
- [ ] `MO16` (qa.md:5951) step: Witch hut, ask about the Cathars | say: *"And when the Inquisition has finished writing its book...?"* -> *"I must know what sort of *aid* you intend to give."* | expect: Her answer about the allies, then the secret stash offer
- [ ] `MO17` (qa.md:5952) step: Witch hut after speaking to Nostradamus about her | say: *"The seer told me what you were, and what you did."* | expect: `300 confront the weird woman 1`; the reply is absent before the seer

**Brother Michel and Andre**

- [ ] `LE10` (qa.md:6407) where: **Fresh spawn.** Kill Andre, then attack Michel | steps: - | pass: *"By God you are a fiend that doesn't deserve life!"*
- [ ] `LE11` (qa.md:6408) where: Attack Michel with Andre alive | steps: - | pass: *"Brothers! Help me!"* as always

**DaVinci**

- [ ] `DL1` (qa.md:6362) where: Montaillou, first talk to DaVinci | steps: Take *"A pity you survived the crash."* | pass: His usual *"It pains me to see a dark nature..."*, as vanilla
- [ ] `DL2` (qa.md:6363) where: Talk again, *"What are you doing here?"*, then *"Why are you checking on my progress?"*, then *"And what makes you think..."* | steps: - | pass: You **hear** *"I have suffered quite enough of your insolence..."*, and afterwards he resumes his muttering at the flying machine. Only one copy of the reply shows
- [ ] `DL4` (qa.md:6365) where: **The regression.** A polite character in Montaillou | steps: Ask for his help once, never insult him | pass: *"Youth today..."* is the only route to any rebuke, and `320 general surly response 3` cannot appear on the first one
- [ ] `LE1` (qa.md:6398) where: Montaillou, DaVinci, the gem is with the Inquisitor | steps: Reply *"I could try to speak with the Inquisition about the gem."* | pass: You **hear** *"Ah, I would owe you a great debt..."* and the conversation ends. It must not be his goodbye. Fails with goodbye: the retarget did not ship
- [ ] `LE2` (qa.md:6399) where: Same, via *"I could not, in good conscience, oppose the Inquisition"* | steps: Take the same reply from `320 no to inquisition` | pass: Same line. The reply appears in two places and both were moved
- [ ] `LE3` (qa.md:6400) where: Same, after LE1 | steps: Talk to him again | pass: He is still there and still talkable, and the gem quest is unchanged. `10 Goodbye` used to run here, so this is the row that proves it did nothing he needed
- [ ] `LE4` (qa.md:6401) where: DaVinci, holding the Spirit Transfer Gem | steps: Hand it over, either reply | pass: You **hear** *"You've returned with a feisty spirit!"*, then 3001's silent text follows with no click on a blank reply
- [ ] `LE5` (qa.md:6402) [eyes + save] where: Same | steps: Finish the scene, count your gold | pass: **1000** gold, once. If you see 1400, 340's payout survived

**DaVinci's workshop**

- [ ] `DL3` (qa.md:6364) where: Workshop, press a coloured button on the steam engine three times, and a fourth | steps: Watch DaVinci | pass: First press only hisses. Second: *"No! Not that button!"* Third and fourth: fire, 25 damage, and **you hear** *"Don't touch that button again!"*

**Gate District, Quinn (return trip)**

- [ ] `NR10` (qa.md:3740) [eyes + save] where: **The brew.** Carry the root back to Quinn | steps: - | pass: He takes it without asking where it came from, grinds it, and gives you the **Hangover Cure Potion** -- an item referenced by nothing in the shipped game. The root is **consumed**

**Machiavelli**

- [ ] `MA1` (qa.md:2026) step: **The betrayal.** Take her ring, then kill her, then reach Machiavelli in Montaillou | say: - | expect: `233` or `303`, depending on whether you saved him in Barcelona. He approves -- the keeping-faith line from chapter 18
- [ ] `MA3` (qa.md:2028) step: **The blunt kill.** Kill her without ever taking the ring, then reach him | say: - | expect: `234` or `304`: *"Those who rely simply on the lion do not understand what they are about."* On the ambush path **the assassins still come**
- [ ] `MA4` (qa.md:2029) step: **Regression.** Take the ring, leave her alive, then reach him | say: - | expect: The existing `232` / `301`, unchanged

**Machiavelli ambush path**

- [ ] `MA2` (qa.md:2027) step: On the ambush path, after the betrayal | say: - | expect: The ambush is called off. He fires `machiavelli leaves`

**Montaillou (Brother Michel)**

- [ ] `S6` (qa.md:1033) where: Brother Michel, Montaillou | pass: 3 new replies
- [ ] `MS17` (qa.md:1292) where: Michel, Montaillou | steps: After questioning the assassin | pass: *"I know who attacked Montserrat..."* replaces the vanilla question; `141 out of the east`
- [ ] `PM17` (qa.md:1331) where: PM16, Montaillou, Brother Michel, Advice | steps: *"...Their captain sent me north with this"* | pass: *"A snake eating its tail..."*; the reply absent without the ring
- [ ] `CR27` (qa.md:1374) where: Montaillou, Brother Michel, ask how the complex was sealed, with Divine **or** Tribal magic at 80+ | steps: *"A seal like that is not a wall, it is a promise..."* | pass: `161 how a seal is broken`; he admits the order used borrowed desert magic. Absent below 80 in both schools; present from either of his two seal nodes
- [ ] `BM5` (qa.md:2559) step: **Regression, and the important one.** On the peaceful route, go on to Montaillou and talk to Brother Michel | say: - | expect: He recognises you and the act proceeds. His entry tests `SAXRA7U2` seven times, which is why the route keeps that state
- [ ] `BM6` (qa.md:2560) step: Do the same having fought through | say: - | expect: Michel behaves identically
- [ ] `NQ1` (qa.md:2699) [eyes + save] step: **The row that matters.** Take DaVinci's quest, go to Montaillou, ask Michel about the Caverns and follow it through to his warning | say: any reply on *"But if you go, take care"* | expect: The **Caverns of Nostradamus appear on the world map**, and the quest step changes to *"Brother Michel has shown you the location of the Cave of Nostradamus"*
- [ ] `NQ3` (qa.md:2701) [save] step: **The no-rewind check.** Get the location from the witch **first**, then go through Michel's warning | say: - | expect: The quest step does **not** change back. His reveal is gated on the quest still sitting at DaVinci's step
- [ ] `NQ4` (qa.md:2702) step: **Regression.** Michel's other conversations: the Crypt, the demon, his prayers, the Montaillou quests | say: - | expect: All unchanged. Only two replies on one node gained an action
- [ ] `BM1` (qa.md:2881) step: Talk to Michel and take *"You're a demokin, aren't you?"* | say: - | expect: His answer as before, and a new option among the replies: **"Is that why you pray in private?"**
- [ ] `BM2` (qa.md:2882) step: Take it | say: - | expect: **With voiceover.** *"One of the reasons why I prefer to pray in private, away from the cold stares and sneers of strangers. All my life I have strived to overcome the burden of my heritage - it took extraordinary...patience to endure the tests for knighthood, made all the more difficult because of my appearance."*
- [ ] `BM3` (qa.md:2883) step: **The row that matters.** Click through his answer | say: - | expect: You land on *"You are a good person, and I can only wish there were more in this world like you. Is there something I can help you with?"* and can carry on. Not dropped out of the conversation
- [ ] `BM4` (qa.md:2884) step: **All four variants.** Repeat BM1 on a human, on an Inquisitor, on a Sylvant or Feralkin, and on a demokin Knight or Inquisitor | say: - | expect: The new option is on every one of the four. They are chosen by race and order, and only one is reachable per character
- [ ] `BM5` (qa.md:2885) step: **Regression.** Take the other replies on that node | say: - | expect: Unchanged: the Montserrat quest hands over, the sympathetic one and the Lucius one still reach their own answers, the hostile one still annoys him
- [ ] `BM6` (qa.md:2886) [eyes + save] step: **Regression, karma.** Take the new reply and check your karma did not drop | say: - | expect: It fires `Good karma`, which is what both of its neighbours fire

**Montaillou (DaVinci's flying machine)**

- [ ] `SN8` (qa.md:2923) step: **DaVinci, needs a save that has not been to Montaillou's hamlet.** Stand near him while he works on the flying machine and listen to the rotation | say: - | expect: Five lines become six, the new one being *"Oh, there is so much damage...Where to begin?"* -- *Needs a save that has not visited Montaillou's hamlet.*

**Montaillou (Esclarmonde)**

- [ ] `TD5` (qa.md:2690) step: **Esclarmonde's bubble** | say: - | expect: She stops asking for help once Thierry is accounted for, alive or dead

**Montaillou / English Shrine**

- [ ] `MN10` (qa.md:4568) where: **Act 3 Montaillou** and **act 7 English Shrine** | steps: Play any English fight | pass: **Unchanged.** No can was edited, so no drop behaviour anywhere in the game moved

**Montaillou church**

- [ ] `PK13` (qa.md:3644) [save] where: **The regression. Do this one first if you only do one.** Kill **Inquisitor Fournier** in Montaillou's church while at least one of his three quests is active | steps: Check the quest log | pass: **All three quests still fail** -- `Find the Witch for the Inquisitor`, `Talk with The Mayor for the Inquisitor`, `Purify the Shadow Dryad` -- **and** you gain Enemy of the Inquisition. If the quests no longer fail, a wrap replaced an action instead of adding to it

**Montaillou grove**

- [ ] `MO20` (qa.md:5955) step: Montaillou grove, approach the warden without watching the bear change | say: - | expect: *"What are you doing here? I do not take kindly to trespassers in my grove."*; after watching the change, the *"What did you see?"* greeting instead

**Montaillou hamlet**

- [ ] `FP5` (qa.md:6350) [eyes + save] where: FP3, go to Montaillou | steps: - | pass: Thierry is at the north of the hamlet, once. Esclarmonde thanks you. His reward works

**Montaillou inn**

- [ ] `TD10` (qa.md:1217) [eyes + save] where: Montaillou inn | steps: Save Machiavelli in Barcelona, then enter the inn | pass: He is **at the bar**, greets you with `300`, and the speech runs through to *"Beware the Old Man from the east"*. **500 gold** is paid
- [ ] `TD11` (qa.md:1218) steps: Refuse his partnership in Barcelona (`215 reject offer`), then enter the inn | pass: He is at the bar on the customer side. He gloats -- *"you forced me to seek aid from those that seek to do us harm"* -- then **walks out the door**, and **two assassins** come in behind him and attack at once. They wear the game's assassin model, not the snake-women, and hit harder than Montaillou's guards. **PASSED** on the reporting save
- [ ] `TD11b` (qa.md:1219) steps: During that fight, cast spirit magic within sight of the Inquisition agent at the far table | pass: He shouts *"Heretic!"* (or one of its variants) and **turns hostile**. **This is expected, not a bug**: the agent runs the shipped `Detect Spellcast` reaction that 107 Inquisitors and guards across the game share, and no vanilla spell-detect exempts an Inquisition member. Fight with steel and he stays a bystander
- [ ] `TD12` (qa.md:1220) steps: Let him die, or kill him yourself, then enter the inn | pass: He is **absent**. No ghost, no error
- [ ] `TD13` (qa.md:1221) steps: Never take his bodyguard job at all | pass: He is absent
- [ ] `PM21` (qa.md:1335) where: Holding the ring, Montaillou inn, saved Machiavelli | steps: After his supplies line, *"You have seen this before"* | pass: `301`/`302`; the reply absent without the ring
- [ ] `PM22` (qa.md:1336) where: Holding the ring, Montaillou inn, refused Machiavelli | steps: *"Before your friends come in"* | pass: `232`; he walks out alone, no assassins; without the ring the 0.9.0 ambush as before

**Montaillou road (Andre)**

- [ ] `AG1` (qa.md:3801) where: **Baseline, no betrayal.** Meet Andre on the Montaillou road, keep his secret, come and go several times | steps: - | pass: Normal dialogue throughout -- `02 Return Dialogue`, or `03 Return accepted Lethos quest` once the Mneme quest is active. **Neither `900` line appears**
- [ ] `AG2` (qa.md:3802) where: **Betray him, no money taken.** Never accept his gold; tell the mayor; return to Andre | steps: - | pass: *"You are a very, very bad man and you lead a trite and meaningless existence. Now leave me alone."* **And you should hear it** -- 96 KB that never played
- [ ] `AG3` (qa.md:3803) where: After AG2, approach him repeatedly | steps: - | pass: Same brush-off each time. He does not attack and does not revert to normal dialogue
- [ ] `AG4` (qa.md:3804) where: **The row to walk. Take his money, then betray him.** Accept gold at `830 Extortion`, then tell the mayor, then return to Andre | steps: - | pass: *"I paid you your blood money and still you betray me! I have had all I can stand from you, runt!"* -- audible (84 KB) -- **and then he attacks you.** That `CGoToCombatAction` has never fired in this game
- [ ] `AG5` (qa.md:3805) where: Survive or flee AG4, then re-approach | steps: - | pass: He stays hostile. He must not fall back into dialogue mid-fight
- [ ] `AG6` (qa.md:3806) where: **Both map paths.** Repeat AG2 and AG4 having reached him by the *other* route -- fighting past him versus talking past him | steps: - | pass: Identical behaviour. The two selectors (`Lucius Wrasslin`, `Talked past Lucius`) were edited identically and must agree
- [ ] `AG7` (qa.md:3807) where: **Order check.** Take his gold **and** betray him, with the titan hunt **unfinished** | steps: - | pass: The extorted line wins, not the generic brush-off. Extortion-then-betrayal outranks everything
- [ ] `AG8` (qa.md:3808) [eyes + save] where: **The regression guard.** Betray him (no gold taken), **complete `Kill the Titans of Toulouse`**, then return | steps: - | pass: He uses **`1003`** -- *"I think our dealings are at an end, fleshling"* -- **not** the generic `900` brush-off. If the brush-off appears instead, 0.42.0 has shadowed 0.41.0's wiring and must be pulled
- [ ] `AG9` (qa.md:3809) where: As AG8 but **with** gold taken | steps: - | pass: The extorted line and the fight still win. Combat outranks the post-quest dismissal
- [ ] `AG10` (qa.md:3810) where: **The shipped cascade survived.** Without betraying him, verify `02 Return Dialogue`, `03 Return accepted Lethos quest`, `1100 Surrender`, `120 Andre Defeated` and `3000 Unlocked the door` all still work as before | steps: - | pass: Unchanged. The whole shipped chain was demoted inside the new tests and must be byte-identical in behaviour
- [ ] `AG11` (qa.md:3811) where: **Hand over the hearts** after betraying him, where he is not hostile (AG2 path) | steps: - | pass: `1002 Hearts in Hand but Lucius betrayed` still fires, as 0.41.0 intended. The two releases must compose
- [ ] `LU1` (qa.md:3835) where: **The secret.** Meet Andre on the Montaillou road, get through to `805 Sticky Situation` and hear his story | steps: - | pass: Unchanged from vanilla. He asks you to keep his secret and kill the Toulouse titans
- [ ] `LU2` (qa.md:3836) where: **Keep the secret.** Take `820 PC Saves the day`, never speak to the mayor | steps: - | pass: Unchanged
- [ ] `LU3` (qa.md:3837) [eyes + save] where: **Take his money.** `830 Extortion` | steps: - | pass: You get gold and the `Lucius extorted` marker sets, as in vanilla
- [ ] `LU6` (qa.md:3840) [eyes + save] where: Do LU5 **without** betraying him | steps: - | pass: He uses `1000 Hearts in Hand` and pays you, exactly as vanilla did. The two replies are mutually exclusive -- **never both**
- [ ] `LU9` (qa.md:3843) where: **The regression that matters.** Keep the secret, complete `Kill the Titans of Toulouse`, then return to Andre | steps: - | pass: He must **not** say *"I think our dealings are at an end, fleshling."* In vanilla he always did. A loyal player gets normal return dialogue
- [ ] `LU10` (qa.md:3844) where: Do LU9 **after** betraying him | steps: - | pass: Now he **does** use `1003` -- and you should hear it (55 KB)
- [ ] `LU11` (qa.md:3845) where: **`1001 Lucious Exposed`.** Reach the node where he explains whose hearts you brought | steps: - | pass: Audible -- 293 KB that never played. *"These cold hearts belonged to the other elders of my tribe, the ones who forced me to run for my life."*
- [ ] `LU14` (qa.md:3848) where: **The extortion combination.** Take his gold (LU3) **and then** betray him (LU4), then return with hearts | steps: - | pass: `1002` fires. Note that Andre's own angrier `900 Lucius extorted and thrown out of town` greeting is **still not wired** -- that is known and deliberate, not a failure of this row

**Montaillou street**

- [ ] `CT7` (qa.md:3346) [eyes + save] step: After any peaceful ending, walk up to a Cathar tough and talk to him | say: - | expect: *"Welcome to town."* and **nothing else happens** -- no XP, nobody despawns, no sequence ends. This is vanilla's greeting and it must stay inert. Getting this wrong was this release's first attempt

**Montaillou tavern and street**

- [ ] `CT1` (qa.md:3340) step: As a **Templar**, eat meat with the Inquisitor in the Montaillou tavern, then leave and let the toughs stop you | say: - | expect: `61 the knights` -- *"What is a winter worth, brother?"*
- [ ] `CT2` (qa.md:3341) step: Pay the 150 gold | say: - | expect: **The scene ends and you get control back.** The gears must stop. This is the whole report
- [ ] `CT3` (qa.md:3342) step: `CT2`: watch the three toughs | say: - | expect: They stand down and walk off, the same way they do if you frighten them off as a Wielder. They must not stand there frozen
- [ ] `CT4` (qa.md:3343) [save] step: `CT2`: check your purse | say: - | expect: 150 gold gone. The reply is gated on having it, so it is absent if you cannot pay
- [ ] `CT5` (qa.md:3344) step: As a **Wielder**, reach `70 Challenge Answer` and give the Wielder reason | say: - | expect: Same ending, same release. This route has been hanging since 0.14.0 and nobody reported it
- [ ] `CT6` (qa.md:3345) step: Refuse instead, by any of the insult replies | say: - | expect: The fight starts and control returns. Those four exits always worked and must still

**Montaillou witch hovel (Na Roqua)**

- [ ] `TD4` (qa.md:1211) where: Na Roqua, Montaillou witch hovel | steps: Promise no harm will come to the Cathars, leave the hut, return | pass: She greets you with **`100 Favorable Return`** -- *"Welcome spiritbearer and Cathar friend"*. **PASSED**
- [ ] `TD5` (qa.md:1212) steps: Same, as an Inquisitor using *"I am willing to spare the Cathars"* | pass: Same greeting. An Inquisitor who spares them counts as a friend. **PASSED** (the reporting character is an Inquisitor)
- [ ] `TD6` (qa.md:1213) steps: Refuse or never make the promise | pass: You get `03 Return Dialogue if Heard 50` as before. **Unchanged from vanilla**
- [ ] `TD7` (qa.md:1214) steps: On the favourable greeting, ask about the shapeshifting Daeva your spirit named | pass: She admits *"we once hunted together"* and describes the periapt in her cave. **PASSED**. The ask needs `met the demon` and vanishes once the cave is open
- [ ] `TD8` (qa.md:1215) steps: Take that branch to its end | pass: The **cave opens** -- she says *"Step through the fire"* -- exactly as the other phrasing of the question already does. **PASSED** -- the relay fires

**Montaillou, Brother Michel's house**

- [ ] `LU7` (qa.md:3841) where: **Brother Michel.** After LU4, find him in the house interior and talk to him | steps: - | pass: He meets you with *"Lucius, despite his flaws, was a harmless, lonely soul. Your meddling has cast him out of the only home he is likely ever to have."* Audible (149 KB). Talk again: *"Leave. Now."* (25 KB)
- [ ] `LU8` (qa.md:3842) where: Talk to Brother Michel **without** betraying Lucius | steps: - | pass: Normal dialogue. And if Andre is dead, his shipped `05`/`07` Andre-Slain greetings must still work -- that chain was demoted to the `Else` and must be intact

**Montaillou, the mayor**

- [ ] `LU4` (qa.md:3838) [eyes + save] where: **Betray him.** Go to the mayor, take *"I've spoken with Lucius. He has been lying"* through to `951 Furious Mayor` and the reply that gets you hired | steps: - | pass: The mayor is furious. **This now sets a flag that persists** -- in vanilla it activated nothing

**Montaillou, the weird woman**

- [ ] `NR3` (qa.md:3733) where: **The row that proves the gate fix.** Get the quest to the nightshade step, travel to **Montaillou**, and talk to the weird woman | steps: - | pass: A `Quest Icon` reply about nightshade root appears. **This is a gate file living in Barcelona's global requirements folder being read by an act-3 dialogue tree** -- if the reply is missing, the gate is resolving as nothing
- [ ] `NR8` (qa.md:3738) [eyes + save] where: **The root.** Take the witch's reply | steps: - | pass: She gives it **free** -- *"a thing like this is given or it is nothing"* -- with the warning that a thimble quiets a man and a spoon quiets him permanently. You receive **Nightshade Root**

**Montaillou, witch's interior**

- [ ] `NQ1` (qa.md:3283) step: Enter the witch's interior in Montaillou carrying the **Ancestral** spirit | say: - | expect: Your spirit names her *Druj*; she answers *"...not since we clashed so long ago as bitter enemies"*, then *"I am no longer Druj... I am Na Roqua, and I have atoned for my past"*, then *"I have a new life here among the folk of Montaillou... otherwise leave in peace."*
- [ ] `NQ2` (qa.md:3284) step: **The report. Do this one if you do only one.** The same scene carrying the **Beast** spirit | say: - | expect: **Her answer to the beast**: *"...the beast spirit within you knew me long ago when I was *different*, when I lived in darkness. But seasons turn, and I travel a new path, one of atonement..."* In the shipped game she plays the **elemental** line here, to everyone who brought a beast spirit
- [ ] `NQ3` (qa.md:3285) step: The same scene carrying the **Demonic** spirit | say: - | expect: He recognises her and reminisces about corrupting mortals together; **then her answer to him**: *"...you should beware of this impish spirit you keep as counsel, he has deceived others before you."* Then her two closing lines, then **his parting shot**: *"Oh, who to trust? Your dutiful spirit companion, or the witch of lies?"*
- [ ] `NQ4` (qa.md:3286) step: In **every** arm, watch the scene to its end | say: - | expect: **Control comes back.** The whole scene runs inside a non-interactive sequence and each arm must release it exactly once. A freeze here is the Cathar hang of 0.55.0 all over again
- [ ] `NQ5` (qa.md:3287) step: Count her lines in any arm | say: - | expect: Five of hers: the two introductions, her spirit-specific answer, and both closing lines. **No line twice**, and no silence between them
- [ ] `NQ6` (qa.md:3288) step: After the scene, talk to Na Roqua normally, and leave and re-enter | say: - | expect: Unchanged. Only the scripted scene was edited; her conversation was not touched

**Port District tavern (return trip)**

- [ ] `NR11` (qa.md:3741) [eyes + save] where: **The delivery.** Take the potion to the drunkard | steps: - | pass: He drinks it in one go, goes quiet, and teaches **Clear Head**: +3 Find Traps and Secret Doors. The potion is consumed and the quest completes
- [ ] `NR13` (qa.md:3743) [save] where: **No double perk.** After NR11, check your perk list, then talk to him again | steps: - | pass: **One** `Clear Head`, and he does not re-offer. The grant is guarded by a `CHasPerkExpression`

**Secret chamber**

- [ ] `DL6` (qa.md:6367) [eyes + save] where: Secret chamber, hand him the rotary gear | steps: *"Your rotary gear. Your engine cut it."* | pass: You **hear** *"Ah! There! It is complete."*, then with no click the silent `902` text. The gear leaves your inventory and the quest completes once

**Titan Village**

- [ ] `DV6` (qa.md:5624) step: Compare with the Toulouse escape on Titan Village | say: - | expect: `35 teleport out of toulouse` still plays there. The two lines are a pair and should now read as one chain
- [ ] `TO1` (qa.md:5890) [eyes + save] step: Toulouse, Lethos, reach `50 Lucius is the fugitive` by any of the five routes (nodes 20, 22, 22-tainted, 23, 24) | say: - | expect: Nothing visible; the flag `PC is told Toulouse was harboring Lucius` is now set on every one of them
- [ ] `TO2` (qa.md:5891) step: TO1, then reach Thierry in the pen and ask about the town harbouring one of their kind | say: *"The titans said this town was harboring one of their kind, is that true?"* | expect: `30 Lucius` -> `32 Lucius 2` -> `34 Alexander eaten`; offered from both `20 Questions` and `25 The rest of the townspeople`; absent to a player who never heard Lethos say it
- [ ] `TO3` (qa.md:5892) step: Toulouse, Iapetus, walk the caged-humans chain to `35 Humans not informed` | say: *"I want to talk to the prisoners."* | expect: He refuses (`37`); afterwards Poimaino offers the bluff. Without asking Iapetus, the bluff reply is absent
- [ ] `TO4` (qa.md:5893) step: TO3, then Poimaino at Speech 95+ / below 95 | say: *"It's okay, Iapetus said I could speak with the prisoners."* | expect: `30 bluff SUCCESS` -- he stands down and the pen is enterable without him turning hostile / `30 bluff FAILURE`, he refuses; exactly one of the two replies is ever offered
- [ ] `TO5` (qa.md:5894) [eyes + save] step: Toulouse, get the flask from the rock (Mathuo's `10 Shapeshifter` -> *"Where were you when the attack occurred?"* first), then Poimaino at Speech 50+ | say: *"...Wouldn't a little mercury be good right about now?"* | expect: `40 Mercury SUCCESS`; the mercury leaves inventory; he stops challenging you and answers *"Leave me alone, runt"*; the pen is enterable
- [ ] `TO6` (qa.md:5895) [eyes + save] step: TO5 with Speech under 50 | say: The same reply | expect: `40 Mercury FAILURE` -- *"I won't take a drink from the likes of *you*... You'll have more luck with Mathuo"*; the flask is **not** taken and the Mathuo route still works
- [ ] `TO7` (qa.md:5896) step: Carrying no mercury, talk to Poimaino | say: - | expect: Neither mercury reply is offered (the old Wine-gated version is gone)
- [ ] `TO8` (qa.md:5897) step: TO5, then free the prisoners through Thierry (`100 See you in Montaillou`) | say: - | expect: `Prisoners escape` runs as it does on the Mathuo route; the rescue completes and Thierry can be met in Montaillou
- [ ] `TO9` (qa.md:5898) step: Toulouse, Iapetus, reach `60 It feeds off titan magic` as any spirit-bearing character | say: *"I carry a bound spirit of my own..."* | expect: `61 your spirit`: it would take the spirit and leave you standing empty; the three replies out all work. A Pureblood must not see the reply
- [ ] `TO10` (qa.md:5899) step: Toulouse, Iapetus, `65 Forms`, as a Feralkin or Sylvant | say: *"A bear leaves a bear's tracks..."* | expect: `66 tracks`: the spoor by the rocks in the southeast cul-de-sac; a human or Demokin never sees the reply
- [ ] `TO11` (qa.md:5900) [eyes + save] step: Toulouse, Iapetus, `75 Mercenary help`, at Barter 40+ | say: *"Put gold beside the gems..."* | expect: `77 haggle`, then *"Agreed"*; kill the Daeva and return: three Expensive Gems **and** 2,000 gold. Below Barter 40 the reply is absent, and without the bargain the payout is gems only -- *Needs Barter 40.*
- [ ] `TO12` (qa.md:5901) step: Toulouse, Rhea, walk the History branch to `30 History 3`, as an Ancestral / Beastial / Demonic spirit-bearer | say: The matching reply | expect: Exactly one of the three is offered, matching your spirit, each with its own answer, then back to `30 Utnapishtim`. **This is the first `CHasSpirit` in a dialogue requirement in the game: check it fires at all, and that it fires for the right spirit** -- *Needs one spirit-bearer of each kind.*
- [ ] `TO13` (qa.md:5902) step: TO12 as a Demokin with a Demonic spirit | say: *"The thing bound to me is neither an ancestor nor a beast."* | expect: `30 spirit demonic`. `Spirits/Demonic` is extrapolated from the model name -- if this reply never appears while TO12's other two do, that value is wrong
- [ ] `TO14` (qa.md:5903) step: Toulouse, Rhea, `30 Utnapishtim`, as a sworn Inquisitor | say: *"Utnapishtim was the first Inquisitor, then."* | expect: `31 the first inquisitor`; absent to everyone else
- [ ] `TO15` (qa.md:5904) step: Toulouse, Rhea, Memory branch to `53 Sacrifice`, carrying the Necromancer title | say: *"You cut a crystal out of a living elder..."* | expect: `53 necromancer`; she steps back; the three replies out all land; absent without the title
- [ ] `TO16` (qa.md:5905) step: Toulouse, Mathuo, `10 Shapeshifter`, at PE 7+ | say: *"Unready. You were deep in the mercury..."* | expect: `11 drunk`; afterwards the flask is in the rocks (the reply fires `mercury relay`), so `25 Mercury` and the pickup both work. Below PE 7 the reply is absent
- [ ] `TO17` (qa.md:5906) step: Toulouse, Tereo's first challenge, as a sworn Inquisitor | say: *"I am the Inquisition..."* | expect: `51 the Inquisition`; he grants the offices are alike; the four replies out all land. Absent to anyone not of the Inquisition
- [ ] `TO18` (qa.md:5907) step: Toulouse, Tereo, reach `24 A titan must earn his name`, carrying the Child Killer title | say: *"They call me a killer of children."* | expect: `25 the name you have earned`; he steps back and refuses your birth-name
- [ ] `TO19` (qa.md:5908) step: TO18 carrying Goblin Champion instead | say: *"The goblins of the Crossroads named me their champion."* | expect: `25 a name that was earned`; he approves. Carrying both titles, both replies show; carrying neither, neither does
- [ ] `TO20` (qa.md:5909) step: Toulouse, Tereo, `22 Titans aren't named at birth`, as a Feralkin, Sylvant or Demokin | say: *"My kind was named twice..."* | expect: `23 named twice`; a human never sees the reply
- [ ] `TO21` (qa.md:5910) step: Toulouse, Tereo, `41 Ogres`, at Outwit 7+ | say: *"One human, or two?"* | expect: `43 counting`: two, perhaps three, and the ogres are not watched closely. Below Outwit 7 the reply is absent
- [ ] `TO22` (qa.md:5911) step: Toulouse, Lethos, `101 Lucius must die`, as a tainted or demokin character with Speech under 50 | say: *"Your tribe decided what he is..."* | expect: `120 Nonviolent help` -- the negotiated ending opens without the Speech check; a human under Speech 50 still cannot get there
- [ ] `TO23` (qa.md:5912) step: Toulouse, Lethos, `140 Explanation for the very dim`, as a Wielder | say: *"My order binds spirits into stones..."* | expect: `141 a Wielder reads the mneme`; he denies the comparison; the three replies out land. Absent to non-Wielders
- [ ] `TO24` (qa.md:5920) step: **Fresh Toulouse.** Walk into the prisoner pen past Poimaino without the bluff or the bribe | say: - | expect: *"Stop, you are entering the human pen. If you insist on proceeding I'll have the pleasure of squashing you."* over Poimaino, and then he and Mathuo turn on you as before. After the bluff or the bribe, crossing the line does neither -- *Line now ends 'the pleasure of killing you'.*
- [ ] `TO25` (qa.md:5925) step: Toulouse, talk to Ephebos (the young titan beside Rhea) | say: Each of his four openings in turn | expect: `10 the chain` / `11 no name yet` / `12 Tereo` / `40 the pen` / `41 like me` all land; the mercury reply is absent without the flask, and the *"Rhea caught you"* reply is absent until you have overheard Rhea's lecture
- [ ] `TO26` (qa.md:5926) [eyes + save] step: TO25 carrying Titan Mercury, give it to Ephebos | say: *"I am carrying a flask of quicksilver..."* | expect: `30 mercury`: he takes it, the flask leaves inventory, and he gives up Baktron and Klao. Mathuo and Poimaino can then **not** be given it
- [ ] `TO27` (qa.md:5927) step: Toulouse, the prisoner pen: talk to the man, the woman, and the child | say: Each reply in turn | expect: The man on the bait and on running; the woman on her neighbour's voice at the fence and the deer that did not run; the child's count of when nobody is watching. **The child is a new placement -- check he is in the pen and not standing outside it**
- [ ] `TO28` (qa.md:5928) step: TO27 as a Feralkin, Sylvant or Demokin | say: The woman's and the child's extra replies | expect: `64 the face` and `66 the child and the devil`; a human sees neither
- [ ] `TO29` (qa.md:5929) [eyes + save] step: Toulouse, carrying a skin of wine, talk to an ogre | say: *"I have a skin of wine. What is it worth to you?"* | expect: The wine leaves inventory, `51 wine` -> `52 what the ogre saw` -> `53 where`: the deer that walked on two legs, and the rocks in the southeast. Without wine the reply is absent
- [ ] `TO30` (qa.md:5930) step: Toulouse, walk into the cul-de-sac in the south-east | say: - | expect: One balloon about churned ground; at PE 7+ a second line about deer slots with no stride. Fires once only
- [ ] `TO31` (qa.md:5931) step: Toulouse, Iapetus, `65 Forms` | say: *"Is there anything that can pin such a thing into one shape?"* | expect: `67 the prophets`: a relic of Zarathustra strips a Daeva's shape. Then fight the Daeva **carrying the Amulet of the Prophet** and confirm its own `31 amulet speech` branch fires
- [ ] `TO33` (qa.md:5933) step: Toulouse, attack any titan | say: - | expect: Menoetius turns hostile with the rest of the tribe (the alarm relay could not reach him before)
- [ ] `TO34` (qa.md:5934) step: Toulouse, walk past Baktron and Klao at the north end until their argument plays, then talk to each | say: Their new replies | expect: `02 the plot` / `03 patience` from Baktron, `02 patience is not obedience` from Klao. Before overhearing them, neither reply is offered
- [ ] `MO6` (qa.md:5941) step: Titan Village, after Rhea, Speech 50+ | say: Ask if it can end without killing -> *"Hear a proposal before you spend him."* | expect: `120 Nonviolent help`; the press is absent below Speech 50
- [ ] `MO7` (qa.md:5942) step: MO6, Outwit 8+ / under 8 | say: The proposal | expect: `121 Nonviolent success` / `122 Nonviolent failure`; both then let you name your price as the killing route does
- [ ] `MO10` (qa.md:5945) step: MO9, back to Lethos | say: *"Memnos is coming back to you."* | expect: `502`; the reward paid; the titans pack up and leave Toulouse as they do for the crystal
- [ ] `MO22` (qa.md:5957) step: Toulouse, Lethos, before Rhea | say: *"What is it you want of me, then?"* -> *"I will speak with Rhea."* | expect: `60 Go speak to Rhea`; a second visit then opens *"Hello again"* rather than the first meeting again

**Toulouse**

- [ ] `TD6` (qa.md:2691) step: Walk past the prisoner pen with Thierry alive | say: - | expect: His prompt still works. The prompter also tests whether he is alive and was deliberately left alone
- [ ] `FP1` (qa.md:6346) [eyes + save] where: Talk Lethos into leaving with Thierry alive | steps: Watch the fade | pass: The titans go. **The prisoners and Thierry are still in the pen afterwards**, and nobody attacks -- *Needs a save that has not entered Toulouse.*
- [ ] `FP2` (qa.md:6347) where: FP1, click a villager man or woman | steps: - | pass: *"The ogres have gone, and nobody will say why..."*, not the old downcast line. The child says *"Is it over?..."*
- [ ] `FP3` (qa.md:6348) where: FP1, click Thierry | steps: *"The titans have gone. All of them. You are free to go."*, then *"Then go..."* | pass: *"Follow me, brothers!"*, then he **and all three villagers walk** out along the path. If they stand still, the AI Done did not land
- [ ] `FP4` (qa.md:6349) [eyes + save] where: FP3, follow them | steps: Wait 30 seconds | pass: They disappear at the end of the path and do not stand there forever. Clicking one mid-walk does nothing
- [ ] `FP7` (qa.md:6352) where: **Thierry dead.** Kill him or let him die, then FP1 | steps: Click a villager man or woman | pass: *"Thierry is dead..."*, then *"You are free to go."* Everyone walks. No balloon, and Esclarmonde still offers the dead-husband reply. The child never offers this
- [ ] `FP8` (qa.md:6353) where: **The regression.** Any other ending: free them through Thierry, kill the titans, or Memnos | steps: - | pass: Exactly as before. `TD3`-`TD4` still pass, and no villager uses the new lines

**Toulouse (Andre)**

- [ ] `TG7` (qa.md:2813) step: **Regression.** Andre's errand in Toulouse | say: - | expect: Still wants the four named Stone Hearts. Neither of these stones is one of them

**Toulouse (Lucius)**

- [ ] `TC6` (qa.md:2827) step: **Regression.** Lucius' Mneme, from Toulouse | say: - | expect: Still **violet**, unchanged. It shares the original icon; only the loot copy was recoloured

**Toulouse, then Montaillou**

- [ ] `TD4` (qa.md:2689) [eyes + save] step: Same for the other three resolutions: the prisoners escaping, the quest completing normally, and Memnos returning to his tribe | say: - | expect: Thierry alive sends him home; Thierry dead records it. All four behave the same way now

**Toulouse, then Montaillou road**

- [ ] `LU5` (qa.md:3839) where: **The row that proves it.** After LU4, kill the four Toulouse titans, return to Andre and hand over the four stone hearts | steps: - | pass: He uses **`1002 Hearts in Hand but Lucius betrayed`**: *"I've heard that you exposed me to the mayor despite the agreement we reached... you'll get not one more ounce of gold from me."* **And you should hear him say it** -- 306 KB of recording that never played

**Toulouse; Montaillou**

- [ ] `FP6` (qa.md:6351) [eyes + save] where: **Walk away.** FP1, leave Toulouse without talking to him, go to Montaillou, come back | steps: - | pass: Thierry is in Montaillou, and the pen is empty on your return. **He must not be in both**

**Witch cave**

- [ ] `TD9` (qa.md:1216) [eyes + save] where: Witch cave | steps: Walk through the fire, open the chest | pass: You get the **Ring of the Prophet**, and it kills the shapeshifting Daeva permanently. **PASSED** as far as the Ring; the permanent kill is vanilla and untested here

**inn and church**

- [ ] `HH47` (qa.md:6147) [eyes + save] where: Same, then Montaillou | steps: The inn and the church | pass: The Inquisitor Agent and Fournier attack. The siege is unchanged later

**anywhere in the act**

- [ ] `MA13` (qa.md:3680) where: **The Montaillou payoff.** Much later, meet him again in Montaillou | steps: - | pass: `300 machiavelli helps you in montaillou` still fires. Nothing in this release touches that chain, and it must not have broken
- [ ] `NR16` (qa.md:3746) where: Judge the **writing**, which no check can settle | steps: - | pass: Does the drunkard read as pitiable rather than comic? Is Na Roqua's warning about the dose unsettling? And is `Clear Head` a joke that lands, or one that explains itself too much?
- [ ] `LU13` (qa.md:3847) [save] where: **No duplicate journal.** Check the quest log through all of the above | steps: - | pass: Only `Retrieve the Crystal Mneme from Lucius` appears. `Help Andre the Titan with his tasks` is a superseded duplicate and must **stay** dormant
- [ ] `PO3` (qa.md:4378) [eyes + save] step: Hit a soldier **once** for light damage, well above 40% | say: - | expect: **Nothing.** It does not waste the draught on a scratch. This is the half that the health gate buys, and the reason the potion is not simply in series position
- [ ] `PO5` (qa.md:4380) [eyes + save] step: Fight a **`Soldier1`** or **`Soldier2`** of any variant | say: - | expect: **No draught.** Only the Soldier3 and Soldier4 tiers carry one
- [ ] `PO6` (qa.md:4381) [eyes + save] step: Fight each of the twelve: `Soldier3` ×3, `Soldier4` ×3, `Soldier4 Bow` ×3, `Soldier4 Mace` ×3 | say: - | expect: All drink, scaled to their own maximum -- 35 at the bottom of the ladder, 72 at the top
- [ ] `PO7` (qa.md:4382) step: **The regression row.** Listen to the veterans in a long fight | say: - | expect: Their **barks still work**. The first build of this destroyed the bark bank on all twelve cans; they were restored, but this is the row that proves it in play rather than in a diff
- [ ] `PO8` (qa.md:4383) step: Watch a soldier's attacks after it drinks | say: - | expect: **Unchanged.** The draught is in `Damaged Script Action`; the attack bank in `Shoot Completed` was not touched, and `Skill to select` counts are identical to before
- [ ] `PO9` (qa.md:4384) step: Judge whether it changes the fight | say: - | expect: A veteran should feel like it has **one more round in it** than before, not like a different enemy. If a `Soldier4 Super` now feels spongy, the dial is the 35% fraction or the 40% threshold -- say which direction -- *Judge against the 0.98.0 fidget-and-spill version.*
- [ ] `PO11` (qa.md:4386) [eyes + save] step: Check the drops after killing one | say: - | expect: **Unchanged.** No drop table was touched; the veterans still drop no spirit energy, which is a separate note in the act 6 section
- [ ] `MO28` (qa.md:5963) step: Fabrisse as a Feralkin, Sylvant or Demokin | say: *"...a face like mine on your street"* | expect: `25 tainted`; she does not step back; a human never sees the reply
- [ ] `MO29` (qa.md:5964) step: Aidan at Barter 40+ | say: *"...you are already charging war prices."* | expect: The peace price, then the shop opens 20% cheaper; below Barter 40 the reply is absent

## 4 Crypt (106)


**02 Hamlet Burned**

- [ ] `CR6` (qa.md:5889) [eyes + save] step: Take the quest, then let Montaillou burn (`02 Hamlet Burned`) | say: - | expect: The vanilla failure sweep fails it, as it always tried to -- now against a quest that has states to fail

**02 Hamlet Burned / world map**

- [ ] `BU23` (qa.md:4819) step: Reach the Crypt or Nostradamus, return to the burned hamlet, then try to travel to any Wilderness map | say: - | expect: **You cannot.** Confirm where the world map stops offering them. Everything in acts 1-4 is one-way after this point, and all 780 goblins live behind it

**1 Crypt Entrance / The Garrison's Camp**

- [ ] `CR14` (qa.md:1361) where: **A save that has never entered `1 Crypt Entrance`.** Walk to the sealed shrine door; a stairwell now stands beside it | steps: Step onto the stair | pass: You arrive in **The Garrison's Camp**. **Check the stair is visible, reachable, and not inside the door's own polygon**
- [ ] `CR15` (qa.md:1362) where: In the camp, walk back into the transition polygon | steps: - | pass: You return to `1 Crypt Entrance` at the stair, not at `Start Here` and not into a wall
- [ ] `CR16` (qa.md:1363) where: In the camp, look around | steps: - | pass: No zombies, terrors or festering undead spawn: the four horde spawners inherited from `3 Misc Crypt 1` are stood down. Three Templar knights are standing there
- [ ] `CR17` (qa.md:1364) where: Talk to the camp sentry | steps: *"I'm not here to steal the relic, I'm here to protect it."* | pass: `10 relic` -> *"Are you a Knight? Have you been sent to reinforce us?"* -> the quest opens (CR1), now reachable **before** the Doomed Plateau
- [ ] `CR18` (qa.md:1365) where: Talk to the knight at the fire, and to the one on the wall | steps: Each branch in turn | pass: `1 the fire` through `12 Jehanne`, and `1 the wall` through `41 what we are`. He sends you to Jehanne on the plateau and tells you to speak to her Council first
- [ ] `CR19` (qa.md:1366) where: CR18 after taking the quest from the Spirit Council (state `CRY2CURS`) | steps: *"I am here to end it."* / *"I may be him."* | pass: `30 end it` and `42 the order` -- both absent without the quest state
- [ ] `CR20` (qa.md:1367) where: CR18 after speaking to the Spirit Council at all | steps: *"Your commander says the Council has not spoken to her in a long while."* | pass: `20 the council`; absent to a player who has not been to the Council
- [ ] `CR21` (qa.md:1368) where: Attack any of the three camp knights | steps: - | pass: He goes to combat and gives the garrison's *"You will be destroyed!"*, as the forward knight does

**2 Retreat of Souls**

- [ ] `CR10` (qa.md:1357) where: **A save that has never entered `2 Retreat of Souls`.** Walk in from the Retreat of Souls Entry and head south-east towards the first zombies | steps: - | pass: A Templar knight is standing at (3060, 2140), in the open ground the zombies spawn into. **Check he is on floor and reachable, and that the horde attacks him**
- [ ] `CR11` (qa.md:1358) where: CR10, talk to him | steps: *"I'm not here to steal the relic, I'm here to protect it."* | pass: `10 relic`: *"Are you a Knight? Have you been sent to reinforce us?"* -- then the Templar answer, the lie, or the honest refusal, and the quest opens (CR1)
- [ ] `DP16` (qa.md:5670) step: Check `2 Retreat of Souls` | say: - | expect: Its three `Second Guardian` spawns are now at the restored strength too. They are weight 1, so they stay rare

**7 Doomed Plateau**

- [ ] `CR13` (qa.md:1360) where: Doomed Plateau, talk to the knight by the entrance repeatedly | steps: - | pass: The barks vary across the nine written lines rather than repeating *"Evil things lurk in the darkness"* every time
- [ ] `CV1` (qa.md:3316) step: Enter `7 Doomed Plateau` with **Joan of Arc** as a companion and fight | say: - | expect: She calls out while fighting, **in her recorded voice**: *"Hold strong, brothers!"*, *"En nom Dieu!"*, *"Fight bravely! Pour la France, pour Dieu!"*, *"Is there no end to these abominations?"* or *"These creatures must not steal the relic!"* Roughly one per eight of her own attacks
- [ ] `CV3` (qa.md:3318) step: Stand with Joan while nothing is fighting | say: - | expect: **Silence.** The bank hangs off completed attacks, so an idle companion says nothing
- [ ] `CV4` (qa.md:3319) step: **The regression row for the cutscene.** Arrive on the plateau for the first time and watch the Joan sequence | say: - | expect: Unchanged: `420 wait`, then `421 Now`, then *"These creatures must not steal the relic!"*, **and control returns**. That line is now also in her bark pool; the scene must still play it in its place and end
- [ ] `CV5` (qa.md:3320) [eyes + save] step: Check the dialogue log after a fight with Joan | say: - | expect: Her barks are **not** logged. The cutscene lines still are. Barks repeat, and the log is not for repeats
- [ ] `BL1` (qa.md:5438) step: Fight the **Bonecaller** on the Doomed Plateau | say: - | expect: Roughly one attack in four is a summon: a spellcast animation, then ghouls rising beside him with a summoning effect
- [ ] `BL2` (qa.md:5439) step: Count what the base Bonecaller raises across a whole fight | say: - | expect: Four ghouls, then no more. Tough raises five, Super six -- *0.26.0 also adds a one-time 3-5 ghoul burst below 40% (PH1), so the total is higher than four.*
- [ ] `BL3` (qa.md:5440) [eyes + save] step: Check what comes up | say: - | expect: Ghoul Male and Ghoul Female and their Tough/Super variants -- the Plateau's existing `ghoul clone generator`, not a new creature
- [ ] `BL4` (qa.md:5441) step: Kill the Bonecaller mid-summon | say: - | expect: No orphaned clone generator is left behind and nothing keeps spawning
- [ ] `BL5` (qa.md:5442) step: Talk the Bonecaller down instead, as 0.21.0 allows | say: - | expect: He stops summoning along with everything else. The stand-down is unaffected
- [ ] `DP1` (qa.md:5648) step: Enter `7 Doomed Plateau` and find the Bonecaller, north-east of the slope | say: - | expect: A lich in rotted mail that **does not attack on sight**: `1 the bonecaller`, *"you are the first new thing on this plateau in ninety years"* -- *Line now reads 'in longer than I can count', not 'ninety years'.*
- [ ] `DP2` (qa.md:5649) step: Talk to it as a **Wielder**, or with **Divine 80+**, or **Speech 80+** | say: - | expect: A route into `10 bound`. Each order of approach has its own line; all three reach the same node
- [ ] `DP3` (qa.md:5650) step: Ask *"What are you?"* first | say: - | expect: `5 the answer` -- it raises what falls, the knights cut it down, and tomorrow it raises them again
- [ ] `DP4` (qa.md:5651) step: At `10 bound`, use **Speech 110** or **Divine 80** | say: - | expect: `20 stands down`. It stops, and is retagged into the other army
- [ ] `DP5` (qa.md:5652) [eyes + save] step: Watch it after it stands down | say: - | expect: **The horde attacks it and it fights back.** It is retagged `Scripted Custom 2,Undead` and pointed at `Enemy`, which is what all 81 horde generators target and what every horde spawn carries
- [ ] `DP5a` (qa.md:5653) [eyes + save] step: Check the journal XP after standing it down | say: - | expect: **2000 XP**, from the anchor part `Fixt Talked the Bonecaller Down XP`. If the horde then kills the Lich, that kill XP is theirs, not yours -- 2000 is the whole of the peaceful route's award
- [ ] `DP5b` (qa.md:5654) step: On a character with **karma under 600**, reach `10 bound` | say: - | expect: A third reply: *"Keep your orders. I will open the keep for you, and you will owe me the spear."* -> `21 the bargain`. A high-karma character does not see it -- *Needs karma under 600.*
- [ ] `DP5c` (qa.md:5655) [eyes + save] step: Take the bargain | say: - | expect: 2000 XP from `Fixt Sworn to the Bonecaller XP`, and the Lich is retagged `Player Friend,Undead` pointed at `Undead`
- [ ] `DP5d` (qa.md:5656) step: Walk it toward the keep | say: - | expect: **The Templar garrison attacks it** -- they target `Player,Player Friend` -- and the horde ignores its own commander. It fights the knights
- [ ] `DP5e` (qa.md:5657) step: After the bargain, talk to an Undead Templar | say: - | expect: *"Are you a Knight? Have you been sent to reinforce us?"* has **no good answer left**: all three recruitment replies are gone, including the `<Lie>`. Only *"No, I came to destroy you"* remains
- [ ] `DP5f` (qa.md:5658) step: On a separate run, release the Lich instead, then talk to a Templar | say: - | expect: Recruitment still works. `Fixt sworn to the Bonecaller` is only set by the bargain
- [ ] `DP5g` (qa.md:5659) step: On a **high-karma** character, check the release arm is still offered | say: - | expect: Yes. The release arm is ungated by karma on purpose -- anyone may free it, only the wicked may recruit it
- [ ] `DP6` (qa.md:5660) step: Refuse it, or say you have nothing to say to the dead | say: - | expect: It fights. HP 385/462/520 by party level, AC 80 -- easy to hit, huge pool, **immune to cold, poison and disease, and weakest to fire**
- [ ] `DP7` (qa.md:5661) [eyes + save] step: Kill it | say: - | expect: 1500/2000/2500 XP by tier. This is the first time anything in the game has spawned a `Boss Lich`: three races, a sprite and seventeen animations shipped with no template pointing at them
- [ ] `DP8` (qa.md:5662) step: Find the Bonewright, mid-slope west | say: - | expect: `100 the bonewright` as it plants its standard, and the fallen around you start getting up
- [ ] `DP9` (qa.md:5663) step: Stand and fight near it for a minute without killing it | say: - | expect: Waves keep arriving, roughly every 22 seconds. They are `Greater Skeleton` tiers from a generator it switches on
- [ ] `DP10` (qa.md:5664) step: Kill the Bonewright | say: - | expect: `101 the bonewright falls`, and **the waves stop** -- the relay and its generator are both shut off permanently
- [ ] `DP11` (qa.md:5665) step: Check the Bonewright's own strength | say: - | expect: HP 250/400/600, AC 175/215/300. In vanilla it ran on `Ghoul Male Large` at 150/200/275 while its own race sat unused
- [ ] `DP12` (qa.md:5666) step: Find the Revenant Sergeant, east of mid-slope | say: - | expect: `110 the sergeant`. It is fighting the Templar knights and **has not looked at you**
- [ ] `DP13` (qa.md:5667) step: Bring it below **66%** | say: - | expect: `111 the sergeant rallies` -- its section leaves the knights and closes on you
- [ ] `DP14` (qa.md:5668) [eyes + save] step: Bring it below **33%** | say: - | expect: `112 the sergeant fixates`. It abandons the battle: `Valid Targets` narrows to `Player` and it comes through its own dead
- [ ] `DP15` (qa.md:5669) step: Check the Templar garrison still works | say: - | expect: `UndeadTemplar` unchanged: it still mistakes you for a monster, still recruits a Templar, still says *"Find Jehanne"*
- [ ] `CR2` (qa.md:5885) [eyes + save] step: CR1, then the Spirit Council on `7 Doomed Plateau`, hear the wish out to `40 Pious Child` | say: *"I will see what I can do."* | expect: State 2. Also reachable from `30 Efreet`. A player who never talks to a knight should still get the quest here
- [ ] `CR5` (qa.md:5888) [eyes + save] step: Kill Jehanne, then talk to the Spirit Council | say: - | expect: Its Joan-dead curse plays and the quest **fails** if it was active. If she dies before you ever met a knight, the quest was never active and nothing should appear in the journal

**7 Doomed Plateau (Jehanne)**

- [ ] `CR9` (qa.md:1356) where: Do **not** convince her; return and talk again | steps: - | pass: Still *"I warn you, monster, leave this crypt with haste"*. The warm greeting must not open for a player who never spoke for the Council
- [ ] `CR31` (qa.md:1378) where: Crypt, Jehanne, as a **Templar**: claim the Lance for the order, then press her | steps: *"look at the shield properly, commander"* | pass: `43 the successor` -> `44 what we became`. She stops, will not call you a liar again, and still refuses the Lance
- [ ] `CR32` (qa.md:1379) where: As an **Inquisitor** | steps: *"I hold the Church's writ over the unquiet dead"* | pass: `45 jurisdiction`: Rouen, and then the practical point. `46 the same enemy` from the conciliatory reply -- *0.99.1 removed the Rouen history from her lines; match by node, not text.*
- [ ] `CR33` (qa.md:1380) where: As a **Knight of Saladin** | steps: *"A Saracen of my order stood where I am standing"* | pass: `47 the lamp` -> `48 undo it`. Then the Spirit Council's `31 the Saracen was yours` from its wish account -- *0.99.1: she no longer knows the lamp at a first meeting; check node only.*
- [ ] `CR34` (qa.md:1381) where: As a **Wielder without** the Necromancer title | steps: *"It was not a curse. It was a contract, badly worded."* | pass: `49 the binder`. The Dark Wielder reply must **not** be offered
- [ ] `CR35` (qa.md:1382) where: As a **Wielder carrying** the Necromancer title | steps: *"Your Council is right about me."* | pass: `50 she was right` -> `51 not your knights`. The plain Wielder reply must **not** be offered: the two are mutually exclusive
- [ ] `CR36` (qa.md:1383) where: As a member of the **Goblin Horde**, or carrying Goblin Champion | steps: *"I ride with the Horde of the Khan"* | pass: `52 the khan` -> `53 nothing to weigh`; offered from her first meeting, her hostile return and `10 jehanne`
- [ ] `CR47` (qa.md:1394) where: Recruit Jehanne on the Doomed Plateau | steps: - | pass: She says *"Let us cleanse this place of evil."* over her own head as she joins -- **the first time this line has ever played**
- [ ] `CR48` (qa.md:1395) where: Talk to her as a companion, answer *"No, wait here for my return"* | steps: - | pass: `600 Companion Wait`: *"If that is your order, I will wait and guard here until you return."* Then the reply *"Hold this ground until I return."* closes the conversation. **Check it closes cleanly rather than hanging**
- [ ] `CR57` (qa.md:1404) where: Ask Jehanne *"Tell me about yourself"* as a **female** Scion | steps: *"They burned you for wearing a man's armour..."* | pass: `54 the same armour`. As a **male** Scion, *"What was the charge, in the end?"* -> `55 the charge`. Never both -- *0.99.1 rewrote her trial lines; nodes 54/55 remain, text differs.*
- [ ] `CR58` (qa.md:1405) where: From `54`/`55`, take each of the three routes out | steps: - | pass: `100 spoke to counsel` (only when the Council has been spoken to), `50 Counsel`, `5 Goodbye`

**8 Ante Chamber, 9 Burial Chamber**

- [ ] `CV2` (qa.md:3317) step: `CV1`: keep her through `8 Ante Chamber` and `9 Burial Chamber` | say: - | expect: The line **varies**. All five should turn up over a long fight; one line repeating means the pool is not wired as a pool

**9 Burial Chamber**

- [ ] `AF5` (qa.md:5562) step: In `9 Burial Chamber`, secure the relic, then re-enter Jehanne's polygon | say: - | expect: She reacts to the relic being secured
- [ ] `CR3` (qa.md:5886) [eyes + save] step: CR2, find the lamp of Jah'roosh in `9 Burial Chamber` and talk to the Efreeti | say: *"<Say nothing yet, and look at the lamp.>"* | expect: State 3, whose text warns that the garrison is undead too. The reply loops back so the wish menu is still available
- [ ] `CR4` (qa.md:5887) [eyes + save] step: CR3, wish the curse undone | say: *"I wish to undo the curse laid upon Jehanne's soul..."* | expect: `100 save inga`; the quest completes and pays 2,500 XP; the existing relays (`Wished to Save Inga and Knights`, `Efreet goes away`) still fire
- [ ] `TS6` (qa.md:6081) [eyes + save] where: **Act 4, `9 Burial Chamber`.** Carry the Lion Shield in | steps: Free the knights: *"I wish to undo the curse laid upon Jehanne's soul..."* | pass: The Lion Shield is **taken** and the Holy Shield given, with a combat-log line. The quest completes and its XP still arrives
- [ ] `TS7` (qa.md:6082) [save] where: Same, **without** the Lion Shield | steps: Make the same wish | pass: Quest completes, XP arrives, **no shield**. The grant is gated on carrying it and must not fire empty-handed
- [ ] `TS8` (qa.md:6083) [eyes + save] where: Same | steps: Reach the wish via the clever route -- *"I've heard stories of your kind"* or *&lt;Read the wish itself.&gt;* -- then spend the true wish on the knights | pass: Identical outcome to TS6. Both routes land on the same node
- [ ] `TS9` (qa.md:6084) [save] where: Same | steps: Wish **selfishly** instead: stronger, richer, smarter, or tell him to get lost | pass: No shield, and no quest completion. Only the selfless wish frees them

**Burial Chamber**

- [ ] `CR49` (qa.md:1396) where: Take her into the Burial Chamber and **attack a garrison templar** | steps: - | pass: She turns on the player (`601 Joan Leaves party and Attacks Player`). **This has never fired in vanilla; it is the one thing in tier 9 most worth watching**
- [ ] `CR50` (qa.md:1397) where: CR49 without her -- enter the Burial Chamber alone and attack a templar | steps: - | pass: Nothing of hers fires, no error. The check now asks whether she is alive on the map, so an absent companion must read as absent
- [ ] `CR51` (qa.md:1398) where: Take the Bleeding Lance with her beside you, then walk away from the plinth | steps: - | pass: *"the relic is *safe* at last. I may finally...rest..."* Fires **once**: walk back in and out again and it must not repeat
- [ ] `CR52` (qa.md:1399) where: CR51 without her, and CR51 without picking up the Lance | steps: - | pass: Silence in both cases

**Burial Chamber (assassin)**

- [ ] `PM23` (qa.md:1337) where: Holding the ring, Crypt Burial Chamber assassin | steps: *"Your captain at Montserrat sent me north under this"* | pass: `21 her mark`, then the vanilla vanish-and-fight exactly as `20 threat`; the reply absent without the ring

**Crypt**

- [ ] `AT9` (qa.md:2906) step: **Regression.** Take Joan as an ally into the Crypt and fight beside her | say: - | expect: Her combat banter from 0.56.0 still plays

**Crypt (Efreeti)**

- [ ] `CR26` (qa.md:1373) where: Crypt, the Efreeti, with any Thought magic skill at 80+ | steps: *"<Read the wish itself.>... Grant mine straight."* | pass: `211 true wish` -- the same node IN 6 + Speech 95 reaches. Below 80 the reply is absent, and the social route still works

**Crypt (Joan of Arc)**

- [ ] `S7` (qa.md:1034) where: Joan of Arc, the Crypt | pass: 3 new replies, including claiming the Bleeding Lance for the Order

**Crypt (any trap)**

- [ ] `CR22` (qa.md:1369) [eyes + save] where: Crypt, any trap, with `Lockpick Disarm Traps` **40 or better** | steps: Click the trap | pass: It disarms as before: the sound, *"Disarmed Trap"*, 75 XP, and the trap's polygon goes dead
- [ ] `CR23` (qa.md:1370) where: The same trap with the skill **under 40** | steps: Click the trap | pass: *"The mechanism is beyond you"*, and the trap is still armed -- walking over it still triggers it
- [ ] `CR24` (qa.md:1371) where: CR23, then raise the skill to 40+ and click the same trap again | steps: - | pass: It disarms. **`Trigger Only Once` was 1 in vanilla, so without this release's change to 0 the failed attempt would have locked the trap forever**

**Crypt / Alamut maps**

- [ ] `WD1` (qa.md:4012) [eyes + save] step: **The row this exists for.** Play act 4 or act 8 -- the Crypt, Alamut's Maw of the Assasin, Chamber of Torment, Dark Temple -- and look at what drops | say: - | expect: **Magic rings, amulets, belts, bracers, cloaks and helmets.** 40 enchantments that have never appeared on those slots in this game. Previously only the plain versions dropped
- [ ] `WD2` (qa.md:4013) step: Compare against a vanilla install in the same maps | say: - | expect: Plain equipment still dominates -- it keeps its weighting of 17 against the magic branch's 2. If plain gear has become scarce, the weighting is wrong

**Crypt camp**

- [ ] `TF1` (qa.md:3352) step: Ask the knight at the fire in the Crypt camp how the war goes, at each of the three tide states | say: - | expect: `60 the line has moved`, `61 the line has slipped`, `62 the line is where it was`. **Unchanged.** Three superseded drafts were deleted from `The Fronts`, and this is the report that survives

**Doomed Plateau**

- [ ] `AT4` (qa.md:2901) step: Attack Joan of Arc on the Doomed Plateau | say: - | expect: *"So be it, monster. We will send you back to the fires of perdition."*
- [ ] `PH1` (qa.md:5340) step: Fight a Bonecaller down past **40%** health | say: - | expect: It raises a burst of ghouls once, with the summoning effect. 3, 4 or 5 by tier
- [ ] `PH2` (qa.md:5341) step: Keep fighting below 40% | say: - | expect: The burst does **not** repeat. It is a threshold crossing, not a state
- [ ] `PH3` (qa.md:5342) step: Kill one from above 40% in a single burst of damage | say: - | expect: Crossing below still fires it, or it dies first. Either is acceptable; note which
- [ ] `PH4` (qa.md:5343) step: Judge whether the Plateau is still winnable | say: - | expect: The row that decides whether this stays. The only item that adds enemies mid-fight

**Joan's gallery**

- [ ] `CE3` (qa.md:2572) [eyes + save] step: **The repair.** Walk into Joan's gallery in the Crypt without talking her down, and level up | say: - | expect: **No balloon and no grant.** On 0.72.0 she gained +5 HP and +3 AC per level while still hostile

**Misc Crypts 1-4**

- [ ] `CR38` (qa.md:1385) where: **A save that has never entered the Misc Crypts.** Walk into each of the four | steps: - | pass: Each map now says what it is, once, as you enter: the rear passage, the stone door, the last coffin's walls, the three crypts. **Check each voice fires where the polygon is and not through a wall**
- [ ] `CR39` (qa.md:1386) where: `3 Misc Crypt 1`: throw the lever by the wooden door | steps: - | pass: *"The bar drops into its brackets"*; the door closes visibly (it starts Open); tide +1
- [ ] `CR40` (qa.md:1387) where: `4 Misc Crypt 2`: pass the stone door, then throw the lever behind it | steps: - | pass: *"The counterweight drops and the stone seats itself"*; `Door1` closes; tide +1. **Check the door can still be reopened normally so nobody is sealed in**
- [ ] `CR41` (qa.md:1388) where: `5 Misc Crypt 3`: throw the lever by the last coffin | steps: - | pass: All thirteen protect walls open at once; tide -1
- [ ] `CR42` (qa.md:1389) where: `6 Misc Crypt 4`: throw vanilla's crypt-opening switch | steps: - | pass: The three crypts open and spawn as they always did, plus *"whatever the garrison was keeping in here is loose"*; tide -1

**Retreat of Souls / Doomed Plateau / Ante Chamber / Burial Chamber (coffins)**

- [ ] `CR28` (qa.md:1375) where: Crypt, find the broken coffins on `2 Retreat of Souls`, `7 Doomed Plateau`, `8 Ante Chamber`, `9 Burial Chamber` **without** Necrosage or the Necromancer title | steps: Click each | pass: Bones and dust -- one plain line each. **Check each marker is visible and clickable where it stands**
- [ ] `CR29` (qa.md:1376) where: CR28 carrying **Necrosage** | steps: Click each | pass: The four readings: died twice, killed nine times, opened from the inside, and the untouched original tenants
- [ ] `CR30` (qa.md:1377) where: CR28 carrying the **Necromancer** title instead | steps: Click each | pass: The same four readings: the check is Necrosage OR Necromancer

**Spirit Council**

- [ ] `CR53` (qa.md:1400) where: Ask the Spirit Council *"Who do you think I am?"* as each spirit | steps: - | pass: Ancestral -> `11 we see your dead`; Beastial -> `12 we see the beast`; Demonic -> `13 we see the pit`. **Exactly one of the three should ever be offered**
- [ ] `CR54` (qa.md:1401) where: CR53, then *"Then tell me the rest of it."* | steps: - | pass: Lands on `20 The Wish Explained` and the vanilla story runs normally from there
- [ ] `CR55` (qa.md:1402) where: Reach `40 Pious Child` with karma **1200+** | steps: *"You are asking a great deal of a stranger."* | pass: `41 we know what you are`. With karma **800 or less**, `42 we asked anyway`. Between the two, neither reply is offered and the node is exactly as vanilla left it
- [ ] `CR56` (qa.md:1403) [eyes + save] where: CR55 -> *"I will see what I can do."* | steps: - | pass: Quest state `CRY2CURS` activates, same as vanilla's own reply on that node

**The Garrison's Camp (knight at the fire)**

- [ ] `CR43` (qa.md:1390) where: With tide **positive**, ask the knight at the fire how the line stands | steps: *"How does the line stand today?"* | pass: `60 the line has moved`. With tide negative, `61 the line has slipped`; at zero, `62 the line is where it was`. Exactly one of the three replies should ever be offered
- [ ] `CR44` (qa.md:1391) where: Free the knights (CR4) with tide **positive** | steps: - | pass: *"freed in good order"* -- they go out from the corridors you shut first
- [ ] `CR45` (qa.md:1392) where: CR44 with tide **negative** | steps: - | pass: *"freed into a ruin"*
- [ ] `CR46` (qa.md:1393) where: CR44 having touched no lever at all | steps: - | pass: *"freed from a stalemate"* -- the siege stops having two sides. **This is the vanilla-equivalent path: confirm a player who ignores tier 8 entirely still completes the quest normally**

**anywhere in the act**

- [ ] `PS5` (qa.md:2306) step: Carry it through the **Crypt** (act 4) | say: - | expect: Effectively a plain weapon for that whole act. This is intended, and is why its number is higher than any unconditional suffix
- [ ] `GS4` (qa.md:2352) step: A weapon of **Exorcism** against the Crypt's undead | say: - | expect: Noticeably larger than before, about 12.6 on a 6,000 gold weapon. Undead are 85% of act 4, so this is the easiest of the three to feel
- [ ] `WD8c` (qa.md:4022) step: **The Crypt onward, mojo above 16** | say: - | expect: The full **40**, including Very Rare and Unique. A `Ring Metal Fist` or `Helmet Sylvant` is fair here and was not in act 1
- [ ] `TS13` (qa.md:6091) [eyes + save] where: **The regression.** Play a non-Templar through the Crypt | steps: Finish the act normally | pass: Nothing about the Doomed Knights questline changed: same dialogue, same quest states, same XP. The only addition is one conditional action that does nothing without the Lion Shield

## 5 Nostradamus (110)


**01 Heart Entrance**

- [ ] `HJ1` (qa.md:6331) [eyes + save] where: `01 Heart Entrance`, reach Huko without fighting if you can | steps: *"I have come to help the Prophet."* | pass: The Hujark **standing around you** stop attacking at once. This row proves the retarget. If they keep swinging, the names or the spawn timing are wrong

**01 Heart Entrance (English ogres)**

- [ ] `NO26` (qa.md:1431) where: **A save that has never entered act 5.** Stand near the English ogres on the Heart Entrance for a minute | steps: - | pass: They bark every five seconds or so, eight lines shuffled: *"Engage the savages!"*, *"Press on for England, men!"*, *"For the Queen!"* and so on. **None of these has ever played -- their speaker did not exist and the relay was fired by nothing**
- [ ] `NO27` (qa.md:1432) where: Watch where the English barks appear | steps: - | pass: Over one particular ogre (`English loser`, from the `Big Fight` at 2096,1418), not over the player and not over a Hujark

**01 Heart Entrance (Huko)**

- [ ] `NO1` (qa.md:1406) [eyes + save] where: **A save that has never entered act 5.** Walk in from the wilderness | steps: - | pass: Huko, General to the Hujark, and his guard are standing up the path. **Check first that he is on the floor and can walk to you** -- this spawn point has never run in the shipped game
- [ ] `NO2` (qa.md:1407) where: Stand still after arriving | steps: - | pass: Within a second or two he crosses the ground towards you and opens *"Where do you stand, stranger? Have you come to harm the Prophet, or help us save him from the Druids?"* He must **talk, not attack**
- [ ] `NO3` (qa.md:1408) where: Walk away before he reaches you, then click him | steps: - | pass: Same conversation, `1 Conversation Start`. His talk specifier had no action at all in vanilla
- [ ] `NO4` (qa.md:1409) where: Close the conversation without choosing, then click him again | steps: - | pass: `3 Return Dialogue`: *"You return? Have you changed your stance?"* -- **never reachable in the shipped game**
- [ ] `NO6` (qa.md:1411) [eyes + save] where: Instead answer *"If getting to the Prophet means killing you, then you're my enemy"* | steps: - | pass: The quest **Defeat the Hujark defenders and capture Nostradamus** enters the journal, he says *"Then I will kill you with my own hands!"*, and the fight starts
- [ ] `NO7` (qa.md:1412) where: As an **Inquisitor**, reach any of his nodes | steps: *"In the name of the Inquisition, your cult dies here."* | pass: Replaces the ordinary fight reply -- the two are gated `Inquisitor IS` / `Inquisitor NOT` and never both
- [ ] `NO8` (qa.md:1413) [eyes + save] where: Attack Huko or his guard without talking at all | steps: - | pass: The damaged-script fires: the English quest enters the journal and both turn on you
- [ ] `NO10` (qa.md:1415) [save] where: Leave the act to the wilderness and come back | steps: - | pass: Exactly one Huko. `Already Generated=0` must not produce a second
- [ ] `NO11` (qa.md:1416) where: Stand near Huko for half a minute before talking | steps: - | pass: He barks the Hujark lines every five seconds or so (`HujarkWarriorCanned`, eight nodes). Confirm they position over **his** head
- [ ] `NO60` (qa.md:1465) where: Ask Huko *"Who are the Hujark?"* as a **Feralkin**, **Sylvant** or **Demokin** | steps: - | pass: `41 driven out as we were` -- he looks at you properly for the first time
- [ ] `NO61` (qa.md:1466) where: The same as a **Human** | steps: - | pass: `42 you wear a face they accept`. Never both, and never neither
- [ ] `NO62` (qa.md:1467) where: Reach `10 explanation` with karma **1300+** | steps: *"Then let me say where I stand, and judge it as you like."* | pass: `43 you ask to be believed`. At **700 or below**, `44 you ask to be believed anyway`. Between them, neither reply is offered and the node is exactly as vanilla left it
- [ ] `NO63` (qa.md:1468) where: From each of Huko's four new nodes, take *"I have come to help the Prophet."* | steps: - | pass: `50 help prophet`, and the Hujark quest activates as in NO5
- [ ] `NO64` (qa.md:1469) where: From each of them, take the fight reply | steps: - | pass: The English quest activates and the fight starts, as in NO6. As an **Inquisitor** the reply is the Inquisition's version instead -- never both
- [ ] `NO78` (qa.md:1483) where: **A save that has never entered act 5**, with Speech **below 75**. Talk to Huko | steps: - | pass: Only the two vanilla doors. The third reply must not be offered
- [ ] `NO79` (qa.md:1484) where: The same with Speech **75 or better** | steps: *"I am not here for your Prophet and not here for the Druids."* | pass: `46 safe conduct`. Offered from `1 Conversation Start`, `3 Return Dialogue` and `10 explanation`
- [ ] `NO87` (qa.md:1492) where: **A save that has never entered act 5**, carrying the **Child Killer** title. Let Huko approach, or click him | steps: - | pass: `47 not from you` -- he has the sword up before a word is said. He must **never** open `1 Conversation Start` for this character, from either hook
- [ ] `NO88` (qa.md:1493) where: NO87: look for any way to offer him help, from every node you can reach including `30 Prophet` | steps: - | pass: There is none. All fifteen replies that reach `50 help prophet` are closed to the title. **The first cut of this tier leaked through `30 Prophet`**
- [ ] `NO89` (qa.md:1494) where: NO87 with Speech 75+ | steps: - | pass: The safe conduct is still offered and still works -- he wants you gone, and that is a deal he will take
- [ ] `NO90` (qa.md:1495) where: NO87 without Speech | steps: - | pass: Ask about the Prophet, or fight. Those are the only doors left
- [ ] `NO91` (qa.md:1496) where: Without the title, talk to Huko | steps: - | pass: `1 Conversation Start`, exactly as before. Nothing about the ordinary path changes
- [ ] `NO92` (qa.md:1497) where: Ask Huko *"Who are the Hujark?"* with **Tribal magic at 80+** | steps: - | pass: `48 your magic is ours` -- he looks at your hands rather than your face

**01-04 and caves**

- [ ] `NO34` (qa.md:1439) where: Side with Huko (NO5), then fight through `01`, `02`, `03`, `04` and the caves | steps: - | pass: **English soldiers and bowmen** (`Nos Soldier1/2/3`, `Nos Soldier2 Bow`) instead of Hujark swordsmen. 99 generator parts across nine maps; `02` has the most (34)
- [ ] `NO36` (qa.md:1441) where: NO34: count enemies against NO33 on the same map | steps: - | pass: Roughly the same. If the Hujark path feels heavier, the pacify branch is not firing; if much lighter, the English parts are not activating
- [ ] `NO38` (qa.md:1443) where: NO34 anywhere: wound an English soldier past half health | steps: - | pass: **No snake.** Tier 2's trigger is stripped from every English twin
- [ ] `NO39` (qa.md:1444) where: NO34: check the cave fauna | steps: - | pass: Snakebreed, spirits and vodyanoi attack you on both paths. They were deliberately left alone
- [ ] `NO80` (qa.md:1485) [eyes + save] where: Take it, then cross `01`, `02`, `03`, `04` and the caves | steps: - | pass: **The Hujark ignore you and the English hunt you.** No escort, no commentary line, and **nothing in the journal** -- neither quest activates
- [ ] `NO86` (qa.md:1491) where: Side with the English (NO6), then cross the act | steps: - | pass: Unchanged from tier 3b: Hujark hostile, no English, an English escort, the capture quest

**02 Clan of the Hand A or 04 Clan of the Skull B**

- [ ] `HW1` (qa.md:6205) **NEW** [eyes + save] where: Clan of the Hand or Skull, first visit, fighting the Hujark | steps: Arrive | pass: The log says the acolytes are chanting a ward over their warriors. Warriors are harder to hit while acolytes live | new: True
- [ ] `HW2` (qa.md:6206) **NEW** [eyes + save] where: The same | steps: Kill every acolyte on the map | pass: The log says the ward breaks, and within seconds the warriors are as easy to hit as before | new: True

**02 or 03**

- [ ] `HJ3` (qa.md:6333) where: **The war.** HJ2, stand back on 02 or 03 | steps: Watch | pass: English and Hujark fight each other without you

**02, 03 Tourniquet of Pain, 04**

- [ ] `HJ2` (qa.md:6332) [eyes + save] where: HJ1, walk on to `02`, `03` and `04` | steps: - | pass: No Hujark attacks you. `03 Tourniquet of Pain` is the map that failed most

**02, 03, 04, 08, 09, 10 (escort)**

- [ ] `NO72` (qa.md:1477) where: **A save that has never entered act 5.** Side with Huko, then enter `02`, `03`, `04`, `08`, `09` and `10` in turn | steps: - | pass: A Hujark soldier is standing with you on each, and about a second and a half after you land he calls the stage of the advance -- *"Thank you for your help!"*, then *"You must get to the Seer before the Druids do!"*, and so on to *"Protect the Seer!"*. **Twelve of these lines have never played**
- [ ] `NO73` (qa.md:1478) where: NO72: watch what the escort does | steps: - | pass: He fights the English and **never the player**. An escort swinging at you is the bug to report
- [ ] `NO74` (qa.md:1479) where: Side with the English instead, then cross the same six maps | steps: - | pass: An English soldier escorts you and calls the English series -- *"We must bring the savages to their knees!"* through *"Hurry! We have almost broken through."*
- [ ] `NO75` (qa.md:1480) where: Never commit to either side, then cross those maps | steps: - | pass: Neither escort appears and no line plays. Both ship inactive
- [ ] `NO76` (qa.md:1481) where: Re-enter any of the six maps after hearing its line | steps: - | pass: No repeat. `the advance has been called` holds it per map
- [ ] `NO77` (qa.md:1482) where: NO72 and NO74: confirm you only ever hear one side's line on a map | steps: - | pass: The Hujark line if you sided with Huko, the English line if you sided against him, never both

**02, 04, 08, 09, 10 (summoners and shamans)**

- [ ] `NO67` (qa.md:1472) where: Wound a **shaman** past half health on `08 Cave 3`, `09 Cave 4` or `10 Cave 5` | steps: - | pass: A snake erupts beside it. Those three maps carried the checker and the clone source and had nothing to trigger them
- [ ] `NO68` (qa.md:1473) where: NO67 while carrying **Sahar's ring** | steps: - | pass: No snake, and the *"nothing comes up out of it"* line once per map. Shamans are gated exactly as the swordsmen are
- [ ] `NO69` (qa.md:1474) where: Wound a **Snakebreed Summoner** to a quarter health on `02 Clan of the Hand A` or `04 Clan of the Skull B` | steps: - | pass: It calls in something much worse than a snake -- a Mongol archer or an ogre for a weak party, up to a **Rock Titan** for a strong one
- [ ] `NO70` (qa.md:1475) where: NO69 while carrying **Sahar's ring** | steps: - | pass: It still summons. The ring stops serpents, not rock titans. **If the ring silences the summoners too, the gate has been put in the wrong place**
- [ ] `NO71` (qa.md:1476) where: Kill a summoner outright from above a quarter health | steps: - | pass: Nothing. The trigger is a crossing below 25%

**03 Tourniquet of Pain**

- [ ] `NO81` (qa.md:1486) where: NO80 on `03 Tourniquet of Pain` specifically | steps: - | pass: The map is **full of English**. It has no cave fauna at all, so if the English are not coming on, this is the map that will be empty and the whole design has failed

**05**

- [ ] `HJ5` (qa.md:6335) where: **The seer.** Ally, reach `05`, kill the Assassin and the English guard only | steps: - | pass: You can talk to Nostradamus **without touching the shaman or the Hujark guard**

**05 (the seer)**

- [ ] `EF6` (qa.md:6323) who: Ally with Huko and reach the seer | steps: - | pass: *"Thank you! Now quickly come with me."* now appears over the shaman

**05 Nostrodomus Demesne**

- [ ] `NO9` (qa.md:1414) [save] where: After NO5 or NO6, reach `05 Nostrodomus Demesne` | steps: - | pass: The active quest completes on arrival. **In vanilla this completion fired against a quest that had never been activated**
- [ ] `NO28` (qa.md:1433) where: Side with Huko (NO5), then fight through to `05 Nostrodomus Demesne` | steps: - | pass: After the arrival cutscene the assassin attacks **alone**. The Hujark Shaman says *"The Seer has been expecting you. You may enter now."*, the guard follows with *"Thank you! Now quickly come with me."*
- [ ] `NO29` (qa.md:1434) where: NO28, then stand around for twelve seconds without entering | steps: - | pass: The shaman adds *"Do not keep the Seer waiting."*
- [ ] `NO30` (qa.md:1435) where: Reach the Demesne having sided with the **English** (NO6/NO8) | steps: - | pass: Vanilla behaviour exactly: assassin, then the shaman 1.5s later, then the guard, all hostile
- [ ] `NO31` (qa.md:1436) where: Reach the Demesne having **never met Huko** | steps: - | pass: Same as NO30. The checker is off unless the Hujark flag fired
- [ ] `NO32` (qa.md:1437) [save] where: NO28, then check the journal | steps: - | pass: Only *Protect Nostradamus from the invading English forces* should be active -- confirm siding with the Hujark has not also activated the English quest
- [ ] `NO82` (qa.md:1487) where: NO80, then reach the Demesne | steps: - | pass: The shaman stands aside and says the Seer has been expecting you, exactly as for an ally. Huko's word covers his own men all the way to the door

**05 Nostrodomus Demesne (Nostradamus)**

- [ ] `NO41` (qa.md:1446) where: **A save that has never entered act 5.** Reach Nostradamus and hit him once | steps: - | pass: He opens `30 Combat` -- *"Fool, you cannot fight your fate"* -- then taunts with `1001 Goto combat`, and four seconds later starts casting lightning at you from across the room. **In the shipped game he stood there and took it**
- [ ] `NO42` (qa.md:1447) where: NO41, then hit him again several times | steps: - | pass: No repeat of the opening conversation. The `the seer has laughed once` checker holds it
- [ ] `NO43` (qa.md:1448) where: NO41, then kill him | steps: - | pass: *"I have already transcended this mortal coil... Your failure has been foreseen."* and then the portal opens as it always did
- [ ] `NO44` (qa.md:1449) where: Talk to him without ever attacking | steps: - | pass: No combat, no taunt. The whole thread hangs off the first blow
- [ ] `NO45` (qa.md:1450) where: Ask him **"The Hujark call you their Prophet. What are you to them?"** | steps: - | pass: `10 Nostradamus`: *"To the Hujark, I am a prophet... But I was not always like this."* Offered from both `5 questions` and `3 Return Dialog`, and **never reachable before**
- [ ] `NO46` (qa.md:1451) where: Ask *"What are you?"* as well | steps: - | pass: Still `35 Prophet` -> `35 prophet 2` -> `45 element of prophecy`, unchanged
- [ ] `NO47` (qa.md:1452) where: From `70 dangers`, take *"Tell me about the Betrayer."* and *"Tell me about the serpent."* | steps: - | pass: `70 Betrayer` and `100 Dragon Prophecy`. These were spelled in lowercase in vanilla; if they worked before they still work, and if they did not they do now
- [ ] `NO48` (qa.md:1453) where: NO41 while **sided with the Hujark** (NO28) | steps: - | pass: The shaman and guard stood aside at the door, and the seer still defends himself. Confirm attacking him does not un-pacify the Hujark
- [ ] `NO58` (qa.md:1463) where: Reach `45 element of prophecy` with each of the three spirits | steps: - | pass: Ancestral -> `46 the crowded joining`; Beastial -> `47 the unspeaking joining`; Demonic -> `48 the burning joining`. **Exactly one of the three should ever be offered**, and act 5 has never had a spirit check
- [ ] `NO59` (qa.md:1464) where: NO58, then take each route out | steps: - | pass: `60 visions`, `5 questions`, and goodbye. No dead ends
- [ ] `NO83` (qa.md:1488) where: NO80, then ask Nostradamus *"I took no side to get in here. Does that show, in your visions?"* | steps: - | pass: `49 the one who owed nobody`. Offered only while the safe conduct holds
- [ ] `NO93` (qa.md:1498) where: Ask the seer his questions with **Divine 80+**, then **Thought 80+** | steps: - | pass: `51 the church would burn you` and `52 what you are becoming`. Each offered only to its own specialist
- [ ] `NO94` (qa.md:1499) where: The same carrying the **Necromancer** title | steps: - | pass: `53 the same trade`: *"The difference is not skill and it is certainly not mercy. It is that I asked."*
- [ ] `NO95` (qa.md:1500) where: Ask him about his visions carrying **Stargazer** | steps: - | pass: `54 the stars you read`. This perk is read in exactly one other place in the game
- [ ] `NO96` (qa.md:1501) where: Reach the seer with none of those four | steps: - | pass: None of the four replies is offered and his conversation is exactly as vanilla left it

**06 Cave 1**

- [ ] `NO37` (qa.md:1442) where: NO34 on `06 Cave 1` | steps: - | pass: Unchanged -- that map fields no Hujark, only the apprentice set-piece and fauna

**06 Cave 1 / 02 Clan of the Hand A**

- [ ] `NO65` (qa.md:1470) where: **A save that has never entered act 5.** On `06 Cave 1`, let the Frightened Apprentice flee, then go to `02 Clan of the Hand A` | steps: - | pass: He is there, as he always was. That path is unchanged
- [ ] `NO66` (qa.md:1471) [eyes + save] where: NO65 but **kill him on Cave 1**, then go to `02 Clan of the Hand A` | steps: - | pass: He is **not** there. In the shipped game he was waiting on the next map having just died in front of you

**07 Cave 2 / 09 Cave 4**

- [ ] `NO54` (qa.md:1459) where: Enter `07 Cave 2` from either direction | steps: - | pass: *"The passage narrows and keeps narrowing..."* -- **once**, then never again on that save
- [ ] `NO55` (qa.md:1460) where: Reach the far end of `07 Cave 2` where the loot is | steps: - | pass: *"The crack ends. Whatever the Hujark wanted out of this cave they stopped wanting some time ago..."*
- [ ] `NO56` (qa.md:1461) where: Enter `09 Cave 4`, then find the `Hidden Treasure` | steps: - | pass: *"A store cave, or it was..."* on arrival, and at the cache *"Somebody hid this and did not come back for it."*
- [ ] `NO57` (qa.md:1462) where: Re-enter either cave a second time | steps: - | pass: No repeat of the arrival line

**10 Cave 5**

- [ ] `BW1` (qa.md:2364) [eyes + save] step: **New character, never been to act 5's caves.** Reach `10 Cave 5` and find the Hidden Treasure | say: - | expect: It yields the **Bow of Fiery Smite**, not a random item, and still awards **50 XP**
- [ ] `BW2` (qa.md:2365) step: **The row that proves it is still a secret.** Walk past the spot without searching | say: - | expect: Nothing appears. It is a `CAISecretReveal` and must still require detection, not be lying on the floor
- [ ] `BW4` (qa.md:2367) [save] step: The combat text when it is found | say: - | expect: Still "You have found an item buried at the base of the pole." The line was deliberately not rewritten, because it is as true of a bow as of anything else

**10 Cave 5; Chamber of Torment (act 8)**

- [ ] `BW9` (qa.md:2372) step: **Regression, the one that would be expensive to miss.** In `10 Cave 5`, check the act 5 quest content still works, and in the Chamber of Torment check the Knight of Saladin escort still appears | say: - | expect: Both intact. Each map already carried Fixt work, 2,227 changed lines and 164, and the swap had to layer on top of it rather than revert it

**Caverns of Nostradamus**

- [ ] `NQ5` (qa.md:2703) [save] step: Go to the Caverns and finish the act | say: - | expect: The quest completes and pays its experience on arrival at Nostradamus' demesne, as before

**Clan of the Hand / Skull maps**

- [ ] `HW3` (qa.md:6207) **NEW** [eyes + save] where: The same, on the Hujark alliance or safe conduct | steps: Walk through | pass: Nothing changes: the warriors are not hostile, and no English invader is warded on any route | new: True

**English in Caverns of Nostrodomus**

- [ ] `EH15` (qa.md:4483) step: Fight the **Nostradamus Priests** in act 5 (`English in Caverns of Nostrodomus`) | say: - | expect: **No healing.** A separate can family that casts the plain `Magical Shield` and rotates six selections rather than four; it needs its own pass rather than the same edit

**Heart Entrance, 02 Clan of the Hand A**

- [ ] `NO20` (qa.md:1425) where: **Carrying Sahar's ring**, enter act 5 and wound a helmeted swordsman past half health | steps: - | pass: No snake. Instead, once per map: *"The Hujark strikes the floor with the flat of his blade and calls... Nothing comes up out of it."*
- [ ] `NO21` (qa.md:1426) where: NO20, then wound a second and third helmeted swordsman on the same map | steps: - | pass: No snake and **no repeat of the line** -- `the mark has been read` holds it after the first
- [ ] `NO22` (qa.md:1427) where: NO20, then cross into `02 Clan of the Hand A` and wound a helmeted swordsman | steps: - | pass: The line plays once there too. The mark is set on all five summoning maps from the Heart Entrance, through `COtherMapAction`
- [ ] `NO23` (qa.md:1428) where: Enter act 5 **without** the ring | steps: - | pass: Snakes as in NO12. This is the path that must stay unchanged
- [ ] `NO24` (qa.md:1429) where: Sell or drop the ring before entering act 5, then enter | steps: - | pass: Snakes. The check is made on arrival at the Heart Entrance, so what matters is what you are carrying when you walk in
- [ ] `NO25` (qa.md:1430) where: Enter act 5 with the ring, having **killed** Sahar rather than taken her word | steps: - | pass: Not reachable: the ring is only given at `50 her word`. Worth confirming there is no other source

**Heart Entrance, 02, 03, 04, 07 Cave 2**

- [ ] `NO12` (qa.md:1417) where: **A save that has never entered act 5.** Fight the Hujark on the Heart Entrance and wound a **helmeted** swordsman past half health | steps: - | pass: A snake erupts from the floor within about 75 units of him and joins the fight. **This is the whole of tier 2: if no snake ever appears, the clone is not resolving `$Trigger` and the act simply fights as it always did**
- [ ] `NO13` (qa.md:1418) where: NO12 on `02 Clan of the Hand A`, `03 Tourniquet of Pain`, `04 Clan of the Skull B` and `07 Cave 2` | steps: - | pass: The same. 03 has the most summoners of any map (13 generators)
- [ ] `NO14` (qa.md:1419) where: Wound an **unhelmeted** swordsman, a shaman, or a snakebreed past half health | steps: - | pass: Nothing. Only shield-helmet swordsmen summon
- [ ] `NO15` (qa.md:1420) where: Wound **Huko's guard** past half health during the opening conversation | steps: - | pass: Nothing -- he is a named character and was deliberately excluded. A snake appearing mid-conversation would be the bug
- [ ] `NO16` (qa.md:1421) where: Kill a helmeted swordsman in one blow from full health | steps: - | pass: No snake: the trigger is a crossing below 50%, not a death
- [ ] `NO17` (qa.md:1422) where: Let the same swordsman summon, then check he does not summon again | steps: - | pass: One snake per swordsman per crossing
- [ ] `NO18` (qa.md:1423) where: Watch the party level a snake is summoned at | steps: - | pass: `Snakebreed Venom` for a weak party, `Venom Tough` for a stronger one -- the source generator's four `Max Party Mojo` groups should still scale
- [ ] `NO19` (qa.md:1424) where: **Balance read.** Cross a whole map fighting normally and count the snakes | steps: - | pass: If the act feels longer rather than more varied, the fix is one number (`Constant Value=50`) or one checker per map. Record which map felt worst

**any act 5 map**

- [ ] `NO84` (qa.md:1489) where: NO80, then **strike any Hujark** | steps: - | pass: He fights back, and from then on every Hujark that spawns is hostile again -- on this map **and the next one**. The reply NO83 unlocks should also stop being offered
- [ ] `NO85` (qa.md:1490) where: Side with Huko normally (NO5), then strike one of his men | steps: - | pass: The same revocation. Siding with him and then cutting his men down has to cost the alliance

**any act 5 map (traps)**

- [ ] `NO49` (qa.md:1454) where: **A save that has never entered act 5**, with a **low** Find Traps / Lockpick skill. Cross any map | steps: - | pass: Traps fire: a fire circle, an electrical burst or an ice ring, then damage scaled by Mojo. **Act 5 has never had a trap of any kind**
- [ ] `NO50` (qa.md:1455) where: The same ground with **Lockpick Disarm Traps at 50 or better** | steps: - | pass: The trap is spotted before it fires, and can be disarmed for 250 XP. Below 50 on the disarm attempt: *"The mechanism is beyond you"*
- [ ] `NO51` (qa.md:1456) where: Walk back over a trap that has already fired | steps: - | pass: Nothing. `Trigger Only Once=1`
- [ ] `NO52` (qa.md:1457) where: Count traps per map against the table in the notes | steps: - | pass: 43 across ten maps, heaviest on `02` (6). If a trap seems to be inside rock or unreachable, report the map and rough position -- they are placed on monster spawn points, which should all be walkable
- [ ] `NO53` (qa.md:1458) where: Compare trap damage against a Mojo-30 and a Mojo-15 character | steps: - | pass: 30-45 versus 15-25. The first cut of this tier shipped the Crypt's weaker numbers by mistake; these should be the higher ones

**anywhere in the act**

- [ ] `HJ4` (qa.md:6334) where: Hit an allied Hujark | steps: - | pass: He turns on you, as before. Note whether the rest do
- [ ] `HJ6` (qa.md:6336) [eyes + save] where: **Safe conduct**, Speech 75 | steps: Walk the whole act | pass: Same as HJ1, HJ2 and HJ5
- [ ] `HJ7` (qa.md:6337) where: **The regression.** Ignore Huko, or fight him | steps: Walk the act | pass: Hujark attack as always. No English appear
- [ ] `HJ8` (qa.md:6338) where: **Judgement.** Compare a full walk on the ally route with the ignore route | steps: - | pass: The ally route should now feel like choosing a side. Note if the two armies leave too little to do, or too much -- *Judgement row.*

## 6 Barcelona Attack (120)


**Blacksmith map**

- [ ] `BA7` (qa.md:5825) step: **A save that has never entered act 6.** Find the blacksmith during the siege and ask where Galileo and Leonardo are | say: *"Where are Galileo and Leonardo? Their workshops are open to the street."* | expect: He puts the hammer down and says they were taken west with a guard who had a list. **Find Galileo and DaVinci** enters the journal -- a quest that shipped with a blank name and no states
- [ ] `BA8` (qa.md:5826) [eyes + save] step: BA7, then check the journal | say: - | expect: One entry, one state. Not an empty or unnamed quest line
- [ ] `BA13` (qa.md:5831) step: Ask the blacksmith for supplies as before | say: - | expect: His vendor path is unchanged, and his three recorded voice-over lines still play
- [ ] `BA48` (qa.md:5875) step: As a Templar, then as an Inquisitor, talk to the blacksmith | say: - | expect: Both get `30 the orders` -- what the two orders lost in the district
- [ ] `BA49` (qa.md:5876) step: As a Feralkin or Sylvant, talk to the blacksmith | say: - | expect: `40 no flinching`. He has no attention left for a tainted face today
- [ ] `BA50` (qa.md:5877) step: Holding **Slayer of Innocents** (BA22), talk to the blacksmith | say: - | expect: `50 the reports`. He sells to you and tells you not to come back after the city is standing
- [ ] `BA51` (qa.md:5878) step: As a plain human with no order and no title | say: - | expect: None of the three appear, and his vanilla replies are unchanged

**Church Crypt Interior Siege**

- [ ] `BA52` (qa.md:5879) step: Enter `Church Crypt Interior Siege` and look around | say: - | expect: Hover lines for the room and for one slab in the wall. **This map had thirteen parts and nothing to do**
- [ ] `BA53` (qa.md:5880) step: Walk toward the chest at 560,600 without any Traps skill | say: - | expect: Poison gas, 25-40, once
- [ ] `BA54` (qa.md:5881) step: The same with Traps/Perception enough to spot it (`Skill Adjustment=10`) | say: - | expect: The trap is revealed and can be disarmed at Lockpick 40
- [ ] `BA55` (qa.md:5882) step: Open the chest behind it | say: - | expect: Locked at -40. The sacristan's plate
- [ ] `BA56` (qa.md:5883) step: Use the dead guard on the stair | say: - | expect: A line about his sword and which way his feet are pointing

**Crossroads Siege**

- [ ] `EH9` (qa.md:4477) step: `Crossroads Siege` -- where the nearest soldier generator is **308** away, beyond the radius | say: - | expect: The Priest heals **only itself**. Expected, not a bug: 7 of the 24 Priest placements are out of reach of anyone else
- [ ] `MN1` (qa.md:4559) where: **Crossroads Siege**, as a mage, on a save that has **never entered act 6** | steps: Fight the siege normally and do not go out of your way to hunt pickups | pass: You run dry **noticeably less** than before. This is the row the whole change exists for, and it is a feel question -- report whether it still runs out, not whether you saw the orbs
- [ ] `MN2` (qa.md:4560) where: The same map, same character | steps: Count roughly how often a spirit orb is within reach of a fight | pass: Mana now appears **where the fighting is**, because every new fount sits inside an enemy spawn area. If orbs feel like they are in empty ground instead, say so
- [ ] `MN6` (qa.md:4564) where: Any new orb | steps: Walk over it | pass: It is picked up and credits mana like any other. The blocks are copies of vanilla's own fount, so a difference here means the template is wrong
- [ ] `MN7` (qa.md:4565) where: Watch for an orb inside a wall or on unreachable ground | steps: - | pass: None. Placement is inside generator ovals only, but *walkable is not reachable* -- if one is stranded behind geometry, report the map and roughly where
- [ ] `MN8` (qa.md:4566) where: Two orbs stacked on the same spot | steps: - | pass: None. All 36 positions are distinct and checked against the existing founts
- [ ] `MN9` (qa.md:4567) where: A **melee** character through Crossroads Siege | steps: - | pass: No worse than before. Nothing was removed and no enemy changed; the only risk is orbs cluttering a fight visually
- [ ] `BA14` (qa.md:5832) step: **A save that has never entered act 6.** Cross from `Gate District Siege` into `Crossroads Siege` | say: - | expect: About a second after landing: *"The crossroads is not a crossroads any more..."* **This map had no balloon, no conversation and no dialogue tree at all**
- [ ] `BA16` (qa.md:5834) step: Reach the road to England at the western end | say: - | expect: *"The road west, and the ruts in it are fresh..."*
- [ ] `BA17` (qa.md:5835) step: BA16 **without** having asked the blacksmith (BA7) | say: - | expect: The plain line, and no XP. The evidence is what the blacksmith's answer turns the ruts into
- [ ] `BA18` (qa.md:5836) [eyes + save] step: BA16 **after** BA7, with *Find Galileo and DaVinci* active | say: - | expect: The longer line -- the cracked lens and the wax tablet -- and **1500 XP, once**
- [ ] `BA19` (qa.md:5837) [eyes + save] step: Walk back over the western end again | say: - | expect: No repeat and no second payment
- [ ] `BA20` (qa.md:5838) step: Fight anywhere on the map for a minute | say: - | expect: English soldiers shout: *"Press forward, men!"*, *"Attack! For England!"*, *"For the Queen!"* Six of the thirty-four generators are armed
- [ ] `BA21` (qa.md:5839) step: Compare the volume against `Gate District Siege` (BA4) | say: - | expect: Similar. This map has no defenders, so only the English are heard
- [ ] `XS22` (qa.md:6277) where: Crossroads Siege, on a save that has not entered it | steps: Walk the road to the junction | pass: The stand is at the junction just west of the catapult rocks, whole, and nothing is drawn over it. You can walk up to it from the road and click it. The description fires as you approach -- *Needs a save that has not entered Crossroads Siege.*
- [ ] `XS23` (qa.md:6278) where: The same, with Jehanne or the golem, and soldiers still alive around you | steps: Take that route | pass: They reach the base of the stand before they die. If frozen men block them, the 12 second timer still ends the scene
- [ ] `XS2` (qa.md:6288) where: Click it, with none of the routes | steps: - | pass: The description and only *<Leave it.>*
- [ ] `XS3` (qa.md:6289) [eyes + save] where: Thought 150 | steps: *<Obliterate it.>* and click on | pass: Fire, lightning, ice, shake. **All mana gone, about half your health.** The standard vanishes and a burn mark stands in its place
- [ ] `XS3a` (qa.md:6290) [eyes + save] where: The same | steps: Compare your mana before and after | pass: It is **zero**. 0.98.0's first draft took nothing, because a take larger than the pool fails
- [ ] `XS4` (qa.md:6291) [eyes + save] where: **The row this exists for.** After any route | steps: Stand among the soldiers | pass: **Every English soldier stops attacking** and you can walk through. Stay among them for a minute, near bowmen and near melee men: barks keep coming from individual soldiers on screen, *"This is Spain..."*, and they keep coming as you walk Druids, golems and wolves still attack. If soldiers keep swinging, the names or the pacify failed
- [ ] `XS5` (qa.md:6292) [eyes + save] where: Divine 150, Tribal 150, and ST 10 with EN 8 | steps: Each in turn | pass: Each with its own text and effects. Brute force takes about two thirds of your health and no mana
- [ ] `XS6` (qa.md:6293) [eyes + save] where: Joan with you | steps: *<Look to Jehanne.>*, *Do it.* | pass: She **walks to the standard** before the light takes her, her body stays there, the soldiers wake, and the ending shows `900 friend joan standard`. **Refusing keeps her** and the standard stands
- [ ] `XS6a` (qa.md:6294) where: **The cutscene.** XS6 or XS7, in the thick of the fight | steps: - | pass: **Nothing moves but the one walking, and you take no damage.** The camera follows them to the standard and holds on the body, then returns to you with your controls back. **If you are left unable to move, that is the bug this row exists for**
- [ ] `XS7` (qa.md:6295) [eyes + save] where: War Golem with you | steps: *<Order the golem to destroy it.>* | pass: It **walks to the standard**, then explodes, and the ending shows `900 friend golem standard`
- [ ] `XS8` (qa.md:6296) where: **Wounded.** At 60% health, and again below 25%, any route | steps: - | pass: You survive it, and **nothing hits you during the scene**. Controls come back afterwards
- [ ] `XS9` (qa.md:6297) where: **Judgement.** A mage at the Siege | steps: What is your level, and your school total? | pass: Is 150 a main school rather than a hybrid? -- *Judgement row.*
- [ ] `XS11` (qa.md:6299) [eyes + save] where: **The price.** After any route | steps: Attack one woken soldier in melee, then one with a bow or spell | pass: He alone fights back in **both** cases. The rest stand. **Karma falls by 50 per kill.** XP and the drop still arrive
- [ ] `XS21` (qa.md:6306) where: **Waking.** Stand among soldiers and break the standard | steps: - | pass: Within about three seconds of the scene ending, every man in view says a bewildered line once, not all in the same instant, with none of them in the log. After that it settles to the occasional line
- [ ] `XS20` (qa.md:6307) where: **The stand.** Find it at the crossroads before breaking it | steps: - | pass: A dark twisted druid lamp-stand, whole and fully visible with nothing drawn over it, and the opening text calls it a lamp-stand. The charm effect pulses at its lamps every four to six seconds, silently, and stops the moment it breaks. After it falls the burn scar sits under where its base was, and sacrifices walk to its base -- *Find it at the junction per 0.98.1, not the 0.98.0 spot.*
- [ ] `XS19` (qa.md:6308) where: **Talking to them.** After the standard breaks, hover and click several English soldiers. Then force attack one | steps: - | pass: The cursor shows talk, not attack, on a man you have not hit. The player walks up and he says one of the eight waking lines over his own head. Force attack still works. A soldier you have damaged fights back. Your attack stops after that first hit, and one more click on him then attacks continuously as normal, without stopping at each swing
- [ ] `XS14` (qa.md:6309) [eyes + save] where: **Save and reload.** Save just after the break, reload, leave the map and return | steps: - | pass: Soldiers stay stood down. If barks stop after a reload that is minor; note it. Karma and the slide flag survive

**Crossroads to England**

- [ ] `DF1` (qa.md:2949) step: Leave the Crossroads siege, cross the road map and walk up to the portal at the far side | say: - | expect: Your spirit's summoning effect plays, the spirit appears beside you, and your controls lock
- [ ] `DF2` (qa.md:2950) step: Listen | say: - | expect: The finale, **with voiceover**, in your own spirit's register. Beast: *"Now the wolf has shed its false coat"*. Demonic: *"...placing the world in *check*. Perhaps we should pursue with haste before he declares *mate*"*. Elemental: *"Now our *true* adversary has moved against us directly"*
- [ ] `DF3` (qa.md:2951) step: **The row that matters most.** Take any reply through to its end | say: - | expect: The spirit plays its disappear animation and **your controls come back**. This scene runs inside a non-interactive sequence and four of its exits ended nothing
- [ ] `DF4` (qa.md:2952) step: Elemental only: take *"Do you know the identity of our adversary?"* | say: - | expect: Two more nodes, the Daeva and the Disjunction, then three karma replies
- [ ] `DF5` (qa.md:2953) step: Elemental only: from there take *"Agreed, we must pursue our enemy and recover the relics."* | say: - | expect: *"Your valor inspires strength and hope within me, rivaling even King Richard's courage."* Vanilla pointed this reply at a node that does not exist in that tree
- [ ] `DF6` (qa.md:2954) step: Beast only: take *"Agreed, we must pursue our enemy and recover the relics."* | say: - | expect: *"Let us continue our hunt for the truth."* **Not** *"Be wary! Such instincts have led many to ruin"*, which is what both replies used to fire
- [ ] `DF7` (qa.md:2955) step: After the scene, walk out of the area and back to the portal | say: - | expect: Nothing fires a second time
- [ ] `DF8` (qa.md:2956) step: Click the portal | say: - | expect: You relocate to the English Shrine as before
- [ ] `DF10` (qa.md:2958) [save] step: **Regression.** Check your quest log on that road | say: - | expect: *"The Druid force is falling back west through the crossroads, and the True Cross is going with them. Follow it."* unchanged from 0.32.0
- [ ] `MN3` (qa.md:4561) [eyes + save] where: **Crossroads to England map** | steps: Walk it end to end | pass: Eight founts rather than one. This map had the worst ratio in the act at 1.2 mana per spawn

**Crossroads to England map**

- [ ] `ES54` (qa.md:5740) step: Carrying **Servant of the Queen** from act 1, talk to Surrey O'Connell at `Crossroads to England map` | say: - | expect: A third reply, about the service the Queen set her hand to. He goes cold: *"Do not say my name where anybody writes things down."* -- *Needs Servant of the Queen from act 1.*
- [ ] `ES55` (qa.md:5741) step: Open the Regent's chest after ES54 | say: - | expect: No shout, no guards. Same outcome as the clover and the Holy Office -- all three set `Surrey looks away`
- [ ] `ES56` (qa.md:5742) step: Tell him *"You have nothing to fear from me, Surrey."* | say: - | expect: *"No. No, I have not, and I have not from the last four either, and here I still am weighin' out bolts on the wrong road."*
- [ ] `ES57` (qa.md:5743) step: Carrying the clover **and** the title | say: - | expect: Both replies offered. They are different reasons, not ranked alternatives; either works
- [ ] `ES58` (qa.md:5744) step: Carrying neither, and no Inquisitor rank | say: - | expect: Only his vanilla replies plus the PE 8 and Speech 70 routes. Unchanged
- [ ] `BA9` (qa.md:5827) [eyes + save] step: Reach `Crossroads to England map` | say: - | expect: **Pursue the Retreating Druid Forces and Recover the True Cross** enters the journal about a second after you land
- [ ] `BA10` (qa.md:5828) [eyes + save] step: Leave and re-enter that map | say: - | expect: No second copy of the entry. `the pursuit has been called` holds it
- [ ] `BA43` (qa.md:5870) step: **A save that has never entered act 6**, carrying the Clover from the Port District Irish sailor. Talk to Surrey O'Connell | say: - | expect: A new reply offering the clover. He stops grovelling and tells you to take what you need off the Regent's pile
- [ ] `BA44` (qa.md:5871) step: BA43, then open the Regent's chest | say: - | expect: **No shout, no guards, and Surrey stays friendly.** In vanilla only Sneak 100 avoided the alarm
- [ ] `BA45` (qa.md:5872) step: The same without the clover and without Sneak 100 | say: - | expect: He shouts *"That's the Regent's loot!"*, the `chest guards generator` wakes and he turns on you -- unchanged
- [ ] `BA46` (qa.md:5873) step: As a sworn Inquisitor, talk to Surrey | say: - | expect: *"The Spanish -- no. No, guvna', I never --"* and the same look-away
- [ ] `CO1` (qa.md:6213) **NEW** [eyes + save] where: Crossroads to England, having broken the standard, on a save that has not walked the road | steps: Walk it | pass: Two archer groups do not attack. Clicking one gives a deserter line. Without the standard broken they fight as before | new: True
- [ ] `SH9` (qa.md:6259) **NEW** [eyes + save] where: Crossroads to England | steps: - | pass: Three of the archer pairs are druids | new: True

**Gate District Siege**

- [ ] `MN4` (qa.md:4562) where: **Gate District Siege** | steps: Play it | pass: **Unchanged.** 19 founts, 1,077 mana. If this map feels different, something leaked and the change is wrong
- [ ] `BA1` (qa.md:5819) step: **A save that has never entered act 6.** Stand in the fighting on `Gate District Siege` for a minute | say: - | expect: Both sides shout. Spaniards: *"To Hell with these accursed druids!"*, *"God save Barcelona!"*; English: *"Attack! For England!"*, *"For the Queen!"* **Nineteen lines across three trees, none of which has ever played**
- [ ] `BA3` (qa.md:5821) step: Watch where the balloons appear | say: - | expect: Over the soldiers themselves, not over the player. They position on `$Trigger`
- [ ] `BA4` (qa.md:5822) step: Listen for about a minute on either map | say: - | expect: Roughly one line per armed soldier every eight seconds, plus a steadier defender line every twenty-four. **If it reads as a wall of text, the count to reduce is the six-per-side cap** -- *Judgement row on volume.*
- [ ] `BA5` (qa.md:5823) step: Listen for the steadier defender lines specifically | say: - | expect: *"We must remain vigilant."*, *"The gall of these druids!"*, *"Spain is too powerful for the druids!"* One of the six is *"I'll secure this area."*, which can land mid-fight -- known, and noted in the release
- [ ] `BA6` (qa.md:5824) step: Kill every English soldier near an armed defender | say: - | expect: The defender keeps talking. There is no end-of-fight event on these maps, so the lines are timed rather than triggered
- [ ] `BA27` (qa.md:5854) step: **Without** the title, enter `Gate District Siege` and talk to the man calling for Phillipe | say: - | expect: He asks you to look for a boy in a red cap. **Vanilla gave every player the accusation instead**
- [ ] `BA28` (qa.md:5855) step: **With** the title, do the same | say: - | expect: *"Leave me alone! Haven't you done enough?!"* -- the shipped line, now on the shipped condition
- [ ] `BA29` (qa.md:5856) step: Walk past him without talking | say: - | expect: The old polygon bark still fires: *"Phillipe! Where are you?!"*
- [ ] `BA30` (qa.md:5857) step: Find Phillipe around 2694,1251, behind a barrel, **before** speaking to his father | say: - | expect: He talks, but the reply that sends him home is not offered
- [ ] `BA31` (qa.md:5858) [eyes + save] step: Speak to the father first, then find Phillipe | say: - | expect: The reply is offered; he runs; **1000 XP, once**, and a closing line about the man who stops saying one word
- [ ] `BA32` (qa.md:5859) step: Go back to where Phillipe was | say: - | expect: He is gone, and no second payment
- [ ] `BA33` (qa.md:5860) step: **A save that has never entered act 6.** On `Gate District Siege`, find the woman around 2551,1520 and talk to her | say: - | expect: An ordinary Barcelona citizen greeting. **She did not exist; the map's relay was positioning a balloon over her name**
- [ ] `BA34` (qa.md:5861) step: Murder her, or murder the man searching for Phillipe, while she is alive to see it | say: - | expect: *"Ayudame! Help me! Guards!"* and about two seconds later **the whole garrison turns on you**, with a +40% AC buff -- the same consequence vanilla gives for attacking a guard
- [ ] `BA35` (qa.md:5862) step: Murder the man searching for Phillipe **after** killing her | say: - | expect: No scream and no turn. The witness has to be alive
- [ ] `BA36` (qa.md:5863) step: Let the English kill defenders all around you without lifting a hand | say: - | expect: Nothing happens. The scream is armed on civilians only, so the garrison never blames you for the siege
- [ ] `BA37` (qa.md:5864) step: Attack a defender directly, as in vanilla | say: - | expect: The garrison turns, as before. Unchanged
- [ ] `BA38` (qa.md:5865) [eyes + save] step: Find the `Generic Gaurd NPC` body at 1618,845 and use it | say: - | expect: *"Stranger...here...take my gold. Don't let those English have it..."* and **250 gold**, once
- [ ] `BA39` (qa.md:5866) step: Find the `Soldier1` body at 1678,2914 | say: - | expect: *"I am sorry Espana...I do not know why we came with swords drawn and bloodlust in our hearts..."*
- [ ] `SG1` (qa.md:6197) **NEW** [eyes + save] where: Gate District Siege, on a save that has not entered it | steps: Kill every druid priest on the map | pass: Within seconds the English soldiers stop fighting, each says a waking line ("This is Spain. Why am I in Spain?"), and clicking one talks | new: True
- [ ] `SG2` (qa.md:6198) **NEW** [eyes + save] where: The same, after the stand-down | steps: Force attack one soldier | pass: Every English soldier on the map turns hostile again | new: True

**Gate District Siege / Temple District Siege**

- [ ] `EH1` (qa.md:4470) step: **The row the feature exists for.** `Gate District Siege` or `Temple District Siege`, a fight with a **Priest and soldiers together**. Wound a soldier, do not kill it, and watch the Priest | say: - | expect: The soldier's health **goes back up**. This is the first time anything in Lionheart has healed an enemy, and it is the one thing that cannot be proved statically

**Temple District Siege**

- [ ] `MN5` (qa.md:4563) where: **Temple District Siege** | steps: Play it | pass: **Unchanged.** 30 founts, 2,087 mana. Same test as MN4
- [ ] `BA2` (qa.md:5820) step: BA1 on `Temple District Siege` | say: - | expect: The same, quieter -- that map has one defender generator and three attacker generators still standing
- [ ] `BA40` (qa.md:5867) step: On `Temple District Siege`, walk the length of the map using bodies | say: - | expect: Six of them speak, three Spanish and three English, spread west to east. **Vanilla had 62 bodies and zero talkable ones on this map**
- [ ] `BA41` (qa.md:5868) [eyes + save] step: The dying Spaniard on the Temple District | say: - | expect: Also pays 250, once
- [ ] `SG3` (qa.md:6199) **NEW** [eyes + save] where: Temple District Siege | steps: Repeat SG1 and SG2, and check the siege still plays to its end | pass: Same results, and nothing in the siege waits forever on English deaths | new: True

**anywhere in the act**

- [ ] `BF1` (qa.md:3596) where: Act 6 or 7, find ordinary English infantry (`Soldier1`) | steps: Hit one once, then watch it | pass: A visual effect plays over it, and it becomes **more durable** than its unhit companions for about 20 seconds
- [ ] `BF2` (qa.md:3597) where: **The row that proves it.** Any of the seven archetypes | steps: Hit it and watch for the effect over its head | pass: **Something visibly happens.** If no effect ever plays on any archetype, the hook is not firing and nothing else in this section is testable
- [ ] `BF3` (qa.md:3598) where: `Soldier1` again | steps: Keep hitting the same one well past 20 seconds | pass: The buff **does not re-apply**. One per creature, ever
- [ ] `BF4` (qa.md:3599) where: Swordsmen / axemen (`Soldier2`, `Soldier2 Axe`) | steps: Wound one to **below half health** | pass: Only *then* does it buff -- it should hit noticeably harder and faster afterwards, not from the first blow
- [ ] `BF5` (qa.md:3600) where: Same, but kill one quickly from full health | steps: - | pass: It **never** buffs. The trigger is a health threshold, so a fast kill should skip it entirely
- [ ] `BF6` (qa.md:3601) where: English archers (`Soldier2 Bow`) | steps: Hit one once, then back off and let it shoot | pass: It fires **faster** and should hit more often. This is the one buff whose effect is easiest to misread -- watch the rate, not the damage
- [ ] `BF7` (qa.md:3602) where: English priests or priestesses | steps: Hit one once, then let it cast | pass: It casts **faster**. Compare against an unhit one beside it if you can
- [ ] `BF8` (qa.md:3603) where: War golems -- fire, cold or electricity | steps: Wound one below 40% | pass: It buffs, and the effect differs by element: venting, riming, arcing
- [ ] `BF9` (qa.md:3604) where: **The element check.** Bring the matching damage type to a golem -- fire against a fire golem | steps: Wound it below 40%, then keep using that element | pass: It gets **harder to hurt with its own element specifically**, not with everything. If all three golems feel identical, the per-element resistance is not landing
- [ ] `BF10` (qa.md:3605) where: Fight a mixed English group | steps: - | pass: Buffs fire **independently per creature**. One soldier bracing must not brace the others, and must not consume their one-shot
- [ ] `BF11` (qa.md:3606) where: **The timing.** Trigger a buff, then disengage and wait ~30 seconds | steps: Re-engage | pass: The buff has **expired**. These are windows, not permanent upgrades. If it never wears off, the duration is not being applied
- [ ] `BF12` (qa.md:3607) where: Any buffed creature | steps: Let it buff, then check it is not healing | pass: These 36 cans buff and do **not** heal. Healing belongs to the 12 veteran cans only
- [ ] `BF13` (qa.md:3608) where: The two excluded cans | steps: Find `Priest Near Death` and a deactivated war golem | pass: Neither buffs. Both were deliberately left out
- [ ] `BF14` (qa.md:3609) where: **The regression.** Find a veteran soldier from 0.34.0 (`Soldier3` / `Soldier4` lines) | steps: Wound it to 40% health | pass: **It still drinks and heals, exactly as in 0.34.0, and gains no buff.** Those 12 cans were meant to be untouched by this release
- [ ] `BF15` (qa.md:3610) where: **The control.** Fight any non-English enemy -- goblins, undead, thugs | steps: - | pass: Nothing changed anywhere outside the English army
- [ ] `BF16` (qa.md:3611) where: Judge the **feel**, which no check settles | steps: Fight several English groups | pass: Does the army read as reacting to you, or as arbitrarily getting stronger? The two trigger styles were chosen so stiffening-on-contact and escalating-near-death feel different. If they are indistinguishable in play, the triggers want rethinking rather than the numbers
- [ ] `PO10` (qa.md:4385) step: Fight a **mixed group**: a Priest plus veteran soldiers | say: - | expect: The Priest heals them *and* they drink their own draught. That stacking is intended but has never been seen -- if it makes a group unkillable, this is the row that will say so
- [ ] `EH2` (qa.md:4471) step: Fight a Priest **alone** and wound it | say: - | expect: It heals **itself** -- the Priest is `Category=Enemy` like everything else, so it is inside its own oval
- [ ] `EH6` (qa.md:4474) step: Watch a Priest over a long fight and count | say: - | expect: Roughly **one cast in four** is a heal; the other three are Fire Orb, Spike or Lightning Bolt. If healing feels relentless, the bank weighting is the dial -- say so rather than guessing a number
- [ ] `EH7` (qa.md:4475) step: **Does it change how you fight?** Take the same Priest-and-soldiers fight twice: once ignoring the Priest, once killing it first | say: - | expect: Killing the Priest first should be **noticeably better**. That is target priority, and it is the entire point -- the first thing in this game that makes *your* behaviour change rather than the enemy's
- [ ] `EH8` (qa.md:4476) step: Judge the magnitude: about **11-18 HP** per trigger, up to twice per cast | say: - | expect: Enough to matter, not enough to make a soldier unkillable. If it out-paces your damage, the race preset of 150 is the dial
- [ ] `EH11` (qa.md:4479) [eyes + save] step: Kill a Priest and check the drops | say: - | expect: **Unchanged.** `English Priest Drop Action` was not touched; it carries no spirit energy, which is a separate note in the act 6 section
- [ ] `EH12` (qa.md:4480) step: Fight **`Priest Tough`**, then **`Priest Super`** | say: - | expect: Both heal, and **harder**: presets 200 and 250 against the base tier's 150, so roughly **14-22** and **17-26 HP** per trigger. If a Super Priest out-heals your damage outright, that is the row to report and the preset is the dial
- [ ] `EH13` (qa.md:4481) step: Compare the three tiers side by side if you can | say: - | expect: The heal should scale with the tier the same way their shield already does -- the presets are copied from `ENEMY Magical Shield`'s own 150/200/250 ladder on these exact cans, not chosen freshly
- [ ] `EH14` (qa.md:4482) step: Fight **`Priest Near Death`** | say: - | expect: **No healing.** It selects no skill at all in vanilla and is a scripted one-off, so it was left alone
- [ ] `ES28` (qa.md:5795) [save] step: Check your titles after act 6 has failed the conspiracy quest | say: - | expect: **The title survives.** Act 6's bulk quest-fail is `IfActive`, so a completed conspiracy is untouched
- [ ] `BA42` (qa.md:5869) step: Re-use any body that has already spoken | say: - | expect: Nothing. Each specifier is once-only, and no second payment

## 7 English Shrine (104)


**01 Outside Shrine**

- [ ] `SU3` (qa.md:5419) step: Meet Grace O'Malley on the act 7 landing beach and let her fight | say: - | expect: She survives it -- 190 AC, 165 HP, OneHandedMelee 110, Evasion 55, which is what 0.19.0's review intended
- [ ] `AL51` (qa.md:5730) step: Recruit Grace in act 7 and dismiss her on `01 Outside Shrine` | say: - | expect: Unchanged from 0.19.0. Her switch replies are goto-only from the arrival conversation on that map, so they were never at risk
- [ ] `ES38` (qa.md:5757) [eyes + save] step: **A save that has never entered act 7.** After ES37, land at `01 Outside Shrine` | say: - | expect: **Grace is on the beach at 505,639**: *"You have found me! First you spared me in Barcelona and now you have come so far to rescue me."* Her generator shipped inactive, unnamed and with no AI
- [ ] `ES39` (qa.md:5758) step: Ask her about the druids | say: - | expect: *"Once they fought the English with us, but now they have formed an alliance with the Queen."* **The shipped text saying what Sir Roger says in tier 3**
- [ ] `ES40` (qa.md:5763) step: With **Grace's Regard**, accept her in act 7 with *"My dear, your companionship is most welcome."* | say: - | expect: *"Together we cannot fail. My heart and my sword are yours!"* and **she joins as a companion**
- [ ] `ES40a` (qa.md:5764) step: **Without** Grace's Regard, check her act-7 replies | say: - | expect: The romantic acceptance is **not offered**. She still declares herself -- she is voiced and that line is hers -- but the routes left are the sword without the heart, and refusal
- [ ] `ES41` (qa.md:5765) step: Accept with *"Your sword is welcome, but I have no use for your heart."* | say: - | expect: *"I will honor it, and serve you not for love, but for duty."* She joins anyway
- [ ] `ES42` (qa.md:5766) step: Refuse with *"Sorry, I work alone."* | say: - | expect: *"Do not worry - we will not cross paths again."* No companion
- [ ] `ES43` (qa.md:5767) [eyes + save] step: Instead reach act 7 having **driven her off or turned her in to the Duke** | say: - | expect: **She is not on the beach at all.** The shipped `Captain Isabella fled` checker is what act 1 sets in both cases
- [ ] `ES44` (qa.md:5768) step: Instead reach act 7 having **taken her bribe, or lied, or never accused her** | say: - | expect: `500`: *"if I can't kill the English, I will settle the score with you"* -- and she attacks
- [ ] `ES45` (qa.md:5769) step: With her as a companion, talk to her again | say: - | expect: *"Are you ready to continue our quest?"*
- [ ] `ES50` (qa.md:5776) step: Talk to Grace while she is a companion | say: - | expect: *"Are you ready to continue our quest?"* -- **and you should now hear it**, because the node was renamed back to match its recording
- [ ] `ES51` (qa.md:5777) step: Tell her *"Wait here. I will come back for you."* | say: - | expect: *"If that is your desire. I will await your return here."* She stops following
- [ ] `ES52` (qa.md:5778) step: Come back and talk to her | say: - | expect: *"Let us continue our quest."* -- the second renamed recording -- and she rejoins
- [ ] `ES53` (qa.md:5779) step: Check she is not still following after ES51 | say: - | expect: She should stay put until ES52

**02 Temple Initiate**

- [ ] `SN1` (qa.md:5582) [eyes + save] step: At Sneak 25, enter 02 Temple Initiate and open the secret door at the south-west wall | say: - | expect: A balloon about two lines of wear in the flagstones, **250 XP**, the room revealed, the strongbox usable
- [ ] `SN2` (qa.md:5583) step: After SN1, walk to the far end of that room | say: - | expect: A passage that relocates straight to 05 Exalted Chambers, skipping 03 and 04
- [ ] `SN3` (qa.md:5584) step: At Sneak 10-19, open the same door | say: - | expect: Only the draught balloon. No strongbox, no passage
- [ ] `SN4` (qa.md:5585) step: At Sneak 9 or below, open the same door | say: - | expect: Nothing at all, exactly as vanilla
- [ ] `SN9` (qa.md:5591) step: Come back into 02 from 05 the vanilla way, having never passed a Sneak check | say: - | expect: The secret opens on arrival as it always did, and no Fixt balloon plays
- [ ] `ES24` (qa.md:5791) step: Carrying the title, talk to **Sir Roger** in act 7 -- first meeting or any return | say: - | expect: A new reply about the Queen owing you a service. He tells you **the Queen keeps druids**, and that his Order came to the shrine **without her leave**
- [ ] `ES25` (qa.md:5792) step: Press him on it | say: - | expect: *"she will call it hers when it is done, and the men who stopped it will have been brigands."* Both nodes lead into `10 accept`, so it is a way into the alliance
- [ ] `ES26` (qa.md:5793) step: Without the title, check Sir Roger's replies | say: - | expect: The new reply is not offered, on any of his six entry nodes, and everything else is as vanilla
- [ ] `ES27` (qa.md:5794) step: Carrying the title, ask the Templar camp surgeon for healing as a plain human with no order | say: - | expect: Healed free. A servant of the Queen counts as a knight to him
- [ ] `ES9` (qa.md:5796) [eyes + save] step: **A save that has never entered act 7.** Accept Sir Roger's offer of help, then look around the entrance of `02 Temple Initiate` | say: - | expect: A Templar post: a quartermaster, a field surgeon and a guard, around 2820,1300. **Act 7 had no merchant on any of its eleven maps**
- [ ] `ES10` (qa.md:5797) [eyes + save] step: **Refuse** his help instead -- *"I am not interested in help from any Englishman"* -- and look in the same place | say: - | expect: **Nothing there.** No camp, no shop, no surgeon. That reply cost nothing at all before this
- [ ] `ES12` (qa.md:5799) step: Talk to a camp guard | say: - | expect: *"My sword is yours."* **The one dialogue tree in the act that nothing opened**
- [ ] `ES13` (qa.md:5800) step: Buy from the quartermaster with **none** of Quinn's three errands done | say: - | expect: One "Show me what you have" reply. Potions, 40 bolts, 40 arrows, hard leather, a medium shield
- [ ] `ES14` (qa.md:5801) step: The same having done **one or two** of Quinn's errands | say: - | expect: The reply mentions a herbalist who owes you, and the stock adds **Great Healing** potions
- [ ] `ES15` (qa.md:5802) step: The same having done **all three** | say: - | expect: The reply says you did the herbalist some favours, and the stock adds **Superior** and **Supreme Healing** -- the potions 0.4.0 unlocked, six acts earlier
- [ ] `ES16` (qa.md:5803) step: Count the "Show me what you have" replies in any of ES13-ES15 | say: - | expect: **Exactly one, ever.** The first draft would have shown three identical replies to a player who had done all three errands
- [ ] `ES17` (qa.md:5804) step: As a **Templar**, then as a **Knight of Saladin**, ask the surgeon for help | say: - | expect: Healed to full, free. He treats both orders as brothers
- [ ] `ES18` (qa.md:5805) [eyes + save] step: As a sworn **Inquisitor** | say: - | expect: He heals you, and **charges the 200** like anyone else. Deliberate: the Inquisition is Spanish and ecclesiastical, not his brotherhood
- [ ] `ES19` (qa.md:5806) step: With fewer than 200 gold and no order | say: - | expect: The paid reply is not offered
- [ ] `ES20` (qa.md:5807) step: Ask the surgeon how many he has lost, and the quartermaster whose stock it is | say: - | expect: Two answers about the twenty who held the gate. Neither is a shop
- [ ] `TS10` (qa.md:6085) [eyes + save] where: **Act 7, `02 Temple Initiate`.** Meet **Sir Roger Templeton** carrying the Holy Shield, as a Templar | steps: Take the reply that shows him the shield | pass: He speaks the relic line, and *"Then let it be seen raised."* takes the Holy Shield and gives the **Aegis**. He should then recruit normally, exactly as the ordinary Templar greeting does -- *Since 0.93.2 the reply needs the Holy Shield WORN (Fixt Wearing Templar Shield), and he notices it rather than you showing it.*
- [ ] `TS11` (qa.md:6086) where: Same, **without** the Holy Shield, or as a non-Templar | steps: Talk to him | pass: The shield reply is **absent** and the conversation is unchanged in every other respect. Nothing fires -- *Since 0.93.2 'without' means not wearing it.*
- [ ] `TS11b` (qa.md:6087) where: **The cutscene check.** Finish that conversation through the relic branch | steps: - | pass: The scene ends and you regain control. The greeting runs inside a non-interactive sequence, and 0.9.0 soft-locked one for two years with a reply that did not exit properly. **If control is not returned, this release is broken and nothing else matters**
- [ ] `TS11c` (qa.md:6088) [eyes + save] where: Refuse Sir Roger at the greeting, then talk to him again | steps: Take the shield reply on the **return** dialogue | pass: Same result. The branch is on all four greeting nodes, so one refusal must not lose the shield
- [ ] `HN1` (qa.md:6221) **NEW** [eyes + save] where: 02 Temple Initiate, first visit, on a save that has not entered it | steps: Open the journal | pass: Under the druid quest, "The Spellbound Soldiers" says they fight as though spellbound. It tells you nothing to do. With Sir Roger along he says something has hold of them | new: True
- [ ] `SH3` (qa.md:6253) **NEW** where: 02, Sir Roger, Servant of the Queen perk | steps: Reach "The Queen keeps druids" and answer "That changes nothing. Stand aside." | pass: The scene ends and you can move; he can be spoken to again. Before this you were stuck | new: True
- [ ] `SH4` (qa.md:6254) **NEW** [eyes + save] where: 02 at Sneak 25 | steps: Take the second passage, go on to 05, then come back the vanilla way | pass: One payment of the passage XP and balloon, on the way in only | new: True

**02, 03 or 04**

- [ ] `SH7` (qa.md:6257) **NEW** [eyes + save] where: 02, 03 or 04 | steps: Kill every druid on the map, leave the soldiers | pass: Within a few seconds every soldier on that map stops fighting and says one dazed line; clicking one talks. A map with druids alive keeps fighting | new: True
- [ ] `SH8` (qa.md:6258) **NEW** [eyes + save] where: The same, after the stand-down | steps: Force attack one soldier | pass: Every soldier on that map turns hostile again, not just the one; the first hit stops your attack and one more click carries on. No Karma lost | new: True

**02, 03, 04**

- [ ] `SH5` (qa.md:6255) **NEW** [eyes + save] where: 02, 03, 04 | steps: Look at the enemies | pass: Some are druids in robes casting spells, not soldiers standing still until struck. None stands idle while his friends fight | new: True

**03, 04, 05**

- [ ] `SH10` (qa.md:6260) **NEW** where: 03, 04, 05 with Roger and Grace | steps: Enter each map the first time | pass: Each says one line, Roger first. Neither says it twice, and with one of them absent the other still speaks | new: True

**04 Antechamber of Lore**

- [ ] `ES11` (qa.md:5798) [eyes + save] step: Reach `04 Antechamber of Lore` after accepting | say: - | expect: A second post around 5880,1560. It is opened from `02` by a `COtherMapAction`, so it should already be there when you arrive

**05 Exalted Chambers**

- [ ] `PC3` (qa.md:5431) step: Fight a **Priestess Super** in `05 Exalted Chambers` | say: - | expect: Fire Orb, Lightning Bolt, Spike or Static Charge, varying
- [ ] `PC6` (qa.md:5434) step: Judge the Exalted Chambers approach as a whole | say: - | expect: Meaningfully harder: eleven Priestesses and six Supers in that room now cast. **This is the row that decides whether the tier stays** -- *Judgement row: decides whether the tier stays.*
- [ ] `PC8` (qa.md:5436) step: Watch one **Priestess Super** over four or more casts | say: - | expect: She works through all four spells before repeating any. She should not cast the same one twice running
- [ ] `DS1` (qa.md:5574) step: Reach the Druid Master at Speech 130 and take *"And what kind of power do you offer?"* first | say: - | expect: No Speech reply on the temptation node. The route is on the lore branch only -- *Needs Speech 130.*
- [ ] `DS2` (qa.md:5575) step: Ask *"How are you going to raise the dragon?"*, then sit through `30 ley lines` and `40 ley lines 2` | say: - | expect: A Speech-icon reply about Richard's blood and the grave nine paces away
- [ ] `DS3` (qa.md:5576) step: Take it | say: - | expect: `50 the bloodline`: *"If you are wrong I lose a night of work. If you are right I lose the hill"*
- [ ] `DS4` (qa.md:5577) [eyes + save] step: Press it home | say: - | expect: She calls the fires out, `51 the fires out` plays as a balloon, **3,000 XP**, and **no fight starts**
- [ ] `DS5` (qa.md:5578) step: After DS4, walk the chamber | say: - | expect: Controls work, the camera has let go, the ambush door stays shut, no golems, and she does not attack
- [ ] `DS7` (qa.md:5580) step: Repeat at Speech 129 or below | say: - | expect: The Speech reply is absent; the three vanilla replies and the four faction refusals are unchanged
- [ ] `DS8` (qa.md:5581) step: On `50 the bloodline`, take the other reply instead | say: - | expect: The normal fight, ambush and all
- [ ] `SN5` (qa.md:5586) step: Reach 05 at Sneak 20+ **with sneak mode switched on** and cross the floor in front of her | say: - | expect: A fifth reply on her opening node naming the men behind the wall
- [ ] `SN5a` (qa.md:5587) step: Cross that same floor at Sneak 20+ **not** sneaking, then step back out, switch sneak on and cross again | say: - | expect: No reply the first time; the reply is there the second time. The check retries
- [ ] `SN6` (qa.md:5588) [eyes + save] step: Take it | say: - | expect: The fight starts and her golems appear, but **the ambush door stays shut and no soldiers come out of it**. 500 XP
- [ ] `SN7` (qa.md:5589) step: Repeat SN5 as a sylvant, a feralkin and a demokin | say: - | expect: The same reply on each of the three race openings, each node's own refusals still reading correctly
- [ ] `SN8` (qa.md:5590) step: Reach 05 at Sneak 19 or below, sneaking | say: - | expect: No fifth reply. The vanilla fight, ambush included -- the toggle alone is not enough
- [ ] `DM1` (qa.md:5600) step: Reach the Druid Master as an **Inquisitor** and hear her temptation, then look at the replies | say: - | expect: A refusal no one else gets: *"You have just offered the destruction of the Holy Office to a sworn officer of it."*
- [ ] `DM2` (qa.md:5601) step: The same as a **Wielder** | say: - | expect: *"You are offering me the one thing I have ever wanted, and you are offering it with a dragon."*
- [ ] `DM3` (qa.md:5602) step: The same as a **Templar** | say: - | expect: *"My Order crossed a sea to keep a relic out of your hands, and you have just told me why."*
- [ ] `DM4` (qa.md:5603) step: The same as a **Knight of Saladin** | say: - | expect: *"You are promising to settle a quarrel I am not in."*
- [ ] `DM5` (qa.md:5604) step: The same carrying **no order** | say: - | expect: Her three vanilla refusals and the question about the ley lines. None of the four new lines appear
- [ ] `DM6` (qa.md:5605) step: Pick any of the four | say: - | expect: The fight starts exactly as it does from her vanilla refusals -- same `Fighting the Druids Last Chamber` relay, same Fight Icon
- [ ] `DM7` (qa.md:5606) step: Check her **race** greetings still work: arrive as a Sylvant, a Feralkin, a Demokin and a human | say: - | expect: Four different openings, unchanged from vanilla. The race layer is hers, not ours
- [ ] `DM8` (qa.md:5607) step: Ask *"How are you going to raise the dragon?"* first, then refuse with a faction line | say: - | expect: `30 ley lines` then `40 ley lines 2` as before, and the faction refusals are still offered afterwards
- [ ] `ES4` (qa.md:5748) step: Reach `05 Exalted Chambers`, the Druid Master's chamber | say: - | expect: **Priestesses**, including `Priestess Super`. All three Priestess templates were fielded nowhere in the entire game, while the Druid Master herself has the race `Priestess Super`
- [ ] `ES7` (qa.md:5753) step: Fight the Druid Master | say: - | expect: **A real boss fight now.** She shipped on the rank-and-file `Priestess Super` race at HP 95 / AC 150 / no resistance -- weaker than her own guards, and against an `Assasin Master` on the same map at HP 400 / AC 305. She is now HP 350 / AC 300 / 65% resist, four spells at 130 and Evasion 60
- [ ] `ES7a` (qa.md:5754) [eyes + save] step: Check the XP for killing her | say: - | expect: **2,500**, up from 1,100. She shipped paying less than the 1,949 her own attendant priestesses pay
- [ ] `ES7b` (qa.md:5755) step: Fight a rank-and-file `Priestess Super` in the same room | say: - | expect: Distinctly weaker than the Master: HP 135 / AC 310. They no longer share a race
- [ ] `SH1` (qa.md:6251) **NEW** where: 05 Exalted Chambers | steps: Talk to the Druid Master | pass: She is voiced: her lines play aloud. Before this she was silent | new: True

**06-08 Meditation Chambers**

- [ ] `ES3` (qa.md:5747) step: Fight through the three Meditation Chambers | say: - | expect: Druids alongside the golems and priests. These rooms had no soldiers at all in vanilla -- *The slots now hold real Druid/Druidess cans (0.99.0).*

**10 Inner Sanctum**

- [ ] `ES29` (qa.md:5780) step: **A save that has never entered act 7.** Enter `10 Inner Sanctum` from the Antechamber | say: - | expect: About a second in: *"There is a great deal of wall for a room this size -- and the wall does not ring the same all the way round."* **This map had no tree, no balloon and no label printer at all** -- *Line now opens 'Whatever the druids do here...'; the wall sentence follows.*
- [ ] `ES30` (qa.md:5781) step: Cross to the western corner, around 1500,1400, and look at the wall | say: - | expect: *"Three stones are set into the wall here at shoulder height, worn paler than the rest..."* The hover covers all three switches
- [ ] `ES31` (qa.md:5782) step: Click the switch at 1482,1379 | say: - | expect: A panel opens in the **eastern** wall on two strongboxes with the Temple's mark, and you are told so -- the door is 800 units away and vanilla gave no feedback whatsoever
- [ ] `ES32` (qa.md:5783) [eyes + save] step: Open those two chests | say: - | expect: Good weapons and arrows/bolts, on `Chest Generator Good`. **The best loot in the act outside a boss, behind an unmarked switch in vanilla**
- [ ] `ES33` (qa.md:5784) step: Click the switch at 1620,1364 | say: - | expect: Grinding to the **north** and *"a great many boots"* -- an ambush of soldiers, bowmen and druids
- [ ] `ES34` (qa.md:5785) step: Click the switch at 1508,1471 | say: - | expect: Grinding to the **south**, hot iron and wet stone -- war golems, a priest, a druid and a priestess
- [ ] `ES36` (qa.md:5787) step: Check that the doors, ambushes and chests behave as before | say: - | expect: Unchanged. Only balloons were added to the three relays; every vanilla action on them is intact
- [ ] `SH2` (qa.md:6252) **NEW** [eyes + save] where: 10 Inner Sanctum | steps: Pull the three stones in any order | pass: Each opens what it opens, then a separate line counts down: two left, one left, the last of them. Not "Two stones left" three times | new: True

**10 Inner Sanctum, 09 Secret Chamber**

- [ ] `PC7` (qa.md:5435) step: The Inner Sanctum (14 of them) and the Secret Chamber (12) | say: - | expect: The same change, and the same question

**England to Alamut**

- [ ] `DS6` (qa.md:5579) [eyes + save] step: Walk out to the Alamut crossing without touching her | say: - | expect: `Stop the Druids` completes and the 4,000 XP fires exactly as it does after killing her

**English Shrine (Sir Roger)**

- [ ] `S8` (qa.md:1035) where: Sir Roger, English Shrine | pass: 7 new replies -- the largest single block

**Shrine, then England to Alamut and the ending**

- [ ] `SH11` (qa.md:6261) **NEW** [eyes + save] where: Finish the shrine four ways: talk her down; spoil the ambush and kill her; kill her; walk on with her alive | steps: Reach England to Alamut with Roger, then the ending | pass: Roger says the line for that outcome, and the ending shows the matching Shrine slide with the Druid Master on the stage, before the companions | new: True -- *Four playthrough branches; the slide is read at the ending.*

**anywhere in the act**

- [ ] `MN11` (qa.md:4569) where: **Act 7**, find a Mana Tome and use it repeatedly | steps: - | pass: Declining grants, then an *"empty"* balloon forever. This is vanilla behaviour, measured but **not modified** -- confirm it matches the description above
- [ ] `DN13` (qa.md:4899) [save] step: **Sir Roger Templeton** as a companion, taking a hit | say: - | expect: **"Sir Roger Templeton"**, not "Knight Templar 5" -- *0.60.3 found the log prints the can's User Assigned Name, not the race name this release edited. Expected names here came from race names, but 0.60.3 found the log prints the can's User Assigned Name (a hat goblin logs Goblin Striker). A different name is not a failure on its own; check it against the can.*
- [ ] `BK4` (qa.md:5270) step: Act 7, English soldiers: a Super and a Bow | say: - | expect: Officer *"Not one step back, do you hear me!"* against archer *"Nock and draw!"* -- and no thief line from either
- [ ] `PC1` (qa.md:5429) step: Fight a **Priestess** in act 7 | say: - | expect: She casts **Spike** at you instead of only closing to melee
- [ ] `PC2` (qa.md:5430) step: Fight a **Priestess Tough** | say: - | expect: Fire Orb or Spike, varying between casts
- [ ] `PC4` (qa.md:5432) step: Watch a Priestess of any tier over several attacks | say: - | expect: She does **not** cast `ENEMY Magical Shield` -- that is the Priests' opener, and no Priestess race knows it
- [ ] `PC5` (qa.md:5433) step: Fight a **Priest**, **Priest Tough** or **Priest Super** | say: - | expect: Unchanged: shield first, then Fire Orb / Spike / Lightning Bolt -- *Priests also heal since 0.33.0/0.34.0; the shield-then-spells opener is unchanged.*
- [ ] `PC9` (qa.md:5437) step: Watch a **Priestess Tough** | say: - | expect: Fire Orb and Spike alternate rather than randomly repeating
- [ ] `ES5` (qa.md:5749) step: Fight priestesses at all three tiers | say: - | expect: They should feel like priests who hit harder and shield less. The shipped ladder had AC **260 / 80 / 150** and no damage resistance at any tier; it is now 260 / 280 / 310 with 50 / 60 / 65%
- [ ] `ES5a` (qa.md:5750) step: Hit a priestess with cold, electrical or fire damage | say: - | expect: It resists, 50-65% by tier. In vanilla no priestess resisted anything
- [ ] `ES6` (qa.md:5752) step: Check XP gain across the act against your notes, if you have any | say: - | expect: Roughly **+15% act-wide**, concentrated in `05`, `09` and `10` (+40-54%). A Druid pays 950 where the identically-statted Soldier1 pays 348. **Report if this feels like too much; the weights are one table** -- *The druid XP figures predate 0.99.0's can swap.*
- [ ] `ES46` (qa.md:5770) step: With Grace as a companion, fight for a minute | say: - | expect: She shouts *"For Ireland."*, *"We cannot fail."*, *"I need healing!"* **Never played in vanilla**
- [ ] `ES47` (qa.md:5771) step: Let her drop below about 60% health, then below 25% | say: - | expect: *"I require aid!"* then *"I will not survive much longer...Help me!"* -- **both are recorded lines that had no trigger**
- [ ] `ES48` (qa.md:5772) step: With Sir Roger along, fight for a minute | say: - | expect: *"For England!"*, *"For The Queen!"*, *"For The Templars!"*, *"We shall Prevail!"*, *"On my honor!"* Five authored barks, opened by nothing in vanilla
- [ ] `ES49` (qa.md:5775) step: Take a companion through a map transition and keep fighting | say: - | expect: Barks still play. They ride on the character's own AI list, not a relay belonging to one map
- [ ] `SH6` (qa.md:6256) **NEW** [eyes + save] where: Any act 7 map | steps: Bring a druid under half health | pass: The log says she calls a wolf, a wolf appears beside her with a summoning flash, and she does it once only | new: True

## 8 Alamut (108)


**01 Desert Sprawl**

- [ ] `BU19` (qa.md:4694) [eyes + save] step: Be the Khan's **Champion**, leave him **alive**, **do not** side with Hrargrub, then reach `01 Desert Sprawl` | say: - | expect: Unchanged from 0.30.0: the **Rumjun Khan appears** and **Grumdjum joins as a companion**
- [ ] `BU20` (qa.md:4695) [eyes + save] step: Same run, but **hand Hrargrub the book** first | say: - | expect: **Neither appears.** A mid-game choice in an optional cave costs a late-game companion. This is the row the whole feature exists for
- [ ] `BU21` (qa.md:4696) [save] step: Check the marker is doing it and not something else | say: - | expect: `Sided with Butu's heir` lives in `01 Desert Sprawl` itself, `Active=0`, flipped from Ravine Cave East by `COtherMapAction`. It is **not** in the Wilderness, because the expiry door closes those maps before act 8
- [ ] `BU22` (qa.md:4697) [eyes + save] step: **Open question, and it predates this build.** Kill Plumjum Khan in act 1, then reach `01 Desert Sprawl` as his Champion | say: - | expect: He should **not** appear. But `Goblin Khan is Dead` lives in `Inquisition Chambers2` and `Grumdjum Dead` lives in `Lake`, and **both maps are expired** by `3 Montaillou/02 Hamlet Burned`'s `From Crypt or Nostro Portal` spawn point before act 8. If the Khan turns up in Persia anyway, those markers are being read out of expired maps and Fixt's act 8 gate has never worked -- *0.99.3 moved the act 8 gate to Fixt Khan Slain, so the expired-map question is likely moot.*
- [ ] `SR16` (qa.md:5529) step: As **any** Knight of Saladin (rank does not matter), talk to the desert merchant in `01 Desert Sprawl` | say: - | expect: A new first reply about riding for the Sultan's house, then `40 the order`
- [ ] `SR17` (qa.md:5530) step: Buy something, then compare with a non-Saladin character | say: - | expect: Visibly cheaper: his multiplier drops 2.0 to 1.5
- [ ] `SR18` (qa.md:5531) step: Talk to him again, take the Saladin reply's node a second time | say: - | expect: The reply is gone -- the discount lands once, not once per conversation
- [ ] `SR19` (qa.md:5532) step: As a Knight of Saladin with Barter 40 and then 95, haggle after taking the discount | say: - | expect: Both haggle steps still work and stack on top: 1.5, then 1.4, then 1.3
- [ ] `SR20` (qa.md:5533) step: Open his shop as anyone at all | say: - | expect: `Great Healing` x3, `Superior Healing` x2 and `Supreme Healing` x1 on the shelf -- Quinn's tiers, available in act 8 for the first time
- [ ] `SR21` (qa.md:5534) step: Buy and drink a Supreme Healing bought from him | say: - | expect: Heals as the herbalist's does. It is the same addition on the same base potion
- [ ] `SR22` (qa.md:5535) step: As a Knight of Saladin, walk up to Fazeem in `01 Desert Sprawl` **without** having spoken to the merchant | say: - | expect: A first reply about the men in black who use this road. The Speech 70 route is still absent until the merchant mentions them
- [ ] `SR23` (qa.md:5536) step: Take it, then answer his challenge truthfully | say: - | expect: `31 the bargain`, and the bird men turn on the Assassins -- the same outcome the con produces
- [ ] `SR24` (qa.md:5537) [eyes + save] step: Check your gold before and after | say: - | expect: **No payment.** The con's gold is on the Barter branches only; the honest route pays nothing
- [ ] `SR25` (qa.md:5538) [eyes + save] step: Check XP | say: - | expect: The same `Talked Fazeem into Fighting Assassins XP` award the con gives
- [ ] `SR26` (qa.md:5539) step: Afterwards, walk into the Assassins on that map | say: - | expect: Fazeem and the bird men near him fight them, as they do after the con
- [ ] `SR27` (qa.md:5540) step: As a Knight of Saladin with Speech 70 who **has** heard the merchant | say: - | expect: Both routes offered. The Saladin reply sits above the Speech one and does not replace it
- [ ] `SR28` (qa.md:5541) step: Take the new route's "I think I will kill you instead" or its exit reply | say: - | expect: `Make All Bird Men Attack`, exactly as every other exit in that tree
- [ ] `SR29` (qa.md:5542) step: Approach Fazeem carrying no order | say: - | expect: The vanilla encounter, unchanged
- [ ] `AL15` (qa.md:5694) [eyes + save] step: Reach **Goblin Champion** (`Goblin Rank` 3) with the Horde, leave the goblin Khan **alive**, then enter `01 Desert Sprawl` from England | say: - | expect: Grumdjum is waiting near where you arrive. `300 companion`: *"Greetings, goblin friend... since my Khan has tasked me to aid with your quest, let us seek the Old Man in Alamut"*
- [ ] `AL16` (qa.md:5695) step: Ask *"Why do you want to help me?"* | say: - | expect: `300 kill old man` -- the Great Khan's warriors died trying, and he wants the Old Man's brain as his fee
- [ ] `AL17` (qa.md:5696) step: Accept from either node | say: - | expect: He joins as a companion. `300 companion quips 3` plays. Both accept replies now carry `CSetCompanionAction`
- [ ] `AL18` (qa.md:5697) step: Fight alongside him for a minute | say: - | expect: `300 companion quips 1/2/3` shuffle roughly every 13 seconds, in rhyming couplets, anchored over him and not over you
- [ ] `AL19` (qa.md:5698) step: Let him drop below half health, then below a fifth | say: - | expect: `300 grumdjum hurting` then `300 grumdjum hurting 2`. Each fires once
- [ ] `AL20` (qa.md:5699) step: Talk to him while he is your companion | say: - | expect: `300 player speaks to goblin as companion`: *"What can Grumdjum do for you?"* -- not the recruitment node again
- [ ] `AL21` (qa.md:5700) step: Dismiss him with *"I work alone. Leave."* | say: - | expect: `300 companion leaves you`, he stays put, and he calls `300 grumdjum asks to rejoin` as you pass
- [ ] `AL22` (qa.md:5701) step: Talk to him again | say: - | expect: `300 companion joins you` **with two replies** -- it was recorded reply-less, asking a question nobody could answer. Accepting plays `300 grumdjum rejoins`
- [ ] `AL23` (qa.md:5702) step: Tell him *"I'd rather kill you where you stand"* | say: - | expect: He actually fights. This reply had a Fight Icon and no action in vanilla
- [ ] `AL24` (qa.md:5703) step: Walk a little further in with the Khan alive | say: - | expect: Rumjun Khan is there too, as a cameo: `500 Start in Persia`, **and it is voiced** -- all three Persia nodes shipped with the VO flag off and the recordings present
- [ ] `AL25` (qa.md:5704) step: Accept the Khan's offer, then decline on another run | say: - | expect: `501 Excellent` and `502 Too bad`. He is not a companion either way -- he sows his own destruction, or takes his brethren east
- [ ] `AL26` (qa.md:5705) [eyes + save] step: On a character who **killed the goblin Khan** for Torquemada in act 1, enter act 8 | say: - | expect: **No goblin at all.** Neither generator activates. The gate reads vanilla's own `Goblin Khan is Dead` checker -- *Gate now reads Fixt Khan Slain (0.99.0), not the vanilla checker.*
- [ ] `AL27` (qa.md:5706) [eyes + save] step: On a **Goblin Chum or Blooded** (rank 1 or 2), Khan alive | say: - | expect: **Neither goblin appears.** Both are gated on `Goblin Horde Highlevel`, the same can the Khan gates his own top-tier replies on -- the Khan tasks a warrior to his Champion, not to an acquaintance
- [ ] `AL28` (qa.md:5707) [eyes + save] step: As a Goblin Champion who killed Grumdjum at the Lake | say: - | expect: The Khan appears; Grumdjum does not. The gate reads `Grumdjum Dead`, the marker his own vanilla generator sets -- *Gate now reads Fixt Companion Goblin Grumdjum >= 2 (0.99.0).*
- [ ] `AL29` (qa.md:5708) [eyes + save] step: As a Goblin Champion who never met Grumdjum at all | say: - | expect: He still comes. Champion standing is the whole gate -- the Khan sent him, and his *"once again"* is the Horde's camp, not the lake

**01, 02**

- [ ] `AT11` (qa.md:6241) **NEW** [eyes + save] where: 01, 02 | steps: Look at the packs | pass: Roughly one pack in four is Sand Spirits instead of beasts | new: True

**02 Shifting Dunes**

- [ ] `SR1` (qa.md:5514) step: As an Exalted **male** knight, meet the Knight of Saladin in the dunes | say: - | expect: *"Salaam - Exalted... Command me, Brother"* -- not the vanilla "You do much honor to Saladin's name"
- [ ] `SR2` (qa.md:5515) step: The same as an Exalted **female** knight | say: - | expect: The same greeting, addressed Sister
- [ ] `SR3` (qa.md:5516) step: Ask what the order says about this place | say: - | expect: `24 the standing order`: the oath every Aswaran takes, and that you are the one who is nearest
- [ ] `SR5` (qa.md:5518) step: Repeat SR1 as a knight who took the initiation but **not** all five crystals | say: - | expect: The vanilla Brother/Sister greeting. No Exalted line, no standing order, no second Old Man reply
- [ ] `SR6` (qa.md:5519) step: Repeat as a **Templar** | say: - | expect: The vanilla Knight Templar greeting and the tribute reply, unchanged
- [ ] `SR7` (qa.md:5520) step: Repeat carrying **no order** | say: - | expect: `1 Conversation Start`, unchanged
- [ ] `SR8` (qa.md:5521) step: As an Exalted knight, dismiss the companion and pick him up again | say: - | expect: `666 Rejoin` and `3 Return` behave exactly as before; the rank greeting is a first-meeting only, as vanilla's are
- [ ] `SR9` (qa.md:5522) step: As an Exalted knight, take `24 the standing order` and then *"Then come the whole way in"* | say: - | expect: `25 the order rides`, and he agrees to come as far as the Old Man's door
- [ ] `AL30` (qa.md:5709) step: Meet the Knight of Saladin on `02 Shifting Dunes` and ask *"What is inside Alamut?"* | say: - | expect: `20 alamut` answers. Five replies pointed at `20 Alamut` with a capital A against a lowercase node
- [ ] `AL31` (qa.md:5710) step: Recruit him the **first** time you meet him, via *"Let's carry the battle to Alamut, then"* | say: - | expect: He **follows you**. In vanilla this path set the companion flag without the escort AI, so he stood where he was
- [ ] `AL32` (qa.md:5711) step: Talk to him while he is following | say: - | expect: `3 Return`, *"Salaam. May the Prophet give us strength"* -- **not** *"Do you need my help again?"*, which is what vanilla opened for an already-recruited companion
- [ ] `AL33` (qa.md:5712) step: Tell him *"Hold this ground and wait for me."* | say: - | expect: He is released and stays. Vanilla had no dismissal for him anywhere in the tree
- [ ] `AL34` (qa.md:5713) step: Talk to him again | say: - | expect: `666 Rejoin`. *"Yes, please rejoin me"* restores the escort AI as well as the flag; *"No, wait here"* now does the right thing, because he is waiting
- [ ] `AL36` (qa.md:5715) step: Recruit him on a **return** visit instead, via `3 Return`'s *"Let's go."* | say: - | expect: Same result as AL31. Both recruit paths now give the escort AI and open `3 Return` afterwards
- [ ] `AL45` (qa.md:5724) step: Greet the Knight of Saladin on `02 Shifting Dunes` as a **Templar** | say: - | expect: A fourth reply about the two orders' arrangement, leading to `22 the tribute`
- [ ] `AL46` (qa.md:5725) step: Greet him as a **Knight of Saladin**, male or female | say: - | expect: A fourth reply, *"They sent knives into Saladin's own tent. Twice."*, leading to `23 the tent`
- [ ] `AL47` (qa.md:5726) step: Greet him carrying **no order** | say: - | expect: His three vanilla replies only. `1 Conversation Start` is unchanged

**03 Sand Dragon, 04 Maw of the Assasin**

- [ ] `SR10` (qa.md:5523) [eyes + save] step: Walk on into 03 Sand Dragon, then 04 Maw of the Assasin | say: - | expect: A Knight of Saladin is standing at each arrival and fights with you. He is talkable and gives `3 Return`

**03 to 07**

- [ ] `AT13` (qa.md:6243) **NEW** [eyes + save] where: Act 8 with the Knight of Saladin from Exalted | steps: Walk 03 to 07 | pass: Only one Knight of Saladin. If two appear, report it with a save | new: True

**04 Maw of the Assasin**

- [ ] `SR15` (qa.md:5528) step: Reach the Maw as a Templar or with no order | say: - | expect: No escort, no ride reply, no Exalted greeting
- [ ] `AL35` (qa.md:5714) step: Fight beside him in `04 Maw of the Assasin` or later | say: - | expect: He survives contact. Repaired to HP 220 / AC 215 from 150/145, with `OneHandedMelee 200` untouched
- [ ] `AL48` (qa.md:5727) step: Recruit Grumdjum on `01 Desert Sprawl`, walk him to `04 Maw of the Assasin` or later, then dismiss him there | say: - | expect: He is released **and** his interaction switches to `300 companion joins you`. Before the review pass the switch sat on a relay that only exists on `01 Desert Sprawl`
- [ ] `AL49` (qa.md:5728) step: Talk to him on that far map after dismissing him | say: - | expect: `300 companion joins you`, answerable, not *"What can Grumdjum do for you?"*

**04 Maw of the Assasin and others**

- [ ] `AT7` (qa.md:6237) **NEW** where: The Maw's Assassin Master, the Elemental Spirit, DaVinci's evil lines, Galileo's survival line, the Old Man's Inquisition scene | steps: Hear them | pass: Each speaks aloud where it was silent | new: True

**04 to 07**

- [ ] `AT10` (qa.md:6240) **NEW** [eyes + save] where: 04 to 07 | steps: Bring several Assassin Masters under half health | pass: About half whistle up two guard dogs, with a log line; none does it twice | new: True

**05 Acid Wash**

- [ ] `AL1` (qa.md:5680) step: Enter `05 Acid Wash` from `04 Maw of the Assassin` and walk west along the channel | say: - | expect: `1 the channel` arrives **before** any acid: the cut channel and its fall to the west, the stone eaten smooth like a streambed, and the bowmen on the terraces who have no intention of being in it
- [ ] `AL2` (qa.md:5681) step: Keep going until the first wash fires | say: - | expect: `2 the first sluice` as it launches -- it lets go up-slope to the east, and the channel is ready again about ten seconds later. The wash is unchanged: 20-40 Acid, `Defend Against=1`, so acid resistance still applies
- [ ] `AL3` (qa.md:5682) step: Stand clear, wait, then cross the same spot again | say: - | expect: The wash fires again. `First Trap Trigger` is still `Trigger Only Once=0`, so the hazard cycles exactly as it shipped -- but neither balloon repeats
- [ ] `AL4` (qa.md:5683) step: Reach the western gate's trigger | say: - | expect: `3 the second sluice`. The trigger polygon is vanilla's own, byte for byte
- [ ] `AL5` (qa.md:5684) step: Walk up to the switch beside the spiked gates | say: - | expect: `4 the sluice control`: an iron switch at waist height, rock worn pale by hands, and the gates standing closed across the passage
- [ ] `AL6` (qa.md:5685) step: Press it | say: - | expect: All five of vanilla's own effects -- the `Spike Door near Switch` gates open, the coffin-lid sound plays, both wash triggers deactivate, and **Disarmed trap** prints emphasised -- and then `5 the gates open` as a sixth
- [ ] `AL7` (qa.md:5686) step: Walk back over both wash triggers | say: - | expect: Neither fires. Vanilla's two `CDeactivateAction`s are untouched
- [ ] `AL8` (qa.md:5687) step: Press the switch again | say: - | expect: Nothing happens. The relay is `Trigger Only Once=1`, as it shipped
- [ ] `AL9` (qa.md:5688) step: On a fresh character, enter instead from `06 Chamber of Torment` and walk east | say: - | expect: All four triggers still fire when crossed from that side, but the ordering is only guaranteed on the forward path: approaching from the west, `2 the first sluice` can arrive before `1 the channel`. Worth knowing whether that reads badly -- *Needs a fresh character entering from 06.*
- [ ] `AL10` (qa.md:5689) [save] step: Check the combat log after AL1-AL6 | say: - | expect: All five balloon texts are in the log. Every node carries `Include In Log=1`
- [ ] `HN3` (qa.md:6223) **NEW** where: 05 Acid Wash | steps: Walk the channel without the search skill, then with it | pass: No valve line without it. With it, the line plays as the valve is revealed | new: True
- [ ] `AT8` (qa.md:6238) **NEW** where: 05 Acid Wash | steps: Lure an assassin into the channel as a sluice fires | pass: The acid hurts him too. A companion standing in it is hurt as well | new: True
- [ ] `AT9` (qa.md:6239) **NEW** where: 05 Acid Wash, near the entrance | steps: Search for secrets (a good trap and secret skill) | pass: A hidden valve is revealed; using it shuts both sluices and opens the spiked gates, as the far switch does. Without the skill it stays hidden | new: True

**05 Acid Wash, 06 Chamber of Torment, 07 Dark Temple**

- [ ] `SR11` (qa.md:5524) [eyes + save] step: Continue through 05 Acid Wash, 06 Chamber of Torment and 07 Dark Temple | say: - | expect: The same on each. He is the 220 HP / 215 AC companion race, not a citizen

**05 Acid Wash, 07 Dark Temple**

- [ ] `AT12` (qa.md:6242) **NEW** where: 05 and 07 with the Knight of Saladin and Grumdjum | steps: Enter each the first time | pass: Each says one line, the knight first; neither repeats | new: True

**06 Chamber of Torment**

- [ ] `BW5` (qa.md:2368) step: **New character, never been to the Chamber of Torment.** Trigger `secret 05` in act 8 | say: - | expect: **Two** items still drop, not one: a roll from the MASTER ALL list and a random magic item. If only one appears, the swap dropped a slot
- [ ] `BW6` (qa.md:2369) step: The same secret, watching what else happens | say: - | expect: The guards still spawn with it: two spirits, an assassin and a guard dog. Eight entities share that name, so one trigger must still do all of it

**08 Final Encounter**

- [ ] `DN12` (qa.md:4898) [save] step: The endgame **Leonardo** in `08 Final Encounter` | say: - | expect: **"Leonardo DaVinci"**, not "Leo" -- *0.60.3 found the log prints the can's User Assigned Name, not the race name this release edited. Expected names here came from race names, but 0.60.3 found the log prints the can's User Assigned Name (a hat goblin logs Goblin Striker). A different name is not a failure on its own; check it against the can.*
- [ ] `SR4` (qa.md:5517) step: Reach the Old Man and read the replies at `40 ruse` | say: - | expect: **Two** Saladin lines: the vanilla-era *"I am what came back"* and the new standing-order one. Both lead to the fight
- [ ] `SR12` (qa.md:5525) step: Enter 08 Final Encounter | say: - | expect: **He does not follow.** The finale plays exactly as vanilla, with no extra body in the scripted scene
- [ ] `AL12` (qa.md:5691) [eyes + save] step: Enter `08 Final Encounter` carrying **Find Galileo and DaVinci** from act 6's blacksmith | say: - | expect: It completes. DaVinci speaks in the opening cinematic, through `DaVinci Ending / 100 Respond ask about Tank`, so the find is dramatised and not only a journal tick
- [ ] `AL13` (qa.md:5692) [eyes + save] step: Enter it carrying **Pursue the Retreating Druid Forces**, activated at act 6's crossroads | say: - | expect: It completes when `Cross Regret for Player generator` hands over the `TRUE CROSS` -- the relics the Old Man is using in the ritual are the ones stolen in act 6
- [ ] `AL37` (qa.md:5716) step: Reach `40 ruse` in the final confrontation as a **Knight of Saladin** | say: - | expect: A sixth reply: *"Twice your knives found Saladin's tent, and twice they found nothing in it. I am what came back."* Leads to `45 combat` like the rest
- [ ] `AL38` (qa.md:5717) step: The same as a **Templar** | say: - | expect: *"The Temple has sent you coin for sixty years to keep your knives out of our chapter houses."*
- [ ] `AL39` (qa.md:5718) step: The same as an **Inquisitor** | say: - | expect: *"I have put men to the fire for a tenth of the heresy you have spoken since I walked in."*
- [ ] `AL40` (qa.md:5719) step: The same as a **Wielder** | say: - | expect: *"Something else lives in me, and it has never once lied to me about what it wants."*
- [ ] `AL41` (qa.md:5720) step: The same as a **Goblin Champion** | say: - | expect: *"The Great Khan sent proud warriors after you once and not one of them came home."* This is the Khan's attempt that `300 kill old man` describes
- [ ] `AL42` (qa.md:5721) step: Reach `40 ruse` with **no order and no goblin rank** | say: - | expect: Exactly vanilla's five replies. None of the new ones show
- [ ] `AL43` (qa.md:5722) step: Carry two of those at once, e.g. Templar **and** Goblin Champion | say: - | expect: Both replies offered. They are alternatives, not ranked
- [ ] `AL44` (qa.md:5723) step: Check the Speech path is untouched: reach `200 begin non combat solution path` at Speech 100 | say: - | expect: Still gated on Speech 100, then 130, then 180, with karma branching at 600. Nothing about the talk-down route changed

**10 Cave 5 and 06 Chamber of Torment**

- [ ] `BW7` (qa.md:2370) step: **Regression.** The Bow of Fiery Smite must not exist twice | say: - | expect: It is in Cave 5 and **nowhere** in act 8. This was a relocation, not a duplication

**END GAME Calle Perdida**

- [ ] `AT2` (qa.md:6232) **NEW** where: A dark ending (Calle Perdida) | steps: Finish it | pass: After Nostradamus the game goes to the stage, plays the slides this character earned, then the credits. Before this the dark endings showed no slide | new: True

**Final Encounter**

- [ ] `AT6` (qa.md:6236) **NEW** where: Final Encounter | steps: Let the Old Man escape | pass: The escape plays through: camera, spirits, then the ending. Nothing stops at his disappearance | new: True

**the Demesne**

- [ ] `AT3` (qa.md:6233) **NEW** where: The Demesne, before either ending | steps: Press Escape on Nostradamus | pass: The scene continues to the right ending map | new: True

**the three ending maps**

- [ ] `AT1` (qa.md:6231) **NEW** where: Any good ending | steps: Press Escape on each Nostradamus line after the battle | pass: The ending carries on exactly as clicking would, and reaches the stage. Nothing stalls | new: True

**anywhere in the act**

- [ ] `DN8` (qa.md:4861) [save] step: Grumdjum as a companion, taking damage | say: - | expect: **"Goblin Grumdjum"**, with the d. Vanilla's race spelled it *Grumjun* while all twelve of his map entity names and his whole dialogue tree spell it Grumdjum -- *0.60.3 found the log prints the can's User Assigned Name, not the race name this release edited. Expected names here came from race names, but 0.60.3 found the log prints the can's User Assigned Name (a hat goblin logs Goblin Striker). A different name is not a failure on its own; check it against the can.*
- [ ] `GB17` (qa.md:4966) [eyes + save] step: **Grumdjum as a companion**, with a fire-casting player | say: - | expect: He is `Goblin Grumjun`, so fire-vulnerable too -- but at the boss tier's **-10**, not -25. If he still burns down noticeably faster than other companions, say so: the taper exists for this and can go further
- [ ] `KS1` (qa.md:5364) step: Meet him, do **not** recruit, then talk again | say: - | expect: Only *"Let's go."* is offered. **No** "Hold this ground" -- he is not with you to dismiss
- [ ] `KS2` (qa.md:5365) step: Recruit him, then talk | say: - | expect: Only *"Hold this ground and wait for me."*. **No** "Let's go."
- [ ] `KS3` (qa.md:5366) step: Dismiss him, then talk | say: - | expect: *"Do you need my help again?"* with "Yes, please rejoin me." -- the `666 Rejoin` node
- [ ] `KS4` (qa.md:5367) step: Rejoin, then talk | say: - | expect: Back to only the dismiss line
- [ ] `KS5` (qa.md:5368) step: Recruit him the first time through `30 go` | say: - | expect: Works as before; that node still has its default reply
- [ ] `KS6` (qa.md:5369) step: Cycle dismiss and rejoin three times, then talk | say: - | expect: Still exactly one of the two replies, never both and never neither. The variable must not drift
- [ ] `KS7` (qa.md:5370) [save] step: `python tools/savecheck.py grep "Saladin Knight Follows" --save latest` | say: - | expect: 1 while he follows, 0 or absent otherwise
- [ ] `SR13` (qa.md:5526) step: Do **not** take the ride reply, then walk in | say: - | expect: No escort on any of the five maps. The act is unchanged
- [ ] `SR14` (qa.md:5527) step: Take the ride reply, then walk *backwards* to a map you already crossed | say: - | expect: No escort there until you leave and re-enter -- the checker is read on arrival. Recorded, not a defect
- [ ] `AL14` (qa.md:5693) step: Reach act 8 with Grace O'Malley recruited in act 7 | say: - | expect: She follows and has nothing to say, exactly as Sir Roger does. This is parity with vanilla, not a gap
- [ ] `AL50` (qa.md:5729) step: Recruit the Knight of Saladin, walk him off `02 Shifting Dunes`, dismiss him there | say: - | expect: Same: released, and his interaction switches to `666 Rejoin` on whatever map he is standing on
- [ ] `AT5` (qa.md:6235) **NEW** where: Dismiss Grumdjum, then click him | steps: - | pass: He says "Are you ready to continue our quest - to put the Old Man to rest?" aloud before the rejoin conversation | new: True

## Ending (60)


**epilogue stage**

- [ ] `ES20` (qa.md:6267) **NEW** where: Finish the game, or `Ending tests` then `As I am` | steps: - | pass: After Javier the screen goes black and the stage opens with no visible pan. No crash on the teleport | new: True
- [ ] `ES21` (qa.md:6268) **NEW** where: The same | steps: Read through | pass: Every slide this character earned plays, in order, with the right figure centre-stage and none left over from the slide before. Slides with no figure (the pits, the Savage Heart, the woodcutter, no allegiance) play on the empty stage | new: True
- [ ] `ES22` (qa.md:6269) **NEW** [eyes + save] where: The same, having talked Ahriman into death | steps: - | pass: The Templar slide is the one that says the order was never sworn to him: the flag survived the teleport | new: True
- [ ] `ES23` (qa.md:6270) **NEW** where: The same | steps: Press Escape on a slide | pass: It advances to the next slide, and the credits still roll at the end | new: True
- [ ] `ES24` (qa.md:6271) **NEW** where: With companions alive | steps: - | pass: Nobody you travelled with wanders into frame, and every figure stands still, including the golem and Fang | new: True
- [ ] `EF4` (qa.md:6321) who: A character with no slide for several steps in a row | steps: Watch the gaps | pass: No visible hang: empty steps pass in a blink. If there is a long blank pause, tell me how long
- [ ] `EF5` (qa.md:6322) who: **Judgement.** A full character | steps: Read the whole ending | pass: Does it drag? Up to about 30 slides can now play -- *Judgement row.*

**anywhere in the act**

- [ ] `CE2` (qa.md:2571) step: **The row that proves the record, not the slide.** Recruit Cervantes, lose him in a fight, finish the game | say: - | expect: His **died in your service** slide, not his surviving one
- [ ] `CE4` (qa.md:2573) step: Talk Jehanne down and leave her holding the Lance, then finish the game | say: - | expect: The slide where she raises the gate and goes back to standing where she stood
- [ ] `CE5` (qa.md:2574) step: Free Jehanne and her knights with the lamp, then finish the game | say: - | expect: The **released** slide. Her knights go in the same minute, down the corridor, without being told
- [ ] `CE6` (qa.md:2575) step: Kill her for the Lance instead | say: - | expect: The **killed** slide, and not the released or passed one
- [ ] `CE7` (qa.md:2576) step: Judge the Cortes and Shylocke dispute for Shylocke, never recruit Cortes, finish | say: - | expect: *"here I thought you would vindicate me"*, the ship sold inside a month
- [ ] `CE8` (qa.md:2577) step: Take the Dark Inquisitors' contract on Bishop Diego and finish the game | say: - | expect: The **sold** slide, not his ordinary death
- [ ] `CE9` (qa.md:2578) step: Never free Darsh from the goblin camp, report it to Raphael, finish | say: - | expect: The Warrens argue about the red spice against the grey
- [ ] `CE10` (qa.md:2579) step: Save Juan, keep Fernand, finish | say: - | expect: The slide with the small boat that leaks. Then fail to save Juan on another run and get the other one
- [ ] `CE13` (qa.md:2582) step: **Regression on Grace.** Recruit Grace, let her die, finish the game | say: - | expect: Her death slide, and **not** `900 order omalley` claiming she took prizes for twenty years
- [ ] `ES2` (qa.md:2771) step: Look at the box the slides appear in | say: - | expect: **No name and no portrait.** If it says *Nostrodomus*, the wrong tree is being spoken and 0.70.0 is still installed
- [ ] `ES3` (qa.md:2772) step: **Regression.** Watch Nostradamus's own prophecy and all four of Javier's lines | say: - | expect: Unchanged, in the same order, same pacing. His tree is vanilla again apart from one previously-empty field
- [ ] `ES5` (qa.md:2774) step: Finish as a **Templar** who did **not** talk Ahriman to death | say: - | expect: Javier swears the order; three tiers by rank. A Templar who has also killed Templars gets a different paragraph again, ending *"struck out by a hand nobody signed for"*
- [ ] `ES7` (qa.md:2776) step: **The Wielders, three ways.** Finish (a) as a Wielder with the city intact, (b) having told Raphael where La Calle Perdida was, (c) having used Relican's ring | say: - | expect: Three different paragraphs. (b) also fires an Inquisition slide, since you did them a service. (c) calls you Dark Lord of a place that no longer existed
- [ ] `ES8` (qa.md:2777) step: **The Horde, five ways.** Chum, Blooded, Champion, `Goblin Traitor`, and none of them | say: - | expect: Highest standing wins, and the traitor paragraph beats all of them. Remember the titles accumulate: a Champion still carries Chum and Blooded, so the order of testing is what makes this correct
- [ ] `ES9` (qa.md:2778) step: **Enemy of the ...** Finish as an Inquisitor, Knight of Saladin or Wielder who has killed that faction's own | say: - | expect: The hostile paragraph rather than the ordinary one. These are 0.47.0's titles, so they are earned by killing a member anywhere in the game
- [ ] `ES10` (qa.md:2779) step: **The Savage Heart.** Take Raylark's contract and finish; then on another character take it and kill him for the Khan | say: - | expect: Two different paragraphs. A character who never took the contract gets neither
- [ ] `ES11` (qa.md:2780) step: **England.** Finish carrying `Servant of the Queen`, and separately `Grace's Regard` | say: - | expect: One paragraph each, and **both** if you hold both
- [ ] `ES12` (qa.md:2781) step: Finish as a character who joined **nothing** and holds none of the fate titles | say: - | expect: *"All four accounts survive in the archives, and not one of them is true."* And **only** that one -- if any other slide also fires, a gate in the no-allegiance chain is wrong -- *Shrine and companion slides now play too; check only that no order slide fires.*
- [ ] `HH14` (qa.md:6114) where: Finish the game, HH11's character | steps: Watch the slides | pass: `900 order inquisition dark`, and not the `killer` slide
- [ ] `HH15` (qa.md:6115) where: Finish the game, HH12's character with no faction | steps: Watch the slides | pass: `900 order inquisition broken`, and **not** the no-allegiance slide. Then a Templar killer: broken **and** their own order's slide
- [ ] `HH17` (qa.md:6117) where: No cult dealings at all, finish the game | steps: Watch the slides | pass: **No** cult slide, and the series carries on. This is the regression: a missing branch here would hang the ending
- [ ] `HH18` (qa.md:6118) [eyes + save] where: Kill all five without ever meeting Diego, finish the game | steps: - | pass: `900 order cult ended`. If it is absent, the fifth-death write did not run
- [ ] `HH19` (qa.md:6119) [eyes + save] where: Finish Diego's quest, report to Torquemada, finish the game | steps: - | pass: `900 order cult told`
- [ ] `HH20` (qa.md:6120) where: Destroy them **and** kill Torquemada | steps: - | pass: `900 order cult ended dead`, after his own slide
- [ ] `HH21` (qa.md:6121) where: Kill Diego for them, finish the game | steps: - | pass: `900 order cult served`, with Diego's `sold` slide in its usual place
- [ ] `HH23` (qa.md:6123) where: Kill Diego for them, collect, then kill all five | steps: - | pass: `ended`, **not** `served`. There is no cult left to prosper
- [ ] `HH24` (qa.md:6124) where: Templar, knights freed, no Aegis, finish the game | steps: - | pass: `900 order templar relic`, straight after the Templar slide
- [ ] `HH25` (qa.md:6125) [eyes + save] where: Templar, take the Aegis from Sir Roger, finish the game | steps: - | pass: `900 order templar aegis`. Check the handover scene still exits through `10 accept` and gives you control back
- [ ] `HH26` (qa.md:6126) where: Templar who passed through the Crypt or killed Jehanne, finish the game | steps: - | pass: **No** shield slide, and the series carries on
- [ ] `HH27` (qa.md:6127) where: Non-Templar who freed the knights, finish the game | steps: - | pass: **No** shield slide. Jehanne's `released` slide is theirs
- [ ] `HH28` (qa.md:6128) where: Knight of Saladin, Shard route, riddles, finish the game | steps: - | pass: `900 order saladin shard scholar`, straight after the Saladin slide. Then combat instead: `shard dervish`
- [ ] `HH29` (qa.md:6129) where: Scimitar route, riddles, finish the game | steps: - | pass: `900 order saladin scimitar scholar`. Then combat instead: `scimitar dervish`, the burning blade
- [ ] `HH30` (qa.md:6130) [eyes + save] where: Scimitar route, hand Amir the Shard unasked, finish the game | steps: - | pass: The `unasked` version, with the closing line about the coin. Also check the scene itself still ends normally
- [ ] `HH31` (qa.md:6131) where: Not a Knight of Saladin, finish the game | steps: - | pass: **No** slide here, and the series carries on
- [ ] `HH32` (qa.md:6132) where: Finish `Hunt down Relican` for Cedric, finish the game | steps: - | pass: `900 order relican hunted`, after the Wielder slide. Then cure Brambles too: `hunted cured`
- [ ] `HH33` (qa.md:6133) [eyes + save] where: Refuse the ring, finish the game | steps: - | pass: `900 order relican refused`. The scene itself must still end normally, and it needs a save that has not yet refused
- [ ] `HH34` (qa.md:6134) where: Cure Brambles, no Cedric, any faction | steps: - | pass: `900 order relican cured`
- [ ] `HH35` (qa.md:6135) where: Use the ring and complete Relican's service, with Quinn joined and Leonardo agreed | steps: - | pass: `900 order relican dark joined joined`, straight after `900 order wielder ring`
- [ ] `HH36` (qa.md:6136) where: The same, Quinn killed and Leonardo refused | steps: - | pass: `dark killed refused`
- [ ] `HH37` (qa.md:6137) where: Use the ring and take no rank from Relican. Then, separately, do none of this | steps: - | pass: **No** Relican slide in either case, and the series carries on
- [ ] `HH38` (qa.md:6138) [eyes + save] where: Kill the Khan **without** Torquemada's quest, on a save that has not entered the Warrens | steps: Finish the game | pass: `900 order goblins khan`. This is the row that proves the flag is in the right slot
- [ ] `HH40` (qa.md:6140) where: Earn `Goblin Slayer`, Khan alive, then return the poems | steps: Finish the game | pass: `900 order goblins count poems`
- [ ] `HH41` (qa.md:6141) where: Bring Rakeb the eyes and kill Esteban for the patrol | steps: Finish the game | pass: `900 order goblins eyes esteban`, as one slide
- [ ] `HH42` (qa.md:6142) where: Do none of this, in any faction | steps: Finish the game | pass: Neither slide, and the series carries on. Then read the Khan's greeting: *Plumdjum*
- [ ] `HH43` (qa.md:6143) where: Give Fawkes the plans, decline the Duke, finish the game | steps: - | pass: `900 order england`, unchanged
- [ ] `HH44` (qa.md:6144) where: Lure the Duke to the gunpowder, finish the game | steps: - | pass: `900 order england duke`, with the keg line
- [ ] `HH45` (qa.md:6145) where: Kill Fawkes for the Duke of Medina, finish the game | steps: - | pass: `900 order spain`, and the England slide does not fire
- [ ] `HH56` (qa.md:6156) where: Finish the game, HH50's character | steps: Watch the slides | pass: `900 order inquisition dark`: Raphael in the chair
- [ ] `HH57` (qa.md:6157) where: Finish the game, HH51's, then an outsider who never reached him | steps: - | pass: `donated`, then `broken`
- [ ] `HH58` (qa.md:6158) where: Finish the game, HH55's, member and outsider. Then one who served the cult | steps: - | pass: `dark sede` and `broken sede`. The cult slide is `inherited` only here, and `contested` when Raphael lives
- [ ] `XS10` (qa.md:6298) [eyes + save] where: **The regression.** Finish the game without breaking it | steps: - | pass: No `900 order standard` slide, and Joan's and the golem's usual slides
- [ ] `XS12` (qa.md:6300) [eyes + save] where: XS11, then finish the game | steps: - | pass: `900 order standard blood`, not the plain slide
- [ ] `SP12` (qa.md:6388) where: Finish the game after SP7, SP8 and SP9 in turn | steps: Watch the slides | pass: Exactly one `900 order pits` slide, matching the choice, none if you never decided. With `Fixt Inquisition Hostile` set, no buyer and no Sell reply -- *Three runs or reloads; with Fixt Inquisition Hostile set, check the buyer is absent in the yard.*

## Anywhere (377)


**Cervantes, Cortes as enemies**

- [ ] `FB12` (qa.md:1765) step: **Negative, the one that could break the game.** Fight Cervantes or Cortes as enemies, and watch for whatever their own damaged action does | say: - | expect: It still fires. Four of the fifteen cans already had something in that slot and were **wrapped**, not overwritten -- their `CRandomAction` and `CMultipleActionsAction` survive beside the new call -- *Could break the game*

**English soldiers**

- [ ] `XS16` (qa.md:6303) [eyes + save] where: **Draught, undisturbed.** Hit a Royal Guardsman, English Captain, English Lieutenant and English Bowmaster to under 40% health, then stop damaging that man for three seconds | steps: - | pass: Each logs *"reaches for a healing draught"*, stands fidgeting and does not attack or move, then logs *"drinks a healing draught"* with visibly more health and the Divine Strength effect, and goes back to fighting. A bowman's fidget is sped up, not cut off
- [ ] `XS17` (qa.md:6304) [eyes + save] where: **Draught, spilled.** Same four, but land any hit inside those three seconds | steps: - | pass: About 40% of hits log *"is struck and spills the draught"*: health does **not** rise, and he attacks again at once rather than finishing the fidget. The rest log *"takes the blow and keeps drinking"* and he still heals at the end unless a later hit spills it. Bring him under 40% again: he never reaches for another
- [ ] `XS18` (qa.md:6305) [eyes + save] where: **Killing blow.** Take one from above 40% to dead in a single hit, and kill another mid-fidget | steps: - | pass: The first plays his death and stays down with no *"reaches for"* line; the second stays dead with no heal or effect afterwards

**English soldiers and War Golems**

- [ ] `XS15` (qa.md:6302) [eyes + save] where: **Fresh spawns.** Fight a Royal Guardsman, a Sergeant, a Bowman and a War Golem down past half | steps: - | pass: Each ability prints a line in the log naming the enemy and what it did, once per enemy, and no English bark mentions a shield

**Fernand**

- [ ] `HV6` (qa.md:1832) step: Hover **Fernand** while he is hurt | say: - | expect: `Fernand Desoto (Injured)`. His scripting name is `Distressed Sailor` and only the display name changes, so the label must read the name his dialogue uses. If his hover read something else before, this release changes it

**Gate District; Plains; act 3 Secret Cave**

- [ ] `BW8` (qa.md:2371) step: **Regression.** The other three bows | say: - | expect: Composite Long Bow in the Gate District, Icy Carnage in the Plains, Maelstrom in act 3's Secret Cave, all unchanged at Ranged 50, 85 and 105

**Mongol vendor village; deactivated war golem**

- [ ] `FB11` (qa.md:1764) step: **Negative, the shared cans.** Fight a Mongol vendor-village goblin or a deactivated war golem that is **not** your companion | say: - | expect: They behave exactly as before. Two companion cans are shared with non-companions, and the hook does nothing unless `Fixt Companion Stance` is 2, which a non-companion never has

**Mountain Pass, Alamut or Montaillou**

- [ ] `MB12` (qa.md:2414) step: **Regression, the whole point of the release.** Travel with the boots to a map where Marco has not yet spoken | say: - | expect: He still speaks. Five of the seven are once-only, so pick one you have not triggered: the Mountain Pass, Alamut or Montaillou

**Playtest kit**

- [ ] `TS2` (qa.md:6077) where: Same | steps: Take the **Helm of the Templars**, equip it | pass: Same: it renders at all. It wears `Helmet1`, which is the icon it already had
- [ ] `TS3` (qa.md:6078) where: Same | steps: Equip the helm **and** either Templar shield, and watch AC | pass: **+4 AC** over wearing one of them. This is `Number of Templar Items == 2` in the AC attribute's own Expression. If AC does not move, the set counter is not seeing both
- [ ] `TS5` (qa.md:6080) where: Same | steps: Take the **Aegis**, compare against the Holy Shield | pass: Gold cross where the Holy Shield's is red-outlined, brighter steel, and **two gold lions flanking the stem**. Check the inventory icon and the on-body model agree -- both carry lions

**Port District, Slave Pits, Clan of the Hand A, Cave 3, Hamlet Exterior and others**

- [ ] `FB15` (qa.md:1768) step: **The filter repair.** In Clan of the Hand A, Cave 3, the Slave Pits, Hamlet Exterior, Clan of the Skull B, Hamlet Burned, the Troll Pit, Inquisition Chambers2 or the Port District, stand a companion nearer an enemy than yourself | say: - | expect: That enemy can now attack the companion. **35 pickers** that allowed `Player` alone were widened to `Player,Player Friend`, which is what 547 other pickers in the game already allow

**Sewers / Alamut / Shrine traps**

- [ ] `CR25` (qa.md:1372) where: A trap in any act **outside** the Crypt (the Sewers, Alamut, the Shrine) with no skill at all | steps: Click it | pass: It still disarms for free: the 241 shared-can uses elsewhere in the game are untouched

**Snakebreed Boss, Assassin Master, Bird Man King, Thug Boss, Aka Manah**

- [ ] `FB16` (qa.md:1769) step: **Negative, the bosses.** Fight the Snakebreed Boss, the Assassin Master in the Slave Pits or the Burial Chamber, the Bird Man King, the Juanita shakedown Thug Boss or Aka Manah | say: - | expect: They still focus **you**. Nine boss pickers were left `Player`-only deliberately. Also unchanged: the chickens, the tortured prisoners, the Surrey merchant, the cloned guards, Joan of Arc, the Knight of Saladin, and the **Lost Knight**, who is a recruitable companion

**animals; Sewers creatures**

- [ ] `PS4` (qa.md:2305) step: The same weapon against a **wolf or bear**, and against a **sewer** creature | say: - | expect: Also nothing. Animals and the Sewers are immune too, which is less obvious than the undead and is the part a player is most likely to report as a bug

**any locked chest**

- [ ] `WN9` (qa.md:1523) step: Read **Lockpicking**'s description, then use it on a locked chest | say: - | expect: It says the lock still has to be picked and the wand only makes you better at it. It raises Lockpick for a duration; it does not open anything. Its old text claimed it "will open most non-magical locks", which it never did

**any map with English draught soldiers**

- [ ] `HN2` (qa.md:6222) **NEW** where: Any act with the English draught soldiers | steps: Bring one under 40% health | pass: `<Reaches for a potion>` appears over him as he starts his fidget | new: True

**bonus level**

- [ ] `SN1` (qa.md:5318) [eyes + save] step: Fight a **Super** bow thief, save, run `savecheck events latest --combat` | say: - | expect: Critical hits from the archer, far more often than from a base or Tough bow thief
- [ ] `SN4` (qa.md:5321) step: Judge whether the bonus level is now unfair at range | say: - | expect: **The row that decides whether this stays.** 100 bow thieves stand there

**chests and shield drops**

- [ ] `BK7` (qa.md:6032) where: **The regression that matters.** Open chests and take shield drops away from merchants | steps: Watch what shields appear | pass: Only **Small, Medium and Large**. The buckler is merchant-only by design, so a buckler out of a chest means the `All Shields` can was modified and every drop site in the game is affected

**every wasp map**

- [ ] `QS2` (qa.md:1901) [save] step: **The floor that matters.** A character **above mojo 5** who clears every wasp in the game and the Queen, then counts | say: - | expect: At least five. Before this the worst legal roll gave that player **four**, because the upper bands trade whole-tainted groups for mixed ones with no floor. It is now exactly five, so **do not** let a companion take any of the kills

**goblin camp, Mongol patrol or Troll Pit**

- [ ] `BV2` (qa.md:3479) where: **The row that proves it.** A fight where you are surrounded -- a goblin camp, a Mongol patrol, the Troll Pit | steps: Let a group engage you and watch the hover text | pass: **Noticeably less chatter than before.** There should rarely be two balloons up at once, where previously a crowd produced them faster than once per swing-round

**main menu**

- [ ] `SU1` (qa.md:5417) step: Launch the game | say: - | expect: It reaches the main menu. No "DataCrash Explanation - Fatal Not Found Error" dialog naming `Skills/Fighting/Melee` -- *Launch check; the whole release.*

**shield merchants (Blacksmith, Alvaro, Mauldo, Pierre, Aidan, Traveling Merchant)**

- [ ] `BK1` (qa.md:6025) where: Any shield merchant: the Blacksmith, Alvaro at the Crossroads, Mauldo on the Plains, Pierre, Aidan, the Traveling Merchant | steps: Look at the stock, revisiting if needed | pass: A **Buckler** appears, at roughly one shield in four. If several merchants across a few visits never show one, the placement did not take

**spirit companion: dragon warning, druid finale**

- [ ] `LE6` (qa.md:6403) where: Demonic spirit, karma 800 or below. The dragon warning, and the druid finale | steps: Take any of the three exits | pass: *"Lead the way, O Dark One."* and **you get control back**: the node has to end the spirit's scene. Then repeat above 800: unchanged, and exactly **one** copy of each exit is offered

**thieves, sewer thieves, assassins**

- [ ] `SP1` (qa.md:6376) where: Any `Theif`, `Sewer Theif` or `Assasin`, melee | steps: Hit one until it drops a patch | pass: You **see** spikes on the ground. If you see nothing, the model or `Cur Sequence` is wrong
- [ ] `SP2` (qa.md:6377) where: Same | steps: Stand on the patch | pass: A hit about a second later, with the Spike Hit effect, and the patch is gone
- [ ] `SP3` (qa.md:6378) where: Same | steps: Step off before the tick | pass: No damage, and the patch stays armed

**anywhere in the act**

- [ ] `G10` (qa.md:190) [save] where: Character sheet at rank 3 | steps: Sum the three tiers | pass: Sneak +30, Barter +14, Poison res +35, Disease res +10, Agility +1, carry weight +30
- [ ] `G11` (qa.md:191) [save] where: Character sheet after **each** rank | steps: Check the perk list, not just the stats | pass: A TITLE PERK appears at every rung: `Goblin Chum`, `Goblin Blooded`, `Goblin Champion`
- [ ] `F2` (qa.md:220) [save] do: Compare each rank's bonuses to the one below | expect: Each tier is the running total of everything beneath it. Champion used to cost you Blooded's disease resistance and drop Barter
- [ ] `F6` (qa.md:224) where: Anywhere | do: Read the rank titles you hold | expect: Each describes standing, not a deed you may not have done
- [ ] `P6` (qa.md:285) where: Inventory | steps: Move the pie to a HotKey slot | pass: It is accepted (vanilla could not be slotted at all)
- [ ] `P7` (qa.md:286) steps: Eat it at full health | pass: Poison damage ticks over roughly a minute; not instantly lethal
- [ ] `P8` (qa.md:287) steps: Drop it | pass: Ground pickup model appears and can be picked back up
- [ ] `SR11` (qa.md:811) [save] where: Journal | steps: After SR10 | pass: A quest **Steal from A Noble of the Temple District** with the entry *"Find location in Temple district to thieve"*
- [ ] `S9` (qa.md:1036) where: Any of the above, **not** a Saladin | pass: All of those replies are **absent**. This is the gate-failing-open check
- [ ] `S27` (qa.md:1067) steps: Compare the two blades | pass: Sacred+Flame must still beat Crescent+Flame -- the Crescent never gains the base +5 critical or +10 piercing
- [ ] `MS21` (qa.md:1296) [save] where: Any vodyanoi spawned after install, with the Anatomist perk | steps: Hit one | pass: A second damage entry per landed hit, 4-10 Piercing, in the combat log and on screen. **PASSED** from the save's log
- [ ] `WN2` (qa.md:1516) [eyes + save] step: Cast Lesser Healing from the spell list with charges in hand | say: - | expect: You and a nearby ally heal, the combat log says **The wand discharges.**, and exactly one Wand Charge leaves your pack
- [ ] `WN3` (qa.md:1517) [eyes + save] step: Cast it with **no** charges | say: - | expect: **The wand has no charges left**, and nothing is spent. The silent failure is gone
- [ ] `WN4` (qa.md:1518) [eyes + save] step: **The counting row.** Note how many Wand Charges you hold, then cast until the message changes | say: - | expect: The number of successful casts equals the number of charges you held. If you get fewer, something consumes without delivering; if more, something delivers without consuming
- [ ] `WN11` (qa.md:1525) step: Read **The Swarm**'s description, then look for the spell it names | say: - | expect: It names **Insect Plague**, which is what the wand casts and what the spell calls itself. It used to name "Swarm", and no skill by that name exists anywhere
- [ ] `WI1` (qa.md:1553) step: **The release.** Hold each wand in turn and open the skill window | say: - | expect: **Every wand spell has an icon.** Eight had none: Lightning Bolt, Spike, Fire Circle, Poison Ring, Insect Plague, Ice Storm, Slow and Fear. Their `Image=` had been repointed into `Fake Wand Spells`, where no art exists -- *WI1 proves the release*
- [ ] `WI2` (qa.md:1554) step: Look at the three headers under **Wand Magic** | say: - | expect: Three *different* icons: Fortitude for Charged Spells, Fire for Charged Elements, Wounding for Charged Afflictions. All three were the wand icon before, so the window showed three identical headers
- [ ] `WI3` (qa.md:1555) step: Count the spells under each of the three branches | say: - | expect: **Five each**, no more. No vanilla branch holds more than five and only differentials 0/24/49/74/89/109 exist; Charged Spells held six, the sixth off the ladder at 134
- [ ] `WI4` (qa.md:1556) step: Find **Poisonous Touch** in the skill window | say: - | expect: Under **Charged Afflictions**, bottom row, not under Charged Spells. It moved to a free row; its pin moved with it, 164 to 139, so it still rests uncastable and still lifts to +30 with the wand in hand
- [ ] `WI5` (qa.md:1557) [eyes + save] step: **Negative.** Cast Poisonous Touch after the move, with and without a charge | say: - | expect: Unchanged from 0.88.1: 6 poison a tick for 20 seconds with a charge, **The wand has no charges left** without one. Only its row and its pin changed
- [ ] `WE1` (qa.md:1572) [eyes + save] step: **The release.** Take **Fireball Minor** and charges, equip it, and cast | say: - | expect: A fireball, **The wand discharges.**, one charge gone. This wand has never cast anything: its plugin was disabled before the first cast and its pin read nothing
- [ ] `WE2` (qa.md:1573) step: Cast **Fireball Major** and compare the damage with Minor | say: - | expect: Major hits harder. Minor casts at skill level 5 and Major at 25, which is what vanilla's `skilllevel` always meant, and the pin now sets it
- [ ] `WE3` (qa.md:1574) [eyes + save] step: **Negative.** Cast any of the twelve with no charges | say: - | expect: **The wand has no charges left**, nothing happens, nothing spent
- [ ] `WE4` (qa.md:1575) step: Look in the skill window with a converted wand held | say: - | expect: Three branches under **Wand Magic**: Charged Spells, Charged Elements, Charged Afflictions. The spell your wand grants is in one of them and nothing else is
- [ ] `WE5` (qa.md:1576) step: **The unequip row.** Cast a wand spell, then swap to a different wand | say: - | expect: The spell leaves your list. Each rests below zero and only its own wand's pin lifts it
- [ ] `WE6` (qa.md:1577) [eyes + save] step: Cast **Slowing**, **Poison Rings**, **Fire Circles**, **Spikes** (both), **Lightning Bolts** (both) | say: - | expect: All cast, all spend exactly one charge, all print on success
- [ ] `WE7` (qa.md:1578) [eyes + save] step: **Fire and Ice.** Equip it and look at your spell list | say: - | expect: **Two** wand spells, Fireball and Ice Storm, both castable, each spending a charge. It carried two plugins and nearly lost one in conversion
- [ ] `WE8` (qa.md:1579) step: **The Mage.** Equip it and check your magic skills | say: - | expect: Lightning Bolt and Fear are both castable as wand spells, and **every base magic skill you possess reads 4 higher**. That bonus has never applied: its pin read an expression class that returns nothing
- [ ] `WE9` (qa.md:1580) step: Check Fire and Ice's and The Mage's resistances on the character screen | say: - | expect: Fire and Cold +15 for Fire and Ice; Fire, Cold and Electrical +10 for The Mage. These never applied either, for the same reason
- [ ] `WE10` (qa.md:1581) [eyes + save] step: **The Swarm.** Cast it, and check your piercing resistance | say: - | expect: Insect Plague at skill level 30, one charge, and the ranged damage resistance applies. Its range is preserved as a range, not flattened to one number
- [ ] `WE11` (qa.md:1582) [eyes + save] step: **The regression row.** Equip **Rigor Mortis** with exactly **one** charge. Cast it, spend the charge, then cast again | say: - | expect: The second cast does nothing but say the wand is empty. **Before this it still froze**, because its launcher carried a second copy of the freeze with no charge check. On the first cast the freeze should also apply **once**, not twice
- [ ] `WE12` (qa.md:1583) step: **Negative.** Cast a real Fireball or Lightning Bolt you have actually learned | say: - | expect: Unchanged. The copies are separate skills; your own spells read your own skill and cost mana as before
- [ ] `WE13` (qa.md:1584) step: **Negative.** Check that no wand costs mana | say: - | expect: None does. A wand supplies its own power, so `ManaUse` is cleared on every copy
- [ ] `WE14` (qa.md:1585) step: **The area row.** Cast **Fire Circles**, **Fireballs**, **Poison Rings**, **The Swarm** or **Fire and Ice**'s Ice Storm into a *group* of enemies | say: - | expect: **Everything standing in the circle takes damage**, not just one target and not nothing. These five are aimed at the ground, so their damage had to move inside an area manager; placed at the top of the payload it reached no creature at all and the wand would have spent a charge, said **The wand discharges.** and done nothing -- *WE14 proves the area conversion*
- [ ] `WE15` (qa.md:1586) [eyes + save] step: Cast one of those five at bare ground with nobody near it | say: - | expect: A charge is spent and the message prints, and nothing takes damage. That is correct, and it is also what a broken area spell looks like, so judge this one by `WE14` rather than by this row
- [ ] `WP1` (qa.md:1617) [eyes + save] step: **The release.** Take Poisonous Touch and charges, equip it, and cast at an enemy | say: - | expect: The enemy is poisoned, the effect plays **on it** rather than on you, **The wand discharges.**, one charge gone. 6 poison every 5 seconds for 20 seconds, 24 in all
- [ ] `WP2` (qa.md:1618) step: Count the ticks | say: - | expect: Four of them, five seconds apart, 6 damage each. If the number is 0 the effect is reading an expression off the wrong object again, which is the defect this release found in its own predecessor
- [ ] `WP3` (qa.md:1619) step: Read Poisonous Touch's description against what WP2 showed | say: - | expect: It promises exactly 6 points every 5 seconds for 20 seconds. The numbers are constants on both the skill and the addition precisely so the text and the effect cannot disagree
- [ ] `WP5` (qa.md:1621) step: **Negative.** Try to attack with any wand equipped | say: - | expect: You cannot, and that is vanilla. A wand has no attack behaviour. No wand description promises a strike any more; two did before
- [ ] `WP6` (qa.md:1622) step: **The unequip row.** Equip Poisonous Touch, select its spell, cast, then swap to another wand and try again | say: - | expect: The spell is gone from your list. It rests at -134 and only the wand's pin lifts it. This is the bug reported against 0.87.0 -- *Pin is now 139, not 134, after 0.88.2; the pass condition is unchanged*
- [ ] `WP9` (qa.md:1625) step: **Negative.** Cast Lesser Healing, Greater Healing, Lockpicking, Revelation | say: - | expect: All four unchanged. Only their differentials were touched, and then put back
- [ ] `SG1` (qa.md:1649) step: Get any cloak and drop it on the floor | say: - | expect: A dark crumpled garment, **not an open book**. Plain and enchanted cloaks all resolve to `Cloak_PU`, so every one of the seven enchantments shows it
- [ ] `SG2` (qa.md:1650) step: Drop a cloak and a **chain mail** on the same patch of floor | say: - | expect: They read as the same kind of object at the same scale: 40x31, 562 opaque pixels, luminance 55 against 58, warmth 25 against 25. The cloak borrows that sprite's envelope, so if one looks out of place beside the other the fit is wrong
- [ ] `SG3` (qa.md:1651) step: Look at the drop point | say: - | expect: The cloak sits on the ground, neither floating nor sunk. Hotspot (24, 17), taken from `ChainMail_PU` at the same dimensions
- [ ] `SG4` (qa.md:1652) step: **The row that matters.** Hover the dropped cloak, then pick it up | say: - | expect: The **green pickup cursor**, and it goes back in the pack. The first build of this sprite rendered correctly and could not be picked up -- a spinning cursor -- because a from-scratch icon declares buffers 4/5 empty and **no shipped pickup is single-plane**. The hit test at `0x0055f2a0` needs them. Rendering is not the test; interacting is -- *The row that matters*
- [ ] `SG5` (qa.md:1653) step: Open the inventory with a cloak in it | say: - | expect: Unchanged. Only the ground sprite was touched; the inventory images (`Cloak`, `Cloak Decorated`, `CloakExtra`, `Cloak DecoratedGreen`, `Cloak Special`) are all vanilla and all still resolve
- [ ] `SG6` (qa.md:1654) step: **Negative.** Drop a book, and any armour: chain mail, hauberk, plate, full plate, leather, hard leather | say: - | expect: Every one unchanged. The fix is one file. `Book_PU` in particular must still be a book -- it was the donor the broken cloak was cloned from, and it is used by 14 items including every history book and Shakespeare's works
- [ ] `SD1` (qa.md:1681) step: Buy or find a **Scroll of Healing**. Take damage to roughly half health and read it | say: - | expect: **24-28 points plus 10% of your maximum health**, in one jump. At 100 max HP that is about 36
- [ ] `SD2` (qa.md:1682) step: Read a Scroll of Healing at **full** health | say: - | expect: Nothing is consumed into nothing: the absolute-maximum message, same as a potion. The cap is `1.5 x maxHP - current`, so a full-health read has no headroom
- [ ] `SD4` (qa.md:1684) step: **The row that proves the repair.** On one character, read a Scroll of Healing and drink an **Extra Healing potion** at the same max HP, noting both numbers | say: - | expect: The scroll heals **more** (24-28 + 10% against 18-22 + 10%). Before this it healed *less* (12-14 + 5%) while costing 50 against the potion's 22. If the scroll still heals less, the retune did not take and every other row here still passes
- [ ] `SD5` (qa.md:1685) step: **The row that proves the chain.** Read a **Scroll of Mending** at low health and watch the health bar for twenty seconds | say: - | expect: **Four separate jumps** of 9-11 plus 3% of max HP, five seconds apart, starting immediately. Total about 40 + 12%. **One jump means the delay chain broke** and only the first tick fired, which SD6 and SD7 would not catch -- *One jump means the delay chain broke*
- [ ] `SD6` (qa.md:1686) step: Read a Scroll of Mending, then **keep fighting** through the twenty seconds | say: - | expect: The ticks keep arriving while you swing. This is the case the item exists for, and the one an instant potion cannot cover
- [ ] `SD7` (qa.md:1687) step: Read a Scroll of Mending at **full** health, then take a hit after ten seconds | say: - | expect: The early ticks heal nothing and are **not wasted**: the cap is re-checked per tick, so the ticks after the hit still heal. No absolute-maximum message, by design -- four of them would be spam
- [ ] `SD8` (qa.md:1688) step: **Die** during a Mending chain, or read it and then let a companion die mid-chain | say: - | expect: No crash and no healing of a corpse. Each tick is wrapped in `CIsAliveAction`, the guard `Wound Constrictor` uses
- [ ] `SD9` (qa.md:1689) step: **The risk row.** Read a Scroll of Mending, then **change map** before the twenty seconds are up | say: - | expect: Unknown and untested: nothing in the game runs a delay chain from an item across a transition. Losing the remaining ticks is acceptable; a crash or a stuck effect is not. `Wound Constrictor` proves a delayed heal works from an item, not that it survives a map change -- *Risk row: losing ticks is fine, a crash or stuck effect is not*
- [ ] `SD10` (qa.md:1690) step: With a companion beside you, read a **Scroll of Mass Healing** | say: - | expect: **Both** of you heal 16-20 plus 8% of max HP. Radius 200, categories `Player,Player Friend`. It used to heal the identical amount to its own potion at 75 against 30
- [ ] `SD11` (qa.md:1691) step: With a companion beside you, read a **Scroll of Renewal** | say: - | expect: Both of you heal **four times**, five seconds apart, 7-9 plus 2.5% each. An ally who walks into range after the first pulse is picked up by a later one, because each pulse re-reads who is nearby
- [ ] `SD14` (qa.md:1694) step: **Negative.** Buy or find each of the five ward scrolls -- Acid, Cold, Electrical, Fire Protection, Strength | say: - | expect: Unchanged in every respect: 40 resistance, their own durations, Very Rare and Unique, prices 125 and 350. Only the healing entries were touched
- [ ] `SD15` (qa.md:1695) step: Play a **Demokin with Vampiric Fury** and read each of the four scrolls | say: - | expect: Every heal is **halved** -- 12-14 + 5% for Healing, 8-10 + 4% for Mass Healing, 4-6 + 1.5% per Mending tick, 4-5 + 1.25% per Renewal pulse. Every healing item in the game carries this branch and all four mirror it -- *Needs a Demokin with Vampiric Fury*
- [ ] `SD16` (qa.md:1696) step: Compare a **Scroll of Mending** (110) against a **Superior Healing potion** (150) at around 100 max HP | say: - | expect: Mending totals a little more, about 52 against 48, and takes twenty seconds to deliver it. That is the whole trade the scroll line is built on, and the reason the total is allowed to exceed an instant potion: no tick overheals
- [ ] `FB3` (qa.md:1730) step: *(re-walk, 0.85.1's fix)* Set a companion to **Only fight back**, then let something hit **them** rather than you | say: - | expect: They swing back at what hit them. The forced target decays on their next pick, several times a second, so a burst then a pause is a pass; standing still and taking it is not -- *Re-walk of FB3 under 0.85.2's forced-target fix*
- [ ] `FB1` (qa.md:1754) step: Talk to a companion | say: Let's talk about how you fight. | expect: A second screen, *"How should they handle a fight?"*, offering **Only fight back**, **Fight as you see fit** and **Never mind**
- [ ] `FB2` (qa.md:1755) step: **The row that proves the release.** Set *Only fight back*, then attack something yourself and leave them out of it | say: Only fight back. | expect: They **do not join in**. Confirmed in play: *"fang didn't participate in the wolves i was fighting"*
- [ ] `FB4` (qa.md:1757) [eyes + save] step: **The defect FB3 hid.** After they have fought back, wait, then attack something else yourself and leave them out of it | say: - | expect: They stand down again and stay out of it. The first cut took their filter back and **never gave it up** -- the save showed `Valid Targets=Enemy` with the stance still reading 2, so the menu promised *"Do not start anything"* and after one blow they started things for the rest of the game. They now stand down 8 seconds after the last blow
- [ ] `FB5` (qa.md:1758) step: Set *Only fight back*, then change your mind mid-fight | say: Fight as you see fit. | expect: They resume picking their own targets at once. The stand-down re-checks the stance before firing, so a late timer cannot un-do an order you have just given
- [ ] `FB6` (qa.md:1759) [eyes + save] step: Set a stance on one companion while travelling with two | say: - | expect: Only that one changes. The stance is held **on the companion**, one variable per instance, not fifteen player-scoped flags
- [ ] `FB7` (qa.md:1760) [save] step: Set *Only fight back*, save, reload | say: - | expect: It survives. Read it from the save as `Game Scripting Variables/Fixt Companion Stance=2`
- [ ] `FB8` (qa.md:1761) [eyes + save] step: **Regression.** Release a companion, and ask one how they are holding up | say: Release Companion | expect: 0.84.0's replies are untouched: the report still prints four lines and releasing still prints *"A companion has left your party"*
- [ ] `FB9` (qa.md:1762) step: **Negative.** Check the attributes window | say: - | expect: `Fixt Companion Stance` does not appear. `Display In Attributes Window=0`, cloned from `Fixt Companion Fang`
- [ ] `FB10` (qa.md:1763) step: Recruit each of the fourteen companions in turn and set a stance | say: - | expect: All fourteen obey. Six of them have cans that are **not** named after them -- Bishop Diego is `Diego`, Goblin Girl is `Mongol Vendor Village`, Darsh is `Inquisitor Darsch`, the Golem is `Wargolem Deactivated`, Grace is `Grace OMalley`, Cortes is `Cortez` -- and matching on scripting names alone missed every one -- *Six companions' cans are not named after them*
- [ ] `HV1` (qa.md:1827) [save] step: Click a companion to open the order menu | say: How are you holding up? | expect: The conversation closes and the combat log carries **one line from each group**: how hurt, `Experience: level N`, `Health at full strength: X to Y`, a best-weapon line, `Fighting skill: A to B`. Five lines, no duplicates within a group
- [ ] `HV2` (qa.md:1828) [save] step: HV1 at full health | say: - | expect: `Not a scratch on me.` and nothing else from the health group
- [ ] `HV3` (qa.md:1829) step: **PASSED.** Open the order menu to sync the label, then heal the companion past 75% and open it again | say: - | expect: `Fang (Injured)` and then plain `Fang`. Confirmed in play: *"the injured status was there and then got removed after healing"*. **`CSetCharacterDisplayNameAction` is repeatable** -- it fired twice on one entity in both directions, which no vanilla use does; all six rename the player once inside a conversation -- *Passed in play already*
- [ ] `HV4` (qa.md:1830) step: Drive the same companion below 40%, then below 15% | say: - | expect: `(Badly Injured)` then `(Near Death)`. Healing back up walks the same three states in reverse
- [ ] `HV7` (qa.md:1833) step: **Negative, the one that could break the game.** After a companion has been renamed, level up and watch for the growth balloon | say: - | expect: It still appears over them. The balloon anchors on `Name of Position=Fang` and every quest lookup uses `Name To Check For=Fang`; only the *display* name is rewritten, so nothing that resolves a companion by name may break
- [ ] `HV9` (qa.md:1835) [eyes + save] step: Open the menu on one companion, then immediately on a second | say: How are you holding up? | expect: The second report describes the **second** companion. `Character to get attributes from=$Trigger` must resolve to whoever you clicked
- [ ] `HV10` (qa.md:1836) [eyes + save] step: Report a companion's level against your own | say: - | expect: Plausible, and not stuck at `level 1` for someone who has travelled with you for ten. `CVariableCharacterLevel` has never been read off a non-player character in this project
- [ ] `HV12` (qa.md:1838) [eyes + save] step: Open the menu twice on the same companion and release and re-recruit between | say: - | expect: One watcher, not two. The per-companion `Fixt Companion Health Watch <name>` guard blocks the second install
- [ ] `HV13` (qa.md:1839) step: **The hole HV3 first fell into.** Arm the watcher while the companion is *already* below 75%, then hover without healing them | say: - | expect: The label is correct **immediately**, from the ungated current-band sync. Without that sync nothing appears: `CAIHealthPercentThresholdTrigger` is edge-triggered, so a watcher armed on a wounded companion records their percent as its baseline and fires nothing until they heal past a threshold and come back down. Fang sat at `Previous Health Percent=57.0512` with `Is Valid=1`, a correct six-threshold watcher, and no band at all
- [ ] `HV14` (qa.md:1840) step: Open the order menu twice at different health levels | say: - | expect: The label resyncs each time. The sync is deliberately **ungated** so a missed crossing cannot leave a stale label forever
- [ ] `HV16` (qa.md:1842) step: HV15 on each of the fourteen companions | say: - | expect: All fourteen `Fixt Companion Joined/<name>.can` files now call both installers, outside their own `Fixt Companion <name> == 0` test so a re-recruit arms too. Both installers are internally guarded, so arming twice is a no-op
- [ ] `HV17` (qa.md:1843) step: **Regression on the growth watcher's target.** Level up with a companion present | say: - | expect: The companion gains the modifiers. The growth installer's `CAddAIAction` now targets `Player1` instead of `$Instigator`, because `$Instigator` is only the player when the can is called from a dialogue reply -- pinning it is what lets the Joined cans call it at all. `CXRPGAITriggerWhenLevelUp` must sit on the **player**
- [ ] `HV18` (qa.md:1844) step: Check the attributes window | say: - | expect: None of the fifteen `Fixt Companion Health Watch <name>` variables appear. They carry `Display In Attributes Window=0`, cloned from `Fixt Companion Fang`
- [ ] `WV2` (qa.md:1872) [save] step: Find a fresh stack, in a shop or as loot | say: - | expect: **Two** charges, not five. Vanilla's own pattern: Arrow and Bolt stack 50 at 1 gold, Gem is 1 at 25, so a 50-gold item belongs near the Gem end
- [ ] `WV3` (qa.md:1873) [save] step: Buy or loot several stacks | say: - | expect: They **merge without limit**, as before. `Maximum Count` is still 999 and that is deliberate -- accumulation is fine, and merging is what makes charges work as ammunition at all
- [ ] `WS5` (qa.md:1922) step: Kill a wasp that a **companion or a summon** finishes without you ever damaging it | say: - | expect: **No stinger**, and that is correct, not a bug: the drop is gated on `CWasDamagedByPlayerAction`. Worth knowing before reporting a bad rate
- [ ] `WS8` (qa.md:1925) step: **Negative.** The **Wolf Trapper** perk, with wasps | say: - | expect: **No effect on stingers whatsoever.** It is wolf-specific -- its own checker attribute and its own `Wolf Pelt Perk Quality` item -- and never touched wasps in vanilla or in Fixt
- [ ] `TK1` (qa.md:1937) step: Any character, a cloak and any body armour in the pack | say: Equip the armour, then the cloak | expect: **Both worn at once.** The cloak occupies its own slot; the armour is not displaced. Expect no paper-doll square for it -- equip from the item list, where the equipped background marks it
- [ ] `TK2` (qa.md:1938) step: TK1, holding a second cloak | say: Equip the second cloak | expect: It **replaces** the first. Two cloaks must never both be worn
- [ ] `TK3` (qa.md:1939) step: TK1, holding a second armour | say: Equip the second armour | expect: It **replaces** the first and leaves the cloak alone. **Nothing turns red and nothing becomes unclickable** -- if an item cannot be taken off, the build has regressed to the requirement guard that trapped armour on
- [ ] `TK5` (qa.md:1941) step: Belt of the Thief, then Cloak of the Thief | say: Equip belt first, then cloak | expect: Stealth **+8**, Evasion **+8**, Find Traps = the belt's own figure **plus 15**
- [ ] `TK6` (qa.md:1942) step: The same two items | say: Equip **cloak first**, then belt | expect: Identical to TK5. This is the order that fails if the conditional is read only at equip rather than live
- [ ] `TK7` (qa.md:1943) step: TK5 or TK6 | say: Remove either piece | expect: The cloak drops back to **+4 Stealth, +4 Evasion, +0 Find Traps**; the belt keeps its own bonus
- [ ] `TK8` (qa.md:1944) step: TK5 | say: Equip and unequip each piece **six times**, reading all three skills each time | expect: Every figure returns to exactly its previous value. **Any upward creep in any of the three is the leak** -- 0.83.0's first build added 15 Find Traps and subtracted 0 on every cycle, and a row that only checked "the bonus applies" would have passed it -- *Any upward creep is the leak*
- [ ] `TK9` (qa.md:1945) step: TK5, reading Armor Class | say: - | expect: AC reads **+3** over bare with the set, not +2. Evasion 23 moves `trunc(1 + 0.2*(Evasion-5))` from 3 to 4. This is correct and must not be "fixed"
- [ ] `TK11` (qa.md:1947) step: Any resistance cloak | say: Read its tooltip, then the character window | expect: The tooltip states a figure between 5 and 15 and the window shows that resistance by that amount. **A zero or a mismatch means the addition is still reading the belt's amount** through its cloned self-reference
- [ ] `SC5` (qa.md:2044) step: **The icon.** Open the skills window and look at the staff group | say: - | expect: Centred in its slot, not hard against the left edge
- [ ] `SC6` (qa.md:2045) step: **Regression.** Every other skill group icon | say: - | expect: Unchanged. Only the staff's canvas was resized; its 541 drawn pixels are byte-identical
- [ ] `SB3` (qa.md:2156) step: **Equip the shell** | say: - | expect: It goes in the weapon slot and swings as a club, 1-3 crushing plus the one-handed ladder. Before this it could not be equipped at all, which is the second half of the report
- [ ] `SB4` (qa.md:2157) step: Character sheet, shell equipped | say: - | expect: **No** skill bonuses and **no** Karma change. Both belong to the spirited sceptre only
- [ ] `SB6` (qa.md:2159) step: **Regression.** Equip the spirited sceptre | say: - | expect: 2-8 crushing, +2 to each of the eight Thought and Tribal branches, and the Karma penalty, unchanged
- [ ] `VD1` (qa.md:2173) step: Find a plain **Belt of Voodoo** and read the description | say: - | expect: It names the figure instead of a hardcoded "1 point": "enhances all Tribal spell skills by N". Same for the necklace, the ring and the helm
- [ ] `VD2` (qa.md:2174) step: **Regression, and the common case.** Check that plain belt on the character sheet | say: - | expect: Still exactly **+1** to each of the four Tribal branches. Nothing should have changed for a single-enchantment belt
- [ ] `VD4` (qa.md:2176) step: A **Ring of Divine Attunement** on a richer ring, and a **Helm of the Sylvant** likewise | say: - | expect: 2 to 3 per Divine branch, and 4 to 5 melee, instead of flat 2 and flat 4
- [ ] `VD5` (qa.md:2177) step: **The row that would catch a real break.** Wear the Belt **and** the Necklace of Voodoo together | say: - | expect: The set bonus still fires: **one extra skill point per level up**, counted once for the pair. `Number of Voodoo Items` was deliberately left a literal 1 on each piece; if it had been scaled, one belt would claim to be two items and the set would misfire
- [ ] `VD6` (qa.md:2178) step: **Regression.** `the Sylvant`'s Armor Class and Unarmed bonuses | say: - | expect: Unchanged. Both are race-gated `CIfExpression` modifiers and only the two plain melee skills were scaled
- [ ] `VD7` (qa.md:2179) step: **Regression.** Armour of **"Magery"** (`Mana Stream`) | say: - | expect: Untouched, and that is intentional: it adds +0.4 to a mana-rate attribute whose base is 0.0334, so it already multiplies regeneration about thirteenfold
- [ ] `VD9` (qa.md:2181) step: **Regression.** `Feral Power`, `Wound Constriction` | say: - | expect: Unchanged. Feral Power's value band is inert, so banding it would have been a no-op
- [ ] `VD10` (qa.md:2182) step: Check prices | say: - | expect: No item should cost differently. Each addition's own `Value` field was left exactly as it was; only the band it is read against changed
- [ ] `AR1` (qa.md:2194) step: Find armour **of the Mage** and read its description | say: - | expect: It now names the skill figure instead of promising "+1": "adds +N to each of the magical skill branches". If it still says "+1 skill point" as fixed text, the description edit did not take
- [ ] `AR3` (qa.md:2196) step: On that dear piece, check the four resistances too | say: - | expect: Acid, Cold, Fire and Electrical all around **14 to 20%**, and reaching 20 at 9,000 rather than never. They always scaled; only their ceiling moved
- [ ] `AR4` (qa.md:2197) step: **Regression.** A **cheap** piece of the Mage | say: - | expect: Identical to before: 5% resistances, +1 skill. The floor was deliberately left alone, checked at 3,000 price points
- [ ] `AR5` (qa.md:2198) step: Armour of **Deepest Winter**, 9,000 gold or more | say: - | expect: The frost aura reaches its full **7** damage. Its band is unchanged at 2/4/7; only the value it is read against moved
- [ ] `AR6` (qa.md:2199) step: **Regression.** A cheap piece of Deepest Winter | say: - | expect: Unchanged, 2 damage
- [ ] `AR7` (qa.md:2200) step: **Regression, and the thing most likely to be wrong.** Check the Mage's **twelve** branches, not just the one you use | say: - | expect: Divine, Elemental and Tribal branches should all move together. Twelve modifiers share the one expression, so if any branch is still stuck at +1 the edit reached only some of them
- [ ] `AR9` (qa.md:2202) step: **Regression.** The three amulet auras from 0.75.2, Icy Fury, Acid Touch and Lava Burn | say: - | expect: Unchanged at 2-7. Deepest Winter shares their plugin and was checked against them rather than raised past them
- [ ] `SC1` (qa.md:2215) step: A **dear** melee weapon of Snakebiting, 7,000 gold or more | say: - | expect: Back to "an extra **6** points of damage every 5 seconds for 20 seconds", not 27
- [ ] `SC2` (qa.md:2216) step: A dear weapon of **Venom** | say: - | expect: Per-tick back in the **4 to 20** range, not 18-91. Chance still reads **50%**
- [ ] `SC4` (qa.md:2218) step: **The other fix that must survive.** Confirm both reach their stated maximum on a 7,000 gold weapon | say: - | expect: They do. Their value ceilings stay at 7,000; vanilla's 10,000 and 10,500 were reached by no melee weapon in any save
- [ ] `SC5` (qa.md:2219) step: Compare Snakebiting against a weapon of **Double Biting** on similar weapons | say: - | expect: Snakebiting a little stronger: 1.20 a second against 0.90. Both are damage-over-time, which earlier notes got wrong about Double Biting
- [ ] `SC6` (qa.md:2220) step: Compare either against a **monster's** poison -- a wasp, a desert beast, a snakebreed's spit | say: - | expect: The same order of magnitude. Monster poisons run 0.20 to 0.60 a second through the game's shared tiers; a weapon suffix sitting at 1.20 is the top of the scale, not a different class
- [ ] `SC7` (qa.md:2221) step: **Still the open question.** On a **100+ hit point** target, hit repeatedly and watch the size of each health-bar drop | say: - | expect: The drops do **not** grow. Re-applying refreshes, it does not stack. Untested in play so far: every wolf died to the first application -- *Still the open question: refresh vs stack*
- [ ] `SC10` (qa.md:2224) step: **Regression.** A **cheap** weapon of either poison | say: - | expect: Unchanged from vanilla. Only the value ceiling and, for Venom, the 0.77.0 damage rewire differ from vanilla at all
- [ ] `DT5` (qa.md:2262) step: **The row most likely to look like a bug.** Kill something weak in two or three swings | say: - | expect: It dies to your melee alone and takes **no poison damage**, because the first application is 5 seconds out. Intended, and why the numbers are deliberately short of parity. You will still see the `infected` line on the hit
- [ ] `DT7` (qa.md:2264) [eyes + save] step: **Regression.** Venom's chance -- and the log measures this one exactly | say: - | expect: Count `infected` lines against your landed hits: about **half** on a dear weapon, 1 in 20 on a cheap one. The chance band is untouched at 5/25/50
- [ ] `DT8` (qa.md:2265) step: **Regression.** Both durations | say: - | expect: Snakebiting still 20 seconds, Venom still 10. Only the per-tick amount moved
- [ ] `PO2` (qa.md:2283) step: A dear weapon of **Venom**, 7,000 gold or more | say: - | expect: Noticeably more poison than before, about 12 a swing against 9
- [ ] `PO6` (qa.md:2287) step: Hit an **undead** with either weapon | say: - | expect: No poison damage at all. Not less, zero. Same immunity shape as Pestilence
- [ ] `PS1` (qa.md:2302) step: Find or buy a **dear** melee weapon of Pestilence, several thousand gold, and read the tooltip | say: - | expect: Promises up to **26**, not 14
- [ ] `PS3` (qa.md:2304) step: **The row that proves the gate.** Hit a bandit or a goblin with it, then hit any **undead** with the same weapon | say: - | expect: The living target takes a large extra hit; the undead takes **nothing at all**. Not "less" -- zero. Undead are 4,334 of the 5,783 immune spawns
- [ ] `PS6` (qa.md:2307) step: **The row that proves nothing got worse.** A **cheap** weapon of Pestilence, a few hundred gold | say: - | expect: Identical to before, not merely close. The median case was held to the digit by keeping vanilla's slope; checked at 904 price points
- [ ] `PS7` (qa.md:2308) step: Compare it against a weapon of **Flame** or **Cold Biting** on a similarly dear weapon, against a **living** target | say: - | expect: Pestilence should hit noticeably harder, 15.5 against 11.0 to 13.5. That is what it is paid for having a 37% blind spot
- [ ] `RC1` (qa.md:2323) step: Find or buy a **dear** melee weapon of Acid, several thousand gold, and read the tooltip | say: - | expect: Promises up to **19**, not 12
- [ ] `RC2` (qa.md:2324) step: A dear weapon of **Cold Biting** | say: - | expect: Up to **24**, not 15
- [ ] `RC3` (qa.md:2325) step: A dear weapon of **Flame** or **Shocking** | say: - | expect: Up to **22** and **21**, not 15
- [ ] `RC4` (qa.md:2326) step: **The row that proves the ceiling is reachable.** Compare the tooltip maximum against the damage you actually roll on a weapon worth about 7,000 or more | say: - | expect: The rolls should reach near the stated maximum. This is the whole point of the release: before it, Flame and Shocking stated 15 at a price band topping at 10,000 that **no melee weapon in any save reaches**, so the number was unreachable
- [ ] `RC5` (qa.md:2327) step: **The row that proves nothing got worse.** A **cheap** weapon of any of the four, a few hundred gold | say: - | expect: The same as before or very slightly better, never worse. Checked at 904 price points against the pristine archive, but this is the one a player would notice
- [ ] `RC6` (qa.md:2328) step: Look at the **low end** of the damage range on a mid-priced weapon | say: - | expect: Unchanged or a touch higher. Raising the band ceiling alone would have dropped it about 1.3%, which is what the min term's output ceiling moving in step prevents
- [ ] `RC7` (qa.md:2329) step: **Regression, and the most important one.** A weapon of **Carnage** | say: - | expect: Completely unchanged. Carnage was deliberately not touched, in either this release or 0.77.0
- [ ] `RC9` (qa.md:2331) step: **Regression.** A weapon of **Ripping** | say: - | expect: Unchanged, 4/12/20
- [ ] `RC13` (qa.md:2335) step: Compare the four against each other on similarly priced dear weapons | say: - | expect: They should feel about equal. After the bestiary they land within 0.11 of each other, which has never been true of this family: cold's bigger number exists because only 81% of cold damage lands, against acid's 99%
- [ ] `GS1` (qa.md:2349) step: Find a weapon of **Hunting** worth about 10,000 and read its tooltip | say: - | expect: Promises up to **30**, not 15
- [ ] `GS2` (qa.md:2350) step: **The row that proves the gate still works.** Hit a bear or a wolf with it, then hit a wererat or a thief with the same weapon | say: - | expect: The animal takes a large extra hit; the wererat and the thief take **none**. If both take it, the category check broke; if neither does, the bonus is not firing at all
- [ ] `GS3` (qa.md:2351) step: **The row that proves the band was rewired, not just the ceiling.** Find a **cheap** weapon of Hunting, a few hundred gold | say: - | expect: Still a small bonus, roughly 5 to 7. If a cheap weapon now hits for 20 the `min` scale's input range did not move with the band
- [ ] `GS6` (qa.md:2354) step: The same Goblin Slaying weapon anywhere outside the Wilderness and Barcelona | say: - | expect: Nothing. It is a swap weapon by design, and that is why its number is the biggest of the three -- *Any map outside the Wilderness and Barcelona*
- [ ] `GS7` (qa.md:2355) step: **Resistance check.** Use any of the three against an enemy with high fire or cold resistance | say: - | expect: The bonus still lands in full. All three deal acid, which only 37 races resist
- [ ] `EL7` (qa.md:2363) step: **Regression.** 0.75.0's three chance-gated suffixes, Demonic Bile, Lightning and Firestorms | say: - | expect: Unchanged from 0.75.0, still landing around 12 a hit
- [ ] `BW3` (qa.md:2366) step: Read the bow's requirement with a low Ranged skill | say: - | expect: Needs **Ranged 125** and cannot be equipped yet. Finding it before you qualify is intended; growing into it is the point of moving it earlier
- [ ] `EL1` (qa.md:2384) step: Find or buy a ring of **Killing Frost** | say: - | expect: +20% Cold Damage, matching Fiery Death's fire. 5 Unique, so shop restocks beat chests
- [ ] `EL2` (qa.md:2385) step: A ring of **Thunderstroke** | say: - | expect: +20% Electrical Damage
- [ ] `EL3` (qa.md:2386) step: **Regression.** A ring of Fiery Death | say: - | expect: Still +20% fire, unchanged
- [ ] `EL5` (qa.md:2388) step: Buy the **Gauntlets of Hoarfrost** and wear them | say: - | expect: +25% Cold Damage **and +5 Cold Damage Threshold** on the sheet
- [ ] `EL6` (qa.md:2389) step: **The row that could come back wrong.** Check the threshold is really applied, not just printed | say: - | expect: No item in the game has ever granted a Cold or Electrical damage threshold. If the number does not move, these two need the threshold removing and only the 25% keeping -- *If the threshold does not move, report it: the release says drop it.*
- [ ] `EL7` (qa.md:2390) step: The **Gauntlets of the Tempest** | say: - | expect: +25% Electrical and +5 Electrical Threshold
- [ ] `EL8` (qa.md:2391) step: **Regression.** Gauntlets of Hellfire | say: - | expect: +25% fire and +5 fire threshold, unchanged, and still first on his list
- [ ] `EL9` (qa.md:2392) step: Look at all six icons together | say: - | expect: Three rings and three gauntlets, each readable as fire, ice or lightning at inventory size. The rings keep their jewel; the gauntlets keep their studs
- [ ] `EL10` (qa.md:2393) step: **Regression.** The six Carnage necklaces from 0.75.1 | say: - | expect: Unchanged, 5-15% each. Nothing in this release touched them
- [ ] `MB9` (qa.md:2411) step: Wear the boots and read the sheet | say: - | expect: Carry weight **+60**, not +20. The tooltip still says 20; that is deliberate, the perk's own text supplies the other 40
- [ ] `MB10` (qa.md:2412) step: **The row that catches the worst failure.** Take the boots off, read the sheet, put them on, read it again | say: - | expect: Off: the bonus is gone **entirely**, including the base 20. On: +60 again and **not +120**. A growing number means the modifier is stacking and the release should be pulled -- *A growing carry weight means stacking: pull the release.*
- [ ] `MB11` (qa.md:2413) step: Walk around with them on and off | say: - | expect: Slightly faster with them on. 5% is small; the sheet is the better check if the game shows it
- [ ] `AT1` (qa.md:2429) step: Find or buy an expensive Belt of Titan Strength or Titan Endurance | say: - | expect: **+3**, where vanilla always said +2. 9000 gold or more
- [ ] `AT2` (qa.md:2430) step: A cheap one | say: - | expect: Still **+2**. Today's value is the floor, so nothing in this release can be worse than vanilla
- [ ] `AT3` (qa.md:2431) step: **The row the rule rests on.** A mid-priced one, around 4000 to 6000 | say: - | expect: +2 or +3. If the game shows a fraction such as **+2.2**, say so: the engine interpolates linearly and whether it floors is the open question behind this whole release -- *Report any fractional value such as +2.2.*
- [ ] `AT4` (qa.md:2432) step: Equip it and read the character sheet, not the tooltip | say: - | expect: The attribute really moves by the number the tooltip claims, and drops back when the item comes off
- [ ] `AT5` (qa.md:2433) step: A Shield of the Charismatic Totem, expensive | say: - | expect: +3 Charisma. All three shield sizes were changed, so check whichever you find
- [ ] `AT6` (qa.md:2434) step: A Necklace of Necromancy | say: - | expect: Up to **+25** Summoning on a dear one, where vanilla always said 10. It reaches its ceiling by about 3500 gold
- [ ] `AT7` (qa.md:2435) step: Armour of Giant Strength, a Gauntlet of Heroic Strength, a Helm of Focused Logic | say: - | expect: Up to +2 each, +1 at the bottom. These were flat +1
- [ ] `AT8` (qa.md:2436) step: A Cloak of Charisma | say: - | expect: +2 rising to +3 by about 3500 gold
- [ ] `AT9` (qa.md:2437) step: **Regression.** Anything with `Mastery`, `Haste`, `Speed` or `Lethargy` | say: - | expect: Unchanged and still flat. Rates and multipliers were deliberately left out
- [ ] `AT10` (qa.md:2438) step: **Regression.** The six Carnage necklaces and the three aura amulets | say: - | expect: Unchanged from 0.75.1 and 0.75.2
- [ ] `AU2` (qa.md:2453) step: Read each tooltip | say: - | expect: *"Inflicts 2-7 points of cold / acid / fire damage to any enemy within melee range of the character."* Vanilla said 1-3
- [ ] `AU3` (qa.md:2454) step: **The row that has never been run, in vanilla or here.** Wear one, stand next to something hostile and do nothing | say: - | expect: It takes damage about every two seconds without you attacking. **If nothing happens, the aura is dead in vanilla too** and that is a separate bug worth a report of its own -- *If nothing ticks, the aura is dead in vanilla too: separate report.*
- [ ] `AU4` (qa.md:2455) [eyes + save] step: Watch the combat log while it ticks | say: - | expect: 2 to 7 of the right damage type, and the figure respects the target's resistance to it
- [ ] `AU5` (qa.md:2456) step: Stand further away | say: - | expect: It stops. The radius is 110 and was not changed
- [ ] `AU6` (qa.md:2457) step: **Regression.** A suit of armour of Deepest Winter, if you have one | say: - | expect: Unchanged, 1-2 to 2-7 every six seconds in radius 80. It was the reference for this release, not a target of it -- *0.79.0 lowered its value ceiling to 9000; the 2-7 range is unchanged.*
- [ ] `AU7` (qa.md:2458) step: **Regression.** `Evasion` and `Luck`, the other two UNIQUE additions | say: - | expect: Unchanged. Only the three aura files were edited
- [ ] `CN1` (qa.md:2468) step: **The row the report is about.** Find or buy an expensive necklace of any Carnage and read it | say: - | expect: 15%, where it used to say 10%. 4000 gold or more for Crushing, Piercing or Slashing; 3500 for Fire, Cold or Electrical
- [ ] `CN2` (qa.md:2469) step: A cheap one, early game | say: - | expect: It **exists**, which it could not before, and reads 5%. The band's floor dropped from 3700 to 400
- [ ] `CN3` (qa.md:2470) step: Wear one and check the damage it names | say: - | expect: The bonus matches the number in its own tooltip. Both are read from the same expression, so a mismatch means the modifier is not reading it
- [ ] `CN4` (qa.md:2471) step: Read the sentence itself | say: - | expect: Unchanged except the number, including the double space in Fire Carnage's *"enhanced  15%"*. If any of the six reads differently from vanilla, the prose edit went too far
- [ ] `CN5` (qa.md:2472) step: **Regression.** The necklace's price in a merchant window | say: - | expect: Still 3700 or 4000. The addition's `Value` was deliberately not touched, only its band
- [ ] `CN7` (qa.md:2474) step: **Regression.** 0.75.0's work, a weapon of Firestorms or Lightning and a Shield of the Frostwyrm | say: - | expect: Unchanged from 0.75.0
- [ ] `IB1` (qa.md:2488) step: **The row the report is about.** Find or buy an expensive weapon of Firestorms or of Lightning and read its tooltip | say: - | expect: The chance is well above the old flat 10% and 5%, up toward 50% on a dear weapon, and the damage range is wider: Lightning to 38, Firestorms to 44
- [ ] `IB3` (qa.md:2490) step: A weapon of Demonic Bile | say: - | expect: Chance up to 12% on a dear one, and the 40 to 105 damage untouched. It is still the lottery the text describes, now priced like one
- [ ] `IB4` (qa.md:2491) step: **Regression, the floor.** A cheap weapon of Firestorms, early game | say: - | expect: Still 10%. The chance scales from today's value, so nothing at the bottom of the curve moved
- [ ] `IB6` (qa.md:2493) step: A Shield of the Frostwyrm | say: - | expect: The tooltip now names three bonuses, and the One-Handed Melee one runs 5 to 20 with the shield's price exactly as the Firedrake's does
- [ ] `IB7` (qa.md:2494) step: Equip it and open the skill window | say: - | expect: One-Handed Melee is higher by the number the tooltip claims, and drops back when the shield comes off
- [ ] `IB8` (qa.md:2495) step: **Regression.** A Shield of the Firedrake | say: - | expect: Unchanged, all three bonuses as before. The Frostwyrm was cloned from it; it was not edited
- [ ] `IB9` (qa.md:2496) step: **Regression.** The Frostwyrm's cold resistance and cold damage | say: - | expect: Unchanged. Only the third modifier was added, and the two curves were not touched
- [ ] `WC1` (qa.md:2524) step: **The row that matters.** Get a newly generated wand of Revelation, Lockpicking, Lesser Healing, Greater Healing or Rigor Mortis, and some Wand Charges | say: Equip the wand, pick its spell out of **Wand Magic > Charged Spells**, cast it | expect: It casts and the effect lands. All five were uncastable in vanilla, gated behind `Display and Cast Requirements=CIsEqualTo(0,1)`
- [ ] `WC21` (qa.md:2529) step: **Charges drop.** Open chests over a long session | say: Watch for Wand Charges | expect: They appear at **weight 2** in `All Misc Items except Potions`, the same weight as a wand, so a stack of five turns up about as often as a wand does -- *Stacks are now 2, not 5 (0.83.4).*
- [ ] `WC19` (qa.md:2530) [eyes + save] step: **A crossbow cannot eat your charges.** Carry Wand Charges and bolts, equip a crossbow and fire it | say: Watch both stacks | expect: Bolts fall, charges do not. The charge sits in no slot at all, `Slot Used In=Character Slot Types/!None`, the shape eight vanilla pack stackables use
- [ ] `WC4` (qa.md:2531) [eyes + save] step: **An empty wand does nothing and says so.** Spend every charge, then cast again | say: Watch for floating text | expect: `The wand has no charges left`, no effect, nothing consumed, and **the wand stays in the pack**. It is useless, not destroyed: nothing in the engine can destroy it at the right moment -- *Overlaps WN3 (line 1517) except the wand-stays-in-pack half.*
- [ ] `WC5` (qa.md:2532) step: **Anyone can use it.** Repeat WC1 on a character with no magic skill at all | say: - | expect: Identical. The pin sets the spell's level, so a fighter casts it exactly as a mage does
- [ ] `WC6` (qa.md:2533) step: **Nobody gets them free. This row caught a real defect in play.** Hold no wand | say: Open the skill window and **read the number** on each of the five | expect: Each reads **0 or negative** and refuses to cast. The resting value is `parent - differential` against a parent pinned at 0. **If any reads 450**, a pre-made character file is still baking it: that number lives in `Preexisting Characters/*.Character.txt`, not in any `.Skill`
- [ ] `WC7` (qa.md:2534) step: **A buffed caster still gets nothing.** Max Divine Protective, take the perks, hold no wand | say: Try to cast | expect: Refused. The five hang off a group whose value nothing can move, so no branch bonus can reach them
- [ ] `WC8` (qa.md:2535) step: **One wand, one spell.** Collect wands from the organ and from chests | say: Read each name | expect: `Wand of <one spell>`, optionally with a non-wand bonus after it such as `, Evasion`. **A second spell, or the same one twice, means the additions are back in `Wand Additions`** and the generator is stacking them
- [ ] `WC10` (qa.md:2537) step: **The sign error.** Rigor Mortis, cast at an enemy | say: - | expect: It stands still about 5 seconds, then moves and attacks **slowly**. Vanilla stored `amount=75` on a percent modifier, which would have made it 75% faster
- [ ] `WC11` (qa.md:2538) step: **The friend filter.** Greater Healing, with an ally beside you and an enemy adjacent | say: - | expect: You and the ally heal 19-23. The enemy does not. The `CCheckCategoryAction{Player,Player Friend}` filter is lifted from the real `Healing.Skill`
- [ ] `WC12` (qa.md:2539) step: **Lesser Healing actually heals.** Take damage, cast it on yourself | say: Watch Hit Points | expect: Up by 10 to 13. It read 0 before, because the amount was fetched from the item rather than declared on the spell
- [ ] `WC13` (qa.md:2540) step: Lockpicking | say: Cast it, then try a lock previously refused as too complex | expect: It opens. +50 covers 188 of the 197 locks carrying a numeric `Lock Pick Adjustment`; the nine it misses sit at -300, the game's not-pickable marker
- [ ] `WC14` (qa.md:2541) step: Revelation | say: Cast it, then read the character sheet | expect: Find Traps/Secret Doors up by **60**, falling back after 30 seconds
- [ ] `WC16` (qa.md:2543) step: **Regression, and the one that would break something invisible.** Fight anything that casts Magical Shield at you | say: - | expect: Still cast. `ENEMY Magical Shield` is parented to `Fake Wand Spells/Cure Major Wounds`, which is why that file was left alone
- [ ] `WC18` (qa.md:2545) step: **The rename.** Look at the Lesser Healing wand and at Divine > Protective | say: - | expect: The item reads **Lesser Healing** and does not collide with the real `Healing` spell in that branch
- [ ] `CG1` (qa.md:2604) step: **The row that decides the feature.** Recruit Cervantes, then level up with him beside you | say: - | expect: He says *"I am writing all of this down. Including the parts where I improve."* If no line ever appears, `CXRPGAITriggerWhenLevelUp` does not fire and the timer fallback is needed
- [ ] `CG2` (qa.md:2605) [save] step: **The row that proves the grant, not just the line.** Level up a few times with him, then `python tools/savecheck.py grep Cervantes --save latest` | say: - | expect: His `Derived Character Attribute Permanent Modifiers` has grown by 9 HP and 8 AC per level
- [ ] `CG3` (qa.md:2606) step: **The row that stops the watcher installing twice.** Click a companion several times, dismiss and re-recruit, then level | say: - | expect: Exactly one line per companion per level, never two
- [ ] `CG4` (qa.md:2607) [save] step: A tier B companion: level up beside Joan of Arc or Grumdjum | say: - | expect: +5 HP and +3 AC, not +9 and +8
- [ ] `CG5` (qa.md:2608) step: Two companions at once | say: - | expect: Both speak, each in their own voice
- [ ] `CG6` (qa.md:2609) [eyes + save] step: **Regression.** Beatrice | say: - | expect: No line, no grant, ever. She is excluded on purpose
- [ ] `CG7` (qa.md:2610) step: **Reaches a save in progress.** On a save that already has a companion, click them once, then level | say: - | expect: The line appears. This is the point of installing from the companion overlay's tree rather than from a map -- *Since 0.84.0 the join cans arm growth, so this is moot on a new game.*
- [ ] `CS8` (qa.md:2760) [eyes + save] step: **Attributes window** | say: - | expect: `Fixt Cathedral Summit Done` does not appear. It is a scripting variable with `Display In Attributes Window=0`, like `Fixt Undead Warning Given`
- [ ] `TG4` (qa.md:2810) step: Sell one of each | say: - | expect: Sphere **100**, crystal **200**. The sphere now matches all four Stone Hearts and Lucius' Mneme; the crystal is double, as the rarer organ
- [ ] `TC2` (qa.md:2823) step: **The row that matters.** Look at it in your inventory | say: - | expect: **Green over the whole icon**, not green at the edges and violet in the middle. The whole-image recolour is the point of this release; a partial one would look exactly like a bug
- [ ] `TC7` (qa.md:2828) step: **Regression.** Check every other inventory icon you own | say: - | expect: Unchanged. An identity recolour reproduces all 259 of the game's icons byte for byte, both planes included
- [ ] `RT3` (qa.md:2839) step: Pick it up and find it in your inventory | say: - | expect: **Blue**, under **Miscellaneous**, not under Quest Items. The four Stone Hearts are the amber version of the same shape and stay amber
- [ ] `AT7` (qa.md:2904) step: Let one of them drop combat and provoke the same character again | say: - | expect: The line plays **once**. The transition is `Trigger=First Time`, which is what Brother Michel's uses
- [ ] `SN1` (qa.md:2916) step: Open a conversation with your spirit and reach its hub, *"do you have other questions for me, or can we resume our journey together?"* | say: - | expect: A new option, **"What is your name?"**, above *"I tire of your counsel"*
- [ ] `SN2` (qa.md:2917) step: Take it | say: - | expect: **With voiceover.** Elemental: *"I am Armati, a divine spirit, one of the amesha spentas of fertility of the earth."* Demonic: *"Moi? I am the patron saint of discontentment... know me as Saurva."* Beast: *"Far to the east I was called Raiju, the thunder beast..."*
- [ ] `SN3` (qa.md:2918) step: **The row that matters.** Click through the answer | say: - | expect: You are **back at the hub**, able to ask the next question. Not dropped out of the conversation, and not stuck with the controls locked
- [ ] `SN4` (qa.md:2919) step: **Beast spirit only.** On the hub, take **"What of good and evil?"** | say: - | expect: *"Such concepts of good and evil are unknown to animals... mortals that fail to achieve perfection in life, return as animals in their next life to help the balance."* With voiceover, then back to the hub
- [ ] `SN5` (qa.md:2920) step: On the other two spirits, count the hub's options | say: - | expect: **Six**, not seven. Only the Beast has the good-and-evil answer recorded
- [ ] `SN6` (qa.md:2921) step: **Regression.** Ask the three questions that were always there | say: - | expect: Unchanged, and each still returns you to the hub
- [ ] `SN7` (qa.md:2922) step: **Regression, inside a scene.** Trigger a spirit scene that locks your controls (a mana pickup, or a cave warning), ask the name there, then leave through *"Thank you, spirit. Let's continue on."* | say: - | expect: Your controls come back. The new answers exit through the hub's own goodbyes, which already end the sequence
- [ ] `DF9` (qa.md:2957) step: **Regression, any save with the Beast spirit.** Talk to it, work to its introduction (*"I am a spirit that has lived in your family for generations"*) and take *"I tire of your counsel. Begone."* | say: - | expect: *"Stay cautious and trust your senses."* Vanilla named a node the beast tree does not have, so the dismissal answered with nothing
- [ ] `DV1` (qa.md:2966) step: Ask him about the Daevas and hear the lecture out to its last part | say: - | expect: A new third option: *"You keep saying *so-called* Divine Ones. What are they?"*
- [ ] `DV2` (qa.md:2967) step: Take it | say: - | expect: 414 KB of him on the Ahura Spentas, the Cherubim and the Ombwiri, ending *"if you ask me, which you did"*. **With voiceover**
- [ ] `DV3` (qa.md:2968) step: From there, ask *"What is a Daeva?"* | say: - | expect: It loops back into the Daeva explanation, which runs on to its last part again. No dead end
- [ ] `DV4` (qa.md:2969) step: **The row that matters most.** Take *"I've heard enough"* from the Divine answer | say: - | expect: The scene ends and your controls come back. This conversation runs inside a non-interactive sequence, and every exit the new path can reach has to fire `end spirit nis`
- [ ] `DV5` (qa.md:2970) step: **Regression.** Count the options on his Divine answer | say: - | expect: **Two**, not three. Vanilla had two identical *"What is a Daeva?"* replies and the second led to a node that does not exist in his tree
- [ ] `HR35` (qa.md:2987) step: **Regression.** Any other map that was fine before | say: - | expect: Fine. The broken file was new in 0.60.5 and is referenced only by the horse -- *Implicit in the whole playtest.*
- [ ] `FN14` (qa.md:3015) [save] step: Take him as a companion and get into a fight | say: - | expect: The log names him Fernand Desoto on every line about him
- [ ] `UE7` (qa.md:3077) step: **Regression.** Pick up a spirit-mana charge for the first time on a fresh character | say: - | expect: The *mana* scene still plays normally. The new can is a copy of it and must not have disturbed it
- [ ] `CV6` (qa.md:3321) step: Travel with **Cortes** after the install and fight beside him | say: - | expect: *"Por Espana!"*, *"You are a fool to attack a conquistador of Espana!"*, *"For God and Espana!"* or *"By my father's sword, I will be victorious!"* About one per ten of his attacks -- *Needs Cortes in the party.*
- [ ] `CV7` (qa.md:3322) step: Let Cortes take hits in a fight | say: - | expect: *"I need assistance!"* or *"I need healing - I will perish soon!"*, about one damage event in twelve
- [ ] `CV8` (qa.md:3323) step: Fight a long stretch beside **Cervantes** | say: - | expect: *"Ah hah! Beast, you will not survive my flashing blade!"* -- **rare on purpose**, about one in sixteen of his attacks, because it is the only attack line he has -- *Needs Cervantes in the party.*
- [ ] `CV10` (qa.md:3325) step: Let an enemy wound Cervantes while he travels with you | say: - | expect: *"Ayudame! Help me squire!"* or a pained grunt, occasionally
- [ ] `WT2` (qa.md:3441) where: A **newly generated** `Revelation` wand (not one you already owned) | steps: Read its description | pass: It says **"The wielder of this wand receives 60 skill points..."** -- not "the target"
- [ ] `WT5` (qa.md:3444) where: **Was known-broken, fixed in 0.52.3 -- this row now means the opposite.** A newly generated Lightning, Fireball, Spikes, Slow, Poison Ring, Fire Circle or Swarm wand | steps: Read its description | pass: It reads **`at skill level 5`** (or 10, 15, 20, 25, 30 -- Lightning/Fireball /Spikes Minor 5, Fire Circle 10, Slow 15, Poison Ring 20, Lightning/Fireball Major 25, Swarm 30). **`(Could not evaluate expression)` is now a FAILURE**, as is a negative number. The wand pins your effective skill to that level while selected, so the number is what you cast at regardless of your own skill
- [ ] `WT6` (qa.md:3445) where: Fire a `Revelation` wand, then check your own character | steps: Look at Find Traps/Secret Doors | pass: **Your** skill went up by 60 for 30 seconds. This confirms the reworded text is the accurate one -- the mechanic was always the wielder
- [ ] `BV1` (qa.md:3478) where: **The pull-trigger row.** Any fight with goblins, thieves, English soldiers, trolls or Snakebreed | steps: Fight for a minute or two | pass: **Barks still appear.** Floating text over a creature's head. Fewer than before, but present -- if none appear at all in several fights, the splice is broken, not the number
- [ ] `BV3` (qa.md:3480) where: One enemy, alone | steps: Fight a single goblin or thief | pass: It still barks, and a solitary fight should feel **much closer to before** than a crowded one does -- the wounded hook was left alone precisely so this case did not go quiet
- [ ] `BV4` (qa.md:3481) where: Wound something and let it live | steps: Hit a creature, back off, hit it again | pass: **Wounded barks fire at exactly their old rate.** This hook was not changed. If these feel rarer than they used to, say so -- it would mean the swing cut is reading as an overall cut and the two hooks need looking at together
- [ ] `BV6` (qa.md:3483) where: Any **archer** can -- Mongol Goblin Archer, Soldier2 Bow, Sewer Theif3 Bow | steps: Fight one at range | pass: It still shoots. `CActionSelectSkill` in the padding is what selects the ranged attack, so an archer that has stopped using its bow would mean the padding was damaged
- [ ] `BV7` (qa.md:3484) where: **The judgement row.** After a few hours | steps: - | pass: Is the swing rate right now? If crowds are still loud, the attack hook comes down again. If crowds are good but the game overall feels too quiet, the wounded hook is the one to *raise* -- it is still at its original 1/6 and is the hook carrying the reactive lines
- [ ] `AM1` (qa.md:3507) where: Anywhere with chests or ammunition drops | steps: Collect ammunition over a normal play session | pass: Arrows and bolts drop as they always did. Most are plain
- [ ] `AM3` (qa.md:3509) [eyes + save] where: Same, for arrows | steps: - | pass: Enchanted **arrows** appear too, outside the Sewers. They were previously reachable from one map in two hundred
- [ ] `AM4` (qa.md:3510) where: Equip an enchanted bolt in a crossbow and shoot something | steps: - | pass: The enchantment does what it says -- extra damage, a better chance to hit, or elemental damage of the right type. These additions are vanilla's own and were always implemented; only the route to them was missing
- [ ] `AM5` (qa.md:3511) [eyes + save] where: **The control, and the one that matters most.** Play normally and pay attention to ammunition | steps: - | pass: **Ordinary arrows and bolts are still the common case** -- roughly ten of eleven. If most ammunition is suddenly magical, the weighting is wrong and should come down. This file is used by 38 maps, so a mistake here is felt everywhere
- [ ] `AM7` (qa.md:3513) where: Check nothing else in loot shifted | steps: Open ordinary chests across a couple of areas | pass: Weapons, armour, potions and scrolls are unchanged. Only the ammunition aggregate was touched
- [ ] `AM8` (qa.md:3514) where: **The judgement row.** After a few hours of play | steps: - | pass: Does roughly one ammunition drop in eleven being enchanted feel right? Too generous makes elemental ammunition unremarkable; too mean leaves these six enchantments as rare as they effectively were. The fix either way is one weighting
- [ ] `FI1` (qa.md:3564) where: Obtain **`Fire and Ice`** (kit, or a magic wand drop) | steps: Look at it in the inventory | pass: It is called *Fire and Ice*, is magical, shows the fire-circle wand icon, and its description reads **15%** fire and cold resistance -- the number is interpolated from the implementation, so if it shows a placeholder or a zero the expression is not resolving
- [ ] `FI6` (qa.md:3569) where: Obtain **`The Mage`** | steps: Look at it | pass: It is called *The Mage*, shows the lightning wand icon, and its description reads **4** skill points and **10%** resistances, both interpolated
- [ ] `FI10` (qa.md:3573) where: Deselect both wands | steps: - | pass: Every bonus goes away cleanly. These are `Modification is permanent=0`, so nothing should stick -- a bonus that persists after deselecting is a real bug and worth reporting at once
- [ ] `FI12` (qa.md:3575) where: **The control.** Collect ordinary wands from the magic pool | steps: - | pass: The other 16 wands still appear and still work. Adding two entries must not have disturbed the pool -- `Array Count` went 16 to 18
- [ ] `PK14` (qa.md:3645) [save] where: Kill a **second** member of a faction you have already angered | steps: - | pass: Nothing happens twice: no duplicate title, no error, no message. The grant checks for the perk before giving it
- [ ] `EB14` (qa.md:3920) where: **The exploit, which must be gone.** Equip `Rod Bone WITH Spirit`, note Thought and Tribal, then **drop it and pick it up** five times | steps: - | pass: Skills do **not** climb. As shipped this granted +2 to eight disciplines per pickup, without limit. If they still climb, the fix did not take
- [ ] `EB15` (qa.md:3921) where: Equip and unequip the spirited Sceptre | steps: - | pass: The +2 to each Thought and Tribal discipline appears **only while equipped**, and is fully removed on unequip
- [ ] `EB16` (qa.md:3922) where: **The set bonus.** Wear the Amulet alone, then the Ring alone, then both, noting Mana Capacity each time | steps: - | pass: +20, +10, and **+40** -- the pair is worth 10 more than the sum. Spell Resistance +5 comes from the amulet only
- [ ] `WD3` (qa.md:4014) [eyes + save] step: **Wands.** Watch for any wand at all dropping | say: - | expect: Wands now appear. In vanilla only `Wand Lightning Major` was placed anywhere, and the random pool was disconnected, so this is 16 enchantments appearing for the first time
- [ ] `WD4` (qa.md:4015) [eyes + save] step: Specifically: a **Wand of Swarm** | say: - | expect: `5 Unique`, summons insects via `Insect Plague`, and confers ranged-damage resistance while it still has charges. Weighting 5 of 255 in the wand pool, so rare -- do not expect it quickly
- [ ] `WD5` (qa.md:4016) step: Try a wand you find | say: - | expect: It casts, and spends a charge. The `CPlugInBehaviorWand` machinery was always complete; only the placement was missing
- [ ] `WD6` (qa.md:4017) step: **The balance row.** Judge whether loot now feels too generous | say: - | expect: Magic equipment is **9%** of one branch of one generator. If the game now rains magic items, that share is the dial. This is the row I would most expect to need adjusting
- [ ] `WD7` (qa.md:4018) step: Check whether magic equipment appears in **shops** as well as drops | say: - | expect: Whatever vanilla does. Merchant inventories were not touched, so if shops draw from the same generator they will stock it too -- worth knowing either way
- [ ] `WD8e` (qa.md:4024) step: Compare against **vanilla armour** drops at the same points | say: - | expect: They should feel consistent -- the thresholds are literally vanilla's own 7 / 16 / 999 from `All Armor`, so magic equipment and armour now step up together
- [ ] `WD9` (qa.md:4025) step: Look for an item that appears **unenchanted but named** as if magic | say: - | expect: None. All 40 enchantments were verified implemented before wiring, unlike the two wand shells
- [ ] `WD11` (qa.md:4027) step: **Potions and scrolls** | say: - | expect: **Unchanged.** Both branches were already connected and their weightings were not touched
- [ ] `WD12` (qa.md:4028) step: The eight **plain** base items | say: - | expect: All still present and still at weighting 17. Verified in the shipped bytes, but this is the row that proves it in play
- [ ] `WD14` (qa.md:4030) step: Boots, gauntlets and necklaces | say: - | expect: Their magic versions still only come from the one map each that references them. Unchanged by design -- if that inconsistency is annoying, it is one entry each to fix
- [ ] `WD15` (qa.md:4031) step: Sell a new magic item to a merchant | say: - | expect: It prices by its enchantment's own value. Nothing here set a price; all values are vanilla's
- [ ] `WD16` (qa.md:4032) step: **The regression row.** Confirm armour and weapon drops are untouched | say: - | expect: `All Armor and Shields` and `All Weapons` are separate branches of the master and were not edited
- [ ] `SM1` (qa.md:4088) step: **The row this exists for.** A Tribal caster with **Monster Summoning at 200+**. Cast it | say: - | expect: A **Rock Titan**, a Desert Beast or a Sand Spirit. No summon above tier 3 has ever appeared in this game
- [ ] `SM2` (qa.md:4089) step: The same caster at **150-199** | say: - | expect: Snake Women, an Ogre variant or a Wererat Boss -- tier 4
- [ ] `SM3` (qa.md:4090) step: At **100-149** | say: - | expect: Guard Dog 03 / Vodyanoi 03 / Wolf 03, exactly as before. **This tier's contents did not change**, it is only bounded above now. If it changed, the splice hit the wrong block
- [ ] `SM4` (qa.md:4091) step: At **under 50**, and then **50-99** | say: - | expect: The two lowest tiers, unchanged. These were not touched at all
- [ ] `SM5` (qa.md:4092) step: **The upkeep row.** Watch your mana while a tier-4 or tier-5 summon is alive | say: - | expect: It drains, at the same rate as a low-tier summon -- **3 mana** per tick. If a high summon is free to maintain, the cloned `CAddAIAction` did not come across and that is a real bug
- [ ] `SM6` (qa.md:4093) step: Let a tier-5 summon expire or die | say: - | expect: It vanishes cleanly like any other summon, and the drain stops. The clone carried the whole lifecycle, not just the creation
- [ ] `SM7` (qa.md:4094) step: **The multi row.** Cast with multi-summon available (high skill) | say: - | expect: Two creatures, and the second draw can now roll any of **9** options including the new six. Previously it drew from 3
- [ ] `SM8` (qa.md:4095) step: Cast single, then multi, then single again | say: - | expect: No interference. The two branches are separate structures in the same file and the edit touched each independently
- [ ] `SM9` (qa.md:4096) step: Judge whether a **Rock Titan** is too strong as a summon | say: - | expect: It is 170 HP against the previous ceiling of a Wolf 03. This is the one number worth arguing about -- the cans are vanilla's own, but nobody has ever fought alongside one. If it trivialises fights, say so
- [ ] `SM10` (qa.md:4097) [eyes + save] step: Check the summon's name in the combat log and on hover | say: - | expect: It will probably read **"Black Wolf"** -- all six races carry that display name in vanilla, copied from the wolf summon and never renamed. **Expected, not a new bug**, but worth confirming so it can be fixed deliberately rather than found by surprise -- *0.60.3 found the log prints User Assigned Name, not race Display Name, so the expected name may differ.*
- [ ] `SM11` (qa.md:4098) step: Try to maintain two summoning spells at once | say: - | expect: Still refused. `CDisableRecastingOfSpellForSpellsDuration` was untouched, and the skill description says you may not
- [ ] `SM12` (qa.md:4099) step: Cast `Raise Undead` and `Spiritual Knight` | say: - | expect: **Unchanged.** They use their own projectiles -- `Raise Undead Instant Hit Projectile` draws `Zombie 01`, `Spiritual Knight` draws the five `Knight Templar` cans. Only Monster Summoning's projectile was edited
- [ ] `SM13` (qa.md:4100) step: A **non-Tribal** character | say: - | expect: Nothing changes. The edit is inside one spell's projectile
- [ ] `SM14` (qa.md:4101) step: Watch for a summon appearing with no model or dropping through the floor | say: - | expect: None. All six cans resolve to real `Cache/Models/*.mdl16` files and `Rock Titan Blue` also has a `Models3D/.../Rock Titan Blue.MODEL.GR2`, so no art is missing. But these have never been spawned, so this is the row that proves it
- [ ] `TS2` (qa.md:4201) step: **The repair row.** Look at the Helm in your inventory | say: - | expect: It looks like a **helmet** -- helmet icon, and a helmet on the ground when dropped. In vanilla it would have shown a large shield. If it still looks like a shield, the art repair did not take
- [ ] `TS3` (qa.md:4202) step: Check where the Helm sorts in the inventory list | say: - | expect: With **armour**, not with shields. Its grouping moved from `Shield Large` to `Armor`
- [ ] `TS6` (qa.md:4205) step: Drop both on the ground and look at them | say: - | expect: A helmet and a shield, two different models. Both previously used the same `LionShield_PU`
- [ ] `TS7` (qa.md:4206) step: **Equip the Helm and watch AC.** Note your Armor Class, put it on, note it again | say: - | expect: **+6** -- double the best plain helmet, and nothing enchanted beats it because `Helmets/Protection` grants +0 AC. As shipped the Helm gave **nothing at all**
- [ ] `TS7b` (qa.md:4207) step: Equip the Shield and watch AC and resistances | say: - | expect: **AC +8**, **Piercing +15, Slashing +12, Crushing +12**, attack speed **-0.03**. That beats `ShieldLarge` (+7, P15 S10 C10) on AC at **half its encumbrance** and with a lighter speed penalty -- the set's identity is protection at medium weight
- [ ] `TS7d` (qa.md:4209) step: Take one piece back off | say: - | expect: The set bonus **goes away** and AC drops by 4 more than the piece itself. If it sticks, the counter is not decrementing and that is a real bug
- [ ] `TS15` (qa.md:4211) step: **Equip the Shield and check your one-handed skill** | say: - | expect: **+5 OneHandedMelee**. Below the +8 that enchantments give, so it should feel like a competent shield rather than a weapon upgrade
- [ ] `TS16` (qa.md:4212) step: **Equip the Helm and check Luck** | say: - | expect: **+1 Luck**. Watch what moves with it -- `Fortune`, `CriticalChance` and the Cold, Fire and Electrical resistances all read Luck, so a single point touches several numbers. **No other item in the game grants a flat attribute**, so if this feels disproportionate, say so: it is the one number here with no vanilla precedent to anchor it
- [ ] `TS17` (qa.md:4213) step: Take the Helm off and confirm Luck returns | say: - | expect: Back to its old value, and the derived numbers that read Luck follow it down. An attribute bonus that sticks after unequipping is a real bug
- [ ] `TS14` (qa.md:4214) step: **The calibration row.** Compare the set against a `ShieldLarge` plus the best helmet you can find | say: - | expect: The set should be **clearly better**, or it is not worth two slots and a unique find. If it still feels outclassed, the numbers are the dial and this is the row that says so
- [ ] `TS11` (qa.md:4216) [eyes + save] step: **The latent-bug row.** Confirm the Helm registers as a helmet | say: - | expect: It now sets `Wearing a Helmet`, which **three shipped files read**, including `Resurrect player.can`. As shipped it did not, so a Templar helm was not a helmet as far as the game was concerned
- [ ] `TS12` (qa.md:4217) step: **The blast-radius row.** Make a character with **neither** piece and check AC against a vanilla install | say: - | expect: **Identical.** The set bonus lives in `(AC) Armor Class`, a core attribute every character uses, so the conditional must return 0 for everyone else. If base AC moved at all, back this out
- [ ] `TS13` (qa.md:4218) step: Check an **enemy's** behaviour in combat after the AC change | say: - | expect: Unchanged. Enemies cannot equip items so the counter stays 0, but `(AC) Armor Class` is in every creature's attribute map and this is the row that proves the edit is inert for them
- [ ] `CT2` (qa.md:4297) step: Wound the same enemy repeatedly | say: - | expect: **One patch only.** If it scatters caltrops every time it is hit, the `CSeriesAction` one-shot is not holding -- the same failure `PO2` watches for, now backed by decompilation showing the index is per-instance, so a failure here would be a build error rather than a wrong assumption
- [ ] `CT3` (qa.md:4298) step: **The safety row.** Lure *other enemies* across a patch | say: - | expect: **They are unharmed.** Only `Triggered By Players` is set. If an enemy triggers it, the trigger flags are wrong
- [ ] `CT4` (qa.md:4299) step: Take a **companion** across a patch | say: - | expect: **Unharmed.** Companions and player friends are both 0. This matters more than CT3 -- a trap that kills Fernand would be a serious fault
- [ ] `CT5` (qa.md:4300) step: Walk around a patch rather than through it | say: - | expect: **Nothing happens.** It is avoidable, and that is the design -- if patches land where you cannot avoid them, say where
- [ ] `CT6` (qa.md:4301) step: Kill the layer, then walk into its patch | say: - | expect: The patch **still works**. It is an independent entity, not tied to its creator's life
- [ ] `CT7` (qa.md:4302) step: Leave a patch untriggered and fight on for a while | say: - | expect: It stays until walked on. It only removes itself after firing, so an unused patch persists for the fight
- [ ] `CT8` (qa.md:4303) step: Leave the map with patches still on the ground, then come back | say: - | expect: Whatever the engine does with the save snapshot. Not a designed behaviour, just worth knowing -- report what you see rather than judging it
- [ ] `CT10` (qa.md:4305) step: Compare the damage against a real map trap in the Crypt or Alamut | say: - | expect: The caltrops should hurt **noticeably less** -- about half -- and scale with your mojo the same way
- [ ] `CT11` (qa.md:4306) step: Try **Find Traps** near a patch | say: - | expect: **Nothing to find.** These are visible by design and carry no `CAISecretReveal`. If that reads as a missed opportunity rather than a kindness, say so -- the machinery exists and could be added
- [ ] `CT12` (qa.md:4307) step: Try to **disarm** a patch | say: - | expect: **Not offered.** Same reason. The map traps' disarm specifier was deliberately not copied
- [ ] `CT13` (qa.md:4308) step: **The regression row.** Listen to the thieves while fighting them | say: - | expect: Barks intact on all 36 thief cans. The assassins never had any, which is why 12 of the 48 are silent and that is not a fault -- *0.97.0 added Montserrat assassins and Assassin Masters as layers.*
- [ ] `CT14` (qa.md:4309) step: Watch an assassin's attacks after it lays a patch | say: - | expect: **Unchanged.** The hurt slot was empty on all 48 and nothing else in any can was touched
- [ ] `EH3` (qa.md:4472) step: **The safety row.** Cast your own **Healing** on yourself with enemies nearby | say: - | expect: It heals **you and your friends only**, exactly as before. The vanilla `Healing.Skill` was not touched and is still gated to `Player,Player Friend`. If your heal is now topping up enemies, stop and report immediately
- [ ] `EH4` (qa.md:4473) step: Open your skill tree and look under Magic Divine / Defensive | say: - | expect: **No `ENEMY Healing` anywhere**, not castable, not listed, no icon. It is reparented under Fake Wand Spells with `Image=!None` and an always-false display requirement
- [ ] `DN18` (qa.md:4904) step: Check Sir Roger, Esteban and Sir Jorge all still fight as they did | say: - | expect: Each got a clone of the tier race they were using, presets carried verbatim; only the name differs -- *Expected names here came from race names, but 0.60.3 found the log prints the can's User Assigned Name (a hat goblin logs Goblin Striker). A different name is not a failure on its own; check it against the can.*
- [ ] `GB28` (qa.md:5046) step: Fight a bow thief, a bow soldier and a Snakebreed Venom | say: - | expect: They should shoot as they always did. **21 archer cans shipped since 0.27.0 with a bark filler selecting `Skills/Fighting/OneHandedMelee` -- a skill not present on their race at all.** Vanilla uses that action in that slot to choose the next attack (`Priest Super` casts its shield, then picks Fire Orb or Spike), so it was never inert. Each is now repointed at its own race's primary. `Soldier4 Bow Super` has Ranged 97 and was told to select melee three attacks in four
- [ ] `GB29` (qa.md:5047) step: Specifically: did bow units get *better*? | say: - | expect: If archers were visibly fumbling before and are not now, that is GB28 landing, and it means the defect was live rather than silently ignored. Worth knowing either way
- [ ] `BK7` (qa.md:5273) [save] step: Check the combat log | say: - | expect: Barks are **not** in it. `Include In Log=0`
- [ ] `SN2` (qa.md:5319) [eyes + save] step: Fight base and Tough bow thieves | say: - | expect: Unchanged. Only the Super pair carries it
- [ ] `SN3` (qa.md:5320) [eyes + save] step: Fight a `Thug3 Bow` or `Thug4 Bow` anywhere | say: - | expect: Unchanged. Thugs do not share the new races
- [ ] `SU2` (qa.md:5418) step: Load any save and check the character screen | say: - | expect: Normal. Nothing about this touched the player
- [ ] `AF6` (qa.md:5563) step: Every one-shot trigger from earlier releases -- the gate parley at the Grove, the Montaillou gate strip, the four Misc Crypt hovers, the two cave hovers, the two Crossroads Siege hovers, the Plains rogue strip | say: - | expect: Unchanged. They still fire exactly once -- *Spans the Grove, Montaillou, the Crypt, the caves, Crossroads Siege and the Plains.*
- [ ] `BA26f` (qa.md:5845) [save] step: Keep hitting the same child, or attack a second one after the first | say: - | expect: No duplicate grant. Each hook is `COnlyOnce` and the grant checks the perk first
- [ ] `BA22a` (qa.md:5848) [save] step: Let your own character be killed by anything, at any point in the game | say: - | expect: **No title is granted by dying.** The first pass armed the player's own death by mistake; the hook belongs on the citizen, not on whoever the balloon was talking to
- [ ] `BK2` (qa.md:6026) where: Equip it | steps: Read the character sheet | pass: **+1 AC, +4 Unarmed, +2 Critical Chance.** No damage resistances at all -- that absence is deliberate, not a missing modifier
- [ ] `BK4` (qa.md:6028) where: With it equipped, look at your character | steps: Compare against a Small Shield | pass: A **small round buckler**, visibly not the small shield's kite. Its mesh is 30% smaller than the small shield's. If it looks like a kite shield the `Buckler` mesh name did not resolve; if your arm is **empty**, it resolved to nothing, which is what a missing composite registry name does
- [ ] `BK5` (qa.md:6029) where: A magic buckler, **Better** grade | steps: Equip it, and look at the inventory icon too | pass: A **steel** buckler, in both places -- `BucklerBetter`, authored for this release because the game shipped two skins for three grades. If it shows the copper base in either place, the new art did not reach the build
- [ ] `BK5b` (qa.md:6030) where: A magic buckler, **Special** grade | steps: Equip it | pass: The **gilded** buckler (`BucklerSpecial`). All three tiers should now read as a material ladder: copper, steel, gold
- [ ] `BK8` (qa.md:6033) where: **Judgement, not pass/fail.** Play an unarmed character with and without it | steps: Compare how fists feel | pass: It should be a clear upgrade over an empty hand and still not tempt an armed build. If an armed character wants one, +2 crit is too much and should come down -- *Judgement row.*
- [ ] `BD1` (qa.md:6042) where: Obtain **Bracers of Defense** -- magic bracers from a drop, a chest or a merchant | steps: Look at them in the inventory | pass: Their **own** icon, not the plain bracer picture every other pair wears. A blank square means the path did not resolve
- [ ] `BD2` (qa.md:6043) where: Hold them beside any **other** magic bracers -- of Archery, of Fire Resistance | steps: Compare | pass: Only the Defense pair changed. The others still wear the plain bracer icon, correctly: no art was ever drawn for them
- [ ] `BD3` (qa.md:6044) where: **The regression.** Equip them | steps: - | pass: Unchanged. This release touches one `Inventory Window` field and nothing else -- no stat, no pool, no drop
- [ ] `OA2` (qa.md:6059) where: **Amulet of Dour Tidings** | steps: Look at it in the inventory | pass: Its own icon, not the green opal it shared with eight other amulets. A blank square means the `Images for RED file/` path did not resolve
- [ ] `OA3` (qa.md:6060) where: **Gauntlets of La Mancha** | steps: Compare against an ordinary pair of Gauntlets | pass: ~~A different, spiked icon.~~ **Replaced in 0.92.0 with art painted for it**: the same leather, gilded accents, and a small windmill on the back of each hand. If they look like the Gauntlets of Hellfire without the fire, the 0.90.0 icon is still in the build and the revert did not reach it; if they look like the plain pair, the painted icon did not
- [ ] `OA5` (qa.md:6062) where: A **Wielder Rod of Spirits**, either version | steps: **Drop it on the ground** | pass: Same, and distinct from the Rod of Bone's. Compare against `Scepter of the INQ Chambers`, which already had its own sprite
- [ ] `OA6` (qa.md:6063) where: **The regression.** Any of the five | steps: Use it as you would have before | pass: Unchanged. These edits touch art fields only -- no stat, script, drop or requirement moved. If a rod stopped casting or the amulet stopped granting its bonus, something went wrong that this release had no business touching
- [ ] `TS11d` (qa.md:6089) [eyes + save] where: Complete *Search for the Five Ways Crystals* as any faction | steps: - | pass: Your promotion fires exactly as in vanilla. **No shield appears there any more** -- that grant was removed, and the two maps it lived in are back to their previous state -- *Fires at the fifth crystal.*
- [ ] `TS12` (qa.md:6090) where: **Judgement, not pass/fail.** Equip the Aegis and let something hit you in melee | steps: Watch its health | pass: It should take a visible share back -- 15% -- without the fight becoming trivial. **This number is calibrated against `Dragon Scales` (10%, permanent) and `Backlash` (20-35%, temporary) and has never been measured in play.** If attackers melt, it is too high; if nothing is observable, the attribute may not be read for permanent item modifiers at all -- *Judgement row.*
- [ ] `LE12` (qa.md:6409) where: **Judgement.** Read the Demonic split beside vanilla | steps: Does *"Dark One"* land at 800, or does it want a lower bar? | pass: Karma 1000 is neutral and 0 is the worst there is, so 800 is a moderately bad character. Each of the three exits carries the number twice, in `tools/build_loose_ends.py` -- *Judgement row.*
- [ ] `WM1` (qa.md:6431) [eyes + save] where: **The row that matters.** Any magic melee weapon, from a drop or a merchant | steps: Read its name and tooltip | pass: It has an **enchantment name and a working effect** -- *Long Sword of Snakebiting*, not a bare *Long Sword*. If magic melee weapons have stopped rolling enchantments, the per-base group tree is broken and nothing else in this release matters
- [ ] `WM2` (qa.md:6432) where: A **Better** magic long sword, equipped | steps: Compare against a plain one in hand | pass: The blade is visibly a different, fancier mesh. Both at the same size: the family shares `Render Scaling=0.55`, so the variant reads about 12% longer and no more
- [ ] `WM3` (qa.md:6433) where: A **Special** magic long sword, equipped | steps: Compare against plain and Better | pass: A third distinct mesh, not a repeat of either
- [ ] `WM4` (qa.md:6434) where: A **Special** magic scimitar, on a **male** character | steps: Equip it and look at the blade | pass: It **appears**, and the blade hangs **down**. Both halves are fixes: the mesh was absent from the male registry so it rendered nothing, and the art itself was rotated. If it appears blade-up the rotation axis is wrong; if it does not appear, the registry patch did not take
- [ ] `WM5` (qa.md:6435) where: A **Better** magic war hammer, on a **male** character | steps: Equip it | pass: It appears. This is the second registry entry, and unlike the scimitar its art needed no rotation
- [ ] `WM6` (qa.md:6436) where: A **Great Mace**, magic or not | steps: Look at it in hand | pass: It is **the size it has always been**. An early build of this release shrank it 11% on a pattern match and that was reverted, so a Great Mace that looks smaller than you remember means the revert did not reach the build. A magic one still rolls enchantments but shows no mesh change, because no Great variant art exists
- [ ] `WM7` (qa.md:6437) where: A **Better or Special** magic **Composite** Long Bow | steps: Compare against a plain Composite Long Bow | pass: Same mesh, `BowSpecial`. The Composite's own base art is the best bow in the game, so its copies name `BowSpecial` at both tiers rather than downgrading it to `BowBetter`. **The grade is the whole row.** A Composite carrying a Basic addition such as `of Dodging` has already been held in play and looked right, but Basic additions name no mesh, so that proves only that the Composite's pool delivers. Confirm the enchantment is Better or Special before reading anything into the model
- [ ] `WM8` (qa.md:6438) where: A **Better** magic **plain** Long Bow | steps: Compare against a plain Long Bow | pass: A different mesh at **the same size**. It rendered 1.8x oversize before the scaling fix, so an obviously huge bow means the `MODEL.TXT` edit did not reach the build
- [ ] `WM10` (qa.md:6440) where: **Judgement, not pass/fail.** Collect magic weapons over a stretch of play | steps: Watch the variety of enchantments | pass: It should feel unchanged. Each base weapon's pool is asserted to keep vanilla's 3/20/6 shape with nothing double-weighted, so any felt change in variety is worth reporting as a surprise -- *Judgement row.*
- [ ] `S2` (qa.md:6447) pass: No conflict on any shared file -- *Needs the other tools-repo mods enabled.*
- [ ] `S3` (qa.md:6448) pass: Clean

## Old saves only, not part of the new-game run

- `Q2` (qa.md:990) where: Wilderness | steps: Kill wolves **without** the Wolf Trapper perk, return | pass: The plain pelts are accepted -- this is the vanilla-perk path and it worked before this release too | old_save: True
- `CR7` (qa.md:1354) where: Crypt `7 Doomed Plateau`: talk to Jehanne, reach `50 Counsel` then `100 spoke to counsel`, and convince her (*"Jehanne, I speak for the Council..."*) | steps: Walk away, leave the map or let the conversation end, then talk to her again | pass: *"You have returned"* -- the civil greeting, with *"Do you know where the efreet is?"* among the replies. **Before this release every return was *"I warn you, monster"* even after convincing her**, because the checker was set nowhere | old_save: True
- `CR8` (qa.md:1355) where: CR7, then say goodbye from the civil greeting | steps: *"No, I will return when I do. Goodbye."* | pass: `5 Goodbye Joan Likes You`: *"Dieu est avec vous."* Unreachable before this release | old_save: True
- `CR12` (qa.md:1359) where: CR10, attack him instead | steps: - | pass: He goes to combat and says *"You will be destroyed!"* (`20 monster`). **Before this release the clone's damaged script fired a relay that does not exist on this map, so he would have died without fighting** | old_save: True
- `CR37` (qa.md:1384) where: Carrying the Bleeding Lance, talk to Jehanne from her **civil** greeting (needs CR7) | steps: *"I have recovered the Bleeding Lance."* | pass: `200 have lance` -> `201 what now`. **Vanilla pointed at a node that does not exist; before this release the reply led nowhere** | old_save: True
- `NO5` (qa.md:1410) where: Answer *"I have come to help the Prophet"* | steps: - | pass: *"Good to hear, friend."* The quest **Protect Nostradamus from the invading English forces** enters the journal, and Huko and his guard walk off, fade and vanish. Neither quest could be entered at all before this release | old_save: True
- `NO40` (qa.md:1445) where: NO34 then reload a save from before the choice and side with the English instead | steps: - | pass: The English parts stay off. The checker is per-map and set only by the Hujark relay | old_save: True
- `HV15` (qa.md:1841) step: **The shipped defect this playtest found.** Recruit a companion and **never open the order menu**. Level up | say: - | expect: The growth balloon still appears. Before this release both installers were invoked from *one* place -- a reply in `Generic Companion Dialog` -- so a player who never clicked a companion got **no growth for the whole game**. A save with Fang in the party for several levels had `Fixt Companion Growth Watch`, `CXRPGAITriggerWhenLevelUp`, `Fixt Companion Health Watch` and `CAIHealthPercentThresholdTrigger` all at zero | old_save: True
- `TK10` (qa.md:1946) step: A character below mojo 7, looting magic misc items | say: - | expect: Cloaks appear, and the only enchantments on them are Cold, Fire or Poison Resistance. Before this release cloaks could not drop in that band at all | old_save: True
- `MA5` (qa.md:2030) step: **Regression.** Never go to the sanctum, then reach him | say: - | expect: The existing default, unchanged. Before this release the blunt kill was indistinguishable from this | old_save: True
- `SB1` (qa.md:2154) step: **The row that proves the release.** Loot the shell from DaVinci's secret chamber *before* Relican names the Sceptre errand. Then take the initiation from him | say: - | expect: The journal entry reads the lifeless-sceptre state, not "recover the fabled Sceptre". Talk to him again: *"I have the Sceptre, but it is a dead thing"* is offered -> `47 Fixt Relican Binds Shell`, the spirited sceptre arrives and the quest completes. Before this release no reply was offered at all and the initiation stopped here | old_save: True
- `VD3` (qa.md:2175) step: **The row that proves the release.** Find a Belt or Necklace of Voodoo that *also* carries another enchantment, so it is worth more | say: - | expect: **1.5 to 2** per Tribal branch instead of a flat 1. Before this release no Voodoo piece ever gave more than 1, however rich the item | old_save: True
- `AR2` (qa.md:2195) step: **The row that proves the release.** Compare a cheap piece of the Mage against a dear one, 6,000 gold or more, on the character sheet | say: - | expect: The cheap one gives **+1** to each magical branch; the dear one gives **3 to 5**. Before this release both gave +1, however expensive the armour | old_save: True
- `PS2` (qa.md:2303) step: **The row that proves the ceiling is reachable.** Check the damage you actually roll on a weapon worth about 7,000 | say: - | expect: Rolls reach near 26. Before this release the band topped at 10,000, which **no melee weapon in any save reaches**, so the stated 14 was never paid either | old_save: True
- `IB2` (qa.md:2489) step: Swing it at something and watch | say: - | expect: It fires on something like half your hits, not one in twenty. Before this release you could finish a fight without ever seeing it | old_save: True
- `BM1` (qa.md:2555) step: **The row that matters.** Take the peaceful route at Montserrat, then report to your patron | say: - | expect: He credits **the assassin**, not Brother Montgomerie. Before this release all three patrons named a man you never met | old_save: True
- `CE11` (qa.md:2580) step: **The two repaired beats.** Talk Don Quixote out of existing at Barcelona Coast | say: - | expect: A feather comes down where he was standing. Before this release the scene ended on nothing at all | old_save: True
- `RJ1` (qa.md:2598) step: Draw on Inquisitor Raphael in the foyer, serve the jail, walk back to the foyer and approach him | say: - | expect: He balloons *"For your sake, I pray your time in prison has soothed your belligerence."* Before this release he said *"Welcome back, child"* | old_save: True
- `SN1` (qa.md:2635) step: Walk up to the Grove sentry on any character with no Outwit and no Demokin or Sylvant blood | say: *"I came to learn what happened to this house."* | expect: The reply is **there**. Before this release a plain character's only way in was *"I am. Take me to your captain."* | old_save: True
- `UC4` (qa.md:2656) step: **The gap.** Pick the lock, then stay in the cell block for two full minutes without crossing into the warden's room | say: - | expect: **Nothing fetches you.** Before this release the warden escorted you upstairs at 100 seconds while the cell door hung open | old_save: True
- `TD2` (qa.md:2687) step: Take that reply | say: - | expect: She answers **"No! No, it can't be!"** and the rescue quest resolves. Before this release the reply never appeared and the quest sat open forever | old_save: True
- `NQ2` (qa.md:2700) step: Check the world map afterwards | say: - | expect: The Caverns are selectable. Before this release only the witch or the titan Menoetius could do that | old_save: True
- `RL4` (qa.md:2714) step: **Regression.** Fight her instead and win | say: `<Draw.>` | expect: Level 2 empties exactly as it did before this release. The death ending is untouched | old_save: True
- `MP8` (qa.md:2743) step: **The funnel.** Reach Sahar with Outwit 7 and Machiavelli's task taken, use the Machiavelli line | say: `I carry Machiavelli's word...` | expect: She answers, and you can still ask her questions or say *"Then send me north"*. Before this release `<Draw.>` was the only reply and the ring was gone for good | old_save: True
- `CS4` (qa.md:2756) step: **The wrong-scene fix.** On a character who has never entered the Cathedral, join the **Wielders** and take Cedric's briefing | say: - | expect: **The Wielder scene**, not the Saladin or Templar one. Before this release the `if wielder` flag was lost in transit and the player got whichever scene the fallback pointed at | old_save: True
- `IQ3` (qa.md:2867) step: **The row that matters.** Check your quest log | say: - | expect: **Investigate the fate of Montserrat** is now active. Before this release no node in the game could start it | old_save: True
- `TS2` (qa.md:2933) step: Note the price of something in his shop **before** begging, then beg and reopen the shop | say: - | expect: The same item is **15% dearer**. Before this release begging cost nothing at all | old_save: True
- `FN13` (qa.md:3014) step: **New character.** Reach the dying sailor on the Port District docks and look at the name over him, then at the combat log | say: - | expect: **Fernand Desoto**, not Sailor. Before this release his template still carried the generic name | old_save: True
- `LJ1` (qa.md:3039) step: **The report.** Reach the Montserrat briefing, and when the conversation opens ask *"Before I go, tell me about the Sacred Lance."* | say: - | expect: He explains the Lance. Say you will go and **the scene ends**: his farewell, the screen fades, controls come back and you are in the Temple District. Before this release the gears spun forever | old_save: True
- `SW6` (qa.md:3059) step: **The row that was broken before it shipped.** On a different character, take *"This place is too dangerous for you. Return to Barcelona."* | say: - | expect: He says farewell **and goes**: he stops being talkable, fades out over a second and a half, and is gone. Before this release the reply had no action and he would have stood there forever | old_save: True
- `GF12` (qa.md:3089) step: On a male character, read which line you got | say: - | expect: *"Signore!"*, and the male text. Before this release the gender read happened in a context with no instigator and every character would have fallen to the female line | old_save: True
- `TR34` (qa.md:3136) step: Go upstairs and talk to the workshop DaVinci | say: - | expect: 0.57.8's reaction is still offered. Two of him being pleased is intended; the chamber one is the scene, the workshop one is the fallback for anyone who finished the quest before this release | old_save: True
- `SM2` (qa.md:3349) step: Count how often it summons across a few fights, against a pre-0.55.0 save if you have one | say: - | expect: **Unchanged.** The bark is inside the summon branch, not a sibling entry, so the rate is identical. If summoning feels rarer, the bark was added in the wrong place | old_save: True
- `SV3` (qa.md:3366) step: Talk to him again | say: - | expect: **The new reply: *"The silver is gone, I know that. Is there enough left for the shield?"*** (or the scimitar). Before this release there was nothing here, which is the whole report | old_save: True
- `SV10` (qa.md:3373) step: Deliver the **first** item and then check the silver errand | say: - | expect: Unchanged. The silver path is byte-identical to before this release; if the first delivery behaves differently, that is a regression | old_save: True
- `SH2` (qa.md:3375) step: `SH1`, then talk to Jafar | say: - | expect: **The new reply: *"I have something that belongs to your Order. Nobody asked me to bring it."*** Before this release the Shard was unreturnable | old_save: True
- `BP13` (qa.md:3408) step: Attack the **chief** first, rather than a drone | say: - | expect: The scene still fires. The three boss cans had no damage hook at all before this release, so this is new ground, not a regression check | old_save: True
- `AM2` (qa.md:3508) where: **The row that proves it.** Keep collecting ammunition | steps: Watch for an enchanted one | pass: **An enchanted bolt appears** -- Acid, Cold, Extra Chance to Hit, Extra Damage, Fire or Poison. Before this release enchanted bolts could not drop anywhere in the game | old_save: True
- `FJ2` (qa.md:3533) where: **The row that proves it.** Keep collecting from `FJ1` past the tenth book | steps: - | pass: **The `Feralkin Journal` is among them.** Before this release it existed in the files and could not be got hold of anywhere in the game | old_save: True
- `MA8` (qa.md:3675) where: Fight them | steps: - | pass: They take a real number of hits rather than dropping instantly, and they land real blows. Before this release they had no armour class or hit points at all | old_save: True
- `MA11` (qa.md:3678) where: Listen during the fight | steps: - | pass: All four speak, the leader included -- hissing barks over their heads. Before this release the leader was the only mute one | old_save: True
- `HR11` (qa.md:3711) where: **The ignore case.** Play the Crossroads normally without touching the horse at all | steps: - | pass: Everything is exactly as it was before this release. Alvaro trades, the bandits behave, nothing else changed | old_save: True
- `CR1` (qa.md:5884) step: Crypt, reach a talking Templar knight (`7 Doomed Plateau` or `9 Burial Chamber`), answer that you are a Knight or will help | say: *"Then I am at your orders. Where is she?"* | expect: The journal opens **Release the Doomed Knights from their Torment** at state 1. Before this release the quest had no states at all | old_save: True
- `MO31` (qa.md:5913) step: Montaillou, accept the Inquisitor's witch task, find the weird woman, return to the Bishop | say: *"I have found the witch you seek..."* | expect: The reply appears, the quest completes and pays XP. **It was gated on an empty canned object belonging to another NPC; if it never appeared before this release, that is the bug this fixed** | old_save: True
- `GD1` (qa.md:5923) step: Gate District, Farshad, as a Knight of Saladin (male and female) | say: Talk to him after joining | expect: `3 Return Knight of Saladin Male` / `3 Retun Knight of Saladin Sister` -- the two "Welcome into the Order of Saladin" greetings. **Before this release his check pointed at a can that does not exist, so every player got the stranger's opening** | old_save: True
- `TO32` (qa.md:5932) step: Toulouse, kill the titans or hand over the mneme, then watch the camp empty | say: - | expect: Menoetius leaves with the rest. **Before this release his generator named him Rhea, so he stayed behind while one of the two Rheas vanished** | old_save: True
- `MO33` (qa.md:5935) step: **End Toulouse any of the three ways, then return to Montaillou** | say: Tell the mayor, Maury, and a gate knight | expect: `941 the titans have left`, `270 the road is quiet`, `110 the titans have left`. **Before this release the cross-map flag had no part to land on, so none of the village could be told** | old_save: True
- `OA1` (qa.md:6058) where: **Nightshade Root**, from the hangover-cure chain | steps: Hold it beside **Darkwood** in the inventory | pass: They are **different icons**. Before this release both wore Darkwood's. If Nightshade Root is blank, `Quest Items/Rare Herb` did not resolve | old_save: True
- `OA4` (qa.md:6061) where: A **Wielder Rod of Bone**, either version | steps: **Drop it on the ground** | pass: Its own sprite, not the generic wand. The inventory icon was already correct before this release, so the inventory tells you nothing here -- it has to be dropped | old_save: True
- `TS1` (qa.md:6076) where: Playtest kit, *The Templar shields* | steps: Take the **Spirit Templar Shield**, equip it | pass: Something appears on your character. Before this release it rendered **nothing**. It should be the wooden crusader-cross shield, matching its own inventory icon -- *not* the gold Lion Shield, which was the first fix and was wrong | old_save: True
- `HH39` (qa.md:6139) where: Kill the Khan for Torquemada, on an older save | steps: Finish the game | pass: The same slide, through the quest state | old_save: True
- `AT4` (qa.md:6234) where: Act 8, Goblin Champion, having killed the Khan before Persia | steps: Enter Desert Sprawl | pass: The Khan does not appear. Likewise Grumdjum, if he died earlier. A save that killed them before this release still shows them | new: True | old_save: True
- `LE13` (qa.md:6410) where: Barcelona Cathedral, walk down into the crypt | steps: Stand there a full 2:18 | pass: The monks fade in as the cathedral's ambience fades out, and the loop point is not jarring. **Note whether this save had already entered the crypt.** If an old save keeps the cathedral loop and a fresh one chants, the mix is frozen into the save and the release notes must say so | old_save: True
- `WM9` (qa.md:6439) where: **The regression.** Load a save from 0.88.2 or earlier that holds a magic melee weapon | steps: Look at it | pass: It still has its enchantment and its effect. The 29 original additions were deliberately kept and repointed rather than deleted, because saves reference them by path -- if an old magic weapon has lost its enchantment, that decision failed | old_save: True
