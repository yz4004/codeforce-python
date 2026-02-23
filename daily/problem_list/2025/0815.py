"""
https://codeforces.com/problemset/problem/551/E

输入 n(1≤n≤5e5) q(1≤q≤5e4) 和长为 n 的数组 a(1≤a[i]≤1e9)。

然后输入 q 个询问，格式如下：
"1 L R x"：把下标在闭区间 [L,R] 中的 a[i] 都增加 x(0≤x≤1e9)。注：a 的下标从 1 开始。
"2 y"：设 i 和 j 为元素 y(1≤y≤1e9) 在 a 中的最左下标和最右下标，输出 j-i。如果 a 中没有 y，输出 -1。

注：本题时间限制为 10s。提示分块 q*n^1/2



为什么线段树不行
- 查询x是否出现在区间 [l,r] 没有可提炼O(1)信息的做法

分块
每个块维护 1. 懒加值 2. 元素哈希表
操作1 - O(1) 操作2 - O(n^1/2)

"""
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x
MOD = 10 ** 9 + 7

n, Q = RII()
a = RILIST()

b = 300 #isqrt(n)
# [0, b) [b, 2b) ...
m = (n-1)//b + 1 
tags = [0]*m 

block_posi = [None]*m

def get_block_index(i):
    return i//b


def get_block_range(block_i):
    l = block_i * b
    r = mn(l+b, n)
    return l,r

def apply(block_i):
    t = tags[block_i]
    if t:
        tags[block_i] = 0
        l,r = get_block_range(block_i)
        for i in range(l,r): a[i] += t 
        
def shuffle(block_i):
    l,r = get_block_range(block_i)

    # 某人已经apply过
    # t = tag[block_i]
    # if t:
    #     tags[block_i] = 0
    #     for i in range(l,r): a[i] += t 
    
    posi = {}
    for i in range(l,r):
        x = a[i]
        if x in posi:
            posi[x][1] = i 
        else:
            posi[x] = [i,i]
    block_posi[block_i] = posi
        
# build blocks
for block_i in range(m):
    shuffle(block_i)
    
def add_partial(block_i, l,r,v):        
    # 指定block_i 添加 v [l,r]
    apply(block_i)
    
    for i in range(l,r+1):
        a[i] += v 
    shuffle(block_i)
    

def add(l,r,v): 
    bl, br = get_block_index(l), get_block_index(r)

    # 左侧block残余
    if l % b != 0: # 不是某个block的开头
        tmp_r = mn((l- l%b) + b, n) # 防止越界
        add_partial(bl, l, mn(r, tmp_r-1), v)
        bl += 1

    # 右侧block残余
    if bl <= br and (r+1) % b != 0:  # 不是某个block的结尾
        add_partial(br, r - r%b, r, v)
        br -= 1

    for bi in range(bl, br+1):
        tags[bi] += v 

def query(y):
    # 遍历blocks
    left_most = right_most = -1

    # 找最左块
    for bi in range(m):
        yt = y - tags[bi]
        posi = block_posi[bi]
        if yt in posi:
            left_most = posi[yt][0]     # 直接拿
            break

    # 找最右块
    for bi in range(m - 1, -1, -1):
        yt = y - tags[bi]
        posi = block_posi[bi]
        if yt in posi:
            right_most = posi[yt][1]    # 直接拿
            break

    if left_most == -1:
        print(-1)
    else:
        print(right_most - left_most)

for _ in range(Q):
    q = RILIST()
    if q[0] == 1:
        L,R,v = q[1]-1, q[2]-1, q[3]
        add(L,R,v)
    else:
        y = q[1]
        query(y)


sys.exit(0)
# ------------------------------

# block 信息
B = mx(1, isqrt(n)) # [b, 2b) ...
m = (n-1)//B + 1

tag = [0]*m
first = [{} for _ in range(m)]
last = [{} for _ in range(m)]

def brange(bi):
    L = bi * B
    R = mn((bi + 1) * B, n)-1
    return L, R # 闭区间 [L,R]

def push(bi):
    if not tag[bi]: return
    L, R = brange(bi)
    t = tag[bi]
    for i in range(L, R+1): a[i] += t
    tag[bi] = 0
    # rebuild(bi)

def rebuild(bi):
    L, R = brange(bi)
    f, g = {}, {}
    for i in range(L,R+1):
        x = a[i]
        if x not in f:
            f[x] = i
        g[x] = i
    first[bi], last[bi] = f, g

for bi in range(m):
    rebuild(bi)

def add(l, r, x):
    bl, br = l // B, r // B
    if bl == br: # 在同一块
        push(bl)
        for i in range(l,r+1): a[i] += x
        rebuild(bl)
        return

    # [l, bl*B) [...] [br*B, r]
    push(bl)
    for i in range(l, (bl + 1) * B): a[i] += x
    rebuild(bl)

    for bi in range(bl+1, br):
        tag[bi] += x

    push(br)
    for i in range(B * br, r+1): a[i] += x
    rebuild(br)


def query(y):
    left = -1
    for bi in range(m):
        v = y - tag[bi]
        # if v in first[bi]:
        #     left = first[bi][v]
        #     break
        fb = first[bi]
        if v in fb:
            left = fb[v]
            break

    if left == -1: return -1

    right = left
    for bi in range(m-1, -1, -1):
        v = y - tag[bi]
        # if v in last[bi]:
        #     right = last[bi][v]
        #     break

        lb = last[bi]
        if v in lb:
            right = lb[v]
            break
    return right - left


for _ in range(Q):
    t, *rest = RII()

    if t == 1:
        l, r, x = rest
        l, r = l-1, r-1

        # add
        # [0, b) [b, 2b) ...
        add(l,r,x)
    else:
        y,  = rest
        print(query(y))


