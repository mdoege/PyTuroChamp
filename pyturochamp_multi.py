#!/usr/bin/env python3

# Multiprocessing version of PyTuroChamp

# A Python chess engine,
# inspired by (but not compatible with)
# http://en.chessbase.com/post/reconstructing-turing-s-paper-machine

import ptc_worker
import pyturochamp as ptc
import chess as c
import sys, math, time
from queue import Empty, Full
from random import random, choice

# computer plays as Black by default

COMPC = c.BLACK
PLAYC = c.WHITE

MAXPLIES = 1	# maximum search depth
QPLIES    = MAXPLIES + 2
PSTAB     = 0	# influence of piece-square table on moves, 0 = none
PDEAD     = 1   # version of dead position eval
MATETEST  = False	# if True, include mate and draw detection in the material eval

# Easy play / random play parameters
MoveError = 0		# On every move, randomly select the best move or a move inferior by this value (in decipawns)
BlunderError = 0	# If blundering this move, randomly select the best move or a move inferior by this value (in decipawns)
			# Blunder Error overrides Move Error and should be > Move Error.
BlunderPercent = 0	# Percent chance of blundering this move

b = c.Board()

ptc_worker.start()

def pm():
	if COMPC == c.WHITE:
		return 1
	else:
		return -1

def getindex(ll):
	"Select either the best move, or an almost equivalent move, or a blunder from the list of moves"
	if random() < (BlunderPercent / 100.):
		err = BlunderError / 10.
	else:
		err = MoveError / 10.
	if err == 0:
		return 0	# best move
	else:
		vals = [x[1] + x[2] for x in ll]
		inds = zip(vals, range(len(ll)))
		mm = [x for x in inds if (abs(x[0] - vals[0]) < err)]
		return choice(mm)[1]

def getmove(b, silent = False, usebook = False):
	"Get move list for board"
	global COMPC, PLAYC, MAXPLIES

	lastpos = ptc.getpos(b)
	ll = []

	if b.turn == c.WHITE:
		COMPC = c.WHITE
		PLAYC = c.BLACK
	else:
		COMPC = c.BLACK
		PLAYC = c.WHITE

	if not silent:
		print(b.unicode())
		print(ptc.getval(b))
		print("FEN:", b.fen())

	nl = len(list(b.legal_moves))
	cr0 = b.has_castling_rights(COMPC)

	inlist = list(b.legal_moves)
	nummov = len(inlist)

	start = time.time()
	while len(ll) < nummov:
		#if len(inlist) > 0:
		#	print(len(inlist), len(ll), nummov)
		if len(inlist):
			ptc_worker.urlq.put_nowait(
				(b.copy(), inlist.pop(), lastpos, COMPC, cr0, MAXPLIES, QPLIES, PSTAB, PDEAD, MATETEST))
		try:
			ll.append(ptc_worker.urlr.get_nowait())
		except Empty:
			pass
	ll.sort(key = lambda m: m[1] + 1000 * m[2])
	if COMPC == c.WHITE:
		ll.reverse()
	i = getindex(ll)
	#print('# %.2f %s' % (ll[i][1] + ll[i][2], [str(ll[i][0])]))
	print('info depth %d seldepth %d score cp %d time %d pv %s' % (MAXPLIES + 1, QPLIES + 1,
		100 * pm() * ll[i][2], 1000 * (time.time() - start), str(ll[i][0])))
	return ll[i][1] + ll[i][2], [str(ll[i][0])]

if __name__ == '__main__':
	while True:	# game loop
		while True:
			print(b.unicode())
			print(ptc.getval(b))
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


