"""
https://codeforces.com/problemset/problem/593/D

输入 n(2≤n≤2e5) m(1≤m≤2e5)。
然后输入一棵无向树的 n-1 条边（节点编号从 1 到 n），每条边包含 3 个数 x y z(1≤z≤1e18)，表示有一条边权为 z 的边连接 x 和 y。

然后输入 m 个操作，格式如下：
"1 x y val"：其中 1≤val≤1e18。依次经过从 x 到 y 的最短路上的边，每经过一条边，就把 val 更新为 floor(val / 边权)。你需要输出最终的 val。
"2 i z"：把输入的第 i(1≤i≤n-1) 条边的边权改为（减小为）z(1≤z<旧边权)。

key:
1. 离散除法也满足结合律 - 单步除和整体除是一样的 n/(xy) = (n/x)/y
2. 除法log下降


1. n/(xy) = (n/x)/y
    即使有floor 单独除每段等于整体除

    n = k*xy + r
    n/x = k*y + (r/x) ... r=px+r1  where r<xy  r1<x
    这一步可以分开 前半部分可以对x约 所以可以单独拆开剩余 k*y
    (n/x)/y = k + p/y
    同理k也可以拆开，p/y一定是0 如果p>y 代入上面r 与r<xy矛盾

2. 如果x-y预处理lca  x-lca-y 只要查询两次 x-lca的边权积
    但若有修改 如何维护 x-lca
    本质是每个x维护自己上方 2^0 2^1 ... 2^k 个祖先的距离 想像一条单链的情况 x-y 修改会导致很多其下方的点 2^i 需要修改

3. 除法下降 = logn
    除k>1 如果减小到0 以后一直是0. 除1不会变化
    而除法下降是log (除以2就是log 除以>2 更快)
    log下降意味着对单个val暴力也只是log级别 - val一旦下降到0 就不再变化
    上述条件只在边=1时失效 避免长距离不下降 要跳过连续1段 - 整段合并

"""
from collections import defaultdict, deque
import sys
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 998244353

def solve(n, m, edges, queries) -> List[int]:

    pa = [-1]*n
    pa[0] = 0
    wt = [None]*n

    g = [[] for _ in range(n)]
    for idx, (a,b,w) in enumerate(edges):
        a,b = a-1, b-1
        g[a].append((b,w,idx))
        g[b].append((a,w,idx))

    mp = [0] * len(edges) # edge index -> wt index
    def bfs(rt=0): # 从rt为根出发建树
        inque = [False]*n
        inque[rt] = True
        q = deque([rt])
        while q:
            i = q.popleft()
            for j,w, idx in g[i]:
                if inque[j]: continue
                wt[j] = w
                pa[j] = i
                mp[idx] = j
                q.append(j)
                inque[j] = True
    bfs(0)


    def find(x):
        rt = pa[x]
        # 非递归写法
        while pa[rt] != rt and wt[rt] == 1:  # 1.先找根节点 只对边=1的进行路径压缩
            rt = pa[rt]

        while x != rt:  # 2. 重定向到根节点
            tmp = pa[x]
            pa[x] = rt
            x = tmp
        return rt

    def merge(x,y):
        x,y = find(x), find(y)
        if x != y:
            pa[x] = y

    res = []
    for q in queries:
        if q[0] == 1:
            x,y,val = q[1:]
            x,y = x-1, y-1

            # 从x出发 val log下降的所有祖先 xy 分别找最近公共祖先 vis应该优化
            i = x
            tx = 1
            vis = {}
            while True:
                vis[i] = tx  # 记录 x -> i 路径乘积
                if i == 0 or tx > val:
                    break
                tx *= wt[i] # x -> pa[x] 的积算入tx
                # i = pa[i]
                i = find(i) # 路径压缩 跳过边=1的部分

            t = -1
            j = y
            ty = 1
            while True:
                # t: y->j 路径乘积
                if j in vis:
                    t = vis[j] * ty
                    break
                if j == 0 or ty > val:
                    break
                ty *= wt[j]
                # j = pa[j]
                j = find(j)

            if t == -1:
                res.append(0)
            else:
                res.append(val//t)
        else:
            idx,val = q[1:]
            idx = idx-1

            i = mp[idx]
            j = pa[i]
            wt[i] = val

            if val == 1:
                merge(i, j)

    return res










n, m = RII()
edges = [tuple(RII()) for _ in range(n-1)]
queries = [tuple(RII()) for _ in range(m)]
res = solve(n,m,edges,queries)
print("\n".join(map(str, res)))
