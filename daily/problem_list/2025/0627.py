"""
https://codeforces.com/problemset/problem/266/E

输入 n(1≤n≤1e5) m(1≤m≤1e5) 和长为 n 的数组 a(0≤a[i]≤1e9)。
下标从 1 开始。

然后输入 m 个询问，格式如下：
"= l r x"：把下标在 [l,r] 中的 a[i] 改成 x。(0≤x≤1e9)
"? l r k"：输出 a[l]*1^k + a[l+1]*2^k + ... + a[r]*(r-l+1)^k，其中 ^ 是幂运算，0≤k≤5。
答案模 1e9+7。


提示：
在线段树 【区间修改 + 区间查询和】 的基础上引入了带权前缀和
用 lazy 线段树维护 6 种元素和，即 a[i] * i^j 之和，其中 j=0,1,2,3,4,5。
区间修改，我们需要计算 x * (l^j + (l+1)^j + ... + r^j)，和式的计算可以用前缀和，需要提前预处理 i^0 的前缀和，i^1 的前缀和，……，i^5 的前缀和。即代码中的 sPow。

区间查询，首先从线段树中获取到长为 6 的数组 s[j] = a[l]*l^j + a[l+1]*(l+1)^j + ... + a[r]*r^j，其中 j=0,1,2,3,4,5。
我们要计算的是 sum_{i=l}^r a[i] * (i-l')^k，其中 l'=l-1。
用二项式定理把 (i-l')^k 展开，与 a[i] 相乘，把其中的 a[i]*i^j 用 s[j] 代替，得到最终答案为 C(k,j) * s[j] * (-l')^(k-j)



ai * i^k k=0-5

ai * (i-d)^k
= ai * (i^k * ck0 * d^0 + i^(k-1) * ck1 * d^1  + i^(k-2) * ck2 * d^3 ... i^0 * ckk * d^k)

= ai * i^k      ai * i^(k-1)        ai * i^(k-2)   ...     ai * i^0
ck0 * d^0       ck1 * d^1           ck2 * d^2      ...     ckk * d^k


经过错位后，ai * i^k -> ai * i^(k-1) ... ai * i^0 并对应上系数 ~ (d, k)

当查询子数组 [l,r] with 幂次 k
[l,r]_k = sum(ai * i^k for i in l-r)
= sum(ai*i^k for i=l-r) + sum(ai*i^(k-1) for i=l-r) ...
    ck0 * d^0             ck1 * d^1

= ps[k][l-r] + ps[k-1][l-r] ...
  ck0 * d^0    ck1 * d^1


"""
import itertools
import sys
from math import comb

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
mod = 10 ** 9 + 7


n, m = RII()
nums = RILIST()


# ik[i][k] = i^k  for k=0-5
ik = [[pow(i, k, mod) for k in range(6)] for i in range(n)]
# pow = lambda i,k: ik[i][k]

prefix_ik = [list(itertools.accumulate(ik_col, initial=0)) for ik_col in zip(*ik)]
# l^k + ... r^k
# prefix_ik[k][r+1] - prefix_ik[k][l]

ck = [[comb(k,i) for i in range(k+1)] for k in range(6)]
comb = lambda k,i: ck[k][i]

# ps = []
# for k in range(6):
#     p = [0]*(n+1)
#     for i,x in enumerate(nums):
#         p[i+1] += p[i] * ik[i][k]  # i^k 预处理
#         p[i+1] %= mod
#     ps.append(p)

# ps[k][l-r] -- a[l] * l^k + ... + a[r] * r^k

class SegmentTreeSum:  # sum
    def __init__(self, n, nums=None):
        self.ps = [[0]*6 for _ in range(4*n)] # ps[p] -
        self.tag = [-1] * (4 * n)
        if nums:  # 如果有初始化数组输入，执行build逻辑
            assert n == len(nums)
            self.nums = nums
            self.build(1, 0, n - 1)  # 初始化build

    def build(self, p, l, r):
        # (p,l,r) parent 以及管辖区间
        if l == r:
            self.ps[p] = [self.nums[l] * pow(l, k) for k in range(6)]
            return
        mid = (l + r) // 2
        self.build(2 * p, l, mid)
        self.build(2 * p + 1, mid + 1, r)
        self.pull(p)

    #######################################
    def pull(self, p):  # up
        # 依次对固定幂k=0-6 合并前缀和，索引对应原数组全局索引
        for k in range(6):
            self.ps[p][k] = self.ps[2 * p][k] + self.ps[2 * p + 1][k]

    def push(self, p, l, r):  # down 通知树节点p 下发懒信息
        if self.tag[p] > -1:
            v = self.tag[p]
            self.apply(2 * p, l, (l + r) // 2, v)         # 懒信息推给左
            self.apply(2 * p + 1, (l + r) // 2 + 1, r, v) # 懒信息推给右
            self.tag[p] = -1 # 清空暂存的懒信息，已经下发

    def apply(self, p, l, r, v):  # 下发lazy信息，先更新节点信息，然后暂存懒信息，（不继续下发）
        # 区间 [l,r] 被覆盖成v
        # v*l^k ... v*r^k for k=0-6 需要预处理
        for k in range(6):
            self.ps[p][k] = v * (prefix_ik[k][r+1] - prefix_ik[k][l])
        self.tag[p] = v
    #######################################

    def set(self, p, l, r, L, R, v):
        # (p,l,r) [L, R] = v
        if L <= l and r <= R: # 当(p,l,r) 为 [L, R] 子区间即停止递归，利用懒信息下发函数更新（不要递归到空，否则失去懒更新意义)
            self.apply(p, l, r, v)
            return
        mid = (l + r) // 2
        self.push(p, l, r) #递归左右之前，先分发懒信息
        if L <= mid:
            self.set(2 * p, l, mid, L, R, v)
        if mid < R:
            self.set(2 * p + 1, mid + 1, r, L, R, v)
        self.pull(p)

    def query(self, p, l, r, L, R):
        """
         ps[k][l-r] + ps[k-1][l-r] ...  ps[0][l-r]
         ck0 * d^0    ck1 * d^1    ...  ckk * d^k
        """
        if L <= l and r <= R:
            return [self.ps[p][j] for j in range(0, k+1)]


        mid = (l + r) // 2
        self.push(p, l, r)  # 递归左右之前，先分发懒信息，虽然不会更新，但查询部分左右区间也依赖本层懒信息
        if R <= mid:
            return self.query(2*p, l, mid, L, R)
        if mid < L:
            return self.query(2 * p + 1, mid + 1, r, L, R)
        # [l,mid] [mid+1,r]

        # [l,r]
        # [1, r-l+1]   d=l-1
        # d -- 查询区间 每一项 新的幂底数 和原索引的差

        a = self.query(2*p, l, mid, L, R)
        b = self.query(2 * p + 1, mid + 1, r, L, R)
        # print(a, b, k)
        for j in range(k+1):
            a[j] += b[j]
        return a


tree = SegmentTreeSum(n, nums)
for _ in range(m):
    q = RS().split()
    if q[0] == "=":
        # [l,r] -> x
        l, r, x = map(int, q[1:])
        l, r = l-1, r-1
        tree.set(1, 0, n-1, l, r, x)
    else:
        # a[i] * 1^k + a[i+1] * 2^k + ... + a[r] * (r-l+1)^k
        l, r, k = map(int, q[1:])
        l, r = l-1, r-1

        d = l-1
        ps = tree.query(1, 0, n-1, l, r)
        # res = sum(ps[k-j] * comb(k,j) * ik[d][j] * (1 if j % 2 == 0 else -1) for j in range(0, k+1)) % mod
        res = sum(ps[k-j] * comb(k,j) * pow(-d,j,mod) for j in range(0, k+1)) % mod
        print(res)
