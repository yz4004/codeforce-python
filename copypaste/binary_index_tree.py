from bisect import bisect_left
from math import inf
from typing import List



# 1. BIT 1-based
class BIT:  # 1-based

    def __init__(self, n): # [1,n]
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, i, delta): # a[i] += delta
        n = self.n
        tree = self.tree
        while i <= n:
            tree[i] += delta
            i += i & -i

    def prefix_sum(self, i): # [1, i]
        res = 0
        tree = self.tree
        while i > 0:
            res += tree[i]
            i -= i & -i
        return res

    def kth(self, k): # 1-base - k-base
        idx = 0
        bit = 1 << (self.n.bit_length() - 1)
        tree = self.tree
        while bit:
            nxt = idx + bit
            if nxt <= self.n and tree[nxt] < k:
                k -= tree[nxt]
                idx = nxt
            bit >>= 1
        return idx + 1

# 2. BIT_max
class BIT_max: #1-based
    def __init__(self, n: int):
        self.n = n
        self.tree = [-inf] * (n + 1)   # a
        self.arr = [-inf] * (n + 1)   # b (raw)

    def add(self, i: int, x: int):
        self.arr[i] = max(self.arr[i], x)
        while i <= self.n:
            self.tree[i] = max(self.tree[i], x)
            i += i & -i

    def pref_max(self, i: int) -> int:
        res = -inf
        while i > 0:
            res = max(res, self.tree[i])
            i -= i & -i
        return res

    def range_max(self, l: int, r: int) -> int:
        res = -inf
        while l <= r:
            lb = r & -r
            block_l = r - lb + 1
            if l <= block_l:
                res = max(res, self.tree[r])
                r = block_l - 1
            else:
                res = max(res, self.arr[r])
                r -= 1
        return res
"""
https://chatgpt.com/c/694ca794-73cc-832f-a32c-7702c9a3e241
"""


"""
3. 支持批预处理的BIT (坐标不是1-based)
"""
class BIT:
    # 树状数组维护前缀和 (1-base)
    # 单点更新 + 区间查询 + BIT二分
    # 所有入参坐标均对应原数组坐标
    # - 前缀查询 [:i] 前i个
    # - 区间查询 [l,r] 查询闭区间
    # - 二分查询 [:i] 最小的i使得前缀 [:i] >= target
    def __init__(self, n: int, nums: List = None):
        self.n = n
        self.a = [0] * (n + 1)
        # 启发式更新 i的父节点是 i + lb(i)
        if nums is not None:
            self.nums = nums
            for i, x in enumerate(nums, 1):
                self.a[i] += x
                pa = i + (i & -i)
                if pa <= n:
                    self.a[pa] += self.a[i]

    # nums[i] += x
    def add(self, i, x):
        i = i + 1
        a, n = self.a, len(self.a)
        while i < n:
            a[i] += x
            i += i & -i

    # 前缀查询 [:i] 前i个的和
    def sum(self, i: int):
        res = 0
        while i > 0:
            res += self.a[i]
            i -= i & -i
        return res

    # 区间查询 [l,r] 查询闭区间
    def rsum(self, l: int, r: int) -> int:
        return self.sum(r + 1) - self.sum(l)

    # 二分查询 [:i] 最小的i使得前缀 [:i] >= target （对比静态前缀和数组上二分）
    # 目标i=0b10110 对应从左向右要跳过的管辖区间, 我们从高位向低找 如果 0b10000 对应长度的和小于target就减去，初始枚举段长的n的最高比特位
    # 只有前缀和数组单调递增才能二分
    def lower_bound(self, target):
        # 返回最小 idx，使 self.sum(idx) >= target;
        step = 1 << (self.n.bit_length() - 1)  # 0b1011 取1<<3 = 0b1000
        i = 0  # 从虚节点开始，在位跳里维护的是已确定可以跳过的最大右端点 i，是上一轮跳过后的前缀右端点, [0,i] 计入到target里  sum(idx) < target
        while step:
            # i] [i + 1, i + step]
            # i是枚举过的最大右端点，初始是虚拟节点0，每次查看 [i+1:] step长的区间
            # step 指数下降，一开始从n的最高bit长度开始
            # 最后 step=1 [i+1, i+1] 如果不满足会被跳过，满足则不会被跳过，i+1 是下一个满足的点，输出
            if i + step <= self.n and self.a[i + step] < target:
                target -= self.a[i + step]
                i += step
            step = step >> 1
        return i + 1

    def lb(self, x):
        return x & -x


"""
树状数组维护前缀和
- 可差分信息 (可逆的结合交换群（Abelian group）加法、异或)
- n个节点，i 的管辖区间 [i-lb+1, i]
- i管理lb长度的信息包含 【i本人 + log(lb_i)个子节点】- 分别对应区间长度 1 2 4 ... 2^k 满足 1+2+...+2^k = lb(i) - 1
- i的父节点是 i + lb(i)， (根据i管理的子节点，一个子节点想变成父节点，需要移动lb(子节点)的长度)

- 单点更新，自底向上扩散; 
- 前置求和，自后向前的跳过管辖区间 i进行比特分解后 0b11001 从 lb_i 开始向左遍历管辖区间 至多logi个
- 前缀二分 对比[静态前缀和数组上二分]  从左向右尝试跳过管辖区间，每次从高位尝试跳过
    目标i=0b10110 对应从左向右要跳过的管辖区间, 我们从高位向低找 如果 0b10000 对应长度的和小于target就减去，初始枚举段长的n的最高比特位


不同于线段树的节点管理一段区间，子节点就是两个划分 - bit管理的子节点是 lb_i = 1 + 2 + ... 2^k 的划分 再加上i本人

参考:
https://chatgpt.com/c/6898970e-9798-8329-9a31-1eab42777b42
https://oi-wiki.org/ds/fenwick/#%E7%AE%A1%E8%BE%96%E5%8C%BA%E9%97%B4 （图）

视角:
    动态前缀和 (相比静态前缀和，动态前缀和支持修改前缀)
     - x轴/y轴 支持维护前缀的信息 <= t 的某个量. 如二维偏序
    频次技术
     - 一般只是值域 离散化 +- 1

两种用例：
    维护动态前缀和
    - 以原数组为位置轴，树状数组索引对应于原数组索引，维护前缀和
    
    值域 rank 树状数组/频次树状数组
    - 以值域空间为轴建BIT并维护频次+1，查询前缀和则变成rank统计（需对值域空间离散化）
    - 常见用例：
        维护逆序对, 维持值域空间的频次，add(v,+1/-1) 查询由x引入的逆序对 即为后缀和
        维护第k小，维持值域空间的频次，lower_bound(k) 查询使得前缀大于等于k的第一个元素
        滑窗中位数，同上，相当于 kth((m+1)/2)
    当问题在问有多少个数 ≤ x / 第 k 小时，把 BIT 的索引换成值，频次当作权重做前缀。
        
    总结: 
    位置轴：区间求和 → 想到“sum(r) - sum(l-1)”
    值域轴：个数/秩/第 k → 想到“rank(x) = sum(x)、kth = lower_bound(k)”

计算逆序对数量，两种方法
    1. merge sort计算交换的次数
    2. 树状数组维护值域空间，当出现值为k的数字在 nums[k] += 1
"""
def inverse_pair(a, M):
    # a 已离散化到 [1..M]...
    bit = BIT(M)
    ans = 0
    for v in reversed(a):
        ans += bit.sum(v-1)   # 右边比 v 小的个数
        bit.add(v, 1)         # 记录出现 v


def maintain_kth_smallest(a, M):
    # 动态集合 S，值域 [1..M]
    bit = BIT(M)
    def insert(x): bit.add(x, +1)
    def erase(x):  bit.add(x, -1)  # 保证频次不为负
    def rank(x):   return bit.sum(x)
    def kth(k):    return bit.lower_bound(k)  # 要求总频次 >= k

#################################################################
#################################################################
#################################################################

# 二维偏序问题
# 即点对 (x0,y0) <= (x1,y1) 定义为两个分量都满足 x0 <= x1 and y0 <= y1
# 固定一个维度排序，然后用有序结构/BIT 解决另一分量
# 逆序对本质也是二维偏序问题，(i,nums[i]) vs (j, nums[j]) -- https://zhuanlan.zhihu.com/p/112504092
# 一些三维偏序的应用题 - https://blog.csdn.net/EQUINOX1/article/details/136305243

def test(a): # [(x1,y1)...]
    # 计算满足二维偏序的点对数量
    # (x0,y0) <= (x1,y1) 定义为两个分量都满足 x0 <= x1 and y0 <= y1
    a.sort()
    bit = BIT(len(a))
    res = 0
    for _, y in a:
        res += bit.rsum(0, y-1)
        bit.add(y,1)
    print(res)

