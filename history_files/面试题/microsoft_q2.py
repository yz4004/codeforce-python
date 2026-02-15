"""
Microsoft

2. Code Question 2

You are given an array S made of N strings and an integer K. Choose at most K letters from the alphabet that will allow you to build as many strings from array S as possible. Any of the chosen letters can be used multiple times when building the strings.

What is the maximum number of strings from S that can be built?

Write a function:

def solution(S, K)
that, given an array S and an integer K, returns the maximum number of strings from S that can be built.

Example:

Given S = ["abc", "abb", "cb", "a", "bbb"] and K = 2, the function should return 3. Strings "abb", "a", and "bbb" can be built using the two letters 'a' and 'b'.

Given S = ["adf", "jjbh", "jcgj", "eijj", "adf"] and K = 3, the function should return 2. Two strings "adf" can be built using three letters 'a', 'd', and 'f'.

Given S = ["abcd", "efgh"] and K = 3, the function should return 0. It is not possible to build any string from S using at most three letters.

Given S = ["bc", "edf", "fde", "dge", "abcd"] and K = 4, the function should return 3. Strings "edf", "fde", and "dge" can be built using the four letters 'd', 'e', 'f', and 'g'.

Write an efficient algorithm for the following assumptions:

N is an integer within the range [1..50,000];
K is an integer within the range [1..10];
Each string in S has a length within the range [1..15];
Each string in S is made from only the first ten lowercase letters of the alphabet ('a'–'j')
"""
"""
重点在a-j 2^10才1024
对每个word去重 在对words去重
最后遍历k-size的所有组合，生成一组bitmask
enumerate c(10, 5) = 252 至多有这么多k-size组合 < 5-size
"""
# words = ["abc", "abb", "cb", "a", "bbb", "ad"]
words = ["ac", "ae", "cb", "bbb", "b", "ad", "bd"]  # 2^10  = 1024 - 50000
words = list(set(["".join(sorted(set(word))) for word in words]))
print(words)

# 纯count再选从最大频次往下选不行的 假设word是数对形式 k=3
# a-g a-h a-i a-j  # 从a开始的星图 指向末位字母 -- 选a就错了
# b-c b-d c-d    === bcd全连通图 显然k=3选这个连通图最好
# k = 3

# cnt = [0]*26
# for word in words:
#     for c in set(word):
#         cnt[ord(c) - ord("a")] += 1
# print(cnt)

