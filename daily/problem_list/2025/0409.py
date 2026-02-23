"""
https://www.luogu.com.cn/problem/P2627

输入 n k(1≤k≤n≤1e5) 和长为 n 的数组 a(0≤a[i]≤1e9)。

从 a 中选择一些数，但这些数中，不能有超过 k 个数的下标是连续的，即下标 i,i+1,i+2,...,i+k 不能都选。
输出你选的数的最大和。


- f[i] 定义为前i个最大选择和 （本题提示1e5, 要低于n^2)
- f[i] 如果选i，则可以从 f[j] j<i-1转移过来，但如果前一个选了 i-1 往前不能构成连续k个

    可以构造，[0, i-k-1] [i-k, i-k+1, ... i-1, i]
    f[i-k] + [i-k, ... i-1 i]
    不选i，则f[i-1]
    选i，则[i-k, i-1] 中某个j不选，[0,j-1] [j] [j+1, i] = f[j] + sum([j+1,i])

"""
import itertools
import sys
from math import inf, isqrt
from collections import deque
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n, k = RII()
a = list(RI() for _ in range(n))
ps = list(itertools.accumulate(a, initial=0))
f = [0]*(n+1)

q = deque()

for i in range(n):
    while q and q[0][0] < i-k:
        q.popleft()

    if i < k:
        f[i+1] = ps[i+1]
    else:
        # 滑动窗口内最大值
        # f[i+1] = max(f[j] + ps[i+1] - ps[j+1] for j in range(max(0, i-k), i+1))    --- [i-k, i]
        # max(f[j] - ps[j+1] for j in range(max(0, i-k), i+1) + ps[i+1]
        # f[i+1] = q[0][1] + ps[i+1]
        f[i + 1] = mx(f[i], q[0][1] + ps[i + 1])

    cur = f[i] - ps[i+1]
    while q and q[-1][1] <= cur:
        q.pop()
    q.append((i, cur))
print(f[n])





# for i in range(n):
#     # [0,j-1] [j] [j+1, i-1]
#     # f[j]        ps[i] - ps[j+1]
#
#     if i < k:
#         f[i+1] = ps[i+1]
#     else:
#         f[i+1] = f[i]
#         # [i-k, i-1] i
#         for j in range(max(0, i-k), i):
#             # [0,j-1] [j] [j+1, i-1] [i]
#             # f[j]        ps[i] - ps[j+1]
#             # f[i+1] = mx(f[i+1], f[j] + sum(a[j+1:i+1]))
#             f[i + 1] = mx(f[i + 1], f[j] + ps[i+1] - ps[j+1])
# print(f[n])
