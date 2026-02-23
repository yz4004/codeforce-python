"""
https://codeforces.com/problemset/problem/493/C

输入 n(1≤n≤2e5) 和长为 n 的数组 a(1≤a[i]≤2e9)。
输入 m(1≤m≤2e5) 和长为 m 的数组 b(1≤b[i]≤2e9)。

a 和 b 表示两支篮球队 A 和 B 投篮时到篮筐的距离列表。
设三分线到篮筐的距离为 d。
如果投篮距离 > d 则得到 3 分，否则得到 2 分。

你可以指定 d 的值。
最大化 A 队得分 - B 队得分。
如果有多种方案，最大化 A 队得分。
输出格式 scoreA:scoreB。

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

n, a = RI(), RILIST()
m, b = RI(), RILIST()

a.sort()
b.sort()


if n >= m:
    res = ((n-m)*3, n*3)
else:
    res = ((n-m)*2, n*2)

j = m
for i in range(n-1, -1, -1):
    d = a[i]-1
    while j-1 >= 0 and b[j-1] > d:
        j -= 1
    # [i:n]
    # [j:m]

    score_a = (n-i)*3 + i*2
    score_b = (m-j)*3 + j*2
    gap = score_a - score_b
    if gap > res[0] or (gap == res[0] and score_a > res[1]):
        res = (gap, score_a)

print(str(res[1]) + ":" + str(res[1] - res[0]))
