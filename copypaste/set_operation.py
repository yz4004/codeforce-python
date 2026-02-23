
# traverse set
def traverse_elements(s):
    # 1. 遍历集合 - 检查i in set
    for i in range(s.bit_length()):
        if (s >> i) & 1:
            print(i)

    # 2. 遍历集合 - 从小到大 lowbit
    t = s
    while t:
        lb = t & -t
        i = lb.bit_length()-1
        print(i)
        t ^= lb

def traverse_subsets(n):
    # 1. 枚举所有集合 - 空集到全集
    for s in range(1<<n):
        pass

    # 2. 枚举非空子集
    sub = s
    while sub:
        print(sub)
        sub = (sub - 1) & s
    # 暴力枚举 - s不断数值减一，并检查是否子集 (s-i) & s, 会有大量的稀疏的非子集情况
    # 对于s=10110 想像去掉稀疏0 变成 111, 此时连续减一就是全部子集，然后再把0补回来
    # 111 - 110 - 101 - 100 - 011 ...
    # 规律是减掉lowbit 然后低位都补充1
    # 10..0 -> 01...1
    # 10110 -> 10100 -> 10010 -> 10000 -> 00110
    # 其实就是减去lowbit 然后和原有subset取交

    # 3. 枚举含空子集
    sub = s
    while True:
        print(sub)
        if sub == 0: break
        sub = (sub - 1) & s

    # 4. Gosper's Hack
    # 恰好枚举所有k-size子集

    # 5. 枚举超集
    sup = s
    while sup < (1 << n):
        print(sup)
        sup = (sup + 1) | s


    # 6. 枚举子集的子集/子集转移 - 复杂度O(3^n)
    for s in range(1<<n):
        sub = s
        while sub:
            sub = (sub-1) & s
        # 3^n 证明
        # k-size 子集有 c(n,k) - 外层
        # 每个k-size子集再枚举其子集 - 2^k
        # sum( c(n,k)*2^k for k=0..n) = 3^n


