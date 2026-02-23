"""
https://codeforces.com/problemset/problem/1209/D

输入 n(2≤n≤1e5) 和 k(1≤k≤1e5)。
有 k 个人，每个人都有两种喜欢的零食。零食编号从 1 到 n。
然后输入 k 行，每行两个不同的数，表示第 i 个人喜欢的两种零食的编号。

商店有 n 种零食，每种零食各一个，卖完就没了。
这 k 个人排队购买自己喜欢的所有零食。如果没有买到任何自己喜欢的零食，就会伤心。
请你排列这 k 个人的顺序，最小化伤心的人数。

- 思维题
- 前面的人能都买的会买俩，但即使有人能买一个也可以
    1-2-3-4
    (1,2) (2,3) (3,4)
    如果先选23 则只有1个能满足，如果选 12 34则两人，但本题可以 12 3 4 分配给所有人都买

- 抽象成图，喜好的两个零食是连边，零食是点，则人的喜好构成一张图。（存在两点中间多个边，但这样一定是有人买不到）
- 增长得看，假设我们已有构建最优顺序的序列


- 那么我们一共在这张图上插入了 k 条边。要让一个人不伤心，只需要保证他能买到至少一种自己喜欢的零食——也就是保证他这一条边连到的两个顶点中，有至少一个是“新”出现的

"""
import sys, random
from collections import defaultdict, deque

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x

n, k = RII()
fav = [tuple(RII()) for _ in range(k)]

pa = list(range(n))
def find(x):
    # if pa[x] == x:
    #     return x
    # pa[x] = find(pa[x])
    # return pa[x]

    # 非递归写法
    while pa[rt] != rt: # 1.先找根节点
        rt = pa[rt]

    while x != rt:  #2. 重定向到根节点
        tmp = pa[x]
        pa[x] = rt
        x = tmp
    return rt

def merge(x,y):
    x,y = find(x), find(y)
    if x == y:
        return 0
    else:
        pa[x] = y
        return 1
cnt = 0
for a,b in fav:
    a,b = a-1, b-1
    cnt += merge(a,b)
print(k - cnt)



