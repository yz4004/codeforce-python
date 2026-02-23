"""
https://codeforces.com/problemset/problem/416/D

输入 n(1≤n≤2e5) 和长为 n 的数组 a，其中 a[i] 要么是 -1，要么在 [1,1e9] 中。

你需要把 a 中的每个 -1 分别替换成任意正整数。
替换后，把 a 分割成若干连续段，要求每一段都是等差数列。
注：长为 1 的段一定是等差数列。

输出最少分多少段。

- 贪心思路是从左往右贪 尽早合到左侧 且少给右侧制造限制
- 分组循环，已有点的限制要满足，相当于他们有一些连线 而尽量将-1作为整数点插入其中
- [] x1 [] x2 [] ... xn []. 其中[]内是待插入点
- 每次枚举循环处理: [] x1 [] x2 [] ...
    要先确定整数公差d 通过x1/x2的距离决定
    得到d后要确定前面一段能否满足 （非负）
    如果不满足一定要分出一段，要把整个 [] x1 [] 当做 [x1 ... x1] 分出去 少给x2制造负担
    如果d可以满足，则挨个枚举 贪心走完这段等差


"""

import sys
from collections import Counter

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

mod = 10 ** 9 + 7

n = RI()
nums = RILIST()

def check(n, nums):
    res = 0
    i = 0
    while i < n:
        # [i:]
        # [] x1 [] x2 [] ... 其中 [] = [-1...-1] 待定点

        # 1. 确定开头-1数量 pre_unassigned1
        # 2. 确定第一个到第二个点中间-1数量 pre_unassigned2
        # 3. 确定等差d
        # 如果无法用d串联整个 [] x1 [] x2
        # 则 [] x1 [] 单独成段即可

        pre_unassigned1 = 0
        pre_unassigned2 = 0
        x1 = x2 = None
        j = i
        while j < n:
            if nums[j] == -1:
                if not x1:
                    pre_unassigned1 += 1
                else:
                    pre_unassigned2 += 1
            else:
                if not x1:
                    x1 = j, nums[j]
                else:
                    x2 = j, nums[j]
                    break
            j += 1

        # 确定d
        if not x2: return res + 1

        dx, dy = x2[0] - x1[0], x2[1] - x1[1]

        d = dy // dx
        #print(nums[i:], x1, x2, d)
        if (dy % dx != 0) or (d > 0 and x1[1] - d * (x1[0] - i) <= 0):
            res += 1
            i = j
            #print("!!break")
            continue

        cur = nums[j]
        j = j + 1
        #print(cur, j)

        # cur = x2 [] x3 [] ...
        while j < n:
            if (nums[j] != -1 and nums[j] != cur + d) or (nums[j] == -1 and cur + d <= 0):
                break
            cur += d
            j += 1
        res += 1
        #print("seg:", nums[i:j])

        i = j
    return res
print(check(n, nums))








