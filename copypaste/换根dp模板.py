
"""
两种换根dp写法

"""
from math import inf
from typing import List
class Reroot_dp_lc3772:
    def maxSubgraphScore(self, n: int, edges: List[List[int]], good: List[int]) -> List[int]:
        # lc3772 求子图最大得分 定义子图得分 为子图中好节点的数量减去坏节点的数量
        # 输入无向树 - 子图就是子树
        # 枚举以每个点为root的树 找根节点附近的最大邻域.
        # 考虑每个子树的贡献值 转化为 1/-1 正子树才有贡献、负数就不要. -- 就是lc53

        # 换根dp 两种视角

        # 0. 建图
        g = [[] for _ in range(n)]
        for a, b in edges:
            g[a].append(b)
            g[b].append(a)

        ########################################################################
        # 1. 预处理以0为根视角 - 子树的分数
        f0 = [-inf] * n  # f0[i] 以0-root视角 i为根的子树 的最大得分
        def dfs(i, p):
            cur = 1 if good[i] else -1
            for j in g[i]:
                if j == p: continue
                v = dfs(j, i)
                cur += max(v, 0) # 累计子树正贡献
            f0[i] = cur
            return cur
        dfs(0, -1)

        ########################################################################
        # 视角1
        # 入点i的解已经计算出来 对子节点j进行转移 -- 刷表法
        ans = f0[:]
        def reroot(i, p):
            for j in g[i]:
                if j == p: continue
                up = max(0, ans[i] - max(0, f0[j])) # 计算j上方i 对他的贡献. 即父节点i的最大分数排除j的贡献 （如果是正分数）
                ans[j] = f0[j] + up # 结合j下方的分数
                reroot(j, i)
        # reroot(0, -1)
        # return ans

        ########################################################################
        # 视角2
        # 考虑先计算当前i 再转移
        # 需父节点传入up的值 + 枚举其每个子树 -- 查表法
        ans = f0[:]
        def reroot(i, p, up):
            # 考虑当前i 根的分数. 需要枚举所有子节点的正分数贡献 + 上方传来的最大贡献

            cur = (1 if good[i] else -1) + max(0, up) # 上方贡献已经是正数
            for j in g[i]:
                if j == p: continue
                # 子树j对 以i为根的树贡献
                cur += max(f0[j], 0)
            ans[i] = cur

            # 当前cur转移到子树 排除子树影响
            for j in g[i]:
                if j == p: continue
                # 如果 f0[j] > 0 则说明j对cur有贡献，排除
                up = cur - max(f0[j], 0)
                reroot(j, i, max(up, 0))
        reroot(0, -1, 0)
        return ans
        ########################################################################

        # 其他题目
        # https://leetcode.cn/problems/time-taken-to-mark-all-nodes/description/ 维护最大次大. 写法2
        # 参考刷表法 https://chatgpt.com/c/695b5c74-7b68-832e-b4b7-4a6f09b2140a






