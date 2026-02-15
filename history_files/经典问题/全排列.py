"""
枚举全排列
1. 数组下标视角 无重全排列
2. 数值视角 有重全排列
3. 有重全排列 + 计数
"""
import math
from typing import List
##################################################################
##################################################################
"""
LC46 全排列1
1. 全排列中的重复枚举问题
如果以数组下标为唯一表示，数组元素每个独一无二，则无重 n!
"""
def permute(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    # 选择选哪个
    res = []
    visited = [False] * n

    def dfs(path):
        if len(path) == n:
            res.append(path.copy())
            return

        for i in range(n):  # 没有任何判重逻辑，认为数组元素每个都独一无二
            if visited[i] == False:
                visited[i] = True
                path.append(nums[i])
                dfs(path)
                path.pop()
                visited[i] = False

    dfs([])
    return res

##################################################################
##################################################################
"""
LC47 全排列2
如果不以下标为唯一标志，而是数值，如【122】不区分两个2. 则上面的n!过程会出现枚举重复
    考虑带下标的 1 21 22 (给重复元素带一个下角标）则n!枚举会出现 【1 21 22】【1 22 21】【22 1 21】 【21 1 22】 … 
    重复元素2的重数为k 仅2就会有k! 个重复的instance （从角标 21 22 … 2k 考虑k!的全排列)
	
去重的逻辑：人为指定一个序，对于重复角标 我们只接受 123…k 唯一增序
    排序后，对所有同类重数只考虑递增下角标，即假如枚举数组中枚举了重数2的第k个下角标，只有在前面2_(k-1) 选过后才可以选择
    按类分组，每次只考虑cnt够不够选，这个角度天然去重，正如完全背包每次对i号物品枚举 k*nums[i] k=01... 这个逻辑是忽略选择内部序的 i0 i1 
"""
def permuteUnique(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    # 排序角度
    nums.sort()
    res = []
    path = [0] * n
    visited = [False] * n

    def dfs(i):  # 排列path 下一个要填入的index - i
        if i == n:
            res.append(path.copy())
            return

        for j, x in enumerate(nums):
            if not visited[j]:
                if j > 0 and nums[j] == nums[j - 1] and not visited[j - 1]:  # 如果不是最左侧未被选择的情况 跳过(相比46多的部分)
                    continue
                path[i] = x
                visited[j] = True
                dfs(i + 1)
                visited[j] = False
    dfs(0)
    return res

    ## 从cnt的角度
    cnt = Counter(nums)
    nums = list(cnt.keys())
    res = []
    path = [0] * n
    def dfs(i, p_cnt):  # p_cnt 记录路径上的选择情况
        if i == n:
            res.append(path.copy())
            return
        for x in nums:
            if p_cnt[x] < cnt[x]:  # 只有x还有足够重数供选择时，才加入path 这个计数天然去重
                path[i] = x

                p_cnt[x] += 1
                dfs(i + 1, p_cnt)
                p_cnt[x] -= 1

    dfs(0, defaultdict(int))
    return res
##################################################################
##################################################################
"""
LC996 平方数组的数目 全排列+计数
    在全排列2的基础上引入相邻选取条件，最后计数。
    全排列在叶节点才确定是合法排列 发生一次计数 + 不存在重复状态访问，可不引入cache
    ps 如无相邻条件则就是组合问题计数 n!/k1!...kp! （k为重复元素的重数）
"""
def numSquarefulPerms(nums: List[int]) -> int:
    def is_square(x):
        return int(math.sqrt(x)) ** 2 == x

    n = len(nums)
    nums.sort() # 向后搜索排列 -- s已选的不能再挑
    def dfs(s, last): #全排列不存在状态的重复访问，所以可以不加装饰器
        if s == (1 << n) - 1:
            return 1
        res = 0
        for j in range(n):
            if s >> j & 1 == 1 or (j and nums[j] == nums[j - 1] and s >> (j - 1) & 1 == 0):
                # 跳过的条件，1. 已选过 2. 没选过但不是最小下角标
                continue
            if s == 0 or is_square(last + nums[j]):  # 在全排列基础上额外判断相邻是否构成平方
                res += dfs(s | (1 << j), nums[j])
        return res
    return dfs(0, 0)
##################################################################
##################################################################
