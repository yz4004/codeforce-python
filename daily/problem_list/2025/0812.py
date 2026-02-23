"""
https://codeforces.com/problemset/problem/2053/C

输入 T(≤1e5) 表示 T 组数据。
每组数据输入 n k(1≤k≤n≤2e9)。

定义递归函数 dfs(L,R)：
1. 如果 R-L+1 < k，返回。
2. 设 M = floor((L+R)/2)。
3. 如果 R-L+1 是偶数，递归 dfs(L,M) 和 dfs(M+1,R)。
4. 否则，得到 M 分；然后，如果 L<R，递归 dfs(L,M-1) 和 dfs(M+1,R)。

递归入口为 dfs(1,n)。
输出总得分。

进阶：用 O(1) 时间解决每组数据。

"""
import sys
from functools import cache

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for _ in range(RI()):
    n, k = RII()

    def dfs(n):
        if n < k:
            return 0, 0

        cur = (n+1)//2
        cnt, s = dfs(n//2)

        s = cur * cnt + 2 * s
        cnt *= 2

        if n%2 == 1:
            cnt += 1
            s += cur

        return cnt, s

    print(dfs(n)[1])


