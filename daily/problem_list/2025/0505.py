"""
https://codeforces.com/problemset/problem/1989/B

输入 T(≤1e3) 表示 T 组数据。
每组数据输入两个长度 ≤100 的字符串 s 和 t，只包含小写英文字母。

构造一个字符串 a，使得 s 是 a 的子串，且 t 是 a 的子序列。
输出 a 的最短长度。

- 不是 scs （shortest common supersequence） 这里要求s是子串，t子序列
- s完整出现，t在s中尽可能找最长子序列 （s包含t[i:j]最长子序列）剩余附在两端

"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

def solve(s:str, t:str) -> int:
    m, n = len(s), len(t)
    res = 0
    # t[i:] 在 s中出现的最长子序列
    for i in range(n):
        k = 0
        for j in range(m):
            if t[i+k] == s[j]:
                k += 1
                if i+k == n:
                    break
        res = mx(res, k)
    return m + n - res


m = RI()
for _ in range(m):
    s, t = RS(), RS()
    print(solve(s, t))

sys.exit(0)

def solve(s:str, t:str) -> int:
    # 最短公共超序列a s/t为a的子序列且尽可能短
    # i]      i-1] i     i-1] i
    # j]        j]       j-1] j
    # f[i][j]
    m, n = len(s), len(t)
    f = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): f[i][0] = i
    for j in range(n+1): f[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s[i-1] == t[j-1]:
                f[i][j] = f[i-1][j-1] + 1
            else:
                f[i][j] = mn(f[i-1][j], f[i][j-1]) + 1

    return f[m][n]

m = RI()
for _ in range(m):
    s, t = RS(), RS()
    print(solve(s, t))
