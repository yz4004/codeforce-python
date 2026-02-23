"""
红蓝染色法
参考:https://leetcode.cn/problems/search-insert-position/solutions/2577719/zheng-li-mo-ban-by-dfthb-ses6/

返回第一个大于等于 target 的数的index

l, r, mid = (l+r) >> 1
以mid为界 将数组划分两部分 (mid待定)

红色 < target <= 蓝色

目的是要找蓝色部分的第一个数

（循环不变量） - r+1为最终值
l-1 总是指向 red
r+1 总是指向 blue
在闭区间 [l,r] 上搜索

[mid] < target
说明mid应在红色区域 (但 l = mid + 1
[mid] >= target
说明mid应在蓝色区域 (r = mid - 1)

为什么l = mid + 1
如果 l = mid 我们找第一个蓝，此时 l=mid 为红色，目标绝对不在 l 上，[l,r] 实际上是 (l,r] 变成半开区间
（l, r]
最后只有两个数时，向下取整会导致mid一直在l，而 l=mid，会死循环

（l=r]
只有一个元素，m也会一直在

因为是闭区间 [l,r] 所以搜索区间非空即 [l <= r]
while l <= r
循环截止条件是 l > r
此时 l = r + 1 (所以l 也是最终答案)


"""
import bisect
from typing import List


def lower_bound1(nums: List[int], target: int) -> int:
    # [l,r]
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = l + (r - l) >> 1
        if nums[mid] < target: # mid 红色
            l = mid + 1        # [mid+1, right]
        else:                  # mid 蓝色
            r = mid - 1        # [left, mid-1]
    return l # r+1



def lower_bound2(nums: List[int], target: int) -> int:
    # [l,r)
    # r一直指向蓝色
    l, r = 0, len(nums)
    while l < r:
        mid = l + (r - l) >> 1
        if nums[mid] < target:  # mid 红色
            l = mid + 1         # [mid+1, r)
        else:                   # mid 蓝色
            r = mid             # [left, mid)
    return l # r

def lower_bound3(nums: List[int], target: int) -> int:
    # (l,r)
    l, r = -1, len(nums)
    while l + 1 < r:
        mid = l + (r - l) >> 1
        if nums[mid] < target:  # mid 红色
            l = mid             # (mid, right)
        else:                   # mid 蓝色
            r = mid             # (left, mid)
    return l + 1   # r

"""
while 搜索区间非空时
所以退出while循环 最后一定是搜索区间为空
所以更新后的 l r 不应该指向循环不变量
l-1 r 才是不变量

"""

if __name__ == '__main__':
    pass

    bisect.bisect_left

    """
    bisect_left         返回大于等于x的第一个下标(相当于C++中的lower_bound)
    bisect/bisect_right 返回大于x的第一个下标(相当于C++中的upper_bound)，
                        也就是大于等于x的最后一个下标
                        
        想像一个连续的x段   ... x x x x ....
    
    bisect_left 返回最左侧的x
    bisect_right 返回最右侧的x的下一个位置
    
    如果数列中没有x       ... x-1 x+1 ...
    则两个都返回 x+1 的位置
    
    这篇文章列出了上面两个case，在有无x的情况下 bisec_left/right(x) 的行为
    https://blog.csdn.net/YMWM_/article/details/122378152
    """