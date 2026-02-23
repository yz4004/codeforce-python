"""
https://codeforces.com/problemset/problem/1288/E

输入 n m(1≤n,m≤3e5) 和长为 m 的数组 a(1≤a[i]≤n)。

你的近期聊天列表有 n 个好友，从上到下依次为 1 到 n。
你会依次接收到 m 条消息，记录在数组 a 中。
其中 a[i] 表示好友 a[i] 给你发了消息，这会导致好友 a[i] 移到列表的最上面，其余人下移一位。

对于每个好友 x=1,2,3,...,n，输出在这个过程中（包括开始和结束），x 在列表中的最小位置和最大位置。位置从 1 到 n。
"""
import sys
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

n, m = RII()
nums = RILIST()


class BIT:
    # 树状数组维护前缀和 (1-base)
    # 单点更新 + 区间查询 + BIT二分
    # 所有入参坐标均对应原数组坐标
    # - 前缀查询 [:i] 前i个
    # - 区间查询 [l,r] 查询闭区间
    # - 二分查询 [:i] 最小的i使得前缀 [:i] >= target
    def __init__(self, n: int, nums: List = None):
        self.n = n
        self.a = [0] * (n + 1)
        # 启发式更新 i的父节点是 i + lb(i)
        if nums is not None:
            self.nums = nums
            for i, x in enumerate(nums, 1):
                self.a[i] += x
                pa = i + (i & -i)
                if pa <= n:
                    self.a[pa] += self.a[i]

    # nums[i] += x
    def add(self, i, x):
        i = i + 1
        a, n = self.a, len(self.a)
        while i < n:
            a[i] += x
            i += i & -i

    # 前缀查询 [:i] 前i个的和
    def sum(self, i: int):
        res = 0
        while i > 0:
            res += self.a[i]
            i -= i & -i
        return res

    # 区间查询 [l,r] 查询闭区间
    def rsum(self, l: int, r: int) -> int:
        return self.sum(r + 1) - self.sum(l)


tree = BIT(m + n)
# [0, m-1] [m, m+n-1]
for i in range(m, m+n):
    tree.add(i, 1)

posi = list(i+m-1 for i in range(n+1))  # 1 -> m.  i -> m+i-1
res = [[i, i] for i in range(0, n+1)]
for idx, x in zip(range(m-1, -1, -1), nums):
    j = posi[x]

    res[x][1] = mx(res[x][1], tree.sum(j+1))

    tree.add(j, -1)

    res[x][0] = 1

    tree.add(idx, 1)
    posi[x] = idx
    idx -= 1

for x in range(1, n+1):
    j = posi[x]
    res[x][1] = mx(res[x][1], tree.sum(j+1))

for a,b in res[1:]:
    print(str(a) + " " + str(b))


