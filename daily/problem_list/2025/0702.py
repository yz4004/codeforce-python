"""
https://codeforces.com/problemset/problem/2117/F

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(2≤n≤2e5) 和一棵 n 个节点的无向树的 n-1 条边。节点编号从 1 开始。

根节点为 1。
请你给每个节点分配一个点权，值为 1 或者 2。
要求：所有子树的点权和互不相同。

一共有 2^n 种点权分配方案，其中有多少个合法方案？
答案模 1e9+7。

size为n的子树 [1*n - 2*n]
父树相比其子树严格递增
但叶节点自己也可以作为子树，只要超过2 就必然有重复叶节点
则合法情况只有两类：人字形树，单链
    单链：2^n 可以任意分布, 父树相比子树都严格递增，不会出现任意子树相同值的情况
    人字形：公共部分可以任选，长分别为 m,n的两条单链 要求不能出现重复值子树
    a1 + ... am
    b1 + ... bn
    -- 自底向上考虑 1 2 然后下面只能选 3 4 5 6 ... 会发现奇偶规律

"""

import sys
from collections import Counter

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

mod = 10 ** 9 + 7

for _ in range(RI()):
    n = RI()
    g = [[] for _ in range(n)]
    indegree = [0]*n
    for _ in range(n-1):
        a,b = RII()
        a,b = a-1, b-1
        g[a].append(b)
        g[b].append(a)
        indegree[a] += 1
        indegree[b] += 1


    cnt_leaf = Counter(indegree)[1] - (indegree[0] == 1)

    if cnt_leaf == 1:
        # 单链
        print(pow(2, n, mod))
        continue

    elif cnt_leaf > 2:
        # 多叶
        print(0)
        continue

    # 人字形
    # common_part = [0]
    # branch = []
    # def dfs(i,p, l):
    #     if i != 0 and len(g[i]) == 1:
    #         branch.append(l)
    #     if len(g[i]) == 3 or (len(g[i])==2 and i==0):
    #         common_part[0] = l
    #     for j in g[i]:
    #         if j == p: continue
    #         dfs(j,i,l+1)
    # dfs(0, -1, 1)


    # 公共链
    c = 1
    p, i = -1, 0
    if len(g[0]) == 1:
        while (i != 0 and len(g[i])) == 2 or (i==0 and len(g[0]) == 1):
            nxt = g[i][0] if g[i][0] != p else g[i][1]
            p, i = i, nxt
            c += 1

    # else: 否则从根节点开始分岔

    a = b = 0
    branch = []

    for j in g[i]:
        if j == p: continue
        pj = i
        k = 1
        while len(g[j]) == 2:
            nxt = g[j][0] if g[j][0] != pj else g[j][1]
            pj, j = j, nxt
            k += 1
        branch.append(k)
    a,b = mn(branch[0], branch[1]), mx(branch[0], branch[1])
    d = b-a
    
    # c -- 两个链的公共部分
    # a,b -- 去除公共部分后 两条独立链的长度
    # d -- 长链比短链多的部分
    
    if d == 0:
        # 公共链任意，两个相等链可以互换奇偶 1357 vs 2468
        print(pow(2, c, mod) * 2 % mod)
    else:
        # 公共链任意
        # 长链取偶数，短链取奇数 135 vs 246 [d长度任意]
        # 长链取奇数，短链取偶数 246 vs 1357 [d-1长度任意]
        # 1357
        # 2468
        subchains = pow(2, d-1, mod) + pow(2, d, mod)
        print(pow(2, c, mod) * subchains % mod ) 




