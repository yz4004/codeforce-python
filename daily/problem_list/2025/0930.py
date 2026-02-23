"""
https://codeforces.com/problemset/problem/2075/B

输入 T(≤1e3) 表示 T 组数据。所有数据的 n 之和 ≤5000。
每组数据输入 n(2≤n≤5000) k(1≤k≤n-1) 和长为 n 的数组 a(1≤a[i]≤1e9)。

一开始，所有数都是红色的。
首先，选择 a 中的 k 个元素，涂成蓝色。
然后每次操作，选择一个有蓝色邻居的红色元素，把红色元素涂成蓝色。直到所有元素都是蓝色。

设 S = 一开始选的 k 个元素之和 + 最后一个涂成蓝色的元素值。
输出 S 的最大值。

"""
import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict, deque
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for _ in range(RI()):
    n, k = RII()
    a = RILIST()
    # 选择初始k个后，后续每次操作只选一个涂色 而不是同步扩散 所以可以控制顺序
    # k+1 我们希望 （不一定总是k+1最大的元素 需要联通扩散）
    # 1411131 k=1
    # a.sort(reverse=True)
    # print(sum(a[:k+1]))

    # 如果要扩散两侧，则 0 [1,i-1], [j+1,n-2] n-1 中间两端不可以选择 只能选把头的
    # [0, i] ... [j, n-1]

    # 枚举最后一个扩散到的，从剩下的可选域中选择最大的k个，使得这k个选取能扩散到最后一个
    # 如果是边界则剩余k任意，如果是中间，要求其左右两侧必须都有选取
    # for i,x in enumerate(a):
    #     # [:i] x [i+1:n]
    #     # x作为最后扩散的元素，前/后都保证元素的情况下，最大的k个.

    # 其实如果是k>1 则 k+1 永远可以选两头 然后往中间扩散，只有k=1 时只能选两头

    if k > 1:
        a.sort(reverse=True)
        print(sum(a[:k+1]))
    else:

        p1 = (max(a[1:n-1]) + mx(a[0], a[n-1])) if n > 2 else -inf
        p2 = a[0] + a[n-1]
        print(mx(p1, p2))


