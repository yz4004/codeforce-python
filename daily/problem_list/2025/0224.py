import sys
from math import inf
from typing import List

"""
https://codeforces.com/problemset/problem/327/A

输入 n(1≤n≤100) 和长为 n 的数组 a，只包含 0 和 1。

从 a 中选一个非空连续子数组，把其中的 0 变成 1，1 变成 0。
这个操作必须恰好执行一次。

输出操作后 a 中 1 的个数的最大值。 


状态机dp
- 思考多少种状态 + 限定每种状态条件后，独立推导
- 当前i状态分三种 - 没任何翻转 处于翻转子数组中 已经用过翻转 （三段子数组） 
- 定义 f[012] 分别对应截止到 i] i处于上面三种状态下 的子数组拥有的最多1的数量
- 没翻转 f0 = f0 + x
- 翻转中 f1 = max(f0, f1) + 1-x  可以之前没反转就从当前开始，
- 翻转后 f2 = max(f1, f2) + x    可以是当前结束翻转，或者之前很早就结束翻转
- 初始不合法的转态 f1=f2=-inf 
- 至少翻转一次 应输出 max(f1, f2)

枚举角度 
- 枚举每个 [,r] 翻转子数组右端点，找左端点 [l,r] 使得 cnt0_lr -cnt1_lr 最大
    cnt0_lr - cnt1_lr = (ps0[r+1] - ps0[l]) - (ps1[r+1] - ps1[l]) 最大
                    = ps0[r+1] - ps0[l] - (r+1-ps0[r+1] - l+ps0[l])
                    = 2*ps0[r+1] - (r+1) - (2*ps0[l] - l)
    即维护 2*ps[x] - x 前面的最小值
- 枚举得到了最大的子区间 cnt0_lr -cnt1_lr, 这是可以增加的1，还要加上原始1
- 只要存在0上面就是正数，除非全是1，特判
"""
def solve(nums):
    # 枚举右端点
    if all(x==1 for x in nums):
        return len(nums) - 1
    cnt1 = sum(nums)
    res = -inf
    ps0 = 0
    mi = 0
    for i,x in enumerate(nums):
        ps0 += 1-x
        cur = 2*ps0 - (i+1)
        res = max(res, cur - mi)

        mi = min(cur, mi)
    return res + cnt1


    # 状态机dp - 三种状态
    # 给定01数组
    # [l,r] 选择子数组进行一次01翻转，输出01最大值
    # 选0-1差值最大的子数组
    # 前一个位置两种状态，翻转/翻转子数组中/已经结束翻转 [:i][012] 对应的最多的1
    f = [0,-inf, -inf]
    g = [0,0,0]

    for i,x in enumerate(nums):
        # [:i]

        g[0] = f[0] + x
        g[1] = max(f[0], f[1]) + (1 - x)
        g[2] = max(f[1], f[2]) + x

        f,g = g,f
    return max(f[1], f[2]) # 不能不执行，必须执行一次

Test = False
if Test:
    ########################## 本地调试部分 读取同目录下的 input.txt 数据
    # 输入部分
    with open("../input.txt", "r") as file:
        sys.stdin = file
        input = sys.stdin.read
        data = input().splitlines()

        ###############################################
        # n个数
        n = int(data[0])
        nums = list(map(int, data[1].split()))
        result = solve(nums)

        # 输出结果
        sys.stdout.write(str(result))
        # sys.stdout.write(' '.join(map(str, result)) + '\n')
        ###############################################


        sys.exit()

input = sys.stdin.read
data = input().splitlines()

###############################################
# n个数
n = int(data[0])
nums = list(map(int, data[1].split()))
result = solve(nums)

# 输出结果
sys.stdout.write(str(result))
###############################################
