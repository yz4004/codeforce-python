import math

# 角度值转弧度制 [0,360] - [0, 2pi]
def angle_to_radian(a):
    # a是角度制 [0, 360)
    a = a % 360
    return (a / 180) * math.pi

# 将 (x,y) 映射为弧度制 (r, t) where x=r*cost y=r*sint
def polar_coordinate(x,y) -> (int, int): #返回 半径，极角 (0,2pi)
    r = math.sqrt(x * x + y * y) # 半径
    t = math.atan2((x,y))  # 极角 [0,2pi]
    return r,t

"""
ps: atan(y/x) 是原始的arctan定义 [-pi/2, pi/2] 涉及四个象限的讨论
例题 lc1610 可见点的最大数目讨论了手动应用 atan 求极角
"""