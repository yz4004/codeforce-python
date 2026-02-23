"""
https://atcoder.jp/contests/abc343/tasks/abc343_f

输入 n(1≤n≤2e5) q(1≤q≤2e5) 和长为 n 的数组 a(1≤a[i]≤1e9)。下标从 1 开始。
然后输入 q 个询问，格式如下：
"1 p x"：把 a[p] 改成 x(1≤x≤1e9)。
"2 l r"：输出 a 的子数组 [l,r] 中的严格次大值的个数。
注：严格次大值指不等于最大值的数中的最大值。

- 单点更新+区间查询 严格次大值的个数
- 同时维护最大，次大和次大的个数，汇总逻辑见merge/pull
"""
import sys
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

class SegmentTreeMax:  # max 支持区间修改(值覆盖)
    def __init__(self, nums):
        self.nums = nums
        self.mx = [-inf] * (4 * n)
        self.smx = [-inf] * (4 * n)

        self.mx_cnt = [0] * (4 * n)
        self.smx_cnt = [0] * (4 * n)

        self.build(1, 0, n - 1)  # 初始化build

    def build(self, p, l, r):
        # (p,l,r) parent 以及管辖区间
        if l == r:
            self.mx[p] = self.nums[l]
            self.mx_cnt[p] = 1
            return
        mid = (l + r) // 2
        self.build(2 * p, l, mid)
        self.build(2 * p + 1, mid + 1, r)
        self.pull(p)

    ########################################
    def pull(self, p):  # up/子信息汇总p <- 2*p, 2*p+1
        #self.t[p] = max(self.t[2 * p], self.t[2 * p + 1])  # 更新min
        cands = sorted(list(set([self.mx[2 * p], self.mx[2 * p + 1], self.smx[2 * p], self.smx[2 * p + 1]])))
        self.mx[p] = cands[-1]
        self.smx[p] = cands[-2]

        self.mx_cnt[p] = self.smx_cnt[p] = 0
        for t in (2*p, 2*p+1): # 注意mx[t]也可以贡献给smx，这个逻辑应该和下文的merge合并，都是信息汇总的逻辑
            if self.mx[t] == self.mx[p]:
                self.mx_cnt[p] += self.mx_cnt[t]

            if self.smx[t] == self.mx[p]:
                self.mx_cnt[p] += self.smx_cnt[t]

            if self.mx[t] == self.smx[p]:
                self.smx_cnt[p] += self.mx_cnt[t]

            if self.smx[t] == self.smx[p]:
                self.smx_cnt[p] += self.smx_cnt[t]

    def merge(self, left_mx, left_smx, right_mx, right_smx):  # up/子信息汇总p <- 2*p, 2*p+1
        mx_l, cmx_l = left_mx
        smx_l, csmx_l = left_smx
        mx_r, cmx_r= right_mx
        smx_r, csmx_r = right_smx

        cands = sorted(set([mx_l, mx_r, smx_l, smx_r]))
        mx, smx = cands[-1], cands[-2]
        cmx = csmx = 0
        for (k,v) in (left_mx, left_smx, right_mx, right_smx):
            if k == mx:
                cmx += v
            if k == smx:
                csmx += v
        return (mx, cmx), (smx, csmx)

    def apply(self, p, i, v):
        self.nums[i] = v
        self.mx[p] = v
    ########################################

    def update(self, p, l, r, i, v):
        if l == r:  # 当(p,l,r) 为 [L, R] 子区间即停止递归，利用懒信息下发函数更新（不要递归到空，否则失去懒更新意义)
            self.mx[p] = v
            return
        mid = (l + r) // 2
        if i <= mid:
            self.update(2 * p, l, mid, i, v)
        if mid < i:
            self.update(2 * p + 1, mid + 1, r, i, v)
        self.pull(p)

    def query(self, p, l, r, L, R):
        if L <= l and r <= R:
            return (self.mx[p], self.mx_cnt[p]), (self.smx[p], self.smx_cnt[p])
        mid = (l + r) // 2
        left_mx = right_mx = (-1, 0)
        left_smx = right_smx = (-inf, 0)
        if L <= mid:
            left_mx, left_smx = self.query(2 * p, l, mid, L, R)
        if mid < R:
            right_mx, right_smx = self.query(2 * p + 1, mid + 1, r, L, R)
        return self.merge(left_mx, left_smx, right_mx, right_smx)


n, q = RII()
a = RILIST()
tree = SegmentTreeMax(a)
res = []
for _ in range(q):
    tmp = tuple(RII())
    if tmp[0] == 1:
        p,x = tmp[1]-1, tmp[2]
        tree.update(1, 0, n-1, p, x)
    else:
        l,r = tmp[1]-1, tmp[2]-1
        _, smx = tree.query(1, 0, n-1, l, r)
        res.append(smx[1])

print("\n".join(map(str, res)))

# c++ 翻译
"""
#include <bits/stdc++.h>
using namespace std;

const int INF = INT_MAX;
int n, q;
vector<int> nums;

struct Node {
    int mx = -INF, smx = -INF;
    int mx_cnt = 0, smx_cnt = 0;
};

vector<Node> tree;

void pull(int p) {
    vector<int> cands = {tree[p * 2].mx, tree[p * 2 + 1].mx, tree[p * 2].smx, tree[p * 2 + 1].smx};
    sort(cands.begin(), cands.end());
    cands.erase(unique(cands.begin(), cands.end()), cands.end());

    tree[p].mx = cands.back();
    cands.pop_back();
    tree[p].smx = cands.empty() ? -INF : cands.back();

    tree[p].mx_cnt = tree[p].smx_cnt = 0;

    for (int t : {p * 2, p * 2 + 1}) {
        if (tree[t].mx == tree[p].mx)
            tree[p].mx_cnt += tree[t].mx_cnt;
        if (tree[t].smx == tree[p].mx)
            tree[p].mx_cnt += tree[t].smx_cnt;

        if (tree[t].mx == tree[p].smx)
            tree[p].smx_cnt += tree[t].mx_cnt;
        if (tree[t].smx == tree[p].smx)
            tree[p].smx_cnt += tree[t].smx_cnt;
    }
}

void build(int p, int l, int r) {
    if (l == r) {
        tree[p].mx = nums[l];
        tree[p].mx_cnt = 1;
        return;
    }
    int mid = (l + r) / 2;
    build(p * 2, l, mid);
    build(p * 2 + 1, mid + 1, r);
    pull(p);
}

void update(int p, int l, int r, int i, int v) {
    if (l == r) {
        tree[p].mx = v;
        tree[p].mx_cnt = 1;
        tree[p].smx = -INF;
        tree[p].smx_cnt = 0;
        return;
    }
    int mid = (l + r) / 2;
    if (i <= mid) update(p * 2, l, mid, i, v);
    else update(p * 2 + 1, mid + 1, r, i, v);
    pull(p);
}

pair<pair<int, int>, pair<int, int>> merge(
    pair<int, int> lm, pair<int, int> lsm,
    pair<int, int> rm, pair<int, int> rsm) {

    set<int> cands = {lm.first, lsm.first, rm.first, rsm.first};
    vector<int> v(cands.begin(), cands.end());
    sort(v.begin(), v.end());
    int mx = v.back(); v.pop_back();
    int smx = v.empty() ? -INF : v.back();

    int cmx = 0, csmx = 0;
    for (auto &[val, cnt] : {lm, lsm, rm, rsm}) {
        if (val == mx) cmx += cnt;
        if (val == smx) csmx += cnt;
    }
    return {{mx, cmx}, {smx, csmx}};
}

pair<pair<int, int>, pair<int, int>> query(int p, int l, int r, int L, int R) {
    if (L <= l && r <= R)
        return {{tree[p].mx, tree[p].mx_cnt}, {tree[p].smx, tree[p].smx_cnt}};

    int mid = (l + r) / 2;
    pair<int, int> lm = {-1, 0}, rm = {-1, 0};
    pair<int, int> lsm = {-INF, 0}, rsm = {-INF, 0};

    if (L <= mid)
        tie(lm, lsm) = query(p * 2, l, mid, L, R);
    if (mid < R)
        tie(rm, rsm) = query(p * 2 + 1, mid + 1, r, L, R);

    return merge(lm, lsm, rm, rsm);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> q;
    nums.resize(n);
    for (int i = 0; i < n; ++i) cin >> nums[i];

    tree.resize(4 * n);
    build(1, 0, n - 1);

    vector<int> res;
    while (q--) {
        int t;
        cin >> t;
        if (t == 1) {
            int p, x;
            cin >> p >> x;
            update(1, 0, n - 1, p - 1, x);
        } else {
            int l, r;
            cin >> l >> r;
            auto [mx, smx] = query(1, 0, n - 1, l - 1, r - 1);
            res.push_back(smx.second);
        }
    }

    for (int x : res) cout << x << '\n';

    return 0;
}

"""