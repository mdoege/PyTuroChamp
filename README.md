![logo](https://github.com/mdoege/PyTuroChamp/raw/master/icons/out.png "logo bar")

## PyTuroChamp

A family of chess engines inspired by Alan Turing's 1948 [TUROCHAMP](https://chessprogramming.wikispaces.com/Turochamp)

**PyTuroChamp** is closest to the chess engine in Turing's paper, but adds optional piece-square tables that can be tuned with the PSTAB parameter. A higher parameter means more aggressive forward movement. With PSTAB = 0,

 1. e3

is favored like Turing's algorithm would. Whereas with PSTAB = 2,

 1. e4

is played as in the TUROCHAMP&mdash;Glennie game.

**Bare** removes the Turing heuristics and quiescence search and only contains the bare minimum a chess engine needs to play: alpha-beta search and a piece-square table.

**Newt** also does not use the Turing heuristics and adds newer chess programming techniques such as PV-based iterative deepening and an opening book (which unlike a normal opening book contains both good and bad openings). It is faster than the other two engines at the same search depth and offers more variety during the opening.

**SOMA** (the Smith One-Move Analyzer, 1961) is another early chess engine unrelated to TUROCHAMP. It only looks one ply ahead and uses swap-off values, total material, and square control criteria. SOMA is a much weaker engine than the other three.

**PTC-Host** lets you easily host games between the three engines directly from Python, without the need for a separate chess GUI.

Options for boosting program performance include PyPy and (for PyTuroChamp) running the multi-core version. Note that the multi-core version of PyTuroChamp only works on macOS and Linux but not on Windows. It is also possible to combine PyPy and multi-core.

### Comparison to the TUROCHAMP&mdash;Glennie game

The script glennie.py allows comparison of White's moves from the TUROCHAMP&mdash;Glennie game with PyTuroChamp's moves. Changing the parameters in pyturochamp.py will yield different results.

The best match seems to be PSTAB = 0, MAXPLIES = 1, QPLIES = 7 (or greater):
```
$ pypy3 glennie.py
pstab = 0, maxplies = 1, qplies = 7
1 e2e4 e2e3
4 g1f3 d4e5
6 d4d5 a2a3
10 f1b5 d2e3
15 h1g1 e1g1
17 a6b5 a6c4
19 b5c6 e2c4
22 c1d2 e2d2
23 g5g4 b2b3
25 d5b3 b2b3
26 b3c4 d1g1
27 g4g3 g4g5
===> 12 moves differ
```
This is similar to the [ChessBase Turing Engine](https://en.chessbase.com/post/reconstructing-turing-s-paper-machine), which produces 11 mismatches (in moves 1, 5, 15, 17, 18, 19, 20, 22, 23, 27, and 29), although the CB and PTC moves are seldom the same.

These best-fit parameters also agree with Turing's text who specified a brute-force depth of two plies (equal to MAXPLIES = 1 in the case of PTC) and a high but unknown selective search depth (QPLIES).

Turing's idea to evaluate material by dividing White's value by Black's value (instead of subtracting Black from White) can also be tested. The only difference is in move 17, where "W/B" plays h4h5 and "W-B" plays a6c4.

According to Stockfish analysis, the "W-B" move is also the only winning move for White, while the "W/B" move leads to a drawn position. So at least in this game, "W/B" is inferior to "W-B". (Also note that in the Glennie game, TUROCHAMP plays 17. a6b5, which is a blunder and possibly caused by a wrong computation of TUROCHAMP's moves by Turing and Glennie.)

### Differences between PyTuroChamp (PTC) and Turing's Paper Machine (TPM)

A piece-square table (PST) was added, so e.g. PTC will keep its king and queen on the back rank and advance its pawns. Without a PST, TPM has a tendency to e.g. move its queen all over the board during the opening repeatedly and generally not advance its pawns very much. Turing, had he implemented his TPM on a computer, might have noticed these problems and implemented something analogous to a PST. (The fact that PTC play 1. e3 whereas TUROCHAMP plays 1. e4 may be considered a justification for the need for a PST.)

Move ordering is also used by the engine to speed up search. This was not specified in the TPM, but humans also have a tendency to e.g. consider a queen or rook move before a pawn move, so move ordering might be said to be implicit in the way humans play the game. I.e., Turing first calculated moves that "looked good" to him and only later checked that all other moves were worse.

### Running the engines from a chess GUI

First, install the [python-chess](https://github.com/niklasf/python-chess) chess library: `pip install python-chess`

The recommended option on Linux or macOS is to modify and use the included shell scripts (ptc, bare, newt).

It is also possible and perhaps easier—especially on Windows—to launch Python directly from the GUI as in the Arena screenshot below. (Note that no log or PGN files will be created then, because the working directory will be somewhere where Python cannot create files.)

If you want to use one of the other engines besides pyturochamp.py, add "bare" or "newt" as additional command line parameters.

Cute Chess (Linux):

![screenshot](https://github.com/mdoege/PyTuroChamp/raw/master/pic/Screenshot_20180702_191254.png "Cute Chess configuration")

Arena (Linux):

![screenshot](https://github.com/mdoege/PyTuroChamp/raw/master/pic/Screenshot_20171123_102423.png "Arena configuration")

### UCI parameters

* maxplies (PTC, Bare)/depth (Newt): Brute-force search depth in plies
* qplies: Quiescence search depth in plies
* pstab: Piece-square table factor; 0 = no influence of PST
* pdead: Select function for dead position evaluation
    - 1 = more Turing-like and selective; it is only considered whether the capturing piece can itself be captured
    - 2 = less selective; any capture by the other side counts
* matetest: This switch selects whether mates or draws should also be evaluated at maximum search depth, not just the next move as in Turing's algorithm. It allows PTC to seek out or avoid mates and also avoid draws when it is ahead in material.
* MoveError: Choose randomly from moves that are up to MoveError (in decipawns) worse than the best move
* BlunderPercent: Chance of a blunder in percent
* BlunderError: If this move is a blunder, choose randomly from moves that are up to BlunderError (in decipawns) worse than the best move

Please note that for PTC and Bare, you should use odd numbers for maxplies and qplies (maxplies = 3 equals four plies; maxplies = 1 equals two plies). This is because PTC and Bare do not count the very first ply (i.e. the first own move considered).

Newt on the other hand counts plies normally from the root position, so maxplies and qplies should be even numbers.

### Files

|Filename | Description |
|---|---|
| pyturochamp.py | The chess engine with Turing's heuristics. Plays more human-like, except for weird but typical moves like a2a4 and h2h4. |
| bare.py | Bare bones version of PyTuroChamp, only alpha-beta and piece-square tables are used. Very computer-like and not pretty but sometimes efficient play. Stockfish took [62 moves to checkmate it](https://github.com/mdoege/PyTuroChamp/blob/master/ptc-bare-stockfish.pgn) (with ponder off). |
| newt.py | Like Bare, this engine does not include the Turing heuristics. It adds principal variation (PV)-based iterative deepening and quiescence search like PyTuroChamp and also an opening book, so it will not repeat the same moves in each game. |
| soma.py | The Smith One-Move Analyzer singple-ply engine |
| rmove.py | A random mover, primarily here as an adversary that SOMA can actually defeat |
| ptc, bare, newt, soma, rmove | Shells script to run PTC, Bare, Newt, SOMA or RMove from a chess GUI, e.g. [Cute Chess](https://github.com/cutechess/cutechess) , [KDE Knights](https://www.kde.org/applications/games/knights/) or [XBoard](https://www.gnu.org/software/xboard/). (Change the directory path inside first.)
| ptc-host.py | Hosts a game between PyTuroChamp as White and Bare as Black. Updated board images are written to board.svg. (During play, board.svg should be opened in an image viewer that automatically reloads changed files.)
| ptc_xboard.py | Combined XBoard and UCI interface module for all engines. Moves will also be logged to a PGN file. Uses pyturochamp_multi.py by default now. |
| movetest.py | Test engine responses to board situations |
| pst.py | Helper file with piece-square tables |
| pyturochamp_multi.py | Experimental multi-core version of PyTuroChamp |
| ptc_worker.py | Helper file for pyturochamp_multi.py |
| glennie.py | Compare White moves from TUROCHAMP vs. Glennie game to PyTuroChamp's moves and show differences (uses glennie.pgn) |

In the icons directory, there are several logos in BMP format for various chess engine GUIs which were contributed by [Norbert Raimund Leisner](https://chessprogramming.wikispaces.com/Norbert+Raimund+Leisner).

### Improving performance by using PyPy

Running the scripts with [PyPy3](http://pypy.org/) instead of python3 will make the engines run about two or three times as fast, so it is generally recommended to use PyPy.

Below is a sample terminal session that shows how to set up PyPy under **Arch Linux** and run the PyTuroChamp scripts.

Note that the "--local" command line switch is used here to install pip and python-chess into .local/ in the user's home directory. This is optional, but perhaps a good idea on Linux. It also means that root permissions are not necessary during installation.

```
# Install the Python 3 version of PyPy;
#  this command works only on Arch
#  and might be different on your Linux distro:
$ sudo pacman -S pypy3

# Install the pip package manager for PyPy:
$ pypy3 -m ensurepip --user

# Install python-chess:
$ pypy3 -m pip install python-chess --user

# Show packages installed under PyPy,
#  pyton-chess should be there now:
$ pypy3 -m pip list --user
Package      Version
------------ -------
pip          10.0.1 
python-chess 0.23.8 
setuptools   28.8.0 

# Run one of the chess engines with PyPy:
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

* Python 3 is recommended, but Python 2 should also work
* [python-chess](https://github.com/niklasf/python-chess)

### References

* Turing, Alan (1952): [*Digital computers applied to games*](https://docs.google.com/file/d/0B0xb4crOvCgTNmEtRXFBQUIxQWs/edit)
* [Chess Programming Wiki](https://chessprogramming.wikispaces.com/)
* Muller, H.G.: [*Micro-Max, a 133-line Chess Source*](http://home.hccnet.nl/h.g.muller/max-src2.html)

### License

* Public Domain
* The opening book and the piece-square tables from [Sunfish](https://github.com/thomasahle/sunfish) are licensed under the GPL.
