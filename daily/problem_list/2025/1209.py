"""
https://www.luogu.com.cn/problem/P1282

输入 n(1≤n≤1000) 和 n 行 2 列的矩阵，元素范围 [1,6]。

你可以交换每行的两个数。
你需要最小化 |第一列的和 - 第二列的和|。
输出最小交换次数。

"""
from heapq import heappush, heappop
import sys
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7


def solve_lg1282(n, a):
    # x, y
    # len(a)

    # f[i] : suma - sumb = i  -> minimal swap
    m = sum(max(x, y) - min(x, y) for x, y in a)

    # f[i] = a - b , i in [-m, m]
    f = [float('inf')] * (2 * m + 1)
    f[0] = 0

    for x, y in a:
        f1 = [float('inf')] * (2 * m + 1)

        if x > y:
            d = x - y

            # no swap
            # a + x, b + y
            # a - b + (x - y)
            # i -> i + d
            for i in range(-m, m - d + 1):
                f1[i + d] = f[i]

            # swap
            # a + y, b + x
            # a - b - (x - y)
            # i -> i - d
            for i in range(-m + d, m + 1):
                f1[i - d] = min(f1[i - d], f[i] + 1)

        else:
            d = y - x

            # no swap
            # a + x, b + y
            # a - b - (y - x)
            # i -> i - d
            for i in range(-m + d, m + 1):
                f1[i - d] = f[i]

            # swap
            # a + y, b + x
            # a - b + (y - x)
            # i -> i + d
            for i in range(-m, m - d + 1):
                f1[i + d] = min(f1[i + d], f[i] + 1)

        f = f1

    for i in range(m + 1):
        if f[i] < float('inf') or f[-i] < float('inf'):
            return f[i]

    return -1

n = RI()
a = [tuple(RII()) for _ in range(n)]

print(solve_lg1282(n, a))