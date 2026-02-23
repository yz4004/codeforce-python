"""
https://codeforces.com/problemset/problem/946/E

输入 T(≤1e5) 表示 T 组数据。所有数据的数字长度之和 ≤2e5。
每组数据输入长度 ≤2e5 的数字 s，不含前导零，且保证 s 的长度是偶数。

定义美丽数为不含前导零，长度为偶数，且可以重排成回文数的正整数。
例如 4242 是美丽数，因为它可以重排成回文数 2442。

输出严格小于 s 的最大美丽数。（输入保证有解）
"""
import sys
from collections import Counter, defaultdict
from typing import List
# from sortedcontainers import SortedList

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

def solve(s):
    n = len(s)
    s_ = [int(c) for c in s]

    # 输入s长度偶数
    mask = 0
    for c in s_:  mask ^= 1 << c

    # if mask == 0: return s # 严格小于

    for i in range(n-1, -1, -1):
        c = s_[i]
        # [0, j, n-1]
        # n-1-j = i+1
        mask ^= 1 << c

        # i [i+1,n)
        for d in range(c-1, -1, -1):
            t = mask ^ (1<<d)
            if (not i == d == 0) and t.bit_count() <= l:
                pre = s[:i] + str(d)
                must = ''.join(str(c) for c in range(9, -1, -1) if t >> c & 1)
                l = n - len(pre) - len(must)
                return pre + "9" * l + must
    return "9" * (n-2)


    # 9228
    # 9_19

    # hint 倒着枚举

    # 1. c tight 前面有未补足的
    # 2. c tight 后面有大于等于c的.
    # 3. c 找不到补足，枚举后面最大的 能补足c的
    # ps: 一旦出现降位 则后面都变成自由位 可以和前面补足

# print(solve("28923845"))
# print(solve("1000"))
for _ in range(RI()):
    print(solve(RS()))
