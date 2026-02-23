"""
https://codeforces.com/problemset/problem/2140/E1

输入 T(≤1e4) 表示 T 组数据。所有数据的 2^n 之和 ≤2^20，所有数据的 m 之和 ≤1e6。
每组数据输入 n(1≤n≤20) m(1≤m≤1e6) k(1≤k≤n) 和长为 k 的严格递增数组 c(1≤c[i]≤n)，保证 c 的第一个数是 1。

一开始，有一个长为 n 的数组 a，下标从 1 开始。
Alice 和 Bob 玩游戏，Alice 先手：
每回合，当前玩家从 c 中选择一个 i（不超过 a 的长度），然后从 a 中移除 a[i]。
当 a 中只剩一个数时，游戏结束。
令 x 为最后 a 中剩下的数。Alice 希望最大化最终的 x，Bob 则希望最小化。两名玩家均采取最优策略。

你可以设定一开始的数组 a，要求 1≤a[i]≤m。
这一共有 m^n 种方案，每种方案可以得到一个 x。
输出这 m^n 个 x 之和，模 1e9+7。

"""
import itertools
import sys
from functools import cache
from math import inf
from operator import add, xor
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

def solve(n, m, k, c):

    # 用mask代表石头分布 0:1 1:2
    # f[i][mask] - 石头分布mask 前i个石头 - 这轮起手的人的最优策略
    # a ~ [1 2 1 2...] length-n

    # a操作 从 c=13479...枚举提取石子 剩余b的操作 f[i-1][mask1] mask1代表取走cj后 剩余石子分布
    # a在这种枚举选择最大
    # b枚举选择最小

    # sum(所有情况的最后一位)
    # 枚举最后等于的x=1...m=1e6 对应的方案数
    # 考虑最后=x 对应的博弈过程.
    # 倒数第一次枚举如果是b 则会挑选 >=x 如果是a则挑选<=x 的 -- 转换成binary情况
    # 01010... 最后剩余为0的博弈过程

    # 对于x 固定 f[i][mask] 为石头分布为mask 博弈最后剩余数字情况 0-<= 1- >

    # f[1][...] 只取决于mask首字母
    f = [mask & 1 for mask in range(1<<n)]
    g = [0]*(1<<n)

    # A希望最大化 选1-i个石头中的某个j 使得 max(f[i-1][mask1] -- mask1 是mask提取j后串位的结果
    c = [k-1 for k in c]
    for i in range(2,n+1):
        who = "A" if (n-i)%2 == 0 else "B"

        # 考虑前i个石头的排布 当前who先手
        for mask in range(0, 1<<i):

            cur = -inf if who == "A" else inf
            for k in c:
                if k >= i: break

                # pick k. all lower bit will be preserved. all higher bit will be move forward

                tmp = (1<<k)-1
                low = mask & tmp #all entry lower than k
                high = (mask >> 1) & (-1 ^ tmp)
                mask1 = low | high

                # print(k)
                # print(bin(mask))
                # print(bin(mask1))

                if who == "A":
                    cur = max_(cur, f[mask1])
                else:
                    cur = min_(cur, f[mask1])
            g[mask] = cur

        g, f = f, g

        #print(i, who, f[:(1<<i)])
    # return sum(x+1 for x in f)

    res = 0

    ps = [[1]*(n+1) for _ in range(m+1)] # ps[a][b] = a^b

    for i in range(1, m+1):
        for j in range(1, n+1):
            ps[i][j] = ps[i][j-1] * i % MOD

    @cache
    def get(cnt0, cnt1):
        # cnt0个0 对应 [1,x-1]
        # cnt1个1 对应 [x,m]

        # 对应0可以取任意 1...x-1
        # 1可以任意取 x...m

        # 枚举x 则

        # print(cnt0, cnt1)
        print(list((x, (x-1,cnt0),  ps[x-1][cnt0], (m-x+1,cnt1), ps[m-x+1][cnt1]) for x in range(1,m+1)))
        return sum(ps[m-x+1][cnt1] * ps[x-1][cnt0] % MOD for x in range(1,m+1))


    print(f)
    # last = "B" if (n-1) % 2 == 1 else "A"
    for s in range(1<<n):
        # if f[s] == 1: # <= x
        #     cnt1 = s.bit_count()
        #     cnt0 = n - cnt1
        #
        #     # [x+1,m] [1,x]
        #
        #     # res += sum(pow(m-x, cnt1, MOD) * pow(x, cnt0, MOD) for x in range(1,m+1))
        #     res += get(cnt0, cnt1)
        #     print(s, bin(s), f[s], "-", get(cnt0, cnt1))
        #     print()
        #     res %= MOD
        cnt1 = s.bit_count()
        cnt0 = n - cnt1

        # [x+1,m] [1,x]

        # res += sum(pow(m-x, cnt1, MOD) * pow(x, cnt0, MOD) for x in range(1,m+1))
        res += get(cnt0, cnt1)
        print(s, bin(s), f[s], "-", get(cnt0, cnt1))
        print()
        res %= MOD



    return res





    # t = (1<<j)-1
    # (mask & t) -- keep 1- j-1
    # -1 - t -- keep j-...
    # (mask>>1) &  (-1 - t) -- keep j... 的串位
    # mask1 = (mask & t) + (mask >> 1) & (-1 - t)


for _ in range(RI()):
    n, m = RII()
    k = RI()
    c = RILIST()
    print(solve(n, m, k, c))


