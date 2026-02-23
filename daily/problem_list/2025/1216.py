"""
https://www.luogu.com.cn/problem/P1627

输入 n(1≤n≤1e5) med(1≤med≤n) 和一个 1~n 的排列 p。

输出 p 有多少个长为奇数的连续子数组，满足 med 是子数组的中位数。

进阶：如果没有「长为奇数」的限制呢？长为偶数时取中间靠左的数作为中位数。

7 4
5 7 2 4 3 1 6
输出 4

"""
import sys
from functools import cache
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

def solve_p1627(n, med, permutation):
    idx = next((i for i in range(n) if permutation[i] == med), -1)

    a = [1 if x > med else -1 for x in permutation]
    a[idx] = 0


    # a[l,r] = 0. l < idx < r
    # s[r] - s[l-1] == 0

    cnt = [[0]*(n+1) for _ in range(2)]
    cnt[0][0] = 1

    s = 0
    res = 0
    for i,x in enumerate(a):
        s += x

        odd = (i+1)%2
        if i >= idx:
            # i 是奇数index 需找前面偶数 index的计数
            res += cnt[odd ^ 1][s]
            # print(cnt, i, permutation[:i+1], res)

        cnt[odd][s] += 1
    return res



n, med = RII()
permutation = RILIST()
print(solve_p1627(n, med, permutation))

