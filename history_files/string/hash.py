base = 499
M = 1000_000_000 + 7

"""
hash[i] - hash(s[:i]) 
"""
def hashcode(s):
    n = len(s)
    hash = [0]*(n+1)
    for i in range(n):
        hash[i+1] = (hash[i] * base + ord(s[i]) ) % M
    return hash

"""
hash[i] = a0 * b^(i-1) + ... + ak * b^(i-1-k) + ... a_(i-2) * b + a_(i-1)

    hash[i] 考虑 s[:i] 所以最后一个是 a_(i-1)
    代入特殊点，hash[1] = a0
    ak * b^(i-1-k) 角标之和 k + i-k-1 刚好是最后一个字符的角标/index = i-1
    打头的 a0*b^(i-1) 幂次正是最后一个字符的坐标 计算到前缀 i) 刚好b乘了 i-1 次

find hash(s[i:j])

hash[i] = a0 * b^(i-1) + ... + ak * b^(i-1-k) + ... a_(i-2) * b + a_(i-1) * b ^ 0
hash[j] = a0 * b^(j-1) + ... + ak * b^(i-1-k)                   + a_(i-1) * b ^ (j-i)         + ... a_(j-2) * b + a_(j-1)

hash[j] - hash[i] * b ^ (j-i)
    hashcode - s[i:j]

    如果考虑闭区间 [i,j] 即半开区间 [i:j+1)
    hash[j+1] - hash[i] * b ^ (j+1-i)
    
右边 hash index + 指数 = 左边项 index
"""

# lc 28
# https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string/submissions/515505715/
class Solution:
    base = 499
    M = 1000_000_000 + 7
    def strStr(self, text: str, pattern: str) -> int:
        m, n = len(pattern), len(text)
        p = self.hashcode(pattern)[-1]
        f = self.hashcode(text)
        for i in range(n-m+1):
            # [i:i+m] ... [n-m:n]
            t = (f[i+m] - f[i] * pow(self.base, m)) % self.M
            if t == p:
                return i
        return -1

    def hashcode(self, s):

        n = len(s)
        hash = [0] * (n + 1)
        for i in range(n):
            hash[i + 1] = (hash[i] * self.base + ord(s[i])) % self.M
        return hash