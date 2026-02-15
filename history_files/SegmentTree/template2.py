from typing import List
class NumArray:
    """
    格式
    segmentTree 参数
    1. node index - p, node range - [l, r]
    2. query range [left, right]
    """
    def __init__(self, nums: List[int]):
        n = len(nums)
        self.nums = nums
        # self.t = [0]*(4 * n) # 4*n/n<<2 而不是 2 << n
        self.t = [0]*(2 << n.bit_length()+1)
        self.build(1, 0, n-1)

    def build(self, p, l, r):
        if l > r: return
        if l == r:
            self.t[p] = self.nums[l]
            return
        mid = (l+r)//2
        self.build(2*p, l, mid)
        self.build(2*p+1, mid+1, r)
        self.t[p] = self.t[2*p] + self.t[2*p+1]


    """ index 上加 val """
    def add(self, p, l, r, index, val):
        if l == r:
            self.t[p] += val
            return
        mid = (l+r)//2
        self.t[p] += val
        if index <= mid:
            self.add(2*p, l, mid, index, val)
        else:
            self.add(2*p+1, mid+1, r, index, val)

    """ 查询 [left, right] 的和 """
    def query(self, p, l, r, left, right):
        if l > right or r < left: return 0
        if left <= l and r <= right:
            return self.t[p]
        mid = (l+r)//2
        return self.query(2*p, l, mid, left, right) + self.query(2*p+1, mid+1, r, left, right)
    """ 不能用mid 分割left right 如果他们在某一半区间，这会造成定义混乱"""



    """ 模板到此为止 下面是 lc307 测试api"""
    def update(self, index: int, val: int) -> None:
        n = len(self.nums)
        self.add(1, 0, n-1, index, val - self.nums[index])
        self.nums[index] = val

    def sumRange(self, left: int, right: int) -> int:
        n = len(self.nums)
        return self.query(1, 0, n-1, left, right)

"""
307
https://leetcode.cn/problems/range-sum-query-mutable/description/
"""