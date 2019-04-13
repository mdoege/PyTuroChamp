#!/usr/bin/env python3

# Show White moves that differ between Bernstein program and the IBM 704 game

import chess as c
import chess.pgn
import bernstein as p
p.COMPC = c.WHITE
p.PLAYC = c.BLACK

pgn = open('bernstein_ibm704.pgn')
#pgn = open('bernie_16_moves_win.pgn')
game = chess.pgn.read_game(pgn)

p.PSTAB = 0
p.MAXPLIES = 3	# 4 plies

bad, badpmt = 0, 0
ml = list(game.mainline_moves())
print('pstab = %u, maxplies = %u' % (p.PSTAB, p.MAXPLIES))

# Check if correct move is in PST

b = game.board()

for m in ml:
	if b.turn == c.WHITE:
		pmt = p.get_pmt(b)
		if str(m) not in pmt:
			print(b.fullmove_number, m, pmt)
			badpmt += 1
		else:
			print('OK', b.fullmove_number, m, pmt)
	b.push(m)


print('===>', badpmt, 'moves not in PMT')


print(50 * '*')

# Check if computed move differs

b = game.board()

for m in ml:
	if b.turn == c.WHITE:
		t, r = p.getmove(b, usebook = False, silent = False)
		if r[0] != str(m):
			print(b.fullmove_number, m, r[0], 30 * '<')
			bad += 1
	b.push(m)

print('===>', bad, 'moves differ (%u%%)' % (200 * bad / len(ml)))

