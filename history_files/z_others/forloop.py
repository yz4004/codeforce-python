from math import comb

"""
k-for 无重复实际上就是求组合 c(n,k)
"""
n = 5
cnt = 0
for i in range(n):  # (n, k) k为循环深度
    for j in range(i+1,n):
        for k in range(j+1,n):
            cnt += 1
print(cnt, comb(5, 3))

cnt = 0
for i in range(n):  # 即n^3
    for j in range(n):
        for k in range(n):
            cnt += 1
print(cnt)

"""
k-for 无重复 dfs 选或不选形式
"""
def dfs(i, k):
    if k == 0:
        cnt[0] += 1
        return

    if i == n:
        return
    dfs(i+1, k)
    dfs(i+1, k-1)

n, k = 5, 3
cnt = [0]
dfs(0, k)
print(cnt, comb(n, k), cnt == comb(n, k)) # 可见相等

n, k = 7, 4
cnt = [0]
dfs(0, k)
print(cnt, comb(n, k), cnt == comb(n, k))