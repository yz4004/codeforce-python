"""
倍增算法求后缀数组 - O(n * log(n)^2)

"""

def suffix_array(s):
    """
    计算 suffix array
        ababa
        5 3 1 4 2
    输出一个list a[i]=j 代表 rank为i的后缀是 s[j:] 的rank
    O(n * log(n)^2)
    """

    n = len(s)
    k = n.bit_length()
    #st = [[0] * n for _ in range(k)] #优化点，可以用两个数组替换掉
    st = [0] * n # 空间优化，每次轮转 st_new
    # 初始化排位 单字符排位取char
    for i, c in enumerate(s):
        # st[0][i] = ord(c) #非空间优化
        st[i] = ord(c)

    # 每次考虑所有 s[i:i+2^j] 2^j长度的字符，如果越界，后缀部分取-1
    for j in range(1, k):  # st[j][i]  -- st[j-1][i] st[j-1][i+2^(j-1)]
        rank = [None] * n
        w = 1 << (j - 1)
        for i in range(n):  # n - (1 << j) + 1
            # 考虑当前 s[i:i+2^j] 的排序tuple，由 s[i:i+w//2] s[i+w//2,i+w] 两部分拼接，考虑两个部分的排位，两个排位上轮保证计算出来，如果后者字符串为空，则取-1代表空，其字典序靠前
            # rank[i] = (st[j - 1][i], st[j - 1][i + w] if i + w < n else -1) #非空间优化
            rank[i] = (st[i], st[i + w] if i + w < n else -1)

        # 去重后生成新的rank tmp[tuple] 指向当前tuple对应的位次，填入时根据每个s[i:i+2^j]的tuple查询tmp表
        tmp = {rk: idx for idx, rk in enumerate(sorted(set(rank)))}
        st_new = [0]*n
        for i in range(n):
            # rank[i] -> tmp[rank[i]]
            # st[j][i] = tmp[rank[i]] #非空间优化
            st_new[i] = tmp[rank[i]]
        st = st_new
    # st[i] 是 s[i:] 的rank 还要转换一下
    sa = [0]*n
    for rank, i in sorted(zip(st,range(n))):
        sa[rank] = i+1 #假设从1开始rank 也可以从0开始
    return sa

# s = "aabaaaab"
# print(surfix_array(s)) # 45617283
"""
测试链接
    https://loj.ac/s/2158067 
    https://loj.ac/s/1693225
    ps: 上面的写法过不了这个链接 因为这题要ascii输入 还有数字等字符 ord(c)失效
    
如果不要求生成sa 只求字典序最大的后缀 则可双指针 O(n) 
    这是 LC1163. 按字典序排在最后的子串

SA-IS O(n)算法
    https://zhuanlan.zhihu.com/p/39876310
    https://riteme.site/blog/2016-6-19/sais.html
"""