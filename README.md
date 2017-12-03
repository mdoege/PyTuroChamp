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

First, install the [python-chess](https://github.com/niklasf/python-chess) chess library: `pip install python-chess`

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

### Improving performance by using PyPy

Running the scripts with [PyPy3](http://pypy.org/) instead of python3 will make the engines run about twice as fast.

Here is a sample terminal session which shows how to set up PyPy under Arch Linux and run the PyTuroChamp scripts:

```
$ sudo pacman -S pypy3

$ pypy3 -m ensurepip --user

$ ll .local/bin
insgesamt 12
-rwxr-xr-x 1 martin users 232  3. Dez 20:33 easy_install-3.5
-rwxr-xr-x 1 martin users 204  3. Dez 20:33 pip3
-rwxr-xr-x 1 martin users 204  3. Dez 20:33 pip3.5

$ .local/bin/pip3 install python-chess --user

$ .local/bin/pip3 list
DEPRECATION: The default format will switch to columns in the future. You can use --format=(legacy|columns) (or define a format=(legacy|columns) in your pip.conf under the [list] section) to disable this warning.
cffi (1.11.1)
greenlet (0.4.12)
pip (9.0.1)
python-chess (0.22.0)
readline (6.2.4.1)
setuptools (28.8.0)

$ pypy3 ptc_xboard.py newt
go
#    ()
move g2g3
quit

$ pypy3 pyturochamp.py
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R
0.0
Your move? e2e4
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . P . . .
. . . . . . . .
P P P P . P P P
R N B Q K B N R
0.0
FEN: rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1
(1/20) g8h6 -2.2 0.00
(2/20) g8f6 -3.9 0.00
(3/20) b8c6 -3.6 0.00
(4/20) b8a6 -2.0 0.00
(5/20) h7h6 -2.4 0.00
(6/20) g7g6 -2.3 0.00
(7/20) f7f6 -0.7 0.00
(8/20) e7e6 -6.7 0.00
(9/20) d7d6 -5.0 0.00
(10/20) c7c6 -3.1 0.00
(11/20) b7b6 -2.3 0.00
(12/20) a7a6 -2.2 0.00
(13/20) h7h5 -3.2 0.00
(14/20) g7g5 -2.4 0.00
(15/20) f7f5 -1.2 1.00
(16/20) e7e5 -7.3 0.00
(17/20) d7d5 -6.6 0.00
(18/20) c7c5 -3.6 0.00
(19/20) b7b5 -2.2 1.00
(20/20) a7a5 -3.0 0.00
# -7.30 ['e7e5']
My move: 1. e7e5     ( calculation time spent: 0 m 6 s )
r n b q k b n r
p p p p . p p p
. . . . . . . .
. . . . p . . .
. . . . P . . .
. . . . . . . .
P P P P . P P P
R N B Q K B N R
0.0
Your move?
```
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
