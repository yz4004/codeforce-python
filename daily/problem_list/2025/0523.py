"""
https://codeforces.com/problemset/problem/498/B

输入 n(1≤n≤5000) 和 T(1≤T≤5000)。
有 n 首歌，每首歌输入两个整数 pi(0≤pi≤100) 和 t(1≤t≤T)。

你在听歌识曲，按输入顺序依次播放。
每首歌从头开始听。每过一秒，识别出这首歌的概率是 p。在这首歌的第 t 秒，你可以立刻识别出这首歌。
成功识别后，立刻开始播放下一首歌。
注：相当于有 t 次抽卡机会，且第 t 次（最后一次）一定抽中。
注：如果所有歌曲都播放完毕，则识别结束，不会重复循环。

输出在 T 秒内识别出的歌曲个数的期望值。
与正确答案的绝对（相对）误差必须 ≤ 1e-6。

"""
import itertools
import sys

RI = lambda: int(sys.stdin.readline().strip())
RS = lambda: sys.stdin.readline().strip()
RII = lambda: map(int, sys.stdin.readline().strip().split())
RILIST = lambda: list(RII())
mx = lambda x, y: x if x > y else y
mn = lambda x, y: y if x > y else x


# def solve(a, T):
#     # f[i][j] 前i首歌 恰好j秒识别的概率
#     # i - p,t
#     # 1 2 3 ... t
#
#     # 1 p
#     # 2 (1-p) * p
#     # 3 (1-p)^2 * p
#     # ...
#     # j (1-p)^(j-1) * p
#
#     # t-1 (1-p)^(t-2) * p
#     # t  (1-p)^(t-1)
#
#     n = len(a)
#     f = [[0]*(T+1) for _ in range(n+1)]
#     f[0][0] = 1
#     for i, (p,t) in enumerate(a, 1):
#         for j in range(1, T+1):
#             for k in range(max(0, j-t), j):
#                 # k + d + 1 = j, d=0 1 ... t-1, k=j-1...j-t
#                 d = j-k-1  # d次失败 最后一次成功
#                 prob = ((1-p) ** d) * (p if d < t-1 else 1)
#                 f[i][j] += f[i-1][k] * prob
#         print(i, f[i])
#
#     # f[i][j] - 前i首歌 恰好js 识别完
#     # 求前Ts 识别的歌的期望 = sum(识别i首 * 前Ts恰好识别i首的概率)
#     res = sum(
#         f[i][j]
#         for i in range(1, n + 1)
#         for j in range(0, T + 1)
#     )
#     return res


# def solve(a, T):
#     # f[i][j] 前i首歌 恰好j秒识别的概率
#     n = len(a)
#     f = [[0]*(T+1) for _ in range(n+1)]
#     f[0][0] = 1.0
#
#     # probs[i] = (1-p) ** i
#     for i, (p,t) in enumerate(a, 1):
#
#         if p == 1.0: # 每次识别都百分百成功
#             for j in range(1, T+1):
#                 f[i][j] = f[i-1][j-1]
#             continue
#
#         inv = 1.0 - p
#         p_j = [1] * (T + 1)
#         p_k = [1] * (T + 1)
#         for d in range(1, T + 1):
#             p_j[d] = p_j[d - 1] * inv
#             p_k[d] = p_k[d - 1] / inv
#
#         # f[i-1][k] * (1-p) ^ (-k)
#         g = [f[i-1][k] * p_k[k] for k in range(T+1)]
#         ps_g = list(itertools.accumulate(g, initial=0.0))
#         # k [j-t+1, j-1]
#
#         for j in range(1, T+1):
#             if j - t >= 0:
#                 f[i][j] = p * p_j[j-1] * (ps_g[j] - ps_g[j-t+1]) + f[i-1][j-t] * p_j[t-1]
#             else:
#                 f[i][j] = p * p_j[j-1] * ps_g[j]
#
#     # f[i][j] - 前i首歌 恰好js 识别完
#     # 求前Ts 识别的歌的期望 = sum(识别i首 * 前Ts恰好识别i首的概率)
#     res = sum(
#         f[i][j]
#         for i in range(1, n + 1)
#         for j in range(0, T + 1)
#     )
#     return res

# def solve(a, T):
#     # f[i][j] 前i首歌 恰好j秒识别的概率
#     n = len(a)
#     f = [[0]*(T+1) for _ in range(n+1)]
#     f[0][0] = 1.0
#
#     # probs[i] = (1-p) ** i
#     for i, (p,t) in enumerate(a, 1):
#
#         if p == 1.0: # 每次识别都百分百成功
#             for j in range(1, T+1):
#                 f[i][j] = f[i-1][j-1]
#             continue
#
#         if p == 0: # 每次识别都百分百失败
#             for j in range(t, T+1):
#                 f[i][j] = f[i-1][j-t]
#             continue
#
#         if t == 1:
#             # 无论 p 是多少，只有一次机会必中
#             for j in range(1, T + 1):
#                 f[i][j] = f[i - 1][j - 1]
#             continue
#
#         for j in range(1, T+1):
#             # 先扣掉 d=t-1 的那一项，window = sum_{d=0..t-2} f[i-1][j-1-d]*(1-p)^d
#             if j >= t:
#                 window = f[i][j - 1] - f[i - 1][j - t] * (1 - p) ** (t - 1)
#             else:
#                 window = f[i][j - 1]
#             # 滑动后乘 (1-p)
#             window *= (1 - p)
#             # 加上“最后一次必中”的那一项
#             if j >= t:
#                 window += f[i - 1][j - t] * (1 - p) ** (t - 1)
#             # 再加上“本秒抽中”的新贡献
#             f[i][j] = window + f[i - 1][j - 1] * p
#
#     # f[i][j] - 前i首歌 恰好js 识别完
#     # 求前Ts 识别的歌的期望 = sum(识别i首 * 前Ts恰好识别i首的概率)
#     # print(f)
#     res = sum(
#         f[i][j]
#         for i in range(1, n + 1)
#         for j in range(0, T + 1)
#     )
#     return res

def solve(a, T):
    n = len(a)
    # f[i][j] = Pr( exactly i songs done at time j )
    f = [[0.0]*(T+1) for _ in range(n+1)]
    f[0][0] = 1.0

    for i, (p, t) in enumerate(a, start=1):
        inv = 1.0 - p
        # Special‐case p=1 in one line:
        if p == 1.0:
            for j in range(1, T+1):
                f[i][j] = f[i-1][j-1]
            continue

        # Precompute inv^(t-1), the forced‐success factor.
        inv_pow = inv**(t-1)

        c = [0.0] * (T + 1)
        c[0] = f[i - 1][0]
        for j in range(1, T + 1):
            c[j] = f[i - 1][j] + c[j - 1] * inv

        # 用两项公式填 f[i][j]
        for j in range(1, T + 1):
            # d = 0..t-2 部分
            if j >= t:
                window = c[j - 1] - inv_pow * c[j - t]
            else:
                window = c[j - 1]
            term1 = p * window

            # d = t-1 强制必中部分
            term2 = inv_pow * f[i - 1][j - t] if j >= t else 0.0

            f[i][j] = term1 + term2

    # The expected number is simply ∑_{i=1..n} ∑_{j=0..T} f[i][j]
    return sum(f[i][j] for i in range(1, n+1) for j in range(T+1))

n, T = RII()
a = []
for _ in range(n):
    p, t = RII()
    a.append((p/100,t))
print(solve(a, T))