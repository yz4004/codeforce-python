from typing import List


# 凑出target的所有可能组合总数
# 本质是爬楼梯，比起之前的迈一步或者两步 这里是一个list可选择 所以只需要一个状态定义
# https://leetcode.cn/problems/combination-sum-iv/
class Solution:
    def combinationSum4(self, nums: List[int], target: int) -> int:
        n = len(nums)

        # f[i] 凑出 i 的方案总数
        f = [0]*(target+1)
        f[0] = 1
        for i in range(target):
            f[i] = sum(f[i-x] for x in nums if i-x >= 0)
        # return f[target]


        # 300ms -> 40ms
        def dfs(i):
            # 到达i的方案总数
            if i == 0:
                return 1
            elif i < 0:
                return 0
            return sum(dfs(i - nums[j]) for j in range(n))


        # 下面那个没过，发现不用去重，修改得来，但这里 [0,i] 已经失去意义了，因为每个j都是全体nums里选，及时带着k递归，下次还是从全体nums选，属于无效状态
        def dfs(i, j):
            # [0,i] 在背包容量为 j 的情况下，能凑的总数
            if j==0:
                return 1
            if j<0:
                return 0
            return sum(dfs(k, j-nums[k]) for k in range(0, n)) #如果是 range(0,i+1) 则是按顺序 纯完全背包
        # return dfs(n-1, target)



        def dfs(i, j): # 利用前 [:i]个 凑出j
            if j < 0:
                return 0
            if j == 0:
                return 1
            res = 0
            for k in range(i): #这个写法考虑 无重复，即无视选择的顺序 1 2 1 和 1 1 2 认为是同一种 但本体不要求 不是完全背包问题
                for cnt in range(0, j//nums[k], nums[k]): # 决定当前[k]选多少个
                    res += dfs(k, j - cnt * nums[k])
            return res
        # return dfs(n, target)


