"""
https://atcoder.jp/contests/abc378/tasks/abc378_e

输入 n(1≤n≤2e5) m(1≤m≤2e5) 和长为 n 的数组 a(0≤a[i]≤1e9)。

定义 f(b) = sum(b) % m。
输出 a 的所有非空连续子数组 b 的 f(b) 之和。

- 思路1 枚举以i]结尾的子数组，记住所有对m取余和其count 则只关心前一个到后一个的转移。O(n*m) tle
- 前缀和的角度，所有 sum[l,r] % m
    (ss(r+1) - ss(l)) % m
    ss(r+1) % m - ss(l) % m -- 我们先忽视可能的负数
    固定r 对所有l求和 l=0...r
    (r+1) *ss(r+1)%m - sum(ss(l)%m for l in range(r+1)) -- 以r]结尾的所有数组和

    如果上方是负数
    ss(r+1) % m - ss(l) % m + m 才是目标，需要补一个m
    也就是 ss(l)%m > ss(r+1)%m for l in range(0, r+1) 逆序对的数量

# cf上提交pypy的代码，要是设置的最大递归深度超1e6，就内存超限了，其他oj不会
"""
import sys
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

def merge_count(a):
    n = len(a)
    if n <= 1:
        return 0
    mid = n // 2
    left = a[:mid]
    right = a[mid:]
    cnt = merge_count(left) + merge_count(right)
    i = j = 0
    temp = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            temp.append(left[i])
            i += 1
        else:
            cnt += len(left) - i
            temp.append(right[j])
            j += 1
    temp.extend(left[i:])
    temp.extend(right[j:])
    a[:] = temp
    return cnt


class BIT:  # 维护区间sum(nums[l,r])
    def __init__(self, n: int, nums: List = None):  # 初始数组为0时启用
        self.a = [0] * (n + 1)
        if nums is not None:
            # 预处理nums 计算初始树状数组前缀和
            self.nums = nums
            for i, x in enumerate(nums, 1):  # 所有nums[i] => a[i+1]
                self.a[i] += 1
                pa = i + (i & -i)  # i 父节点，其管辖着i所在的区间
                if pa <= n:
                    self.a[pa] += self.a[i]  # 启发式更新

    # 单点更新 nums[idx]+=x
    def update(self, idx, x):  # nums[idx] => a[i/idx+1]
        i = idx + 1
        a, n = self.a, len(self.a)
        while i < n:
            a[i] += x
            i += i & -i

    def prefix_sum(self, i: int):  # 计算前缀和 sum(nums[:i]) 这里无需串位，原数组i取不到
        res = 0
        while i > 0:
            res += self.a[i]
            i -= i & -i
        return res

    def query_sum(self, l: int, r: int) -> int:  # 区间sum(nums[l,r])
        return self.prefix_sum(r + 1) - self.prefix_sum(l)

n, m = RII()
a = RILIST()
def solve_using_merge_sort_cnt(n, m, a):
    # 计算前缀和并取mod m
    s = [0]*(n+1)
    for i, x in enumerate(a):
        s[i+1] = s[i] + x
        s[i] %= m
    s[-1] = s[-1] % m

    # (r+1) *ss(r+1)%m - sum(ss(l)%m for l in range(r+1))
    p = 0
    res = 0
    for r in range(n):
        res += (r+1) * s[r+1] - p
        p += s[r+1]
    res += merge_count(s) * m
    print(res)

def solve_using_BIT(n, m, a):

    # f = [0] * (n + 1)  # 统计逆序对 f[i] -- 左侧f[j] j in [0,i) s[j]%m > s[i]%m
    f = 0
    s = [0] * (n + 1)
    tree = BIT(m)
    for i, x in enumerate(a):
        s[i + 1] = s[i] + x
        s[i] %= m

        # 求左侧大于 s[i+1]%m 的逆序对
        # f[i + 1] = i - tree.prefix_sum(s[i + 1] % m + 1)
        f += i - tree.prefix_sum(s[i + 1] % m + 1)
        tree.update(s[i + 1] % m, 1)

    s[-1] %= m

    # print(a)
    # print(list(itertools.accumulate(a, initial=0)))
    # print(s)
    # print(f)

    # (r+1) *ss(r+1)%m - sum(ss(l)%m for l in range(r+1))
    p = 0
    res = 0
    for r in range(n):
        res += (r + 1) * s[r + 1] - p #+ m * f[r+1]
        p += s[r + 1]
    res += m * f
    print(res)
solve_using_BIT(n, m, a)




# res = 0
# f = defaultdict(int)
# g = defaultdict(int)
# for x in a:
#     for k, v in f.items():
#         g[(k + x) % m] += v
#     g[x % m] += 1
#
#     res += sum(k*v for k,v in g.items())
#     f, g = g, f
#     g.clear()
# print(res)
