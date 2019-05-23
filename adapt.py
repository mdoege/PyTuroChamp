#!/usr/bin/env python3

# Simple adaptive chess engine using Stockfish

import chess as c
import chess.engine

import sys, math, time

# computer plays as Black by default

COMPC = c.BLACK
PLAYC = c.WHITE

NUMMOV = 5		# number of moves to consider for each position
MTIME = 3		# time in seconds per move
ENGINE = "stockfish"	# name of chess engine binary to use

b = c.Board()

def pm():
	if COMPC == c.WHITE:
		return 1
	else:
		return -1


def getmove(b, silent = False):
	"Get move for board"
	global COMPC, PLAYC

	if b.turn == c.WHITE:
		COMPC = c.WHITE
		PLAYC = c.BLACK
	else:
		COMPC = c.BLACK
		PLAYC = c.WHITE

	if not silent:
		print(b.unicode())
		print("FEN:", b.fen())

	target = -1 * pm()	# evaluation target value

	start = time.time()

	engine = chess.engine.SimpleEngine.popen_uci(ENGINE)
	info = engine.analyse(b, chess.engine.Limit(time = MTIME), multipv = NUMMOV)
	engine.quit()

	mov = []
	resm = len(info)
	#print(resm)
	#for i in info:
	#	print(i)

	for x in range(resm):
		#print("# ", info[x]["score"].white().score(mate_score = 100000) / 100, info[x]["pv"][0])
		mov.append((info[x]["score"].white().score(mate_score = 100000) / 100, info[x]["pv"][0]))

	diff = 1000
	pos = 0
	for x in range(resm):
		if abs(mov[x][0] - target) < diff:
			m = mov[x][1].uci()
			diff = abs(mov[x][0] - target)
			pos = mov[x][0]

	print('info score cp %d time %d pv %s' % (pm() * 100 * pos, 1000 * (time.time() - start), m))
	return pos, [m]

if __name__ == '__main__':
	while True:	# game loop
		while True:
			print(b.unicode())
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


