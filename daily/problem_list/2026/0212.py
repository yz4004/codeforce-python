"""
https://codeforces.com/problemset/problem/1951/D

输入 T(≤1e3) 表示 T 组数据。
每组数据输入 n(1≤n≤1e18) 和 k(1≤k≤1e18)。

Alice 有 n 元钱，想在 Bob 的珠宝店购买珠宝。
珠宝店有若干个展柜。Alice 会先去第 1 个展柜，尽可能多地购买珠宝，然后去第 2 个展柜，依此类推，直到最后一个展柜。

Bob 的珠宝店最多可以放置 60 个展柜（每个展柜有无限数量的珠宝），第 i 个展柜需要设置一个在 [1,1e18] 中的整数价格 p[i]，其中的珠宝价格均为 p[i] 元。
如何设置价格，可以让 Alice 购买的珠宝总数恰好为 k？

如果无法做到，输出 NO。
否则输出 YES，展柜数量，以及每个展柜的珠宝价格。
"""
import sys, itertools
from functools import cache
from heapq import heappop, heapify, heappush
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

def solve(n ,k):
    if n < k: return "NO", None   # 1块钱也凑不够k个
    if n == k:
        return "YES", [1] # 恰好1块钱一个

    """
    第一个摊位定价为p
    c = n//p 
    可购买的最大数量 n//p + n%p （后面按一块卖
    c + n - c*p 
    n - (p-1)*c 
    n - (p-1)(n//p) 
    
    对于后者p越小 整体越大. 
    p=2
    n - n//2 = (n+1)//2 
    
    假如 k > (n+1)//2 则没可能了，因为1也不行 选p=2又凑不够
    k == (n+1)//2就恰好
    k < (n+1)//2 说明还有机会，但能保证一定构造出来吗
    
    
    
    如果第一个放2 alice第一个柜子可以买 n//2  (> k)
    
    放p 买c个 剩余 n - p*c 个. 
    那就尽量贵的买 使得第一次卖不超过 k -- c <= k 
    
    c = n//p <= k 
    
    p*k <= n -- p <= n//k 
    
    取p=n//k
    
    """
    if k > (n+1)//2:
        return "NO", None

    # k < (n+1)//2 肯定有解
    # 最简构造 不是走整除路线 而是第一次贵到只买一个 后面按1填
    return "YES", [n-(k-1), 1]




for _ in range(RI()):
    n, k = RII()
    res, instance = solve(n, k)
    print(res)
    if instance:
        print(len(instance))
        print(" ".join(map(str, instance)))
