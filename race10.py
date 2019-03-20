# https://galacticpuzzlehunt.com/puzzle/race-for-the-galaxy
# Round 10 solver
# Paste the grid into "grid" below, and the word list into "words".
# Run with:
#   python3 race10.py

from __future__ import print_function, division
from itertools import product

grid = """
L	Q	Q	D	H	P	Z	H	G	L	A	A
J	X	G	H	Q	Z	M	P	O	S	G	H
S	P	J	A	O	D	L	P	H	S	K	Q
O	K	S	Q	F	Q	K	D	O	V	A	Q
S	O	D	P	H	C	G	K	O	U	Q	S
Q	C	K	G	Z	B	M	H	P	Z	D	M
M	J	X	Q	O	D	N	V	M	A	J	Q
K	Q	D	M	S	A	P	D	K	N	O	A
K	Q	X	J	G	A	X	I	G	M	P	X
H	X	H	P	K	P	N	K	B	Q	S	N
Q	H	K	Q	C	M	P	C	P	P	K	P
B	P	K	S	P	J	D	X	P	O	V	B
""".upper()

words = """
BIOPSY
CONDO
COUPLET
DISORGANIZED
DROWSILY
GENRE
INDEFENSIBLE
PLAYPEN
PRONOUNCED
RADIOTHERAPY
SHORTCHANGE
SUBTLY
UNSOLD
WARHORSE
""".upper()


grid = [line.strip().split() for line in grid.splitlines() if line]
words = words.strip().split()
words = sorted(words, key=len, reverse=True)
H = len(grid)
W = len(grid[0])

dirs = [
	(1, 0),
	(0, 1),
	(-1, 0),
	(0, -1),
]
include_diagonals = True
if include_diagonals:
	dirs += [(dx, dy) for dx in (-1, 1) for dy in (-1, 1)]

# An lmap is a partial bijective map from the alphabet to the alphabet that matches one or more word placements.
def reverselmap(lmap):
	return { v: k for k, v in lmap.items() }
def isconsistent(lmap1, lmap2):
	if not all(lmap1[k] == lmap2[k] for k in set(lmap1) & set(lmap2)):
		return False
	rmap1 = reverselmap(lmap1)
	rmap2 = reverselmap(lmap2)
	if not all(rmap1[k] == rmap2[k] for k in set(rmap1) & set(rmap2)):
		return False
	return True
def merge(lmap1, lmap2):
	assert isconsistent(lmap1, lmap2)
	return { k: (lmap1[k] if k in lmap1 else lmap2[k]) for k in set(lmap1) | set(lmap2) }

def uniq(lmaps):
	lmaps = set(tuple(sorted(lmap.items())) for lmap in lmaps)
	return [dict(lmap) for lmap in lmaps]

# A placement is a 2-tuple of position (corresponding to the start of the word) and direction.

def within(pos):
	x, y = pos
	return 0 <= y < H and 0 <= x < W

def cellsof(placement, length):
	(x0, y0), (dx, dy) = placement
	return [(x0 + j * dx, y0 + j * dy) for j in range(length)]

def placementwithin(placement, length):
	for cell in cellsof(placement, length):
		if not within(cell):
			return False
	return True

def placements(word):
	for x in range(W):
		for y in range(H):
			for d in dirs:
				placement = (x, y), d
				if placementwithin(placement, len(word)):
					yield placement

def lmapfor(word, placement):
	lmap = {}
	for cell, letter in zip(cellsof(placement, len(word)), word):	
		x, y = cell
		toletter = grid[y][x]
		if letter in lmap and lmap[letter] != toletter:
			return None
		lmap[letter] = toletter
	return lmap

def lmapsfor(word):
	for placement in placements(word):
		lmap = lmapfor(word, placement)
		if lmap is not None:
			yield lmap

lmaps = [{}]
for word in words:
	nlmaps = []
	for lmap1 in lmaps:
		for lmap2 in lmapsfor(word):
			if isconsistent(lmap1, lmap2):
				nlmaps.append(merge(lmap1, lmap2))
#	lmaps = nlmaps
	lmaps = uniq(nlmaps)


def mapgrid(grid, lmap):
	rmap = { v: k for k, v in lmap.items() }
	return [[rmap.get(grid[y][x], "?") for y in range(H)] for x in range(W)]

def spots(lgrid, word):
	for placement in placements(word):
		cells = cellsof(placement, len(word))
		lword = "".join(lgrid[y][x] for x, y in cells)
		if word == lword:
			yield cells

def eliminate(lgrid, wspots):
	cells = set((x, y) for x in range(W) for y in range(H))
	for spot in wspots:
		for cell in spot:
			cells.remove(cell)
	return sorted(cells)

for lmap in lmaps:
	lgrid = mapgrid(grid, lmap)
	for y in range(H):
		print(*[lgrid[y][x] for x in range(W)])
	print()
	for wspots in product(*[spots(lgrid, word) for word in words]):
		print("".join(lgrid[y][x] for x, y in eliminate(lgrid, wspots)))
	print()



