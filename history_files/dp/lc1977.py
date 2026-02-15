"""
将给定的数字字符串划分成一个list 要求递增，且无前导0
字符串数字过于长，不能化成int比较
快速比较字符串数字
    较长的一定大，相通长度考虑第一个不一样的字符，即在公共前缀后第一个不相同的字符的大小

预处理公共前缀
lcp[i][j] s[i:] 和 s[j:] 的公共前缀长度
lcp[i][j] = lcp[i+1][j+1] + 1 if i == j else 0

f[i][j]   = f[i-1][i] + f[i-2][i] + ... + f[k][i] + ... f[2*i-j+1][i] + (f[2*i-j][i] ? 等长，需要判断大小)
f[i][j-1] = f[i-1][i] + ... + f[2*i-j+2][i]  + (f[2*i-j+1][i] ? 比较大小)

后者的更新依赖于前者，
f[i][j-1] = f[i][j] - 
"""
MOD = 1000_000_000 + 7
class Solution:
    def numberOfCombinations(self, s: str) -> int:
        n = len(s)



        # lcp[i][j] s[i:] 和 s[j:] 的公共前缀长度
        lcp = [[0]*n for _ in range(n)]
        for i in range(n-1,-1,-1): # [i:]
            for j in range(n-1,i,-1):
                # [i:] vs [j:]
                lcp[i][j] = (lcp[i+1][j+1] + 1) if s[i] == s[j] else 0

        def test(i,j,l):
            if lcp[i][j] >= l:
                return True
            k = lcp[i][j]
            return s[i + k] < s[j + k]

        # f[i][j] [:i] 所有划分 下一个数是 [i:j]
        # f[0][:] = 1
        # f[k][n] 所有非零k 取和
        f = [[0]*n for _ in range(n+1)]








