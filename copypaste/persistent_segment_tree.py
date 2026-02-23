from typing import List

# 可持久化线段树
# 用法见
# https://leetcode.cn/problems/minimum-operations-to-equalize-subarrays/submissions/681797289/
class Node:
    __slots__ = "l", "r", "lo", "ro", "cnt", "sm"

    # [l,r] lo/ro + 该线段维护内容 - [l,r] 的子区间 cnt, sum
    def __init__(self, l, r, lo=None, ro=None, cnt=0, sm=0):
        self.l = l
        self.r = r
        self.lo = lo
        self.ro = ro
        self.cnt = cnt
        self.sm = sm

    @staticmethod
    def build(l, r) -> "Node":
        o = Node(l, r)
        if l == r:
            return o
        mid = (l + r) // 2
        o.lo = Node.build(l, mid)
        o.ro = Node.build(mid + 1, r)
        return o

    def merge(self):  # 当前节点维护值
        self.cnt = self.lo.cnt + self.ro.cnt
        self.sm = self.lo.sm + self.ro.sm

    def add(self, i, x) -> "Node":
        l, r, lo, ro = self.l, self.r, self.lo, self.ro
        o = Node(self.l, self.r, self.lo, self.ro, self.cnt, self.sm)
        # 自根节点下 新增一条path 对应着更新版本后的树 -- 在i处增加x后的版本
        if self.l == self.r:
            o.cnt += 1
            o.sm += x
            return o

        mid = (self.l + self.r) // 2
        if i <= mid:
            o.lo = self.lo.add(i, x)
        if mid + 1 <= i:
            o.ro = self.ro.add(i, x)
        # self.merge()
        o.merge()  # 要对新版本的节点维护，旧版本不动
        return o

    def kth(self, old: "Node", k) -> int:
        if self.l == self.r:
            return self.l
        cnt_l = self.lo.cnt - old.lo.cnt
        if k <= cnt_l:
            return self.lo.kth(old.lo, k)
        else:
            return self.ro.kth(old.ro, k - cnt_l)

    def query(self, old: "Node", L, R) -> (int, int):
        l, r, lo, ro = self.l, self.r, self.lo, self.ro
        if L <= self.l and self.r <= R:
            return self.cnt - old.cnt, self.sm - old.sm

        res_cnt = res_sm = 0
        mid = (self.l + self.r) // 2
        if L <= mid:
            cnt, sm = self.lo.query(old.lo, L, R)
            res_cnt += cnt
            res_sm += sm
        if mid + 1 <= R:
            cnt, sm = self.ro.query(old.ro, L, R)
            res_cnt += cnt
            res_sm += sm
        return res_cnt, res_sm


# 单点更新线段树 开点写法
class Node:
    __slots__ = "l", "r", "lo", "ro",  "sm"
    # [l,r] lo/ro + 该线段维护内容 - [l,r] 的子区间 sum

    def __init__(self, l, r, lo=None, ro=None, sm=0):
        self.l = l
        self.r = r
        self.lo = lo
        self.ro = ro
        self.sm = sm

    @staticmethod
    def build(l,r, nums: List[int]) -> "Node":
        o = Node(l,r)
        if l == r:
            o.sm = nums[l]
            return o
        mid = (l+r)//2
        o.lo = Node.build(l,mid, nums)
        o.ro = Node.build(mid+1,r, nums)
        o.sm = Node.merge(o.lo, o.ro)
        return o

    @staticmethod
    def merge(lo: "Node", ro: "Node") -> int: # 返回维护的值/更复杂的维护对象
        left_sm = lo.sm if lo else 0
        right_sm = ro.sm if ro else 0
        return left_sm + right_sm

    def add(self, i, val) -> None:
        l, r, lo, ro = self.l, self.r, self.lo, self.ro
        if self.l == self.r:
            self.sm += val
            return

        mid = (self.l + self.r) // 2
        if i <= mid:
            if self.lo is None:
                self.lo = Node(l, mid)
            self.lo.add(i, val)
        if mid+1 <= i:
            if self.ro is None:
                self.ro = Node(mid+1, r)
            self.ro.add(i, val)
        self.sm = Node.merge(self.lo, self.ro)

    def query(self, L, R) -> int:
        l, r, lo, ro = self.l, self.r, self.lo, self.ro
        if L <= self.l and self.r <= R:
            return self.sm

        res = 0
        mid = (self.l + self.r) // 2
        if L <= mid:
            if self.lo is None:
                self.lo = Node(l, mid)
            res += self.lo.query(L,R)
        if mid + 1 <= R:
            if self.ro is None:
                self.ro = Node(mid + 1, r)
            res += self.ro.query(L,R)
        return res

def test():
    # 测试单点更新 区间查询线段树
    a = [1,3,2,4,5]
    tree = Node(0, 4)
    # tree.build(0, 4, a)
    for i in range(4):
        tree.add(i, a[i])

    for l in range(4):
        for r in range(l,4):
            assert sum(a[l:r+1]) == tree.query(l,r)
# test()



