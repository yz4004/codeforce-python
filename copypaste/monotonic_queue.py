from collections import deque


def sliding_window_max_min(nums, k):
    # 维护滑窗内最值 - 静态
    # 1. 可以用RMQ/ST表静态查询
    # 2. 单调队列
    # https://leetcode.cn/problems/count-subarrays-with-cost-less-than-or-equal-to-k/

    n = len(nums)
    # 计算 (mx - mn) * (r-l+1) < k 的子数组数量. mx = max(nums[l,r])
    # (mx - mn) * (r-l+1) 随着l靠近r - 单调减小
    # 滑窗 + 维护窗口内最大最小值 - 单调队列维护滑窗内最值

    qmin = deque()
    qmax = deque()
    res = 0
    j = 0
    for i in range(n):
        x = nums[i]
        while qmin and qmin[-1][0] >= x:
            qmin.pop()

        while qmax and qmax[-1][0] <= x:
            qmax.pop()

        qmin.append((x, i))
        qmax.append((x, i))

        while j <= i and (qmax[0][0] - qmin[0][0]) * (i - j + 1) > k: # 非法左端点条件
            if qmin[0][1] == j:
                qmin.popleft()
            if qmax[0][1] == j:
                qmax.popleft()
            j += 1

        res += i - j + 1
    return res
