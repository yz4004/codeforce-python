"""
https://codeforces.com/problemset/problem/1270/F

输入长度 ≤2e5 的字符串 s，只包含 0 和 1。

输出 s 有多少个子串 t，满足 t 包含 1，且 t 的长度是 t 中 1 的个数的倍数。
例如子串 1,1010,111 符合要求，0,110,01010 不符合要求。

注：本题时限 8s。

"""
import itertools
import sys
from bisect import bisect_left
from collections import defaultdict
from math import inf, isqrt

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

s = list(map(int, RS()))

# 0 1...1 0
# k个1, 1段落长k0 两侧0 L,R

# (l + k0 + r) = 0 mod k for l,r in 0-L, 0-R
# 枚举左侧右侧要补的0 数量分别为 l,r
# (l,r) 多少个对满足上式

# l = pl * k + a
# r = pr * k + b

#


# 但是不能只用a,b来求，因为l可以等于 (pl-1) * k + 【一个大于a小于k的数】

# a+b+k0 = 0 mod k 找a b 数对 再乘以 pl+1 * pr+1


def get_num_of_subarray(L, R, k0, k):
    # 统计满足条件的 l,r 数对数量
    # (l + k0 + r) = 0 mod k for l,r in 0-L, 0-R

    # l
    #

    pl = L // k if L % k else L//k - 1
    pr = R // k if R % k else R//k - 1
    res = 0
    for a in range((L%k+1 if L % k else k)):
        for b in range((R%k+1 if R % k else k)):
            res += (a+b+k0) % k == 0
    return res * (pl+1) * (pr+1)


def count_lr(L, R, k0, k):
    d = (-k0) % k
    a0, ar = divmod(L, k)
    b0, br = divmod(R, k)

    base = a0 * b0 * k
    linear = (ar + 1) * b0 + (br + 1) * a0

    L1 = (d - br) % k
    R1 = d % k
    if L1 <= R1:
        X = max(0, min(ar, R1) - L1 + 1)
    else:
        X = (min(ar, R1) + 1) + (0 if ar < L1 else (ar - L1 + 1))
    return base + linear + X

    return (1+r) * p + k * (p-1) * p // 2


n = len(s)
B = isqrt(n)
res = 0
ps = list(itertools.accumulate(s, initial=0))
posi = [-1] + [i for i in range(n) if s[i] == 1] + [n]

# 枚举 1 的数量
for k in range(1, B+1):
    # less 1, more segments
    # sliding window, sqrt(n) * n

    for i in range(k, len(posi)-1):
        # [j, i]
        j = i-k+1

        l_seg = posi[j] - posi[j-1] - 1
        r_seg = posi[i+1] - posi[i] - 1

        k0 = posi[i] - posi[j] + 1
        res += get_num_of_subarray(l_seg, r_seg, k0, k)
        # res += count_lr(l_seg, r_seg, k0, k)




# 当1很多 k in [B, n]
# 枚举1会接近于n 但展开的段数较少 < sqrt(n)，即 p*k = 子数组长度
# 此时应枚举 p in [1,B] 即段数  （子数组长度/k=1的数量的能拓展倍数 是显著少于1的，因为1很长）
# [j,i) 有k个1则需要满足
# i-j = p*k (where p in [1,B]
# i-j = p*(psi - psj)
# i-p*psj = j-p*psj 即对固定的p满足这个式子

# 但是这个枚举会和上面造成重复，i-p*psj = j-p*psj 没规定k的大小，小k应已被枚举过
# i-j = p*k for k > B, 即查找的j应该 <= i-p*k < i-p*B

for p in range(1, B+1): # 只统计 k > B, 对应p应该能取到B, [1-B]
    f = defaultdict(int)

    # j指针控制前面信息的加入，只有 [j,i) > p*B, 即此时枚举到的 i-j=p*k > p*B 满足 k > B 不会和前面统计小k时重复
    j = 0
    for i in range(1, n+1):
        res += f[i-p*ps[i]]

        while j <= i-p*B:
            f[j - p * ps[j]] += 1
            j += 1
print(res)
sys.exit(0)
# --------------------------------------------------------------------------------

def count_lr(L, R, k0, k):
    d = (-k0) % k
    a0, ar = divmod(L, k)
    b0, br = divmod(R, k)

    base = a0 * b0 * k
    linear = (ar + 1) * b0 + (br + 1) * a0

    L1 = (d - br) % k
    R1 = d % k
    if L1 <= R1:
        X = max(0, min(ar, R1) - L1 + 1)
    else:
        X = (min(ar, R1) + 1) + (0 if ar < L1 else (ar - L1 + 1))
    return base + linear + X

    return (1+r) * p + k * (p-1) * p // 2

n = len(s)
B = isqrt(n)
res = 0
ps = list(itertools.accumulate(s, initial=0))
posi = [-1] + [i for i in range(n) if s[i] == 1] + [n]

# 枚举 1 的数量
for k in range(1, B+1):
    # less 1, more segments
    # sliding window, sqrt(n) * n

    for i in range(k, len(posi)-1):
        # [j, i]
        j = i-k+1

        l_seg = posi[j] - posi[j-1] - 1
        r_seg = posi[i+1] - posi[i] - 1

        k0 = posi[i] - posi[j] + 1
        # res += get_num_of_subarray(l_seg, r_seg, k0, k)

        res += count_lr(l_seg, r_seg, k0, k)

# # --- 大 k：按 p = len / #1（1..B）枚举 + 迟加入避免重数 ---
# for p in range(1, B + 1):
#     key = [i - p * ps[i] for i in range(n + 1)]  # 注意到 n
#     cnt = defaultdict(int)
#     left = 0
#     need = p * (B + 1)  # 只统计 #1 >= B+1 的子串
#     for j in range(n + 1):
#         while left <= j - need:
#             cnt[key[left]] += 1
#             left += 1
#         res += cnt.get(key[j], 0)
print(res)