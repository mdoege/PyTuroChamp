#!/usr/bin/env python3

# El Ajedrecista by Torres-Quevedo (1912)

import chess as c
import sys, math, time
from random import random, choice


b = c.Board('K7/1R6/8/8/8/8/8/7k b - - 0 1')

# pick a random position for the Black King on the first six ranks
b.remove_piece_at(7)
b.set_piece_at(choice(range(6 * 8)), c.Piece(c. KING, c.BLACK))

rookdir = 1
COMPC = c.WHITE
PLAYC = c.BLACK

def wmove(x1, y1, x2, y2, reason):
	"Get White move"
	uci = '%s%s%s%s' % (c.FILE_NAMES[x1], c.RANK_NAMES[y1], c.FILE_NAMES[x2], c.RANK_NAMES[y2])
	print('# ', reason)
	return 0, [uci]

def getmove(b, silent = False, usebook = False):
	"Get move for board"
	global rookdir

	# play random legal moves as Black to allow self play
	if b.turn == c.BLACK:
		bmove = choice(list(b.legal_moves))
		return 0, [str(bmove)]

	for i in b.piece_map().keys():
		m = b.piece_at(i)
		if m.piece_type == c.KING and m.color == c.WHITE:
			wk = i
			wkx, wky = c.square_file(i), c.square_rank(i)
		if m.piece_type == c.KING and m.color == c.BLACK:
			bk = i
			bkx, bky = c.square_file(i), c.square_rank(i)
		if m.piece_type == c.ROOK and m.color == c.WHITE:
			wr = i
			wrx, wry = c.square_file(i), c.square_rank(i)

	if wr in b.attacks(bk):
		if wrx < 4:
			return wmove(wrx, wry, 7, wry, 'move Rook right')
		else:
			return wmove(wrx, wry, 0, wry, 'move Rook left')
	else:
		if wry - bky > 1:
			return wmove(wrx, wry, wrx, wry - 1, 'move Rook down')
		else:
			vd = wky - bky
			hd = abs(wkx - bkx)
			if vd > 2:
				return wmove(wkx, wky, wkx, wky - 1, 'move King down')
			else:
				if hd == 0:
					return wmove(wrx, wry, wrx, wry - 1, 'move Rook down')
				elif hd % 2 == 0:
					if wkx < bkx:
						return wmove(wkx, wky, wkx + 1, wky, 'move King towards King')
					else:
						return wmove(wkx, wky, wkx - 1, wky, 'move King towards King')
				else:
					if wrx == 0:
						rookdir = 1
					if wrx == 7:
						rookdir = -1
					return wmove(wrx, wry, wrx + rookdir, wry, 'move Rook horizontally')

if __name__ == '__main__':
	while True:	# game loop
		while True:
			print(b.unicode())
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


