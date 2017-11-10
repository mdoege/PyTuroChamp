#!/usr/bin/env python3

# computer plays as white

import chess as c
import math

# computer plays as white

COMPC = c.WHITE
PLAYC = c.BLACK

b = c.Board()

for x in b.legal_moves:
	b.push(x)
	ppv = 0
	for i in range(64):
		m = b.piece_at(i)
		if m and m.piece_type in (c.QUEEN, c.ROOK, c.BISHOP, c.KNIGHT) and m.color == COMPC:
			mv_pt, cp_pt = 0, 0
			a = b.attacks(i)
			for s in a:
				e = b.piece_at(s)
				# empty square
				if not e:
					mv_pt += 1
				# enemy square
				elif e.color == PLAYC:
					cp_pt += 2
			ppv += math.sqrt(mv_pt + cp_pt)
			if m.piece_type != c.QUEEN:
				ndef = len(list(b.attackers(COMPC, i)))
				# defended
				if ndef == 1:
					ppv += 1
				# twice defended
				if ndef > 1:
					ppv += .5
	print(x, ppv)
	b.pop()

