# from sortedcontainers import SortedList
from math import isqrt
from typing import List


def mo_queue_template(nums: List[int], queries: List[List[int]]) -> List[int]:
    n = len(nums)

    # 1. 这里可做些预处理 - 如离散化
    vals = sorted(set(nums))
    mp = {v: i for i, v in enumerate(vals, 1)}
    # [L,R]
    a = [mp[v] for v in nums]
    m = len(a)

    # 2. 分块尺寸
    b = isqrt(n) # 300

    # 3. 标准格式 对queries区间 按左端点所属的分块编号 做排序
    # 奇偶排序优化. 偶数块编号 按r升序. 奇数块编号 按r降序. 这样第一个块右端点递增后，可以在第二个块倒着处理. 而不是折返再从头扫
    def sort_key(x):
        idx, l, r = x
        return l // b, r if (l // b) % 2 == 0 else -r
    queries = [(idx, l, r) for idx, (l, r) in enumerate(queries)]
    queries.sort(key=sort_key)

    # 4. 当前处理区间 [cl,cr]
    cl, cr = 0, -1
    cnt_ = sum_ = 0 # 需要的维护的global值，取sum/cnt为例子
    def add_left(i):
        nonlocal sum_
        v = nums[i]
        # todo
        # 每次区间端点变化，对区间 [cl,cr] 内维护的对象的变化.
        # i = mp[x]
        # tree_cnt.add(i, 1) # 取树状数组维护 [cl,cr] 内值域/前缀和为例
        # tree_sum.add(i, x)

    def add_right(i):
        nonlocal sum_
        v = nums[i]
    def remove_left(i):
        nonlocal sum_
        v = nums[i]
    def remove_right(i):
        nonlocal sum_
        v = nums[i]

    res = [0] * len(queries)
    for idx, l, r in queries:

        while cl > l:
            cl -= 1
            add_left(cl)
        while cr < r:
            cr += 1
            add_right(cr)
        while cl < l:
            remove_left(cl)
            cl += 1
        while cr > r:
            remove_right(cr)
            cr -= 1

        # todo
        # 现在[cl,cr] 在 sqrt(n) 的时间得到维护. 利用被维护的对象输出查询
        # ...
        # res[idx] =
    return res

"""
https://chatgpt.com/c/69193a43-d09c-8329-a6ba-27807debbb91

非回退莫队/回滚莫队
    - 缩短窗口不好维护 则可类似分块那样 将左侧窗口独立出去计算 sqrt(n) 然后和右侧连续添加的部分拼合
    例如询问[l,r] 内相同数字之间最大距离 （left_most, right_most) 并不好回退 （也不好直接分块 因为没有浓缩信息）
    
    【算法讲解177【挺难】莫队专题2-回滚莫队、树上莫队】 https://www.bilibili.com/video/BV1Kvapz6EdZ/?share_source=copy_web&vd_source=6263f73035284da1cdd0caf558b11aef

树上莫队
    
    查询树上简单路径之间的unique数字 1e9
    （普通数组就是莫队去重，

"""