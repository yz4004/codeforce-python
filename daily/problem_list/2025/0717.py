"""
https://codeforces.com/problemset/problem/703/D

输入 n(1≤n≤1e6) 和长为 n 的数组 a(1≤a[i]≤1e9)。下标从 1 开始。
然后输入 m(1≤m≤1e6) 和 m 个询问。
每个询问输入 L R(1≤L≤R≤n)，请输出 a 的子数组 [L,R] 中的出现次数为偶数的元素，去重后的异或和。

考虑数组C:
c[i] = nums[i] 如果i是 nums[i] 在 [1,j]

"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

class BIT: # 维护区间sum(nums[l,r])
    def __init__(self, n: int):
        self.a = [0] * (n + 1)

    def add(self, i, x): # 原数组i映射到bit上需加一 nums[i] => a[i+1]
        i = i + 1
        a, n = self.a, len(self.a)
        while i < n:
            a[i] ^= x
            i += i & -i

    def sum(self, i: int): # nums[:i], [0,i) 这里无需串位，原数组i取不到
        res = 0
        while i > 0:
            res ^= self.a[i]
            i -= i & -i
        return res

    def rsum(self, l:int, r:int) -> int: # 区间sum(nums[l,r])
        return self.sum(r+1) ^ self.sum(l)

n, nums = RI(), RILIST()
ps = [0]*(n+1)
for i, x in enumerate(nums):
    ps[i+1] = ps[i] ^ x

queries = []
for i in range(RI()):
    l,r = RII()
    queries.append((l-1,r-1,i))
queries.sort(key=lambda x:(x[1],x[0]))

tree = BIT(n)

res = [0]*len(queries)
j = 0
last = {}
for i, x in enumerate(nums):
    if x in last:
        tree.add(last[x], x)
    tree.add(i, x)
    last[x] = i

    while j < len(queries) and queries[j][1] <= i:
        l,r,idx = queries[j]
        unique = tree.rsum(l,r)
        odd = ps[r+1] ^ ps[l]
        res[idx] = unique ^ odd
        # res.append((tree.rsum(l,r), idx))
        j += 1

sys.stdout.write("\n".join(map(str, res)))






