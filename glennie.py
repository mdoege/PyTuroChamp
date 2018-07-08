#!/usr/bin/env python3

# Show White moves that differ between PyTuroChamp and the TUROCHAMP-Glennie game

import chess as c
import chess.pgn
import pyturochamp as p

pgn = open('glennie.pgn')
game = chess.pgn.read_game(pgn)

b = game.board()
bad = 0

for m in game.main_line():
	if b.turn == c.WHITE:
		t, r = p.getmove(b, usebook = False, silent = True)
		if r[0] != str(m):
			print(b.fullmove_number, m, r[0])
			bad += 1
	b.push(m)

print('===>', bad, 'moves differ')

