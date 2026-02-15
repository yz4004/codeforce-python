"""
 单点更新线段树 + 维护复杂区间信息 + 维护最长连续相同字符子串

维护三种区间，卡左右端点/整段子区间上最长连续相同字符子串 （套打家劫舍模板）
[l...], [...] [...r]

"""
from typing import List


class SegmentTree:  # 单点更新，维护复杂区间信息
    def __init__(self, s):
        n = len(s)
        self.s = s
        # 要维护什么信息
        self.t = [[0, 0, 0] for _ in range(4 * n)]  # 整段，左端点起始 长度+字符，右侧端点起始, 字符则交给nums维护
        self.build(1, 0, n - 1)  # 初始化

    def build(self, p, l, r):
        # (p,l,r) parent 以及管辖区间
        if l == r:
            self.t[p] = [1, 1, 1] #单点信息
            return
        mid = (l + r) // 2
        self.build(2 * p, l, mid)
        self.build(2 * p + 1, mid + 1, r)
        self.pull(p, l, r)

    def pull(self, p, l, r):  # up
        # 子信息汇总p <- 2*p, 2*p+1
        # self.t[p] = self.t[2 * p] + self.t[2 * p + 1] # 更新sum

        # 将合并过程单独放进merge函数里，包装二元操作，因为merge在区间查询里也用得到
        self.t[p] = self.merge(self.t[2 * p], self.t[2 * p + 1], l, (l + r) // 2, r)
        # 假如查询任意子区间也可以


    def merge(self, left, right, l, mid, r): # merge函数维护复杂信息的区间合并逻辑
        # left/right = [最长连续，左起始最长，右起始最长]
        # 更复杂的合并左右区间逻辑；用在pull/query里 self.t[p] = self.t[2 * p] + self.t[2 * p + 1]

        # todo 复杂信息合并逻辑
        ############################################################
        ############################################################
        # [l, mid] [mid+1, r]
        lr = self.s[mid]  # [l,mid] 左右端点
        rl = self.s[mid + 1]  # [mid+1, r] 右左端点

        if lr == rl: #相等时考虑跨区间
            l = left[1] if left[1] < mid - l + 1 else left[1] + right[1]  # 左起，如果长度超过左区间，则加上右区间左侧
            m = left[2] + right[1]  # 中起
            r = right[2] if right[2] < r - mid else left[2] + right[2]  # 右起

            return [max(l, m, r, left[0], right[0]), l, r]  # 左中右 还有原本区间自带最大长度
        else:
            return [max(left[0], right[0]), left[1], right[2]]
        ############################################################
        ############################################################


    def update(self, p, l, r, i, v):
        # if L <= l and r <= R: 区间更新条件
        #     self.apply(p, l, r, v)
        #     return
        if l == r:  # 单点更新条件
            self.s[l] = v #只更新字母信息
            return

        mid = (l + r) // 2
        # self.push(p, l, r) #无分发懒信息
        if i <= mid:
            self.update(2 * p, l, mid, i, v)
        if mid < i:
            self.update(2 * p + 1, mid + 1, r, i, v)
        self.pull(p, l, r)

    def query(self, p, l, r, L, R):
        pass

class Solution:
    """
    LC 2213 https://leetcode.cn/problems/longest-substring-of-one-repeating-character/
    """
    def longestRepeating(self, s: str, queryCharacters: str, queryIndices: List[int]) -> List[int]:
        tree = SegmentTree([x for x in s])
        n = len(s)
        res = []
        for i, c in zip(queryIndices, queryCharacters):
            tree.update(1, 0, n - 1, i, c)
            res.append(tree.t[1][0])
        return res
