"""
https://codeforces.com/problemset/problem/2065/F

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤5e5。
每组数据输入 n(2≤n≤5e5) 和长为 n 的数组 a(1≤a[i]≤n)。
然后输入一棵 n 个节点的无向树的 n-1 条边。节点编号从 1 开始。节点 i 的点权为 a[i]。

对于 1 到 n 的每个整数 x，判断：
树中是否存在一条至少有两个点的简单路径，路径点权的严格众数存在且等于 x？输出 0 或者 1。
注：序列 S 的严格众数为出现次数严格大于 |S|/2 的数。

你需要输出一个长为 n 的 0-1 字符串。

- 严格众数排列到序列上，至少有 相邻两点一样/或隔点一样

"""
import sys
from collections import defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for _ in range(RI()):
    n = RI()
    a = RILIST()
    a = [x-1 for x in RILIST()]

    g = [[] for _ in range(n+1)]
    for _ in range(n-1):
        l,r = RII()
        l,r = l-1, r-1
        g[l].append(r)
        g[r].append(l)

    res = [0]*n

    # 如果是树遍历 父子/祖孙/兄弟一样 直接迭代即可 5e5递归爆栈
    for i in range(n):
        c = a[i]

        # 1 相邻
        for j in g[i]:
            if a[j] == c:
                res[c] = 1
                break

        # 2 隔点, 枚举i作为中间点时
        cnt = defaultdict(int)
        for j in g[i]:
            cnt[a[j]] += 1

        for v,c in cnt.items():
            if c > 1:
                res[v] = 1
    print("".join(map(str, res)))







