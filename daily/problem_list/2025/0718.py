"""
https://codeforces.com/problemset/problem/295/E

输入 n(1≤n≤1e5) 和长为 n 的数组 a(-1e9≤a[i]≤1e9)。

然后输入 m(1≤m≤1e5) 和 m 个询问，格式如下：
"1 i x"：把 a[i] 增加 x。(1≤i≤n，-1e3≤x≤1e3)
"2 L R"：输出所有满足 L ≤ a[i] ≤ a[j] ≤ R 的 a[j] - a[i] 之和。(-1e9≤L≤R≤1e9)
保证任意时刻 a 中都没有重复元素。


原数组的空间信息其实不重要，查询只针对值域。
目标和是应该考虑每个元素的贡献法：  [L,R] 中的数字 b1 ... bk 排序后 其在点对和的贡献与其分位有关 bi * (i-1) 作为正系数减别人  - bi * (k-i) 作为负系数被减
如果对值域建立线段树维护，则变成值域区间上的分治问题 每个区间首先维护区间内的目标值
区间合并，大区间首先加上两个子区间内部点对差和信息，再考虑点对分别来自两侧区间，因为左右区间已经有序，所以左区间都是负系数，右区间都是正系数，需要两侧区间cnt和总和

1. 开点线段树 动态维护区间
2. 离散化，先对所有未来可能的值都收集 + 离散化换成坐标 1-1e5 然后值是目标值
ref:
https://chatgpt.com/c/687c3078-acc4-800a-91de-d510506ee149
"""

import sys
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x


class StNode:
    # 当做全局常量使用，视情况改成 float('-inf')、0 等
    default_val = (0, 0, 0) # (cnt, sum, val)
    empty = None  # 稍后会初始化为哨兵节点

    def __init__(self, l: int = None, r: int = None):
        # 区间 [l, r]
        self.l = l
        self.r = r
        # 左右孩子，初始指向哨兵
        self.lo = StNode.empty
        self.ro = StNode.empty
        # 维护的值
        self.val = StNode.default_val


    def pull(self):
        # 合并左右孩子的信息
        self.val = StNode.merge(self.lo.val, self.ro.val)

    @staticmethod
    def merge(a: List, b: List) -> List[int]:
        # 如果是求最大值，就用 max；求和、求最小等都可以在这里改
        # return max(a, b)

        # [b1 ... bj] [bj+1 ... bk] 值域有序，
        # 区间合并，区间首先维护内部点对差和信息，在考虑点对分别来自两侧区间，因为左右区间已经有序，所以左区间都是负系数，右区间都是正系数，需要两侧区间cnt和总和
        cnt_a, sum_a, val_a = a
        cnt_b, sum_b, val_b = b
        cross = - sum_a * cnt_b + sum_b * cnt_a + val_a + val_b
        return [cnt_a + cnt_b, sum_a + sum_b, cross]

    def update(self, i: int, v: int):
        """
        在位置 i 上“更新”一个值 v，效果是
          node.val = merge_info(old_val, v)
        """
        # 叶节点直接合并
        if self.l == self.r:
            self.val = StNode.merge(self.val, [1, v, 0])
            return

        mid = (self.l + self.r) >> 1
        # 动态开点
        if i <= mid:
            if self.lo is StNode.empty:
                self.lo = StNode(self.l, mid)
            self.lo.update(i, v)
        else:
            if self.ro is StNode.empty:
                self.ro = StNode(mid + 1, self.r)
            self.ro.update(i, v)

        # 回溯时维护当前节点
        self.pull()

    # 清除i的元素
    def delete(self, i):
        if self.l == self.r:
            self.val = self.default_val
            return
        mid = (self.l + self.r) >> 1
        # 动态删点
        if i <= mid:
            if self.lo is not StNode.empty:
                self.lo.delete(i)
        elif mid < i:
            if self.ro is not StNode.empty:
                self.ro.delete(i)

        # 回溯时维护当前节点
        self.pull()

    def query(self, ql: int, qr: int) -> List[int]:
        """
        查询区间 [ql, qr] 上的 merge_info 结果。
        """
        # 与当前节点区间不相交
        if self is StNode.empty or ql > self.r or qr < self.l:
            return StNode.default_val
        # 完全包含
        if ql <= self.l and self.r <= qr:
            return self.val
        # 部分重叠，向下分解
        left_val = self.lo.query(ql, qr)
        right_val = self.ro.query(ql, qr)
        return StNode.merge(left_val, right_val)


# —— 一定要在这里初始化哨兵 ——
StNode.empty = StNode()
StNode.empty.lo = StNode.empty
StNode.empty.ro = StNode.empty
StNode.empty.val = StNode.default_val

root = StNode(-10**9, 10**9)
n, nums = RI(), RILIST()
for x in nums:
    root.update(x, x)

for _ in range(RI()):
    q = tuple(RII())
    if q[0] == 1:
        i, x = q[1]-1, q[2]
        # 把 a[i] 增加 x
        root.delete(nums[i])
        nums[i] += x
        root.update(nums[i], nums[i])

    else:
        l, r = q[1], q[2]
        # L ≤ a[i] ≤ a[j] ≤ R 的 a[j] - a[i] 之和
        print(root.query(l, r)[2])






