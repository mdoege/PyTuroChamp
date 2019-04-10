#!/usr/bin/env python3

# A Random Mover

import chess as c
import sys, math, time
from random import random, choice

COMPC = c.WHITE
PLAYC = c.BLACK


b = c.Board()

def getval(b):
	"Get total piece value of board"
	return (
		len(b.pieces(c.PAWN, c.WHITE))          - len(b.pieces(c.PAWN, c.BLACK))
	+	3 * (len(b.pieces(c.KNIGHT, c.WHITE))   - len(b.pieces(c.KNIGHT, c.BLACK)))
	+	3.5 * (len(b.pieces(c.BISHOP, c.WHITE)) - len(b.pieces(c.BISHOP, c.BLACK)))
	+	5 * (len(b.pieces(c.ROOK, c.WHITE))     - len(b.pieces(c.ROOK, c.BLACK)))
	+	10 * (len(b.pieces(c.QUEEN, c.WHITE))   - len(b.pieces(c.QUEEN, c.BLACK)))
	)

def pm():
	if COMPC == c.WHITE:
		return 1
	else:
		return -1

def getmove(b, silent = False, usebook = False):
	"Get move list for board"
	global COMPC, PLAYC, MAXPLIES

	if b.turn == c.WHITE:
		COMPC = c.WHITE
		PLAYC = c.BLACK
	else:
		COMPC = c.BLACK
		PLAYC = c.WHITE

	if not silent:
		print('# ', b)
		print('# ', getval(b))
		print('# ', "FEN:", b.fen())

	nl = len(list(b.legal_moves))
	move = str(choice(list(b.legal_moves)))
	print('info score cp %d' % (100 * pm() * getval(b)))
	return 0, [move]

if __name__ == '__main__':
	while True:	# game loop
		while True:
			print(b.unicode())
			print(getval(b))
			if sys.version < '3':
				move = raw_input("Your move? ")
			else:
				move = input("Your move? ")
			try:
				try:
					b.push_san(move)
				except ValueError:
					b.push_uci(move)
			except:
				print("Sorry? Try again. (Or type Control-C to quit.)")
			else:
				break

		if b.result() != '*':
			print("Game result:", b.result())
			break

		tt = time.time()
		t, m = getmove(b)
		print("My move: %u. %s     ( calculation time spent: %u m %u s )" % (
			b.fullmove_number, m[0],
			(time.time() - tt) // 60, (time.time() - tt) % 60))
		b.push(c.Move.from_uci(m[0]))

		if b.result() != '*':
			print("Game result:", b.result())
			break


