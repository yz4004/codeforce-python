class SegmentTreeNode:
    # 动态开点线段树节点类，维护max，单点更新 区间查询
    DEFAULT_VAL = 0  # 若维护的max包含负数，改成 float("-inf")
    __slots__= "val", "l", "r", "lo", "ro"

    def __init__(self, l, r):
        self.l, self.r = l, r # 维护区间 [l,r]
        self.val = self.DEFAULT_VAL # 默认维护值
        self.lo =  self.ro = None # 子节点指针

    def pull(self):
        """维护当前节点的值"""
        self.val = self.merge(
            self.lo.val if self.lo else self.DEFAULT_VAL,
            self.ro.val if self.ro else self.DEFAULT_VAL
        )

    def merge(self, a, b):
        """合并两个区间的值，例如取最大值或求和"""
        return max(a, b)  # 可修改为 min(a, b) 或 a + b 视需求而定

    def update(self, i, val):
        """单点更新"""
        if self.l == self.r:
            self.val = self.merge(self.val, val)
            return

        mid = (self.l + self.r) // 2
        if i <= mid:
            if not self.lo:
                self.lo = SegmentTreeNode(self.l, mid)
            self.lo.update(i, val)
        else:
            if not self.ro:
                self.ro = SegmentTreeNode(mid + 1, self.r)
            self.ro.update(i, val)

        self.pull()  # 更新当前节点的值

    def query(self, l, r):
        """查询区间 [l, r] 的最大值"""
        if l > self.r or r < self.l:
            return self.DEFAULT_VAL  # 超出范围，返回默认值
        if l <= self.l and self.r <= r:
            return self.val  # 完全覆盖，直接返回

        left_val = self.lo.query(l, r) if self.lo else self.DEFAULT_VAL
        right_val = self.ro.query(l, r) if self.ro else self.DEFAULT_VAL
        return self.merge(left_val, right_val)
