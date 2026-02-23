"""
https://codeforces.com/problemset/problem/2126/D

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤1e5。
每组数据输入 n(1≤n≤1e5) k(0≤k≤1e9)，分别表示赌场的个数，你的初始钱数。
然后输入 n 个赌场的信息，每个赌场输入 L R real (0≤L≤real≤R≤1e9)。

对于每个赌场，如果你的钱数 k 在 [L,R] 中，则可以更新 k 为 real。
你可以按任何顺序进入赌场，不需要进入所有的赌场，每个赌场只能进入一次。

输出你最终的最大钱数。

注意real小于R，所以初始k 回退到更小的real没有意义
"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7


for _ in range(RI()):
    n, k = RII()
    casinos = []

    for i in range(n):
        L,R,real = RII()
        if k < real :
            casinos.append((L, real))

    # casinos.sort(key=lambda c:c[-1])
    casinos.sort()
    for l,real in casinos:
        # [l, real]
        if l <= k < real:
            k = real

    print(k)





