"""
https://codeforces.com/problemset/problem/2065/D

输入 T(≤1e4) 表示 T 组数据。所有数据的 n*m 之和 ≤2e5。
每组数据输入 n m(1≤n*m≤2e5) 和 n 个长为 m 的数组，元素范围 [1,1e6]。

把这 n 个数组重新排列（数组内部的元素不能重排），拼接成一个长为 n*m 的数组 A。
设 A 的前缀和数组为 pre。
输出 sum(pre) 的最大值。

- n个m长数组拼成n*m数组 s.t. 前缀和最大 肯定是前缀越大放前面越好
    a0 a1 a2  ... ai ... an-1
    a0 a01 a012 ... sum(aj for j in range(i))
sum a0*n + a1*(n-1) ... an-1*1

无论怎么排，选一个数组放在首位 起贡献就是固定的，所以我们根据

"""
import sys
from functools import cache

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

T = RI()
for _ in range(T):
    n, m = RII()
    a = []
    for _ in range(n):
        tmp = RILIST()
        k1 = sum(x*(m-i) for i,x in enumerate(tmp))
        k2 = sum(tmp)
        # k1 + k2 * 后续长度
        # 这个k1是所有人都会贡献一次，k2的贡献才和排序有关
        # 假设两个数组 a,b 上面对应的 k1/2 为 (a1, a2) (b1, b2) 数组长m
        # [a,b] - a1+a2*m + b1
        # [b,a] - b1+b2*m + a1  所以只和k2有关
        a.append((k2, k1))
    a.sort(reverse=True)
    res = sum(k1 + k2 * (n-i) * m for i, (k2, k1) in enumerate(a,1))
    print(res)

