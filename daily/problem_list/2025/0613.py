"""
https://codeforces.com/problemset/problem/498/D

输入 n(1≤n≤1e5) 和长为 n 的数组 a(2≤a[i]≤6)。
有一条公路连接 n+1 个城市。从第 i 个城市到第 i+1 个城市需要 1 个单位时间。
但是，如果你从城市 i 出发时，当前时间 t % a[i] = 0，那么必须等待 1 个单位时间才能出发。

然后输入 q(1≤q≤1e5) 和 q 个询问，格式如下：
"A l r"：输出从城市 l 到城市 r 所需的时间。你在城市 l 时，当前时间 t = 0。其中 1≤l<r≤n+1。
"C i v"：把 a[i] 改成 v。其中 1≤i≤n，2≤v≤6。

012345

t[i][0-5] 从i出发时间余数为j=0-5

[l,r] 0-5 通过时间 [l,mid] [mid+1,r]

[l,r] 从l到r的所需时间，出发时间对nums[l]的取模影响不同

对于一个真实的时间t 分别考虑 t%2 ... t%6

8
8%6 = 2
8%4 = 0






周期与lcm - 如何理解这题的状态设计
https://chatgpt.com/c/684bbe3b-1af0-800a-98f9-eb30ef9c0e2e

1. 从两个周期函数的叠加演示开始
    画图：在纸上画一条时间轴，把「能否起步」看作一个 0/1 的波形。
    比如 a[i]=4 的波形：在 t=0,4,8,12… 处画一个↑，其它地方↓。
    a[j]=6 的波形：在 t=0,6,12,18… 处↑，其它↓。
    叠在一起看：把这两条波形平铺，会发现它们的“共同模式”从 t=0 再重复，要等到 12（这就是 lcm(4,6)=12）才完全对齐。

    反例思考：如果你只记录 “模 6 的余数”，那么 假如真实时间是8 t=8 和 t=2 都会得到 2，但
    8 % 4 = 0 （需要等待），
    2 % 4 = 2 （不需要等待）。
    你就搞不清是哪种情况了。

2.  想象你要同时跟踪 t%4 和 t%6，那你可以把当前时间 t 映射成一个二元组
    (tmod4,tmod6).
    在纸上列出 0 1 2 ... 11 时的所有二元组。你会看到 12（＝lcm(4,6)） 后开始重复。
        t | (t%4, t%6)
        0 | (0,0)
        1 | (1,1)
        2 | (2,2)
        …
        7 | (3,1)
        8 | (0,2)
        …
        11| (3,5)
        12| (0,0) ← 重复
    再想想，如果你只存 “模 6” 的一个数字，就把 “模 4” 的信息完全丢掉了。
    而用一个公共同余系是可以同时追踪 4/6的各种取余情况的

3. 在设计算法时养成「写状态转移」的习惯
    任何时候，只要下一个动作依赖于 t % m，就把状态设计成 记录所有需要的余数：
    state = (t mod a1, t mod a2, …)
    如果你发现要跟踪 k 个模，那最简单的整体周期就是它们的 LCM。
    这套思考模式在做「合并多个周期段」或「合并多个有向边的动态规划」时尤其管用。


"""
import sys
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

u = 60 # 根据数据范围 23456 确定的lcm周期
# t%2 01
# t%3 012
# ...
# t%6 012345 我需要在每个出发点，记住
class SegmentTree:  # sum
    def __init__(self, n, nums=None):
        self.t = [None] * (4 * n)  # t[p][0-5] 区间左侧出发时间对u的取余 通过该区间的用时
        if nums:
            assert n == len(nums)
            self.nums = nums
            self.build(1, 0, n - 1)  # 初始化build

    def build(self, p, l, r): # (p,l,r) parent 以及管辖区间
        if l == r:
            self.apply(p, l, self.nums[l])
            return
        mid = (l + r) // 2
        self.build(2 * p, l, mid)
        self.build(2 * p + 1, mid + 1, r)
        self.pull(p)

    ##############################################

    def pull(self, p):  # up
        # 子信息汇总p <- 2*p, 2*p+1
        self.t[p] = self.merge(self.t[2 * p], self.t[2 * p + 1])

    def merge(self, left, right):

        res = [0]*u
        for i in range(u): # 起始时间i
            t = left[i] # 左侧起始时间i 到达 mid - mid+1 的时间
            res[i] = t + right[(i+t)%u]
        return res

    def apply(self, p, i, v):
        self.nums[i] = v
        res = [1]*u
        for k in range(0, u, v):
            res[k] += 1
        self.t[p] = res
    #######################################

    def update(self, p, l, r, i, v):
        # (p,l,r) [L, R] += v - 支持负数=减法
        if l == r: # 当(p,l,r) 为 [L, R] 子区间即停止递归，利用懒信息下发函数更新（不要递归到空，否则失去懒更新意义)
            self.apply(p, l, v)
            return
        mid = (l + r) // 2
        if i <= mid:
            self.update(2 * p, l, mid, i, v)
        if mid < i:
            self.update(2 * p + 1, mid + 1, r, i, v)
        self.pull(p)

    def query(self, p, l, r, L, R):
        if L <= l and r <= R:
            return self.t[p]
        res = [0]*u
        mid = (l + r) // 2
        if L <= mid:
            res = self.query(2 * p, l, mid, L, R)
        if mid < R:
            res = self.merge(res, self.query(2 * p + 1, mid + 1, r, L, R))
        return res

n = RI()
nums = RILIST()
Q = RI()
tree = SegmentTree(n, nums)
for _ in range(Q):
    q = RS().split()
    if q[0] == "A":
        l,r = int(q[1])-1, int(q[2])-1
        res = tree.query(1, 0, n-1, l, r-1)
        print(res[0])
    else:
        i,v = int(q[1])-1, int(q[2])
        tree.update(1, 0, n-1, i, v)
