"""
https://codeforces.com/problemset/problem/1982/C

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤1e5) L R(1≤L≤R≤1e9) 和长为 n 的数组 a(1≤a[i]≤1e9)。

每次操作，删除 a 的一个非空前缀。
如果该次操作删除的元素之和在闭区间 [L,R] 中，那么得到一分，否则不得分。
操作直到 a 为空。

输出最大总得分。

[:i] -- [L,R]

"""
import itertools
import sys
from bisect import bisect_left
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

class SegmentTreeMax:  # max 支持区间修改(值覆盖)
    def __init__(self, n, nums=None):
        self.n = n
        if nums:  # 如果有初始化数组输入，执行build逻辑
            assert n == len(nums)
            self.nums = nums
            self.t = [-inf] * (4 * n)  # 区间信息，区间最小值对应初始值inf，可替换为更复杂的信息 （如打家劫舍）
            self.tag = [0] * (4 * n)  # 懒信息
            self.build(1, 0, n - 1)  # 初始化build
        else:
            self.t = [-inf] * (4 * n)  # 维护的区间信息, 区间最小值对应初始值inf，可替换为更复杂的信息 （如打家劫舍）
            self.tag = [0] * (4 * n)  # 懒信息

    def build(self, p, l, r):
        # (p,l,r) parent 以及管辖区间
        if l == r:
            self.t[p] = self.nums[l]
            return
        mid = (l + r) // 2
        self.build(2 * p, l, mid)
        self.build(2 * p + 1, mid + 1, r)
        self.pull(p)

    ########################################
    def pull(self, p):  # up/子信息汇总p <- 2*p, 2*p+1
        self.t[p] = max(self.t[2 * p], self.t[2 * p + 1])  # 更新min

    def push(self, p, l, r):  # down 通知树节点p 下发懒信息
        if self.tag[p]:
            v = self.tag[p]
            self.apply(2 * p, l, (l + r) // 2, v)  # 懒信息推给左
            self.apply(2 * p + 1, (l + r) // 2 + 1, r, v)  # 懒信息推给右
            self.tag[p] = 0  # 清空暂存的懒信息，已经下发
            # 当有update操作自上而下准备更新区间p之前，先下发之前p暂存的懒信息 （本例懒信息只是要加的数值）

    def apply(self, p, l, r, v):  # 下发lazy信息，先更新节点信息，然后暂存懒信息，（不继续下发）
        # self.t[p] = max(self.t[p], v) 如何应用懒信息，取min是区间应用值，但不覆盖原值
        self.t[p] = v  # 直接区间覆盖值，适用本题，直接覆盖inf
        self.tag[p] = v
    ########################################

    def update(self, p, l, r, L, R, v):
        if L <= l and r <= R:  # 当(p,l,r) 为 [L, R] 子区间即停止递归，利用懒信息下发函数更新（不要递归到空，否则失去懒更新意义)
            self.apply(p, l, r, v)
            return
        mid = (l + r) // 2
        self.push(p, l, r)  # 递归左右之前，先分发懒信息
        if L <= mid:
            self.update(2 * p, l, mid, L, R, v)
        if mid < R:
            self.update(2 * p + 1, mid + 1, r, L, R, v)
        self.pull(p)

    def query(self, p, l, r, L, R):
        if L <= l and r <= R:
            return self.t[p]
        res = -inf
        mid = (l + r) // 2
        self.push(p, l, r)  # 递归左右之前，先分发懒信息，虽然不会更新，但查询部分左右区间也依赖本层懒信息
        if L <= mid:
            res = max(res, self.query(2 * p, l, mid, L, R))
        if mid < R:
            res = max(res, self.query(2 * p + 1, mid + 1, r, L, R))
        return res

    def update_single(self, i, v): # 仍然走区间更新逻辑
        # 将nums[i]覆盖为v
        n = self.n
        self.update(1, 0, n-1, i, i, v)



for _ in range(RI()):
    n, L, R = RII()
    a = RILIST()

    def solve0(n, L, R, a):
        g = [-1] * n
        s = 0
        l = 0
        for i in range(n):
            s += a[i]
            while s >= L:
                s -= a[l]
                l += 1

            if L <= s + a[l - 1] <= R:
                g[i] = l - 1  # [l,i]

        res = 0
        f = [0] * (n + 1)
        for i in range(n):
            f[i + 1] = f[i]
            pre = g[i]  # [pre,i]
            if pre > -1 and f[pre] + 1 > f[i + 1]:
                f[i + 1] = f[pre] + 1
        return f[n]

    def solve1(n, L, R, a):
        s = 0
        l = 0
        pre = -1
        res = 0
        for i in range(n):
            s += a[i]
            while s >= L:
                s -= a[l]
                l += 1

            if L<=s + a[l-1] <=R:
                # g[i] = l-1 # [l,i]
                if pre < l-1:
                    pre = i
                    res += 1
        return res

    def solve2(n, L, R, a):
        s = 0
        l = 0
        pre = -2
        res = 0
        # from sortedcontainers import SortedList
        # sl = SortedList()

        ps = list(itertools.accumulate(a,initial=0))
        tmp = sorted(list(set(ps)))

        m = len(tmp)
        tree = SegmentTreeMax(m)

        idx0 = bisect_left(tmp, 0)
        tree.update_single(idx0, 0)

        for i,x in enumerate(a):
            s += x
            # t=[l,i] L,R  s-t - [s-R,s-L]
            # 希望s-t前缀和越靠右越好，在全正数的情况下 这个是单调的
            # 如果有负数，前缀和不单调
            tl = s - R
            tr = s - L
            # 搜索在这个范围内最靠右的端点 [tl, tr]

            il = bisect_left(tmp, tl)
            ir = bisect_left(tmp, tr+1)-1
            # [il, ir]

            if 0 <= il <= ir:
                l = tree.query(1, 0, m-1, il, ir)

                if pre < l:
                    res += 1
                    pre = i

            si = bisect_left(tmp, s)
            tree.update_single(si, i+1)  # si] i

        return res

    # print(solve0(n, L, R, a))
    print(solve1(n, L, R, a))
    #print(solve2(n, L, R, a))

