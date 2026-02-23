"""
https://codeforces.com/problemset/problem/2034/C

输入 T(≤1e4) 表示 T 组数据。所有数据的 n*m 之和 ≤1e6。
每组数据输入 n(1≤n≤1e3) m(1≤m≤1e3) 和 n 行 m 列的网格图，只包含 UDLR? 五种字符，分别表示上、下、左、右和待定。

你需要对每个 ? 格子指定具体方向，即改成 UDLR 中的一种。

有 n*m 个格子可以作为移动的起点。每次移动必须遵循所在格子的方向，移动到相邻格子，或者出界。
最大化无法离开网格图（出界）的起点个数。输出这个最大值。

"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

dir = {"U":(-1,0), "D":(1,0), "L":(0,-1), "R":(0,1)}

for _ in range(RI()):
    m, n = RII()
    grid = [RS() for _ in range(m)]

    f = [[0]*n for _ in range(m)]

    vis = [[False]*n for _ in range(m)]
    def dfs(i,j):
        if i < 0 or i == m or j < 0 or j == n:
            return -1

        if f[i][j] != 0:
            return f[i][j]

        if vis[i][j] or grid[i][j] == "?":
            return 1

        dx, dy = dir[grid[i][j]]
        vis[i][j] = True
        f[i][j] = dfs(i+dx, j+dy)
        return f[i][j]

    tmp = []
    res = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == "?" and not vis[i][j]:
                tmp.append((i,j))
                continue

            if dfs(i,j) == 1:
                res += 1

    # print(res, f, tmp)
    for i,j in tmp:
        for (x,y) in ((i-1,j),(i+1,j),(i,j-1),(i,j+1)):
            if 0<=x<m and 0<=y<n and (f[x][y] == 1 or grid[x][y] == "?"):
                res += 1
                f[i][j] = 1
                break

    # print(f)

    print(res)



