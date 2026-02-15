class LazyTree:
    def __init__(self, nums):
        n = len(nums)
        self.nums = nums
        self.t = [0]*(4*n)
        self.todo = [0]*(4*n)


    """ initialization： p,l,r = 1,0,n-1"""
    def build(self, p, l, r):
        if l == r:
            #
            return
        mid = (l+r)//2
        self.build(2*p. l, mid)
        self.build(2*p+1, mid+1, r)
        # merge

    """ [left, right] 上加v"""
    def update(self, p, l, r, left, right, v):
        if left <= l and r <= right:
            self.todo[p] += v
            return
        # 传递lazy tag 如果需要递归更新，则本层lazy tag置为0 然后让左右子区间更新
        if self.todo[p] != 0:
            self.todo[p*2] += self.todo[p]
            self.todo[p*2+1] += self.todo[p]
            self.todo[p] = 0
        mid = (l + r) //2
        if left <= mid: #如果mid左侧包含一部分要更新的区间 [left,mid]
            self.update(2*p, l, mid, left, right, v)
        if mid < right: #如果mid包含一部分要更新的区间 [mid+1,right] 递归
            self.update(2*p+1, mid+1, r, left, right, v)

    def query(self, p, l, r, left, right):
        pass
