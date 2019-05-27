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
elif sys.argv[-1] == 'plan':
	import plan as p
	lf = "Plan-log.txt"
	mf = "Plan.pgn"
	nm = "Plan"
elif sys.argv[-1] == 'shannon':
	import shannon as p
	lf = "Shannon-log.txt"
	mf = "Shannon.pgn"
	nm = "Shannon"
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
elif sys.argv[-1] == 'bern':
	import bernstein as p
	lf = "Bernstein-log.txt"
	mf = "Bernstein.pgn"
	nm = "Bernstein"
elif sys.argv[-1] == 'rmove':
	import rmove as p
	lf = "RMove-log.txt"
	mf = "RMove.pgn"
	nm = "Random Mover"
elif sys.argv[-1] == 'adapt':
	import adapt as p
	lf = "Adapt-log.txt"
	mf = "Adapt.pgn"
	nm = "Simple Adaptive Engine"
else:
	if 'linux' in sys.platform:
		import pyturochamp_multi as p
		lf = "PyTuroChamp-log.txt"
		mf = "PyTuroChamp.pgn"
		nm = "PyTuroChamp Multi-Core"
	else:
		import pyturochamp as p
		lf = "PyTuroChamp-log.txt"
		mf = "PyTuroChamp.pgn"
		nm = "PyTuroChamp"

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
				print2("option name qplies type spin default 7 min 0 max 1024")
				print2("option name pstab type spin default 0 min 0 max 1024")
				print2("option name matetest type check default true")

				print2("option name MoveError type spin default 0 min 0 max 1024")
				print2("option name BlunderError type spin default 0 min 0 max 1024")
				print2("option name BlunderPercent type spin default 0 min 0 max 1024")

				print2("option name EasyLearn type spin default 0 min 0 max 1024")
				print2("option name EasyLambda type spin default 20 min 1 max 1024")

				print2("option name PlayerAdvantage type spin default 0 min -1024 max 1024")
			if nm == 'Bare':
				print2("option name maxplies type spin default 3 min 0 max 1024")
				print2("option name pstab type spin default 5 min 0 max 1024")
				print2("option name matetest type check default true")
			if nm == 'Shannon':
				print2("option name maxplies type spin default 1 min 0 max 1024")
				print2("option name qplies type spin default 7 min 0 max 1024")
				print2("option name matetest type check default true")
				print2("option name pawnrule type check default false")
			if nm == 'Plan':
				print2("option name maxplies type spin default 3 min 0 max 1024")
			if nm == 'Newt':
				print2("option name depth type spin default 14 min 0 max 1024")
				print2("option name qplies type spin default 6 min 0 max 1024")
				print2("option name pstab type spin default 1 min 0 max 1024")
				print2("option name maxnodes type spin default 1000000 min 0 max 1000000000")
				print2("option name usebook type check default true")
				print2("option name matetest type check default true")
			if nm == 'SOMA':
				print2("option name matetest type check default true")
			if nm == 'Bernstein':
				print2("option name maxplies type spin default 3 min 0 max 1024")
				print2("option name pmtlen type spin default 7 min 1 max 1024")
				print2("option name pmtstart type spin default 0 min 0 max 1024")
				print2("option name matetest type check default true")
			if nm == 'Simple Adaptive Engine':
				print2("option name nummov type spin default 20 min 1 max 1024")
				print2("option name mtime type spin default 3 min 1 max 1024")
				print2("option name ev type spin default 100 min -1024 max 1024")
				print2("option name alim type spin default 200 min 0 max 1024")
				print2("option name lambda type spin default 10 min 1 max 1024")
				print2("option name enginepath type string default stockfish")
				print2("option name trueval type check default true")
				print2("option name usebook type check default true")
				print2("option name bookpath type string default Elo2400.bin")
				print2("option name waitbook type check default true")

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
		elif 'setoption name nummov value' in l:
			p.NUMMOV = int(l.split()[4])
			print2("# nummov: %u" % p.NUMMOV)
		elif 'setoption name mtime value' in l:
			p.MTIME = int(l.split()[4])
			print2("# mtime: %u" % p.MTIME)
		elif 'setoption name ev value' in l:
			p.EV = int(l.split()[4]) / 100.
			print2("# ev: %u" % p.EV)
		elif 'setoption name alim value' in l:
			p.ALIM = int(l.split()[4]) / 100.
			print2("# alim: %u" % p.ALIM)
		elif 'setoption name lambda value' in l:
			p.LAMBDA = int(l.split()[4]) / 10.
			print2("# lambda: %u" % p.LAMBDA)
		elif 'setoption name enginepath value' in l:
			p.ENGINE = l.split()[4]
			print2("# enginepath: %s" % p.ENGINE)
		elif 'setoption name bookpath value' in l:
			p.BOOKPATH = l.split()[4]
			print2("# bookpath: %s" % p.BOOKPATH)
		elif 'setoption name trueval value' in l:
			if l.split()[4] == "true":
				p.TRUEVAL = True
			else:
				p.TRUEVAL = False
			print2("# trueval: %s" % p.TRUEVAL)
		elif 'setoption name waitbook value' in l:
			if l.split()[4] == "true":
				p.WAITBOOK = True
			else:
				p.WAITBOOK = False
			print2("# waitbook: %s" % p.WAITBOOK)
		elif 'setoption name pstab value' in l:
			if 'Bare' in nm or 'Newt' in nm:
				p.PSTAB = int(l.split()[4]) / 10.	# convert to pawn units for Bare and Newt
				print2("# pstab: %u" % p.PSTAB)
			else:
				p.PSTAB = int(l.split()[4])
				print2("# pstab: %u" % p.PSTAB)
		elif 'setoption name maxnodes value' in l:
			p.MAXNODES = int(l.split()[4])
			print2("# maxnodes: %u" % p.MAXNODES)
		elif 'setoption name matetest value' in l:
			if l.split()[4] == "true":
				p.MATETEST = True
			else:
				p.MATETEST = False
			print2("# matetest: %s" % p.MATETEST)
		elif 'setoption name pawnrule value' in l:
			if l.split()[4] == "true":
				p.PAWNRULE = True
			else:
				p.PAWNRULE = False
			print2("# pawnrule: %s" % p.PAWNRULE)
		elif 'setoption name usebook value' in l:
			if l.split()[4] == "true":
				p.USEBOOK = True
			else:
				p.USEBOOK = False
			print2("# usebook: %s" % p.USEBOOK)
		elif 'setoption name pmtlen value' in l:
			p.PMTLEN = int(l.split()[4])
			print2("# pmtlen: %u" % p.PMTLEN)
		elif 'setoption name pmtstart value' in l:
			p.PMTSTART = int(l.split()[4])
			print2("# pmtstart: %u" % p.PMTSTART)

		elif 'setoption name MoveError value' in l:
			p.MoveError = int(l.split()[4])
			print2("# MoveError: %u" % p.MoveError)
		elif 'setoption name BlunderError value' in l:
			p.BlunderError = int(l.split()[4])
			print2("# BlunderError: %u" % p.BlunderError)
		elif 'setoption name BlunderPercent value' in l:
			p.BlunderPercent = int(l.split()[4])
			print2("# BlunderPercent: %u" % p.BlunderPercent)
		elif 'setoption name EasyLearn value' in l:
			p.EasyLearn = int(l.split()[4])
			print2("# EasyLearn: %u" % p.EasyLearn)
		elif 'setoption name EasyLambda value' in l:
			p.EasyLambda = int(l.split()[4]) / 10.
			print2("# EasyLambda: %u" % p.EasyLambda)
		elif 'setoption name PlayerAdvantage value' in l:
			p.PlayerAdvantage = int(l.split()[4])
			print2("# PlayerAdvantage: %u" % p.PlayerAdvantage)
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


