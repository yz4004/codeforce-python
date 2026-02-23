"""
https://www.luogu.com.cn/problem/P1725

输入 n L R(1≤L≤R≤n≤2e5) 和长为 n+1 的数组 a(-1e3≤a[i]≤1e3)，下标从 0 开始。保证 a[0]=0。

有 n+1 个格子，编号从 0 到 n。
你从 0 号格子向右跳。如果你在格子 i，可以跳到编号 [i+L,i+R] 中的任意格子。
跳到格子 i 后，总得分增加 a[i]。

如果跳出界（i>n），游戏结束。
输出游戏结束后的最大总得分。

i -> [i+L, i+R]
[j-R, j-L] -> j
- 对每个j查询左侧固定区间的最大值
- 可以通过线段树等维护，但是因为是查询左侧静态 不涉及修改. 栈/队列等静态线性结构更适合
- 单调队列维护
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

n, L, R = RII()
a = RILIST()

# f = [0]*(n+1)
# for i in range(n+1):
#     for j in range(min(i+L,n), min(i+R,n)+1):
#         f[j] = mx(f[j], f[i] + a[j])
# print(max(f))

q = deque() # (idx, value)
f = [a[0]] + [-inf]*n
for j in range(1, n+1):
    # 1. 整理队列，清除旧数据
    while q and q[0][0] < j-R:
        q.popleft()

    if j-L >= 0:
        # 2. 加入新数据，队列up to date
        while q and q[-1][1] <= f[j-L]:
            q.pop()
        q.append((j-L, f[j-L]))

        # 3. 更新结果
        # [j-R, j-L] -> j 找左侧这个区间的max
        f[j] = q[0][1] + a[j]

print(max(f[n-R+1:])) # 因为支持负数，只能选这段 否则0来捣乱
