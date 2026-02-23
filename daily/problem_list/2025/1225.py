"""
https://codeforces.com/problemset/problem/1667/B

输入 T(≤5e5) 表示 T 组数据。所有数据的 n 之和 ≤5e5。
每组数据输入 n(1≤n≤5e5) 和长为 n 的数组 a(-1e9≤a[i]≤1e9)。

你需要把 a 分割成若干个非空连续子数组。注：这一共有 2^(n-1) 种分割方法。

对于子数组 b，设 s = sum(b)。
如果 s > 0，则 b 的价值为 len(b)。
如果 s < 0，则 b 的价值为 -len(b)。
如果 s = 0，则 b 的价值为 0。

哪种划分方法，可以让所有子数组的价值之和最大？
输出这个最大值。

"""
import itertools
from collections import defaultdict
import sys
from math import inf
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
man_ = lambda x, y: y if x > y else x
MOD = 998244353


class BIT_max:
    def __init__(self, n: int):
        self.n = n
        self.a = [-inf] * (n + 1)
        self.b = [-inf] * (n + 1)


    # nums[i] 上 apply x
    def add(self, i, x):
        a, b, n = self.a, self.b, len(self.a)
        b[i] = max_(b[i], x)
        while i < n:
            if x > a[i]:
                a[i] = x
            i += i & -i

    # 前缀查询 [,i] 前i个的max
    def max(self, i: int):
        a, n = self.a, len(self.a)
        res = -inf
        while i > 0:
            if a[i] > res:
                res = a[i]
            i -= i & -i
        return res

    # [i,j]
    def rmax(self, i, j):
        a, b, n = self.a, self.b, len(self.a)

        res = -inf
        while i <= j:
            lb = j & -j
            l = j - lb + 1
            # [l,j] = [j-lb+1, j]

            if i <= l:
                res = max_(res, a[j])
                j = l-1
            else:
                res = max_(res, b[j])
                j = j-1
        return res


def solve(n, nums):


    """
    划分dp + 数据结构优化 + 树状数组维护最大值
    fi - 前i个最大划分
    fi = fj + (i-j) if si > sj  从满足条件的 j,sj 里选最大的 fj + (i-j) 
    fi = fj - (i-j) if si < sj  从满足条件的 j,sj 里选最大的 fj - (i-j) 
    fi = fj         if si == sj  
    
    where si - [,i]
    
    等式变形
    fi = max(fj-j, for sj < si) + i
    fi = max(fj+j, for sj > si) - i 
    fi = max(fj for si == si)

    空项特殊处理
    (j,sj) = (-1,0)
    """

    # 离散化前缀和
    ps = list(itertools.accumulate(nums, initial=0))
    vals = sorted(set(ps))
    mp = {v:i for i,v in enumerate(vals, 1)}
    u = len(vals)

    tree1 = BIT_max(u+1)
    tree2 = BIT_max(u+1)
    equal = [-inf]*(u+1)

    # s[-1] 0+ -1 0- -1
    tree1.add(mp[0], -1)  # tree1 - fj+j
    tree2.add(mp[0],1)  # tree2 - fj-j
    equal[mp[0]] = 0
    fn = -inf

    for i in range(n):
        si = ps[i+1]
        si = mp[si]

        a = tree1.rmax(si+1, u) - i  # si < sj -- fj + j
        b = tree2.max(si-1) + i     # si > sj -- fj - j
        c = equal[si]                    # si

        fi = max(a,b,c)

        tree1.add(si, fi + i)
        tree2.add(si, fi - i)
        equal[si] = max_(equal[si], fi)
        fn = fi

    return fn

for _ in range(RI()):
    n, nums = RI(), RILIST()
    print(solve(n, nums))
