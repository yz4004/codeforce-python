"""
https://codeforces.com/problemset/problem/2081/A

输入 T(≤1e5) 表示 T 组数据。所有数据的 n 之和 ≤1e5。
每组数据输入 n(1≤n≤1e5) 和长为 n 的字符串 s，表示一个二进制整数 x。保证最高位 s[0]=1。

每次操作，要么把 x 变成 floor(x/2)，要么把 x 变成 ceil(x/2)，概率都是 1/2。

输出把 x 变成 1 的期望操作次数，模 M=1e9+7。
设答案为既约分数 P/Q，你需要输出 P*pow(Q,M-2)%M。

"""

import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x


mod = 10 ** 9 + 7
def solve(n, s):
    # n = len(s)
    MOD = 10 ** 9 + 7
    inv2 = (MOD + 1) // 2

    f0, f1 = 0, 1  # f0=f[0][0], f1=f[0][1]
    for i in range(1, n):
        if s[i] == '0':
            nf0 = (f0 + 1) % MOD
            nf1 = ((f0 + f1) * inv2 % MOD + 1) % MOD
        else:
            nf0 = ((f0 + f1) * inv2 % MOD + 1) % MOD
            nf1 = (f1 + 1) % MOD
        f0, f1 = nf0, nf1
    return f0

    # f = [[0]*2 for _ in range(n)]
    # f[0][1] = 1
    # # f[i][0/1] 前i个字符，无/有进位的期望操作
    # # s[0,i] 操作次数
    # for i in range(1, n):
    #     if s[i] == "0":
    #         f[i][0] = f[i-1][0] + 1
    #         f[i][1] = (f[i-1][0] + f[i-1][1]) / 2 + 1
    #     else:
    #         f[i][0] = (f[i-1][0] + f[i-1][1]) / 2 + 1
    #         f[i][1] = f[i-1][1] + 1
    # return f[n-1][0]

T = RI()
for _ in range(T):
    n, s = RI(), RS() # 10110...
    print(solve(n, s))
