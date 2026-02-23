"""
https://codeforces.com/problemset/problem/691/E

输入 n(1≤n≤100) k(1≤k≤1e18) 和长为 n 的数组 a(0≤a[i]≤1e18)。

构造一个长为 k 的数组 b，每个 b[i] 都等于 a 中的某个数，且对于 b 中任意相邻元素 (x,y)，都满足 x XOR y 中的 1 的个数是 3 的倍数。

输出有多少个不同的数组 b，模 1e9+7。
注意：即使元素值相同，但选自 a 的位置不同，也算不同的 b。例如 a=[1,1]，k=1，有两个不同的 b=[1]。

https://chatgpt.com/c/68e72e75-44ac-8332-b518-c28cf7e8d742

15 1 2 4 8
- 允许 (x,x) 则 (x,y) 每个x可选所有 cnt_x 个任意
- 则变成状态机，考虑当前y. f[y] 当前以y结尾 “按值类聚合”的状态是
    前一个元素 xi 要使得 xi^y.bit_count() % 3 = 0

    f[y] = f[x1]*cnt_y + ... f[xj]*cnt_y
    where xi^y.bit_count()
    注意cnt记录在前一个状态到当前的转移中，当前 f[y] 不能擅自乘以 cnt_y

    则处理列向量 f = [f[x1] f[x2] ...] 得到递推线性矩阵 -- 快速幂

    f0 * A = f1
    f1 * A = f2
    ...
    fn-2 * A = fn-1

15 1 2 4 8

1 1 1 1 1   15
1 1 0 0 0   1
1 0 1 0 0   2
1 0 0 1 0   4
1 0 0 0 1   8

"""
import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict, deque, Counter
from math import inf, gcd, comb

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

n, k = RII()
a = RILIST()

a = [(x,c) for x,c in Counter(a).items()]
keys = [x for x, _ in a]

# f[x] = f[x1]*c1 + f[x2]*c2 ...
# x1 ^ x
# c1 = cnt(x1)

m = len(keys)
A = [[0]*m for _ in range(m)]
for i, x in enumerate(keys):
    A[i][i] = a[i][1]
    for j in range(i):
        y = keys[j]
        if (x^y).bit_count() % 3 == 0:
            # A[i] = [...] * f = f[i]
            # 第i行对应 f[i] 值i的聚类. 每个前面能构成的 j (j,i) 计入的乘数是 i的count
            A[i][j] = a[i][1]
            A[j][i] = a[j][1]

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

    @staticmethod
    def state_dp_power(A, init_state, n):
        # s_{i+1} = A * s_i
        # s0 = init_state（列向量），返回 s_steps。
        # S0 ... Sn
        # A * S0 = S1
        # A^n * S0 = Sn

        # 列向量 k×1
        f0 = init_state

        # Sn = A^n * S0
        M = FastMatPow.mat_pow(A, n)  # A^n = M
        S = FastMatPow.mat_vec(M, f0)  # Sn = A^n * S0 = M * s0
        return S


fmp = FastMatPow()
mod = 10 ** 9 + 7
f0 = [y for _, y in a] # f0 是每个独特y的count
f = fmp.state_dp_power(A, f0, k-1) # f0 * A^k-1 = fk-1.  f0 * A = f1

res = 0
for y in f:
    res = (res + y) % mod
print(res)
