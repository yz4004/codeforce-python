from collections import Counter
from typing import List
# https://leetcode.cn/problems/most-frequent-ids/
# 区间左边为nums 的 id 维护的值是 频次 max值
# 1 <= nums[i] <= 105 所以index最大范围只有 10^5
# https://leetcode.cn/problems/most-frequent-ids/solutions/2710984/shu-zhuang-shu-zu-ye-ke-yi-zuo-dang-ran-meeht
class Node:
    __slots__ = "l", "r", "val", "lc", "rc"
    def __init__(self, l, r):
        self.l = l
        self.r = r
        self.val = 0
        self.lc = self.rc = None

class Solution:
    def mostFrequentIDs(self, nums: List[int], freq: List[int]) -> List[int]:
        n = len(nums)

        mx = max(nums) # 10 ** 5
        root = Node(1, mx)
        def query(p:Node, l, r, left, right):
            if l <= left and right <= r:
                return p.val
            mid = (l+r)//2
            res = float("-inf")
            if l <= left:
                res = max(res, query(p.lc, l, mid, left, right))
            if right <= r:
                res = max(res, query(p.rc, mid+1, r, left, right))
            return res

        def update(p:Node, l,r, index, val):
            if l == r:
                p.val = val
                return
            mid = (l + r) // 2
            if not p.lc:
                p.lc = Node(l, mid)
            if not p.rc:
                p.rc = Node(mid+1, r)
            if index <= mid:
                update(p.lc, l, mid, index, val)
            if mid < index:
                update(p.rc, mid+1, r, index, val)
            p.val = max(p.lc.val, p.rc.val)

        cnt = Counter()
        ans = [0]*n
        for i in range(n):
            cnt[nums[i]] += freq[i]
            update(root, 1, mx, nums[i], cnt[nums[i]])
            ans[i] = query(root, 1, mx, nums[i], nums[i])
        return ans


if __name__ == '__main__':
    s = Solution()
    print(s.mostFrequentIDs([2,3,2,1], [3,2,-3,1]))
    # [5, 5, 3], freq = [2, -2, 1]
    print(s.mostFrequentIDs([5, 5, 3], [2, -2, 1]))

