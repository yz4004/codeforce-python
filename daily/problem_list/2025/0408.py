"""
https://codeforces.com/problemset/problem/1791/F

输入 T(≤1e3) 表示 T 组数据。所有数据的 n 之和 ≤2e5，q 之和 ≤2e5。
每组数据输入 n q(1≤n,q≤2e5) 和长为 n 的数组 a(1≤a[i]≤1e9)。下标从 1 开始。
然后输入 q 个询问，格式如下：
"1 l r"：把下标在 [l,r] 中的数都更新成其数位和，例如 a[i]=420，更新成 a[i]=4+2+0=6。
"2 x"：输出 a[x]。


- 将a[l,r]中的 x => x的数位和，除了个位数都是单调递减
- 1357 => 1 + 5 + 3 + 7 每次更新是 logN, k次更新 k*logN, 最多更新不超过logN次
- 区间加1 单点查询 （lazy线段树维护区间和）然后查询每个点被更新多少次
- 因为是单向的 只会不断减小不会revert 所以查询时再a上原地更新即可，然后记录他被更新的次数
"""
import itertools
import sys
from math import inf, isqrt
from typing import List

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x


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



T = RI()
for _ in range(T):
    n, Q = RII()
    a = RILIST()
    tree = SegmentTreeSum(n, None)

    res = []
    for _ in range(Q):
        query = tuple(RII())
        if len(query) == 3:
            l,r = query[1]-1, query[2]-1
            tree.add(1, 0, n-1, l, r, 1)
        else:
            i = query[1]-1
            t = tree.query(1, 0, n-1, i, i)
            res.append((t,i))
            # 记录索引i应该被更新了t次，暂存，最后统一执行 t是单增的

    tmp = [0]*n # 记录索引i被更新多少次
    for t,i in res:
        x = a[i]
        while tmp[i] < t:
            # 进行一次数位和，知道tmp[i] -> t
            y = 0
            while x:
                y += x % 10
                x //= 10
            x = y
            tmp[i] += 1
        a[i] = x
        print(x)



# c++能通过
"""
#include <bits/stdc++.h>
using namespace std;

#define int long long
const int INF = 1e18;

class SegmentTreeSum {
public:
    vector<int> t, tag;
    int n;

    SegmentTreeSum(int n_, const vector<int>& nums = {}) {
        n = n_;
        t.assign(4 * n, 0);
        tag.assign(4 * n, 0);
        if (!nums.empty()) {
            build(1, 0, n - 1, nums);
        }
    }

    void build(int p, int l, int r, const vector<int>& nums) {
        if (l == r) {
            t[p] = nums[l];
            return;
        }
        int mid = (l + r) / 2;
        build(2 * p, l, mid, nums);
        build(2 * p + 1, mid + 1, r, nums);
        pull(p);
    }

    void pull(int p) {
        t[p] = t[2 * p] + t[2 * p + 1];
    }

    void apply(int p, int l, int r, int v) {
        t[p] += (r - l + 1) * v;
        tag[p] += v;
    }

    void push(int p, int l, int r) {
        if (tag[p]) {
            int v = tag[p];
            int mid = (l + r) / 2;
            apply(2 * p, l, mid, v);
            apply(2 * p + 1, mid + 1, r, v);
            tag[p] = 0;
        }
    }

    void add(int p, int l, int r, int L, int R, int v) {
        if (L <= l && r <= R) {
            apply(p, l, r, v);
            return;
        }
        push(p, l, r);
        int mid = (l + r) / 2;
        if (L <= mid) add(2 * p, l, mid, L, R, v);
        if (mid < R) add(2 * p + 1, mid + 1, r, L, R, v);
        pull(p);
    }

    int query(int p, int l, int r, int L, int R) {
        if (L <= l && r <= R) return t[p];
        push(p, l, r);
        int mid = (l + r) / 2;
        int res = 0;
        if (L <= mid) res += query(2 * p, l, mid, L, R);
        if (mid < R) res += query(2 * p + 1, mid + 1, r, L, R);
        return res;
    }
};

int digital_root(int x, int times) {
    while (times-- && x >= 10) {
        int y = 0;
        while (x) {
            y += x % 10;
            x /= 10;
        }
        x = y;
    }
    return x;
}

int32_t main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n, Q;
        cin >> n >> Q;
        vector<int> a(n);
        for (int& x : a) cin >> x;

        SegmentTreeSum tree(n);
        vector<int> tmp(n, 0);
        vector<pair<int, int>> res;

        while (Q--) {
            int type;
            cin >> type;
            if (type == 1) {
                int l, r;
                cin >> l >> r;
                l--, r--;
                tree.add(1, 0, n - 1, l, r, 1);
            } else {
                int i;
                cin >> i;
                i--;
                int t = tree.query(1, 0, n - 1, i, i);
                res.emplace_back(t, i);
            }
        }

        for (auto [t, i] : res) {
            int& x = a[i];
            int cnt = tmp[i];
            x = digital_root(x, t - cnt);
            tmp[i] = t;
            cout << x << '\n';
        }
    }

    return 0;
}

"""
