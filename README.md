## PyTuroChamp

A family of toy chess engines inspired by Alan Turing's 1948 [TUROCHAMP](https://chessprogramming.wikispaces.com/Turochamp)

**PyTuroChamp** is closest to the chess engine in Turing's paper, but adds piece-square tables that can be tuned with the PSTAB parameter. A higher parameter means more aggressive forward movement. With PSTAB = 0,

 1. e3

is favored like Turing's algorithm would.

**Bare** removes the Turing heuristics and quiescence search and only contains the bare minimum a chess engine needs to play: alpha-beta search and a piece-square table.

**Newt** also ditches the old heuristics and adds newer techniques like PV-based iterative deepening and an opening book. It is comparatively strong and fast.

**PTC-Host** lets you easily host games between the engines directly from Python, without the need for a chess GUI.

Pyturochamp.py does not actually reproduce the results of either the Turing paper or the [Chessbase implementation](http://en.chessbase.com/post/reconstructing-turing-s-paper-machine) for Fritz. But then again Turing's paper was meant as a proof-of-concept, so maybe reproducibility is not important.

### Running the engines from a chess GUI

The recommended option on Linux or MacOS is to modify and use the included shell scripts (ptc, bare, newt).

It is also possible and perhaps easier—especially on Windows—to launch Python directly from the GUI as in the Arena screenshot below. (Note that no log or PGN files will be created then, because the working directory will be somewhere where Python cannot create files.)

If you want to use one of the other engines besides pyturochamp.py, add "bare" or "newt" as additional command line parameters.

![screenshot](https://github.com/mdoege/PyTuroChamp/raw/master/Screenshot_20171123_102423.png "Arena screenshot")

### Files

|Filename | Description |
|---|---|
| pyturochamp.py | The chess engine with Turing's heuristics. Plays more human-like, except for weird but typical moves like a2a4 and h2h4. |
| bare.py | Bare bones version, only alpha-beta and piece-square tables are used. Very computer-like and not pretty but sometimes efficient play. Stockfish took [62 moves to checkmate it](https://github.com/mdoege/PyTuroChamp/blob/master/ptc-bare-stockfish.pgn) (with ponder off). |
| newt.pt | Like Bare, this one ditches the heuristics. It adds principal variation (PV)-based iterative deepening and quiescence search like PyTuroChamp and also an opening book. |
| ptc, bare, newt | Shells script to run PTC/Bare/Newt from a chess GUI, e.g. [KDE Knights](https://www.kde.org/applications/games/knights/) (works very well) or [XBoard](https://www.gnu.org/software/xboard/). (Change the directory path inside first.)
| ptc-host.py | Hosts a game between PyTuroChamp as White and Bare as Black. Updated board images are written to board.svg. (During play, board.svg should be opened in an image viewer that automatically reloads changed files.)
| ptc_xboard.py | XBoard interface module for PTC/Bare/Newt. Moves will also be logged to a PGN file. |
| movetest.py | Test engine responses to board situations |
| pst.py | Helper file with piece-square tables |

### Prerequisites

* Python 3
* [python-chess](https://github.com/niklasf/python-chess)

### References

* Turing, Alan (1952): [*Digital computers applied to games*](https://docs.google.com/file/d/0B0xb4crOvCgTNmEtRXFBQUIxQWs/edit)
* [Chess Programming Wiki](https://chessprogramming.wikispaces.com/)
* Muller, H.G.: [*Micro-Max, a 133-line Chess Source*](http://home.hccnet.nl/h.g.muller/max-src2.html)

### License

* Public Domain
* Opening book: GPL
