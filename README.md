## The PyTuroChamp, *Plankalkül*, SOMA, Bernstein, and *El Ajedrecista* Python chess engines

Python implementations of Alan Turing's [TUROCHAMP](https://chessprogramming.org/Turochamp) (1950), John Maynard Smith's [SOMA](https://chessprogramming.org/SOMA) (1961), [The Bernstein Chess Program](https://chessprogramming.org/The_Bernstein_Chess_Program) (1957), Leonardo Torres y Quevedo's [*El Ajedrecista*](https://en.wikipedia.org/wiki/El_Ajedrecista) (1912), and some related engines

### Prerequisites

* PyPy 3 is best, but regular Python 3 or 2 also works
* [python-chess](https://github.com/niklasf/python-chess) (Note that since v0.24, python-chess is for Python 3 only.)

### Quick start

Install python-chess and then either run one of the chess engines with the UCI/XBoard interface (mainly for chess GUIs), e.g.:

 $ pypy3 ptc_xboard.py soma

Or run an engine with the console interface (Unicode output; enter your moves as e.g. "e2e4"; use black on white text in the terminal for correct piece colors):

 $ pypy3 pyturochamp.py

See the [chess GUI page](http://mdoege.github.io/PyTuroChamp/gui.html) for details on how to set up the chess engines in e.g. Cute Chess or Arena.

### Documentation

Full documentation at [mdoege.github.io/PyTuroChamp/](http://mdoege.github.io/PyTuroChamp/)

### Web browser version

There are also browser-based versions of most of these engines (with a Python backend) at [github.com/mdoege/TUROjs](https://github.com/mdoege/TUROjs).

### License

* Public Domain
* The opening book is licensed under the GPL.
