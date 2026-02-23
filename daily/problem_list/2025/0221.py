import sys
from math import inf
from typing import List
from collections import  defaultdict


sys.setrecursionlimit(10**7)
"""
0221
https://atcoder.jp/contests/abc163/tasks/abc163_f

输入 n(1≤n≤2e5) 和长为 n 的数组 a(1≤a[i]≤n)。
然后输入一棵无向树的 n-1 条边，节点编号从 1 到 n。
节点 i 的颜色是 a[i]。

定义 f(c) = 包含颜色 c 的简单路径的数目。注：只有 1 个点也算路径。
输出 f(1),f(2),...,f(n)。

- hint 正难则反，总路径 - 不包含c的路径
- 总路径=树上任意两点之间的路径 c(n,2)
- 不含c的路径，去掉c 则剩下若干连通块，连通块内部 c(m,2)
- 如何快速计算连通块的尺寸，而且对n个颜色而言。
- 如果仅是一个颜色c，则树dfs 如果根节点是c 则每个子树的连通块大小确定，然后对父节点返回0 想像这个子树从未存在


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
    # print([total - x for x in res])
    # print(res)
    # print(size)
    for i in range(n):
        component = size[i][0]
        res[i] += component * (component + 1) // 2
    # print(colors)
    # print(size)
    # print(res)

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
