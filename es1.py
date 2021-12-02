import math


def lds(arr):
    if len(arr) < 1:
        return []
    DP = [[(0, math.inf) for i in range(j+1)] for j in range(len(arr))]
    for j in range(len(arr)):
        for i in range(j, -1, -1):
            if i == j:
                DP[j][i] = arr[i], arr[i]
            else:
                par_max = 0
                ind_max = i
                for k in range(i, j):
                    if DP[k][i][1] >= arr[j]:
                        cur = DP[k][i][0] + arr[j]
                    else:
                        cur = DP[k][i][0]
                    if cur > par_max:
                        par_max = cur
                        ind_max = k

                if DP[j][i+1][0] > par_max:
                    DP[j][i] = DP[j][i+1]
                else:
                    par_sum, last = DP[ind_max][i]
                    if last >= arr[j]:
                        DP[j][i] = par_sum + arr[j], arr[j]
                    else:
                        DP[j][i] = DP[j-1][i]

    for r in DP:
        print(r)

    return solution(DP, arr)


def solution(DP, arr):
    j = len(arr) - 1
    i = 0
    sol = [DP[j][i][1]]

    while i < j and j >= 0:
        if DP[j][i][0] == DP[j][i+1][0]:
            i += 1
        else:
            target = DP[j][i][0] - DP[j][i][1]
            while i < j:
                if DP[j][i][0] != target:
                    j-=1
                else:
                    sol.append(DP[j][i][1])
                    break
        
    sol.append(DP[j][i][1])
    return list(reversed(sol))


res = lds([4, 4, 3, 7, 5])

print(res)
