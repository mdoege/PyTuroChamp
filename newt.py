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

DEPTH = 4	# maximum search depth
QPLIES    = 4
PSTAB     = .1	# influence of piece-square table on moves, 0 = none

b = c.Board()
PV = 50 * [0]

def getpos(b):
	"Get positional-play value for a board"
	ppv = 0
	for i in b.piece_map().keys():
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
				ppv += PSTAB * pst[mm][i]               / 100
	# ppv has been computed as positive = good until here,
	#   finally we add the sign here to be compatible with getval()'s score
	if COMPC == c.WHITE:
		return ppv
	else:
		return -ppv

def getval(b):
	"Get total piece value of board"
	return (
		len(b.pieces(c.PAWN, c.WHITE))          - len(b.pieces(c.PAWN, c.BLACK))
	+	3 * (len(b.pieces(c.KNIGHT, c.WHITE))   - len(b.pieces(c.KNIGHT, c.BLACK)))
	+	3.5 * (len(b.pieces(c.BISHOP, c.WHITE)) - len(b.pieces(c.BISHOP, c.BLACK)))
	+	5 * (len(b.pieces(c.ROOK, c.WHITE))     - len(b.pieces(c.ROOK, c.BLACK)))
	+	10* (len(b.pieces(c.QUEEN, c.WHITE))    - len(b.pieces(c.QUEEN, c.BLACK)))
	)

def isdead(b, p):
	"Is the position dead? (quiescence) I.e., can the capturing piece be recaptured?"
	if p <= -QPLIES:
		return True
	if b.is_check():
		return False
	x = b.pop()
	if (b.is_capture(x) and len(b.attackers(not b.turn, x.to_square))) or b.is_check():
		b.push(x)
		return False
	else:
		b.push(x)
		return True

# https://chessprogramming.wikispaces.com/Alpha-Beta
def searchmax(b, ply, alpha, beta):
	"Search moves and evaluate positions for White"
	if ply <= 0 and isdead(b, ply):
		return getval(b) + getpos(b), [str(q) for q in b.move_stack]
	v = None
	for x in order(b, ply):
		b.push(x)
		t, vv = searchmin(b, ply - 1, alpha, beta)
		b.pop()
		if t >= beta:
			return beta, vv
		if t > alpha:
			alpha = t
			v = vv
	return alpha, v

def searchmin(b, ply, alpha, beta):
	"Search moves and evaluate positions for Black"
	if ply <= 0 and isdead(b, ply):
		return getval(b) + getpos(b), [str(q) for q in b.move_stack]
	v = None
	for x in order(b, ply):
		b.push(x)
		t, vv = searchmax(b, ply - 1, alpha, beta)
		b.pop()
		if t <= alpha:
			return alpha, vv
		if t < beta:
			beta = t
			v = vv
	return beta, v

def order(b, ply):
	"Move ordering"
	if 1 < ply < MAXPLIES:
		return b.legal_moves
	am, bm = [], []
	for x in b.legal_moves:
		#if MAXPLIES - ply < len(PV) and str(x) == PV[MAXPLIES - ply]:
		if str(x) in PV:
			am.append((x, 1000))
			#print(x)
		elif b.is_capture(x):
			if b.piece_at(x.to_square):
				# MVV/LVA sorting (http://home.hccnet.nl/h.g.muller/mvv.html)
				am.append((x, 10 * b.piece_at(x.to_square).piece_type
							- b.piece_at(x.from_square).piece_type))
			else:	# to square is empty during en passant capture
				am.append((x, 10 - b.piece_at(x.from_square).piece_type))
		else:
			am.append((x, b.piece_at(x.from_square).piece_type))
	am.sort(key = lambda m: m[1])
	am.reverse()
	bm = [q[0] for q in am]
	return bm

def pm():
	if COMPC == c.WHITE:
		return 1
	else:
		return -1

def getmove(b, silent = False):
	"Get move list for board"
	global COMPC, PLAYC, MAXPLIES, PV

	if b.turn == c.WHITE:
		COMPC = c.WHITE
		PLAYC = c.BLACK
	else:
		COMPC = c.BLACK
		PLAYC = c.WHITE

	if not silent:
		print("FEN:", b.fen())

	for MAXPLIES in range(2, DEPTH + 1):
		if COMPC == c.WHITE:
			t, PV = searchmax(b, MAXPLIES, -1e6, 1e6)
		else:
			t, PV = searchmin(b, MAXPLIES, -1e6, 1e6)

		try:
			PV = PV[len(b.move_stack):]	# separate principal variation from moves already played
			print('# %u %.2f %s' % (MAXPLIES, t, str(PV)))
		except:
			PV = [str(list(b.legal_moves)[0])]	# we will get checkmated very soon, so pick the available move

	return t, PV

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
				print(b)
			except:
				print("Sorry? Try again. (Or type Control-C to quit.)")
			else:
				break

		if b.result() != '*':
			print("Game result:", b.result())
			break

		tt = time.time()
		t, ppp = getmove(b)
		print(t, ppp)
		print("My move: %u. %s" % (b.fullmove_number, ppp[0]))
		print("  ( calculation time spent: %u m %u s )" % ((time.time() - tt) // 60, (time.time() - tt) % 60))
		b.push(c.Move.from_uci(ppp[0]))

		if b.result() != '*':
			print("Game result:", b.result())
			break


