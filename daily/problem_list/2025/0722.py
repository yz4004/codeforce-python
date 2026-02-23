"""
https://codeforces.com/problemset/problem/2123/E

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) 和长为 n 的数组 a(0≤a[i]≤n)。

定义 mex(A) 为不在数组 A 中的最小非负整数。特别地，mex(空数组)=0。
定义 f(k) 为从 a 中删除恰好 k 个数后，剩余元素的 mex 值的不同个数。

输出 f(0),f(1),f(2),...,f(n)。


分析发现
    不删除 -- mex(A)=t （删除也不会取到大于t的数；小于t的所有数一定全部出现 0-t-1)
    从0到n个删除 能取的范围是 t t-1 ... 0
    直接枚举 i [t-0] 不好确定删除方案
    但从大到小分析，t对应的删除范围应该是 不删 - 删掉数组中最大的数(cnt) 至少这么多个删除后 一定会造成某个小于t的数暴露
    所以若让k是删除后最小不在 删除的范围是 [cnt[k], 所有大于等于k的所有计数]
    分类讨论 + 差分问题
"""
import sys
from collections import defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

for _ in range(RI()):
    n, nums = RI(), RILIST()

    # [0,k] 都在 nums 中则 k+1 是mex(A)
    # 删除一个，如果有重数 则删重数可和不删一样
    # 所有小于 f[0]=mex(A) 的distinct的数 删掉一次后都能有个新值.

    # t   [0,所有大于等于t的数的个数]
    # t-1 [t-1的计数，所有大于等于t-1的数的个数]
    # ...

    cnt = defaultdict(int)
    for x in nums:
        cnt[x] += 1

    i = 0
    target = -1
    d = 0 # 小于target的计数 （最后要求大于等于target的计数
    for t in range(n+1):
        if t not in cnt:
            target = t
            break
        d += cnt[t]

    d = n - d  # 大于等于target的计数

    res = [0]*(n+2)
    res[0] = 1  # res[0] -- target
    d += sum(cnt[x] - 1 for x in cnt if x < target)
    res[d+1] -= 1

    for i in range(target-1, -1, -1):
        # i - [i 在nums里的计数， 大于等于i的所有数量]
        d += 1

        res[cnt[i]] += 1
        res[d+1] -= 1

    for i in range(1, n+1):
        res[i] += res[i-1]

    print(" ".join(map(str, res[:-1])))
