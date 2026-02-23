"""
长度为k的最小字典序子序列
大于目标字符串t的最小字典序排列

"""


from collections import Counter




# 长度为k的最小字典序子序列
def smallest_alphabetic_subsequence(s, k):

    # 从前往后贪心
    # 前k个先保留 然后枚举到的新字符串 尝试从后往前替换
    n = len(s)
    def is_tail_enough(i, st):
        # st [i,n)
        # 当引入i发现比栈尾更小时 如果drop掉栈尾元素 包括i在内的后缀 [i,n) 足够构成k长吗？
        return len(st)-1 + (n-i) >= k

        # drop = n - k 也可以用allowed drop思考 最多drop n-k次

    st = []
    for i,c in enumerate(s):
        while st and (st[-1] > c and is_tail_enough(i, st)):
            st.pop()
        st.append(c)

    if len(st) < k:
        return None
    return "".join(st[:k])

    # lc2030 最小字典序k长子序列 + 额外限制
    # https://leetcode.cn/problems/smallest-k-length-subsequence-with-occurrences-of-a-letter


# 大于目标字符串t的最小字典序排列
def lexGreaterPermutation(s: str, t: str):
    # 找s的一个排列，使得大于目标串t 且字典序最小
    # hint: 排列可以用计数解决 对s只需维护计数

    # 正序构造 n^2
    # 枚举目标串t的前缀 s能否构造出一样的前缀 + 后缀可行解 (s后缀排列能否构造出大于 t[i+1:] --s后缀能构造的最大字典序（倒叙排列）)
    # - 枚举t[i+1:] 如果存在一个后缀使得 s能换来一个大字符对应t[j] < s[j] 则成立.

    # 倒叙构造 n
    # 贪心模型是前缀与t贴合且尽量长，在尽量靠后的某个位置s[j]稍稍大于t[j] s[j+1:]后缀再最小字典序
    # 如果字典序要大于t. 枚举翻转大于的位置，前缀只需要检查计数，能凑够前缀就有解

    # 贪心答案形态 + 枚举pivot点
    #   看起来像“倒序贪心”，但它和“字典序最小 k 长子序列”的核心贪心结构其实不一样。
    #   关键差异在于：这题的目标不是“全局尽量小”，而是“在必须严格大于 t 的前提下尽量小”。
    #   这会强制答案具有一个非常特殊的形态，从而把“贪心点”从“逐位选最小”变成了“先确定最靠右的增大位置（pivot），再让后缀最小”
    cnts = Counter(s)
    cntt = Counter(t)
    n = len(s)
    for p in range(n - 1, -1, -1):
        # 在当前p尝试找一个s的字母 j > t[p]. 如果s的计数都大于t的前缀计数 （需维护t的前缀计数）则有解退出
        ch = t[p]
        cntt[ch] -= 1
        for j in range(ch + 1, 26):
            # s ... p
            # t ... ch
            if cnts[j] == 0: continue

            cnts[j] -= 1
            if all(cnts[c] >= cntt[c] for c in range(26)):
                tail = ""
                for c in range(26):
                    d = cnts[c] - cntt[c]
                    if d > 0:
                        tail += chr(c + ord("a")) * d

                res = t[:p] + chr(j + ord("a")) + tail
                return res
            cnts[j] += 1
    return ""

    # lc3720
    # 大于目标字符串的最小字典序排列
    # https://leetcode.cn/problems/lexicographically-smallest-permutation-greater-than-target/description/
    # 3734
    # 在大于t且字典序最小的排列基础上 要求s是回文串 （回文串只需确定左半部分即可）
    # https://leetcode.cn/problems/lexicographically-smallest-palindromic-permutation-greater-than-target/description/
