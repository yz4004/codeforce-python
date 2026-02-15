"""
kmp 记录所有text中pattern出现的位置

生成pattern最大前后缀匹配
    稳定循环指针是pattern以i为结尾的前缀
    动态指针是（上一个）pattern前缀匹配的 【最大匹配前后缀长度】

计算pattern在文本中的匹配
    稳定循环指针是文本指针 text[i:] vs pattern[cnt:]
"""

def kmp(pattern, text):
    m, n = len(pattern), len(text)
    # 1. 对于pattern[,i] 计算最大前缀后缀匹配长度 pi[i] - pattern[,i] 截止到i，循环跳过首字母
    pi = [0] * m
    cnt = 0  # 动态指针，维持当前遍历前缀的最大前后缀匹配长度
    for i in range(1, m):
        # 1.1 如果不匹配 则不断缩减直到匹配
        while cnt and pattern[i] != pattern[cnt]:
            cnt = pi[cnt - 1]
        # 1.2 延展当前长度 （cnt=0时有可能不进入if）
        if pattern[i] == pattern[cnt]:
            cnt += 1
        pi[i] = cnt  # pi[i] 对应以i结尾的 pattern [0,i] 的前后匹配

    res = []

    # 2. text[i:] 匹配 pattern[cnt:]
    cnt = 0  # 动态指针，模式串上的匹配位置
    for i in range(n):
        # 2.1 如果不匹配 模式串指针动
        while cnt and text[i] != pattern[cnt]:
            cnt = pi[cnt - 1]

        # 2.2 如果匹配 i/cnt 各进一步
        if text[i] == pattern[cnt]:
            cnt += 1

        # 2.3 匹配完成 记录一段结果 重置模式串动态指针 （不是重置到0）
        if cnt == m:
            res.append(i - cnt + 1)
            # cnt = 0 这里不应该重置0 而是对pattern的整体匹配前后缀回退
            cnt = pi[cnt - 1]
    return res


"""
为什么是最长匹配前后缀 - 这样回退最短

找到匹配前后缀后，相当于把模式串根据这个匹配部分对应到文本串上

1. 发生失配
... 【匹配的部分    】x ...
    【匹配的部分    】y ...
 
2. 考虑最长匹配前后缀 
... 【     _______】x ...
    【_______     】y ...
    最长的匹配前后缀
    按照这段去拉齐，效果上patten上待与文本匹配的第一个指针从原来指向y 
    回退到了最大匹配前后缀 （___部分___） 的下一个字符，去匹配x
    实际上回退的部分是 最大匹配前后缀 以外的部分

3. 重新尝试匹配
... 【     _______】x ...
         【_______     】y ...
        如果这段也没匹配成功，再对这段的最大匹配前后缀回退（实际上是上面的次大匹配前后缀，回退的更多了）
   
   
测试
lc28
lc3008
"""