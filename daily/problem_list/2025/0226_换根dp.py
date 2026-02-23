import sys
from collections import defaultdict
from math import inf
from typing import List

"""
https://atcoder.jp/contests/abc348/tasks/abc348_e

输入 n(1≤n≤1e5)。
输入一棵无向树的 n-1 条边，边权为 1，节点编号从 1 到 n。
输入长为 n 的数组 a(1≤a[i]≤1e9)。

定义 f(x) = sum(dist(x, i) * a[i] for i in [1, n])，其中 dist(x, i) 表示 x 到 i 的最短路长度。

输出 f(1),f(2),...,f(n) 中的最小值。

- 树上的全局问题 考虑换根
- 假设从0点出发，已经算出了子树的f值，当向一个子树转移时，其他子树的所有距离增加1，但f值增量只是其他子树的所有value之和
- 可以想见本题如果dist有权值，转移也是可以做的
"""

sys.setrecursionlimit(10**7)

def solve(n, edges, nums):

    g = [[] for _ in range(n)]
    for a,b in edges:
        a,b = a-1, b-1
        g[a].append(b)
        g[b].append(a)

    # 1. 从0出发的所有f值，2. 每个子树的所有value和
    s = [0]*n
    def dfs(i, p, dist):
        res = dist * nums[i]
        value_sum = nums[i]
        for j in g[i]:
            if j == p: continue
            a, b = dfs(j, i, dist + 1)
            res += a
            value_sum += b
        s[i] = value_sum
        return res, value_sum

    res = f = dfs(0, -1, 0)[0]

    def dfs(i, p, f): # f即为当前i节点对应的目标值，和res取min
        nonlocal res
        res = min(res, f)

        pre_values = s[0] - s[i] # 除了i子树以外所有祖先的value sum. i转移到子节点j时，这些pre_val 对应的dist都加一 （j-i的权值)
        for j in g[i]:
            if j == p: continue
            # i向下转移给j，f的三种变化
            # 1. i祖先边远 + pre_value
            # 2. j的peer子树距离边远 + s[i] - s[j]
            # 3. j的子树边近 - s[j]
            dfs(j, i, f + pre_values + (s[i] - s[j]) - s[j])
    dfs(0, -1, f)
    return res


Test = False
if Test:
    ########################## 本地调试部分 读取同目录下的 input.txt 数据
    # 输入部分
    with open("../input.txt", "r") as file:
        sys.stdin = file
        input = sys.stdin.read
        data = input().splitlines()

        ###############################################
        # n个点
        n = int(data[0])
        edges = []
        for i in range(1, n):
            edges.append(list(map(int, data[i].split())))
        nums = list(map(int, data[n].split()))
        result = solve(n, edges, nums)

        # 输出结果
        sys.stdout.write(str(result))
        # sys.stdout.write(' '.join(map(str, result)) + '\n')
        ###############################################


        sys.exit()

input = sys.stdin.read
data = input().splitlines()

###############################################
n = int(data[0])
edges = []
for i in range(1, n):
    edges.append(list(map(int, data[i].split())))
nums = list(map(int, data[n].split()))
result = solve(n, edges, nums)

# 输出结果
sys.stdout.write(str(result))
###############################################
