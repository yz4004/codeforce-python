"""
[子序列]

https://codeforces.com/problemset/problem/1194/C

输入 T(≤100) 表示 T 组数据。
每组数据输入三个长度均 ≤100 的字符串 s t p，只包含小写英文字母。

每次操作，你可以选择 p 中的一个字母，将其删除，然后把该字母插入 s 中的任意位置。
至多操作 |p| 次。

能否把 s 变成 t？输出 YES 或 NO。
"""
import sys
from collections import Counter

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for _ in range(RI()):
    s, t, p = RS(), RS(), RS()
    n = len(s)

    i = 0
    cntp = Counter(p)
    for c in t:
        if i < n and s[i] == c:
            i += 1
        else:
            if cntp[c] > 0:
                cntp[c] -= 1
            else:
                i = 0
                break

    if i != len(s):
        print("NO")
    else:
        print("YES")


