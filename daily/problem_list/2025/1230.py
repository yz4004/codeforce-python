"""
https://www.luogu.com.cn/problem/P10031

输入 T(≤100) 表示 T 组数据。
每组数据输入 n(1≤n≤1e18)。

输出 gcd(n,1) XOR gcd(n,2) XOR gcd(n,3) XOR ... XOR gcd(n,n) 的结果。

"""
from collections import defaultdict
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

def solve(n):
    # n - 1e18
    # gcd(n,1) xor gcd(n, 2) ... gcd(n,n)

    # n = p^a
    # gcd(i, n=p^a)
    # - k=n//p = p^(a-1)个数 gcd(i,n) = p .... n//p
    # - phi(n) 个数与n互质 -- gcd(i,n) = 1 .... phi(n)


    # n = p1^a p2^b
    # k1 p1
    # k2 p2
    # k3 p1*p2

    # k3 = n//(p1 p2)
    # k1 = n//p1 - k3
    # k2 = n//p2 - k3

    # 考虑n的质因子 p1 ... pk
    # 容斥求出只被 pi*...pj 整除的系数 奇偶代表是否将 pi...pj 纳入xor

    # 考虑 gcd(i,n) = d
    # phi(n//d) 所有 1...n//d 中与 n//d 互斥的数 x. 则 gcd(x,n//d) = 1 gcd(x*d, n) = d
    # phi 除了1/2 都是偶数
    # 考虑
    # phi(2) 即 n//d = 2. -> d=n//2
    # phi(1)  n//d = 1 -> d = n

    if n % 2 == 0:
        return (n//2) ^ n
    return n




for _ in range(RI()):
    n = RI()
    print(solve(n))
