"""
https://codeforces.com/problemset/problem/60/E

输入 n(1≤n≤1e6) x y(0≤x,y≤1e18, x+y>0) mod(2≤mod≤1e9) 和长为 n 的递增数组 a(0≤a[i]≤1e9)。

有 n 个蘑菇排成一行，重量 a[i] 从左到右依次递增。
每过一分钟，在每一对相邻蘑菇 (x,y) 之间，会长出一个重量为 x+y 的蘑菇。

x 分钟后，把所有蘑菇重新排列，重量从左到右依次递增。
然后再过 y 分钟，输出此时所有蘑菇的重量之和，模 mod。

x y z
1 1 1

x x+y y y+z z

+1 +2 +2... +1
2 3 3 ... 2

x 2x+y x+y x+2y y 2y+z y+z y+2z z

10 01
10 11 01




"""
import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict, deque, Counter
from itertools import pairwise
from math import inf, gcd, comb

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x


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


# x,y
# x x+y y
# x 2x+y x+y x+2y y
#  3x+y 3x+2y x+y 2x+3y x+2y


"""
s = s*3 - (a1+an)

3  0         s
1 -(a1+an)   1


2 7 vs 4 5
 97 vs 95

2 6 vs 4 5
 86 vs 95
 14 8 vs 14 9 

"""
n, x, y, mod = RII()
a = RILIST()


# for (p,q) in pairwise(a):
#     p, q = mx(p,q), mn(p,q)
#
#     # t = 0
#     # while t < x:
#     #     a, b = a+b, a
#     #     t += 1
#
#     # 1 1   a  a+b
#     # 1 0   b  a
#
#     A = [[1,1], [1,0]]
#     t = fmp.state_dp_power(A, [p,q], x, mod)[0]
#     an = mx(an, t)

def solve(n,x,y,mod,a):
    if n == 1:
        return a[0] % mod

    fmp = FastMatPow()

    a1 = min(a)

    A = [[1,1], [1,0]]
    an = fmp.state_dp_power(A, [a[-1], a[-2]], x, mod)[0]

    A = [[3, -(a[0]+a[n-1])], [0, 1]]
    f0 = [sum(a)%mod, 1]
    s0 = fmp.state_dp_power(A, f0, x, mod)[0]

    A = [[3, -(a1+an)], [0, 1]]
    f0 = [s0, 1]
    res = fmp.state_dp_power(A, f0, y, mod)[0]
    return res

print(solve(n,x,y,mod,a))

