# Lionheart Fixt 0.25.7 - Fernand's conversation actually opens

**0.25.3 and 0.25.4 fixed nothing.** This is the repair they should have been.

Reported: hitting release on Fernand says *"a companion has left your party"*, and talking to him again
gives the same thing over. Reading the save settled it -- `Fernand Is Waiting` was absent entirely. The
variable had never been written once.

## The cause, upstream of everything those releases touched

The `fernand joins you` relay in `Port District.zax` adds an interaction specifier whose action is:

    Action=CDisplayDialogBalloonAction
    {
    Dialog Tree File=.../Distressed Sailor
    Node ID=100 companion banter

A **balloon**. It floats "Where you go, I follow." over his head and closes. A balloon has no reply
list, so the dismiss and rejoin replies added to node 100 were never displayed at all. Whatever the player
clicked, it was not a reply of ours.

## What went wrong in the diagnosis

The finding in 0.25.3 -- node 100 is his only interaction and offers no way back -- was correct. The
repair was aimed at the node instead of at the thing that opens it.

The evidence was there and was misread twice. Node 100 having no replies was first treated as an
authoring omission; then, when a sweep found **49** reply-less nodes opened as conversations elsewhere in
the game, that was taken as proof the shape was normal and the node fine. Both readings skipped the
actual question: *what class of action opens this node?* The sweep even held the answer -- it collected
entry points from `CDisplayDialogTreeAction` only, so node 100 should never have appeared in its results,
and it did not. Nobody asked why.

A reply-less node **is** normal for a balloon. That is what balloons are. The defect was that his
post-join interaction was a balloon at all, when every other companion uses a conversation: Grumdjum's
post-join specifier is a `CDisplayDialogTreeAction`, and so is the Knight of Saladin's `3 Return`, which
is why 0.25.5 worked first time.

## The fix

The specifier now opens node 100 as a conversation, with `Speaker=$trigger` and
`Player Being Spoken To=$Instigator` copied from the working specifiers in the same map. That second
field is also what makes `Character to modify=$Instigator` resolve in the reply's modifier action --
the other half of why the variable never moved.

One behaviour changes deliberately: walking up to Fernand while he follows now opens a short conversation
instead of floating a line over him. That is the cost of him having replies at all.

## **This one needs a character who has not yet recruited him**

Unlike 0.25.3 and 0.25.4, this is an **entity** change, and entity state is snapshotted per save on first
visit. The reporting save carries the old balloon in both its Port District layer and the live layer that
travels with him -- confirmed by reading the save. So this repair reaches a character who has not yet
triggered `fernand joins you`, not one already partway through.

## A correction: there is no party UI

An earlier draft of these notes said the player had clicked "the game's own party UI". **There is no
party UI**, and that was asserted without checking. The game has a stat-bar control --
`"Companion Follow / Stop Following"`, handled by
`CXrpgStatBar::Server_HandleCompanionFollowStateChangeMessageFromClient` -- which toggles **following**,
not membership. It releases nobody, and the attribute it writes, `Companion Follow Enabled`, is one
global flag for the whole party, so it cannot say whether Fernand specifically is a companion.

It does not print *"A companion has left your party"* either. That string is not in the executable; it is
a `Text to print=` in map scripts, and the one in `Port District.zax` belongs to the Lost Knight leaving
after he is saved.

None of that changes this repair, which rests on a verified fact: node `100 companion banter` was opened
by a `CDisplayDialogBalloonAction`, and a balloon has no reply list.

**Fixt** is a cumulative restoration-and-repair mod for Lionheart, after Fallout Fixt.

Download, unzip, run `Mod Manager.bat`.

https://github.com/EricHype/LionheartFixt/releases/tag/v0.25.7
