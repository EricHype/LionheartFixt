# Lionheart Fixt 0.25.5 - the Knight of Saladin knows whether he is with you

After 0.25.4 fixed Fernand, every companion was audited for the same two failures: a rejoin unreachable
after dismissal, and a dismiss/rejoin pair that does not know which state it is in.

**Most came back clean**, and two came back better designed than Fernand ever was:

| companion | verdict |
|---|---|
| Grace O'Malley | **correct.** A map part in `01 Outside Shrine.zax` holds a `CConditionalAction` on the `Grace has been left behind` marker -- if she is waiting, simply talking to her re-recruits her and clears the marker |
| the Goblin Girl | **correct.** Same design, via `Goblin Girl is a companion` read by `Goblin Warrens.zax` |
| Grumdjum | **not a defect.** His join-and-release nodes are *recruitment* nodes; the release reply is "I work alone. Leave.", a refusal, and the action on it is a no-op when he is not following |
| Joan of Arc, Sir Roger, Diego, Inquisitor Darsh, the Trapped Conquistador | pure vanilla, untouched here; all join with no release, which is vanilla's design for companions who leave by script |
| **the Knight of Saladin** | **the one real finding** |

## The knight

His node `3 Return` offered both **"Hold this ground and wait for me."** and **"Let's go."**, neither
gated -- and `02 Shifting Dunes.zax` points his specifier at that node **twice**, from the initial map
wiring and from the `Knight AI switcher` relay fired when he joins. So it is reached before recruitment
and while following, and one of the two replies was always wrong.

**Fernand's variable would not have worked.** His node is only reached after joining, so an "is waiting"
flag splits it cleanly in two. The knight's is reached in *three* states -- never recruited, following,
waiting -- and "is waiting" cannot tell the first from the second, since both read 0. Gating his join on
it would have made him unrecruitable.

So the variable tracks the other thing: **`Saladin Knight Follows`**, 1 while he is with you.

| site | gate | does |
|---|---|---|
| `3 Return` "Let's go." | **not** 1 | join, then +1 |
| `3 Return` "Hold this ground and wait for me." | **is** 1 | release, then -1 |
| `30 go`, the first recruitment | none | join, then +1 |
| `666 Rejoin` "Yes, please rejoin me." | none | join, then +1 |

The two gated replies can each only fire from the side that makes them legal, which is what confines the
variable to 0 and 1 without needing set-rather-than-accumulate semantics. `Allow Accumulation=0` does
exist in vanilla, 37 times, but what it means is not established and this did not need to find out.

The other two sites are ungated deliberately. **`30 go` has exactly one reply**, the default, so a gate
that hid it would leave the node with nothing to click -- and it is unreachable while following anyway,
since `3 Return` offers no path to it and the specifier moves to `3 Return` the moment he joins.
`666 Rejoin` is only ever reached at 0, because the release is the only thing that points the specifier
there.

Existing actions were **wrapped**, not edited: each `Custom Action=X` became
`CMultipleActionsAction{Action=Array{Item Count=2, Action=X, Action=<bump>}}`, which avoids renumbering
an `Item Count` inside a live array -- a splice this project has got wrong before.

## What the audit was worth

A raw count of "ungated companion replies" said six trees were at fault. Reading what each node actually
is said one. The signal is not whether a reply carries a gate but **whether the node it lives on can be
reached in more than one state**: Grace and the Goblin Girl gate by map-side condition, Grumdjum gates by
position, and only the knight gated by nothing.

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt.

Download, unzip, run `Mod Manager.bat`. Dialogue and attribute repair; applies to any character,
including one with the knight already recruited or already dismissed.

https://github.com/EricHype/LionheartFixt/releases/tag/v0.25.5
