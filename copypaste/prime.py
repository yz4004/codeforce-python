import math
from collections import defaultdict
from typing import List

"""
1. euler 线性筛
2. 埃氏筛
3. is prime
4. 根号复杂度返回x的因子
5. 倍数枚举预处理因子 - 对1-1e5每个数 列出全部因子 
    处理因子两种方法: 根号枚举/倍数调和级数枚举
    

"""

# 1. Euler 线性筛 + spf (smallest prime factor)
def euler_sieve(N):
    primes = []
    is_prime = [True] * (N+1)
    is_prime[0] = is_prime[1] = False
    spf = [0]*(N+1)   # spf[x] = x 的最小质因数

    for i in range(2, N+1):
        if is_prime[i]:
            primes.append(i)
            spf[i] = i

        # 按递增素数p 作为spf去筛 t=p*i 保证每个p是x的spf (当p到达i的spf就应停止 见下break)
        for p in primes:
            t = i * p
            if t > N: break

            spf[t], is_prime[t] = p, False

            if i % p == 0: # p|i 从小到大遍历p 的第一个 p|i 说明p=spf[i] 对后面大于p的 p'*i 就多余了，因为p`*i已被i的spf过滤掉
                break
    return primes, is_prime, spf
N = 10 ** 6
prime, is_prime, spf = euler_sieve()

def factorize(x) -> List:
    res = []
    while x > 1:
        p = spf[x]
        cnt = 0
        while x % p == 0:
            x //= p
            cnt += 1
        res.append((p,cnt))
    return res

"""
线性欧拉筛 + smallest prime factor
1. 每个合数只被其最小素因子筛除一次 n = p_min * k
2，外层for遍历乘数i，然后作用于当前找到的所有素因子，从小到大 直到遍历到i的最小素因子 p_min_i 
（如果再超过这个数，筛到的合数实际上会以i的最小素因数为最小素因数，违背了只被最小素因数筛一次的要求，重复筛了）
3. 代码上对应的就是一旦发现 p | i 时就截止循环。（保证每个合数只被筛一次）
"""


# 2. 埃氏筛
def Eratosthenes(n: int) -> list:
    prime = []
    is_prime = [True]*(n+1) # 每个数去更新其倍数，没被更到的就是质数
    for i in range(2, math.isqrt(n) + 1):
        if is_prime[i]:
            prime.append(i)
        # for multiple in range(i*i, n+1, i): 其实加法更快一些，乘法理解性好
        #     is_prime[multiple] = False
        for factor in range(i, n+1):
            if factor * i > n:
                break
            is_prime[factor * i] = False
    return prime, is_prime
"""
埃氏筛
1. 外层循环 i - 以每个数 i 去更新其倍数 - 都是合数
2. 只需从大于i的因子开始更新 i*i i*(i+1) ... i*j (j>i)
    因为小于i的乘数 k 已经在之前筛过了 i*k = k*i （此前k作为外层循环的数，更新过k*i 那是i是大于k的乘数
"""


# 3. is prime
def is_prime(x):
    if x <= 1: return False
    k = 2
    while k * k <= x:
        if x % k == 0:
            return False
        k += 1
    return True

# 4. 根号复杂度返回x的因子
def get_factors(x):
    factors = []
    for d in range(1, math.isqrt(x) + 1): # 没有isqrt用while loop
        if x % d == 0:
            factors.append(d)
            if d * d < x:
                factors.append(x//d)
    return factors

# 5. 倍数枚举预处理因子 - 对1-1e5每个数 列出全部因子
def preprocess_factors(N=10 ** 5 + 1):
    factors = [[] for _ in range(N)]
    for d in range(1, N): # d是谁的因子?
        for x in range(d, N, d): #d是x的因子
            factors[x].append(d)
    return factors


"""
线性质数筛的详细过程： 
考虑每个合数的最小素因子 
    一个合数 = 最小素因子 * 其他
再已获得一些最小质数的情况下，去遍历那个其他 
从2。。。 n-1遍历【其他】
对每个 i 其乘以已经找到的素数，筛掉一部分合数，【这部分合数是以那个素因数为最小素数的】
2 3 4 5 6 。。。  --- 外层遍历
【2】             --- 当前质数
2                --- 当前for遍历到的i 最小素因子对应的乘数
2*2              --- 能筛掉谁

【2，3】
3
3*2 3*3

【2，3】
4
4*2  4*3 【这个4*3 其实不能在这里重复筛，要给 6*2筛】

【2，3，5】
5
5*2， 5*3  5*5

【2，3，5】
6
6*2 6*3 6*5

可以感受到 每个合数，最后都被其最小素因数筛掉了，当然遍历过程中 我们遍历的是最小素因数对应的系数

上面可以观察到 6*2 = 12 已经被 3*4 筛掉了

其实12的最小质因子是2 我们如果想保证线性 就让每个合数被他的最小素因数唯一触碰

所以再4*3那里，因为4是被2整除的，所以用4去遍历其他质数的到的合数，将来会被某个 因数*2筛掉 （如6*2） 

假设遍历到乘数 i 他的最小素因数是 pk

p1 p2 p3 。。。 pk pk+1 。。。

i乘上小于pk得到的合数是没毛病的，那些合数的最小素因数是 p1 p2 。。。 pk-1
乘上 pk 也需要 因为得到的数 pk*i 仍以pk为最小素因数 (此时不乘以后就没机会了, 假设每个合数都只会被其最小素因子触碰一次）
但进一步对于 pk+1 后面的数
i*pj (pj > pk) 得到的合数 不是以pj 为最小素因子的，而是以i的最小素因子 pk 为最小的
实际上应该让 pk * （i / pk） * pj
等外层循环遍历到 （i / pk） * pj 去筛
这对所有大于pk的当前素数都是成立的
所以当i超过了 最小素因子 pk 后就不能继续了，都会造成重复访问

如此这样 我们证明了每个合数都只会被筛去一次，即被其最小素因子筛去一次
假设对于某一个合数其最小素因数是pk
t = pk * i
i 不能有小于等于pk的因子
依据上述过程，这个数只会被pk筛掉一次，即当pk * i 外层遍历到i时

t会被他某个非最小素因数重复筛吗？ (形式化的描述上文break的作用)
设t有非最小素因数 pj： pj * （t / pj）= pj * （pk * i / pj） where pj > pk 
筛法的双for循环只能是这种形式
t/pj = pk * i / pj 小于 i，因为pk小于pj 分母大的反而小 这个数会在外层循环中 先于 i 被遍历到
但是因为我们检查 i 一旦超过了 i的最小素因数 p_mi 就会截止循环，
根据上面的假设 pk * i i没有小于pk的因子 所以 pj > p_mi >= pk 而到p_mi就截断，所以任何t到非最小素因数 pj 都不会筛t
"""


"""
本题可以测试筛法：
一道单调栈题，但要求出所有每个数的质数分数（所有的质因子数量）
求出质数分数，一种做法是先求出范围内所有质因子，然后考虑每个数的素数构成，即利用素数分解，简单dp
但更高效的方法是从每个素数出发去更新其倍数，类似埃氏筛，不提前截断，要的就是重复更新
https://leetcode.cn/problems/apply-operations-to-maximize-score/
"""














