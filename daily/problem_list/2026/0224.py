"""
https://codeforces.com/problemset/problem/1991/C

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) 和长为 n 的数组 a(0≤a[i]≤1e9)。

你可以执行如下操作至多 40 次：
选择一个 [0,1e9] 中的整数 x，把每个 a[i] 变成 |a[i]-x|。
目标是把所有 a[i] 都变成 0。

如果无法做到，输出 -1。
否则输出两行，第一行输出操作次数，第二行输出每次操作的 x。
注意，你不需要最小化操作次数。
"""
import sys, itertools
from functools import cache
from heapq import heappop, heappush
from math import inf, isqrt, gcd
from bisect import bisect_left
from collections import deque, defaultdict

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

"""
结论题 缩小数字之间的距离 极差

ai = |ai-x| - 40

80 40 20 10
-60
20 20 40 50
-30
10 10 10 20
-15
5 5 5 5 

从例子入手观察规律 
    最后只有两个不一样的数 10 20 想办法减掉平均数 (他们到平均数的距离相等) 保留距离绝对值 
    以此类推 两两取平均数 只要能把两个归一 问题规模就缩减了 （只关心unique的数字)

-- 两数之差是奇数，则任何操作 他俩一直保持奇数差; 要求两数之差是偶数
    只要有奇偶同在就不行
    纯奇数/纯偶数
    
-- 至多40次
    如果从开头开始两两平均，对长1e5的必然不能覆盖
    考虑极差 最大最小取平均 
    d = (mx - mn)  
    
    x = (mx + mn) // 2 
    
    -x 将mn mx 缩到d
    
    
    对于其他任意 mn < a < mx 
    |a-x| <= |mn-x| = |mx-x| = d//2 -- a到区间中点x的距离 小于端点 [mn, mx] 到中点的距离 
    
    mx-x = mx - (mx + mn) // 2 = (mx-mn)//2 = d//2 
    mn-x ... d//2 
    
    一次操作 所有数落入 [0, d//2] 所以是log级别下降
    
直观理解这个过程
    -x 相当于求所有人到x 即mn mx 中点的距离，所有人向中点靠近一点. 然后只保留绝对值距离 
    为什么减半 - 直观说所有中线x下面的都翻上去了 保留了相等距离. 现在所有新的值 mn mx 都分布在原先一般的区间内 
    
    ref:
    https://chatgpt.com/c/699d2d8d-5fc8-8330-934b-4e95bd468d7d
"""

def solve(n, a):

    odd = sum(x%2==1 for x in a)
    if odd != 0 and odd != n:
        return "-1"


    res = []
    for _ in range(40): # 枚举logD次数 每次单独判断 mn mx
        mn = min(a)
        mx = max(a)

        # d = mx - mn
        if mn == mx == 0:
            break

        if mn == mx:
            res.append(mn)
            break
        else:
            x = (mn + mx)//2
            res.append(x)
            a = [abs(v-x) for v in a]

    return str(len(res)) + "\n" + " ".join(map(str, res))




for _ in range(RI()):
    n, a = RI(), RILIST()
    res = solve(n, a)
    print(res)


