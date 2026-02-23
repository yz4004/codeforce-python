"""
https://atcoder.jp/contests/abc367/tasks/abc367_d

输入 n(2≤n≤2e5) m(1≤m≤1e6) 和长为 n 的数组 a(1≤a[i]≤1e9)。下标从 1 开始。

一个环上有 n 个位置，顺时针编号从 1 到 n。
从 i 顺时针移动到 i+1，需要走 a[i] 步。
特别地，从 n 顺时针移动到 1，需要走 a[n] 步。

输出有多少对位置 (s,t)，满足 s≠t，且从 s 顺时针移动到 t 的最小步数是 m 的倍数。

(i,j)
sum[i:j) % m == 0
(ps[j] - ps[i]) % m == 0
ps[j] % m ==  ps[i] % m

"""
import sys, random
from collections import defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n, m = RII()
a = RILIST()
def solve(n, m, a):
    cnt = defaultdict(int)
    cnt[0] = 1
    s = res = 0
    for x in a[:-1]:
        s += x
        res += cnt[s % m]
        cnt[s % m] += 1

    # 防止计入整段 [0,n) 先移除 cnt[0]-=1
    s += a[-1]
    cnt[0] -= 1
    res += cnt[s % m]

    # ...a-1] [a ... b-1] [b...  轮转 b-a 仍然考虑中间 a-b.
    # 在b要找前面的a 使得
    # (ps[b]-ps[a]) % m == s % m  (剩余部分则变成 (s - (ps[b]-ps[a])) % m == 0
    # 确保 [a-b] 是一个中间子数组，不会触及边缘
    d = 0
    cnt.clear()
    for x in a[:-1]:
        d += x
        res += cnt[(d-s) % m]
        cnt[d % m] += 1
    return res
print(solve(n,m,a))

def brute(n, m, a):
    """暴力枚举所有 (s, t)，计算顺时针距离是否能被 m 整除"""
    total = sum(a)
    def dist(s, t):
        # s, t 都是 1…n
        if s < t:
            return sum(a[s-1:t-1])
        else:
            return total - sum(a[t-1:s-1])
    cnt = 0
    for s in range(1, n+1):
        for t in range(1, n+1):
            if s == t:
                continue
            if dist(s, t) % m == 0:
                cnt += 1
    return cnt

def optimized(n, m, a):
    """两段前缀和+哈希的 O(n) 解"""
    # 第一段：不绕圈（s < t），只用 a[:-1]
    cnt = defaultdict(int)
    cnt[0] = 1
    s = res = 0
    for x in a[:-1]:
        s = (s + x) % m
        res += cnt[s]
        cnt[s] += 1

    # 第二段：绕圈（s > t）
    total = sum(a) % m
    cnt.clear()
    cnt[0] = 1
    d = 0
    for x in a[:-1]:
        d = (d + x) % m
        res += cnt[(d - total) % m]
        cnt[d] += 1

    return res

def test(num_trials=1000):
    for it in range(num_trials):
        n = random.randint(2, 10)
        m = random.randint(1, 10)
        a = [random.randint(1, 20) for _ in range(n)]
        r1 = brute(n, m, a)
        # r2 = optimized(n, m, a)
        r2 = solve(n,m,a)
        if r1 != r2:
            print(f"❌ 不匹配！\nn={n}, m={m}\na={a}\nbrute={r1}, optimized={r2}")
            return
    print("✅ 全部测试通过！")

if __name__ == "__main__":
    test()