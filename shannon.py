#!/usr/bin/env python3

import chess as c
import sys, math, time

# computer plays as Black by default

COMPC = c.BLACK
PLAYC = c.WHITE

MAXPLIES = 1	# maximum search depth
QPLIES    = MAXPLIES + 6
MATETEST  = True	# if True, include draw and mate on next move detection in the material eval
PAWNRULE  = True	# use pawn criteria

b = c.Board()
NODES = 0

def getpawnfile(b, col):
	pf = 10 * [0]
	for i in b.piece_map().keys():
		m = b.piece_at(i)
		if m and m.color == col:
			mm = m.piece_type
			if mm == c.PAWN:
				mf = c.square_file(i)
				pf[mf + 1] += 1
	return pf

def getiso(pf):
	iso = 0
	for i in range(1, 9):
		if pf[i] > 0 and pf[i - 1] == 0 and pf[i + 1] == 0:
			iso += 1
	return iso

def getdoub(pf):
	doub = 0
	for i in range(1, 9):
		if pf[i] > 1:
			doub += pf[i] - 1
	return doub

def getback(b, col):
	back = 0
	for i in b.piece_map().keys():
		m = b.piece_at(i)
		if m and m.color == col:
			mm = m.piece_type
			if mm == c.PAWN:
				sf = c.square_file(i)
				left_f = max(0, sf - 1)
				right_f = min(7, sf + 1)
				sr = c.square_rank(i)
				if col == c.WHITE:
					top_r = sr
					bot_r = 0
				else:
					top_r = 7
					bot_r = sr
				num_p = 0
				for x in range(left_f, right_f + 1):
					for y in range(bot_r, top_r + 1):
						q = b.piece_at(8 * y + x)
						if q and q.color == col and q.piece_type == c.PAWN:
							num_p += 1
				if num_p == 1:
					if col == c.WHITE:
						top_r = 7
						bot_r = sr + 1
					else:
						top_r = sr - 1
						bot_r = 0
					for y in range(bot_r, top_r + 1):
						j = 8 * y + sf
						enpawn = False
						for att in b.attackers(not col, j):
							if b.piece_at(att).piece_type == c.PAWN:
								enpawn = True
					if enpawn:
						back += 1
	return back

def getval(b):
	"Get total piece value of board"
	v = (
		len(b.pieces(c.PAWN, c.WHITE))          - len(b.pieces(c.PAWN, c.BLACK))
	+	3 * (len(b.pieces(c.KNIGHT, c.WHITE))   - len(b.pieces(c.KNIGHT, c.BLACK)))
	+	3 * (len(b.pieces(c.BISHOP, c.WHITE))   - len(b.pieces(c.BISHOP, c.BLACK)))
	+	5 * (len(b.pieces(c.ROOK, c.WHITE))     - len(b.pieces(c.ROOK, c.BLACK)))
	+	9 * (len(b.pieces(c.QUEEN, c.WHITE))    - len(b.pieces(c.QUEEN, c.BLACK)))
	)
	if PAWNRULE:
		wf = getpawnfile(b, c.WHITE)
		bf = getpawnfile(b, c.BLACK)
		wiso = getiso(wf)
		biso = getiso(bf)
		wdoub = getdoub(wf)
		bdoub = getdoub(bf)
		wback = getback(b, c.WHITE)
		bback = getback(b, c.BLACK)
		v = v - .5 * (wdoub - bdoub + wiso - biso + wback - bback)
	oturn = b.turn
	b.turn = c.WHITE
	wmov = len(list(b.legal_moves))
	b.turn = c.BLACK
	bmov = len(list(b.legal_moves))
	b.turn = oturn
	v += .1 * (wmov - bmov)
	return v

def isdead(b, ml, p):
	"Is the position dead? (quiescence)"
	if p >= QPLIES or not len(ml):
		return True
	x = b.pop()
	if (b.is_capture(x) and len(b.attackers(not b.turn, x.to_square))):
		b.push(x)
		return False
	else:
		b.push(x)
		return True

# https://chessprogramming.org/Alpha-Beta
def searchmax(b, ply, alpha, beta):
	"Search moves and evaluate positions"
	global NODES

	NODES += 1
	if MATETEST:
		res = b.result(claim_draw = True)
		if res == '0-1':
			return -1000
		if res == '1-0':
			return 1000
		if res == '1/2-1/2':
			return 0
	ml = order(b, ply)
	if ply >= MAXPLIES and isdead(b, ml, ply):
		return getval(b)
	if ply >= MAXPLIES:
		ml2 = []
		for x in ml:
			if b.is_capture(x):
				ml2.append(x)
		if len(ml2) == 0:	# no considerable moves
			return getval(b)
	else:
		ml2 = ml
	for x in ml2:
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
	global NODES

	NODES += 1
	if MATETEST:
		res = b.result(claim_draw = True)
		if res == '0-1':
			return -1000
		if res == '1-0':
			return 1000
		if res == '1/2-1/2':
			return 0
	ml = order(b, ply)
	if ply >= MAXPLIES and isdead(b, ml, ply):
		return getval(b)
	if ply >= MAXPLIES:
		ml2 = []
		for x in ml:
			if b.is_capture(x):
				ml2.append(x)
		if len(ml2) == 0:	# no considerable moves
			return getval(b)
	else:
		ml2 = ml
	for x in ml2:
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
		return list(b.legal_moves)
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

def getmove(b, silent = False, usebook = False):
	"Get move list for board"
	global COMPC, PLAYC, MAXPLIES, NODES

	ll = []
	NODES = 0

	if b.turn == c.WHITE:
		COMPC = c.WHITE
		PLAYC = c.BLACK
	else:
		COMPC = c.BLACK
		PLAYC = c.WHITE

	if not silent:
		print(b.unicode())
		print(getval(b))
		print("FEN:", b.fen())

	nl = len(list(b.legal_moves))

	start = time.time()
	for n, x in enumerate(b.legal_moves):
		b.push(x)
		p = 0
		if COMPC == c.WHITE:
			t = searchmin(b, 0, -1e6, 1e6)
		else:
			t = searchmax(b, 0, -1e6, 1e6)
		if MATETEST:
			res = b.result(claim_draw = True)
			if res == '1/2-1/2':
				t = 0
			if res == '1-0':
				t = 1e8
			if res == '0-1':
				t = -1e8
		if not silent:
			print("(%u/%u) %s %.1f %.2f" % (n + 1, nl, x, p, t))
		ll.append((x, p, t))
		b.pop()

	ll.sort(key = lambda m: m[1] + 1000 * m[2])
	if COMPC == c.WHITE:
		ll.reverse()
	print('# %.2f %s' % (ll[0][1] + ll[0][2], [str(ll[0][0])]))
	print('info depth %d score cp %d time %d nodes %d pv %s' % (MAXPLIES + 1,
		100 * pm () * ll[0][2], 1000 * (time.time() - start), NODES, str(ll[0][0])))
	return ll[0][1] + ll[0][2], [str(ll[0][0])]

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


