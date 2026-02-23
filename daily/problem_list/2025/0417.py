"""
https://www.luogu.com.cn/problem/P3957

输入 n(1≤n≤5e5) d(1≤d≤2e3) k(1≤k≤1e9) 和 n 个 pair，每个 pair 输入两个数 xi(1≤xi≤1e9) 和 si(-1e5≤si≤1e5)。保证 xi 是递增的。

坐标轴上有 n 个点，xi 是点的位置，si 是到达这个点可以得到的分数。

你的跳跃能力为 d。
你可以花费 g 个金币，增加跳跃能力，使得你可以从 x 跳到在 [x+max(d-g,1), x+d+g] 中的点。
注意你必须跳到输入的 n 个点中，不能跳到其他位置。

你从原点 0 开始向右跳。
你可以在任意时刻结束游戏。

目标是让总得分 >= k。
输出 g 的最小值。

提示：请先完成昨天的题目。

0 - [d-g, d+g]
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

# import platform
# print(platform.python_implementation())

n, d, k = RII()
a = [None]*n
for i in range(n):
    a[i] = tuple(RII())
# print(a)

def check(g):
    # [i-d-g, i-max(d-g,1)] -> i
    j = 0
    f = [-inf]*n # max score
    q = deque([(0,0)]) # posi, score
    for i, (xi, si) in enumerate(a):
        # 1. maintain deque
        while q and q[0][0] < xi - d - g:
            q.popleft()
        while j < n and a[j][0] <= xi - mx(d-g,1):
            while q and q[-1][1] <= f[j]:
                q.pop()
            q.append((a[j][0], f[j]))
            j += 1

        # 2. update
        if q and xi - d - g <= q[0][0] <= xi - mx(d-g,1):
            f[i] = q[0][1] + si
            if f[i] >= k:
                return True
    return False

l,r = 0,a[-1][0]-d+1
res = bisect_left(range(l,r+1), True, key=lambda x:check(x))
print(res if res < r else -1)


sys.exit(1)

# given g
def check(g):
    # f = [0]*n # f[i] 最大分数
    # f = [[0] * n for _ in range(g+1)]  # f[c][i] 不超过cost 最大分数
    # i -> [i+max(d-g,1), i+d+g]
    # [i-d-g, i-max(d-g,1)] -> i
    for c in range(1, g+1):
        for i, (xi, si) in enumerate(a):
            for j in range(i):
                # xj - xi
                xj = a[j][0]
                cost = abs(xi - xj - d)
                if cost <= c:
                    f[c][i] = mx(f[c][i], f[c-cost][j] + si)
                    if f[c][i] >= k:
                        return True
    return False

l,r = 0,a[-1][0]+1
res = bisect_left(range(l,r+1), True, key=lambda x:check(x))
print(res if res < r else -1)
# print(check(1))
# print(check(2))
# print(check(3))

# print(check(1))
# print(check(2))
# print(check(3))


