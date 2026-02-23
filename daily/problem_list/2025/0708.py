"""
https://codeforces.com/problemset/problem/2110/C

输入 T(≤1e4) 表示 T 组数据。所有数据的 n 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) 和长为 n 的数组 d(-1≤d[i]≤1)。
然后输入 n 个闭区间 [li,ri]，范围 [0,n]。

你需要把数组 d 中的每个 -1 改成 0 或者 1。
然后计算 d 的前缀和数组 s（即 d 的前 i 个数之和），要求满足 li <= si <= ri。

输出任意一个符合要求的修改后的 d。
无解输出 -1。

"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

for _ in range(RI()):
    n, nums = RI(), RILIST()
    queries = [RII() for _ in range(n)]
    #print(n, nums)

    invalid = False
    s = 0
    xl = xr = 0 # 1的数量上下界
    tmp = []
    for i in range(n):
        l,r = queries[i]
        if nums[i] == -1:
            xr = xr+1
        else:
            s += nums[i]

        # [l-s, r-s]
        # cnt=x+y 其中x个1  x in [l-s, r-s]

        l, r = l-s, r-s
        # [xl, xr], [l,r]
        if xr < l or r < xl:
            invalid = True
            break
        xl = mx(xl, l)
        xr = mn(xr, r)
        tmp.append((xl,xr)) # 1的数量

    # print(tmp)
    if invalid:
        print("-1")
    else:
        cur = tmp[-1][1] # 最大可填
        for i in range(n-1, -1, -1):
            l,r = tmp.pop()
            if nums[i] != -1:
                continue
            # [,i] 填入的1应该满足 [l,r] 数量
            # 但假如前一个-1 对应的限制是 [l,...] 则前面也至少是l个1 当前不能填1
            # 前面的上界则不会影响当前，因为r是前面取过mn的结果

            pre_l = tmp[-1][0] if tmp else 0

            # if l != pre_l:
            if cur - 1 >= pre_l:
                cur -= 1
                nums[i] = 1
            else:
                nums[i] = 0

        print(" ".join(map(str, nums)))