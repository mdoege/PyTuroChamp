#!/usr/bin/env python3

# A Python chess engine

from pst import pst

import chess as c
import os, sys, math, time
from random import choice

if sys.path[0]:
	os.chdir(sys.path[0])	# change working directory to script directory so the opening book will be found

# computer plays as Black by default

COMPC = c.BLACK
PLAYC = c.WHITE

DEPTH  = 14	# maximum search depth (with not be reached due to either time controls or MAXNODES)
QPLIES = 6	# additional maximum quiescence search plies
PSTAB  = .1	# influence of piece-square table on moves, 0 = none
USEBOOK = True	# use opening book
MATETEST  = True	# if True, include mate and draw detection in the material eval
MAXNODES = 1e6	# stop search when MAXNODES nodes are reached,
		#   to avoid crashing the machine on longer time controls

b = c.Board()
PV = []		# array for primary variation
NODES = 0

wtime, btime, movestogo, movetime = -1, -1, -1, -1	# time management variables
endtime = time.time() + 1e8
searchok = True

def getpos(b):
	"Get positional-play value for a board for both players"
	ppv = 0
	if not moves and b.is_checkmate():
		if b.turn == c.WHITE:
			ppv = -1000
		else:
			ppv =  1000
	pm = b.piece_map()
	for i in pm.keys():
		mm = pm[i].piece_type
		if mm == c.KING and (
		  len(b.pieces(c.PAWN, COMPC)) + len(b.pieces(c.PAWN, PLAYC)) ) <= 8:	# endgame is different
			mm = 8								#   for the King
		if pm[i].color == c.WHITE:
			j, k = i // 8, i % 8
			ppv += PSTAB * pst[mm][8 * (7 - j) + k] / 100
		else:
			ppv -= PSTAB * pst[mm][i]               / 100
	return ppv

def getval(b):
	"Get total piece value of board"
	return (
		len(b.pieces(c.PAWN, c.WHITE))          - len(b.pieces(c.PAWN, c.BLACK))
	+	2.8 * (len(b.pieces(c.KNIGHT, c.WHITE))   - len(b.pieces(c.KNIGHT, c.BLACK)))
	+	3.2 * (len(b.pieces(c.BISHOP, c.WHITE))   - len(b.pieces(c.BISHOP, c.BLACK)))
	+	4.79 * (len(b.pieces(c.ROOK, c.WHITE))     - len(b.pieces(c.ROOK, c.BLACK)))
	+	9.29 * (len(b.pieces(c.QUEEN, c.WHITE))    - len(b.pieces(c.QUEEN, c.BLACK)))
	)

def getneg(b):
	"Board value in the Negamax framework, i.e. '+' means the side to move has the advantage"
	if b.turn:
		return getval(b) + getpos(b)
	else:
		return -getval(b) - getpos(b)

def isdead(b, p):
	"Is the position dead? (quiescence) E.g., can the capturing piece be recaptured? Is there a check on this or the last move?"
	if p <= -QPLIES or not moves:	# when too many plies or checkmate
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

# https://chessprogramming.org/Alpha-Beta
def searchmax(b, ply, alpha, beta):
	"Search moves and evaluate positions for player whose turn it is"
	global moves, NODES, searchok

	moves = [q for q in b.legal_moves]
	NODES += 1
	if MATETEST:
		res = b.result(claim_draw = True)
		if res == '1/2-1/2':
			return 0, PV
	if ply <= 0 and isdead(b, ply):
		return getneg(b), [str(q) for q in b.move_stack]
	o = order(b, ply)
	if ply <= 0:
		if not o:
			return getneg(b), [str(q) for q in b.move_stack]
	v = PV
	for x in o:
		b.push(x)
		if (time.time() < endtime and NODES < MAXNODES) or MAXPLIES == 1:
			t, vv = searchmax(b, ply - 1, -beta, -alpha)
		else:
			searchok = False
			return alpha, v
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
	if ply >= 0:		# try moves from PV before others
		am, bm = [], []
		for x in moves:
			if str(x) in PV:
				am.append(x)
			else:
				bm.append(x)
		return am + bm

	# quiescence search (ply < 0), sort captures by MVV/LVA value
	am, bm = [], []
	for x in moves:
		if b.is_capture(x):
			if b.piece_at(x.to_square):
				# MVV/LVA sorting (http://home.hccnet.nl/h.g.muller/mvv.html)
				am.append((x, 10 * b.piece_at(x.to_square).piece_type
							- b.piece_at(x.from_square).piece_type))
			else:	# to square is empty during en passant capture
				am.append((x, 10 - b.piece_at(x.from_square).piece_type))
	am.sort(key = lambda m: m[1])
	am.reverse()
	bm = [q[0] for q in am]
	return bm

def getnewmove(m, n):
	if len(m) <= len(n):
		return []
	i = 0
	for x, y in zip(m, n):
		if x == y:
			i += 1
		else:
			break
	if i == len(n):
		return m[i]
	else:
		return []

try:
	ob = open("chess-eco.pos.txt").readlines()
except:
	print("Opening book not found!")
	ob = []

def getopen(b):
	"Identify opening and get a book move if possible"
	op = []
	d = c.Board()
	for x in b.move_stack:
		op.append(d.san(x))
		d.push(x)
	played = '%s' % (' '.join(op))

	hits = []
	id = '', '', ''
	sm = []

	for l in ob:
		h5 = l.split('"')
		if len(h5) > 5:
			eco, name, mv = h5[1], h5[3], h5[5]
			if played[:len(mv)] == mv:
				if len(mv) > len(id[1]):
					id = name, mv, eco
			sm1 = getnewmove(mv.split(), op)
			try:
				if sm1:
					sm1 = str(b.parse_san(sm1))
			except:
				#print("# Illegal book move", sm1)
				sm1 = []
			if sm1 and sm1 not in sm:
				sm.append(sm1)
	#print('# %s %s  (%s)' % (id[2], id[0], id[1]))
	return sm

def setendtime():
	"Set system time to finish move computation at"
	global endtime, movestogo

	if movetime > 0:
		endtime = time.time() + movetime / 1000.
		return
	if wtime < 0 and btime < 0:
	#	endtime = time.time() + 3		# 3 seconds default move time
		return
	if movestogo < 0:
		movestogo = 60
	if COMPC == c.WHITE:
		thetime = wtime / 1000.
	else:
		thetime = btime / 1000.
	endtime = time.time() + thetime / (movestogo + 3)

def getmove(b, silent = False, usebook = True):
	"Get value and primary variation for board"
	global COMPC, PLAYC, MAXPLIES, PV, NODES, searchok

	if b.turn == c.WHITE:
		COMPC = c.WHITE
		PLAYC = c.BLACK
	else:
		COMPC = c.BLACK
		PLAYC = c.WHITE

	if not silent:
		print("FEN:", b.fen())

	try:
		if usebook and USEBOOK:
			opening = getopen(b)
			if opening:
				return 0, [choice(opening)]
	except:
		pass
	NODES = 0
	aa, ab = -1e6, 1e6	# initial alpha and beta

	start = time.time()

	lastboard = b.copy()
	try:
		lastboard.pop()		# check previous position if available
	except:
		pass

	# null move pruning (http://home.hccnet.nl/h.g.muller/null.html)
	if not b.is_check() and not lastboard.is_check():
		d = b.copy()
		d.turn = not d.turn
		t, enemyPV = searchmax(d, 2, -1e6, 1e6)
		t = -t
		if t > 1:
			ab = t  + .5
	setendtime()	# set end time for computation based on time control

	for MAXPLIES in range(1, DEPTH):	# iterative deepening loop
		while time.time() < endtime and NODES < MAXNODES:
			searchok = True
			t, newPV = searchmax(b.copy(), MAXPLIES, aa, ab)
			newPV = newPV[len(b.move_stack):]	# separate principal variation from moves already played
			if newPV:
				break		# search has been successful
			else:
				ab += 10	# increase Beta if search fails and try again
		# if search is succesful and complete, then update PV:
		if searchok:
			PV = newPV
			print('info depth %d score cp %d time %d nodes %d pv %s' % (MAXPLIES, 100 * t,
				1000 * (time.time() - start), NODES, ' '.join(PV)))
			sys.stdout.flush()
			if PV and (t < -500 or t > 500):	# found a checkmate
				break
	return t, PV

if __name__ == '__main__':
	while True:	# game loop
		while True:
			print(b.unicode())
			print()
			#print(getopen(b))
			if sys.version < '3':
				move = raw_input("Your move? ")
			else:
				move = input("Your move? ")
			if move == "quit":
				sys.exit(0)
			try:
				try:
					b.push_san(move)
				except ValueError:
					b.push_uci(move)
				print(b.unicode())
			except:
				print("Sorry? Try again. (Or type quit to quit.)")
			else:
				break

		if b.result() != '*':
			print("Game result:", b.result())
			break

		tt = time.time()
		t, ppp = getmove(b)

		print("My move: %u. %s" % (b.fullmove_number, ppp[0]))
		print("  ( calculation time spent: %u m %u s )" % ((time.time() - tt) // 60, (time.time() - tt) % 60))
		b.push(c.Move.from_uci(ppp[0]))

		if b.result() != '*':
			print("Game result:", b.result())
			break


