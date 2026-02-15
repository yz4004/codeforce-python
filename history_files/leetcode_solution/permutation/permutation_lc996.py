import math
from collections import Counter
from functools import cache
from typing import List

"""
https://leetcode.cn/problems/number-of-squareful-arrays/
写法1 全排列2改
全排列2的基础上 考虑相邻排列 是否能组成平方数
全排列2 对多个重复元素不计入其内部的顺序如 122 总共有 3！/2！个排列结果，本题在其基础上考虑相邻排列
代码上
    全排列2需要生成所有排列的instance所以维持一个待填入的数组 （如果是计数直接组合方法即可）
    然后每次递归填入排列位置i 其前一个位置自然即是 [i-1] 递归入参只需位置i的index
    
    本题不需要知道instance和更早的元素，只需知道选取情况和上一个元素即可 s入参选取情况，pre前一个选择元素
    
    本题不存在重复状态，不用cache记忆化，全排列的每一个搜索路径只会遍历一次
    
有重元素的排列去重，如122 只需考虑重复元素的内部序 1 2_1 2_2 给他们一个隐形下角标，我们最后只取递增角标的instance
122
1 21 22  【1 22 21 不要】
21 1 22
21 22 1
3！/2! 共3种全排列

代码上排序后，如果每次尝试填入的 x，他的下角标应该是没选取x的重复部分的最小的 查看数组 x 前一个元素是否也是 x 以及是否已经选过了，如果是且没选过，则不是最小下标x 不符合
"""
def numSquarefulPerms(self, nums: List[int]) -> int:
    def is_square(x):
        return int(math.sqrt(x)) ** 2 == x

    # 向后搜索排列 -- s已选的不能再挑
    n = len(nums)
    nums.sort()
    def dfs(s, last):
        if s == (1 << n) - 1:
            return 1
        res = 0
        for j in range(n):
            if s >> j & 1 == 1 or (j and nums[j] == nums[j - 1] and s >> (j - 1) & 1 == 0): # 跳过的条件，1. 已选过 2. 没选过但不是最小下角标
                continue
            if s == 0 or is_square(last + nums[j]): #在全排列基础上额外判断相邻是否构成平方
                res += dfs(s | (1 << j), nums[j])
        return res
    return dfs(0, 0)

"""
写法2
普通全排列写法不去重 + 最后利用组合方法去重
因为有重复元素，他们的先后选择，会在搜索树上造成重复子树 21 -> 22 -> s, 和 22 -> 21 -> s 最后都是询问s 但是该状态会被询问两次 所以需要cache记忆化 

[1,17,8] 对于无重实例，不会有重复入参，
[2,2,2 ...] 对于有重实例，会出现重复入参，一个状态被反复访问
"""
def numSquarefulPerms(self, nums: List[int]) -> int:
        n = len(nums)
        def is_perfect_square(el):
            if el < 0:
                return False
            return math.sqrt(el) % 1 == 0

        # cnt = Counter()
        @cache  # 必须缓存装饰器，避免重复计算 dfs 的结果
        def dfs(s: int, pre: int) -> int:  # 考虑前i个排列 当前选择状态为j 递归前第i+1个排列是pre （要求本轮选择与pre组成平方）求排列总数
            if s == 0:
                return 1
            # cnt[(s,pre)] += 1
            res = 0
            for x in range(s.bit_length()):      #因为是从s的已选状态中排出，倒着退，所以至多枚举到 s/bit_length()
                if s >> x & 1 == 1:              #枚举过程中没有任何额外检查，对于多个重复元素，实际上先访问21 还是先访问 22 不固定，两个多会被计入（造成s不同）
                    cur = nums[x] + pre          #代码上，实际上就重复计数了，实际上当全排列做了，最后会利用组合去重
                    if is_perfect_square(cur):   #为什么状态会被重复访问？对于多个222： (0b110, 2) - (0b010,2) vs (0b011,2) (0b010,2) 相同的两个2 他们先21后22 和 先22后21 然后访问的都是状态 (s,2) 搜索树纵向选择差异
                        res += dfs(s ^ (1 << x), nums[x])
            return res

        s = (1 << len(nums)) - 1
        rep = 1
        for k, v in Counter(nums).items(): #利用排列组合技巧 n!/k! 清除重复组合
            rep *= math.factorial(v)
        res = sum(dfs(s ^ (1 << i), x) for i, x in enumerate(nums)) // rep
        return res