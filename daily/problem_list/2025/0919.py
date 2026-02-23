"""
https://codeforces.com/problemset/problem/1221/F

输入 n(1≤n≤5e5)，在平面直角坐标系上有 n 个坐标点。
每个坐标点输入三个整数 x y(0≤x,y≤1e9) c(-1e6≤c≤1e6)，表示横纵坐标，以及这个点的分数。

定义特殊正方形为平行于坐标轴的正方形，且正方形的左下角和右上角都在直线 y=x 上。
你需要用一个特殊正方形去覆盖点。得分为覆盖的点的 c 之和，减去特殊正方形的边长。
特殊正方形的边长可以是 0。

输出两行：
第一行，输出最大得分。
第二行，输出特殊正方形的左下角横纵坐标，右上角横纵坐标，坐标范围必须在 [0,2e9] 中。多解输出任意解。

c1+...ck - d

https://chatgpt.com/c/68ccf7e5-7e98-8332-86e6-3f5b82f042da


"""
import sys
from bisect import bisect_left, bisect_right
# from collections import Counter, defaultdict
# from typing import List
from math import inf
# from sortedcontainers import SortedList

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7


class SegmentTree:
    def __init__(self, n, xs):
        self.n = n
        self.t = [-inf] * (4 * n)
        self.pos = [0] * (4 * n)
        self.tag = [0] * (4 * n)  # 懒信息

        self.build(1, 0, n-1, xs)

    def build(self, p, l, r, xs):
        # (p,l,r) parent 以及管辖区间
        if l == r:
            self.t[p] = xs[l]
            self.pos[p] = l
            return
        mid = (l + r) // 2
        self.build(2 * p, l, mid, xs)
        self.build(2 * p + 1, mid + 1, r, xs)
        self.pull(p)

    ########################################
    def pull(self, p):  # up/子信息汇总p <- 2*p, 2*p+1
        lc, rc = 2*p, 2*p+1
        if self.t[lc] >= self.t[rc]:
            self.t[p], self.pos[p] = self.t[lc], self.pos[lc]
        else:
            self.t[p], self.pos[p] = self.t[rc], self.pos[rc]

    def push(self, p, l, r):  # down 通知树节点p 下发懒信息
        if self.tag[p]:
            c = self.tag[p]
            self.apply(2 * p, c)  # 懒信息推给左
            self.apply(2 * p + 1, c)  # 懒信息推给右
            self.tag[p] = 0

    def apply(self, p, c):  # 下发lazy信息，先更新节点信息，然后暂存懒信息，（不继续下发）
        self.t[p] += c
        self.tag[p] += c
    ########################################

    def update(self, p, l, r, i, c):
        # 对前缀 [0..i] 做区间加 c
        if i < l:
            return
        if r <= i:
            self.apply(p, c)
            return
        self.push(p, l, r)
        mid = (l + r) // 2
        self.update(2 * p, l, mid, i, c)  # 左儿子整段都在前缀内或部分在内——必须递归
        self.update(2 * p + 1, mid + 1, r, i, c)  # 右儿子也要递归；谁整段在内会在下一层触发 r<=i
        self.pull(p)

    def query(self, p, l, r, R): #查询前缀 [,R] 最大维护值和对应坐标x
        if R < l:
            return -inf, -1

        if r <= R:
            return self.t[p], self.pos[p]

        self.push(p, l, r)
        mid = (l + r) // 2
        L = self.query(2 * p, l, mid, R)
        Rv = self.query(2 * p + 1, mid + 1, r, R)
        return L if L[0] >= Rv[0] else Rv


n = RI()
pts = []
for _ in range(n):
    x, y, c = RII()
    a, b = mn(x,y), mx(x,y)
    pts.append((a,b,c))

pts.sort(key=lambda x:x[1])

xs = sorted(list(set(p[0] for p in pts)))
ys = sorted(list(set(p[1] for p in pts)))
i = 0
m = len(xs)
tree = SegmentTree(m, xs)

# 在读完 pts 之后、建树之前
M = min(2_000_000_000, max(max(x, y) for x, y, _ in pts) + 1)
best = 0
best_t = best_s = M

for y in ys:
    while i < len(pts) and pts[i][1] <= y:
        x, _, c = pts[i]
        a = bisect_left(xs, x)
        tree.update(1, 0, m-1, a, c)
        i += 1

    # [x,y] -> sum(c) - y + x
    # y 固定，即搜索 max sum(c)+x where c/(a,b,c) a >= x

    # 搜索 [l,r] 折半后即维护 [l,mid] [mid+1,r] 的两个max, 以及取到max的对应x正方形左侧
    # 维护，(x,c) 加入. 对所有 [0.x] += c

    # 初始化 sum(c) + x where (a,b,c) a >= x, b <= y. x要初始化

    # 只允许 t <= s
    lim = bisect_right(xs, y) - 1
    if lim >= 0:
        val, idx = tree.query(1, 0, m-1, lim)    # 取 f(t) 的最大值
        cur = val - y                    # 减去边长 y
        #print(pts[:i], (cur, xs[idx]), (best, (best_t, best_s)))
        if cur >= best:
            best = cur
            best_t, best_s = xs[idx], y

if best < 0:         # 不取任何点，边长 0
    M = min(2_000_000_000, max(max(x, y) for x, y, _ in pts) + 1)
    print(0)
    print(M, M, M, M)
else:
    print(best)
    print(best_t, best_t, best_s, best_s)

