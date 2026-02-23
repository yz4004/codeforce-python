"""
https://codeforces.com/problemset/problem/145/C

输入 n k(1≤k≤n≤1e5) 和长为 n 的数组 a(1≤a[i]≤1e9)。

定义幸运数字为：只包含 4 和 7 的数字。
输出 a 中有多少个长为 k 的子序列 b，满足 b 中没有相同的幸运数字。（非幸运数字可以有一样的）
答案模 1e9+7。

注：子序列不一定连续。如果两个子序列完全一样，但有元素下标不一样，也视作不同的子序列。

4/7 - n
f[i][j] - 前i个幸运数字选择j个的选取
"""

import sys, math
from collections import defaultdict
from math import comb

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x


n, k = RII()
a = RILIST()

cnt = defaultdict(int)
for x in a:
    # if lucky 47477...
    t = x
    while t:
        r = t%10
        if r not in (4,7):
            break
        t //= 10
    if t == 0:
        cnt[x] += 1

nums = list(cnt.values())
# f[i][j] 前i个数字选j个lucky number
f = [0]*(k+1)
f[0] = 1
# for i in range(len(nums)):
#     for j in range(1, k+1):
#         f[i][j] = f[i-1][j] + f[i-1][j-1] * nums[i-1]
for c in nums:
    for j in range(k, 0, -1):
        f[j] += f[j-1] * c

# f[j] 从所有幸运数字中选j个的方案数，余下k-j个从non-lucky中选择

m = n - sum(nums) # non-lucky
MOD = mod = 1_000_000_007
MX = m
fac = [0] * (MX+1)  # f[i] = i!
fac[0] = 1
for i in range(1, MX+1):
    fac[i] = fac[i - 1] * i % MOD
inv_fac = [0] * (MX+1) # inv_fac[i] = i!^-1  i的阶乘在模p=10**9+7下的乘法逆元
inv_fac[-1] = pow(fac[-1], MOD-2, MOD) # pow(fac[-1], -1, MOD) 等价写法
for i in range(MX-1, -1, -1):
    inv_fac[i] = inv_fac[i+1] * (i+1) % MOD

def comb(n, m):
    if n < m or m < 0: return 0
    # n!/m! (n-m)!
    return (fac[n] * inv_fac[m] * inv_fac[n-m])

res = 0
for j in range(k+1):
    # j, k-j
    res = (res + f[j] * comb(m, k-j)) % mod
print(res)




"""
#include <bits/stdc++.h>
using namespace std;

#define MOD 1000000007
using LL = long long;

bool isLucky(int x) {
    if (x == 0) return false;
    while (x) {
        int d = x % 10;
        if (d != 4 && d != 7) return false;
        x /= 10;
    }
    return true;
}

LL power(LL x, LL n) {
    LL res = 1;
    while (n) {
        if (n & 1) res = res * x % MOD;
        x = x * x % MOD;
        n >>= 1;
    }
    return res;
}

vector<LL> fac, inv_fac;

void init_fac(int MX) {
    fac.resize(MX+1);
    inv_fac.resize(MX+1);
    fac[0] = 1;
    for (int i = 1; i <= MX; i++)
        fac[i] = fac[i-1] * i % MOD;
    inv_fac[MX] = power(fac[MX], MOD-2);
    for (int i = MX-1; i >= 0; i--)
        inv_fac[i] = inv_fac[i+1] * (i+1) % MOD;
}

LL comb(int n, int m) {
    if (n < m || m < 0) return 0;
    return fac[n] * inv_fac[m] % MOD * inv_fac[n-m] % MOD;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    vector<int> a(n);
    unordered_map<int, int> cnt;

    for (int &x : a) {
        cin >> x;
        if (isLucky(x)) cnt[x]++;
    }

    vector<int> nums;
    for (auto &[_, c] : cnt) nums.push_back(c);

    vector<LL> f(k+1);
    f[0] = 1;

    for (int c : nums)
        for (int j = k; j >= 1; j--)
            f[j] = (f[j] + f[j-1] * c) % MOD;

    int m = n - accumulate(nums.begin(), nums.end(), 0);
    init_fac(m);

    LL res = 0;
    for (int j = 0; j <= k; j++) {
        res = (res + f[j] * comb(m, k - j)) % MOD;
    }

    cout << res << '\n';

    return 0;
}
"""