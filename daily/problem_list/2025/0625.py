"""
https://codeforces.com/problemset/problem/2094/G

输入 T(≤1e4) 表示 T 组数据。所有数据的 q 之和 ≤2e5。

一开始，你有一个空数组 a。
每组数据输入 q(1≤n≤2e5) 和 q 个操作，格式如下：
"1"：把 a 循环右移一位。也就是把 a 的最后一个数去掉，插到 a 的第一个数左边。
"2"：反转 a。
"3 x"：把 x(1≤x≤1e6) 添加到 a 的末尾。

保证第一个操作是 "3 x"。

每次操作后，输出 S(a) = 1*a[1] + 2*a[2] + 3*a[3] + ... + m*a[m]，其中 m 为 a 的长度。

- 先尝试维护 S1(a) = 1*a[1] + 2*a[2] + 3*a[3] + ... + m*a[m]，
   因为要支持翻转 再维护 S2(a) = m*a[1] + (m-1)*a[2] + ... + 1*a[m]，
   轮转/添加则很容易处理

https://chatgpt.com/c/6861f39d-113c-800a-8212-dce1d2ba7b10
"""

import sys
from collections import deque
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

def check(queries) -> List[int]:
    res = []
    q = deque([])
    rev = False
    s0 = 0
    s1 = s2 = 0

    for query in map(tuple, queries):
        n = len(q)
        if query[0] == 1:
            # 向右轮转

            last = q[-1] if not rev else q[0]

            s1 = s1 - n * last + s0
            s2 = s2 - s0 + n * last

            if rev:
                q.append(q.popleft())
            else:
                q.appendleft(q.pop())
            res.append(s1)

        elif query[0] == 2:
            # 反转

            s1, s2 = s2, s1
            rev = not rev
            res.append(s1)

        if query[0] == 3:
            # 队尾新增
            new = query[1]

            s1 = s1 + (n+1) * new
            s2 = s2 + s0 + new
            s0 += new

            if rev:
                q.appendleft(new)
            else:
                q.append(new)
            res.append(s1)
    return res

for _ in range(RI()):
    queries = []
    for _ in range(RI()):
        queries.append(RII())
    for x in check(queries):
        print(x)
