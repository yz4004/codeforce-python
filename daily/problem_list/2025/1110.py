"""
https://codeforces.com/problemset/problem/2000/D

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(2≤n≤2e5)，长为 n 的数组 a(1≤a[i]≤1e5)，长为 n 的字符串 s，只包含大写字母 'L' 和 'R'。

每次操作：
选择 a 的一个子数组 [i,j]，满足 s[i] = 'L' 且 s[j] = 'R'。
获得等于子数组 [i,j] 的元素和的分数。
把 s 的子串 [i,j] 中的字符全部改成 '.'

输出总得分的最大值。

只能有nested [l,r] 不能有 intersection
"""
import itertools
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for _ in range(RI()):
    n, a, s = RI(), RILIST(), RS()

    ps = list(itertools.accumulate(a, initial=0))
    res = 0

    j = n-1
    for i in range(n):
        if s[i] == "L":
            while j >= i and s[j] == "L":
                j -= 1
            if i < j:
                # [i,j]
                res += ps[j+1] - ps[i]
                j -= 1

    print(res)



