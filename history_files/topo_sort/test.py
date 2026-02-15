# class Node:
#     def __init__(self):
#         self.index = -1
#         self.left, self.right = None
#
#
# # s = "2 4 L 2 6 R 4 8 L 4 10 R".split(" ")
# # n = len(s)
# # i_to_node = defaultdict(Node)
# # for i in range(0, n, 3):
# #     f, c = s[i], s[i+1]
# #     i_to_node[f]
# #
#
#
# a = [0, 1, 0, 0, 1]
# def test(a):
#     cnt = 0
#     for i in range(len(a)):
#         if a[i] == 0:
#             a[i] = -1
#         else:
#             cnt += 1
#     print(a)
#     mi = t = 0
#     for x in a:
#         t = min(0, t) + x
#         mi = min(mi, t)
#
#     return cnt - mi
from collections import Counter
from typing import List


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


class Solution:
    def findKthSmallest(self, coins: List[int], k: int) -> int:
        coins.sort()
        n = len(coins)

        p = [set() for _ in range(n + 1)]
        p[1] = set([coins[0]])
        def dfs(i):
            # []2 []3 []4 []
            for j in range(i, 0, -1):
                for l in list(p[j]):
                    # if coins[i] == l: continue
                    p[j + 1].add(lcm(l, coins[i]))
                # print(i, j, p)
            p[1].add(coins[i])

        for i in range(n): dfs(i)
        for i in range(n+1): p[i] = list(p[i])
        print(p)
        def count(k):
            # cnt coin cnt in [0:k]
            r = 0
            sign = -1
            for i in range(1, n + 1):
                tmp = 0
                for c in p[i]:
                    tmp += k // c
                r -= sign * tmp
                sign *= -1
                print(i, tmp)
            print(k, r)
            return r

        l = coins[0]
        r = coins[-1] * k

        while l < r:
            mid = (l + r) // 2
            if count(mid) < k:
                l = mid + 1
            else:
                r = mid
        return l


if __name__ == "__main__":
    s = Solution()
    print(s.findKthSmallest([1,3,4,8], 10))
    print()





        #
        # # print(count(3))
        # # return 0
        #
        # l = coins[0]
        # r = coins[-1] * k
        #
        # while l < r:
        #     mid = (l + r) // 2
        #     if count(mid) < k:
        #         l = mid + 1
        #     else:
        #         r = mid
        #     # print(mid, count(mid))
        # return l



