"""
https://codeforces.com/problemset/problem/2065/C2

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5，m 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) m(1≤m≤2e5)，长为 n 的数组 a(1≤a[i]≤1e9)，长为 m 的数组 b(1≤b[i]≤1e9)。

对于每个 a[i]，你可以把 a[i] 改成 b[j] - a[i]（b[j] 可以自由选择），也可以让 a[i] 保持不变。
对于每个 a[i]，至多修改一次。

能否让 a 变成非递减数组？（a[i] <= a[i+1]）
输出 YES 或 NO。


贪心 无修改次数限制
-- 每次决策 -- 必须改小/可选择改小
-- 另外一种风格，是直接算出「对当前元素能取的最小合法值」，然后只需判断它和 pre 的关系. t + a[i] + pre 再和pre比
"""
import bisect
import sys
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

for _ in range(RI()):
    n, m = RII()
    a, b = RILIST(), RILIST()

    invalid = False
    b.sort()
    pre = -inf
    for i in range(n):

        # 必须改大ai
        if a[i] < pre:
            # bj - ai >= pre/a[i-1]
            t = a[i] + pre
            j = bisect.bisect_left(b, t)
            if j < m:
                a[i] = b[j] - a[i]
            else:
                invalid = True
                break

        else: # 尝试改小a[i] 只要 pre <= bj-ai
            t = a[i] + pre
            j = bisect.bisect_left(b, t)
            if j < m:
                a[i] = mn(a[i], b[j]-a[i])
        pre = a[i]

    print("NO" if invalid else "YES")
