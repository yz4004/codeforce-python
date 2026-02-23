"""
https://atcoder.jp/contests/abc380/tasks/abc380_e

输入 n(1≤n≤5e5) 和 q(1≤q≤2e5)。
有一条长为 n 的，有 n 个格子的纸带，其中第 i 个格子的初始颜色为 i。

然后输入 q 个询问，格式如下（1≤x≤n，1≤c≤n）：
"1 x c"：把第 x 个格子所在的连续同色段全部涂成颜色 c（类似画图软件的油漆桶工具）。比如 112233 把第三个格子涂成 4，得到 114433。
"2 c"：输出整个纸带的颜色为 c 的格子的数量。

并查集 + 在root处维护额外信息
"""
from collections import defaultdict
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

def solve(n, queries):
    pa = list(range(n+1))
    color = list(range(n+1))
    right = list(range(n+1))
    cnt = [1]*(n+1)


    def find(x):
        rt = pa[x]
        # 非递归写法
        while pa[rt] != rt:  # 1.先找根节点 只对边=1的进行路径压缩
            rt = pa[rt]

        while x != rt:  # 2. 重定向到根节点
            tmp = pa[x]
            pa[x] = rt
            x = tmp
        return rt

    def merge(a,b):
        a,b = find(a), find(b)
        if a != b:
            if a > b: a,b = b,a
            pa[b] = a
            right[a] = right[b] # b大 范围也大


    res = []
    for q in queries:
        if q[0] == 1:
            i, v = q[1], q[2]

            # 当前颜色块范围
            i = find(i)
            j = right[i]

            if color[i] == v:
                continue

            # 调整颜色+计数
            cnt[color[i]] -= j-i+1
            cnt[v] += j-i+1
            color[i] = v

            # 与块两侧合并
            if i > 1 and color[find(i-1)] == v:
                merge(i-1, i)
            if j < n and color[find(j+1)] == v:
                merge(i, j+1)
            # print([(x,y) for x,y in zip(pa, right)])
            # print(color, cnt)
            # print()
        else:
            c = q[1]
            res.append(str(cnt[c]))
    return res

n, q = RII()
queries = [tuple(RII()) for _ in range(q)]
res = solve(n, queries)

print("\n".join(res))






