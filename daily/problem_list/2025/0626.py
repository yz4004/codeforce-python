"""
https://codeforces.com/problemset/problem/2101/C

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) 和长为 n 的数组 a(1≤a[i]≤n)。

构造数组 b，满足 1≤b[i]≤a[i]。
定义 d(x) 为 b 中最左边的元素 x 的下标与最右边的元素 x 的下标的绝对差。如果 x 不在 b 中，则 d(x)=0。
输出 d(1)+d(2)+...+d(n) 的最大值。

- 给定上界数组a，元素范围1-n
- 考虑 d(x) 为一个数最早最晚出现下标之差 需在满足上界a限制下让 sum d最大
-
"""

import sys
from bisect import bisect_left
# from sortedcontainers import SortedList

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x



def check(n, nums) -> int:
    # tmp = SortedList(range(1,n+1))

    pa = list(range(0, n+1))
    def find(x):
        if x == pa[x]:
            return x
        pa[x] = find(pa[x])
        return pa[x]


    suf = [-1]*n
    sum_r = [0]*(n+1)
    s = cnt = 0
    for i in range(n-1, -1, -1):
        x = nums[i]
        # j = bisect_left(tmp, x+1) - 1 # 从未选中的剩余元素中 取小于等于x的最大值 然后移除
        # if j >= 0:
        #     tmp.remove(tmp[j])
        #     s += i
        #     sum_r[n-len(tmp)] = s

        j = find(x)
        if j > 0:
            # tmp.remove(tmp[j])
            pa[j] = j-1
            cnt += 1
            s += i
            sum_r[cnt] = s
            # [i:] 的 suffix 能包含的 1-k 即移除元素的个数
        suf[i] = cnt

    res = 0
    pa = list(range(0, n+1))

    s = pre_cnt = 0
    sum_l = [0]*(n+1)
    for i, x in enumerate(nums):
        # pre = n - len(tmp)  # 前缀能包含的 1-k
        d = mn(pre_cnt, suf[i])
        res = mx(res,  sum_r[d] - sum_l[d])

        j = find(x)
        if j > 0:
            pa[j] = j-1
            s += i
            pre_cnt += 1
            sum_l[pre_cnt] = s
    return res

for _ in range(RI()):
    print(check(RI(), RILIST()))
