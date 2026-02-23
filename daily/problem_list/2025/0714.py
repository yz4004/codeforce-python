"""
https://codeforces.com/problemset/problem/2117/D

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(2≤n≤2e5) 和长为 n 的数组 a(1≤a[i]≤1e9)。

a 的下标从 1 开始。
每次操作，你可以：
对于每个 a[i]，执行 a[i] -= i。
或者，对于每个 a[i]，执行 a[i] -= n-i+1。

能否把 a 变成全 0 数组？
输出 YES 或 NO。

0...i, i+1...n-1

如果是分别操作则利用bezout定理 但本题是统一操作
    p*i + q*(n-i+1) = a[i] 线性组合 本题 p,q >= 0 因为操作只能减
    gcd(i, n-i+1) | a[i]
    or
    p*i + q*n - q*i + q = (p-q)*i + q*(n+1) = a[i]

找到p,q 对全体 a[i] 同时操作
p*i + q*n - q*i + q
= (p-q)*i + q*(n+1) = a[i]

a[i] 变成以 p-q 为公差的等差数列， offset是 q个 n+1
q >=0 正整数，上式不保证整除

"""
import itertools
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x


for _ in range(RI()):
    n, nums = RI(), RILIST()


    def check():
        d = nums[1] - nums[0] # = p-q

        C = nums[0] - d*1  # q*(n+1)

        # 1. 整除性 nums[0] - d*1 = q*(n+1) -- q不一定是正数 可以是个有理数 (nums[0] - d*1) // (n+1)
        if C % (n+1):
            return "NO"

        # 2. p,q 非负系数
        # 检查整数公差 + 给定整数输入 只保证整数，不保证offset是非负数，offset非负
        q = (nums[0] - d*1) // (n+1)
        if q < 0 or d+q < 0: # q,p>=0
            return "NO"

        # 3. 公差
        if any(y-x != d for x,y in itertools.pairwise(nums)):
            return "NO"

        return "YES"
    print(check())
    #https://chatgpt.com/c/68747c7b-e694-800a-af28-cc31c0583e79
    #guard clause, 一系列if assertion 保证安全，提前返回错误，便于debug
