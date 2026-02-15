from collections import deque
from typing import List
"""
1. 无向图上拓扑排序 （考虑多点）
2. 有向图上拓扑排序 - 
3. 无向图上dfs检测环 (代码同下)
4. 有向图上dfs检测环 (color染色法，考虑菱形图）
- 部分题单
"""

##########################################################
# 无向图拓扑排序 叶子节点现在是indegree=1 入队以indegree=1 为标准 (即发现了新叶子) 访问过一个点后将indegree置0
# 如果存在拓扑排序，all(x==0 for x in indegree) = True
# 如果存在环，则所有的环路不会进入queue，会存在 indegree=2 的一些点，他们是环路
def toposort_non_directed(n:int, edges:List[List[int]]):
    # ex: 输入
    # n = 11
    # edges = [[0, 1], [1, 2], [1, 3], [2, 4], [4, 5], [5, 6], [5, 7], [4, 8], [7, 9], [7, 10], [10, 11]]
    g = [[] for _ in range(n)]
    indegree = [0] *n
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
        indegree[a] += 1
        indegree[b] += 1

    instance = [x for x in range(n) if indegree[x] == 1] # 记录一个拓扑排序的实例
    q = deque(instance)
    while q:
        cur = q.popleft()
        indegree[cur] = 0  # 置0 代表访问过
        for j in g[cur]:
            if indegree[j] == 0:  # 访问过的=0
                continue

            indegree[j] -= 1
            if indegree[j] == 1:  # 新的叶节点=1
                q.append(j)
                instance.append(j) #所有在j前面的排列都已经标记完毕
    if all(x == 0 for x in indegree):
        print("一个拓扑排序：", instance)
    print("无拓扑排序/有环, 环上点：", [i for i,x in enumerate(indegree) if x == 2])


##########################################################
# 有向图拓扑排序
# 核心思想：每次挑indegree=0的元素入队, 有环则不会入队
# 如果是普通bfs 则无法区分环与多入度 后者是toposort支持的, 而toposort做法能区分环与多入度
# 如果存在拓扑排序，all(x==0 for x in indegree) = True
# 如果存在环，则所有的环路不会进入queue，会存在 indegree=1 的一些点，他们是环路
def toposort_non_directed(n:int, edges:List[List[int]]):
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    for b, a in edges:
        graph[a].append(b)
        indegree[b] += 1

    instance = [i for i in range(n) if indegree[i] == 0]
    q = deque(instance) # 记录顺序 先放入入度0的初始人
    while q:
        cur = q.popleft() #q 始终保存0入度元素，即将从图上删除
        for j in graph[cur]:
            indegree[j] -= 1
            # indegree[cur] = 0  # 相比无向图少了0标记 下面变成0入队
            if indegree[j] == 0:
                q.append(j)  # indegree置0 则这是新图的source节点 其所有的入边被标记完，是符合拓扑排序的
                instance.append((j))
            # 如果有环，indegree是不会被置0的，所以压根不会进入queue

    if all(x == 0 for x in indegree):
        print("一个拓扑排序：", instance)
    print("无拓扑排序/有环", [i for i,x in enumerate(indegree) if x == 1])

##########################################
# dfs检查无向图的环
# 只需要在dfs的过程 如果发现某个邻居是dfs访问过的点（在要么是正在递归栈里/要么是访问过) 就标记环
# 其实无向图无环就是树，这就是 LC261 以图判树
def dfs_check_is_tree(n: int, edges: List[List[int]]) -> bool:
    # undirected graph 只要在dfs的路径上遇到正在递归栈中的人 就有问题
    g = [[] for _ in range(n)]
    for b, a in edges:
        g[a].append(b)
        g[b].append(a)

    color = [0] * n
    def dfs(i): # 用的其实是下文有向图的代码
        color[i] = 1 # 标记为栈中
        for j in g[i]:
            if color[j] == 1 or (color[j] == 0 and dfs(j)): # 其实不会遇到color[j]=2 因为你邻居j如果是2说明是先访问的，他一定来访问你 轮不到你后访问它
                return True
        color[i] = 2 # 标记为访问过
        return False
    return all(dfs(i) == False for i in range(n) if color[i] == 0) # 检测森林，不是单树


##########################################
# dfs检查有向图的环
# color 012 三色标记法，区分未入栈，栈中，访问后出栈
def dfs_check_loop_directed_graph(n: int, edges: List[List[int]]) -> bool:
    # directed graph 比 undirected graph要额外考虑菱形图
    g = [[] for _ in range(n)]
    indegree = [0] * n
    for b, a in edges:
        g[a].append(b)
        indegree[b] += 1

    color = [0] * n
    def dfs(i): # 用的其实是下文有向图的代码
        color[i] = 1 # 标记为栈中
        for j in g[i]:
            if color[j] == 1 or (color[j] == 0 and dfs(j)): # 其实不会遇到color[j]=2 因为你邻居j如果是2说明是先访问的，他一定来访问你 轮不到你后访问它
                return True
        color[i] = 2 # 标记为访问过
        return False
    return all(dfs(i) == False for i in range(n) if color[i] == 0)


"""
无向图检测环
    261. 以图判树

有向图检测环
    207. 课程表 

拓扑排序，记录排序结果
    210. 课程表 II （需使用正经的拓扑排序记录路径结果）
    802. 找到最终的安全状态 （反图上拓扑排序）
    913. 猫和老鼠 （拓扑排序 + 博弈dp)
"""