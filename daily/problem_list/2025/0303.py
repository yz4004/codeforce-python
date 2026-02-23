T = int(input())
for _ in range(T):
    n = int(input())
    a = list(map(int, input().split()))

    # ai & aj >= ai ^ aj
    # 当遍历到ai 时，前面所有 a1-ai-1 的比特位
    m = max(a)
    cnt = [0]*(m.bit_length() + 1)
    res = 0
    for x in a:
        h = x.bit_length()
        # 如果前面的数在h为0. 则一定不满足 ai & aj >= ai ^ aj
        # 如果前面的数在h为1，且ai高于h的位没有1，则满足 ai & aj >= ai ^ aj
        res += cnt[h]
        cnt[h] += 1
    print(res)
