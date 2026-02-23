

"""
模质数下的组合数
取模快速幂
lucas定理 大数模小素数/小合数
组合数递推
拓展欧几里得算法 辗转相除
中国剩余定理 crt
"""
from math import comb


# 模质数下的组合数
def comb_mod():
    """
    comb(n,k) = n!/(n-k)! k!
    利用乘法逆元计算 mod 质数下的组合数 comb(n,k) mod p.
    """
    MOD = 1_000_000_007
    MX = 1000
    fac = [0] * (MX + 1)  # f[i] = i!
    fac[0] = 1
    for i in range(1, MX + 1):
        fac[i] = fac[i - 1] * i % MOD

    inv_fac = [0] * (MX + 1)  # inv_fac[i] = i!^-1  i的阶乘在模p=10**9+7下的乘法逆元
    inv_fac[-1] = pow(fac[-1], MOD - 2, MOD)  # pow(fac[-1], -1, MOD) 等价写法
    for i in range(MX - 1, -1, -1):
        inv_fac[i] = inv_fac[i + 1] * (i + 1) % MOD

    def comb(n, m):
        if n < m or m < 0: return 0
        # n!/m! (n-m)!
        return (fac[n] * inv_fac[m] * inv_fac[n - m])
    # ref
    # https://leetcode.cn/discuss/post/3584387/fen-xiang-gun-mo-yun-suan-de-shi-jie-dan-7xgu/

# 取模快速幂
def mod_pow(a, e, mod=10**9+7):
    # a^e  e=0b1011
    # 不断计算a a^2 a^4 ... a^(1<<k) 同时如果e在k-bit是1 apply a^(1<<k) 到a^e
    res = 1
    a %= mod
    while e:
        if e & 1:
            res = res * a % mod
        a = a * a % mod
        e >>= 1
    return res

# lucas定理 大数模小素数/小合数
def lucas(p):
    """
    n,k - 1e9， p很小的素数
    返回 comb(n,k) mod p
    """

    # 预处理 fac/inv_fac 应对小于p的组合数
    def lucas_prepare(p):
        fac = [1] * p
        for i in range(1, p):
            fac[i] = fac[i - 1] * i % p
        inv_fac = [1] * p
        inv_fac[p - 1] = pow(fac[p - 1], p - 2, p)  # Fermat inverse
        for i in range(p - 2, -1, -1):
            inv_fac[i] = inv_fac[i + 1] * (i + 1) % p

    # 小 n,k 组合数
    def comb(n, k, p, fac, inv_fac):
        # 0 <= n,k < p
        if k < 0 or k > n: return 0
        return fac[n] * inv_fac[k] * inv_fac[n-k] % p

    def lucas(n, k, fac, inv_fac):
        # c(n,k) mod p
        if k < 0 or k > n: return 0

        res = 1
        while n > 0 or k > 0:
            ni, ki = n % p, k % p
            # n = n0 + n1*p + n2*p^2 ... 从低到高枚举ni
            if ki > ni:
                return 0
            res = res * comb(ni, ki, p, fac, inv_fac) % p
            n, k = n//p, k//p
        return res

    # ====== 用法示例 ======
    # p = 1000003  # 素数
    # fac, inv_fac = lucas_prepare(p)
    # print(lucas(10**18, 10**9, p, fac, inv_fac))


    # ps 当p<5000 也可以递推预处理 comb(n,m)
    def lucas_prepare_pascal(p: int):
        C = [[0] * p for _ in range(p)]
        for n in range(p):
            C[n][0] = 1
            for k in range(1, n + 1):
                C[n][k] = (C[n - 1][k - 1] + C[n - 1][k]) % p
        return C

    def lucas_pascal(n: int, k: int, p: int, C) -> int:
        if k < 0 or k > n:
            return 0
        res = 1
        while n > 0 or k > 0:
            ni = n % p
            ki = k % p
            if ki > ni:
                return 0
            res = res * C[ni][ki] % p
            n //= p
            k //= p
        return res


    def lucus_mod10():
        # lc3463 https://leetcode.cn/problems/check-if-digits-are-equal-in-string-after-operations-ii/
        # 求 (n,k) mod 10
        # 1. 先求对每个质数幂的mod
        #   x = r2 mod 2
        #   x = r5 mod 5
        # 2. mod10即找出r 同时满足上两式. 解同余方程
        # 3. 解同余方程可以用 crt 但10枚举即可

        def comb2(n, k):
            return 1 if (n & k) == k else 0

        n = 5
        C = [[1] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            for j in range(i+1):
                C[i][j] = C[i-1][j] + C[i][j-1]

        def comb5(n, k):
            # 考虑 n,k在5进制下的log分解 n = n0 + n1 * 5 + ... ni *5^i
            # comb(n,k) % 5 = prod of comb(ni,ki) % 5
            res = 1
            while n > 0 and k > 0:
                i = n % 5
                j = k % 5
                res *= C[i][j]
                res %= 5
                n //= 5
                k //= 5
            return res

        def comb10(n, k):
            r2 = comb2(n, k)  # 01
            r5 = comb5(n, k)  # 01234
            # comb(n, k) % 10 = r

            # 解同余方程
            # r2 mod 2
            # r5 mod 5
            # ? mod 10 -- 即找10的余数 同时满足上面两个条件
            # 1. 枚举所有10的余数 满足上面两个条件
            for r in range(10):
                if r % 2 == r2 and r % 5 == r5:
                    return r
            return -1







    """
    乘法逆元 - a * b = 1 mod p 
    根据fermat小定理 a^(p-1) = 1 mod p. 
    a在模质数p下 的乘法逆元是 a^(p-2) 
    所以对于模MOD，对应逆元 a^(MOD-2)
    
    i! 的乘法逆元是 rev_i. 分一个i出去就得到 (i-1)! 逆元 以此类推 
    """

    """
    comb(n,k) = n!/(n-k)! k!
    当 n,k 特别大 (1e9) 无法与处理 fac 和 inv_fac 序列 
    不过如果p很小 仍有办法

    n = n0 + n1*p + n2*p^2 ... 
    k = k0 + k1*p + k2*p^2 ...
    将n,k按p进制分解 得到对应的系数 (n0...) (k0...) log级别 

    根据lucas定理 
    (n,k) = (ni,ki) mod p 的乘积
    
    (a+b)^p = a^p + b^p mod p
    p | (p, k) for k < p

    """


# 组合数递推
def combination_recurrence(N=5000):
    # c(n,k) = c(n-1, k-1) + c(n-1, k)
    # dp递推 选或不选，选第n个元素，不选第n个元素

    N = 5000
    c = [[1] * (N + 1) for _ in range(N + 1)]  # 初始所有人是1 这包含边界条件 g[i][j], g[i][0] = 1
    for i in range(1, N + 1):
        for j in range(1, i + 1):
            c[i][j] = c[i - 1][j] + c[i - 1][j - 1]
            # assert g[i][j] == math.comb(i, j)


# 拓展欧几里得算法
def extented_euclidan():
    def extgcd(a, b):
        """
        d = gcd(a,b) = x*a + y*b
        返回 gcd(a,b) 已经对应的线性组合系数 x,y (根据bezout定理）
        """
        if b == 0:
            return a, 1, 0
        d, x, y = extgcd(b, a % b)
        return d, y, x - (a // b) * y

    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a


# 中国剩余定理 crt
# - 以2元同余方程为例
def crt_pair():
    def extgcd(a, b):
        """
        d = gcd(a,b) = x*a + y*b
        返回 gcd(a,b) 已经对应的线性组合系数 x,y (根据bezout定理）
        """
        if b == 0:
            return a, 1, 0
        d, x, y = extgcd(b, a % b)
        return d, y, x - (a // b) * y

    def crt_pair(a, m, b, n):
        """
        解
        x = a mod m
        x = b mod n

        返回 (x0, l) 表示：
            x ≡ x0 (mod l)
        若无解，返回 None
        """

        d, x, y = extgcd(m, n)  # x*m + y*n = d
        if (b - a) % d != 0:
            return None

        diff = b - a

        # 在模 n/d 下求 t： (m/d)*t ≡ diff/d (mod n/d)
        md = m // d
        nd = n // d

        # x 是 md 在模 nd 下的逆元（因为 x*m ≡ d (mod n) => x*md ≡ 1 (mod nd)）
        t = (diff // d) * x
        t %= nd

        x0 = a + m * t
        l = m * nd  # lcm(m,n) = m*(n/d)

        x0 %= l

        return x0, l


    """
    x = a1 mod m1
      = a2 mod m2 
      
      
    x = a1 * s + a2 * t 
    
    x mod m1 
    =>
        (a1 * s + a2 * t) mod m1 
        保留 a1 mod m1
        前面项目 s = 1 mod m1  
        后面项目 t = 0 mod m1 
    
    x mod m2 
    =>
        (a1 * s + a2 * t) mod m2 
        保留 a2 mod m2
        前面项目 s = 0 mod m2
        后面项目 t = 1 mod m2 
    
    s = 1 mod m1   
    s = 0 mod m2
        s = p*m2 
        p*m2 = 1 mod m1 
        p即为 m2在模m1下的乘法逆 p=m2^-1 mod m1 -- 这要求乘法逆存在 bezout (m1,m2)=1 
        
        s = (m2^(-1) mod m1) * m2
    
    t = 0 mod m1
    t = 1 mod m2
    
        t = q*m1 
        q*m1 = 1 mod m2 
        q即为 m1 在模m2下的乘法逆 q=m1^-1 mod m2
        
        t = (m1^(-1) mod m2) * m1
    
    所以最后构造是
        x = a1 * s + a2 * t  mod m1*m2 
        where 
        s = (m2^(-1) mod m1) * m2
        t = (m1^(-1) mod m2) * m1
        
    ref https://chatgpt.com/c/69523e52-688c-8328-b5bd-8c4b878740ff
    """

"""
欧拉函数
phi(x) -> 计算单个元素的欧拉函数 即1-x) 互质数

参考
https://chatgpt.com/c/695715c2-1914-832a-b9eb-f1fec6189aea
"""
# 计算欧拉函数（n 以内的与 n 互质的数的个数）
# phi(n) = n * prod( (1 - 1/p) for p|n) 利用欧拉函数公式
def phi(n: int) -> int:
    res = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            res = res // i * (i - 1)  # (1 - 1/i) i是当前n的最小素因子
            while n % i == 0: # 清除i因子
                n //= i
        i += 1
    if n > 1:
        res = res // n * (n - 1)
    return res


# 线性筛预处理欧拉函数
# phi(i * p) = phi(i) * p     for p|i
# phi(i * p) = phi(i) * (p-1) for (p,i) = 1
def phi_sieve(n: int):
    phi = [0] * (n + 1)
    primes = []
    is_comp = [False] * (n + 1)
    phi[0] = 0
    if n >= 1:
        phi[1] = 1
    for i in range(2, n + 1):
        if not is_comp[i]:
            primes.append(i)
            phi[i] = i - 1
        for p in primes:
            v = i * p
            if v > n:
                break
            is_comp[v] = True
            if i % p == 0:
                phi[v] = phi[i] * p
                break
            else:
                phi[v] = phi[i] * (p - 1)
    return phi

