#!/usr/bin/env python3

# Show White moves that differ between the recorded SOMA game and soma.py

import chess as c
import chess.pgn
import soma as p

pgn = open('soma-mac.pgn')
game = chess.pgn.read_game(pgn)

b = game.board()
bad = 0
o = open('somatest.txt', 'a')
o2 = open('somatest-diff.txt', 'a')

for m in game.mainline_moves():
	if b.turn == c.WHITE:
		t, r = p.getmove(b, usebook = False, silent = True)
		if r[0] == str(m):
			o.write('%u %s %s\n' % (b.fullmove_number, m, r[0]))
		else:
			o2.write('%u %s %s\n' % (b.fullmove_number, m, r[0]))
			bad += 1
	b.push(m)

print('===>', bad, 'moves differ')

