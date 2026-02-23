import sys
from math import inf
from typing import List
from collections import  defaultdict


sys.setrecursionlimit(10**7)
"""
0219
https://atcoder.jp/contests/abc100/tasks/abc100_d

输入 n(1≤n≤1000) m(0≤m≤n) 和一个 n 行 3 列的矩阵 a。

从 n 行中选择 m 行，输出 abs(第一列元素和) + abs(第二列元素和) + abs(第三列元素和) 的最大值。

"""
def solve(n, colors, edges):
    g = [[] for _ in range(n)]
    for a,b in edges:
        g[a].append(b)
        g[b].append(a)

    subtree_size = [0]*n
    def dfs(i, p):
        subtree_size[i] = 1
        for j in g[i]:
            if j == p: continue
            dfs(j, i)
            subtree_size[i] += subtree_size[j]
    dfs(0, -1)

    res = [0]*n
    size = [[n] for _ in range(n)]
    def dfs(i, p):
        # 考虑不含颜色c的连通块尺寸
        # 当前color[i] = c 往下看当前不包含c的连通块应该是 子树size - 子树中以c为颜色的root
        c = colors[i]
        for j in g[i]:
            if j == p: continue
            size[c].append(subtree_size[j])
            dfs(j, i)
            component = size[c].pop() # 当前不含c的连通块，所有路径 c(m,2) + m = m * (m-1) // 2 + m
            res[c] += component * (component + 1) // 2

        size[c][-1] -= subtree_size[i]
        # print(i,p, c, subtree_size[i], "--", size, res, res[c])
    dfs(0, -1)
    total = n * (n + 1) // 2

    for i in range(n):
        component = size[i][0]
        res[i] += component * (component + 1) // 2
    return [total - x for x in res]




Test = False
if Test:
    ########################## 本地调试部分 读取同目录下的 input.txt 数据
    # 输入部分
    with open("../input.txt", "r") as file:
        sys.stdin = file
        input = sys.stdin.read
        data = input().splitlines()

        ###############################################
        n = int(data[0])
        colors = list(map(lambda x: int(x)-1, data[1].split())) # 也转换为0-base
        edges = []
        for i in range(n - 1):
            a, b = map(int, data[2 + i].split())
            edges.append((a - 1, b - 1))

        result = solve(n, colors, edges)
        for x in result:
            sys.stdout.write(str(x) + "\n")
        ###############################################

        sys.exit()

input = sys.stdin.read
data = input().splitlines()

###############################################
n = int(data[0])
colors = list(map(lambda x: int(x) - 1, data[1].split()))  # 也转换为0-base
edges = []
for i in range(n - 1):
    a, b = map(int, data[2 + i].split())
    edges.append((a - 1, b - 1))

result = solve(n, colors, edges)
for x in result:
    sys.stdout.write(str(x) + "\n")
###############################################
