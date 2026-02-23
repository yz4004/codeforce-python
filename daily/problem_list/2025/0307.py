"""
https://codeforces.com/problemset/problem/17/E

输入 n(1≤n≤2e6) 和长度为 n 的字符串 s，只包含小写英文字母。

从 s 中选两个重叠（有公共部分）的非空回文子串，有多少种选法？
答案模 51123987。

- 正难则反，先考虑任意回文子串comb(x,2) 在减去不重叠的回文子串
- manacher计算回文子串 差分+三次前缀和
- pypy3 64超内存，换c++
- 参考其他人的提交 https://codeforces.com/contest/17/status
"""

import sys
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x


# import itertools
# from math import comb
import sys
mod = 51123987
# n = int(input())
# s = input()
n = int(sys.stdin.readline().strip())
s = sys.stdin.readline().strip()

def manacher(s):
    n = len(s)
    t = ["#"] * (2 * n + 1)
    for i, c in enumerate(s):
        t[2 * i + 1] = c

    m = 2 * n + 1
    z = [1] * (2 * n + 1)  # g[i]
    l = r = 0
    #  [l, r] 沿着l对称 x-l = l-y    y=2*l-x
    for i in range(m):
        # [l,r]
        if i <= r:
            z[i] = min(r - i + 1, z[2 * l - i])
        while i + z[i] < m and t[i + z[i]] == t[i - z[i]]:
            l, r = i, i + z[i]
            z[i] += 1
    return z  # 2*n+1

z = manacher(s) # s[i] -- z[2*i+1]/z[2*i+2]分别对应以i为心的奇偶回文半径 -- 折半向下取整 z[2*i+1]/z[2*i+2] // 2
# f[i] - 以i为结尾的回文子串的数量

f = [0]*(n+1)
for i in range(n):
    # 以i为心的奇/偶最长回文子串，[l,r] 说明任意以 i,i+1 ... r] 为右端点有一个回文子串，差分数组更新

    # [i-d+1, i, i+d-1] ... [i]
    d = z[2*i+1]//2
    f[i] += 1
    f[i+d] -= 1

    # [i-d+1, i, i+1, i+d] ... [i, i+1]
    d = z[2*i+2]//2
    f[i+1] += 1
    f[i+d+1] -= 1

'''
f = list(itertools.accumulate(f, lambda x, y: (x + y) % mod))[:n] # f[i] - 以i为结尾的回文子串的数量
# sum(f) 对应所有回文子串，comb(sum(f), 2) 作为第一项，任意选2
# 现在计算不重叠的两个回文子串, 枚举第二个回文子串（枚举的是中心），中心扩展进行dp转移 后进行前缀和优化
f = list(itertools.accumulate(f, lambda x, y: (x + y) % mod, initial=0)) # f[i] - 前i个前缀包含的所有回文子串的数量
TOTAL = f[n]
pre = list(itertools.accumulate(f, lambda x, y: (x + y) % mod, initial=0)) # 前缀和优化
'''

for i in range(1, n):
    f[i] = (f[i-1] + f[i]) % mod
f[-1] = 0

pre = [0]*(n+2)
for i in range(1, n+1):
    pre[i] = (pre[i-1] + f[i-1]) % mod

TOTAL = pre[n]
for i in range(1, n+2):
    pre[i] = (pre[i] + pre[i-1]) % mod

for i in range(n+1, 0, -1):
    pre[i] = pre[i-1]

cnt = 0
for i in range(n):
    # [i]
    # [i-d+1, i, i+d-1] ... [i] 枚举当前的第二个回文子串，则前一个回文串的所有选择是 f[i-d+1] ... f[i]
    d = z[2*i+1]//2
    # cnt += sum(f[j] for j in range(i-d+1, i+1))
    cnt += (pre[i+1] - pre[i-d+1]) % mod

    # [i,i+1]
    # [i-d+1, i, i+1, i+d] ... [i, i+1]
    d = z[2*i+2]//2
    # cnt += sum(f[j] for j in range(i-d+1, i+1)) # [:j)
    cnt += (pre[i+1] - pre[i-d+1]) % mod

# total = comb(f[n], 2)
total = int(TOTAL * (TOTAL-1)) // 2 % mod
print((total - cnt + mod) % mod)