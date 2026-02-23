from collections import defaultdict

from sortedcontainers import SortedList


# 维护频次 + 维护众数/最大频次
# 利用了 mx +- 1 的平滑过渡特性 无需有序结构
class mode_maintainer:
    def __init__(self):
        self.freq = defaultdict(int) # x的频次
        self.cnt = defaultdict(int)  # 频次为x的元素有几种
        self.mx = 0 # 当前众数频次

    # 增加x的频率
    def add(self, x):
        t = self.freq[x]
        # 元素 x 的频率从 t 变为 t + 1
        self.freq[x] += 1
        if t > 0:
            self.cnt[t] -= 1
        self.cnt[t+1] += 1
        self.mx = max(self.mx, t+1)

    # 减少元素 x 的频率
    def remove(self, x):
        freq, cnt, mx = self.freq, self.cnt, self.mx
        t = freq[x]

        # 元素 x 的频率从 t 变为 t - 1
        freq[x] -= 1
        cnt[t] -= 1
        if t - 1 == 0:
            del freq[x]
        else:
            cnt[t-1] += 1

        # 如果这个t对应了 mx 且是唯一计数，则减x mx会平滑下降1
        if cnt[mx] == 0:
            self.mx -= 1

# 维护频次 + 维护众数/最大频次 - 维护最小的那个众数
# 利用了 mx +- 1 的平滑过渡特性 无需有序结构
# 应用: lc3636 莫队+众数
# https://leetcode.cn/problems/threshold-majority-queries/description/
class mode_maintainer1:
    def __init__(self):
        self.freq = defaultdict(int) # x的频次
        # self.cnt = defaultdict(int)  # 频次为x的元素有几种
        self.cnt = defaultdict(SortedList)  # 频次为x的元素的种类
        self.mx = 0 # 当前众数频次

    # 增加x的频率
    def add(self, x):
        t = self.freq[x]
        # 元素 x 的频率从 t 变为 t + 1
        self.freq[x] += 1
        if t > 0:
            self.cnt[t].remove(x)
        self.cnt[t+1].add(x)
        self.mx = max(self.mx, t+1)

    # 减少元素 x 的频率
    def remove(self, x):
        freq, cnt, mx = self.freq, self.cnt, self.mx
        t = freq[x]

        # 元素 x 的频率从 t 变为 t - 1
        freq[x] -= 1
        cnt[t].remove(x)
        if t - 1 == 0:
            del freq[x]
        else:
            cnt[t-1].add(x)

        # 如果这个t对应了 mx 且是唯一计数，则减x mx会平滑下降1
        if not cnt[mx]:
            self.mx -= 1



