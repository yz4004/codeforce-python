"""
https://codeforces.com/problemset/problem/1914/D

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤1e5。
每组数据输入 n(3≤n≤1e5) 和一个 3 行 n 列的矩阵，元素范围 [1,1e8]。

从矩阵每行选恰好一个数，要求任意两个数不在同一列。
输出所选元素之和的最大值。

"""
import itertools
import sys
from functools import cache
from operator import add, xor
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

def solve(mat, n): # 3*n

    def get_top3(row):
        m1 = m2 = m3 = 0
        i1 = i2 = i3 = -1
        for i, x in enumerate(row):
            if x >= m1:
                m3, i3 = m2, i2
                m2, i2 = m1, i1
                m1, i1 = x, i
            elif x >= m2:
                m3, i3 = m2, i2
                m2, i2 = x, i
            elif x > m3:
                m3, i3 = x, i

        return [(i1, m1), (i2, m2), (i3, m3)]

    tmp = [get_top3(row) for row in mat]
    res = 0
    for i, x in tmp[0]:
        for j, y in tmp[1]:
            for k, z in tmp[2]:
                if len({i, j, k}) == 3:
                    # return x+y+z
                    res = max(res, x+y+z)
    return res

for _ in range(RI()):
    n = RI()
    mat = [RILIST() for _ in range(3)]
    print(solve(mat, n))

sys.exit(0)
def solve(mat, n): # 3*n
    def get_top3(row):
        m1 = m2 = m3 = 0
        for i, x in enumerate(row):
            if x > m1:
                m3 = m2
                m2 = m1
                m1 = x
            elif m1 > x > m2:
                m3 = m2
                m2 = x
            elif m2 > x > m3:
                m3 = x
        return m1,m2,m3

    res = -1
    for m1 in get_top3(mat[0]):
        l0 = set(i for i in range(n) if mat[0][i] == m1)

        for m2 in get_top3(mat[1]):

            l1 = set(i for i in range(n) if mat[1][i] == m2)
            l0_1 = l0.union(l1)

            for m3 in get_top3(mat[2]):
                l2 = set(i for i in range(n) if mat[2][i] == m3)
                if len(l0_1.union(l2)) >= 3:
                    res = max(res, m1+m2+m3)
    return res

for _ in range(RI()):
    n = RI()
    mat = [RILIST() for _ in range(3)]
    print(solve(mat, n))





