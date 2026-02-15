from math import isqrt

import math

#########################################################
##### 素因数分解
# 不是从 1-n 挨个试 x|n 复杂度是 o(n)
# 考虑n=p1^a1 * p2^a2 ... 如果从小到大尝试，一定会遇见第一个最小质因数，将其从n中完全清除得到一个更小的子问题 n=p2^a2 ...
def breakdown(N):
    result = []
    x = N  # 临时变量，会不断从x中移除起质因数分解的最小素数
    for i in range(2, math.isqrt(N) + 1):
        if x % i == 0:  # 如果 i 能够整除 x，说明 i 为 x 的一个质因子。
            while x % i == 0:
                x //= i
            result.append(i)
    if x != 1:  # 说明再经过操作之后 N 留下了一个素数
        result.append(x)
    return result
    # 1. isqrt(x) 返回 t:t^2 <= x
    # 2. for循环枚举所有小于等于 sqrt(x) 的素因子. if 枚举唯一可能的大于 x^(1/2) 的素因子
    #
    # 3. 如果x是合数
    #   一定存在 小于等于 sqrt(x) 的因子 （包括素因子）
    #   至多存在 一个大于 sqrt(x) 的素因子 会被最后if筛掉 （为什么至多一个？考虑素因数分解，把那个大于n^1/2除掉后，剩余部分都小于n^1/2）
    #
    # 4. 如果是素数 则唯一的素因子是本身 会被最后if 筛掉
    # 5. 复杂度 o(n^(1/2)) 考虑质因数分解，实际是是所有p1...pk的幂次之和


#########################################################
##### 因数分解 （因数成对）
def getFactors1(n): # for 循环形式利用 isqrt
    res = []
    for i in range(1, isqrt(n)+1): # isqrt返回 i: i*i <= n 所以加一取到大于等于的i
        if n % i == 0:
            res.append((i, n%i))
    return res

def getFactors2(n): # while 循环形式
    res = []
    i = 1
    while i*i <= n:
        if n % i == 0:
            res.append((i, n//i))
        i += 1
    return res


#######################################################
#####
##### 根号枚举vs因子枚举
