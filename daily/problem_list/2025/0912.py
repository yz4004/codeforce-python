"""
https://codeforces.com/problemset/problem/121/E

输入 n(1≤n≤1e5) m(1≤m≤1e5) 和长为 n 的数组 a(1≤a[i]≤1e4)。下标从 1 开始。
然后输入 m 个询问，格式如下：
"add L R d"：把 a 中下标在 [L,R] 中的元素都增加 d(1≤d≤1e4)。保证增加后元素始终 ≤1e4。
"count L R"：输出 a 中下标在 [L,R] 中的幸运元素的个数。幸运元素是只包含 4 或者 7 的数，例如 47,744,4 是幸运数，而 5,17,467 不是。

"""
import sys
from bisect import bisect_left
from collections import defaultdict
from math import inf
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7


N = 10**4
lucks = [0]
s = 0
for i in range(4):
    # 2^i, 2 4 8 16
    for j in range(s, s+(1<<i)):
        x = lucks[j]
        lucks.append(x * 10 + 4)
        lucks.append(x * 10 + 7)
    s += 1<<i

class SegmentTree:  # sum
    def __init__(self, n, nums=None):
        self.t = [None for _ in range(4*n)]  # (min_gap, min_cnt, x, res)
        self.tag = [0] * (4 * n)
        if nums:
            assert n == len(nums)
            self.nums = nums
            self.build(1, 0, n - 1)

    def build(self, p, l, r):
        nums = self.nums
        # (p,l,r) parent 以及管辖区间
        if l == r:
            self.t[p] = SegmentTree.apply(nums[l])
            return
        mid = (l + r) // 2
        self.build(2 * p, l, mid)
        self.build(2 * p + 1, mid + 1, r)
        self.pull(p)

    #######################################
    @staticmethod
    def apply(x) -> List[int]:  # (min_gap, min_cnt, x, res)
        j = bisect_left(lucks, x)
        if j == len(lucks):
            return [inf, 1, x, 0]
        else:
            d = lucks[j] - x
            return [d, 1, x, 1 if d == 0 else 0]

    def push(self, p):
        if self.tag[p]:
            v = self.tag[p]
            for c in (2*p, 2*p+1):
                self.tag[c] += v
            self.tag[p] = 0

    def pull(self, p):  # up
        self.t[p] = self.merge(self.t[2 * p], self.t[2 * p + 1])

    def merge(self, t1, t2):  # (min_gap, min_cnt, x, res)
        m = mn(t1[0], t2[0])
        cnt = sum(t[1] for t in (t1, t2) if t[0] == m)
        res = t1[3] + t2[3]
        return [m, cnt, -1, res]
    #######################################

    def add(self, p, l, r, L, R, v):
        # print((p,l,r,L,R), self.tag[p], v, self.t[p][0])
        if L <= l and r <= R and self.tag[p] + v < self.t[p][0]:
            self.tag[p] += v
            return
        elif l == r:
            # v >= self.t[p][0]
            x = self.t[p][2] + self.tag[p] + v
            self.tag[p] = 0
            self.t[p] = SegmentTree.apply(x)
            self.nums[l] = x
            return

        self.push(p)
        mid = (l + r) // 2
        if L <= mid:
            self.add(2 * p, l, mid, L, R, v)
        if mid < R:
            self.add(2 * p + 1, mid + 1, r, L, R, v)
        self.pull(p)

    def query(self, p, l, r, L, R):
        if L <= l and r <= R and self.tag[p] < self.t[p][0]:
            return self.t[p]
        elif l == r:
            x = self.t[p][2] + self.tag[p]
            self.tag[p] = 0
            self.t[p] = SegmentTree.apply(x)
            self.nums[l] = x
            return self.t[p]

        self.push(p)
        mid = (l + r) // 2

        # if L <= mid:
        #     res += self.query(2 * p, l, mid, L, R)
        # if mid < R:
        #     res += self.query(2 * p + 1, mid + 1, r, L, R)

        if R <= mid:
            return self.query(2 * p, l, mid, L, R)
        elif mid + 1 <= L:
            return self.query(2 * p + 1, mid + 1, r, L, R)


        res1 = self.query(2 * p, l, mid, L, R)
        res2 = self.query(2 * p + 1, mid + 1, r, L, R)
        return self.merge(res1, res2)


n, m = RII()
a = RILIST()
tree = SegmentTree(n, a)
res = ""
q_raw = ""
for _ in range(m):
    raw = RS()
    q = raw.split()
    # q_raw += raw
    # print(_, raw)
    if q[0] == "count":
        l, r = map(int, q[1:])
        l, r = l-1, r-1
        res += str(tree.query(1, 0, n-1, l, r)[-1]) + "\n"

    else:
        l, r, d = map(int, q[1:])
        l, r = l-1, r-1
        tree.add(1, 0, n-1, l, r, d)
        print(q)
        print(tree.nums, sum(all(c == "4" or c == "7" for c in str(x)) for x in tree.nums))

#print(q_raw)
print(res)


# --------------------------------------
# --------------------------------------
# --------------------------------------
# --------------------------------------


"""
https://codeforces.com/problemset/problem/121/E

输入 n(1≤n≤1e5) m(1≤m≤1e5) 和长为 n 的数组 a(1≤a[i]≤1e4)。下标从 1 开始。
然后输入 m 个询问，格式如下：
"add L R d"：把 a 中下标在 [L,R] 中的元素都增加 d(1≤d≤1e4)。保证增加后元素始终 ≤1e4。
"count L R"：输出 a 中下标在 [L,R] 中的幸运元素的个数。幸运元素是只包含 4 或者 7 的数，例如 47,744,4 是幸运数，而 5,17,467 不是。

"""
import sys
from bisect import bisect_left
from collections import defaultdict
from math import inf
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7


MAXV, INF = 10_000, 10**9

# 预生成 ≤1e4 的幸运数并排序（恰好 30 个）
lucks = []
def dfs(x=0):
    if x > MAXV: return
    if x: lucks.append(x)
    dfs(x*10+4); dfs(x*10+7)
dfs(); lucks.sort()

def next_lucky_ge(x):
    i = bisect_left(lucks, x)
    return lucks[i] if i < len(lucks) else INF

class Seg:
    # 节点维护: mn(区间D最小值), cnt(=mn的出现次数), add(懒：D已被减去的量)
    def __init__(self, A):
        n = len(A); self.n = n
        self.mn  = [0]*(4*n)
        self.cnt = [0]*(4*n)
        self.add = [0]*(4*n)
        self.ceil = [0]*n          # 仅叶子：当前“下一幸运数”
        self.build(1,0,n-1,A)

    def build(self,p,l,r,A):
        if l==r:
            c = next_lucky_ge(A[l]); self.ceil[l] = c
            self.mn[p] = c - A[l] if c < INF else INF
            self.cnt[p]= 1
            return
        m=(l+r)//2
        self.build(p*2,l,m,A); self.build(p*2+1,m+1,r,A)
        self.pull(p)

    def pull(self,p):
        lm, rm = self.mn[p*2], self.mn[p*2+1]
        self.mn[p] = lm if lm <= rm else rm
        self.cnt[p]= (self.cnt[p*2]   if lm==self.mn[p] else 0) \
                   + (self.cnt[p*2+1] if rm==self.mn[p] else 0)

    def apply(self,p,d):   # 整段 D -= d
        self.mn[p] -= d
        self.add[p]+= d

    def push(self,p):
        if self.add[p]:
            v = self.add[p]
            self.apply(p*2, v)
            self.apply(p*2+1, v)
            self.add[p] = 0

    # 区间加 A += d  ->  区间 D -= d
    def range_add(self,p,l,r,L,R,d):
        if R<l or r<L: return
        if L<=l and r<=R and d <= self.mn[p]:   # 允许等号：恰好把 mn 拉到 0
            self.apply(p,d)
            return
        if l==r:
            # 到叶子：把 d（以及沿路 push 后的 add 已体现在 mn 里）一次算进 A，重建 D
            curD = self.mn[p] - d               # 当前真实 D
            curA = self.ceil[l] - curD          # 反推出真实 A
            c = next_lucky_ge(curA)
            self.ceil[l] = c
            self.mn[p] = c - curA if c<INF else INF
            self.add[p]= 0
            return
        self.push(p)
        m=(l+r)//2
        self.range_add(p*2,  l,   m, L, R, d)
        self.range_add(p*2+1,m+1, r, L, R, d)
        self.pull(p)

    # 返回 [L,R] 的 (mn, cnt)
    def query_pair(self,p,l,r,L,R):
        if R<l or r<L: return (INF, 0)
        if L<=l and r<=R: return (self.mn[p], self.cnt[p])
        self.push(p)
        m=(l+r)//2
        lm, lc = self.query_pair(p*2,  l,   m, L, R)
        rm, rc = self.query_pair(p*2+1,m+1, r, L, R)
        mn  = lm if lm <= rm else rm
        cnt = (lc if lm==mn else 0) + (rc if rm==mn else 0)
        return (mn, cnt)

    def query_count(self,L,R):
        mn, cnt = self.query_pair(1,0,self.n-1,L,R)
        return cnt if mn==0 else 0

# ---- I/O ----
n, m = RII()
A = RILIST()
seg = Seg(A)

out = []
for _ in range(m):
    q = RS().split()
    if q[0] == 'add':
        l, r, d = map(int, q[1:])
        seg.range_add(1,0,n-1,l-1,r-1,d)
    else:
        l, r = map(int, q[1:])
        out.append(str(seg.query_count(l-1,r-1)))
print("\n".join(out))

