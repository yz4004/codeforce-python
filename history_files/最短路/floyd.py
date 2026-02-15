from math import inf
from typing import List

"""
1. floyd模板 （含空间优化）
2. 解析 （本质是按条件枚举）
3. 例题，进一步理解中间点集的枚举 lc2959
"""

def floyd(n, edges):
    """ edges=[[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]
    考虑枚举中间点集合/子图 [:k]，f[i][j][k] 为i-j路径中间（非ij）经过子图 [:k] 的最短路径 """

    """ 空间优化 """
    w = [[inf] * n for _ in range(n)]
    for i in range(n): w[i][i] = 0 #有没有都行
    for x, y, wt in edges:
        w[x][y] = w[y][x] = wt #初始化邻接矩阵

    f = w #初始状态ij中间节点经过index不超过0 即为空图，即没有中间节点，即为ij直连边
    for k in range(n):
        for i in range(n):
            for j in range(n):
                # 考虑 i-j 新过最大节点路径k的一条路径（后者）
                f[i][j] = min(f[i][j], f[i][k] + f[k][j]) #为什么不担心覆盖呢？见下面注释7，当前更新k+1我不担心用f[k+1][i][k] 因为 f[k+1][i][k] <- f[k][i][k] 依赖枚举当前过k路径，但 [k][k]=0; f[k+1][i][k] == f[k][i][k]

    """ 非空间优化 """
    f = [[[0] * n for _ in range(n)] for _ in range(n + 1)]
    f[0] = w
    # floyd 递推/松弛/刷表 (状态转以上看 k层ij依赖所有 k-1) 用k更新k+1层
    for k in range(n):
        for i in range(n):
            for j in range(n):
                # i-j 中间路径经过最大点k vs i-j 不经过最大点k
                f[k + 1][i][j] = min(f[k][i][j], f[k][i][k] + f[k][k][j])
    return f #最后一个状态 f[n]
"""
1. 本质就是选取视角枚举
2. 全局最短路，对每组 (x,y) 之间的所有路径，可以额外指定一个限制条件，从而枚举那个限制条件
    这里限制条件显然只能为点的index，即考虑 (x,y) 通过最大 index (1-n) 的路径
3. 定义 f[k][x][y] 为x-y，不含xy的中间节点index不超过k, 的最短路径
    初始化当xy路径不含任何中间节点时，即为edge
4. 当 （x,y） 考虑节点n时，要求已经计算 1-n-1的情况, 再考虑是否引入n会创造更短的路径，即考虑 
    x - n, n - y  这个组合能否更短 （dfs递归视角下就是选或不选）
5. 不通过n的路径，即要求我们在范围 1-n-1 子图上考虑最短路。这是一个子问题，直接由上一个状态传递过来
6. 注意状态定义。考虑 1-n-1 时，并不是只考虑 1-n-1 上的子图上的最短路径，而是考虑中间节点径过的子图为1-n-1 包含空图。
    中间节点经过空图，即无中间节点，即为xy的edge
7. 空间优化不担心覆盖，没必要用轮换数组，
    f[k + 1][i][j] = min(f[k][i][k] + f[k][k][j], f[k][i][j])
    f[i][j] = min(f[i][j], f[i][k] + f[k][j])
    
    之前需要轮换数组，是因为更新下一个状态本需要上一个状态的数组，但是上一个状态的数组被当前更新修改了。
    即f[i][k]/f[k][j] 可能已经对应k+1状态下的新值了, 即本需要 f[k][i][k] 却使用了 f[k+1][i][k]
    
    f[k + 1][i][j] = min(f[k][i][k] + f[k][k][j],     f[k][i][j])          should be 
    f[k + 1][i][j] = min(f[k+1][i][k] + f[k+1][k][j], f[k][i][j])          actual is 
    
    其实不担心，因为 f[k+1][i][k] == f[k][i][k]，因为 f[k+1][i][k] = min(f[k][i][k], f[k][i][k] + f[k][k][k]) - 新考虑i-k经过中间节点为k的路径，但后者为0
                                                  f[k+1][i][k] = min(f[k][i][k], f[k][i][k] + 0         )
                                                  f[k+1][i][k] =     f[k][i][k]
    所以不会使用到混乱数据
    
    
全局最短路 floyd 题单
1334. 阈值距离内邻居最少的城市 - 力扣（LeetCode） 模板直接用
2642. 设计可以求最短路径的图类 - 力扣（LeetCode） 向图中添加一条边，利用floyd枚举的性质更新最短路
2959. 关闭分部的可行集合数目 - 力扣（LeetCode） 进一步理解floyd的枚举特质，枚举路径经过的中间点集合，但是对所有1-n做更新；而不是只把目光局限在中间点集合内更新
2101. 引爆最多的炸弹 - 力扣（LeetCode） floyd 是枚举，所以不仅可以计算最短路，更可以检查连通性，bitset优化
2976. 转换字符串的最小成本 I - 力扣（LeetCode） 字符串变换（单字符）抽象成图 （dijkstra也可以做，甚至更快 （比较稀疏）
2977. 转换字符串的最小成本 II - 力扣（LeetCode） 字符串变换（区间段） 抽象成图 复杂编码 综合 

floyd vs dijkstra
m 边数， n 点数
全局 floyd:    O(n^3)         
单点 dijkstra O(m*logn)
全局 dijkstra O(n*m*logn) 如果m稠密 m=n^2 显然不如floyd
"""


""" 
lc2959 进一步理解中间点集的枚举
原版：f[k][i][j] 中间点最大不超过k的集合 -- 相比上一个状态 f[k-1][i][j]，  考虑新增一条路径 i-k k-j
现在: f[s][i][j] 中间点子集为s         -- 相比上一个状态 f[s-lb][i][j]，考虑新增一条路径 i-k k-j   k=s&-s; low_bit
"""
class Solution_lc2959():
    def numberOfSets(self, n: int, maxDistance: int, roads: List[List[int]]) -> int:
        ###########################
        # 初始图矩阵 - 邻接矩阵
        graph = [[inf] * n for _ in range(n)]
        for i in range(n): graph[i][i] = 0
        for i, j, w in roads:
            graph[i][j] = graph[j][i] = min(w, graph[i][j])

        f = [[[inf] * n for _ in range(n)] for _ in range(1 << n)]
        f[0] = graph
        for s in range(1, 1 << n):
            lb = s & -s
            # s - lb, s
            k = lb.bit_length() - 1

            # f[s] = f[s - lb] 不能这样更新，因为这个赋值会导致下面对 f[s][...] 的修改作用在 f[s-lb] 转移之前的数据上，污染
            for i in range(n):
                for j in range(n):
                    f[s][i][j] = f[s - lb][i][j]  # 注意是从上一个状态转移过来，而不能直接用当前 f[s][i][j] 此时是没有任何更新的
                    if f[s - lb][i][k] + f[s - lb][k][j] < f[s][i][j]:
                        f[s][i][j] = f[s - lb][i][k] + f[s - lb][k][j]

                    # 转移注意之前的状态是啥
                    # f[s][i][j] = min(f[s-lb][i][j], f[s-lb][i][k] + f[s-lb][k][j]) # 注意是 f[s-lb][i][j] 这是转移之前的上一个状态
                    # f[s][i][j] = min(f[s][i][j],    f[s-lb][i][k] + f[s-lb][k][j]) # 错误写法 f[s][i][j] 还没更新呢，没有用到转移之前的数据

        ## 求完所有的 经过中间子集的状态后 再判断
        res = 0
        for s in range(0, 1 << n):
            group = [i for i in range(n) if s >> i & 1 == 1] #考虑剩余分部集合为s
            valid = True
            for i in group:
                for j in group:
                    if f[s][i][j] > maxDistance:
                        valid = False
                        break
            if valid:
                res += 1
        return res

"""

"""