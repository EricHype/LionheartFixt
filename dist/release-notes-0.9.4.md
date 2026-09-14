**Hotfix. Install this if you have 0.9.1, 0.9.2 or 0.9.3.**

## The crash

Entering the Mongol Camp on those three releases could stop the game with *"Tried to use an
unknown class 'CMultipleActionsAction'"*. That was the camp's gate greeting from 0.9.1 -- one
value in the map began with stray tabs, and the engine refused the map rather than the line.
Fixed, and the build check now catches that class of mistake so it cannot ship again.

## Also in this release

- **The Knights of Saladin's cathedral summit** froze, made Amir attack you, and then would
  not end. All three fixed: it plays, it finishes, and you are sent on to Montserrat.
- **Enrique's third argument** -- the red-ore trade -- was never offered once the trade was
  done. It is now.
- **Made peace with the trolls the hard way?** The chief gives you a hide from his dead for
  Quinn, and Enrique still asks you to find the wererat cure after you talk him out of the
  contract. Before this, the peaceful road cost you both.

## Installing

Download, unzip, run `Mod Manager.bat`. It installs over any earlier release. The Mongol Camp
and cathedral fixes take effect on a character who has not yet entered those maps; everything
else works on any save.
