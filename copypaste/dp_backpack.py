import itertools
from typing import List
from math import inf

# 参考 https://github.com/EndlessCheng/codeforces-go/blob/master/copypasta/dp.go

# @@背包
######################################################################################################
######################################################################################################
def back_pack():
    """ 01背包 物品重量不超过 maxW, 最大价值和
    """


    def zero_one_knapsack(weights: List[int], values: List[int], max_w: int):
        # 最大背包容量max_w, 求最大价值
        n, m = len(weights), max_w
        f = [[0] * (m + 1) for _ in range(n + 1)]  # f[i][j] 前i个物品限制至多装满j （容量限制为j 不是恰好）
        for i in range(1, n + 1):
            for j in range(1, m + 1):  # 这个f[i][0]不更新没关系，本来也是0
                f[i][j] = f[i - 1][j]
                if weights[i - 1] <= j:
                    f[i][j] = max(f[i - 1][j], f[i - 1][j - weights[i - 1]] + values[i - 1])
        print(f[n][m])

        # 空间优化
        f = [0] * (m + 1)
        for i in range(n):
            for j in range(m, 0, -1):  # 1.倒叙更新防止冲突; 2.for循环可以截止到当前weights
                if weights[i] <= j:
                    f[i] = max(f[j], f[j - weights[i]] + values[i])
        print(f[m])


    """ 01背包 物品重量恰好为 maxW, 最大价值和
    """


    def zero_one_knapsack_exact_full(weights: List[int], values: List[int], max_w: int):
        # 最大背包容量max_w, 求能否恰好填满
        n, m = len(weights), max_w
        f = [[-inf] * (m + 1) for _ in range(n + 1)]  # f[i][j] 前i个物品 恰好装满j
        f[0][0] = 0
        for i in range(1, n + 1):
            for j in range(0, m + 1):  # 这个f[i][0]=0须传递
                f[i][j] = f[i - 1][j]
                if weights[i - 1] <= j:
                    f[i][j] = max(f[i - 1][j], f[i - 1][j - weights[i - 1]] + values[i - 1])  #
        # f[n][j] 前n个物品 恰好装满j 的value最大
        # 空间优化
        f = [-inf] * (m + 1)
        f[0] = 0
        for i in range(n):
            for j in range(m, 0, -1):  # 1.倒叙更新防止冲突; 2.for循环可以截止到当前weights
                if weights[i] <= j:
                    f[i] = max(f[j], f[j - weights[i]] + values[i])

        for j in range(m, -1, -1):
            if f[j] >= 0:
                # f[j] 前n个物品 恰好装满j 的value最大
                pass


    """ 01背包 物品重量至少为 maxW, 最小价值和
    """

    def zero_one_knapsack_at_least_fill_up(weights: List[int], values: List[int], max_w: int):
        # f[n][j] 前n个物品 恰好装满j 的value最大
        n, m = len(weights), max_w
        f = [inf] * (m + 1)
        f[0] = 0
        for i in range(n):
            for j in range(m, 0, -1):
                f[i] = min(f[j], f[max(j - weights[i], 0)] + values[i])  # 当weights[i]超过j 则代表选够了weight剩下的可以自由的选或不选（value都正的情况下当然不选）
        # 和恰好形的区别是，< weights 的部分是“至少”会被更新，有的问题只关心“至少”，上界可以控制更小
        # LC879 盈利方案

        # 另一种写法, 当前j能更新谁 vs 当前j被谁更新
        for i in range(n):
            for j in range(m, 0, -1):
                k = min(j + weights[i], m)  # 这个k可以从当前j转移到
                f[k] = min(f[k], f[j] + values[j])


    """ 01背包 凑够 maxW 的方案数
    """


    def zero_one_knapsack_way_to_sum(nums: List[int], target: int):
        n, m = len(nums), target
        f = [0] * (m + 1)
        f[0] = 1
        for i in range(n):
            for j in range(m, 0, -1):
                if nums[i] <= j:  # 当前nums[i] 能参与j的构建
                    f[j] += f[j - nums[i]]  # % mod
        print(f[m])


    """ 01背包 可行解 bitset 优化 （上文方案数的简化版，只问可行性）
    """


    def zero_one_knapsack_has_way_to_sum(nums: List[int], target: int):
        n, m = len(nums), target
        f = [0] * (m + 1)
        f[0] = 1
        for i in range(n):
            for j in range(m, 0, -1):
                if nums[i] <= j:  # 当前nums[i] 能参与j的构建
                    f[j] |= f[j - nums[i]]
        print(f[m] == 1)

        # 上文更新实质是所有 j 由 j - nums[i] 更新而来，可以bit shift
        f = 1  # 我们向左shift,
        for v in nums:
            f |= f << v
        print(f >> m & 1 == 1)  # 第m个bit位

        # LC3181 https://leetcode.cn/problems/maximum-total-reward-using-operations-ii/description/
        # 这题说从0开始构建数字，从nums中挑选数字加在正在构建的数字上，要求挑选的数字大于等于当前正在构建的数字
        # 0 + x1 + x2 ... 满足 sum(x1 + ... xi-1) <= xi
        # 初始顺序无关所以排序，问题变成考虑前i个物品的选取，第i个物品的选择要求，前一个总和小于等于nums[i]
        # 如果考虑 f[i][j] 前i个j可行解问题，就是背包问题，但是转移限制于 f[i][j] - f[i-1][i-nums[i]] s.t. i-nums[i]<=nums[i]
        # 所以用bitmask过滤掉 [i-nums[i]+1, i] 之间的数/只保留 [0, nums[i]] 的状态
        nums = sorted(set(nums))  # 还可以进一步过滤
        f = 1
        for v in nums:
            mask = (1 << v) - 1
            f |= (f & mask) << v
        print(f.bit_length() - 1)


    """完全背包 - 未优化
        给定物品weight value 可以无线选 求满足最大容量不超过max_w的情况下，最大价值和
    """


    def unbounded_knapsack1(weights: List[int], values: List[int], max_w: int):
        n, m = len(weights), max_w
        f = [[0] * (m + 1) for _ in range(n + 1)]  # 前i个物品 容量不超过j 最大价值
        for i in range(1, n + 1):
            w, v = weights[i - 1], values[i - 1]
            for j in range(0, m + 1):
                # 枚举当前第i个元素选 k 个
                # for k in range((j//w)+1):
                #     f[i][j] = max(f[i][j], f[i-1][j - k*w] + k*v)

                f[i][j] = f[i - 1][j]  # 不选当前第i个物品
                if w <= j:
                    f[i][j] = max(f[i][j], f[i][j - w] + v)
                # 无视第i个物品选了几个，只计一个，但仍从i行的状态转移
                # 另一种理解，上面k的遍历，新k只比k-1多计入了一个状态的转移 f[i-1][j - k*w] + k*v，而前k-1个状态早已经更新到 f[i][j-k], 所以额外
        print(f[n][m])


    """完全背包 - 优化
        给定物品weight value 可以无线选 求满足最大容量不超过max_w的情况下，最大价值和
        
    """


    def unbounded_knapsack2(weights: List[int], values: List[int], max_w: int):
        n, m = len(weights), max_w
        f = [0] * (m + 1)  # 前i个物品 容量不超过j 最大价值
        for w, v in zip(weights, values):
            for j in range(w, m + 1):
                f[j] = max(f[j], f[j - w] + v)
        print(f[m])


    """完全背包方案数 - 优化
    // LC518 https://leetcode.cn/problems/coin-change-ii/ 硬币兑换2
    // https://codeforces.com/problemset/problem/1673/C 1500
    // https://www.luogu.com.cn/problem/P1832
    // https://www.luogu.com.cn/problem/P6205（需要高精）
    """


    def unbounded_knapsack_way_to_sum(weights: List[int], max_w: int):
        n, m = len(weights), max_w
        f = [0] * (m + 1)  # 前i个物品 容量不超过j 最大价值
        f[0] = 1
        for w in weights:
            for j in range(w, m + 1):
                f[j] += f[j - w]
        print(f[m])

    # // 完全背包 EXTRA: 二维费用方案数
    # // 注意：「恰好使用 m 个物品」这个条件要当成一种费用来看待
    # // https://codeforces.com/problemset/problem/543/A


    """多重背包 Bounded Knapsack - 未优化
        给定物品weight value 库存上限stick，求满足最大容量不超过max_w的情况下，最大价值和
     
    // 模板题 https://codeforces.com/problemset/problem/106/C
    //       https://www.luogu.com.cn/problem/P1776
    // todo 多重背包+完全背包 https://www.luogu.com.cn/problem/P1782 https://www.luogu.com.cn/problem/P1833 https://www.luogu.com.cn/problem/P2851
    // http://acm.hdu.edu.cn/showproblem.php?pid=2844 http://poj.org/problem?id=1742
    // https://www.luogu.com.cn/problem/P6771 http://poj.org/problem?id=2392
    // https://codeforces.com/contest/999/problem/F
    // https://codeforces.com/problemset/problem/95/E
    // todo 打印方案
    """


    def bounded_knapsack(weights: List[int], values: List[int], stock: List[int], max_w: int):
        n, m = len(weights), max_w
        f = [[0] * (m + 1) for _ in range(n + 1)]  # 前i个物品 容量不超过j 最大价值
        for i in range(1, n + 1):
            w, v, u = weights[i - 1], values[i - 1], stock[i - 1]
            for j in range(1, m + 1):
                t = min(u, j // w)  # 最多可选 = min(库存上线，背包容量） 不能用u 否则覆盖了
                for k in range(t + 1):
                    f[i][j] = max(f[i][j], f[i - 1][j - k * w] + v * j)
        print(f[n][m])

        # 空间优化
        f = [0] * (m + 1)
        for i in range(1, n + 1):
            w, v, u = weights[i - 1], values[i - 1], stock[i - 1]
            for j in range(m, 0, -1):
                for k in range(min(u, j // w) + 1): # 最多可选 = min(库存上线，背包容量）
                    f[j] = max(f[j], f[j - k * w] + v * j)
        print(f[n])


    """多重背包 - 二进制优化
        给定物品weight value 库存上限stick，求满足最大容量不超过max_w的情况下，最大价值和
    """


    def bounded_knapsack_binary(weights: List[int], values: List[int], stock: List[int], max_w: int):
        n, m = len(weights), max_w

        # 通过背包容量上限转移 O(m*n*u)
        f = [0] * (m + 1)
        for i in range(1, n + 1):
            w, v, u = weights[i - 1], values[i - 1], stock[i - 1]
            for j in range(m, 0, -1):
                u = min(u, j // w)  # 最多可选 = min(库存上线，背包容量）
                for k in range(u + 1):
                    f[j] = max(f[j], f[j - k * w] + v * j)
        print(f[n])

        # 物品w 可以选 w*1 w*2 ... w*k k=m//w
        # 将数量k按2幂次拆分，则变成至多logk个物品（假设k的ith bit位为1，则对应i号物品 2^i * w 重量的物品) 则问题变成01背包问题
        # n*m*u -> n*m*logU


        f = [0] * (m + 1)
        for i in range(1, n + 1):
            w, v, u = weights[i - 1], values[i - 1], stock[i - 1]

            #
            # for j in range(m, 0, -1):
            #     u = min(u, j // w)  # 最多可选 = min(库存上线，背包容量）
            #     for k in range(u + 1):
            #         f[j] = max(f[j], f[j - k * w] + v * j)

            # max_w -> min(sum(w*num), max_w))
            # for j in range(m, )

            # 1, 2^1, 2^2 ... 2^i 二进制的基 可以表示 [1,u] 中的任意整数，
            # 这等于进行 k=logU 次 01背包，背包容量不能超过U
            # 所以对U进行完全背包 可以优化成logU
            # t = u.bit_length()
            for l in range(u.bit_length()+1):
                w1, v1 = (1<<l) * w, (1<<l) * v
                for k in range(u, -1, -1): # 当前01背包的容量/当前物品选k次
                    f[k] = max(f[k], f[k-w1] + v1)
            print(f[n])


# @@逆序对dp 前缀优化dp
######################################################################################################
######################################################################################################
def prefix_optimize_dp():
    """
    考虑1-n的全排列，逆序对数量恰好为k个的排列方案有多少

    - 定义f[i][j] 为子问题 前i个排列 恰好包含逆序对j个的排列方案数
        如果你想的是前i个数，当前填入t 需要知道t前面有多少个大于t的数字，那就错了，不能从全局的1-n排列思考，其实在[:i] 全局什么样和我们无关，无论[:i]具体是从[1-n]挑什么样的数，它都等价于 [1-i] 的排列方案

        前i个凑j个逆序对
        = 只考虑子问题[1-i]的全排列凑j个逆序对
        = 【f[i-1][j-(t-1)] 前i个内部凑j-(t-1)的方案】+【第i个填入元素t 引入t-1个逆序对】
    - 实际转移我们不枚举当期填入的数，而是枚举前一个转移来的状态t
    - 边界处理 f[i][0] = 1 唯一方案单增排列
    """
    def count_number_of_inverse(n: int, k: int) -> int:
        f = [[0]*(k+1) for _ in range(n+1)]
        for i in range(n+1): f[i][0] = 1
        for i in range(1, n+1):
            for j in range(1, k+1):
                f[i][j] = sum(f[i-1][t] for t in range(max(0, j-i+1),j+1)) # 当前[1-i]至多提供i-1个逆序对 所以前i-1个能提供的逆序对范围是 [max(0, j-i+1), j]
        print(f[n][k])

        # 手动前缀和优化
        f = [[0]*(k+1) for _ in range(n+1)]
        for i in range(n+1): f[i][0] = 1
        for i in range(1, n+1):
            ps = list(itertools.accumulate(f[i-1], initial=0))
            for j in range(1, k+1):
                # f[i][j] = sum(f[i-1][t] for t in range(max(0, j-i+1),j+1)) # 当前[1-i]至多提供i-1个逆序对 所以前i-1个能提供的逆序对范围是 [max(0, j-i+1), j]
                f[i][j] = ps[j+1] - ps[max(0, j-i+1)]
        print(f[n][k])

        # 观察转移规律 每次只需新增一个 移除一个
        for i in range(1, n + 1):
            f[i][0] = 1
            for j in range(1, k + 1):
                if j - i < 0:
                    f[i][j] = f[i][j - 1] + f[i - 1][j]
                else:
                    f[i][j] = f[i][j - 1] + f[i - 1][j] - f[i - 1][j - i]
        print(f[n][k])

        # 滚动数组优化
        f = [1] + [0] * k
        g = [1] + [0] * k
        for i in range(1, n + 1):
            for j in range(1, k + 1):
                if j - i < 0:
                    g[j] = g[j - 1] + f[j]
                else:
                    g[j] = g[j - 1] + f[j] - f[j - i]
            f, g = g, f
        print(f[k])
    
        # 例题
        # https://www.luogu.com.cn/problem/P2513 - 1-n恰好k个逆序对
        # LC3193 https://leetcode.cn/problems/count-the-number-of-inversions - 要求在一些列节点满足前i个恰好有j对 的排列方案数

"""
1-n 全排列 左侧可视的木棍恰好k个 的全部排列方案
- 第一类斯特林数，所有可视木棍以及挡住的部分形成一个整体，内部可以全部排列（除了打头的）
  反过来对于1-n，我们可以随意划分出k组，将k组每组内的最大设置为可视者前置
  所以问题等价于长为n的排列划分为k个非空圆排列（轮转）的方案数

- 排列也可以dp构造的角度考虑当前填什么 前i个部分无论是任意的 c(n,i)的子集 都等价于考虑 1-i 的排列（思考同逆序对）

第一类斯特林数: n 个不同元素排列 划分成 k 个不相交的循环排列（循环排列就是圆排列）的方法数。
- c(n,k) = c(n-1, k-1) + (n-1) * c(n-1, k) 将第n个元素单独作为一个循环 + 把第 n 个元素插到已有的循环里 

LC1866 https://leetcode.cn/problems/number-of-ways-to-rearrange-sticks-with-k-sticks-visible/
"""
mod = 10 ** 9 + 7
def rearrangeSticks(self, n: int, k: int) -> int:
    # 状态定义就遵从原排列问题
    # 类似的模型 1-n排列在逆序对恰好为k的方案
    # f[i][j] - 前i个排列生成恰好j个可见棍, ps 如果考虑子问题前i个，都等价于考虑1-i的排列
    # 转移 第i个位置是否能被看到，看不到有i-1个选择. 看到有1个选择
    #                   f[i][j-1] * (j-1) + f[i-1][j-1]

    f = [[0]*(n+1) for _ in range(k+1)]
    f[0][0] = 1 # 唯一合法情况，空方案=1; (空排列提供i个可视木棍 f[i][0]=0, f[0][j]=0 j长序列提供0个可视木棍也不可能)
    for i in range(1, k+1):
        for j in range(1, n+1):
            f[i][j] = (f[i-1][j-1] + f[i][j-1] * (j-1)) % mod
    print(f[k][n])

    # 空间压缩 - f[j]迭代到i 生成j个
    f = [0]*(k+1)
    f[0] = 1
    for i in range(1, n+1):
        g = [0]*(k+1)  # 这个不能创建在外面，因为交换会造成g[0]一直带着，实际只有f[0][0]=1 空序列合法 后续都应该有 f[i][0]=0
        for j in range(1, k+1):
            g[j] = (f[j] * (i-1) + f[j-1]) % mod
        f,g = g,f
    print(f[k] % mod)

"""
全排列相关组合问题
1. 逆序对恰好k个的排列方案数
2. 第一类斯特林数/1-n 全排列 左侧可视的木棍恰好k个 的全部排列方案

"""


n, x, y = 0,0,0
"""
n个元素(不同) 划分出x个子集(不同?)，允许空集合 求方案数
- 第i个人可以加入
"""
f = [[0]*(n+1) for _ in range(x+1)]
f[0][0] = 1
for i in range(1, x+1):
    for j in range(1,n+1):
        f[i][j] = f[i-1][j] * j + f[i-1][j-1]



