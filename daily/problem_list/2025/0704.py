"""
https://codeforces.com/problemset/problem/526/E

输入 n(2≤n≤1e6) q(1≤q≤50) 和长为 n 的数组 a(1≤a[i]≤1e9)。
然后输入 q 个询问，每个询问输入 b(max(a)≤b≤1e15)。

a 是一个环形数组。
对于每个询问，输出：把 a 分成若干段，每段元素和不超过 b，最少要分多少段？

"""
import itertools
import sys
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x


n, q = RII()
nums = RILIST()
ps = list(itertools.accumulate(nums, initial=0))
g = [0]*n
f = [[0,0] for _ in range(n+1)] # f[i] 前i个切了多少刀

for _ in range(q):
    b = RI()

    for i in range(1, n):
        l = g[i-1]
        # [l,i-1] i]
        s = ps[i+1] - ps[l]
        while s > b:
            s -= nums[l]
            l += 1
        g[i] = l

    # [:k] < b
    # [i:j]
    # print(g)
    res = inf
    for i in range(n):
        # [j, i] 是最大窗口 <= b
        j = g[i]
        f[i+1][0] = f[j][0] + 1

        if j == 0:
            f[i+1][1] = ps[i+1]
        elif j > 0:
            f[i + 1][1] = f[j][1]

        if i < n-1 and ps[n] - ps[i+1] <= b:
            can_merge = f[i + 1][1] + ps[n] - ps[i+1] <= b
            res = mn(res, f[i+1][0] + 1 - can_merge)

            # print(i, nums[:i+1], j, nums[j:i+1])
            # print(f[:i+2], res)
            # print()

    res = mn(res, f[n][0])
    print(res)

