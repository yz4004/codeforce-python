"""
https://codeforces.com/problemset/problem/220/E

输入 n(2≤n≤1e5) k(0≤k≤1e18) 和长为 n 的数组 a(1≤a[i]≤1e9)。

输出有多少个 (L,R)，满足 L<R 且删除子数组 [L+1,R-1] 后，剩余元素的逆序对数量至多为 k。

5 2
1 3 2 1 4
输出 6

3 1
1 3 2
输出 3


如果不移除就可以让总数小于k 即任意数对直接可以实现 直接输出 n-1 + n-2 + ... + 1
枚举需要删除的最短子数组 r] 滑窗 - [l,r] 最短的子数组需要删除 使得剩余逆序对总数 <= k 则任意 l 左侧都可以 (不包含0)

"""
from collections import defaultdict
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

# 滑窗 容斥 逆序对
class BIT:  # 1-based - 值域树状数组

    def __init__(self, n): # [1,n]
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, i, delta): # a[i] += 1
        n = self.n
        tree = self.tree
        while i <= n:
            tree[i] += delta
            i += i & -i

    def prefix_sum(self, i): # [1,i]
        res = 0
        tree = self.tree
        while i > 0:
            res += tree[i]
            i -= i & -i
        return res

    def kth(self, k): # 1-based 1...k
        idx = 0
        bit = 1 << (self.n.bit_length() - 1)
        tree = self.tree
        while bit:
            nxt = idx + bit
            if nxt <= self.n and tree[nxt] < k:
                k -= tree[nxt]
                idx = nxt
            bit >>= 1
        return idx + 1

def solve(n, k, a):
    vals = sorted(set(a))
    mp = {v: i for i, v in enumerate(vals, 1)}
    # [L,R]
    a = [mp[v] for v in a]
    m = len(a)

    total = 0
    tree = BIT(m)  # [1,m]
    for i, x in enumerate(a):
        # [0,i-1] i
        total += i - tree.prefix_sum(x)  # 总数-小于等于x的 = 严格大于x
        tree.add(x, 1)

    # 如果不移除就可以让总数小于k 即任意数对直接可以实现 直接输出 n-1 + n-2 + ... + 1
    if total <= k:
        return n * (n-1) // 2

    # [L+1,R-1] 移除后剩余至多为k - 该区间引入的逆序对至少为 total-k

    tree0 = BIT(m)  # [1,m]
    tree1 = tree

    res = 0 if total > k else n - 1

    cur = total
    l = 0
    for i in range(n - 1):
        x = a[i]
        # [l,i]
        # 引入x后的变化
        # x和左侧部分的逆序对
        tree1.add(x, -1)

        # [l,i]
        # 移除x 左侧损失的逆序对 右侧损失的逆序对
        left_cnt = l - tree0.prefix_sum(x)  # [0,l-1]
        right_cnt = tree1.prefix_sum(x - 1)  # [i+1,n-1]

        cur -= left_cnt + right_cnt

        while l <= i and cur <= k:
            # [0,l-1] l
            y = a[l]
            left_cnt = l - tree0.prefix_sum(y)
            right_cnt = tree1.prefix_sum(y - 1)
            cur += left_cnt + right_cnt

            tree0.add(y, 1)
            l += 1

        # cur -- 移除 [l,i] 剩余逆序对 <=k
        # [l,i]
        # 0...l-1
        if l > 0:
            res += l - 1

    return res

n, k = RII()
a = RILIST()
print(solve(n, k, a))







