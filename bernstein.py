#!/usr/bin/env python3

# The Bernstein chess engine (1958)

import chess as c
import sys, math, time

# computer plays as Black by default

COMPC = c.BLACK
PLAYC = c.WHITE

MAXPLIES = 3	# 4 plies
PMTLEN   = 7	# size of Plausible Move Table
PMTSTART = 0	# first ply where the PMT is used,
		#    so e.g. PMTSTART = 2 means the PMT will not be used during the first two plies
MATETEST = True

b = c.Board()
PV = []		# array for primary variation
NODES = 0

def ppos(x, r):
	print(c.SQUARE_NAMES[x], r)

def getpos(b):
	"Get positional-play value for a board"

	# 1. number of available moves
	u = b.copy()
	u.turn = c.WHITE
	wm = len(list(u.legal_moves))
	u.turn = c.BLACK
	bm = len(list(u.legal_moves))

	# 2. number of controlled squares
	ws, bs = 0, 0
	for i in range(64):
		m = b.piece_at(i)
		if len(list(b.attackers(c.WHITE, i))) and not len(list(b.attackers(c.BLACK, i))):
			ws += 1
		if len(list(b.attackers(c.BLACK, i))) and not len(list(b.attackers(c.WHITE, i))):
			bs += 1

	# 3. controlled squares around each King
	wk, bk = 0, 0
	wking, bking = b.king(c.WHITE), b.king(c.BLACK)
	for i in range(64):
		if wking in b.attackers(c.WHITE, i):
			if not len(list(b.attackers(c.BLACK, i))):
				wk += 1
		if bking in b.attackers(c.BLACK, i):
			if not len(list(b.attackers(c.WHITE, i))):
				bk += 1

	posval = wm + ws + wk - bm - bs - bk
	#print('# ', wm, ws, wk, '  ', bm, bs, bk, '=', posval)
	if b.turn == c.WHITE:
		return posval
	else:
		return -posval

def getneg(b):
	"Board value in the Negamax framework, i.e. '+' means the side to move has the advantage"
	return .001 * getpos(b) + (
		     len(b.pieces(c.PAWN, b.turn))     - len(b.pieces(c.PAWN, not b.turn))
	+	3 * (len(b.pieces(c.KNIGHT, b.turn))   - len(b.pieces(c.KNIGHT, not b.turn)))
	+	3 * (len(b.pieces(c.BISHOP, b.turn))   - len(b.pieces(c.BISHOP, not b.turn)))
	+	5 * (len(b.pieces(c.ROOK, b.turn))     - len(b.pieces(c.ROOK, not b.turn)))
	+	9 * (len(b.pieces(c.QUEEN, b.turn))    - len(b.pieces(c.QUEEN, not b.turn)))
	)

def piece(t):
	"Get piece value"
	if t == c.QUEEN:
		return 9
	if t == c.ROOK:
		return 5
	if t == c.BISHOP or t == c.KNIGHT:
		return 3
	if t == c.PAWN:
		return 1
	if t == c.KING:
		return 100

def home_rank(b):
	"Get home rank for side"
	if b.turn:
		return 0
	else:
		return 7 * 8

def get_pmt(b):
	"Get Plausible Move Table (PMT) for board b"
	pmt = []
	m = list(b.legal_moves)
	# 1. King in check?
	if b.is_check():
		pmt = [str(x) for x in m]
		return pmt

	# Can checkmate be given?
	for x in m:
		b.push(x)
		if b.is_checkmate():
			pmt.append(x)
		b.pop()

	# 2. Can material be (a) gained, (b) lost, or (c) exchanged?
	#   (2a)
	for x in m:
		if b.is_capture(x):
			i = x.from_square
			j = x.to_square
			try:
				mdiff = piece(b.piece_type_at(j)) - piece(b.piece_type_at(i))
			except:
				mdiff = 0	# en passant capture
			b.push(x)
			if mdiff > 0 or len(list(b.attackers(b.turn, j))) == 0:
				#print("# 2a", x)
				pmt.append(x)
			b.pop()

	# try to block the promotion square of an advanced enemy pawn
	mindist, pr_square = 8, None
	for i in b.piece_map().keys():
		pt = b.piece_at(i)
		if pt and pt.piece_type == c.PAWN and pt.color is not b.turn:
			mm2 = abs(c.square_rank(i) - home_rank(b))
			if mm2 < mindist:
				mindist = mm2
				pr_square = c.square(c.square_file(i), home_rank(b))
	if pr_square and mindist < 4:
		for x in m:
			if x.to_square == pr_square and x not in pmt:
				pmt.append(x)

	#   (2b)
	for x in m:
		i = x.from_square
		j = x.to_square
		if len(list(b.attackers(not b.turn, i))):
			b.push(x)
			if len(list(b.attackers(b.turn, j))) == 0:
				#print("# 2b", x)
				pmt.append(x)
			b.pop()

	#   (2c)
	for x in m:
		if b.is_capture(x):
			i = x.from_square
			j = x.to_square
			try:
				mdiff = piece(b.piece_type_at(j)) - piece(b.piece_type_at(i))
			except:
				mdiff = 0	# en passant capture
			b.push(x)
			if mdiff == 0:
				#print("# 2c", x)
				pmt.append(x)
			b.pop()

	# 3. Is castling possible?
	caspos = False
	for x in m:
		if b.is_castling(x):
			caspos = True
			pmt.append(x)
	if caspos:
		pmt = [str(x) for x in pmt]
		return pmt

	# 4. Can minor pieces be developed?
	msq = [2, 5, 1, 6]
	mfrom = []
	for mp in msq:
		i = mp + home_rank(b)
		pt = b.piece_at(i)
		if pt and (pt.piece_type == c.BISHOP or pt.piece_type == c.KNIGHT) and pt.color == b.turn:
			mfrom.append(i)
	for x in m:
		if x.from_square in mfrom:
			if b.piece_type_at(x.from_square) == c.KNIGHT:
				pmt.append(x)
			else:
				if len(list(b.attackers(not b.turn, x.to_square))) == 0:
					pmt.append(x)

	# Can check be given?
	for x in m:
		b.push(x)
		if b.is_check() and len(list(b.attackers(b.turn, x.to_square))) == 0 and x not in pmt:
			#print("# check", x)
			pmt.append(x)
		b.pop()

	# 5. Can key squares be controlled by pawns?
	ksq = []
	chf = c.PAWN, c.BISHOP, c.QUEEN
	for i in range(64):
		att = b.attackers(b.turn, i)
		for pt in att:
			if b.piece_type_at(pt) in chf:
				u = b.copy()
				u.set_piece_at(i, c.Piece(c.PAWN, b.turn))
				att2 = u.attacks(i)
				for p2 in att2:
					mp = b.piece_at(p2)
					if mp and mp.piece_type in chf and mp.color == b.turn:
						ksq.append(i)
	for x in m:
		if b.piece_type_at(x.from_square) == c.PAWN and x.to_square in ksq:
			pmt.append(x)

	# 6. Can open files be controlled?
	sof = 8 * [True]
	for i in b.piece_map().keys():
		pt = b.piece_at(i)
		if pt and pt.piece_type == c.PAWN:
			sof[c.square_file(i)] = False
	for x in m:
		pt = b.piece_at(x.from_square)
		if ( (pt.piece_type == c.QUEEN or pt.piece_type == c.ROOK)
		  and sof[c.square_file(x.to_square)]
		  and len(list(b.attackers(not b.turn, x.to_square))) == 0 ):
			pmt.append(x)

	# 7. Can pawns be moved?
	pawn = []
	pawnfile = (1, 2, 3, 4, 4, 3, 2, 1)
	for x in m:
		pt = b.piece_at(x.from_square)
		if pt.piece_type == c.PAWN and pt.color == b.turn:
			pawn.append((x, pawnfile[c.square_file(x.from_square)]))
	pawn.sort(key = lambda m: -m[1])
	pmt += [pm for pm, x in pawn]

	# 8. Can any piece be moved?
	pmt += [str(x) for x in m]

	pmt = [str(x) for x in pmt]
	pmt2 = []
	for x in pmt:
		if x not in pmt2:
			pmt2.append(x)

	return pmt2[:PMTLEN]

# https://chessprogramming.org/Alpha-Beta
def searchmax(b, ply, alpha, beta):
	"Search moves and evaluate positions for player whose turn it is"
	global NODES

	NODES += 1
	if ply >= MAXPLIES:
		###print([str(q) for q in b.move_stack])
		return getneg(b), [str(q) for q in b.move_stack]
	o = list(order(b, ply))
	if ply >= MAXPLIES:
		if not o:
			return getneg(b), [str(q) for q in b.move_stack]
	v = PV
	mypmt = get_pmt(b)

	for x in o:
		if ply + 1 >= PMTSTART and str(x) not in mypmt:
			continue
		b.push(x)
		t, vv = searchmax(b, ply + 1, -beta, -alpha)
		t = -t
		b.pop()
		if t >= beta:
			return beta, vv
		if t > alpha:
			alpha = t
			v = vv
	if MATETEST:
		res = b.result(claim_draw = True)
		if res == '1/2-1/2':
			return 0, v
	return alpha, v

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

def getmove(b, silent = False, usebook = False):
	"Get move list for board"
	global COMPC, PLAYC, MAXPLIES, NODES

	ll = []

	if b.turn == c.WHITE:
		COMPC = c.WHITE
		PLAYC = c.BLACK
	else:
		COMPC = c.BLACK
		PLAYC = c.WHITE

	if not silent:
		print(b.unicode())
		print(getneg(b))
		print("FEN:", b.fen())

	start = time.time()
	NODES = 0
	nl = len(list(b.legal_moves))

	pmt = get_pmt(b)
	for n, x in enumerate(b.legal_moves):
		b.push(x)
		if b.is_checkmate():	# play checkmate directly if possible
			b.pop()
			return 1e6, [str(x)]
		else:
			b.pop()

	for n, x in enumerate(b.legal_moves):
		if PMTSTART == 0 and str(x) not in pmt:
			continue
		print()
		print('# ', str(x))
		b.push(x)
		u = b.copy()
		t, PV = searchmax(u, 0, -1e6, 1e6)
		t = -t
		PV = PV[len(b.move_stack) - 1:]
		print("# (%u/%u) %s %.2f" % (n + 1, nl, x, t))
		print('# ', PV)
		ll.append((x, t, PV))
		b.pop()

	ll.sort(key = lambda m: m[1])
	ll.reverse()
	print('info depth %d score cp %d time %d nodes %d pv %s' % (MAXPLIES + 1, 100 * ll[0][1],
		1000 * (time.time() - start), NODES, ' '.join(ll[0][2])))
	return ll[0][1], [str(ll[0][0])]

if __name__ == '__main__':
	while True:	# game loop
		while True:
			print(b.unicode())
			print(getneg(b))
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
			print("THANK YOU FOR THIS INTERESTING GAME")
			break

		tt = time.time()
		t, m = getmove(b)
		print("My move: %u. %s     ( calculation time spent: %u m %u s )" % (
			b.fullmove_number, m[0],
			(time.time() - tt) // 60, (time.time() - tt) % 60))
		b.push(c.Move.from_uci(m[0]))

		if b.result() != '*':
			print("Game result:", b.result())
			if (COMPC == c.WHITE and b.result() == '1-0') or (COMPC == c.BLACK and b.result() == '0-1'):
				print("Feel the Bern!")
			print("THANK YOU FOR THIS INTERESTING GAME")
			break


