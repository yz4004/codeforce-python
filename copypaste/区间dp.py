#
def isPalindrome(s):
    # 计算回文子串 s[i,j] f[i][j]=T/F
    """
    [i,j] <- i [i+1, j-1] j
    f[i][j] <- f[i+1][j-1]  要求里面先更新完毕
    1. 如选择外层遍历左端点i，内层j需要更新下列状态 [i,i+1] ... [i,n) 这要求大于i的左端点都更新过，所以i倒叙更新
    2. 边界情况, 从 f[i][i+1] 出发，上一个状态是 f[i+1][i]，则预处理为 True，且在i=n-1越界
    """
    n = len(s)
    f = [[False]*n for _ in range(n)]
    for i in range(n-1, -1, -1):
        f[i][i] = True
        if i+1<n: f[i+1][i] = True
        for j in range(i+1, n): # 所有的状态fij 都是合法状态，依赖在内部更是合法，只有在i=n-1时依赖状态会越界
            # [i,j] <- i [i+1, j-1] j
            f[i][j] = f[i+1][j-1] and s[i] == s[j]
    print(f)

    # 中心扩展式更新更好理解，虽然要从奇/偶两种中心出发

def longestPalindromeSubseq(s):
    """
    计算最长回文子序列 s[i,j] 对应区间内最长回文子序列
    1. 区间dp 状态仍对应闭区间端点。
    """
