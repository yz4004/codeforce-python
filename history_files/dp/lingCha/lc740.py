import math
from collections import Counter
from functools import cache

class Solution:
    def test(self, s, x, y) -> int:
        @cache
        def dfs(i, j):
            print(i, j, "-")
            if i == 0:
                return 0
            if j < 0:
                return -math.inf

            if s[i-1] == "0":
                return dfs(i-1, j) + j * y

            if s[i-1] == "1":
                return dfs(i-1, j-1) + (i - j) * x

            # if si == !
            # 1 0
            # 01 - x
            res = max(dfs(i-1, j - 1) + (i - j) * x, dfs(i-1, j) + j * y)
            print(i, j, res)
            return res


        cnt = Counter(s)
        n = len(s)
        p = cnt["!"]
        one = cnt["1"]
        return sum(dfs(n, k) for k in range(p+1))

if __name__ == "__main__":

    s = Solution()
    # print(s.test("01!0", 2,3))
    print(s.test("01!", 2, 3))