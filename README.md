## PyTuroChamp

A toy chess engine inspired by Alan Turing's 1948 [TUROCHAMP](https://chessprogramming.wikispaces.com/Turochamp)

This does not actually reproduce the results of either the Turing paper or the [Chessbase implementation](http://en.chessbase.com/post/reconstructing-turing-s-paper-machine) for Fritz. But then again Turing's paper was meant as a proof-of-concept, so maybe reproducibility is not important.

### Files

|Filename | Description |
|---|---|
| pyturochamp.py | The chess engine with Turing's heuristics. Plays more human-like, except for weird but typical moves like a2a4 and h2h4. |
| bare.py | Bare bones version, only alpha-beta and piece-square tables are used. Very computer-like and not pretty but efficient play. Stockfish takes [62 moves to checkmate it](https://github.com/mdoege/PyTuroChamp/blob/master/stockfish-ptc.pgn). |
| ptc | Shell script to run PTC from a chess GUI, e.g. [KDE Knights](https://www.kde.org/applications/games/knights/) (works very well) or [XBoard](https://www.gnu.org/software/xboard/). (Change the directory path inside first.)
| bare | The same thing for the bare bones engine |
| ptc_xboard.py | XBoard interface module for PTC |
| bare_xboard.py | XBoard interface module for Bare Bones |
| movetest.py | Test engine responses to board situations |
| pst.py | Helper file with piece-square tables |

### Prerequisites

* Python 3
* [python-chess](https://github.com/niklasf/python-chess)

### License

Public Domain
