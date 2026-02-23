"""
https://codeforces.com/problemset/problem/2134/B

输入 T(≤1e3) 表示 T 组数据。所有数据的 n 之和 ≤1e5。
每组数据输入 n(1≤n≤1e5) k(1≤k≤1e9) 和长为 n 的数组 a(1≤a[i]≤1e9)。

你可以执行如下操作至多 k 次：
选择 a 的一个子序列，把其中元素都增加 k（直接修改 a）。
注：子序列不一定连续。

目标是让 gcd(a) > 1。可以证明，这一定可以做到。
输出最终的 a。多解输出任意解。

"""
from collections import defaultdict
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

def solve(n, k, a):

    # 整除理论 余数 构造
    # 加法在取模意义下可能意为着减法
    # 特别的+k 在 (mod k+1) 意义下是 -1
    # k = -1 mod (k+1)
    # 加法然后又构造整除 -- 往往要找因数分解

    # x + k 2k ... k*k
    # k=1 奇数变偶数
    # k=2 考虑x+4/x+2/x的所有因子 选一个gcd
    # k=3 奇数变偶数
    # ...

    # 注意说至多k次. 即一个元素可加 k 2k ... k*k - 似乎是暗示某种跟k余数有关的循环
    # x + q*k 如何构造出一个乘积:

    # x=p(k+1)+r
    # x + r*k = p(k+1) + r*(k+1) = (p+r)*(k+1) -- where r<k

    # k = -1 mod (k+1)
    # 加k 在mod k+1的意义下等价于-1
    # x + q*k 在mod k+1情况下 等价于减去 q个1 且q可选0...k 暗示q覆盖了 x mod k+1 的所有余数空间
    # https://chatgpt.com/c/6951f485-7d98-8325-93a0-ac9f516ae8ed

    if k % 2 == 1: # 如果k是奇数 就走全偶数构造
        return [x + (k if x % 2 == 1 else 0) for x in a]

    # 对于偶数k 走 k+1 余数构造
    res = [0]*n
    for i,x in enumerate(a):
        p, r = x//(k+1), x%(k+1)
        res[i] = (p+r) * (k+1)
    return res

for _ in range(RI()):
    n, k = RII()
    a = RILIST()
    res = solve(n, k, a)
    print(" ".join(map(str, res)))
