"""
https://codeforces.com/problemset/problem/514/E

输入 n(1≤n≤1e5) x(0≤x≤1e9) 和长为 n 的数组 d(1≤d[i]≤100)。

有一棵无限大的 n 叉树，每个节点都有 n 个儿子。
对于每个节点，到其第 i 个儿子的距离为 d[i]。

输出距离根节点不超过 x 的节点个数，模 1e9+7。
注意根节点一定满足要求，也算在内。

 1 2 3

d1 d2 ... dn

新增一个根节点并加入n个子树
f[x] = f[x-d[1]] ... f[x-d[n]] + 1

f[x] = c1 * f[x-d1] ... cm * f[x-dm] + 1

di - depth 为 di 1-100
ci - 对应count

f[x] = d[0] * f[x-1] ... d[k] * f[x-k] + 1 * 1

"""
import itertools
import sys
from collections import defaultdict
from functools import cache
from math import inf
from operator import add, xor
from typing import List

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
        # init/sk-1 = [f0,...fk-1, constant]
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
        #   [...     1 0]   fn-k    =  fn-k+1
        #   [...       1]]  constant
        #
        # 只有第一行递推，后面就是串位

        A = [[0] * k for _ in range(k)]
        A[0] = [x % mod for x in c]  # 第一行: c0..ck-1
        for i in range(1, k):
            A[i][i - 1] = 1  # 次对角线 1

        # S_{k-1} = [f_{k-1},...,f_0]^T
        S = [[init[k - 1 - i] % mod] for i in range(k)]


        e = n - (k - 1)
        M = FastMatPow.mat_pow(A, e, mod)
        U = FastMatPow.mat_vec(M, S, mod)
        return U[0][0] % mod

    @staticmethod
    def linear_recursion_with_constant(c, init, n, mod=MOD, constant=0):
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
        # fk+1 = c0*f1 + ... ck-1*fk + c

        # A               * Sn-1    =  Sn
        # [[c0 c1 ... ck]   fn-1    =  fn
        #   [1 0 ...   0]   fn-2    =  fn-1
        #   [0 1 0 ... 0]   fn-3    =  fn-2
        #   [...       0]   ...
        #   [...     1 0]   fn-k    =  fn-k+1
        #   [...       1]]  constant
        #
        # 只有第一行递推，后面就是串位

        A = [[0] * (k+1) for _ in range(k+1)]
        for i,x in enumerate(c):
            A[0][i] = x % mod

        for i in range(1, k):
            A[i][i - 1] = 1  # 次对角线 1

        A[0][k] = 1
        A[k][k] = 1

        # s - f[k] => f[n]
        s = init[::-1] + [constant]

        e = n - k
        M = FastMatPow.mat_pow(A, e, mod)
        U = FastMatPow.mat_vec(M, s, mod)
        return U[0] % mod

    """
    状态机dp 
    A * f[i][状态...] = f[i+1][状态...]

    """

    @staticmethod
    def state_dp_power(A, init_state, n, mod=MOD):
        # s_{i+1} = A * s_i
        # s0 = init_state（列向量），返回 s_steps。
        # S0 ... Sn
        # A * S0 = S1
        # A^n * S0 = Sn

        if n == 0:
            return init_state

        f0 = init_state
        M = FastMatPow.mat_pow(A, n, mod)  # A^n = M
        S = FastMatPow.mat_vec(M, f0, mod)  # Sn = A^n * S0 = M * s0
        return S


n, x = RII()
d = [0] * 100
for i in RILIST():
    d[i-1] += 1

# f[0...100]
f = [0]*101
f[0] = 1
for k in range(1,101):
    f[k] = 1
    for e in range(1, k+1):
        f[k] += f[k-e] * d[e-1] # 深度 e 的边 对应深度的子树数量
        f[k] %= MOD

fmp = FastMatPow()
# c, init, n, mod=MOD
fx = fmp.linear_recursion_with_constant(d, f, x, MOD, 1)
print(fx)