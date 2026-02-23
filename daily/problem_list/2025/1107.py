"""
https://codeforces.com/problemset/problem/1895/F

输入 T(≤50) 表示 T 组数据。
每组数据输入 n(1≤n≤1e9) x(0≤x≤40) k(1≤k≤1e9)。

有多少个数组 a，满足如下条件？
1. 长为 n。
2. 元素值均为非负整数。
3. 至少有一个 a[i] 在 [x,x+k-1] 中。
4. a 中所有相邻元素 (x,y)，均满足 |x-y|≤k。

输出符合要求的 a 的个数，模 1e9+7。

x-y <= k
y-x <= k
- x-k <= y <= x+k
- 2k+1

[x,x+k-1]

hint
- a要求非负 x <= 40. 考虑a的min
- 正难则反 总方案为 min(a) <= 40
0..x x+1...x+k-1

假设第一个选x0 然后取任意波动
- (2k+1)^(n-1)
- 每种对应一个波形，只是首字母不同，通过平移可以将最小值贴合到 [0 - x+k-1]
- 每个最小值 0- x+k-1 对应pattern有 (2k+1)^(n-1)

考虑非法情况
- 最小值位于 [0-x-1] 波动不超过 x-1
- f[i][j] 长为i 结尾j 在 [0-x-1] 波动的数组数量

fij = fij + fij-1 + ... fii 前一个可选的结尾值 j...i 无常数项

fij = sum(f[i-1][l] for l in range(0,x) abs(l-j) <= k)


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

        # S_{k-1} = [f_{k-1},...,f_0] 向量顶对应最新状态 k-1. 初始状态长为k 包含初始0
        s = init[::-1]

        e = n - (k - 1)  # k-1 -> k -> ... -> n 间隔对应的矩阵自乘 n-(k-1)
        M = FastMatPow.mat_pow(A, e, mod)
        U = FastMatPow.mat_vec(M, s, mod)
        return U[0] % mod

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

for _ in range(RI()):
    n, x, k = RII()

    total = (x+k) * pow(2 * k + 1, n - 1, MOD) % MOD
    if x == 0:
        print(total)
        continue

    fmp = FastMatPow()

    # fij 以j结尾的 0-x-1长i数组数量
    f1 = [1]*x
    A = [[0]*x for _ in range(x)]

    for j in range(x):
        for l in range(max_(j-k,0), min_(j+k,x-1)+1):
            A[j][l] = 1
    # f1 ... fn
    fn = fmp.state_dp_power(A, f1, n-1)

    invalid = 0
    for y in fn:
        invalid = (invalid + y) % MOD

    res = (total - invalid + MOD) % MOD
    print(res)

