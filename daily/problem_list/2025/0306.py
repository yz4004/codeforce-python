import itertools

"""
https://codeforces.com/problemset/problem/835/D

输入长度 ≤5000 的字符串 s，只包含小写英文字母。

如果字符串 s 是回文串，我们称 s 为 1 阶回文串。
如果字符串 s 的左半部分等于 s 的右半部分，且左半部分和右半部分都是 k-1 阶回文串，我们称 s 为 k 阶回文串（k > 1）。
注：设 m = floor(len(s)/2)，「左半部分」指 s 的长为 m 的前缀，「右半部分」指 s 的长为 m 的后缀。

输出 n 个数，分别表示 s 的 1,2,3,...,n 阶非空回文子串的个数。

- 如果是回文串，再考虑半串的阶数，在经典n^2 计算回文子区串的基础上修改. 

"""

s = input()
n = len(s)
# 1 2 3 ... n
# f[i][j]

# 区间dp写法n^2计算回文子串 （也可以用中心扩散法）
# f = [[False]*n for _ in range(n)]
# for i in range(n-1, -1, -1):
#     f[i][i] = True
#     if i+1<n: f[i+1][i] = True
#     for j in range(i+1, n): # i-1
#         # [i,j]
#         # i [i+1, j-1] j
#         f[i][j] = f[i+1][j-1] and s[i] == s[j]
# print(f)

# res = [0]*n
d = [0]*(n+1)
f = [[0]*n for _ in range(n)]
# f[i][j]
for i in range(n-1, -1, -1):
    f[i][i] = 1
    if i+1<n: f[i+1][i] = 1
    for j in range(i+1, n): # i-1
        # [i,j]
        # i [i+1, j-1] j
        if f[i+1][j-1] and s[i] == s[j]:
            m = j-i+1
            # [i:i+m//2] [i+(m+1)//2,j]
            f[i][j] = f[i][i+m//2-1] + 1

            # [i,j] 是k阶，也一定是k-1阶，差分对所有 1...k阶进行更新
            d[0] += 1
            d[f[i][j]] -= 1

res = list(itertools.accumulate(d))[:n]
res[0] += n
print(" ".join(map(str, res)))