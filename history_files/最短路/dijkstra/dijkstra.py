import heapq
from math import inf
from typing import List


class Solution:
    def minimumCost(self, n: int, edges: List[List[int]], query: List[List[int]]) -> List[int]:
        graph = [[] * n for _ in range(n)]
        d = [[inf] * n for _ in range(n)]
        an = -1
        for a, b, w in edges:
            if a > b: a, b = b, a
            graph[a].append(b)
            graph[b].append(a)
            an &= w
            d[a][b] = min(d[a][b], w)
            d[b][a] = d[a][b]

        dist = [None] * n  # 保存每个source生成的最短路径 对本体无用

        def dijkstra(c):  # 以c为起点的单源最短路，返回list 代表c到其他点的最短路径
            q = [(-1, c)]
            distance = [inf] * n
            distance[c] = 0
            cnt = 0
            visited = [False] * n
            while q:
                w, x = heapq.heappop(q)
                if not visited[x]:
                    visited[x] = True
                    cnt += 1
                if cnt == n: break
                for y in graph[x]:
                    c = d[x][y]
                    if distance[y] > w & c:
                        distance[y] = w & c
                        heapq.heappush(q, (distance[y], y))
            return distance

        res = [-1] * len(query)
        for i, (s, t) in enumerate(query):
            # s -> t
            res[i] = dijkstra(s)[t] & an if dijkstra(s)[t] != inf else -1

        return res