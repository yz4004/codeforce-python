from math import inf


"""
将nums中的数装进一些容量为t的桶，求用桶最少的数量
"""
def minimal_bucket_usage(nums, t):
    n = len(nums)

    if any(x > t for x in nums): # 如果有超过容量的，则下面会无限递归
        return -1

    all_path = []

    def dfs(i, used, u, path):
        print((i, used, u, path))
        if all(used):
            all_path.append([p[:] for p in path])
            return 0

        if all(nums[i] > u for i in range(n) if not used[i]):
            path.append([])
            res = dfs(0, used, t, path) + 1
            path.pop()
            return res
            # return dfs(0, used, t, left, path + [[]]) + 1

        res = inf
        for j in range(i, n):
            if not used[j] and nums[j] <= u:
                used[j] = True
                path[-1].append(j)
                res = min(res, dfs(j+1, used, u - nums[j], path))
                path[-1].pop()
                used[j] = False
        return res

    res = dfs(0, [False]*n, t, [[]])
    print(all_path)
    return res

"""

    [2 2 2 2] t=4
     0 1 2 3
    上面的无剪枝枚举 选或不选没有任何条件，所有的任意下标的路径的2都会组合尝试一次
    minimal_bucket_usage([2,2,2,2], 4)
        [[[0, 1], [2, 3]], 
        [[0, 2], [1, 3]], 
        [[0, 3], [1, 2]],
        [[1, 2], [0, 3]], 
        [[1, 3], [0, 2]], 
        [[2, 3], [0, 1]]]
"""


