"""
数位dp2.0 通用版本
1.0 版本只支持 [0,n] 如果是范围 [low, high] 可以f(high) - f(low-1)
2.0 考虑每位是否受到上下限制
2999. 统计强大整数的数目
https://leetcode.cn/problems/count-the-number-of-powerful-integers/description/
本题要求选取数字处于 [start, finish] 范围内的数字 + 额外限制1 每位小于limit；额外限制2 必须以s为后缀

f(i, is_low, is_high):
    i 枚举位置 （从左往右）
    is_low 前面的数字是否都等于下界限制low 若是，当前位置不能低于当前位置的下界
    is_high                   上界                       高于

时间复杂度 状态*单个状态计算用时 = O(15) * 10
"""
from functools import cache


class Solution:
    def numberOfPowerfulInt(self, start: int, finish: int, limit: int, s: str) -> int:
        low, high = str(start), str(finish)
        n = len(high)
        low = '0' * (n - len(low)) + low  # 补前导零，和 high 对齐
        diff = n - len(s)

        ######################################
        # 4. 拓展 支持前导0 （主要参考写法）
        # is_num 前面是否填了非零数字
        @cache
        def dfs(i: int, limit_low: bool, limit_high: bool, is_num: bool) -> int:
            if i == n:
                return 1 if is_num else 0  # 看题目是否允许0

            res = 0
            # 额外多一个前导零通道, 此通道为本位填0用
            if not is_num and low[i] == "0":  # 全是前导零 一定有 limit_low = True
                if i < diff:  # 超过后缀就不允许从这里下降
                    res += dfs(i + 1, True, False, False)

            # 第 i 个数位可以从 lo 枚举到 hi
            # 如果对数位还有其它约束，应当只在下面的 for 循环做限制，不应修改 lo 或 hi
            lo = int(low[i]) if limit_low else 0
            hi = int(high[i]) if limit_high else 9

            res = 0
            d0 = 0 if is_num else 1  # 前导零改出时 [1,9] 其他时间无前导零 []
            if i < diff:  # 枚举这个数位填什么
                for d in range(max(d0, lo), min(hi, limit) + 1):
                    res += dfs(i + 1, limit_low and d == lo, limit_high and d == hi, True)
            else:  # 这个数位只能填 s[i-diff]
                x = int(s[i - diff])
                if max(lo, d0) <= x <= min(hi, limit):
                    res = dfs(i + 1, limit_low and x == lo, limit_high and x == hi, True)
            return res

        return dfs(0, True, True, True)


        low, high = str(start), str(finish)
        n = len(high)
        low = '0' * (n - len(low)) + low  # 补前导零，和 high 对齐
        diff = n - len(s)

        ######################################
        # 3. 根据下面的2模板 填充条件
        @cache
        def dfs(i: int, limit_low: bool, limit_high: bool) -> int:
            if i == n:
                return 1

            # 第 i 个数位可以从 lo 枚举到 hi
            # 此处逻辑不要修改, 如果对数位有其他约束 应当只在下面for循环枚举中做限制,不应修改 lo 或 hi,
            # 否则会影响下次递归后前缀是否受限制的逻辑 is_low/high
            lo = int(low[i]) if limit_low else 0  # 不受下限制 0-?
            hi = int(high[i]) if limit_high else 9  # 如果不收上方限制 ?-9   # hi=min(hi, limit)

            res = 0
            if i < diff:  # 未进入后缀s 枚举这个数位填什么
                for d in range(lo, min(hi,
                                       limit) + 1):  # 注意取limit不能在上面high 否则high变成limit 会让d==high 错误的认为当前位受到上界约束，假如下一位的限制小于limit 则会造成只取 hi_nxt] 而不是 limit]
                    res += dfs(i + 1, limit_low and d == lo, limit_high and d == hi)
            else:  # 进入后缀 这个数位只能填 s[i-diff]
                x = int(s[i - diff])
                if lo <= x <= min(hi, limit):
                    res = dfs(i + 1, limit_low and x == lo, limit_high and x == hi)
            return res

        return dfs(0, True, True)

        ######################################
        # 2. 支持下界的框架（在此之上结合题意填充）
        high = str(finish)  # 题目指定的枚举上界
        low = str(start)  # 下界
        n = len(high)
        low = "0" * (n - len(low)) + low  # 补上前导0

        def f(i, limit_low: bool, limit_high: bool) -> int:
            if i == n:
                return 1
            lo = int(low[i]) if limit_low else 0
            hi = int(high[i]) if limit_high else 9
            res = 0
            for d in range(lo, hi + 1):
                res += f(i + 1, limit_low and d == lo, limit_high and d == hi)
                # 同时满足 1.此前位都等于上/下界; 2.当前位选取上/下界 - 则下次递归受到上/下界约束
            return res
        return f(0, True, True)

        ######################################
        # 1. 最基础的框架（在此之上结合题意填充）
        high = str(finish)  # 题目指定的枚举上界
        def f(i, limit_high):
            if i == n:
                return 1

            lo = 0
            hi = int(high[i]) if limit_high else 9
            res = 0
            for d in range(lo, hi + 1):
                res += f(i + 1, limit_high and d == hi)  # 同时满足 1.此前位都等于上界; 2.当前位选取上界 - 则下次递归受到上界约束
            return res

        return f(0, True)