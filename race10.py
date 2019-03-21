# https://galacticpuzzlehunt.com/puzzle/race-for-the-galaxy
# Round 10 solver
# Paste the grid into "grid" below, and the word list into "words".
# Run with:
#   python3 race10.py

from __future__ import print_function, division
from itertools import product

grid = """
F	R	P	G	Y	U	H	W	K	G	S	C
J	T	K	F	B	K	G	X	J	T	P	C
T	T	T	X	C	L	D	R	G	G	R	Y
K	U	C	X	T	D	P	J	R	G	G	C
F	F	O	G	K	D	I	D	F	C	C	Y
D	U	Z	U	R	O	Y	C	W	J	Y	D
U	K	I	C	R	K	O	C	U	K	G	W
C	G	L	S	Y	G	G	K	C	C	U	C
W	B	D	D	L	C	R	R	U	U	J	L
P	D	G	M	Y	D	G	P	K	C	Y	H
G	K	G	D	U	K	A	F	G	R	T	U
L	C	T	J	D	L	D	V	D	X	G	D
""".upper()

words = """
APPAREL
BLACKANDBLUE
BUILDER
COUNTRYMAN
CRANK
CZARINA
HEREBY
INDIVISIBLE
NOISE
NUMERICAL
PRONOUN
SANITATION
TENEMENT
TIMES
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

def unused(lmap):
	return "".join(c for c in "ABCDFEGHIJKLMNOPQRSTUVWXYZ" if c not in lmap)

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
	toremove = set(cell for spot in wspots for cell in spot)
	return sorted(cells - toremove)

for lmap in lmaps:
	lgrid = mapgrid(grid, lmap)
	for y in range(H):
		print(*[lgrid[y][x] for x in range(W)])
	print()
	for wspots in product(*[spots(lgrid, word) for word in words]):
		print("".join(lgrid[y][x] for x, y in eliminate(lgrid, wspots)))
	print("Unmapped letters:", unused(lmap))
	print()




