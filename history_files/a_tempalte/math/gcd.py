"""
    批量更新 gcd
    gcd(x,y) = gcd(y%x, x)  where x<y
"""
N = 13
g = [[1]*N for _ in range(N)]
for i in range(1, N):
    for j in range(1, i+1):
        if i % j == 0:
            g[i][j] = g[j][i] = j
        else:
            g[i][j] = g[j][i] = g[j][i%j]


