"""
https://codeforces.com/problemset/problem/2161/D

输入 T(≤6e4) 表示 T 组数据。所有数据的 n 之和 ≤3e5。
每组数据输入 n(1≤n≤3e5) 和长为 n 的数组 a(1≤a[i]≤n)。

删除 a 中的一些元素，得到数组 b。
要求 b 满足：不存在 i < j 且 b[j] - b[i] = 1 的下标对 (i, j)。

最少要删多少个数？
"""
import itertools
import sys
from bisect import bisect_left
from collections import defaultdict
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

def solve(n, a):
    # f[x][i] 保留 x [,i] 其中x最右侧的index是i -- 得到的 <=x 的最长序列 (n-即为最小删除)
    # 需要删掉 [0,i) 内的 x-1. 加上 [0,i] 内的x
    # 对于大于 i 的 x-1 可以保留. 即从 max(f[x-1][j] > 0 转移过来)
    # f[x][i]

    keys = set()
    posi = [None]*(n+1)
    for i,x in enumerate(a):
        if posi[x] is None:
            posi[x] = []
            keys.add(x)
        posi[x].append(i)

    keys = sorted(list(keys))

    pre_x2 = 0
    f = []
    for cnt,i in enumerate(posi[keys[0]], 1):
        f.append((i, cnt))

    for i in range(1, len(keys)):
        x = keys[i]
        pos = posi[x]
        m = len(pos)

        #print(x,f, pre_x2)

        g = []
        if keys[i-1] < x-1:
            pre_x2 = max(max(y for _,y in f), pre_x2)
            for j,pj in enumerate(pos):
                cnt = j+1
                g.append((pj, pre_x2 + cnt))

        else:

            k = len(f)-1

            pre = -inf

            for j in range(m-1, -1, -1):
                pj = pos[j]
                while k >= 0 and f[k][0] > pj:
                    if pre == -inf or f[k][1] > pre:
                        pre = f[k][1]
                    k -= 1

                cnt = (j+1) - (k+1) # [0,pj] 保留的 x - [0,pj] 移除的 x-1
                # cnt_x = (j+1)
                # cnt_x1 = (k+1)
                g.append((pj, max(pre_x2 + j+1, pre + cnt)))

                #print((j,pj), k, (pre_x2, cnt), g[::-1])

            pre_x2 = max(pre_x2, max(y for _, y in f))

            g = g[::-1]
        f = g

    return n - max(pre_x2, max(y for _,y in f))






for _ in range(RI()):
    n, a = RI(), RILIST()
    print(solve(n, a))
    # print()