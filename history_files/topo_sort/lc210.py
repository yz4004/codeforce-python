import collections
from typing import List
"""
https://leetcode.cn/problems/course-schedule-ii/
三种写法，最需要掌握bfs的 kahn algo

"""

def findOrder(self, n: int, prerequisites: List[List[int]]) -> List[int]:
    # 入度为0入队的 bfs 写法 kahn algorithm
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    for b, a in prerequisites:
        graph[a].append(b)
        indegree[b] += 1
    res = [i for i in range(n) if indegree[i] == 0]
    q = collections.deque(res)
    while q:
        cur = q.popleft()
        for j in graph[cur]:
            indegree[j] -= 1
            if indegree[j] == 0:
                q.append(j)
                res.append(j)  # indegree置0 则这是新图的source节点 其所有的入边被标记完，是符合拓扑排序的
            # 如果有环，indegree是不会被置0的，所以压根不会进入queue
    if all(x == 0 for x in indegree):
        return res
    return []

def findOrder(self, n: int, prerequisites: List[List[int]]) -> List[int]:
    # 入度为0 dfs递归 更安全的写法
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    for b, a in prerequisites:
        graph[a].append(b)
        indegree[b] += 1

    init = [i for i in range(n) if indegree[i] == 0]  # 初始入度为0的点，单独遍历他们
    res = init[::]
    def dfs(i):
        for j in graph[i]:
            indegree[j] -= 1
            if indegree[j] == 0:
                res.append(j)  # pre-traversal 先记录后递归
                dfs(j)
    for i in init:
        dfs(i)
    return res if len(res) == n else []



def findOrder(self, n: int, prerequisites: List[List[int]]) -> List[int]:
    # 入度为0的 dfs写法，但这个写法并不是很好，
    # 因为入口遍历indegree 但是dfs也会修改indegree 虽然重复进去后indegree变-1也不影响 但是不安全
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    for b, a in prerequisites:
        graph[a].append(b)
        indegree[b] += 1
    res = []

    def dfs(i):
        indegree[i] = -1
        for j in graph[i]:
            indegree[j] -= 1
            if indegree[j] == 0:
                res.append(j)
                dfs(j)


    for i in range(n):
        if indegree[i] == 0:
            res.append(i)
            dfs(i)
    return res if len(res) == n else []