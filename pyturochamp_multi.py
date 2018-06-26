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

# computer plays as Black by default

COMPC = c.BLACK
PLAYC = c.WHITE

MAXPLIES = 3	# maximum search depth
QPLIES    = MAXPLIES + 4
PSTAB     = 5	# influence of piece-square table on moves, 0 = none

b = c.Board()

ptc_worker.start()

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
		print(b)
		print(ptc.getval(b))
		print("FEN:", b.fen())

	nl = len(list(b.legal_moves))
	cr0 = b.has_castling_rights(COMPC)

	inlist = list(b.legal_moves)
	nummov = len(inlist)

	while len(ll) < nummov:
		#if len(inlist) > 0:
		#	print(len(inlist), len(ll), nummov)
		if len(inlist):
			ptc_worker.urlq.put_nowait(
				(b.copy(), inlist.pop(), lastpos, COMPC, cr0))
		try:
			ll.append(ptc_worker.urlr.get_nowait())
		except Empty:
			pass
	ll.sort(key = lambda m: m[1] + m[2])
	if COMPC == c.WHITE:
		ll.reverse()
	print('# %.2f %s' % (ll[0][1] + ll[0][2], [str(ll[0][0])]))
	return ll[0][1] + ll[0][2], [str(ll[0][0])]

if __name__ == '__main__':
	while True:	# game loop
		while True:
			print(b)
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


