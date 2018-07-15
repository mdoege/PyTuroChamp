#!/usr/bin/env python3

# XBoard/UCI interface to PyTuroChamp

# Start with:
# xboard -fcp "python3 xboard.py"

#    Optional debug flags:  -debug -nameOfDebugFile debug.txt -engineDebugOutput 2

from __future__ import print_function

import sys, datetime
import chess as c
import chess.pgn

abc = "abcdefgh"
nn  = "12345678"

is_uci = False

if sys.argv[-1] == 'newt':
	import newt as p
	lf = "Newt-log.txt"
	mf = "Newt.pgn"
	nm = "Newt"
elif sys.argv[-1] == 'ptc':
	import pyturochamp as p
	lf = "PyTuroChamp-log.txt"
	mf = "PyTuroChamp.pgn"
	nm = "PyTuroChamp"
elif sys.argv[-1] == 'bare':
	import bare as p
	lf = "Bare-log.txt"
	mf = "Bare.pgn"
	nm = "Bare"
elif sys.argv[-1] == 'soma':
	import soma as p
	lf = "SOMA-log.txt"
	mf = "SOMA.pgn"
	nm = "SOMA"
elif sys.argv[-1] == 'torres':
	import torres as p
	lf = "Torres-log.txt"
	mf = "Torres.pgn"
	nm = "El Ajedrecista"
elif sys.argv[-1] == 'rmove':
	import rmove as p
	lf = "RMove-log.txt"
	mf = "RMove.pgn"
	nm = "Random Mover"
else:
	import pyturochamp_multi as p
	lf = "PyTuroChamp-log.txt"
	mf = "PyTuroChamp.pgn"
	nm = "PyTuroChamp Multi-Core"

try:
	log = open(lf, 'w')
except:
	log = ''
	print("# Could not create log file")

def print2(x):
	print(x)
	if log:
		log.write("< %s\n" % x)
		log.flush()

d = ''
r = ''

def move(r):
	rm = r[0]
	d.push_uci(rm)
	if is_uci:
		print2("bestmove %s" % rm)
	else:
		print2("move %s" % rm)
	pgn()

def pgn():
	game = chess.pgn.Game.from_board(d)
	now = datetime.datetime.now()
	game.headers["Date"] = now.strftime("%Y.%m.%d")
	if p.COMPC == c.WHITE:
		game.headers["White"] = nm
		game.headers["Black"] = "User"
	else:
		game.headers["Black"] = nm
		game.headers["White"] = "User"
	try:
		with open(mf, 'w') as f:
			f.write(str(game) + '\n\n\n')
	except:
		print2("# Could not write PGN file")

def newgame():
	global d

	d = c.Board()

def fromfen(fen):
	global d

	try:
		d = c.Board(fen)
	except:
		print2("Bad FEN")
	#print(d)

def set_newt_time(line):
	xx = line.split()
	for x in range(len(xx)):
		if xx[x] == 'wtime':
			p.wtime = int(xx[x + 1])
		if xx[x] == 'btime':
			p.btime = int(xx[x + 1])
		if xx[x] == 'movestogo':
			p.movestogo = int(xx[x + 1])
		if xx[x] == 'movetime':
			p.movetime = int(xx[x + 1])
		if xx[x] == 'nodes':
			p.MAXNODES = int(xx[x + 1])

while True:
	l = ''
	try:
		if sys.version < '3':
			l = raw_input()
		else:
			l = input()
	except KeyboardInterrupt:	# XBoard sends Control-C characters, so these must be caught
		if not is_uci:
			pass		#   Otherwise Python would quit.
	if l:
		if log:
			log.write(l + '\n')
			log.flush()
		if l == 'xboard':
			print2('feature myname="%s" setboard=1 done=1' % nm)
		elif l == 'quit':
			sys.exit(0)
		elif l == 'new':
			newgame()
		elif l == 'uci':
			is_uci = True
			print2("id name %s" % nm)
			print2("id author Martin C. Doege")
			if 'PyTuroChamp' in nm:
				print2("option name maxplies type spin default 1 min 0 max 1024")
				print2("option name qplies type spin default 3 min 0 max 1024")
				print2("option name pstab type spin default 0 min 0 max 1024")
				print2("option name pdead type spin default 1 min 1 max 2")
				print2("option name matetest type check default false")

				print2("option name MoveError type spin default 0 min 0 max 1024")
				print2("option name BlunderError type spin default 0 min 0 max 1024")
				print2("option name BlunderPercent type spin default 0 min 0 max 1024")
			if nm == 'Bare':
				print2("option name maxplies type spin default 3 min 0 max 1024")
				print2("option name pstab type spin default 5 min 0 max 1024")
			if nm == 'Newt':
				print2("option name depth type spin default 14 min 0 max 1024")
				print2("option name qplies type spin default 6 min 0 max 1024")
				print2("option name pstab type spin default 1 min 0 max 1024")
				print2("option name maxnodes type spin default 1000000 min 0 max 1000000000")
				print2("option name matetest type check default false")
			if nm == 'SOMA':
				print2("option name matetest type check default false")

			print2("uciok")
		elif l == 'ucinewgame':
			newgame()
		elif 'position startpos moves' in l:
			mm = l.split()[3:]
			newgame()
			for mo in mm:
				d.push_uci(mo)
		elif 'position fen' in l:
			if l.split()[6] == 'moves':	# Shredder FEN
				l = ' '.join(l.split()[:6] + ['0', '1'] + l.split()[6:])
			ff = l.split()[2:8]
			mm = l.split()[9:]
			ff = ' '.join(ff)
			if d:
				old = d.copy()
				fromfen(ff)
				# Test if new position continues the current game.
				# In that case, do not discard the current game but append the new moves.
				if old.fen() == ff:
					for mo in mm:
						old.push_uci(mo)
					d = old.copy()
				else:
					for mo in mm:
						d.push_uci(mo)
			else:
				fromfen(ff)
				for mo in mm:
					d.push_uci(mo)
		elif 'setoption name maxplies value' in l:
			p.MAXPLIES = int(l.split()[4])
			print2("# maxplies: %u" % p.MAXPLIES)
		elif 'setoption name depth value' in l:
			p.DEPTH = int(l.split()[4])
			print2("# depth: %u" % p.DEPTH)
		elif 'setoption name qplies value' in l:
			p.QPLIES = int(l.split()[4])
			print2("# qplies: %u" % p.QPLIES)
		elif 'setoption name pstab value' in l:
			if 'Bare' in nm or 'Newt' in nm:
				p.PSTAB = int(l.split()[4]) / 10.	# convert to pawn units for Bare and Newt
				print2("# pstab: %u" % p.PSTAB)
			else:
				p.PSTAB = int(l.split()[4])
				print2("# pstab: %u" % p.PSTAB)
		elif 'setoption name pdead value' in l:
			p.PDEAD = int(l.split()[4])
			print2("# pdead: %u" % p.PDEAD)
		elif 'setoption name maxnodes value' in l:
			p.MAXNODES = int(l.split()[4])
			print2("# maxnodes: %u" % p.MAXNODES)
		elif 'setoption name matetest value' in l:
			if l.split()[4] == "true":
				p.MATETEST = True
			else:
				p.MATETEST = False
			print2("# matetest: %s" % p.MATETEST)

		elif 'setoption name MoveError value' in l:
			p.MoveError = int(l.split()[4])
			print2("# MoveError: %u" % p.MoveError)
		elif 'setoption name BlunderError value' in l:
			p.BlunderError = int(l.split()[4])
			print2("# BlunderError: %u" % p.BlunderError)
		elif 'setoption name BlunderPercent value' in l:
			p.BlunderPercent = int(l.split()[4])
			print2("# BlunderPercent: %u" % p.BlunderPercent)
		elif l == 'isready':
			if not d:
				newgame()
			print2("id name %s" % nm)
			print2("readyok")
		elif 'setboard' in l:
			fen = l.split(' ', 1)[1]
			fromfen(fen)
		elif l[:2] == 'go' or l == 'force':
			if not d:
				newgame()

			if nm == 'Newt':	# Newt has time management
				set_newt_time(l)

			t, r = p.getmove(d, silent = True)
			if r:
				move(r)
		elif l == '?':
			print2("move", r)
			if log:
				log.write("move %s\n" % r)
				log.flush()
		else:
			if not d:
				newgame()
			if l[0] in abc and l[2] in abc and l[1] in nn and l[3] in nn:
				if len(l) == 6:
					l = l[:4] + 'q'	# "Knights" outputs malformed UCI pawn promotion moves
				d.push_uci(l)
				pgn()
				t, r = p.getmove(d, silent = True)
				if r:
					move(r)


