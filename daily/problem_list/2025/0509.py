"""
https://codeforces.com/problemset/problem/1739/E

输入 n(2≤n≤2e5) 和一个 2 行 n 列的 01 矩阵。

这个矩阵表示一条长为 n，宽为 2 的走廊。走廊上某些格子有污渍，用 1 表示。没有污渍的格子用 0 表示。
有一个扫地机器人，从左上角出发。扫地机每一步可以移动到上下左右相邻的格子。
每次，扫地机会移动到（曼哈顿）距离最近的污渍，打扫干净。重复该过程，直到没有污渍。
但如果有多个污渍都离扫地机最近呢？扫地机会宕机！
为避免扫地机宕机，你需要在扫地机开始工作之前，手动清理掉一部分污渍。

输出留给扫地机清理的最大污渍数。

"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n = RI()
mat = [list(map(int, RS())), list(map(int, RS()))]

def solve(mat):
    n = len(mat[0])
    # f[i][0/1] 出发最小花费
    f = [[0]*2 for _ in range(n)]
    # print(mat)
    for i in range(n-2, -1, -1):
        for j in (0,1):
            # if mat[j][i+1] == mat[j^1][i] == 1:
            #     f[i][j] = mn(f[i+1][j], f[i+2][j^1] if i+2 < n else 0) + 1
            # elif mat[j][i+1] == 1:
            #     f[i][j] = f[i+1][j]
            # elif mat[j^1][i] == 1: --- here
            #     f[i][j] = f[i+1][j^1]
            # else:
            #     f[i][j] = f[i + 1][j]

            # 走右侧
            f[i][j] = f[i+1][j] + mat[j^1][i]
            # 横移
            if mat[j^1][i]:
                cost = mat[j][i+1]
                f[i][j] = mn(f[i][j], (f[i+2][j^1] if i+2 < n else 0) + cost)
        #print(f)

    total = sum(sum(row) for row in mat)
    # print(total-f[0][0])
    return total-f[0][0]
print(solve(mat))

def validate(mat):
    n = len(mat[0])
    f = [[0]*2 for _ in range(n)]
    for i in range(n-2, -1, -1):

        for r in (0, 1):
            # 只往右：要不要擦下面这一格
            f[i][r] = f[i + 1][r] + mat[r ^ 1][i]

            # 往下：一定下→右→右
            if mat[r ^ 1][i]:  # 下面是脏，才允许往下
                cost = mat[r][i + 1]  # 右边这一格如果脏就得擦掉
                f[i][r] = min(f[i][r], (f[i + 2][r ^ 1] if i+2 < n else 0) + cost)

        print(f)
    total = sum(sum(row) for row in mat)
    # print(total-f[0][0])
    return total-f[0][0]



# import random
# def check():
#     def generate_case(n):
#         return [[random.randint(0, 1) for _ in range(n)] for _ in range(2)]
#
#     for _ in range(1):
#         #n = random.randint(2, 30)  # limit size for quick check
#         # mat = generate_case(n)
#         mat = [ [0, 0, 1, 1, 0,  1, 0, 1, 0], \
#                 [1, 0, 0, 1, 0,  1, 0, 0, 1]]
#         # mat = [[0, 0], \
#         #         [1, 0]]
#         res1 = validate(mat)
#
#         print("---")
#         res2 = solve(mat)
#         if res1 != res2:
#             print(f"Mismatch found! n={n}")
#             print("Matrix:")
#             for row in mat:
#                 print(row)
#             print(f"Main: {res1}, Alt: {res2}")
#             return
#     print("All test cases passed.")
# check()
