"""
https://codeforces.com/problemset/problem/2093/D

输入 T(≤10) 表示 T 组数据。所有数据的 q 之和 ≤2e4。
每组数据输入 n(1≤n≤30)。

同 周赛第二题，你需要在一个 2^n * 2^n 大小的网格中填数字，顺序是左上 - 右下 - 左下 - 右上。

输入 q(1≤q≤2e4) 和 q 个询问，格式如下：
"-> x y"：输出 x 行 y 列所填数字是多少。
"<- d"：输出数字 d 所在行列编号。
行列编号从 1 开始，所填数字从 1 开始。

-
"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

def solve(n, queries):
    """
    2^n * 2^n
    a  d
    c  b
    a < b < c < d
    """
    def dfs1(x,y, x1,y1,x2,y2,base):
        # [x1,y1] * [x2,y2]
        mx, my = (x1+x2)//2, (y1+y2)//2





    for q in queries:
        if len(q) == 2:
            pass


N = RI()
for _ in N:
    n, Q = RI(), RI()
    queries = []
    for _ in range(Q):
        q = RS()
        qry = []
        if q[0] == ">":
            a,b = map(int, q[3:].strip().split())
            qry.append((a,b))
        else:
            a = int(q[3:].strip())
            qry.append((a))
    solve(n, qry)


