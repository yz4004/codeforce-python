from typing import List

######################################################################################################################
######################################################################################################################
"""
andrew 单调栈+向量叉乘 求凸包
例题：LC587 https://leetcode.cn/problems/erect-the-fence/description/
"""
def convex_hull_andrew(p: List[List]):
    def cross(a, b):
        # 对两向量 a=(x1,y1), b=(x2,y2) 做差乘 x1*y2 - x2*y1
        # return a * b
        return a[0] * b[1] - a[1] * b[0]

    def sub(a, b):
        # 向量减法 a - b, b -> a
        return a[0] - b[0], a[1] - b[1]

    p.sort()
    n = len(p)
    if n == 1:
        return p
    stk = [0]  # 单调栈存下标; 0 提前入栈，而不标记used 因为最后计算上凸包时要访问一次
    used = [False] * n

    # 先求下凸壳 - lower convex hull
    # 新的右侧点要不断往下拐.
    # stk[-2] -> stk[-1] -> new_x 三点形成两个向量, 向量箭头向右，（因为按横坐标排序）
    # stk[-2] -> stk[-1] 以该向量方向为界. 观察 stk[-1] -> new_x, 向上的即为保持凸性，向下则不满足凸性质
    # 所谓的上下，根据左手定则/叉积符号可以判断，食指顺向量弯曲，大拇指纸面向外, 叉积<0 向下， <= 0 是共线在凸壳上
    # 如果是下，不满足凸性，说明栈顶stk[-1] 实际上不在下凸边界里，弹出
    for i in range(1, n):
        x = p[i]
        while len(stk) >= 2 and cross(sub(p[stk[-2]], p[stk[-1]]), sub(p[stk[-1]], x)) < 0:
            d = stk.pop()
            used[d] = False # 不在下凸壳，有可能在上凸壳
        stk.append(i)
        used[i] = True

    # print([p[i] for i in stk])
    # 计算上凸壳
    # 此时在栈中的是下凸壳全体
    tmp = len(stk) # 全体下凸壳，包括最后一个点n-1一定是下凸壳的结束
    for i in range(n - 2, -1, -1):
        x = p[i]
        if not used[i]:
            while len(stk) >= tmp + 1 and cross(sub(p[stk[-2]], p[stk[-1]]), sub(p[stk[-1]], x)) < 0:
                d = stk.pop()
                used[d] = False
            stk.append(i)
            used[i] = True

    return [p[i] for i in stk[:-1]]

######################################################################################################################
######################################################################################################################
# point 结构体定义替代tuple
# def convex_hull(p: List[Point]):
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):  # 向量减法 subtract
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):  # 叉积 multiply
        return self.x * other.y - self.y * other.x

    def __lt__(self, other):  # 排序 less than, 先按横坐标 再按纵坐标
        return (self.x, self.y) < (other.x, other.y)

    def __repr__(self):  # 打印方便调试
        return f"({self.x}, {self.y})"
