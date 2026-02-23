"""
https://codeforces.com/problemset/problem/2121/E

输入 T(≤1e4) 表示 T 组数据。
每组数据输入 L R(1≤L≤R<1e9)，保证 L 和 R 的十进制长度相同，无前导零。

定义 f(a,b) 为 a 和 b 的十进制表示中，相同位置上数字相同的位数。
例如，f(12,21)=0，f(31,37)=1，f(19891,18981)=2，f(54321,24361)=3。

输出 f(L,x)+f(x,R) 的最小值，其中 x 是 [L,R] 中的整数。
"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

for _ in range(RI()):
    L, R = sys.stdin.readline().strip().split()

    # 1
    # 2

    # 32
    # 42


    carry = 0
    res = 0
    for i, (a,b) in enumerate(zip(L, R)):
        a, b = int(a), int(b)

        if carry == 0:
            if a == b:
                res += 2
            elif a + 1 == b:
                res += 1
                carry = 1
            else:
                break
        else:
            # 9 10
            # 9 11
            if a + 1 == 10 + b:
                res += 1
            else:
                break
    print(res)



