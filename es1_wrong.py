import math


def lds(arr): # TODO: Fixa con un solo elemento negativo; Fixa con molti negativi
    if len(arr) < 1:
        return []
    DP = [[(0, math.inf) for i in range(j+1)] for j in range(len(arr))]
    for j in range(len(arr)):
        for i in range(j, -1, -1):
            if i == j:
                DP[j][i] = arr[i], arr[i]
            else:
                col_max = 0, math.inf
                for k in range(i, j):
                    if DP[k][i][1] >= arr[j]:
                        cur = DP[k][i][0] + arr[j], arr[j]
                    else:
                        cur = DP[k][i]
                    if cur[0] > col_max[0]:
                        col_max = cur

                if DP[j][i+1][0] > col_max[0]:
                    DP[j][i] = DP[j][i+1]
                else:
                    DP[j][i] = col_max

    return solution(DP, arr)


def solution(DP, arr):
    j = len(arr) - 1
    i = 0
    sol = [DP[j][i][1]]

    while i < j and j >= 0:
        if DP[j][i] == DP[j][i+1]:
            i += 1
        else:
            target = DP[j][i][0] - DP[j][i][1]
            while i < j:
                j -= 1
                if DP[j][i][0] == target:
                    sol.append(DP[j][i][1])
                    break

    return list(reversed(sol))
