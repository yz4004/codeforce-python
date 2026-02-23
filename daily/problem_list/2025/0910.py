"""
https://codeforces.com/problemset/problem/846/F

输入 n(1≤n≤1e6) 和长为 n 的数组 a(1≤a[i]≤1e6)。下标从 1 开始。

从 [1,n] 中随机选择一个整数，记作 L。
从 [1,n] 中随机选择一个整数，记作 R。
L 和 R 互相独立。
如果 L>R，交换 L 和 R。

输出 a 的子数组 [L,R] 的不同元素个数的期望值。
与答案的误差必须 <= 1e-4。

1. 期望可以统一应用概率 只需要注意区分单元素和>=2长度的数组概率对期望的贡献 2/n^2, 1/n^2
2. 统计所有子数组的distinct的元素数量的和
    维护以i为结尾的所有子数组的值，拓展到i+1时可以O(1)传递
    https://chatgpt.com/c/68c0eca3-42e8-832b-a29e-6e4abcac6958

    右端点扫、可加贡献、O(1) 传递：
    1. 子数组贡献
        最近一次. distinct. 首次计数 (本题)
        恰好一次/至少两次. 记录最近第一次 第二次

    2. 前缀状态. 和/异或/括号 -- 即状态机dp
    3. 某个和区间长度呈单调的量 -- 即不定长滑窗

"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

n = RI()
a = RILIST()

MAXA = 10**6
pre = [-1] * (MAXA + 1)   # last[v] = v 上次出现的位置（0-based），-1 表示未出现

res = cur = 0
for i,x in enumerate(a):
    #  [j,i-1] i
    # 考虑每个i结尾的所有子数组对distinct元素和的贡献
    #  引入x 所有以 i-1 结尾的子数组. 在上一个x出现的位置后面的子数组，x的加入会贡献1
    j = pre[x]
    if j == -1:
        cur += i+1  # 第一次出现：给所有 [0..i] 各 +1
    else:
        cur += i - j  # 非第一次：只给左端在 (j..i] 的区间各 +1
    pre[x] = i
    res += cur  # 把所有以 i 为右端的贡献累加到总和 S

ans = (2.0 * res) / (n * n) - (1.0 / n)  # 转化为期望 去掉单元素的重复统计 （没有L R互换）
print(f"{ans:.6f}")

