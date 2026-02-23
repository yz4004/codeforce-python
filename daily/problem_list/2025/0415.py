"""
https://atcoder.jp/contests/abc347/tasks/abc347_d

输入 a(0≤a≤60) b(0≤b≤60) 和 xor(0≤xor<2^60)。

构造两个在 [0,2^60) 中的整数 x 和 y，满足 x 的二进制中有 a 个 1，y 的二进制中有 b 个 1，且 x 异或 y 等于 xor。

输出 x 和 y。
多解输出任意解。
如果无法构造，输出 -1。

分配比特，xor为1的是对应位置有一人，其余大家个凑d个bit抵消，则有下面公式，需要保持有正整数解
0b11100 -- x
0b11011 -- y
  0b111 -- x^y

d + d1 = a      # x 中与 y 同位为 1 的位数 + x 独有的位数
d + d2 = b      # 同理，y 的 1 总数 = 与 x 相同的位 + y 独有的位
d1 + d2 = c     # c 为 t 中 1 的个数（即 xor 后的不同位数） (c = xor.bit_count())

d1 = (c+a-b)/2
d2 = (c+b-a)/2
d = a - d1
三个都需要正整数
"""
import sys, itertools
from math import inf, isqrt, gcd
from bisect import bisect_left
from collections import deque, defaultdict
RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

a, b, t = RII()


def solve(a,b,t):
    # d + d1 = a
    # d + d2 = b
    # d1 + d2 = c = xor.bit_count()
    c = t.bit_count()

    # 判断三个正整数
    if (c+a-b) % 2 == 1 or c + min(a - b, b - a) < 0 or (a+b) - c < 0:
        return -1

    d1 = (c + a - b) // 2
    d2 = (c + b - a) // 2
    d = a - d1

    # print(d1, d2, d)
    x = y = 0
    for i in range(60):
        if t >> i & 1 == 1:
            if d1 > 0:
                d1 -= 1
                x |= (1 << i)
            elif d2 > 0:
                d2 -= 1
                y |= (1 << i)
        elif d > 0:
            x |= (1 << i)
            y |= (1 << i)
            d -= 1
    # if d1 != 0 or d2 != 0 or d != 0:
    #     return -1
    if d != 0: # 本题有2^60限制，d可能用不完也要报错
        return -1
    return x, y
# a = 60
# b = 0
# t = (1 << 60) - 1
res = solve(a,b,t)
if res == -1:
    print(res)
else:
    print(" ".join(map(str, res)))


# 随机生成器构造测试用例
import random
def generate_case():
    a = random.randint(0, 60)
    b = random.randint(0, 60)
    t = random.getrandbits(60)  # 生成 [0, 2^60) 的随机数
    return a, b, t

def is_valid_solution(a, b, t, x, y):
    if x ^ y != t:
        return False, f"xor mismatch: x^y = {x^y}, expected {t}"
    if bin(x).count("1") != a:
        return False, f"x bit count mismatch: {bin(x).count('1')} != {a}"
    if bin(y).count("1") != b:
        return False, f"y bit count mismatch: {bin(y).count('1')} != {b}"
    if not (0 <= x < (1 << 60)) or not (0 <= y < (1 << 60)):
        return False, "x or y out of range"
    return True, ""

def test_random_cases(num_tests=10000):
    for i in range(num_tests):
        a, b, t = generate_case()
        res = solve(a, b, t)
        if res == -1:
            # brute force check if it's truly unsolvable (skip for now)
            continue
        else:
            x, y = res
            ok, msg = is_valid_solution(a, b, t, x, y)
            if not ok:
                print(f"❌ Failed on case {i+1}")
                print(f"a={a}, b={b}, t={t}")
                print(f"x={x}, y={y}")
                print(msg)
                break
    else:
        print(f"✅ Passed {num_tests} random cases")

# Run it
test_random_cases()