"""
https://codeforces.com/problemset/problem/2064/C

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) 和长为 n 的数组 a(-1e9≤a[i]≤1e9, a[i]≠0)。

每次操作，你可以选择 a 中的一个数 a[i]，得到 |a[i]| 分。
然后：
如果 a[i] < 0，移除 a[i] 及其右边的所有元素。
否则，移除 a[i] 及其左边的所有元素。
操作直到数组为空。

输出最大总得分。

-41 5 -23 62 -40 13
5 62 -40
104/107?

做出决策，第一个要移除+-
移除正数则移除左侧第一个正数，负数则移除右侧第一个负数. (因为他永远比移除内侧更优)
所以连块的正负数可以合并成一个数了，要选都选

观察上面最优选择是一个子序列，且左侧都是正数 右侧负数，从外向内
选一个负数后右侧的都会被清除 不会被再选入子序列中

前缀和分解 - 枚举分割点

贪心思路走不通

"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for _ in range(RI()):
    n, a = RI(), RILIST()

    suf = [0]*(n+1)
    for i in range(n-1, -1, -1):
        d = -a[i] if a[i] < 0 else 0
        suf[i] = suf[i+1] + d
    res = 0
    pre = 0
    for i in range(n):
        d = a[i] if a[i] > 0 else 0
        pre += d
        res = max(res, suf[i] + pre)
    print(res)
