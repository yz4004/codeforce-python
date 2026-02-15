import collections

graph = []  # 建图省略
n = 10 # 图size

inque = [False]*n  # 其中包括 所有起始点 bool false 数组
inque[0] = True # 从0出发
q = collections.deque([i for i in range(n) if inque[i]])

while q:
    c = q.popleft()
    for j in graph[c]:
        if not inque[j]:  # 唯一入队 不在queue内
            inque[j] = True # 单向 永远不再入队
            q.append(j)
    # 核心是避免重复入队，而不是出队时再检查是否更新过，那样只是防止重复更新，但重复入队仍造成 O(n*m)
    # 一次入队则是 O(n+m)
