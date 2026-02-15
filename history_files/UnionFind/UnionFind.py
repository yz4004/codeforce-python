"""
1. find(x: int) -> int              点x的所属集合代表元p 路径压缩
2. union(x: int, y: int) -> bool    将x y所属集合合并，true - 合并成功 false - 本来就是一个集合

两个数组
pa: i -> pa[i] 元素i的parent 路径压缩后指向集合代表元
size： size[i] 代表元i所属集合的size
"""
class UnionFind:
    def __init__(self, n):
        self.pa = list(range(n))
        self.size = [1]*n

    def find(self, x) -> int:
        if self.pa[x] == x:
            return x
        self.pa[x] = self.find(self.pa[x])
        return self.pa[x]

    def union(self, x:int, y:int) -> bool:
        size, pa = self.size, self.pa
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return False
        else:
            # 小的size合并到大的size上
            if size[x] < size[y]:
                size[y] += size[x]
                pa[x] = y
            else:
                size[x] += size[y]
                pa[y] = x
            return True

"""
721. 账户合并 https://leetcode.cn/problems/accounts-merge/

1584 最小生成树的 kruskal
https://leetcode.cn/problems/min-cost-to-connect-all-points/
"""

