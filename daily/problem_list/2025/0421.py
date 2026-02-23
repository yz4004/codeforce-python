"""
https://atcoder.jp/contests/abc353/tasks/abc353_d

输入 n(2≤n≤2e5) 和长为 n 的数组 a(1≤a[i]≤1e9)。

定义 f(x,y) 表示拼接 x 和 y 得到的数字。
例如 f(3,14) = 314。

输出所有 f(a[i],a[j]) 之和，其中 i < j。
答案模 998244353。

3 14 15

314, 315, 1415
15和所有的左侧枚举过得数组合：3 15, 14 15. x * 10 ** t + 15. t是15的长度
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

mod = 998244353
n = RI()
a = RILIST()
s = 0 # sum of traversed int
res = 0
for cnt, v in enumerate(a):
    l = len(str(v))
    res += s * 10 ** l + cnt * v
    #当前v和所有枚举过得左侧数组合，x * (10 ** l) + v where t是v的10进制位数. cnt是左侧所有个数
    res %= mod
    s += v
print(res)


