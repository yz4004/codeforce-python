"""
https://codeforces.com/problemset/problem/2107/C

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) k(1≤k≤1e12)，长为 n 的 01 字符串 s，长为 n 的数组 a(-1e6≤a[i]≤1e6)。

如果 s[i]=0，表示你可以修改 a[i] 的值为 [-1e18,1e18] 中的任意整数。保证 s[i]=0 时 a[i]=0。
能否让 a 的最大子数组和恰好等于 k？

如果无解，输出 No。
否则输出 Yes 和修改后的 a。



只考虑以i为右端点的子数组 [...i] 能否构造出k不充分：
- 如果枚举 [...i] 就算构造出k 也要考虑后面接上他的子数组 [i+1,j] >= 0
- 枚举所有可能修改的位置 x [ ] x [ ] x
- 对两端固定值的数，调整中间x可以构造出k 而两侧x为防止干扰设成-inf （先把可变点变成极小值，再枚举是否需要修改)
- 但 [] 不保证最大子数组，要截取从 x+1] [x-1 开始的最大子数组再修改。
- 还要保证k不存在于不可修改的端中，引入x必须使得 x] [x+1 or x-1] [x 是两个正数（最大子数组）相加等于k>0

"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

inf = 10 ** 18
def check(n, k, s, nums):

    s1 = [0]*(n+1)
    for i in range(n):
        s1[i+1] = mx(s1[i], 0) + nums[i] if s[i] == "1" else -inf

    s2 = [0]*(n+1)
    for i in range(n-1, -1, -1):
        s2[i] = mx(s2[i+1], 0) + nums[i] if s[i] == "1" else -inf

    nums = [nums[i] if s[i] == "1" else -inf for i in range(n)]

    m = max(s1)
    if m > k:
        return "No"
    elif m == k:
        return "Yes\n" + " ".join(map(str, nums))

    for i in range(n):
        if s[i] == "0":
            left, right = s1[i], s2[i+1]
            left = mx(left, 0)
            right = mx(right, 0)
            nums[i] = k - left - right
            return "Yes\n" + " ".join(map(str, nums))
    return "NO"

T = RI()
for _ in range(T):
    n, k = RII()
    s = RS()
    a = RILIST()
    print(check(n, k, s, a))

sys.exit(0)






def check(n, k, s, a):
    ps = [0]*(n+1)
    vis = {0: 0}
    a_sum = sum(a)
    total = suf = sum(1 for c in s if c == "0")
    zeros = [i for i in range(n) if s[i] == "0"]
    inf = -10 ** 18

    j = 0
    for i, x in enumerate(a):
        # [...i]
        ps[i+1] = ps[i] + x
        c = 1 if s[i] == "0" else 0
        suf -= c
        pre = total - suf

        while j < len(zeros) and zeros[j] <= i:
            j += 1

        case0 = pre >= 2
        case1 = ps[i+1] - k in vis and (ps[i+1] - k <= 0 or vis[ps[i+1] - k] > 0)
        case2 = j-1>=0 and ps[zeros[j-1]+1] <= 0  # [zeros[j-1]], i]

        is_prefix_valid = case0 or case1 or case2
        is_suffix_valid = suf >= 1 or a_sum - ps[i+1] <= 0

        if is_prefix_valid and is_suffix_valid:
            if case0:
                l1 = zeros[j-1]
                l2 = zeros[j-2]
                # l2=inf  [l1, i] = k
                r1 = zeros[j] if j < len(zeros) else -1

                a[l1] = k - (ps[i+1] - ps[l1])
                a[l2] = inf
                if r1 != -1: a[r1] = inf
            elif case1:
                if zeros: a[zeros[0]] = inf
            elif case2:
                l1 = zeros[j - 1]
                # [l1, i] = k
                a[l1] = k - (ps[i+1] - ps[l1])
            return "Yes\n" + " ".join(map(str, a))

        vis[ps[i+1]] = pre
    return "No"

T = RI()
for _ in range(T):
    n, k = RII()
    s = RS()
    a = RILIST()
    print(check(n, k, s, a))