"""
https://codeforces.com/problemset/problem/1739/B

输入 T(≤100) 表示 T 组数据。
每组数据输入 n(1≤n≤100) 和长为 n 的数组 d(0≤d[i]≤100)。

下标从 1 开始。
d 是由某个非负整数数组 a 按照如下规则生成的：
d[1] = a[1]
d[2] = |a[2] - a[1]|
...
d[i] = |a[i] - a[i-1]|

如果只有一个符合要求的数组 a，输出 a。
否则输出 -1。
"""
import sys, itertools

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
max_ = lambda x, y: x if x > y else y
min_ = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

"""
直接构造 - 前缀和

    下面这段是在判断“是否唯一”
    如果唯一，则答案一定是前缀和构造：a = [d1, d1+d2, d1+d2+d3, ...]
    
    为什么？
    对于每一步 i>=2，已知 a[i-1] 和 d[i]，a[i] 有两个候选：
      a[i] = a[i-1] + d[i]
      a[i] = a[i-1] - d[i]   (前提是 a[i-1] >= d[i]，且当 d[i]>0 时会形成另一个不同解)
    
    要想“唯一”，就必须在每一步都不能选减法（或减法与加法相同，即 d[i]=0）。
    换句话说，需要保证当前前缀和严格小于后续某个 d，使得“减法会变负数”。
    
    你的这段判定等价于检查是否存在某个位置会产生歧义。
    一旦出现歧义，就返回 -1。
"""



def solve(n, d):
    if n == 1:
        return str(d[0])

    a = [str(d[0])] * n
    s = d[0]
    for i in range(1, n):
        x = d[i]
        if x != 0 and s - x >= 0:
            # in this case we can come up with a construct that
            # this one choose -x and choose + for rest of the suffix - still positive
            return "-1"
        s += x
        a[i] = str(s)
    return " ".join(map(str, a))


for _ in range(RI()):
    n, d = RI(), RILIST()
    print(solve(n, d))

