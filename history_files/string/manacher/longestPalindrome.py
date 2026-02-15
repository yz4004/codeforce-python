# s = str(input())
s = "aaabccccc" #输入
n = len(s)
t = ["#"] * (2 * n + 1) #填充占位符，只变成奇数情况两侧延展
for i in range(n):
    t[2 * i + 1] = s[i]

n = len(t)
z = [1]*n
l = r = -1 # 记录可以查询的最大回文直径
for i in range(n):
    # [l,r] 直径, i与之对称点 l+r-i:  两侧元素数 x-l == r-i
    if i <= r:
        z[i] = min(z[l+r-i], r-i+1) #注意也不能超过当前回文查询范围
    # z[i] i z[i]
    while i + z[i] < n and t[i+z[i]] == t[i-z[i]]:
        # l, r = i - z[i], i + z[i] 在这更新冗余，放下面，况且这个回文未必超过 l,r的范围
        z[i] += 1
    if i + z[i] - 1 > r: #z[i] 是最大半径，但i+r 是有效回文范围的下一个，别忘减1
        l, r = i - z[i] + 1, i + z[i] - 1

# #a# a #a#
# #a#a#
# 挡板字符永远包在实际字符外侧，永远比实际回文部分长1，所以实际最长回文 等于 最大半径减1
print(max(z)-1)










n = len(s)
t = ["#"] * (2 * n + 1)
for i in range(n):
    t[2 * i + 1] = s[i]

n = len(t)
z = [1]*n
l = r = -1
for i in range(n):
    # [l,r] 直径, i与之对称点 l+r-i:  两侧元素数 x-l == r-i
    if i <= r:
        z[i] = min(z[l+r-i], r-i+1)
    #  i z[i]
    while i + z[i] < n and t[i+z[i]] == t[i-z[i]]:
        l, r = i - z[i], i + z[i]
        z[i] += 1
# #a# a #a#
# #a#a#
print(max(z)-1)

print(z)
