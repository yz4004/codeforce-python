import random
import sys
from functools import cache
from typing import List
from math import inf

"""
【选择顺序不相关贪心】

给一个列书，对应一个cost数组，代表选每本书的代价 和 一个数p
可以从左侧或者右侧选一本，代价是对应的cost
或者左右同时选择，代价是p
求问最小的总代价
n = 10^5 (要贪心）
"""

# 实例
p = 6
data = [
[2, 4, 3, 2, 5],  # 0 14 23 = 2 + 6 + 5
[2, 2, 3, 2, 5],  # 6 + 6
[2, 4, 3, 4, 5],  # 2 + 6 + 6
[2, 4, 1, 4, 5],  # 2 + 6 + 5 = 13
[1, 2, 2, 2, 6],  # 11
[2, 2, 2, 2, 6],  # 12
[2, 2, 2, 3, 6]   # 12
]

def dp_validator(nums : List[int], p: int) -> int: # O(n^2) 区间dp验证器
    """ solve1([2, 4, 3, 2, 5], p) """
    n = len(nums)
    f = [[0]*n for _ in range(n)] # f[i][j]
    for j in range(0, n):
        f[j][j] = nums[j]
        for i in range(j-1, -1, -1):
            a = b = c = inf
            if i+1 < n:
                a = f[i+1][j] + nums[i]
            if j-1 >= 0:
                b = f[i][j-1] + nums[j]
            if i+1 < n and j-1 >= 0:
                c = f[i+1][j-1] + p
            # f[i][j] = min(f[i+1][j] + nums[i], f[i][j-1] + nums[j], f[i+1][j-1] + p)
            f[i][j] = min(a, b, c)

    return f[0][n-1]

    # @cache
    # def dfs(i,j):
    #     if i > j:
    #         return 0
    #     return min(dfs(i+1, j)+nums[i], dfs(i,j-1)+nums[j], dfs(i+1,j-1) + p)
    # res = dfs(0, len(nums)-1)
    # dfs.cache_clear()
    # return res


"""
如果一个数小于p/2 那他就应该直选，任何组队行为都是亏摸的
如果一个数大于=p/2 那应该组队，但是我还要知道有没有另一个配对 
    假如没有 则要从小于p/2的里选尽量大的，会亏最少，也可以这个多余的数直接选

数组就是这样的 y y x y x y... x y 
若干分布的y<p/2 和一些分布的x
所以左右选什么的 就是所有x 22组队，如果当前一遍有y就先只选即可。然后xx两两剥离

所以统计x的对数，y的和
如果x是偶数就 x正好cnt//2对，+ y的和
如果x是奇数，可以决定是选x里的最小 或是y的最大加入配对，所以额外维护min(x) max(y)

其实配对顺序是不必要的，因为配对两个x无论是谁都被截断成p了 大出多少不必要。那个最大y 最小x的位置也不必要，转化成y/x 一并处理就行了
"""
def greedy_solver(nums, p):
    # cnt = sum(2*x >= p for x in nums) # x >= p/2
    mi = inf
    mx = -inf
    s = 0
    cnt = 0
    for x in nums:
        if 2*x >= p:
            cnt += 1
            mi = min(mi, x)
        else:
            mx = max(mx, x)
            s += x

    if cnt % 2 == 0:
        res = cnt//2*p + s
    else:
        res1 = (cnt-1)//2 * p + mi + s
        res2 = (cnt+1)//2 * p - mx + s
        res = min(res1, res2)
    return res

# sys.setrecursionlimit(10000) 默认递归栈1000
for _ in range(100):
    nums = [random.randint(0, 10000) for _ in range(500)] #随机生成长度500的1-10000内数 p取随机【min, max】区间内的数
    p = random.randint(min(nums), max(nums))
    assert (dp_validator(nums, p) == greedy_solver(nums, p))

# data = [[2, 4, 3, 2, 5], [2, 2, 3, 2, 5], [2, 4, 3, 4, 5], [1, 2, 2, 2, 6], [2, 2, 2, 2, 6], [2, 2, 2, 3, 6]]
# p = 6
# for nums in data:
#     assert(solve1(nums, p) == solve2(nums, p))
