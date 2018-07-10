#!/usr/bin/env python3

# SOMA, the Smith One-Move Analyzer (1961)
# https://chessprogramming.wikispaces.com/SOMA

import chess as c
import sys, math, time
from random import random, choice

COMPC = c.WHITE
PLAYC = c.BLACK


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
		print('# ', c.SQUARE_NAMES[i], own, my, his)
		#print(swapval(own, my, his))
		sv = max(swapval(own, my, his), 0)
		print('# ', sv)
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

	print('# ', swapvalue)
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
				if i in b.attackers(PLAYC, i):
					score += 3
				elif s in (c.D4, c.D5, c.E4, c.E5):
					score += 2
				else:
					score += 1
	return score

def getval(b):
	"(i) Get total material value of board (White - Black, the usual method)"
	return (
		10 * (len(b.pieces(c.PAWN, c.WHITE))     - len(b.pieces(c.PAWN, c.BLACK)))
	+	30 * (len(b.pieces(c.KNIGHT, c.WHITE))   - len(b.pieces(c.KNIGHT, c.BLACK)))
	+	30 * (len(b.pieces(c.BISHOP, c.WHITE))   - len(b.pieces(c.BISHOP, c.BLACK)))
	+	50 * (len(b.pieces(c.ROOK, c.WHITE))     - len(b.pieces(c.ROOK, c.BLACK)))
	+	90 * (len(b.pieces(c.QUEEN, c.WHITE))    - len(b.pieces(c.QUEEN, c.BLACK)))
	)


def getmove(b, silent = False, usebook = False):
	"Get move list for board"
	global COMPC, PLAYC, MAXPLIES

	ll = []

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

	for n, x in enumerate(b.legal_moves):
		b.push(x)
		p = getval(b) + getsquare(b) + gettotalswap(b) - lastpos
		if not silent:
			print('# ', "(%u/%u) %s %.1f" % (n + 1, nl, x, p))
		ll.append((x, p))
		b.pop()

	ll.sort(key = lambda m: m[1])
	maxval = max([y for x, y in ll])
	ll = [(x, y) for x, y in ll if y == maxval]
	print('# ', maxval)
	print('# ', ll)
	move = choice(ll)
	print('# ', move)
	return move[1], [str(move[0])]


if __name__ == '__main__':
	while True:	# game loop
		while True:
			print(b)
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


