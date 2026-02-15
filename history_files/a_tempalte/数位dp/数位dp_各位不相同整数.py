from functools import cache
"""
LC 2376. 统计特殊整数
https://leetcode.cn/problems/count-special-integers/?envType=problem-list-v2&envId=IRYvHnIJ
说明:本题统计这样的整数 【123456各位不相同】【1123456一位重复不统计】

0. lc实例解析 
- 135内 [11-99] [110-119] [101 121 131] [100 122 133] 9 + 10 + 3 + 3 找出25个非特殊整数 
- 所以答案是135-25=110
- 在只使用 0-9 至多一次的情况下排列组合出的数量（组合解法不好推广）

数位dp解法
f(i, mask, isLimit, isNum)
    i 当前位数
    mask 记录之前填过的数字 （本题要求互不相同
    isLimit 限制
    isNum  leading zero

1. 如果前面不是卡limit 则当前i可以正常选取0-9; 否则如果卡limit 当前位限制在n的对应位
2. 关于前导0
    a. 前导零不计入mask，会一直递降到0，任何时刻脱离前导0，进入正常循环，前导0标记false
    b. 纯前导0 直走is_num=False的前导0下降通道 
    c. 一旦脱离前导0 当前选取范围 【low=1，9】 然后is_num标记位true 前导0标记消失，以后可以再选0
"""

def countSpecialNumbers(self, n: int) -> int:
    s = str(n)
    @cache
    def f(i, mask, is_limit, is_num):
        if i == len(s):
            return int(is_num)  # 排除全是0 如果填过数字就return 1

        res = 0
        # 走前导0下降通道  目前还都只有leading zero
        if not is_num:
            res = f(i + 1, mask, False, False)

        # 非limit通道 最高位可选10 但是最低位要考虑前导0
        # 如果当前递归入参仍是前导0 is_num=False 这里决定脱离前导0选取范围 [1-9]
        #              不是前导 is_num=True  这里决定脱离前导0选取范围 [0-9]
        if not is_limit:
            for j in range(1 - int(is_num), 10): # 当前i位可以填 ?-9
                if mask >> j & 1 == 0:
                    res += f(i + 1, mask | 1 << j, False, True)

        # limit通道，最高位可选 n[i] 但是最低位要考虑前导0
        # 相比上面 前导零逻辑不变，n[i]处新增了 is_limit=True通道
        if is_limit:
            for j in range(1 - int(is_num), int(s[i])):
                if mask >> j & 1 == 0:
                    res += f(i + 1, mask | 1 << j, False, True)
            # 最高位
            h = int(s[i])
            if mask >> h & 1 == 0:
                res += f(i + 1, mask | 1 << h, True, True)
        return res

    return f(0, 0, True, False)  # is_limit = False 则代表后面都不收到约束了，必须用true表示有约束
    # 上面诸多if条件合并，就是最下面的灵茶题解

    s = str(n)
    @cache
    def f(i, mask, isLimit, isNum):
        if i == len(s):
            return int(isNum)
        res = 0
        if not isNum:
            res = f(i + 1, mask, False, False)

        up = int(s[i]) if isLimit else 9
        # 1. 额外对isLimit判断
        # for k in range(0 if isNum else 1, up):
        #     if mask >> k & 1 == 0:
        #         res += f(i+1, mask | (1 << k), False, True)
        # res += f(i+1, mask | (1 << up), True, True) is_limit=True的唯一通道

        # 2. isLimit与k==up合并
        for k in range(0 if isNum else 1, up + 1):
            if mask >> k & 1 == 0:
                res += f(i + 1, mask | (1 << k), isLimit and k == up, True)
        return res
    return f(0, 0, True, False)
