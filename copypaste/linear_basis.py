import sys
from typing import List

"""
xor线性基
    - 给定一组数找最大xor/某个数能否被xor得到


给定一组无符号整数 x1...xn 长为 W=64 GF(2) 向量
span子空间: x1...xn 任意子集xor组合得到的结果集合
目标: 得到一组线性基 
    b[0-W-1] 第i存放最高位是i的基向量


同矩阵 模拟高斯消元
最后化简得到的基底形成如下阶梯结构
1 ...       |
  1 ...     |
       1... |
         1..|

每个阶梯开头对应的比特位 -- 这些位置是我们可以自由表达的, 从高到低，如果某一位有基向量可以消掉高位在这里产生的1
    从高到低 对这个线性空间里的bit进行表达
    所有非阶梯位置 包括剩余低位bit 都是被支配的部分

应用:
最大xor    -- 从高到低容纳所有阶梯开头
检查线性表出 -- 从高到低检查
"""

class LinearBasis: # XorBasis
    def __init__(self, n: int): # with n digits
        self.b = [0]*n # bi 对应 ith 比特位的基向量
        self.base_cnt = 0

    def insert(self, x):
        b = self.b
        while x:
            i = x.bit_length() # 从高到低尝试插入阶梯位置
            if b[i] == 0:
                b[i] = x
                return
            x ^= b[i]

    def search(self, x) -> bool:
        b = self.b
        while x:
            i = x.bit_length()
            if b[i] == 0:  # 如果i位置没有基向量 则x不能被表出
                return False
            x ^= b[i]
        return True

    def max_xor(self) -> int:
        b = self.b
        n = len(b)
        mx_xor = 0
        for i in range(n-1, -1, -1):
            if b[i] and mx_xor >> i & 1 == 0: # ith 补充基向量 b[i]
                mx_xor ^= b[i]
        return mx_xor

        # res = 0
        # for i in range(n-1, -1, -1):
        #     res = max(res, res ^ b[i])
        # return res

"""

https://codeforces.com/problemset/problem/1101/G

"""