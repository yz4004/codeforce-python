from typing import List
"""
https://leetcode.cn/problems/longest-turbulent-subarray/description/
"""
class Solution:
    def maxTurbulenceSize(self, nums: List[int]) -> int:
        # turbulent 震荡数组
        n = len(nums)
        i = 0
        res = 1

        while i < n - 1:
            if nums[i+1] == nums[i]:
                i += 1
                continue
            if nums[i+1] > nums[i]:
                last = 1
            else:
                last = -1
            j = i + 1
            while j + 1 < n and (nums[j+1] - nums[j]) * last < 0:
                j += 1
                last *= -1
            # [i,j]
            res = max(res, j-i+1)
            i = j
        return res


if __name__ == "__main__":
    s = Solution()
    print(s.maxTurbulenceSize([9,4,2,10,7,8,8,1,9]))