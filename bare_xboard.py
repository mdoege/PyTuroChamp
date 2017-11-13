#!/usr/bin/env python3

# XBoard interface to PyTuroChamp

# Start with:
# xboard -fcp "python3 ptc_xboard.py" -initialMode MachineWhite -firstProtocolVersion 1

#    Optional debug flags:  -debug -nameOfDebugFile debug.txt -engineDebugOutput 2

import sys
import chess as c
import bare as p

abc = "abcdefgh"
nn  = "12345678"

log = open("Bare-log.txt", 'w')
d = ''
r = ''

def move(r):
	rm = str(r[0][0])
	d.push_uci(rm)
	print("move", rm)
	print("# % .2f" % (r[0][1] + r[0][2]))
	log.write("move %s\n" % rm)
	log.write("# % .2f\n" % (r[0][1] + r[0][2]))
	log.flush()

while True:
	l = ''
	try:
		l = input()
	except KeyboardInterrupt:
		pass
	if l:
		log.write(l + '\n')
		log.flush()
		if l == 'xboard':
			print('feature myname="PyTuroChamp" done=1')
		elif l == 'quit':
			sys.exit(0)
		elif l == 'new':
			d = c.Board()
		elif l == 'go' or l == 'force':
			if not d:
				d = c.Board()
			r = p.getmove(d, silent = True)
			if r:
				move(r)
		elif l == '?':
			print("move", r)
			log.write("move %s\n" % r)
			log.flush()
		else:
			if not d:
				d = c.Board()
			if l[0] in abc and l[2] in abc and l[1] in nn and l[3] in nn:
				if len(l) == 6:
					l = l[:4] + 'q'	# "Knights" outputs malformed UCI pawn promotion moves
				d.push_uci(l)
				r = p.getmove(d, silent = True)
				if r:
					move(r)


