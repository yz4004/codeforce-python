"""
https://codeforces.com/problemset/problem/1989/C

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) 和一个 2 行 n 列的矩阵，只包含 -1 0 1。

每一列选一个数。
设第一行所选元素和为 s0，第二行所选元素和为 s1。
最大化 min(s0, s1)。

"""
import sys
from collections import defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for test in range(RI()):
    n = RI()

    cnt = defaultdict(int)
    for t in zip(RILIST(), RILIST()):
        cnt[t] += 1

    # 00
    # 01/10
    # 0-1/-10
    # 1-1/-11 不相等时肯定挑大的，即使是 1/-1 -- 讨论

    # 对11 -1-1 提出来单独讨论
    # 11
    # -1 -1


    s0 = cnt[(1,0)] + cnt[(1,-1)]
    s1 = cnt[(0,1)] + cnt[(-1,1)]

    inc = cnt[(1,1)]
    dec = cnt[(-1,-1)]

    if s0 > s1:
        s0, s1 = s1, s0

    if s0 + inc <= s1 - dec:
        res = s0 + inc

    elif s0 + inc > s1 - dec:

        res = (s0 + s1 + inc - dec) // 2

        # if s0 + inc <= s1:
        #     t = s1 - (s0 + inc) # 消耗的dec
        #     res = s0 + inc - (dec - t + 1)//2
        #
        # else: # s0 + inc > s1
        #     t = s1 - s0 # 消耗的inc
        #     # 双方都从s1出发
        #     if inc - t - dec < 0:
        #         res = s1 - (-(inc - t - dec) + 1)//2
        #     else:
        #         res = s1 + (inc - t - dec) // 2

    # 设 x,y 为分配给 s0 的 inc 和 dec
    # inc, x
    # dec, y

    # s0 + x - y
    # s1 + (inc-x) - (dec-y)

    # s0 + x - y = s1 + (inc-x) - (dec-y)
    # s0 + x - y = s1 + inc - x - dec + y

    # t = x-y = (s1 - s0 + inc - dec)/2


    # s0 + x - y
    # = s0 + t
    # = s0 + (s1 - s0 + inc - dec)/2
    # = (s1 + s0 + inc - dec) / 2

    # 这是小数情况，实际向下取整，注意负数时也要向下取整
    # https://chatgpt.com/c/68ad54c6-96dc-8324-ba08-82b7cd531d7e

    # 总和不变 = 初始s0 s1 以及净加 inc - dec = s0 + s1 + inc - dec
    # 希望max min 当能交叉时就是均匀分配总和 (s0 + s1 + inc - dec)//2 向下取整

    # 当不能均匀分割时，如果还均分相当于 s0 + inc, s1 - dec 后还试图拿大的补贴小的，这不允许

    # 这类你加我减的情况，自由度太多，目前有2个 x y
    # s0 + x - y
    # s1 + (inc-x) - (dec-y)

    # 数学运算尝试消除自由度，发现全消掉了

    print(res)

# python 与 非python 的取整问题
# (-3)//2 = -2 向下取整
# (-3)//2 = -(3//2) = -1 向0取整




