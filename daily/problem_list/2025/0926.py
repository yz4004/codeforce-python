
"""
https://codeforces.com/problemset/problem/1304/F2

输入 n(1≤n≤50) m(1≤m≤2e4) k(1≤k≤m) 和 n 行 m 列的矩阵，元素范围 [0,1e3]。

用 n 个 2 行 k 列的矩形覆盖矩阵。
要求每行恰好包含一个矩形的第一行，不能有两个矩形的第一行都在同一行。
特别地，第 n 行的矩形出界了，出界的部分不算。相当于一个 1 行 k 列的矩形。

输出被至少一个矩形覆盖的元素之和的最大值。

4 4 0 6 5
4 4 0 0 1
0 0 0 5 5
9 9 0 0 0

f[i][j] = max(f[i][j], f[i-1][l] + area(i,j) - overlap(i,l,j)
overlap 是第i行的  [l,l+k-1],[j,j+k-1] 而且我们这里单侧更新 (先左后右)

max(f[i-1][l] - overlap(i,l,j) for l in range(j))


"""
import itertools
import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict, deque
# from collections import Counter, defaultdict
# from typing import List
# from math import inf
# from sortedcontainers import SortedList

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

n, m, k = RII()
mat = [RILIST() for _ in range(n)]

# f[i][j]
# 暴力做法 i代表上一行 [i,i+k) j代表当前行[j,j+k) 扣掉重叠的覆盖面积，枚举50行 n*m^2

ps = []
for r in mat:
    ps.append(list(itertools.accumulate(r, initial=0)))
ps.append([0]*(m+1))

# [l,r]
get_row = lambda i,l,r: ps[i][r+1] - ps[i][l]


# [0, m-k] [i,i+k)
# get_area = lambda i,j: ps[i][j+k] - ps[i][j] + ps[i+1][j+k] - ps[i+1][j]
get_area = lambda i,j: get_row(i,j,j+k-1) + get_row(i+1,j,j+k-1)

f = [get_area(0,j) for j in range(m-k+1)]
for i in range(1, n):


    # 1. p+k <= j 维持max left
    # [p, p+k)
    #        [j, j+k)

    # left_max + area(i,j)

    # 2. p+k > j
    #   [p, p+k) .. |
    #        [j, j+k)

    # 不用area - overlap.
    # i 行继承 - f[i-1][p]
    # i 行新增 - s[i][j+k] - s[i][p+k]  随着p向右减小
    # i+1     - row[i+1][j,j+k]        对j固定

    # f[i-1][p] + (s[i][j+k] - s[i][p+k]) 没有单调性
    # ij 可以理解为 【i-1,p 的2行矩形面积】 + 【 i行[p+k,j+k) 未重叠部分】.

    # 所有和 j,j+k 重叠的方块，向左未重叠面积大，但是2行矩形面积可能小

    # max(f[i-1][p] + s[i][j+k] - s[i][p+k] for p, p+k > j)

    # f[i-1][p] - s[i][p+k]

    g = [0]*(m-k+1)

    q = deque()
    left_max = 0
    for j in range(m-k+1):
        if j >= k:
            left_max = mx(left_max, f[j-k])

        # [j,j+k)
        while q and q[0][0]+k-1 < j:
            q.popleft()

        t = f[j] - ps[i][j+k]
        while q and q[-1][1] <= t:
            q.pop()
        q.append((j, t))

        cur = q[0][1] + ps[i][j+k] + (ps[i+1][j+k] - ps[i+1][j])
        area = (ps[i][j + k] - ps[i][j]) + (ps[i + 1][j + k] - ps[i + 1][j])
        g[j] = mx(left_max + area, cur)
        #print((i,j), left_max, area, cur)



    q = deque()
    right_max = 0
    for j in range(m-k, -1, -1):
        # [j, j+k)
        if j + k < m-k+1:
            right_max = mx(right_max, f[j+k])

        #      [p,p+k)
        # [j,j+k)
        # f[i][j] = max(f[i-1][p] + [i][j,p)) = max(f[i-1][p] + ps[i][p] - ps[i][j])
        while q and j+k-1 < q[0][0]:
            q.popleft()

        t = f[j] + ps[i][j]
        while q and q[-1][1] <= t:
            q.pop()
        q.append((j, t))

        cur = q[0][1] - ps[i][j] + (ps[i + 1][j + k] - ps[i + 1][j])
        area = (ps[i][j + k] - ps[i][j]) + (ps[i + 1][j + k] - ps[i + 1][j])

        g[j] = mx(g[j], mx(right_max + area, cur))

    f = g
print(max(f))



########################
f = [get_area(0,i) for i in range(m-k+1)]
for i in range(1, n):

    g = [0]*(m-k+1)
    for j in range(m-k+1):

        area = get_area(i,j)
        for l in range(m-k+1):
            # [l,l+k-1] [j,j+k-1]

            overlap = 0
            if j <= l+k-1 <= j+k-1:
                overlap = get_row(i, j, l+k-1)
            elif j <= l <= j+k-1:
                overlap = get_row(i, l, j+k-1)

            g[j] = mx(g[j], f[l] + area - overlap)
    f = g
print(max(f))