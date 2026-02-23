import sys
# sys.setrecursionlimit(10**7)

# input = sys.stdin.read
# data = input().splitlines()
m, n, q = map(int, input().split())
grid = [input() for _ in range(m)]

ps_node = [[0]*(n+1) for _ in range(m+1)] # ps_node[i][j] -- grid[:i][:j] 蓝色格点数量
ps_edge = [[0]*(n+1) for _ in range(m+1)] # ps_node[i][j] -- grid[:i][:j] 内部蓝色格点共享边数

v = [[0]*(n+1) for _ in range(m+1)] # v[i][j] 第i-column
h = [[0]*(n+1) for _ in range(m+1)] # h[i][j]

for i in range(m):
    for j in range(n):
        ps_node[i+1][j+1] = ps_node[i+1][j] + ps_node[i][j+1] - ps_node[i][j] + (1 if grid[i][j] == "1" else 0)
        if grid[i][j] == "1":
            d = (1 if 0 <= i-1 and grid[i-1][j] == "1" else 0) \
                + (1 if 0 <= j-1 and grid[i][j-1] == "1" else 0)
        else:
            d = 0
        ps_edge[i+1][j+1] = ps_edge[i+1][j] + ps_edge[i][j+1] - ps_edge[i][j] + d

        v[i + 1][j + 1] = v[i][j + 1] + (1 if grid[i][j] == "1" and j + 1 < n and grid[i][j + 1] == "1" else 0)
        h[i + 1][j + 1] = h[i + 1][j] + (1 if grid[i][j] == "1" and i + 1 < m and grid[i + 1][j] == "1" else 0)

for _ in range(q):
    a,b,c,d = map(lambda x: int(x)-1, input().split())
    nodes = ps_node[c+1][d+1] - ps_node[a][d+1] - ps_node[c+1][b] + ps_node[a][b]
    edges = ps_edge[c+1][d+1] - ps_edge[a][d+1] - ps_edge[c+1][b] + ps_edge[a][b]
    bound = h[a][d+1] - h[a][b] + v[c+1][b] - v[a][b]
    print(nodes - edges + bound)



"""
可以前缀和查询点数，但如何知道连通块数量, 且截取的矩形会把原图上的连通块分成多个部分（但切分开仍是树）
- 树的性质, 点数=边数+1. 多棵树，点数边数之差即为树的个数
- 两个相邻的蓝色格点构成了一条树边
- 分别统计格点/边数 
"""
