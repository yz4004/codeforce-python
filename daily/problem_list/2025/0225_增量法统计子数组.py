import sys
from collections import defaultdict
from math import inf
from typing import List

"""
https://atcoder.jp/contests/abc371/tasks/abc371_e

输入 n(1≤n≤2e5) 和长为 n 的数组 a(1≤a[i]≤n)。

定义 f(i,j) 为连续子数组 a[i]~a[j] 中的不同元素个数。

输出所有 f(i,j) 之和，其中 i<=j。

统计子区间的思路
- 枚举子数组右端点 （常规/优先，如果受阻在考虑其他）
- 反复统计子区间，转化视角，贡献法 （本题会考虑 i (l,r) 上次/下次出现的位置，但进一步讨论不容易）

枚举右端点 + 贡献法/增量法
    本题枚举右端点，当前nums[i] 在以左端点 l: [last[nums[i]]+1, i] 结尾的子数组 [l,i] 中有一次贡献，更早的子数组 [j,i] 贡献同 [j,i-1] 
    所以从前一个位置 i-1 转移，记住以i为右端点结尾的所有子数组的计数之和 ,i] 然后再考虑当前 ,i+1] 在前人基础上引入的增量
"""

def solve(nums):
    # 增量法，考虑当前i结尾的子数组所有计数之和，相比与i-1]结尾子数组的增量
    left = defaultdict(lambda :-1)
    res = pre = 0
    for i,x in enumerate(nums):
        # left[x]+1, i
        pre += i - left[x]
        res += pre
        left[x] = i
    return res



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
        nums = map(int, data[1].split())
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
nums = map(int, data[1].split())
result = solve(nums)
# 输出结果
sys.stdout.write(str(result))
###############################################
