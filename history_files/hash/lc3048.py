"""
判断s1是s2 的 prefix 且 surfix
字典树
abc 是 abc...abc 的 prefix + surfix

字符串 hash
如果s是一个满足要求的字符 则 s 的 hash值应为 s2 的某个 surfix + prefix 的hash值
字符串hash计算 所有 s2[:i] 和 s2[n-i:n] 的hash值对，如果相等，再去检查前面访问过的所有word的hash值

"""
from collections import defaultdict
from typing import List

class Solution:
    def countPrefixSuffixPairs(self, words: List[str]) -> int:

        # words = sorted(words, key=len)
        # words.sort(key=len)
        # 本题要求保持顺序

        base = 499
        M = 1000_000_000 + 7

        # [:i] hashcode(word[:i])
        def hashcode(word) -> list:
            n = len(word)
            hash = [0]*(n+1)
            for i, c in enumerate(word):
                hash[i+1] = (hash[i] * base + ord(c)) % M
            return hash

        visited = defaultdict(int)
        res = 0
        for word in words:
            hash = hashcode(word)
            # print(word, hash) for debug
            m = len(word)
            for i in range(1, m+1):
                # [:i] [m-i:m]
                surfix = (hash[m] - hash[m-i] * pow(base, i, M)) % M
                if surfix == hash[i] and surfix in visited:
                    res += visited[surfix]
            visited[hash[m]] += 1
        return res

if __name__ == "__main__":
    s = Solution()
    # arr = ["a", "aba", "ababa", "aa"]
    # arr = ["abab","ab"]
    arr = ["a", "a"]
    print(s.countPrefixSuffixPairs(arr))

""" 
https://leetcode.cn/problems/count-prefix-and-suffix-pairs-ii/solutions/2644035/mei-ju-ha-xi-by-tsreaper-koi1
https://leetcode.cn/problems/count-prefix-and-suffix-pairs-ii/solutions/2644159/zi-fu-chuan-ha-xi-fu-shu-zu-ha-xi-tong-y-m6ls/
"""

class Node:
    __slots__ = "children", "cnt"

    # cnt 记录词的数量
    def __init__(self):
        self.children = defaultdict(Node)
        self.cnt = 0


# 要求一个词完全是另一个词的前后缀 （而不是有公共前缀就行）
class Solution:
    def countPrefixSuffixPairs(self, words: List[str]) -> int:

        # word_pairs = []
        # for word in words:
        #     word_pair = [(x,y) for (x,y) in zip(word, word[::-1])]
        #     word_pairs.append(word_pair)

        # res = 0
        # root = Node()
        # for word in word_pairs:
        #     cur = root
        #     for pair in word:
        #         cur = cur.children[pair]
        #         res += cur.cnt
        #     cur.cnt += 1
        # return res

        # print(self.cal_z("ababa"))
        # trie =

        return -1

    """
    z[i]: s[i:] 与 s 的最长公共前缀
    如果想知道s中一段相等的前后缀，
    即找 z[i] = n-i 
    (s[i:]与s公共前缀刚好为 s[i:n], 即为i-n后缀)
    对于字典树中的匹配前缀 只需查询对应长度的后缀
    前缀index i - 查询 z[n-i] ~ [n-i:]
    """

    def cal_z(self, s: str) -> list:
        n = len(s)
        z = [0] * n  # z[i] 定义为 lcp(s[i:], s)
        l = r = 0  # z-box  [l, i,  r]
        for i in range(1, n):
            if i <= r:
                z[i] = min(z[i - l], r - i + 1)
            while i + z[i] < n and s[i + z[i]] == s[z[i]]:
                l, r = i, i + z[i]  # 先更新z-box 顺序不能错
                z[i] += 1
        return z








