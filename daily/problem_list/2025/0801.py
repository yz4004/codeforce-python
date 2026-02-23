"""
https://codeforces.com/problemset/problem/959/F

输入 n(1≤n≤1e5) q(1≤q≤1e5) 和长为 n 的数组 a(0≤a[i]<2^20)。下标从 1 开始。
然后输入 q 个询问，每个询问输入 i(1≤i≤n) 和 x(1≤x<2^20)。

对于每个询问，输出 a 的前 i 个数（下标 1 到 i）中的子序列个数，满足子序列的异或和恰好等于 x。
答案模 1e9+7。
注：子序列不一定连续。
"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7


# 线性基模板
class XorBasis:
    def __init__(self, n: int): # with n digits
        self.b = [0]*n
        self.zero = 0 # 自由度

    def insert(self, x):
        b = self.b
        while x:
            i = x.bit_length()
            if b[i] == 0: # 如果i位置没有基向量 则x作为基
                b[i] = x
                return
            x ^= b[i] # 否则消掉x最高位 尝试加入低位的基

        if x == 0:
            self.zero += 1

    def search(self, x) -> bool:
        b = self.b
        while x:
            i = x.bit_length()
            if b[i] == 0: # 如果i位置没有基向量 则x不能被表出
                return False
            x ^= b[i]
        return True

n, Q = RII()
nums = RILIST()
queries = []
for idx in range(Q):
    i,x = RII()
    queries.append((i,x,idx))
queries.sort()

# 预处理幂次
mod2 = [1]*(n+1)
for i in range(1, n+1):
    mod2[i] = mod2[i-1] * 2 % MOD

res = [0]*len(queries)
basis = XorBasis(21)
j = 0
for i, q, idx in queries:
    while j < i:
        basis.insert(nums[j])
        j += 1

    if basis.search(q):
        # res[idx]  = (1 << basis.zero) % MOD
        res[idx] = mod2[basis.zero]
print("\n".join(map(str, res)))



