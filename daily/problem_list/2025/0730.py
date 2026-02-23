"""
https://codeforces.com/problemset/problem/2052/F

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) 和一个 2 行 n 列的网格图，只包含点号和 # 号。

你需要用 1x2 的木板，把网格图中的点号全部铺满，木板不能重叠，不能覆盖在 # 号上。
有多少种铺设方案？

如果方案数为 0，输出 None。
如果方案数为 1，输出 Unique。
如果方案数大于 1，输出 Multiple。

"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

# 状态机dp
# [前一个位置放置木板对当前的占模 00 01 10 11] * [当前位置障碍分布 00 ... 11] pre * barrier
# 状态有4*4 组合
# 可能有冲突，则转移不合法
# 无冲突 ，则必须填满当前位置, pre | barrier 是当前放置状态，
# 每种组合下，为了填满当前位置都有固定的转移

def solve(n, nums):
    # 00 01 10 11 代表障碍信息
    f = [0]*4 # 前一个位置对当前i的占位，012 对应无 有唯一 多解 （只有可以横纵2*2才有可能多解）
    f[0] = 1
    for i in range(n):

        tmp = [0]*4
        for pre in range(4):
            # pre是前一个填入对当前的占位，下面如果发现冲突就过 或者前面本身无解
            if nums[i] & pre or f[pre] == 0: continue

            # 和当前障碍合并后的占位状态 我们尝试填满空格，不管后面，让冲突检测处理
            cur = pre | nums[i]

            if cur == 0:
                tmp[0] = f[pre]
                tmp[3] = 2   # 也尝试纵向放两对，但会完全占位
            elif cur == 0b01:
                tmp[2] = f[pre]
            elif cur == 0b10:
                tmp[1] = f[pre]
            else:
                tmp[0] = f[pre]
            # 上述条件的转移规则是固定的，可以简写成一个全局nxt表，即 nxt[cur] 是当前pre转移到的entry
            """
            _nexts = {
                0b00: [0, 3],  # cur=0: 可以不留横板 (0)，也可以上下都横 (3)
                0b01: [2],  # cur=1: 上面空，下面障碍，只能横放到上面 → 留横板到 row=0，对应 mask=2
                0b10: [1],  # cur=2: 下面空，上面障碍，只能横放到下面 → 留横板到 row=1，对应 mask=1
                0b11: [0],  # cur=3: 全障碍，只能什么都不留
            }
            
            cur = bm | pre
            # 查表把 cnt 累加到所有可能的 next_mask 上
            for nm in _nexts[cur]:
                # 上限 2，就当 “Multiple”
                tmp[nm] = min(tmp[nm] + cnt, 2) ?
            """
        f = tmp

    # 最后考虑对 n+1 的影响，如果是2/1 且不占n+1 任何位置 说明恰好填满
    if f[0] == 2:    return "Multiple"
    elif f[0] == 1:  return "Unique"
    else:            return "None"

for _ in range(RI()):
    n = RI()

    nums = []
    for a,b in zip(RS(), RS()):
        cur = 0
        if a == "#":
            cur |= 1
        if b == "#":
            cur |= 2
        nums.append(cur)
    print(solve(n, nums))





