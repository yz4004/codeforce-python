"""
https://codeforces.com/problemset/problem/1912/K

输入 n(3≤n≤2e5) 和长为 n 的数组 a(1≤a[i]≤2e5)。

输出 a 有多少个长度至少为 3 的子序列 b，满足任意连续三个数之和 b[i]+b[i+1]+b[i+2] 一定是偶数。
答案模 998244353。

注：子序列不一定连续。

000
011
101
110


"""
from collections import defaultdict
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 998244353


def solve(n, a):

    # cnt = [0]*2 # cnt0/cnt1
    # f = [0]*4 # 00 01 10 11
    # 用计数变量 替代上面f的索引 代表以00/01...结尾的子序列

    # c0 c1 是 0/1计数 （不是以0/1结尾的子序列)
    # c00 c01... 是以 00/01 结尾的子序列
    c0 = c1 = 0
    c00 = c01 = c10 = c11 = 0

    # 注意 如果x=0 c00 += cnt0 这只生成二元对，我们希望所有c00结尾的子序列 包括3元更多
    # c00 += c00 + cnt0 -- 其中c00+[0] 代表3元以上 cnt0+[0] 代表新二元
    # c10 += c11 + cnt1 -- 其中c11+[0] 代表110取10 cnt1+[0] 代表二元10

    # 合法子序列 状态设计
    # 后缀状态 - 以01..后缀结尾的所有（合法）子序列
    # 计数状态 - 以某一pattern的所有计数
    # 分层长度 <k 的准备态 >=k合法态

    res = 0
    for x in a:
        x %= 2

        if x == 1:
            # 01 10 + [1]
            res += c01 + c10

            # t01 = c01 + (c10 + c00 + c0) 注意本题是要求出处合法 如果计入所有01结尾会算入 001 （由c00提供的）
            # t11 = c11 + (c01 + c11 + c1)
            # c01, c11 = t01, t11

            c11 += (c01 + c1) # 注意顺序如果先更新当前01 污染内部
            c01 += (c10 + c0)
            c1 += 1

        else:
            # 00 11 + [0]
            res += c00 + c11

            c00 += (c00 + c0)
            c10 += (c11 + c1)
            c0 += 1

        res %= MOD
    return res

n = RI()
a = RILIST()
print(solve(n, a))
sys.exit(0)



def solve(n, a):

    # cnt = [0]*2 # cnt0/cnt1
    # f = [0]*4 # 00 01 10 11
    # 用计数变量 替代上面f的索引 代表以00/01...结尾的子序列

    # c0 c1 是 0/1计数 （不是以0/1结尾的子序列)
    # c00 c01... 是以 00/01 结尾的子序列
    c0 = c1 = 0
    c00 = c01 = c10 = c11 = 0

    # 注意 如果x=0 c00 += cnt0 这只生成二元对，我们希望所有c00结尾的子序列 包括3元更多
    # c00 += c00 + cnt0 -- 其中c00+[0] 代表3元以上 cnt0+[0] 代表新二元
    # c10 += c11 + cnt1 -- 其中c11+[0] 代表110取10 cnt1+[0] 代表二元10

    res = 0
    for x in a:
        x %= 2
        # 01 10 + [1]
        # 00 11 + [0]

        if x == 1:
            res += c01 + c10

            t01 = c01 + (c10 + c00 + c0)
            t11 = c11 + (c01 + c11 + c1)
            c01, c11 = t01, t11
            c1 += 1

        else:
            res += c00 + c11

            t00 = c00 + (c10 + c00 + c0)
            t10 = c10 + (c01 + c11 + c1)
            c00, c10 = t00, t10
            c0 += 1

        res %= MOD
    return res

n = RI()
a = RILIST()
print(solve(n, a))
sys.exit(0)








# eoo
# oeo  oeooeoo...
# eee  eee.../ eeeooeoo...

# 两个o相当于一个e

# o o e o o e ..


# .oo e

#  eoo
#   oo
# .eoo

res = 0
f = defaultdict(int)

# f[0] f[1] f[01] f[10] f[11] f[00]

# 以0开头
# 000...
# 011
# 0110  - 合法的10后面只能接1
# 01101 - 合法的01后面只能接1
# 011011 - 合法的的11后面只能接0

# 以1开头
# 101
# 1011
# 10110
b0 = b1 = 0

c00 = c01 = c10 = c11 = 0
for i,x in enumerate(a):
    x %= 2
    if x == 0:
        res += c00 + c11

        c00 += c00 + b0 # c00+0 合法   c10+0 不合法
        c10 += c11 + b1 # c11+0 合法   c01+0 不合法
        b0 += 1

    else:
        res += c01 + c10

        c11 += c01 + b1    # c01+1 合法 c11+1 不合法
        c01 += c10 + b0    # c10+1 合法 c00+1 不合法
        b1 += 1

    b0, b1, c00, c01, c10, c11, res = b0%MOD, b1%MOD, c00%MOD, c01%MOD, c10%MOD, c11%MOD, res%MOD
print(res)

# for i,x in enumerate(a):
#     x %= 2
#     if x == 0:
#         res += f["00"] + f["11"]
#
#         f["00"] += f["0"]
#         f["10"] += f["1"] # 以1结尾也包含 01
#         f["0"] += 1 + f["0"] + f["1"]
#     else:
#         res += f["10"] + f["01"]
#
#         f["01"] += f["0"]
#         f["11"] += f["1"]
#         f["1"] += 1 + f["0"] + f["1"]
# print(res)


