"""
子集划分问题 - 正好划分 k-size子集

LC473 火柴拼正方形 问能否划分成4个k-size子集 https://leetcode.cn/problems/nums-to-square/description/
    展示5段代码
        1. 球桶回溯 4^n + 剪枝 
        1. 生成当前子集 （有cache）通过 v1
        2. 生成当前子集 （无cache）超时 v2
        3. 预处理+枚举子集 超时        v3
        4. 回溯+剪枝 通过             v4
        5. 写法1的dp形式 通过         v5
"""

"""
Q: 为什么会有重复? 
A: 子集划分不仅要考虑选取的一个子集内部的序，也要考虑k个子集选取之间的序
    1. 一个子集内部的 (a,b...) 无序
    2. 一组划分内部，{s1, s2 ...} 无序 -- 划分是集合间的加和方案，划分彼此之间也是无序的

    关于1 由选择选哪个写法的向后选取保证。 [mark1]
    关于2 类似于1 我们也给划分指定一个序，
"""
from collections import Counter
from functools import cache
from typing import List

####################################################################
#################################################################### 

def makesquare_v1( nums: List[int]) -> bool:
    n = len(nums)
    stickSum = sum(nums)
    if stickSum % 4: return False
    target = stickSum // 4

    # 暴力球桶回溯（球入哪个桶视角） 4^n （超时）
    buckets = [0]*4
    def dfs(i):
        if i == n:
            return True

        for k in range(4):
            if buckets[k] + nums[i] <= target:
                buckets[k] += nums[i]
                if dfs(i+1):
                    return True
                buckets[k] -= nums[i]
        return False
    #return dfs(0)


    # 上述代码引入倒叙排序后 buckets[k] + nums[i] <= target 生效，复杂度降到 4^n/n^(3/2)
    # 证明 https://leetcode.cn/problems/nums-to-square/solutions/1531945/guan-fang-ti-jie-de-fu-za-du-fen-xi-by-h-dtk1

    # 暴力球桶回溯（球入哪个桶视角）+ 排序剪枝
    nums.sort(reverse=True)  # 增序排序则不会通过
    buckets = [0] * 4
    def dfs(i):
        if i == n:
            return True
    
        for k in range(4):
            if buckets[k] + nums[i] <= target:
                buckets[k] += nums[i]
                if dfs(i + 1):
                    return True
                buckets[k] -= nums[i]
        return False
    return dfs(0)

####################################################################
####################################################################
def makesquare_v2(nums: List[int]) -> bool:
    n = len(nums)
    stickSum = sum(nums)
    if stickSum % 4: return False
    target = stickSum // 4

    # 预处理每个子集的和，快速判断是否是合法的一个划分 2^n
    g = [0] * (1 << n)
    for s in range(1, 1 << n):
        lb = s & -s
        g[s] = g[s - lb] + nums[lb.bit_length() - 1]

    # 枚举子集，尝试对每个子集进行子集划分 3^n  这个复杂度是纯3^n 因为每个状态都得到枚举更新，不存在剪枝（虽然复杂度小于上面的排序剪枝，但通不过）
    f = [False] * (1 << n)
    f[0] = True
    for s in range(1, 1 << n):
        sub = s
        while sub:
            if g[sub] == target:
                f[s] = f[s] or f[s ^ sub]
            sub = s & (sub - 1)
    res = f[-1]
    #return res

    # dfs因为有true 剪枝，规避了很多无效状态 能通过 （500ms)
    @cache
    def dfs(s):
        if s == 0:
            return True
        sub = s
        while sub:
            if g[sub] == target and dfs(s ^ sub):
                return True
            sub = s & (sub - 1)
        return False


    return dfs((1 << n) - 1)

####################################################################
####################################################################
def makesquare_v3(nums: List[int]) -> bool:
    n = len(nums)
    stickSum = sum(nums)
    if stickSum % 4: return False
    target = stickSum // 4

    # 视角 生成当前子集 （下面枚举子集的翻版，但是没有预处理子集和，而是遍历的过程中动态的生成） （不加cache超时 因为false路径有重复状态）
    # s未选集合 k已经构成边长的边，v当前正在构成的边的长度 （小于等于target边长）
    @cache  # 无cache不通过 （子集内部有序问题没有解决）有cache解决 1318ms
    def dfs(s, k, v):
        if k == 4:
            return s == (1 << n) - 1
        res = False
        for i in range(n):
            if s >> i & 1 == 0 and nums[i] <= target - v:
                t = nums[i] + v
                if t == target:
                    k += 1
                    t = 0
                res = res or dfs(s | (1 << i), k, t)
        return res
    #return dfs(0, 0, 0)

    # cache 1615ms 对上面 解决了相邻元素重复搜索树问题 但并没有更快，估计是continue那行判断太多
    # 解决了并列划分之间出现的先选22再选21现象，但对同一个搜索树内的重复项，上面的代码已经可以解决
    nums.sort()

    @cache
    def dfs(s, k, v):
        if k == 4:
            return s == (1 << n) - 1
        res = False
        for j in range(0, n):
            if s >> j & 1 == 1 or (j and s >> (j - 1) & 1 == 0 and nums[j - 1] == nums[j]): continue
            # 同组 [21 22 23...] 只接受12..k增序 如果当前选择2k 前一个元素2k-1没选，则跳过
            t = nums[j] + v
            if t == target:
                k += 1
                t = 0
            res = res or dfs(s | (1 << j), k, t)
        return res
    #return dfs(0, 0, 0)

    mycache = Counter()
    visited = set()
    # @cache
    def dfs_test(s, k, v, path, path2):
        # if s == 0b111: #- cache截断了子集内乱序的情况。
        #     print(bin(s), k, v, path, path2, (s,k,v) in visited)
        if (s,k,v) in visited:
            return False
        mycache[(path, k, v)] += 1
        if k == 4:
            return s == (1 << n) - 1
        res = False
        for i in range(n):
            if s == 0b11:
                print(path2, i, s >> i & 1 == 0 and nums[i] <= target - v)
            if s >> i & 1 == 0 and nums[i] <= target - v:
                t = nums[i] + v
                if t == target:
                    k += 1
                    t = 0
                res = res or dfs_test(s | (1 << i), k, t, path+str(nums[i]), path2 + [(nums[i], i)])
        visited.add((s, k, v))
        print("-"*len(path), (path, k, v), res, "---------", path2)
        return res
    #res = dfs_test(0, 0, 0, "", [])
    # print(mycache, res)
    # return res

    nums.sort()
    mycache = Counter()
    visited = set()
    # @cache
    def dfs_test_2(s, k, v, path, path2):
        # if s == 0b111: #- cache截断了子集内乱序的情况。
        #     print(bin(s), k, v, path, path2, (s,k,v) in visited)
        if (s,k,v) in visited:
            return False
        mycache[(path, k, v)] += 1
        if k == 4:
            return s == (1 << n) - 1
        res = False
        for j in range(0, n):
            if s >> j & 1 == 1 or (j and s >> (j - 1) & 1 == 0 and nums[j - 1] == nums[j]): continue
            # 同组 [21 22 23...] 只接受12..k增序 如果当前选择2k 前一个元素2k-1没选，则跳过
            t = nums[j] + v
            if t == target:
                k += 1
                t = 0
            res = res or dfs_test_2(s | (1 << j), k, t, path+str(nums[j]), path2 + [(nums[j], j)])
        visited.add((s, k, v))
        print("-"*len(path), (path, k, v), res, "---------", path2)
        return res

    #res = dfs_test(0, 0, 0, "", []) #'33' 二次使用  [(3, 1), (3, 2)] [(3, 2), (3, 1)]
    res = dfs_test_2(0, 0, 0, "", []) #'33' [(3, 1), (3, 2)]  一次使用
    print(mycache, res)
    return res
"""
其实相邻重复项
1. 重复只会出现在false路径, 一旦有true就会剪枝一直返回结束递归
2. 
"""
makesquare_v3([3,3,2,4]) # 12 = 3333 = 3324 --  target=3 不可能划分4份

"""
注意‘33’打印两次
    解释: 31 32； 32 31 第一个31结束了一个划分 后续false 回溯回退尝试第二个划分32，重置i从0又选第一个31
"""
# makesquare_v3([1,1,1,1,2,2,4]) # target=3 不可能划分4份
"""
可以看到 12 11 分属两个划分，但是不能观察到 11 12 10 在同一个划分，其实这是cache阶段（可以观察到
"""


####################################################################
####################################################################
# 生成当前子集
def makesquare_v4(nums: List[int]) -> bool:
    n = len(nums)
    stickSum = sum(nums)
    if stickSum % 4: return False
    target = stickSum // 4
    @cache  # 无cache 3368 有cache 563ms 解决了选取有序问题  相邻复选问题还是没有解决
    def dfs(s, k, v, i):
        if k == 4:
            return s == (1 << n) - 1
        res = False
        for j in range(i, n):
            if s >> j & 1 == 0 and nums[j] <= target - v:
                t = nums[j] + v
                nxt = j + 1
                if t == target:
                    k += 1
                    t = 0
                    nxt = 0
                res = res or dfs(s | (1 << j), k, t, nxt)
        return res
    #return dfs(0, 0, 0, 0)



    # 最终解决所有重复枚举的代码 62ms (复杂度依赖于数据集 + 对应合适的剪枝)
    # s目前选取的所有子集，k当前正在构建第k个划分，v当前划分的累计和（凑够target再清零进位）i考虑从 [i:]后面枚举下一个填入当前划分的元素
    # 1. 解决一个枚举子集内有序问题
    # 2. 解决枚举的划分与划分之间有序问题
    # 3. 解决相邻重复项重复搜索树问题 -- 任意情况下 前一个相邻重复项 只要被选（无论是在当前生成子集还是此前划分）才能考虑选或不选，没被选就一定不枚举，而是枚举前面的相邻重复项
    nums.sort() #解决相邻复选
    # @cache
    def dfs(s, k, v, i):
        if k == 4:
            return s == (1 << n) - 1
        res = False
        # if i == n or v + nums[i] > target: return False 剪枝位置放在哪都行
        for j in range(i, n):
            if s >> j & 1 == 1 or (j and s >> (j - 1) & 1 == 0 and nums[j - 1] == nums[j]): continue
            # 同组 [21 22 23...] 只接受12..k增序 如果当前选择2k 前一个元素2k-1没选，则跳过
            if v + nums[j] > target: return False #因为排好序了，这里超过了就直接剪枝不枚举了
            t = nums[j] + v
            nxt = j + 1
            if t == target:
                k += 1
                t = 0
                nxt = 0
            res = res or dfs(s | (1 << j), k, t, nxt)
        return res
    return dfs(0, 0, 0, 0)
######################################################################
######################################################################


"""

- 如果计数会发生重复，s1 s2 s3 s4 这四个划分子集不应有序，但是上述代码，从全集开始如果先枚举
    s3 s4 ... 
    s4 s3 ... 这两个不应有序，但是这里枚举被视作两个状态
【子集枚举应该认为引入顺序控制】
1. 背包问题考虑【前】i个
2. 状压/回溯子集划分问题，排序后从头按顺序枚举

"""

# nums = [1, 1, 1, 1]
# makesquare_v2(nums)

# nums = [1, 1, 2, 3, 4, 4, 5]
# nums = [1,1,1,1]
# print(len(nums))
# makesquare_v1(nums)
# makesquare_v1_no_cache(nums)
# makesquare_v2(nums)


"""
1. 枚举子集复杂度分析 - 3^n
    a. 利用一般的粗分析
        状态个数 * 每个状态枚举的复杂度
        2^n * 2^n = 4^n

    b. 更精细化的分析：考虑k-size子集 对应的子集的子集数量为 2^k, 而所有ksize子集的数量为 c(n, k)  
    所有k-size子集的状态计算数为 c(n, k) * 2*k. 这正是 3^n 的binominal expansion

    2^n = c(n, 1) + ... c(n, k) + ...  + c(n, n)

    c(n, 1) + ... c(n, k) + ...  + c(n, n)
    * 2^1            2^k             2*n
    = (1+2)^n
    = 3^n
"""