from bisect import bisect_left
from typing import List


def mono_stack(nums):
    n = len(nums)
    s = []
    left_large = [-1]*n
    right_large = [n]*n
    for i,x in enumerate(nums):
        while s and nums[s[-1]] < x:
            d = s.pop()
            right_large[d] = i
        if s:
            left_large[i] = s[-1]
        s.append(i)
    print(left_large)
    print(right_large)
"""
模版题
- 只关心一个维度的大小比较 维护的是一个严格单调（增或减）的下标栈，时间复杂度恰好 O(n)
739. 每日温度
503. 下一个更大元素 II

准确的说栈内维护的是 [(i,nums[i]) ...] 下标因为遍历方向单调 + 维护值域 nums[i] 单调

单调栈二分
- 维护一个  二维的 Pareto 前沿（又叫 skyline）
- 不能总是决定支配关系，但是一般有栈内值域有序的特性 [(x,y)...] y值域单调
456. 132 模式 
2736. 最大和查询 （离线版本）
"""


def maximumSumQueries(nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
    # 2736 最大和查询
    # 给一系列queries (x,y) 求 max(nums1[j] + nums2[j] | nums1[j]>=x, nums2[j]>=y for any j)
    n = len(nums1)


    # 离线版本
    # 一般优先思考离线版本，处理queries能简化思考
    # 考虑j 使得 nums1[j], nums2[j] 对应大于 x y 同时满足，再考虑所有同时满足的最大值
    # 定一议二，先得到所有满足条件1的下标集，在考虑第二个条件
    # 绑定后按nums1倒序排序，即考虑前缀
    a = sorted([(x, y) for x, y in zip(nums1, nums2)], reverse=True)
    res = [-1] * len(queries)
    # queries 按照倒序
    queries = sorted([(q0, q1, i) for i, (q0, q1) in enumerate(queries)], key=lambda x: -x[0])
    s = []  # 栈内存 (n2, n1+n2)
    i = 0
    for x, y, idx in queries:
        while i < n and a[i][0] >= x:
            # n1+n2
            n1, n2 = a[i]
            # 如果 n2 小于栈顶 s[-1][0] 则不入 （因为n1也小, n1+n2小于）
            # 如果 n2 大于栈顶 s[-1][0]
            #         n1+n2也大于，则清掉栈顶
            #         n1+n2 小于， 不好说
            # 沿着 (n2, n1+n2) 的 n2 单调递增, n1+n2单调递减
            # 第一个维度n2的单调对应了遍历方向（类似传统单调栈的下标）
            # 第二个维度的n1+n2 也有值域的单调性，所以歧义情况没问题
            if not s or s[-1][0] < n2:
                while s and s[-1][1] <= n1 + n2:
                    s.pop()
                s.append((n2, n1 + n2))
            i += 1

        # 根据y 因为栈内(n2,n1+n2)第一个维度单增，第二个维度单减，其实就是一个值域下降序列，找第一个满足y的即可
        j = bisect_left(s, y, key=lambda x: x[0])
        if j < len(s):
            res[idx] = s[j][1]
    return res

