from typing import List
mod = 10 ** 9 + 7
"""
单点更新线段树 + 维护复杂区间信息 + 打家劫舍（有限制的子序列）

维护四种形态区间信息
[], [), (], ()
 （打家劫舍，不相邻最大子数列信息，子区间也是类似逻辑）
"""

class SegmentTree:  # 单点更新，维护复杂区间信息
    def __init__(self, nums):
        n = len(nums)
        self.nums = nums
        # self.t = [0] * (4 * n)  # 区间信息，本例保存区间和，可以替换为更复杂的信息
        # 1. 将所有需要维护的情况平铺列出
        # self.tm = [0] * (4 * n)  # 区间max子数组和
        # self.tl = [0] * (4 * n)  # 左端点 (l,r]
        # self.tr = [0] * (4 * n)  # 右端点 [l,r)
        # self.to = [0] * (4 * n)  # 开区间 (l,r)

        # 2. 将所有信息合并到t上，所有区间段维护的信息都在 t[p] 中 t[p][0 1 2 3] 对应上述tm tl tr to
        self.t = [[0,0,0,0] for _ in range(4 * n)]

        self.build(1, 0, n - 1)  # 初始化

    def build(self, p, l, r):
        # (p,l,r) parent 以及管辖区间
        if l == r:
            # self.tm[p] = self.nums[l]
            self.t[p][0] = self.nums[l]
            return
        mid = (l + r) // 2
        self.build(2 * p, l, mid)
        self.build(2 * p + 1, mid + 1, r)
        self.pull(p, l, r)

    def pull(self, p, l, r):  # up
        # 子信息汇总p <- 2*p, 2*p+1
        # self.t[p] = self.t[2 * p] + self.t[2 * p + 1] # 更新sum

        # 2. 将合并过程单独放进merge函数里，包装二元操作，因为merge在区间查询里也用得到
        self.t[p] = self.merge(self.t[2*p], self.t[2*p+1])

        # 1. 按照初始思路，将平铺信息合并，四种区间，tm不考虑边界的子序列最大值; tl (l,r] 区间子序列最大值; tr [l,r);  to (l,r)
        # # [l, mid] [mid+1, r]
        # self.tm[p] = max(self.tr[2*p] + self.tm[2*p+1], self.tm[2*p] + self.tl[2*p+1]) # [l,mid] (mid+1, r], [l,mid) [mid+1, r]
        # self.tl[p] = max(self.tl[2*p] + self.tl[2*p+1], self.to[2*p] + self.tm[2*p+1]) # (l,mid] (mid+1, r], (l,mid) [mid+1, r]
        # self.tr[p] = max(self.tr[2*p] + self.tr[2*p+1], self.tm[2*p] + self.to[2*p+1]) # [l,mid] [mid+1, r), [l,mid] (mid+1, r)
        # self.to[p] = max(self.tl[2*p] + self.to[2*p+1], self.to[2*p] + self.tr[2*p+1]) # (l,mid) [mid+1, r), (l,mid] (mid+1, r)

    def merge(self, left, right):
        # 更复杂的合并左右区间逻辑；用在pull/query里 self.t[p] = self.t[2 * p] + self.t[2 * p + 1]
        # [l, mid] [mid+1, r]
        tm1, tl1, tr1, to1 = left
        tm2, tl2, tr2, to2 = right

        tm = max(tr1 + tm2, tm1 + tl2)
        tl = max(tl1 + tl2, to1 + tm2)  # (l,mid] [mid+1, r]
        tr = max(tr1 + tr2, tm1 + to2)  # [l,mid] [mid+1, r)
        to = max(tl1 + to2, to1 + tr2)  # (l,mid] [mid+1, r)
        return [tm, tl, tr, to]

    def update(self, p, l, r, i, v):
        # if L <= l and r <= R: 区间更新条件
        #     self.apply(p, l, r, v)
        #     return
        if l == r:  # 单点更新条件
            # self.tm[p] = v  # 注意tm内是区间编号p
            self.t[p][0] = v
            return

        mid = (l + r) // 2
        # self.push(p, l, r) #无分发懒信息
        if i <= mid:
            self.update(2 * p, l, mid, i, v)
        if mid < i:
            self.update(2 * p + 1, mid + 1, r, i, v)
        self.pull(p, l, r)

    def query(self, p, l, r, L, R):
        if L <= l and r <= R:
            return self.t[p]
        mid = (l + r) // 2
        # self.push(p, l, r) #无分发懒信息

        left = [0]*4
        right = [0]*4
        if L <= mid:
            left = self.query(2 * p, l, mid, L, R)
        if mid < R:
            right = self.query(2 * p + 1, mid + 1, r, L, R)
        return self.merge(left, right) #区间查询合并左右信息，也需要合并操作



class Solution_3165:
    # LC3165:  https://leetcode.cn/problems/maximum-sum-of-subsequence-with-non-adjacent-elements/description/?envType=daily-question&envId=2024-10-31
    def maximumSumSubsequence(self, nums: List[int], queries: List[List[int]]) -> int:
        tree = SegmentTree(nums)
        ans = 0
        n = len(nums)
        for i, v in queries:
            tree.update(1, 0, n - 1, i, v)
            # ans = (ans + max(tree.tm[1], 0)) % mod  # 允许空数组
            ans = (ans + max(tree.t[1][0], 0)) % mod  # 允许空数组
        return ans



from typing import Callable, Generic, List, Optional, TypeVar

S = TypeVar("S") # segment value
F = TypeVar("F") # lazy tag type
class SegTree(Generic[S, F]):
    """
    op(a,b) -> S             :合并两个维护值的逻辑
    e() -> S                 :op 的单位元 （线段树 维护数据的单位元）
    mapping(f:F, x:S, length:int) -> S :将lazy tag f 下发到值x 长length的区间
    composite(f_new, f_old) : f_new . f_old 函数符合，在f_old的基础上符合 f_new
    id() -> F :懒更新值的单位元

            懒信息，维护信息
    单位元     id     e
    内部复合   comp   op
    懒信息施加   mapping
    """


    def __init__(self,
                 n: int,
                 op: Callable[[S,S], S], # op(a:S, b:S) -> S 合并两个维护值的运算
                 e: Callable[[], S], # provider 返回 S 单位元
                 mapping: Callable[[F, S, int], S], # lazy 下发
                 composition: Callable[[F, F], F],
                 id_: Callable[[], F],
                 nums: Optional[List[S]] = None,
                 ):
        ##############
        self.e = 0
        self.id_ = 0

        ##############
        self.n = n
        self.t = [self.e] * (4*n)

        self.op = op
        self.e = e
        self.map = mapping
        self.comp = composition
        self.id_ = id_
        self.t: List[S] = [e()] * (4 * n)
        self.tag: List[F] = [id_()] * (4 * n)
        if nums is not None:
            assert len(nums) == n
            self.nums = nums
            self._build(1, 0, n-1)

    # 合并两个t内信息
    @staticmethod
    def op(x, y):
        return x + y

    # 合并两个tag内懒信息
    @staticmethod
    def composite(f_old, f_new):
        return f_old + f_new
    # 区间加法 l_old + l_new
    # 区间复制 l_new
    # 放射变换 l=(mul, add) => (m2, a2) * (m1, a1) = (m1*m2, m2*a1+a2)
    #         x -> m1*x+a1 -> m2*(m1*x+a1) + a1 = m1*m2*x + a1*m2+a1

    # 给区间施加懒信息，更新当前区间被操作后的值 t[p], 暂存懒信息tag[p] 暂缓向下操作. (懒信息是没有向下传导的信息，而当前区间已经被其更新)
    @staticmethod
    def mapping(f, x, length):
        return


    def _build(self, p: int, l: int, r: int) :
        if l == r:
            self.t[p] = self.nums[l]
            return
        mid = (l + r) // 2
        self._build(p << 1, l, mid)
        self._build(p << 1 | 1, mid + 1, r)
        self._pull(p)

    # ---------- internal ----------
    def _pull(self, p: int) -> None:
        self.t[p] = self.op(self.t[2*p], self.t[2*p+1])                 # ************ op/merge

    def _apply(self, p:int, l:int, r:int, f:F) -> None:
        # 来自父节点的懒信息f:F 被施加到当前节点p
        self.t[p] = self.map(f, self.t[p], r-l+1) # map 将懒信息更新到 t[p] ************** mapping
        self.tag[p] = self.comp(f, self.tag[p])   # 懒信息复合             ************** composite

    def _push(self, p:int, l:int, r:int) -> None:
        f = self.tag[p]
        if f != self.id_():
            mid = (l+r)//2
            self._apply(p << 1, l, mid, f)
            self._apply(p << 1 | 1, mid + 1, r, f)
            self.tag[p] = self.id_() # 懒信息单位元

    # ---------- public ----------
    def range_apply(self, L: int, R: int, f: F) -> None:
        """ 区间更新 Apply lazy tag f to all i in [L, R]."""
        assert 0 <= L <= R < self.n
        self._range_apply(1, 0, self.n - 1, L, R, f)

    def _range_apply(self, p: int, l: int, r: int, L: int, R: int, f: F) -> None:
        if L <= l and r <= R:
            self._apply(p, l, r, f)
            return
        self._push(p, l, r)
        m = (l + r) // 2
        if L <= m:
            self._range_apply(p << 1, l, m, L, R, f)
        if m < R:
            self._range_apply(p << 1 | 1, m + 1, r, L, R, f)
        self._pull(p)

    def range_query(self, L: int, R: int) -> S:
        """ 区间查询 Query op over [L, R]."""
        assert 0 <= L <= R < self.n
        return self._range_query(1, 0, self.n - 1, L, R)

    def _range_query(self, p: int, l: int, r: int, L: int, R: int) -> S:
        if L <= l and r <= R:
            return self.t[p]
        self._push(p, l, r)
        m = (l + r) // 2
        res = self.e()
        if L <= m:
            res = self.op(res, self._range_query(p << 1, l, m, L, R))
        if m < R:
            res = self.op(res, self._range_query(p << 1 | 1, m + 1, r, L, R))
        return res

    def point_set(self, idx: int, value: S) -> None:
        """ 单点更新 Set a[idx] = value."""
        assert 0 <= idx < self.n
        self._point_set(1, 0, self.n - 1, idx, value)

    def _point_set(self, p: int, l: int, r: int, i: int, v: S) -> None:
        if l == r:
            self.t[p] = v
            self.tag[p] = self.id()
            return
        self._push(p, l, r)
        m = (l + r) // 2
        if i <= m:
            self._point_set(p << 1, l, m, i, v)
        else:
            self._point_set(p << 1 | 1, m + 1, r, i, v)
        self._pull(p)

    def point_query(self, idx: int) -> S:
        return self.range_query(idx, idx)

    def to_list(self) -> List[S]:
        """Materialize all values by querying each point (O(n log n))."""
        return [self.point_query(i) for i in range(self.n)]
