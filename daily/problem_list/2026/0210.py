"""
https://codeforces.com/problemset/problem/2179/D

输入 T(≤16) 表示 T 组数据。所有数据的 2^n 之和 ≤2^16。
每组数据输入 n(1≤n≤16)。

构造一个长为 2^n 的排列 p，元素范围为 [0, 2^n - 1]。
计算 p 的前缀 AND，即前 i=1,2,...,2^n 个数的 AND，得到一个长为 2^n 的数组 pre。
定义 S(p) = popcount(pre[1]) + popcount(pre[2]) + ... + popcount(pre[2^n])，其中 popcount(x) 表示 x 二进制中的 1 的个数。

目标是最大化 S(p)。
在所有让 S(p) 最大的排列 p 中，输出字典序最小的 p。

进阶：做到 O(1) 空间。
"""
import sys, itertools
from functools import cache
from heapq import heappop, heapify, heappush
from math import inf, isqrt, gcd
from bisect import bisect_left
from collections import deque, defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

"""
pre[i] = p1 &... & pi 
一直and 一旦有一个位置是0 这位后面就不用看了
肯定把 111.. 放前面 然后再放就得牺牲一位了 
只看1计数. 1的地位是均等的，牺牲哪位都一样 就从上往下

1010
1100
1111
1111... 

每次看 前i位置能不能满足 
1111? 
.111? - 所有的计数 
..11? - 所有的计数 (注意 .. 统计0-111 但要排除之前 111统计过得 即 ...1 形式的排除 否则应该计入前面的)

在此基础上输出字典序最小 即 ...1111 前面...做到字典序最小 0000 -> 1110

"""

def solve(n):

    res = [0]*(1<<n)
    res[0] = (1<<n)-1 # all one

    idx = 1 # fill res index

    # layer 从 1 到 n:
    # layer = 1: 形如 [高位 0 bits][0][低位 n-1 个 1] - 中间[0]分开高位和低位的连续1
    # layer = 2: 形如 [高位 1 bits][0][低位 n-2 个 1]
    # ...
    # layer = n: 形如 [高位 n-1 bits][0][低位 0 个 1]  => 其实就是偶数序列
    for layer in range(1, n + 1):

        low_ones_len = n - layer          # 低位连续 1 的长度
        high_free_len = layer - 1         # 更高位自由变化的长度

        low_mask = (1 << low_ones_len) - 1  # 例如 low_ones_len=3 => 0b000111

        # 位结构（从高到低）：
        #   [ high_free_len bits: x ] [ 1 bit: 0 ] [ low_ones_len bits: all 1 ]
        #
        # 也就是：
        #   (x << (low_ones_len + 1))  把 x 放到高位区域
        #   中间那个 0 bit 不用显式加（天然是 0）
        #   | low_mask                 把低位填成全 1
        """
        [  高位自由 x  ] [  1 个固定 0  ] [  低位全 1  ]
           high_free_len         1      low_ones_len
           
        比如n=9 某一层 low one len=5
           x x x | 0 | 1 1 1 1 1
        """
        shift = low_ones_len + 1

        for x in range(1 << high_free_len):
            res[idx] = (x << shift) | low_mask
            idx += 1

    return res

for _ in range(RI()):
    n = RI()
    res = solve(n)
    print(" ".join(map(str, res)))