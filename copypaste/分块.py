from bisect import bisect_left
from math import isqrt, inf
from typing import List


def block_template(nums: List[int], queries: List[List[int]]) -> List[int]:
    n = len(nums)

    # 1. 这里可做些预处理 - 如离散化 - 位置数组
    # vals = sorted(set(nums))
    # mp = {v: i for i, v in enumerate(vals, 1)}
    # # [L,R]
    # a = [mp[v] for v in nums]
    # n = len(a)


    # 分块
    b = isqrt(n)  # 300  block size
    m = (n-1)//b+1 # number of block 最后一个是余数

    def get_block_index(i): # 0-index. i-所在的block index
        return i // b

    def get_block_range(idx): # -> [l,r] close interval 返回block idx 对应的 block 范围
        l = idx * b
        r = (l+b if l+b < n else n) - 1
        return l, r

    def rebulid(idx):
        # todo 如更新了block[idx] 重建
        pass

    # 两种风格的block
    blocks = [None]*m # block[idx]
    f = [[None]*m for _ in range(m)] # f[i][j] block [i...j] 对应的整体信息 如mode
    for idx in range(m):
        for i in range(idx*b, min(idx+1)*b, n):
            # todo 初始化 block[idx]
            pass
        for i in range(idx*b, n): # 处理 f[idx][...]
            # todo 初始化 f[i..j] 从i到j的 block
            pass

    res = []
    for l, r, *args in queries:
        # get_block_index
        li = l//b
        ri = r//b #
        # [li+1, ri-1]
        if li+1 <= ri-1:
            # todo 可以询问 f[li+1][ri-1]

            # todo 或者遍历 blocks[li+1...ri-1]
            for idx in range(li+1, ri):
                pass


        # left window
        for i in range(l, min(li*b+b, n)):
            x = nums[i]
            # todo

        # right window
        for i in range(ri*b, r+1):
            x = nums[i]
            # todo

        # todo 更新res
        # res.append(...)

        return res

"""
模版应用
区间最小众数 回滚莫队/分块
    https://leetcode.cn/problems/threshold-majority-queries/description/


"""


