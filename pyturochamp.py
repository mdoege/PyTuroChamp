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

IMAXPLIES = 3	# inital maximum search depth
QPLIES    = IMAXPLIES + 4
PSTAB     = 5	# influence of piece-square table on moves, 0 = none

b = c.Board()

### Various test positions, with White to play:

#b = c.Board("8/k7/8/3Q4/8/3r4/6K1/3b4 w - - 0 1")

# test position from Stockfish game
#b = c.Board("rn2k2r/1p3ppp/p4n2/Pb2p1B1/4P2P/2b1K3/R1P2PP1/3q1BNR w kq - 0 15")

#b = c.Board("rnbqkb1r/pp3ppp/5n2/2pp4/P2Q3P/4P3/1PP2PP1/RNB1KBNR w KQkq - 0 6")

#b = c.Board("r1bqr1k1/1p3pp1/p1n2n1p/P1b4P/R5PR/2N1pN2/1PP2P2/3QKB2 w - - 0 15")

# http://www.telegraph.co.uk/science/2017/03/14/can-solve-chess-problem-holds-key-human-consciousness/
#b = c.Board("8/p7/kpP5/qrp1b3/rpP2b2/pP4b1/P3K3/8 w - - 0 1")

#b = c.Board("r2qk2r/1pp2ppp/p1nb1n2/8/3p2bP/1P4Q1/P1PP1P2/RNB1KBNR w KQkq - 2 10")

#b = c.Board("r3k2r/1pp2ppp/p2b4/8/1n1p1PbP/NP4K1/P1PP4/R1B1qBNR w kq - 1 15")

def sqrt(x):
	"Rounded square root"
	return round(math.sqrt(x), 1)

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
				ppv += PSTAB * pst[mm][i]               / 100

		if m and m.piece_type in (c.KING, c.QUEEN, c.ROOK, c.BISHOP, c.KNIGHT) and m.color == COMPC:
			mv_pt, cp_pt = 0, 0
			a = b.attacks(i)
			for s in a:
				e = b.piece_at(s)
				# empty square
				if not e:
					mv_pt += 1
				# enemy square
				elif e.color == PLAYC:
					cp_pt += 2
			ppv += sqrt(mv_pt + cp_pt)
			if m.piece_type != c.QUEEN and m.piece_type != c.KING:
				ndef = len(list(b.attackers(COMPC, i)))
				# defended
				if ndef == 1:
					ppv += 1
				# twice defended
				if ndef > 1:
					ppv += .5
			# king safety
			if m.piece_type == c.KING:
				b2 = c.Board(b.fen())
				b2.set_piece_at(i, c.Piece(c.QUEEN, COMPC))
				mv_pt, cp_pt = 0, 0
				a = b2.attacks(i)
				for s in a:
					e = b2.piece_at(s)
					# empty square
					if not e:
						mv_pt += 1
					# enemy square
					elif e.color == PLAYC:
						cp_pt += 2
				ppv -= sqrt(mv_pt + cp_pt)
		if m and m.piece_type == c.PAWN and m.color == COMPC:
			# pawn ranks advanced
			if COMPC == c.WHITE:
				ppv += .2 * (i // 8 - 1)
			else:
				ppv += .2 * (6 - i // 8)
			# pawn defended (other pawns do not count)
			pawndef = False
			for att in b.attackers(COMPC, i):
				if b.piece_at(att).piece_type != c.PAWN:
					pawndef = True
			if pawndef:
				ppv += .3
	# black king
	if b.is_check():
		ppv += .25
	for y in b.legal_moves:
		b.push(y)
		if b.is_checkmate():
			ppv += 1
		b.pop()
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
	if p >= QPLIES:
		return True
	x = b.pop()
	if b.is_capture(x) and len(b.attackers(not b.turn, x.to_square)):
		b.push(x)
		return False
	else:
		b.push(x)
		return True

# https://chessprogramming.wikispaces.com/Alpha-Beta
def searchmax(b, ply, alpha, beta):
	"Search moves and evaluate positions"
	if ply >= MAXPLIES and isdead(b, ply):
		return getval(b)
	for x in order(b, ply):
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
	if ply >= MAXPLIES and isdead(b, ply):
		return getval(b)
	for x in order(b, ply):
		b.push(x)
		t = searchmax(b, ply + 1, alpha, beta)
		b.pop()
		if t <= alpha:
			return alpha
		if t < beta:
			beta = t
	return beta

def order(b, ply):
	"Move ordering"
	if ply > 0:
		return b.legal_moves
	am, bm = [], []
	for x in b.legal_moves:
		if b.is_capture(x):
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
	global COMPC, PLAYC, MAXPLIES

	lastpos = getpos(b)
	ll = []

	MAXPLIES = IMAXPLIES + 3 * (((32 - len(b.piece_map())) / 32) ** 2)

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
	cr0 = b.has_castling_rights(COMPC)

	for n, x in enumerate(b.legal_moves):
		if b.is_castling(x):		# are we castling now?
			castle = 2 * pm()	# Turing uses 1
		else:
			castle = 0
		b.push(x)
		p = getpos(b) - lastpos + castle
		cr = b.has_castling_rights(COMPC)
		if cr0 == True and cr == True:	# can we still castle later?
			p += pm()
		for y in b.legal_moves:
			if b.is_castling(y):	# can we castle in the next move?
				p += pm()

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


