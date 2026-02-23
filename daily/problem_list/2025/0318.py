"""
https://codeforces.com/problemset/problem/709/B

输入 n(1≤n≤1e5) x(-1e6≤x≤1e6) 和长为 n 的数组 a(-1e6≤a[i]≤1e6)。

一维数轴上有 n 个苹果，坐标记录在数组 a 中。
你一开始在 x 处。
你需要收集至少 n-1 个苹果。
输出最少移动距离。

进阶：改成收集 k(1≤k≤n) 个苹果呢？（见右侧题解）

- 行走模式是要么一边走到头，要么走一段再拐到另一边
- 本题明确n/n-1 所以只有一个点不必取到, 所以我们可以考虑子区间 [0,n-2] vs [1, n-1]
- 取一个子区间的苹果，本身走遍整个区间，再加上一个调转，x走到某个端点再折返，而这个逻辑也适用startPos子区间外
    d1 = a[-1] - a[1] + min(abs(x - a[1]), abs(a[-1] - x))
- 如果是k个，则枚举每个k子区间
- lc2106 固定距离
"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n, x = RII()
a = RILIST()
a.sort()

if n == 1:
    print(0)
else:
    d1 = a[-1] - a[1] + min(abs(x - a[1]), abs(a[-1] - x))
    d2 = a[-2] - a[0] + min(abs(x - a[0]), abs(a[n-2] - x))
    print(min(d1, d2))

# else:
#     if x <= a[0]:
#         print(a[-2] - x)
#     elif x >= a[-1]:
#         print(x - a[1])
#     else:
#         # [1, n-1] vs [0, n-2]
#         d1 = a[-1] - a[1] + min(abs(x - a[1]), abs(a[-1] - x))
#         d2 = a[-2] - a[0] + min(abs(x - a[0]), abs(a[n-2] - x))
#         print(min(d1, d2))


