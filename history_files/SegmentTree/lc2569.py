from typing import List


class Solution:
    def handleQuery(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:

        n = len(nums1)
        a = [0]*(4*n)
        todo = [0] * (4 * n)
        def build(p, l, r):
            if l == r:
                a[p] = nums1[l]
                return
            mid = (l+r)//2
            build(2*p, l, mid)
            build(2*p+1, mid+1, r)
            a[p] = a[2*p] + a[2*p+1]
        build(1, 0, n-1)

        # # (left, right) 計入一次翻轉
        # def update1(p, l, r, left, right):
        #     if left <= l and r <= right:
        #         a[p] = (r-l+1) - a[p]
        #         return
        #
        #     # if l == r: # tle
        #     #     a[p] ^= 1
        #     #     return
        #
        #     mid = (l + r) // 2
        #     if left <= mid:
        #         update1(2*p, l, mid, left, right)
        #     if mid < right:
        #         update1(2*p+1, mid+1, r, left, right)
        #     a[p] = a[2*p] + a[2*p+1]

        # (left, right) 計入一次翻轉
        def update1(p, l, r, left, right):
            if left <= l and r <= right:
                todo[p] ^= 1
                a[p] = (r - l + 1) - a[p]
                return

            mid = (l + r) // 2
            todo[p] = 0
            if left <= mid:
                update1(2 * p, l, mid, left, right)
            if mid < right:
                update1(2 * p + 1, mid + 1, r, left, right)
            a[p] = a[2 * p] + a[2 * p + 1]

        def query(p, l, r, index):
            if l == r:
                return a[l]
            mid = (l+r)//2
            if index <= mid:
                return query(2*p, l, mid, index)
            else:
                return query(2*p+1, mid+1, r, index)

        s = sum(nums2)
        ans = []
        for (type, l, r) in queries:
            if type == 1:
                update1(1, 0, n-1, l, r)
                print("--", type, l, r)
                print(a)
            elif type == 2:
                print(s, a)
                p = l
                s += a[1] * p #* query(1, 0, n-1, p)
            else:
                ans.append(s)
        print(a)
        return ans

if __name__ == '__main__':
    s = Solution()
    # print(s.handleQuery([1,0,1],[0,0,0], [[1,1,1],[2,1,0],[3,0,0]]))
    # print(s.handleQuery([1],[5], [[2,0,0],[3,0,0]]))
    print(s.handleQuery([1,0,1],[0,0,0], [[1,0,1],[1,1,2],[2,1,0],[3,0,0]]))
