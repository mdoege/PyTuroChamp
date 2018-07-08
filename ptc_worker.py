# PyTuroChamp worker processes

import pyturochamp as ptc
import chess as c
from multiprocessing import Queue, Process, cpu_count
from queue import Empty, Full

def worker():
	while True:
		try:
			b, x, lastpos, compc, cr0, MAXPLIES, QPLIES, PSTAB, PDEAD, MATETEST = urlq.get()
		except:
			pass
		else:
			ptc.MAXPLIES = MAXPLIES
			ptc.QPLIES = QPLIES
			ptc.PSTAB = PSTAB
			ptc.PDEAD = PDEAD
			ptc.MATETEST = MATETEST
			if compc == c.WHITE:
				ptc.COMPC = c.WHITE
				ptc.PLAYC = c.BLACK
			if b.is_castling(x):		# are we castling now?
				castle = ptc.pm()
			else:
				castle = 0
			b.push(x)
			p = ptc.getpos(b) - lastpos + castle
			cr = b.has_castling_rights(compc)
			if cr0 == True and cr == True:	# can we still castle later?
				p += ptc.pm()
			for y in b.legal_moves:
				if b.is_castling(y):	# can we castle in the next move?
					p += ptc.pm()

			if compc == c.WHITE:
				t = ptc.searchmin(b, 0, -1e6, 1e6)
			else:
				t = ptc.searchmax(b, 0, -1e6, 1e6)
			urlr.put((x, p, t))

def start():
	global num_worker_threads, urlq, urlr, new_data, program_run, ti
	num_w = cpu_count()	# determine number of worker processes automatically
	urlq = Queue()		# query queue
	urlr = Queue()		# result queue

	for i in range(num_w):
		ti = Process(target=worker)
		ti.daemon = True
		ti.start()

