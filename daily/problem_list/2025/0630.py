"""
https://codeforces.com/problemset/problem/2094/E

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) 和长为 n 的数组 a(0≤a[i]<2^30)。

下标从 1 开始。
定义 S(k) = (a[k] XOR a[1]) + (a[k] XOR a[2]) + ... + (a[k] XOR a[n])。
输出 S(1),S(2),...,S(n) 中的最大值。

- 从bit视角 变成计数问题 (xor bit直接独立）

"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

for _ in range(RI()):
    n, nums = RI(), RILIST()

    cnt = [0]*31
    m = 0
    for x in nums:
        m = mx(m, x.bit_length())
        for i in range(x.bit_length()):
            if x >> i & 1 == 1:
                cnt[i] += 1

    res = 0
    for x in nums:
        tmp = 0
        for i in range(m):
            if x >> i & 1 == 1:
                tmp += (n - cnt[i]) * (1 << i)
            else:
                tmp += cnt[i] * (1 << i)
        res = mx(res, tmp)
    print(res)


