"""
https://atcoder.jp/contests/abc332/tasks/abc332_f
https://atcoder.jp/contests/abc332/submissions/me

输入 n(1≤n≤2e5) m(1≤m≤2e5) 和长为 n 的数组 a(0≤a[i]≤1e9)。下标从 1 开始。
输入 m 个操作，每次操作输入 L R x(0≤x≤1e9)，表示在 [L,R] 中等概率地选一个整数 i，然后把 a[i] 替换成 x。

输出最终 a[1],a[2],...,a[n] 的期望值，模 M=998244353。
注：如果期望值是一个分数 p/q，你需要输出 p*pow(q,M-2)%M。

------
def get_mode(x):
    p, q = x
    if p % q == 0:
        return (p // q) % M
    return p * pow(q, M-2, M) % M
-----------

E -(x,p)->  E*(1-p) + x*p

e (p1,x1) (p2,x2)

(1-p1)e + p1 x1
(1-p2)(1-p1)e + p2*p1*x1 + p2*x2 + p1*x1



区间修改
"""

import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

M = mod = 998244353
class SegmentTree:  # 区间修改
    def __init__(self, n, nums=None):
        self.tag = [(1,0)] * (4 * n)  # 懒信息 (p,x)
        if nums:  # 如果有初始化数组输入，执行build逻辑
            assert n == len(nums)
            self.nums = nums
            self.build(1, 0, n - 1)  # 初始化build

    def build(self, p, l, r): # (p,l,r) parent 以及管辖区间
        if l == r:
            return
        mid = (l + r) // 2
        self.build(2 * p, l, mid)
        self.build(2 * p + 1, mid + 1, r)

    ##############################################
    def push(self, p, l, r):  # down 通知树节点p 下发懒信息
        if self.tag[p] != (1,0):
            op = self.tag[p]
            self.apply(2 * p, op)  # 懒信息推给左
            self.apply(2 * p + 1, op)  # 懒信息推给右
            # self.tag[p] = None  # 清空暂存的懒信息，已经下发
            self.tag[p] = (1,0)

    def apply(self, p, op):  # 区间更新并下发懒信息
        # E -> (1-p)E + px
        # p = 1/l
        if self.tag[p]:
            self.tag[p] = self.merge(op, self.tag[p])
        else:
            self.tag[p] = op

    def merge(self, new, old):
        # op1 -> op2
        # E -> (1-p)E + px
        # p = 1/l
        # op1 = (l1, x1) op2 = (l2, x2)
        # op1 = (a,b), op2 = (c,d)
        a, b = new
        c, d = old
        # a*(c*E + d) + b
        return a*c % mod, (a*d + b) % mod

    ##############################################

    def update_interval(self, p, l, r, L, R, op): # (p,l,r) 区间覆盖成v [L, R] = v 逻辑取决于apply
        if L <= l and r <= R:
            self.apply(p, op)  # 区间更新，停止递归并暂存懒信息（不要递归到空，否则失去懒更新意义)
            return
        mid = (l + r) // 2
        self.push(p, l, r)  # 递归左右之前，先分发懒信息
        if L <= mid:
            self.update_interval(2 * p, l, mid, L, R, op)
        if mid < R:
            self.update_interval(2 * p + 1, mid + 1, r, L, R, op)

    def touch(self, p, l, r): # (p,l,r) 区间查询 [L,R]
        if l == r:
            a,b = self.tag[p]
            self.nums[l] = (self.nums[l] * a + b) % M
            return
        mid = (l + r) // 2
        self.push(p, l, r)  # 递归左右之前，先分发懒信息，虽然不会更新，但查询部分左右区间也依赖本层懒信息
        self.touch(2*p, l, mid)
        self.touch(2*p+1, mid+1, r)

n, q = RII()
a = RILIST()
tree = SegmentTree(n, a)
for _ in range(q):
    l, r, x = RII()
    l, r = l-1, r-1
    L = r - l + 1
    # E = (1-p)*E + x*p, p=1/L
    inv_L = pow(L, M-2, M)
    op = ((L-1) * inv_L % M, x * inv_L % M)
    tree.update_interval(1, 0, n - 1, l, r, op)
tree.touch(1, 0, n-1)
print(" ".join(map(str, tree.nums)))
#
# sys.exit(0)
#
# def solve():
#     pass
#
# def solver_brute_force():
#    pass
#
#
# import random
# # 对拍测试
# for _ in range(0):
#     n = random.randint(1, 10)
#     # random.sample(range(1 << 30), n)
#     # a = [random.randint(1, 1<<30) for _ in range(n)]
#     # b = [random.randint(1, 1<<5) for _ in range(n)]
#
#     # a = [1002501680, 806845573, 1072860959, 767443906, 705458535, 856321116, 861410079, 603864214, 250108046, 915287742]
#     # b = [2, 15, 4, 28, 29, 2, 25, 25, 19, 19]
#
#     a = [8, 4, 9, 3, 2, 5, 6, 1, 0, 7]
#     b = [0, 2, 1, 5, 6, 0, 4, 4, 3, 3]
#
#     # a = [1,2,2,2]
#     # b = [0,3,2,1]
#
#     # for brute force
#     # nums = sorted(zip(a, b))
#     # b_sorted = [x[1] for x in nums]
#     #
#     # # 构造b_sorted在b中的位置顺序
#     # pos = {v: i for i, v in enumerate(sorted(b_sorted))}
#     # mapped = [pos[x] for x in b_sorted]
#     #
#     # expected = brute_force_inversions(mapped)
#     expected = solver_brute_force(a, b)
#     actual = solve(a, b)
#
#     if expected != actual:
#         print("Mismatch!")
#         print(f"a = {a}")
#         print(f"b = {b}")
#         print(f"expected = {expected}, actual = {actual}")
#         break
# else:
#     print("✅ All tests passed!")