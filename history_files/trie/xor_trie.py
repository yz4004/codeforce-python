from collections import  defaultdict
from typing import List

m = 31  # 最大的数据范围

class Node:
    __slots__ = 'children', 'passed'
    def __init__(self):
        self.children = [None]*2
        self.passed = 0
class Trie:
    def __init__(self):
        self.root = Node()
        # 最大数据范围见上

    def insert(self, x):
        cur = self.root
        self.root.passed += 1
        for i in range(m, -1, -1):
            c = x >> i & 1
            if not cur.children[c]:
                cur.children[c] = Node()
            cur = cur.children[c]
            cur.passed += 1

    def remove(self, x):
        cur = self.root
        self.root.passed -= 1
        # 没有删除节点，只是标记passed-1直到0
        for i in range(m, -1, -1):
            c = x >> i & 1
            cur = cur.children[c]
            cur.passed -= 1

            # 删除节点，先删子节点的，如果为0直接删除子节点 （可能要反复new节点，只有空间紧张时才会这么做）
        # for i in range(m, -1, -1):
        #     c = x >> i & 1
        #     cur.children[c].passed -= 1
        #     if cur.children[c].passed == 0:
        #         cur.children[c] = None
        #         return
        #     cur = cur.children[c]

    def query(self, x):
        cur = self.root
        res = 0
        for i in range(m, -1, -1):
            c = x >> i & 1
            if cur.children[c ^ 1] and cur.children[c ^ 1].passed:
                cur = cur.children[c ^ 1]
                res |= (1 << i)
            elif cur.children[c] and cur.children[c].passed:
                cur = cur.children[c]
        return res


class Solution:
    def maxXor(self, n: int, edges: List[List[int]], values: List[int]) -> int:
        g = defaultdict(list)
        for a,b in edges:
            g[a].append(b)
            g[b].append(a)
        A = [0]*n
        def dfs(u,f):
            A[u] = sum(dfs(v,u) for v in g[u] if v!=f)+values[u]
            return A[u]
        dfs(0,-1)
        L = A[0].bit_length()
        T = [set() for _ in range(L)]
        self.res = 0
        def dfs(u,f):
            x, y = A[u], 0
            for j in range(L-1,-1,-1):
                y *= 2
                y += (y+1)^(x>>j) in T[j]
            self.res = max(self.res,y)
            for v in g[u]:
                if v!=f:
                    dfs(v,u)
            for j in range(L):
                T[j].add(x>>j)
        dfs(0,-1)
        return self.res