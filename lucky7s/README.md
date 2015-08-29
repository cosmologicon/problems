# Lucky 7s

Find the sum of all positive integers between 0 and 10^N that are divisible by 7, and also divisible by 7 when the digits are reversed. We want to handle N = 11 instantly, and N = 10,000 on the order of 1 minute.

## Basic setup

First off, it's okay to treat every number as having exactly N digits, possibly with some leading zeros, because it doesn't matter whether you count leading zeros when you reverse it, because all that does is multiply by some power of 10. For example, it doesn't matter if we treat `259` as `000259`, because `952` and `952000` are both divisible by 7.

So let's say that every number has exactly N digits, `d0`, `d1`, `d2`, ... `d[N-1]`, with `0 <= d[i] < 10`. Let's write out the test for divisibility by 7 in terms of the d's:

	d0 + 10 d1 + 100 d2 + 1000 d3 + 10000 d4 + 100000 d5 + ... = 0 (mod 7)

## Simplifying the arithmetic

Let's simplify that by taking `10^i mod 7`. This is a sequence that goes `1, 3, 2, 6, 4, 5, 1, ...` Once it gets to `1`, you know it repeats. So now our formula looks like this:

	d0 + 3 d1 + 2 d2 + 6 d3 + 4 d4 + 5 d5 + d6 + 3 d7 + 2 d8 + ... = 0 (mod 7)

Let's combine terms with the same number:

	(d0 + d6 + d12 + ...) + 3 (d1 + d7 + d13 + ...) +
	2 (d2 + d8 + d14 + ...) + 6 (d3 + d9 + d15 + ...) +
	4 (d4 + d10 + d16 + ...) + 5 (d5 + d11 + d17 + ...) = 0 (mod 7)

To make things cleaner, let's write those digit sums as `D0` through `D5`. Where `D0 = d0 + d6 + d12 + ...`, and so on through `D5 = d5 + d11 + d17 + ...`.

	D0 + 3D1 + 2D2 + 6D3 + 4D4 + 5D5 = 0 (mod 7)  [eq 1]

So that's one of the two equations a number will have to satisfy in order to be counted. The other one is if we reverse the number, so that `d[N-1]` is the first digit and `d0` is the last digit. I'll use `N = 11` as an example:

	d10 + 10 d9 + 100 d8 + 1000 d7 + 10000 d6 + 100000 d5 + ... = 0 (mod 7)

We can apply the same logic as before, and we'll get the same grouped sums, but with different coefficients:

	4D0 + 6D1 + 2D2 + 3D3 + D4 + 5D5 = 0 (mod 7)  [eq 2]

Let's multiply both sides by 2 so that the coefficient on `D0` is `1` and we can compare it to eq 1.

	D0 + 5D1 + 4D2 + 6D3 + 2D4 + 3D5 = 0 (mod 7)  [eq 3]

Now, eq 2 depends on `N`. If `N` were something other than `11`, then the coefficient on `D0` could be something other than `4`. However, when you multiply through to get eq 3, it will always come out looking the same regardless of `N`. You can check this by just trying it for all `N mod 6`, or you can realize that when you multiply eq 2 by a number, you're just cycling the coefficients through the cycle `1, 5, 4, 6, 2, 3`, so if you cycle the `1` to the beginning, you'll always get eq 3.

Anyway, let's rewrite the two equations we need a number to satisfy, that will work for all N:

	D0 + 3D1 + 2D2 + 6D3 + 4D4 + 5D5 = 0 (mod 7)  [eq 1]
	D0 + 5D1 + 4D2 + 6D3 + 2D4 + 3D5 = 0 (mod 7)  [eq 3]

These equations are only over 6 variables, and modulo 7, there are only 7 possible values for each variable. So we don't need to use algebra to solve these equations simultaneously. There are only 6^7 possible solutions, which is less than 300,000, so we can just try them all very efficiently.

## Down to 3 variables

So, one possibility is to find all possible values of `(D0, D1, D2, D3, D4, D5)` that satisfy those equations modulo 7. For instance, one solution is `(3, 0, 6, 4, 0, 1)`. Then we could find all possible ways that `D0 = 3 (mod 7)`. Remember that `D0 = d0 + d6 + d12 + ...`. For `N = 11`, that's only `d0 + d6`, and each one can only take `10` values, so that's only `100` possible values to check. Once we list all the ways that `D0 = 3 (mod 7)`, `D1 = 0 (mod 7)`, `D2 = 6 (mod 7)`, etc., we could combine them efficiently.

And that would work fine. There's actually one insight that makes this even easier, where we only have 3 variables instead of the 6 variables `D0` through `D5`. Notice that, in eq 1 and eq 3, `D0` and `D3` have the same coefficients, `1` and `6` respectively. So let's combine those into a variable called `X = D0 + 6D3`.

	X + 3D1 + 2D2 + 4D4 + 5D5 = 0 (mod 7)
	X + 5D1 + 4D2 + 2D4 + 3D5 = 0 (mod 7)

Now what if we multiplied both equations through to get the coefficients on `D1` to be the same? Let's multiply the top by 5 and the bottom by 3:

	5X + D1 + 3D2 + 6D4 + 4D5 = 0 (mod 7)
	3X + D1 + 5D2 + 6D4 + 2D5 = 0 (mod 7)

Notice that `D1` and `D4` now have the same coefficients, so let's call that `Y = D1 + 6D4`:

	5X + Y + 3D2 + 4D5 = 0 (mod 7)
	3X + Y + 5D2 + 2D5 = 0 (mod 7)

And if you do this one more time, multiplying the top by 5 and the bottom by 3 again, you see that you can do the same with `Z = D2 + 6D5`:

	4X + 5Y + Z = 0 (mod 7)
	2X + 3Y + Z = 0 (mod 7)

This is plenty good to work with, but if you want, you can combine algebraically reduce those two equations to these two:

	X = -Y = Z (mod 7)  [eq 4]

(For aesthetic reasons, I probably should have defined `Y` as `-Y`, but I'll stick with my convention. I don't think it makes things much harder.)

So there are obviously 7 possible solutions to this pair of equations, one for each value of `X`. For instance `(X, Y, Z) = (1, 6, 1)`. So we just need to step through these 7 possibilities, tally up all the possible ways that `X`, `Y`, and `Z` can take the necessary values, and add them to the total.

As one final simplification, remember that `X` is defined as `D0 + 6D3`, which is `d0 + 6d3 + d6 + 6d9 + d12 + 6d15 + ...`. But notice that `6 = -1 (mod 7)`, so we can rewrite it (and similarly `Y` and `Z`) as:

	X = D0 + 6D3 = D0 - D3 = d0 - d3 + d6 - d9  + d12 - ...
	Y = D1 + 6D4 = D1 - D4 = d1 - d4 + d7 - d10 + d13 - ...
	Z = D2 + 6D5 = D2 - D5 = d2 - d5 + d8 - d11 + d14 - ...

So that's how I'll use them, as alternating sums of every 3rd digit.

## Tallying the possibilities

So let's say we've picked one of the 7 possible values for `(X, Y, Z)`, such as `(1, 6, 1)`. We want to sum up the value:

	d0 + 10 d1 + 100 d2 + 1000 d3 + 10000 d4 + ....

for every set of d's that satisfies:

	1 = d0 - d3 + d6 - d9 + ... (mod 7)  [eq 5]
	6 = d1 - d4 + d7 - d10 + ... (mod 7)
	1 = d2 - d5 + d8 - d11 + ... (mod 7)

Let's think about a simpler problem. What's the sum of all 3-digit numbers, each of whose digits is prime (`2`, `3`, `5`, or `7`)? So `222 + 223 + 225 + ... + 775 + 777`? There are `4 x 4 x 4 = 64` such numbers. How many times will `2` appear in the ones place? One time for each of the 4 possibilities for the tens place, and the 4 possibilities for the hundreds place. So it will appear in the ones place `4 x 4 = 16` times. So will `3`, `5`, and `7`. So the ones-place total will be `4 x 4 x (2 + 3 + 5 + 7)`. The contribution from each of the other two places are similar:

	4 x 4 x (2 + 3 + 5 + 7) +
	4 x (20 + 30 + 50 + 70) x 4 +
	(200 + 300 + 500 + 700) x 4 x 4

Equivalently, if you don't mind using fractions for a while (don't worry, they'll cancel out), you can look at the _average_ of the ones place, which is (2 + 3 + 5 + 7) / 4 = 4.25. Similarly the average is 42.5 for the tens place, and 425 for the hundreds. So the total is:

	4 x 4 x 4 x (425 + 42.5 + 4.25)

So we're able to get the sum without enumerating all possibilities as long as we have the total (or average) value of `d0`, `10 d1`, and `100 d2`, as well as the number of possibilities for `d0`, `d1`, and `d2`.

We're going to follow a similar strategy for Lucky 7s, but we need to combine multiple digits together into independent groups, based on the three equations in eq. 4, since any set of d's satisfying the first equation can be paired with any set of d's satisfying each of the other two equations. Right? We can't just list the valid values for `d0`, since it depends on `d3`, `d6`, `d9`, etc. But it doesn't depend on `d1`, `d2`, `d4`, etc. So here are our three independent subtotals:

	d0 + 10^3 d3 + 10^6 d6 + 10^9 d9 + ...
	10 d1 + 10^4 d4 + 10^7 d7 + 10^10 d10 + ...
	10^2 d2 + 10^5 d5 + 10^8 d8 + 10^11 d11 + ...

We want the number of solutions to each equation in eq 4, and also the sum of all those solutions as listed here. Here's the definitions:

	n0(X) = number of solutions to:
		X = d0 - d3 + d6 - d9 + ... (mod 7)
	T0(X) = sum over these n0(X) solutions of:
		d0 + 10^3 d3 + 10^6 d6 + 10^9 d9 + ...

	n1(Y) = number of solutions to:
		Y = d1 - d4 + d7 - d10 + ... (mod 7)
	T1(Y) = sum over these n1(Y) solutions of:
		10 d1 + 10^4 d4 + 10^7 d7 + 10^10 d10 + ...

	n2(Z) = number of solutions to:
		Z = d2 - d5 + d8 - d11 + ... (mod 7)
	T2(Z) = sum over these n2(Z) solutions of:
		10^2 d2 + 10^5 d5 + 10^8 d8 + 10^11 d11 + ...

So our total contribution from `(X, Y, Z) = (1, 6, 1)` is:

	n0(1) n1(6) n2(1) (T0(1) / n0(1) + T1(6) / n1(6) + T2(1) / n2(1))

or equivalently:

	T0(1) n1(6) n2(1) +  [eq 6]
	n0(1) T1(6) n2(1) +
	n0(1) n1(6) T2(1)

Add up similar sums for each of the seven solutions to eq 4, and you've got your grand total.

Let's simplify things just a little more. You may have noticed there's a lot of overlap in the definitions of the `n`s and `T`s. When `N = 11`, for instance, there are 4 terms in each of the sums for `X` and `Y`, so `n0` is exactly the same function as `n1`. Let's just define a single function:

	n(k, m) = number of solutions to:
		k = a0 - a1 + a2 - a3 + a4 - ... (mod 7)
	where 0 <= a[i] < 10, and there are m terms in the sum

Now `n0(X)` is replaced with `n(X, (N+2)//3)`, because there are `(N+2)//3` terms in the `X` sum. Similarly:

	n0(X) = n(X, (N+2)//3)
	n1(Y) = n(Y, (N+1)//3)
	n2(Z) = n(Z, N//3)

The `T`s are similar:

	T(k, m) = sum over the n(k, m) solutions of:
		a0 + 10^3 a1 + 10^6 a2 + 10^9 a3 + ...

So:

	T0(X) = T(X, (N+2)//3)
	T1(Y) = 10 T(Y, (N+1)//3)
	T2(Z) = 100 T(Z, N//3)

So eq 6 becomes with the new definitions:

	Tx ny nz + 10 nx Ty nz + 100 nx ny Tz
		where:
	nx = n(X, (N+2)//3)    Tx = T(X, (N+2)//3)
	ny = n(Y, (N+1)//3)    Ty = T(Y, (N+1)//3)
	nz = n(Z, N//3)        Tz = T(Z, N//3)

## Dynamic programming

So all that remains is to implement the `n` and `T` functions, which can be done with dynamic programming or recursion with memoization. I'll use recursion.

Again, the definition of `n` is:

	n(k, m) = number of solutions to:
		k = a0 - a1 + a2 - a3 + a4 - ... (mod 7)
	where 0 <= a[i] < 10, and there are m terms in the sum

The base case is `m = 0`, in which case the equation becomes:

	n(k, 0) = number of solutions to:
		k = 0 (mod 7)

This has one solution when `k = 0`, and no solutions otherwise. Thus `n(0, 0) = 1`, and `n(k, 0) = 0` for `k > 0`.

Now consider `m > 0`, for example, `m = 5`. We can assume `n` values exist for all `m < 5`. So we want to loop through the possible values of `a4`, and add them each to the corresponding `n` values for `m = 4`. For instance, if `k = 4` and `a4 = 1`, then the formula is:

	k = a0 - a1 + a2 - a3 + a4 (mod 7)
	4 = a0 - a1 + a2 - a3 + 1 (mod 7)
	3 = a0 - a1 + a2 - a3 (mod 7)

which is the formula for `n(3, 4)`. Adding up these values for `n(k-a4, 4)` for all possible `a4` values will give us our answer. One complication is that because the sums are alternating, when `m` is even, we need to add the latest `a` term instead of subtracting it. That's it for `n`; now for `T`:

	T(k, m) = sum over the n(k, m) solutions of:
		a0 + 10^3 a1 + 10^6 a2 + 10^9 a3 + ...

The base case in this case is always `T(k, 0) = 0`, because this sum is `0` if there are 0 `a`s. For higher `m`s like `m = 5`, we can again loop over `a4`, adding up the total for the correspoinding `T(k-a4, 4)`. But there's an additional term of `10^12 a4` added for each solution, so the actual subtotal we need to add in is `10^12 a4 n(k-a4, 4) + T(k-a4, 4)`. Again, the sign will be swapped for even `m`.

In the program, I found it useful to compute both `n` and `T` together, since that's how they're used, so I combined them into a single function `nT`.
