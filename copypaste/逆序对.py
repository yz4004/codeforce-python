from math import isqrt
from typing import List


class BIT:  # 1-based - 值域树状数组

    def __init__(self, n): # [1,n]
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, i, delta): # a[i] += 1
        n = self.n
        tree = self.tree
        while i <= n:
            tree[i] += delta
            i += i & -i

    def prefix_sum(self, i): # [1,i]
        res = 0
        tree = self.tree
        while i > 0:
            res += tree[i]
            i -= i & -i
        return res

    def kth(self, k): # 1-based 1...k
        idx = 0
        bit = 1 << (self.n.bit_length() - 1)
        tree = self.tree
        while bit:
            nxt = idx + bit
            if nxt <= self.n and tree[nxt] < k:
                k -= tree[nxt]
                idx = nxt
            bit >>= 1
        return idx + 1

# 模版
# mo queue 查询闭区间内逆序对 nums - [1,1e9]
# https://chatgpt.com/c/693dfd3d-10b0-8329-96af-05d45f09bc0c
def mo_queue_template(nums: List[int], queries: List[List[int]]) -> List[int]:
    n = len(nums)

    # 1. 预处理 - 离散化
    vals = sorted(set(nums))
    mp = {v: i for i, v in enumerate(vals, 1)}
    nums = [mp[x] for x in nums]
    m = len(vals)
    tree = BIT(m)  # 1-based & closed [1,m]

    # 2. 分块尺寸
    b = isqrt(n)  # 300

    # 3. 标准格式 对queries区间 按左端点所属的分块编号 做排序
    # 奇偶排序优化. 偶数块编号 按r升序. 奇数块编号 按r降序. 这样第一个块右端点递增后，可以在第二个块倒着处理. 而不是折返再从头扫
    def sort_key(x):
        idx, l, r = x
        return l // b, r if (l // b) % 2 == 0 else -r
    queries = [(idx, l, r) for idx, (l, r) in enumerate(queries)]
    queries.sort(key=sort_key)

    # 4. 当前处理区间 [cl,cr]
    cl, cr = 0, -1
    cnt = 0 # 需要的维护的global值，取sum/cnt为例子

    # BIT维护窗口内逆序对
    # [i, j-1] j 添加j到窗口内 更新逆序对
    def add_right(j):
        nonlocal cnt
        x = nums[j]

        t = tree.prefix_sum(m) - tree.prefix_sum(x)  # 减去小于等于x的计数 得到 左侧严格大于x的计数
        cnt += t
        tree.add(x, 1)

    # i [i+1, j] 添加i到窗口内 更新逆序对
    def add_left(i):
        nonlocal cnt
        x = nums[i]

        t = tree.prefix_sum(x - 1)  # 窗口内严格小于x的数量 右侧
        cnt += t
        tree.add(x, 1)

    # [i, j] 窗口移除i
    def remove_left(i):
        nonlocal cnt
        x = nums[i]

        t = tree.prefix_sum(x - 1)  # 窗口内严格小于x的数量 右侧
        cnt -= t
        tree.add(x, -1)

    # [i, j] 窗口移除j
    def remove_right(j):
        nonlocal cnt
        x = nums[j]

        t = tree.prefix_sum(m) - tree.prefix_sum(x) # 减去小于等于x的计数 得到 左侧严格大于x的计数
        cnt -= t
        tree.add(x, -1)

    res = [0] * len(queries)
    for idx, l, r in queries:

        while cl > l:
            cl -= 1
            add_left(cl)
        while cr < r:
            cr += 1
            add_right(cr)
        while cl < l:
            remove_left(cl)
            cl += 1
        while cr > r:
            remove_right(cr)
            cr -= 1

        # todo
        # 现在[cl,cr] 在 sqrt(n) 的时间得到维护. 利用被维护的对象输出查询
        # ...
        res[idx] = cnt

    return res

"""
固定窗口长度k内的最大逆序对数量 
https://leetcode.cn/problems/minimum-inversion-count-in-subarrays-of-fixed-length/description/

删除子数组计算剩余逆序对 滑窗 + 维护两个BIT 
https://codeforces.com/problemset/problem/220/E - 20251211

"""