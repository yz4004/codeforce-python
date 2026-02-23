"""
https://codeforces.com/problemset/problem/557/E

输入长度 ≤5000 的字符串 s，只包含 'a' 和 'b'。
设 t 是 s 的一个连续子串，长为 m，下标从 1 开始。如果对于 [1,(m+1)/2] 中的所有奇数下标 i，都满足 t[i] = t[m-i+1]，那么称 t 为半回文串。

然后输入正整数 k。
输出 s 的字典序第 k 小的半回文子串。
保证 k 不超过 s 的半回文子串的个数。

0110101
要求奇数部分回文，也就是s分两组奇偶组，每组找一个回文子串
（只关心偶回文）
检查s拆成的两组奇偶部分 (m+1)//2, m//2, 关心他们的


"""

import sys, math
from collections import defaultdict
from math import comb

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

s = list(map(lambda c: ord(c) - ord("a"), sys.stdin.readline().strip()))
k = RI()
n = len(s)
f = [defaultdict(int) for _ in range(n)] # f[i][j] - cnt 从i出发 长j的子串是半回文的 cnt
for i in range(n):
    # [i-j, i+j]
    for j in range(0,min(i+1,n-i),2):
        if s[i-j] != s[i+j]:
            break
        # [i-j, ..., i-2, i, i+2, ... i+j] palindrome at odd index, should note down [i-j,i+j] in trie
        f[i-j][2*j+1] += 1

    # [i-j, i+1+j]
    for j in range(0, min(i+1,n-i-1),2):
        if s[i-j] != s[i+1+j]:
            break
        # [i-j, ..., i-2, i, i+1, i+1+2, ... i+1+j]
        f[i-j][2*j+2] += 1

# print(f)
# build trie
N = (n+1)*n//2
nxt = [[0]*2 for _ in range(N+1)] # nxt[p][c] 节点p c分支映射的下一节点
cnt = [[0]*2 for _ in range(N+1)]

# insert/build
global_p = 0
for i in range(n):
    p = 0
    print(i, f[i])
    for j in range(max(f[i])):
        # [i, i+l)
        c = s[i+j]
        if not nxt[p][c]:
            global_p += 1
            nxt[p][c] = global_p
        cnt[p][c] += f[i][j + 1]
        p = nxt[p][c]
    print()

# print(cnt)
print()

# 在树上进行topk搜索
cnt_t = [0]*(N+1)
def dfs(i, c):
    cnt_t[i] = c
    if nxt[i][0]:
        p = nxt[i][0]
        dfs(p, c + cnt[i][0])

    if nxt[i][1]:
        p = nxt[i][1]
        dfs(p, c + cnt[i][1])
    print(i, cnt_t[i])
dfs(0, 0)
print(cnt_t)
total = cnt_t[0]
path = []
def dfs(i, k):
    if k <= 0:
        return

    left, right = nxt[i][0], nxt[i][1]
    if k <= cnt_t[left]:
        path.append("a")
        dfs(nxt[i][0], k)
    else:
        path.append("b")
        dfs(nxt[i][1], k - cnt_t[left])
# dfs(0, k)
print("".join(path))











