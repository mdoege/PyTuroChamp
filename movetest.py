#!/usr/bin/env python3

# Compare moves from PyTuroChamp with desired results

import chess as c
#import pyturochamp as p
#import bare as p
import newt as p

t = [
 ("r1bb2rk/pp3p1p/5p1Q/2p2N2/2p1P3/2B5/PPPK1PPP/R6R w - - 1 18", 'c3f6', 'Mate in 3 vs Sunfish'),
 #("5rkr/p5p1/1b1N2q1/3Pp2p/4N1b1/5B2/PPP1QP1P/RK1R4 w - - 1 29", 'f3g4', 'Newt-Bare first blunder'),
 #("5rkr/p5p1/1b1N2q1/3Pp2p/4N3/3R1b2/PPP1QP1P/RK6 w - - 0 30", 'e2e1', 'Newt-Bare 2nd blunder'),
 #("7k/1P3ppp/8/8/8/8/2K5/8 w - - 0 1", 'b7b8q', 'pawn promotion'),
 #("r1bqk1nr/pppp1ppp/1bn1p3/8/2BP4/4PN2/PPP2PPP/RNBQK2R w KQkq - 1 5", 'e1g1', 'castling'),
 #("5rk1/2p1bppp/Q7/1p2n3/5n2/2Pq3b/PP1P1PPP/RNBB1RK1 b - - 0 14", 'h3g2', 'HAL 9000 vs Poole'),
]

for x, y, z in t:
	d = c.Board(x)
	t, r = p.getmove(d, usebook = False)
	if r[0] == y:
		print(z, "test passed", 30 * '=')
	else:
		print(z, "test FAILED:", r[0], 30 * '*')


