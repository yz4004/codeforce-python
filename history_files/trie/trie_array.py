from typing import List
"""
用静态数组实现的字典树
"""
N = 100000
class trie:
    def __init__(self):
        self.nex = [[0 for i in range(26)] for j in range(N)] # nxt[p][c] 节点p的c字母分支有单词，则nxt[p][c] > 0 且指向层数
        self.cnt = 0 # globel插入节点指针 永不会退指向下一个可以初始化的空节点位置
        self.exist = [False] * N  # 该结点结尾的字符串是否存在

    def insert(self, s):  # 插入字符串
        p = 0
        for i in s:
            c = ord(i) - ord("a")
            if not self.nex[p][c]:
                self.cnt += 1
                self.nex[p][c] = self.cnt  # 如果没有，就添加结点
            p = self.nex[p][c]
        self.exist[p] = True

    def find(self, s):  # 查找字符串
        p = 0
        for i in s:
            c = ord(i) - ord("a")
            if not self.nex[p][c]:
                return False
            p = self.nex[p][c]
        return self.exist[p]

"""
应用例题：
lc421 -- 数组实现01字典树
https://leetcode.cn/problems/maximum-xor-of-two-numbers-in-an-array/description/

"""

MAXN = 200000
f = [[0]*2 for _ in range(31*MAXN)]

def clear(idx): #清空已开辟的数组
    for i in range(idx):
        for j in range(2): #26
            f[i][j] = 0

class Solution:
    def findMaximumXOR(self, nums: List[int]) -> int:
        n = len(nums)
        m = max(x.bit_length() for x in nums)
        # f = [[0]*2 for _ in range(min(31*n, 1<<(m+1)))] 快一点
        idx = 1 # global 指针 -- 对应插入 下一个节点的index
        res = 0
        for x in nums:
            # 查询
            cur = 0 # root
            tmp = 0
            for i in range(m, -1, -1):
                c = x >> i & 1
                if f[cur][c ^ 1] > 0:
                    cur = f[cur][c ^ 1]
                    tmp ^= 1 << i
                elif f[cur][c] > 0:
                    cur = f[cur][c]
                else:
                    break
            res = max(res, tmp)

            # 插入
            cur = 0
            for i in range(m, -1, -1):
                c = x >> i & 1
                if f[cur][c] == 0:
                    f[cur][c] = idx
                    idx += 1
                cur = f[cur][c]
        clear(idx)
        return res

"""
参考
字典树oi-wiki 模板 https://oi-wiki.org/string/trie/#%E7%BB%B4%E6%8A%A4%E5%BC%82%E6%88%96%E6%9E%81%E5%80%BC
内存消耗分析（宫水三叶 lc208题解） https://zhuanlan.zhihu.com/p/374363453#:~:text=%E4%B8%BA%E4%BA%86%E6%96%B9%E4%BE%BF%E5%90%84%E4%BD%8D%E5%90%8C%E5%AD%A6%E8%83%BD%E5%A4%9F

"""