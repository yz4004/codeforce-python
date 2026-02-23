"""
https://atcoder.jp/contests/abc372/tasks/abc372_d
https://atcoder.jp/contests/abc372/submissions/64835887
输入 n(1≤n≤2e5) 和一个 1~n 的排列 a。下标从 1 开始。

有 n 幢楼房，高度从左到右记录在 a 中。
定义 f(i) 表示 j 的个数，满足 i<j<=n 且在 [i+1,j-1] 中没有比 j 高的楼房。
输出 f(1),f(2),...,f(n)。
- 单调栈相关。从右往左维护单调递减栈
- 非典型结构（不是找右侧第一个比他大的）
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

n = RI()
a = RILIST()

res = [0]*n
s = []
for i in range(n-1, -1, -1):
    x = a[i]
    res[i] = len(s)
    while s and s[-1] < x:
        s.pop()
    s.append(x)
print(" ".join(map(str, res)))
