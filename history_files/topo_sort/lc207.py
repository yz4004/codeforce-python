"""

从 bfs 角度检测环

基础bfs算法，不能区分环和多入度
    从root点群出发去遍历，如果一个点的临点没被入队过，就入队
    但他不能区分菱形还是环，对于环，重新回到环首，发现访问过了，bfs就停止了
    但如果我们遇到一个重复访问的点（已经入过对）那又不适用于菱形图，多个课通向同一个课
    所以基础bfs不能区分环和多入度 （他们都会造成重复访问）

           1
          / \
         2   3
          \ /
           4
          / \
          ...
"""
import collections
from typing import List


# bfs 找环
def bfs_template(self, n: int, prerequisites: List[List[int]]) -> bool:
    graph = [] # 建图省略
    init = [] #所有起始点 （入度为0）
    q = collections.deque([i for i in range(n) if init[i]])
    if not q:
        return False
    inque = init[:]
    while q:
        c = q.popleft()
        for j in graph[c]:
            if not inque[j]: # bfs模板 只要发现 j 不在q内就将他入队，并标记
                inque[j] = True
                q.append(j)
            # else:  但多入度也可以导致 inque为true 不应返回false
            #     return False
    return all(x for x in inque)

"""  
改进
对多入度的点来说，其一个入边访问过他，她还不能入队，等待其所有入边都被访问过，再入队。这时候就算完成标记了，如果未来访问到已经入队的点，这就说明是环上点
"""
def canFinish(self, n: int, prerequisites: List[List[int]]) -> bool:
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    for b, a in prerequisites:
        graph[a].append(b)
        indegree[b] += 1

    # bfs 找环
    q = collections.deque([i for i in range(n) if indegree[i] == 0])
    # 定义q内的元素是当前要学习的课程，则有前提，其所有prerequsite都学完了，即入度标记为0
    while q:
        c = q.popleft()
        for j in graph[c]:
            indegree[j] -= 1
            if indegree[j] == 0:
                q.append(j)
            # elif indegree[j] < 0:  其实是不必要的
            #     return False
    return all(x == 0 for x in indegree)
    # 这个写法安全，因为每次都修改一次indegree再入队，永远不会重复入队
    # 另一种更好的判别是，只对indegree==0 入队，同时记录visited cnt 所有入队过的都cnt+1 最后看cnt是否等于n
    # 对于环，其实永远不会进入，因为对有环图，在通过一条匝道到环入口后，那个入口点的indegree其实是2，减去1后仍正，所以永远不会入队 如果只有纯环，则没有起始点
    # 这个升级版bfs 叫 kahn 算法
    # 想找字典序，可以将kahn种queue换成pq 则每次取出字典序最小的拓扑排序
    # https://oi-wiki.org/graph/topo/#dfs-%E7%AE%97%E6%B3%95

# 同样的思想改成 dfs，只有indegree=0才可以递归进去, 不会无线递归，indegree代替了路径上的visited数组，另记录一个起始入口数组，因为后面的递归会将indegree改为0
# 如果从ind==0进入，可能进入了已经遍历过的点，而他前后都已经访问过并置0，如果再进入，会把好的0变成-1，或者再额外记录一个visited数组也是可以的，记录dfs visited过得的点
# 这个只能算bfs变形，换个结构而已
def canFinish(self, n: int, prerequisites: List[List[int]]) -> bool:
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    for b, a in prerequisites:
        graph[a].append(b)
        indegree[b] += 1

    init = [i for i in range(n) if indegree[i] == 0]
    def dfs(i):
        for j in graph[i]:
            indegree[j] -= 1
            if indegree[j] == 0:
                dfs(j)
    for i in init:
        dfs(i)
    return all(indegree[i] == 0 for i in range(n))

"""

环和多入度
    虽然都是重复访问，但是访问的时机是不同的，
    环是在一次深度搜索上遇到 【当前】 搜索路径上的访问过点
    多入度则是不同的搜索路径都访问过同一点，这是两种情况，如何区分呢？
    
    关键是区分 visited， visiting， to visit 三种状态
    bfs控制这种办法是通过indegree
    在纵深dfs过程中 我们注意标记路径上访问过的点为1 如果递归中遇到了1 那就有环了
    但对于多入度，如果一个点的所有出边已经遍历完，我们把它标记成2，而再递归中预见 2 则不会报错，
    标记成2的条件是 他的出边已经遍历完（且没有报错返回），也就是我们再预见2时，可以安全的知道从他往后没有路径成环的点，可以返回
    这同时也区分了同路径和不同路径访问过的点
    1 是同路径上的，2是不同路径上的
"""

def canFinish(self, n: int, prerequisites: List[List[int]]) -> bool:
    graph = [[] for _ in range(n)]
    for b, a in prerequisites:
        graph[a].append(b)

    visited = [0] * n  # 0-未访问 1-路径上访问 2-以经搜索完所有从i出发的路径
    def dfs(i):
        if visited[i] == 2:
            return True
        res = True
        visited[i] = 1
        for j in graph[i]:
            if visited[j] == 1:
                return False
            res = res and dfs(j)
        visited[i] = 2
        return res
    return all(dfs(i) for i in range(n))

"""
另一种dfs写法也是类似思路
只有访问过所有出边后 将点标成global visited
而路径visited我们要报警，global visited不报警
但是双visit数组 路径visited在回溯结束后要取消标记，因为他可能是另一个
"""
def canFinish(self, n: int, prerequisites: List[List[int]]) -> bool:
    graph = [[] for _ in range(n)]
    for b, a in prerequisites:
        graph[a].append(b)
    global_visit = [False] * n  # i globally visited 条件：只有所有从i出发的枝杈都被搜索后 才能标记为True
    visited = [False] * n  # 在一条路径上搜索时需要的标记 （不能和全局visited混淆）

    def dfs(i):
        if global_visit[i]:
            return True
        res = True
        for j in graph[i]:
            if visited[j]:  # 如果在当前的dfs路径上找到了该路径已访问过的点 -- 即有环
                return False
            visited[j] = True  # 标记路径访问过的点
            res = res and dfs(j)  # 沿j搜索到底 是否发现环
            visited[j] = False  # 离开时取消标记 回溯的标准结构，如果不标记，对于同路径上重访问当然会报错，但是不同路径上的重访问也会发现已访问，返回了，比如对于菱形图，最低下的那个多入度点
        global_visit[i] = True  # 当所有从i出发路径都被搜索过，标记i已被搜索过
        return res
    return all(dfs(i) for i in range(n))


"""
拓扑排序, 4231的伪代码
 TopologicalOrder(G)
      Find a source vertex s and order it first
      Delete s and its adjacent edges from G; let G be the new graph.
      TopologicalOrder(G')
      Append the order found after s.
所谓删除一个点，即删除改点和其所有的边 outgoing edge
这个实现就是标记一个点所有外出的相邻边 dfs的 visited=2 标记，在dfs搜索完该点后，再把该点标记成2，代表所有纵深搜索已经完成
不过注意 删除的这个点 一定是新图的source点 即更新indegree后入度为0的点，实际上是kahn算法的实现
"""
# 错误
# class Solution:
#     def canFinish(self, n: int, prerequisites: List[List[int]]) -> bool:
#         graph = [[] for _ in range(n)]
#         init = [False] * n
#         for b, a in prerequisites:
#             graph[a].append(b)
#             init[b] = False
#
#         q = collections.deque([i for i in range(n) if init[i]])
#         inque = init
#         visited = [False]*n
#         while q:
#             cur = q.popleft()
#             for j in graph[cur]:
#                 if visited[j]:
#                     return False
#                 if not inque[j]:
#                     inque[j] = True
#                     q.append(j)
#             visited[cur] = True
#         return True
#
