"""
n行m列
每一行的已占座位 最小
子树的剩余座位之和

https://leetcode.cn/problems/booking-concert-tickets-in-groups/solutions/2715106/xian-duan-shu-de-ying-yong-by-dfthb-6gk8
"""
from typing import List

class BookMyShow:
    def __init__(self, n: int, m: int):
        self.a = [0] * (4 * n) # 维护区间内最小值 （区间内的行 最少的人数）
        self.b = [0] * (4 * n) # 维护区间和 （区间内 的总人数）
        self.n = n # 行数
        self.m = m # 列数

    def gather(self, k: int, maxRow: int) -> List[int]:
        # [0 maxRow] 最小的能装下k人的行号 区间查询单点
        n = self.n
        r, c = self.query(1, 0, n-1, maxRow, k)
        if r == -1: # 如果[0,maxRow]内不存在能容纳k人的行，返回特殊index -1 超出索引 代表结果不存在
            return []
        else:
            return [r, c]

    """
    查询前缀 [0, maxRow] 能容纳 k 的最小行值 如果存在则更新并返回行列坐标，不存在返回 [n,-1]
    
    线段树前三个入参固定为 节点编号以及对应的左右区间
     + 查询区间/节点/criteria
    
    关于查询节点维护区间和查询区间
    一般写法 查询区间为固定值，节点维护区间跟节点编号走 但节点区间范围落在查询区间内 则停止递归
    不担心遗漏 因为开始递归根节点时 查询区间包含在全体区间内，一定会被覆盖到
    
    本题只需查询前缀，查询入参只有maxRow 
    最开始maxRow处于全部查询范围内 而每次递归都保证往前缀范围走，
    所以每次递归函数被call 都默认 max in [l,r] 无须检查范围
    """
    def query(self, p, l, r, maxRow, k): #递归前认为max在[l,r]之中
        n, m = self.n,  self.m
        if m - self.a[p] < k: #该子节点对应的行最大单行容量不够装下k
            return -1, -1

        if l == r:
            c = self.a[p]
            self.a[p] += k
            self.b[p] += k
            return l, c

        mid = (l+r)//2
        # 先递归左，如果不存再递归右
        row, col = self.query(2*p, l, mid, maxRow, k)
        if row == -1 and mid < maxRow:
            row, col = self.query(2*p+1, mid + 1, r, maxRow, k)

        # 合并区间, 如果发生了更新 （找到了行号）则更新
        if row != -1:
            self.a[p] = min(self.a[2*p], self.a[2*p+1])
            self.b[p] = self.b[2*p] + self.b[2*p+1]
        return row, col

    # 加强版 查询 left， right内满足k的最小index
    def query1(self, p, l, r, left, right, k):
        n, m = self.n,  self.m
        if m - self.a[p] < k:  # 放在统一入口好，防止特殊情况 即根节点范围只有单点 [1,1]
            return -1, -1
        if l == r:
            col = self.a[p]
            self.a[p] += k
            self.b[p] += k
            return l, col

        mid = (l+r)//2
        row = col = -1
        if left <= mid: #查询区间与左子区间有交集
            row, col = self.query1(2*p, l, mid, left, right, k)
        if row == -1 and mid < right: #只有左侧没有递归进去 再来看右边
            row, col = self.query1(2*p+1, mid + 1, r, left, right, k)

        if row != -1:
            self.a[p] = min(self.a[2*p], self.a[2*p+1])
            self.b[p] = self.b[2*p] + self.b[2*p+1]
        return row, col

    """ 先查询 再更新 不能做到查询更新同步，因为是区间查询 + 区间修改（只增加，单向修改）
     
     本题区间添加后就不再需要递归进子数组了，假如满了是不会离场的，所以不需要lazy tag什么的
    """
    def scatter(self, k: int, maxRow: int) -> bool:
        m, n = self.m, self.n
        if (maxRow + 1)*m - self.getSum(1, 0, n-1, 0, maxRow) < k:
            return False
        self.update(1, 0, n-1,  k)
        return True

    # 标准查询和模板 
    def getSum(self, p, l, r, left, right): 
        if left <= l and r <= right:
            return self.b[p]
        mid = (l+r)//2
        res = 0
        if left <= mid:
            res += self.getSum(2*p, l, mid, left, right)
        if mid < right:
            res += self.getSum(2*p+1, mid+1, r, left, right)
        return res

    """ 范围[l,r] 插入k人 默认足够人数
    这个update不能用lazy tag 也就是必须深入到更新每一个点 l == r
    每次更新复杂度是 O(k) 且为一次性的 （默认k很小，如果是区间更新可能O(n) 则要考虑lazy tag）
    """
    def update(self, p, l, r, k):
        m = self.m
        if l == r:
            self.a[p] += k
            self.b[p] += k
            return

        mid = (l+r)//2
        # [l, mid] [mid+1, r]
        l_vacancy = (mid-l+1)*m - self.b[2*p] #左侧区间的空位
        if l_vacancy >= k: #只递归更新左侧
            self.update(2 * p, l, mid, k)
        else: #左边放满 剩余更新右边
            self.update(2 * p, l, mid, l_vacancy)
            self.update(2*p+1, mid+1, r, k - l_vacancy)

        self.a[p] = min(self.a[2*p], self.a[2*p+1])
        self.b[p] = self.b[2*p] + self.b[2*p+1]
        return




if __name__ == '__main__':
    # print("hello")
    # s = BookMyShow(94, 270375234)
    # print(s.scatter(207095844, 4))
    # print(s.a)
    # print(s.b)
    # print(s.gather(77100725, 62))

    # s = BookMyShow(2, 5)
    # print(s.gather(4,0))
    # print(s.gather(2, 0))
    # print(s.scatter(5,1))
    # print(s.scatter(5, 1))
    # print(s.a)
    # print(s.b)

    s = BookMyShow(5,9)
    print(s.scatter(2,2))
    print(s.gather(7,2))
    print(s.gather(4,1))
    print(s.gather(6,2))
    print(s.a)
    print(s.b)
    print(s.scatter(2,1))
    print(s.a)
    print(s.b)


# Your BookMyShow object will be instantiated and called as such:
# obj = BookMyShow(n, m)
# param_1 = obj.gather(k,maxRow)
# param_2 = obj.scatter(k,maxRow)