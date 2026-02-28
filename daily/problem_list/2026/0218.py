"""
https://codeforces.com/problemset/problem/1995/C

输入 T(≤1e3) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) 和长为 n 的数组 a(1≤a[i]≤1e6)。

每次操作，你可以把一个 a[i] 变成 a[i] * a[i]。

把 a 变成递增数组（a[i] <= a[i+1]），至少要操作多少次？
如果无法做到，输出 -1。

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
ps 暴力肯定超时

数学 - 指数运算 指数的指数
1. x^(a*b) = (x^a)^b
    x^(a^b) 则远大于
    
    x^(a+b) = x^a * x^b

2. 观察相邻 x y
    如果 x > y 且x自平方k次 则y首先自平方t次 刚好超过x 再进行k次 (可证)
                                y^(2^t) > x 
    如果 x < y 则考虑反过来找 x^(2^t) < y 找恰好的 t  
    现在x被平方m次
    x^(2^t) = x^(2^(t-m + m)) = x^(2^(t-m) * 2^m)) < y  
    
    - 这里用 x^(a*b) = x^a)^b
    
    = (x^2^m)^(2^(t-m)) 
    代表x先自平方m次 再自平方 t-m 次 假设t-m>0
    
    这说明 x^(2^m) < y - y不用做任何事
    
    
    如果 t-m < 0 则改写成
    x^(2^m) = x^(2^(m-t + t)) = x^(2^(m-t) * 2^t))   
    
    x^(2^t) ^ (2^(m-t)) -- (也是利用指数乘法=指数再指数)
    
    x自平方m次 等于先自平方t次 再自平方 m-t 次 所以y只需自平方 m-t 
     
"""

def solve(n, a):
    res = 0
    k1 = 0
    x = a[0]
    for i in range(1, n):
        # while a[i-1] > a[i]:
        #     if a[i] == 1: return -1
        #     a[i] *= a[i]
        #     res += 1

        # x x^2 x^4 x^8 x^16..
        # ai ^ 2^k

        # x^k1 -- y^k2

        # x^(2^k1) -- y^(2^k2)

        # x^1 = x^(2^0) --> x^(2^k)
        # x^2 = x^(2^1)
        # x^4 = x^(2^2)

        x, y = a[i-1],  a[i]
        if x == y:
            res += k1
            continue

        if x > y:
            if y == 1: return -1
            # x > y
            # x < y^(2^k)

            # x^(2^k1) < (y^(2^k)) ^ (2^k1)

            k = 0
            y2 = y
            while y2 < x:
                y2 *= y2
                k += 1

            res += k1 + k
            k1 = k1 + k
        else:
            # x < y
            # x^(2^t) < y < x^(2^(t+1))

            # x^(ab) = (x^a)^b

            # x^(2^k) = x^(2^(k-t) * 2^t) = (x^(2^t)) ^ [2^(k-t)] < y ^ [2^(k-t)]

            if x == 1: continue

            t = 0
            x2 = x
            while x2 <= y:
                x2 *= x2
                t += 1
            t -= 1
            # print("-", x, y, x2, t, k1)

            k1 = max(0, k1 - t)
            res += k1
        # print(x, y, (res, k1))
    return res

for _ in range(RI()):
    n, a = RI(), RILIST()
    print(solve(n, a))

