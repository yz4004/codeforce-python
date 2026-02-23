"""
https://codeforces.com/problemset/problem/1030/F

输入 n(1≤n≤2e5) q(1≤q≤2e5) 和长为 n 的数组 a(1≤a[i]≤1e9)，长为 n 的数组 w(1≤w[i]≤1e9)。
保证 a 是严格递增数组。

数轴上有 n 个物品，第 i 个物品的位置是 a[i]，权重为 w[i]。
定义 f(L,R) 表示把下标 [L,R] 中的物品排在一起且位置连续的最小带权距离和。
比如三个物品的位置分别为 1,3,7，若把物品分别移动到 4,5,6，则带权距离和为 |4-1|*w[1] + |5-3|*w[2] + |6-7|*w[3]。

然后输入 q 个询问，每个询问包含两个数，格式如下：
"i newW"：把 w[i] 改成 newW(1≤newW[i]≤1e9)。数组下标从 1 到 n。
"L R"：输出 f(L,R) % (1e9+7)。其中 1≤L≤R≤n。

用输入的第一个数区分这两种询问：
如果第一个数是负数，表示第一种询问。把第一个数取反，就是正确的 i。
如果第一个数是正数，表示第二种询问。

a1 ... ak

al...ar

(al+1 - al) * wl+1 ... (ar - al) * wr
= sum(ai * wi for i in [l,r]) - al * sum(wi for i in [l,r])


带权中位数 - 考虑权重和的一半
    https://leetcode.cn/problems/minimum-cost-to-make-array-equal
    两种视角：贪心移动/将权重视为计数
    1贪心移动一个单位 前面的权重每次增加，后面的权重每次减小 +(w1...wi) -(wi+1...wn)
    则最优是


移动到中位数 - 但槽位有容量限制
    最优是中位数 但其余人要逐步往两边排，一共k个数，现在要将k-1个数沿中位展开
    一边放 d=(k-1)//2, 一边 k-1-d

集中排列
al ... ar
m, m+1 ... m+r-l

每个人的移动距离是如下 （省略绝对值, 只关注每个term）
al-m, al+1 - m-1, ... al+k - m-k ...

al-m, (al+1 -1)-m ... (al+k -k)-m
做变换 bi=ai-i 则问题转化为对 bl...br 找中位m

选中 [l,r]

al - c, al+1 - c - 1, ... al+k - c - k ...

考虑变换 ai+ (i-l) 则上述相当于 bi=ai - (i-l) 进行一次中位数贪心

有权重时
al - c, al+1 - c - 1, ... al+k - c - k ...
wl      wl+1              wl+k
就当对bl...br 带权中位数

al - c, al+1 - c - 1, ... al+k - c - k ...

bi = ai-i 求变换，最后

bl - c - l, bl+1 - c - l, ... bl+k - c - l ...
wl          wl+1              wl+k

上述有绝对值

bl - l... br - l
mid 由 b决定

求出w的一半后，搜索 bl - l.... br - l 的 bi - l


现在w可以动态修改，对 [l,r] 需要查询 sum(w[l,r])/2
树状数组维护区间和 但需要查询前缀和中点


动态查询 【l,r】 对所有 al...ar 变换后的 bl...br 带权中位数贪心，w[l,r] 查询前缀和

在前缀和数组ps_w上查询 sum(w[l,r])/2 + ps_w[l]



"""
import itertools
import sys
from bisect import bisect_left
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

class BIT: # 维护区间sum(nums[l,r])
    def __init__(self, n: int, nums: List=None): #初始数组为0时启用
        self.a = [0] * (n + 1)
        self.n = n
        if nums is not None:
            # 预处理nums 计算初始树状数组前缀和
            self.nums = nums
            for i, x in enumerate(nums, 1): # 所有nums[i] => a[i+1]
                self.a[i] += x
                pa = i + (i & -i) # i 父节点，其管辖着i所在的区间
                if pa <= n:
                     self.a[pa] += self.a[i] # 启发式更新

    def add(self, i, x):
        i = i + 1
        a, n = self.a, len(self.a)
        while i < n:
            a[i] += x
            i += i & -i

    def sum(self, i: int): # nums[:i], [0,i) 这里无需串位，原数组i取不到
        res = 0
        while i > 0:
            res += self.a[i]
            i -= i & -i
        return res

    def rsum(self, l:int, r:int) -> int: # 区间sum(nums[l,r])
        return self.sum(r+1) - self.sum(l)


    def lower_bound(self, target):
        # 返回最小 idx，使 sum(idx) >= target；若 target<=0 返回 1
        if target <= 0:
            return 1
        idx = 0
        step = 1 << (self.n.bit_length() - 1)
        while step:
            nxt = idx + step
            if nxt <= self.n and self.a[nxt] < target:
                target -= self.a[nxt]
                idx = nxt
            step >>= 1
        return idx + 1

    def search_from_l(self, l0, t):
        # l0 为 0-indexed 起点；返回最小 r(0-indexed) 使 sum(l0..r) >= t；不存在则返回 -1
        l = l0 + 1  # 转 1-indexed
        base = self.sum(l-1)
        need = base + t
        total = self.sum(self.n)
        if need > total:
            return -1
        r = self.lower_bound(need)  # 1-indexed
        return r - 1                 # 转回 0-indexed


n, q = RII()
a = RILIST()
w = RILIST()

b = [x-i for i,x in enumerate(a)]

# ps_w = list(itertools.accumulate(w, initial=0))
tree_w = BIT(n, w)
# tree_w = BIT(n)
# for i,x in enumerate(w):
#     tree_w.add(i, x)

bw = [x*y for x,y in zip(b,w)]
tree_bw = BIT(n, bw)
# tree_bw = BIT(n)
# for i,bw in enumerate(bw):
#     tree_bw.add(i, bw)

for _ in range(q):
    x,y = RII()
    if x < 0:
        i, v = -x-1, y
        tree_w.add(i, v-w[i])
        tree_bw.add(i, b[i]*(v-w[i]))  # b[i]*w[i] -> b[i]*v

        w[i] = v

    else:
        l, r = x-1, y-1
        # 在前缀和数组ps_w上查询 sum(w[l,r])/2 + ps_w[l]

        ws = tree_w.rsum(l, r) # 闭区间搜索
        j = tree_w.search_from_l(l, (ws+1)//2) # [l,j] >= ws/2

        mid = b[j]
        # bl ... br -> bl-l ... br-l

        # al ... ar
        # wl ... wr
        # |al-mid| ... |ar-mid|

        # sum(al*wl for l) - sum(wl)*mid # 左半
        # sum(wr)*mid - sum(ar*wr for r) # 右半

        # 搜索 mid 使得 bl-l ... br-l, mid>=bi-l

        left = mid * tree_w.rsum(l, j) % MOD - tree_bw.rsum(l, j) % MOD
        right = tree_bw.rsum(j+1, r) % MOD - mid * tree_w.rsum(j+1, r) % MOD
        print((left + right) % MOD)


