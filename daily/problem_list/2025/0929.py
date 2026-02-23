"""
https://codeforces.com/problemset/problem/2137/E

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(2≤n≤2e5) k(1≤k≤1e9) 和长为 n 的数组 a(0≤a[i]≤n)。

每次操作：
1. 创建一个长为 n 的数组 b，其中 b[i] 等于 a 中除去 a[i] 后的 mex，即不在这 n-1 个数中的最小非负整数。
2. 更新 a 为 b。

输出操作 k 次后的 sum(a)。

mex {1..k, k1... where k1 > k+1} = k+1

1...k-1 _ ...

所有大于k的数，扣掉 mex仍然是k
所有小于k的数，且cnt>1 扣掉 mex仍是k

所有小于k的数且cnt=1 mex才是他本身。



"""
import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict, deque
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for _ in range(RI()):
    n, k = RII()
    a = RILIST()

    cnt = defaultdict(int)
    for x in a:
        cnt[x] += 1

    pre = []
    u = -1
    # 01...u 最大的连续0-u
    for x,c in sorted(cnt.items()):
        if x == u+1:
            if c == 1:
                pre.append(x)
        else:
            # u+1 是mex （第一轮）
            break
        u += 1

    #print(sorted(cnt.items()), u, pre)

    if u == -1:
        # 此时没有单元素，此后 0..0 1..1 反复横跳
        print(0 if k % 2 == 1 else n)
        continue
    elif u == 0:
        print(0 if k % 2 == 0 else n)
        continue

    if k == 1:
        total = sum(a)
        print(sum(pre) + (n-len(pre)) * u)
        continue
    else:
        # 考虑 pre = [x1...xk] 的前缀 0...u 则u+1

        u2 = -1
        for i,x in enumerate(pre):
            if x == i:
                u2 = i

        # u2 是 0...u2 pre中最大的出现
        # [0...u2] ...

        # print(sorted(a))
        # print(pre, u2, n)




        k -= 1  # 从新从1开始计数

        if (n-(u2+1)) == 0:
            # 没有更大，则移除每个人原序列不变
            print((0+u2)*(u2+1)//2)
        elif (n-(u2+1)) == 1:
            # 0...u2 _ u2+2
            # 缺了u2+1
            print((0 + u2) * (u2 + 1) // 2 + u2+1)
        else:
            # 0...u2 _ u2+2 ...
            # 前面 0-u2 不变; 后面每个u2+2清除后变成u2+1
            # 下一次序列变成 0...u2 u2+1 ... u2+1
            # 会再变成 0...u2 _ u2+2 ...

            #print("?", k % 2 == 1, (0 + u2) * (u2 + 1) // 2, n-(u2+1))

            if k % 2 == 0:
                bulk = n-(u2+1)
                print((0+u2)*(u2+1)//2 + bulk * (u2+1))
            else:
                bulk = n - (u2 + 1)
                print((0 + u2) * (u2 + 1) // 2 + bulk * (u2 + 2))
