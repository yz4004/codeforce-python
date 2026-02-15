"""
自定义堆排序
-- 自定义对象
-- 重写lt比较器
"""
import heapq

class MyObject:
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2

    def __lt__(self, other):
        # 自定义比较器: 按照 value2 进行比较
        return self.value2 < other.value2

    def __repr__(self):
        return f'MyObject(value1={self.value1}, value2={self.value2})'

# 创建一个 MyObject 的列表
data = [
    MyObject(1, 3),
    MyObject(2, 1),
    MyObject(3, 2)
]

# 将 MyObject 的列表转化为堆
heapq.heapify(data)

# 打印堆中的元素
while data:
    print(heapq.heappop(data))
