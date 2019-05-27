#!/usr/bin/env python3

# Simple adaptive chess engine using Stockfish

import chess as c
import chess.polyglot
if c.__version__ < '0.26':
	import chess.uci
else:
	import chess.engine

import sys, math, time
from random import expovariate

# computer plays as Black by default

COMPC = c.BLACK
PLAYC = c.WHITE

NUMMOV = 20		# number of moves to consider for each position
MTIME = 3		# time in seconds per move
EV = 1			# target evaluation
ALIM = 2		# limit for adaptive playing
LAMBDA = 1		# blunder parameter
ENGINE = "stockfish"	# name of chess engine binary to use
TRUEVAL = True	# show true evaluation instead of evalution of chosen computer move?
USEBOOK = True	# use opening book?
BOOKPATH = "Elo2400.bin"	# path to Polyglot opening book
WAITBOOK = True	# slow down book moves

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

	target = (EV + expovariate(LAMBDA)) * -pm()	# evaluation target value

	start = time.time()
	mov = []

	# get a book move if available:
	if USEBOOK:
		with chess.polyglot.open_reader(BOOKPATH) as book:
			try:
				mv = book.weighted_choice(b)
			except:
				pass
			else:
				if WAITBOOK:
					time.sleep(MTIME + 1)
				if c.__version__ >= '0.28':
					mm = mv.move.uci()
				else:
					mm = mv.move().uci()
				print('info score book time %d pv %s' % (1000 * (time.time() - start), mm))
				return 0, [mm]

	if c.__version__ >= '0.26':
		engine = chess.engine.SimpleEngine.popen_uci(ENGINE)
		info = engine.analyse(b, chess.engine.Limit(time = MTIME), multipv = NUMMOV)
		engine.quit()

		resm = len(info)
		for x in range(resm):
			#print("# ", info[x]["score"].white().score(mate_score = 100000) / 100, info[x]["pv"][0])
			mov.append((info[x]["score"].white().score(mate_score = 100000) / 100, info[x]["pv"][0]))
	else:
		engine = c.uci.popen_engine(ENGINE)
		engine.uci()
		engine.setoption({"MultiPV": NUMMOV})
		engine.isready()
		engine.position(b)
		info_handler = chess.uci.InfoHandler()
		engine.info_handlers.append(info_handler)
		engine.go(movetime = 1000 * MTIME)
		engine.quit()

		pv = info_handler.info["pv"]
		score = info_handler.info["score"]
		resm = len(pv)
		for x in range(1, resm + 1):
			sc = score[x].cp
			if sc == None:
				sc = score[x].mate
				if sc > 0:
					sc = 1000 - sc
				else:
					sc = -1000 - sc
			mov.append((pm() * sc / 100, pv[x][0]))

	diff = 1e6
	pos = 0
	if COMPC == c.WHITE:
		realpos = max([q[0] for q in mov])
	else:
		realpos = min([q[0] for q in mov])
	if ALIM > 0:
		# play best move if eval is outside bounds:
		if (COMPC == c.WHITE and realpos > ALIM) or (COMPC == c.BLACK and realpos < -ALIM):
			target = realpos

	for x in range(resm):
		if abs(mov[x][0] - target) < diff:
			m = mov[x][1].uci()
			diff = abs(mov[x][0] - target)
			pos = mov[x][0]

	if TRUEVAL:
		pos = realpos
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


