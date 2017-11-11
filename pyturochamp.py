#!/usr/bin/env python3

# A Python chess engine,
# inspired by (but not compatible with)
# http://en.chessbase.com/post/reconstructing-turing-s-paper-machine

# not implemented: castling, pawn promotion, en passant capture

import chess as c
import math

# computer always plays as White

COMPC = c.WHITE
PLAYC = c.BLACK

MAXPLIES = 2	# maximum search depth; values between 0 and 3 are recommended

b = c.Board()

#b = c.Board("8/k7/8/3Q4/8/3r4/6K1/3b4 w - - 0 1")	# test position

# test position from Stockfish game
#b = c.Board("rn2k2r/1p3ppp/p4n2/Pb2p1B1/4P2P/2b1K3/R1P2PP1/3q1BNR w kq - 0 15")

def sqrt(x):
	"Rounded square root"
	return round(math.sqrt(x), 1)

def getpos(b):
	"Get positional-play value for a board"
	ppv = 0
	for i in range(64):
		m = b.piece_at(i)
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
			ppv += .2 * (i // 8 - 1)	# assumes computer plays White
			# pawn defended (other pawns do not count)
			pawndef = False
			for att in b.attackers(COMPC, i):
				if b.piece_at(att).piece_type != c.PAWN:
					pawndef = True
			if pawndef:
				ppv += .3
	# black king
	if b.is_check():
		ppv += .5
	for y in b.legal_moves:
		b.push(y)
		if b.is_checkmate():
			ppv += 1
		b.pop()
	return ppv

vals = {
c.PAWN : 1,
c.KNIGHT : 3,
c.BISHOP : 3.5,
c.ROOK : 5,
c.QUEEN : 10,
c.KING : 0.001,
}

def getval(b):
	"Get total piece value of board"
	wv, bv = 0, 0
	for i in range(64):
		m = b.piece_at(i)
		if m and m.color == c.WHITE:
			wv += vals[m.piece_type]
		if m and m.color == c.BLACK:
			bv += vals[m.piece_type]
	return wv / bv

def search(b, ply):
	"Search moves and evaluate positions (computer is assumed to play White)"
	b2 = c.Board(b.fen())
	if (ply // 2) == 0:
		bm = 0
	else:
		bm = 1000
	for x in b2.legal_moves:
		b2.push(x)
		if ply == MAXPLIES:
			t = getval(b2)
			if (ply // 2) == 0 and t > bm:
				bm = t
			if (ply // 2) == 1 and t < bm:
				bm = t
		else:
			bm = search(b2, ply + 1)
		b2.pop()
	return bm

while True:	# game loop
	lastpos = getpos(b)
	ll = []

	print(b)
	print(getval(b))
	print("FEN:", b.fen())

	nl = len(b.legal_moves)
	for n, x in enumerate(b.legal_moves):
		b.push(x)
		p = getpos(b) - lastpos
		t = search(b, 0)
		print("(%u/%u) %s %.1f %.3f" % (n + 1, nl, x, p, t))
		ll.append((x, p, t))
		b.pop()

	# sort mainly by piece values, and then by positional value
	ll.sort(key = lambda m: 100 * m[2] + m[1])
	ll.reverse()

	if not ll:
		print("You win!")
		break

	for x in ll:
		print(x)
	print()
	print("My move: %s" % ll[0][0])
	b.push(ll[0][0])

	while True:
		print(b)
		print(getval(b))
		move = input("Your move? ")
		try:
			b.push_san(move.strip())
		except:
			print("Sorry? Try again")
		else:
			break


