"""
https://codeforces.com/problemset/problem/2118/C

输入 T(≤5000) 表示 T 组数据。所有数据的 n 之和 ≤5000。
每组数据输入 n(1≤n≤5000) k(0≤k≤1e18) 和长为 n 的数组 a(0≤a[i]≤1e9)。

你可以执行至多 k 次如下操作：
把一个 a[i] 加一。

定义 popcount(x) 为 x 的二进制中的 1 的个数。
输出 popcount(a[i]) 之和的最大值。
"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

for _ in range(RI()):
    n, k = RII()
    nums = RILIST()

    # pop count(x): x的set bit数量
    # sum(pop count(a[i]))

    # 要将 1<<i 置1 需要操作 (1<<i)
    # 最大范围 k=1e18 = (2^10)^6 取61个bit

    res = 0
    for i in range(61):
        cnt = 0
        for x in nums:
            cnt += x >> i & 1

        # cnt, n-cnt
        d = 1 << i
        t = mn(k//d, n-cnt)  # 可将t个数在此位置1
        k -= t*d
        res += cnt + t
    print(res)
