import itertools

s = input()
# s[i,j] s[p,q]

"""
挑选出k个不重叠的回文子串 不严格划分
 
https://codeforces.com/problemset/problem/159/D

输入长度 ≤2000 的字符串 s，只包含小写英文字母。

从 s 中选两个不重叠的非空回文子串，有多少种选法？
正式地，计算四元组 (i,j,p,q) 的个数，其中 1≤i≤j<p≤q≤n 且 s[i..j] 和 s[p..q] 都是回文串。

进阶：做到 O(n)。
进阶：改成选三个呢？选四个呢？选 k 个呢？


枚举第二个回文串, 枚举右维护左 
- 枚举分割点不便计算回文串，但是枚举回文中心+中心拓展 可以做到检查回文+计算结果
- 当找到第二个回文串[l,r] 左侧所需信息是 [0,l) 的回文串总数，用f[i] 维护前i个 [0,i) 的回文子串数量.
- [l,r] 会在 f[r+1] 计入1，假如他是最长，则会停止拓展，但从定义上, f[r+2...] 也应该计入那个1，什么时候进行 f[i+1] += f[i] - 当f[i] 所有前i个回文串都找完位置才更新 f[i+1] 也就是遍历到最后一个中心拓展的位置 [i-1] 计算完后
- O(n^2)
"""
n = len(s)
f = [0]*(n+1) # f[i] - s[:i] 的回文串数量
res = 0
for i in range(n):
    # ,i]

    # [i-1, i, i+1]
    # [i,i+1]
    # f[i + 1] += f[i] 可以在这加

    j = 0
    while i-j >= 0 and i+j < n: # [i-1, i, i+1]
        if s[i-j] != s[i+j]: break
        # [i-j, i, i+j]
        res += f[i-j]
        f[i+j+1] += 1
        j += 1

    j = 0
    while i-j >= 0 and i+1+j < n: # [i,i+1]
        if s[i - j] != s[i + j + 1]: break
        # [i-j, i+1+j]
        res += f[i-j]
        f[i+j+2] += 1
        j += 1

    # 计算完i的中心拓展位置，前i+1个所有回文都计算完了
    if i+2 <= n: f[i+2] += f[i+1]
print(f)
print(res)




"""
前缀优化 + manacher
manacher预处理回文信息后，差分+两次前缀和
    差分数组记录每个最长回文部分
    第一次前缀和是右端点=i的回文串个数，第二次才是右端点<=i的串数
剩下再做一次前缀和优化dp
"""
def manacher(s):
    n = len(s)
    t = ["#"] * (2 * n + 1)
    for i, c in enumerate(s):
        t[2 * i + 1] = c

    m = 2 * n + 1
    z = [1] * (2 * n + 1)  # g[i]
    l = r = 0
    #  [l, r] 沿着l对称 x-l = l-y    y=2*l-x
    for i in range(m):
        # [l,r]
        if i <= r:
            z[i] = min(r - i + 1, z[2 * l - i])
        while i + z[i] < m and t[i + z[i]] == t[i - z[i]]:
            l, r = i, i + z[i]
            z[i] += 1
    return z  # 2*n+1

z = manacher(s)
n = len(s)
f = [0]*(n+1) # f[i] 对应以i为结尾的差分数组
for i in range(n):
    # 处理每个回文中心
    # [i]  [i,i+1]
    d = z[2*i+1] # 以i为中心的最大回文半径 （拓展后的）#x#x#x#, d//2 是实际的回文半径（含中心）
    d = d//2
    # [i-d+1,i,i+d-1] 最长的回文范围, i-i+d-1 每个结尾的索引都添加了一个回文串 - 差分
    f[i] += 1
    f[i+d] -= 1
    #print(i, d, s[i-d+1:i+d])

    d = z[2*i+2] # 以 [i,i+1] 中心padding # 为中心的最大回文半径 （拓展后的）
    d = d//2
    # [i-d+1, i, i+1, i+d]
    f[i+1] += 1
    f[i+d+1] -= 1
    # print(i, d, s[i-d+1:i+d+1])
    # print()


# 整合差分数组
f = list(itertools.accumulate(f)) # f[i] 以i结尾的回文串数量
f = list(itertools.accumulate(f[:-1], initial=0)) # 前i个包含的所有可能回文串选取方案，因为答案只要求两个划分 所以对于前缀只关心总体方案数，不是要求不重叠划分
# print(f)

res = 0
pre = list(itertools.accumulate(f, initial=0)) # dp前缀和查询优化辅助数组
for i in range(n):

    # [i]
    d = z[2*i+1] # 以i为中心的最大回文半径 （拓展后的）#x#x#x#, d//2 是实际的回文半径（含中心）
    d = d//2
    # [i-d+1,i,i+d-1] 最长的回文范围
    # res += sum(f[j] for j in range(i-d+1, i+1)) # [:j) 等价上面，需要前缀和优化
    res += pre[i+1] - pre[i-d+1]

    # [i,i+1]
    d = z[2*i+2] # 以 [i,i+1] 中心padding # 为中心的最大回文半径 （拓展后的）
    d = d//2
    # [i-d+1, i, i+1, i+d] 最长的回文范围
    # res += sum(f[j] for j in range(i-d+1, i+1)) # [:j)
    res += pre[i+1] - pre[i-d+1]
print(res)


"""
因为只要求找出两个不重叠的子串，所以f[i]可以统计前i个回文串的所有方案

进阶1，如果是3,4 ... k个不重叠的子串呢？
- 上述方法推广到k, 第二个dp得到前i个所有不重叠回文子串对的数量，是恰好截止到i 再进行一次前缀得到 <= i 的所有方案， 然后再枚举第三个
- 当前枚举第j个回文串，要求 i] 前面记录独立的 j-1个不重叠的子串信息
- O(n*k)

进阶2，算重叠的回文子串的数量
- https://codeforces.com/contest/17/problem/E
- 正难则反，所有任意两个的回文子串 comb(n,2) - 上面算过的不重叠回文子串的数量
"""

