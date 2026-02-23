"""
https://codeforces.com/problemset/problem/1073/C

输入 n(1≤n≤2e5) 和长为 n 的字符串 s，只包含 UDLR，表示上下左右。
然后输入 x y(-1e9≤x,y≤1e9)。

一个机器人一开始在原点，从左到右读取 s 中的指令，目标是移动到 (x,y)。每次只能移动一个单位长度。
你可以修改 s 中的某些指令为其他方向。注意是修改，不是删除。
设修改的指令的最大下标为 r，最小下标为 l，则修改范围长度为 r-l+1。
特别地，如果不修改，则修改范围长度为 0。

输出最小的修改范围长度。
如果无法做到，输出 -1。


"""
import sys
from bisect import bisect_left

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

MOD = 10 ** 9 + 7
n, s = RI(), RS()
x, y = RII()

# dir = {"U":(0,1), "L":(-1,0), "R":(1,0),"D":(0,-1)}

def solve(x, y, n, s):
    d = abs(x) + abs(y)
    if n < d or d % 2 != n % 2:
        return -1

    ps_x = [0]*(n+1)
    ps_y = [0]*(n+1)
    for i, c in enumerate(s):
        ps_x[i+1] = ps_x[i]
        ps_y[i+1] = ps_y[i]

        if c == "U":  ps_y[i+1] += 1
        if c == "D":  ps_y[i+1] -= 1
        if c == "R":  ps_x[i+1] += 1
        if c == "L":  ps_x[i+1] -= 1

    # 因为k越大越宽松 可以二分
    # 固定可修改窗口k后，其余部分不变 会指到一个destination 再看加上k后能否调整到目标即可，即两点的L1距离是否在k步内
    dx, dy = x - ps_x[n], y - ps_y[n]
    # ps_x[n] 实际终点，距离目标x 的差值是 dx
    def check(k):
        for i in range(0, n-k+1):
            # [i,i+k) 考虑修改这一窗口, 将k步指令修改为任意
            # 原本位移是 wx = ps_x[i+k] - ps_x[i]，取消掉这段原本贡献
            # 原目标 -> 新目标 ps_x[n] -> ps_x[n] - wx
            # 则新的距离差 dx=x-ps_x[n] -> x-(ps_x[n]-wx)=dx+wx

            dx1 = dx + (ps_x[i+k] - ps_x[i]) # 回撤掉 [i,i+k] 上的行动，为什么是加?
            dy1 = dy + (ps_y[i+k] - ps_y[i])
            if abs(dx1) + abs(dy1) <= k:
                return True
        return False
    #return bisect_left(range(0,n), True, key=lambda k:check(k))
    # 滑窗

print(solve(x,y, n,s))