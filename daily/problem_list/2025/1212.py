"""
https://www.luogu.com.cn/problem/P9474

输入 n(1≤n≤1e5) m(1≤m≤ceil(n/2)) 和长为 n 的数组 a(1≤a[i]≤1e9)，所有 a[i] 互不相同。

从 a 中选择恰好 m 个互不相邻的数，得到序列 b。
输出 max(b) - min(b) 的最小值。

5 3
1 2 3 4 5
输出 4

输入
6 3
1 7 8 3 4 6
输出 4

输入
100 43
11451 28255 11021 1888 13765 12592 30989 18758 7833 21591 15085 13547 11805 31668 23385 18266 30204 6101 22525 22939 13550 20258 21998 29574 11834 1879 21829 16600 6777 9016 18445 23687 5532 18560 4191 26195 11824 16922 10699 5790 31201 21139 506 17533 21309 2768 17554 4623 9403 30972 7770 13070 25852 17349 15263 419 10320 1480 1494 21887 27516 32073 25730 20775 31675 25640 1368 6543 8194 1040 28577 11243 26504 23282 26337 17858 16774 25522 24758 4932 16955 22304 4610 6109 14644 31017 22348 1290 31946 17999 31844 29548 3820 5462 10054 12827 32543 320 27201 8252
输出 23219

"""
from collections import defaultdict
import sys
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

# [L,R]
n, m = RII()
a = RILIST()

# 枚举r 对应max 左侧窗口对应最小值
# 给定值域区间 [l,r] 查询能否在所选定的值域区间 找到m个元素的不相临的子序列
# m个不相邻元素选取，数轴上有一些 01101 选择不相临的最长的1
# 每个连续的块可以提供 (k+1)//2 个元素. 加总即可
# 右指针的扩展引入新的1 左指针收缩伴随1的消失
# k1 1 k2  如果我知道

# 左侧把头连续1 右侧把头连续1 该区间总共

class SegmentTree:  # house rob
    def __init__(self, n, nums=None):
        self.t = [(1,0,0,0)] * (4 * n)

    ##############################################
    def pull(self, p):  # up 子信息汇总p <- 2*p, 2*p+1
        self.t[p] = self.merge(self.t[2*p], self.t[2*p+1])

    def merge(self, left_i, right_i):
        l_len, ll, lr, lt = left_i
        r_len, rl, rr, rt = right_i

        # mid = (lr+rl+1) // 2
        # total = lt + rt + mid - (lr+1)//2 - (rl+1)//2

        ans = lt + rt
        if lr > 0 and rl > 0:
            ans -= (lr+1)//2 + (rl+1)//2
            ans += (lr + rl + 1) // 2

        #print(left_i, right_i, mid, total)

        ll += rl if ll == l_len else 0
        rr += lr if rr == r_len else 0

        return l_len + r_len, ll, rr, ans

    def apply(self, p, v): # 单点更新逻辑 apply 0 or 1
        self.t[p] = 1,v,v,v
    ##############################################

    def update(self, p, l, r, i, v):
        if l == i == r:
            self.apply(p, v) # 单点更新
            return
        mid = (l + r) // 2
        if i <= mid:
            self.update(2 * p, l, mid, i, v)
        if mid < i:
            self.update(2 * p + 1, mid + 1, r, i, v)
        self.pull(p)

    def query(self, p, l, r, L, R): # 查询 [L,R] 区间最小值
        if L <= l and r <= R:
            return self.t[p]
        mid = (l + r) // 2

        if R <= mid:
            return self.query(2 * p, l, mid, L, R)
        if mid < L:
            return self.query(2 * p + 1, mid + 1, r, L, R)

        left_i = self.query(2 * p, l, mid, L, R)
        right_i= self.query(2 * p + 1, mid + 1, r, L, R)
        return self.merge(left_i, right_i)


tree = SegmentTree(n)
res = inf
b = sorted([(x,i) for i,x in enumerate(a)])
l = 0
for i in range(n):

    x,j = b[i]
    tree.update(1, 0, n-1, j,1)
    # [i-m, i]

    while tree.query(1, 0, n-1, 0, n-1)[3] >= m:
        l_min, l_idx = b[l]
        res = mn(res, x - l_min)
        tree.update(1, 0, n-1, l_idx, 0)
        l += 1
print(res if res < inf else -1)