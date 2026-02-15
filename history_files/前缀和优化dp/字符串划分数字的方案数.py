# LC 1977
from collections import defaultdict

mod = 10 ** 9 + 7
class Solution:

    def numberOfCombinations3(self, num: str) -> int:
        n = len(num)

        # ####### LCP + 前缀和优化
        # f[i][j] num[:j] 以最后一个数字为 [i:j] 的全部方案数
        f = [[0] * (n + 1) for _ in range(n)]

        # lcp检查 [i:i+l] [i+l:i*2l]
        # lcp = defaultdict(lambda: defaultdict(int))  # 嵌套字典形式
        lcp = [[0]*(n+1) for _ in range(n+1)]          # lcp[i][j] 以ij分别开头的lcp长度, lcp[i+1][j+1]+1 only if [i][j]
        for i in range(n - 1, -1, -1):
            for j in range(n - 1, i, -1):
                lcp[i][j] = lcp[i + 1][j + 1] + 1 if num[i] == num[j] else 0

        # f[0][j] 初始化
        col = [[0] * (n + 1) for _ in range(n + 1)]  # col[j] -- prefix sum
        if num[0] != "0":  # [0:i] 第一个数字
            for j in range(1, n + 1):
                f[0][j] = col[j][1] = 1

        for i in range(1, n):
            if num[i] == "0": continue

            for j in range(i + 1, n + 1):

                l = j - i
                if i - l >= 0:
                    p = lcp[i - l][i]
                    if p >= l or num[i - l + p] < num[i + p]:
                        f[i][j] += f[i - l][i]

                ps = col[i]
                f[i][j] += ps[i] - ps[max(i - l + 1, 0)]
                f[i][j] %= mod

                col[j][i + 1] = col[j][i] + f[i][j]

        return sum(f[i][n] for i in range(n)) % mod


    def numberOfCombinations2(self, num: str) -> int:
        n = len(num)

        ######### draft LCP优化
        # # f[i][j] num[:j] 以最后一个数字为 [i:j] 的全部方案数
        f = [[0]*(n+1) for _ in range(n)]
        # lcp检查 [i:i+l] [i+l:i*2l]
        lcp = [[0]*(n+1) for _ in range(n+1)]          # lcp[i][j] 以ij分别开头的lcp长度, lcp[i+1][j+1]+1 only if [i][j]
        for i in range(n-1, -1, -1):
            for j in range(n-1, i, -1):
                lcp[i][j] = lcp[i+1][j+1] + 1 if num[i] == num[j] else 0

        # f[0][j] 初始化
        if num[0] != "0": # [0:i] 第一个数字
            for j in range(1, n+1): f[0][j] = 1

        for i in range(1, n):
            if num[i] == "0": continue  # 不允许任何形式的前导0 单0也不行 只能作为tailing 0

            for j in range(i+1, n+1):
                # f[i][j] [i:j] [i-l:i] [i:j]
                l = j-i
                if i-l >= 0:
                    p = lcp[i-l][i]
                    if p >= l or num[i-l+p] < num[i+p]:
                        f[i][j] += f[i-l][i]

                for k in range(max(i-l+1,0),i):
                    # if num[k] != "0" and int(num[k:i]) <= cur: 如果有外层前导0判断，这里就不必更新
                    # if int(num[k:i]) <= cur:
                        f[i][j] += f[k][i]
        return sum(f[i][n] for i in range(n))

    def numberOfCombinations1(self, num: str) -> int:
        n = len(num)

        # ############# draft1 无优化
        # f[i][j] [:j] 最后一个数字的范围是 [i:j] [0:1] [0:i] [0:n]
        f = [[0]*(n+1) for _ in range(n)]
        # f[0][j]
        if num[0] != "0": # [0:i] 第一个数字
            for j in range(1, n+1): f[0][j] = 1

        for i in range(1, n):
            if num[i] == "0": continue  # 不允许任何形式的前导0 单0也不行 只能作为tailing 0

            for j in range(i+1, n+1):
                # f[i][j] [i:j] [i-l:i] [i:j]
                cur = int(num[i:j])
                l = j-i
                for k in range(max(i-l,0),i):
                    # if num[k] != "0" and int(num[k:i]) <= cur: 如果有外层前导0判断，这里就不必更新
                    if int(num[k:i]) <= cur:
                        f[i][j] += f[k][i]
        return sum(f[i][n] for i in range(n))
