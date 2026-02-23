"""
https://codeforces.com/problemset/problem/150/B

输入 n m k(1≤n,m,k≤2000)。

输出有多少个长为 n 的字符串 s，满足 s 中的每个长为 k 的连续子串都是回文串。
其中 m 为字母表的大小。
答案模 1e9+7。

进阶：做到 O(log n)。

- 连续回文数会引入大量限制，从回文中心考虑 如果偶数回文会导致中间所有的临项相等，奇数回文会导致隔项相等.
- 回文右半扇还能传递到左边，所以一般的，偶数长度k会导致全体字母一样=m 奇数会交错两种选择，m*m
- 不满足的特殊情况，恰好为k 则没有临项传递，变成一组回文的情况，长度不够k，不存在回文，每个k=1也不存在回文
- 只要n=k+1
"""
import sys
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
mod = int(1e9 + 7)

n, m, k = RII()
if k > n or k == 1:
    print(pow(m, n, mod))
elif k == n:
    print(pow(m, (n+1)//2, mod))
elif k % 2 == 0:
    print(m)
else:
    print(m*m%mod)
