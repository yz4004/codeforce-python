"""
https://codeforces.com/problemset/problem/1926/E

输入 T(≤5e4) 表示 T 组数据。
每组数据输入 n k(1≤k≤n≤1e9)。

一开始，有一个长为 n 的数组 a = [1,2,...,n] 和一个空数组 b = []。
首先取出 a 中的奇数，从小到大添加到 b 的末尾。
然后取出 a 中剩余的是奇数*2 的数，从小到大添加到 b 的末尾。
然后取出 a 中剩余的是奇数*3 的数，从小到大添加到 b 的末尾。
然后取出 a 中剩余的是奇数*4 的数，从小到大添加到 b 的末尾。
依此类推，直到 a 为空。
例如 n = 7 时，b = [1,3,5,7] + [2,6] + [] + [4] = [1,3,5,7,2,6,4]。

b 的下标从 1 开始。
输出 b[k]。

"""
import itertools
import sys
from bisect import bisect_left
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

import itertools, sys
from bisect import bisect_left

MOD = 10 ** 9 + 7

def solve(n, k):   # usage
    # ...1
    # ...10
    # ...100

    # 二进制指数 + 二分
    # 注意到每次生成的数是 以 lowbit= 1, 10 100... 为单位 x*lb <= n 的所有奇数
    # 所以第k个 先找对应的lowbit 再找对应lowbit内部的第几个 1 3 5 7 ... * lb
    # 1010 = 10
    # 1000
    # _100
    # __10
    # ___1

    # 注意被4整除的同时也被2整除，所以倒叙要排除
    tmp = []
    for i in range(n.bit_length() - 1, -1, -1):
        t = 1 << i
        exclude = n // (1 << (i+1)) if 1 < n.bit_length() - i else 0
        tmp.append(n // t - exclude)

    tmp = tmp[::-1]
    tmp = list(itertools.accumulate(tmp))
    i = bisect_left(tmp, k)    # >= k 对应lowbit

    pre = tmp[i-1] if i > 0 else 0 # 该lowbit 前面的计数

    # 1<<i  1...t  =>  2k+1
    # range(1, (n-1)//(1<<i)+2, 2)   k-pre  该lowbit内部的第 k-pre 个 1 3 5 7 ... 2*j-1 取 j= k-pre

    j = (k - pre) * 2 - 1
    return j * (1 << i)

for _ in range(RI()):
    n,k = RII()
    print(solve(n,k))