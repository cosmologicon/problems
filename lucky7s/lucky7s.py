# Solution to the Lucky 7s problem. See README.md for derivation of relevant formulas.

# Usage:
#   time python lucky7s.py 11
# To get the sums of the digits:
#   time python lucky7s.py 10000 | sed 's/./+&/g;s/^/0/' | bc

import sys

# Will compute the sum of all numbers between 0 and 10^N that are divisible by 7, and are still
# divisible by 7 when the digits are reversed.
N = int(sys.argv[1])
sys.setrecursionlimit(N + 20)

# Number of terms in each of the X, Y, and Z sums.
Nx, Ny, Nz = (N + 2) // 3, (N + 1) // 3, N // 3

# Returns (n(k, m), T(k, m))
# n(k, m) = number of solutions to:
#     k = a0 - a1 + a2 - a3 + a4 - ... (mod 7)
# T(k, m) = sum over the n(k, m) solutions of:
#     a0 + 10^3 a1 + 10^6 a2 + 10^9 a3 + ...
# where 0 <= a[i] < 10, and there are m terms in the sum
cache = {}  # memoization cache
def nT(k, m):
	if m == 0:
		# Base case. 1 solution if k = 0 and no solutions otherwise.
		return (1, 0) if k == 0 else (0, 0)
	if (k, m) in cache:
		return cache[(k, m)]
	n, T = 0, 0
	for a in range(10):
		ksub = (k - a) % 7 if m % 2 else (k + a) % 7
		nsub, Tsub = nT(ksub, m - 1)
		n += nsub
		T += Tsub + a * 1000 ** (m - 1) * nsub
	cache[(k, m)] = n, T
	return n, T

total = 0
for X in range(7):
	# Loop over all possible solutions to X = -Y = Z (mod 7).
	Y = -X % 7
	Z = X
	nx, Tx = nT(X, Nx)
	ny, Ty = nT(Y, Ny)
	nz, Tz = nT(Z, Nz)
	total += Tx * ny * nz + 10 * nx * Ty * nz + 100 * nx * ny * Tz
print(total)

