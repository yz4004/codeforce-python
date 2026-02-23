"""
https://codeforces.com/problemset/problem/1580/B

输入 n(1≤n≤100) m(1≤m≤n) k(1≤k≤n) mod(1≤mod≤1e9)。

对于数组 A 的所有包含 A[i] 的连续子数组 B，把 max(B) 记录到集合 S 中，如果 |S| = m，也就是恰好有 m 个不同的 max(B)，则称 A[i] 是好数。

输出有多少个 1~n 的排列 A，满足 A 中恰好有 k 个好数。
答案模 mod。

"""
from functools import cache
from math import comb, factorial
import sys
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x



# def dfs(n, k, m):
#     # n节点树 深度为m的节点恰好有k个

n, m, k, mod = RII()
# @cache
# def dfs(n, m):
#     f = [0]*(k+1)  # f[i] 深度为m-1的节点数量恰好为i个的数量
#     # if n < m:
#     #     return [0]*(n+1)
#     # if n == m:
#     #     f[m-1] = 1
#     #     return f
#
#     # c(n,1) * c(n-1, i)
#     for i in range(n):
#         # 左边i个点, 深度为m-1的点 恰好有 tl [0...k]
#         tl, tr = dfs(i, m-1), dfs(n - 1 - i, m-1)
#         for j in range(1, k+1):
#             f[j] = sum(tl[o] * tr[j-o] for o in range(0, k+1)) * n * comb(n-1, i)
#     return f

C = [[0]*(n+1) for _ in range(n+1)]
C[0][0] = 1
for i in range(1, n+1):
    C[i][0] = 1
    for j in range(i+1):
        C[i][j] = (C[i-1][j] + C[i-1][j-1]) % mod

def comb(n,k):
    return C[n][k]

fac = [1]*(n+1)
for i in range(1, n+1):
    fac[i] = fac[i-1] * i % mod

# dp[d][s][t] := dep=d (还剩 d 层到 m-1)、size=s 时恰有 t 个好节点的方案数
dp = [ [ [0]*(k+1) for _ in range(n+1) ] for __ in range(m) ]

# base: d=0 时，只有根是好节点
# dp[0][s][1] = s!  （只有 t==1 时合法）

for s in range(n+1):
    dp[0][s][1] = fac[s]
    # dp[0][s][t!=1] 默认就是 0

# 依次往上“填表” d=1,2,...,m-1
for d in range(1, m):
    for s in range(1, n+1):
        # 枚举左右子树大小
        for left_sz in range(s):
            right_sz = s-1-left_sz
            c = C[s-1][left_sz]
            # 合并左右的“好节点”个数
            # 同时根不再是好节点，所以 root_contrib=0
            for left_need in range(0, min(left_sz, k)+1):
                if dp[d-1][left_sz][left_need] == 0:
                    continue
                # 剩余给右子树
                max_r = min(right_sz, k-left_need)
                for right_need in range(0, max_r+1):
                    dp[d][s][left_need+right_need] = (
                        dp[d][s][left_need+right_need]
                        + c * dp[d-1][left_sz][left_need] * dp[d-1][right_sz][right_need]
                    ) % mod
print(dp)
print(dp[m-1][n][k])


@cache
def dfs(n, m, t): # 深度为m的节点数量恰好为t个的数量
    if n == 0:
        return 1 if t == 0 else 0

    if m == 0:
        # 根节点应该是唯一一个所需的，其余自由排列 t=0
        return fac[n] if t == 1 else 0

    res = 0
    for i in range(n):
        for j in range(0, t+1):
            if j > i or t-j > n-1-i:
                continue
            left = dfs(i, m-1, j)
            right = dfs(n - 1 - i, m-1, t - j) # 左侧 i个提供j个恰好，右侧n-1-i提供 t-j个
            res += comb(n-1, i) * left * right # 不需要乘n -- 大根树
    return res % mod
res = dfs(n, m-1, k)
print(res)



