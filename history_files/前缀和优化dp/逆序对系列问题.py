import itertools
from typing import List

MOD = 1000_000_000 + 7
"""
0. 这些题一般问你，给你n个排列，要求：
- 满足恰好有k个逆序对；
- 在一些节点 [i,cnt_i] 上，要求前缀 [0,i] 满足恰好 cnt_i 个逆序对


1. 多维dp/逆序对 状态设计
- 如果ij为当前填入j 我还要记住什么可以填 之前填过什么数 2^1000 不可接受
- 排列逆序对的一个性质 135 和 123是一样的，
  如果当前填入j我知道左侧有多数比他小，算出逆序对后，左侧i-1个数只需考虑1-i-1的排列的逆序对 （子问题）

  所以从最右边，我随便枚举一个j 则左侧又变成i-1子问题，而j提供了 i-1-j 个逆序对，
  我们只需要设计状态ik为当前排列需要凑k个逆序对 
  
  
2. 前缀和优化dp 三段式
- 写出原dp
- 将枚举条件改成从哪个状态转移过来
- 前缀和
"""

class Solution_LC629:
    def kInversePairs(self, n: int, k: int) -> int:
        """
        要求n长排列提供恰好k个逆序对，最基础版本
        """
        f = [[0] * (k + 1) for _ in range(n + 1)]
        f[0][0] = 1
        for i in range(1, n + 1):
            for j in range(0, k + 1):  # 0个逆序对也是合法状态
                for l in range(max(0, j - i + 1), j + 1):  # 枚举从哪里转移过来，上一个状态是还剩多少个逆序对 【当前用了最大的i-1个，当前没用逆序对】
                    f[i][j] += f[i - 1][l]
                f[i][j] %= MOD
        #return f[n][k]

        ###################
        # 前缀和优化
        f = [[0] * (k + 1) for _ in range(n + 1)]
        f[0][0] = 1
        for i in range(1, n + 1):
            ps = list(itertools.accumulate(f[i - 1], initial=0))
            for j in range(0, k + 1):  # 0个逆序对也是合法状态
                # for l in range(max(0,j-i+1), j+1): # 枚举从哪里转移过来，上一个状态是还剩多少个逆序对 【当前用了最大的i-1个，当前没用逆序对】
                #     f[i][j] += f[i-1][l]
                # f[i][j] = sum(f[i-1][l] for l in range(max(0,j-i+1), j+1))

                f[i][j] = ps[j + 1] - ps[max(0, j - i + 1)]
                f[i][j] %= MOD
        #return f[n][k]

        ###################
        # 滚动数组优化
        pre = [0] * (k + 1)
        pre[0] = 1
        for i in range(1, n + 1):
            ps = list(itertools.accumulate(pre, initial=0))
            f = [0] * (k + 1)
            for j in range(0, k + 1):  # 0个逆序对也是合法状态
                # for l in range(max(0,j-i+1), j+1): # 枚举从哪里转移过来，上一个状态是还剩多少个逆序对 【当前用了最大的i-1个，当前没用逆序对】
                #     f[i][j] += f[i-1][l]
                # f[i][j] = sum(f[i-1][l] for l in range(max(0,j-i+1), j+1))

                f[j] = (ps[j + 1] - ps[max(0, j - i + 1)]) % MOD
            pre = f
        return pre[k]
###########################################
###########################################

mod = 10 ** 9 + 7

class Solution_LC3193:
    def numberOfPermutations(self, n: int, requirements: List[List[int]]) -> int:
        """
        给你n个排列，要求在一些节点 [i,cnt_i] 上，要求前缀 [0,i] 满足恰好 cnt_i 个逆序对
        """
        # n * n^2

        requirements = {i: req for i, req in requirements}
        m = max(requirements.values())
        f = [[0] * (m + 1) for _ in range(n + 1)]
        f[0][0] = 1
        for i in range(1, n + 1):
            ps = list(itertools.accumulate(f[i - 1], initial=0))
            for k in range(0, m + 1):
                if i - 1 in requirements and k != requirements[i - 1]: continue
                # [0 j i-1]
                # for j in range(max(0, i-k-1), i): # 当前从 [0,i) 选j 枚举的是选取的数 然后提供i-j-1个逆序对
                #     f[i][k] += f[i-1][k-(i-j-1)] # k-i+j+1>=0  j >= i-k-1

                # for j in range(0, min(k,i-1)+1): # 从上面改变，枚举可以提供的逆序对数量，还是不好优化成前缀和
                #     f[i][k] += f[i-1][k-j] # k-i+j+1>=0  j >= i-k-1

                # for j in range(max(0,k-i+1), k+1): # 考虑ik从空间上哪些前置转态转移过来，意义对应的就是-还剩余的逆序对数量
                #     f[i][k] += f[i-1][j] # k-i+j+1>=0  j >= i-k-1
                # f[i][k] = sum(f[i-1][j] for j in range(max(0,k-i+1), k+1)) 可以容易改成前缀和

                f[i][k] = ps[k + 1] - ps[max(0, k - i + 1)]
                f[i][k] %= mod
        return f[n][m]

        ######################### 先写出递归形式/dfs逻辑，再改递推
        # 多维dp/逆序对 状态设计
        # - 如果ij为当前填入j 我还要记住什么可以填 之前填过什么数 2^300 不可接受
        # - 排列逆序对的一个性质 135 和 123是一样的，
        #   如果当前填入j我知道左侧有多数比他小，算出逆序对后，左侧i-1个数只需考虑1-i-1的排列的逆序对 （子问题）

        #   所以从最右边，我随便枚举一个j 则左侧又变成i-1子问题，而j提供了 i-1-j 个逆序对，
        #   我们只需要设计状态ik为当前排列需要凑k个逆序对
        requirements = {i: req for i, req in requirements}
        # q[i]: 前i个 [0,i) 至少要提供的数对数量
        @cache
        def dfs(i, k):
            # 前i个 需要的逆序对为k       --- 第i个元素填j
            if i == 0:
                return 1 if k == 0 else 0

            # 查询如果当前k不满足这个恰好条件就返回0
            if i - 1 in requirements and k != requirements[i - 1]: return 0
            res = 0
            for j in range(i):
                # j提供的逆序对 i-j-1  j [j+1 ... i-1]
                res += dfs(i - 1, k - (i - j - 1))
            return res % mod
        # return dfs(n, max(requirements.values()))





