"""
https://codeforces.com/problemset/problem/1194/B

输入 T(≤5e4) 表示 T 组数据。所有数据的 n 之和 ≤5e4，n*m 之和 ≤4e5。
每组数据输入 n m(1≤n,m≤5e4 且 n*m≤4e5) 和 n 行 m 列的字符矩阵，只包含 '.' 和 '*'。

你需要把矩阵中的某些格子改成 '*'，使得矩阵中存在一个十字 '*'，即一整行和一整列都是 '*'。
输出最小修改次数。

"""
import sys
from bisect import bisect_left, bisect_right
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

def solve(m, n, mat):

    row = [0]*m
    col = [0]*n
    for i in range(m):
        for j in range(n):
            if mat[i][j] == "*":
                row[i] += 1
                col[j] += 1

    res = inf
    for i in range(m):
        for j in range(n):
            c = mat[i][j] == "*"
            res = mn(res, n + m - 1 - col[j] - row[i] + c)
    return res

for _ in range(RI()):
    m, n = RII()
    mat = [RS() for _ in range(m)]
    print(solve(m,n, mat))
