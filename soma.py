#!/usr/bin/env python3

# SOMA, the Smith One-Move Analyzer (1961)
# https://chessprogramming.org/SOMA

import chess as c
import sys, math, time
from random import random, choice

COMPC = c.WHITE
PLAYC = c.BLACK

MATETEST  = True	# if True, include mate and draw detection in the material eval


b = c.Board()


def piece(t):
	"Get piece value"
	if t == c.QUEEN:
		return 90
	if t == c.ROOK:
		return 50
	if t == c.BISHOP or t == c.KNIGHT:
		return 30
	if t == c.PAWN:
		return 10
	if t == c.KING:
		return 1000

def sumval(a, b, c):
	"Get sum of own minus enemy piece values"
	for x in b:
		a += x
	for y in c:
		a -= y
	return a

def swapval(x, y, z):
	"Get swap-off value for a piece"
	if len(z) == 0:
		return 0
	y.sort()
	z.sort()
	start = sumval(x, y, z)
	#print(start, '###')
	while True:
		if len(z) > 0 and len(y) > 0:
			z.pop(0)
		else:
			return -sumval(0, y, z) + start
		if len(y) > 0 and len(z) > 0:
			y.pop(0)
		else:
			return -sumval(0, y, z) + start

def getswap(b, compcolor, playcolor):
	"(iii) Get swap-off value"
	svl = []
	for i in b.piece_map().keys():
		m = b.piece_at(i)
		my, his = [], []
		if m and m.color == compcolor:
			for ax in b.attackers(playcolor, i):
				his.append(piece(b.piece_at(ax).piece_type))
			for ay in b.attackers(compcolor, i):
				my.append(piece(b.piece_at(ay).piece_type))
		own = piece(m.piece_type)
		#print('# ', c.SQUARE_NAMES[i], own, my, his)
		#print(swapval(own, my, his))
		sv = max(swapval(own, my, his), 0)
		#print('# ', sv)
		if sv > 0:
			svl.append(sv)
	return svl

def gettotalswap(b):
	"Get total swap value for board"
	swapvalue = 0
	wp = getswap(b, COMPC, PLAYC)
	wp.sort()

	if len(wp):
		swapvalue -= wp.pop()
		swapvalue -= 5 * len(wp)

	bp = getswap(b, PLAYC, COMPC)
	bp.sort()
	if len(bp) == 1:
		swapvalue += 5
	elif len(bp) > 1:
		bp.pop()
		swapvalue += bp.pop()
		swapvalue += 5 * len(bp)

	#print('# ', swapvalue)
	return swapvalue

def getsquare(b):
	"(ii) Get value of attacked squares"
	score = 0
	kingsq = b.king(PLAYC)
	for i in b.piece_map().keys():
		m = b.piece_at(i)
		if m and m.color == COMPC:
			a = b.attacks(i)
			for s in a:
				if kingsq in b.attackers(PLAYC, s):
					score += 3
				elif s in (c.D4, c.D5, c.E4, c.E5):
					score += 2
				else:
					score += 1
	return score

def getsquare2(b):
	"(ii) Get value of attacked squares (alternate version)"
	score = 0
	kingsq = b.king(PLAYC)
	for i in range(64):
		if b.attackers(COMPC, i):
			if kingsq in b.attackers(PLAYC, i):
				score += 3
			elif i in (c.D4, c.D5, c.E4, c.E5):
				score += 2
			else:
				score += 1
	return score


def getval(b):
	"(i) Get total material value of board (White - Black, the usual method)"
	# test for a draw
	if MATETEST:
		res = b.result(claim_draw = True)
		if res == '1/2-1/2':
			return 0
	return (
		10 * (len(b.pieces(c.PAWN, c.WHITE))     - len(b.pieces(c.PAWN, c.BLACK)))
	+	30 * (len(b.pieces(c.KNIGHT, c.WHITE))   - len(b.pieces(c.KNIGHT, c.BLACK)))
	+	30 * (len(b.pieces(c.BISHOP, c.WHITE))   - len(b.pieces(c.BISHOP, c.BLACK)))
	+	50 * (len(b.pieces(c.ROOK, c.WHITE))     - len(b.pieces(c.ROOK, c.BLACK)))
	+	90 * (len(b.pieces(c.QUEEN, c.WHITE))    - len(b.pieces(c.QUEEN, c.BLACK)))
	)

def psquares(u):
	"Get squares attacked by advancing enemy pawns"
	u.turn = not u.turn
	sq = []
	for h in u.legal_moves:
		pt = u.piece_type_at(h.from_square)
		if pt == c.PAWN:
			u.push(h)
			for att in u.attacks(h.to_square):
				sq.append(att)
			u.pop()
	return sq

def attacked(b):
	"Get material value of own pieces under attack"
	attacked = 0
	for i in b.piece_map().keys():
		m = b.piece_at(i)
		if m and m.color == COMPC:
			if b.attackers(PLAYC, i):
				attacked += piece(m.piece_type)
	return attacked

def getpin(b):
	"Get squares with pinned pieces, as we do not want to move those"
	sqp = []
	nowval = attacked(b)
	for i in b.piece_map().keys():
		m = b.piece_at(i)
		if m and m.color == COMPC:
			u = b.copy()
			u.remove_piece_at(i)
			pinval = attacked(u)
			if pinval > nowval:
				sqp.append(i)
	#print('# ', [c.SQUARE_NAMES[x] for x in sqp])
	return sqp

def getmove(b, silent = False, usebook = False):
	"Get move list for board"
	global COMPC, PLAYC, MAXPLIES

	ll = []
	start = time.time()

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
	lastpos = getval(b) + getsquare(b) + gettotalswap(b)

	psq = psquares(b.copy())
	pins = getpin(b)

	for n, x in enumerate(b.legal_moves):
		if b.is_castling(x):		# Is this move a castle move?
			cb = 10
		else:
			cb = 0
		if x.to_square in psq:		# Does this move go to a square threatened by a pawn advance?
			pawn = -.1
		else:
			pawn = 0
		if x.from_square in pins:	# Is this move moving a pinned piece?
			pin = -.1
		else:
			pin = 0
		b.push(x)
		if COMPC == c.BLACK:
			posval = - getval(b)
		else:
			posval =   getval(b)
		p = posval + getsquare(b) + .9 * gettotalswap(b) - lastpos + cb + pawn + pin
		if not silent:
			print('# ', "(%u/%u) %s %.1f" % (n + 1, nl, x, p))
			print('# ', getval(b) , getsquare(b) ,  gettotalswap(b) ,  lastpos ,  cb , pawn , pin )
		ll.append((x, p, posval))
		b.pop()
	#print('# ', [c.SQUARE_NAMES[x] for x in psq])
	ll.sort(key = lambda m: m[1])
	maxval = max([y for x, y, z in ll])
	ll = [(x, y, z) for x, y, z in ll if y == maxval]
	#print('# ', maxval)
	#print('# ', ll)
	move = choice(ll)
	print('info depth %d score cp %d time %d nodes %d' % (1, 10 * move[2], 1000 * (time.time() - start), nl))
	sys.stdout.flush()
	#print('# ', move)
	return move[1], [str(move[0])]


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


