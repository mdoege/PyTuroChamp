## PyTuroChamp

A family of toy chess engines inspired by Alan Turing's 1948 [TUROCHAMP](https://chessprogramming.wikispaces.com/Turochamp)

**PyTuroChamp** is closest to the chess engine in Turing's paper, but adds piece-square tables that can be tuned with the PSTAB parameter. A higher parameter means more aggressive forward movement. With PSTAB = 0,

 1. e3

is favored like Turing's algorithm would.

**Bare** removes the Turing heuristics and quiescence search and only contains the bare minimum a chess engine needs to play: alpha-beta search and a piece-square table.

**Newt** also ditches the old heuristics and adds newer techniques like PV-based iterative deepening. It is by far the strongest of the three engines here.

**PTC-Host** lets you easily host games between the engines directly from Python, without the need for a chess GUI.

Pyturochamp.py does not actually reproduce the results of either the Turing paper or the [Chessbase implementation](http://en.chessbase.com/post/reconstructing-turing-s-paper-machine) for Fritz. But then again Turing's paper was meant as a proof-of-concept, so maybe reproducibility is not important.

### Files

|Filename | Description |
|---|---|
| pyturochamp.py | The chess engine with Turing's heuristics. Plays more human-like, except for weird but typical moves like a2a4 and h2h4. |
| bare.py | Bare bones version, only alpha-beta and piece-square tables are used. Very computer-like and not pretty but sometimes efficient play. Stockfish took [62 moves to checkmate it](https://github.com/mdoege/PyTuroChamp/blob/master/ptc-bare-stockfish.pgn) (with ponder off). |
| newt.pt | Like Bare, this one ditches the heuristics. It adds principal variation (PV)-based iterative deepening and quiescence search like PyTuroChamp. |
| ptc, bare, newt | Shells script to run PTC/Bare/Newt from a chess GUI, e.g. [KDE Knights](https://www.kde.org/applications/games/knights/) (works very well) or [XBoard](https://www.gnu.org/software/xboard/). (Change the directory path inside first.)
| ptc-host.py | Hosts a game between PyTuroChamp as White and Bare as Black. Updated board images are written to board.svg. (During play, board.svg should be opened in an image viewer that automatically reloads changed files.)
| ptc_xboard.py | XBoard interface module for PTC/Bare/Newt. Moves will also be logged to a PGN file. |
| movetest.py | Test engine responses to board situations |
| pst.py | Helper file with piece-square tables |

### Prerequisites

* Python 3
* [python-chess](https://github.com/niklasf/python-chess)

### License

Public Domain
