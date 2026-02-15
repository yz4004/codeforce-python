from functools import cache

primes = "2357"
class Solution:

    def beautifulPartitions(self, s: str, K: int, minLength: int) -> int:
        n = len(s)
        p = []
        for i, c in enumerate(s):
            if c in primes:
                p.append(i)
        m = len(p)
        p.append(n)
        print(p)
        if p[0] != 0:
            return 0

        @cache
        def dfs(i, j):
            # number of partition ending at  p[j]) (p[j] is the start of next segment) i partition before
            # if j == 0:  # p0)  [p0
            #     return 1 if i == 0 else 0
            # print(i, j)
            if i == 0 and j == 0:
                return 1
            if (i > 0 and j == 0) or (i == 0 and j > 0):
                return 0


            # res = dfs(i, j)
            res = 0
            for k in range(j):
                # [:p[k]] [p[k], p[j]]
                if p[k] > p[j] - minLength : continue # [pi-minLength, pi)
                if k>0 and s[p[k]-1] in primes: continue
                res += dfs(i-1, k)
            print(i, j, "-", i, p[j], "-" , res)
            return res
        return dfs(K, m)
        # return sum(dfs(K-1, j) for j in range(m))

if __name__ == "__main__":
    s = Solution()
    print(len("23542185131"))
    r = s.beautifulPartitions("23542185131", 3, 3)

    print(r)



