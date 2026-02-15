# def gcd(a, b):
#     while b:
#         a, b = b, a % b
#     return a


# def lcm(a, b):
#     return abs(a * b) // gcd(a, b)

class Solution:
    def findKthSmallest(self, coins: List[int], k: int) -> int:
        coins.sort()
        n = len(coins)

        p = [[] for _ in range(n + 1)]
        for s in range((1 << n)):
            group = []
            for i in range(n):
                if s >> i & 1 == 1:
                    group.append(coins[i])
            p[s.bit_count()].append(math.lcm(*group))

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
            #     print(i,  tmp)
            # print("===", r)
            return r

        l = coins[0]
        r = coins[-1] * k

        while l < r:
            mid = (l + r) // 2
            if count(mid) < k:
                l = mid + 1
            else:
                r = mid
            # print(mid, count(mid))
        return l
