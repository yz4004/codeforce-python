"""
找最长非递减子序列
x - [:i] 小于x的最大子序列

123 9 10 4 11?
"""
from bisect import bisect_left
from typing import List



class Solution:

    """
    树状数组维护最长非减子序列
    """
    def findLengthOfShortestSubarray(self, arr: List[int]) -> int:
        idx = sorted(set(arr))
        t = BIT(len(idx))
        res = 0
        for i, x in enumerate(arr):
            j = bisect_left(idx, x) + 1 # x的坐标 + 1 for BIT 因为x一定出现在bit里所以 bisect直接返回x的坐标
            l = t.query(j) # 返回大于等于j/x 的最长非减序列
            res = max(res, l + 1)
            t.update(j, l + 1) #在j上更新
        return res

class BIT:
    def __init__(self, n):
        self.a = [0] * (n + 1)
    def update(self, i, x):
        a, n = self.a, len(self.a)
        while i < n:
            a[i] = max(a[i], x)
            i += i & -i
    def query(self, i):
        res = 0
        while i > 0:
            res = max(res, self.a[i])
            i -= i & -i
        return res

arr = [1,2,2,3,5,2,3,4,4,4,4,5]
s1 = Solution()
print(len(arr), s1.findLengthOfShortestSubarray(arr))