"""
https://codeforces.com/problemset/problem/631/E

输入 n(2≤n≤2e5) 和长为 n 的数组 a(-1e6≤a[i]≤1e6)。

执行如下操作恰好一次：
把 a[i] 从 i 移动到 j。
可以原地不动，即 i = j。

输出 a[1] * 1 + a[2] * 2 + ... + a[n] * n 的最大值。

- i [i+1, j-1] j

    nums[i] * (j-i) - sum(nums[i+1:j])
    nums[i] * (j-i) - (ps[j+1] - ps[i+1])
    利用si 指代 ps[i+1] = sum(nums[:i+1])

    si - sj - ai * (i - j)

    对于每个i 计算所有j 使得上式最大，对于每个i 如何用 O(1) 的复杂度计算上式

    si - ai * i - (sj - ai * j)

    即让 sj - ai * j 最小化.

    (x,y) = (j,sj)
    y = a*x + b
    yj - a * xj = bj 最小化bj

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
nums = RILIST()
s = list(itertools.accumulate(nums, initial=0))
# (i,si) 点集维护下凸包
def cross(a, b):
    # 对两向量 a=(x1,y1), b=(x2,y2) 做差乘 x1*y2 - x2*y1
    # return a * b
    return a[0] * b[1] - a[1] * b[0]


def sub(a, b):
    # 向量减法 a - b, b -> a
    return a[0] - b[0], a[1] - b[1]

def get_b(p, a) -> int:
    # y = x*a +b => b = y - a*x
    return p[1] - a*p[0]


def convex():
    base = sum(x * (i + 1) for i, x in enumerate(nums))
    points = [(i, s[i]) for i in range(len(s))]
    # print(points)

    # 1. get convext hull
    st = []
    for i, x in enumerate(points):
        while len(st) >= 2 and cross(sub(points[st[-2]], points[st[-1]]), sub(points[st[-1]], x)) < 0:
            st.pop()
        st.append(i)

    # print(st) # 下凸壳
    # print([points[i] for i in st])
    # print("---------------------------")

    st = [points[i] for i in st]
    slopes = sorted([(i, a) for i, a in enumerate(nums)], key=lambda x: x[1])
    j = 0
    res = base
    # print([(i, a) for i, a in enumerate(nums)])
    # print(slopes)
    # print("---------------------------")
    for i,a in slopes:
        # min(sj - ai * j for j in range(n))
        while j+1 < len(st) and get_b(st[j], a) >= get_b(st[j+1], a):
            j += 1

        # si - ai * i - (sj - ai * j)
        d = s[i] - a * i - get_b(st[j], a)
        res = max(res, base + d)

        # print((i,a))
        # print(j, st[j], get_b(st[j], a))
        # print((base, d, base+d), res)
        # print("====")
        # print("====")
    # print(base, res)
    return res

print(convex())







import sys, itertools
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n = RI()
nums = RILIST()
s = list(itertools.accumulate(nums, initial=0))
# (i,si) 点集维护下凸包
def cross(a, b):
    # 对两向量 a=(x1,y1), b=(x2,y2) 做差乘 x1*y2 - x2*y1
    # return a * b
    return a[0] * b[1] - a[1] * b[0]


def sub(a, b):
    # 向量减法 a - b, b -> a
    return a[0] - b[0], a[1] - b[1]

def get_b(p, a) -> int:
    # y = x*a +b => b = y - a*x
    return p[1] - a*p[0]


def convex():
    base = sum(x * (i + 1) for i, x in enumerate(nums))
    points = [(i, s[i]) for i in range(len(s))]

    # 1. get convext hull
    st = []
    for i, x in enumerate(points):
        while len(st) >= 2 and cross(sub(points[st[-2]], points[st[-1]]), sub(points[st[-1]], x)) < 0:
            st.pop()
        st.append(i)

    # print(st) # 下凸壳
    # print([points[i] for i in st])
    # print("---------------------------")

    st = [points[i] for i in st]
    slopes = sorted([(i, a) for i, a in enumerate(nums)], key=lambda x: x[1])
    j = 0
    res = base
    for i,a in slopes:
        # min(sj - ai * j for j in range(n))
        while j+1 < len(st) and get_b(st[j], a) >= get_b(st[j+1], a):
            j += 1
        # si - ai * i - (sj - ai * j)
        d = s[i] - a * i - get_b(st[j], a)
        res = max(res, base + d)
    return res
print(convex())
