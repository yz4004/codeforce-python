from math import sqrt

EPS = 1e-7

EPS = 1e-7

"""
L2 norm
"""
def dist2(a, b):
    dx = a[0]-b[0]
    dy = a[1]-b[1]
    return dx*dx + dy*dy

"""
和差化积公式 
sum to product formula

    sin(a+b) = sina * cosb + cosa + sinb  - (sc + cs)
    cos(a+b) = cosa * cosb - sina + sinb  - (cc - ss)
     
"""
def sum_ab(cosa, sina, cosb, sinb):
    # sin(a+b), cos(a+b)
    sab = sina * cosb + cosa * sinb
    cab = cosa * cosb - sina * sinb
    return sab, cab

"""
给定两点+半径，找圆心
LC1453 https://leetcode.cn/problems/maximum-number-of-darts-inside-of-a-circular-dartboard/?envType=problem-list-v2&envId=1NRMDux1
"""
def centers_trig(A, B, r):
    x1, y1 = A
    x2, y2 = B
    dx = x2 - x1
    dy = y2 - y1
    d2 = dx * dx + dy * dy
    if d2 == 0:
        return [(x1, y1)]
    d = sqrt(d2)
    if d > 2 * r + EPS:
        return []

    # cosa = d/(2r), sina = sqrt(1-cosa^2)
    cosa = d / (2 * r)
    t = 1.0 - cosa * cosa
    if t < 0: t = 0.0
    sina = sqrt(t)

    cosb = dx / d
    sinb = dy / d

    # +alpha
    s1, c1 = sum_ab(cosa, sina, cosb, sinb)
    C1 = (x1 + c1 * r, y1 + s1 * r)

    # -alpha  (equivalent to flip sina -> -sina)
    s2, c2 = sum_ab(cosa, -sina, cosb, sinb)
    C2 = (x1 + c2 * r, y1 + s2 * r)

    return [C1, C2]


"""
向量
-- 
https://chatgpt.com/c/695b4e26-efd8-8333-96c0-4e8e720a1fad
"""
from dataclasses import dataclass
@dataclass(frozen=True)
class P:
    x: float
    y: float

    # vector ops
    def __add__(self, other: "P") -> "P": return P(self.x + other.x, self.y + other.y)
    def __sub__(self, other: "P") -> "P": return P(self.x - other.x, self.y - other.y)
    def __mul__(self, k: float) -> "P": return P(self.x * k, self.y * k)
    def __truediv__(self, k: float) -> "P": return P(self.x / k, self.y / k)

"""
向量点积
(x1,y1) * (x2,y2) = x1*x2 + y1*y2 
"""
def dot(a: P, b: P) -> float:
    """a · b"""
    return a.x*b.x + a.y*b.y

def cross(a: P, b: P) -> float:
    """a × b (2D scalar cross)"""
    return a.x*b.y - a.y*b.x

def norm2(a: P) -> float:
    """|a|^2"""
    return dot(a, a)

def norm(a: P) -> float:
    """|a|"""
    return sqrt(norm2(a))

def dist2(a: P, b: P) -> float:
    return norm2(a - b)

def dist(a: P, b: P) -> float:
    return norm(a - b)

def perp(a: P) -> P:
    """Rotate vector by +90°: (x,y)->(-y,x)"""
    return P(-a.y, a.x)

def rotate(a: P, theta: float) -> P:
    """Rotate vector by theta (radians) around origin"""
    c, s = cos(theta), sin(theta)
    return P(a.x*c - a.y*s, a.x*s + a.y*c)

def unit(a: P) -> P:
    """Unit vector; caller must ensure a != 0"""
    l = norm(a)
    return a / l