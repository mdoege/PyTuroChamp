#!/usr/bin/env python3

# Compare moves from PyTuroChamp with desired results

import chess as c
import pyturochamp as p

t = [
 ("7k/1P3ppp/8/8/8/8/2K5/8 w - - 0 1", 'b7b8q', 'pawn promotion'),
 ("r1bqk1nr/pppp1ppp/1bn1p3/8/2BP4/4PN2/PPP2PPP/RNBQK2R w KQkq - 1 5", 'e1g1', 'castling'),

]

for x, y, z in t:
	d = c.Board(x)
	l = p.getmove(d)
	r = str(l[0][0])
	if r == y:
		print(z, "test passed", 30 * '=')
	else:
		print(z, "test FAILED:", r, 30 * '*')


