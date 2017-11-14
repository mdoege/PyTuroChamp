#!/usr/bin/env python3

# A Python chess engine,
# inspired by (but not compatible with)
# http://en.chessbase.com/post/reconstructing-turing-s-paper-machine

from pst import pst

import chess as c
import math, time

# computer plays as Black by default

COMPC = c.BLACK
PLAYC = c.WHITE

MAXPLIES = 3	# maximum search depth
PSTAB    = 1	# influence of piece-square table on moves, 0 = none

b = c.Board()

def getpos(b):
	"Get positional-play value for a board"
	ppv = 0
	for i in range(64):
		m = b.piece_at(i)
		if m and m.color == COMPC:
			mm = m.piece_type
			if mm == c.KING and (
			  len(b.pieces(c.PAWN, COMPC)) + len(b.pieces(c.PAWN, PLAYC)) ) <= 8:	# endgame is different
				mm = 8								#   for the King
			if COMPC == c.WHITE:
				j, k = i // 8, i % 8
				ppv += PSTAB * pst[mm][8 * (7 - j) + k] / 100
			else:
				ppv -= PSTAB * pst[mm][i]               / 100
	return ppv

def getval(b):
	"Get total piece value of board"
	return (
		len(b.pieces(c.PAWN, c.WHITE))          - len(b.pieces(c.PAWN, c.BLACK))
	+	3 * (len(b.pieces(c.KNIGHT, c.WHITE))   - len(b.pieces(c.KNIGHT, c.BLACK)))
	+	3.5 * (len(b.pieces(c.BISHOP, c.WHITE)) - len(b.pieces(c.BISHOP, c.BLACK)))
	+	5 * (len(b.pieces(c.ROOK, c.WHITE))     - len(b.pieces(c.ROOK, c.BLACK)))
	+	10* (len(b.pieces(c.QUEEN, c.WHITE))    - len(b.pieces(c.QUEEN, c.BLACK)))
	)

# https://chessprogramming.wikispaces.com/Alpha-Beta
def searchmax(b, ply, alpha, beta):
	"Search moves and evaluate positions"
	if ply == MAXPLIES:
		return getval(b)
	for x in b.legal_moves:
		b.push(x)
		t = searchmin(b, ply + 1, alpha, beta)
		b.pop()
		if t >= beta:
			return beta
		if t > alpha:
			alpha = t
	return alpha

def searchmin(b, ply, alpha, beta):
	"Search moves and evaluate positions"
	if ply == MAXPLIES:
		return getval(b)
	for x in b.legal_moves:
		b.push(x)
		t = searchmax(b, ply + 1, alpha, beta)
		b.pop()
		if t <= alpha:
			return alpha
		if t < beta:
			beta = t
	return beta

def pm():
	if COMPC == c.WHITE:
		return 1
	else:
		return -1

def getmove(b, silent = False):
	"Get move list for board"
	global COMPC, PLAYC

	lastpos = getpos(b)
	ll = []

	if b.turn == c.WHITE:
		COMPC = c.WHITE
		PLAYC = c.BLACK
	else:
		COMPC = c.BLACK
		PLAYC = c.WHITE

	if not silent:
		print(b)
		print(getval(b))
		print("FEN:", b.fen())

	nl = len(b.legal_moves)

	# move ordering
	am = []
	for x in b.legal_moves:
		if b.is_capture(x):
			am.append((x, 10))
		else:
			am.append((x, b.piece_at(x.from_square).piece_type))
	am.sort(key = lambda m: m[1])
	am.reverse()

	for n, q in enumerate(am):
		x = q[0]
		b.push(x)
		p = getpos(b) - lastpos
		if COMPC == c.WHITE:
			t = searchmin(b, 0, -1e6, 1e6)
		else:
			t = searchmax(b, 0, -1e6, 1e6)
		if not silent:
			print("(%u/%u) %s %.1f %.2f" % (n + 1, nl, x, p, t))
		ll.append((x, p, t))
		b.pop()

	ll.sort(key = lambda m: m[1] + m[2])
	if COMPC == c.WHITE:
		ll.reverse()
	return ll

if __name__ == '__main__':
	while True:	# game loop
		while True:
			print(b)
			print(getval(b))
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
		ll = getmove(b)
		for x in ll:
			print(x)
		print()
		print("My move: %u. %s     ( calculation time spent: %u m %u s )" % (
			b.fullmove_number, ll[0][0],
			(time.time() - tt) // 60, (time.time() - tt) % 60))
		b.push(ll[0][0])

		if b.result() != '*':
			print("Game result:", b.result())
			break


