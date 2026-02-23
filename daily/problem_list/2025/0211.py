import sys
from math import inf
from typing import List



def solve(k, nums):

    # (x or nums[0]) + (x or nums[1]) + ... + (x or nums[n-1]) = 最大值

    # 拆位 从高到低贪心
    m = max(k.bit_length(), max(nums).bit_length())
    res = 0
    mask_x = 0
    for i in range(m-1, -1, -1):
        # 1 << i 能否取到
        # 即存在一个x 使得x在不大于k的情况下，将
        #
        pass
        # mask_x |= 1 << i
        # tmp = 0
        # for x in nums:
        #     tmp += mask | x
        #     if tmp > k







Test = False
if Test:
    ########################## 本地调试部分
    # 输入部分
    with open("../input.txt", "r") as file:
        sys.stdin = file
        input = sys.stdin.read
        data = input().splitlines()

        # n个数，限制为k
        n,k = data[0].split()
        n,k = int(n), int(k)

        nums = map(int, data.split())
        result = solve(k, nums)

        # 输出结果
        sys.stdout.write(str(result))
        # sys.stdout.write(' '.join(map(str, result)) + '\n')
        sys.exit()

input = sys.stdin.read
data = input().splitlines()

# n个数，限制为k
n, k = data[0].split()
n, k = int(n), int(k)

nums = map(int, data.split())
result = solve(k, nums)
# 输出结果
sys.stdout.write(str(result))