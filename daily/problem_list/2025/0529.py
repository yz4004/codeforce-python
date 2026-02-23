"""
https://codeforces.com/problemset/problem/2064/D

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5，q 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) q(1≤q≤2e5) 和长为 n 的数组 a(1≤a[i]<2^30)。
然后输入 q 个询问，每个询问输入 x(1≤x<2^30)。

有 n 个史莱姆排成一行，大小为 a[i]。
在 a 的最右边添加一个大小为 x 的史莱姆。
如果 x >= 左边相邻史莱姆的大小 v，那么 x 吃掉左边的史莱姆，同时 x 更新为 x XOR v。
如果没有史莱姆，或者 x < 左边相邻史莱姆的大小，结束。
输出被吃掉的史莱姆的个数。
注意：每个询问互相独立。

a1 ... an x

xor
10101
11001
-
01100

"""
import itertools
from bisect import bisect_left
from math import comb, factorial
import sys
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

def solve(nums, queries):
    n = len(nums)
    m = mx(max(nums), max(queries)).bit_length()
    t = [[] for _ in range(m)] # t[j] jth 1 出现的位置

    ps = [0]*(n+1) # ps[i] -- nums[0:i] 的 xor
    # x连续吃掉 [l,r) 等于 x 和 区间xor结果 xor
    for i, x in enumerate(nums):
        for j in range(m):
            if x >> j & 1 == 1:
                t[j].append(i)
        ps[i+1] = ps[i] ^ x
    eat = lambda l,r: ps[r] ^ ps[l] # [l,r)

    # 查询 jth 1-bit 在 [0,r) 出现的最右位置
    # bisect_left(t[j], r)-1
    # print(t)

    def check(x):
        l, r = 0, n
        # 搜索区间 [l,r)
        for i in range(m-1, -1, -1):
            if l >= r: break
            # find the rightmost slime < r that has bit i = 1
            k = bisect_left(t[i], r) - 1
            # t[i][k] 代表1在原数组的位置
            pos = t[i][k] if k >= 0 else -1
            # print(i, t[i])
            # print(k, pos)

            if x >> i & 1 == 0:
                if pos >= l:
                    l = pos + 1
            else:
                # x的最大位，会在 [l,r) 往左方向第一个出现位置被置0
                if pos < l: # 搜索区间里找不到高位为1的点了，可以一直取到l，但l是不可预约的高位，吃了区间也没用
                    break
                if nums[pos] > x and x ^ eat(pos+1,r) < nums[pos]: # 打不过pos l应该设成其右侧，吃了 [l+1,r]也没用
                    l = pos + 1
                    break
                # 有限制，选最近的
                # x = x ^ nums[pos] 需要连续吃 [pos+1, r)
                x ^= eat(pos+1, r) # mask = (1 << i) - 1 不需要mask 因为高位也不会看了
                r = pos+1
                if k-1 >= 0:
                    l = mx(l, t[i][k-1] + 1)
        return l

    res = []
    for q in queries:
        res.append(n - check(q))
    return res
# print(45, 61^7^14^18, 61^7^14, 61 ^ 7, 61)

T = RI()
for _ in range(T):
    n, q = RII()
    nums = RILIST()
    queries = []
    for _ in range(q):
        x = RI()
        queries.append(x)
    res = solve(nums, queries)
    print(" ".join(map(str, res)))
