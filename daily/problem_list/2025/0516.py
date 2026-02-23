"""
https://codeforces.com/problemset/problem/1701/E

输入 T(≤5000) 表示 T 组数据。所有数据的 n 之和 ≤5000。
每组数据输入 n m(1≤m≤n≤5000)，长为 n 的字符串 s 和长为 m 的字符串 t，只包含小写英文字母。

文本编辑器中有一个字符串 s，现在光标在 s 末尾字母的右侧。
有五个按键，功能与电脑键盘一致：
1. ←：光标向左移动一位。
2. →：光标向右移动一位。
3. Home：光标移到 s 首字母的左侧。
4. End：光标移到 s 末尾字母的右侧。
5. Backspace：删除光标左侧相邻字母。

输出把 s 变成 t 的最少按键次数（操作次数）。
如果无法做到，输出 -1。（注意我们只能删除字母，不能添加字母）

提示 f[i][j][k=0/1/2]
a[j]−j>a[i]−i.
(a[j]−j)> min (a[i]−i)
"""
import sys, random
from collections import defaultdict, deque
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

def solve(s, t):
    n, m = len(s), len(t)

    pre = [[inf]*(m+1) for _ in range(n+1)] # pre[i][j] -- s[:i] t[:j] 从前往后使s变成t的最小操作
    pre[0][0] = 0
    for i in range(1, n + 1):
        pre[i][0] = 2*i
        for j in range(1, m + 1):
            # s[:i]  t[:j]
            if s[i-1] != t[j-1]:
                pre[i][j] = pre[i-1][j] + 2
            else:
                pre[i][j] = mn(pre[i-1][j-1]+1, pre[i-1][j]+2)

    if pre[n][m] == inf:
        return -1
    # suf[i][j] 从后往前 s[i:] t[j:] 使得后缀一致的最小操作

    suf = [[inf]*(m+1) for _ in range(n+1)] # pre[i][j] -- s[:i] t[:j] 从前往后使s变成t的最小操作
    suf[n][m] = 0
    for i in range(n-1, -1, -1):
        # suf[i][m] - s[i:n] t[m:]
        suf[i][m] = n-i
        for j in range(m-1, -1, -1):
            # s[i:]  t[j:]
            if s[i] != t[j]:
                suf[i][j] = suf[i+1][j] + 1
            else:
                suf[i][j] = mn(suf[i+1][j+1], suf[i+1][j]) + 1

    # s[i:j]
    # t[a:b] ?
    # lcp[i][j] = lcp(s[i:], t[j:])
    lcp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n-1, -1, -1):
        for j in range(m-1, -1, -1):
            if s[i] == t[j]:
                lcp[i][j] = lcp[i+1][j+1] + 1

    res = inf
    for i in range(n):
        for j in range(m):
            # s[:i] t[:j] 交给pre处理
            a = pre[i][j]
            l = lcp[i][j]
            b = suf[i+l][j+l] if i+l <= n and j+l <= m else 0
            d = 0 if i == 0 and j == 0 else 1
            res = mn(res, a + b + d)

    return res

T = RI()
for _ in range(T):
    n, m = RII()
    s, t = RS(), RS()
    print(solve(s, t))






