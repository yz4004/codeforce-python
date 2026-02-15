from math import inf
"""
树的重心 centroid
1. 以重心为根的树，其最大子树的节点最少，且所有子树大小 < 节点数/2
    ps 如果某个子树节点超过 n/2, 说明重心在那个子树中
2. 偶树有两个重心且相邻，且平分节点总数，奇树一个
3. 重心划分的子树，保证最大子树不超过 n/2 保证了分治不会退化成 n^2 
"""

def findCentroid(n, edges):
    # g[]
    g = [[] for _ in range(n)]
    for a,b in edges:
        g[a].append(b)
        g[b].append(a)

    minOfMaxSubSize = inf
    centroid = -1

    def dfs(i,p) -> int: # 子树size
        nonlocal minOfMaxSubSize, centroid

        size = 1
        maxSubSize = 0
        for j in g[i]:
            if j == p: continue
            sz = dfs(j,i)  # 找最大子树
            maxSubSize = max(maxSubSize,  sz)
            size += sz
        maxSubSize = max(maxSubSize, n - size) # 上方“子树” 不算节点i
        if maxSubSize < minOfMaxSubSize:
            minOfMaxSubSize = maxSubSize
            centroid = i
        return size
    dfs(0, -1)
    return centroid, minOfMaxSubSize


""" 
点分治 重心分解（CD, Centroid Decomposition）
路径相关问题

"""
def centroid_decomposition(n, edges):
    g = [[] for _ in range(n)]
    for a,b,w in edges:
        g[a].append((b,w))
        g[b].append((a,w))

    deleted = [False]*n
    size = [0]*n

    def findCentroid(i, p, comp_size) -> (int, int, int):
        # 返回以子树i 重心后选尺寸，重心后选，重心后选的父节点

        minSize = inf
        maxSubSize = 0
        size[i] = 1

        centroid = fa_centroid = -1

        for j,w in g[i]:
            if j == p or deleted[j]: continue
            minSize_w, centroid_w, fa_c_w = findCentroid(j,i, comp_size)  # 找最大子树
            if minSize_w < minSize: # 更优的重心后选
                minSize, centroid, fa_centroid = minSize_w, centroid_w, fa_c_w

            maxSubSize = max(maxSubSize, size[j])
            size[i] += size[j] # 加到当前子树尺寸

        # i的上方子树
        maxSubSize = max(maxSubSize, comp_size - size[i])
        if maxSubSize < minSize:
            minSize, centroid, fa_centroid = maxSubSize, i, p
        return minSize, centroid, fa_centroid

    ans = 0 # 演示用 全局结果
    def dfs(i, p, comp_size):
        # 以i为根节点的子树 找到子树重心
        _, centroid, fa_centroid = findCentroid(i, p, comp_size)

        # 收集以重新 centroid 为起点，到各子树节点路径的权值和
        path_val_set = set([0]) # 重心到自己的距离 0 放进去

        # 对重心每个 未删除/在当前子树 中的邻居做dfs收集
        for j,w in g[centroid]:
            if deleted[j]: continue

            # 从重心centroid出发，到j的路径和 计入到tmp中
            tmp = []
            def f(i, p, path_val):
                tmp.append(path_val)
                for j, w in g[i]:
                    if j == p or deleted[j]: continue
                    f(j, i, path_val + w)
            f(j, centroid, w) # 以 centroid -> j,w 这条边开始

            # 遍历完 j 子树，收集进当前总子树 (i) 的路径集合中
            for _, path_val in tmp:
                path_val_set.add(path_val)

        # 删除重心
        deleted[centroid] = True

        # 对删除重心后 重心的临接子树进行递归分治 （不是对i的邻居，因为i又不是被删除的那个人）
        for j,w in g[centroid]:
            if deleted[j]: continue
            # 需要区分j相对于centroid的视角，如果是父视角，应该从comp_size减去
            if j == fa_centroid:
                dfs(j, centroid, comp_size - size[j])
            else:
                dfs(j, centroid, size[centroid])

    # 初始从编号0入手点分治
    dfs(0, -1, n)
    return ans




"""
计算树中路径长度为k的路径总数
- 每个子树返回所有小于等于k长的枝条统计 [0,k] 长度为i的branch有几个
"""







