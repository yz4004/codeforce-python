"""
1. z函数模板
2. 利用z函数进行pattern/text字符串匹配
3. 利用z-box思想的 manacher 回文串匹配
4. 其他题单

参考
https://oi-wiki.org/string/z-func/
"""

"""
z-func原理
1. z[i]: 从i开始的字符串和从0开始的前缀的最大匹配前缀/最长公共前缀 LCP(s[i:], s[0:])
    (对比kmp中的 pi函数 是每个前缀的 s[:i] 最大匹配的前后缀
       
2. z-box 复用已经匹配的部分
    想象暴力，算出 s[i:]和前缀的匹配段后，开始算s[i+1:] 还要挨个循环一遍，但注意 s[i+1:...] 和之前 s[i+1:] 信息有一段公共部分
    lcp(s[i:], s) = l 
    s[0: l]
            s[i:i+l]
        所以当从i+1开始的时候，它其实就是对应s[1:].  s[1:l] 和 s[i+1:l] 这段是完全一样的, 而之前的z函数已经算过，所以从i+1开始的匹配可以先利用z[1]的信息
        可以跳到 i+min(z[1], i+l) 开始匹配
        我们称 s[i:i+l] 和前缀映射的部分叫z-box 用两个指针 [l,r] 维护
    
    算法
    1. 外层循环当前i,z[i] (从1开始）
    2. 每次从i匹配 根据自己所在的z-box 找左侧已匹配的相同段信息 复用/跳过 从右侧下一个开始匹配
    3. 更新z-box
"""

def z_func(s):
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n): #计算当前z[i:] 但s[i-1:] 已经和前缀有公共部分 s[0:l] 可以利用z[1]的信息，但这里我们使用lr指针，是为了推广这个状态机概念，manacher也可以用
        if i <= r:  # [l, r]  x-0 = i-l 当前i对应的从0前缀部分x=i-l； z-box [l,r] 是目前和前缀匹配/可复用z信息的部分
            z[i] = min(z[i - l], r - i + 1)
        while i + z[i] < n and s[i + z[i]] == s[z[i]]: #跳过, 匹配下一个
            l, r = i, i + z[i] #更新z-box 当前向右最大匹配范围
            z[i] += 1
    return z


"""
利用z-func进行字符串匹配
1. 如果进行pattern/text 匹配，构造 s = pattern  + "-" + text 后面的lcp(s[i:], s) 一旦等于pattern长度（只会等于，因为设置里分隔符）就找到了一个匹配
    分割符作用防止多余匹配（假如不是找第一个而是找全部 occurrence)
"""
class Solution:
    def strStr(self, text: str, pattern: str) -> int:
        # pattern + text， 找一个match的 z[i] 长度等于 pattern
        # 中间可以插一个分隔符 防止过长的无效匹配
        m = len(pattern)
        s = pattern + "." + text

        n = len(s)
        z = [0]*n
        l = r = 0
        for i in range(m+1, n):
            if i <= r: # [l, r]  x-0 = i-l
                z[i] = min(z[i-l], r-i+1)
            while i + z[i] < n and s[i + z[i]] == s[z[i]]:
                l, r = i, i + z[i]
                z[i] += 1
            if z[i] == m:
                return i
        return -1


    def z_func(self, s):
        n = len(s)
        z = [0]*n
        l = r = 0
        for i in range(1, n):
            if i <= r: # [l, r]  x-0 = i-l
                z[i] = min(z[i-l], r-i+1)
            while i + z[i] < n and s[i + z[i]] == s[z[i]]:
                l, r = i, i + z[i]
                z[i] += 1
        return z

"""
利用类似思路进行回文串匹配 manacher 算法
在padding/inertion/delimiter字符填充后
f[i] 以i为心的最大回文半径
    
  s[i-1] 
       s[i]
  显然已经计算了i-1/或是前面某个j为心的最大回文范围 我们记录半径为 [l,r] （类似z-box 信息可复用部分，l为其中心，r为最右段）
  i 处在右半边 [l,r] 根据l的对称部分是x [x,l] [l,i] 外侧两边等长所以有 l-x=i-l => x=2*l-i
  我可以复用 f[x=2*l-i] 的回文半径信息
  max(f[x=2*l-i], r-i+1)
  
"""
class Solution_lc647:
    def countSubstrings(self, s: str) -> int:
        #############################################
        #############################################
        # 样例
        # 012         0123
        # aba         abba
        # #a#b#a#     #a#b#b#a#
        # 0123456     012345678

        # n -> 2*n+1  原字符长n 变成2*n+1
        # i -> 2*i+1  原字符索引i -> 2*i+1

        # 最后算得z[i]对应了 2*n+1上的索引i 代表以i为中心的回文半径长度 （一半是填充#）

        # 模板输出的z-array
        # aba
        # #a#b#a#  padding-s
        # 1214121  z-array

        # abba
        # #a#b#b#a# padding-s
        # 121252121 z-array

        # 计算回文半径
        # 原字符串奇数（padding-s字母为中心） 【字母 #】 【字母 #】 ... 永远外层跟一个# 最后半径是偶数，除半刚好是原串上回文半径（算中心点）
        # 原字符串偶数（padding-s #为中心） 【#】 【字母 #】【字母 #】 ... 中心一个# 然后成对，外层#，除半下取整是原串上回文半径
        # 所以原字符 s[i] 为中心的回文半径为 z[2*i+1]//2

        # 计算原回文长度/判断[l,r]是否为回文子串
        # 给定 [l,r] 检查以其中心扩展的最长回文串长度 （超过lr即可）
        # z/halfLen -- z[i]-1 即为 [l,r] 中心扩展后的最长回文串 （上面奇数减去外侧，偶数减去中心）

        # 原字符 s[l,r] 是回文串:
        # z[l+r+1] >= r-l+1

        def manacher(s):
            n = len(s)
            t = ["#"] * (2 * n + 1)
            for i, c in enumerate(s):
                t[2 * i + 1] = c

            m = 2 * n + 1
            z = [1] * (2 * n + 1)  # g[i]
            l = r = 0
            #  [l, r] 沿着l对称 x-l = l-y    y=2*l-x
            for i in range(m):
                # [l,r]
                if i <= r:
                    z[i] = min(r - i + 1, z[2 * l - i])
                while i + z[i] < m and t[i + z[i]] == t[i - z[i]]:
                    l, r = i, i + z[i]
                    z[i] += 1
            return z  # 2*n+1

        z = manacher(s) # s[i] -- z[2*i+1]/z[2*i+2]分别对应以i为心的奇偶回文半径 -- 折半向下取整 z[2*i+1]/z[2*i+2] // 2

        def getPalindromDiameter(z, i):
            # z ~ padding-s 2*n+1
            return z[2 * i + 1] // 2

        def isPalindrome(l, r):
            # [l,r] -> [2*l+1, 2*r+1]  --- length = 2*r - 2*l + 1   --- mid = 2*l+1 + (length//2) = r+l+1
            # mid = l + r + 1
            return z[l + r + 1] >= r - l + 1
        #############################################
        return sum(x//2 for x in z)
        # 本题输出回文串数量，即每个最长的回文子串 拥有【回文半径长度】个子串，加起来即可

"""
待补充题单

3303. 第一个几乎相等子字符串的下标 
3327. 判断 DFS 字符串是否是回文串 (判断树的输出子串是回文串）
"""



def manacher(s):
    # Manacher 模板
    # 将 s 改造为 t，这样就不需要讨论 len(s) 的奇偶性，因为新串 t 的每个回文子串都是奇回文串（都有回文中心）
    # s 和 t 的下标转换关系：
    # (si+1)*2 = ti
    # ti/2-1 = si
    # ti 为偶数，对应奇回文串（从 2 开始）
    # ti 为奇数，对应偶回文串（从 3 开始）
    t = "#".join("^" + s + "$")

    # 定义一个奇回文串的回文半径=(长度+1)/2，即保留回文中心，去掉一侧后的剩余字符串的长度
    # half_len[i] 表示在 t 上的以 t[i] 为回文中心的最长回文子串的回文半径
    # 即 [i-half_len[i]+1,i+half_len[i]-1] 是 t 上的一个回文子串
    half_len = [0] * (len(t) - 2)
    half_len[1] = 1
    # box_r 表示当前右边界下标最大的回文子串的右边界下标+1
    # box_m 为该回文子串的中心位置，二者的关系为 r=mid+half_len[mid]
    box_m = box_r = max_i = 0
    for i in range(2, len(half_len)):
        hl = 1
        if i < box_r:
            # 记 i 关于 box_m 的对称位置 i'=box_m*2-i
            # 若以 i' 为中心的最长回文子串范围超出了以 box_m 为中心的回文串的范围（即 i+half_len[i'] >= box_r）
            # 则 half_len[i] 应先初始化为已知的回文半径 box_r-i，然后再继续暴力匹配
            # 否则 half_len[i] 与 half_len[i'] 相等
            hl = min(half_len[box_m * 2 - i], box_r - i)

        # 暴力扩展
        # 算法的复杂度取决于这部分执行的次数
        # 由于扩展之后 box_r 必然会更新（右移），且扩展的的次数就是 box_r 右移的次数
        # 因此算法的复杂度 = O(len(t)) = O(n)
        while t[i - hl] == t[i + hl]:
            hl += 1
            box_m, box_r = i, i + hl

        half_len[i] = hl
        if hl > half_len[max_i]:
            max_i = i

    hl = half_len[max_i]
    # 注意 t 上的最长回文子串的最左边和最右边都是 '#'
    # 所以要对应到 s，最长回文子串的下标是从 max_i-hl+2 到 max_i+hl-2
    # 结合上文的下标转换关系，得到其在 s 上的下标范围是从 (max_i-hl)/2 到 (max_i+hl)/2-2
    return s[(max_i - hl) // 2: (max_i + hl) // 2 - 1]