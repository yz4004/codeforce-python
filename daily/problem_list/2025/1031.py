"""
https://codeforces.com/problemset/problem/93/D

输入 L R(1≤L≤R≤1e9)。

定义 C(n) 表示给一条长为 n 的纸带（n 个格子）涂色的不同方案数。涂色方案需满足如下要求：
1. 每个格子只能使用白色、黑色、红色或黄色。
2. 相邻格子颜色必须不同。
3. 不能有相邻的白色和黄色。
4. 不能有相邻的红色和黑色。
5. 连续三个颜色不能是黑白红，或者红白黑。
如果有两种涂色方案互为逆序，那么这两种方案是相同的。例如 ABCD 和 DCBA 互为逆序。

输出 C(L) + C(L+1) + ... + C(R)，模 1e9 + 7。

w b r y bw rw
0 1 2 3 10 20

0 1 1 0 0  0  -- f0
1 0 0 1 0 -1  -- f1
1 0 0 1 -1 0  -- f2
0 1 1 0 0  0  -- f3
bw
10
0 1 0 0 0 0 - f4

rw
20
0 0 1 0 0 0 - f5

f6 - prefix sum
2 2 2 2 -1 -1 1

1 1 1 1 0 0 ..0 - f6 = sum(.w .b .r .y) -- current sum

f1 = [1,1,1,1,0,0]

fL - A - fL+1
fL...fR

fL, A*fL, A2*fL, ... Ak*fL

(I + A + A^2 ... A^k)*fL, where k=R-L

seq1/seq[::-1]
关于逆序方案只计入一次
    abcd,dcba 都会被统计到，所以这部分应除以2
    abba 回文对称方案在上面的计算中只计入一次

    即对每个 n in [L,R] 考虑 (n+1)//2 的全部方案. P(n) = T((n+1)//2) where T(n) 是全部
    除重后的结应该是 T(n)+P(n) //2 for n in L,R

w  b  r  y  bw  rw
0  1  2  3  10  20
f0 f1 f2 f3 f4  f5

fn = 1+x+x^2 ... x^n
fn-1 = 1+x+...+x^n-1
fn = x*fn-1 + 1

1+x+...x^n + x^n+1 ... x^2n

f(2n) = fn * x^n + fn - x^n
f(n) = fn//2 * x^(n//2) + fn//2 - x^(n//2) +

f3 = x^3 + x^2 + x + 1         f1 = x + 1
f3 = f1 * x^2 + f1 - x^2

f4 = x^4 + x^3 + x^2 + x + 1
f4 = f2 * x^2 + f2 - x^2


"""
import itertools
import sys
from functools import cache
from operator import add, xor
from typing import List
from math import gcd, lcm, isqrt

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7


class FastMatPow:
    MOD = 10 ** 9 + 7

    # A*B = C
    # m*k * k*n = m*n
    # cij = ail * blj for l=1...k
    @staticmethod
    def mat_mul(A, B, mod=MOD):
        m, k, n = len(A), len(B), len(B[0])
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            Ai = A[i]
            for j in range(n):
                cij = 0
                for l in range(k):
                    cij = (cij + Ai[l] * B[l][j]) % mod
                    # cij = ail * blj for l=1...k
                C[i][j] = cij
        return C

    # A^e = U
    @staticmethod
    def mat_pow(A, e, mod=MOD):
        k = len(A)
        I = [[1 if i == j else 0 for j in range(k)] for i in range(k)]
        U = I  # 从单位阵起手
        base = [row[:] for row in A]
        while e > 0:
            if e & 1:
                U = FastMatPow.mat_mul(U, base, mod)
            base = FastMatPow.mat_mul(base, base, mod)
            e >>= 1
        return U

    # A*x = b
    # m*n * n*1 = m*1
    @staticmethod
    def mat_vec(A, x, mod=MOD):
        m = len(A)
        b = [0] * m
        for i, Ai in enumerate(A):
            bi = 0
            for aij, xj in zip(Ai, x):
                bi = (bi + aij * xj) % mod
            b[i] = bi
        return b

    """
    线性递推dp - 快速幂优化
    fn = c0*fn-1 ... ck-1*fn-k


    1. 系数顺序：按近到远填第一行
    c =  [c0   c1 ...   ck-1]  
          fn-1 fn-2 ... fn-k
    对应递推
        fn = c0*fn-1 ... ck-1*fn-k


    2. 幂次 e = n - (k-1)
    初始状态 Sk-1 = [fk-1 ... f0] 
    fn:    Sn   = [fn ... fn-k+1]

    A * Sk-1 = Sk    

    A^e * Sk-1 = Sn where e = n - (k-1)
    """

    @staticmethod
    def linear_recursion(c, init, n, mod=MOD):
        # c = [c0,...ck-1]
        # f_n = c[0]*f_{n-1} + ... + c[k-1]*f_{n-k},  n >= k
        #
        # init/sk-1 = [f0,...fk-1]
        # return f_n % mod

        k = len(c)
        if n < k: return init[n] % mod

        # 伴随矩阵/companion matrix A
        # A*sk = sk+1
        # sk = [f1...fk], sk-1 = [f0...fk-1]
        # fk+1 = c0*f1 + ... ck-1*fk

        # A               * Sn-1    =  Sn
        # [[c0 c1 ... ck]   fn-1    =  fn
        #   [1 0 ...   0]   fn-2    =  fn-1
        #   [0 1 0 ... 0]   fn-3    =  fn-2
        #   [...       0]   ...
        #   [...     1 0]]  fn-k    =  fn-k+1
        # 只有第一行递推，后面就是串位

        A = [[0] * k for _ in range(k)]
        A[0] = [x % mod for x in c]  # 第一行: c0..ck-1
        for i in range(1, k):
            A[i][i - 1] = 1  # 次对角线 1

        # S_{k-1} = [f_{k-1},...,f_0]^T
        S = [[init[k - 1 - i] % mod] for i in range(k)]

        e = n - (k - 1)
        M = FastMatPow.mat_pow(A, e, mod)
        U = FastMatPow.mat_mul(M, S, mod)
        return U[0][0] % mod

    """
    状态机dp 
    A * f[i][状态...] = f[i+1][状态...]

    """

    @staticmethod
    def state_dp_power(A, init_state, n):
        # s_{i+1} = A * s_i
        # s0 = init_state（列向量），返回 s_steps。
        # S0 ... Sn
        # A * S0 = S1
        # A^n * S0 = Sn

        f0 = init_state
        M = FastMatPow.mat_pow(A, n)  # A^n = M
        S = FastMatPow.mat_vec(M, f0)  # Sn = A^n * S0 = M * s0
        return S



L,R = RII()

A = [[0, 1, 1, 0, 0,  0, 0],
    [1, 0, 0, 1, 0, -1, 0],
    [1, 0, 0, 1, -1, 0, 0],
    [0, 1, 1, 0, 0,  0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [2,2,2,2,-1, -1, 1]]  # 最后一个状态对应截止到当前状态的前缀和 当前f0+f1+f2+f3 + 前缀和状态
fmp = FastMatPow()

f1 = [1,1,1,1,0,0,4] # 前缀和是包括当前结尾的 所以初始状态是 f0...f3 初始状态之和4

# x        for x in L...R
# (x+1)//2 for x in L...R

# f1, ... fL
tl = fmp.state_dp_power(A, f1, L-2)[-1] if L-2 >= 0 else 0
tr = fmp.state_dp_power(A, f1, R-1)[-1] if R-1 >= 0 else 0

# 5678
# 3344

# 56789
# 33445

# 4567
# 2334

# if (R-L+1)%2 == 1:
#     l1 = (L+1)//2
#     r1 = (R+1)//2
#
#     l2 = l1
#     r2 = r1-1
#     # 33445
#     # =
#     # 345
#     # 34
# else:
#     l1 = (L + 1) // 2
#     r1 = R // 2
#
#     l2 = (L + 2) // 2
#     r2 = (R + 1) // 2
#     # 3344
#     # =
#     # 34
#
#     # 2334
#     # 23
#     # 34
#
# pl1 = fmp.state_dp_power(A, f1, l1-1)[-1]
# pr1 = fmp.state_dp_power(A, f1, r1)[-1]
#
# pl2 = fmp.state_dp_power(A, f1, l2-1)[-1]
# pr2 = fmp.state_dp_power(A, f1, r2)[-1]

# 34
# 22
# print(tl,tr, (L,R))
# print(l1,r1, l2,r2, pl1,pr1, pl2,pr2, (pr1-pl1) + (pr2-pl2))

# res = (tr - tl + (pr1-pl1) + (pr2-pl2)) // 2 % MOD
# def inv2(x)

# tmp = 0
# for x in range(1, L):
#     fx = fmp.state_dp_power(A, f1, x-1)
#     tx = sum(fx[:4])
#     print(tx, fx, fx[-1])
# for x in range(L,R+1):
#     fx = fmp.state_dp_power(A, f1, x-1)
#     tx = sum(fx[:4])
#     print(tx, fx, fx[-1])
#     #tx = fmp.state_dp_power(A, f1, x-1)[-1]
#
#     px = sum(fmp.state_dp_power(A, f1, (x+1)//2-1)[:4]) if x%2 == 1 else 0
#     cur = (tx + px)//2
#     tmp += cur

# inv2 = (MOD+1)//2
# res = (tr - tl + (pr1-pl1) + (pr2-pl2)) * inv2 % MOD
# print(res)


# [L,R] 中的奇数
# 2345  35 - 23
# 23456 35 - 23
# 3456  35 - 23
# 34567 357 - 234

l1 = L if L % 2 else L+1
r1 = R if R % 2 else R-1

l1, r1 = (l1+1)//2, (r1+1)//2
pl = fmp.state_dp_power(A, f1, l1-2)[-1] if l1-2 >= 0 else 0
pr = fmp.state_dp_power(A, f1, r1-1)[-1] if r1-1 >= 0 else 0


inv2 = (MOD+1)//2
res = (tr - tl + pr-pl) * inv2 % MOD
print(res)
