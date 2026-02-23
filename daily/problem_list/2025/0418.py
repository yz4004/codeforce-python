"""
https://codeforces.com/problemset/problem/1866/K

输入 n(2≤n≤1e5) 和一棵无向树的 n-1 条边（节点编号从 1 开始），每条边包含 3 个数 x y z(1≤z≤1e9)，表示有一条边权为 z 的边连接 x 和 y。
然后输入 q(1≤q≤1e5) 和 q 个询问，每个询问输入 x 和 k(1≤k≤1e9)。

询问之间互相独立（每个询问都是在初始树上操作的）。
把所有与 x 相连的边的边权都乘以 k，
然后输出这棵树的直径。

假设对根节点临边进行放大 （无父节点的情况下）
    [(wi,di)...]
    k*wi + di -- 选取mx smx

    (xi,yi) = (wi,di)
    k*wi + di =  xi*k + yi
    max(xi*k + yi, for i)



"""
import sys, itertools
from math import inf, isqrt, gcd
from bisect import bisect_left
from collections import deque, defaultdict
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x


n = RI()
g = [[] for _ in range(n)]
for _ in range(n-1):
    a,b,w = RII()
    a,b = a-1, b-1
    g[a].append((b,w))
    g[b].append((a,w))

pa = [-1]*n
depth = [None]*n #depth[i] i-子树最大次大枝条
o_diameter = [0]
def dfs(i, p) -> int:
    pa[i] = p

    m1 = m2 = 0
    for j, wj in g[i]:
        if j == p: continue
        r = dfs(j, i) + wj
        if r >= m1:
            m1, m2 = r, m1
        elif r > m2:
            m2 = r
    o_diameter[0] = mx(o_diameter[0], m1 + m2)
    depth[i] = (m1, m2)
    return m1
dfs(0, -1)

# print(g)
# print(depth)
# print("--"*10)

# 换根dp 处理来自父节点的
convex1 = [None]*n
convex2 = [None]*n
sub = lambda x,y : (x[0]-y[0], x[1]-y[1])
cross = lambda x,y: x[0]*y[1] - x[1]*y[0]
def get_upper_convex(pts):
    pts.sort()
    st = []
    for cur in pts:
        # (st[-2], st[-1], cur)
        while len(st) >= 2 and cross(sub(st[-2], st[-1]), sub(st[-1], cur)) > 0:
            st.pop()
        st.append(cur)
    return st
def dfs(i, p, wp, dp) -> (int, int):
    # dp 父节点传来的最大枝条 (不算临近边)
    # wp 最大枝条对应的临近边

    pts = []
    if i != 0:
        pts.append((wp, dp))

    # 1. 收集所有点集 (wi, di), di是子节点最大枝条，wi是到达子节点对应边
    # 2.1 整理最大次大di
    for j, wj in g[i]:
        if j == p: continue
        pts.append((wj, depth[j][0]))

    #print(i, wp, dp, pts)

    # 2.2 根据最大次大进行换根, 递归进j传入父节点i除了j分支的最大分支 （含上层传来）
    tmp = sorted((depth[i][0], depth[i][1], dp+wp))  # 最大次大子树枝条
    d1, d2 = tmp[-1], tmp[-2]
    for j, wj in g[i]:
        if j == p: continue
        branch = depth[j][0] + wj
        if branch == d1:
            dfs(j,i, wj, d2)
        else:
            dfs(j,i, wj, d1)

    # 3. 整理外层上凸包 去掉外层后的内层点集的上凸包 - 内层上凸包
    convex1[i] = get_upper_convex(pts)
    pts2 = [p for p in pts if p not in set(convex1[i])]
    convex2[i] = get_upper_convex(pts2)

dfs(0, -1, 0, 0)
# print(convex1)
# print(convex2)

# f(x,y) = y + k*x
dot = lambda p, k: p[1] + p[0]*k
def query(x, k):
    # x所有临边 * k
    hull1, hull2 = convex1[x], convex2[x]
    def check(hull):
        l,r = 0, len(hull)-1
        while r - l > 2:
            m1 = l + (r - l) // 3
            m2 = r - (r - l) // 3
            if dot(hull[m1], k) < dot(hull[m2], k):
                l = m1
            else:
                r = m2
        best = l
        for i in range(l + 1, r + 1):
            if dot(hull[i], k) > dot(hull[best], k):
                best = i
        return best #hull[best]
    b1 = check(hull1)
    b2 = check(hull2)

    m1 = dot(hull1[b1], k)
    m2 = dot(hull2[b2], k) if hull2 else 0

    # print(b1, hull1, hull1[b1], m1)
    # print(b2, hull2, hull2[b2] if hull2 else None, m2)

    for b in (b1-1, b1+1):
        if 0 <= b < len(hull1) and dot(hull1[b], k) > m2:
            m2 = dot(hull1[b], k)

    return m1 + m2

# print("__"*10)
q = RI()
for _ in range(q):
    x, k = RII()
    r = query(x-1, k)
    # print(x-1, k, r)
    print(mx(o_diameter[0], r))


# print(cross((1,1), (1,-1)))











