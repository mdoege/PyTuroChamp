#!/usr/bin/env python3

import chess as c
import chess.pgn
import shannon as p

pgn = open('shannon_exhib_1.pgn')
game = chess.pgn.read_game(pgn)

b = game.board()
bad = 0

p.MAXPLIES = 1	# equals 2 plies
p.QPLIES = 7
p.MATETEST = False
p.PAWNRULE = False

print('maxplies = %u, qplies = %u' % (p.MAXPLIES, p.QPLIES))

for m in game.mainline_moves():
	if b.turn == c.WHITE:
		t, r = p.getmove(b, usebook = False, silent = True)
		if r[0] != str(m):
			print(b.fullmove_number, m, r[0])
			bad += 1
	b.push(m)

print('===>', bad, 'moves differ')

