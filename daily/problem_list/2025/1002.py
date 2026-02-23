"""
https://codeforces.com/problemset/problem/1117/D

输入 n(1≤n≤1e18) m(2≤m≤100)。

构造一个数组 a，只包含 1 和 m，且 sum(a) = n。
输出方案数，模 1e9+7。

注意元素顺序不同，也算不同的数组，比如 [1,1,m] 和 [m,1,1] 是不同的数组。

f0 = ... = fm-1 = 1

f0 + fm-1 = fm
f1 + fm = fm+1
f2 + fm+1 = fm+2

fm = f0 + fm-1
fm+1 = f1 + fm = f0 + f1 + fm-1
fm+2 = fm+1 + f2 = f0 + f1 + f2 + fm-1

1  ...   1
1 1 ...  1
1 1 1... 1

1 0 1
1 1 1

f0 + f2 = f3
f1 + f3 = f4 = f1 + f0 + f2
f2 + f4 = f5 = f1 + f0 + f2 + f2

1 1 1
1 2 2
2 3 4

1 1 1 1 1 -- fm
1 2 2 2 2 -- fm+1 = fm + (f1...fm-1)
2 3 4 5 6 -- fm+2 = fm+1 + fm + (f2 ... fm-1)
4 6 7 9 10 -- fm+3 = fm+2 + fm+1 + fm + (f3 ... fm-1)
8 12 14 17 20 -- fm+4 = fm+3 + fm+2 + fm+1 + fm + fm-1



"""
import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict, deque
from math import inf, gcd

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

n, m = RII()

f = [1]*m
# f0 = ... = fm-1 = 1
# fm   = fm-1 + f0
# fm+1 = fm + f1

A = [None for _ in range(m)]
A[0] = [0]*m
A[0][0] = A[0][-1] = 1
for i in range(1, m):
    A[i] = A[i-1][:]
    # A[i] -- fm+i = fm+i-1 + fi
    A[i][i] += 1
# print(A)

def Ax(A, x):
    # A*x = b
    # m*n * n*1 = m*1
    m = len(A)
    b = [0]*m
    for i, row_a in enumerate(A):
        cur = 0
        for aij, xj in zip(row_a, x):
            cur = (cur + aij * xj) % MOD
        b[i] = cur
    return b

def mat_multiply(A, B):
    # A*B = C
    # m*k * k*n = m*n
    # cij = aik * bkj
    m, k, n = len(A), len(B), len(B[0])
    C = [None]*m
    for i, row_a in enumerate(A):
        row_c = [0]*n
        for j in range(n):
            cij = 0
            for p in range(k):
                cij = (cij + row_a[p] * B[p][j]) % MOD
            row_c[j] = cij
        C[i] = row_c
    return C

def pow_Ak(A, k):
    # k=0b10110
    n = len(A)
    I = [[1 if (i==j) else 0 for j in range(n)] for i in range(n)]
    res = I
    cur = A

    for i in range(k.bit_length()):
        if k >> i & 1:
            res = mat_multiply(res, cur)
        cur = mat_multiply(cur, cur)
    return res

k, r = n//m, n % m
# Af0 - f1 ... fk

A = pow_Ak(A, k)
y = Ax(A, f)

print(y[r])




