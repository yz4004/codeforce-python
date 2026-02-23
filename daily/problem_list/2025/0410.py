"""
https://codeforces.com/problemset/problem/474/F

输入 n(1≤n≤1e5) 和长为 n 的数组 a(1≤a[i]≤1e9)。
然后输入 q(1≤q≤1e5) 和 q 个询问，每个询问输入两个数 L 和 R，表示下标从 L 到 R 的连续子数组 (1≤L≤R≤n)。
对于每个询问，输出 R-L+1-C，其中 C 为子数组中的元素 x 的个数，满足 x 能整除子数组中的每个数。

- x整除 [L,R] 的每个人（x作为因子）x <= gcd([L,R]), x应该是gcd的因子，但gcd又整除x 所以x就是gcd
- 区间gcd 和 区间gcd的个数

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
a = RILIST()
q = RI()

# [L,R]

# st[i][j] [j, j+2^i) 的 gcd
m = n.bit_length()
st = [[-1]*n for _ in range(m)]
st[0] = a[:]

for j in range(0, m-1):
    # [i, 2^(j+1)) = [i, i+2^j) [i+2^j, i+2^(j+1))
    for i in range(n):
        if i+(1 << j) >= n: break
        st[j + 1][i] = gcd(st[j][i], st[j][i+(1 << j)])
    # print(st[j+1])
# print("===")
# print(st)

index_map = defaultdict(list)
for i,x in enumerate(a):
    index_map[x].append(i)
for x in index_map:
    index_map[x].sort()

for _ in range(q):
    l, r = RII()
    l, r = l-1, r-1
    # [l,r]/[l,r+1)
    d = a[l]
    # k=r-l+1 = 0b10101101
    k = r-l+1
    #print(k, bin(k))

    i = l
    for j in range(m):
        if k >> j & 1 == 1:
            d = gcd(d, st[j][i])
            i += (1 << j)
    #
    #print((l,r), "-", d)
    d_indices = index_map[d]
    c = bisect_left(d_indices, r+1) - bisect_left(d_indices, l)
    print(r - l + 1 - c)




