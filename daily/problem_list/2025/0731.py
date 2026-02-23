"""
https://codeforces.com/problemset/problem/1101/G

输入 n(1≤n≤2e5) 和长为 n 的数组 a(0≤a[i]≤1e9)。

把 a 分割成若干段（连续非空子数组），要求：从这些子段中任取若干子段，它们包含的所有数的异或和不能为 0。

输出最多能分成多少段。
如果不存在合法分割方案，输出 -1。

随便考虑一个数组的划分，从划分中任取若干段，里面包含的所有数在所有比特位上的 1 count 不全是偶数

101
101
111
010
所有异或和不为0 = 某一位必为奇数cnt
任取任意子段，其所有元素xor和不为0
- 每个子段本身xor>0, 任意子段集合的xor不为0

[j,i] 本身xor[j,i]>0
其xor和 考虑前面所有划分段的xor, 0不在这个子空间里
划分dp 对于每个i] 枚举左侧所有的非0 [j,i] 且 xor[j,i] 不能被 j-1] 左侧xor划分线性表出 （即作为一个新的基）


[a1, ] [a2, ] ... [ak, ]

"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7


n, nums = RI(), RILIST()
ps = 0

# 线性基模板
class XorBasis:
    def __init__(self, n: int): # with n digits
        self.b = [0]*n
        self.base_cnt = 0

    def insert(self, x):
        b = self.b
        while x:
            i = x.bit_length()
            if b[i] == 0:
                b[i] = x
                return
            x ^= b[i]

    def search(self, x) -> bool:
        b = self.b
        while x:
            i = x.bit_length()
            if b[i] == 0: # 如果i位置没有基向量 则x不能被表出
                return False
            x ^= b[i]
        return True


basis = XorBasis(31)
res = -1
for i in range(n):
    ps ^= nums[i]
    basis.insert(ps)

t = 0
for x in nums:
    t ^= x

if t:
    print(sum(1 for x in basis.b if x > 0))
else:
    print(-1)






