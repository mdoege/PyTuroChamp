![logo](https://github.com/mdoege/PyTuroChamp/raw/master/icons/out.png "logo bar")

## PyTuroChamp, SOMA, and *El Ajedrecista*

Python implementations of Alan Turing's [TUROCHAMP](https://chessprogramming.wikispaces.com/Turochamp) (1950), John Maynard Smith's [SOMA](https://chessprogramming.wikispaces.com/SOMA) (1961), [The Bernstein Chess Program](https://chessprogramming.wikispaces.com/The+Bernstein+Chess+Program) (1957), Leonardo Torres y Quevedo's [*El Ajedrecista*](https://en.wikipedia.org/wiki/El_Ajedrecista) (1912), and some related engines

**PyTuroChamp** is closest to the chess engine in Turing's paper, but adds optional piece-square tables that can be tuned with the PSTAB parameter. A higher parameter means more aggressive forward movement. With PSTAB = 0,

 1. e3

is favored like Turing's algorithm would. Whereas with PSTAB = 2,

 1. e4

is played as in the TUROCHAMP&mdash;Glennie game.

**Bare** removes the Turing heuristics and quiescence search and only contains the bare minimum a chess engine needs to play: alpha-beta search and a piece-square table.

**Newt** also does not use the Turing heuristics and adds newer chess programming techniques such as PV-based iterative deepening and an opening book (which unlike a normal opening book contains both good and bad openings). It is faster than the other two engines at the same search depth, offers more variety during the opening, and has time management, so it works well for Blitz games.

**SOMA** (the Smith One-Move Analyzer, 1961) is another early chess engine and works very differently to TUROCHAMP.

SOMA was created by British biologist John Maynard Smith as a challenger to *Machiavelli*, which itself had been developed around the same time as TUROCHAMP. A game (with human-computed moves) between TUROCHAMP and *Machiavelli* was intended but never took place, but SOMA is very similar to *Machiavelli* in terms of its algorithm and playing strength, so it can be pitted against PyTuroChamp.

SOMA only looks one ply ahead and uses swap-off values, total material, and square control criteria. While SOMA is a somewhat weaker engine than the other ones, it requires far less than a second to compute a move.

**The Bernstein Chess Program'' was developed by Alex Bernstein with his colleagues Michael de V. Roberts, Timothy Arbuckle, and Martin Belsky in 1957 and ran on an IBM 704. The Bernstein Chess Program was the prototype of a selective forward pruning, Shannon Type B program. On an IBM 704, one of the last vacuum tube computers, it searched four plies minimax in around 8 minutes, considering the seven most plausible moves from each position and evaluated material, mobility, area control and king defense.

***El Ajedrecista*** is an automaton built in 1912 by Leonardo Torres y Quevedo, one of the first autonomous machines capable of playing chess. It played an endgame with three chess pieces, automatically moving a White King and a Rook to checkmate the Black King moved by a human opponent.

The starting position should be set up with White's King and Rook on A8 and B7, respectively, while the Black King can be positioned anywhere on the first six ranks:

![torres](https://github.com/mdoege/PyTuroChamp/raw/master/pic/torres_start.png "A valid Torres starting position")

**PTC-Host** lets you easily host games between the three engines directly from Python, without the need for a separate chess GUI.

Options for boosting program performance include PyPy and (for PyTuroChamp) running the multi-core version. Note that the multi-core version of PyTuroChamp only works on macOS and Linux but not on Windows. It is also possible to combine PyPy and multi-core.

### Comparisons to historical games

#### TUROCHAMP&mdash;Glennie (1952)

The script glennie.py allows comparison of White's moves from the TUROCHAMP&mdash;Glennie game with PyTuroChamp's moves. Changing the parameters in pyturochamp.py will yield different results.

The best match seems to be PSTAB = 0, MAXPLIES = 1, QPLIES = 7 (or greater):
```
$ pypy3 glennie.py
pstab = 0, maxplies = 1, qplies = 7
# orig PTC
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

#### SOMA&mdash;Machiavelli (1961)

A similiar comparison can be done to the SOMA game recorded in *New Scientist* (November 9, 1961; page 369) using somatest.py.

Taking into account the random move selection feature of SOMA, the best-matched game from soma.py includes eight moves that differ from those given in the *New Scientist* article. (Soma.py's own moves also vary due to randomness of course.)

However, the description of the SOMA algorithm in *New Scientist* leaves out some details, so a few differences are to be expected. Also, SOMA's moves in the 1961 article were computed by the article's author, not a computer, so errors in computation are a possibility.
```
# orig soma.py
2 d2d4 d1g4
3 b1c3 g1f3
7 c1d2 d1h5
10 f1e2 f2f3
13 f3e4 e2a6
18 e2f3 e2d3
24 d5b5 d5d8
27 e4f5 a5c3
```

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

* maxplies (PTC, Bare): Brute-force search depth in plies
* depth (Newt): Maximum brute-force search depth in plies. This can be set quite high, because it will never be reached: for Blitz games, time management will prevent it, while for longer time controls, maxnodes sets an upper limit for computation.
* maxnodes (Newt): How many nodes to search at most. Mainly useful for non-Blitz games to limit computation effort.
* qplies: Quiescence search depth in plies
* pstab: Piece-square table factor; 0 = no influence of PST
* pdead: Select function for dead position evaluation
    - 1 = more Turing-like and selective; it is only considered whether the capturing piece can itself be captured
    - 2 = less selective; any capture by the other side counts
* matetest: This switch selects whether mates or draws should also be evaluated at maximum search depth, not just the next move as in Turing's algorithm. It allows PTC to seek out or avoid mates and also avoid draws when it is ahead in material. This also works for Newt and SOMA, which also have a tendency to reeach a draw even when they are ahead in material, because their normal evaluation function does not include any draw rules.
* pmtlen (Bernstein): Length of the Plausible Move Table
* MoveError: Choose randomly from moves that are up to MoveError (in decipawns) worse than the best move
* BlunderPercent: Chance of a blunder in percent
* BlunderError: If this move is a blunder, choose randomly from moves that are up to BlunderError (in decipawns) worse than the best move

Please note that for PTC and Bare, you should use odd numbers for maxplies and qplies (maxplies = 3 equals four plies; maxplies = 1 equals two plies). This is because PTC and Bare do not count the very first ply (i.e. the first own move considered).

Newt on the other hand counts plies normally from the root position, so maxplies and qplies should be even numbers.

### Files

#### Engines

|Filename | Description |
|---|---|
| pyturochamp.py | The chess engine with Turing's heuristics. Plays more human-like, except for weird but typical moves like a2a4 and h2h4. |
| bare.py | Bare bones version of PyTuroChamp, only alpha-beta and piece-square tables are used. Very computer-like and not pretty but sometimes efficient play. Stockfish took [62 moves to checkmate it](https://github.com/mdoege/PyTuroChamp/blob/master/ptc-bare-stockfish.pgn) (with ponder off). |
| newt.py | Like Bare, this engine does not include the Turing heuristics. It adds principal variation (PV)-based iterative deepening and quiescence search like PyTuroChamp and also an opening book, so it will not repeat the same moves in each game. |
| soma.py | The Smith One-Move Analyzer single-ply analyzer engine |
| bernstein.py | The Bernstein Chess Program |
| torres.py | *El Ajedrecista*, an automaton that checkmates Black with a Rook |
| rmove.py | A random mover |
| pyturochamp_multi.py | Experimental multi-core version of PyTuroChamp |

#### Helper scripts

|Filename | Description |
|---|---|
| ptc, bare, newt, soma, bern, rmove | Shells script to run PTC, Bare, Newt, SOMA or RMove from a chess GUI, e.g. [Cute Chess](https://github.com/cutechess/cutechess) , [KDE Knights](https://www.kde.org/applications/games/knights/) or [XBoard](https://www.gnu.org/software/xboard/). (Change the directory path inside first.)
| ptc-host.py | Hosts a game between PyTuroChamp as White and Bare as Black. Updated board images are written to board.svg. (During play, board.svg should be opened in an image viewer that automatically reloads changed files.)
| ptc_xboard.py | Combined XBoard and UCI interface module for all engines. Moves will also be logged to a PGN file. Uses pyturochamp_multi.py by default now, but also allows selecting a different engine via a command line parameter (newt, ptc, bare, soma, bern, torres, and rmove). |
| pst.py | Helper file with piece-square tables |
| ptc_worker.py | Helper file for pyturochamp_multi.py |

#### Test scripts

|Filename | Description |
|---|---|
| movetest.py | Test engine responses to board situations |
| glennie.py | Compare White moves from TUROCHAMP vs. Glennie game to PyTuroChamp's moves and show differences (uses glennie.pgn) |
| somatest.py | Compare White moves from SOMA vs. Machiavelli game to soma.py's moves and show differences (uses soma-mac.pgn) |
| berntest.py | Compare White moves to the IBM 704 vs Human game (uses bernstein_ibm704.pgn)

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
* Smith, John M. and Michie, Donald (1961): [Machines that play games](https://books.google.de/books?id=lo7r0zX_T0sC&lpg=PA369&dq=Machines+that+play+games.+1961,+New+Scientist,+12&pg=PA367&redir_esc=y#v=onepage&q&f=false)
* [Chess Programming Wiki](https://chessprogramming.wikispaces.com/)
* Muller, H.G.: [*Micro-Max, a 133-line Chess Source*](http://home.hccnet.nl/h.g.muller/max-src2.html)

### License

* Public Domain
* The opening book and the piece-square tables from [Sunfish](https://github.com/thomasahle/sunfish) are licensed under the GPL.
