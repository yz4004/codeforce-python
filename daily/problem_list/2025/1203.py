"""
https://codeforces.com/problemset/problem/961/E

输入 n(1≤n≤2e5) 和长为 n 的数组 a(1≤a[i]≤1e9)。

某电视剧有 n 季，第 i 季有 a[i] 集。i 从 1 开始。
输出有多少对 (x,y) 满足 1≤x<y≤n，且同时存在第 x 季第 y 集和第 y 季第 x 集。

进阶：一边读入，一边计算答案。
"""
from heapq import heappush, heappop
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7



class BIT:  # 1-based

    def __init__(self, n): # [1,n]
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, i, delta): # a[i] += delta
        n = self.n
        tree = self.tree
        while i <= n:
            tree[i] += delta
            i += i & -i

    def prefix_sum(self, i): # [1, i]
        res = 0
        tree = self.tree
        while i > 0:
            res += tree[i]
            i -= i & -i
        return res

    def kth(self, k): # 1-base - k-base
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




def solve(n, a):
    # ai ...
    # (x, y)  (y, x)

    # vals = sorted(set(a))
    # 数据压缩/离散化会导致变形 值域至多n

    # 将 a1 ... an 在第一象限画直方图，以 y=x 分割，则发现下三角需要查询上三角（前缀）
    # 每当扫到 i 时，对应高度 ai = x
    # 对于 min(x, i)，前缀 [1, i] 上有多少个竖线 高度超过 i
    # 则对于这些线 (j, aj) where aj >= i 有 (j, i) ~ (i, j)
    # 在 (i, ai = x) 高于 i 的部分，未来也会被作为后面元素的部分，他会在前缀加相应 1 处理成 1
    # 直到后面查询 >= x 后被删除，当 x = i 时，删除前缀位置 i 处的 1，删除队列记录信息 (x, i)

    tree = BIT(n+1)
    rmv = []   # 标记删除位置
    res = 0

    for i in range(1, n+1):

        x = mn(a[i-1], n)
        # [1, x]

        if x >= i:
            # 当前竖线高于对角线，只查询低于对角线的部分，高于对角线的部分会被未来的查询访问到 并记录删除位置
            # [1, i-1]
            res += tree.prefix_sum(i)   # 查询 [1, i-1] 上的前缀
            tree.add(i, 1)

            # [i, x]
            heappush(rmv,  (x, i))   # 删除时刻 + 位置

        else:
            # 低于对角线 只查询 [1,x] 部分
            res += tree.prefix_sum(x)  # x] 查询 [1, x] 上的前缀

        while rmv and rmv[0][0] == i:
            x, j = heappop(rmv)
            tree.add(j, -1)
    return res

n, a = RI(), RILIST()
print(solve(n, a))

