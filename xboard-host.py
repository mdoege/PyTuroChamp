#!/usr/bin/env python3

# Hosts a game between two XBoard engines (GNU Chess and mame-chessengine)
# (Updated board images are written to board.svg.)

# Probably only works on POSIX systems

import os, sys, select, time
from subprocess import Popen, PIPE
import chess as c
import chess.svg

board = c.Board()
p1 = Popen(["gnuchess", "-x", "-e"], stdin = PIPE, stdout = PIPE, stderr = None)
p2 = Popen(["academy"], stdin = PIPE, stdout = PIPE, stderr = None)

def svg():
	lm = board.peek()
	a = [(lm.from_square, lm.to_square)]
	s = chess.svg.board(board, arrows = a, size = 800)

	with open("board.svg", 'w') as f:
		f.write(s)

# https://stackoverflow.com/questions/36476841/python-how-to-read-stdout-of-subprocess-in-a-nonblocking-way
y = select.poll()
y.register(p1.stdout, select.POLLIN)

z = select.poll()
z.register(p2.stdout, select.POLLIN)

a, b = [], []

tt = time.time()

def e(x):
	return x.encode("ascii")

def d(x):
	return x.decode("ascii")

def gc(x):
	if b":" in x:
		return []
	x = d(x)
	if "move" in x:
		m = x.split()[1]
	else:
		x = x.split()
		if '.' in x[0]:
			if '.' in x[1]:
				m = x[2]
			else:
				m = x[1]
	try:
		board.push_uci(m)
		print(board)
		print(board.move_stack)
	except:
		print("Bad UCI")
		m = ''
	svg()
	if board.result() != '*':
		print(board.result())
		sys.exit(0)
	return m

start = False
while True:
	if y.poll(1):
		aa = p1.stdout.readline()
		a.append(aa)
		print(aa)
		if start:
			c = gc(aa)
			if c:
				print(c, "*** W")
				p2.stdin.write(e(f"{c}\n"))
				p2.stdin.flush()
			
	elif z.poll(1):
		bb = p2.stdout.readline()	
		b.append(bb)
		print(bb)
		if start:
			c = gc(bb)
			if c:
				print(c, "*** B")
				p1.stdin.write(e(f"usermove {c}\n"))
				p1.stdin.flush()
	else:
		if time.time() - tt > 10:
			print("Game starts now...")
			p1.stdin.write(b"xboard\n")
			p2.stdin.write(b"xboard\nnew\nblack\n")
			p1.stdin.write(b"go\n")
			p1.stdin.flush()
			start = True
			tt = time.time() + 1e6


