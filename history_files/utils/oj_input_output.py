"""
输入输出
https://blog.csdn.net/justidle/article/details/104706316
官方
https://help.luogu.com.cn/manual/luogu/problem/testcase-config

a = list(map(lambda x:int(x), input().split())) #直接在命令行输入若干隔开的数字 回车即可
print(a)
# console log:

还有多行输入的例子
"""

ans = []
while True:
    try:
        x = input()
        if x == "eof": break #手动输入一个eof ctrl+z可能不会被传导过去
        ans.append(int(x))
    except EOFError:
        print("报错信息")
        print(EOFError)
        break
# oj 会在最后输入 EOF 代表文件结尾
# 本地运行命令行交互时，多敲一个回车会结束输入
print(ans)