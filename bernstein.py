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
SVFAC    = 60	# influence of swap-off value on evaluation in percent
MATETEST = False

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
			ws += len(list(b.attackers(c.WHITE, i)))
		if len(list(b.attackers(c.BLACK, i))) and not len(list(b.attackers(c.WHITE, i))):
			bs += len(list(b.attackers(c.BLACK, i)))

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
	return posval	

def getneg(b):
	"Board value in the Negamax framework, i.e. '+' means the side to move has the advantage"
	if MATETEST:
		res = b.result(claim_draw = True)
		if res == '1/2-1/2':
			return 0
	tsv = 0
	if SVFAC > 0:
		svl, svn, svz, svv = getswap(b, not b.turn, b.turn)
		for i in svl:
			tsv += svv[i]
	return .001 * getpos(b) + SVFAC / 100. * tsv + (
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

def get_smallest_attacker(b, square, side):
	"Get attacking piece with smallest value"
	n = 1000
	att = None
	for a in b.attackers(side, square):
		if piece(b.piece_type_at(a)) < n:
			att = a
			n = piece(b.piece_type_at(a))
	return att

def getcap(b, x, y, side):
	"Get capturing move from x to y"
	u = b.copy()
	u.turn = side
	for l in u.legal_moves:
		if l.from_square == x and l.to_square == y:
			return l
	return None

# https://chessprogramming.wikispaces.com/Static%20Exchange%20Evaluation
def see(b, square, side):
	"Static Exchange Evaluation"
	value = 0
	ex = False
	ppp = get_smallest_attacker(b, square, side)
	mov = None
	last = -1000
	if ppp:
		mov = getcap(b, ppp, square, side)
		ex = True
	if mov:
		piece_just_captured = piece(b.piece_type_at(square))
		#print('# ', mov)
		#print('# ', c.SQUARE_NAMES[ppp], c.SQUARE_NAMES[square])
		if piece_just_captured:
			b.push(mov)
			last = piece_just_captured - see(b, square, not side)[0]
			value = max(0, last)
			b.pop()
		else:
			print('# swapfail', square, side)
	return value, ex, last

def getswap(b, compcolor, playcolor):
	"(iii) Get swap-off value"
	svl = []
	svz = 64 * [0]
	svn = 64 * [0]
	svv = 64 * [0]
	u = b.copy()
	for i in u.piece_map().keys():
		m = u.piece_at(i)
		if m and m.color == compcolor:
			sv, ex, last = see(u, i, playcolor)
			#print('# ', c.SQUARE_NAMES[i], compcolor, sv, last)
			if sv > 0:
				svl.append(i)
				svv[i] = sv
			if last == 0:
				svz[i] = 1
			if ex:
				svn[i] += 1
	return svl, svn, svz, svv

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

	# Can check or checkmate be given?
	for x in m:
		b.push(x)
		if b.is_checkmate():
			pmt.append(x)
		b.pop()
	for x in m:
		b.push(x)
		if b.is_check() and x not in pmt:
			pmt.append(x)
		b.pop()

	# 2. Can material be (a) gained, (b) lost, or (c) exchanged?
	enemy_swap, eex, ezero, esv = getswap(b, not b.turn, b.turn)	# (a)
	for x in m:
		if x.to_square in enemy_swap:
			pmt.append(x)

	my_swap, mex, mzero, msv = getswap(b, b.turn, not b.turn)	# (b)
	defcount = 64 * [0]
	# b1, find one retreating defensive move
	defend = 64 * [[-1000, None]]
	for x in m:
		b.push(x)
		att = len(list(b.attackers(not b.turn, x.to_square))) - 10 * len(list(b.attackers(b.turn, x.to_square)))
		if ( x.from_square in my_swap and att > defend[x.from_square][0] ):
			defend[x.from_square] = att, x
		b.pop()

	for x in m:
		if defend[x.from_square][1]:
			m2 = defend[x.from_square][1]
			if m2 not in pmt:
				pmt.append(m2)
				defcount[x.from_square] += 1
	# b2, find one attacking defensive move
	defend = 64 * [[-1000, None]]
	for x in m:
		b.push(x)
		att2 = 0
		for q in b.attacks(x.to_square):
			m2 = b.piece_at(q)
			if m2 and m2.color is b.turn:
				att2 += 1
		att = att2 - 10 * len(list(b.attackers(b.turn, x.to_square)))
		if ( x.from_square in my_swap and att > defend[x.from_square][0] ):
			defend[x.from_square] = att, x
		b.pop()

	for x in m:
		if defend[x.from_square][1]:
			m2 = defend[x.from_square][1]
			if m2 not in pmt:
				pmt.append(m2)
				defcount[x.from_square] += 1
	# b3, if fewer than three defensive moves have been found so far, add others
	for x in m:
		if x.from_square in my_swap and defcount[x.from_square] <= 2:
			if x not in pmt:
				pmt.append(x)
				defcount[x.from_square] += 1

	for x in m:							# (c)
		if x.to_square not in enemy_swap and ezero[x.to_square]:
			pmt.append(x)

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
		if x.from_square in mfrom: # and len(list(b.attackers(not b.turn, x.to_square))) == 0:
			pmt.append(x)

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
	for f in range(8):
		for r in range(8):
			pt = b.piece_at(8 * r + f)
			if pt:
				t = pt.piece_type
				if t != c.KING:
					sof[f] = False
	for x in m:
		pt = b.piece_at(x.from_square)
		if (pt.piece_type == c.QUEEN or pt.piece_type == c.ROOK) and sof[c.square_file(x.to_square)]:
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

# https://chessprogramming.wikispaces.com/Alpha-Beta
def searchmax(b, ply, alpha, beta):
	"Search moves and evaluate positions for player whose turn it is"
	global NODES

	NODES += 1
	if ply >= MAXPLIES:
		###print([str(q) for q in b.move_stack])
		return getneg(b), [str(q) for q in b.move_stack]
	o = order(b, ply)
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

def pm():
	if COMPC == c.WHITE:
		return 1
	else:
		return -1

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
		print(b)
		print(getneg(b))
		print("FEN:", b.fen())

	start = time.time()
	NODES = 0
	nl = len(list(b.legal_moves))

	pmt = get_pmt(b)
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
			print(b)
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


