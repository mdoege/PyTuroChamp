#!/usr/bin/env python3

# Show White moves that differ between PyTuroChamp and the TUROCHAMP-Kasparov game

import chess as c
import chess.pgn
import pyturochamp as p

pgn = open('kasparov_2012.pgn')
game = chess.pgn.read_game(pgn)

b = game.board()
bad = 0

p.MAXPLIES = 1	# equals 2 plies
p.QPLIES = 7
p.PSTAB = 0
p.PDEAD = 1
p.MATETEST = False

print('pstab = %u, maxplies = %u, qplies = %u' % (p.PSTAB, p.MAXPLIES, p.QPLIES))

for m in game.mainline_moves():
	if b.turn == c.WHITE:
		t, r = p.getmove(b, usebook = False, silent = True)
		if r[0] != str(m):
			print(b.fullmove_number, m, r[0])
			bad += 1
	b.push(m)

print('===>', bad, 'moves differ')

