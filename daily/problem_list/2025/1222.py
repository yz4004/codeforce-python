"""
https://www.luogu.com.cn/problem/P9242

输入 n(1≤n≤1e5) 和长为 n 的数组 a(1≤a[i]≤1e9)，保证 a[i] 无前导零。

你需要从 a 中删除一些数，得到一个接龙序列 b，满足 b[i-1] 的末位数字等于 b[i] 的首位数字。
例如 12,23,35,56,61,11 是接龙序列；12,23,34,56 不是接龙序列。
长为 1 的序列是接龙序列。

输出最少删除多少个数。

"""
import itertools
import sys
from functools import cache
from math import inf
from operator import add, xor
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RSS = lambda: sys.stdin.readline().strip().split()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
RSLIST = lambda: list(RSS())

max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

def solve(n, nums):

    # 11 11 22 12 23 只需考虑收尾字母
    # 如果改成任意排列 （欧拉回路 euler trial）
    # 可能需要 min cost flow解决
    # euler trial - 七桥问题 欧拉路 - 通过图中所有边的简单路 - 根据连边关系 给数组找一个排列

    def mp(s):
        return int(s[0] + s[-1]) # 11 12...99

    nums = [mp(s) for s in nums]

    # 子序列状态机/合法子序列
    # 最长接龙序列 考虑开头数字接前一个数字
    f = [0]*10
    for x in nums:
        p,q = x//10, x%10
        f[q] = max(f[q], f[p] + 1)
    return n - max(f)

n, nums = RI(), RSLIST()
print(solve(n, nums))


