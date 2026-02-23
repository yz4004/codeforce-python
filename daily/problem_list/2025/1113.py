"""
https://codeforces.com/problemset/problem/821/E

输入 n(1≤n≤100) 和 k(1≤k≤1e18)。
然后输入 n 条水平线段，每条线段输入 L R(0≤L<R≤1e18) Y(0≤Y≤15)，表示线段左右端点的横坐标，以及线段的纵坐标。
保证 L[1] = 0，R[i] = L[i+1]，L[n]≤k≤R[n]。
这些水平线段组成了上边界。下边界为 x 轴。

你从平面直角坐标系的原点 (0,0) 出发，目标是 (k,0)。
每一步，你可以从 (x,y) 移动到 (x+1,y-1)、(x+1,y) 或者 (x+1,y+1)。
对于第 i 条线段，你的纵坐标必须满足 0≤y≤Y[i]。
特别地，当一条线段结束、另一条线段开始时，需要同时满足两条线段的 Y 限制。

输出从 (0,0) 移动到 (k,0) 的合法方案数，模 1e9+7。

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

n,k = RII()
a = []
for _ in range(n):
    a.append(RII())

MOD = 10 ** 9 + 7


def solve(n, k, a):
    # [l, r, y]
    # [0, k]
    # f[i][j] = length-i, height-j <= 15
    # f[0][0] = 1
    # f[i][j] = f[i-1][j-1] + f[i-1][j] + …

    """
    f[m-1] = f[m-1] + f[m-2]

    f[j] = f[j+1], f[j], f[j-2]

    f[0] = f[1] + f[0]

        j
    1 1          m-1
    1 1 1
    1   1   j
    …
    1 1 0
    """

    fmp = FastMatPow()
    m = 16
    f = [0] * m
    f[0] = 1

    for idx, (l, r, y) in enumerate(a):

        # [0, y]
        if len(f) < y:
            f = f + [0] * (y - len(f))
        else:
            f = f[:y+1]

        A = [None for _ in range(y+1)]
        for j in range(y+1):
            row = [0] * m
            if j-1 >= 0:
                row[j - 1] = 1
            if j + 1 < m:
                row[j + 1] = 1
            row[j] = 1
            A[j] = row

        # [l, r] or [l, k] --
        n = r-l if r < k else k-l
        f = fmp.state_dp_power(A, f, n)

    return f[0]
print(solve(n, k, a))