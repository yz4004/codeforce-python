from functools import cache


class Solution_LC3791:
    #
    # https://leetcode.cn/problems/number-of-balanced-integers-in-a-range/

    def countBalanced(self, low: int, high: int) -> int:
        # 奇/偶数位分别求和相等

        # 当有数位range [l,r] check(r) - check(l-1)
        def check(x): # check [0,x]
            if x < 10:
                return 0
            s = [int(c) for c in str(x)]
            m = len(s)

            @cache
            def f(i, diff, even, is_limit, is_num):
                if i == m:
                    return 1 if is_num and diff == 0 else 0

                res = 0
                if not is_num:
                    res = f(i + 1, 0, 0, False, False)

                # [lo,hi] 当前枚举范围. 如果有前导零，继续前导零走上面，进入合法数走下面for-loop最低位从1开始
                lo = 0 if is_num else 1
                hi = 9 if not is_limit else s[i]
                for d in range(lo, hi + 1):
                    cur = d if even else -d
                    res += f(i + 1, diff + cur, even ^ 1, is_limit and (d == hi), True)
                return res

            return f(0, 0, 0, True, False)

        return check(high) - check(low - 1)

"""
数位dp分类
https://chatgpt.com/c/695c30f8-5ff8-832d-9213-56f145584688

相邻无关 “全局累积量”相关（remainder / sums / counts）
    只需维护一个变量 最简单 
    （上例

相邻相关（1-step / Markov 型） 只和“上一位”有关，状态记 last 就能搞定。
    相邻不相等：d != last
    相邻差值限制：|d - last| <= k，或 d - last 必须属于某集合
    单调递增
    游程长度（run length）：不允许出现长度 ≥ L 的连续相同数字 - 状态记 (last, runLen)

短距离相关（k-step） 依赖最近 k 位（k 很小，比如 2、3、4），常见做法是“滑窗记忆”。
    例如
    禁止长度为 2/3 的子串：如不能出现 “13”，不能出现 “007”
    长度 2：记 last
    长度 3：记 last2 = lastTwoDigits 或记 (prev, last)

长距离相关但属于“正则语言”（Automaton / DFA 型）
    当约束是“包含/不包含某些模式串”“统计某些子串出现次数”，历史依赖可能很长，但可以用自动机状态压缩成有限个节点。
    kmp匹配

跨数位的算术耦合（Carry/Borrow DP）
    这类依赖不是“相邻数字模式”，而是加法/减法/乘法的进位/借位导致的跨位相关。它同样是“短距离依赖”，但依赖的是上一位的 carry。
    计数满足 x + y = S（或 x - y = S）的对数
    计数满足 x + reverse(x) 有某性质
    计数满足某种逐位运算结果（如逐位加和、带进位的规则）成立

    状态例子：
    f(pos, carry, tightX, tightY, startedX, startedY)
    （做两数/多数组合的 digit DP 时很常见）
    
题单
https://leetcode.cn/problems/count-of-integers/description/

markov形 记住前面短距状态
https://leetcode.cn/problems/total-waviness-of-numbers-in-range-ii/description/
"""