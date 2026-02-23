"""
https://www.luogu.com.cn/problem/P3572

输入 n(1≤n≤1e6) 和长为 n 的数组 a(1≤a[i]≤1e9)。
然后输入 t(≤25) 和 t 组数据。每组数据输入 k(1≤k≤n-1)。

有 n 棵树，高度从左到右记录在数组 a 中。
有一只鸟，从第一棵树开始飞。
它每次可以从下标 i 飞到下标在 [i+1,i+k] 中的任意一棵树。但如果飞到一棵高度大于等于当前树的树，鸟的疲劳值会增加 1。

输出鸟从第一棵树飞到最后一颗树的最小疲劳值。

- [i-k, i-1] -> i 最小的疲劳值转移过来
[h1 h2 ... hk]

(v,-h)

1 5 2 3 4

"""
import sys
from heapq import heappop, heappush
# from collections import deque

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n = RI()
a = RILIST()
T = RI()
f = [0]*n
for _ in range(T):
    k = RI()

    # n,k
    # [i+1, i+k]
    # f[i] 到达i的最低疲劳值
    q = [(0, -a[0], 0)] # (f[i], -a[i], i)
    for i in range(1,n):
        # [i-k, i-1] -> i 取min
        while q and q[0][2] < i-k:
            heappop(q)

        f[i] = q[0][0] + (1 if -q[0][1] <= a[i] else 0)

        heappush(q, (f[i], -a[i], i))
    print(f[n-1])



    # q = deque([(0, 0)]) # (i, f[i])
    # for i in range(1,n):
    #     # [i-k, i-1] -> i 取min
    #     while q and q[0][0] < i-k:
    #         q.popleft()
    #
    #     f[i] = q[0][1] + (1 if a[q[0][0]] <= a[i] else 0)
    #
    #     while q and q[-1][1] > f[i]:
    #         q.pop()
    #     q.append((i, f[i]))
    # print(f[n-1])




