"""
[二分答案],[最小化最大值],[贪心]
https://codeforces.com/problemset/problem/2070/C

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤3e5。
每组数据输入 n(1≤n≤3e5) k(0≤k≤n)，长为 n 的只包含 R 和 B 的字符串 s，长为 n 的数组 a(1≤a[i]≤1e9)。

有一条长为 n 的纸带，包含 n 个单元格。最初，所有单元格都是红色。
每次操作，选择一段连续的单元格，涂成蓝色。
至多操作 k 次。

对于第 i 个单元格，其惩罚值定义如下：
如果第 i 个单元格的最终颜色不等于 s[i]（R 表示红色，B 表示蓝色），那么其惩罚值为 a[i]，否则惩罚值为 0。

最小化最大的惩罚值。

（注意是只考虑最大值，而不是求惩罚值和）

R -> B

B R B R B B R R B R
5 1 2 4 5 3 6 1 5 4

"""
import sys


RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for _ in range(RI()):
    n, k = RII()
    s = RS()
    a = RILIST()

    isB = [1 if ch == 'B' else 0 for ch in s]  # 预处理，避免反复比较字符

    def check(t):
        # 能不能减小到t

        cnt = 0
        open_seg = False  # 当前是否有一段在“延伸”
        _isB = isB
        _a = a
        _n = n
        for i in range(_n):
            vi = _a[i]
            if vi > t:
                if _isB[i]:        # 必须蓝
                    if not open_seg:
                        cnt += 1
                        if cnt > k: # 超出k允许 剪枝
                            return False
                        open_seg = True
                else:  # 严禁蓝（R 且 a[i]>t），切断
                    open_seg = False
        return True

    lo, hi = -1, max(a)  # 在 [0..max(a)] 找最小可行 t
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if check(mid):
            hi = mid
        else:
            lo = mid
    print(hi)
    # l, r = 0, max(a)
    # print(bisect_left(range(l,r+1), True, key=lambda x:check(x)))





from bisect import bisect_left
from functools import cache
from heapq import heappop
from itertools import accumulate
from math import inf

def is_checking_sum(a, s, n, k):

    ps = list(accumulate(a, initial=0))
    ps_r = list(accumulate([a[i] if s[i] == "B" else 0 for i in range(n)], initial=0))
    def cost(l,r):
        return (ps[r] - ps[l]) - (ps_r[r] - ps_r[l])

    # [,i]
    f = [[inf]*(k+1) for _ in range(n+1)]
    f[0][0] = 0
    for i in range(1, n+1):

        f[i][0] = ps_r[i]
        for j in range(1, k+1):
            # f[i][j] 前i个划成j段
            f[i][j] = f[i-1][j] + (a[i-1] if s[i-1] == "B" else 0)
            t = min(f[l][j-1] + cost(l,i) for l in range(i))
            f[i][j] = min(f[i][j], t)

    print(min(f[n]))

    # 求和 -- 划分形dp 前缀优化
    # https://chatgpt.com/c/68c8de05-ef20-832a-a487-f90ade8e4096
    #...
    ####################################
    #
    # # [,i]
    # f = [[inf]*(k+1) for _ in range(n+1)]
    # f[0][0] = 0
    # prev = inf
    # for j in range(1, k + 1):
    #
    #     f[i][0] = ps_r[i]
    #     for i in range(1, n + 1):
    #         # f[i][j] 前i个划成j段
    #         f[i][j] = f[i-1][j] + (a[i-1] if s[i-1] == "B" else 0)
    #
    #         # cost(l,r) = (ps[r] - ps[l]) - (ps_r[r] - ps_r[l])
    #         # t = min(f[l][j-1] + cost(l,i) for l in range(i))
    #         # t = min(f[l][j-1] + ps[i] - ps[l] - ps_r[i] + ps_r[l] for l in range(i))
    #         # t = min(f[l][j-1] + ps_r[l] - ps[l] for l in range(i)) + ps[i] - ps_r[i]
    #         # 即维护 f[l][j-1] + ps_r[l] - ps[l] for l in range(i) 前缀min
    #         t = prev + ps[i] - ps_r[i]
    #         f[i][j] = min(f[i][j], t)
    #
    #         prev = min(prev, f[i][j])
    # print(min(f[n]))