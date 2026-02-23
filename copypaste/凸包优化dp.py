from typing import List

mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

"""
给你两个长度相等的整数数组 nums 和 cost，和一个整数 k。

你可以将 nums 分割成多个子数组。第 i 个子数组由元素 nums[l..r] 组成，其代价为：
(nums[0] + nums[1] + ... + nums[r] + k * i) * (cost[l] + cost[l + 1] + ... + cost[r])。
注意，i 表示子数组的顺序：第一个子数组为 1，第二个为 2，依此类推。
返回通过任何有效划分得到的最小总代价。

输入： nums = [3,1,4], cost = [4,6,6], k = 1
输出： 110

思路一，硬拆公式 + 下凸包
    f[i][r] 前r个划分成i组
    f[i][r] = min_l{ f[i-1][j] + (nums[0,r] + k*i) * cost[l,r]}
    
    s[r+1] = sum(nums[0,r])
    c[r+1] = sum(cost[0,r])
    
    f[i][r] = min_l f[i-1][j] + (s[r+1] + k*i) * (c[r+1] - c[l]) 
            = min_l f[i-1][j] - (s[r+1] + k*i) * c[l] + (s[r+1]+k*i)*c[r+1]  尾项不参与 min_l 可以放在外部
            
    min( f[i-1][j] - (s[r+1] + k*i) * c[l] for l in range(0,r))
    
    (xl,yl) = (c[l], f[i-1][j]) 均为单增
    k = (s[r+1] + k*i) > 0
    
    则 min(yl - k * xl) for l in range(0,r) 
    维护  (xl,yl) 的下凸包即可做到均摊 o(1) 找到 min
        
"""
def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
    n = len(nums)
