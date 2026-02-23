"""
https://codeforces.com/problemset/problem/679/C

输入 n(1≤n≤500) k(1≤k≤n) 和一个 n 行 n 列的网格图，只包含 .（表示空地）和 X（表示障碍）。

你可以把一个 k*k 大小的区域中的格子全部变成空地。这个操作只能执行一次。

输出操作后，网格图的最大空地连通块的大小（连通块的空地个数）。
注：网格图是上下左右四连通的。
"""
import sys
from math import inf
from collections import defaultdict, deque

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n, k = RII()
k2 = k*k
mat = [[None]*n for _ in range(n)]
for i in range(n):
    for j, c in enumerate(RS()):
        mat[i][j] = c


pa = [[None]*n for _ in range(n)]
size = [[0]*n for _ in range(n)]
def bfs(x0,y0):
    q = deque([(x0,y0)])
    mat[x0][y0] = "X"
    area = 1
    a,b,c,d = inf,-1,inf,-1
    while q:
        i,j = q.popleft()
        pa[i][j] = (x0,y0)
        a,b,c,d = mn(a,i), mx(b,i), mn(c,j), mn(d,j)
        for x,y in ((i-1,j),(i+1,j),(i,j-1),(i,j+1)):
            if 0 <= x < n and 0 <= y < n and mat[x][y] == ".":
                mat[x][y] = "X"
                area += 1
                q.append((x,y))
        size[x0][y0] = area

for i in range(n):
    for j in range(n):
        if mat[i][j] == "." and pa[i][j] is None:
            bfs(i,j)

def inc_count(block_set, block_index):
    if block_index:
        block_set[block_index] += 1
def dec_count(block_set, block_index):
    if block_index:
        block_set[block_index] -= 1
        if block_set[block_index] == 0:
            del block_set[block_index]


res = 0 # max(block.values())
for i in range(n-k+1): # [n-k,n-1]

    # 减去窗口内的
    for r in range(i,i+k):
        for c in range(0, k-1):
            if pa[r][c]:
                x,y = pa[r][c]
                size[x][y] -= 1

    # [0,n-k-2]
    up = defaultdict(int)
    if i > 0:
        for c in range(k-1):
            inc_count(up, pa[i-1][c])

    lo = defaultdict(int)
    if i + k < n:
        for c in range(k-1):
            inc_count(lo, pa[i+k][c])


    for j in range(0,n-k+1):
        # [i,i+k) * [j,j+k)
        # area = ps[i+k][j+k] - ps[i][j+k] - ps[i+k][j] + ps[i][j]

        # 右侧一列纳入窗口
        for r in range(i,i+k):
            c = j+k-1
            if pa[r][c]:
                x,y = pa[r][c]
                size[x][y] -= 1

        # 上下边界新增右侧接触
        if i > 0:
            inc_count(up, pa[i-1][j+k-1])

        if i+k < n:
            inc_count(lo, pa[i+k][j + k - 1])

        # 右边界新增 [i,i+k-1][j+k]
        right = defaultdict(int)
        if j+k < n:
            for r in range(i,i+k):
                inc_count(right, pa[r][j+k])

        # 左边界新增 [i,i+k-1][j-1]
        left = defaultdict(int)
        if j-1 >= 0:
            for r in range(i,i+k):
                inc_count(left, pa[r][j-1])

        # 四周接触的【不同区块】面积之和
        bks = set(p for e in (up,lo,left,right) for p in e)
        s = sum([size[r][c] for r,c in bks]) + k2
        res = mx(res, s)
        #print(i,j, (i,i+1), "*", (j,j+k), bks, s)

        # 上下边界移除左侧
        if i > 0:
            dec_count(up, pa[i-1][j])

        if i+k < n:
            dec_count(lo, pa[i+k][j])

        # 左侧一列离开窗口
        for r in range(i,i+k):
            c = j
            if pa[r][c]:
                x,y = pa[r][c]
                size[x][y] += 1

    for r in range(i,i+k):
        for c in range(n-k+1, n): # n-(k-1) ... n-1
            if pa[r][c]:
                x,y = pa[r][c]
                size[x][y] += 1
print(res)


