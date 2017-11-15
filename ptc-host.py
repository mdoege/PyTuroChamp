#!/usr/bin/env python3

# Hosts a game between PyTuroChamp as White and Bare as Black
# (Updated board images are written to board.svg.)

import sys
import chess as c
import chess.svg
import pyturochamp as white
import bare as black

d = c.Board()

def svg():
	lm = d.peek()
	a = [(lm.from_square, lm.to_square)]
	s = chess.svg.board(d, arrows = a, size = 800)

	with open("board.svg", 'w') as f:
		f.write(s)

def move(r, t = ''):
	if r:
		rm = str(r[0][0])
		print("%u. %s%s" % (d.fullmove_number, t, str(r[0][0])))
		d.push_uci(rm)
	if d.result() != '*':
		svg()
		print(d.result())
		sys.exit(0)
	svg()

while True:
	move(white.getmove(d, silent = True))
	move(black.getmove(d, silent = True), t = '... ')

