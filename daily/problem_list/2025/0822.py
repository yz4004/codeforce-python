"""
https://codeforces.com/problemset/problem/348/C

输入 n m q(1≤n,m,q≤1e5) 和长为 n 的数组 a(-1e8≤a[i]≤1e8)。
然后输入 m 个下标集合：对于每个集合，首先输入集合大小 k，然后输入 k 个互不相同的 [1,n] 中的下标。保证所有集合的大小之和 ≤1e5。
然后输入 q 个询问，格式如下：
"+ k x"：把第 k(1≤k≤m) 个下标集合中的 a[i] 都增加 x(-1e8≤x≤1e8)。
"? k"：输出第 k(1≤k≤m) 个下标集合中的 a[i] 之和。

注：如果两个集合 A 和 B 有交集，那么增加集合 A 的 a[i]，会影响集合 B 的 a[i] 之和。

对整个下标集合整体加x 如果下标集大，则挨个枚举不可以。
以集合的尺寸分界，小于 B=sqrt(n) 的小组直接在原数组上暴力枚举，大于B的大组则维护整组的和
下标集总和不超过 n=1e5, 约有m=1e5个组， 大组数量不超过 sqrt(n)
小组的 修改 查询均在a上直接操作
大组的修改对每个组单独维护加和 （一个lazy tag整数）
同时大组直接重叠形成 B size 图. A,B 重叠点数记一个边权，每次A+x 则按边权populate给B. w*x, 每次对集合修改，只对所有邻居集合（即有重点的）populate 不超过 B=sqrt(n)
查询一个大组，即lazy tag

小组的修改对每个点也记录多少个大组share这个点，单词populate复杂度也不超过 sqrt(n)
小组的查询也要对每个点查对应大组在该点上修改之和

对小组的单次修改
点遍历a上更新sqrt(n) * 每个点的populate到大组 sqrt(n)

对大组的单次修改
本人O(1) 懒更新 + 有重边大组的 populate sqrt(n)

对小组的单次查询
点遍历a上查询sqrt(n) - 查a的值=代表原a和所有小组修改 + 每个点对应大组的修改之和

对大组的单次查询
lazy tag + 本人修改次数 - O(1)


"""
import itertools
import sys
from collections import defaultdict
from math import isqrt

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n, M, Q = RII()
a = RILIST()

B = isqrt(n)

size = [0]*M
points = [None]*M

big = {}


ptos = [[] for _ in range(n)]
for s in range(M):
    cur = RILIST()
    size[s] = k = cur[0]
    points[s] = [i-1 for i in cur[1:]]

    if k > B:
        for i in points[s]:
            ptos[i].append(s)
        big[s] = sum(a[i] for i in points[s])

# 点overlap，g[s1][s2]  交点数
g = defaultdict(lambda: defaultdict(int))
for i in range(n):
    cur_big = ptos[i] # 经过该点的所有大集合 （不超过sqrt(m))

    for p,q in itertools.combinations(cur_big, 2):
        g[p][q] += 1
        g[q][p] += 1


add = {s:0 for s in big}
for _ in range(Q):
    operation, *arg = RS().strip().split()
    if operation == "?":
        # 查询集合 s 的点和
        s = int(arg[0])-1
        if size[s] <= B:
            # 小集合：遍历a + 每个点被大集合懒加
            res = 0
            for i in points[s]:
                res += a[i]
                for s1 in ptos[i]:
                    res += add[s1]
        else:
            # 大集合：已经被维护在big里
            res = big[s]

        print(res)

    else:
        s, k = map(int, arg)
        s -= 1

        if size[s] <= B:
            # 小集合加：每个点加 + 维护经过每个点的大集合的和
            for i in points[s]:
                a[i] += k
                for s1 in ptos[i]:
                    big[s1] += k

        else:
            # 大集合加：
            add[s] += k
            big[s] += size[s] * k
            for s2, cnt in g[s].items():
                big[s2] += cnt * k