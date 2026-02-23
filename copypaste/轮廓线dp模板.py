


"""

参考 https://chatgpt.com/c/69633fe2-0e2c-8328-9276-9ab9d3c1bcaf

"""


from functools import cache
def profile_dp_recursive(grid, MOD=10**9+7):
    m, n = len(grid), len(grid[0])

    @cache
    def dfs(i, j, mask, carry, extra):
        """
        i, j: 当前处理的格子坐标（逐格推进）
        mask: 轮廓线状态（通常是按列的 bitmask，长度 n）
              包括前一行+当前行已更新过的部分
        carry: 当前行/当前格子相关的小状态（0/1 或小整数）
               常见：行内延伸、括号未闭合、当前段是否在进行等
        extra: 题目额外约束计数/标志（例如已用次数、已漏次数、组件数等）
        """

        # 1) 终止条件：扫完所有格子
        if i == m:
            # TODO: 返回是否接受该终态（通常是 1 或 0）
            return 1

        # 2) 计算下一个坐标（逐格推进）
        ni, nj = (i, j + 1) if j + 1 < n else (i + 1, 0)

        cell = grid[i][j]

        # 3) 行尾效应：在从 (i, n-1) 到 (i+1, 0) 时，对 carry 做换行处理
        # 常见：carry 必须清零（水平信息不跨行）
        ncarry = 0 if (j == n-1) else carry

        res = 0

        # 4) 根据 cell 类型（墙/空地/障碍等）分类
        if cell == 'x':
            # TODO: 更新规则（典型：切断通道）
            # 例如：清掉该列的 mask 位，carry 清零

            # 例
            nmask = mask | (1<<j)  # 引入j
            # nmask = mask & ~(1<<j) # 删除j
            nextra = extra
            # 换行时可能还需要额外处理

            res += dfs(ni, nj, nmask, ncarry, nextra)

        else:
            pass

        return res % MOD

    # 初始状态：mask=0, carry=0, extra=0（按题意调整）
    return dfs(0, 0, 0, 0, 0)


"""
例题 
lc 1411 - N*3 网格涂色 https://leetcode.cn/problems/number-of-ways-to-paint-n-3-grid/
https://codeforces.com/problemset/problem/845/F 士兵实现覆盖问题 0109 茶

"""
def cf_845f(m, n, mat):
    MOD = 10 ** 9 + 7

    # 至多一个1个空点没被监视
    # 全被监视/只有一个没被监视

    # s 左侧列视线
    # pre 当前列上方往下的视线
    @cache
    def f(s, pre, i, j, ok):
        if i == m:
            return 1

        if j+1 == n:
            ni, nj = i+1, 0
        else:
            ni, nj = i, j+1

        res = 0
        if mat[i][j] == ".":
            if pre == 0 and s >> j & 1 == 0:
                if ok == 0:
                    res += f(s, (pre if j+1 < n else 0) , ni, nj, ok+1) #
                # 这个ok不能合并到上面 否则ok=1会走下面 导致这个格子没被cover
                # 注意pre也有换行逻辑
            else:
                res += f(s, (pre if j+1 < n else 0), ni, nj, ok)

            # 布置士兵 同时有两种视线
            res += f(s | (1<<j), (1 if j+1 < n else 0), ni, nj, ok)

        else:
            ns = s ^ (s & (1 << j)) # 清除j列的s中的1
            res += f(ns, 0, ni, nj, ok)

        return res % MOD
    return f(0,  0, 0, 0, 0)