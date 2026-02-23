"""
https://codeforces.com/problemset/problem/226/C

输入 mod(1≤mod≤1e9) L R(1≤L<R≤1e12) k(2≤k≤r-l+1)。

定义斐波那契数列 F(1)=F(2)=1，F(n)=F(n-1)+F(n-2) (n≥3)。
从 [L,R] 中选择恰好 k 个不同整数，计算这 k 个数的 F(i) 的 GCD。
比如选择 2,4,5，那么计算的是 GCD(F(2), F(4), F(5))。

输出 GCD 的最大值，模 mod。
注意：先满足 GCD 最大，再算 mod。

k - [L,R]

R//k - (L-1)//k

i*i > R

1e12 -> 1e6


"""
import sys
from math import isqrt

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
# MOD = 10 ** 9 + 7

MOD, L, R, k = RII()


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



# d - (L-1)//d, R//d

# d*k > R
# - 此时d作为gcd 肯定是凑不够k个的 [L,R]
# d <= R//k 枚举的d不应该大于 R//k

# [ i    R]
# d*p
# d<i 考虑d作为gcd
# 考虑d作为段数，则对应gcd是p
# d作为段数 小于k的就不考虑了，考虑大于k的时候（还有L)

# 对于任意大于i的d
# d*p < R 对应的p < i 其作为段数应该被枚举过了


m = isqrt(R)+1
g = 1
for d in range(2, m + 1):
    # print(d)
    for d1 in (d, R // d):
        if R // d1 - (L - 1) // d1 >= k:
            g = mx(g, d1)
            #print(d1, (R // d1, (L - 1) // d1), R // d1 - (L - 1) // d1)

# print(g)
# F(g)
# f2 = f1 + f0
# f3 = f2 + f1

# 1 1
# 1 2


A = [[1, 1], [1, 2]]
f = [0, 1]

k, r = g//2, g%2
A = pow_Ak(A, k)
y = Ax(A, f)
# print(k, r, y)
print(y[r])