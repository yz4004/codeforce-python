"""
每次填入若干0或者若干1 要求最后总长度在给定范围内的所有可能字符串的数量

"""
import functools
from functools import cache

M = 1000_000_000 + 7
class Solution:
    def countGoodStrings(self, low: int, high: int, zero: int, one: int) -> int:

        # c = [zero, one]

        # f[i] 长为i的字符的所有数量
        f = [0] * (high + 1)
        f[0] = 1
        # f[zero] = f[one] = 1
        for i in range(min(zero, one), high + 1):
            f[i] = (f[i-zero] + f[i-one]) % M
        return functools.reduce(lambda x,y:(x+y)%M, f[low:high+1])

        @cache
        def dfs(i):
            if i == 0:
                return 1
            if i < 0:
                return 0
            r = (dfs(i - zero) + dfs(i - one) )% M
            return r

        res = 0
        for k in range(low, high + 1):
            res = (res + dfs(k)) % M
        return res

if __name__ == "__main__":
    print(Solution().countGoodStrings(3,3,1,1))