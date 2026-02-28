"""
https://codeforces.com/problemset/problem/1592/E

输入 n(1≤n≤1e6) 和长为 n 的数组 a(1≤a[i]≤1e6)。

输出 a 的最长连续子数组的长度，满足子数组 AND > 子数组 XOR（子数组所有元素的按位与 > 子数组所有元素的异或和）。
如果没有这样的子数组，输出 0。

"""
import sys, itertools
from functools import cache
from heapq import heappop, heappush
from math import inf, isqrt, gcd
from bisect import bisect_left
from collections import deque, defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

"""
子数组必须是偶数长度
    子数组and保留的1 是所有人公共1, 如果子数组长度奇数，xor在这位也是1 (子数组&不可能严格大于子数组xor), 长度只能是偶数 保证这位1在xor里消掉

只关注and后最高位的1
    因为是偶数长度 xor在这位是0 且xor在更高位没有1 (即都是偶数appearance)


https://chatgpt.com/c/69a0eda1-7ae8-832d-b3ef-28c35c418eab
"""

def solve1(n, a):

    u = max(a).bit_length()
    pre = [{(0, 0): 0} for _ in range(u)]

    s = [0]*u
    cnt = [0]*u

    res = 0
    for r,x in enumerate(a, 1):
        # 当前j位的最近的一个0 (后面就是连续1)
        # 01...1
        # 在这里考虑所有偶数长度 [l,r]
        # 如果 [l,r] 内某个高于j的位置 bit count是奇数 - bit_count[jh][l-r] % 2 == 1 那and小于xor
        # 如何维护 pre0[j] 后 l%2 ==  r%2 的 l 的 高于j位置所有bit的odd/even情况 - even/odd - 即直接算xor

        # 检查j
        # 区间内 [l,r] j 全是 1
        # 区间 [l,r] 在 [j,u] 包含j的高位里xor都是0

        # bj = x & high_mask_j ... 保留 [j,u]
        # [l,r] 区间内 b 的xor是0
        # [l,r] 区间内 j位都是1
        # 奇偶长度用xor概括

        # xor(xl >> j ... xr >> j)==0
        # => s(l-1)>>j == sr >> j

        # cnt[xl >> j & 1 ... xr >> j & 1) == r-l+1
        # => j_th[r] - r == j_th[l-1] - (l-1)

        # -- 注意上面两个条件只对jth bit成立

        for j in range(u):
            s[j] ^= x >> j
            cnt[j] += x >> j & 1

        for j in range(u-1, -1, -1):

            q = (s[j], cnt[j] - r)
            pj = pre[j]
            if q in pj:
                res = max_(res, r - pj[q])
            else:
                pj[q] = r

    return res

#
def solve(n, a):
    u = max(a).bit_length()
    # 按j位遍历数组 j位=0 切分数组 省去一个维度

    res = 0
    pre = {}
    for j in range(u):

        l = 0
        while l < n:
            if a[l] >> j & 1 == 0:
                l += 1
                continue

            r = l+1
            while r < n and a[r] >> j & 1 == 1:
                r += 1

            sj = 0
            pre[0] = l-1  # pre[i] -- xi >> j 的前缀xor
            for i in range(l, r):
                sj ^= a[i] >> j

                if sj in pre:
                    res = max_(res, i - pre[sj])
                else:
                    pre[sj] = i

            pre.clear()
            l = r+1
    return res



n, a = RI(), RILIST()
print(solve(n, a))