"""
https://codeforces.com/problemset/problem/498/E

输入一个长为 7 的数组 w(0≤w[i]≤1e5)，保证至少有一个 w[i]>0。

对于 i=1,2,...,7，从左到右依次拼接高为 i，底边长为 w[i] 的矩形（底边对齐），我们可以得到一个阶梯图形。
图形的边缘已经涂色。
你需要把图形内部格子的部分边界涂色，要求每个格子的四条边不能都被涂色。

输出涂色方案数，模 1e9+7。

fj for j in range(0...1<<7) 代表一种顶边涂色方案 从下面转移的方案

"""
import itertools
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
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






w = RILIST()

# 2^7-1
u = 7
m = 1<<7
f = [0]*m
f[m-1] = 1

fmp = FastMatPow()
# f = [0]*(1<<7)
# # 0b00001 = 1

for i in range(7):
    # 高度为h
    h, n = i+1, w[i]

    if i > 0:
        base = 0
        for j in range(i, h):  # [pre, h]
            base |= 1 << j
        g = [0] * (1 << h)  # 左侧边界的涂色情况
        for s in range(1 << i):
            g[s | base] += f[s]
        f = g
    else:
        f = [0]*(1<<h)
        f[1] = 1

    A = [[0] * (1<<h) for _ in range(1<<h)]
    for right in range(1 << h):

        # fj <- f1...fh
        for left in range(1 << h):

            # 台阶高出的一段没有涂满色没意义
            # if left & base != base: continue

            g = [None for _ in range(h+1)]  # g[i] i都不涂色 i底下涂色 i顶上涂色 i上下都涂色
            g[0] = (0, 1, 0, 0)
            for i in range(h):
                p00, p01, p10, p11 = g[i]
                if right >> i & 1 and left >> i & 1:
                    #  10/00 -- 00
                    s00 = p10 + p00
                    s01 = p10 + p00
                    s10 = p11 + p01
                    s11 = 0
                else:
                    s00 = p00 + p10
                    s01 = p00 + p10
                    s10 = p11 + p01
                    s11 = p01 + p11
                g[i + 1] = (s00, s01, s10, s11)

            # 考虑右侧边界必须涂色的
            cur = g[h][1] + g[h][3]
            A[left][right] = cur

    f = fmp.state_dp_power(A, f, n)

print(f[-1])






