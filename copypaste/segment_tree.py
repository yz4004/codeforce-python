import math
from math import inf
"""
更多模版参考
https://leetcode.cn/contest/weekly-contest-440/ranking/?region=local_v2 （第三题）

"""



##############################################################################
##############################################################################
# 线段树维护最小值 单点更新 区间查询
# LC3749 https://leetcode.cn/problems/fruits-into-baskets-iii/
# LC2940 找到 Alice 和 Bob 可以相遇的建筑
# ps 和是可差分信息，fenwick两次更新也可以做
class SegmentTreeMin:  # min
    def __init__(self, n, nums=None):
        self.t = [inf] * (4 * n)  # 维护的区间信息, 区间最小值对应初始值inf，可替换为更复杂的信息 （如打家劫舍）
        if nums:  # 如果有初始化数组输入，执行build逻辑
            assert n == len(nums)
            self.nums = nums
            self.build(1, 0, n - 1)  # 初始化build

    def build(self, p, l, r): # (p,l,r) parent 以及管辖区间
        if l == r:
            self.t[p] = self.nums[l]
            return
        mid = (l + r) // 2
        self.build(2 * p, l, mid)
        self.build(2 * p + 1, mid + 1, r)
        self.pull(p)

    ##############################################
    def pull(self, p):  # up 子信息汇总p <- 2*p, 2*p+1
        self.t[p] = min(self.t[2 * p], self.t[2 * p + 1]) # 更新min

    def apply(self, p, i, v): # 单点更新逻辑
        #self.t[p] = min(self.t[p], v) # 结合原有信息取min
        self.t[p] = v # 覆盖原有信息
    ##############################################

    def update_single(self, p, l, r, i, v):
        if l == i == r:
            self.apply(p, i, v) # 单点更新
            return
        mid = (l + r) // 2
        if i <= mid:
            self.update_single(2 * p, l, mid, i, v)
        if mid < i:
            self.update_single(2 * p + 1, mid + 1, r, i, v)
        self.pull(p)

    def query(self, p, l, r, L, R): # 查询 [L,R] 区间最小值
        if L <= l and r <= R:
            return self.t[p]
        res = math.inf
        mid = (l + r) // 2
        if L <= mid:
            res = min(res, self.query(2 * p, l, mid, L, R))
        if mid < R:
            res = min(res, self.query(2 * p + 1, mid + 1, r, L, R))
        return res

    def find_first_idx_smaller_than_v(self, p, l, r, v):  # 线段树二分，找到从左往右第一个小于等于v的索引
        if self.t[p] > v:  # (p,l,r) 维护区间最小值都大于v 跳过这段区间
            return -1
        if l == r:  # 找到自左往右第一个满足的索引
            return l

        mid = (l + r) // 2
        i = self.find_first_idx_smaller_than_v(2 * p, l, mid, v)
        if i == -1:
            i = self.find_first_idx_smaller_than_v(2 * p + 1, mid + 1, r, v)
        return i



##############################################################################
##############################################################################
# 线段树维护最小值 单点、区间修改 区间查询
class SegmentTreeMin:  # 单点、区间修改 区间查询
    def __init__(self, n, nums=None):
        self.t = [inf] * (4 * n)  # 维护的区间信息, 区间最小值对应初始值inf，可替换为更复杂的信息 （如打家劫舍）
        self.tag = [0] * (4 * n)  # 懒信息
        if nums:  # 如果有初始化数组输入，执行build逻辑
            assert n == len(nums)
            self.nums = nums
            self.build(1, 0, n - 1)  # 初始化build

    def build(self, p, l, r): # (p,l,r) parent 以及管辖区间
        if l == r:
            self.t[p] = self.nums[l]
            return
        mid = (l + r) // 2
        self.build(2 * p, l, mid)
        self.build(2 * p + 1, mid + 1, r)
        self.pull(p)

    ##############################################
    def pull(self, p):  # up/子信息汇总p <- 2*p, 2*p+1
        self.t[p] = min(self.t[2 * p], self.t[2 * p + 1])  # 更新min

    def push(self, p, l, r):  # down 通知树节点p 下发懒信息
        if self.tag[p]:
            v = self.tag[p]
            self.apply(2 * p, l, (l + r) // 2, v)  # 懒信息推给左
            self.apply(2 * p + 1, (l + r) // 2 + 1, r, v)  # 懒信息推给右
            self.tag[p] = 0  # 清空暂存的懒信息，已经下发

    def apply(self, p, l, r, v):  # 区间更新并下发懒信息
        # self.t[p] = min(self.t[p], v) 不覆盖原值，而且和前文信息叠加
        self.t[p] = v  # 覆盖原值
        self.tag[p] = v
    ##############################################

    def update_interval(self, p, l, r, L, R, v): # (p,l,r) 区间覆盖成v [L, R] = v 逻辑取决于apply
        if L <= l and r <= R:
            self.apply(p, l, r, v)  # 区间更新，停止递归并暂存懒信息（不要递归到空，否则失去懒更新意义)
            return
        mid = (l + r) // 2
        self.push(p, l, r)  # 递归左右之前，先分发懒信息
        if L <= mid:
            self.update_interval(2 * p, l, mid, L, R, v)
        if mid < R:
            self.update_interval(2 * p + 1, mid + 1, r, L, R, v)
        self.pull(p)

    def query(self, p, l, r, L, R): # (p,l,r) 区间查询 [L,R]
        if L <= l and r <= R:
            return self.t[p]
        res = math.inf
        mid = (l + r) // 2
        self.push(p, l, r)  # 递归左右之前，先分发懒信息，虽然不会更新，但查询部分左右区间也依赖本层懒信息
        if L <= mid:
            res = min(res, self.query(2 * p, l, mid, L, R))
        if mid < R:
            res = min(res, self.query(2 * p + 1, mid + 1, r, L, R))
        return res

    def find_first_idx_smaller_than_v(self, p, l, r, v):  # 线段树二分，找到从左往右第一个小于等于v的索引
        if self.t[p] > v:  # (p,l,r) 维护区间最小值都大于v 跳过这段区间
            return -1
        if l == r:  # 找到自左往右第一个满足的索引
            return l
        mid = (l + r) // 2
        self.push(p, l, r) # 下发懒信息
        i = self.find_first_idx_smaller_than_v(2 * p, l, mid, v)
        if i == -1:
            i = self.find_first_idx_smaller_than_v(2 * p + 1, mid + 1, r, v)
        return i




##############################################################################
##############################################################################
# 线段树维护最大 区间更新
# 线段树维护原数组 + 线段树二分查找左侧第一个大于v的索引 https://leetcode.cn/problems/fruits-into-baskets-iii/
# 线段树维护可叠加的最大值，可以区间加，但是维护的是最大值 LC3356 https://leetcode.cn/problems/zero-array-transformation-ii/
class SegmentTreeMax:  # max 支持区间修改(值覆盖)
    def __init__(self, n, nums=None):
        if nums:  # 如果有初始化数组输入，执行build逻辑
            assert n == len(nums)
            self.nums = nums
            self.t = [-inf] * (4 * n)  # 区间信息，区间最小值对应初始值inf，可替换为更复杂的信息 （如打家劫舍）
            self.tag = [0] * (4 * n)  # 懒信息
            self.build(1, 0, n - 1)  # 初始化build
        else:
            self.t = [-inf] * (4 * n)  # 维护的区间信息, 区间最小值对应初始值inf，可替换为更复杂的信息 （如打家劫舍）
            self.tag = [0] * (4 * n)  # 懒信息

    def build(self, p, l, r):
        # (p,l,r) parent 以及管辖区间
        if l == r:
            self.t[p] = self.nums[l]
            return
        mid = (l + r) // 2
        self.build(2 * p, l, mid)
        self.build(2 * p + 1, mid + 1, r)
        self.pull(p)

    ########################################
    def pull(self, p):  # up/子信息汇总p <- 2*p, 2*p+1
        self.t[p] = max(self.t[2 * p], self.t[2 * p + 1])  # 更新min

    def push(self, p, l, r):  # down 通知树节点p 下发懒信息
        if self.tag[p]:
            v = self.tag[p]
            self.apply(2 * p, l, (l + r) // 2, v)  # 懒信息推给左
            self.apply(2 * p + 1, (l + r) // 2 + 1, r, v)  # 懒信息推给右
            self.tag[p] = 0  # 清空暂存的懒信息，已经下发
            # 当有update操作自上而下准备更新区间p之前，先下发之前p暂存的懒信息 （本例懒信息只是要加的数值）

    def apply(self, p, l, r, v):  # 下发lazy信息，先更新节点信息，然后暂存懒信息，（不继续下发）
        # self.t[p] = max(self.t[p], v) 如何应用懒信息，取min是区间应用值，但不覆盖原值
        self.t[p] = v  # 直接区间覆盖值，适用本题，直接覆盖inf
        self.tag[p] = v
    ########################################

    def update(self, p, l, r, L, R, v):
        if L <= l and r <= R:  # 当(p,l,r) 为 [L, R] 子区间即停止递归，利用懒信息下发函数更新（不要递归到空，否则失去懒更新意义)
            self.apply(p, l, r, v)
            return
        mid = (l + r) // 2
        self.push(p, l, r)  # 递归左右之前，先分发懒信息
        if L <= mid:
            self.update(2 * p, l, mid, L, R, v)
        if mid < R:
            self.update(2 * p + 1, mid + 1, r, L, R, v)
        self.pull(p)

    def query(self, p, l, r, L, R):
        if L <= l and r <= R:
            return self.t[p]
        res = -inf
        mid = (l + r) // 2
        self.push(p, l, r)  # 递归左右之前，先分发懒信息，虽然不会更新，但查询部分左右区间也依赖本层懒信息
        if L <= mid:
            res = max(res, self.query(2 * p, l, mid, L, R))
        if mid < R:
            res = max(res, self.query(2 * p + 1, mid + 1, r, L, R))
        return res

    def update_single(self, i, v): # 仍然走区间更新逻辑
        # 将nums[i]覆盖为v
        n = len(self.nums)
        self.update(1, 0, n-1, i, i, v)

    def find_first_idx_greater_than_v(self, p, l, r, v):
        if self.t[p] < v: # 如果 (p,l,r) 最大值小于v 则跳过，我们找自左往右第一个大于v的索引
            return -1
        if l == r:
            return l

        mid = (l + r) // 2
        self.push(p, l, r)
        i = self.find_first_idx_greater_than_v(2 * p, l, mid, v)
        if i == -1:
            i = self.find_first_idx_greater_than_v(2 * p + 1, mid + 1, r, v)
        return i


##############################################################################
##############################################################################
# 线段树维护区间和 区间更新 区间查询

class SegmentTreeSum:  # sum
    def __init__(self, n, nums=None):
        self.t = [0] * (4 * n)  # 维护的区间信息, 区间最小值对应初始值inf，可替换为更复杂的信息 （如打家劫舍）
        self.tag = [0] * (4 * n)
        if nums:  # 如果有初始化数组输入，执行build逻辑
            assert n == len(nums)
            self.nums = nums
            self.build(1, 0, n - 1)  # 初始化build

    def build(self, p, l, r):
        # (p,l,r) parent 以及管辖区间
        if l == r:
            self.t[p] = self.nums[l]
            return
        mid = (l + r) // 2
        self.build(2 * p, l, mid)
        self.build(2 * p + 1, mid + 1, r)
        self.pull(p)

    #######################################
    def pull(self, p):  # up
        # 子信息汇总p <- 2*p, 2*p+1
        self.t[p] = self.t[2 * p] + self.t[2 * p + 1] # 更新sum


    def push(self, p, l, r):  # down 通知树节点p 下发懒信息
        if self.tag[p]:
            v = self.tag[p]
            self.apply(2 * p, l, (l + r) // 2, v)         # 懒信息推给左
            self.apply(2 * p + 1, (l + r) // 2 + 1, r, v) # 懒信息推给右
            self.tag[p] = 0 # 清空暂存的懒信息，已经下发
            # 当有update操作自上而下准备更新区间p之前，先下发之前p暂存的懒信息 （本例懒信息只是要加的数值）

    def apply(self, p, l, r, v):  # 下发lazy信息，先更新节点信息，然后暂存懒信息，（不继续下发）
        self.t[p] += (r - l + 1) * v
        self.tag[p] += v
    #######################################

    def add(self, p, l, r, L, R, v):
        # (p,l,r) [L, R] += v - 支持负数=减法
        if L <= l and r <= R: # 当(p,l,r) 为 [L, R] 子区间即停止递归，利用懒信息下发函数更新（不要递归到空，否则失去懒更新意义)
            self.apply(p, l, r, v)
            return
        mid = (l + r) // 2
        self.push(p, l, r) #递归左右之前，先分发懒信息
        if L <= mid:
            self.add(2 * p, l, mid, L, R, v)
        if mid < R:
            self.add(2 * p + 1, mid + 1, r, L, R, v)
        self.pull(p)

    def query(self, p, l, r, L, R):
        if L <= l and r <= R:
            return self.t[p]
        res = 0
        mid = (l + r) // 2
        self.push(p, l, r) #递归左右之前，先分发懒信息，虽然不会更新，但查询部分左右区间也依赖本层懒信息
        if L <= mid:
            res += self.query(2 * p, l, mid, L, R)
        if mid < R:
            res += self.query(2 * p + 1, mid + 1, r, L, R)
        return res


################# 动态开点 单点修改
class StNode:
    # 当做全局常量使用，视情况改成 float('-inf')、0 等
    default_val = 0
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
    def merge(a: int, b: int) -> int:
        # 如果是求最大值，就用 max；求和、求最小等都可以在这里改
        return max(a, b)

    def update(self, i: int, v: int):
        """
        在位置 i 上“插入”或“更新”一个值 v，效果是
          node.val = merge_info(old_val, v)
        """
        # 叶节点直接合并
        if self.l == self.r:
            self.val = StNode.merge(self.val, v)
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

    def query(self, ql: int, qr: int) -> int:
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


# —— 在模块顶端/全局部位，先构造并注册“空节点”哨兵 ——
StNode.empty = StNode()
StNode.empty.lo = StNode.empty
StNode.empty.ro = StNode.empty
# 其它字段不重要，empty.val 已默认为 default_val

def new_st_root(l: int, r: int) -> StNode:
    """
    构造一个代表区间 [l, r] 的根节点：
        root = new_st_root(min_value, max_value)
    """
    return StNode(l, r)

# 用例：
# 假设你要支持的值域是 [0, 10**9]：
root = new_st_root(0, 10**9)

# 更新：把位置 i 增加一个值 x
# root.update(i, x)

# 查询：[L, R] 范围内的最大值
# res = root.query(L, R)








##########################################
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

    __slots__ = ("n", "op", "e", "map", "comp", "id", "t", "tag", "nums")

    def __init__(self,
                 n: int,
                 op: Callable[[S,S], S], # op(a:S, b:S) -> S 合并两个维护值的运算
                 e: Callable[[], S], # provider 返回 S 单位元
                 mapping: Callable[[F, S, int], S], # lazy 下发
                 composition: Callable[[F, F], F],
                 id_: Callable[[], F],
                 nums: Optional[List[S]] = None,
                 ):
        self.n = n
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


    """
    | 需求                          | S（结点值）      | F（懒标记）                          | mapping(f, x, len)            | composition(f\_new, f\_old)                      | e()  | id()     |
    | --------------------------- | ----------- | ------------------------------- | ----------------------------- | ------------------------------------------------ | ---- | -------- |
    | 区间加、区间和                     | `int`（区间和）  | `int`（要加的值）                     | `x + f * len`                 | `f_new + f_old`                                  | `0`  | `0`      |
    | 区间加、区间最小值                   | `int`（区间最小） | `int`                           | `x + f`                       | `f_new + f_old`                                  | `+∞` | `0`      |
    | 区间赋值、区间和                    | `int`       | `Optional[int]`（None=无操作，v=赋值v） | `x if f is None else f * len` | `f_new if f_new is not None else f_old`（新赋值覆盖旧的） | `0`  | `None`   |
    | 仿射变换（乘加）、区间和                | `int`       | `(mul, add)`                    | `x * mul + add * len`         | `(m2, a2) ∘ (m1, a1) = (m2*m1, a2*m1 + a1)`      | `0`  | `(1, 0)` |
    | 区间取 min 限制（chmin）、区间和/最小值\* | 常为复杂结构      | `int`（上界）                       | 需要维护更多状态（如 max/次大/其个数）        | 需要按可下推条件合并                                       | 视实现  | 视实现      |

    """


# n,
# op: Callable[[S, S], S],
# e: Callable[[], S],
# mapping: Callable[[F, S, int], S],
# composition: Callable[[F, F], F],
# id_: Callable[[], F],
# nums

def make_range_add_sum(nums):
    # s: 区间和
    # f: 区间懒更新值 （区间每个人加f)
    n = len(nums)
    op = lambda x,y: x+y
    e = lambda: 0
    mappping = lambda f,x, length: length * f + x  # 应用懒更新值到区间和x
    id_ = lambda: 0
    composition = lambda f_new, f_old: f_new + f_old
    tree = SegTree(n, op, e, mappping, composition, id, nums)