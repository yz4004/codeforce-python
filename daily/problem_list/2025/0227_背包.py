# # import sys
# # from math import inf
# # from typing import List
# #
# # # sys.setrecursionlimit(10**7)
# #
# # mod = 998244353
# # def solve(m, nums):
# #
# #     # 01
# #     n = len(nums)
# #     res = [0]*n
# #     f = [0]*(m+1) # f[i][j] 前i个数 子集和恰好为j的方案数
# #     f[0] = 1
# #     for i in range(1, n+1):
# #         # 考虑第i个物品
# #         x = nums[i - 1]
# #         if x > 0:
# #             for j in range(m, x-1, -1):
# #                 f[j] = (f[j] + f[j-x]) % mod # 组合j 由一个x参与的方案数
# #         else:
# #             x = -x
# #             for j in range(x, m+1):
# #                 # 现在撤销了物品x 所有x参与构建的方案 j = x + (a1 a2 ... ) 没了x 就剩下 j-x = (a1 a2 ... )
# #                 # 如何维持 有没有x参与构建的信息？ 其实反过来看就是撤销后 f[j-x] 的数值从 f[j] 转移而来，
# #                 # f[j] 保存了所有等于j的方案; f[j-x] 有所有等于j-x的方案
# #                 # f[j] 里是包含一个 f[j-x] 的
# #                 # f[j] -= f[j-x]
# #                 # 注意更新顺序
# #                 f[j] = (f[j] - f[j - x] + mod) % mod
# #         res[i-1] = f[m]
# #     return res
# #
# #
# # Test = True # False #
# # if Test:
# #     ########################## 本地调试部分 读取同目录下的 input.txt 数据
# #     # 输入部分
# #     with open("./input.txt", "r") as file:
# #         sys.stdin = file
# #         input = sys.stdin.read
# #         data = input().splitlines()
# #
# #         ###############################################
# #         # n个数，限制为k
# #         q,k = data[0].split()
# #         q,k = int(q), int(k)
# #
# #         nums = []
# #         for i in range(1, q+1):
# #             sign, x = data[i].split()
# #             nums.append((1 if sign == "+" else -1) * int(x))
# #         result = solve(k, nums)
# #
# #         # 输出结果
# #         # sys.stdout.write(str(result))
# #         sys.stdout.write('\n'.join(map(str, result))) # 要求分行输出
# #         ###############################################
# #
# #
# #         sys.exit()
# #
#
# import sys
# # from math import inf
# # from typing import List
# # sys.setrecursionlimit(10**7)
# import os
# # print(os.path.exists("input.txt"))
# # print("Start reading input...")
# mod = 998244353
# input = sys.stdin.read
# data = input().splitlines()
# # print("Finished reading input:", data)
# n, m = map(int, data[0].split())
# f = [0] * (m + 1)  # f[i][j] 前i个数 子集和恰好为j的方案数
# f[0] = 1
# for i in range(1, n + 1):
#     sign, x = data[i].split()
#     x = int(x)
#     if sign == "+":
#         for j in range(m, x - 1, -1):
#             f[j] = (f[j] + f[j - x]) % mod  # 组合j 由一个x参与的方案数
#     else:
#         for j in range(x, m + 1):
#             # 现在撤销了物品x 所有x参与构建的方案 j = x + (a1 a2 ... ) 没了x 就剩下 j-x = (a1 a2 ... )
#             # 如何维持 有没有x参与构建的信息？ 其实反过来看就是撤销后 f[j-x] 的数值从 f[j] 转移而来，
#             # f[j] 保存了所有等于j的方案; f[j-x] 有所有等于j-x的方案
#             # f[j] 里是包含一个 f[j-x] 的
#             # f[j] -= f[j-x]
#             # 注意更新顺序
#             f[j] = (f[j] - f[j - x] + mod) % mod
#     sys.stdout.write(str(f[m]) + "\n")
# sys.exit()
#
# # 输出结果
# # sys.stdout.write(str(result))
# ###############################################
#
#
# # def backpack_01(nums, m):
# #     # 给定一组nums 求子集和恰好等于m的子集数量
# #     # 只考虑子集和的方案数 （也可以统计方案之间的最小成本）
# #     # m = 背包容量
# #     n = len(nums)
# #     f = [[0] * (m + 1) for _ in range(n + 1)]  # f[i][j] 前i个数 子集和恰好为j的方案数
# #     for i in range(n + 1):
# #         for j in range(m + 1):
# #             # 考虑第i个物品
# #             f[i][j] = f[i - 1][j]
# #             if nums[i - 1] <= j:
# #                 f[i][j] += f[i - 1][j - nums[i - 1]]
# #     # return f[n][m]
# #
# #     f = [0] * (m + 1)
# #     for i in range(1, n + 1):
# #         for j in range(m, 0, -1):  # 顺序
# #             # 考虑第i个物品
# #             # f[i][j] = f[i-1][j]
# #             if nums[i - 1] <= j:
# #                 # f[i][j] += f[i-1][j-nums[i-1]]
# #                 f[j] += f[j - nums[i - 1]]
# #     return f[m]



mod = 998244353
n, m = map(int, input().split())
f = [0] * (m + 1)
f[0] = 1
for _ in range(1, n + 1):
    sign, x = input().split()
    x = int(x)
    if sign == "+":
        for j in range(m, x - 1, -1):
            f[j] = (f[j] + f[j - x]) % mod
    else:
        for j in range(x, m + 1):
            # f[j] = (f[j] - f[j - x]) % mod
            f[j] = (f[j] - f[j - x] + mod) % mod
    # sys.stdout.write(str(f[m]) + "\n")
    print(f[m])

# import sys
# mod = 998244353
# input = sys.stdin.read
# data = input().splitlines()
# n, m = map(int, data[0].split())
# f = [0] * (m + 1)
# f[0] = 1
# for i in range(1, n + 1):
#     sign, x = data[i].split()
#     x = int(x)
#     if sign == "+":
#         for j in range(m, x - 1, -1):
#             f[j] = (f[j] + f[j - x]) % mod
#     else:
#         for j in range(x, m + 1):
#             f[j] = (f[j] - f[j - x] + mod) % mod
#     sys.stdout.write(str(f[m]) + "\n")
# sys.exit()