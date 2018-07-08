#!/usr/bin/env python3

# Compare moves from PyTuroChamp with desired results

import chess as c
import pyturochamp as p
#import bare as p
#import newt as p
#import heu2 as p
#import test as p

t = [
 ('8/8/1KN5/8/3P4/3p4/P2k4/8 w - - 0 1', 'c6b4', 'CB Turing'),
 #('rnbqkbnr/ppp2ppp/8/3pp3/8/2N1P3/PPPP1PPP/R1BQKBNR w KQkq - 0 3', 'g1h3', 'CB TUROCHAMP'),
  #  ("rn1qk2r/pp4pp/2p1pp2/3n2B1/P2Pp2P/2P3N1/2P2PP1/R2QK2R w KQkq - 0 12", "g5d2", "keine Rochade"),
  #   ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "e2e4", "Opening"),
   #  ("rnb1kbnr/ppp2ppp/8/4p3/3P1q2/2N2N2/PPP3PP/R1BQKB1R b KQkq - 0 6", 'f4g4', 'Dame'),
   #  ("r2qkbnr/ppp2ppp/3p4/4N3/2BnP1b1/2N5/PPPP1PPP/R1BQ1RK1 b kq - 0 6",  'd6e5', 'Seekadettenmatt'),
  #   ("r2q1rk1/ppp1bppp/4p3/3p1b2/1n1PnP2/2NBPN2/PPP3PP/R2QBRK1 w - - 8 10",  'f3e5', 'Right knight'),

     #("rnb1kbnr/ppp1pppp/8/2Nq4/3p4/5N2/PPPPPPPP/R1BQKB1R b KQkq - 3 4",  'd5c5', 'Get your knights'),
#("rnb1kbnr/ppp1pppp/8/3q4/N2p4/5N2/PPPPPPPP/R1BQKB1R w KQkq - 2 4", 'e5e4', 'Keep your knights'),
    #  ("r1bqkbnr/ppp2ppp/2n5/3pp3/7N/3P4/PPP1PPPP/RNBQKB1R w KQkq - 0 4", 'h4f3', 'Keep your knights'),
#("rn1qkbnr/pppb3p/5pp1/1Q6/2p1p2P/2N1P3/PPPP1PP1/R1B1KB1R w KQkq - 2 9", "b5d5", "queen"),
 #("r1bqk1nr/1pp2ppp/p1n5/4p3/2Np4/3P1N2/PPPbPPPP/R2QKB1R w KQkq - 0 8", 'd1d2', 'Keep your castling rights'),
 #("r1bb2rk/pp3p1p/5p1Q/2p2N2/2p1P3/2B5/PPPK1PPP/R6R w - - 1 18", 'c3f6', 'Mate in 3 vs Sunfish'),
 #("r2q1rk1/ppp1nppp/2nb4/5b2/3PQ3/2N2N2/PP2P1PP/R1B1KB1R w KQ - 1 10", 'e4h4', 'Sturm gambit epic fail'),
 #("5rkr/p5p1/1b1N2q1/3Pp2p/4N1b1/5B2/PPP1QP1P/RK1R4 w - - 1 29", 'f3g4', 'Newt-Bare first blunder'),
 #("5rkr/p5p1/1b1N2q1/3Pp2p/4N3/3R1b2/PPP1QP1P/RK6 w - - 0 30", 'e2e1', 'Newt-Bare 2nd blunder'),
 #("7k/1P3ppp/8/8/8/8/2K5/8 w - - 0 1", 'b7b8q', 'pawn promotion'),
 #("r1bqk1nr/pppp1ppp/1bn1p3/8/2BP4/4PN2/PPP2PPP/RNBQK2R w KQkq - 1 5", 'e1g1', 'castling'),
 #("5rk1/2p1bppp/Q7/1p2n3/5n2/2Pq3b/PP1P1PPP/RNBB1RK1 b - - 0 14", 'h3g2', 'HAL 9000 vs Poole'),
]

for x, y, z in t:
	d = c.Board(x)
	t, r = p.getmove(d, usebook = False)
	if r[0] == y:
		print(z, "test passed", 30 * '=')
	else:
		print(z, "test FAILED:", r[0], 30 * '*')


