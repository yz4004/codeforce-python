"""
https://codeforces.com/problemset/problem/2014/D

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤1e5) d(1≤d≤n) k(1≤k≤n) 和 k 个闭区间，左右端点范围在 [1,n] 中。

输出两个数：
选一个长为 d 的范围 [i,i+d-1]（左右端点必须是 [1,n] 中的整数），这个范围与尽量多的闭区间有交集（只有一个点也可以），输出满足该要求的最小 i。
选一个长为 d 的范围 [i,i+d-1]（左右端点必须是 [1,n] 中的整数），这个范围与尽量少的闭区间有交集（只有一个点也可以），输出满足该要求的最小 i。
注：最大化/最小化与范围相交的区间个数，而非长度。

"""
import sys
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7
