
"""
扩展欧几里得算法
问题 ax + by = gcd(a, b) 求 x y
bezout定理 一定存在一个 x y 使得上式有解



原理辗转相除法
a x + b y = (a, b)
a = q b + r

a x + b y = (qb + r)x + by = (qx + y)b + xr = (b ,r)

但反过来说，递归算法将 (a,b) 化简为一个更小的问题 (b, r) 假如我求出它的结果 x2 b + y2 r = gcd(a, b)
那就有
    qx + y = x2
    x      = y2

q是 [a/b] r是 a mod b = a % b
则 x = y2, y = x2 - [a/b]*y2

这对应下面的 y, x - (a//b) * y
那里的 x y 是递归算法的返回，即上文的 x2, y2

d 是gcd 因为所有人的gcd 都是 gcd(a, b)
(a, b) = (b, r1) = (r1, r2) ... (rn, rn+1)
最后一个 rn+1 | rn
倍数d (d * rn+1 = rn) 就是 gcd
所以下面递归算法返回的d是不变

递归边界
最后的 ax + by = gcd(a,b)
（a,b对应 rn, rn+1)
有 b | a
则 q = a//b, r = a%b = 0
再下一层递归传入参数即为 (b, 0) 而这个b就是gcd, 考虑式子 ax + by = gcd (这里a是形参 代入前面的b 所以a的系数x=1 y=0, gcd = a)
所以递归边界 when b = 0 返回 a, 1, 0
"""
import itertools
import math
# math.comb()

def Exgcd(a, b):
    if b == 0:
        return a, 1, 0
    d, x, y = Exgcd(b, a % b)
    return d, y, x - (a // b) * y

# - 返回三个参数，gcd，p, q
# - 递归的理解d, p q的计算,
#     d remains as same while recursion
#     (a,b) = (b, a mod b)  (a>b)
#     则 d = p*a + q*b = p'b + q'*r
#     即可以根据 (b, a mod b) 算得的对d的表示 递归的算出 (a,b) 对d的表示
# (也有迭代法 需要对式子变形即可，不需要用栈)

# 普通 gcd
def gcd(a, b):
    if b == 0:
        return a
    d = gcd(b, a % b)
    return d

# 迭代gcd
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
# 不用care a b 大小关系，因为a 小于 b 上面就发生一次swap 回到a > b的情况
# https://oi-wiki.org/math/number-theory/gcd/#%E6%AC%A7%E5%87%A0%E9%87%8C%E5%BE%97%E7%AE%97%E6%B3%95
# 递归深度/迭代次数
# 对a取mod -- 至少折半 (b=2) 所以是 loga / log(max(a,b))

"""
1. bezout 定理和辗转相除是一回事
    1.1 bezout定理可以应用于 ax + by = c 的不定方程判断，有解等价于 gcd(a,b) | c. 由特解+公式 得到通解，特解即为euclidean算法得到的系数
2. 在辗转相除的过程中，记住参数的变换过程可以帮我们得到 bezout定理的一个可行解，就是扩展欧几里得算法
    2.1 euclidean 本质是缩小问题，只需要自上向下，（所以迭代法很容易） ext euclidean 为了得到参数需要反向应用链式求余，得到参数，所以递归更容易 (当然也有迭代)
    2.2. 扩展欧几里得算法有矩阵表示
    
3. 乘法在同余意义下的逆元 即 ax = 1 mod n 知a求a的逆元x 即为 ax + kn = 1 该不定方程的一组解 ，且我们只关心 x, 由bezout定理，其有解条件即为 (a,n) = 1
    3.1 根据bezout ax + kn 有解要求 (a,n)=1. 求解a逆时直接带入 extgcd(a,n) 即可 a n 大小关系会在里面自动弄好，最后系数拿a对应的那个即可
    3.1 n个数的逆元 可以通过前缀积，最后只需要一次extgcd 然后逐个利用前缀即消除逆元
    https://oi-wiki.org/math/number-theory/inverse/#%E7%BA%BF%E6%80%A7%E6%B1%82%E9%80%86%E5%85%83

3.5 fermat小定理
    根据fermat小定理 a^(p-1) = 1 mod p， 如果n是素数，a^(p-2) 是a的一个逆元 a a^2 a^3 ... a^p-1 是关于同余乘法下的循环群 (extgcd不要求素数，但快速幂法要求素数)
    fermat小定理的归纳法证明思路
    假设 a^p = a 要证 (a+1)^p = (a+1) 这里a是任意整数， p为素数
    二项式展开 证明 p | c(p, k) （组合数 - p中选k） 这是显然的，因为分子无p 分母有p 且组合数为整数，所以每个二项系数都包含了p因子，即证明
    
4. 欧拉定理
    a^phi(m) = 1 mod m  (a, m) = 1
     
    phi(m) 欧拉函数为 m 同余系的互质数的个数 (p 即为 p-1)
    
    证明不能再用归纳和二项系数的整除性, 而是构造法 
    考虑m的互质剩余系 r1 ... rk k=phi(m), 将他们乘上一个a也是m的互质剩余系. a*ri, 两组剩余系都乘起来 放在等式两边既有 a^*phi(m) = 1 mod m   
    
    欧拉定义的推广, 其实是利用了 a^k 的循环性质，k无论多少我都知道他在循环群里，所以可以进行降幂
    
https://oi-wiki.org/math/number-theory/fermat/#%E6%89%A9%E5%B1%95%E6%AC%A7%E6%8B%89%E5%AE%9A%E7%90%86

    欧拉函数是对循环群往上看的，但没说那一定是最小的幂，最小的幂即循环群的真实size 即 d 使得 a^d = 1 mod m 这个最小的d 称为原根
    这个d整除所有的 k （a^k = 1) 这也是循环群的性质
"""
