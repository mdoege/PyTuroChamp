## PyTuroChamp

A toy chess engine inspired by Alan Turing's 1948 [TUROCHAMP](https://chessprogramming.wikispaces.com/Turochamp)

This does not actually reproduce the results of either the Turing paper or the [Chessbase implementation](http://en.chessbase.com/post/reconstructing-turing-s-paper-machine) for Fritz. But then again Turing's paper was meant as a proof-of-concept, so maybe reproducibility is not important.

The computer plays as White and will always start with

  1. e3 

### Files

* pyturochamp.py: The chess engine itself
* ptc_xboard.py: XBoard interface
* ptc: Shell script to run from a GUI, e.g. [KDE Knights](https://www.kde.org/applications/games/knights/) or [XBoard](https://www.gnu.org/software/xboard/). (Change the directory path inside first.) Also keep in mind the engine can only play as White at the moment, so set up the GUI accordingly.
* movetest.py: Test engine response to board situations
* *.pgn: Sample games in PGN format

### Prerequisites

* Python 3
* [python-chess](https://github.com/niklasf/python-chess)

### License

Public Domain
