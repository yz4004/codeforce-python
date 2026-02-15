"""
枚举子集
"""
from typing import List

"""
1. LC78 无重集合 枚举子集 https://leetcode.cn/problems/subsets/description/
    认为每个数组下标unique 每个元素独一无二 2^n
    选或不选 - 搜索树叶节点写入
    选择选哪个 - 搜索树每个节点写入

2. LC90 有重集合 枚举子集 https://leetcode.cn/problems/subsets-ii/description/
如果不以下标为唯一标志，而是数值，如【122】不区分两个2. 则上面的2^n 过程会出现枚举重复
    考虑带下角标 1 21 22 枚举中会出现重复 【1 21】 【1 22】
    其实是完全背包，种类i可以考虑选 k*nums[i] k=012... 
    
去重的逻辑：人为指定一个序，对于重复角标 我们只接受形如 123…k 唯一增序，且差值必须为1 【同排列，但是k可以提前截断】
    排序后，对所有同类重数只考虑递增下角标，即假如枚举数组中枚举了重数2的第k个下角标，只有在前面2_(k-1) 选过后才可以选择
    按类分组，每次只考虑cnt够不够选，这个角度天然去重，正如完全背包每次对i号物品枚举 k*nums[i] k=01... 这个逻辑是忽略选择内部序的 i0 i1 
"""


def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
    n = len(nums)
    nums.sort()
    res = []
    def dfs(i, s):
        if i == n: # 选或不选 - 叶节点才是一条搜索路径的结束
            res.append([nums[i] for i in range(n) if s >> i & 1 == 1])
            return
        dfs(i + 1, s)  # 不选
        if i == 0 or nums[i - 1] != nums[i] or (s >> (i - 1) & 1 == 1 and nums[i - 1] == nums[i]):  # 选 但有条件 只有增序差值为1的下角标才可以
            # 1.一个种类的开头/数组元素开头 2. 相同元素的前一个下角标 a_(k-1) 已经选了
            dfs(i + 1, s | (1 << i))
    dfs(0, 0)

    def dfs(i, path): #选择选哪个写法，参考
        res.append([nums[k] for k in path])  # 而是选择选哪个写法 在每个搜索树的节点记录 （注意两种写法的搜索树不同）
        for j in range(i, n):
            if j > i and nums[j] == nums[j - 1]:  # 控制下角标 选择选哪个，i是可以无脑选的，绝对保证+1增序 所以只检查j>i
                continue
            dfs(j + 1, path + [j])
    dfs(0, [])
    return res

##################################################################
##################################################################
"""
当枚举子集有额外条件时
上面的回溯框架 + 判断 + 剪枝
例LC40 组合总数 （引入剪枝）
"""
def combinationSum2(candidates: List[int], target: int) -> List[List[int]]:
    nums = candidates
    n = len(nums)
    nums.sort()
    res = []
    def dfs(i, path, s):  # 选或不选枚举子集; 去重逻辑 [21 22 23...] 只接受 12...k 重复下角表的选取顺序
        if s == target:
            res.append([nums[j] for j in path])
            return
        if s > target: return  # 需要引入剪枝
        if i == n: return
        dfs(i + 1, path, s) #path代替了s
        if i == 0 or nums[i - 1] != nums[i] or (path and path[-1] == i - 1):
            # 1.一个种类的开头/包括数组元素开头 2. 相同元素的前一个下角标 a_(k-1) 已经选了，体现在path末位的角标
            dfs(i + 1, path + [i], s + nums[i])
    dfs(0, [], 0)
    return res
""" 
枚举子集 + 条件剪枝
77. 组合 - 力扣（LeetCode） k-size子集
39. 组合总和 - 力扣（LeetCode） 和为target 的子集
2597. 美丽子集的数目 - 力扣（LeetCode） 选或不选枚举子集 + 限制选择条件（不允许选择前有差值为k的元素）
40. 组合总和 II - 力扣（LeetCode）和为target 的【去重】子集
216. 组合总和 III - 力扣（LeetCode）子集和恰好为t 引入多种剪枝
"""

