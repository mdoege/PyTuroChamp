![logo](https://github.com/mdoege/PyTuroChamp/raw/master/pic/ptc_banner.png "logo bar")

## PyTuroChamp, *Plankalkül*, SOMA, Bernstein, and *El Ajedrecista*

Python implementations of Alan Turing's [TUROCHAMP](https://chessprogramming.wikispaces.com/Turochamp) (1950), John Maynard Smith's [SOMA](https://chessprogramming.wikispaces.com/SOMA) (1961), [The Bernstein Chess Program](https://chessprogramming.wikispaces.com/The+Bernstein+Chess+Program) (1957), Leonardo Torres y Quevedo's [*El Ajedrecista*](https://en.wikipedia.org/wiki/El_Ajedrecista) (1912), and some related engines

**PyTuroChamp** is closest to the chess engine in Turing's paper, but adds optional piece-square tables that can be tuned with the PSTAB parameter. A higher parameter means more aggressive forward movement. With PSTAB = 0

 1. e3

is favored like Turing's algorithm would. Whereas with PSTAB = 2,

 1. e4

is played as in the TUROCHAMP&mdash;Glennie game.

**Bare** removes the Turing heuristics and quiescence search and only contains the bare minimum a chess engine needs to play: alpha-beta search and a piece-square table.

**Newt** also does not use the Turing heuristics and adds newer chess programming techniques such as PV-based iterative deepening and an opening book (which unlike a normal opening book contains both good and bad openings). It is faster than the other two engines at the same search depth, offers more variety during the opening, and has time management, so it works well for Blitz games.

***Plankalkül*** (1948) by Konrad Zuse is an early chess algorithm only based on material with no positional criteria. (Strictly speaking, *[Plankalkül](https://en.wikipedia.org/wiki/Plankalk%C3%BCl)* is Zuse's programming language in which his chess algorithm is implemented, but the terms are used interchangeably here.) If no tactics are within its tree search horizon, *Plankalkül* will play random moves.

Normally *Plankalkül* would only search one ply deep, but the version here defaults to four plies, at which it is somehwat weaker than PTC at its default settings but a bit stronger than SOMA.

**SOMA** (the Smith One-Move Analyzer, 1961) is another early chess engine and works very differently to TUROCHAMP.

SOMA was created by British biologist John Maynard Smith as a challenger to *Machiavelli*, which itself had been developed around the same time as TUROCHAMP. A game (with human-computed moves) between TUROCHAMP and *Machiavelli* was intended but never took place, but SOMA is very similar to *Machiavelli* in terms of its algorithm and playing strength, so it can be pitted against PyTuroChamp.

SOMA only looks one ply ahead and uses swap-off values, total material, and square control criteria. While SOMA is a somewhat weaker engine than the other ones, it requires far less than a second to compute a move.

**The Bernstein Chess Program** (1957) was developed by Alex Bernstein with his colleagues Michael de V. Roberts, Timothy Arbuckle, and Martin Belsky. On an IBM 704, one of the last vacuum tube computers, it searched four plies minimax in around 8 minutes, considering material, mobility, area control, and King defense.

The Bernstein Chess Program was the prototype of a selective forward pruning, Shannon Type B program: For each of four plies, seven plausible moves are selected by certain rules and saved to the plausible move table (PMT). Therefore, up to 7⁴+7³+7²+7 = 2,800 positions will be analyzed, although in practice due to Alpha-Beta the number will be lower.

***El Ajedrecista*** (1912) is an automaton built by Leonardo Torres y Quevedo, one of the first autonomous machines capable of playing chess. It played an endgame with three chess pieces, automatically moving a White King and a Rook to checkmate the Black King moved by a human opponent.

***El Ajedrecista* needs to play as White! (With Black, it will play random moves to enable self play.)**

The starting position should be set up with White's King and Rook on A8 and B7, respectively, while the Black King can be positioned anywhere on the first six ranks:

![torres](https://github.com/mdoege/PyTuroChamp/raw/master/pic/torres_start.png "A valid Torres starting position")

**PTC-Host** lets you easily host games between the three engines directly from Python, without the need for a separate chess GUI.

Options for boosting program performance include PyPy and (for PyTuroChamp) running the multi-core version. Note that the multi-core version of PyTuroChamp only works on macOS and Linux but not on Windows. It is also possible to combine PyPy and multi-core.

### Differences between PyTuroChamp (PTC) and Turing's Paper Machine (TPM)

**Material is evaluated as White minus Black** by PTC, while Turing preferred White divided by Black. Support for the latter is present in the code, but using the common approach of W-B means that the evaluation can be more easily compared to other engines. And in most situations, the choice between W-B and W/B does not influence the move chosen.

**Move ordering is used by the engine** to speed up search. This was not specified in the TPM, but humans also have a tendency to e.g. consider a queen or rook move before a pawn move, so move ordering might be said to be implicit in the way humans play the game. I.e., Turing first calculated moves that "looked good" to him and only later checked that all other moves were worse.

**An optional piece-square table (PST) was added**, so e.g. PTC will keep its king and queen on the back rank and advance its pawns. Without a PST, TPM has a tendency to e.g. move its queen all over the board during the opening repeatedly and generally not advance its pawns very much. Turing, had he implemented his TPM on a computer, might have noticed these problems and implemented something analogous to a PST. (The fact that PTC play 1. e3 whereas TUROCHAMP plays 1. e4 may be considered a justification for the need for a PST.)

### Running the engines from a chess GUI

First, install the [python-chess](https://github.com/niklasf/python-chess) chess library: `pip install python-chess`

The recommended option on Linux or macOS is to modify and use the included shell scripts (ptc, bare, newt).

It is also possible and perhaps easier—especially on Windows—to launch Python directly from the GUI as in the Arena screenshot below. (Note that no log or PGN files will be created then, because the working directory will be somewhere where Python cannot create files.)

If you want to use one of the other engines besides pyturochamp.py, add an additional command line parameter to ptc_xboard.py: newt, ptc, bare, plan, soma, bern, torres, or rmove.

**Cute Chess** (Linux version shown here):

![screenshot](https://github.com/mdoege/PyTuroChamp/raw/master/pic/Screenshot_20180702_191254.png "Cute Chess configuration")

**Arena** (Linux version shown here):

![screenshot](https://github.com/mdoege/PyTuroChamp/raw/master/pic/Screenshot_20171123_102423.png "Arena configuration")

### UCI parameters

* maxplies (PTC, Bare): Brute-force search depth in plies
* depth (Newt): Maximum brute-force search depth in plies. This can be set quite high, because it will never be reached: for Blitz games, time management will prevent it, while for longer time controls, maxnodes sets an upper limit for computation.
* usebook (Newt): Use opening book?
* maxnodes (Newt): How many nodes to search at most. Mainly useful for non-Blitz games to limit computation effort.
* qplies: Quiescence search depth in plies
* pstab: Piece-square table factor; 0 = no influence of PST
* matetest: This switch selects whether mates or draws should also be evaluated at maximum search depth, not just the next move as in Turing's algorithm. It allows PTC to seek out or avoid mates and also avoid draws when it is ahead in material. This also works for Newt and SOMA, which also have a tendency to reeach a draw even when they are ahead in material, because their normal evaluation function does not include any draw rules.
* pmtlen (Bernstein): Size of the plausible move table
* pmtstart (Bernstein): First ply where the PMT is used, so e.g. PMTSTART = 2 means that the PMT will not be used during the first two plies.
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
| plan.py | The *Plankalkül* engine |
| soma.py | The Smith One-Move Analyzer single-ply analyzer engine |
| bernstein.py | The Bernstein Chess Program |
| torres.py | *El Ajedrecista*, an automaton that checkmates Black with a Rook |
| rmove.py | A random mover |
| pyturochamp_multi.py | Experimental multi-core version of PyTuroChamp |

#### Helper scripts

|Filename | Description |
|---|---|
| ptc, bare, newt, plan, soma, bern, rmove | Shell script to run PTC, Bare, Plan, Newt, SOMA or RMove from a chess GUI, e.g. [Cute Chess](https://github.com/cutechess/cutechess) , [KDE Knights](https://www.kde.org/applications/games/knights/) or [XBoard](https://www.gnu.org/software/xboard/). (Change the directory path inside first.)
| ptc-host.py | Hosts a game between PyTuroChamp as White and Bare as Black. Updated board images are written to board.svg. (During play, board.svg should be opened in an image viewer that automatically reloads changed files.)
| ptc_xboard.py | Combined XBoard and UCI interface module for all engines. Moves will also be logged to a PGN file. Uses pyturochamp_multi.py by default now, but also allows selecting a different engine via a command line parameter (newt, ptc, bare, plan, soma, bern, torres, and rmove). |
| pst.py | Helper file with piece-square tables |
| ptc_worker.py | Helper file for pyturochamp_multi.py |

#### Test scripts

|Filename | Description |
|---|---|
| movetest.py | Test engine responses to board situations |
| glennie.py | Compare White moves from TUROCHAMP vs. Glennie game to PyTuroChamp's moves and show differences (uses glennie.pgn) |
| kasparov.py | Compare White moves from ChessBase TUROCHAMP vs. Kasparov game to PyTuroChamp's moves and show differences (uses kasparov_2012.pgn) |
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
```

### Comparison to historical games

#### TUROCHAMP&mdash;Glennie (1952)

The script glennie.py allows comparison of White's moves from the TUROCHAMP&mdash;Glennie game with PyTuroChamp's moves. Changing the parameters in pyturochamp.py will yield different results.

The best match is observed with PSTAB = 0, MAXPLIES = 1, QPLIES = 7 (or greater):
```
$ pypy3 glennie.py
pstab = 0, maxplies = 1, qplies = 7
# orig PTC
1 e2e4 e2e3
4 g1f3 d1d3
6 d4d5 a2a3
10 f1b5 d2e3
15 h1g1 e1g1
17 a6b5 a6c4
19 b5c6 e2c4
22 c1d2 e2e3
23 g5g4 b2b3
25 d5b3 d1g1
26 b3c4 d2e2
27 g4g3 g4g5
===> 12 moves differ
```
This is similar to the [ChessBase Turing Engine](https://en.chessbase.com/post/reconstructing-turing-s-paper-machine), which produces 11 mismatches (in moves 1, 5, 15, 17, 18, 19, 20, 22, 23, 27, and 29), although the CB and PTC moves are seldom the same.

These best-fit parameters also agree with Turing's text who specified a brute-force depth of two plies (equal to MAXPLIES = 1 in the case of PTC) and a high but unknown selective search depth (QPLIES).

Turing's idea to evaluate material by dividing White's value by Black's value (instead of subtracting Black from White) can also be tested. The only difference is in move 17, where "W/B" plays h4h5 and "W-B" plays a6c4.

According to Stockfish analysis, the "W-B" move is also the only winning move for White, while the "W/B" move leads to a drawn position. So at least in this game, "W/B" is inferior to "W-B". (Also note that in the Glennie game, TUROCHAMP plays 17. a6b5, which is a blunder and possibly caused by a wrong computation of TUROCHAMP's moves by Turing and Glennie.)

#### ChessBase TUROCHAMP&mdash;Kasparov (2012)
```
$ pypy3 kasparov.py
pstab = 0, maxplies = 1, qplies = 7
3 g1h3 h2h4
5 f1d3 a2a4
8 e4g3 e1g1
9 e1g1 b2b3
15 f1e1 c4b5
===> 5 moves differ
```
The ChessBase TUROCHAMP implementation does not play TUROCHAMP's signature moves a4 or h4 and prefers 3. Nh3 instead. As [Andre Adrian](http://www.andreadrian.de/schach/) notes, this probably means ChessBase TUROCHAMP has a bug, since the Knight would have more mobility on f3.

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
