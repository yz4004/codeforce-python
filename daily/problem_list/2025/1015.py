"""
https://codeforces.com/problemset/problem/2140/C

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) 和长为 n 的数组 a(1≤a[i]≤1e9)。

定义 f(a) = cost + (a1-a2+a3-a4...an)，cost 初始值为 0。
Alice 和 Bob 玩游戏，Alice 先手。
每回合，玩家可以结束整个游戏，或者交换 a 中的两个数 a[i] 和 a[j]，并将 cost 增大 |i-j|。
Alice 的目标是最大化 f(a)，Bob 的目标是最小化 f(a)。

假设双方都采取最优策略。输出最终 f(a) 的值。

1000 1
1000 - 1

9 9 9 9 9
0       4
+9-9...+9

7 1 8 4
+7 -1 +8 -4
    1    3

1 14 1 14 1 15
1 -14 +1 -14 +1 -15
0               5

15 -14 +1 -14 +1 -1
-12 + 5



"""
import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict, deque
from math import inf, gcd, comb

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

def solve(n, nums):

    # a0 - a1 + a2 ...
    # even index -- min  p
    # odd index -- max   q
    # p-q -> q-p
    # d = 2q - 2p  + |i-j|  maximize

    # d = 2q - 2p + i - j

    # i - odd
    # nums[i] = q
    # 2q + i - (2p + j) -- previous p (even index) -- min 2p+j

    # i - even
    # nums[i] = p
    # -2p+i + (2q-j)  -- previous q (odd index) -- max 2q-j

    d = 0
    if n > 2:
        # 0123  - 2-0
        # 01234 - 4-0
        d = (n-1) - (n-1)%2

    a = inf   # min 2*p+j
    b = -inf  # max 2*q-j

    for i in range(n):
        if i % 2 == 1:
            q = nums[i]
            t = 2*q + i
            if t - a > d:
                d = t - a

            b = mx(b, 2*q-i)
        else:
            p = nums[i]
            t = i - 2*p
            if t + b > d:
                d = t + b

            a = mn(a, 2*p+i)

    return sum(nums[0:n:2]) - sum(nums[1:n:2]) + d


for _ in range(RI()):
    n, a = RI(), RILIST()
    print(solve(n, a))
