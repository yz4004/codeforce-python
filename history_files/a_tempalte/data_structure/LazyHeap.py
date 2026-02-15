import heapq
from collections import defaultdict
class LazyHeap:
    def __init__(self):
        self.heap = []
        self.todo = defaultdict(int) #懒删除用，如果todo[v] > 0 说明需要删除todo[v]个v
        self.size = 0 # 堆的actual size
        self.sum = 0 # 堆的元素和（可结合题维护其他变量）

    def push(self, v):
        if self.todo[v] > 0:
            self.todo[v] -= 1 #少删一个 刀下留人
        else:
            heapq.heappush(self.heap, v) ##### min_heap #####
        self.size += 1
        self.sum += v

    def pop(self):
        self._clean()
        v = heapq.heappop(self.heap) ##### min_heap #####
        self.size -= 1
        self.sum -= v
        return v

    def top(self):
        self._clean()
        return self.heap[0] ##### min_heap #####

    def delete(self, v):
        self.todo[v] += 1
        self.size -= 1
        self.sum -= v

    def _clean(self): #堆顶todo>0 需要删除
        while self.heap and self.todo[self.heap[0]] > 0: ##### min_heap #####
            self.todo[self.heap[0]] -= 1  ##### min_heap #####
            heapq.heappop(self.heap)
"""
包装懒删除操作
1. 待删除的部分加入todo 由delete函数加入
2. 在pop/top 前执行 clean
3. 默认维护min_heap 小的在上，如果维护大根堆，手动推入负数 必要时需要自定义定义排序对象重写lt方法

lc 3013 用两个堆顶堆维护滑动窗口内k-1小的元素
"""

# 自定义排序对象，lc2102 所需
class Node0: # 自定义小根堆排序对象（符合题意描述的排序）
    def __init__(self, score:int, name:str):
        self.score = score
        self.name = name
    def __repr__(self):
        return f'{self.score, self.name}'
    def __lt__(self, other):
        if self.score == other.score:
            return self.name > other.name #名字大的排后面
        return self.score < other.score #分数小的排后面
class Node1: #大根堆对象，和上面取反
    def __init__(self, score:int, name:str):
        self.score = score
        self.name = name
    def __repr__(self):
        return f'--{self.score, self.name}'
    def __lt__(self, other):
        if self.score == other.score:
            return self.name < other.name
        return self.score > other.score
