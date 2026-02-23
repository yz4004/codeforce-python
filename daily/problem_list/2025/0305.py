s = input()
k = int(input())
n = len(s)
"""
严格划分出至少k个回文子串，允许修改

https://codeforces.com/problemset/problem/137/D

输入长度 ≤500 的字符串 s，包含大小写英文字母。
输入 k(1≤k≤|s|)。

每次操作，你可以把一个 s[i] 改成任意字符。
把 s 分割为至多 k 个非空子串，要求每个子串都是回文串，最少要修改多少次？

第一行，输出最少修改次数。
第二行，输出修改后的字符串，并用 '+' 表示分割位置，详见样例。
如果有多种分割方案，输出其中任意一种。

- 严格划分，上一个划分也是回文串截止位置，因为允许修改，只能从中心扩展转移. 同时从上一个划分的截止位置转移
- 返回一个instance，从最后一个dp状态向前回溯，通过状态计算关系转移，只需一个实例循环即可.
- 也可以在dp过程中记录from 当前状态由上一个哪个状态更新过来
- 对比0304不严格划分，我们这里只是定义结尾状态，无需额外做一次前缀和. （严不严格差个前缀和）
- 0304在有前缀和打包前缀信息的情况下需要做到O(nk) 本体严格划分信息不能打包，需要老式枚举每个子串，O(n^2*k)
- 有修改也提示只能中心拓展不能做到线性，不能manacher
"""

from math import inf
f = [[inf]*(k+1) for _ in range(n+1)] # f[i][j] 前i前缀串，划分出恰好j个，最小的改动次数
f[0][0] = 0

change = [[0]*n for _ in range(n)] # change[i][j] -- [i,j] 变成回文串需要改多少个数

for i in range(n):
    # [i]
    d = 0
    for j in range(0, min(i+1,n-i)): # 奇数长度回文串，以i中心
        d += 0 if s[i-j] == s[i+j] else 1
        change[i-j][i+j] = d
        # [i-j, i+j] 当前回文串划分
        for l in range(1, k+1):
            f[i+j+1][l] = min(f[i+j+1][l], f[i-j][l-1] + d) # 前一个划分位置 [0,i-j-1] 对应f是前i-j个

    d = 0
    for j in range(0, min(i + 1, n - i - 1)): # 偶数长度回文串，以 [i,i+1] 为中心
        d += 0 if s[i - j] == s[i + 1 + j] else 1
        change[i - j][i + j + 1] = d
        # [i-j, i+1+j]
        # f[i + j + 2] = min(f[i + j + 2], f[i - j] + d)
        for l in range(1, k+1):
            f[i+j+2][l] = min(f[i+j+2][l], f[i-j][l-1] + d)

# res = min(f[n][l] for l in range(k+1)) #at most
res = inf
seg = -1
for l in range(1, k+1):
    if f[n][l] < res:
        res = f[n][l]
        seg = l

# f[n][seg] 从最后一个状态出发，对上一个状态进行转移，因为是找一个路径即可，不需要dfs 循环即可

path = []
i,seg = n,seg # 最后一个状态出发
while seg:
    for j in range(i):
        if f[j][seg-1] + change[j][i-1] == f[i][seg]: # 当前回文串 [j,i-1]
            path.append(s[j:i])
            # dfs(i, seg-1)
            i, seg = j, seg - 1 # 上一个状态是 f[i][seg-1] 当前选择回文串划分 使得刚好
            break

# def dfs(n, seg):
#     nonlocal res
#     if len(path) == res: return
#     if seg == 0:
#         return
#     for i in range(n):
#         if f[i][seg-1] + change[i][n-1] == f[n][seg]:
#             path.append(s[i:n])
#             dfs(i, seg-1)
# dfs(n, seg)

instance = []
for part in path[::-1]:
    m = len(part)
    instance.append(part[:m//2] + part[:(m+1)//2][::-1]) # 创造出回文串，讨论奇偶，如果奇数 (m+1)//2 会保留中心
print(res)
print("+".join(instance))