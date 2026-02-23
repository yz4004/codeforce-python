"""
https://codeforces.com/problemset/problem/605/D

输入 n(1≤n≤1e5) 和 n 张魔法卡，每张魔法卡包含四个整数 a,b,c,d，范围 [0,1e9]。

你在二维坐标系中，设当前位置为 (x,y)。
每一步，你可以选择一张满足 a<=x 且 b<=y 的魔法卡，传送到 (c,d)。

一开始，你在 (0,0)。
你的目标是使用第 n 张魔法卡。

如果无法做到，输出 -1。
否则：
第一行，输出最少使用的魔法卡个数（包含第 n 张魔法卡）。
第二行，按顺序输出你使用的魔法卡的下标（编号从 1 到 n），最后一张卡一定是 n。

最后一个点，查询包含 ab 的所有点的最小步骤 (x,y) x,y >= a,b
bfs 正向搜索，每个点能到达的点 -- 其保住的区域的桥点 ab 的 cd
如何搜索每个x,y包含的桥点
    先按桥点排序，a,b,c,d
    枚举到某个c,d (他是被跳到的点) 考虑前面遍历的 ab

"""
import sys
from bisect import bisect_left
from collections import defaultdict, deque
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n = RI()
pts = []
xs, ys = {0}, {0}
for _ in range(n):
    a,b,c,d = RII()
    pts.append((a,b,c,d))

    xs.add(a)
    xs.add(c)
    ys.add(b)
    ys.add(d)

xs = sorted(list(xs))
ys = sorted(list(ys))

groups = defaultdict(list)
new_pts = []
for i, (a,b,c,d) in enumerate(pts):
    a, c = bisect_left(xs, a), bisect_left(xs, c)
    b, d = bisect_left(ys, b), bisect_left(ys, d)
    groups[a].append((b,i))
    new_pts.append((c,d))

for i in groups:
    groups[i].sort(key=lambda bi: bi[0])

pts = new_pts
m = len(xs)

# x,y 每次所处的位置，尝试从包含的区域中
q = deque([(0,0,-1)])
class SegmentTreeMin:  # min
    def __init__(self, n):
        self.t = [inf] * (4 * n)
    ##############################################
    def pull(self, p):  # up 子信息汇总p <- 2*p, 2*p+1
        self.t[p] = min(self.t[2 * p], self.t[2 * p + 1]) # 更新min

    def apply(self, p, i, v): # 单点更新逻辑
        self.t[p] = v # 覆盖原有信息

    def update_single(self, p, l, r, i, v):
        # print((p,l,r), i,v)
        if l == i == r:
            self.apply(p, i, v)  # 单点更新
            return
        mid = (l + r) // 2
        if i <= mid:
            self.update_single(2 * p, l, mid,         i, v)
        if mid < i:
            self.update_single(2 * p + 1, mid + 1, r, i, v)
        self.pull(p)

    def query(self, p, l, r, L, R): # 查询 [L,R] 区间最小值
        if L <= l and r <= R:
            return self.t[p]
        res = inf
        mid = (l + r) // 2
        if L <= mid:
            res = min(res, self.query(2 * p, l, mid, L, R))
        if mid < R:
            res = min(res, self.query(2 * p + 1, mid + 1, r, L, R))
        return res

    def find_first_idx_smaller_than_v(self, p, l, r, v):  # 线段树二分，找到从左往右第一个小于等于v的索引
        if self.t[p] > v:  # (p,l,r) 维护区间最小值都大于v 跳过这段区间
            return -1
        if l == r:  # 找到自左往右第一个满足的索引
            return l

        mid = (l + r) // 2
        i = self.find_first_idx_smaller_than_v(2 * p, l, mid, v)
        if i == -1:
            i = self.find_first_idx_smaller_than_v(2 * p + 1, mid + 1, r, v)
        return i


tree = SegmentTreeMin(m) # [0,m]
line = [0]*m
prev = [-1]*n

for i in range(m):
    if groups[i]:
        first_b = groups[i][0][0]  # 桶里最小的 b_idx
    else:
        first_b = inf
    tree.update_single(1, 0, m-1, i, first_b)

found = False
while q:
    x,y,cur = q.popleft()

    # 线段树维护小于x的区间最小值，如果小于y则作为ab加入

    # [,x]
    while True and not found:
        i = tree.find_first_idx_smaller_than_v(1, 0, m-1, y)
        #print((x, y, cur), i, i > x)
        if i == -1 or i > x: break

        j = line[i]
        grp = groups[i]  # x -> (y, idx)

        while j < len(grp) and grp[j][0] <= y:
            idx = grp[j][1]
            prev[idx] = cur
            if idx == n-1:
                found = True
                break

            c,d = pts[idx]
            q.append((c,d,idx))
            j += 1


        if found:
            break

        line[i] = j
        if j < len(grp):
            tree.update_single(1, 0, m-1, i, grp[j][0])
        else:
            tree.update_single(1, 0, m-1, i, inf)

if found:
    path = []
    t = target = n-1
    while t != -1:
        path.append(t)
        t = prev[t]
    path.reverse()
    print(len(path))
    print(" ".join(str(x+1) for x in path))
else:
    print(-1)









