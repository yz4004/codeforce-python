"""
https://codeforces.com/problemset/problem/2118/D2

输入 T(≤2e5) 表示 T 组数据。所有数据的 n 之和 ≤2e5，q 之和 ≤2e5。
每组数据输入 n(1≤n≤2e5) k(1≤k≤1e15)，长为 n 的严格递增数组 x(1≤x[i]≤1e15)，长为 n 的数组 d(0≤d[i]<k)。

一维数轴上有 n 个信号灯，坐标记录在 x 中。
位于 x[i] 的信号灯在第 d[i],d[i]+k,d[i]+2k,... 秒为红灯，其余时刻为绿灯。

然后输入 q(1≤q≤2e5) 和 q 个询问，每个询问输入 v(1≤v≤1e15)。
在第 0 秒，你位于坐标 v，面朝右。
每一秒，执行如下指令：
首先，如果当前位置有信号灯且为红灯，移动方向反向，否则移动方向不变。
然后，移动一个单位。

对于每个询问，判断能否移动出界，即移动到第一个信号灯的左边，或者最后一个信号灯的右边。
输出 YES 或 NO。

逃不出去的情况 - 从v出发撞到挡板，且从那个挡板出发反弹 无限反弹.
抽象成图 - 考虑每个挡板出发到 其他/最近的 碰撞挡板. 如果出不去就是环

xi -> xj 向右运动发生碰撞反弹 (右侧第一个xj)

    t + (xj-xi) = dj mod k  (初始时间 + 距离)

    从xi 出发的 本身也包含xi处发生碰撞 初始时间 t = di mod k

    di - xi = dj - xj mod k

xj <- xi

    t + (xi-xj) = dj mod k, where t=di mod k

    di + xi = xj + dj mod k


"""
import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict, deque
from math import inf

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

# print(-1%2) - 1
def get_circles(n, k, xs, ds):
    # n点，di mod k. [x1...xn] [d1...dn]

    # xi -> xj
    # di - xi = dj - xj mod k

    # xj <- xi
    # di + xi = xj + dj mod k

    rs = defaultdict(list)
    ls = defaultdict(list)
    for i, (x,d) in enumerate(zip(xs,ds)):
        rs[(d-x)%k].append(i)
        ls[(d+x)%k].append(i)
    # ls[t] 里的坐标 i1 i2... 满足任意ij. di + xi = xj + dj mod k. 则碰撞只会发生在相邻的坐标
    # 每个坐标 在两个方向上最多两个后继，避免稠密图

    # 左右方向的下一个碰撞
    ld = [-1]*n
    rd = [-1]*n
    ind = [[0]*2 for _ in range(n)] # (xi,0) 向左 (xi,1) 向右
    for tmp in ls.values():
        for i in range(1, len(tmp)):
            xj, xi = tmp[i-1], tmp[i]
            ld[xi] = xj
            ind[xj][1] += 1 # (xi,0) -> (xj,1) 然后 xj 向右反弹，入度应该是 xj 向右

    for tmp in rs.values():
        for i in range(len(tmp)-1):
            xi, xj = tmp[i], tmp[i+1]
            rd[xi] = xj
            ind[xj][0] += 1 # (xi,1) -> (xj,0)

    # 基环树 - 每个元素只有至多一个后继 （这里规定了反弹方向 实际图应该是 (i,+-1）点和入口方向)
    # 减去枝条即可，剩余自然就是环，本题不需要输出环，只需知道点在环上即可
    q = deque([(i,d) for i in range(n) for d in (0,1) if ind[i][d] == 0])
    while q:
        i,d = q.popleft()

        if d == 0 and ld[i] != -1:
            j = ld[i]
            ind[j][1] -= 1
            if ind[j][1] == 0:
                q.append((j, 1))
        if d == 1 and rd[i] != -1:
            j = rd[i]
            ind[j][0] -= 1
            if ind[j][0] == 0:
                q.append((j, 0))

    # 向左入射产生的环
    left_cycle = [ind[i][0] == 1 for i in range(n)] # ind[i][0] > 0
    return left_cycle

    # q = deque()
    # removed = [[False] * 2 for _ in range(n)]
    # for i in range(n):
    #     for d in (0, 1):
    #         if ind[i][d] == 0:
    #             q.append((i, d))
    #
    # while q:
    #     i, d = q.popleft()
    #     if removed[i][d]:       # 防止重复处理
    #         continue
    #     removed[i][d] = True
    #
    #     if d == 0 and ld[i] != -1:
    #         j = ld[i]           # (i,0)->(j,1)
    #         ind[j][1] -= 1
    #         if ind[j][1] == 0:
    #             q.append((j, 1))
    #     if d == 1 and rd[i] != -1:
    #         j = rd[i]           # (i,1)->(j,0)
    #         ind[j][0] -= 1
    #         if ind[j][0] == 0:
    #             q.append((j, 0))
    #
    # # 用 removed 判环最稳
    # left_cycle = [not removed[i][0] for i in range(n)]
    # return left_cycle



for _ in range(RI()):
    n, k = RII()
    xs = RILIST()
    ds = RILIST()
    # xi - di, di+k ... di+t*k

    left_cycle = get_circles(n, k, xs, ds)

    # 预处理：按 (x - d) % k 分桶，并保证桶内索引有序 因为顺序插入 已经有序
    hits = defaultdict(list)
    for i, (x, d) in enumerate(zip(xs, ds)):
        hits[(x - d) % k].append(i)

    RI()
    ans = []
    for v in RILIST():
        s = v % k
        if s not in hits:
            ans.append("YES")
            continue

        idx = bisect_left(xs, v)  # 右边界，从第一个 x >= v 的灯开始找
        vec = hits[s]

        pos = bisect_left(vec, idx)  # 桶内第一个 >= idx 的灯
        if pos == len(vec):
            ans.append("YES")  # 右侧没有可撞灯，直接出界
            continue
        j = vec[pos]  # 全局灯索引
        # 撞到 j 后立刻反向，下一步朝左 => 查 lefts[j]
        ans.append("NO" if left_cycle[j] else "YES")

    print("\n".join(ans))
