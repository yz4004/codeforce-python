"""
https://codeforces.com/problemset/problem/1980/C

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5，m 之和 ≤2e5。
每组数据输入五行：
n(1≤n≤2e5)。
长为 n 的数组 a(1≤a[i]≤1e9)。
长为 n 的数组 b(1≤b[i]≤1e9)。
m(1≤n≤2e5)。
长为 m 的数组 d(1≤d[i]≤1e9)。

你需要对数组 a 执行 m 次修改操作，其中第 i 次操作把 a 中的某个数改成了 d[i]。

能否把 a 变成 b？
输出 YES 或 NO。

"""
import random
import sys, itertools
from functools import cache
from heapq import heappop, heapify, heappush
from math import inf, isqrt, gcd
from bisect import bisect_left
from collections import deque, defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

"""
数组构造题

4
3 1 7 8
2 2 7 10
5
10 3 2 2 1

只关注a/b不一样的部分 变数字没有顺序或其他限制 只看b在不在m中
但这题是必须变，不能跳过d里数字
假设d中有a不需要的数字，我们就随便挑个ab不一致的地方换了 一致也行 只要d后面能把它变回来
但如果d最后一个对不上a需要的数字就不行 （如果能对上 它就可以作为backup)

"""


# 1. 防止卡哈希 - 自定义包装类 + 重写hash
# 2. 生成随机盐值，防止哈希碰撞攻击
RANDOM_SALT = random.getrandbits(64)

# 3. 定义包装类
class Wrapper:
    __slots__ = 'val'  # 节省内存

    def __init__(self, val):
        self.val = val

    def __hash__(self):
        # 核心：异或随机盐，打乱哈希分布
        return hash(self.val ^ RANDOM_SALT)

    def __eq__(self, other):
        # 比较时解包比较真实值
        return self.val == other.val
# 4. 使用样例
#     w_x = Wrapper(x)
#     c = cnt.get(w_x, 0)

# 5. 更简洁的构造
"""
SEED = random.getrandbits(64)
def K(x):  # 把 int key 打散
    return x ^ SEED
    
ky = K(y)
if cnt[ky] == 0:...

https://chatgpt.com/c/6993cd6c-f418-832d-9d75-eb290a3028e4
"""



def solve(a,b,d):
    cnt = defaultdict(int)
    for x in d: cnt[Wrapper(x)] += 1

    for x,y in zip(a,b):
        if x != y:
            w_y = Wrapper(y)
            c = cnt.get(w_y, 0)
            if c == 0:
                return "NO"
            cnt[w_y] = c - 1
    return "YES" if d[-1] in b else "NO"


for _ in range(RI()):
    n, a, b, m, d = RI(), RILIST(), RILIST(), RI(), RILIST()
    print(solve(a,b,d))