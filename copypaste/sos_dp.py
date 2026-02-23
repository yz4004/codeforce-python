
"""

101011

101
  1001
  0011
     1

101011

    11




sos dp
sum over subset

f[s] = f[s1] + f[s2] + ... f[sk] 其中si是s的子集

根据s的某位 1__ s所有的转移子集可以划分成两份，包含此元素的 不含此元素的
s= 111
s1 000
s2 001
s3 010
s4 011

s5 100
s6 101
s7 110
s8 111

先假设i是最高位
    不含这个元素的s ^ (1<<i) 的 f[s^(1<<i)] 已经算得
    则 f[s] = f[s^(1<<i)] + f[t...] 所有的在最高位是1的子集 t
    这就是转移
    for s in range(1<<m):
        if s >> i & 1:
            f[s] += f[s ^ (1<<i)]
    其中i这里假设是最高位

101...01 - 将他的子集划分两类
101...10 - 前i-1位置位的子集应该集中在 f[s^(1<<i)]
       1 - 第i位是1的 s的子集们的传递

对于不是最高位的i呢? f[s]







"""

# 对每个x 其对所有其超集有贡献1
def solve(nums):
    n = len(nums)
    m = max(nums).bit_length()
    total = 0
    for x in nums: total |= x

    # 1. 外层枚举超集 对每个超集s 每个遍历所有x
    f = [0]*(1<<m)
    for s in range(1<<m):
        if s & total != s: continue # 需要在total内部
        for x in nums:
            if s & x == x:
                f[s] += 1

    # 2. 外层枚举x 考虑x的所有超集. x向外传播 需要考虑超集在 total内
    f = [0]*(1<<m)
    for x in nums:
        sup = x
        while sup < total:
            if sup & total == sup:
                f[sup] += 1
            sup = (sup+1) | x

    # sos 传播
    # sum over subset - 高维前缀和
    # https://zhuanlan.zhihu.com/p/651143987

    # 前缀和
    ps = [0]*(n+1)
    for i in range(n): ps[i+1] = ps[i] + nums[i]

    # 二维前缀和
    mat = [[0]*n for _ in range(m)]
    ps2 = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m):
        for j in range(n):
            ps2[i+1][j+1] = mat[i][j] + ps2[i+1][j] + ps2[i][j+1] - ps2[i][j]

    ps2 = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            # 先对每一行做一维前缀和
            ps2[i+1][j+1] += mat[i][j]

    for i in range(m):
        for j in range(n):
            ps2[i+1][j+1] += ps2[i+1][j]

    # 扩展到n维
    # 一共n组 每组都是对前i维上做前缀和
    # 从 i 维扩展到 i+1
    # 1111

    f = [0]*(1<<m)
    for x in nums: f[x] += 1

    for i in range(m): # 考虑在 前i位上进行子集传递
        for s in range(1<<m):
            if s >> i & 1:
                f[s] += f[s ^ (1<<i)]


    # 10110 - 求这个集合 满足x是其子集的x的数量. 下面三个x 预计3
    # 00010
    # 00100
    # 10010

    # 枚举前i位上的传递 局部是前缀和
    # ...1... 当某个i位是1时
    # ...0... 需要把i位为0结果传递给上面

    # 初始已经有 f[00010]=1 f[00100]=1 f[10010]=1
    
    # i=2
    # 00100 -> f[00110] += 1 ... f[00110] = 1

    # i=3
    # 00010 -> f[00110] += 1 ... f[00110] = 2
    # 10010 -> f[10110] += 1 ... f[10110] = 1

    # i=5
    # 00110 -> f[10110] += 2 ... f[10110] = 3

