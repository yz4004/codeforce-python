"""
https://codeforces.com/problemset/problem/1931/D

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(2≤n≤2e5) x y(1≤x,y≤1e9) 和长为 n 的数组 a(1≤a[i]≤1e9)。

输出有多少个下标对 (i,j) 同时满足：
1. i < j。
2. a[i]+a[j] 是 x 的倍数。
3. a[i]-a[j] 是 y 的倍数。

ai+aj = k*x
ai-aj = k*y

ai = k*x - aj = -aj mod x
ai = k*y + aj = aj mod y

9 + 1 = 2*5 ----- 9 = -1 mod 5
9 - 1 = 4*2 ----- 9 =  1 mod 2


所以 需要同时满足
ai = -aj mod x
ai = aj mod y

即 同时满足，维护左侧 (-aj % x, aj % y) 枚举右侧 (ai%x, ai%y)
ai%x == -aj % x
ai%y == aj % y

ps: 1. 同时满足用 tuple
    2. -ai % x 负数运算优先级高于% 输出正数

"""
import sys
from collections import defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7


for _ in range(RI()):
    n, x, y = RII()
    a = RILIST()

    res = 0
    pre = defaultdict(int)
    for ai in a:

        t = (ai % x,  ai % y)
        if t in pre:
            res += pre[t]

        r = ((-ai) % x, ai % y)
        pre[r] += 1
    print(res)


