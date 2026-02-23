"""
https://www.luogu.com.cn/problem/P1712

输入 n m(1≤m≤n≤5e5) 和 n 个闭区间，数据范围 $[0,1e9]$。

从这 n 个区间中，选择 m 个区间，要求这 m 个区间的交集不为空。
输出这 m 个区间的「最大区间长度减去最小区间长度」的最小值。无解输出 -1。
注：区间长度为右端点减去左端点。

[a1 ... at]

"""
from bisect import bisect_left
from collections import defaultdict, deque
from sortedcontainers import SortedList
from functools import cache
from math import comb, factorial, inf
import sys
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

class SegmentTreeSum:  # sum
    def __init__(self, n):
        self.t = [0] * (4 * n)  # 维护的区间信息, 区间最小值对应初始值inf，可替换为更复杂的信息 （如打家劫舍）
        self.tag = [0] * (4 * n)

    def pull(self, p):  # up
        # 子信息汇总p <- 2*p, 2*p+1
        self.t[p] = mx(self.t[2 * p], self.t[2 * p + 1])

    def push(self, p, l, r):  # down 通知树节点p 下发懒信息
        if self.tag[p]:
            v = self.tag[p]
            self.apply(2 * p, l, (l + r) // 2, v)         # 懒信息推给左
            self.apply(2 * p + 1, (l + r) // 2 + 1, r, v) # 懒信息推给右
            self.tag[p] = 0 # 清空暂存的懒信息，已经下发
            # 当有update操作自上而下准备更新区间p之前，先下发之前p暂存的懒信息 （本例懒信息只是要加的数值）

    def apply(self, p, l, r, v):  # 下发lazy信息，先更新节点信息，然后暂存懒信息，（不继续下发）
        self.t[p] += v
        self.tag[p] += v
    #######################################

    def add(self, p, l, r, L, R, v):
        # (p,l,r) [L, R] += v - 支持负数=减法
        if L <= l and r <= R: # 当(p,l,r) 为 [L, R] 子区间即停止递归，利用懒信息下发函数更新（不要递归到空，否则失去懒更新意义)
            self.apply(p, l, r, v)
            return
        mid = (l + r) // 2
        self.push(p, l, r) #递归左右之前，先分发懒信息
        if L <= mid:
            self.add(2 * p, l, mid, L, R, v)
        if mid < R:
            self.add(2 * p + 1, mid + 1, r, L, R, v)
        self.pull(p)

    def query(self, p, l, r, L, R):
        if L <= l and r <= R:
            return self.t[p]
        res = 0
        mid = (l + r) // 2
        self.push(p, l, r)
        if L <= mid:
            res = mx(res, self.query(2 * p, l, mid, L, R))
        if mid < R:
            res += mx(res, self.query(2 * p + 1, mid + 1, r, L, R))
        return res

n, m = RII()
a = [tuple(RII()) for _ in range(n)]

keys = sorted(list(set(x for t in a for x in t)))
a = sorted(a, key=lambda x: x[1]-x[0])

N = len(keys)
tree = SegmentTreeSum(N)

res = inf
j = 0
b = [None]*n
for i, (x,y) in enumerate(a):
    l,r = bisect_left(keys, x), bisect_left(keys, y)
    b[i] = (l,r, y-x+1)

    # 已有的区间重合？
    # [l,r] + 1
    tree.add(1, 0, N-1, l, r, 1)

    while tree.query(1, 0, N-1, 0, N-1) >= m:
        l, r, d = b[j]
        tree.add(1, 0, N-1, l, r, -1)
        res = mn(res, y-x+1 - d)
        j += 1
print(res)



# sys.exit(0)
#
# keys = []
# for x,y in a:
#     l = y - x + 1
#     keys.append((x,0,l))
#     keys.append((y,1,l))
#
# keys.sort()
# sl = SortedList()
# res = inf
# for _,ty,l in keys:
#     if ty == 0:
#         j = bisect_left(sl, l) # >= l
#         # [j, j+m) 所有这些值作为mx时，随着l的插入，原本对应 (k-m+1, k) 现在对应 (k-m+2, k)
#         # sl.add(l)
#         # if len(sl) >= m:
#         #     j = bisect_left(sl, l)
#         pass
#     else:
#         sl.remove(l)
#
#
