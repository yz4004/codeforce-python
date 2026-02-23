"""
https://codeforces.com/problemset/problem/2001/D

输入 T(≤5e4) 表示 T 组数据。所有数据的 n 之和 ≤3e5。
每组数据输入 n(1≤n≤3e5) 和长为 n 的数组 a(1≤a[i]≤n)。

从 a 中选择一个子序列 b，满足：
1. b 包含 a 中的所有元素，无重复元素。（相当于把 a 去重）
2. （b 的下标从 1 开始）如果把 b 的奇数下标的元素乘以 -1，得到的新序列 c 的字典序是最小的。

输出 b 的长度，以及 b。

"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

print(bin(37))
print(hex(37))
x = 0x3f3f3f3f3f
print(x)
# for _ in range(RI()):
#     n, nums = RI(), RILIST()
#
#     # [


