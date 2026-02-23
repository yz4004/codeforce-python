"""
https://codeforces.com/problemset/problem/1701/F

输入 q(1≤q≤2e5) 和 d(1≤d≤2e5)。
然后输入 q 个询问，每个询问输入 v(1≤x≤2e5)。

一开始，集合为空。
如果 v 不在集合中，那么把 v 加到集合中，否则把 v 从集合中删除。

定义美丽三元组 (x,y,z) 为满足 x < y < z 且 z - x ≤ d 的三元组。
对于每个询问，输出添加/删除 v 之后，集合中的美丽三元组个数。

1. 静态查询
x,y,z
    [z-d, z) - comb(c,2)

引入v
    [v-d,v) - c1 - comb(c1,2)

    [v+1,v+d] 中的 z 对应的 comb(c,2) -> comb(c+1,2)

    for z in [v+1,v+d]:
        c: cnt[z-d,z] += 1

        fz = comb(c,2) -> comb(c+1,2)

        c*(c-1)/2 -> (c+1)*c/2
        c2 - c/2 -> (c+1)2 - (c+1)/2 = c2 + c/2

        where c = cnt([z-d,z))

        即对区间 z [v+1,v+d] 里所有维护的 fz 每个人加一个c 但c不是常量，而是一个随z的函数 c(z) 即引入v前左侧d区间的计数

    c(z) = cnt([z-d,z)) 可以通过区间和/动态前缀和计算
    但是没加一次1 c就要重新计算 所以lazy tag不能直接叠加

    分别维护 c2, c
    c^2 -> (c+1)^2 -- 2*c+1
    c -> c+1 -- 1

    c^2 -> (c+1)^2 - (c+2)^2 - c^2+4c+4
    2c+1 4c+4 6c+9 8c+16
    tag=t
    tc + t^2

    c^2 - (c-1)^2 - (c-2)^2

    f_8 = 2^2, 2
    f_5 = 1^1, 1
3 5 8

"""
import itertools
import sys
from operator import add, xor
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

n, d = RII()
nums = RILIST()
class SegTree:
    def __init__(self, n, d):
        self.n = n
        self.d = d

        self.cnt = [0] * (4*n) # 区间内的点数
        self.s1 = [0] * (4*n)  # [l,r] sum(f_z = c*c - c)//2 = (s2[l,r]-s1[l,r])//2 -- s1/s2 只计入区间的活跃点
        self.s2 = [0] * (4*n)
        self.tag = [0] * (4 * n) # lazy tag

    #######################################
    def pull(self, p):           # ★ 回溯合并三者
        lc, rc = p<<1, p<<1|1
        self.cnt[p] = self.cnt[lc] + self.cnt[rc]
        self.s1[p]  = self.s1[lc]  + self.s1[rc]
        self.s2[p]  = self.s2[lc]  + self.s2[rc]

    def push(self, p):
        v = self.tag[p]
        if v:
            lc, rc = p<<1, p<<1|1
            self.apply(lc, v)
            self.apply(rc, v)
            self.tag[p] = 0

    # set v
    # 1.更新右侧 [v+1,v+d] 所有点z需要 c_z + 1
    # f_z = cz ^ 2 - cz
    #       cz2 = cz^2 => (cz+1)^2 = cz2 + 2*cz+1.
    #       (cz+t)^2 => cz2 + 2*t*cz + t^2
    # 2.同时enable v
    # f_v = cv ^ 2 - cv 这里cv是 [v-d,v) 计数
    def apply(self, p, v): # v [v+1,v+d] 区间懒加 1
        # v = 1/-1
        ct = self.cnt[p]  # [l,r] 的点数
        c = self.s1[p]

        self.s1[p] += ct * v
        self.s2[p] += 2*v*c + ct * v*v

        # self.cnt[p] += v
        self.tag[p] += v
    #######################################

    def set(self, v, enable):
        n, d = self.n, self.d
        if enable:
            # 1.设v
            cv = 0
            if 0 <= v-1:
                L,R = max_(v-d,0), v-1
                cv = self.query(1, 0, n-1, L,R)[0]
            self._set_v(1, 0, n-1, v, cv, True)

            # 2. 更新 [v+1,v+d] 里的z
            if v+1 <= n-1:
                L, R = v+1, min_(v+d,n-1)
                self._add(1, 0, n-1, L, R, 1)
        else:
            # 1. v重置为0
            self._set_v(1, 0, n-1, v, 0, False)

            # 2. 更新 [v+1,v+d] 里的z
            if v+1 <= n-1:
                L, R = v+1, min_(v+d, n-1)
                self._add(1, 0, n-1, L, R, -1)

    def _set_v(self, p, l, r, v, cv, enable):
        if l == r:
            self.cnt[p] = 1 if enable else 0
            self.s1[p] = cv if enable else 0
            self.s2[p] = cv * cv if enable else 0
            self.tag[p] = 0
            return
        mid = (l+r)//2
        self.push(p)
        if v <= mid:
            self._set_v(2*p, l, mid, v, cv, enable)
        elif mid < v:
            self._set_v(2*p+1, mid+1, r, v, cv, enable)
        # self.cnt[p] = self.cnt[2*p] + self.cnt[2*p+1]
        self.pull(p)


    def _add(self, p, l, r, L, R, v):
        if L > R or R < l or L > r: return
        if L <= l and r <= R:
            self.apply(p,v)
            return
        mid = (l + r) // 2
        self.push(p)
        self._add(2 * p, l, mid,        L, R, v)
        self._add(2 * p + 1, mid + 1, r, L, R, v)
        self.pull(p)

    def query(self, p, l, r, L, R):
        if L > R or R < l or L > r:
            return 0, 0, 0
        if L <= l and r <= R:
            return self.cnt[p], self.s1[p], self.s2[p]
        self.push(p)
        mid = (l + r) // 2
        c1, s11, s21 = self.query(2 * p, l, mid, L, R)
        c2, s12, s22 = self.query(2 * p + 1, mid + 1, r, L, R)
        # self.pull(p)
        return c1 + c2, s11 + s12, s21 + s22
    def answer(self):
        return (self.s2[1] - self.s1[1]) // 2   # Σ_active C(c(z),2)



m = 200005 #max(nums)+1
tree = SegTree(m+1, d)
seen = [False]*(m+1)
res = 0
for v in nums:
    v -= 1
    if seen[v]:
        seen[v] = cur = False
    else:
        seen[v] = cur = True

    tree.set(v, cur)
    print(tree.answer())
