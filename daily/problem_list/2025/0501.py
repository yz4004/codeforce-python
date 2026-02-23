"""
https://www.luogu.com.cn/problem/P3694

输入 n(1≤n≤1e5) m(1≤m≤20) 和长为 n 的数组 a(1≤a[i]≤m)。

n 个偶像排成一行，第 i 个偶像来自第 a[i] 个乐队。每个乐队至少有一个偶像。
重排这 n 个偶像，使得来自同一乐队的偶像连续的站在一起。

最小化需要改变位置的人数。


- [] [] [] ... []
1 3 2 4 2 1 2 3 1 1 3 4
3 3 3 4 4 2 2 2 1 1 1 1
  .   .     .   .
一旦确定前面某些人不变后，就能得到前面所有的分布 []
考虑最大不变的个数，10110
一旦确定了前面的组成元素，如何排布使得其尽量和原有的对齐。
f[s | (1<<i)] -- f[s] 再将i的所有出现次数放在后面
"""
import math
import sys, itertools
from math import inf, isqrt, gcd
from bisect import bisect_left
from collections import deque, defaultdict
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n, m = RII()
a = [0]*n
for i in range(n):
    a[i] = RI()

# ps = [list(itertools.accumulate([x == i+1 for x in a], initial=0)) for i in range(m)]
# def query(i,j, x):
#     # x - [i,j)
#     return ps[x][j] - ps[x][i]
# print(math.factorial(20)) 2432902008176640000

pos = [[] for _ in range(m)]
for idx, x in enumerate(a):
    pos[x-1].append(idx)
def query(i,j, x):
    return bisect_left(pos[x], j) - bisect_left(pos[x], i)
lth = [0]*(1<<m)

f = [0]*(1<<m)
for s in range(1<<m):
    # s
    #l = sum(ps[i][-1] for i in range(m) if s >> i & 1 == 1)
    lb = s & -s
    # l = lth[s] = lth[s - lb] + ps[lb.bit_length()-1][-1] if s > 0 else 0
    l = lth[s] = lth[s - lb] + len(pos[lb.bit_length() - 1]) if s > 0 else 0

    tmp = 0
    for i in range(m):
        if s >> i & 1 == 1:
            c = len(pos[i]) # ps[i][-1]
            # [l-c, l]

            tmp = mx(tmp, f[s ^ (1<<i)] + query(l-c, l, i))
    f[s] = tmp
print(n - f[-1])








