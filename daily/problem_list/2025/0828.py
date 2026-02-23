"""
https://codeforces.com/contest/2075/problem/D

输入 T(≤1e5) 表示 T 组数据。
每组数据输入 x(0≤x≤1e17) 和 y(0≤y≤1e17)。

每次操作，选择一个正整数 k，把 x 变成 floor(x / pow(2,k))，或者把 y 变成 floor(y / pow(2,k))。这个操作的代价是 pow(2,k)。
所有操作中的 k 必须互不相同。

输出使 x 等于 y 的最小总代价。

x = (ai * 2^i + ... a0 * 2^0)
floor(x / a^k) 相当于右移k位 -- 2^(i-k) for i < k 就floor成0

最后转化为 x==y 即x,y二进制表示的某个prefix，越长越好，但x操作 t1次 y操作 t2次 需由不同的k表示出

t1 = k1 + k2 ... kt
t2 = ...

"""
import sys
from bisect import bisect_left
from collections import defaultdict
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 998244353

# f[i][j] 凑够 i j 且选择方案不重 利用前k个元素 1...k
# 1e18 = (10^3)^6 = 2^60
n = 61
f = [[inf] * (n + 1) for _ in range(n + 1)]
f[0][0] = 0

for k in range(1, n + 1):
    # k 前k个1-k 01背包的凑出 (i,j) 的最小花费
    for i in range(n, -1, -1):
        for j in range(n, -1, -1):
            tmp1 = inf if i < k else f[i - k][j] + (1<<k)
            tmp2 = inf if j < k else f[i][j - k] + (1<<k)
            f[i][j] = mn(f[i][j], mn(tmp1, tmp2))


for _ in range(RI()):
    x, y = RII()
    # x -> floor(x / 2^k)
    # y -> floor(y / 2^k)


    if x == y:
        print(0)
        continue

    if x > y:
        x, y = y, x

    m = x.bit_length()
    n = y.bit_length()

    res = inf
    for i in range(61):
        for j in range(61):
            if x >> i == y >> j:
                res = mn(res, f[i][j])
    # ps最大公共前缀并不充分
    print(res)


    # j = n-1
    # for i in range(m-1, -1, -1):
    #     # [,i]
    #     if y >> j != x >> i:
    #         break
    #     j -= 1
    # d = y.bit_length() - 1 - j

    # g = [[f[i][j] for j in range(n + 1)] for i in range(n + 1)]
    # for i in range(n, -1, -1):
    #     for j in range(n, -1, -1):
    #         tmp = mn(g[i + 1][j] if i < n else inf, g[i][j + 1] if j < n else inf)
    #         g[i][j] = mn(g[i][j], tmp)
    # res = g[m][n]  #inf # 任何大于 f[x][y] x>m y>n 的最小值
    # for i in range(d+1):
    #     res = mn(res, f[m-d][n-d])
    # print(res)




# query type
# type1. revenue, referee (0-k, or -1 for none)
# type2. revenue, lowest_k

queries = []
from sortedcontainers import SortedList
sl = SortedList()  #
revenue = {}
u = 0

for q in queries:
    if q[0] == 1:
        r, referee = q[1], q[2]

        revenue[u] = r
        sl.append((r,u))
        u += 1

        if referee != -1:
            cur = revenue[referee]
            sl.remove((cur,referee)) # logn
            sl.add((cur+r, referee)) # logn
            revenue[referee] += r

    else:
        r, k = q[1], q[2]

        j = bisect_left(sl, r) # sl[j] >= r
        print(sl[j:j+k])
        # logn + k
    # n * (logn + k)
    # n * n


m = 10 ** 5
tree_cnt = BIT(m)
tree_sum = BIT(m)

cnt = tree_cnt.sum(x) # < x
v = tree_cnt.lower_bound(cnt) # lowest k



for q in queries:
    if q[0] == 1:
        r, referee = q[1], q[2]

        revenue[u] = r
        sl.append((r,u))
        u += 1

        if referee != -1:
            cur = revenue[referee]
            sl.remove((cur,referee)) # logn
            sl.add((cur+r, referee)) # logn
            revenue[referee] += r

    else:
        r, k = q[1], q[2]

        j = bisect_left(sl, r) # sl[j] >= r
        print(sl[j:j+k])
