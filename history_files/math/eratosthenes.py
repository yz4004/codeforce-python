"""
想知道小于等于n的所有素数

1. 暴力逐个判断
2. eratosthenes numberTheory
    一个数的倍数肯定是合数，所以遍历1-n 计算每个数的所有倍数 标记成合数 剩下的是素数
    具体的，遍历到i时，考虑i所有的倍数 1*i 2*i ... i*i  停在i+1 它属于下一个数的考虑 (i+1*i)
    也就是对一个数i 只考虑小于等于它的因素

    假如一个数平方超过n 我们就不考虑这个数了 j*i (j<i) 已经在

"""
import math


# 暴力，逐个判断
def isPrime(x):  # 用 2 - sqrt(n) 的因数去整除n
    k = 2
    while k * k <= x:
        if x % k == 0:
            return False
        k += 1
    return True

def isPrime(n: int) -> bool:
    return all(n % i for i in range(2, math.isqrt(n) + 1)) # isqrt integer square root （向下取整）

# 如果当前遍历到素数，（之前遍历过的数中，没有因子更新它为false），则考虑其所有倍数
# 这中间有很多重复 比如 p*q 过去/将来也会有 q*p，实际上一个数对被重复计入了一次
def Eratosthenes(n: int) -> list:
    prime = []
    is_prime = [True] * (n+1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, n + 1):
        if is_prime[i]:
            prime.append(i)
            # [i, n]
            for j in range(i+i, n + 1, i):
                is_prime[j] = False
    print(is_prime)
    return prime

N = 100
prime = []
is_prime = [False] * N
# 相比上个实现 只考虑 单向的倍数，即 p*q 永远考虑 q >= p
# 因为对于 2*p ... (p-1)*p 其实这些数都被 以2 3 。。。 p-1为出发点 的p的倍数更新过了
def Eratosthenes(n):
    is_prime[0] = is_prime[1] = False
    for i in range(2, n + 1):
        is_prime[i] = True
    for i in range(2, n + 1):
        if is_prime[i]: # 遍历到一个素数，从其平方开始出发。不考虑 j*p (j<p) 因为小于它的倍数乘数，已经在之前的倍数中考虑过了
            prime.append(i)
            if i * i > n: #如没有更大的倍数 则跳过，（这里不能break 因为后面可能有更大的素数，需要append，如果不需要prime 则可以直接break）
                continue
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

# 只需筛到平方根
def Eratosthenes(n):
    is_prime[0] = is_prime[1] = False
    for i in range(2, n + 1):
        is_prime[i] = True
    # 让 i 循环到 <= sqrt(n)
    for i in range(2, math.isqrt(n) + 1): # `isqrt` 是 Python 3.8 新增的函数
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    for i in range(2, n + 1):
        if is_prime[i]:
            prime.append(i)

prime = []
is_prime = [True]*N
def eular(n):
    for i in range(2, n+1):
        if is_prime[i]:
            prime.append(i)
        for p in prime:
            if i * p > n:
                break
            is_prime[i * p] = False
            if i % p == 0:
                break



if __name__ == '__main__':

    print(Eratosthenes(10))