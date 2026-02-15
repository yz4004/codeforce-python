"""
记住前驱/路径的dijkstra
https://leetcode.cn/problems/find-edges-in-shortest-paths/
找所有0-n-1最短路上的边
"""
import heapq
from math import inf
from typing import List


class Solution:
    def findAnswer(self, n: int, edges: List[List[int]]) -> List[bool]:

        g = [[] for _ in range(n)]
        e = {} # 边的map 用来记录是否在最短路上 其实也没必要 一次dfs按最短路走就可以，当前距离，下一个状态哪个是最短路
        for a, b, c in edges:
            g[a].append((b, c))
            g[b].append((a, c))
            if a > b: a, b = b, a
            e[(a, b)] = False

        q = [(0, 0)]
        dist = [inf] * n
        pred = [[] for _ in range(n)] # 前驱
        while q:
            w, x = heapq.heappop(q)
            if w > dist[x]: continue  # (O(mn) -> O(mlogm + n)) 提前剪枝 避免空转
            for y, c in g[x]:
                if dist[y] > w + c:
                    dist[y] = w + c
                    heapq.heappush(q, (dist[y], y))
                    pred[y] = [x]
                elif dist[y] == w + c:
                    pred[y].append(x)

        def all_paths(predecessors, start, end): # 递归构建所有路径
            def build_path(end):
                if end == start:
                    return
                for pred in predecessors[end]:
                    # (end, pred)
                    a, b = end, pred
                    if a > b: a, b = b, a
                    e[(a, b)] = True # 标记ab在最短路上
                    build_path(pred)
            build_path(end)
        all_paths(pred, 0, n - 1)

        res = []
        for (a, b, c) in edges:
            if a > b: a, b = b, a
            res.append(e[(a, b)])
        return res

    def build_all_paths(predecessors, start, end):
        # 递归打印/构建所有路径
        def build_path(end, path):
            if end == start:
                all_paths.append(path[::-1])
                return
            for pred in predecessors[end]:
                build_path(pred, path + [end]) # append的简洁写法
        all_paths = []
        build_path(end, [start])
        return all_paths