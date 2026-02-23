"""
https://codeforces.com/problemset/problem/2014/F

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) c(1≤c≤1e9) 和长为 n 的数组 a(-1e9≤a[i]≤1e9)。
然后输入一棵无向树的 n-1 条边，节点编号从 1 到 n。节点 v 的点权为 a[v]。

你可以标记树上的一些点。
每当你标记一个点 v，就把 v 的所有邻居的点权都减少 c。注意一个节点的点权可以被多次减少。

输出你标记的节点的点权的最大和。
比如 n=2，如果两个节点都标记，那么互相把对方的点权减 c，答案为 a[1] + a[2] - c * 2。

树形dp + 状态机，当前节点选或不选
- 当前节点选或不选是context，同时对子节点的决定由当前做出，则子节点不用再考虑父节点状态
"""
import sys
from functools import cache

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

def solve(c, g, a):
    # 根节点选或不选
    @cache
    def dfs(i, p, marked):
        # marked - 当前节点选或不选 （父节点p在决定选当前节点时已经扣除了对p的影响，假设p不存在，只关注该子树）
        res = 0
        for j in g[i]:
            if j == p: continue
            # 如果当前节点已选，如选子节点，则子节点和当前节点同时-c
            # 如果当前节点已选，如不选子节点，则都不减c
            # 如果没选当前节点，如选子节点，则无人减c
            res += max(dfs(j, i, False), dfs(j, i, True) - (2*c if marked else 0))
        if marked:
            res += a[i]
        return res
    return max(dfs(0, -1, False), dfs(0, -1, True))


T = RI()
for _ in range(T):
    n,c = RII()
    w = RILIST()
    g = [[] for _ in range(n)]
    for _ in range(n-1):
        a,b = RII()
        g[a-1].append(b-1)
        g[b-1].append(a-1)
    print(solve(c, g, w))


""" c++ 应该用数组记忆化
#include <iostream>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <tuple>

using namespace std;

typedef long long ll;

typedef tuple<int, int, bool> State;
struct TupleHash {
    template <typename T1, typename T2, typename T3>
    size_t operator()(const tuple<T1, T2, T3>& t) const {
        auto [a, b, c] = t;
        return hash<T1>()(a) ^ (hash<T2>()(b) << 1) ^ (hash<T3>()(c) << 2);
    }
};

unordered_map<State, ll, TupleHash> memo;

ll dfs(int i, int p, bool marked, ll c, const vector<vector<int>> &g, const vector<ll> &a) {
    State state = make_tuple(i, p, marked);
    if (memo.count(state)) return memo[state];

    ll res = 0;
    for (int j : g[i]) {
        if (j == p) continue;
        res += max(dfs(j, i, false, c, g, a), dfs(j, i, true, c, g, a) - (marked ? 2 * c : 0));
    }
    if (marked) res += a[i];

    return memo[state] = res;
}

ll solve(ll c, const vector<vector<int>> &g, const vector<ll> &a) {
    memo.clear();
    return max(dfs(0, -1, false, c, g, a), dfs(0, -1, true, c, g, a));
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        int n;
        ll c;
        cin >> n >> c;
        vector<ll> w(n);
        for (int i = 0; i < n; ++i) {
            cin >> w[i];
        }
        vector<vector<int>> g(n);
        for (int i = 0; i < n - 1; ++i) {
            int a, b;
            cin >> a >> b;
            --a, --b;
            g[a].push_back(b);
            g[b].push_back(a);
        }
        cout << solve(c, g, w) << '\n';
    }
    return 0;
}

"""